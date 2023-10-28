import io
import os
import picamera
import RPi.GPIO as GPIO                    #Import GPIO library
import time                                #Import time library


#GPIO Mode (BOARD / BCM)
GPIO.setmode(GPIO.BCM)

# Imports the Google Cloud client library
from google.cloud import vision
from google.cloud.vision import types
from PIL import Image, ImageDraw

#Constants, PIN Configuration
#set GPIO Pins
GPIO_MODE = 12
GPIO_TRIGGER = 18
GPIO_ECHO = 24
RED_LED_NO_RECYCLE = 25        #Pin #2 BCM Mode
BLUE_LED_RECYCLE = 7        #Pin #3 BCM Mode
YELLOW_LED_GLASS_RECYCLE = 8        #Pin #4 BCM Mode
STRING_RECYCLE = ["Recycling","Recycling symbol", "textile", "paper", "material", "document", "writing", "reading"]
STRING_GLASS_RECYCLE = ["Glass recycling", "bottle", "bottled water", "glass bottle", "glass", "glasses", "alcoholic beverage", "wine glass"]
STRING_NO_RECYCLE = ["WEEE", "mobile phone","electronics", "electronic device"]
LOGO_MODE = 0
LABEL_MODE = 1

## Initialization
#Initialize output for LEDs, GPIOs
GPIO.setwarnings(False)
GPIO.setup(RED_LED_NO_RECYCLE,GPIO.OUT)
GPIO.setup(BLUE_LED_RECYCLE,GPIO.OUT)
GPIO.setup(YELLOW_LED_GLASS_RECYCLE,GPIO.OUT)
GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)
GPIO.setup(GPIO_MODE, GPIO.IN)
GPIO.setup(GPIO_MODE, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
mode = LOGO_MODE   #LOGO_MODE is default

def get_crop_hint(path):
    """Detect crop hints on a single image and return the first result."""
    client = vision.ImageAnnotatorClient()

    with io.open(path, 'rb') as image_file:
        content = image_file.read()

    image = types.Image(content=content)

    crop_hints_params = types.CropHintsParams(aspect_ratios=[1.77])
    image_context = types.ImageContext(crop_hints_params=crop_hints_params)

    response = client.crop_hints(image=image, image_context=image_context)
    hints = response.crop_hints_annotation.crop_hints

    # Get bounds for the first crop hint using an aspect ratio of 1.77.
    vertices = hints[0].bounding_poly.vertices

    return vertices


def draw_hint(image_file):
    """Draw a border around the image using the hints in the vector list."""
    vects = get_crop_hint(image_file)

    im = Image.open(image_file)
    draw = ImageDraw.Draw(im)
    draw.polygon([
        vects[0].x, vects[0].y,
        vects[1].x, vects[1].y,
        vects[2].x, vects[2].y,
        vects[3].x, vects[3].y], None, 'red')
    im.save('output-hint.jpg', 'JPEG')


def crop_to_hint(image_file):
    """Crop the image using the hints in the vector list."""
    vects = get_crop_hint(image_file)

    im = Image.open(image_file)
    im2 = im.crop([vects[0].x, vects[0].y,
                  vects[2].x - 1, vects[2].y - 1])
    im2.save('images/test.jpg', 'JPEG')

def led_blinking(n, period_in_second):
    for i in range(n):
        GPIO.output(BLUE_LED_RECYCLE,GPIO.HIGH)
        GPIO.output(RED_LED_NO_RECYCLE,GPIO.HIGH)
        GPIO.output(YELLOW_LED_GLASS_RECYCLE,GPIO.HIGH)
        time.sleep(period_in_second)
        GPIO.output(YELLOW_LED_GLASS_RECYCLE,GPIO.LOW)
        GPIO.output(BLUE_LED_RECYCLE,GPIO.LOW)
        GPIO.output(RED_LED_NO_RECYCLE,GPIO.LOW)
        time.sleep(period_in_second)

def change_mode(channel):
    global mode
    if GPIO.input(GPIO_MODE) == GPIO.HIGH:
        print('\n▼  Pressed')
        if mode == LABEL_MODE:
            mode = LOGO_MODE
            print("MODE changes to LOGO_MODE")
            led_blinking(2,1)
        else:
            mode = LABEL_MODE
            print("MODE changes to LABEL_MODE")
            led_blinking(4,1)
    else:
        print('\n ▲ Released')

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

# Add button event : change mode
GPIO.add_event_detect(GPIO_MODE, GPIO.BOTH, callback=change_mode)
# Instantiates a Camera object
camera = picamera.PiCamera()
if __name__ == '__main__':
    try:
        led_blinking(5,0.5)
        while True:
            print ("Current MODE", mode)
            dist = distance()
            print ("Measured Distance = %.1f cm" % dist)
            if dist>=10 and dist <=20:
                print("Action.............")
                #Caputre a picture
                camera.capture('images/test.jpg')
                #time.sleep(0.5)
                led_blinking(1,1)
                # Instantiates a client
                client = vision.ImageAnnotatorClient()
                #Drop to  hint
                #crop_to_hint('images/test.jpg')

                # The name of the image file to annotate
                file_name = os.path.join(os.path.dirname(__file__),'images/test.jpg')

                # Loads the image into memory
                with io.open(file_name, 'rb') as image_file:
                    content = image_file.read()

                image = types.Image(content=content)

                # Performs label detection on the image file
                if mode == LOGO_MODE:
                    response = client.logo_detection(image=image)
                    labels = response.logo_annotations
                    print('Labels: ')
                    if (len(labels)==0):
                        GPIO.output(BLUE_LED_RECYCLE,GPIO.HIGH)
                        time.sleep(5)
                        GPIO.output(BLUE_LED_RECYCLE,GPIO.LOW)
                    for label in labels:
                        print(label.description)
                        if label.description in STRING_NO_RECYCLE:
                            #print(STRING_NO_RECYCLE)
                            GPIO.output(RED_LED_NO_RECYCLE,GPIO.HIGH)
                            time.sleep(5)
                            GPIO.output(RED_LED_NO_RECYCLE,GPIO.LOW)
                            break;

                        elif label.description in STRING_GLASS_RECYCLE:
                            #print(STRING_GLASS_RECYCLE)
                            GPIO.output(YELLOW_LED_GLASS_RECYCLE,GPIO.HIGH)
                            time.sleep(5)
                            GPIO.output(YELLOW_LED_GLASS_RECYCLE,GPIO.LOW)
                            break;
                        else:
                            GPIO.output(BLUE_LED_RECYCLE,GPIO.HIGH)
                            time.sleep(5)
                            GPIO.output(BLUE_LED_RECYCLE,GPIO.LOW)
                            break;

                else:
                    response = client.label_detection(image=image)
                    labels = response.label_annotations
                    print('Labels:')
                    for label in labels:
                        print(label.description)

                        if label.description in STRING_RECYCLE:
                            #print(STRING_RECYCLE)
                            GPIO.output(BLUE_LED_RECYCLE,GPIO.HIGH)
                            time.sleep(5)
                            GPIO.output(BLUE_LED_RECYCLE,GPIO.LOW)
                            break;

                        if label.description in STRING_NO_RECYCLE:
                            #print(STRING_NO_RECYCLE)
                            GPIO.output(RED_LED_NO_RECYCLE,GPIO.HIGH)
                            time.sleep(5)
                            GPIO.output(RED_LED_NO_RECYCLE,GPIO.LOW)
                            break;

                        if label.description in STRING_GLASS_RECYCLE:
                            #print(STRING_GLASS_RECYCLE)
                            GPIO.output(YELLOW_LED_GLASS_RECYCLE,GPIO.HIGH)
                            time.sleep(5)
                            GPIO.output(YELLOW_LED_GLASS_RECYCLE,GPIO.LOW)
                            break;
            print("Next capture**********")
            time.sleep(0.5)
    # Reset by pressing CTRL + C
    except KeyboardInterrupt:
        print("Measurement stopped by User")
        GPIO.cleanup()
