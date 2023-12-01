import os
os.environ["OMP_NUM_THREADS"] = '1'
import win32gui
from PIL import ImageGrab
import cv2 as cv
import time
import pyautogui
import numpy as np

def get_window_pos(name):
    handle = win32gui.FindWindow(0, name)
    return None if handle==0 else win32gui.GetWindowRect(handle)

def grab_screen(position):
    return ImageGrab.grab(position)
def play():
    x1, y1, x2, y2 = get_window_pos('大家来找茬')
    game_window_img = grab_screen((x1, y1, x2, y2))
    img = np.array(game_window_img)
    IMG1_TOP = 312
    IMG1_BOTTOM = 598
    IMG1_LEFT = 93
    IMG1_RIGHT = 474
    IMG2_OFFSET = IMG1_RIGHT-IMG1_LEFT+76
    img1 = img[IMG1_TOP:IMG1_BOTTOM,IMG1_LEFT:IMG1_RIGHT,:]
    img2 = img[IMG1_TOP:IMG1_BOTTOM,IMG1_LEFT+IMG2_OFFSET:IMG1_RIGHT+IMG2_OFFSET,:]
    
    offset = img1.mean(0).mean(0) - img2.mean(0).mean(0)
    offset_img = np.zeros(img1.shape)
    offset_img[:,:,0] = offset[0]
    offset_img[:,:,1] = offset[1]
    offset_img[:,:,2] = offset[2]
    offset_img = offset_img.astype(np.uint8)
    offset_img = cv.add(img2,offset_img)
    img2 = offset_img
    redimg = abs(img1[:,:,0].astype('int16') - img2[:,:,0].astype('int16')).astype('uint8')
    greenimg = abs(img1[:,:,1].astype('int16') - img2[:,:,1].astype('int16')).astype('uint8')
    blueimg = abs(img1[:,:,2].astype('int16') - img2[:,:,2].astype('int16')).astype('uint8')
    redimg = cv.fastNlMeansDenoising(redimg,0.5,7,21)
    greenimg = cv.fastNlMeansDenoising(greenimg,0.5,7,21)
    blueimg = cv.fastNlMeansDenoising(blueimg,0.5,7,21)
    redimg = redimg.astype('int16')
    redimg = (redimg*redimg*0.2).astype('uint8')
    greenimg = greenimg.astype('int16')
    greenimg = (greenimg*greenimg*0.2).astype('uint8')
    blueimg = blueimg.astype('int16')
    blueimg = (blueimg*blueimg*0.2).astype('uint8')
    rgbimg = cv.add(redimg,greenimg)
    rgbimg = cv.add(rgbimg,blueimg)
    ret,thresh = cv.threshold(rgbimg,100,1,cv.THRESH_BINARY)
    rgbimg = cv.fastNlMeansDenoising(rgbimg,None,7,21)

    contours, hierarchy = cv.findContours(thresh, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    contours = sorted(list(contours),key = lambda x:cv.contourArea(x),reverse=True)
    for i in range(6):
        M = cv.moments(contours[i])
        cX = int(M["m10"] / M["m00"])
        cY = int(M["m01"] / M["m00"])
        clickX = x1+IMG1_LEFT+int(cX)
        clickY = y1 +IMG1_TOP+int(cY)
        pyautogui.click(x=clickX,y=clickY)
        time.sleep(2) 
    pyautogui.moveTo(100,100)
for i in range(1):#设置游戏轮数
    play()
    time.sleep(4)