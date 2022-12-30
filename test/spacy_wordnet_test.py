import spacy

from spacy_wordnet.wordnet_annotator import WordnetAnnotator 

# Load an spacy model
nlp = spacy.load('en_core_web_sm')
# Spacy 3.x
nlp.add_pipe("spacy_wordnet", after='tagger')
# Spacy 2.x
# nlp.add_pipe(WordnetAnnotator(nlp, name="spacy_wordnet"), after='tagger')
token = nlp('prices')[0]
# print(token)
# wordnet object link spacy token with nltk wordnet interface by giving acces to
# synsets and lemmas 
# print(token._.wordnet.synsets())
# print(token._.wordnet.lemmas())

# And automatically tags with wordnet domains
# print(token._.wordnet.wordnet_domains())
# print(token._.wordnet.wordnet_synsets_for_domain(["money"]))
synsets = token._.wordnet.wordnet_synsets_for_domain(["money"])
print([lemma for s in synsets for lemma in s.lemma_names()])