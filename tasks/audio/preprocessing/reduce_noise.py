from scipy.io import wavfile
import noisereduce as nr
import numpy as np

class ReduceNoise:
    def __init__(self, input_audio_path: str, output_audio_path: str) -> None:
        '''
            input_audio_path: audio path that is to be preprocessed (to be noise reduced)
            output_audio_path: audio path of the noise reduced audio
        '''
        self.input_audio_path =input_audio_path
        self.output_audio_path = output_audio_path

    def reduce_noise(self) -> None:
        


# load data
rate, data = wavfile.read("test.wav")

data = np.mean(data, axis=1, dtype=data.dtype)

# perform noise reduction
reduced_noise = nr.reduce_noise(y=data, sr=rate)
wavfile.write("test_reduce.wav", rate, reduced_noise)