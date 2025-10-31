import os
import pandas as pd

class DataLoader:
    """Carga y valida los datos bibliométricos del proyecto."""
    def __init__(self, data_dir="data/download"):
        self.data_dir = data_dir
        self.unified_path = os.path.join(data_dir, "unified.csv")
        self.similarity_path = os.path.join(data_dir, "similarities.csv")

    def load_unified(self):
        df = pd.read_csv(self.unified_path)
        print(f"✅ Cargados {len(df)} artículos desde unified.csv")
        return df

    def load_similarities(self):
        if os.path.exists(self.similarity_path):
            df = pd.read_csv(self.similarity_path)
            print(f"✅ Cargadas {len(df)} relaciones de similitud")
            return df
        else:
            print("⚠️ No se encontró similarities.csv")
            return pd.DataFrame()
