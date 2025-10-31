import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pandas as pd
from src.clustering.preprocess import preprocess_series
from src.clustering.hierarchical import run_linkage_and_dendrogram
from src.similarity.ai_models import load_sentence_model
from src.similarity.vector_models import compute_embeddings

# Rutas base
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DATA_DIR = os.path.join(BASE_DIR, "data")
INPUT_FILE = os.path.join(DATA_DIR, "download/unified.csv")
CLUSTERING_DIR = os.path.join(DATA_DIR, "clustering")

# Crear directorio de clustering si no existe
os.makedirs(CLUSTERING_DIR, exist_ok=True)

print("🔍 Requerimiento 3 - Análisis de clustering jerárquico")
print(f"📂 Leyendo archivo: {INPUT_FILE}")

# ---------- Validar archivo ----------
if not os.path.exists(INPUT_FILE):
    raise FileNotFoundError(f"No se encontró el archivo: {INPUT_FILE}\n"
                          f"Asegúrate de ejecutar primero run_downloader.py")

# ---------- Cargar datos ----------
df = pd.read_csv(INPUT_FILE)
print(f"📄 Se cargaron {len(df)} artículos")

# Seleccionar artículos: pedir al usuario o usar todos
subset = df  # o filtrar por índice / selección

# Validar que haya abstracts
if "abstract" not in subset.columns:
    raise ValueError("El archivo no contiene la columna 'abstract'")

# Filtrar abstracts vacíos
subset = subset[subset['abstract'].notna()]
subset = subset[subset['abstract'].astype(str).str.strip() != '']
print(f"📄 Artículos con abstract válido: {len(subset)}")

if len(subset) == 0:
    raise ValueError("No hay artículos con abstracts válidos para procesar")

# ---------- Preprocesamiento ----------
print("\n🔧 Preprocesando textos...")
texts = preprocess_series(subset['abstract'], do_lemmatize=False)
print(f"✅ Textos preprocesados: {len(texts)}")

# ---------- Embeddings semánticos ----------
print("\n🤖 Cargando modelo de embeddings...")
model = load_sentence_model()

print("🧮 Generando embeddings...")
embs = compute_embeddings(model, texts).cpu().numpy()
print(f"✅ Embeddings generados: {embs.shape}")

# ---------- Preparar etiquetas ----------
labels = subset['title'].fillna('Sin título').apply(lambda s: s[:80]).tolist()

# ---------- Clustering con diferentes métodos ----------
print("\n🌳 Generando dendrogramas con diferentes métodos de linkage...")
methods = ['single', 'complete', 'average']
results = {}

for m in methods:
    print(f"\n  📊 Procesando método: {m}")
    out_file = os.path.join(CLUSTERING_DIR, f"dendrogram_{m}.png")
    
    try:
        Z, coph = run_linkage_and_dendrogram(
            embs, 
            labels, 
            method=m, 
            metric='cosine', 
            out_path=out_file
        )
        results[m] = coph
        print(f"     ✅ Dendrograma guardado: {out_file}")
        print(f"     📈 Coeficiente cofonético: {coph:.4f}")
    except Exception as e:
        print(f"     ⚠️ Error en método {m}: {e}")
        results[m] = 0.0

# ---------- Resultados ----------
print("\n" + "="*60)
print("📊 RESULTADOS DEL ANÁLISIS DE CLUSTERING")
print("="*60)

print("\n🔢 Coeficientes cofonéticos por método:")
for method, coph in sorted(results.items(), key=lambda x: x[1], reverse=True):
    print(f"   • {method:10s}: {coph:.4f}")

if results:
    best = max(results, key=results.get)
    best_coph = results[best]
    print(f"\n🏆 Mejor método: {best.upper()} (coeficiente: {best_coph:.4f})")
    print(f"\n💡 Interpretación:")
    if best_coph > 0.8:
        print("   ✅ Excelente correlación - El clustering representa muy bien las distancias")
    elif best_coph > 0.7:
        print("   ✅ Buena correlación - El clustering es confiable")
    elif best_coph > 0.6:
        print("   ⚠️  Correlación moderada - El clustering es aceptable")
    else:
        print("   ⚠️  Correlación baja - Considera revisar los datos o método")
else:
    print("\n⚠️  No se pudo calcular ningún método de clustering")

print(f"\n📁 Dendrogramas guardados en: {CLUSTERING_DIR}")
print("\n✅ Proceso completado exitosamente!")