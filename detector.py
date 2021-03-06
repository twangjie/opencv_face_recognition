import cv2
import numpy as np 
import sqlite3
import os
from PIL import Image, ImageDraw, ImageFont

conn = sqlite3.connect('database.db')
c = conn.cursor()

fname = "recognizer/trainingData.yml"
if not os.path.isfile(fname):
    print("Please train the data first")
    exit(0)

face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
cap = cv2.VideoCapture(0)
recognizer = cv2.face.LBPHFaceRecognizer_create()
#recognizer = cv2.face.FisherFaceRecognizer_create()
recognizer.read(fname)

while True:
    ret, img = cap.read()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    cv2.equalizeHist(gray,gray)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    for (x,y,w,h) in faces:
    
        cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),3)
        #print("w:%d,h:%d" % (w,h))
        
        #if w < 150 or h < 150:
        #    img_ex = cv2.resize(img, (2*cols, 2*rows), interpolation=cv2.INTER_CUBIC)
        
        face = gray[y:y+h,x:x+w]
        if w < 150 or h < 150:
            face = cv2.resize(face, (300, 300), interpolation=cv2.INTER_CUBIC)
            print("w:%d,h:%d" % (w,h))
            
        ids,confidence = recognizer.predict(face)
        c.execute("select name from users where id = (?);", (ids,))
        result = c.fetchall()
        name = result[0][0]
        if confidence < 50:
            #cv2.putText(img, name, (x+2,y+h-5), cv2.FONT_HERSHEY_SIMPLEX, 1, (150,255,0),2)
            print("w:%d,h:%d" % (w,h))
            result = "confidence:%.2f, %s" % (confidence, name)
            cv2_im = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            pil_im = Image.fromarray(cv2_im)
            draw = ImageDraw.Draw(pil_im)
            font = ImageFont.truetype("simhei.ttf", 20, encoding="utf-8")
            draw.text((x+2,y+h-5), result, (0, 0, 255), font=font)
            img = cv2.cvtColor(np.array(pil_im), cv2.COLOR_RGB2BGR)
        #else:
            #cv2.putText(img, 'No Match', (x+2,y+h-5), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255),2)
            #print("confidence:%.2f" % (confidence))
    cv2.imshow('Face Recognizer',img)
    k = cv2.waitKey(30) & 0xff
    if k == 27:
        break

cap.release()
cv2.destroyAllWindows()