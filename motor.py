import RPi.GPIO as GPIO
import time
import cv2
from picamera2 import Picamera2, Preview
from libcamera import Transform
import numpy as np

Hertz = 20
PWMA = 18
NMA = 17

PWMB = 19
NMB = 16

def motor_go(speed):
    L_Motor.ChangeDutyCycle(speed)
    R_Motor.ChangeDutyCycle(speed)
    
def motor_right(speed):
    L_Motor.ChangeDutyCycle(speed)
    R_Motor.ChangeDutyCycle(0)
    
def motor_left(speed):
    L_Motor.ChangeDutyCycle(0)
    R_Motor.ChangeDutyCycle(speed)

def motor_stop():
    L_Motor.ChangeDutyCycle(0)
    R_Motor.ChangeDutyCycle(0)

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

GPIO.setup(PWMA, GPIO.OUT)
GPIO.setup(NMA, GPIO.OUT)
GPIO.setup(PWMB, GPIO.OUT)
GPIO.setup(NMB, GPIO.OUT)

L_Motor = GPIO.PWM(PWMA, Hertz)
L_Motor.start(0)
GPIO.output(NMA, False)

R_Motor = GPIO.PWM(PWMB, Hertz)
R_Motor.start(0)
GPIO.output(NMB, False)



def main():
    picam2 = Picamera2()
    camera_config = picam2.create_still_configuration(main={"format": 'BGR888',"size": (1920, 1080)}, lores={"format": 'BGR888',"size": (160, 120)}, transform=Transform(hflip=True, vflip=True))
    picam2.configure(camera_config)
    picam2.start_preview(Preview.QTGL)
    picam2.start()

    while True:
        ret,frame = picam2.capture_array("cv")
        cv2.imshow('normal',frame)
        
        crop_img =frame[60:120, 0:160]
        
        gray = cv2.cvtColor(crop_img, cv2.COLOR_BGR2GRAY)
    
        blur = cv2.GaussianBlur(gray,(5,5),0)
        
        ret,thresh1 = cv2.threshold(blur,130,255,cv2.THRESH_BINARY)
        
        mask = cv2.erode(thresh1, None, iterations=2)
        mask = cv2.dilate(mask, None, iterations=2)
        cv2.imshow('mask',mask)
    
        contours,hierarchy = cv2.findContours(mask.copy(), 1, cv2.CHAIN_APPROX_NONE)
        
        if len(contours) > 0:
            c = max(contours, key=cv2.contourArea)
            M = cv2.moments(c)
            
            cx = int(M['m10']/M['m00'])
            cy = int(M['m01']/M['m00'])
            
            if cx >= 95 and cx <= 125:              
                print("Turn Left!")
                motor_left(50)
            elif cx >= 39 and cx <= 65:
                print("Turn Right")
                motor_right(50)
            else:
                print("go")
                motor_go(50)
        
        if cv2.waitKey(1) == ord('q'):
            break
    
    picam2.stop()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()
    GPIO.cleanup()
