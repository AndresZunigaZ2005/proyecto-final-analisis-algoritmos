import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pandas as pd
from src.clustering.preprocess import preprocess_series
from src.clustering.hierarchical import run_linkage_and_dendrogram
from src.similarity.ai_models import load_sentence_model
from src.similarity.vector_models import compute_embeddings

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")
df = pd.read_csv(os.path.join(DATA_DIR, "unified.csv"))
# seleccionar artículos: pedir al usuario o usar todos
print("Se cargaron", len(df), "artículos")
subset = df  # o filtrar por índice / selección

texts = preprocess_series(subset['abstract'], do_lemmatize=False)

# Opción A: embeddings semánticos
model = load_sentence_model()
embs = compute_embeddings(model, texts).cpu().numpy()

labels = subset['title'].fillna('').apply(lambda s: s[:80]).tolist()

# Probar los tres linkage y elegir el mejor por cophenetic
methods = ['single','complete','average']
results = {}
for m in methods:
    out_file = os.path.join(DATA_DIR, f"dendrogram_{m}.png")
    Z, coph = run_linkage_and_dendrogram(embs, labels, method=m, metric='cosine', out_path=out_file)
    results[m] = coph
print("Cophenetic coeffs:", results)
best = max(results, key=results.get)
print("Mejor método:", best)
