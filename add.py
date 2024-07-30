import cv2
import pickle
import numpy as np
import os

v=cv2.VideoCapture(0)
m=cv2.CascadeClassifier('data/haarcascade_frontalface_default.xml')

data=[]

name= input("Enter your name:")

i=0
#a=rate,b=frame

while True:
    a,b=v.read()
    g=cv2.cvtColor(b,cv2.COLOR_BGR2GRAY)
    d=m.detectMultiScale(g,1.3,5)
    for (x,y,w,h) in d:
        crop=b[y:y+h,x:x+w,:]
        resize=cv2.resize(crop,(50,50))
        if len(data)<=100 and i%10==0:
            data.append(resize)
        i+=1
        cv2.putText(b,str(len(data)),(50,50),cv2.FONT_HERSHEY_COMPLEX,1,(50,50,255,),1)
        cv2.rectangle(b,(x,y),(x+w ,y+h), (50,50,255), 3)
    cv2.imshow("frame",b)
    c=cv2.waitKey(1)
    if c== ord('0') or  len(data)==100:
        break
v.release()
cv2.destroyAllWindows()

data= np.asanyarray(data)
data=data.reshape(100,-1)

if 'names.pkl' not in os.listdir("data/"):
    names=[name]*100
    with open('data/names.pkl','wb') as f:
        pickle.dump(names,f)
else:
    with open('data/names.pkl','rb') as f:
       names= pickle.load(f)
    names=names+[name]*100
    with open('data/names.pkl','wb') as f:
        pickle.dump(names,f)

if 'data.pkl' not in os.listdir("data/"):    
    with open('data/data.pkl','wb') as f:
        pickle.dump(data,f)
else:
    with open('data/data.pkl','rb') as f:
       d= pickle.load(f)
    d=np.append(d,data,axis=0)
    with open('data/data.pkl','wb') as f:
        pickle.dump(d,f)





