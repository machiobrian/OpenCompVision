import cv2 as cv

#determine if a rectabgle is inside another
def is_inside(i,o):
    ix,iy,iw,ih = i #possbile inner rect
    ox,oy,ow,oh = o #possible outer rect

    #true if i is inside o

    return ix > ox and ix+iw < ox+ow and \
        iy > oy and iy+ih < oy + oh

#specify that we will us the default people detctor
hog = cv.HOGDescriptor()
hog.setSVMDetector(cv.HOGDescriptor_getDefaultPeopleDetector()) #SVM is a classifier

img = cv.imread('pep.png')
#detect peopplpe using
found_rects, found_weights = hog.detectMultiScale(
    img, winStride=(4,4), scale=1.02, finalThreshold =3.0)
    #winstride -> tuple, distance the window moves while trying to detect people

#To filter the detections
found_rects_filtered = []
found_weights_filtered = []
for ri, r in enumerate(found_rects):
    for qi, q in enumerate(found_rects):
        if ri != qi and is_inside(r, q):
            break
        else:
            found_rects_filtered.append(r)
            found_weights_filtered.append(found_weights[ri])


#draw the rectangle og the people rthat have bee found
for ri, r in enumerate(found_rects_filtered):
    x,y,w,h = r
    cv.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 1)
    text = '%.2f' % found_weights_filtered[ri]
    cv.putText(img, text, (x, y - 20),
    cv.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 1)

cv.imshow('People', img)
#cv.imwrite()
cv.waitKey(0)