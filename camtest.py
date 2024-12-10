import cv2 #OpenCV를 사용하기위해 import해줍니다.
import numpy as np #파이썬의 기본 모듈중 하나인 numpy

def main():
    camera = cv2.VideoCapture(-1) #카메라를 비디오 입력으로 사용. -1은 기본설정이라는 뜻
    camera.set(3,160) #띄울 동영상의 가로사이즈 160픽셀
    camera.set(4,120) #띄울 동영상의 세로사이즈 120픽셀
    
    while( camera.isOpened() ): #카메라가 Open되어 있다면,
        ret, frame = camera.read() #카메라를 읽어서 image값에 넣습니다.
        frame = cv2.flip(frame,-1) #카메라 이미지를 flip, 뒤집습니다. -1은 180도 뒤집는다
        cv2.imshow( 'normal' , frame)  #'normal'이라는 이름으로 영상을 출력
        
        crop_img =frame[60:120, 0:160] #세로는 60~120픽셀, 가로는 0~160픽셀로 crop(잘라냄)한다.
        
        cv2.imshow('crop' ,crop_img) #crop이라는 이름으로 영상을 출력
        
        
        if cv2.waitKey(1) == ord('q'): #만약 q라는 키보드값을 읽으면 종료합니다.
            break
        
    cv2.destroyAllWindows() #이후 openCV창을 종료합니다.
     
if __name__ == '__main__':
    main()