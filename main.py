#!/usr/bin/env python

import cv2
import sys
import numpy as np
import toolbox
import progressbar

# debug = True
debug = False

def overlayImage(bg, overlay):
	gray = cv2.cvtColor(overlay, cv2.COLOR_BGR2GRAY)
	res, mask = cv2.threshold(gray, 10, 1, cv2.THRESH_BINARY_INV)

	h, w = mask.shape
	mask = np.repeat(mask, 3).reshape((h, w, 3))

	bg *= mask
	bg += overlay

def init(inputFile, outputFile):
	capture = cv2.VideoCapture(inputFile, 0)

	screen_size = (480, 360)
	fourcc = cv2.VideoWriter_fourcc(*'VP80')

	video = cv2.VideoWriter()
	video.open(outputFile, fourcc, 20.0, screen_size, True)

	return (capture, video)

def loop(capture, video):
	total_frames = toolbox.getTotalFrames(sys.argv[1])
	frame_count = 0

	last_eye_left = [0, 0, 0, 0]
	last_eye_right = [0, 0, 0, 0]

	while True:
		_, frame = capture.read()
		
		if frame is None:
			return

		gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

		faces = face_cascade.detectMultiScale(gray, 1.1, 5)
		for (x, y, w, h) in faces:

			half = int(w / 2)
			paddingTop = int(h * 0.2)
			paddingBottom = int(h * 0.45)

			if debug:
				color = (0, 255, 0)
				top = y+paddingTop
				bottom = y+h - paddingBottom
				cv2.rectangle(frame, (x 	, top), (x+half, bottom), color, 2)
				cv2.rectangle(frame, (x+half, top), (x+w   , bottom), color, 2)

			def processEye(eye, ex, ey, ew, eh):
				if debug:
					cv2.rectangle(frame, (ex, ey), (ex+ew, ey+eh), (0, 0, 255), 2)

				eye_copy = cv2.resize(eye, (ew, eh))
				roi_eye = frame[ey:ey+ew, ex:ex+ew]
				overlayImage(roi_eye, eye_copy)

			def processListOfEyes(eyes, offset, last_eye):
				for (ex, ey, ew, eh) in eyes:
					
					ex, ey = toolbox.getBetterPosition((ex, ey, ew, eh), last_eye)

					ew, eh = int(w * 0.25), int(w * 0.25)

					processEye(eye, x+ex+offset, y+ey+paddingTop, ew, eh)

					last_eye[:] = []
					last_eye.extend((ex, ey, ew, eh))

			# Define 2 areas for the left and right part of the face

			face_gray_left = gray[y+paddingTop:y+h - paddingBottom, x:x+half]
			face_gray_right = gray[y+paddingTop:y+h - paddingBottom, x+half:x+w]

			# Get 2 lists of detected eyes

			eyes_left = eye_cascade.detectMultiScale(face_gray_left, 1.02, 5,
				# minSize=(int(w / 8), int(h / 8)),
				# maxSize=(int(w / 3), int(h / 3))
			)
			eyes_right = eye_cascade.detectMultiScale(face_gray_right, 1.02, 5,
				# minSize=(int(w / 8), int(h / 8)),
				# maxSize=(int(w / 3), int(h / 3))
			)

			# Draw eyes from list of detected eyes

			processListOfEyes(eyes_left, 0, last_eye_left)
			processListOfEyes(eyes_right, half, last_eye_right)

			# If no eye was detected draw the eye from the previous frame

			if last_eye_left is not None and len(eyes_left) == 0:
				ex, ey, ew, eh = last_eye_left
				processEye(eye, x+ex, y+ey+paddingTop, ew, eh)

			if last_eye_right is not None and len(eyes_right) == 0:
				ex, ey, ew, eh = last_eye_right
				processEye(eye, x+ex+half, y+ey+paddingTop, ew, eh)

		# Write the frame to the output video file

		video.write(frame)

		# Update the progress bar

		frame_count += 1
		progress = frame_count / total_frames
		progressbar.update(progress)

def quit(capture, video):
	capture.release()
	video.release()

def main():
	global face_cascade, eye_cascade, eye
	face_cascade = toolbox.loadCascade('haarcascade_frontalface_default.xml')
	eye_cascade = toolbox.loadCascade('haarcascade_eye.xml')

	eye = cv2.imread('resources/eye.jpg')

	cap, video = init(sys.argv[1], sys.argv[2])

	progressbar.init()

	loop(cap, video)

	quit(cap, video)

if __name__ == '__main__':
	if (len(sys.argv) == 3):
		main()
	else:
		print('usage: python', sys.argv[0], '<input.webm> <output.webm>')
		sys.exit(1)
