import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setup(16, GPIO.OUT) #Yellow
GPIO.setup(20, GPIO.OUT) #Red
GPIO.setup(21, GPIO.OUT) #Green
GPIO.output(16, GPIO.LOW)
GPIO.output(20, GPIO.LOW)
GPIO.output(21, GPIO.LOW)

GPIO.output(16, GPIO.HIGH)
time.sleep(2)
GPIO.output(20, GPIO.HIGH)
time.sleep(2)
GPIO.output(21, GPIO.HIGH)
time.sleep(2)
GPIO.cleanup()