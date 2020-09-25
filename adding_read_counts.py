#!/usr/bin/env python3
'''
    extract only rows contaning expected gene targets
'''

import sys, re
import pandas as pd

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



def add_read_counts(csv_file):
    s = csv_file.split('/')
    out_file = "total_sample_counts_" + s[len(s) - 1]

    data = pd.read_csv(csv_file)
    sample_start = start_loc("P18103",data)

    samples = data.columns.tolist()
    ngi_ids = []
    for i,v in enumerate(samples[sample_start[0]:]):
        ngi_ids.append("_".join(v.split("_")[0:2]))
    unique_ngi_ids = set(ngi_ids)
    

    total_sample_count = pd.DataFrame()
    total_sample_count['Gene'] = data['Gene']
    for sample in unique_ngi_ids:
        cols_to_add = []
        for i in samples:
            if re.search(sample,i) != None:
                cols_to_add.append(i)
        total_sample_count[sample] = data[cols_to_add[0]] + data[cols_to_add[1]]

    total_sample_count.to_csv(out_file)
    print(total_sample_count.head())
    print(total_sample_count.shape)


if __name__ == '__main__':
    csv_file = sys.argv[1]

    add_read_counts(csv_file)
