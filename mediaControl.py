import cv2 
import numpy as np
import pyautogui
from time import sleep

import sys
capture_port = int(sys.argv[1]) if len(sys.argv) > 1 else 2


# cascade = cv2.CascadeClassifier('./data/haarcascade_frontalface_alt.xml')
fist = cv2.CascadeClassifier('./data/fist.xml')
palm = cv2.CascadeClassifier('./data/open_palm.xml')
# cascade = cv2.CascadeClassifier('./data/haarcascade_righteye_2splits.xml')
cap = cv2.VideoCapture(capture_port) 
scaling_factor = 0.5

pressed = False
spacePressed = False 

while True:
	ret, frame = cap.read() 
	frame = cv2.flip(frame,1)   
	frame = cv2.resize(frame, None, fx=scaling_factor, fy=scaling_factor, interpolation=cv2.INTER_AREA)
	fist_rects = fist.detectMultiScale(frame, scaleFactor=1.3, minNeighbors=3)  
	palm_rects = palm.detectMultiScale(frame, scaleFactor=1.3, minNeighbors=3)
	for (x,y,w,h) in palm_rects:
		centerx = 150
		cv2.rectangle(frame, (x,y), (x+w,y+h), (0,255,100), 5)
		centerx=x+w//2
		centery=y+h//2
		cv2.circle(frame,(centerx,centery),4,(200,200,0),3)
		if (pressed==False and centerx<120):
			pyautogui.press('left')
			pressed = True
			sleep(1)
		if (pressed==False and centerx>210):
			pyautogui.press('right')
			pressed = True
			sleep(1)
		if (pressed==False and centery<120):
			pyautogui.press('up')
			pressed = True
			sleep(1)
		if (pressed==False and centery>160):
			pyautogui.press('down')
			pressed = True
			sleep(1)
		# if (centerx>120 and centerx<210):
		else:
			pressed = False
		print (centery) #show the x position

	for (x,y,w,h) in fist_rects:
		cv2.rectangle(frame, (x, y), (x+w,y+h), (0,255,100), 5)
		if (spacePressed==False):
			pyautogui.press('space')
			spacePressed = True
			print('pressed space' )
			sleep(1)
		else:
			spacePressed = False
			
	cv2.imshow('Media control', frame)
	    
	c = cv2.waitKey(1)     
	if c == 27:        
		break
cap.release() 
cv2.destroyAllWindows()