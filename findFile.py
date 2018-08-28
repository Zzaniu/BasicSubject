# coding=utf8

import os
import re
import sys
import zipfile
import datetime

import numpy as np
from collections import Counter

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PARAMETER = ('-a', '-s', '-r', '-rc', '-rd', '-f')


class FindStrToFile(object):
    def __init__(self, para):
        self.para = para
        print('self.args = ', self.para)

    def filterFile(self, file_lists, *args):
        para_dict = {
            'a': 'all',
            's': 'success',
            'r': 'receipt',
            'rc': 'receipt_c',
            'rd': 'receipt_d',
            'f': 'failed',
        }
        file_path_dict = {
            'sas': 'Sas',
            'dec': 'DecCus001',
        }
        for file_name in file_lists:
            if 'all' == para_dict.get(*args):
                yield file_name
            else:
                if file_name.lower().startswith(para_dict.get(args)):
                    yield file_name


    def findFile(self, need_find, *args):
        index = 0
        file_lists = os.listdir(BASE_DIR)
        ret_file_list = []
        for shut_file_name in self.filterFile(file_lists, *args):
            index += 1
            full_file_name = os.path.join(BASE_DIR, shut_file_name)
            if full_file_name.endswith('.zip'):
                with zipfile.ZipFile(full_file_name) as f:
                    for name in f.namelist():
                        content = f.read(name).decode('utf8')
                        if content.find(need_find) > -1:
                            ret_file_list.append('_&_'.join([shut_file_name, name]))
            else:
                with open(full_file_name, 'r', encoding='utf-8') as f:
                    content = f.read()
                    if content.find(need_find) > -1:
                        ret_file_list.append(shut_file_name)

        return tuple(ret_file_list)

    @staticmethod
    def echo_help():
        print('功能：查找所有包含传入字符串的文件')
        print('格式与参数：-[?/h/help], -[a/s/r/f/rc/rd] -[sas/dec] str [20180827] >[输出文件名], 参数不区分大小写，但字符串str区分大小写')
        print('?/h/help: 查看帮助信息')
        print('     a  : 查找目录下所有包含该字符串的文件，默认查找所有')
        print('     s  : 查找目录下Success开头且包含该字符串的文件')
        print('     r  : 查找目录下Receipt开头且包含该字符串的文件')
        print('     rc : 查找目录下Receipt_C开头且包含该字符串的文件')
        print('     rd : 查找目录下Receipt_D开头且包含该字符串的文件')
        print('     f  : 查找目录下Failed开头且包含该字符串的文件')
        print('    sas : 查找Sas文件夹下的目录，默认查找Sas')
        print('    dec : 查找DecCus001文件夹下的目录')
        print('20180827: 查找日期文件夹下的目录，默认查找当天，6位日期')

    def run(self):
        file_names = None
        para_cnt = len(self.para)
        if para_cnt < 1:
            print('程序运行错误，应该给程序至少1个参数，但是没有给...')
            sys.exit(-1)
        else:
            para_list = []
            file_name = []
            find_str = []
            for _para in self.para:
                if _para.startswith('-') and len(_para) > 1:
                    para_list.append(_para.split('-')[1])
                elif _para.startswith('>') and len(_para) > 1:
                    file_name.append(_para.split('>')[1])
                else:
                    find_str.append(_para)

            if para_list.count('?') + para_list.count('h') + para_list.count('help') > 1 or len(find_str) > 1 or len(file_name) > 1:
                print('参数有误, 查看帮助请输入参数：-?/h/help')
                sys.exit(-1)

            if 1 == para_cnt:
                if para_list[0].lower() in ('-?', '-h', '-help'):
                    self.echo_help()
                    sys.exit(0)
                else:
                    file_names = self.findFile(find_str[0], *para_list, *file_name)

            if file_names:
                print('已找到相关文件，文件名是:')
                for file_name in file_names:
                    print(''.join(file_name))
            else:
                print('未找到相关文件...')


if __name__ == "__main__":
    obj = FindStrToFile(sys.argv[1:])
    obj.run()
    print('程序执行完毕...')
