#!/usr/bin/env python3
'''
    extract only rows contaning expected gene targets
'''

import sys, re
import pandas as pd

def extract_expected(csv_file,genes_file_to_extract):
    data = pd.read_csv(csv_file, sep = "\t")
    genes = pd.read_csv(genes_file_to_extract)
    search_list = data['Gene'].tolist()
    genes_list = genes['gene'].tolist()

    # import pdb; pdb.set_trace()

    rows_to_keep = []

    for row in range(genes.shape[0]):
        for j,val in enumerate(search_list):
            if re.search(genes.iloc[row,1],val) != None and re.search(genes.iloc[row,2],val) != None:
                rows_to_keep.append(j)
                data['Gene'].values[j] = genes.iloc[row,1]

    expected_data_out = data.loc[rows_to_keep,:].copy()

    rows_to_discard = []
    for i in range(data.shape[0]):
        if i not in rows_to_keep:
            rows_to_discard.append(i)


    unexpected_data_out = data.loc[rows_to_discard,:].copy()


    expected_data_out.to_csv("expected_data_out.csv")
    unexpected_data_out.to_csv("unexpected_data_out.csv")

    print(expected_data_out.shape)
    print(unexpected_data_out.shape)
    # print(expected_data_out.head)

if __name__ == '__main__':
    csv_file = sys.argv[1] # barcode counts in multiple columns corresponding to read pairs scanned in either direction
                         # with zero values
    genes_file_to_extract = sys.argv[2] # outfile with mean counts
    extract_expected(csv_file,genes_file_to_extract)
