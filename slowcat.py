#!/usr/bin/env python3
# coding=utf-8

import sys
from time import sleep

""" 文字の表示間隔(sec) """
PUTCHAR_INTERVAL = 1 / (400 / 8)

def slowcat_char(c):
	"""
	文字を、コンソールにゆっくり出力する。
	"""
	sys.stdout.write(c)
	sys.stdout.flush()
	sleep(PUTCHAR_INTERVAL)

def slowcat_line(line, addNewLine = True):
	"""
	文字列(1行)を、コンソールにゆっくり出力する。
	"""
	for c in list(line):
		slowcat_char(c)
	if (addNewLine):
		slowcat_char('\n')

def slowcat_string(s):
	"""
	文字列(複数行)を、コンソールにゆっくり出力する。
	"""
	for line in list(s):
		slowcat_char(line)

def main():
	if (len(sys.argv) > 1):
		# 引数(=ファイルパス)が指定されている場合、そのファイルの内容を出力。
		with open(sys.argv[1], 'r') as f:
#			for line in f:
#				slowcat_line(line, False)
			while True:
				line = f.readline()
				if not line:
					break
				slowcat_line(line, False)
	else:
		# 引数(=ファイルパス)が指定されていない場合、標準入力の内容を出力。
		slowcat_string(sys.stdin.read())

if __name__ == "__main__":
	main()
