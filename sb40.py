import io
import os
import picamera
import RPi.GPIO as GPIO                    #Import GPIO library
import time                                #Import time library


# Imports the Google Cloud client library
from google.cloud import vision
from google.cloud.vision import types
from PIL import Image, ImageDraw

#GPIO Mode (BOARD / BCM)
GPIO.setmode(GPIO.BCM)

#Constants, PIN Configuration
#set GPIO Pins
#Ultrasonic
GPIO_TRIGGER = 18
GPIO_ECHO = 24

#LEDs
GPIO_YELLOW_LED = 16
GPIO_RED_LED = 20
GPIO_GREEN_LED = 21

#Conveyor
GPIO_CONVEYOR_RIGHT = 2 #Move right
GPIO_CONVEYOR_LEFT = 27 #Move left

#ARM
GPIO_ARM_UP = 4
GPIO_ARM_DOWN = 3

#Buttons
GPIO_BUTTON_YELLOW = 19 #GLASS
GPIO_BUTTON_RED = 26 #NO RECYCLE
GPIO_BUTTON_GREEN = 13 #RECYCLE

STRING_RECYCLE = ["teapot", "figurine", "art", "recycling","recycling symbol", "textile", "paper", "material", "document", "writing", "reading", "plastic", "plastic bag"]
STRING_GLASS_RECYCLE = ["glass recycling", "bottle", "bottled water", "glass bottle", "glass", "glasses", "alcoholic beverage", "wine glass"]
STRING_NO_RECYCLE = ["automotive lighting", "lighting", "light", "weee", "mobile phone","electronics", "electronic device"]

RECYCLE = 1
GLASS = 2
NO_RECYCLE = 3

def detect_garbage(path):
    result = -1
    client = vision.ImageAnnotatorClient()
    with io.open(path, 'rb') as image_file:
        content = image_file.read()
    image = vision.types.Image(content=content)
    response = client.label_detection(image=image)
    labels = response.label_annotations
    print('Labels:')
   
    for label in labels:
        print(label.description)
        print(label.score)
        if label.description.lower() in STRING_RECYCLE:
            print "Recycle"
            result = RECYCLE
            break
        if label.description.lower() in STRING_NO_RECYCLE:
            print "No recycle"
            result = NO_RECYCLE
            break
        if label.description.lower() in STRING_GLASS_RECYCLE:
            print "Glass"
            result = GLASS
            break

    return result

def led_blinking(n, period_in_second):
    for i in range(n):
        GPIO.output(GPIO_YELLOW_LED, GPIO.HIGH)
        GPIO.output(GPIO_RED_LED, GPIO.HIGH)
        GPIO.output(GPIO_GREEN_LED, GPIO.HIGH)
        time.sleep(period_in_second)
        GPIO.output(GPIO_YELLOW_LED, GPIO.LOW)
        GPIO.output(GPIO_RED_LED, GPIO.LOW)
        GPIO.output(GPIO_GREEN_LED, GPIO.LOW)
        time.sleep(period_in_second)

def led_yellow_blinking(n, period_in_second):
    for i in range(n):
        GPIO.output(GPIO_YELLOW_LED, GPIO.HIGH)
        time.sleep(period_in_second)
        GPIO.output(GPIO_YELLOW_LED, GPIO.LOW)
        time.sleep(period_in_second)
def led_red_blinking(n, period_in_second):
    for i in range(n):
        GPIO.output(GPIO_RED_LED, GPIO.HIGH)
        time.sleep(period_in_second)
        GPIO.output(GPIO_RED_LED, GPIO.LOW)
        time.sleep(period_in_second)
def led_green_blinking(n, period_in_second):
    for i in range(n):
        GPIO.output(GPIO_GREEN_LED, GPIO.HIGH)
        time.sleep(period_in_second)
        GPIO.output(GPIO_GREEN_LED, GPIO.LOW)
        time.sleep(period_in_second)


def led_yellow_on():
    GPIO.output(GPIO_YELLOW_LED, GPIO.HIGH)
def led_red_on():
    GPIO.output(GPIO_RED_LED, GPIO.HIGH)
def led_green_on():
    GPIO.output(GPIO_GREEN_LED, GPIO.HIGH)
def led_yellow_off():
    GPIO.output(GPIO_YELLOW_LED, GPIO.LOW)
def led_red_off():
    GPIO.output(GPIO_RED_LED, GPIO.LOW)
def led_green_off():
    GPIO.output(GPIO_GREEN_LED, GPIO.LOW)
    
def distance():
    # set Trigger to HIGH
    GPIO.output(GPIO_TRIGGER, True)

    # set Trigger after 0.01ms to LOW
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGGER, False)

    StartTime = time.time()
    StopTime = time.time()
    # save StartTime
    while GPIO.input(GPIO_ECHO) == 0:
        StartTime = time.time()

    # save time of arrival
    while GPIO.input(GPIO_ECHO) == 1:
        StopTime = time.time()
    # time difference between start and arrival
    TimeElapsed = StopTime - StartTime
    # multiply with the sonic speed (34300 cm/s)
    # and divide by 2, because there and back
    distance = (TimeElapsed * 34300) / 2
    return distance

#Conveyor moves left in n second - RECYCLE
def conveyor_left_recycle(n):
    GPIO.output(GPIO_CONVEYOR_LEFT, GPIO.LOW)
    time.sleep(n)
    GPIO.output(GPIO_CONVEYOR_LEFT, GPIO.HIGH)

#Conveyor moves right in n second - GLASS
def conveyor_right_glass(n):
    GPIO.output(GPIO_CONVEYOR_RIGHT, GPIO.LOW)
    time.sleep(n)
    GPIO.output(GPIO_CONVEYOR_RIGHT, GPIO.HIGH)

#Conveyor moves right in n second - No RECYCLE
def arm_no_recycle(n):
    GPIO.output(GPIO_ARM_UP, GPIO.LOW)
    time.sleep(n)
    GPIO.output(GPIO_ARM_UP, GPIO.HIGH)
    GPIO.output(GPIO_ARM_DOWN, GPIO.LOW)
    time.sleep(n)
    GPIO.output(GPIO_ARM_DOWN, GPIO.HIGH)
    
## Initialization
#Initialize output for LEDs, GPIOs
GPIO.setwarnings(False)
GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)

GPIO.setup(GPIO_YELLOW_LED, GPIO.OUT) #Yellow
GPIO.setup(GPIO_RED_LED, GPIO.OUT) #Red
GPIO.setup(GPIO_GREEN_LED, GPIO.OUT) #Green

GPIO.output(GPIO_YELLOW_LED, GPIO.LOW)
GPIO.output(GPIO_RED_LED, GPIO.LOW)
GPIO.output(GPIO_GREEN_LED, GPIO.LOW)

GPIO.setup(GPIO_CONVEYOR_RIGHT, GPIO.OUT) #in1 of Relay
GPIO.setup(GPIO_CONVEYOR_LEFT, GPIO.OUT) #in 2 of Relay
GPIO.output(GPIO_CONVEYOR_RIGHT, GPIO.HIGH)
GPIO.output(GPIO_CONVEYOR_LEFT, GPIO.HIGH)

GPIO.setup(GPIO_ARM_DOWN, GPIO.OUT) #in1 of Relay - DOWN
GPIO.setup(GPIO_ARM_UP, GPIO.OUT) #in 2 of Relay - UP
GPIO.output(GPIO_ARM_DOWN, GPIO.HIGH)
GPIO.output(GPIO_ARM_UP, GPIO.HIGH)

#Buttons
GPIO.setup(GPIO_BUTTON_RED, GPIO.IN, pull_up_down=GPIO.PUD_UP) #Red Button
GPIO.setup(GPIO_BUTTON_YELLOW, GPIO.IN, pull_up_down=GPIO.PUD_UP) #Yello Button
GPIO.setup(GPIO_BUTTON_GREEN, GPIO.IN, pull_up_down=GPIO.PUD_UP) #Green Button

#GPIO.setup(GPIO_MODE, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

# Add button event : change mode
#GPIO.add_event_detect(GPIO_MODE, GPIO.BOTH, callback=change_mode)

# Instantiates a Camera object
camera = picamera.PiCamera()
camera.image_effect = 'washedout'
camera.resolution = (1024, 768)
camera.zoom = (0.07, 0.22, 0.80, 0.55) #(x, y, width, height)


if __name__ == '__main__':
    try:
        led_blinking(5,0.2)
        while True:
            dist = distance()
            print ("Measured Distance = %.1f cm" % dist)
            if dist>=5 and dist <=20:
                print("Action.............")
                led_blinking(1,1)
                #Caputre a picture
                camera.capture('images/test.jpg')
                result = detect_garbage('images/test.jpg')
                print "Detected:", result
                if result == RECYCLE:
                    conveyor_left_recycle(8)
                if result == GLASS:
                    conveyor_right_glass(8)
                if result == NO_RECYCLE:
                    arm_no_recycle(2)
                if result == -1:
                    led_yellow_on()
                    led_red_on()
                    led_green_on()
                    while True:
                        input_state_Y = GPIO.input(GPIO_BUTTON_YELLOW)
                        input_state_R = GPIO.input(GPIO_BUTTON_RED)
                        input_state_G = GPIO.input(GPIO_BUTTON_GREEN)
                        if input_state_Y == False: #GLASS
                            led_red_off()
                            led_green_off()
                            led_yellow_off()
                            led_yellow_blinking(5, 0.2)
                            led_yellow_off()
                            conveyor_right_glass(5)
                            break
                        if input_state_R == False:
                            led_red_off()
                            led_green_off()
                            led_yellow_off()
                            led_red_blinking(5, 0.2)
                            led_red_off()
                            arm_no_recycle(2)
                            break
                        if input_state_G == False:
                            led_red_off()
                            led_green_off()
                            led_yellow_off()
                            led_green_blinking(5, 0.2)
                            led_green_off()
                            conveyor_left_recycle(5)
                            break
                
            
            print("Next capture**********")
            time.sleep(0.5)
    # Reset by pressing CTRL + C
    except KeyboardInterrupt:
        print("Measurement stopped by User")
        GPIO.cleanup()
