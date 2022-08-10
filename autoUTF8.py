# coding=<UTF-8>
# SPDX-FileCopyrightText: 2022 Darren <1912544842@qq.com>
# SPDX-License-Identifier: Apache-2.0

import os
import pprint
import shutil
import sys
import chardet
import codecs
import matplotlib.pyplot as plt

detect_file = ["c", "cpp", "h", "hpp", "cc"]
sum_dict = {"Unknown": 0}
err_dict = {}
DO_ENCODE = False


def find_all_file(base):
    for root, ds, fs in os.walk(base):
        for f in fs:
            if os.path.splitext(f)[-1][1:] in detect_file:
                fullname = os.path.join(root, f)
                yield fullname


def convert_file_to_utf8(infile, outfile):
    with open(infile, "rb") as f:
        data = f.read()
        try:
            t = chardet.detect(data)['encoding'].upper()
            if DO_ENCODE:
                print(infile + "[" + "\033[31m" + t + "\033[0m" + "]" + "==>" + outfile + "[\033[95mUTF-8\033[0m]")
                c = codecs.open(infile, "r", t).read()
                codecs.open(outfile, "w", "UTF-8").write(c)
            else:
                print(infile + "[" + "\033[31m" + t + "\033[0m" + "]")

            if t in sum_dict:
                sum_dict[t] += 1
            else:
                sum_dict[t] = 1
        except Exception as e:
            print("\033[31m" + infile + ":" + str(e) + "\033[0m")
            err_dict[infile] = str(e)
            sum_dict["Unknown"] += 1


def _main(base):
    if DO_ENCODE:
        if os.path.exists("./out"):
            print("found out/ remove it")
            shutil.rmtree("./out")
        shutil.copytree(base, "./out")
        print("copy ok")
    for i in find_all_file(base):
        convert_file_to_utf8(i, "./out/" + i.replace(base, "").replace("\\", "/"))
    print("encode ok")


if __name__ == '__main__':
    plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']
    plt.rcParams['axes.unicode_minus'] = False
    plt.figure(figsize=(12, 9))
    key = []
    val = []

    _main(sys.argv[1])
    pprint.pprint(sum_dict)
    print(err_dict)

    sum = sorted(sum_dict.items(), key=lambda d: d[1], reverse=False)
    for i in range(len(sum)):
        plt.bar(sum[i][0], sum[i][1])
        key.append(sum[i][0])
        val.append(sum[i][1])
    print(sum_dict)

    for a, b, i in zip(key, val, range(len(key))):
        plt.text(a, b, val[i], ha='center', fontsize=12)

    plt.title('Number of Files in Different Encoding Formats\n(Source Code Files of XXX Official Project)')
    # plt.xlabel("Format")
    plt.ylabel("Number of Files")
    plt.yscale('log')
    plt.xticks(rotation=20)
    plt.show()
