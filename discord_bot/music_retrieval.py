import os
import pandas as pd
from rapidfuzz import fuzz, process

MUSIC_DIRECTORY_PATH = os.getenv('MUSIC_FILE_PATH')
list_of_instruments = ['fife', 'drum']

def music_request_retrieval(excel_path, tune_name, instrument):
    df = pd.read_excel(excel_path)

    if instrument not in list_of_instruments:
        raise Exception('Invalid instrument. Please choose from fife or drum.\nWhen requesting a tune, please use the format: !tune <instrument> <tune_name>.')
    
    
