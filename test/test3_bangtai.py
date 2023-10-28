import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setup(2, GPIO.OUT) #in1 of Relay
GPIO.setup(27, GPIO.OUT) #in 2 of Relay
GPIO.output(2, GPIO.HIGH)
GPIO.output(27, GPIO.HIGH)

GPIO.output(2, GPIO.LOW)
time.sleep(3)
GPIO.output(2, GPIO.HIGH)
GPIO.output(27, GPIO.LOW)
time.sleep(3)

GPIO.cleanup()
