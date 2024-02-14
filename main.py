import cv2
from cvzone.HandTrackingModule import HandDetector
import time

class Button:
    def __init__(self, pos, width, height, value, color=(0, 255, 0), border_color=(0, 0, 255), border_width=3):
        self.pos = pos
        self.width = width
        self.height = height
        self.value = value
        self.color = color
        self.border_color = border_color
        self.border_width = border_width

    def draw(self, img):
        cv2.rectangle(img, self.pos, (self.pos[0] + self.width, self.pos[1] + self.height),
                      (225,225,225), cv2.FILLED)  # Draw filled interior
        cv2.rectangle(img, self.pos, (self.pos[0] + self.width, self.pos[1] + self.height),
                      (50,50,50), self.border_width)  # Draw borders
        cv2.putText(img, self.value, (self.pos[0] + 5, self.pos[1] + 35), cv2.FONT_HERSHEY_PLAIN,
                    2, (50, 50, 50), 2)

    def checkClick(self, x, y):
        if self.pos[0]<x<self.pos[0]+self.width and \
            self.pos[1]<y<self.pos[1]+self.height:
            cv2.rectangle(img, self.pos, (self.pos[0] + self.width, self.pos[1] + self.height),
                      (255,255,255), cv2.FILLED)  # Draw filled interior
            cv2.rectangle(img, self.pos, (self.pos[0] + self.width, self.pos[1] + self.height),
                      (50,50,50), self.border_width)  # Draw borders
            cv2.putText(img, self.value, (self.pos[0] + 3, self.pos[1] + 45), cv2.FONT_HERSHEY_PLAIN,
                    3, (0, 0, 0), 3)
            return True
        else:
            return False

# Initialize the HandDetector object


# Create buttons with customizable positions, sizes, colors, and text
# Buttons
buttonListValues = [['7', '8', '9', '*'],
                    ['4', '5', '6', '-'],
                    ['1', '2', '3', '+'],
                    ['0', '/', '.', '=']]
buttonList = []
for y in range(4):
    for x in range(4):
        xpos = x * 50    # Adjusted for 640x480 resolution
        ypos = y * 50+50   # Adjusted for 640x480 resolution
        buttonList.append(Button((xpos, ypos), 50, 50, buttonListValues[y][x]))  # Adjusted button size


#variable
myEquation = ''
delayCounter = 0

# Replace with your webcam index (check with `ls /dev/video*` on Linux/macOS)
cap = cv2.VideoCapture(0)
# Set camera resolution to 640x480
cap.set(3, 640)  # width
cap.set(4, 480)  # height
detector = HandDetector(detectionCon=0.8, maxHands=1)


while True:
    # Get image from camera
    success, img = cap.read()
    img = cv2.flip(img, 1)  # Flip horizontally (optional)
    # Detect hands
    hands, img = detector.findHands(img, flipType=False)
    # Draw All buttons
    cv2.rectangle(img, (0, 0), (0 + 200, 0 + 50),
                  (125, 125, 125), cv2.FILLED)
    cv2.rectangle(img, (0, 0), (0 + 210, 0 + 50),
                  (50, 50, 50), 3)
    cv2.rectangle(img, (0, 0), (0 + 240, 0 + 50),
                  (100, 100, 100), cv2.FILLED)
    cv2.rectangle(img, (0, 0), (0 + 240, 0 + 50),
                  (50, 50, 50), 3)
    cv2.putText(img, "c", (0 + 210, 0 + 30), cv2.FONT_HERSHEY_PLAIN,
                    2, (225, 225, 225), 2)
    for button in buttonList:
        button.draw(img)

    #check for hand
    if hands:
        lmList = hands[0]['lmList']
        length,_,img = detector.findDistance(lmList[8][:2], lmList[12][:2], img) 
        x,y = lmList[8][:2]
        if length < 40:
            for i, button in enumerate(buttonList):
                if button.checkClick(x,y) and delayCounter == 0:
                    myvalue = buttonListValues[int(i/4)][int(i%4)]
                    if myvalue == "=":
                        myEquation = str(eval(myEquation))
                    else:    
                        myEquation += myvalue
                    delayCounter = 1
              
    
    # To avoid Duplicates
    if delayCounter != 0 :
        delayCounter += 1
        if delayCounter > 10 :
            delayCounter = 0
    

    #Display the Equation/Result
    cv2.putText(img, myEquation, (10, 40), cv2.FONT_HERSHEY_PLAIN,
                2, (50, 50, 50), 2)

    cv2.imshow("Image", img)
    # Check for exit key press
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    if cv2.waitKey(1) == ord('c'):
        myEquation = ''

# Release resources
cap.release()
cv2.destroyAllWindows()
