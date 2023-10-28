from picamera import PiCamera
from time import sleep
camera = PiCamera()
#camera.awb_mode = 'flash'
camera.image_effect = 'washedout'
camera.resolution = (1024, 768)
#camera.crop = (0.05, 0.05, 0.85, 0.85)
camera.zoom = (0.07, 0.22, 0.80, 0.55) #(x, y, width, height)
camera.capture('/home/pi/Desktop/org2.jpg')
camera.start_preview()
sleep(20)
camera.stop_preview()