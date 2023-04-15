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
from calculate_direction import *
from PIL import Image, ImageFilter
import numpy as np
from Coordenadas_Snake import *
from Coordenadas_Fruta import find_food
# Inicializar el navegador
driver = webdriver.Chrome()

# Cargar la página web con el canvas
driver.get("https://www.google.com/fbx?fbx=snake_arcade")

# Esperar a que la página cargue completamente
driver.implicitly_wait(100)

# Localizar el elemento canvas
play_button = driver.find_element(By.CLASS_NAME,"FL0z2d.Uxkl7b")
play_button.click()
canvas = driver.find_element(By.CLASS_NAME,"cer0Bd")
previous_image = None
# Acciones en el elemento canvas

#actions = ActionChains(driver)
#actions.move_to_element(canvas).click_and_hold().move_by_offset(50, 50).release().perform()

# Cerrar el navegador
#driver.quit()
# Definir el tamaño de la cuadrícula y el tamaño de cada celda

#cell_size = 32
snake_length =3
previous_fruit = (12,7)
snake_position_list = []
previous_snake = None
previous_fruit = None
cell_size = 32
def generate_graph():
    # Define the dimensions of the board and the cell size

    # Initialize the graph
    graph = {}
    # Loop through the cells and add nodes to the graph
    for x in range(cell_size // 2, width-32, cell_size):
        for y in range(cell_size // 2, height-32, cell_size-1):
           r, g, b, a = pixels[x, y]
           #print(x//32,y//32, r,g,b)
           if ((r < 215 or r > 230) and (g < 105 or g > 140)):
            node = (x // cell_size, y // cell_size)
            graph[node] = {} 
                # Check the neighboring cells to find connections
            for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                nx, ny = x + dx * cell_size, y + dy * cell_size
                if 0 <= nx < width-32 and 0 <= ny < height-32:
                    r, g, b, a = pixels[nx, ny]
                    if ((r < 215 or r > 240) and (g < 105 or g > 140)):
                        neighbor = (nx // cell_size, ny // cell_size)
                        graph[node][neighbor] = 1
    #for node, neighbors in graph.items():
        #print(f"Node {node}:")
        #for neighbor, cost in neighbors.items():
           #print(f"  -> Neighbor {neighbor} (cost {cost})")#g = draw_graph_on_image(graph, ci)
    #g = draw_graph_on_image(graph,ci)
    #print(snake)
    return graph


def draw_graph_on_image(graph, image_path):
    # Load the original image
    image = image_path
    # Draw the edges between nodes
    draw = ImageDraw.Draw(image)
    for x in range(0, image.width, cell_size):
        draw.line([(x, 0), (x, image.height)], fill=(0, 255, 0), width=1)
    for y in range(0, image.height, cell_size):
        draw.line([(0, y), (image.width, y)], fill=(0, 255, 0), width=1)
    
    # Save the new image with the graph drawn on it
    img = np.array(image)
    cv2.imshow('Game Image', img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
def find_snake_pixels(ci):
    pixels = ci.load()
    snake_pixels = []
    for x in range(ci.width):
        for y in range(ci.height):
            r, g, b, a = pixels[x, y]
            if r == 0 and g == 255 and b == 0:
                snake_pixels.append((x, y))
    return snake_pixels


previous_move="right"
while True:
    width = 18*cell_size-4
    height = 16*cell_size-7
    canvas_base64 = driver.execute_script("return arguments[0].toDataURL('image/png').substring(21);", canvas)
    canvas_png = base64.b64decode(canvas_base64)
    canvas_image = Image.open(io.BytesIO(canvas_png))
    box = (28, 25, width, height)
    ci = canvas_image.crop(box)
    snake = snake_position(ci)
    snake_pixel=find_snake_pixels(ci)
    fruit = find_food(ci)
    if fruit != previous_fruit:
        snake_length += 1
        previous_fruit = fruit

    if snake is not None and snake != previous_snake:
        if len(snake_position_list) < snake_length:
            snake_position_list.append(snake)
        else:
            # Mover todas las posiciones hacia la izquierda, eliminando el primer elemento
            snake_position_list.pop(0)
            snake_position_list.append(snake)

        if previous_snake is not None:
            if snake[0] != previous_snake[0]:
                # Añadir la nueva posición en el eje y
                y_range = range(min(previous_snake[1], snake[1]), max(previous_snake[1], snake[1])+1)
                for y in y_range:
                    position = (snake[0], y)
                    if position not in snake_position_list:
                        snake_position_list.append(position)
            elif snake[1] != previous_snake[1]:
                # Añadir la nueva posición en el eje x
                x_range = range(min(previous_snake[0], snake[0]), max(previous_snake[0], snake[0])+1)
                for x in x_range:
                    position = (x, snake[1])
                    if position not in snake_position_list:
                        snake_position_list.append(position)

        previous_snake = snake

    # Mostrar la imagen resultante
    pixels = ci.load()
    #ci.show()

    current_image = np.array(ci)
    if previous_image is not None:
        previous_image = np.array(previous_image)

        difference = np.sum(np.abs(current_image - previous_image))
        
        #if difference != 0:
            #print("El canvas ha cambiado")

        # Guardar la imagen actual para la próxima comparación
        previous_image = ci
        graph = generate_graph()
        print ("snake: ", snake)
        print ("fruit: ", fruit)
        if fruit is not None:
                #direction = a_star(graph, snake_position, food_position)
                    try:
                    #direction = calculate_direction(direction, snake_position, food_position)
                        #astar=a_star(graph, snake, fruit)
                    #print(astar)
                        #previous_move = move(previous_move,astar)
                        previous_move = calculate_direction(snake, fruit, previous_move,snake_position_list)
                        
                        print(previous_move)
                       
                    except:
                        continue
                #pyautogui.press(direction)
                #pyautogui.press("space")

                #print("Posición de la comida: ", food_position)
            #print("Posición de la snake: ", snake_position)
        else:
            print("No se encontró comida en la imagen.")
        # Emitir una orden de movimiento a la serpiente para que se mueva en la dirección adecuada
    previous_image = ci
    if previous_move == "right":
        ActionChains(driver)\
        .key_down(Keys.ARROW_RIGHT)\
        .perform()
    elif previous_move == "left":
        ActionChains(driver)\
        .key_down(Keys.ARROW_LEFT)\
        .perform()
    elif previous_move == "up":
        ActionChains(driver)\
        .key_down(Keys.ARROW_UP)\
        .perform()
    elif previous_move == "down":
        ActionChains(driver)\
        .key_down(Keys.ARROW_DOWN)\
        .perform()

# Dibujar la cuadrícula en el canvas

# Esperar un momento para ver la cuadrícula
time.sleep(5)