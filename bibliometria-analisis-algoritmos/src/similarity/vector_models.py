import torch

def compute_embeddings(model, texts):
    """Genera embeddings para una lista de textos."""
    embeddings = model.encode(texts, convert_to_tensor=True, show_progress_bar=True)
    return embeddings
