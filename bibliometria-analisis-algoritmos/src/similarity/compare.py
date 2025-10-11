import pandas as pd
from sentence_transformers import util
from src.similarity.classical import (
    levenshtein_similarity,
    jaccard_similarity,
    cosine_tfidf_similarity,
    spacy_embedding_similarity
)
from src.similarity.ai_models import (
    sbert_similarity,
    transformer_embedding_similarity
)

def comparar_abstracts(csv_path="data/unified.csv", titulo1=None, titulo2=None):
    df = pd.read_csv(csv_path)
    if titulo1 not in df["title"].values or titulo2 not in df["title"].values:
        raise ValueError("Los títulos no existen en el CSV")

    t1 = df.loc[df["title"] == titulo1, "abstract"].values[0]
    t2 = df.loc[df["title"] == titulo2, "abstract"].values[0]

    print(f"\n🧾 Comparando abstracts:\n1️⃣ {titulo1}\n2️⃣ {titulo2}\n")

    resultados = {
        "Levenshtein": levenshtein_similarity(t1, t2),
        "Jaccard": jaccard_similarity(t1, t2),
        "Cosine TF-IDF": cosine_tfidf_similarity(t1, t2),
        "SpaCy Embeddings": spacy_embedding_similarity(t1, t2),
        "SBERT": sbert_similarity(t1, t2),
        "Transformer Alt": transformer_embedding_similarity(t1, t2)
    }

    print("📊 Resultados de similitud (0 = sin similitud, 1 = idéntico):\n")
    for k, v in resultados.items():
        print(f"{k:<20}: {v:.4f}")
    return resultados


def compute_similarity(df, embeddings, threshold=0.75):
    """Compara embeddings y devuelve pares con alta similitud."""
    cosine_scores = util.cos_sim(embeddings, embeddings)
    pairs = []
    for i in range(len(df)):
        for j in range(i + 1, len(df)):
            score = cosine_scores[i][j].item()
            if score > threshold:
                pairs.append({
                    "articulo_1": df.iloc[i]["title"],
                    "articulo_2": df.iloc[j]["title"],
                    "similaridad": round(score, 3)
                })
    return pd.DataFrame(pairs)
