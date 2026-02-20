import pygame
import sys
import json
import random

pygame.init() # initializing
pygame.mixer.init() # intiizialaitiznig mixer

pygame.mixer.music.load("audio/superman.mp3") # 
pygame.mixer.music.play()

# main variables
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
subtown_selected = "none"
map_set_width = 500//8 * 4
map_set_height = 500//8 * 4
map_set_x = None
map_set_y = None
reached_middle = False
inf = 10**9
all_subtowns = ["redmarsh"]
outlined = None
map_text_color = None

#animation sheets
capesway_sheet = pygame.image.load("animations/capesway_sheet.png")

#images
main_menu_bg = pygame.image.load("images/mm_background.png")
left_studio_logo = pygame.image.load("images/lefthalfstudiologo.png")
right_studio_logo = pygame.image.load("images/righthalfstudiologo.png")

#town stuff 
aestheticing = ""
mission_board_bg = pygame.image.load("images/missionboardbg.png")
compass_black = pygame.image.load("images/compass.png")
compass_white = pygame.image.load("images/compass_white.png")

town_bg = pygame.image.load("map_background.png")
townbg_rect = town_bg.get_rect()
townbg_rect.center = (960, 540)
building_menuimage = pygame.image.load("images/buildmenu.png")
building_menu_rect = building_menuimage.get_rect()

original_town_bg = pygame.image.load("map_background.png").convert_alpha()
zoom = 1.0
zoom_speed = 0.1
max_zoom = 2
town_hover = ""
sell_hover = False
moving_hover = False
building_menu = False

hovered = []
moving_building = ""

all_mission_maps = None

#opening a json file with a dictionary that stores button positions (top left corner and top right corner)
with open("maps/map_mission_buttons.json", "r") as f:
    all_mission_maps = json.load(f)

dragging = False
mouse_start = (0, 0)
bg_start = townbg_rect.center

#more town variables
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

build_popup = pygame.image.load("images/build_popup.png") 
build_popup_rect = build_popup.get_rect()
hovered_tobuild = ""

timer = 0
# buildings

#storing button positions for buildlings
buildings = ["house1", "tree1", "house2", "path1", "path2", "path3", "path4", "path5", "tree2", "house3", "fountain1", "path6", "path7", "barracks1", "barracks2"]
buildings_info = {
"house1_type": "house1", "house1_location": [1800,1100],
"house2_type": "house1", "house2_location": [1915,1100],
"tree1_type": "tree1", "tree1_location": [1860, 1107],
"path1_type": "path1", "path1_location": [1790, 1157],
"path2_type": "path1", "path2_location": [1855, 1157],
"path3_type": "path1", "path3_location": [1920, 1157],
"path4_type": "path1", "path4_location": [1985, 1157],
"path5_type": "path1", "path5_location": [2045, 1157],
"tree2_type": "tree1", "tree2_location": [1977, 1107],
"house3_type": "house1", "house3_location": [2040,1100],
"fountain1_type": "fountain1", "fountain1_location": [1917,1200],
"path6_type": "path2", "path6_location": [1860, 1205],
"path7_type": "path2", "path7_location": [1978, 1205],
"barracks1_type": "barracks1", "barracks1_location": [1801, 1195],
"barracks2_type": "barracks1", "barracks2_location": [2040, 1195],
                }

#helper function for clamping numbers (inbetween one and another number SANTIAGO)
def clamp(n, min_val, max_val):
    return max(min_val, min(n, max_val))

#helper function for drawing circle anim when you hover over a map on the mission board (SANTIAGO)
inner_radius_length = 1
outer_radius_length = 1
radius_timer = 0
def draw_circles(map_length, map_width, fps):
    global radius_timer, outer_radius_length, inner_radius_length

    #keeping track of time, all of them are converted to seconds
    radius_timer += clock.get_time()/1000 #typicaly in ms, so /1000 to transfer into seconds
    frame_duration = 1 / fps #depending on the fps will tell you how many seconds before a frame changes

    if radius_timer >= frame_duration:
        radius_timer -= frame_duration
        if inner_radius_length < map_width // 1.5:
            inner_radius_length *= 1.6 #exponential movement (constantly getting increased by 1.6 times)
            inner_radius_length = clamp(inner_radius_length, 0, map_width//1.5) #clamp function ensures that the radius cannot get too large nor too small
        if outer_radius_length < map_width // 2:
            outer_radius_length *= 1.65
            outer_radius_length = clamp(outer_radius_length, 0, map_width//2)
        
    return [outer_radius_length, inner_radius_length]

#function for sending map drawing towards the middle nicely (SANTIAGO, AND SAME EXACT THING AS DRAW CIRCLES SO NO COMMENTS)
map_timer_count = 0
def send_towards_mid(map_name, fps):
    global map_timer_count, map_set_x, map_set_y, map_set_height, map_set_width
    
    map_timer_count += clock.get_time()/1000
    frame_duration = 1 / fps

    if map_timer_count >= frame_duration:
        map_timer_count -= frame_duration
        if map_set_x > 600:
            map_set_x /= 1.04
            map_set_x = clamp(map_set_x, 600, inf)
        if map_set_y > 200:
            map_set_y /= 1.06
            map_set_y = clamp(map_set_y, 130, inf)
        if map_set_height < 700:
            map_set_height *= 1.05
            map_set_height = clamp(map_set_height, 0, 700)
        if map_set_width < 700:
            map_set_width *= 1.05
            map_set_width = clamp(map_set_width, 0, 700)

#reusable animation function (SANTIAGO AND RARES)
current_sheets_being_animated = {} #main dictionary keeps track of all sheets being animated, keeping track of both time and frame

def animate(sheet, fps, frame_width, frame_height, pause):
    if sheet not in current_sheets_being_animated:
        current_sheets_being_animated[sheet] = {"frame" : 0, "timer": 0} # initializing the sheet

    current_sheets_being_animated[sheet]["timer"] += clock.get_time() / 1000
    frame_duration = 1 / fps

    #if the timer passes the frame duration which is the time that it takes before swapping frames, then we switch frames
    if current_sheets_being_animated[sheet]["timer"] >= frame_duration:
        current_sheets_being_animated[sheet]["frame"] += 1
        current_sheets_being_animated[sheet]["timer"] -= frame_duration
    
    #getting how many total frames there are
    frames_per_row = sheet.get_width() // frame_width

    if current_sheets_being_animated[sheet]["frame"] > frames_per_row - 1:
        current_sheets_being_animated[sheet]["frame"] = 1

    #taking slices of frame width where the left of the slice is the frame times the frame width
    return sheet.subsurface(pygame.Rect(current_sheets_being_animated[sheet]["frame"] * frame_width, 0, frame_width, frame_height))

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        screen.fill((0, 0, 0))

        if event.type == pygame.MOUSEBUTTONDOWN:  # main event handler when the player presses a button
            mouse_x, mouse_y = pygame.mouse.get_pos()
            # (SANTIAGO MAIN MENU BRANCH)
            if current_screen == "main_menu":
                if mouse_x > 1200 and mouse_x < 1400 and mouse_y < 600 and mouse_y > 550 and event.button == 1: #(RARES) if the play button clicked then switch screens
                    current_screen = "town"
                    pygame.mixer.music.stop()
                    pygame.mixer.music.load("audio/town_music.mp3") # 
                    pygame.mixer.music.play()

            # (VIVEK SECTION OF CODE FOR THE TOWN)
            if current_screen == "town":
                if event.button == 1:
                    dragging = True # 
                    mouse_start = pygame.mouse.get_pos()
                    bg_start = townbg_rect.center
                if event.button == 1 and aestheticing == "door":
                    current_screen = "mission_board"

                mouse_x, mouse_y = pygame.mouse.get_pos()

                # gets the mouse coordinates relative to the position of the background (offset)
                rel_x = mouse_x - townbg_rect.left
                rel_y = mouse_y - townbg_rect.top

                old_zoom = zoom # used to see how much it has grown or shrunk when doing later math

                if event.button == 1: # left click

                    if moving_building != "":
                        moving_building = ""

                    if aestheticing == "build" and building_menu == False:
                        building_menu = True
                    elif aestheticing == "build" and building_menu == True:
                        building_menu = False

                    for building in buildings: # seeing if what we clicked is ontop of an existing building
                        world_x, world_y = buildings_info[building + "_location"]
                        building_x = townbg_rect.left + world_x * zoom 
                        building_y = townbg_rect.top  + world_y * zoom
                        building_found = False

                        if mouse_x > building_x - (32 * zoom) and mouse_x < building_x + (32 * zoom) and mouse_y  > building_y - (32 * zoom)   and mouse_y < building_y + (32 * zoom):
                            print(building)
                            hovered = []
                            hovered.append(building)
                            
                            building_found = True
                            break
                        
                        if building_found == False: # if a building isn't found then either reset the hovering list or do nothing
                            if sell_hover == True and len(hovered) != 0:
                                buildings.remove(hovered[0])

                            if moving_hover == True and len(hovered) != 0:
                                moving_building = hovered[0]
                                 

                            hovered = [] #reset the hovered list to take away the hover ui

                    if building_menu == True and hovered_tobuild != "":
                        building_id = random.randint(1, 99999999)
                        buildings.append(hovered_tobuild + str(building_id))
                        buildings_info[hovered_tobuild + str(building_id) + "_type"] = hovered_tobuild 
                        buildings_info[hovered_tobuild + str(building_id) + "_location"] = [0,0]
                        moving_building = hovered_tobuild + str(building_id) 

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

            # (SANTIAGO section of code for the mission board)
            if current_screen == "mission_board":
                if subtown_selected == "none":
                    for name in all_mission_maps:
                        button = all_mission_maps[name]
                        if mouse_x > button[0][0] * 4 and mouse_x < button[1][0] * 4 and mouse_y > button[0][1] * 4 and mouse_y < button[1][1] * 4:
                            subtown_selected = name
                            map_set_x = button[0][0] * 4
                            map_set_y = button[0][1] * 4

        if event.type == pygame.MOUSEBUTTONUP: # stopped click
            mouse_x, mouse_y = pygame.mouse.get_pos()
            if current_screen == "town":
                if event.button == 1:
                    dragging = False
            
        if event.type == pygame.MOUSEMOTION: # updates as mouse moves
            mouse_x, mouse_y = pygame.mouse.get_pos()
            #(SANTIAGO) section of code for the main menu button hovering
            if current_screen == "main_menu":
                if mouse_x > 1200 and mouse_x < 1400 and mouse_y < 600 and mouse_y > 550:
                    play_text_btn_color = (255,255,255)
                else:
                    play_text_btn_color = (89, 0, 0)

            #(SANTIAGO) section of code for mission board
            if current_screen == "mission_board": #mission board branch
                for name in all_mission_maps:
                    button = all_mission_maps[name]
                    if mouse_x > button[0][0] * 4 and mouse_x < button[1][0] * 4 and mouse_y > button[0][1] * 4 and mouse_y < button[1][1] * 4: #each one is multiplied by 4 because it was drawn on a resolution that was 1920 / 4 by 1080/4
                        outlined = name
                    else:
                        if outlined == name:
                            outlined = None
                            map_text_color = (255,255,255)
                            inner_radius_length = 1
                            outer_radius_length = 1

            #(VIVEK) section of code for the town 
            if current_screen == "town":
                mouse_x, mouse_y = pygame.mouse.get_pos() # constantly fetch mouse position into 2 vars
                if dragging:
                     
                    dx = mouse_x - mouse_start[0] # offset compared to OG mouse pos
                    dy = mouse_y - mouse_start[1] # ^
                    townbg_rect.center = (bg_start[0] + dx, bg_start[1] + dy) # add the offsets to the starting position of the background

                
                if moving_building != "":
                    world_x = (mouse_x - townbg_rect.left) / zoom
                    world_y = (mouse_y - townbg_rect.top) / zoom
                    buildings_info[moving_building + "_location"] = [world_x, world_y]


                #print(mouse_x, mouse_y)
                #town ui aesthetics:
                if mouse_x > 337 and mouse_x < 400 and mouse_y < 1070 and mouse_y > 1013:
                    sell_hover = True
                else:
                    sell_hover = False

                if mouse_x > 337 and mouse_x < 400 and mouse_y < 997 and mouse_y > 937:
                    moving_hover = True
                else:
                    moving_hover = False

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
                 
                # build menu stuff
                #88
                if mouse_x > 1273 and mouse_x < 1341 and mouse_y < 619 and mouse_y > 551 and building_menu == True:
                    hovered_tobuild = "house1"
                elif mouse_x > 1361 and mouse_x < 1429 and mouse_y < 619 and mouse_y > 551 and building_menu == True:
                    hovered_tobuild = "barracks1"
                elif mouse_x > 1449 and mouse_x < 1517 and mouse_y < 619 and mouse_y > 551 and building_menu == True:
                    hovered_tobuild = "fountain1"
                elif mouse_x > 1537 and mouse_x < 1605 and mouse_y < 619 and mouse_y > 551 and building_menu == True:
                    hovered_tobuild = "tree1"
                elif mouse_x > 1625 and mouse_x < 1693 and mouse_y < 619 and mouse_y > 551 and building_menu == True:
                    hovered_tobuild = "path1"
                elif mouse_x > 1713 and mouse_x < 1781 and mouse_y < 619 and mouse_y > 551 and building_menu == True:
                    hovered_tobuild = "path2"
                else:
                    hovered_tobuild = ""

    screen.fill((0, 0, 0))
    #drawing town (VIVEK)
    if current_screen == "town":
        screen.blit(town_bg, townbg_rect)
        
        # drawing the actual town itself
            
        for building in buildings:
            building_blit = pygame.image.load("images/" + buildings_info[building + "_type"] + ".png").convert_alpha()
            building_scaled = pygame.transform.scale(building_blit, (int(building_blit.get_width() * zoom),int(building_blit.get_height() * zoom)))
            building_blit_rect = building_scaled.get_rect()

            world_x, world_y = buildings_info[building + "_location"]

            
            building_blit_rect.center = (townbg_rect.left + world_x * zoom, townbg_rect.top  + world_y * zoom) # simply scaling with zoom then adding the offset from the townbgs left and top
             


            square_surf = pygame.Surface((building_blit_rect.width, building_blit_rect.height)) # hover square ]
            square_surf.set_alpha(50) # transperency
            square_surf.fill((0, 0, 0)) # ]

            if building in hovered: # if it is being hovered then draw the square
                screen.blit(square_surf, building_blit_rect) 

                # building popup
                screen.blit(build_popup, build_popup_rect)
                popup_building = pygame.image.load("images/" + buildings_info[building + "_type"] + ".png").convert_alpha()
                popup_scaled = pygame.transform.scale(popup_building, (int(popup_building.get_width() * 2), int(popup_building.get_height() * 2)))
                popup_rect = popup_scaled.get_rect()
                popup_rect.center = (163, 800)
                screen.blit(popup_scaled, popup_rect)

                smaller_pixel_font = pygame.font.Font('all_fonts/VCR_OSD_MONO_1.001.ttf', 50)
                screen.blit(smaller_pixel_font.render(building, True, play_text_btn_color), (60, 615))

            screen.blit(building_scaled, building_blit_rect)

         
        # build menu

        if building_menu == True:
            screen.blit(building_menuimage, building_menu_rect)
        # hovered squares:
        if hovered_tobuild == "house1":
            square_surf = pygame.Surface((70,70)) # hover square ]
            square_surf.set_alpha(50) # transperency
            square_surf.fill((255,255,255)) # ]
            screen.blit(square_surf, (1273, 551))
        if hovered_tobuild == "barracks1":
            square_surf = pygame.Surface((70,70)) # hover square ]
            square_surf.set_alpha(50) # transperency
            square_surf.fill((255,255,255)) # ]
            screen.blit(square_surf, (1363, 551))
        if hovered_tobuild == "fountain1":
            square_surf = pygame.Surface((70,70)) # hover square ]
            square_surf.set_alpha(50) # transperency
            square_surf.fill((255,255,255)) # ]
            screen.blit(square_surf, (1451, 551))
        if hovered_tobuild == "tree1":
            square_surf = pygame.Surface((70,70)) # hover square ]
            square_surf.set_alpha(50) # transperency
            square_surf.fill((255,255,255)) # ]
            screen.blit(square_surf, (1539, 551))
        if hovered_tobuild == "path1":
            square_surf = pygame.Surface((70,70)) # hover square ]
            square_surf.set_alpha(50) # transperency
            square_surf.fill((255,255,255)) # ]
            screen.blit(square_surf, (1627, 551))
        if hovered_tobuild == "path2":
            square_surf = pygame.Surface((70,70)) # hover square ]
            square_surf.set_alpha(50) # transperency
            square_surf.fill((255,255,255)) # ]
            screen.blit(square_surf, (1715, 551))

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
     
             
    #drawing main menu (SANTIAGO)
    if current_screen == "main_menu":
        screen.blit(pygame.transform.scale(main_menu_bg, (1920, 1080)), (0,0))
        screen.blit(pygame.transform.scale(animate(capesway_sheet, 3, 480, 270, False), (1920, 1080)), (0,0)) #animate function worked on by santi and rares
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

    #drawing the mission board (SANTIAGO)
    if current_screen == "mission_board":
        screen.blit(pygame.transform.scale(mission_board_bg, (mission_board_bg.get_width()*4, mission_board_bg.get_height()*4)), (0,0))
        screen.blit(pygame.transform.scale(compass_white, (compass_white.get_width()*2, compass_white.get_height()*2)), (100,100))

        if subtown_selected == "none":
            for map in all_subtowns:
                map_img = pygame.image.load("maps/" + map + "_map.png")
                map_img = pygame.transform.scale(map_img, (map_img.get_width()//8 * 4, map_img.get_height()//8 * 4))
                
                map_text_color = (255,255,255)
                screen.blit(pygame.font.Font('all_fonts/VCR_OSD_MONO_1.001.ttf', 30).render(map.upper(), True, (map_text_color)), (all_mission_maps[map][0][0] * 4 - (25 * len(list(map))), all_mission_maps[map][0][1] * 4 + 100))
                screen.blit(map_img, (all_mission_maps[map][0][0] * 4, all_mission_maps[map][0][1] * 4))

                #checking when you are hovering over a map and then drawing the inner and outer circle for a nice animation for hovering 
                if outlined: 
                    map_text_color = (255,78,0)
                    outer_radius_length, inner_radius_length = draw_circles(map, map_img.get_height(), map_img.get_width())
                    pygame.draw.circle(screen, (255,255,255), (all_mission_maps[map][0][0] * 4 + map_img.get_width()//2, all_mission_maps[map][0][1] * 4 + map_img.get_height()//2), inner_radius_length, 5)
                    pygame.draw.circle(screen, (255,255,255), (all_mission_maps[map][0][0] * 4 + map_img.get_width()//2, all_mission_maps[map][0][1] * 4 + map_img.get_height()//2), outer_radius_length, 5)
        else:
            if not reached_middle:
                send_towards_mid(subtown_selected, 180) #constantly moving the map towards the middle of the screen when you click on a map
            
            map_img = pygame.image.load("maps/" + map + "_map.png")
            map_img = pygame.transform.scale(map_img, (map_set_width, map_set_height))
            roads = pygame.image.load("maps/" + map + "_roads.png")
            roads = pygame.transform.scale(roads, (map_set_width, map_set_height))
            cities = pygame.image.load("maps/" + map + "_cities.png")
            cities = pygame.transform.scale(cities, (map_set_width, map_set_height))

        # smaller_pixel_font = pygame.font.Font('all_fonts/VCR_OSD_MONO_1.001.ttf', 50)
        # screen.blit(smaller_pixel_font.render("PLAY", True, play_text_btn_color), (1200, 550))

            screen.blit(map_img, (map_set_x, map_set_y))
            screen.blit(roads, (map_set_x, map_set_y))
            screen.blit(cities, (map_set_x, map_set_y))

    timer+=1
    pygame.display.flip()

    clock.tick(60)