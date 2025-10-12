import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.analysis.data_loader import DataLoader
from src.analysis.metrics import MetricsGenerator
from src.analysis.visualizer import Visualizer
from src.analysis.report_generator import ReportGenerator

BASE_KEYWORDS = [
    "Generative models", "Prompting", "Machine learning", "Multimodality",
    "Fine-tuning", "Training data", "Algorithmic bias", "Explainability",
    "Transparency", "Ethics", "Privacy", "Personalization",
    "Human-AI interaction", "AI literacy", "Co-creation"
]

if __name__ == "__main__":
    print("📈 Iniciando Requerimiento 3: Análisis de Palabras y Frecuencia")

    # --- Cargar datos ---
    loader = DataLoader()
    df_articles = loader.load_unified()

    # --- Calcular métricas ---
    metrics = MetricsGenerator(df_articles)
    keyword_freq = metrics.keyword_frequency(BASE_KEYWORDS)
    new_keywords = metrics.extract_new_keywords(max_terms=15)
    precision = metrics.precision_of_new_keywords(new_keywords, BASE_KEYWORDS)

    all_metrics = {
        "keyword_freq": keyword_freq,
        "new_keywords": new_keywords,
        "precision": precision
    }

    # --- Visualizar resultados ---
    viz = Visualizer()
    viz.plot_keyword_frequency(keyword_freq)

    # --- Generar reporte PDF ---
    report = ReportGenerator(all_metrics)
    report.save_summary()

    print("✅ Requerimiento 3 completado correctamente.")
