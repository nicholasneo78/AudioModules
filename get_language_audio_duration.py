import json
import logging
from tqdm import tqdm

# Setup logging in a nice readable format
logging.basicConfig(level=logging.INFO,
                    format='[%(levelname)5s][%(asctime)s][%(name)s]: %(message)s',
                    datefmt='%H:%M:%S')

class LanguageDuration:
    def __init__(self, annotation_filepath: str, target_language: str) -> None:
        self.annotation_filepath = annotation_filepath
        self.target_language = target_language

    def language_duration(self) -> None:
        
        # initiate the audio duration count for that particular language
        audio_duration = 0

        with open(self.annotation_filepath, mode='r', encoding='utf-8') as f:
            # # reading an entry
            # for _, line in tqdm(enumerate(f.readlines())):
            d = json.load(f)

            for entry in tqdm(d):
                # iterate the number of segments
                for idx_seg, segment in enumerate(entry['language']):
                    if segment == self.target_language:
                        audio_duration += (entry['labels'][idx_seg]['end'] - entry['labels'][idx_seg]['start'])

        logging.getLogger('Total Audio Length').info(f'audio duration for {self.target_language} (s): {audio_duration}')
        logging.getLogger('Total Audio Length').info(f'audio duration for {self.target_language} (min): {audio_duration/60}')

    def __call__(self):
        return self.language_duration()

if __name__ == '__main__':
    
    # english
    l = LanguageDuration(annotation_filepath='mms_20220417.json', 
                         target_language='english')

    l()

    # bahasa
    l = LanguageDuration(annotation_filepath='mms_20220417.json', 
                         target_language='bahasa')

    l()