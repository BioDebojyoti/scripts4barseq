#!/usr/bin/env python3
'''
    heatmap of normalized total count for samples
'''

import sys, re
import numpy as np
import pandas as pd
from sklearn import preprocessing
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

import os

if not os.path.exists("images"):
    os.mkdir("images")

def GROUPS(data):
    GROUP = []
    for i,val in enumerate(data.index):
         name = val.split('_')
         if len(name) <= 2:
              line = val
         else:
              line = name[1] + " " + name[2]

         GROUP.append(line)
    return GROUP

def TREATMENTS(data):
    TREATMENT = []
    for i,val in enumerate(data.index):
         name = val.split('_')
         if len(name) <= 2:
              line = val
         else:
              line = name[1]

         TREATMENT.append(line)
    return TREATMENT

def start_loc(string,data):
    start = None
    pool = None
    column = None
    for i,v in enumerate(data.columns.tolist()):
        if re.search(string, v, re.IGNORECASE):
            start = i
            pool = v.split("_")[0]
            column = v
            break
    output = [start]
    output.append(pool)
    output.append(column)
    return output


def pca_analysis(csv_file):
    s = csv_file.split('/')
    # out_file = "normalized_sample_counts_" + s[len(s) - 1]

    normalized = pd.read_csv(csv_file)
    normalized.index = normalized['Gene']

    sample_start = start_loc("pool",normalized)
    input_start = start_loc("input", normalized)
    gdna_start = start_loc("gDNA", normalized)
    # normalized = normalized.drop([input_start[2]], axis = 1)
    # normalized = normalized.drop([input_start[2], gdna_start[2]], axis = 1)
#    normalized = normalized.drop(['poolC2_P_BL6_d7_m4'], axis = 1)

    normcolnames = normalized.columns.tolist()[sample_start[0]:]
    # print(normcolnames)
    # exit()
    cols_needed = []
    cols_needed.extend(normcolnames)
    normalized = normalized.loc[:,cols_needed]
    # print(normalized.head())
    transposed_normalized = normalized.T

    transposed_normalized['GROUP'] = GROUPS(transposed_normalized)
    # import pdb; pdb.set_trace()
    transposed_normalized['TREATMENT'] = TREATMENTS(transposed_normalized)
    transposed_normalized['SAMPLE'] = transposed_normalized.index.tolist()


    #
    # PCA analysis
    features = transposed_normalized.columns[:transposed_normalized.shape[1] - 3] # last three columns are GROUP TREATMENT and SAMPLE
    # Separating out the features
    x = transposed_normalized.loc[:, features].values
    # Separating out the target == LINE
    y = transposed_normalized.loc[:,['GROUP','TREATMENT','SAMPLE']].values
    # Standardizing the features
    x = StandardScaler().fit_transform(x)

    pca = PCA(n_components = 2)
    principalComponents = pca.fit_transform(x)
    principalDf = pd.DataFrame(data = principalComponents, columns = ['principal component 1', 'principal component 2'])
    principalDf.index = transposed_normalized.index
    finalDf = pd.concat([principalDf, transposed_normalized[['GROUP']],transposed_normalized[['TREATMENT']],transposed_normalized[['SAMPLE']]], axis = 1)

    fig = px.scatter(finalDf, x = "principal component 1", y = "principal component 2",
                 hover_name = "SAMPLE", hover_data = ['GROUP','TREATMENT'], color = 'GROUP')
    fig.update_traces(marker=dict(size=12))
    fig.update_layout(title = sample_start[1])
    # fig.update_xaxes(range=[-5,10])
    # fig.update_yaxes(range=[-5,5])
    # fig.update_xaxes(range=[np.min(finalDf['principal component 1']), np.max(finalDf['principal component 1'])])
    # fig.update_yaxes(range=[np.min(finalDf['principal component 2']), np.max(finalDf['principal component 2'])])
    fig.show()
    fig.write_image("images/NORMALIZED_ALL_SAMPLES_" + sample_start[1].upper() + "_PCA.pdf")
    # fig.write_image("images/NORMALIZED_ALL_SAMPLES_WO_OUTLIER_" + sample_start[1].upper() + "_PCA.pdf")
    # fig.write_image("images/NORMALIZED_ALL_SAMPLES_WO_INPUT_" + sample_start[1].upper() + "_PCA.pdf")
    # fig.write_image("images/NORMALIZED_ALL_SAMPLES_WO_INPUT_AND_GDNA_" + sample_start[1].upper() + "_PCA.pdf")
    # fig.write_image("images/NORMALIZED_ALL_SAMPLES_WO_INPUT_AND_GDNA_OUTLIER_" + sample_start[1].upper() + "_PCA.pdf")


if __name__ == '__main__':
    csv_file = sys.argv[1]

    pca_analysis(csv_file)
