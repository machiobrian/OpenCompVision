import cv2 as cv #import the cv module

#initialize two cascade classifiers for eyes and face
face_cascade = cv.CascadeClassifier('./cascades/haarcascade_frontalface_default.xml')
eye_cascade = cv.CascadeClassifier('./cascades/haarcascade_eye.xml')

#open a camera feed and start iterating over frames
camera = cv.VideoCapture(0)
while (cv.waitKey(1) == -1):
    success, frame = camera.read()
    if success: 
        gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
        #face detect
        faces = face_cascade.detectMultiScale(gray, 1.3, 5, minSize =(120,120))
        #no face smaller than 120 by 120 will be detected => we are sitting near the camera

        for (x,y,w,h) in faces:
            cv.rectangle(frame, (x,y), (x+w, y+h), (255,0,0), 1)
            roi_gray = gray[y:y+h, x:x+w]
            eyes = eye_cascade.detectMultiScale(roi_gray, 1.03, 5, minSize=(40,40))

            for (ex, ey, ew, eh) in eyes:
                cv.rectangle(frame, (x+ex, y+ey),
                        (x+ex+ew, y+ey+eh), (0, 255, 0), 2)
                cv.imshow("Face_Det", frame)

          