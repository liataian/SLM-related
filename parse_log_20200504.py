#!/usr/bin/python
# -*- coding: utf-8 -*-
from os import listdir
from os.path import isfile, isdir, join
import socket
import time
import sys

#print('Number of arguments:', len(sys.argv), 'arguments.')
#print('Argument List:', str(sys.argv[1]))

#---------------------
wakeup_care = str(50)
file_check_end = []
path = "\\"
files = []
count = 0
ips = [] #Step 1
results = [] #Step 2-1
counts = [] #Step 2-2
zips = [] #Step 3
before_remove_dup = []
after_remove_dup = []
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
            with open(join(path, file), errors='ignore') as f: #忽略編碼error
                lines = f.readlines()
                for line in lines:
                    if 'src addr' in line: #如果該行有match的字串
                        l = line.split(" ") #切割該行
                        ip = l[len(l)-1].replace(":", ".").replace("\n", "") #將該行最後一個字串的:換成.，並且拿掉最後的\n
                        ips.append(ip) #加入到ips這個list
            continue
        else:
            continue
    print("")
    for ip in ips:
        results.append("{}".format(ip))
        counts.append("{}".format(ips.count(ip))) #計算ip出現的次數
    #print(results)
    #print(counts)
    zips = zip(counts, results) #結合兩個list，每個對應元素會合成一個sublist

    for z in zips:
        before_remove_dup.append(list(z))
    #print(before_remove_dup)

    after_remove_dup = list(set(tuple(i) for i in before_remove_dup)) #要用tuple跟set來移除重複元素
    #print(after_remove_dup)
    print("===Parse result: ===")
    for i in sorted(after_remove_dup, key = lambda x: int(x[0]), reverse=True): #以每個sublist中的第一個元素來排序，由大排到小
        if (int(i[0]) < int(wakeup_care)): #小於指定次數不管
            continue
        count = str(i[0])
        ip = str(i[1])
        try:
            domain_name = socket.gethostbyaddr(str(i[1]))[0] #詢問domain name
        except: #問不到的狀況，可能是local address或...
            print(" "+count+", "+ ip+", Parse fail")
            continue
        print(" "+count+", "+ ip+", "+domain_name)




def check_args():
    global path
    path = str(sys.argv[1])

    if (len(sys.argv) >= 3):
        global wakeup_care
        if(str(sys.argv[2]).startswith((".", "0")) or int(sys.argv[2]) <= 0): #判斷第二個參數是否有問題(開頭不能是.或0，一定要是數字且大於0)
            print("wakeup_care FAIL")
            return -1
        wakeup_care = str(sys.argv[2])

    if (len(sys.argv) >= 4):
        global file_check_end
        file_check_end.append(sys.argv[3:])
    #print("path="+path+", wakeup_care="+wakeup_care+", file_check_end="+str(file_check_end))
    return 0



def main():
    if (len(sys.argv) < 2 or check_args() < 0):
        print("===Usage===")
        print("python PYTHON_FILE LOG_PATH [wakup_count_above] [file_end_with] [file_end_with] ...")
        print("  [wakup_count_above] need > 0, default is 50")
        print("  [file_end_with] indicate we want to parse specified logcat.txt[file_end_with] so need give .05 or .06 or etc, default is all files")
        return -1
    parse()



if __name__== "__main__":
    main()