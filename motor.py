import pigpio
import time
import cv2
from picamera2 import Picamera2, Preview
from libcamera import Transform
from time import sleep
import numpy as np

SPD = 225000
HSPD = 180000

FREQ = 15
PWMA = 18
NMA = 12
PWMB = 19
NMB = 13
global_flag = -1
global buffer
def motor_go():
    global global_flag
    if global_flag == 0:
        return
    pi.hardware_PWM(PWMA, FREQ, SPD)
    pi.hardware_PWM(PWMB, FREQ, SPD)
    pi.write(NMA, 0)
    pi.write(NMB, 0)
    global_flag = 0
    
def motor_right():
    global global_flag
    if global_flag == 1:
        return
    pi.hardware_PWM(PWMA, FREQ, HSPD)
    pi.hardware_PWM(PWMB, FREQ, 10000)
    pi.write(NMA, 0)
    pi.write(NMB, 0)
    global_flag = 1
    
def motor_left():
    global global_flag
    if global_flag == 2:
        return
    pi.hardware_PWM(PWMA, FREQ, 10000)
    pi.hardware_PWM(PWMB, FREQ, HSPD)
    pi.write(NMA, 0)
    pi.write(NMB, 0)

pi = pigpio.pi()

pi.set_mode(NMA, pigpio.OUTPUT)
pi.set_mode(NMB, pigpio.OUTPUT)
pi.hardware_PWM(PWMA, FREQ, 0)
pi.hardware_PWM(PWMB, FREQ, 0)

pi.write(NMA, 0)
pi.write(NMB, 0)

def main():
    picam2 = Picamera2()
    camera_config = picam2.create_still_configuration(main={"format": 'BGR888',"size": (3280, 2464)}, transform=Transform(hflip=True, vflip=True))
    picam2.configure(camera_config)
    picam2.start()
    try:
        while True:
            raw = picam2.capture_array("main")
            frame = cv2.resize(raw, (160, 120))
            cv2.imshow('normal',frame)
            
            crop_img = frame[70:120, 0:160]

            
            gray = cv2.cvtColor(crop_img, cv2.COLOR_BGR2GRAY)

        
            blur = cv2.GaussianBlur(gray,(5,5),0)
            
            ret,thresh1 = cv2.threshold(blur,127,255,cv2.THRESH_BINARY)
            
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
                    print("Turn Left!", format(cx))
                    motor_left()
                elif cx >= 39 and cx <= 65:
                    print("Turn Right", format(cx))
                    motor_right()
                else:
                    print("go", format(cx))
                    motor_go()
            
                if cv2.waitKey(1) == ord('q'):
                    break
    except KeyboardInterrupt:
        pass

    picam2.stop()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()
    pi.hardware_PWM(PWMA, 100, 0)
    pi.hardware_PWM(PWMB, 100, 0)
    pi.stop()
