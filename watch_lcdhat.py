#!/usr/bin/env python3
# coding: utf-8

import LCD_1in44
import LCD_Config
from lcdhat import HatKeys
import lcdhat_module

import sys
import signal

#from gpiozero import Button, LED
from time import sleep
import subprocess


def key1_pressed():
	lcdhat_module.drawtest(LCD)

def key2_pressed():
	lcdhat_module.put_bitmap(LCD, 'images/sky.bmp')

def key3_pressed():
	lcdhat_module.put_bitmap(LCD, 'images/goodbye.bmp')
	hk.resetKeyEvents()
	sleep(2)
	LCD.LCD_Clear()
	sys.exit()

def jkey_pressed():
	lcdhat_module.put_bitmap(LCD, 'images/goodbye.bmp')
	hk.resetKeyEvents()
	sleep(2)
	LCD.LCD_Clear()
	print("shutdown.")
	subprocess.call(['sudo', 'shutdown', '0'])
	sys.exit()


if __name__ == '__main__':
	# LCDを初期化する。
	LCD = LCD_1in44.LCD()
	if (LCD.LCD_Init(LCD_1in44.SCAN_DIR_DFT) != None):
		print("LCD Hat NOT set.")
		sys.exit()

	# ロゴを表示する。
	lcdhat_module.put_logo(LCD)

	# キーイベントをバインドする。
	hk = HatKeys()
	hk.key1.when_pressed = key1_pressed
	hk.key2.when_pressed = key2_pressed
	hk.key3.when_pressed = key3_pressed
	hk.jkey.when_pressed = jkey_pressed

#	bl = LED(LCD_Config.LCD_BL_PIN)
#	while(True):
#		print "backlight on."
#		bl.on()
#		sleep(3)
#		print "backlight off."
#		bl.off()
#		sleep(0.5)

	# プログラムを待ち状態にする。
	signal.pause()

