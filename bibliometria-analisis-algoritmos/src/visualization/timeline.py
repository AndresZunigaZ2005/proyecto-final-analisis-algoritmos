import matplotlib.pyplot as plt
import os

def plot_timeline_by_year(df, year_col='year', out_path='data/reports/timeline_year.png'):
    years = df[year_col].astype(str).str.extract(r'(\d{4})')[0].dropna()
    counts = years.value_counts().sort_index()
    plt.figure(figsize=(10,4))
    counts.plot(kind='line', marker='o')
    plt.title("Publicaciones por año")
    plt.xlabel("Año")
    plt.ylabel("Número de publicaciones")
    plt.tight_layout()
    plt.savefig(out_path)
    plt.close()

def plot_timeline_by_journal(df, year_col='year', journal_col='journal', out_path='data/reports/timeline_journal.png'):
    df['year4'] = df[year_col].astype(str).str.extract(r'(\d{4})')[0]
    pivot = df.groupby(['year4', journal_col]).size().unstack(fill_value=0)
    pivot.plot(kind='line', figsize=(12,6))
    plt.title("Publicaciones por año y revista")
    plt.tight_layout()
    plt.savefig(out_path)
    plt.close()
