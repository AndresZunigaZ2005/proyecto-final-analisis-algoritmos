import re
import numpy as np
import pandas as pd
import spacy

nlp = None
def ensure_spacy():
    global nlp
    if nlp is None:
        try:
            nlp = spacy.load("en_core_web_sm")
        except:
            import spacy
            spacy.cli.download("en_core_web_sm")
            nlp = spacy.load("en_core_web_sm")

def clean_text(text):
    if not isinstance(text, str):
        return ""
    text = text.lower()
    text = re.sub(r'\s+', ' ', text)
    text = re.sub(r'[^a-z0-9\s]', ' ', text)
    return text.strip()

def preprocess_series(series, do_lemmatize=False):
    texts = series.fillna("").astype(str).apply(clean_text).tolist()
    if do_lemmatize:
        ensure_spacy()
        lemmas = []
        for doc in nlp.pipe(texts, disable=["parser","ner"]):
            lemmas.append(" ".join([t.lemma_ for t in doc if not t.is_stop and t.is_alpha]))
        return lemmas
    return texts
