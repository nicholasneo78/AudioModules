from scipy.stats import norm
import scipy.signal as sig
from scipy.io import wavfile
import copy
import os
import random

from pydub import AudioSegment
from tqdm import tqdm
import numpy as np
from typing import List

class ExportMergedAudio:
    def __init__(self, root_dir: str, target_channel: str, audio_split_size: int, num_batches: int, audio_duration_per_split: float, export_dirname: str, export_wav_filename: str, export_wav_format: str='.wav') -> None:
        '''
            root_dir: the root directory for which the audio filepath of the stated channel is present
            target_channel: the comms channel of interest
            audio_split_size: how many audio filepath in a batch
            num_batches: number of batches of audio required to be exported
            audio_duration_per_split: the ideal duration (in seconds) of the merged batched audio that is to be exported
            export_dirname: the directory where the batched audio files will be located
            export_wav_filename: filename of the batched wav file
            export_wav_format: audio format of the merged batched audio file
        '''

        self.root_dir = root_dir
        self.target_channel = target_channel
        self.audio_split_size = audio_split_size
        self.num_batches = num_batches
        self.audio_duration_per_split = audio_duration_per_split
        self.export_dirname = export_dirname
        self.export_wav_filename = export_wav_filename
        self.export_wav_format = export_wav_format

    def create_new_dir(self, directory: str) -> None:
        '''
            creates new directory and ignore already created ones

            directory: the directory path that is being created
        '''
        try:
            os.mkdir(directory)
        except OSError as error:
            pass # directory already exists!

    def batch_audio_filepath(self) -> List[List[str]]:
        '''
            to get all the audio filepath of a specific channel, then batch them based on the number of batches and the number of audio filepath in each batch
        '''
        # get the subdir of the root folder
        subdir = os.listdir(self.root_dir)

        # get the overall CH x list with all the filepaths from batch y
        wavfile_list = []

        # get all the audio files from channel x that are from batch y
        for sub in subdir:
            subroot_dir = f'{self.root_dir}/{sub}/{self.target_channel}/'
            wavfile_list_one_date = [subroot_dir+s for s in os.listdir(f'{subroot_dir}') if s.endswith(self.export_wav_format)]
            wavfile_list.extend(wavfile_list_one_date)

        # shuffle the audio filepath lists
        random.shuffle(wavfile_list)

        ## split into batches of 2.5k audio -> 10 batches
        wavfile_batch_list = []
        for batch_num in range(self.num_batches):
            wavfile_batch = wavfile_list[batch_num*self.audio_split_size: (batch_num+1)*self.audio_split_size]
            wavfile_batch_list.append(wavfile_batch)

        return wavfile_batch_list

    def export_batched_audio(self) -> None:
        '''
            to concatenate the audio files together from the same batch
        '''

        # get the wavfile_batch_list
        wavfile_batch_list = self.batch_audio_filepath()
        for batch in range(self.num_batches):
            for idx, audio in tqdm(enumerate(wavfile_batch_list[batch])):
                if idx == 0:
                    sound = AudioSegment.from_wav(audio)
                else:
                    sound += AudioSegment.from_wav(audio)
                
                # create a new directory to store all the merged audio samples of the stated duration
                self.create_new_dir(self.export_dirname)

                # if over the specific number of seconds, break it, as the limit is hit
                if sound.duration_seconds > self.audio_duration_per_split:       
                    sound.export(f'{self.export_dirname}/{self.export_wav_filename}_{batch}.{self.export_wav_format}', format=self.export_wav_format)         
                    break

    def __call__(self):
        return self.export_batched_audio()

if __name__ == '__main__':
    export_audio = ExportMergedAudio(root_dir='/preproc/datasets_silence_removed/mms_batch_1',
                                     target_channel='CH 14', 
                                     audio_split_size=1500, 
                                     num_batches=10, 
                                     audio_duration_per_split=1*60*60, 
                                     export_dirname='/preproc/batched_1_hr_audio', 
                                     export_wav_filename='CH14_batch', 
                                     export_wav_format='wav')

    export_audio()