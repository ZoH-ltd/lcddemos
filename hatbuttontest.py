#!/usr/bin/env python3
# coding: utf-8

import LCD_1in44
import LCD_Config
from lcdhat import HatKeys

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
from PIL import ImageColor

from gpiozero import Button, LED
from time import sleep
from signal import pause
import socket
import subprocess
import psutil

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


def put_logo():
	logo = Image.open('images/logo-RasPi.bmp')
	monofont10 = ImageFont.truetype('/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc', 10)

	image = Image.new("RGB", (LCD.width, LCD.height), "BLUE")
	draw = ImageDraw.Draw(image)
	rm = psutil.virtual_memory().total // (1024 * 1024)
	draw.text((24, 88), 'RAM:{}Mbytes'.format(rm), fill = "WHITE", font = monofont10)

	for i in range(47, -1, -3):
		lp = logo.crop((0, 0, 109, 54 - i))
		image.paste(lp, (9, 32 + i))

		LCD.LCD_ShowImage(image, 0, 0)

	LCD_Config.Driver_Delay_ms(500)

def key1_pressed():
	print("key1 pressed.")

def key2_pressed():
	print("key2 pressed.")

def key1b_pressed():
	print("キー1が押されました。")

def key2b_pressed():
	print("キー2が押されました。")

def key1_released():
	print("key1 released.")

def key2_released():
	print("key2 released.")


def key3_pressed():
	print("switch key-events.")
	hk.key1.when_pressed = None
	hk.key2.when_pressed = None
	LCD_Config.Driver_Delay_ms(100)

	key3_pressed.hk_sw = not key3_pressed.hk_sw
	if (key3_pressed.hk_sw):
		hk.key1.when_pressed = key1b_pressed
		hk.key2.when_pressed = key2b_pressed
	else:
		hk.key1.when_pressed = key1_pressed
		hk.key2.when_pressed = key2_pressed

def jkey_pressed():
	print("jkey pressed.")
	exit()


if __name__ == '__main__':
	LCD = LCD_1in44.LCD()
	if (LCD.LCD_Init(LCD_1in44.SCAN_DIR_DFT) != None):
		print("LCD Hat NOT set.")
		exit()

	put_logo()

	hk = HatKeys()
	key3_pressed.hk_sw = False

	hk.key1.when_pressed = key1_pressed
	hk.key2.when_pressed = key2_pressed

	hk.key1.when_released = key1_released
	hk.key2.when_released = key2_released

	hk.key3.when_pressed = key3_pressed

	hk.jkey.when_pressed = jkey_pressed

	pause()

