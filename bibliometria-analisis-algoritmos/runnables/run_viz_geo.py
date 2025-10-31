import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pandas as pd
from src.visualization.geography import build_heatmap
from src.visualization.wordclouds import generate_wordcloud
from src.visualization.timeline import plot_timeline_by_year, plot_timeline_by_journal
from src.visualization.exporter import images_to_pdf

# Rutas base
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DATA_DIR = os.path.join(BASE_DIR, "data")
INPUT_FILE = os.path.join(DATA_DIR, "download/unified.csv")
VISUALIZATION_DIR = os.path.join(DATA_DIR, "visualization")

# Crear directorio de visualización si no existe
os.makedirs(VISUALIZATION_DIR, exist_ok=True)

print("🎨 Requerimiento 4 - Visualización de datos")
print(f"📂 Leyendo archivo: {INPUT_FILE}")

# ---------- Validar archivo ----------
if not os.path.exists(INPUT_FILE):
    raise FileNotFoundError(f"No se encontró el archivo: {INPUT_FILE}\n"
                          f"Asegúrate de ejecutar primero run_downloader.py")

# ---------- Cargar datos ----------
df = pd.read_csv(INPUT_FILE)
print(f"📄 Se cargaron {len(df)} artículos\n")

# ---------- 1) Mapa de calor geográfico ----------
print("🗺️  Generando mapa de calor geográfico...")
if 'country' not in df.columns:
    print("   ⚠️  No hay columna 'country' - Se omite el mapa geográfico")
    print("   💡 Intenta inferir desde 'affiliation' o 'authors', o provee un mapping")
    map_html = None
else:
    try:
        map_html = build_heatmap(df, country_col='country')
        map_path = os.path.join(VISUALIZATION_DIR, "geographic_heatmap.html")
        map_html.save(map_path)
        print(f"   ✅ Mapa guardado: {map_path}")
    except Exception as e:
        print(f"   ⚠️  Error generando mapa: {e}")
        map_html = None

# ---------- 2) Wordcloud ----------
print("\n☁️  Generando nube de palabras...")
try:
    texts = df['abstract'].fillna("").tolist()
    if 'keywords' in df.columns:
        texts += df['keywords'].fillna("").tolist()
    
    wc_path = os.path.join(VISUALIZATION_DIR, "wordcloud.png")
    generate_wordcloud(texts, wc_path)
    print(f"   ✅ Wordcloud guardado: {wc_path}")
    images = [wc_path]
except Exception as e:
    print(f"   ⚠️  Error generando wordcloud: {e}")
    images = []

# ---------- 3) Timeline por año ----------
print("\n📅 Generando timeline por año...")
try:
    timeline_year = os.path.join(VISUALIZATION_DIR, "timeline_year.png")
    plot_timeline_by_year(df, year_col='year', out_path=timeline_year)
    print(f"   ✅ Timeline por año guardado: {timeline_year}")
    images.append(timeline_year)
except Exception as e:
    print(f"   ⚠️  Error generando timeline por año: {e}")

# ---------- 4) Timeline por journal ----------
print("\n📰 Generando timeline por journal...")
try:
    timeline_journal = os.path.join(VISUALIZATION_DIR, "timeline_journal.png")
    plot_timeline_by_journal(df, year_col='year', journal_col='journal', out_path=timeline_journal)
    print(f"   ✅ Timeline por journal guardado: {timeline_journal}")
    images.append(timeline_journal)
except Exception as e:
    print(f"   ⚠️  Error generando timeline por journal: {e}")

# ---------- 5) Exportar a PDF ----------
print("\n📄 Exportando visualizaciones a PDF...")
if images:
    try:
        out_pdf = os.path.join(VISUALIZATION_DIR, "visual_analysis.pdf")
        images_to_pdf(images, out_pdf)
        print(f"   ✅ PDF generado: {out_pdf}")
    except Exception as e:
        print(f"   ⚠️  Error generando PDF: {e}")
else:
    print("   ⚠️  No hay imágenes para exportar a PDF")

# ---------- Resumen ----------
print("\n" + "="*60)
print("📊 RESUMEN DE VISUALIZACIONES GENERADAS")
print("="*60)
print(f"\n📁 Directorio de salida: {VISUALIZATION_DIR}")
print(f"\n📝 Archivos generados:")

generated_files = []
if map_html:
    generated_files.append("   • geographic_heatmap.html (mapa interactivo)")
if os.path.exists(os.path.join(VISUALIZATION_DIR, "wordcloud.png")):
    generated_files.append("   • wordcloud.png")
if os.path.exists(os.path.join(VISUALIZATION_DIR, "timeline_year.png")):
    generated_files.append("   • timeline_year.png")
if os.path.exists(os.path.join(VISUALIZATION_DIR, "timeline_journal.png")):
    generated_files.append("   • timeline_journal.png")
if os.path.exists(os.path.join(VISUALIZATION_DIR, "visual_analysis.pdf")):
    generated_files.append("   • visual_analysis.pdf (reporte completo)")

if generated_files:
    for f in generated_files:
        print(f)
else:
    print("   ⚠️  No se generó ningún archivo")

print("\n✅ Proceso completado!")