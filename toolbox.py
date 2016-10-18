import cv2
import math

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

def loadCascade(file):
	return cv2.CascadeClassifier('cascades/' + file)

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