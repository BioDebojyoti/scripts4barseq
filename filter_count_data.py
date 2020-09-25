#!/usr/bin/env python3

'''
    Remove rows and columns having count less than a threshold!
'''

__author__ = "Debojyoti Das"
__email__ = "debojyoti.das@umu.se"

import sys
import numpy as np
import pandas as pd


def filter_count_data(csv_file,out_file):
    data = pd.read_csv(csv_file, sep = "\t")


    col_names = list(data.columns)
    # col_names_to_sum = col_names
    col_names_to_sum = col_names[:data.shape[1] - 2]

    data_out = data.copy()

    data_out['row_sums'] = data_out[col_names_to_sum].sum(axis = 1, numeric_only = True)  # sum of counts for each row!

    column_sums = data_out.sum(axis = 0, numeric_only = True)  # sum of counts for each column!
    data_out.loc["col_sums",:] = np.nan
    data_out.loc["col_sums",2:] = column_sums

    columns_to_keep = data_out.loc["col_sums"] > 20
    columns_to_keep[0:2] = True # Gene and barcode columns are retained!
    columns_to_keep = columns_to_keep[columns_to_keep == True]

    rows_to_keep = data_out["row_sums"][data_out["row_sums"] > 100]


    rows_to_keep = rows_to_keep[0:len(rows_to_keep)-1]
    columns_to_keep = columns_to_keep[0:len(columns_to_keep)-1]
    # print(rows_to_keep.index)
    # print(columns_to_keep.index)
    # import pdb;pdb.set_trace()
    filtered_data = data_out.loc[rows_to_keep.index, columns_to_keep.index]

    print(filtered_data.shape)

    filtered_data = filtered_data[filtered_data.iloc[:,138] + filtered_data.iloc[:,139] > 0]
    print(filtered_data.shape)

    col_out_data = filtered_data.columns
    row_out_data = filtered_data.index

    filtered_data.to_csv(out_file)

if __name__ == '__main__':
    csv_file=sys.argv[1] # barcode with zero values
    out_file=sys.argv[2] # outfile with removed zeros

    filter_count_data(csv_file,out_file)
