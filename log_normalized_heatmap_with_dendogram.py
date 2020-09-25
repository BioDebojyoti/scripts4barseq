#!/usr/bin/env python3

# Libraries
import seaborn as sns
import pandas as pd
from matplotlib import pyplot as plt
import sys, re
import numpy as np


def start_loc(string,data):
    start = None
    pool = None
    for i,v in enumerate(data.columns.tolist()):
        if re.search(string, v):
            start = i
            pool = v[:5]
            break
    output = [start]
    output.append(pool)
    return output


def plot_heatmap(csv_file):
    # Data set
    df = pd.read_csv(csv_file)
    df.index = df['Gene']
    sample_start = start_loc("pool",df)
    df = df.iloc[:,sample_start[0]:]

    normplotdata = df.apply(lambda x: x/x.sum(), axis = 0).copy()
    lognormplotdata = normplotdata.apply(lambda x: np.log(x+0.0000000001)).copy()

    corrdata = lognormplotdata.corr(method = 'spearman')
    ax = sns.clustermap(corrdata, metric = 'euclidean', mask = 0, figsize = (12,8), xticklabels = True, yticklabels = True)
    ax.ax_heatmap.set_xticklabels(ax.ax_heatmap.get_xmajorticklabels(), fontsize = 6)
    ax.ax_heatmap.set_yticklabels(ax.ax_heatmap.get_ymajorticklabels(), fontsize = 6)
    ax.savefig('log_norm_correlation_heatmap_' + sample_start[1] + '.pdf')
    plt.show()



if __name__ == '__main__':
    csv_file = sys.argv[1] # un-normalized data file

    plot_heatmap(csv_file)
