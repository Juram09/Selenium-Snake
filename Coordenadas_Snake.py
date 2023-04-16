from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import time
from PIL import Image, ImageDraw
import io
import base64
import cv2
import numpy as np
from calculate_direction import move, a_star
from PIL import Image, ImageFilter
import numpy as np


cell_size=32

def snake_position(ci):
    # Convertir la imagen a formato HSV
    hsv_image = cv2.cvtColor(np.array(ci), cv2.COLOR_RGB2HSV)
    lower_orange = np.array([0, 0, 240])
    upper_orange = np.array([255, 255, 255])
    # Crear una máscara que detecte los colores dentro de los límites especificados
    mask = cv2.inRange(hsv_image, lower_orange, upper_orange)
    pil_image = Image.fromarray(mask)
    pil_image = pil_image.filter(ImageFilter.GaussianBlur(radius=2))
    cv2_image = cv2.cvtColor(np.array(pil_image), cv2.COLOR_RGB2BGR)
    #pil_image.show()
    # Detectar los bordes en la imagen usando el operador Canny
    #blur_image = cv2.GaussianBlur(cv2_image, (5, 5), 0)
    canny_image = cv2.Canny(cv2_image, 100, 200) 
    contours, _ = cv2.findContours(canny_image, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    if len(contours) > 0:
        largest_contour=max(contours, key=cv2.contourArea)
        moments = cv2.moments(largest_contour)
        if moments['m00'] > 0:
            cx = int(moments['m10'] / moments['m00'])
            cy = int(moments['m01'] / moments['m00'])
        #cv2.circle(mask, (cx, cy), 5, (255, 255, 255),-1)
        #cv2.circle(mask, (cx, cy), 2, (255, 255, 255))
        #cv2.imshow('Game Image', cv2_image)
        #cv2.waitKey(0)
        #cv2.destroyAllWindows()
        snake_head_position = (cx // cell_size, cy // cell_size)
        return snake_head_position
    
    # Si no se detectó ningún contorno, devolver None
    return None


def eyes_position(ci):
    # Convertir la imagen a formato HSV
    hsv_image = cv2.cvtColor(np.array(ci), cv2.COLOR_RGB2HSV)
    lower_orange = np.array([0, 0, 200])
    upper_orange = np.array([255, 20, 255])
    # Crear una máscara que detecte los colores dentro de los límites especificados
    mask = cv2.inRange(hsv_image, lower_orange, upper_orange)
    # Detectar los bordes en la imagen usando el operador Canny
    blur_image = cv2.GaussianBlur(mask, (5, 5), 0)
    canny_image = cv2.Canny(blur_image, 100, 200) 
    contours, _ = cv2.findContours(canny_image, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    if len(contours) > 0:
        largest_contour=max(contours, key=cv2.contourArea)
        moments = cv2.moments(largest_contour)
        if moments['m00'] > 0:
            cx = int(moments['m10'] / moments['m00'])
            cy = int(moments['m01'] / moments['m00'])
        #cv2.circle(mask, (cx, cy), 5, (255, 255, 255),-1)
        #cv2.circle(mask, (cx, cy), 2, (255, 255, 255))
        #cv2.imshow('Game Image', mask)
        #cv2.waitKey(0)
        #cv2.destroyAllWindows()
        snake_head_position = (cx // cell_size, cy // cell_size)
        return snake_head_position
    # Si no se detectó ningún contorno, devolver None
    return None
 