import cv2
from cvzone.HandTrackingModule import HandDetector
from time import sleep
import numpy as np
from pynput.keyboard import Controller
import pygame

pygame.init()
pygame.mixer.init()

mc = pygame.mixer.Sound("kc.wav")

cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)

detector = HandDetector(detectionCon=0.9)
keys = [["Q", "W", "E", "R", "T", "Y", "U", "I", "O", "P"],
        ["A", "S", "D", "F", "G", "H", "J", "K", "L", ";"],
        ["Z", "X", "C", "V", "B", "N", "M", ",", ".", "/"],
        [" ", "Clear"]]

finalText = ""
keyboard = Controller()


class Button():
    def __init__(self, pos, text, size):
        self.pos = pos
        self.size = size
        self.text = text


buttonList = []
buttonSize = [100, 100]
buttonGap = 20

rows = len(keys)
cols = max(len(row) for row in keys)

keyboardWidth = cols * buttonSize[0] + (cols - 1) * buttonGap
keyboardHeight = rows * buttonSize[1] + (rows - 1) * buttonGap

startX = (1280 - keyboardWidth) // 2 
startY = 720 - keyboardHeight - 50

for i in range(rows):
    for j, key in enumerate(keys[i]):
        posX = startX + j * (buttonSize[0] + buttonGap)
        posY = startY + i * (buttonSize[1] + buttonGap)
        buttonList.append(Button([posX, posY], key, buttonSize))


def drawAll(img, buttonList):
    for button in buttonList:
        x, y = button.pos
        w, h = button.size
        cv2.rectangle(img, button.pos, (x + w, y + h), (255, 0, 255), 3)
        centerX = x + w // 2
        centerY = y + h // 2
        textSize, _ = cv2.getTextSize(button.text, cv2.FONT_HERSHEY_PLAIN, 2, 2)
        textX = centerX - textSize[0] // 2
        textY = centerY + textSize[1] // 2
        cv2.putText(img, button.text, (textX, textY),
                    cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 255), 2)
    return img


while True:
    success, img = cap.read()

    if success:
        img = cv2.resize(img, (1280, 720))
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        hands, _ = detector.findHands(imgRGB)
        img = drawAll(img, buttonList)

        if hands:
            for hand in hands:
                lmList = hand["lmList"]

                for button in buttonList:
                    x, y = button.pos
                    w, h = button.size

                    if x < lmList[8][0] < x + w and y < lmList[8][1] < y + h:
                        cv2.rectangle(img, (x - 5, y - 5), (x + w + 5, y + h + 5), (175, 0, 175), cv2.FILLED)
                        cv2.putText(img, button.text, (x + 20, y + 70),
                                    cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 255), 2)
                        l = np.linalg.norm(np.array(lmList[8]) - np.array(lmList[12]))
                        print(l)

                        if l < 30:
                            if button.text == "Clear":
                                finalText = ""
                                keyboard.release('a')
                                keyboard.release('b')
                                keyboard.release('c')
                                keyboard.release('d')
                                keyboard.release('e')
                                keyboard.release('f')
                                keyboard.release('g')
                                keyboard.release('h')
                                keyboard.release('i')
                                keyboard.release('j')
                                keyboard.release('k')
                                keyboard.release('l')
                                keyboard.release('m')
                                keyboard.release('n')
                                keyboard.release('o')
                                keyboard.release('p')
                                keyboard.release('q')
                                keyboard.release('r')
                                keyboard.release('s')
                                keyboard.release('t')
                                keyboard.release('u')
                                keyboard.release('v')
                                keyboard.release('w')
                                keyboard.release('x')
                                keyboard.release('y')
                                keyboard.release('z')
                                keyboard.release(';')
                                keyboard.release(',')
                                keyboard.release('.')
                                keyboard.release('/')
                                keyboard.release(' ')
                                sleep(0.1)
                            else:
                                keyboard.press(button.text)
                                pygame.mixer.Sound.play(mc)
                                cv2.rectangle(img, button.pos, (x + w, y + h), (0, 255, 0), cv2.FILLED)
                                cv2.putText(img, button.text, (x + 20, y + 70),
                                            cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 255), 2)
                                finalText += button.text
                                sleep(0.3)
                        else:
                            keyboard.release(button.text)

        cv2.rectangle(img, (startX, startY - 70), (startX + keyboardWidth, startY - 10), (175, 0, 175), cv2.FILLED)
        cv2.putText(img, finalText, (startX + 20, startY - 20),
                    cv2.FONT_HERSHEY_PLAIN, 5, (255, 255, 255), 5)

        cv2.imshow("Image", img)

    if cv2.waitKey(1) == ord('q'):
        break

cv2.destroyAllWindows()
