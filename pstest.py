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

def ps_watch():
	""" psutil によりシステム状態を監視する。
	"""
	# 監視開始前のネットワーク使用量を取得。
	net_byte_prev = get_net_bytes()

	while True:
		# 各種監視データを取得。
		# ※CPU使用量の取得において、監視間隔も設定。
		cpu_per  = psutil.cpu_percent(interval=WATCH_INTERVAL)
		cpus_per = psutil.cpu_percent(interval=None, percpu=True)
		cpu_freq = psutil.cpu_freq()
		cpu_temp = psutil.sensors_temperatures()['cpu-thermal'][0].current
		mem      = psutil.virtual_memory()
		net_byte = get_net_bytes()

		# 表示用の内容に整形。
		# ○CPU:稼働率
		cpus_disp = ''
		for core_per in cpus_per:
			if cpus_disp != '':
				cpus_disp += ':'
			cpus_disp += '{p:>3.0f}'.format(p = core_per)
		cpu_disp  = '{:>5.1f}%'.format(cpu_per)

		# ○CPU:動作クロック&温度
		cpu_disp += '[' + cpus_disp + ']'
		cpu_disp += ' ({f:>6.1f}MHz:{t:>5.1f}C)'.format(f = cpu_freq.current, t = cpu_temp)

		# ○ネットワーク
		n_val  = (net_byte - net_byte_prev) / (1024 * WATCH_INTERVAL / 8)
		n_unit = "K"
		if n_val > 1280:
			n_val = n_val / 1024
			n_unit = "M"
		net_disp = '{nv:>7.2f}{nu}bps/sec'.format(nv = n_val, nu = n_unit)

		# 取得したデータのうち、必要な内容を画面表示する。
		line = 'CPU:{p},  MEM:{m:>5.1f}%,  NET:{n}' \
		.format( \
			p = cpu_disp, \
			m = mem.percent, \
			n = net_disp \
		)
#		print(line)
		# 単純な print-line ではなく、表示行を上書きするように表示。
		sys.stdout.write('\r' + line)
		sys.stdout.flush()

		# 現在のネットワーク使用量を保存。
		net_byte_prev = net_byte

if __name__ == "__main__":
	ps_watch()
