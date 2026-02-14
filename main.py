import pygame
import sys

pygame.init()

screen = pygame.display.set_mode((1920, 1080))
running = True
town_view = True

town_bg = pygame.image.load("map_test.png")
townbg_rect = town_bg.get_rect()
townbg_rect.center = (960, 540)

original_town_bg = pygame.image.load("map_test.png").convert_alpha()
zoom = 1.0
zoom_speed = 0.1

dragging = False
mouse_start = (0, 0)
bg_start = townbg_rect.center

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        screen.fill((0, 0, 0))

        if town_view == True:
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
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 4: # scroll up / zoom in
                    zoom += zoom_speed
                if event.button == 5: # scroll down / zoom out
                    zoom -= zoom_speed
                    if zoom < 0.2:  # max zoom out
                        zoom = 0.2

                # (default zoom is 1)
                width = int(original_town_bg.get_width() * zoom) # multiplying the map size according to zoom
                height = int(original_town_bg.get_height() * zoom) # ^

                town_bg = pygame.transform.smoothscale(original_town_bg, (width, height)) # smooth scale is the same thing as .scale but slower and better interpolation
            screen.blit(town_bg, townbg_rect)
         


     
    pygame.display.flip()