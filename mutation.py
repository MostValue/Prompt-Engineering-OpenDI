import random
import spacy

def replace_pos(string1, string2, POS):

    """
    Replace tokens of specific parts of speech (POS) in string1 with corresponding
    tokens of the same POS from string2.
    
    Parameters:
    - string1 (str): The input string where certain POS will be replaced.
    - string2 (str): The reference string from which POS replacements will be taken.
    - POS (list): A list of POS tags to identify which tokens to replace in string1.

    Returns:
    - str: The modified string with replacements of tokens based on specified POS tags.
    
    Possible POS:
    "ADJ": "adjective",
    "ADP": "adposition",
    "ADV": "adverb",
    "AUX": "auxiliary",
    "CONJ": "conjunction",
    "CCONJ": "coordinating conjunction",
    "DET": "determiner",
    "INTJ": "interjection",
    "NOUN": "noun",
    "NUM": "numeral",
    "PART": "particle",
    "PRON": "pronoun",
    "PROPN": "proper noun",
    "PUNCT": "punctuation",
    "SCONJ": "subordinating conjunction",
    "SYM": "symbol",
    "VERB": "verb".
    """
    nlp = spacy.load("en_core_web_sm")
    doc1 = nlp(string1)
    doc2 = nlp(string2)
    
    new_tokens = []
    
    for token1 in doc1:
        if token1.pos_ in POS:
            #generating a list of all matching tokens
            matching_tokens = [token2.text for token2 in doc2 if token2.pos_ == token1.pos_]
            #use a random token if possible, or else use the same
            if matching_tokens:
                new_token = random.choice(matching_tokens)
            else:
                new_token = token1.text
        else:
            new_token = token1.text
        new_tokens.append(new_token)
    
    # Join the modified tokens to form the final string
    result = ' '.join(new_tokens)
    return result

# Requries LLM

