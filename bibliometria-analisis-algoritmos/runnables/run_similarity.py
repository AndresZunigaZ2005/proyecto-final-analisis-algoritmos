import os
import sys

# Agregar el directorio raíz del proyecto al sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pandas as pd
from src.similarity.ai_models import load_sentence_model
from src.similarity.vector_models import compute_embeddings
from src.similarity.compare import compute_similarity

# Rutas correctas desde la raíz del proyecto
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DATA_DIR = os.path.join(BASE_DIR, "data")
INPUT_FILE = os.path.join(DATA_DIR, "unified.csv")
OUTPUT_FILE = os.path.join(DATA_DIR, "similarities.csv")


# ---------- Cargar datos ----------
df = pd.read_csv(INPUT_FILE)
if "abstract" not in df.columns:
    raise ValueError("El archivo unified.csv no contiene la columna 'abstract'.")

df["abstract"] = df["abstract"].astype(str)
df = df[df["abstract"].str.strip() != ""]
print(f"📄 Abstracts cargados: {len(df)}")

# ---------- Modelo y embeddings ----------
model = load_sentence_model()
embeddings = compute_embeddings(model, df["abstract"].tolist())

# ---------- Comparación ----------
sim_df = compute_similarity(df, embeddings, threshold=0.75)

# ---------- Guardar resultados ----------
OUTPUT_PATH = os.path.join(DATA_DIR, "similarities.csv")
sim_df.to_csv(OUTPUT_PATH, index=False, encoding="utf-8")
print(f"✅ Resultados guardados en {OUTPUT_PATH}")
print(f"🔗 Pares similares encontrados: {len(sim_df)}")
