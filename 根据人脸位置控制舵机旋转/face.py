import numpy as np
import cv2
import ctypes  
ll = ctypes.cdll.LoadLibrary   
lib = ll("./duoji/duoji")
 
faceCascade = cv2.CascadeClassifier('/media/pi/userdata/root/usr/local/share/OpenCV/haarcascades/haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier('/media/pi/userdata/root/usr/local/share/OpenCV/haarcascades/haarcascade_eye.xml')


cap = cv2.VideoCapture(10)
cap.set(3,640) # set Width
cap.set(4,480) # set Height
i=0
moveAngle_1=1435

while True:
    ret, img = cap.read()
    img = cv2.flip(img, 1) 
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = faceCascade.detectMultiScale(
        gray,     
        # 表示每次图像尺寸减小的比例
        scaleFactor=1.1,
        # 表示每一个目标至少要被检测到3次才算是真的目标
        minNeighbors=10,     
        minSize=(20, 20)
    )
    
    for (x,y,w,h) in faces:
        cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
        print("%d,x = %d,x+w = %d,y = %d,y+h = %d" %(i,x,x+w,y,y+h))
        i+=1
         # 框选出人脸区域，在人脸区域而不是全图中进行人眼检测，节省计算资源
        face_area = img[y:y+h, x:x+w]  # 人脸区域
        eyes = eye_cascade.detectMultiScale(face_area,1.1,5)
        for (ex,ey,ew,eh) in eyes:
            #画出人眼框，绿色，画笔宽度为1
            cv2.rectangle(face_area,(ex,ey),(ex+ew,ey+eh),(0,255,0),1)

        # x 是人脸识别框中的左上角横坐标，根据 x 坐标在相机中的位置，判断相机（舵机）的移动方向
        if(x < 320-0.7*w):
            print(x)
            # 0 或 1 表示转动方向，moveAngle_1 为转动角度系数
            moveAngle_1=lib.fmain(0,moveAngle_1)
            # print("lib.fmain(0)="+str(lib.fmain(0)))
        if(x+w > 320+0.7*w):
            moveAngle_1=lib.fmain(1,moveAngle_1)

        roi_gray = gray[y:y+h, x:x+w]
        roi_color = img[y:y+h, x:x+w]  
    
    cv2.namedWindow("enhanced",0);

    cv2.resizeWindow("enhanced", 640, 640);
    cv2.imshow('video',img)
    
    k = cv2.waitKey(30) & 0xff
    if k == 27: # press 'ESC' to quit
        break
 
cap.release()
cv2.destroyAllWindows()