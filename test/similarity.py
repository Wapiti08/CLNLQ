import spacy

nlp = spacy.load("en_core_web_sm")

word1="password"
word2="passwd"

doc1 = nlp(word1)
doc2 = nlp(word2)

print(doc1.similarity(doc2))
print(type(doc2))
import nltk
print(nltk.edit_distance(word1, word2))

from fuzzywuzzy import fuzz, process

print(fuzz.ratio(word1, word2))
print(fuzz.ratio("test","test"))


word_list = ["pwd","passwd","paswd"]
best_match = process.extractOne(word1, word_list)
print(best_match)
print(best_match[1])
