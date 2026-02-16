import pygame
import sys

pygame.init() # initializing
pygame.mixer.init() # intiizialaitiznig mixer

pygame.mixer.music.load("audio/superman.mp3") # 
pygame.mixer.music.play()

clock = pygame.time.Clock()
screen = pygame.display.set_mode((1920, 1080))
main_pixel_font = pygame.font.Font('all_fonts/VCR_OSD_MONO_1.001.ttf', 70)
running = True
current_screen = "main_menu"
opening_cutscene = False
opening_cutscene_playing = False
opening_cutscene_speed = 1.01
start_ticks = pygame.time.get_ticks()
play_text_btn_color = (89,0,0)

#animation sheets
capesway_sheet = pygame.image.load("animations/capesway_sheet.png")

#images
main_menu_bg = pygame.image.load("images/mm_background.png")
left_studio_logo = pygame.image.load("images/lefthalfstudiologo.png")
right_studio_logo = pygame.image.load("images/righthalfstudiologo.png")

#town stuff 

aestheticing = ""

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

town_ui = pygame.image.load("images/town_ui.png")
town_ui_rect = town_ui.get_rect()

town_ui_rup = pygame.image.load("images/townrup.png")
town_ui_rup_rect = town_ui_rup.get_rect()
town_ui_tup = pygame.image.load("images/towntup.png")
town_ui_tup_rect = town_ui_tup.get_rect()
town_ui_mup = pygame.image.load("images/townmup.png")
town_ui_mup_rect = town_ui_mup.get_rect()
town_ui_dup = pygame.image.load("images/towndup.png")
town_ui_dup_rect = town_ui_dup.get_rect()
town_ui_bup = pygame.image.load("images/townbup.png")
town_ui_bup_rect = town_ui_bup.get_rect()

# buildings

buildings = ["house1", "tree1", "house2"]
buildings_info = {
"house1_type": "house1", "house1_location": [1800,1100],
"house2_type": "house1", "house2_location": [1915,1100],
"tree1_type": "tree1", "tree1_location": [1860, 1107]

                }

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

        screen.fill((0, 0, 0))

        if event.type == pygame.MOUSEBUTTONDOWN:  # if click start the other drag function and fetch starting pos
            mouse_x, mouse_y = pygame.mouse.get_pos()
            if current_screen == "main_menu":
                if mouse_x > 1200 and mouse_x < 1400 and mouse_y < 600 and mouse_y > 550:
                    current_screen = "town"

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
                    global_left = new_left
                    global_top = new_top

        if event.type == pygame.MOUSEBUTTONUP: # stopped click
            mouse_x, mouse_y = pygame.mouse.get_pos()
            if current_screen == "town":
                if event.button == 1:
                    dragging = False
            
        if event.type == pygame.MOUSEMOTION: # updates as mouse moves
            mouse_x, mouse_y = pygame.mouse.get_pos()
            if current_screen == "main_menu":
                if mouse_x > 1200 and mouse_x < 1400 and mouse_y < 600 and mouse_y > 550:
                    play_text_btn_color = (255,255,255)
                else:
                    play_text_btn_color = (89, 0, 0)

             

            if current_screen == "town":
                mouse_x, mouse_y = pygame.mouse.get_pos() # constantly fetch mouse position into 2 vars
                if dragging:
                     
                    dx = mouse_x - mouse_start[0] # offset compared to OG mouse pos
                    dy = mouse_y - mouse_start[1] # ^
                    townbg_rect.center = (bg_start[0] + dx, bg_start[1] + dy) # add the offsets to the starting position of the background

                #print(mouse_x, mouse_y)
                #town ui aesthetics:

                if mouse_x > 1269 and mouse_x < 1370 and mouse_y < 1061 and mouse_y > 985:
                    #print("yoooooo")
                    aestheticing = "build"
                elif mouse_x > 1384 and mouse_x < 1485 and mouse_y < 1061 and mouse_y > 985:
                    aestheticing = "tax"
                elif mouse_x > 1499 and mouse_x < 1600 and mouse_y < 1061 and mouse_y > 985:
                    aestheticing = "mail"
                elif mouse_x > 1614 and mouse_x < 1715 and mouse_y < 1061 and mouse_y > 985:
                    aestheticing = "relationships"
                elif mouse_x > 1729 and mouse_x < 1830 and mouse_y < 1061 and mouse_y > 985:
                    aestheticing = "door"
                else:
                    aestheticing = ""
                 
                     

    screen.fill((0, 0, 0))
    #drawing town
    if current_screen == "town":
        screen.blit(town_bg, townbg_rect)

        # aesthethics
        if aestheticing == "":
            screen.blit(town_ui, town_ui_rect)
        if aestheticing == "build":
            screen.blit(town_ui_bup, town_ui_bup_rect)
        if aestheticing == "tax":
            screen.blit(town_ui_tup, town_ui_tup_rect)
        if aestheticing == "mail":
            screen.blit(town_ui_mup, town_ui_mup_rect)
        if aestheticing == "relationships":
            screen.blit(town_ui_rup, town_ui_rup_rect)
        if aestheticing == "door":
            screen.blit(town_ui_dup, town_ui_dup_rect)

        # drawing the actual town itself
            
        for building in buildings:
            building_blit = pygame.image.load("images/" + buildings_info[building + "_type"] + ".png").convert_alpha()
            building_scaled = pygame.transform.scale(building_blit, (int(building_blit.get_width() * zoom),int(building_blit.get_height() * zoom)))
            building_blit_rect = building_scaled.get_rect()

            world_x, world_y = buildings_info[building + "_location"]

            building_blit_rect.center = (townbg_rect.left + world_x * zoom, townbg_rect.top  + world_y * zoom) # simply scaling with zoom then adding the offset from the townbgs left and top

            screen.blit(building_scaled, building_blit_rect)
                
             
    #drawing main menu
    if current_screen == "main_menu":
        screen.blit(pygame.transform.scale(main_menu_bg, (1920, 1080)), (0,0))
        screen.blit(pygame.transform.scale(animate(capesway_sheet, 3, 480, 270, False), (1920, 1080)), (0,0))
        screen.blit(main_pixel_font.render("THRONE ALONE", True, (89,0,0)), (1000, 450))
        smaller_pixel_font = pygame.font.Font('all_fonts/VCR_OSD_MONO_1.001.ttf', 50)
        screen.blit(smaller_pixel_font.render("PLAY", True, play_text_btn_color), (1200, 550))

        if not opening_cutscene:
            if not opening_cutscene_playing:
                pygame.draw.rect(screen, (57, 57, 54), pygame.Rect(0,0, 1920/2, 1080))
                pygame.draw.rect(screen, (57, 57, 54), pygame.Rect(1920/2,0, 1920/2, 1080))
                screen.blit(pygame.transform.scale(left_studio_logo, (left_studio_logo.get_width()//2, left_studio_logo.get_height()//2)), (669, 260))        
                screen.blit(pygame.transform.scale(right_studio_logo, (right_studio_logo.get_width()//2, right_studio_logo.get_height()//2)), (954, 260))

            if (pygame.time.get_ticks() - start_ticks) / 1000 > 5:
                opening_cutscene_playing = True
                pygame.draw.rect(screen, (57, 57, 54), pygame.Rect(0,0, 1920/2 - opening_cutscene_speed, 1080))
                pygame.draw.rect(screen, (57, 57, 54), pygame.Rect(1920/2 + opening_cutscene_speed,0, 1920/2, 1080))
                screen.blit(pygame.transform.scale(left_studio_logo, (left_studio_logo.get_width()//2, left_studio_logo.get_height()//2)), (669 - opening_cutscene_speed, 260))        
                screen.blit(pygame.transform.scale(right_studio_logo, (right_studio_logo.get_width()//2, right_studio_logo.get_height()//2)), (954 + opening_cutscene_speed, 260))                
                opening_cutscene_speed *= 1.5

    pygame.display.flip()

    clock.tick(60)