#!/usr/bin/env python
# coding: utf-8
import cv2

pythonPath = 'D:\Python\Python37'

face_cascade = cv2.CascadeClassifier(
    pythonPath + '\Lib\site-packages\cv2\data\haarcascade_frontalface_alt2.xml')
eye_cascade = cv2.CascadeClassifier(
    pythonPath + '\Lib\site-packages\cv2\data\haarcascade_eye_tree_eyeglasses.xml')


def check(frame1):
    gray = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.1, 5, cv2.CASCADE_SCALE_IMAGE)
    if len(faces) > 0:
        for faceRect in faces:
            x, y, w, h = faceRect
            cv2.rectangle(frame1, (x, y), (x + w, y + h), (255, 0, 0), 2, 8, 0)
            roi_gray = gray[y:y + h, x:x + w]
            roi_color = frame1[y:y + h, x:x + h]
            eyes = eye_cascade.detectMultiScale(roi_gray, 1.1, 1, cv2.CASCADE_SCALE_IMAGE, (2, 2))
            for (ex, ey, ew, eh) in eyes:
                cv2.rectangle(roi_color, (ex, ey), (ex + ew, ey + eh), (0, 255, 0), 2)
    cv2.imshow("识别图", frame1)


cap = cv2.VideoCapture(0)
while True:
    ret, frame2 = cap.read()
    cv2.imshow("原图", frame2)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    check(frame2)

cap.release()
cv2.destroyAllWindows()
cv2.waitKey(0)
