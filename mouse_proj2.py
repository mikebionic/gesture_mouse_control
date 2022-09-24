import cv2
import numpy as np
import pyautogui

import _thread

global newPoints

import sys
capture_port = int(sys.argv[1]) if len(sys.argv) > 1 else 2
screenWidth  = int(sys.argv[2]) if len(sys.argv) > 2 else 1920
screenHeight = int(sys.argv[3]) if len(sys.argv) > 3 else 1080

#screenWidth = 1366
#screenHeight = 768

frameWidth = 640
frameHeight = 480
cap = cv2.VideoCapture(capture_port)
cap.set(3,frameWidth)
cap.set(4,frameHeight)
# brightness
cap.set(10,150)
# get colorPicker.py (1:52:24)
global myColors
myColors = [[5,107,0,19,255,255],
			[133,56,0,159,156,255],
			[57,76,0,100,255,255],
			[90,48,0,118,255,255]]

myColorValues = [[51,153,255],
				[255,0,255],
				[0,255,0],
				[255,0,0]]
myPoints = []

def findColor(img,myColors,myColorValues):
	imgHSV = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
	count = 0
	newPoints=[]
	for color in myColors:
		lower = np.array(color[0:3])
		upper = np.array(color[3:6])
		mask = cv2.inRange(imgHSV,lower,upper)
		x,y = getContours(mask)
		cv2.circle(imgResult,(x,y),10,myColorValues[count],cv2.FILLED)
		if x!=0 and y!=0:
			newPoints.append([x,y,count])
		count+=1
		# cv2.imshow(str[0]),mask)
	return newPoints

def getContours(img):
	contours,hierarchy = cv2.findContours(img,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
	x,y,w,h = 0,0,0,0
	for cnt in contours:
		area = cv2.contourArea(cnt)
		# print(area)
		if area>500:
			# cv2.drawContours(imgResult,cnt,-1,(255,0,0),3)
			peri = cv2.arcLength(cnt,True)
			approx = cv2.approxPolyDP(cnt,0.02*peri,True)
			x,y,w,h = cv2.boundingRect(approx)
	return x+w//2,y

def drawOnCanvas(myPoints,myColorValues):
	for point in myPoints:
		cv2.circle(imgResult,(point[0],point[1]),10,myColorValues[point[2]],cv2.FILLED)


def moveUI(newPoints):
	while 1:
		action_type = "move"
		point_x = 450
		point_y = 450

		# action types : move drag zoom
		if len(newPoints) > 0:
			if len(newPoints) > 1:
				action_type = "drag"
			if len(newPoints) == 1:
				action_type = "move"

			if len(newPoints) > 2:
				pyautogui.press("space")

			if not len(newPoints) > 2:
				for this_point in newPoints:
					if this_point[-1] == 3:
						point_x = newPoints[-1][0]
						point_y = newPoints[-1][1]
								
						screen_x = point_x*screenWidth/frameWidth
						screen_y = point_y*screenHeight/frameHeight
						if action_type == "move":
							pyautogui.mouseUp(button='left')
							pyautogui.moveTo(screen_x, screen_y)
						elif action_type == "drag":
							pyautogui.mouseDown(button='left')
							pyautogui.moveTo(screen_x, screen_y)
							# pyautogui.dragTo(screen_x, screen_y, 0, button='left')
						# else:

			# pyautogui.moveTo(1080, 380)
			# pyautogui.mouseDown(button='left')
			# pyautogui.dragTo(917, 564, 1, button='left')
			# time.sleep(10)
			# pyautogui.mouseUp(button='left')
			# time.sleep(2)


def processing_cv():
	while True:
		success, img = cap.read()
		img = cv2.flip(img,1)
		imgResult = img.copy()
		global newPoints
		newPoints = findColor(img,myColors,myColorValues)
		if len(newPoints)!=0:
			for newP in newPoints:
				myPoints.append(newP)
		# print(myPoints)
		# if len(myPoints)!=0:
		# 	drawOnCanvas(myPoints,myColorValues)
		cv2.imshow("dolanshyk",imgResult)
		if cv2.waitKey(1) & 0xFF == ord('q'):
			break

newPoints = [[81, 24, 3]]
_thread.start_new_thread(processing_cv,())
_thread.start_new_thread(moveUI,(newPoints,()))

while 1:
	pass


