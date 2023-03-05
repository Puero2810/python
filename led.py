import RPi.GPIO as GPIO
from time import *

def rojo(pin1):
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(pin1, GPIO.OUT)
    GPIO.output(pin1, GPIO.HIGH)

def verde(pin1, pin2):
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(pin1, GPIO.OUT)
    GPIO.setup(pin2, GPIO.OUT)
    GPIO.output(pin1, GPIO.LOW)
    GPIO.output(pin2, GPIO.HIGH)
    sleep(5)
    GPIO.output(pin1, GPIO.HIGH)
    GPIO.output(pin2, GPIO.LOW)