import librosa
import soundfile as sf
from audiomentations import Compose, AddGaussianNoise, PitchShift, HighPassFilter, LowPassFilter, BandPassFilter
# import torchaudio
# import torch
# from torch_audiomentations import Compose, BandPassFilter

augment = Compose([
    #AddGaussianNoise(min_amplitude=0.001, max_amplitude=0.001, p=1),
    BandPassFilter(min_center_freq=20.0, max_center_freq=4000.0, min_bandwidth_fraction=0.5, max_bandwidth_fraction=1.99, min_rolloff=12, max_rolloff=24, zero_phase=False, p=1)
])

if __name__ == "__main__":

    # signal, sr = librosa.load("/preproc/datasets/example_libri/input_1.wav", sr=16000)   
    # print(sr)
    # print(signal.shape)
    ## load the audio with torch
    # signal = torch.Tensor(signal)  
    # signal, sr = torchaudio.load('/preproc/datasets/example_libri/input_1.wav', normalize=True)
    # signal = signal.float()
    # signal = signal.unsqueeze(0).unsqueeze(0)
    # print(signal.size())
    # augmented_signal = augment(signal, sr)
    # print(augmented_signal.size())
    # sf.write("/preproc/datasets/example_libri/output_1p.wav", augmented_signal.squeeze(0).squeeze(0), sr)

    # no torch
    signal, sr = librosa.load("/preproc/datasets/example_libri/input_1.wav", sr=16000)
    augmented_signal = augment(signal, sr)
    sf.write("/preproc/datasets/example_libri/output_1d.wav", augmented_signal, sr)