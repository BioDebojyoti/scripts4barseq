import pandas as pd
import sys, re

def view_csv(csv_file):
    data = pd.read_csv(csv_file)
    cols = data.columns
    rows = data.index
    print(len(set(data[cols[1]].values)))

    for i in range(len(rows)):
        replacement = re.search(r'PBANKA_\d+', data[cols[1]].values[i])
        data[cols[1]].values[i] = replacement[0]


    output_file = "renamed_" + csv_file
    data.to_csv(output_file)

if __name__ == '__main__':
    csv_file = sys.argv[1]

view_csv(csv_file)
