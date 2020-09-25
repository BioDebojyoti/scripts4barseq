#!/usr/bin/env python3

import sys, re, os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import plotly.express as px
from matplotlib.backends.backend_pdf import PdfPages


def start_loc(string,data):
    start = None
    pool = None
    column = None
    for i,v in enumerate(data.columns.tolist()):
        if re.search(string, v):
            start = i
            parts = v.split("_")
            pool = parts[0]
            column = v
            break
    output = [start]
    output.append(pool)
    output.append(column)
    return output


if not os.path.exists('images'):
    os.makedirs('images')

def time_plot(csv_file):
    data = pd.read_csv(csv_file)

    data.index = data['Gene']
    sample_start = start_loc("pool", data)
    gdna_start = start_loc("gDNA", data)
    input_start = start_loc("input", data)
    data = data.iloc[:,sample_start[0]:]

    if gdna_start[2]:
        data = data.drop([gdna_start[2]], axis = 1)

    if input_start[2]:
        data = data.drop([input_start[2]], axis = 1)
    # data = data.drop(['Unnamed: 0', 'Unnamed: 0.1','Unnamed: 0.1.1', 'Gene', 'Barcodes', 'gDNA barseq pool 1'], axis = 1)

    data = data.apply(lambda x: (x+1)/x.sum(), axis = 0)
    data = data.apply(lambda x: np.log(x))

    data = data.T

    DAY = []
    STRAIN = []
    REPLICATE = []
    TREATMENT = []

    for i,v in enumerate(data.index.tolist()):
        string = v.split('_')
        day = int(string[3].replace('d',''))
        strain = string[2]
        replicate = string[4].replace('m','')
        treatment = string[1]
        DAY.append(day)
        STRAIN.append(strain)
        REPLICATE.append(replicate)
        TREATMENT.append(treatment)

    data['DAY'] = DAY
    data['STRAIN'] = STRAIN
    data['REPLICATE'] = REPLICATE
    data['TREATMENT'] = TREATMENT
    data['GROUP1'] = data['STRAIN'] + '_' + data['TREATMENT'] + '_' + data['REPLICATE']
    data['GROUP'] = data['STRAIN'] + '_' + data['TREATMENT']

    with PdfPages("images/time_plot_per_gene_" + sample_start[1] + ".pdf") as pdf:

        for i in data.columns.tolist():
            if re.search('PBANKA',i) != None:

                print('processing ' + i)
                # P BL6
                P_BL6_x_axis = []
                P_BL6_y_axis = []
                P_BL6_y_error = []
                P_BL6_color = []
                P_BL6_tmp = pd.DataFrame()
                # NP BL6
                NP_BL6_x_axis = []
                NP_BL6_y_axis = []
                NP_BL6_y_error = []
                NP_BL6_color = []
                NP_BL6_tmp = pd.DataFrame()
                # P RAG1KO
                P_RAG1KO_x_axis = []
                P_RAG1KO_y_axis = []
                P_RAG1KO_y_error = []
                P_RAG1KO_color = []
                P_RAG1KO_tmp = pd.DataFrame()
                # NP RAG1KO
                NP_RAG1KO_x_axis = []
                NP_RAG1KO_y_axis = []
                NP_RAG1KO_y_error = []
                NP_RAG1KO_color = []
                NP_RAG1KO_tmp = pd.DataFrame()


                for k,v in data.groupby(['DAY', 'STRAIN', 'TREATMENT']).indices.items():
                    ID = k[2]+ '_' + k[1]
                    if ID == 'NP_BL6':
                        NP_BL6_tmp=data.loc[data.index[v],i]
                        med = NP_BL6_tmp.median()
                        mad = NP_BL6_tmp.mad()
                        NP_BL6_y_axis.append(med)
                        NP_BL6_y_error.append(mad)
                        NP_BL6_x_axis.append(k[0]+0.2)
                        NP_BL6_color.append('r')
                    if ID == 'P_BL6':
                        P_BL6_tmp=data.loc[data.index[v],i]
                        med = P_BL6_tmp.median()
                        mad = P_BL6_tmp.mad()
                        P_BL6_y_axis.append(med)
                        P_BL6_y_error.append(mad)
                        P_BL6_x_axis.append(k[0]+0.10)
                        P_BL6_color.append('b')
                    if ID == 'NP_RAG1KO':
                        NP_RAG1KO_tmp=data.loc[data.index[v],i]
                        med = NP_RAG1KO_tmp.median()
                        mad = NP_RAG1KO_tmp.mad()
                        NP_RAG1KO_y_axis.append(med)
                        NP_RAG1KO_y_error.append(mad)
                        NP_RAG1KO_x_axis.append(k[0]-0.2)
                        NP_RAG1KO_color.append('g')
                    if ID == 'P_RAG1KO':
                        P_RAG1KO_tmp=data.loc[data.index[v],i]
                        med = P_RAG1KO_tmp.median()
                        mad = P_RAG1KO_tmp.mad()
                        P_RAG1KO_y_axis.append(med)
                        P_RAG1KO_y_error.append(mad)
                        P_RAG1KO_x_axis.append(k[0]-0.10)
                        P_RAG1KO_color.append('m')
                # if i == "PBANKA_051490":
                #    import pdb;pdb.set_trace()
                
                
                plt.plot(NP_BL6_x_axis,NP_BL6_y_axis, 'ro-', label = 'NP_BL6')
                plt.legend()
                plt.plot(P_BL6_x_axis,P_BL6_y_axis, 'go:', label = 'P_BL6')
                plt.legend()
                plt.plot(NP_RAG1KO_x_axis, NP_RAG1KO_y_axis, 'bo-.', label = 'NP_RAG1KO')
                plt.legend()
                plt.plot(P_RAG1KO_x_axis, P_RAG1KO_y_axis, 'mo--', label = 'P_RAG1KO')
                plt.legend()
                plt.errorbar(NP_BL6_x_axis, NP_BL6_y_axis, ecolor = 'r', yerr = NP_BL6_y_error, capsize = 5.0, fmt= 'None')
                plt.errorbar(P_BL6_x_axis, P_BL6_y_axis, ecolor = 'g', yerr = P_BL6_y_error, capsize = 5.0, fmt= 'None')
                plt.errorbar(NP_RAG1KO_x_axis, NP_RAG1KO_y_axis, ecolor = 'b', yerr = NP_RAG1KO_y_error, capsize = 5.0, fmt='None')
                plt.errorbar(P_RAG1KO_x_axis, P_RAG1KO_y_axis, ecolor='m', yerr = P_RAG1KO_y_error, capsize = 5.0, fmt='None')
                plt.title(i)
                plt.xlabel('Day')
                plt.ylabel('log(normalized count)')
                pdf.savefig()
                plt.close()
                # plt.savefig('images/' + str(i) + '.pdf')
                # plt.clf()



if __name__ == '__main__':
    csv_file = sys.argv[1]

    time_plot(csv_file)
