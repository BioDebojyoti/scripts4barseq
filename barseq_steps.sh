#!/bin/bash

./barseq.py --input ../POOL4 --barcodes barcode_gene_file.csv --result POOL4_RESULT

./remove_zero_barseq_count.py barcode_counts_table.csv wo_zero_row_col_barcode_counts_table.csv

./expected_genes_count_tables.py wo_zero_row_col_barcode_counts_table.csv ../pool4_gene_list.csv

# if number of rows greater than expected number of genes
# manual filtering required
# remove the duplicate gene entries with zero counts!
# For example:
# awk -F, '{print $2}' expected_wo_zero_row_col_barcode_counts_table.csv | sort | uniq -c | awk '{if($1!=1) printf $2" "}END{printf "\n"}'
# grep -n -e PBANKA_030600 -e PBANKA_031230 -e PBANKA_111270 -e PBANKA_143160 expected_wo_zero_row_col_barcode_counts_table.csv
# sed -i '2d' expected_wo_zero_row_col_barcode_counts_table.csv # remove duplicates one by one or in a loop

./adding_read_counts.py expected_wo_zero_row_col_barcode_counts_table.csv

./replace_ngi_id_sample_name.sh total_sample_counts_expected_wo_zero_row_col_barcode_counts_table.csv ../pool4_ngi_sampleID_sampleID.csv

./log_normalized_heatmap_with_dendogram.py total_sample_counts_expected_wo_zero_row_col_barcode_counts_table.csv

./genes_percent_reads.py total_sample_counts_expected_wo_zero_row_col_barcode_counts_table.csv

./time_plot.py total_sample_counts_expected_wo_zero_row_col_barcode_counts_table.csv

./normalization.py total_sample_counts_expected_wo_zero_row_col_barcode_counts_table.csv

./pca.py normalized_total_sample_counts_expected_wo_zero_row_col_barcode_counts_table.csv
