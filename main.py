import pygame
import sys

pygame.init()

screen = pygame.display.set_mode((1920, 1080))
running = True
town_view = False

town_bg = pygame.image.load("map_test.png")
townbg_rect = town_bg.get_rect()
townbg_rect.center = (960, 540)

dragging = False
mouse_start = (0, 0)
bg_start = townbg_rect.center

print("test")

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # if click start the other drag function and fetch starting pos
            dragging = True # 
            mouse_start = pygame.mouse.get_pos()
            bg_start = townbg_rect.center
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1: # stopped click
            dragging = False
        if event.type == pygame.MOUSEMOTION and dragging: # updates as mouse moves
            mouse_x, mouse_y = pygame.mouse.get_pos() # constantly fetch mouse position into 2 vars
            dx = mouse_x - mouse_start[0] # offset compared to OG mouse pos
            dy = mouse_y - mouse_start[1] # ^
            townbg_rect.center = (bg_start[0] + dx, bg_start[1] + dy) # add the offsets to the starting position of the background

    screen.fill((0, 0, 0))
    screen.blit(town_bg, townbg_rect)
    pygame.display.flip()