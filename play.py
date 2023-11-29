import os
os.environ["OMP_NUM_THREADS"] = '1'
import win32gui
from PIL import ImageGrab
import cv2 as cv
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
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
    plt.imshow(img1)
    plt.show()
    img1_bgr = cv.cvtColor(img1,cv.COLOR_RGB2BGR)
    img2_bgr = cv.cvtColor(img2,cv.COLOR_RGB2BGR)
    img1_blur = cv.blur(img1_bgr,(5,5)).astype(np.int16)
    img2_blur = cv.blur(img2_bgr,(5,5)).astype(np.int16)
    newimg = abs(img2_blur-img1_blur).astype(np.uint8)
    newimg = cv.cvtColor(newimg,cv.COLOR_BGR2GRAY)
    contrast = 0
    brightness = 0
    newimg = newimg.astype(np.int16) * (contrast/127 + 1) - contrast+brightness 
    newimg = newimg.astype(np.uint8)
    ret,thresh = cv.threshold(newimg,20,1,cv.THRESH_BINARY)#阈值设置为25 大于该阈值设置为1

    contours, hierarchy = cv.findContours(thresh, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    km = KMeans(n_clusters=5,n_init=20)
    data = np.vstack(contours)
    dataShape = data.shape
    data = data.reshape((dataShape[0],dataShape[2]))
    km.fit(data)
    for x,y in km.cluster_centers_:
        clickX = x1+IMG1_LEFT+int(x)
        clickY = y1 +IMG1_TOP+int(y)
        pyautogui.click(x=clickX,y=clickY)
        time.sleep(0.5)   
    pyautogui.moveTo(100,100)
for i in range(1):
    play()
    time.sleep(4)