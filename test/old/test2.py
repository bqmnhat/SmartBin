import RPi.GPIO as GPIO
import time

i = 1
GPIO.setmode(GPIO.BCM)
GPIO.setup(2, GPIO.OUT) #in1 of Relay
GPIO.setup(27, GPIO.OUT) #in 2 of Relay
GPIO.output(2, GPIO.HIGH)
GPIO.output(27, GPIO.HIGH)

GPIO.setup(17, GPIO.OUT) # Signal of Mosfet
p = GPIO.PWM(17,100)          #GPIO17 as PWM output, with 100Hz frequency
p.start(0)                              #generate PWM signal with 0% duty cycle


GPIO.output(2, GPIO.LOW)
p.ChangeDutyCycle(60)

time.sleep(1)
GPIO.cleanup()
# pwm = GPIO.PWM(17, 1000)
# pwm.start(60)
# dc=60
# while i<4:
#     GPIO.output(27, GPIO.HIGH)
#     GPIO.output(2, GPIO.LOW)
#     sleep(3)
#     pwm.ChangeDutyCycle(dc+20)
#     sleep(1)
#     i+=1
# i=1
# pwm.ChangeDutyCycle(60)
# dc=60
# while i<4:
#     GPIO.output(2, GPIO.HIGH)
#     GPIO.output(27, GPIO.LOW)
#     sleep(3)
#     pwm.ChangeDutyCycle(dc+20)
#     sleep(1)
#     i+=1
# #a=1
# #pwm.ChangeDutyCycle(50)
# ####   sleep(3)
# #    pwm.ChangeDutyCycle(100)
# #a+=1
