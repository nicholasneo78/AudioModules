import pydub
import numpy as np
sound_file = pydub.AudioSegment.from_wav("/preproc/datasets/mms/mms/mms_batch_1/mms_20220417/CH 73/0000001437_CHDIR_154_2022-04-17_23_59_24.wav")
sound_file_Value = np.array(sound_file.get_array_of_samples())
# milliseconds in the sound track
ranges = [(int(0.0801*16000),int(1.122*16000)),(int(1.323*16000),int(2.766*16000))] 
for x, y in ranges:
    new_file=sound_file_Value[x : y]
    song = pydub.AudioSegment(new_file.tobytes(), frame_rate=sound_file.frame_rate, sample_width=sound_file.sample_width,channels=1)
    song.export(str(x) + "-" + str(y) +".wav", format= "wav")