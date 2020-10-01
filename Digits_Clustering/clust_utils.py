import numpy as np
import pandas as pd
import pickle

from sklearn.cluster import AgglomerativeClustering, KMeans
from sklearn.metrics import (homogeneity_score, completeness_score,
                             v_measure_score)
from sklearn.metrics import silhouette_score

import seaborn as sns
import matplotlib.pyplot as plt


def group_mean(X, col):
    col_uniq = np.sort(np.unique(col))
    res = np.array([np.mean(X[col==col_i], axis=0) for col_i in col_uniq])
    
    return res


def plot_digits(data, suptitle, interpolation='bicubic'):
    fig = plt.figure(figsize=(6, 6))
    fig.subplots_adjust(hspace=0.2, wspace=0.2, top=0.94)
    fig.suptitle(suptitle, fontsize=14)

    for i in range(10):
        ax = fig.add_subplot(3, 4, i + 1, xticks=[], yticks=[])    
        ax.imshow(data[i].reshape((8, 8)), cmap=plt.cm.binary,
                  clim=(0, 13), interpolation=interpolation)


def get_metrics(low, upper, method, data, target):
    K = range(low, upper)
    silhouette = []
    homogeneity = []
    completeness = []
    v_ms = []

    for n_clusters in K:
        if method=='KMeans':
            clusterer = method(n_clusters=n_clusters, n_init=100)
        else:
            clusterer = method(n_clusters=n_clusters)
            
        preds = clusterer.fit_predict(data)
        silhouette.append(silhouette_score(data, preds))
        homogeneity.append(homogeneity_score(target, preds))
        completeness.append(completeness_score(target, preds))
        v_ms.append(v_measure_score(target, preds))
        
    return silhouette, homogeneity, completeness, v_ms   


def plot_scores(data, hue, style):    
    plt.figure(figsize=(9, 6))
    sns.set(style="whitegrid")
    sns.lineplot(
    x="Number of clusters",
    y="Values",
    hue=hue,
    style=style,
    dashes=False,
    markers=True,
    palette="tab10",
    data=data);
    

def dim_reduction(meth_reduce, meth_clust, data, target):
    num_comp = [2, 5, 10, 20]
    silhouette = []
    v_ms = []

    for i in num_comp:
        reducer = meth_reduce(n_components=i, random_state=42)
        data_reduced = reducer.fit_transform(data)
                
        if meth_clust=='KMeans':
            clusterer = meth_clust(n_clusters=10, n_init=100)
        else:
            clusterer = meth_clust(n_clusters=10)
            
        preds = clusterer.fit_predict(data_reduced)
        
        silhouette.append(silhouette_score(data_reduced, preds))
        v_ms.append(v_measure_score(target, preds))
        
    return silhouette, v_ms
