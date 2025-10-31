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
DATA_DIR = os.path.join(BASE_DIR, "data/download")
INPUT_FILE = os.path.join(DATA_DIR, "unified.csv")
OUTPUT_PATH = os.path.join(BASE_DIR, "data/similarity/similarities.csv")

# Crear directorios si no existen
os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)

print("🔍 Requerimiento 2 - Análisis de similitud semántica")
print(f"📂 Leyendo archivo: {INPUT_FILE}")

# ---------- Cargar datos ----------
if not os.path.exists(INPUT_FILE):
    raise FileNotFoundError(f"No se encontró el archivo: {INPUT_FILE}\n"
                          f"Asegúrate de ejecutar primero run_downloader.py")

df = pd.read_csv(INPUT_FILE)

if "abstract" not in df.columns:
    raise ValueError("El archivo unified.csv no contiene la columna 'abstract'.")

# Filtrar abstracts válidos
df["abstract"] = df["abstract"].astype(str)
original_count = len(df)
df = df[df["abstract"].str.strip() != ""]
filtered_count = len(df)

print(f"📄 Abstracts totales: {original_count}")
print(f"📄 Abstracts válidos (no vacíos): {filtered_count}")
if original_count - filtered_count > 0:
    print(f"⚠️  Se filtraron {original_count - filtered_count} abstracts vacíos")

if len(df) == 0:
    raise ValueError("No hay abstracts válidos para procesar.")

# ---------- Modelo y embeddings ----------
print("\n🤖 Cargando modelo de embeddings...")
model = load_sentence_model()

print("🧮 Generando embeddings de abstracts...")
embeddings = compute_embeddings(model, df["abstract"].tolist())
print(f"✅ Embeddings generados: {embeddings.shape}")

# ---------- Comparación ----------
print("\n🔗 Calculando similitudes entre artículos...")
sim_df = compute_similarity(df, embeddings, threshold=0.75)

# ---------- Guardar resultados ----------
print(f"\n💾 Guardando resultados en: {OUTPUT_PATH}")
sim_df.to_csv(OUTPUT_PATH, index=False, encoding="utf-8")

print(f"\n✅ Proceso completado exitosamente!")
print(f"📊 Pares similares encontrados (threshold ≥ 0.75): {len(sim_df)}")
print(f"📁 Archivo generado: {OUTPUT_PATH}")

# Mostrar muestra de resultados si hay datos
if len(sim_df) > 0:
    print("\n🔍 Muestra de resultados (top 5 similitudes):")
    print(sim_df.head().to_string(index=False))
else:
    print("\n⚠️  No se encontraron pares de artículos similares con el threshold actual (0.75)")
    print("   Considera reducir el threshold en src/similarity/compare.py")