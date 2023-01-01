from thefuzz import fuzz, process


class Matcher:
    def __init__(self) -> None:
        pass

    def insert_synonyms(self,):

        if self.simi_score(token1, token2) > 75:
            # .insert(0, )
            # .append()
        else:
            
    
    def simi_score(self, word1:str, word2:str) -> int:
        return fuzz.ratio(word1, word2)
    
    def simi_word_from_list(self, word:str, word_list:list) -> str:
        # match one word from a list of words
        best_match = process.extractOne(word, word_list)
        # extract the score of best match
        if best_match[1] > 75:
            return best_match[0]
        else:
            return ""
    
    def match_rules(self, string: str):
