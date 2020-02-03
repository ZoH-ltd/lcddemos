#!/usr/bin/env python3
# coding=utf-8

import sys
import psutil

""" 監視の間隔(sec) """
WATCH_INTERVAL = 2

def get_net_bytes():
	""" ネットワーク使用量を返す。
	"""
	net_per = psutil.net_io_counters()
	return net_per.bytes_sent + net_per.bytes_recv

if __name__ == "__main__":
	# 監視開始前のネットワーク使用量を取得。
	net_byte_prev = get_net_bytes()

	while True:
		# 各種監視データを取得。
		# ※CPU使用量の取得において、監視間隔も設定。
		cpu_per  = psutil.cpu_percent(interval=WATCH_INTERVAL)
		cpu_freq = psutil.cpu_freq()
		cpu_temp = psutil.sensors_temperatures()['cpu-thermal'][0].current
		mem      = psutil.virtual_memory()
		net_byte = get_net_bytes()

		# 取得したデータのうち、必要な内容を画面表示する。
		line = 'CPU:{p:>5.1f}% ({f:>6.1f}MHz:{t:>5.1f}C),  MEM:{m:>5.1f}%,  NET:{n:>9.2f}KB/sec' \
		.format( \
			p = cpu_per, \
			f = cpu_freq.current, \
			t = cpu_temp, \
			m = mem.percent, \
			n = (net_byte - net_byte_prev) / (1024 * WATCH_INTERVAL) \
		)
#		print(line)
		# 単純な print-line ではなく、表示行を上書きするように表示。
		sys.stdout.write('\r' + line)
		sys.stdout.flush()

		# 現在のネットワーク使用量を保存。
		net_byte_prev = net_byte
