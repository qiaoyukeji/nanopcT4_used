import cv2
import os

cam = cv2.VideoCapture(10)  # 获取摄像头
cam.set(3, 640) # set video width  # 设置视频的高度和宽度
cam.set(4, 480) # set video height

# 检测人脸
face_detector = cv2.CascadeClassifier('/media/pi/userdata/root/usr/local/share/OpenCV/haarcascades/haarcascade_frontalface_default.xml')

# For each person, enter one numeric face id
face_id = input('\n enter user id end press <return> ==>  ')

#print("\n [INFO] Initializing face capture. Look the camera and wait ...")
# Initialize individual sampling face count
count = 0

while(True):
    ret, img = cam.read() # 从摄像头读取图像
    # img = cv2.imread("/home/pi/Desktop/陈卓璇/" + str(count) + '.jpg')
    #print("/home/pi/Desktop/兔子牙/" + str(count) + '.jpg')
    # 翻转图像 1  水平翻转  0 垂直翻转   -1 水平垂直翻转
    #img = cv2.flip(img, -1) # flip video image vertically
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) # 转化为灰度图
    faces = face_detector.detectMultiScale(gray, 1.2, 5) # 识别人脸
    
    count += 1
# 在人脸上画矩形
    for (x,y,w,h) in faces:
        cv2.rectangle(img, (x,y), (x+w,y+h), (255,0,0), 2)
        

        # Save the captured image into the datasets folder
        cv2.imwrite("./userImg/" + str(face_id) + '.' + str(count) + ".jpg", gray[y:y+h,x:x+w])
        # cv2.imshow('image', img) # 显示
        
    cv2.imshow('image', img) # 显示
    k = cv2.waitKey(100) & 0xff # Press 'ESC' for exiting video
    if k == 27:
        break
    elif count >= 10: # Take 10 face sample and stop video
        break

# Do a bit of cleanup
print("\n [INFO] Exiting Program and cleanup stuff")
cam.release()
cv2.destroyAllWindows()
