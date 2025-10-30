import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pandas as pd
from src.visualization.geography import build_heatmap
from src.visualization.wordclouds import generate_wordcloud
from src.visualization.timeline import plot_timeline_by_year, plot_timeline_by_journal
from src.visualization.exporter import images_to_pdf

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")
df = pd.read_csv(os.path.join(DATA_DIR, "unified.csv"))

# 1) Build map (needs a column 'country' or 'affiliation' mapping)
if 'country' not in df.columns:
    print("⚠️ No 'country' column -- intenta inferir desde 'affiliation' o 'authors', o provee un mapping.")
else:
    map_html = build_heatmap(df, country_col='country')

# 2) Wordcloud (abstracts + keywords)
texts = df['abstract'].fillna("").tolist() + df.get('keywords', pd.Series([], dtype=str)).fillna("").tolist()
wc_path = os.path.join(DATA_DIR, "reports", "wordcloud.png")
generate_wordcloud(texts, wc_path)

# 3) Timelines
timeline_year = os.path.join(DATA_DIR, "reports", "timeline_year.png")
plot_timeline_by_year(df, year_col='year', out_path=timeline_year)
timeline_journal = os.path.join(DATA_DIR, "reports", "timeline_journal.png")
plot_timeline_by_journal(df, year_col='year', journal_col='journal', out_path=timeline_journal)

# 4) Export to PDF
images = [wc_path, timeline_year, timeline_journal]
out_pdf = os.path.join(DATA_DIR, "reports", "visual_analysis.pdf")
images_to_pdf(images, out_pdf)
print("✅ Visualizaciones generadas y exportadas a PDF:", out_pdf)
