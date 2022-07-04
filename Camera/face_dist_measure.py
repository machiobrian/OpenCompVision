import cv2 as cv

#dist from camera to face(object) measured in cm
known_dist = 50

#width of the face in real world/ object plane in cm
known_width = 15

# Colors
GREEN = (0, 255, 0)
RED = (0, 0, 255)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

#define fonts
fonts = cv.FONT_HERSHEY_COMPLEX_SMALL

#face detector object
face_detector = cv.CascadeClassifier('/home/machio_b/Documents/Python/OpenCV_4/Camera/cascades/haarcascade_frontalface_alt.xml')

#focal length finder
def focal_length_finder(measured_dist, real_width, width_in_rf_image):

    #finding the focal length
    focal_length = (width_in_rf_image * measured_dist) / real_width
    return focal_length

def dist_finder(focal_length, real_face_width, face_width_in_frame):

    dist = (real_face_width * focal_length)/face_width_in_frame
    return dist


def face_data(image):
    face_width = 0 #initialize an empty variable
    gray_image = cv.cvtColor(image, cv.COLOR_BGR2GRAY)

    #detect the face in the image
    faces = face_detector.detectMultiScale(gray_image, 1.3, 5)

    #looping through the face detected in the image and getting the coordinates
    # x, y, width, height

    for(x,y,width, height) in faces:

        #draw rectagle around the face
        cv.rectangle(image, (x,y), (x+width ,y+height), GREEN, 2)

        #fetch face width in pixels
        face_width = width

    return face_width #returns face_widths in pixels

#reading the reference image from the directory
ref_image = cv.imread('/home/machio_b/Documents/Python/OpenCV_4/Camera/ref_img.jpg')
#find the face width in the ref image - pixels
ref_image_face_width = face_data(ref_image)

#get the focal by calling, focal_length_finder, face width in reference in pixel, the 
#known dist and the known width.
focal_length_found = focal_length_finder(
    known_dist, known_width, ref_image_face_width
)
print('focal length found')

cv.imshow('img,', ref_image)





#initialize the cam object so that we get the frame from it
cap = cv.VideoCapture(0)

#loop through the frames incoming from the camera

while True:

    #read the frames from the video
    _, frame = cap.read()

    #call the face_data function to find the width of the face in the frame
    face_width_in_frane = face_data(frame)

    #if the face is !0 -> find distance

    if face_width_in_frane != 0:
        Distance = dist_finder(
            focal_length_found,
            known_width,
            face_width_in_frane
        )

        # draw line as background of text
        cv.line(frame, (30, 30), (230, 30), RED, 32)
        cv.line(frame, (30, 30), (230, 30), BLACK, 28)

        # Drawing Text on the screen
        cv.putText(
            frame, f"Distance: {round(Distance,2)} CM", (30, 35),
          fonts, 0.6, GREEN, 2)
        
    #show frame on the screen
    cv.imshow('frame', frame)

    # quit the program if you press 'q' on keyboard
    if cv.waitKey(1) == ord("q"):
        break

# closing the camera
cap.release()
 
# closing the the windows that are opened
cv.destroyAllWindows()