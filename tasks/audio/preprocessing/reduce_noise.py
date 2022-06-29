from scipy.io import wavfile
import noisereduce as nr
import numpy as np

class ReduceNoise:
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

        data = np.mean(data, axis=1, dtype=data.dtype)

        # perform noise reduction
        reduced_noise = nr.reduce_noise(y=data, sr=rate)

        # export the noise reduced audio file
        wavfile.write(self.output_audio_path, rate, reduced_noise)

    def __call__(self):
        return self.reduce_noise()

if __name__ == '__main__':
    reduce_noise_audio = ReduceNoise(input_audio_path='/preproc/batched_1_hr_audio/CH10_batch_0.wav', 
                                     output_audio_path='/preproc/batched_1_hr_audio/CH10_batch_0_reduce_noise.wav')

    reduce_noise_audio()