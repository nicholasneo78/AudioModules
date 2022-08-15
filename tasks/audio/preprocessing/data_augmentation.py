import librosa
import soundfile as sf
from audiomentations import Compose, AddGaussianNoise, PitchShift, HighPassFilter, LowPassFilter, BandPassFilter, Gain

augment = Compose([
    #AddGaussianNoise(max_amplitude=0.001, p=1),
    BandPassFilter(min_center_freq=2000.0, max_center_freq=2000.0, min_bandwidth_fraction=1.5, max_bandwidth_fraction=1.5, min_rolloff=12, max_rolloff=12, zero_phase=False, p=1),
    
])

if __name__ == "__main__":

    # no torch implementation
    signal, sr = librosa.load("/preproc/datasets/example_libri/input_1.wav", sr=16000)
    augmented_signal = augment(signal, sr)
    sf.write("/preproc/datasets/example_libri/output_1_band.wav", augmented_signal, sr)