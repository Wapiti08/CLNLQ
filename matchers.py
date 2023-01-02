from thefuzz import fuzz, process
from tqdm import tqdm

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
    
    def match_rules(self, token_dict: dict):
        ''' define rule-based assumptions from NLQ token type to SQL Slot
        
        '''
        # create SQL Slot key
        token_dict["SQL Slot"] = []
        for i, _ in tqdm(enumerate(token_dict['Token']), desc="matching tokens to SQL slot"):
            if token_dict["Token Type"][i] == "Proper Noun":
                token_dict["SQL Slot"][i] = "WHERE condition"
            elif token_dict["Token Type"][i] in ["Adjective, Adverb, Gerund"]:
                token_dict["SQL Slot"][i] = "SELECT or WHERE clause"
            elif token_dict["Token Type"][i] == "Number":
                token_dict["SQL Slot"][i] = "WHERE condition"
            elif token_dict["Token Type"][i] == "Common Noun":
                token_dict["SQL Slot"][i] = "SELECT/FROM selection operator clause"
            elif token_dict["Token Type"][i] == "Comparative Expression":
                token_dict["SQL Slot"][i] = "MAX, MIN, AVG, etc, clauses or with WHERE clause"
            elif token_dict["Token Type"][i] == "Verb":
                token_dict["SQL Slot"][i] = "WHERE condition, JOIN, AS, or IN"
            elif token_dict["Token Type"][i] == "Conjunction":
                token_dict["SQL Slot"][i] = "WHERE condition AND, OR, etc"
            else:
                token_dict["SQL Slot"][i] = "N/A"
    
    def sql_tag(self,):
        pass
             
