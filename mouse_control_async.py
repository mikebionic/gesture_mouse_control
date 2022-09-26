import sys, json, time
import cv2
import numpy as np
import pyautogui
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

# print(config, type(config['frameHeight']))
capture_port = int(sys.argv[1]) if len(sys.argv) > 1 else config['capture_port']
screenHeight = int(sys.argv[3]) if len(sys.argv) > 3 else config['screenHeight']
screenWidth  = int(sys.argv[2]) if len(sys.argv) > 2 else config['screenWidth']
frameWidth = config['frameWidth']
frameHeight = config['frameHeight']
button_pause_time = config['button_pause_time']
button_action_key = config['button_action_key']

myPoints = []
newPoints = []
perform = False

cap = cv2.VideoCapture(capture_port)
cap.set(3,frameWidth)
cap.set(4,frameHeight)

# brightness
cap.set(10,150)

# get colorPicker.py
# 1 pink
# 2 green
# 3 red
# 4 blue
myColors = config['myColors'] if 'myColors' in config else [
	[133, 37,163,179,210,255],
	[70,98,2,94,250,255],
	# [0,149,52,34,253,255],
	[0,207,255,112,255,255]]

myColorValues = config['myColorValues'] if 'myColorValues' in config else [
	[245,12,241],
	[2,199,50],
	# [0,40,255],
	[245,45,45]]

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
	return newPoints

def getContours(img):
	contours,hierarchy = cv2.findContours(img,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
	x,y,w,h = 0,0,0,0
	for cnt in contours:
		area = cv2.contourArea(cnt)
		if area>500:
			peri = cv2.arcLength(cnt,True)
			approx = cv2.approxPolyDP(cnt,0.02*peri,True)
			x,y,w,h = cv2.boundingRect(approx)
	return x+w//2,y

def drawOnCanvas(myPoints,myColorValues):
	for point in myPoints:
		cv2.circle(imgResult,(point[0],point[1]),10,myColorValues[point[2]],cv2.FILLED)


def moveUI(newPoints):
	print(newPoints)
	action_type = "move"
	point_x = 450
	point_y = 450

	# action types : move drag zoom
	if len(newPoints) > 0:
		if len(newPoints) == 2:
			action_type = "drag"
		if len(newPoints) == 1:
			action_type = "move"

		if len(newPoints) > 2:
			pyautogui.press(button_action_key)
			time.sleep(button_pause_time)

		if not len(newPoints) > 2:
			for this_point in newPoints:
				if this_point[-1] == 0:
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

		# pyautogui.moveTo(1080, 380)
		# pyautogui.mouseDown(button='left')
		# pyautogui.dragTo(917, 564, 1, button='left')
		# pyautogui.mouseUp(button='left')

while 1:
	success, img = cap.read()
	img = cv2.flip(img,1)
	imgResult = img.copy()
	newPoints = findColor(img,myColors,myColorValues)
	if len(newPoints)!=0:
	# 	drawOnCanvas(myPoints,myColorValues)
		for newP in newPoints:
			myPoints.append(newP)

	keyboard_command = cv2.waitKey(10) & 0xFF
	if keyboard_command == ord('p'):
		perform = not perform
		if perform:
			print ('Mouse simulation ON...')
		else:
			print ('Mouse simulation OFF...')

	if perform:
		_thread.start_new_thread(moveUI,(newPoints,))

	cv2.imshow("dolanshyk",imgResult)
	if keyboard_command == ord('q'):
		break
