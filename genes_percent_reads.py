#!/usr/bin/env python3

import math
import sys, re, os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages


def start_loc(string,data):
    start = None
    pool = None
    for i,v in enumerate(data.columns.tolist()):
        if re.search(string, v):
            start = i
            pool = v.split("_")[0]
            break
    output = [start]
    output.append(pool)
    return output



def genes_percent_reads(csv_file):
    file = csv_file.split("/")
    outputfile = file[len(file)-1][:-4]

    data = pd.read_csv(csv_file)
    data.index = data['Gene']
    # print(data.head())

    sample_start = start_loc("pool",data)
    input_start = start_loc("input",data)
    gdna_start = start_loc("gDNA",data)

    print(sample_start[0],sample_start[1])
    print(input_start[0],input_start[1])
    print(gdna_start[0],gdna_start[1])

    data = data.iloc[:,sample_start[0]:]

    if input_start[0]:
        data = data.iloc[:,:-1]

    if gdna_start[0]:
        data = data.iloc[:,:-1]

    rel_abundance = data.apply(lambda s: s/s.sum(axis = 0))

    # print(rel_abundance.sum())

    sum_rel_abundance_per_gene = []
    for i,v in enumerate(rel_abundance.index.tolist()):
        row_sum = rel_abundance.loc[v,:].sum()
        sum_rel_abundance_per_gene.append(row_sum)



    with PdfPages("genes_percent_reads_pie_chart_per_sample_" + sample_start[1] + ".pdf") as pdf:
        for i,v in enumerate(rel_abundance.columns.tolist()):
            col = rel_abundance.loc[:,v]
            col.plot.pie(y = v, rotatelabels = True, fontsize = 6, radius = 0.75)
            # plt.title(v)
            pdf.savefig()
            plt.close()
    # 
    # if sample_start[1] == "pool1":
    #     over_represented_genes = ["PBANKA_031480", "PBANKA_134630", "PBANKA_051490",  "PBANKA_051500"] # gDNA pool1
    # if sample_start[1] == "pool2":
    #     over_represented_genes = ["PBANKA_030600", "PBANKA_050650", "PBANKA_103780", "PBANKA_051490",  "PBANKA_051500"] # gDNA pool2.2
    # no_over_rep_gene_data = data.drop(over_represented_genes, axis = 0)
    # no_over_rep_gene_data.to_csv(sample_start[1] + "_no_over_abundant_gene.csv")

if __name__ == '__main__':
    csv_file = sys.argv[1]
    genes_percent_reads(csv_file)
