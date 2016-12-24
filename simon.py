# Simon says game, by Felix Leger (october 25 2016)

# Config for your breadboard:
# 	Top LED=GPIO 18
# 	Right LED=GPIO 19
# 	Left LED=GPIO 20
# 	Bottom LED=GPIO 21

import RPi.GPIO as GPIO
import time
import random


# Reads a single character from user input. Stolen from here: http://code.activestate.com/recipes/134892-getch-like-unbuffered-character-reading-from-stdin/
class _Getch:
    """Gets a single character from standard input.  Does not echo to the
screen."""
    def __init__(self):
        try:
            self.impl = _GetchWindows()
        except ImportError:
            self.impl = _GetchUnix()

    def __call__(self): return self.impl()


class _GetchUnix:
    def __init__(self):
        import tty, sys

    def __call__(self):
        import sys, tty, termios
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch


class _GetchWindows:
    def __init__(self):
        import msvcrt

    def __call__(self):
        import msvcrt
        return msvcrt.getch()

getch = _Getch()


# Flash a LED n seconds
def flash (l, n):
	GPIO.output(l+18,GPIO.HIGH) # The +18 is because the numbering scheme of the GPIO pins begins at 18
	time.sleep(n)
	GPIO.output(l+18,GPIO.LOW)
	return;

# Flash the LEDs n times
def flash_all (n):
	for i in range (0,n):
		GPIO.output(18,GPIO.HIGH)
		GPIO.output(19,GPIO.HIGH)
		GPIO.output(20,GPIO.HIGH)
		GPIO.output(21,GPIO.HIGH)
		time.sleep(0.3)
		GPIO.output(18,GPIO.LOW)
		GPIO.output(19,GPIO.LOW)
		GPIO.output(20,GPIO.LOW)
		GPIO.output(21,GPIO.LOW)
		time.sleep(0.3)
	return;

# Verify if user input matches value in expected sequence	
def correct_input (wasd, value):
	if wasd == 'w':
		converted_wasd=0
	elif wasd == 'd':
		converted_wasd=1
	elif wasd == 's':
		converted_wasd=2
	elif wasd == 'a':
		converted_wasd=3
	else:
		return 0

	if converted_wasd == value:
		return 1
	else:
		return 0

#####################################
# MAIN PROGRAM, a game of simon says#
#####################################
def main():
	random.seed()	# Different seed for every game
	count=0	# Keeps track of player score
	sequence = [] # Will contain the sequence of light for the simon says

	print "Simon Says, the game! Control with wasd keys on your keyboard. Good luck!"

	# Setup the GPIO
	GPIO.setmode(GPIO.BCM)
	GPIO.setup(18,GPIO.OUT)
	GPIO.setup(19,GPIO.OUT)
	GPIO.setup(20,GPIO.OUT)
	GPIO.setup(21,GPIO.OUT)

	# Start with lights off
	GPIO.output(18,GPIO.LOW)
	GPIO.output(19,GPIO.LOW)
	GPIO.output(20,GPIO.LOW)
	GPIO.output(21,GPIO.LOW)

	while True :
		time.sleep(1)
		new_value=random.randint(0,3)
		sequence.append(new_value)
		for i in range (0,len(sequence)):
			flash(sequence[i],0.4)
			time.sleep(0.1)
		for i in range (0,len(sequence)):
			status=correct_input(getch.impl(),sequence[i])
			if status == 1:
				flash(sequence[i],0.1)
			else:
				flash_all(5)
				break
		else:
			count+=1
			continue
		break

	# End with lights off
	GPIO.output(18,GPIO.LOW)
	GPIO.output(19,GPIO.LOW)
	GPIO.output(20,GPIO.LOW)
	GPIO.output(21,GPIO.LOW)
	print "Your score is",count
	return 0

try:
    main()
except KeyboardInterrupt:
    pass
finally:
    GPIO.cleanup()
