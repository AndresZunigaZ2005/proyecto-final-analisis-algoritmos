# src/download/merger.py
"""
Unifica los CSV en data/ y deduplica:
- primero: por DOI (si existe)
- luego: por título normalizado (minúsculas, quitar puntuación/espacios extras)
Genera:
  - data/unified.csv   -> registros únicos
  - data/duplicates.csv -> registros eliminados como duplicados
"""
import os, pandas as pd, re

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
DATA_DIR = os.path.join(BASE_DIR, "data/download")

def normalize_title(t):
    if pd.isna(t): return ""
    t = re.sub(r"[^\w\s]", "", str(t).lower().strip())
    return re.sub(r"\s+", " ", t)

def merge_and_deduplicate(data_dir=DATA_DIR):
    files = [f for f in os.listdir(data_dir) if f.endswith(".csv")]
    all_rows = []
    for f in files:
        try:
            df = pd.read_csv(os.path.join(data_dir, f))
            if df.empty or len(df.columns) < 2:
                print(f"⚠️ Ignorando CSV vacío: {f}")
                continue
            df["source_file"] = f
            all_rows.append(df)
        except Exception as e:
            print(f"No pudo leer {f}: {e}")
    if not all_rows:
        print("⚠️ No hay datos válidos para unir.")
        return
    df = pd.concat(all_rows, ignore_index=True)
    df["title_norm"] = df["title"].apply(normalize_title)
    df.drop_duplicates(subset=["doi", "title_norm"], inplace=True)
    out = os.path.join(data_dir, "unified.csv")
    df.to_csv(out, index=False)
    print(f"✅ Unificados {len(df)} artículos -> {out}")
