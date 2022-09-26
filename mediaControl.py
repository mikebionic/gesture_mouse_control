import cv2 
import numpy as np
import pyautogui
from time import sleep
import sys
import _thread

config = {
    "capture_port": 0,
    "screenWidth": 1920,
    "screenHeight": 1080,
    "frameWidth": 640,
    "frameHeight": 480,
	"button_pause_time": 1,
    "button_action_key": "space"
}

try:
	with open('config.json', 'r') as f:
		config = json.load(f)
except:
	pass

capture_port = int(sys.argv[1]) if len(sys.argv) > 1 else config['capture_port']
screenHeight = int(sys.argv[3]) if len(sys.argv) > 3 else config['screenHeight']
screenWidth  = int(sys.argv[2]) if len(sys.argv) > 2 else config['screenWidth']
frameWidth = config['frameWidth']
frameHeight = config['frameHeight']
button_pause_time = config['button_pause_time']
button_action_key = config['button_action_key']

fist = cv2.CascadeClassifier('./data/fist.xml')
palm = cv2.CascadeClassifier('./data/open_palm.xml')

cap = cv2.VideoCapture(capture_port) 
scaling_factor = 0.5

pressed = False
spacePressed = False 

def control_by_rect(palm_rects, fist_rects):

	global pressed
	global spacePressed 

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
			pyautogui.press(button_action_key)
			spacePressed = True
			print('Button action called')
			sleep(1)
		else:
			spacePressed = False

while True:
	ret, frame = cap.read() 
	frame = cv2.flip(frame,1)   
	# frame = cv2.resize(frame, None, fx=scaling_factor, fy=scaling_factor, interpolation=cv2.INTER_AREA)
	fist_rects = fist.detectMultiScale(frame, scaleFactor=1.3, minNeighbors=5)  
	palm_rects = palm.detectMultiScale(frame, scaleFactor=1.3, minNeighbors=5)
	
	_thread.start_new_thread(control_by_rect,(palm_rects, fist_rects))
	cv2.imshow('Media dolanshyk', frame)
	    
	c = cv2.waitKey(1)     
	if c == 27:        
		break
cap.release() 
cv2.destroyAllWindows()