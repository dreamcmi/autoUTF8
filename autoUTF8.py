# coding=<UTF-8>
# SPDX-FileCopyrightText: 2022 Darren <1912544842@qq.com>
# SPDX-License-Identifier: Apache-2.0

import json
import os
import pprint
import shutil
import sys
import chardet
import codecs

detect_file = ["c", "cpp", "h", "hpp", "cc"]
sum_dict = {}
err_dict = {}
file_dict = {}
DO_ENCODE = True


def find_all_file(base):
    for root, ds, fs in os.walk(base):
        for f in fs:
            if os.path.splitext(f)[-1][1:] in detect_file:
                fullname = os.path.join(root, f)
                yield fullname


# TODO:
#  The result of detection mode and encoding mode will be different
#  because the encoding mode will have one more read and write operation
def convert_file_to_utf8(infile, outfile):
    with open(infile, "rb") as f:
        data = f.read()
        try:
            t = chardet.detect(data)['encoding'].upper()
        except Exception as e:
            print("\033[31m" + infile + ":" + str(e) + "\033[0m")
            err_dict[infile] = str(e)
            if "Unknown" not in sum_dict:
                sum_dict["Unknown"] = 1
            else:
                sum_dict["Unknown"] += 1
        try:
            if DO_ENCODE:
                print(infile + "[" + "\033[31m" + t + "\033[0m" + "]" + "==>" + outfile + "[\033[95mUTF-8\033[0m]")
                c = codecs.open(infile, "r", t).read()
                codecs.open(outfile, "w", "UTF-8").write(c)
            else:
                print(infile + "[" + "\033[31m" + t + "\033[0m" + "]")
            #  coding type count
            if t in sum_dict:
                sum_dict[t] += 1
            else:
                sum_dict[t] = 1
            # file coding type record
            if t in file_dict:
                file_dict[t].append(infile)
            else:
                file_dict[t] = []
                file_dict[t].append(infile)
        except Exception as e:
            print("\033[31m" + infile + ":" + str(e) + "\033[0m")
            err_dict[infile] = str(e)
            if "Unknown" not in sum_dict:
                sum_dict["Unknown"] = 1
            else:
                sum_dict["Unknown"] += 1
            if "Unknown" not in file_dict:
                file_dict[t] = []
                file_dict[t].append(infile)
            else:
                file_dict[t].append(infile)


def _main(base, name="XXX"):
    if DO_ENCODE:
        if os.path.exists("./out"):
            print("found out/ remove it")
            shutil.rmtree("./out")
        shutil.copytree(base, "./out")
        print("copy ok")
    else:
        print("start detect")
    for i in find_all_file(base):
        convert_file_to_utf8(i, "./out/" + i.replace(base, "").replace("\\", "/"))
    print("encode ok")
    pprint.pprint(sum_dict)

    with open("%s_LOG.json" % name, "w", encoding="UTF-8") as f:
        json.dump(file_dict, f, ensure_ascii=False, indent=4)
        f.close()
    with open("%s_SUM.json" % name, "w", encoding="UTF-8") as f:
        json.dump(sum_dict, f, ensure_ascii=False, indent=4)
        f.close()
    with open("%s_ERR.json" % name, "w", encoding="UTF-8") as f:
        json.dump(err_dict, f, ensure_ascii=False, indent=4)
        f.close()


if __name__ == '__main__':
    _main(base=sys.argv[1])
