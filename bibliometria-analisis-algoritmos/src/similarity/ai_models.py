from sentence_transformers import SentenceTransformer, util

# Cargamos un modelo pequeño de Sentence-BERT
model = SentenceTransformer('all-MiniLM-L6-v2')

def sbert_similarity(text1: str, text2: str) -> float:
    embeddings = model.encode([text1, text2], convert_to_tensor=True)
    sim = util.cos_sim(embeddings[0], embeddings[1])
    return float(sim.item())

def transformer_embedding_similarity(text1: str, text2: str) -> float:
    # También usa SentenceTransformer, pero puede simular un "modelo IA distinto"
    # (puedes cambiarlo por otro como 'paraphrase-MiniLM-L3-v2' si deseas)
    model_alt = SentenceTransformer('paraphrase-MiniLM-L3-v2')
    embeddings = model_alt.encode([text1, text2], convert_to_tensor=True)
    sim = util.cos_sim(embeddings[0], embeddings[1])
    return float(sim.item())

def load_sentence_model(model_name="sentence-transformers/all-MiniLM-L6-v2"):
    """Carga el modelo preentrenado para embeddings semánticos."""
    print("🧠 Cargando modelo:", model_name)
    model = SentenceTransformer(model_name)
    return model
