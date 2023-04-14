import pyautogui
import cv2
import numpy as np

cell_size = 32
def find_food(ci, width,height):

      # Convertir la imagen a formato HSV
    hsv_image = cv2.cvtColor(np.array(ci), cv2.COLOR_BGR2HSV)

    # Definir los límites de color para la manzana (naranja)
    lower_orange = np.array([0, 0, 0])
    upper_orange = np.array([100, 255, 255])

    # Aplicar la máscara para detectar la manzana (naranja)
    mask = cv2.inRange(hsv_image, lower_orange, upper_orange)
    #cv2.imshow('Game Image', mask)
    #cv2.waitKey(0)
    #cv2.destroyAllWindows()
    # Aplicar un filtro Gaussiano para reducir el ruido
    blur_image = cv2.GaussianBlur(mask, (5, 5), 0)

    # Detectar los bordes en la imagen usando el operador Canny
    canny_image = cv2.Canny(blur_image, 100, 200)
    # Encontrar los contornos de la máscara
    contours, _ = cv2.findContours(canny_image, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    
    # Si se detectó un contorno, devolver la posición de su centro
    if len(contours) > 0:
        #print(contours)
        largest_contour = min(contours, key=cv2.contourArea)
        moments = cv2.moments(largest_contour)
        #print(moments)
        if moments['m00'] > 0:
            cx = int(moments['m10'] / moments['m00'])
            cy = int(moments['m01'] / moments['m00'])
            for x in range(width):
                for y in range(height):# Red pixel for the fruit
                    fruit_position = (cx // cell_size, cy // cell_size)
                    return fruit_position
    
    # Si no se detectó ningún contorno, devolver None
    return None





