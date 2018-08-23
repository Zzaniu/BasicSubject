# coding=utf8

import os
import sys


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PARAMETER = ('-a', '-s', '-r', '-rc', '-rd', '-f')


def reName():
	file_list = os.listdir(BASE_DIR)

	for i in file_list:
		os.rename(os.path.join(file_dir, i), os.path.join(file_dir, file_name))


def filterFile(file_lists, flag):
	a_dict = {'-a': 'all', '-s': 'success', '-r': 'receipt', '-rc': 'receipt_c', '-rd': 'receipt_d', '-f': 'failed'}
	for file_name in file_lists:
		if 'all' == a_dict.get(flag):
			yield file_name
		else:
			if file_name.lower().startswith(a_dict.get(flag)):
				yield file_name


def findFile(need_find, contains_file='-a'):
	index = 0
	file_lists = os.listdir(BASE_DIR)
	ret_file_list = []
	for shut_file_name in filterFile(file_lists, contains_file):
		index += 1
		full_file_name = os.path.join(BASE_DIR, shut_file_name)
		with open(full_file_name, 'r', encoding='utf-8') as f:
			content = f.read()
			if content.find(need_find) > -1:
				ret_file_list.append(shut_file_name)
				
	return tuple(ret_file_list)


def echo_help():
	print('功能：查找所有包含传入字符串的文件')
	print('格式与参数：-[?/h/help], -[a/s/S/r/R/f/F] str, 参数不区分大小写，但字符串str区分大小写')
	print('?/h/help: 查看帮助信息')
	print('     a: 查找所有包含该字符串的文件')
	print('     s  : 查找Success开头且包含该字符串的文件')
	print('     r  : 查找Receipt开头且包含该字符串的文件')
	print('     rc : 查找Receipt_C开头且包含该字符串的文件')
	print('     rd : 查找Receipt_D开头且包含该字符串的文件')
	print('     f  : 查找Failed开头且包含该字符串的文件')


if __name__ == "__main__":
	file_names = None
	para_cnt = len(sys.argv)
	if para_cnt < 2:
		print('程序运行错误，应该给程序至少1个参数，但是没有给...')
		sys.exit(-1)
	else:
		if para_cnt > 3:
			print('给的参数个数大于2个，第3个参数以及后面的参数将被忽略...')
		if 2 == para_cnt:
			if sys.argv[1].lower() in ('-?', '-h', '-help'):
				echo_help()
				sys.exit(0)
			else:
				file_names = findFile(sys.argv[1])
		if 3 == para_cnt:
			if sys.argv[1].lower() in PARAMETER:
				file_names = findFile(sys.argv[2], contains_file=sys.argv[1].lower())
			else:
				print('参数错误，查看帮助请输入参数：?/h/help')
				
		if file_names:
			print('已找到相关文件，文件名是:')
			for file_name in file_names:
				print(''.join(file_name))
		else:
			print('未找到相关文件...')
	print('程序执行完毕...')
