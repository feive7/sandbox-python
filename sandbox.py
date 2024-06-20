import pygame
import numpy as np
from time import sleep
import random
pygame.init()
pygame.display.init()
pygame_icon = pygame.image.load('icon.png')
pygame.display.set_icon(pygame_icon)
pygame.display.set_caption("Sandbox")

SIZE = 64
SCREEN_SIZE = SIZE * 4
tile_size = SCREEN_SIZE//SIZE
Map = np.zeros((SIZE,SIZE))
screen = pygame.display.set_mode((SCREEN_SIZE,SCREEN_SIZE))
color = ["Black","Red","Green","Blue","Cyan","Magenta","Yellow","White"]
current_color = 1
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
    buffer = np.zeros((SIZE,SIZE))
    for x in range(SIZE):
        for y in range(SIZE):
            if get_tile(x,y+1) and get_tile(x,y):
                moves = []
                if not get_tile(x+1,y+1):
                    moves.append(1)
                if not get_tile(x-1,y+1):
                    moves.append(-1)
                if len(moves) > 0:
                    buffer[y+1][x+random.choice(moves)] = get_tile(x,y)
                else:
                    buffer[y][x] = get_tile(x,y)
            elif get_tile(x,y-1):
                buffer[y][x] = get_tile(x,y-1)
    Map = buffer
clock = pygame.time.Clock()
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            else:
                key = pygame.key.name(event.key)
                if key in "1234567":
                    current_color = pygame.key.name(event.key)
    clock.tick(60)
    if pygame.mouse.get_pressed()[0]:
        draw(pygame.mouse.get_pos(),current_color)
    elif pygame.mouse.get_pressed()[2]:
        draw(pygame.mouse.get_pos(),0)
    draw_map()
    pygame.display.update()
    tick()
pygame.quit()
