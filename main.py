import pygame
import sys

pygame.init()

screen = pygame.display.set_mode((1920, 1080))
running = True
current_screen = "town"

town_bg = pygame.image.load("map_background.png")
townbg_rect = town_bg.get_rect()
townbg_rect.center = (960, 540)

original_town_bg = pygame.image.load("map_background.png").convert_alpha()
zoom = 1.0
zoom_speed = 0.1
max_zoom = 2

dragging = False
mouse_start = (0, 0)
bg_start = townbg_rect.center

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        screen.fill((0, 0, 0))

        if event.type == pygame.MOUSEBUTTONDOWN:  # if click start the other drag function and fetch starting pos
            if current_screen == "town":
                if event.button == 1:
                    dragging = True # 
                    mouse_start = pygame.mouse.get_pos()
                    bg_start = townbg_rect.center

                mouse_x, mouse_y = pygame.mouse.get_pos()

                # gets the mouse coordinates relative to the position of the background (offset)
                rel_x = mouse_x - townbg_rect.left
                rel_y = mouse_y - townbg_rect.top

                old_zoom = zoom # used to see how much it has grown or shrunk when doing later math

                if event.button == 4: # scroll up / zoom in
                    if zoom <= max_zoom:
                        zoom += zoom_speed
                        print(zoom)
                if event.button == 5: # scroll down / zoom out
                    zoom -= zoom_speed
                    if zoom < 0.2:  # max zoom out
                        zoom = 0.2

                if zoom <= max_zoom:
                    # (default zoom is 1)
                    width = int(original_town_bg.get_width() * zoom) # multiplying the map size according to zoom
                    height = int(original_town_bg.get_height() * zoom) # ^

                    town_bg = pygame.transform.smoothscale(original_town_bg, (width, height)) # smooth scale is the same thing as .scale but slower and better interpolation
                    scale_factor = zoom / old_zoom # how much the background has grown or shrunk, seeing new zoom amount vs the one before

                    new_left = mouse_x - rel_x * scale_factor # ] getting the new distance, you have to subtract rel_x(scale_factor) so the map is at the same point in relative to cursor
                    new_top = mouse_y - rel_y * scale_factor #  | ^
                    townbg_rect = town_bg.get_rect()#           | get it's rect info 
                    townbg_rect.topleft = (new_left, new_top)#  ] set it's new position with the new info
        if event.type == pygame.MOUSEBUTTONUP: # stopped click
            if current_screen == "town":
                if event.button == 1:
                    dragging = False
        if event.type == pygame.MOUSEMOTION: # updates as mouse moves
            if current_screen == "town":
                if dragging:
                    mouse_x, mouse_y = pygame.mouse.get_pos() # constantly fetch mouse position into 2 vars
                    dx = mouse_x - mouse_start[0] # offset compared to OG mouse pos
                    dy = mouse_y - mouse_start[1] # ^
                    townbg_rect.center = (bg_start[0] + dx, bg_start[1] + dy) # add the offsets to the starting position of the background

        if current_screen == "town":
            screen.blit(town_bg, townbg_rect)
        
    pygame.display.flip()