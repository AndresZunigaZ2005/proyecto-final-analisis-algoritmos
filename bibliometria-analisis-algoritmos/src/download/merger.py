# src/download/merger.py
"""
Unifica los CSV en data/ y deduplica:
- primero: por DOI (si existe)
- luego: por título normalizado (minúsculas, quitar puntuación/espacios extras)
Genera:
  - data/unified.csv   -> registros únicos
  - data/duplicates.csv -> registros eliminados como duplicados
"""

import os
import pandas as pd
import re

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
DATA_DIR = os.path.join(BASE_DIR, "data")

def normalize_title(t):
    if pd.isna(t):
        return ""
    s = str(t).lower().strip()
    # quitar puntuación
    s = re.sub(r"[^\w\s]", "", s)
    s = re.sub(r"\s+", " ", s)
    return s

def merge_and_deduplicate(data_dir=DATA_DIR, out_unique="unified.csv", out_duplicates="duplicates.csv"):
    files = [f for f in os.listdir(data_dir) if f.lower().endswith(".csv")]
    if not files:
        print("No CSV en", data_dir)
        return
    all_rows = []
    for f in files:
        path = os.path.join(data_dir, f)
        try:
            df = pd.read_csv(path, dtype=str).fillna("")
            df["source_file"] = f
            all_rows.append(df)
        except Exception as e:
            print("No pudo leer", path, e)
    df_all = pd.concat(all_rows, ignore_index=True, sort=False).fillna("")
    # normalizaciones
    df_all["doi_norm"] = df_all["doi"].astype(str).str.strip().str.lower()
    df_all["title_norm"] = df_all["title"].apply(normalize_title)

    seen_dois = set()
    seen_titles = set()
    uniques = []
    duplicates = []

    for _, row in df_all.iterrows():
        doi = str(row.get("doi_norm","") or "").strip()
        title_norm = str(row.get("title_norm","") or "").strip()
        if doi:
            if doi in seen_dois:
                duplicates.append(row.to_dict())
            else:
                seen_dois.add(doi)
                uniques.append(row.to_dict())
        else:
            if title_norm and title_norm in seen_titles:
                duplicates.append(row.to_dict())
            else:
                seen_titles.add(title_norm)
                uniques.append(row.to_dict())

    df_uni = pd.DataFrame(uniques)
    df_dup = pd.DataFrame(duplicates)

    out_uni_path = os.path.join(data_dir, out_unique)
    out_dup_path = os.path.join(data_dir, out_duplicates)
    df_uni.to_csv(out_uni_path, index=False, encoding="utf-8")
    df_dup.to_csv(out_dup_path, index=False, encoding="utf-8")
    print(f"Unificados: {len(df_uni)} -> {out_uni_path}")
    print(f"Duplicados guardados: {len(df_dup)} -> {out_dup_path}")

    return out_uni_path, out_dup_path

if __name__ == "__main__":
    merge_and_deduplicate()
