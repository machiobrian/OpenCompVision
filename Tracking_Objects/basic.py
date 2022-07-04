import cv2 as cv

BLUR_RADIUS = 21
erode_kernel = cv.getStructuringElement(cv.MORPH_ELLIPSE,(5,5))
dilate_kernel = cv.getStructuringElement(cv.MORPH_ELLIPSE,(9,9))

#capture 10 frames from cam, discard the 9
cap = cv.VideoCapture(0)

for i in range(10):
    success, frame = cap.read()
if not success:
    exit(1) #if we are unable to capture 10 frames exit = true
    
gray_background = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
gray_background = cv.GaussianBlur(gray_background, (BLUR_RADIUS, BLUR_RADIUS), 0)

#since we now have a reference image for the background, proceed to capture more frames
#from which we detect motion
success, frame = cap.read()
while success:

    gray_frame = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    gray_frame = cv.GaussianBlur(gray_frame, (BLUR_RADIUS, BLUR_RADIUS), 0)

#compare the new captured frame to that of the background image -> abs value of these
# values -> apply threshold to obtain pure black/white image -> smoothen Morphological ops
diff = cv.absdiff(gray_background, gray_frame)
_, thresh = cv.threshold(diff, 40, 255, cv.THRESH_BINARY)
cv.erode(thresh, erode_kernel, thresh, iterations=2)
cv.dilate(thresh, dilate_kernel, thresh, iterations=2)
#our thresh contains white blobs whenever there is moving object
#find contours of the white blobs and draw ounding boxes around them
_, contours, heir = cv.findContours(thresh, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

for c in contours:
    if cv.contourArea(c) > 4000:
        x,y,w,h = cv.boundingRect(c)
        cv.rectangle(frame, (x,y), (x+w, y+h), (255,0,255), 2)

cv.imshow('diff', diff)
cv.imshow('thresh', thresh)
cv.imshow('detection', frame) #shows the differenced image, threshold and detction results

#continue reading frames until the user presses Esc

k = cv.waitKey()
# if k == 27: #Escape key ASCII
#     break

#success, frame = cap.read()