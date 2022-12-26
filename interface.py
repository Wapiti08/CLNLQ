escape_words = []

from tqdm import tqdm

def input_pro(text:str) -> list:
    return text.strip().splitlines()

def del_escape_words(token_list: list) -> list:
    pass