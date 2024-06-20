import pygame
import numpy as np
from time import sleep
import random
import colorsys
pygame.init()
pygame.display.init()
pygame_icon = pygame.image.load('icon.png')
pygame.display.set_icon(pygame_icon)
pygame.display.set_caption("Sandbox")

SIZE = 64
SCREEN_SIZE = SIZE * 8
tile_size = SCREEN_SIZE//SIZE
Map = np.zeros((SIZE,SIZE))
screen = pygame.display.set_mode((SCREEN_SIZE,SCREEN_SIZE+30))
color = ["Black"]
color += [np.multiply(colorsys.hsv_to_rgb(i/10, 1, 1),255) for i in range(0,10)]
color += [(i,i,i) for i in range(255,33,-255//6)]
pallette = color[1:len(color)]
current_color = 0
def draw_map():
    for x in range(SIZE):
        for y in range(SIZE):
            pygame.draw.rect(screen, color[int(Map[y][x])], pygame.Rect(tile_size*x,tile_size*y,tile_size,tile_size))
def get_tile(x,y):
    if x >= 0 and x < SIZE and y >= 0 and y < SIZE:
        return Map[y][x]
    elif y >= SIZE or x < 0 or x >= SIZE:
        return 1
    else:
        return 0
def draw(cell,color):
    tile_x = cell[0] // tile_size
    tile_y = cell[1] // tile_size
    if tile_x >= 0 and tile_x < SIZE and tile_y >= 0 and tile_y < SIZE: 
        Map[tile_y][tile_x] = color
def tick():
    global Map
    buffer = np.zeros((SIZE, SIZE))

    for x in range(SIZE):
        for y in range(SIZE):
            current_tile = get_tile(x, y)
            if current_tile:
                below = get_tile(x, y + 1)
                if not below:
                    buffer[y + 1][x] = current_tile
                else:
                    moves = []
                    left_below = get_tile(x - 1, y + 1)
                    right_below = get_tile(x + 1, y + 1)
                    if not right_below:
                        moves.append(1)
                    if not left_below:
                        moves.append(-1)
                    if moves:
                        move = random.choice(moves)
                        buffer[y + 1][x + move] = current_tile
                    else:
                        buffer[y][x] = current_tile
    Map = buffer
def draw_menu():
    pygame.draw.rect(screen, (100,100,100), (0, SCREEN_SIZE, SCREEN_SIZE, 30))
    for i,c in enumerate(pallette):
        pygame.draw.rect(screen, c, ((SCREEN_SIZE//len(pallette)) * i, SCREEN_SIZE + (5 * (i != current_color)), SCREEN_SIZE/len(pallette), 25))
clock = pygame.time.Clock()
running = True
draw_menu()
drawing = False
def handle_mouse_down(pressed):
    if pygame.mouse.get_pressed()[0]:
        draw(pygame.mouse.get_pos(),current_color+1)
    elif pygame.mouse.get_pressed()[2]:
        draw(pygame.mouse.get_pos(),0)
def handle_key_down(event):
    if event.key == pygame.K_ESCAPE:
        running = False
    else:
        key = event.key
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            handle_key_down(event)
        elif event.type == pygame.MOUSEWHEEL:
            current_color = ((current_color - np.sign(event.y)) % len(pallette))
            draw_menu()
    clock.tick(60)
    if pygame.mouse.get_pressed():
        handle_mouse_down(pygame.mouse.get_pressed())
    
    draw_map()
    pygame.display.update()
    tick()
pygame.quit()
