import math
import textdistance
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd

def levenshtein_similarity(text1: str, text2: str) -> float:
    dist = textdistance.levenshtein.distance(text1, text2)
    max_len = max(len(text1), len(text2))
    if max_len == 0:
        return 1.0
    return 1 - dist / max_len

def jaccard_similarity(text1: str, text2: str) -> float:
    set1 = set(text1.lower().split())
    set2 = set(text2.lower().split())
    if not set1 or not set2:
        return 0.0
    return len(set1 & set2) / len(set1 | set2)

def cosine_tfidf_similarity(text1: str, text2: str) -> float:
    vectorizer = TfidfVectorizer(stop_words='english')
    tfidf = vectorizer.fit_transform([text1, text2])
    sim = cosine_similarity(tfidf[0:1], tfidf[1:2])
    return float(sim[0][0])

def spacy_embedding_similarity(text1: str, text2: str) -> float:
    import spacy
    nlp = spacy.load("en_core_web_md")
    doc1 = nlp(text1)
    doc2 = nlp(text2)
    return doc1.similarity(doc2)


def tfidf_similarity(texts, titles, threshold=0.75):
    """Calcula similitud usando TF-IDF + Coseno."""
    tfidf = TfidfVectorizer(stop_words="english").fit_transform(texts)
    sim_matrix = cosine_similarity(tfidf)
    pairs = []
    for i in range(len(titles)):
        for j in range(i + 1, len(titles)):
            if sim_matrix[i][j] > threshold:
                pairs.append({
                    "articulo_1": titles[i],
                    "articulo_2": titles[j],
                    "similaridad": round(sim_matrix[i][j], 3)
                })
    return pd.DataFrame(pairs)

