# coding: utf-8

import LCD_1in44
import LCD_Config

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
from PIL import ImageColor

import psutil

import socket
import subprocess


def put_logo(LCD):
	""" ロゴを表示する。
	"""
	# ロゴ画像を取得。
	logo = Image.open('images/logo-RasPi.bmp')
	# フォントを定義。
	monofont10 = ImageFont.truetype('/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc', 10)

	# ベース部分のイメージを生成する。
	# ・青背景にRAM容量を表示。
	image = Image.new("RGB", (LCD.width, LCD.height), "BLUE")
	draw = ImageDraw.Draw(image)
	rm = psutil.virtual_memory().total // (1024 * 1024)
	draw.text((24, 88), 'RAM:{m}Mbytes'.format(m=rm), fill = "WHITE", font = monofont10)

	# ロゴが下からスクロールして出てくるようなアニメーションを行う。
	for i in range(47, -1, -3):
		lp = logo.crop((0, 0, 109, 54 - i))
		image.paste(lp, (9, 32 + i))

		LCD.LCD_ShowImage(image, 0, 0)

	LCD_Config.Driver_Delay_ms(500)


def put_bitmap(LCD, src):
	""" 画像を表示する。
	"""
	image = Image.open(src)
	LCD.LCD_ShowImage(image, 0, 0)


def getIpv4Addresses():
	addresses = []

	cmd = "./get_ipaddr.sh"
	p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	p.wait()
	o, e = p.communicate()
	lines = o.decode().split('\n')
	for line in lines:
		if '127.0.0.1' in line:
			continue
		if ':' in line:
			continue
		addresses.append(line)

	return addresses

def drawtest(LCD):
	image = Image.new("RGB", (LCD.width, LCD.height), "BLACK")
	draw = ImageDraw.Draw(image)

	draw.line([(0,0),(127,0)], fill = "BLUE",width = 5)
	draw.line([(127,0),(127,127)], fill = "BLUE",width = 5)
	draw.line([(127,127),(0,127)], fill = "BLUE",width = 5)
	draw.line([(0,127),(0,0)], fill = "BLUE",width = 5)

	draw.rectangle([(18,10),(110,20)],fill = "RED")

	draw.font = ImageFont.truetype('/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc', 10)
	draw.text((33, 22), 'WaveShare ', fill = "BLUE")
	draw.text((32, 36), 'Electronic ', fill = "BLUE")
	draw.text((28, 48), '1.44inch LCD ', fill = "BLUE")

	hostname = socket.gethostname()
	draw.text((12, 72), hostname, fill = "WHITE")

	addresses = getIpv4Addresses()
	if len(addresses) > 0:
		draw.text((12, 82), addresses[0], fill = "WHITE")

	LCD.LCD_ShowImage(image, 0, 0)
	LCD_Config.Driver_Delay_ms(500)


if __name__ == '__main__':
	# LCDを初期化する。
	LCD = LCD_1in44.LCD()
	if (LCD.LCD_Init(LCD_1in44.SCAN_DIR_DFT) != None):
		print("LCD Hat NOT set.")
		exit()

	# ロゴを表示する。
	put_logo(LCD)

	# 終了までちょっとWAIT。
	LCD_Config.Driver_Delay_ms(3000)

