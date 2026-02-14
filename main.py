import pygame
import sys

pygame.init()

clock = pygame.time.Clock()
screen = pygame.display.set_mode((1920, 1080))
main_pixel_font = pygame.font.Font('all_fonts/VCR_OSD_MONO_1.001.ttf', 70)
running = True
town_view = False
main_menu = True
opening_cutscene = False
opening_cutscene_playing = False
opening_cutscene_speed = 1.01
start_ticks = pygame.time.get_ticks()

#animation sheets
capesway_sheet = pygame.image.load("animations/capesway_sheet.png")

#images
main_menu_bg = pygame.image.load("images/mm_background.png")
left_studio_logo = pygame.image.load("images/lefthalfstudiologo.png")
right_studio_logo = pygame.image.load("images/righthalfstudiologo.png")

town_bg = pygame.image.load("map_test.png")
townbg_rect = town_bg.get_rect()
townbg_rect.center = (960, 540)

dragging = False
mouse_start = (0, 0)
bg_start = townbg_rect.center

#reusable animation function
current_sheets_being_animated = {}

def animate(sheet, fps, frame_width, frame_height, pause):
    if sheet not in current_sheets_being_animated:
        current_sheets_being_animated[sheet] = {"frame" : 0, "timer": 0}

    current_sheets_being_animated[sheet]["timer"] += clock.get_time() / 1000
    frame_duration = 1 / fps

    if current_sheets_being_animated[sheet]["timer"] >= frame_duration:
        current_sheets_being_animated[sheet]["frame"] += 1
        current_sheets_being_animated[sheet]["timer"] -= frame_duration
    
    frames_per_row = sheet.get_width() // frame_width

    if current_sheets_being_animated[sheet]["frame"] > frames_per_row - 1:
        current_sheets_being_animated[sheet]["frame"] = 1

    return sheet.subsurface(pygame.Rect(current_sheets_being_animated[sheet]["frame"] * frame_width, 0, frame_width, frame_height))


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

    #main menu logic
    if main_menu:
        screen.blit(pygame.transform.scale(main_menu_bg, (1920, 1080)), (0,0))
        screen.blit(pygame.transform.scale(animate(capesway_sheet, 3, 480, 270, False), (1920, 1080)), (0,0))
        screen.blit(main_pixel_font.render("THRONE ALONE", True, (89,0,0)), (1000, 450))

        if not opening_cutscene:
            if not opening_cutscene_playing:
                pygame.draw.rect(screen, (90, 90, 90), pygame.Rect(0,0, 1920/2, 1080))
                pygame.draw.rect(screen, (90, 90, 90), pygame.Rect(1920/2,0, 1920/2, 1080))
                screen.blit(pygame.transform.scale(left_studio_logo, (left_studio_logo.get_width()//2, left_studio_logo.get_height()//2)), (665, 260))        
                screen.blit(pygame.transform.scale(right_studio_logo, (right_studio_logo.get_width()//2, right_studio_logo.get_height()//2)), (666, 260))

            if (pygame.time.get_ticks() - start_ticks) / 1000 > 2:
                opening_cutscene_playing = True
                pygame.draw.rect(screen, (90, 90, 90), pygame.Rect(0,0, 1920/2 - opening_cutscene_speed, 1080))
                pygame.draw.rect(screen, (90, 90, 90), pygame.Rect(1920/2 + opening_cutscene_speed,0, 1920/2, 1080))
                screen.blit(pygame.transform.scale(left_studio_logo, (left_studio_logo.get_width()//2, left_studio_logo.get_height()//2)), (665 - opening_cutscene_speed, 260))        
                screen.blit(pygame.transform.scale(right_studio_logo, (right_studio_logo.get_width()//2, right_studio_logo.get_height()//2)), (666 + opening_cutscene_speed, 260))                
                opening_cutscene_speed *= 1.5

    # screen.blit(town_bg, townbg_rect)
    pygame.display.flip()

    clock.tick(60)