import streamlit as st
import face_recognition
import matplotlib.pyplot as plt
import cv2
import numpy as np
import os
import time

from datetime import datetime
from PIL import Image

path = 'data'
images = []
classNames = []
myList = os.listdir(path)

click=0


   


for cls in myList:
    current_img = cv2.imread(f'{path}/{cls}')
    images.append(current_img)
    classNames.append(os.path.splitext(cls)[0])

def find_encodings(images):
    encode_list = []
    for img in images:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encode_list.append(encode)
    return encode_list

def mark_attendance(name):
    with open('log.csv', 'r+') as f:
        my_data_list = f.readlines()
        name_list = []
        for line in my_data_list:
            entry = line.split(',')
            name_list.append(entry[0])
            if name not in name_list:
               now = datetime.now()
               time = now.strftime('%H:%M:%S')
               f.writelines(f'\n{name},{time}')


encode_list_known = find_encodings(images)
print(len(encode_list_known))

#cap = cv2.VideoCapture(0)
st.markdown("# Camera Application")
text=st.text_input('名前を入力', '')

if st.button("登録"):
   #st.write("clicked")
   click=1;

device = user_input = st.text_input("input your video/camera device", "0")
#辞書ファイル
face_cascade = cv2.CascadeClassifier("haarcascade_frontalface_alt2.xml")

if device.isnumeric():
    # e.g. "0" -> 0
    device = int(device)

cap = cv2.VideoCapture(device)

image_loc = st.empty()
while cap.isOpened:
    #global click
    success, img = cap.read()
    img_resize = cv2.resize(img, (0, 0), None, 0.25, 0.25)
    img_resize = cv2.cvtColor(img_resize, cv2.COLOR_BGR2RGB)

    face_frame = face_recognition.face_locations(img_resize)
    encode_frame = face_recognition.face_encodings(img_resize, face_frame)
    face = face_cascade.detectMultiScale(img , 1.1 , 3)
    
    for encode_face, face_loc in zip(encode_frame, face_frame):
        
        matches = face_recognition.compare_faces(encode_list_known, encode_face)
        face_dis = face_recognition.face_distance(encode_list_known, encode_face)
        print(face_dis)
        match_idx = np.argmin(face_dis)
        #枠表示
        for (x , y , width , height) in face :
            frame_cut = img[y:y+height, x:x+width]
            cv2.rectangle(img, (x, y) , (x + width, y + height) , (166, 236, 147) ,2)
            # 画像を保存
            if click==1:
               click=0
               now=datetime.datetime.now()
               #filename=(now.strftime("%Y%m%d-%M%H%S.jpg"))
               #cv2.imwrite('data/'+"data" + filename, frame_cut)
               cv2.imwrite('data/'+ text +'.jpg', frame_cut)
        #検出
        if matches[match_idx]:
            name = classNames[match_idx].upper()
            y1, x2, y2, x1 = face_loc
            y1, x2, y2, x1 = y1*4, x2*4, y2*4, x1*4
            #cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
            #cv2.rectangle(img, (x1, y2-35), (x2, y2), (0,255,0),cv2.FILLED)
            cv2.putText(img, name, (x1+6, y2-6), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)
            mark_attendance(name)
            
    converted_frame = cv2.cvtColor(img, cv2.COLOR_BGR2RGB) 
    image_loc.image(converted_frame)
    if cv2.waitKey(1) & 0xFF == ord("q"):
       break
       
    # キーを押すとループを止めて破棄します。ウィンドウを終了させます。 ※break重要
    if cv2.waitKey(10) > 0 :
       capture.release()
       cv2.destroyAllWindows()
       break


cap.release()