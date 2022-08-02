import librosa
import soundfile as sf
from audiomentations import Compose, AddGaussianNoise, PitchShift, HighPassFilter, LowPassFilter, BandPassFilter

augment = Compose([
    #AddGaussianNoise(min_amplitude=0.001, max_amplitude=0.001, p=1),
    BandPassFilter(min_center_freq=20.0, max_center_freq=3000.0, p=1)
])

if __name__ == "__main__":
    signal, sr = librosa.load("/preproc/datasets/example_libri/input_1.wav", sr=16000)
    print(sr)
    augmented_signal = augment(signal, sr)
    sf.write("/preproc/datasets/example_libri/output_1d.wav", augmented_signal, sr)