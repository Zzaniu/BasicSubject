# coding=utf8
###这个多线程写的是真JB垃圾。。。毫无意义###
import functools
import os
import re
import sys
import time
import zipfile
import datetime
import threading

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DEFAULT_DIR = r'C:\ImpPath\Sas'
PARAMETER = ('-a', '-s', '-r', '-rc', '-rd', '-f')


def used_time(f):
    """打印程序耗时"""
    @functools.wraps(f)
    def wrapper(*args, **kwargs):
        start = time.time()
        res = f(*args, **kwargs)
        end = time.time()
        print('used_time = ', end - start)
        return res
    return wrapper


class FindStrToFile(object):
    def __init__(self, para):
        self.para = para
        self.para_list = []
        self.out_file_name = []
        self.find_str = []
        self.file_names = []
        self.lock = threading.Lock()
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
                    self.out_file_name.append(_para.split('>')[1])
                else:
                    self.find_str.append(_para)

            if self.para_list.count('?') + self.para_list.count('h') + self.para_list.count('help') > 1 or len(
                    self.find_str) > 1 or len(self.out_file_name) > 1 or len(self.para_list) > 3 or len(
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
        print("len(file_lists) = ", len(file_lists))
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

    def findFile(self, index):
        print("index = ", index)
        need_find = self.find_str[0]
        ret_file_list = []
        while True:
            try:
                with self.lock:
                    full_file_name = self.files.__next__()
                print("full_file_name = ", full_file_name, 'threading.current_thread() = ', threading.current_thread(), 'index = ', index)
            except Exception as e:
                print('大爷好...', 'e = ', e)
                break
            if full_file_name.endswith('.zip'):  # 因为查找过程中，后台脚本有移动文件的动作，所以打开操作有可能会报错
                with zipfile.ZipFile(full_file_name) as f:
                    for name in f.namelist():
                        content = f.read(name).decode('utf8')
                        if content.find(need_find) > -1:
                            ret_file_list.append('_&_'.join([full_file_name, name]))
            else:
                with open(full_file_name, 'r', encoding='utf-8') as f:
                    content = f.read()
                    if content.find(need_find) > -1:
                        ret_file_list.append(full_file_name)

        return self.showFindRet(ret_file_list)

    def showFindRet(self, ret_file_list):
        """追加到列表中，多线程需要加锁操作"""
        with self.lock:
            self.file_names.extend(ret_file_list)
        return True

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

    @used_time
    def run(self):
        if (self.para_list.count('?') == 1 or self.para_list.count('h') == 1 or self.para_list.count(
                'help') == 1) and len(self.para_list) == 1 and len(self.find_str) == 0:
            self.echo_help()
        else:
            self.files = self.filterFile()
            t_list = []
            for i in range(4):
                t = threading.Thread(target=self.findFile, args=(i,))
                t.name = '线程{}'.format(i)
                t_list.append(t)
            for t in t_list:
                print('t.name = ', t.name)
                t.start()
            for t in t_list:
                t.join()
            if self.file_names:
                print('已找到相关文件，文件名是:')
                for file_name in self.file_names:
                    print(''.join(file_name))
            else:
                print('未找到相关文件...')


if __name__ == "__main__":
    obj = FindStrToFile(sys.argv[1:])
    obj.run()
    print('程序执行完毕...')
