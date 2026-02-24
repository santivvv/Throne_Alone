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
# (RARES) role selection elements
KING_BOX = pygame.Rect(0, 0, 420, 520)
QUEEN_BOX = pygame.Rect(0, 0, 420, 520)
CONFIRM_BUTTON = pygame.Rect(0, 0, 420, 110)
KING_BOX.center = (1920 // 2 - 260, 1080 // 2)
QUEEN_BOX.center = (1920 // 2 + 260, 1080 // 2)
CONFIRM_BUTTON.center = (1920 // 2, 1080 - 140)
main_pixel_font = pygame.font.Font('all_fonts/VCR_OSD_MONO_1.001.ttf', 70)
running = True
current_screen = "main_menu"
# role select screen 
chosen_role = None  # final role
role_selected = None  # currently highlighted role

# transition between start screens
transitioning = False
transition_state = None
transition_target = None
transition_alpha = 0  # 0..255
transition_speed = 10  # opacity per frame 
transition_pause_ms = 2000
transition_pause_start = None

# white fade overlay (reused each frame)
transition_overlay = pygame.Surface((1920, 1080))
transition_overlay.fill((255, 255, 255))

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
all_subtowns = ["redmarsh", "daggerfall", "goldcrest", "fenwick", "hallowmere"]
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

town_bg = pygame.image.load("images/map_background.png")
townbg_rect = town_bg.get_rect()
townbg_rect.center = (960, 540)

building_menuimage = pygame.image.load("images/buildmenu.png")
building_menu_rect = building_menuimage.get_rect()

original_town_bg = pygame.image.load("images/map_background.png").convert_alpha()
zoom = 1.0
zoom_speed = 0.1
max_zoom = 2
town_hover = ""
sell_hover = False
moving_hover = False
addoccupant_hover = False
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
build_popup2 = pygame.image.load("images/build_popup2.png")
build_popup2_rect = build_popup2.get_rect()
hovered_tobuild = ""

timer_reversed = False
timer = -300
day = 1

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

citizen_count = 1
citizens = ["citizen1", "citizen2", "citizen3"]
valid_workers = citizens.copy()
citizens_info = {
"citizen1_type": "m_pilgrim1", "citizen1_location": [1900,1200], "citizen1_targetoffset": [0,0], "citizen1_resting": 100,
"citizen2_type": "m_pilgrim2", "citizen2_location": [1950,1250], "citizen2_targetoffset": [0,0], "citizen2_resting": 56,
"citizen3_type": "m_pilgrim3", "citizen3_location": [1900,1150], "citizen3_targetoffset": [0,0], "citizen3_resting": 126,
}
citizen_types = ["m_pilgrim1", "m_pilgrim2", "m_pilgrim3"]
occupied_citizens = {}
population = len(citizens)

#helper function for clamping numbers (inbetween one and another number SANTIAGO)
def clamp(n, min_val, max_val):
    return max(min_val, min(n, max_val))

# (RARES) transition 
def start_transition(target_screen: str):
    global transitioning, transition_state, transition_target, transition_alpha, transition_pause_start
    transitioning = True
    transition_state = "cover"  # fade to white
    transition_target = target_screen
    transition_alpha = 0 # starts transparent
    transition_pause_start = None

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
            if transitioning:
                continue
            # (SANTIAGO MAIN MENU BRANCH)
            if current_screen == "main_menu":
                if mouse_x > 1200 and mouse_x < 1400 and mouse_y < 600 and mouse_y > 550 and event.button == 1: #(RARES) if the play button clicked then switch screens
                    # go to role selection 
                    start_transition("role_select")

            # role select screen
            if current_screen == "role_select":
                if event.button == 1:
                    # select KING/QUEEN
                    if KING_BOX.collidepoint(mouse_x, mouse_y):
                        role_selected = "KING"
                    elif QUEEN_BOX.collidepoint(mouse_x, mouse_y):
                        role_selected = "QUEEN"

                    # confirm
                    if CONFIRM_BUTTON.collidepoint(mouse_x, mouse_y) and role_selected is not None:
                        chosen_role = role_selected
                        # switch music when entering the game
                        pygame.mixer.music.stop()
                        pygame.mixer.music.load("audio/town_music.mp3")
                        pygame.mixer.music.play()
                        start_transition("town")

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
                        if "farmland" in moving_building: # if farmland was the last thing moved / was being moved
                            if moving_building + "_occupants" not in buildings_info:
                                buildings_info[moving_building + "_occupants"] = []
                                buildings_info[moving_building + "_timer"] = 0
                                print("this is what we added to dict: " + moving_building)
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
                        
                        if building_found == False: # if a building isn't found then either reset the hovering list or do nothing / clicking away form building
                            actionmade = False
                            if sell_hover == True and len(hovered) != 0:
                                if "farmland" in hovered[0]: # if a farm is being sold then remove the guys working there from the list
                                    if hovered[0] + "_occupants" in buildings_info and len(buildings_info[hovered[0] + "_occupants"]) != 0:
                                        del occupied_citizens[(buildings_info[hovered[0] + "_occupants"][0])]
                                        valid_workers.append(buildings_info[hovered[0] + "_occupants"][0])
                                        actionmade = True
                                buildings.remove(hovered[0])
                            if addoccupant_hover == True and len(hovered) != 0:
                                 
                                print("this is the building: " + hovered[0])
                                 
                                if len(valid_workers) != 0 and (len(buildings_info[hovered[0] + "_occupants"]) == 0) and actionmade == False: # adding a worker to a building, only if there are valid workers and there isn't already someone working there
                                    chosen_citizen = random.choice(valid_workers)
                                    newoccupant = []
                                    newoccupant.append(chosen_citizen)
                                    buildings_info[hovered[0] + "_occupants"] = newoccupant
                                    occupied_citizens[chosen_citizen] = hovered[0] # add the citizen to the occupied citizens dict with the building they are working at
                                    valid_workers.remove(chosen_citizen)
                                    actionmade = True
                                    citizens_info[chosen_citizen + "_targetoffset"] = [0,0] # reset the citizens offset so they don't walk astray
                                    citizens_info[chosen_citizen + "_location"] = buildings_info[hovered[0] + "_location"].copy() # move the citizen to the building location

                                if len(buildings_info[hovered[0] + "_occupants"]) != 0 and actionmade == False:
                                    actionmade = True
                                    newoccupant = []
                                    del occupied_citizens[(buildings_info[hovered[0] + "_occupants"][0])]
                                    print(citizens_info[buildings_info[hovered[0] + "_occupants"][0] + "_location"])
                                    citizens_info[buildings_info[hovered[0] + "_occupants"][0] + "_location"] = [1900,1200] # move the citizen back to the "unemployed area"
                                    print("This is happening")
                                    valid_workers.append(buildings_info[hovered[0] + "_occupants"][0])
                                    buildings_info[hovered[0] + "_occupants"] = newoccupant

                                     
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

                if mouse_x > 57 and mouse_x < 122 and mouse_y < 1070 and mouse_y > 1013:
                    addoccupant_hover = True
                
                else:
                    addoccupant_hover = False
                    
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
                elif mouse_x > 1801 and mouse_x < 1869 and mouse_y < 619 and mouse_y > 551 and building_menu == True:
                    hovered_tobuild = "farmland1"
                else:
                    hovered_tobuild = ""

    screen.fill((0, 0, 0))
    #drawing town (VIVEK)
    if current_screen == "town":
         
        screen.blit(town_bg, townbg_rect)
            
        hovered_buildings_to_draw = []
        
        for building in buildings:
             
            building_blit = pygame.image.load("images/" + buildings_info[building + "_type"] + ".png").convert_alpha()
            if (building+"_timer") in buildings_info and "farmland" in building:
                if len(buildings_info[building + "_occupants"]) != 0: # if there are people working there then increase the timer, and after a certain amount of time change the image to the next stage of the farm
                    buildings_info[building + "_timer"] += 1

                if buildings_info[building + "_timer"] >= 500: # if the timer reaches 500 then reset it and give the player some crops (not implemented yet, just a ye
                    print("yield crops")
                    buildings_info[building + "_timer"] = 0
                elif buildings_info[building + "_timer"] >= 400:
                    building_blit = pygame.image.load("images/farmland5.png").convert_alpha() 
                elif buildings_info[building + "_timer"] >= 300:
                    building_blit = pygame.image.load("images/farmland4.png").convert_alpha() 
                elif buildings_info[building + "_timer"] >= 200:
                    building_blit = pygame.image.load("images/farmland3.png").convert_alpha()
                elif buildings_info[building + "_timer"] >= 100:
                    building_blit = pygame.image.load("images/farmland2.png").convert_alpha()
                else:
                    building_blit = pygame.image.load("images/farmland1.png").convert_alpha()

            building_scaled = pygame.transform.scale(building_blit, (int(building_blit.get_width() * zoom),int(building_blit.get_height() * zoom)))
            building_blit_rect = building_scaled.get_rect()

            world_x, world_y = buildings_info[building + "_location"]

            
            building_blit_rect.center = (townbg_rect.left + world_x * zoom, townbg_rect.top  + world_y * zoom) # simply scaling with zoom then adding the offset from the townbgs left and top

            screen.blit(building_scaled, building_blit_rect)

            square_surf = pygame.Surface((building_blit_rect.width, building_blit_rect.height)) # hover square ]
            square_surf.set_alpha(50) # transperency
            square_surf.fill((0, 0, 0)) # ]

            if building in hovered: # if it is being hovered then draw the square
                hovered_buildings_to_draw.append((building, building_blit_rect.copy()))
             
        # drawing citizens and their movement(s)

        for citizen in citizens:
            citizen_blit = pygame.image.load("images/" + citizens_info[citizen + "_type"] + ".png").convert_alpha()
            citizen_scaled = pygame.transform.scale(citizen_blit, (int(citizen_blit.get_width() * zoom * 2),int(citizen_blit.get_height()*zoom * 2)))
            citizen_blit_rect = citizen_scaled.get_rect()
            
            if citizens_info[citizen + "_resting"] != 0 and citizens_info[citizen + "_targetoffset"] == [0,0]:
                citizens_info[citizen + "_resting"] = citizens_info[citizen + "_resting"] - 1
                #print(citizens_info[citizen + "_resting"])
            if citizens_info[citizen + "_resting"] == 0 and citizens_info[citizen + "_targetoffset"] == [0,0]:
                if citizen not in occupied_citizens:
                    citizens_info[citizen + "_targetoffset"] = [random.randint(-100, 100), random.randint(-100, 100)]
                else:
                    citizens_info[citizen + "_targetoffset"] = [random.randint(-10, 10), random.randint(-10, 10)]
                if citizen in occupied_citizens:
                    move_back = random.randint(1,3)
                    if move_back == 3: # making them walk back to farm either randomly or if they get too far
                        citizens_info[citizen + "_targetoffset"] = [buildings_info[occupied_citizens[citizen] + "_location"][0] - citizens_info[citizen + "_location"][0], buildings_info[occupied_citizens[citizen] + "_location"][1] - citizens_info[citizen + "_location"][1]]
                    print(buildings_info[occupied_citizens[citizen] + "_location"][0] - citizens_info[citizen + "_location"][0])
                    if buildings_info[occupied_citizens[citizen] + "_location"][0] - citizens_info[citizen + "_location"][0] > 40 or buildings_info[occupied_citizens[citizen] + "_location"][0] - citizens_info[citizen + "_location"][0] < -40:
                        citizens_info[citizen + "_targetoffset"] = [buildings_info[occupied_citizens[citizen] + "_location"][0] - citizens_info[citizen + "_location"][0], buildings_info[occupied_citizens[citizen] + "_location"][1] - citizens_info[citizen + "_location"][1]]
                citizens_info[citizen + "_resting"] = 200
            if citizens_info[citizen + "_targetoffset"] != [0,0]:
                offset_x, offset_y = citizens_info[citizen + "_targetoffset"]

                if offset_x > 0:
                    citizens_info[citizen + "_location"][0] += 1
                    citizens_info[citizen + "_targetoffset"][0] -= 1
                if offset_y > 0:
                    citizens_info[citizen + "_location"][1] += 1
                    citizens_info[citizen + "_targetoffset"][1] -=1

                if offset_x < 0:
                    citizens_info[citizen + "_location"][0] -= 1
                    citizens_info[citizen + "_targetoffset"][0] += 1
                if offset_y < 0:
                    citizens_info[citizen + "_location"][1] -= 1
                    citizens_info[citizen + "_targetoffset"][1] +=1
                #print(citizens_info[citizen + "_targetoffset"])

            world_x, world_y = citizens_info[citizen + "_location"]
            citizen_blit_rect.center = (townbg_rect.left + world_x * zoom, townbg_rect.top  + world_y * zoom) # simply scaling with zoom then adding the offset from the townbgs left and top         
            screen.blit(citizen_scaled, citizen_blit_rect)

        #print(occupied_citizens)
        night_overlay = pygame.Surface((screen.get_width(), screen.get_height()))
        night_overlay.fill((0, 0, 0))
        #print(timer)
        
        if timer < 1700:
            night_overlay.set_alpha(timer / 10)
        else:
            night_overlay.set_alpha(1700 / 10)
        
        if timer >= 2000:
            timer_reversed = True
        if timer == -300 and timer_reversed == True: # new day!
            print("New day")
            day +=1
            timer_reversed = False

            birth_count = int(population / 3)

            for person in range(birth_count):
                 
                citizens.append("citizen" + str(population + 1))
                valid_workers.append("citizen" + str(population + 1))
                population = len(citizens)
                citizens_info["citizen" + str(population) + "_location"] = [random.randint(1900, 2000), random.randint(1100,1300)]
                citizens_info["citizen" + str(population) + "_targetoffset"] = [0,0]
                citizens_info["citizen" + str(population) + "_resting"] = random.randint(1, 200)
                citizens_info["citizen" + str(population) + "_type"] = random.choice(citizen_types)

        screen.blit(night_overlay, (0, 0))

        for building, building_rect in hovered_buildings_to_draw:
    
            square_surf = pygame.Surface((building_rect.width, building_rect.height))
            square_surf.set_alpha(50)
            square_surf.fill((0, 0, 0))
            screen.blit(square_surf, building_rect)
            SMALLER_pixel_font = pygame.font.Font('all_fonts/VCR_OSD_MONO_1.001.ttf', 35)

            if "farmland" not in building:
                screen.blit(build_popup, build_popup_rect)
            else:
                screen.blit(build_popup2, build_popup2_rect)
                len(buildings_info[building + "_occupants"])
                if len(buildings_info[building + "_occupants"]) == 0:
                    screen.blit(SMALLER_pixel_font.render("+", True, (255,255,255)), (81, 1029))
                else:
                    worker_popup = pygame.image.load("images/" + citizens_info[buildings_info[building + "_occupants"][0] + "_type"] + ".png").convert_alpha()
                    worker_popup_scaled = pygame.transform.scale(worker_popup, (int(worker_popup.get_width() * 3), int(worker_popup.get_height() * 3)))
                    worker_popup_rect = worker_popup_scaled.get_rect()
                    worker_popup_rect.center = (93,1041)
                    screen.blit(worker_popup_scaled, worker_popup_rect)

            popup_building = pygame.image.load("images/" + buildings_info[building + "_type"] + ".png").convert_alpha()
            popup_scaled = pygame.transform.scale(popup_building, (int(popup_building.get_width() * 2),int(popup_building.get_height() * 2)))

            popup_rect = popup_scaled.get_rect()
            popup_rect.center = (163, 800)
            screen.blit(popup_scaled, popup_rect)

            smaller_pixel_font = pygame.font.Font('all_fonts/VCR_OSD_MONO_1.001.ttf', 50)
             

            building_name = list(building)
            alphabet = list("abcdefghijklmnopqrstuvwxyz")

            for a in range(len(building_name)):
                if building_name[a] not in alphabet:
                    building_name = building_name[:a]
                    break

            building_name[0] = building_name[0].upper()
            display_name = "".join(building_name)

            screen.blit(smaller_pixel_font.render(display_name, True, (255,255,255)), (60, 615))
            
        # build menu (88)

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
        if hovered_tobuild == "farmland1":
            square_surf = pygame.Surface((70,70)) # hover square ]
            square_surf.set_alpha(50) # transperency
            square_surf.fill((255,255,255)) # ]
            screen.blit(square_surf, (1803, 551))

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
     
        screen.blit(smaller_pixel_font.render("Day " + str(day), True, (255,255,255)), (880, 50))

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

    # (RARES) drawing role select
    if current_screen == "role_select":
        screen.blit(pygame.transform.scale(main_menu_bg, (1920, 1080)), (0,0))

        title_font = pygame.font.Font('all_fonts/VCR_OSD_MONO_1.001.ttf', 60)
        label_font = pygame.font.Font('all_fonts/VCR_OSD_MONO_1.001.ttf', 40)

        title_surf = title_font.render("SELECT YOUR ROLE", True, (255, 255, 255))
        title_rect = title_surf.get_rect(midtop=(1920 // 2, 30))
        screen.blit(title_surf, title_rect)

        # PUT PORTRAITS HERE
        pygame.draw.rect(screen, (0, 0, 0), KING_BOX)
        pygame.draw.rect(screen, (0, 0, 0), QUEEN_BOX)

        # box outlines
        pygame.draw.rect(screen, (255, 255, 255), KING_BOX, 4)
        pygame.draw.rect(screen, (255, 255, 255), QUEEN_BOX, 4)

        # highlight selected
        if role_selected == "KING":
            pygame.draw.rect(screen, (255, 255, 255), KING_BOX, 10)
        if role_selected == "QUEEN":
            pygame.draw.rect(screen, (255, 255, 255), QUEEN_BOX, 10)

        screen.blit(label_font.render("KING", True, (255, 255, 255)), (KING_BOX.centerx - 60, KING_BOX.bottom + 20))
        screen.blit(label_font.render("QUEEN", True, (255, 255, 255)), (QUEEN_BOX.centerx - 60, QUEEN_BOX.bottom + 20))

        # confirm button
        pygame.draw.rect(screen, (0, 0, 0), CONFIRM_BUTTON)
        pygame.draw.rect(screen, (255, 255, 255), CONFIRM_BUTTON, 4)
        confirm_text = label_font.render("CONFIRM", True, (255, 255, 255))
        screen.blit(confirm_text, (CONFIRM_BUTTON.centerx - confirm_text.get_width() // 2,
                                  CONFIRM_BUTTON.centery - confirm_text.get_height() // 2))

    #drawing the mission board (SANTIAGO)
    if current_screen == "mission_board":
        screen.blit(pygame.transform.scale(mission_board_bg, (mission_board_bg.get_width()*4, mission_board_bg.get_height()*4)), (0,0))
        screen.blit(pygame.transform.scale(compass_white, (compass_white.get_width()*2, compass_white.get_height()*2)), (100,100))

        if subtown_selected == "none":
            for map in all_subtowns:
                map_img = pygame.image.load("maps/" + map + "_map.png")
                map_img = pygame.transform.scale(map_img, (map_img.get_width()//8 * 4, map_img.get_height()//8 * 4))
                
                map_text_color = (255,255,255)
                if all_mission_maps[map][0][0] > 100:
                    screen.blit(pygame.font.Font('all_fonts/VCR_OSD_MONO_1.001.ttf', 30).render(map.upper(), True, (map_text_color)), (all_mission_maps[map][0][0] * 4 - (25 * len(list(map))), all_mission_maps[map][0][1] * 4 + 100))
                else:
                    screen.blit(pygame.font.Font('all_fonts/VCR_OSD_MONO_1.001.ttf', 30).render(map.upper(), True, (map_text_color)), (all_mission_maps[map][0][0] * 4 + (25 * len(list(map))) + 20, all_mission_maps[map][0][1] * 4 + 100))
                screen.blit(map_img, (all_mission_maps[map][0][0] * 4, all_mission_maps[map][0][1] * 4))

                #checking when you are hovering over a map and then drawing the inner and outer circle for a nice animation for hovering 
                if map == outlined: 
                    map_text_color = (255,78,0)
                    outer_radius_length, inner_radius_length = draw_circles(map, map_img.get_height(), map_img.get_width())
                    pygame.draw.circle(screen, (255,255,255), (all_mission_maps[map][0][0] * 4 + map_img.get_width()//2, all_mission_maps[map][0][1] * 4 + map_img.get_height()//2), inner_radius_length, 5)
                    pygame.draw.circle(screen, (255,255,255), (all_mission_maps[map][0][0] * 4 + map_img.get_width()//2, all_mission_maps[map][0][1] * 4 + map_img.get_height()//2), outer_radius_length, 5)
        else:
            if not reached_middle:
                send_towards_mid(subtown_selected, 180) #constantly moving the map towards the middle of the screen when you click on a map
            
            map_img = pygame.image.load("maps/" + subtown_selected + "_map.png")
            map_img = pygame.transform.scale(map_img, (map_set_width, map_set_height))
            roads = pygame.image.load("maps/" + subtown_selected + "_roads.png")
            roads = pygame.transform.scale(roads, (map_set_width, map_set_height))
            cities = pygame.image.load("maps/" + subtown_selected + "_cities.png")
            cities = pygame.transform.scale(cities, (map_set_width, map_set_height))

        # smaller_pixel_font = pygame.font.Font('all_fonts/VCR_OSD_MONO_1.001.ttf', 50)
        # screen.blit(smaller_pixel_font.render("PLAY", True, play_text_btn_color), (1200, 550))

            screen.blit(map_img, (map_set_x, map_set_y))
            screen.blit(roads, (map_set_x, map_set_y))
            screen.blit(cities, (map_set_x, map_set_y))

    # (RARES) transition (fade to white, then fade back)
    if transitioning:
        if transition_state == "cover":
            transition_alpha += transition_speed
            if transition_alpha >= 255:
                transition_alpha = 255

                # waiting a second before un-fading
                if transition_pause_start is None:
                    transition_pause_start = pygame.time.get_ticks()

                if pygame.time.get_ticks() - transition_pause_start >= transition_pause_ms:
                    current_screen = transition_target
                    transition_state = "reveal"
                    transition_pause_start = None

        elif transition_state == "reveal":
            transition_alpha -= transition_speed // 1.5 # un-fading is slightly slower than fading for dramatic effect
            if transition_alpha <= 0:
                transition_alpha = 0
                transitioning = False
                transition_state = None
                transition_target = None

        transition_overlay.set_alpha(transition_alpha)
        screen.blit(transition_overlay, (0, 0))

    if current_screen == "town":
        if timer_reversed == False:
            timer+=1
        else:
            timer-=1

    pygame.display.flip()

    clock.tick(60)