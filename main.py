#!/usr/bin/env python

import cv2
import sys
import numpy as np
import os
import math

# debug = True
debug = False

def distance(x1, y1, x2, y2):
	return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

def getTotalFrames(path):
	cap = cv2.VideoCapture(path)
	counter = 0
	while True:
		_, frame = cap.read()
		if frame is None:
			break
		counter += 1
	return counter

def initProgressBar():
	bar_width = os.get_terminal_size().columns - 7

	sys.stdout.write('[%s]' % (' ' * bar_width))
	sys.stdout.flush()
	sys.stdout.write('\r[\n')

def updateProgressBar(progress):
	sys.stdout.write('\033[F') # go to beginning of previous line

	bar_width = os.get_terminal_size().columns - 7

	fill_count = round(progress * bar_width)
	sys.stdout.write('[' + '-' * fill_count)

	blank_count = round((1.0 - progress) * bar_width)
	progress = int(progress * 100)
	padding = '   '[:-len(str(progress))]
	sys.stdout.write(' ' * blank_count + '] ' + padding + str(progress) + '%\n')
	sys.stdout.flush()

def loadCascade(file):
	return cv2.CascadeClassifier('cascades/' + file)

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
	total_frames = getTotalFrames(sys.argv[1])
	frame_count = 0

	last_eye_left = [0, 0, 0, 0]
	last_eye_right = [0, 0, 0, 0]

	while True:
		_, frame = capture.read()
		
		if frame is None:
			return

		frame = np.array(frame, np.uint8)

		gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

		faces = face_cascade.detectMultiScale(gray, 1.1, 5)
		for (x, y, w, h) in faces:

			half = int(w / 2)
			paddingTop = int(h * 0.2)
			paddingBottom = int(h * 0.45)

			if debug:
				cv2.rectangle(frame, (x, y+paddingTop), (x+half, y+h - paddingBottom), (0, 255, 0), 2)
				cv2.rectangle(frame, (x+half, y+paddingTop), (x+w, y+h - paddingBottom), (0, 255, 0), 2)

			def getBetterPosition(rect1, rect2):
				ex1, ey1, ew1, eh1 = rect1
				ex2, ey2, ew2, eh2 = rect2
				if ew1 != 0 and eh1 != 0 and ew2 != 0 and eh2 != 0:
					rate = 0
					# try 20
					# rate = 20

					x = ex1 if distance(ex1, ey1, ex2, ey2) < rate else ex2
					y = ey1 if distance(ex1, ey1, ex2, ey2) < rate else ey2
					return (x, y)
				return (ex1, ey1)

			def processEye(eye, ex, ey, ew, eh):
				if debug:
					cv2.rectangle(frame, (ex, ey), (ex+ew, ey+eh), (0, 0, 255), 2)

				eye_copy = cv2.resize(eye, (ew, eh))
				roi_eye = frame[ey:ey+ew, ex:ex+ew]
				overlayImage(roi_eye, eye_copy)

			def processListOfEyes(eyes, offset, last_eye):
				for (ex, ey, ew, eh) in eyes:
					
					ex, ey = getBetterPosition((ex, ey, ew, eh), last_eye)

					ew, eh = int(w * 0.25), int(w * 0.25)

					processEye(eye, x+ex+offset, y+ey+paddingTop, ew, eh)

					last_eye[:] = []
					last_eye.extend((ex, ey, ew, eh))

			# Define 2 areas for the left and right part of the face

			face_gray_left = gray[y+paddingTop:y+h - paddingBottom, x:x+half]
			face_gray_right = gray[y+paddingTop:y+h - paddingBottom, x+half:x+w]

			# Get 2 lists of detected eyes

			eyes_left = eye_cascade.detectMultiScale(face_gray_left, 1.02, 5)
			eyes_right = eye_cascade.detectMultiScale(face_gray_right, 1.02, 5)

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
		updateProgressBar(progress)

def quit(capture, video):
	capture.release()
	video.release()

def main():
	global face_cascade, eye_cascade, eye
	face_cascade = loadCascade('haarcascade_frontalface_default.xml')
	eye_cascade = loadCascade('haarcascade_eye.xml')

	eye = cv2.imread('resources/eye.jpg')

	cap, video = init(sys.argv[1], sys.argv[2])

	initProgressBar()

	loop(cap, video)

	quit(cap, video)

if __name__ == '__main__':
	if (len(sys.argv) == 3):
		main()
	else:
		print('usage: python', sys.argv[0], '<input.webm> <output.webm>')
		sys.exit()
