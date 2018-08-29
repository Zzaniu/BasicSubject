# coding=utf8

import os
import re
import sys
import zipfile
import datetime

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DEFAULT_DIR = r'C:\ImpPath\Sas'
PARAMETER = ('-a', '-s', '-r', '-rc', '-rd', '-f')


class FindStrToFile(object):
    def __init__(self, para):
        self.para = para
        self.para_list = []
        self.file_name = []
        self.find_str = []
        self.parsePara()

    def parsePara(self):
        para_cnt = len(self.para)
        if para_cnt < 1:
            print('程序运行错误，应该给程序至少1个参数，但是没有给...')
            sys.exit(-1)
        else:
            for _para in self.para:
                if _para.startswith('-') and len(_para) > 1:
                    self.para_list.append(_para.split('-')[1].lower())
                elif _para.startswith('>') and len(_para) > 1:
                    self.file_name.append(_para.split('>')[1])
                else:
                    self.find_str.append(_para)

            if self.para_list.count('?') + self.para_list.count('h') + self.para_list.count('help') > 1 or len(
                    self.find_str) > 1 or len(self.file_name) > 1 or len(self.para_list) > 3 or len(
                self.para_list) > len(set(self.para_list)):
                print('参数有误, 查看帮助请输入参数：-?/h/help')
                sys.exit(-1)

    def filterFile(self):
        para_file = 'all'
        para_path = DEFAULT_DIR
        para_time = datetime.datetime.now().strftime("%Y-%m-%d")
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
            'npts': 'Npts'
        }

        for para in self.para_list:
            _para_file = para_dict.get(para)
            if _para_file:
                para_file = _para_file
                continue
            _para_path = file_path_dict.get(para)
            if _para_path:
                para_path = os.path.join(r'C:\ImpPath', _para_path)
                continue
            _para_time = re.match("20[0-9][0-9](((([0][1,3,5,7,8])|([1][0,2]))(([0][1-9])|([1-2][0-9])|([3][0-1])))|((([0][1,4,6,9])|([1][1]))(([0][1-9])|([1-2][0-9])|([3][0])))|([0][2](([0][1-9])|([1][0-9])|([2][0-8]))))", para)
            if _para_time:
                para_time = "{}-{}-{}".format(para[:4], para[4:6], para[6:])

        file_lists = self.showFile(para_file, para_path, para_time)
        for file_name in file_lists:
            yield file_name

    def showFile(self, para_file, file_path, para_time):
        file_lists = []
        for root, dirs, files in os.walk(file_path):
            if root.endswith('InBox') > 0:
                for file_name in files:
                    if 'all' == para_file:
                        file_lists.append(os.path.join(root, file_name))
                    else:
                        if file_name.lower().startswith(para_file):
                            file_lists.append(os.path.join(root, file_name))
            if root.endswith(para_time):
                for file_name in files:
                    if 'all' == para_file:
                        file_lists.append(os.path.join(root, file_name))
                    else:
                        if file_name.lower().startswith(para_file):
                            file_lists.append(os.path.join(root, file_name))
        return file_lists

    def findFile(self):
        need_find = self.find_str[0]
        index = 0
        ret_file_list = []
        for shut_file_name in self.filterFile():
            index += 1
            full_file_name = os.path.join(DEFAULT_DIR, shut_file_name)
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
        print('格式与参数：-[?/h/help], -[a/s/r/f/rc/rd] -[sas/dec/npts] str -[20180827] >[输出文件名], 参数不区分位置、大小写，但字符串str区分大小写')
        print('?/h/help: 查看帮助信息')
        print('     a  : 查找目录下所有包含该字符串的文件，默认查找所有')
        print('     s  : 查找目录下Success开头且包含该字符串的文件')
        print('     r  : 查找目录下Receipt开头且包含该字符串的文件')
        print('     rc : 查找目录下Receipt_C开头且包含该字符串的文件')
        print('     rd : 查找目录下Receipt_D开头且包含该字符串的文件')
        print('     f  : 查找目录下Failed开头且包含该字符串的文件')
        print('    sas : 查找Sas文件夹下的目录，默认查找Sas')
        print('    dec : 查找DecCus001文件夹下的目录')
        print('   npts : 查找Npts文件夹下的目录')
        print('20180827: 查找日期文件夹下的目录，默认查找当天，6位日期')

    def run(self):
        if (self.para_list.count('?') == 1 or self.para_list.count('h') == 1 or self.para_list.count(
                'help') == 1) and len(self.para_list) == 1 and len(self.find_str) == 0:
            self.echo_help()
        else:
            file_names = self.findFile()
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
