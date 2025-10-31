import matplotlib.pyplot as plt
import os

class Visualizer:
    def __init__(self, output_dir=None):
        # Si no se especifica una carpeta, se usa data/reports por defecto
        if output_dir is None:
            base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
            output_dir = os.path.join(base_dir, "data", "analysis")
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)

    def plot_by_source(self, data):
        if not data:
            print("⚠️ No hay datos para graficar por fuente.")
            return
        plt.figure()
        plt.bar(data.keys(), data.values())
        plt.title("Artículos por fuente")
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig(os.path.join(self.output_dir, "by_source.png"))
        plt.close()

    def plot_by_year(self, data):
        if not data:
            print("⚠️ No hay datos para graficar por año.")
            return
        plt.figure()
        plt.bar(data.keys(), data.values())
        plt.title("Artículos por año")
        plt.tight_layout()
        plt.savefig(os.path.join(self.output_dir, "by_year.png"))
        plt.close()

    def plot_keyword_frequency(self, freq_dict):
        if not freq_dict:
            print("⚠️ No hay palabras clave para graficar.")
            return
        plt.figure(figsize=(10, 5))
        plt.bar(freq_dict.keys(), freq_dict.values(), color='skyblue')
        plt.title("Frecuencia de Palabras Asociadas")
        plt.xticks(rotation=45, ha="right")
        plt.tight_layout()
        plt.savefig(os.path.join(self.output_dir, "keyword_frequency.png"))
        plt.close()
        print(f"✅ Gráfico guardado en {os.path.join(self.output_dir, 'keyword_frequency.png')}")
