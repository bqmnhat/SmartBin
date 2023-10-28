import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setup(16, GPIO.OUT) #Yellow
GPIO.setup(20, GPIO.OUT) #Red
GPIO.setup(21, GPIO.OUT) #Green

GPIO.output(16, GPIO.LOW)
GPIO.output(20, GPIO.LOW)
GPIO.output(21, GPIO.LOW)

#Switch
GPIO.setup(26, GPIO.IN, pull_up_down=GPIO.PUD_UP) #Red Button
GPIO.setup(19, GPIO.IN, pull_up_down=GPIO.PUD_UP) #Yello Button
GPIO.setup(13, GPIO.IN, pull_up_down=GPIO.PUD_UP) #Green Button
while True:
    input_state_G = GPIO.input(13)
    input_state_Y = GPIO.input(19)
    input_state_R = GPIO.input(26)
    if input_state_G == False:
        GPIO.output(21, GPIO.HIGH)
        print('Button Pressed')
        time.sleep(2)
        GPIO.output(21, GPIO.LOW)
    if input_state_Y == False:
        GPIO.output(16, GPIO.HIGH)
        print('Button Pressed')
        time.sleep(2)
        GPIO.output(16, GPIO.LOW)
    if input_state_R == False:
        GPIO.output(20, GPIO.HIGH)
        print('Button Pressed')
        time.sleep(2)
        GPIO.output(20, GPIO.LOW)
GPIO.cleanup()
