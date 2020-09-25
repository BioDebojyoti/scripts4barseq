#!/usr/bin/env python3


import pandas as pd
import sys, re


def sample_info(csv_file,count_file):
        ID = pd.read_csv(csv_file)
        data = pd.read_csv(count_file)
        cols = list(data.columns)
        oldcols = cols
        rows = data.index
        # print(type(cols))
        for i in range(len(cols)):
            string = cols[i]
            # print(string)
            for j in range(ID.shape[0]):
                to_search = ID['NGI_SAMPLE_ID'].iloc[j]
                replacement = ID['SAMPLE_NAME'].iloc[j]
                value_return1 = re.search(to_search, string)

                if value_return1 != None:
                    s = str(replacement)
                    cols[i] = s

        print(data.head())
        data.columns = cols
        print(data.head())
        # out_file = "renamed_" + count_file.split("/")[1]
        out_file = "renamed_" + count_file
        data.to_csv(out_file)

if __name__ == '__main__':

    csv_file = sys.argv[1]
    count_file = sys.argv[2]
    sample_info(csv_file,count_file)
