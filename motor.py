import pigpio
import time
import cv2
from picamera2 import Picamera2, Preview
from libcamera import Transform
import numpy as np

PWMA = 18
NMA = 17
PWMB = 19
NMB = 16

def motor_go(speed):
    pi.set_PWM_dutycycle(PWMA, speed)
    pi.set_PWM_dutycycle(PWMB, speed)
    
def motor_right(speed):
    pi.set_PWM_dutycycle(PWMA, speed)
    pi.set_PWM_dutycycle(PWMB, 0)
    
def motor_left(speed):
    pi.set_PWM_dutycycle(PWMA, 0)
    pi.set_PWM_dutycycle(PWMB, speed)

def motor_stop():
    pi.set_PWM_dutycycle(PWMA, 0)
    pi.set_PWM_dutycycle(PWMB, 0)

pi = pigpio.pi()

pi.set_mode(PWMA, pigpio.ALT5)
pi.set_mode(NMA, pigpio.OUTPUT)
pi.set_mode(PWMB, pigpio.ALT0)
pi.set_mode(NMB, pigpio.OUTPUT)

pi.set_PWM_frequency(PWMA, 100)
pi.set_PWM_range(PWMA, 100)
pi.set_PWM_frequency(PWMB, 100)
pi.set_PWM_range(PWMB, 100)

pi.set_PWM_dutycycle(PWMA, 0)
pi.set_PWM_dutycycle(PWMB, 0)
pi.write(NMA, 0)
pi.write(NMB, 0)



def main():
    picam2 = Picamera2()
    camera_config = picam2.create_still_configuration(main={"format": 'BGR888',"size": (160, 120)}, lores={"size": (160, 120)}, transform=Transform(hflip=True, vflip=True))
    picam2.configure(camera_config)
    picam2.start_preview(Preview.QTGL)
    picam2.start()

    try:
        while True:
            frame = picam2.capture_array("main")
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
    except KeyboardInterrupt:
        pass

    picam2.stop()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()
    pi.stop()
