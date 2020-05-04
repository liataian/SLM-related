#!/usr/bin/python
# -*- coding: utf-8 -*-
from os import listdir
from os.path import isfile, isdir, join
import socket
import time
import sys
import csv

#print('Number of arguments:', len(sys.argv), 'arguments.')
#print('Argument List:', str(sys.argv[1]))

#---------------------
file_check_end = []
path = "./"
files = []
count = 0

new_ratios_wifi = []
new_ratios_mobile = []
lres_wifi = []
lres_mobile = []

ratio_lists = []
lre_lists = []
#---------------------


def parse():
    print()
    print("===Start to parse below files: ===")
    global path, files, ips, results, counts, zips, before_remove_dup, after_remove_dup

    if (len(file_check_end) > 0): #如果有指定要parse目錄下的哪些檔案
        for file in listdir(path):
            if (file.endswith(tuple(file_check_end[0]))): #確認檔名結尾符合指定結尾(例如logca.txt.05或logcat.txt.06等等)
                files.append(file) #加入到files這個list
    else: #預設目錄下的檔案全部都要parse
        files = listdir(path) #全部目錄下的檔案都加入files這個list

    for file in files:
        if file.startswith("logcat.txt"): #如果檔名開頭是logcat.txt
            print(" "+join(path, file))
            with open(join(path, file)) as f: #忽略編碼error
                lines = f.readlines()
                for line in lines:
                    if 'SLA_ASUS_PARSE' in line: #如果該行有match的字串
                        l = line.split(",") #切割該行

                        if 'wlan' in line: #如果是wlan
                            new_ratios_wifi.append(l[3])
                            lres_wifi.append(l[4])

                        if 'rmnet' in line: #如果是mobile
                            new_ratios_mobile.append(l[3])
                            lres_mobile.append(l[4])
            continue
        else:
            continue
    print("")

    #Output LRE to csv file+++
    zips_lre = zip(lres_wifi, lres_mobile)
    for lre in zips_lre: #Transfer from "set" to "list" for output csv file purpose
        lre_lists.append(list(lre))

    with open('output_lre.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['wifi', 'mobile'])
        for lre_list in lre_lists:
            writer.writerow(lre_list)
    #Output LRE to csv file---

    #Output RATIO to csv file+++
    zips_ratio = zip(new_ratios_wifi, new_ratios_mobile)
    for ratio in zips_ratio: #Transfer from "set" to "list" for output csv file purpose
        ratio_lists.append(list(ratio))

    with open('output_ratio.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['wifi', 'mobile'])
        for ratio_list in ratio_lists: 
            writer.writerow(ratio_list)
    #Output RATIO to csv file---


def check_args():
    global path
    path = str(sys.argv[1])
    if (len(sys.argv) > 2):
        global file_check_end
        file_check_end.append(sys.argv[2:])

    print("path="+path+", file_check_end="+str(file_check_end))
    return 0


def main():
    if (len(sys.argv) < 2 or check_args() < 0):
        print("===Usage===")
        print("python PYTHON_FILE LOG_PATH [file_end_with] [file_end_with] ...")
        print("  [file_end_with] indicate we want to parse specific logcat.txt[file_end_with], so need give .05 or .06 or etc, default is all files")
        return -1
    parse()


if __name__== "__main__":
    main()
