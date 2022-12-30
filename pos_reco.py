'''
Cover the pos recognition and disambiguation

'''

from tqdm import tqdm
from sklearn.pipeline import Pipeline
from spacy import tokenizer
from autocorrect import Speller
import speech_recognition as sr
from string import punctuation
from spacy_langdetect import LanguageDetector
import contextualSpellCheck
import spacy 
import pickle
from spacy_wordnet.wordnet_annotator import WordnetAnnotator
from CLNLQ import helper
import nltk
from nltk.corpus import stopwords
import yaml
from pathlib import Path

class PosRecognizer:

    def __init__(self, lan:str, token_id_path:str, config_file:str):
        if lan not in ["en","zh"]:
            print("Please input the supported language code: en or zh")
            return
        self.nlp = spacy.load(f"{lan}_core_web_sm")
        self.nlp.add_pipe("spacy_wordnet", after="tagger")
        self.token_id_path = token_id_path
        self.config_file = config_file

    def word_annotate(self, word:str, domains:list):
        '''
        :param word:
        :param domain:
        '''
        token = self.nlp(word)[0]
        # find all the synsets under domains
        synsets = token._.wordnet.wordnet_synsets_for_domain(domains)
        return [lemma for s in synsets for lemma in s.lemma_names()]

    def type_check(self,):
        pass
 
    ## method 1
    # def spell_check(string_list):
    #     spell = Speller(lang='en')
    #     for token in string_list:
    #         cor_token = spell(token)
    
    ## method 2 ---- get suggested spellcheck only avoid for loop
    def spell_check(self, input_string:str) -> str:
        contextualSpellCheck.add_to_pipe(self.nlp)
        doc = self.nlp(input_string)

        # print(len(doc._.suggestions_spellCheck)) # => Number of errors: 3
        # print(doc._.suggestions_spellCheck)      # => {neww: 'new', firsrt: 'best', neme: 'name'}

        # return string type of corrected input
        return doc._.outcome_spellCheck

    def tokenize_words(self, input_string):
        # check spelling, default English
        # not necessary for Chinese
        corr_string = self.spell_check(input_string)
        doc = self.nlp(corr_string)
        # tokenize to NLQ semantic roles
        for token in tqdm(doc, desc="traversing the tokens"):


    def store_token_ids(self, token_ids:dict):

        if not helper.file_path_check(self.token_id_path):
            # write to a file directly
            with Path(self.token_id_path).open("wb") as fw:
                pickle.dump(dict, fw)
        else:
            # update new token_ids
            self.update_token_ids(token_ids)

        # give Ids to each token --- inside doc.vocab

    # apply asyio here to speed up I/O write
    def update_token_ids(self, new_token_ids:dict):
        token_id_dict = self.read_token_ids()
        # no repetition check --- hash is update key
        token_id_dict.update(new_token_ids)

        # write to file
        with Path(self.token_id_path).open("wb") as fw:
            pickle.dump(token_id_dict, fw)


    def read_token_ids(self,):
        with Path(self.token_id_path).open("rb") as fr:
            token_id_dict = pickle.load(fr)

        return token_id_dict

            

    def max_length(self,):
        ''' remove tokens from attributes list if existed in values list
        
        '''
        




    def token_label(self, ):
        ''' match token to Table, Value, Attribute and Relationships
        according to linguistic categories and semantic roles
        Table: Common Noun
        Value: Proper Noun, Literal Value
        Conditional Values：Comparative Experssion, Comparative Operation
        Relationship: Verb
        Attribute: Common Noun, Adjective, Adv
        '''
    

    
    def escape_words(self, token_list:list):
        filter_tokens = []
        
        # Method 1
        ## built-in stopwords in spacy --- maybe filter some numeric or conditional words
        for token in token_list:
            if token not in stopwords:
                filter_tokens.append(token)

        # Method 2
        ## predefined words --- more accurate but less general
        config = yaml.safe_load(self.config_file)
        escape_words = config["FilterWords"]
        for token in token_list:
            if token not in escape_words:
                filter_tokens.append(token)