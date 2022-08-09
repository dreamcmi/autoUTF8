# coding=<UTF-8>
# SPDX-FileCopyrightText: 2022 Darren <1912544842@qq.com>
# SPDX-License-Identifier: Apache-2.0

import os
import pprint
import shutil
import sys
import chardet
import codecs

sum_dict = {}
err_dict = {}


def find_all_file(base):
    for root, ds, fs in os.walk(base):
        for f in fs:
            if f.endswith('.c') or f.endswith('.h') or f.endswith('.cpp') or f.endswith('.hpp') or f.endswith('.cc'):
                fullname = os.path.join(root, f)
                yield fullname


def convert_file_to_utf8(infile, outfile):
    with open(infile, "rb") as f:
        data = f.read()
        t = chardet.detect(data)['encoding'].upper()
        if t in sum_dict:
            sum_dict[t] += 1
        else:
            sum_dict[t] = 1
        try:
            c = codecs.open(infile, "r", t).read()
            codecs.open(outfile, "w", "UTF-8").write(c)
            print(infile + "[" + "\033[31m" + t + "\033[0m" + "]" + "==>" + outfile + "[\033[95mUTF-8\033[0m]")
        except Exception as e:
            print("\033[31m" + infile + ":" + str(e) + "\033[0m")
            err_dict[infile] = str(e)
        f.close()


def _main(base):
    if os.path.exists("./out"):
        print("found out/ remove it")
        shutil.rmtree("./out")
    shutil.copytree(base, "./out")
    print("copy ok")
    for i in find_all_file(base):
        convert_file_to_utf8(i, "./out/" + i.replace(base, "").replace("\\", "/"))
    print("encode ok")


if __name__ == '__main__':
    _main(sys.argv[1])
    pprint.pprint(sum_dict)
    print(err_dict)
