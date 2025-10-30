from scipy.cluster.hierarchy import cophenet
from scipy.spatial.distance import pdist

def evaluate_cophenetic(Z, embeddings, metric='cosine'):
    dist_vec = pdist(embeddings, metric=metric)
    coph_corr, _ = cophenet(Z, dist_vec)
    return coph_corr
