# coding=utf8
import functools
import os
import re
import sys
import time
import zipfile
import datetime
from multiprocessing import Process, Queue, Lock, JoinableQueue

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


class findFile(object):
    def __init__(self):
        self.input_Q = JoinableQueue()
        self.out_Q = JoinableQueue()

    def run(self):
        p1 = Process(target=self.funcA())
        p2 = Process(target=self.funcB())
        p3 = Process(target=self.funcB())
        p1.start()
        p2.start()
        p3.start()
        p1.join()
        p2.join()
        p3.join()
        self.input_Q.join()
        l = []
        while self.out_Q.empty() is False:
            l.append(self.out_Q.get())
        print('l = ', l)
        print("p1.is_alive() = ", p1.is_alive())
        print("p2.is_alive() = ", p2.is_alive())
        print("p3.is_alive() = ", p3.is_alive())

    def funcA(self):
        while True:
            find_str = input('请输入要查找的字符串:')
            if 'exit' == find_str.lower():
                break
            self.input_Q.put(find_str)

    def funcB(self):
        while True:
            if self.input_Q.empty():
                break
            find_str = self.input_Q.get()
            self.out_Q.put(find_str)
            print('find_str = ', find_str)
            self.input_Q.task_done()


if __name__ == "__main__":
    a = findFile()
    a.run()
    print('程序执行完毕...')
