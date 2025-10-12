import re
from sklearn.feature_extraction.text import TfidfVectorizer
from collections import Counter

class MetricsGenerator:
    def __init__(self, df_articles, df_similarities=None):
        self.df_articles = df_articles
        self.df_similarities = df_similarities

    def count_by_source(self):
        return self.df_articles["source"].value_counts().to_dict()

    def count_by_year(self):
        if "year" in self.df_articles.columns:
            return self.df_articles["year"].value_counts().sort_index().to_dict()
        return {}

    def similarity_stats(self):
        if self.df_similarities is None:
            return {}
        return {
            "promedio": float(self.df_similarities["similarity"].mean()),
            "máximo": float(self.df_similarities["similarity"].max()),
            "mínimo": float(self.df_similarities["similarity"].min())
        }

    # --- NUEVOS MÉTODOS ---
    def keyword_frequency(self, keywords):
        """Cuenta las ocurrencias de palabras clave en los abstracts."""
        text = " ".join(self.df_articles["abstract"].fillna("").tolist()).lower()
        freq = {kw: len(re.findall(rf"\b{re.escape(kw.lower())}\b", text)) for kw in keywords}
        return dict(sorted(freq.items(), key=lambda x: x[1], reverse=True))

    def extract_new_keywords(self, max_terms=15):
        """Extrae nuevas palabras clave relevantes usando TF-IDF."""
        abstracts = self.df_articles["abstract"].dropna().tolist()
        # Limpieza básica: eliminar espacios, caracteres no alfabéticos
        cleaned = [
            " ".join(re.findall(r"[a-zA-Z]{3,}", abs.lower()))
            for abs in abstracts if isinstance(abs, str) and abs.strip() != ""
        ]

        if not cleaned:
            print("⚠️ No se encontraron abstracts válidos para analizar.")
            return []

        from sklearn.feature_extraction.text import TfidfVectorizer
        vectorizer = TfidfVectorizer(stop_words="english", max_features=1000)
        try:
            tfidf_matrix = vectorizer.fit_transform(cleaned)
        except ValueError:
            print("⚠️ Error: vocabulario vacío (no hay palabras relevantes).")
            return []

        scores = tfidf_matrix.sum(axis=0).A1
        vocab = vectorizer.get_feature_names_out()
        freq = sorted(zip(vocab, scores), key=lambda x: x[1], reverse=True)
        return [word for word, _ in freq[:max_terms]]

    def precision_of_new_keywords(self, new_keywords, base_keywords):
        """Evalúa qué tan relacionadas son las nuevas palabras (similitud con las base)."""
        intersect = set(k.lower() for k in new_keywords) & set(k.lower() for k in base_keywords)
        precision = len(intersect) / len(new_keywords) if new_keywords else 0
        return precision
