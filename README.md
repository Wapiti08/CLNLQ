# CLNLQ
NLQ into SQL translation using computational linguistics


## Components:
    - NLQ Input Interface (not included)

    - POS Recognition
    
    - Disambiguation
    
    - Matcher/Mapper

    - SQL template Generator

    - SQL Execution & Result (not included)


## Extension

    - POS Recognition
        - multi-layered translation algorithm framework: NLQ to tokens
            - lemmatize and stem words
            - parsed tokens and POS tags (multi-layered pipeline) 
                - tag an NLQ POS (TextBlob) --- replaced with Spacy
                - tokenizer
                - annotator
                - semantic
                - syntactic (rule-based) parses
                (remove the meaningless escape words -- predefined)
            - generate a parse tree
            - generate a dictionary of tokens' names, syntactic roles and synonyms (NLQ MetaTable)
            - NLQ's subjects, objects, verbs and other linguistic roles are identified

        - tokens to **semantic analyzer**
            - word-type identifier (WordNet)
            - identify conditional or symbolic words and map them with their relative representation from the language ontology

        - compare with RDB MetaTables' contents: keywords in the NLQ sentence