from scipy.io import wavfile
import noisereduce as nr
import numpy as np
import pydub

class ReduceNoise:
    '''
        main class to reduce noise of an audio file
    '''

    def __init__(self, input_audio_path: str, output_audio_path: str) -> None:
        '''
            input_audio_path: audio path that is to be preprocessed (to be noise reduced)
            output_audio_path: audio path of the noise reduced audio
        '''
        self.input_audio_path = input_audio_path
        self.output_audio_path = output_audio_path

    def reduce_noise(self) -> None:
        '''
            main method to reduce noise of the audio
        '''

        # load data
        rate, data = wavfile.read(self.input_audio_path)

        # data = np.mean(data, axis=1, dtype=data.dtype)

        # perform noise reduction
        reduced_noise = nr.reduce_noise(y=data, sr=rate)

        # export the noise reduced audio file
        wavfile.write(self.output_audio_path, rate, reduced_noise)

    def __call__(self):
        return self.reduce_noise()

class IncreaseVolume:
    '''
        main class to increase the volume of the audio by a specified amount (in terms dB)
    '''

    def __init__(self, input_audio_path: str, output_audio_path: str, amplification: int) -> None:
        '''
            input_audio_path: audio path that is to be preprocessed (to be amplified)
            output_audio_path: audio path of the amplified audio
            amplification: amount of amplification (in dB)
        '''
        self.input_audio_path = input_audio_path
        self.output_audio_path = output_audio_path
        self.amplification = amplification

    def increase_volume(self) -> None:
        '''
            main method to increase the volume of the audio in dB
        '''
        wav_file =  pydub.AudioSegment.from_wav(file=self.input_audio_path) 

        # increase the volume of the audio (by dB)
        wav_file += self.amplification

        # export the wavfile
        wav_file.export(self.output_audio_path, format='wav')

    def __call__(self):
        return self.increase_volume()


if __name__ == '__main__':
    # reduce_noise_audio = ReduceNoise(input_audio_path='/preproc/batched_1_hr_audio/CH10_batch_0.wav', 
    #                                  output_audio_path='/preproc/batched_1_hr_audio/CH10_batch_0_nr.wav')

    # test audio
    INPUT_AUDIO_FILEPATH = '/preproc/ch16_test.wav'
    INTERMEDIATE_AUDIO_FILEPATH = '/preproc/ch16_test_nr.wav'
    OUTPUT_AUDIO_FILEPATH = '/preproc/ch16_test_nr_amp.wav'
    AMPLIFICATION = 15

    # reduce noise -> increase volume method
    reduce_noise_audio = ReduceNoise(input_audio_path=INPUT_AUDIO_FILEPATH, 
                                     output_audio_path=INTERMEDIATE_AUDIO_FILEPATH)

    reduce_noise_audio()

    increase_volume_audio = IncreaseVolume(input_audio_path=INTERMEDIATE_AUDIO_FILEPATH, 
                                           output_audio_path=OUTPUT_AUDIO_FILEPATH, 
                                           amplification=15)

    increase_volume_audio()