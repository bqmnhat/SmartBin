import io
import os
import picamera
import RPi.GPIO as GPIO                    #Import GPIO library
import time                                #Import time library

# Imports the Google Cloud client library
from google.cloud import vision
from google.cloud.vision import types
from PIL import Image, ImageDraw


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