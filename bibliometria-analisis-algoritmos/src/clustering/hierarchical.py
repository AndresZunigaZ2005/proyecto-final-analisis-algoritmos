import os
import numpy as np
import matplotlib.pyplot as plt
from scipy.cluster.hierarchy import linkage, dendrogram, cophenet
from scipy.spatial.distance import pdist
from sklearn.decomposition import PCA

def compute_distance_matrix(embeddings, metric='cosine'):
    # embeddings: numpy array (n_samples, n_features)
    return pdist(embeddings, metric=metric)

def run_linkage_and_dendrogram(embeddings, labels, method='average', metric='cosine', out_path=None):
    # embeddings -> distance vector
    dist_vec = compute_distance_matrix(embeddings, metric=metric)
    Z = linkage(dist_vec, method=method) if False else linkage(embeddings, method=method, metric=metric)
    coph_corr, coph_dists = cophenet(Z, dist_vec)
    # plot dendrogram
    plt.figure(figsize=(12, 6))
    dendrogram(Z, labels=labels, leaf_rotation=90)
    plt.title(f"Dendrogram ({method}) - cophenetic={coph_corr:.3f}")
    plt.tight_layout()
    if out_path:
        plt.savefig(out_path)
    plt.close()
    return Z, coph_corr
