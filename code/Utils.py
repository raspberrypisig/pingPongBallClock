from neopixel import *

# LED strip configuration:
LED_PIN        = 18      # GPIO pin connected to the pixels (18 uses PWM!).
LED_COUNT      = 256
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 10       # DMA channel to use for generating signal (try 5)
LED_BRIGHTNESS = 125     # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL    = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53
LED_STRIP      = ws.WS2811_STRIP_GRB   # Strip type and colour ordering

# Define the rows the grid by defining the ball numbers 
ledAddresses = [
[999,999,999,3,16,17,30,31,44,45,58,59,72,73,86,87,100,101,114,115],    #0
[999,999,4,15,18,29,32,43,46,57,60,71,74,85,88,99,102,113,116,126],     #1
[999,2,5,14,19,28,33,42,47,56,61,70,75,84,89,98,103,112,117,125],      #2
[1,6,13,20,27,34,41,48,55,62,69,76,83,90,97,104,111,118,124,127],       #3
[0,7,12,21,26,35,40,49,54,63,68,77,82,91,96,105,110,119,123,999],       #4
[8,11,22,25,36,39,50,53,64,67,78,81,92,95,106,109,120,122,999,999],     #5
[9,10,23,24,37,38,51,52,65,66,79,80,93,94,107,108,121,999,999,999]      #6
]

class Ball:
	def __init__(self, location):   #location is a list of two variables, [row, col]
		self.location = location    #[row,col]
		self.ledNum = ledAddresses[self.location[0]][self.location[1]]   #[row,col]
		self.text = False           #this is used to determine whether the ball is being used for text display or not
		self.color = Color(0,0,0)   #current ball color

# Buffer
buffer = [                          # This is tricky and must be defined this way. I'm creating 7 instances of a list that contains 20 instances of Color(0,0,0). They must all be separately defined
	[Color(0,0,0)] * 20,
	[Color(0,0,0)] * 20,
	[Color(0,0,0)] * 20,
	[Color(0,0,0)] * 20,
	[Color(0,0,0)] * 20,
	[Color(0,0,0)] * 20,
	[Color(0,0,0)] * 20
]      

# -------------------------------------------------
# Fonts
#--------------------------------------------------

# Slanted Numeral Font ----------------------------
slanted = {}    #Define the slanted font dictionary

slanted[ord('0')] = [
	[1,1,1,0],
	[1,0,1,0],
	[1,0,1,0],
	[1,0,1,0],
	[1,1,1,0]
]
slanted[ord('1')] = [
	[0,0,1,0],
	[0,0,1,0],
	[0,0,1,0],
	[0,0,1,0],
	[0,0,1,0]
]
slanted[ord('2')] = [
	[1,1,1,0],
	[0,0,1,0],
	[1,1,1,0],
	[1,0,0,0],
	[1,1,1,0]
]
slanted[ord('3')] = [
	[1,1,1,0],
	[0,0,1,0],
	[0,1,1,0],
	[0,0,1,0],
	[1,1,1,0]
]
slanted[ord('4')] = [
	[1,0,1,0],
	[1,0,1,0],
	[1,1,1,0],
	[0,0,1,0],
	[0,0,1,0]
]
slanted[ord('5')] = [
	[1,1,1,0],
	[1,0,0,0],
	[1,1,1,0],
	[0,0,1,0],
	[1,1,1,0]
]
slanted[ord('6')] = [
	[1,0,0,0],
	[1,0,0,0],
	[1,1,1,0],
	[1,0,1,0],
	[1,1,1,0]
]
slanted[ord('7')] = [
	[1,1,1,0],
	[1,0,1,0],
	[0,0,1,0],
	[0,0,1,0],
	[0,0,1,0]
]
slanted[ord('8')] = [
	[1,1,1,0],
	[1,0,1,0],
	[1,1,1,0],
	[1,0,1,0],
	[1,1,1,0]
]
slanted[ord('9')] = [
	[1,1,1,0],
	[1,0,1,0],
	[1,1,1,0],
	[0,0,1,0],
	[0,0,1,0]
]
slanted[ord(' ')] = [
	[0,0,0,0],
	[0,0,0,0],
	[0,0,0,0],
	[0,0,0,0],
	[0,0,0,0]
]
slanted[ord('-')] = [
	[0,0,0,0],
	[0,0,0,0],
	[0,1,1,0],
	[0,0,0,0],
	[0,0,0,0]
]
slanted[ord(':')] = [
	[1,0],
	[0,0],
	[1,0],
	[0,0]
]
slanted[ord(';')] = [
	[0,0],
	[0,0],
	[0,0],
	[0,0]
]

# Digits Numeral Font ----------------------------
digits = {}    #Define the slanted font dictionary

digits[ord('0')]= [
	[1,1,0,0],
	[1,0,1,0],
	[1,0,0,1],
	[0,1,0,1],
	[0,0,1,1]
]
digits[ord('1')]= [
	[0,1,0,0],
	[0,1,0,0],
	[0,0,1,0],
	[0,0,1,0],
	[0,0,0,1]
]
digits[ord('2')]= [
	[1,1,0,0],
	[0,0,1,0],
	[0,1,1,0],
	[0,1,0,0],
	[0,0,1,1]
]
digits[ord('3')]= [
	[1,1,0,0],
	[0,0,1,0],
	[0,1,1,0],
	[0,0,0,1],
	[0,0,1,1]
]
digits[ord('4')]= [
	[1,0,0,0],
	[1,0,1,0],
	[1,1,1,0],
	[0,0,1,0],
	[0,0,0,1]
]
digits[ord('5')]= [
	[1,1,0,0],
	[1,0,0,0],
	[1,1,1,0],
	[0,0,0,1],
	[0,0,1,1]
]
digits[ord('6')]= [
	[0,1,0,0],
	[0,1,0,0],
	[0,1,1,0],
	[0,1,0,1],
	[0,0,1,1]
]
digits[ord('7')]= [
	[1,1,0,0],
	[0,0,1,0],
	[0,0,1,0],
	[0,0,1,0],
	[0,0,1,0]
]
digits[ord('8')]= [
	[1,1,0,0],
	[1,0,1,0],
	[0,1,1,0],
	[0,1,0,1],
	[0,0,1,1]
]
digits[ord('9')]= [
	[1,1,0,0],
	[1,0,1,0],
	[0,1,1,0],
	[0,0,1,0],
	[0,0,1,0]
]
digits[ord(' ')] = [
	[0,0,0,0],
	[0,0,0,0],
	[0,0,0,0],
	[0,0,0,0],
	[0,0,0,0]
]
digits[ord('-')] = [
	[0,0,0,0],
	[0,0,0,0],
	[0,1,1,0],
	[0,0,0,0],
	[0,0,0,0]
]
digits[ord(':')] = [
	[1,0],
	[0,0],
	[0,1],
	[0,0]
]
digits[ord(';')] = [
	[0,0],
	[0,0],
	[0,0],
	[0,0]
]