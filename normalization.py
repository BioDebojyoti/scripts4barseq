#!/usr/bin/env python3
'''
    normalization total count for samples
'''

import sys, re
import pandas as pd
from sklearn import preprocessing
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
import seaborn as sns

def normalization(csv_file):
    s = csv_file.split('/')
    out_file = "normalized_" + s[len(s) - 1]

    data = pd.read_csv(csv_file)

    for i,v in enumerate(data.columns.tolist()):
        if re.search("pool",v) is not None:
            start = i
            break

    datacols = data.columns.tolist()
    normalized = pd.DataFrame()
    normalized['Gene'] = data['Gene']

    test = data[datacols[start:]].apply(lambda x: x/x.sum(), axis = 0)
    normalized[datacols[start:]] = test
    print(normalized.sum())
    print(normalized.head())
    normalized.to_csv(out_file)

if __name__ == '__main__':
    csv_file = sys.argv[1]

    normalization(csv_file)
