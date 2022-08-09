# coding=<UTF-8>
# SPDX-FileCopyrightText: 2022 Darren <1912544842@qq.com>
# SPDX-License-Identifier: Apache-2.0

import os
import shutil
import sys

import chardet
import codecs


def find_all_file(base):
    for root, ds, fs in os.walk(base):
        for f in fs:
            fullname = os.path.join(root, f)
            yield fullname


def convert_file_to_utf8(infile, outfile):
    with open(infile, "rb") as f:
        data = f.read()
        t = chardet.detect(data)['encoding']
        c = codecs.open(infile, "r", t.upper()).read()
        codecs.open(outfile, "w", "UTF-8").write(c)
        print(infile + "[" + "\033[31m" + t.upper() + "\033[0m" + "]" + "==>" + outfile + "[\033[95mUTF-8\033[0m]")
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
