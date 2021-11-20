import numpy as np
from PIL import Image # python里面的图像库
import os
import cv2

# Path for face image database
path = './userImg' # 数据集的路径

recognizer = cv2.face.LBPHFaceRecognizer_create()
detector = cv2.CascadeClassifier('/media/pi/userdata/root/usr/local/share/OpenCV/haarcascades/haarcascade_frontalface_default.xml');

# function to get the images and label data
def getImagesAndLabels(path):
    imagePaths = [os.path.join(path,f) for f in os.listdir(path)]
    # print(imagePaths) # 输出文件夹所有的文件路径
    faceSamples=[]  # 存放人脸
    ids = []       # 存放人脸的ID
    for imagePath in imagePaths:  # 遍历路径
        PIL_img = Image.open(imagePath).convert('L') # convert it to grayscale
        img_numpy = np.array(PIL_img,'uint8')
        print(os.path.split(imagePath)[-1])
        # id = int(os.path.split(imagePath)[-1].split(".")[1]) # 获取ID
        id = int(os.path.split(imagePath)[-1].split(".")[0]) # 获取ID
        print(id)
        #print(" " + str(id)) # 输入ID
        faces = detector.detectMultiScale(img_numpy)
        for (x,y,w,h) in faces:
            faceSamples.append(img_numpy[y:y+h,x:x+w])
            ids.append(id)
    return faceSamples,ids

print ("\n [INFO] Training faces. It will take a few seconds. Wait ...")
faces,ids = getImagesAndLabels(path)
recognizer.train(faces, np.array(ids))

# Save the model into trainer/trainer.yml
recognizer.write('./trainer/trainer.yml') # recognizer.save() worked on Mac, but not on Pi

# Print the numer of faces trained and end program
print("\n [INFO] {0} faces trained. Exiting Program".format(len(np.unique(ids))))
