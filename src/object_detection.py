from posixpath import abspath
import cv2

# set const variables
# Relative path to xml
rel_path = "haarcascades\haarcascade_s10.xml"

# Absolute path to xml
abs_path = "C:\src\AugmentedBookmarks\src\haarcascades\haarcascade_s10.xml" 

# Camera
camera_no = 0                    

# Name to display
obj_name = 'Sint Bavo Kerk - leidsevaart'

# Display width 
frame_width = 640

# Display height
frame_height = 480

color = (255,0,255)


cap = cv2.VideoCapture(camera_no)
cap.set(3, frame_width)
cap.set(4, frame_height)

def empty(a):
    pass

# Create trackbar
cv2.namedWindow("Result")
cv2.resizeWindow("Result",frame_width,frame_height+100)
cv2.createTrackbar("Scale","Result",400,1000,empty)
cv2.createTrackbar("Neig","Result",8,50,empty)
cv2.createTrackbar("Min Area","Result",0,100000,empty)
cv2.createTrackbar("Brightness","Result",180,255,empty)

# Load the classifier
cascade = cv2.CascadeClassifier(rel_path)
if cascade.empty():
    cascade = cv2.CascadeClassifier(abs_path)

assert not cascade.empty()

while True:
    # Set camera brightness from trackbar value
    camera_brightness = cv2.getTrackbarPos("Brightness", "Result")
    cap.set(10, camera_brightness)

    # GET CAMERA IMAGE AND CONVERT TO GRAYSCALE
    success, img = cap.read()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # DETECT THE OBJECT USING THE CASCADE
    scale_value = 1 + (cv2.getTrackbarPos("Scale", "Result") /1000)
    min_neighbors = cv2.getTrackbarPos("Neig", "Result")
    objects = cascade.detectMultiScale(gray, scale_value, min_neighbors)
    
    # DISPLAY THE DETECTED OBJECTS
    for (x, y, w, h) in objects:
        area = w * h
        minArea = cv2.getTrackbarPos("Min Area", "Result")
        if area >minArea:
            cv2.rectangle(img,(x,y),(x+w,y+h),color,3)
            cv2.putText(img,obj_name,(x,y-5),cv2.FONT_HERSHEY_COMPLEX_SMALL,1,color,2)
            roi_color = img[y:y+h, x:x+w]

    cv2.imshow("Result", img)

    if cv2.waitKey(1) & 0xFF == ord('q'):
         break