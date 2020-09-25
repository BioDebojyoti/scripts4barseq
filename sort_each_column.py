#!/usr/bin/env python3

import pandas as pd
import sys


def sort_each(csv_file):
    data = pd.read_csv(csv_file)
    list_df =[]
    index=[str(i)  for i in range(data.shape[0])]

    for i in range(2,len(data.columns)):
        l=[1] # column number of PBANKA Gene ID 0-based numbering!
        l.append(i)
        curr_data = data.iloc[:,l].copy()
        colname = curr_data.columns[1]
        sorted_curr_data = curr_data.sort_values(by=[colname], ascending=False).copy()
        sorted_curr_data.index=index
        list_df.append(sorted_curr_data)

    merged_data_frame = pd.concat(list_df, axis = 1, ignore_index = False)
    print(merged_data_frame)
    merged_data_frame.to_csv("merged_total_sample_counts_expected_data_out.csv")

if __name__ == '__main__':
    csv_file = sys.argv[1]

sort_each(csv_file)
