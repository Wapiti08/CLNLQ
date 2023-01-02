import spacy

nlp = spacy.load("en_core_web_sm")

doc = nlp("I love coffee most, coffee is equal to tea")
print(doc.vocab)
print(doc.vocab.strings["love"])
print(type(doc.vocab))
for token in doc:
    print(type(token))
    print("The pos of ",token, " is ", token.pos_)
    

assert doc.vocab.strings["coffee"] == 3197928453018144401
assert doc.vocab.strings[3197928453018144401] == "coffee"
