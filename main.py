#!/usr/bin/env python

import cv2
import sys
import math
import numpy

faceCascPath = 'cascades/haarcascade_frontalface_default.xml'
eyeCascPath = 'cascades/haarcascade_eye.xml'

print('args')
print(sys.argv)

videoFile = sys.argv[1]
outputFile = sys.argv[2]

faceCascade = cv2.CascadeClassifier(faceCascPath)
eyeCascade = cv2.CascadeClassifier(eyeCascPath)

video_capture = cv2.VideoCapture(videoFile)

# Either set video to pre-defined size or set width/height to video size manually?
width = 480
height = 360
# video_capture.set(3,width)
# video_capture.set(4,height)

frame_number = 0

# If gui:
#win = cv2.namedWindow('Video')
#cv2.resizeWindow('Video', width, height)

# OpenCV3:
fourcc = cv2.VideoWriter_fourcc('V', 'P', '8', '0')
# OpenCV2:
# fourcc = cv2.cv.CV_FOURCC('V', 'P', '8', '0')

# OpenCV3:
video = cv2.VideoWriter()
video.open(outputFile,fourcc, 20.0, (width,height), True)
# OpenCV2:
# video = cv2.VideoWriter('output.webm',fourcc, 30.0, (width,height), True)

while True:
    # Capture frame-by-frame
    ret, frame = video_capture.read()

    if frame == None:
        break

    frame_number += 1
    print('Frame: %d' % frame_number)

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(30, 30),
        # OpenCV3:
        # ?? Not sure how to set CV_HAAR_SCALE_IMAGE flag
        # OpenCV2:
        # flags=cv2.CV_HAAR_SCALE_IMAGE
    )

    # Draw a rectangle around the faces
    for (x, y, w, h) in faces:
        # print(' > face detected: %d,%d %dx%d' % (x, y, w, h))
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 1)
        roi_gray = gray[y:y+h, x:x+w]
        roi_color = frame[y:y+h, x:x+w]

        eyes = eyeCascade.detectMultiScale(
            roi_gray,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(int(w / 8), int(h / 8)),
            maxSize=(int(w / 3), int(h / 3)),
            # OpenCV2:
            # flags=cv2.cv.CV_HAAR_SCALE_IMAGE
        )
        for (ex,ey,ew,eh) in eyes:
            # print(' > eye detected: %d,%d %dx%d' % (ex, ey, ew, eh))
            # Draw rectangle around eye
            cv2.rectangle(roi_color, (ex, ey), (ex+ew, ey+eh), (255, 0, 0), 1)

    # Display the resulting frame
    # If gui
    # cv2.imshow('Video', frame)
    video.write(frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

print('Finished, close input and write output')
video_capture.release()
video.release()

# If gui
# cv2.destroyAllWindows()
