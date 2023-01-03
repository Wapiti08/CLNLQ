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

    def word_annotate(self, word:str, domains:list) -> list:
        '''
        :param word:
        :param domain:
        '''
        token = self.nlp(word)[0]
        # find all the synsets under domains
        synsets = token._.wordnet.wordnet_synsets_for_domain(domains)
        return [lemma for s in synsets for lemma in s.lemma_names()]
 
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
        ''' tokenize string to tokens with preprocessing

        '''
        # check spelling, default English
        # not necessary for Chinese
        corr_string = self.spell_check(input_string)
        return self.nlp(corr_string)

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

    def max_length(self, att_list:list, val_list:list) -> list:
        ''' remove tokens from attributes list if existed in values list
        
        '''
        # return the intersection of two lists
        com_tokens = list(set(att_list) & set(val_list))
        return list(filter(lambda a: a not in com_tokens, att_list))


    def token_type(self, token_list: list(spacy.tokens.token.Token)) -> dict:
        ''' define token types based on rules (from tag)
        :param token_list: the list of tokens that have been removed with stopwords and corrected
        type (POS Tags)                              tag                           SQL
        noun_phrase(NN)                             ---- noun_phrase              ----  table, attribute
        string()/number(CD)                         ---- literal_value            ----  value
        proper_noun(PROPN)                          ---- proper_noun              ----  value
        literal_value                               ---- literal value            ----  value
        verb(verb)                                  ---- verb                     ----  relationship  
        adverb(adv)                                 ---- adverb                   ----  attribute   
        adjective(adj)                              ---- adjective                ----  attribute
        preposition(IN)                             ---- preposition 
        wh_question                                 wh_question                   reference
        conjunction_phrase(CONJ)                    ---- disjunction_phrase       ---- condition
        comparative_expression(JJR/RBR/KOKOM/cm)    ---- comparative_experssion   ---- condition
        operational_expression()                    ---- operational_expression   ---- condition

        '''
        # create a list to save rule-based assumptions
        token_type_dict = {"Token":[],
                            "Token Type":[],
                            "Category":[],
                            # save synonyms here to avoid loop again
                            # "Synonyms":[]
                            }

        for token in tqdm(token_list, desc="traversing the tokens to generate NLQ MetaTable"):
            # add token itself lemma
            token_type_dict['Token'].append(token.lemma_)

            if token.pos_ == "NN":
                token_type_dict["Token Type"].append("Common Noun")
                token_type_dict["Category"].append(["Table","Attribute"])
                # token_type_dict["Synonyms"].append()
            elif token.pos_ == "CD":
                token_type_dict["Token Type"].append("Number")
                token_type_dict["Category"].append("Value")
            elif token.pos_ == "PROPN":
                token_type_dict["Token Type"].append("Proper Noun")
                token_type_dict["Category"].append("Value")
            elif token.pos_ == "verb":
                token_type_dict["Token Type"].append("Verb")
                token_type_dict["Category"].append("Relationship")
            elif token.pos_ == "adv":
                token_type_dict["Token Type"].append("Adverb")
                token_type_dict["Category"].append("Attribute")
            elif token.pos_ == "adj":
                token_type_dict["Token Type"].append("Adjective")
                token_type_dict["Category"].append("Attribute")
            elif token.pos_ == "VBG":
                token_type_dict["Token Type"].append("Gerund")
                token_type_dict["Category"].append("Attribute")
            elif token.pos_ == "IN":
                token_type_dict["Token Type"].append("Prepositions")
                token_type_dict["Category"].append("N/A")
            elif token.pos_ == "CONJ":
                token_type_dict["Token Type"].append("Conjunction")
                token_type_dict["Category"].append("N/A")
            # more test to do on comparative token type
            elif token.pos_ in ["JJR", "RBR", "KOKOM", "cm"]:
                token_type_dict["Token Type"].append("Comparative Expression")
                token_type_dict["Category"].append("Conditional Values")
            else:
                print("Waiting to add the type of token {}".format(token))
                # in order to make sure the length of key is the same
                token_type_dict["Token Type"].append("N/A")
                token_type_dict["Category"].append("N/A")
    
        return token_type_dict

    
    def escape_words(self, token_list:list) -> list:
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