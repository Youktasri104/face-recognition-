from sklearn.neighbors import KNeighborsClassifier

import cv2
import pickle
import numpy as np
import os
import csv
import time
from datetime import datetime
from win32com.client import Dispatch

def speak(strl):
     speak = Dispatch("SAPI.SpVoice")
     speak.Speak(strl)


v=cv2.VideoCapture(0)
m=cv2.CascadeClassifier('data/haarcascade_frontalface_default.xml')

with open('data/names.pkl','rb') as f:
       LABELS= pickle.load(f)
with open('data/data.pkl','rb') as f:
       FACES= pickle.load(f)

knn=KNeighborsClassifier(n_neighbors=5)
knn.fit(FACES,LABELS)


col= ['names','time']

#a=rate,b=frame

while True:
    a,b=v.read()
    g=cv2.cvtColor(b,cv2.COLOR_BGR2GRAY)
    d=m.detectMultiScale(g,1.3,5)
    for (x,y,w,h) in d:
        crop=b[y:y+h,x:x+w,:]
        resize=cv2.resize(crop,(50,50)).flatten().reshape(1,-1)
        output=knn.predict(resize)
        t= time.time()
        date=datetime.fromtimestamp(t).strftime('%Y-%m-%d ')
        times=datetime.fromtimestamp(t).strftime('%H:%M:%S ')
        s=os.path.isfile("Attendence/attendence_"+ date +".csv")
        cv2.putText(b,str(output[0]),(x,y-15),cv2.FONT_HERSHEY_COMPLEX,1,(255,255,255),1)
        cv2.rectangle(b,(x,y),(x+w ,y+h), (50,50,255), 3)
        attendance=[str(output[0]),str(times)]
    cv2.imshow("frame",b)
    c=cv2.waitKey(1)
    if c==ord('o'):
         speak("attendence taken")
         if s:
               with open("Attendence/attendence_"+ date +".csv","+a") as csvfile:
                   writer=csv.writer(csvfile)
                   writer.writerow(attendance)
               csvfile.close()
         else:
              with open("Attendence/attendence_"+ date +".csv","+a") as csvfile:
                   writer=csv.writer(csvfile)
                   writer.writerow(col)
                   writer.writerow(attendance)
              csvfile.close()
    if c== ord('0'):
        break
v.release()
cv2.destroyAllWindows()

