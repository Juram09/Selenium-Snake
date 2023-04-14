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

# Acciones en el elemento canvas

#actions = ActionChains(driver)
#actions.move_to_element(canvas).click_and_hold().move_by_offset(50, 50).release().perform()

# Cerrar el navegador
#driver.quit()
# Definir el tamaño de la cuadrícula y el tamaño de cada celda

#cell_size = 32

cell_size = 32
def generate_graph():
    width = 18*cell_size-4
    height = 16*cell_size-7
    canvas_base64 = driver.execute_script("return arguments[0].toDataURL('image/png').substring(21);", canvas)
    canvas_png = base64.b64decode(canvas_base64)
    canvas_image = Image.open(io.BytesIO(canvas_png))
    box = (29, 26, width, height)
    ci = canvas_image.crop(box)
    pixels = ci.load()
    ci.show()

    # Define the dimensions of the board and the cell size

    # Initialize the graph
    graph = {}
    # Loop through the cells and add nodes to the graph
    for x in range(cell_size // 2, width-32, cell_size):
        for y in range(cell_size // 2, height-32, cell_size-2):
           r, g, b, a = pixels[x, y]
           print(x//32,y//32, r,g,b)
           if ((r < 215 or r > 240) and (g < 105 or g > 140)):
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
    for node, neighbors in graph.items():
        print(f"Node {node}:")
        #for neighbor, cost in neighbors.items():
           #print(f"  -> Neighbor {neighbor} (cost {cost})")#g = draw_graph_on_image(graph, ci)
    g = draw_graph_on_image(graph,ci)
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

graph=generate_graph()
# Dibujar la cuadrícula en el canvas
driver.execute_script()

# Esperar un momento para ver la cuadrícula
time.sleep(5)