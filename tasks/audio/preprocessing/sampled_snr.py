from scipy.stats import norm
import scipy.signal as sig
from scipy.io import wavfile
import copy
import os
import random

from pydub import AudioSegment
import numpy as np
from typing import List

class SampledSNR:
    def __init__(self, referenced_audio_path: str, noisy_audio_path: str, sample_duration: float=3600, sampling_rate: int=16000) -> None:
        '''
            referenced_audio_path: the path of the audio file that is being the reference for the noisy audio
            noisy_audio_path: the path of the audio file which is to be compared with the reference audio
            sample_duration: the targeted duration of the audio that is being compared in seconds
            sampling_rate: the sampling rate of the audio
        '''
        self.referenced_audio_path = referenced_audio_path
        self.noisy_audio_path = noisy_audio_path
        self.sample_duration = sample_duration
        self.sampling_rate = sampling_rate

    def slice_audio(self, audio_path):
        '''
            slice the audio accurately based on the sampling rate of the audio in the array

            audio_path: the path of the audio that is to be sliced to the target duration
        '''

        # get the audio
        sound = AudioSegment.from_wav(audio_path)

        # convert it into array format
        sample = sound.get_array_of_samples()

        # get the targeted audio length of the audio by slicing it
        sample_sliced = sample[:self.sampling_rate*self.sample_duration]

        # return the array of the sound in numpy format
        return np.array(sample_sliced)

    def signalPower(self, x) -> float:
        '''
            compute the signal power

            x: signal array
        '''
        return np.average(x**2)

    def SNRsystem(self, inputSig, outputSig) -> float:
        '''
            to compute the SNR between the 2 audio
            
            inputSig: reference audio signal
            outputSig: the audio signal that is being compared to the reference audio

        '''
        # treat the difference in the signal power as the noise
        noise = outputSig-inputSig
        powS = self.signalPower(outputSig)
        powN = self.signalPower(noise)
        
        # print(f'noisy: {powS} | reference: {powN}')
        # print((powS-powN)/powN)
        # print(np.abs((powS-powN)/powN))

        return 10*np.log10(np.abs((powS-powN)/powN))

    def sampled_SNR(self):
        '''
            retrieve the sampled SNR
        '''

        # get the sliced audio
        referenced_audio = self.slice_audio(self.referenced_audio_path)
        noisy_audio = self.slice_audio(self.noisy_audio_path)

        return self.SNRsystem(referenced_audio, noisy_audio)

    def __call__(self):
        return self.sampled_SNR()

if __name__ == '__main__':
    
    base_path = '/preproc/batched_1_hr_audio'
    ref_name = 'CH10_batch_'
    noisy_name = 'CH73_batch_'

    for num_ref in range(10):
        for num_noisy in range(1):
            snr = SampledSNR(referenced_audio_path=f'{base_path}/{ref_name}{num_ref}.wav', 
                            noisy_audio_path=f'{base_path}/{noisy_name}{num_noisy}.wav', 
                            sample_duration=3600, 
                            sampling_rate=16000)

            print(f'ref: {ref_name}{num_ref} and noisy: {noisy_name}{num_noisy} -> SNR: {snr()}')
            print()