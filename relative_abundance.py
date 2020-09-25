#!/usr/bin/env python3
'''
    relative abundance
'''

import sys, re
import pandas as pd
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns


def normalize_bar_count_per_sample(csv_file,out_file):
    data = pd.read_csv(csv_file, sep = ",")
    samples = data.columns[3:].tolist()
    # print(samples)
    output_data = pd.DataFrame()
    output_data["Gene"] = data["Gene"]
    output_data["Barcodes"] = data["Barcodes"]
    for i,val1 in enumerate(samples):
        val2 = "bc_ratio_" + val1
        output_data[val2] = data[val1]/sum(data[val1])

    output_data["sum_along_row"] = output_data.sum(axis = 1)
    output_data.iloc[:,2:output_data.shape[1]-1] = output_data.iloc[:,2:output_data.shape[1]-1].div(output_data["sum_along_row"], axis = 0)
    # print(output_data.iloc[0:10,2:output_data.shape[1]-1])
    row_labels = output_data["Gene"].tolist()
    column_labels = data.columns[3:11].tolist()
    # print(row_labels,column_labels)
    sns.heatmap(output_data.iloc[:,2:output_data.shape[1]-1], xticklabels = column_labels, yticklabels = False)
    # sns.heatmap(output_data.iloc[:,2:output_data.shape[1]-1], xticklabels = column_labels, yticklabels = [v for i,v in enumerate(row_labels) if i%50 == 0 ])
    plt.xticks(rotation = 15)
    plt.show()


if __name__ == '__main__':
    csv_file=sys.argv[1] # barcode counts in multiple columns corresponding to read pairs scanned in either direction
                         # with zero values
    out_file=sys.argv[2] # outfile with mean counts
    normalize_bar_count_per_sample(csv_file,out_file)
