import pygame
import sys

pygame.init()

clock = pygame.time.Clock()
screen = pygame.display.set_mode((1920, 1080))
main_pixel_font = pygame.font.Font('all_fonts/VCR_OSD_MONO_1.001.ttf', 70)
running = True
town_view = False

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

    clock.tick(60)