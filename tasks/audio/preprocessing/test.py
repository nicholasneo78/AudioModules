import os


for root, subdirs, files in os.walk('/preproc/datasets/mms/mms_split_audio_segment/'):
    count = 0
    # print(root)
    # print(subdirs)

    for file in files:
        if file.endswith('.wav'):
            print(f'{root}/{file}')
            count +=1

            if count >= 1:
                print()
                break