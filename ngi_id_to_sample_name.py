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
                value_return2 = re.search(r'_R1_', string)
                value_return3 = re.search(r"_F$", string)
                if value_return1 != None:
                    if value_return2 != None:
                        if value_return3 != None:
                            s = str(replacement) + "_R1" + "_F"
                            cols[i] = s
                        else:
                            s = str(replacement) + "_R1" + "_R"
                            cols[i] = s
                    else:
                        if value_return3 != None:
                            s = str(replacement) + "_R2" + "_F"
                            cols[i] = s
                        else:
                            s = str(replacement) + "_R2" + "_R"
                            cols[i] = s

        data.columns = cols
        # out_file = "renamed_" + count_file.split("/")[1]
        out_file = "renamed_" + count_file
        data.to_csv(out_file)





if __name__ == '__main__':

    csv_file = sys.argv[1]
    count_file = sys.argv[2]
    sample_info(csv_file,count_file)
