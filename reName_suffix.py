#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018-08-31 14:01:44
# @Author  : zaniu (Zzaniu@126.com)
# @Version : $Id$

import os
import sys


def reName(file_path, suffix):
    file_list = os.listdir(file_path)
    for shut_file_name in file_list:
    	if 'reName_suffix.py' != shut_file_name:
	        new_shut_file_name = shut_file_name.split(".")[0] + "." + suffix
	        os.rename(os.path.join(file_path, shut_file_name), os.path.join(file_path, new_shut_file_name))


def run(*args):
    if len(*args) != 2:
        print('要有两个参数')
        sys.exit(-1)
    else:
        for i in args:
            file_path, suffix = i
        reName(file_path, suffix)


if __name__ == "__main__":
    run(sys.argv[1:])
