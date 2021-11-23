import cv2
import numpy as np
import os 
import subprocess
# Python 调用 C 驱动舵机
import ctypes  
ll = ctypes.cdll.LoadLibrary   
lib = ll("./pwmduoji")


# RTMP服务器地址，可在 bilibili 直播中心找到
rtmp = r'rtmp://live-push.bilivideo.com/live-bvc/?streamname=live_23472043_40860345&key=8502d5c2c78b9fdf18fc340472008f33&schedule=rtmp&pflag=9'



cam = cv2.VideoCapture(10)


# rtmp 相关配置
# size = (int(cam.get(cv2.CAP_PROP_FRAME_WIDTH)), int(cam.get(cv2.CAP_PROP_FRAME_HEIGHT)))
size = (int(640), int(480))
sizeStr = str(size[0]) + 'x' + str(size[1])
command = ['ffmpeg',
    '-y', '-an',
    '-f', 'rawvideo',
    '-vcodec','rawvideo',
    '-pix_fmt', 'bgr24',
    '-s', sizeStr,
    '-r', '25',
    '-i', '-',
    '-c:v', 'libx264',
    '-pix_fmt', 'yuv420p',
    '-preset', 'ultrafast',
    '-f', 'flv',
    rtmp]

pipe = subprocess.Popen(command, shell=False, stdin=subprocess.PIPE)


moveAngle_1=90
moveAngle_2=90

recognizer = cv2.face.LBPHFaceRecognizer_create()  # 识别器
recognizer.read('/home/pi/face/人脸识别/trainer/trainer.yml') # 加载训练集
# cascadePath = "C:\Users\hotpotman\.conda\envs\face\Lib\site-packages\cv2\data\haarcascade_frontalface_default.xml"
faceCascade = cv2.CascadeClassifier('/media/pi/userdata1/root/usr/local/share/OpenCV/haarcascades/haarcascade_frontalface_default.xml');
 
font = cv2.FONT_HERSHEY_SIMPLEX   # 字体
 
#iniciate id counter
id = 0
 
# names related to ids: example ==> Marcelo: id=1,  etc
names = ['None', 'zhaww', 'liuss','ligb'] 
 
# Initialize and start realtime video capture
# cam = cv2.VideoCapture(10)
cam.set(3, 640) # set video widht
cam.set(4, 480) # set video height
# 在AGX上不要去直接设置帧率，不好用，主要是opencv默认为YUY2格式的视频流，最高帧率只有40,而这个MJPG格式可以很高
# cam.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'))
  
# Define min window size to be recognized as a face
minW = 20
minH = 20
i=0
while True:
    ret, img =cam.read()  # 读取一帧图像
    img = cv2.flip(img, 1) 
    #img = cv2.flip(img, -1) # Flip vertically
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY) # 转化为灰度图
     
    faces = faceCascade.detectMultiScale( 
        gray,
        scaleFactor = 1.2,
        minNeighbors = 5,
        minSize = (int(minW), int(minH)),
       )
   
    for(x,y,w,h) in faces:
        cv2.rectangle(img, (x,y), (x+w,y+h), (0,255,0), 2)
        id, confidence = recognizer.predict(gray[y:y+h,x:x+w])
        print("id=%d"%(id))
        print("%d,x = %d,w = %d,y = %d,h = %d" %(i,x,w,y,h))
        i+=1
        # Check if confidence is less them 100 ==> "0" is perfect match 
        if (confidence < 100):
            print("%id="%(id))
            print(i)
            id = names[id]
            confidence = "  {0}%".format(round(100 - confidence))
        else:
            id = "unknown"
            confidence = "  {0}%".format(round(100 - confidence))
        if(id=="zhaww"):
            # 控制舵机自动旋转的程序
            # x 是人脸识别框中的左上角横坐标，根据 x 坐标在相机中的位置，判断相机（舵机）的移动方向
            if(x < 320-0.7*w):
                print("000")
                # 0 或 1 表示转动方向，moveAngle_1 为转动角度系数
                moveAngle_1 = lib.fmain(0,moveAngle_1)
                # print("lib.fmain(0)="+str(lib.fmain(0)))
            if(x+w > 320+0.7*w):
                moveAngle_1=lib.fmain(1,moveAngle_1)
                print("111")
            x=320

            if(y < 240-0.7*h):
                print("222")
                # 0 或 1 表示转动方向，moveAngle_1 为转动角度系数
                moveAngle_2=lib.fmain(2,moveAngle_2)
                # print("lib.fmain(0)="+str(lib.fmain(0)))
            if(y+h > 240+0.7*h):
                moveAngle_2=lib.fmain(3,moveAngle_2)
                print("333")
            y=240

         
        cv2.putText(img, str(id), (x+5,y-5), font, 1, (255,255,255), 2)
        cv2.putText(img, str(confidence), (x+5,y+h-5), font, 1, (255,255,0), 1)  
    #  rtmp 推流
    pipe.stdin.write(img.tostring()) 
    cv2.imshow('camera',img) 
 
    k = cv2.waitKey(10) & 0xff # Press 'ESC' for exiting video
    if k == 27:
        break
 
# Do a bit of cleanup
print("\n [INFO] Exiting Program and cleanup stuff")

pipe.terminate()
cam.release()
cv2.destroyAllWindows()

