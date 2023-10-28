import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setup(3, GPIO.OUT) #in1 of Relay - DOWN
GPIO.setup(4, GPIO.OUT) #in 2 of Relay - UP
GPIO.output(3, GPIO.HIGH)
GPIO.output(4, GPIO.HIGH)

GPIO.output(4, GPIO.LOW)
time.sleep(1)
GPIO.output(4, GPIO.HIGH)
GPIO.output(3, GPIO.LOW)
time.sleep(1)

GPIO.cleanup()

