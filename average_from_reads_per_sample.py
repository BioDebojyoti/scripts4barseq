#!/usr/bin/env python3
'''
    average count for each sample using counts from both reads
'''

import sys, re
import pandas as pd

def sample_names(sample_and_read_names):
    sample_names = []
    for i,val in enumerate(sample_and_read_names):
        s = val.split("_001_")
        sample_names.append(s[0])

    sample_names = list(set(sample_names))
    sample_names.sort()

    return sample_names

def average_count_per_sample(csv_file,out_file):
    data = pd.read_csv(csv_file, sep = ",")
    sample_and_read_names = data.columns[3:].tolist()
    samples = sample_names(sample_and_read_names)
    output_data = pd.DataFrame()
    output_data["Gene"] = data["Gene"]
    output_data["Barcodes"] = data["Barcodes"]
    for i,val1 in enumerate(samples):
        output_data[val1] = 0
        denominator = 0
        for j,val2 in enumerate(sample_and_read_names):
            if re.search(val1,val2) != None:
                denominator += 1
                output_data[val1] = output_data[val1] + data[val2]

        output_data[val1] = output_data[val1]/denominator
        output_data.to_csv(out_file)

    return 0


if __name__ == '__main__':
    csv_file=sys.argv[1] # barcode counts in multiple columns corresponding to read pairs scanned in either direction
                         # with zero values
    out_file=sys.argv[2] # outfile with mean counts
    average_count_per_sample(csv_file,out_file)
