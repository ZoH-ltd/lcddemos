# coding: utf-8

from gpiozero import Button

class HatKeys:
	def __init__(self):
		self.key1  = Button(21)
		self.key2  = Button(20)
		self.key3  = Button(16)

		self.up    = Button(6)
		self.down  = Button(19)
		self.left  = Button(5)
		self.right = Button(26)

		self.jkey  = Button(13)

	def resetKeyEvents(self):
		self.key1  .when_pressed = None
		self.key2  .when_pressed = None
		self.key3  .when_pressed = None

		self.up    .when_pressed = None
		self.down  .when_pressed = None
		self.left  .when_pressed = None
		self.right .when_pressed = None

		self.jkey  .when_pressed = None

		self.key1  .when_released = None
		self.key2  .when_released = None
		self.key3  .when_released = None

		self.up    .when_released = None
		self.down  .when_released = None
		self.left  .when_released = None
		self.right .when_released = None

		self.jkey  .when_released = None

