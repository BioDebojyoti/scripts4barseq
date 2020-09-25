#!/usr/bin/env bash

COUNT_FILE=$1
NGI_SAMPLID_FILE=$2

IFS=$'\n';

for line in `awk 'BEGIN{FS=",";}NR>1{print $1"\t"$2}' $NGI_SAMPLID_FILE`;
  do
    search=$(echo $line| awk '{print $1}');
    replacement=$(echo $line| awk 'BEGIN{FS="\t"}{print $2}');
    gsed -i "s:${search}:${replacement}:g" $COUNT_FILE;
  done
