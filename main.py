import pygame
import sys
import json
import random
import math

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
war_prompt = False
owned_towns = []
# role select screen 
chosen_role = None  # final role
role_selected = None  # currently highlighted role
original_map_set_y = None
deciding_random_event = False
city_happiness = 80
choice1_rect = pygame.Rect(0, 0, 0, 0)
choice2_rect = pygame.Rect(0, 0, 0, 0)

# transition between start screens
transitioning = False
transition_state = None
transition_target = None
transition_alpha = 0  # 0..255
transition_speed = 10  # opacity per frame 
transition_pause_ms = 2000
transition_pause_start = None
already_ran = False
# white fade overlay (reused each frame)
transition_overlay = pygame.Surface((1920, 1080))
transition_overlay.fill((255, 255, 255))

tax_menu_open = False
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
inner_town_selected = None
town_information_store = {}
troop_cnt = 5   

#animation sheets
capesway_sheet = pygame.image.load("animations/capesway_sheet.png")

#images
main_menu_bg = pygame.image.load("images/mm_background.png")
left_studio_logo = pygame.image.load("images/lefthalfstudiologo.png")
right_studio_logo = pygame.image.load("images/righthalfstudiologo.png")
fancy_back_arrow = pygame.image.load("images/nice_looking_arrow.png")
control_room = pygame.image.load("images/control_room.png")
troop_allocation = pygame.image.load("images/troop_allocation.png")
quick_actions = pygame.image.load("images/quick_actions.png")
tax_control = pygame.image.load("images/tax_control.png")
daily_event = pygame.image.load("images/daily_event.png")
king_standing = pygame.image.load("images/king_standing.png")
queen_standing = pygame.image.load("images/queen_standing.png")
king_portrait = pygame.image.load("images/king_portrait.png")
queen_portrait = pygame.image.load("images/queen_portrait.png")

# execution screen variables
falling_man_y = -200
falling_speed = 5
ground_y = 1080 - 480
execution_timer = 0
blood_counter = 1
prompt_for_war_img = pygame.image.load("images/war_prompt.png")

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
original_map_set_x = None
towns_in_war_with = []
hovered = []
moving_building = ""

barracks_popup = pygame.image.load("images/barracks_popup.png")
barracks_popup_rect = barracks_popup.get_rect()
barracks_open = False
build_popup3 = pygame.image.load("images/build_popup3.png")
build_popup3_rect = build_popup3.get_rect()
train_troopshover = False

all_mission_maps = None
town_to_buttons = {}
random_event_chosen = None

#button locations
tax_buttons = {
    5: [[29, 81], [126, 126]],
    15: [[136, 81], [233, 126]],
    25: [[242, 81], [339, 126]],
    40: [[348, 81], [445, 126]],
}

#button locations for buttons inside the quick action menu
quick_action_buttons = {
    "allocate_troops" : [[37, 63], [213, 92]], #top left and right corner
    "withdraw_troops" : [[37, 109], [214, 139]],
    "tax_control" : [[37, 157], [214, 187]],
    "end_war" : [[37, 202], [214, 232]]
}

random_event_list = [{"title" : ""}]
default_inner_town_values = {
    "daggerfall": {"shadowmere" : {"base_income" : 500, "troops_allocated" : 40, "significance_level" : "high"}, 
                   "oakheart" : {"base_income" : 300, "troops_allocated" : 35, "significance_level" : "low"},
                   "silverkeep" : {"base_income" : 350, "troops_allocated" : 40, "significance_level" : "medium"},
                   "oakenshire" : {"base_income" : 300, "troops_allocated" : 35, "significance_level" : "low"},
                   "wolfden" : {"base_income" : 250, "troops_allocated" : 30, "significance_level" : "medium"},
                   "northpass" : {"base_income" : 200, "troops_allocated" : 30, "significance_level" : "low"}},
    "redmarsh" : {"pavlov" : {"base_income" : 50, "troops_allocated" : 30, "significance_level" : "low"}, 
                   "highcrest" : {"base_income" : 250, "troops_allocated" : 30, "significance_level" : "medium"},
                   "kingsfall" : {"base_income" : 200, "troops_allocated" : 20, "significance_level" : "medium"},
                   "stofler" : {"base_income" : 150, "troops_allocated" : 15, "significance_level" : "high"},
                   "grimholt" : {"base_income" : 100, "troops_allocated" : 10, "significance_level" : "low"},
                   "copernicus" : {"base_income" : 50, "troops_allocated" : 5, "significance_level" : "low"}},
    "fenwick" : {"whitebridge" : {"base_income" : 500, "troops_allocated" : 30, "significance_level" : "medium"}, 
                   "eastreach" : {"base_income" : 500, "troops_allocated" : 30, "significance_level" : "low"},
                   "redmere" : {"base_income" : 550, "troops_allocated" : 35, "significance_level" : "low"},
                   "ebonridge" : {"base_income" : 600, "troops_allocated" : 35, "significance_level" : "low"},
                   "stonehaven" : {"base_income" : 650, "troops_allocated" : 40, "significance_level" : "high"},
                   "riverhold" : {"base_income" : 525, "troops_allocated" : 32, "significance_level" : "low"}},
    "hallowmere" : {"mirefall" : {"base_income" : 600, "troops_allocated" : 30, "significance_level" : "low"}, 
                   "murkfen" : {"base_income" : 700, "troops_allocated" : 40, "significance_level" : "low"},
                   "fenreach" : {"base_income" : 750, "troops_allocated" : 50, "significance_level" : "medium"},
                   "marshhaven" : {"base_income" : 800, "troops_allocated" : 50, "significance_level" : "low"},
                   "dreadmire" : {"base_income" : 750, "troops_allocated" : 40, "significance_level" : "low"},
                   "reedhaven" : {"base_income" : 650, "troops_allocated" : 20, "significance_level" : "low"}},
    "goldcrest" : {"stonebridge" : {"base_income" : 700, "troops_allocated" : 30, "significance_level" : "low"}, 
                   "caerwyn" : {"base_income" : 800, "troops_allocated" : 50, "significance_level" : "low"},
                   "fairhaven" : {"base_income" : 850, "troops_allocated" : 60, "significance_level" : "medium"},
                   "silverbrook" : {"base_income" : 900, "troops_allocated" : 70, "significance_level" : "low"},
                   "sunhaven" : {"base_income" : 1000, "troops_allocated" : 100, "significance_level" : "high"},
                   "southwatch" : {"base_income" : 950, "troops_allocated" : 80, "significance_level" : "low"}}
}

#opening a json file with a dictionary that stores button positions (top left corner and top right corner)
with open("maps/map_mission_buttons.json", "r") as f:
    all_mission_maps = json.load(f)

for value in all_mission_maps:
    with open("maps/" + value + "_buttons.json", "r") as f:
        town_to_buttons[value] = json.load(f)

all_random_events = None
#json file for all of the random events
with open("random_event_possibilities.json") as f:
    all_random_events = json.load(f)


#creating storage of information for each individual inner town
for subtown in all_subtowns:
    town_information_store[subtown] = {}

    over_arching_subtown = town_information_store[subtown]

    for inner_town in town_to_buttons[subtown]:
        over_arching_subtown[inner_town] = {}
        over_arching_inner_town = over_arching_subtown[inner_town]

        over_arching_inner_town["troops_allocated"] = 0
        over_arching_inner_town["tax_level"] = 0
        over_arching_inner_town["base_income"] = default_inner_town_values[subtown][inner_town]["base_income"]
        over_arching_inner_town["citizens_gained"] = 0
        over_arching_inner_town["progress_to_next_citizen"] = 0
        over_arching_inner_town["happiness"] = random.randint(40, 100)
        over_arching_inner_town["significance_level"] = default_inner_town_values[subtown][inner_town]["significance_level"]
        over_arching_inner_town["activity_level"] = "NOT OWNED"
        over_arching_inner_town["stationed_troops"] = default_inner_town_values[subtown][inner_town]["troops_allocated"]

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

moneyandfoodicons = pygame.image.load("images/moneyandfoodicons.png")
moneyandfoodicons_rect = moneyandfoodicons.get_rect()

build_popup = pygame.image.load("images/build_popup.png") 
build_popup_rect = build_popup.get_rect()
build_popup2 = pygame.image.load("images/build_popup2.png")
build_popup2_rect = build_popup2.get_rect()
hovered_tobuild = ""

king_portrait = pygame.image.load("images/kingportrait.png")
king_scaled = pygame.transform.scale(king_portrait, (king_portrait.get_width() / 3, king_portrait.get_height() / 3))
king_portrait_rect = king_scaled.get_rect()
king_portrait_rect.center = (1890,1000)
king_hovered = False
king_transforming = False
king_transform_frame = 1
king_landed = False

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
building_costs = {
"house1": 200,
"tree1": 100,
"path1": 150,
"path2": 150,
"fountain1": 500,
"barracks1": 800,
"farmland1": 400,
}
citizen_count = 1
citizens = ["citizen1", "citizen2", "citizen3", "citizen4", "citizen5", "citizen6", "citizen7", "citizen8", "citizen9", "citizen10", "citizen11", "citizen12", "citizen13", "citizen14", "citizen15", "citizen16", "citizen17", "citizen18", "citizen19"]
valid_workers = ["citizen1", "citizen2", "citizen3", "citizen4", "citizen10", "citizen11", "citizen12", "citizen13", "citizen14", "citizen15", "citizen16", "citizen17", "citizen18", "citizen19"] # first 4 and new 10 are valid workers, soldiers are not
citizens_info = {
"citizen1_type": "m_pilgrim1", "citizen1_location": [1900,1200], "citizen1_targetoffset": [0,0], "citizen1_resting": 100,
"citizen2_type": "m_pilgrim2", "citizen2_location": [1950,1250], "citizen2_targetoffset": [0,0], "citizen2_resting": 56,
"citizen3_type": "m_pilgrim3", "citizen3_location": [1900,1150], "citizen3_targetoffset": [0,0], "citizen3_resting": 126,
"citizen4_type": "m_pilgrim4", "citizen4_location": [1950,1150], "citizen4_targetoffset": [0,0], "citizen4_resting": 126,
"citizen5_type": "m_pilgrim1", "citizen5_location": [1850,1180], "citizen5_targetoffset": [0,0], "citizen5_resting": 75, "citizen5_soldier": True,
"citizen6_type": "m_pilgrim2", "citizen6_location": [2000,1220], "citizen6_targetoffset": [0,0], "citizen6_resting": 90, "citizen6_soldier": True,
"citizen7_type": "m_pilgrim3", "citizen7_location": [1920,1130], "citizen7_targetoffset": [0,0], "citizen7_resting": 110, "citizen7_soldier": True,
"citizen8_type": "m_pilgrim4", "citizen8_location": [1980,1280], "citizen8_targetoffset": [0,0], "citizen8_resting": 65, "citizen8_soldier": True,
"citizen9_type": "m_pilgrim1", "citizen9_location": [1870,1270], "citizen9_targetoffset": [0,0], "citizen9_resting": 85, "citizen9_soldier": True,
"citizen10_type": "m_pilgrim2", "citizen10_location": [1750,1180], "citizen10_targetoffset": [0,0], "citizen10_resting": 80,
"citizen11_type": "m_pilgrim3", "citizen11_location": [2100,1250], "citizen11_targetoffset": [0,0], "citizen11_resting": 95,
"citizen12_type": "m_pilgrim4", "citizen12_location": [1850,1080], "citizen12_targetoffset": [0,0], "citizen12_resting": 105,
"citizen13_type": "m_pilgrim1", "citizen13_location": [2000,1350], "citizen13_targetoffset": [0,0], "citizen13_resting": 70,
"citizen14_type": "m_pilgrim2", "citizen14_location": [1800,1300], "citizen14_targetoffset": [0,0], "citizen14_resting": 120,
"citizen15_type": "m_pilgrim3", "citizen15_location": [2150,1190], "citizen15_targetoffset": [0,0], "citizen15_resting": 60,
"citizen16_type": "m_pilgrim4", "citizen16_location": [1930,1050], "citizen16_targetoffset": [0,0], "citizen16_resting": 135,
"citizen17_type": "m_pilgrim1", "citizen17_location": [2050,1370], "citizen17_targetoffset": [0,0], "citizen17_resting": 55,
"citizen18_type": "m_pilgrim2", "citizen18_location": [1780,1220], "citizen18_targetoffset": [0,0], "citizen18_resting": 140,
"citizen19_type": "m_pilgrim3", "citizen19_location": [1900,1320], "citizen19_targetoffset": [0,0], "citizen19_resting": 45,
}
citizen_types = ["m_pilgrim1", "m_pilgrim2", "m_pilgrim3", "m_pilgrim4"]
occupied_citizens = {}
# track a single nearby citizen by name instead of a list; empty string means none
citizens_in_proximity = ""
training_citizens = []
trained_soldiers = ["citizen5", "citizen6", "citizen7", "citizen8", "citizen9"]

default_personalities = ["friendly", "grumpy", "chill", "hyperactive", "lazy", "anxious", "stoic", "jokester"]
default_dialogues = ["Hello, my liege!", "What do you want?", "Nice weather we're having.", "Have you heard the latest news?", "I'm bored...", "I'm worried about the future.", "Life is meaningless.", "There's been a lot of butterflies lately.", "What brings you here?", "Another boring day, ain't it?"]
flirtatious_responses = ["Oh, stop it you!", "You're making me blush!", "Flattery will get you everywhere ;)", "You have a way with words, my liege.", "Is it getting hot in here or is it just you?", "I think I might be developing feelings for you...", "You're not so bad yourself ;)", "If you keep talking like that, I might have to do something about it..."]
distant_responses = ["That's weird...", "I don't know how to respond to that.", "Um... okay?", "Can we just talk about the weather?", "I'm not really in the mood to chat.", "Sorry, I'm a bit busy right now.", "Let's just focus on ruling the kingdom, shall we?", "I think we should keep things professional."]
default_responses = ["I'm just going out for a walk right now.", "I'm tending to my duties around the town.", "I'm visiting my family.", "I'm off to the market.", "I'm about to relax at home.", "I'm working on a project for the kingdom.", "I'm training with the guards.", "I'm taking care of some errands."]
angry_responses = ["Why are you talking to me?", "Leave me alone!", "I don't want to talk to you!", "Go bother someone else!", "I'm not in the mood for this!", "What did I ever do to you?", "Stop wasting my time!", "I'm warning you, back off!"]
flirtatious_dialogues = ["Why hello there, liege. ;)", "You look good today, liege.", "I was hoping I'd see you today, Liege.", "You know, I've been thinking about you a lot lately...", "I can't stop thinking about you, Liege.", "Funny to see you here, you were just on my mind."]
default_rizzed_reaction = ["Thanks, I guess?", "Um, thanks?", "Oh... thanks?", "I don't know how to respond to that, but thanks?", "I appreciate the compliment, I think?", "Thanks, you're not so bad yourself, I guess?", "Oh, you shouldn't have... but thanks?", "Well, that's flattering, thank you?"]
dialogue_closing = pygame.image.load("images/dialogue_closing.png")
dialogue_closing_rect = dialogue_closing.get_rect()
default_start_options = ["Chat", "Rizz", "Execute", "Leave"]
default_chat_options = {
"Speak of your day, commoner.": -10,
"What are you doing, my loyal servant?": 0,
"Peasant, what brings you in front of me?": -10,
"How are you doing?": 0,
}
default_flirt_options = {
"You're looking especially fine today.": 5,
"You look better than the other peasants.": -5,
"Your eyes remind me of the beauty of the sky.": 10,
"Your lips.. They're pretty.": 5,
"Your face looks good.": -5,
"Ugly bastard." : -20
}

for citizen in citizens:
    citizens_info[citizen + "_likeness_meter"] = 50

citizens_talking = []
population = len(citizens)
text_popupsinfo = {}
text_popups = []
in_chat = False
chat_with = ""
dialogue_ui = pygame.image.load("images/dialogue_ui.png")
dialogue_ui_rect = dialogue_ui.get_rect()
dialogue_hover = ""
dialogue_stage = "default"
onscreen_dialogue = default_start_options.copy() # starts off with the default chat options, but changes depending on the dialogue stage (flirt options, distant options, etc)
current_dialogue = ""
chosen_message = ""
closing_counter = 0

trade_offer = pygame.image.load("images/trade_offer.png")
trade_offer_rect = trade_offer.get_rect()
trade_menu = False
trade_hover = False

money = 2000
food = 100 # start with 100 so they don't lose immediately, since the farms take a while to grow crops and give food, so this gives them a grace period

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

def wrap_text(text, font, max_width):
    words = text.split(' ')
    lines = []
    current_line = ''
    for word in words:
        test_line = current_line + word + ' '
        if font.size(test_line)[0] <= max_width:
            current_line = test_line
        else:
            if current_line:
                lines.append(current_line.rstrip())
            current_line = word + ' '
    if current_line:
        lines.append(current_line.rstrip())
    return lines

#function for sending map drawing towards the middle nicely (SANTIAGO, AND SAME EXACT THING AS DRAW CIRCLES SO NO COMMENTS)
map_timer_count = 0
def send_towards_mid(map_name, fps, direction, scale):
    global map_timer_count, map_set_x, map_set_y, map_set_height, map_set_width
    
    map_timer_count += clock.get_time()/1000
    frame_duration = 1 / fps

    if map_timer_count >= frame_duration:
        map_timer_count -= frame_duration

        if direction == "right":
            map_set_x /= 1.04
            map_set_x = clamp(map_set_x, 600, inf)
        else:
            map_set_x *= 1.04
            map_set_x = clamp(map_set_x, 0, 600)
            
        if scale == "down":
            map_set_y /= 1.06
            map_set_y = clamp(map_set_y, 200, inf)
        else:
            map_set_y *= 1.06
            map_set_y = clamp(map_set_y, 0, 200)

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
   
    if current_screen == "town" and king_landed and "king" in citizens:
        citizens_in_proximity = ""
        proximity = 15
        king_x, king_y = citizens_info["king_location"]
        for citizen in citizens:
            if citizen == "king":
                continue
            dx = abs(citizens_info[citizen + "_location"][0] - king_x)
            dy = abs(citizens_info[citizen + "_location"][1] - king_y)
            if dx <= proximity and dy <= proximity:
                citizens_in_proximity = citizen
                break
    else:
        citizens_in_proximity = ""

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
                        start_transition("control_room")

            # (VIVEK SECTION OF CODE FOR THE TOWN)
            if current_screen == "town":
                if event.button == 1:
                    dragging = True # 
                    mouse_start = pygame.mouse.get_pos()
                    bg_start = townbg_rect.center
                if event.button == 3 and king_transforming == True or event.button == 3 and king_landed == True:
                    king_transforming = False
                    king_transform_frame = 1
                    king_landed = False
                    if "king" in citizens:
                        citizens.remove("king")
                if event.button == 1 and aestheticing == "door":
                    current_screen = "control_room"

                mouse_x, mouse_y = pygame.mouse.get_pos()

                # gets the mouse coordinates relative to the position of the background (offset)
                rel_x = mouse_x - townbg_rect.left
                rel_y = mouse_y - townbg_rect.top

                old_zoom = zoom # used to see how much it has grown or shrunk when doing later math

                if event.button == 1: # left click
                    
                    if in_chat == True and dialogue_hover != "" and dialogue_stage != "closing":
                        if dialogue_hover != "" and onscreen_dialogue[int(dialogue_hover) - 1] == "Leave":
                            in_chat = False
                            chat_with = ""
                            dialogue_hover = ""
                            dialogue_stage = "default"
                            onscreen_dialogue = default_start_options.copy()
                            current_dialogue = ""
                        if dialogue_hover != "" and onscreen_dialogue[int(dialogue_hover) - 1] == "Chat":
                            dialogue_stage = "chat"
                            dialogue_hover = ""
                            options = list(default_chat_options.keys())
                            random.shuffle(options)
                            onscreen_dialogue[0] = options[0]
                            onscreen_dialogue[1] = options[1]
                            onscreen_dialogue[2] = options[2]
                            onscreen_dialogue[3] = "Leave"
                        if dialogue_hover != "" and dialogue_stage == "chat":
                            chosen_message = onscreen_dialogue[int(dialogue_hover) - 1]
                            response_value = default_chat_options[chosen_message]
                            citizens_info[chat_with + "_likeness_meter"] += response_value
                            meter = citizens_info[chat_with + "_likeness_meter"]

                            if meter <= 30:
                                current_dialogue = random.choice(angry_responses)
                            else:
                                current_dialogue = random.choice(default_responses)

                            dialogue_stage = "closing"
                        if dialogue_hover != "" and onscreen_dialogue[int(dialogue_hover) - 1] == "Rizz":
                            dialogue_stage = "flirt"
                            dialogue_hover = ""
                            options = list(default_flirt_options.keys())
                            random.shuffle(options)
                            onscreen_dialogue[0] = options[0]
                            onscreen_dialogue[1] = options[1]
                            onscreen_dialogue[2] = options[2]
                            onscreen_dialogue[3] = "Leave"
                        if dialogue_hover != "" and dialogue_stage == "flirt":
                            chosen_message = onscreen_dialogue[int(dialogue_hover) - 1]
                            response_value = default_flirt_options[chosen_message]
                            citizens_info[chat_with + "_likeness_meter"] += response_value
                            meter = citizens_info[chat_with + "_likeness_meter"]
                            rizz_result = ""

                            if meter >= 70:
                                current_dialogue = random.choice(flirtatious_responses)
                            elif meter <= 30:
                                current_dialogue = random.choice(distant_responses)
                            else:
                                current_dialogue = random.choice(default_rizzed_reaction)

                            if response_value < 0:
                                current_dialogue = random.choice(distant_responses)

                            if response_value >= 5:
                                rizz_result = "W Rizz"
                            if response_value < 0:
                                rizz_result = "L Rizz"

                            if rizz_result != "":
                                text_id = str(random.randint(1,9999))
                                text_popups.append(text_id)  
                                text_popupsinfo[text_id + "_alpha"] = 100  
                                text_popupsinfo[text_id + "_text"] = rizz_result 
                                text_popupsinfo[text_id + "_location"] = [random.randint(0, 1920), random.randint(0, 1080)]  

                            dialogue_stage = "closing"
                        if dialogue_hover != "" and onscreen_dialogue[int(dialogue_hover) - 1] == "Execute":
                            citizens.remove(chat_with)
                            in_chat = False
                            chat_with = ""
                            dialogue_hover = ""
                            dialogue_stage = "default"
                            onscreen_dialogue = default_start_options.copy()
                            current_dialogue = ""
                             

                            current_screen = "execution"

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
                                money += building_costs[buildings_info[hovered[0] + "_type"]]

                                text_id = str(random.randint(1,9999))
                                text_popups.append(text_id)  
                                text_popupsinfo[text_id + "_alpha"] = 100  
                                text_popupsinfo[text_id + "_text"] = "+" + str(building_costs[buildings_info[hovered[0] + "_type"]])
                                text_popupsinfo[text_id + "_location"] = [mouse_x, mouse_y]
                                print(text_popupsinfo[text_id + "_text"])
                                if "farmland" in hovered[0]: # if a farm is being sold then remove the guys working there from the list
                                    if hovered[0] + "_occupants" in buildings_info and len(buildings_info[hovered[0] + "_occupants"]) != 0:
                                        citizens_info[buildings_info[hovered[0] + "_occupants"][0] + "_targetoffset"] = [1900 - citizens_info[buildings_info[hovered[0] + "_occupants"][0] + "_location"][0], 1200 - citizens_info[buildings_info[hovered[0] + "_occupants"][0] + "_location"][1]] # move the citizen back to the "unemployed area"
                                        del occupied_citizens[(buildings_info[hovered[0] + "_occupants"][0])]
                                        valid_workers.append(buildings_info[hovered[0] + "_occupants"][0])
                                        actionmade = True
                                if "barracks" in hovered[0]: # if a barracks is being sold then remove the guys working there from the list and remove them from the training list if they are in it
                                    for occupant in buildings_info[hovered[0] + "_occupants"]:
                                        citizens.append(occupant)
                                        valid_workers.append(occupant)
                                        del occupied_citizens[occupant]
                                        training_citizens.remove(occupant) if occupant in training_citizens else None
                                        citizens_info[occupant + "_targetoffset"] = [0,0]
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
                                    citizens_info[chosen_citizen + "_targetoffset"] = [int(buildings_info[hovered[0] + "_location"][0] - citizens_info[chosen_citizen + "_location"][0]), int(buildings_info[hovered[0] + "_location"][1] - citizens_info[chosen_citizen + "_location"][1])] # set the citizen target offset to the location of the building so they walk towards it
                                     
                                if len(buildings_info[hovered[0] + "_occupants"]) != 0 and actionmade == False:
                                    actionmade = True
                                    newoccupant = []
                                    del occupied_citizens[(buildings_info[hovered[0] + "_occupants"][0])]
                                    print(citizens_info[buildings_info[hovered[0] + "_occupants"][0] + "_location"])
                                    citizens_info[buildings_info[hovered[0] + "_occupants"][0] + "_targetoffset"] = [1900 - citizens_info[buildings_info[hovered[0] + "_occupants"][0] + "_location"][0], 1200 - citizens_info[buildings_info[hovered[0] + "_occupants"][0] + "_location"][1]] # move the citizen back to the "unemployed area"
                                    print("This is happening")
                                    valid_workers.append(buildings_info[hovered[0] + "_occupants"][0])
                                    buildings_info[hovered[0] + "_occupants"] = newoccupant
                            # barrakcs stuff for this

                            if train_troopshover == True and len(hovered) != 0:
                                if buildings_info[hovered[0] + "_training"] != 5:
                                    buildings_info[hovered[0] + "_training"] += 1
                                    chosen_soldier = random.choice(valid_workers)
                                    occupied_citizens[chosen_soldier] = hovered[0]
                                    valid_workers.remove(chosen_soldier)
                                    citizens_info[chosen_soldier + "_targetoffset"] = [int(buildings_info[hovered[0] + "_location"][0] - citizens_info[chosen_soldier + "_location"][0]), int(buildings_info[hovered[0] + "_location"][1] - citizens_info[chosen_soldier + "_location"][1])] # set the citizen target offset to the location of the building so they walk towards it 
                                    buildings_info[hovered[0] + "_occupants"].append(chosen_soldier)
                                    training_citizens.append(chosen_soldier)

                            if moving_hover == True and len(hovered) != 0:
                                moving_building = hovered[0]

                                if "barracks" in hovered[0]:
                                    for occupant in buildings_info[hovered[0] + "_occupants"]:
                                        citizens.append(occupant)
                                        valid_workers.append(occupant)
                                        del occupied_citizens[occupant]
                                        training_citizens.remove(occupant) if occupant in training_citizens else None
                                        citizens_info[occupant + "_targetoffset"] = [0,0]

                            hovered = [] #reset the hovered list to take away the hover ui

                    if building_menu == True and hovered_tobuild != "":
                        if building_costs[hovered_tobuild] > money:
                            dragging = False
                            break
                        building_id = random.randint(1, 99999999)
                        buildings.append(hovered_tobuild + str(building_id))
                        buildings_info[hovered_tobuild + str(building_id) + "_type"] = hovered_tobuild 
                        buildings_info[hovered_tobuild + str(building_id) + "_location"] = [0,0]
                        moving_building = hovered_tobuild + str(building_id) 
                        money -= building_costs[hovered_tobuild]

                        text_id = str(random.randint(1,9999))
                        text_popups.append(text_id)  
                        text_popupsinfo[text_id + "_alpha"] = 100  
                        text_popupsinfo[text_id + "_text"] = "-" + str(building_costs[hovered_tobuild])
                        text_popupsinfo[text_id + "_location"] = [mouse_x - 52, mouse_y + 50]  

                    if king_hovered == True:
                        print("wait3")
                        king_transforming = True
                    if king_transforming == True and king_transform_frame == 25:
                        citizens.append("king")
                        citizens_info["king_type"] = "m_king1"
                        # convert screen coords to world coords relative to the town background and current zoom
                        world_x = (mouse_x - townbg_rect.left) / zoom
                        world_y = (mouse_y - townbg_rect.top) / zoom
                        citizens_info["king_location"] = [world_x, world_y]
                        citizens_info["king_targetoffset"] = [0,0]
                        king_transforming = False
                        king_transform_frame = 1
                        king_landed = True

                
                if event.button == 1 and aestheticing == "tax":
                    trade_menu = True
                     
                else:
                    if trade_hover == False:
                        trade_menu = False
                if event.button == 1 and trade_menu == True and trade_hover == True:
                    if food >= 10:
                        food -= 10
                        money += 5
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

            if deciding_random_event:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()

                    if choice1_rect.collidepoint(mouse_pos):
                        effects = random_event_chosen["choices"][0]["effects"]

                    elif choice2_rect.collidepoint(mouse_pos):
                        effects = random_event_chosen["choices"][1]["effects"]
                    else:
                        effects = None

                    if effects:
                        for stat, value in effects.items():
                            if stat == "money":
                                money += money * value/100
                                money = max(0, money)
                            if stat == "happiness":
                                city_happiness += city_happiness * value/100
                                city_happiness = max(0, city_happiness)
                            if stat == "food":
                                food += food * value/100
                                food = max(0, food)

                        deciding_random_event = False

            # (SANTIAGO section of code for the mission board)
            if current_screen == "mission_board":
                if subtown_selected == "none":
                    for name in all_mission_maps:
                        button = all_mission_maps[name]
                        if mouse_x > button[0][0] * 4 and mouse_x < button[1][0] * 4 and mouse_y > button[0][1] * 4 and mouse_y < button[1][1] * 4:
                            subtown_selected = name
                            original_map_set_x = button[0][0] * 4
                            original_map_set_y = button[0][1] * 4
                            map_set_x = button[0][0] * 4
                            map_set_y = button[0][1] * 4

                    #back arrow to go back to town
                    if mouse_x > 150 and mouse_x < 150 + 375 and mouse_y > 850 and mouse_y < 850 + 180:
                        current_screen = "control_room"
                else:
                    button_vals = town_to_buttons[subtown_selected]
                    
                    #if you click on quick actions
                    if mouse_x >= 200 and mouse_x <= 250 + 200 and mouse_y >= 450 and mouse_y <= 450 + 250:
                        for button_name in quick_action_buttons:
                            lcbutton_x, lcbutton_y = quick_action_buttons[button_name][0]
                            rcbutton_x, rcbutton_y = quick_action_buttons[button_name][1]

                            if mouse_x > lcbutton_x + 200 and mouse_x < rcbutton_x + 200 and mouse_y > lcbutton_y + 450 and mouse_y < rcbutton_y + 450:
                                if button_name == "withdraw_troops":
                                    if town_information_store[subtown_selected][inner_town_selected]["troops_allocated"] > 5:
                                        troop_cnt += 5
                                        town_information_store[subtown_selected][inner_town_selected]["troops_allocated"] -= 5
                                    else:
                                        troop_cnt += town_information_store[subtown_selected][inner_town_selected]["troops_allocated"]
                                        town_information_store[subtown_selected][inner_town_selected]["troops_allocated"] = 0
                                    print(troop_cnt)
                                if button_name == "tax_control" and [inner_town_selected, subtown_selected] in owned_towns:
                                    tax_menu_open = True
                                if button_name == "allocate_troops":
                                    if town_information_store[subtown_selected][inner_town_selected]["activity_level"] == "NOT OWNED":
                                        war_prompt = True
                                    elif town_information_store[subtown_selected][inner_town_selected]["activity_level"] == "ENGAGED IN WAR" or town_information_store[subtown_selected][inner_town_selected]["activity_level"] == "OWNED":
                                        if troop_cnt >= 5:
                                            town_information_store[subtown_selected][inner_town_selected]["troops_allocated"] += 5
                                            troop_cnt -= 5
                                            print(troop_cnt)
                                if button_name == "end_war":
                                    if town_information_store[subtown_selected][inner_town_selected]["activity_level"] == "ENGAGED IN WAR":
                                        troop_cnt += town_information_store[subtown_selected][inner_town_selected]["troops_allocated"]
                                        towns_in_war_with.remove(inner_town_selected)
                                        town_information_store[subtown_selected][inner_town_selected]["troops_allocated"]  = 0
                                        town_information_store[subtown_selected][inner_town_selected]["activity_level"] = "NOT OWNED"
                    #if the player clicks on the tax menu while it is open
                    elif tax_menu_open and (mouse_x > 700 and mouse_x < 700 + 500 and mouse_y > 200 and mouse_y < 200 + 200):
                        for button in tax_buttons:
                            lcbutton_x, lcbutton_y = tax_buttons[button][0]
                            rcbutton_x, rcbutton_y = tax_buttons[button][1]
                            #closing button
                            if mouse_x > 700 + 215 and mouse_x < 272 + 700 and mouse_y > 144 + 200 and mouse_y < 200 + 166:
                                tax_menu_open = False

                            if mouse_x > lcbutton_x + 700 and mouse_x < rcbutton_x + 700 and mouse_y > lcbutton_y + 200 and mouse_y < rcbutton_y + 200:
                                town_information_store[subtown_selected][inner_town_selected]["tax_level"] = button
                                town_information_store[subtown_selected][inner_town_selected]["base_income"] = math.floor(default_inner_town_values[subtown_selected][inner_town_selected]["base_income"] * (1 + button/100))
                                tax_menu_open = False

                    #if the player clicks while a war prompt is on screen and within the war prompt
                    elif war_prompt and (mouse_x > 700 and mouse_x < 700 + 500 and mouse_y > 200 and mouse_y < 200 + 200):
                        #if they click on yes
                        if mouse_x > 41 + 700 and mouse_x < 158 + 700 and mouse_y > 110 + 200 and mouse_y < 150 + 200:
                            town_information_store[subtown_selected][inner_town_selected]["activity_level"] = "ENGAGED IN WAR"
                            
                            if troop_cnt >= 5:
                                town_information_store[subtown_selected][inner_town_selected]["troops_allocated"] += 5
                                troop_cnt -= 5
                                towns_in_war_with.append([inner_town_selected, subtown_selected])
                        
                            war_prompt = False
                        elif mouse_x > 293 + 700 and mouse_x < 410 + 700 and mouse_y > 110 + 200 and mouse_y < 150 + 200:
                            war_prompt = False
                    else:
                        #hiding the town information if you click somewhere else
                        if not (mouse_x >= 1300 and mouse_x <= 1300 + 500 and mouse_y >= 200 and mouse_y <= 200 + 700):
                            inner_town_selected = None

                    #creating a button for each inner town inside the subtown so you can click for invading information
                    for town_name in button_vals:
                        button = button_vals[town_name]

                        if mouse_x >= (button[0][0]) * 1.4 + 600 and mouse_x <= (button[1][0]) * 1.4 + 600 and mouse_y >= (button[0][1] ) * 1.4 + 200 and mouse_y <= (button[1][1]) * 1.4 + 200:
                            if not inner_town_selected:
                                inner_town_selected = town_name

                    #back arrow to go back to other screens
                    if mouse_x > 150 and mouse_x < 150 + 375 and mouse_y > 850 and mouse_y < 850 + 180:
                        original_map_set_x = None
                        original_map_set_y = None
                        map_set_x = None
                        map_set_y = None
                        map_set_width = 500//8 * 4  
                        map_set_height = 500//8 * 4
                        reached_middle = False
                        subtown_selected = "none"
                        tax_menu_open = False
                        inner_town_selected = None
                        war_prompt = False

            if current_screen == "control_room":
                #clicking on door (22 139) (66, 199)
                if mouse_x > 22 * 4 and mouse_x < 66 * 4 and mouse_y > 139 * 4 and mouse_y < 199 * 4:
                    current_screen = "town"
                
                #clicked on mission board (325, 133) (415, 183)
                if mouse_x > 325 * 4 and mouse_x < 415 * 4 and mouse_y > 133 * 4 and mouse_y < 183 * 4:
                    current_screen = "mission_board"

        if event.type == pygame.MOUSEBUTTONUP: # stopped click
            mouse_x, mouse_y = pygame.mouse.get_pos()
            if current_screen == "town":
                if event.button == 1:
                    dragging = False
            
        # keyboard events handled separately from mouse
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_e and current_screen == "town" and king_landed == True and citizens_in_proximity != "":
                in_chat = True
                chat_with = citizens_in_proximity  # holds the single citizen name
                print("running", chat_with)

                # essentially "suspend" the citizen
                citizens_info[chat_with + "_targetoffset"] = [0,0]
                

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
                #print(dialogue_hover)
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

                if mouse_x > 1837 and mouse_x < 1917 and mouse_y < 1024 and mouse_y > 956:
                    if king_landed == False:
                        king_hovered = True
                     
                else:   
                    if king_landed == False:
                        king_hovered = False

                if king_landed == True:
                    if mouse_x > 967 and mouse_x < 1237 and mouse_y < 996 and mouse_y > 873:
                        dialogue_hover = "4"
                    elif mouse_x > 679 and mouse_x < 948 and mouse_y < 842 and mouse_y > 729:
                        dialogue_hover = "1"
                    elif mouse_x > 968 and mouse_x < 1235 and mouse_y < 842 and mouse_y > 729:
                        dialogue_hover = "2"
                    elif mouse_x > 681 and mouse_x < 947 and mouse_y < 996 and mouse_y > 875:
                        dialogue_hover = "3"
                    else:
                        dialogue_hover = ""

                if barracks_open == True:
                    if mouse_x > 713 and mouse_x < 768 and mouse_y < 1067 and mouse_y > 1014:
                        train_troopshover = True
                    else:
                        train_troopshover = False
                
                if trade_menu == True:
                    if mouse_x > 819 and mouse_x < 1092 and mouse_y < 689 and mouse_y > 656:
                        trade_hover = True
                         
                    else:
                        trade_hover = False
    # continuous keyboard input (WASD) for king movement once he has landed
    if current_screen == "town" and king_landed and in_chat == False:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            citizens_info["king_location"][1] -= 4
        if keys[pygame.K_s]:
            citizens_info["king_location"][1] += 4
        if keys[pygame.K_a]:
            citizens_info["king_location"][0] -= 4
        if keys[pygame.K_d]:
            citizens_info["king_location"][0] += 4

    screen.fill((0, 0, 0))
    #drawing town (VIVEK)
    if current_screen == "town":
        population = len(citizens)
        if "king" in citizens:
            population -=1
        if king_landed == True and "king" not in citizens: #
            citizens.append("king")

        screen.blit(town_bg, townbg_rect)
            
        hovered_buildings_to_draw = []
        
        for building in buildings:
             
            building_blit = pygame.image.load("images/" + buildings_info[building + "_type"] + ".png").convert_alpha()
            if (building+"_timer") in buildings_info and "farmland" in building:
                if len(buildings_info[building + "_occupants"]) != 0 and abs(buildings_info[building + "_location"][0] - citizens_info[buildings_info[building + "_occupants"][0] + "_location"][0]) < 40 and abs(buildings_info[building + "_location"][1] - citizens_info[buildings_info[building + "_occupants"][0] + "_location"][1]) < 40: # if there are people working there then increase the timer, and after a certain amount of time change the image to the next stage of the farm
                    buildings_info[building + "_timer"] += 1

                if buildings_info[building + "_timer"] >= 500: # if the timer reaches 500 then reset it and give the player some crops (not implemented yet, just a ye
                    print("yield crops")
                    food += 10
                    text_id = str(random.randint(1,9999))
                    text_popups.append(text_id) # add the text popup to a list of text popups that will be drawn and updated every frame
                    text_popupsinfo[text_id + "_alpha"] = 100 # add a text popup for the crops that lasts 100 frames and add random number for not repeating keys, since the text popups are stored in a dict with the text as the key
                    text_popupsinfo[text_id + "_text"] = "+10 crops" # the text that will be shown in the popup
                    text_popupsinfo[text_id + "_location"] = [random.randint(0, 1920), random.randint(0, 1080)] # the location of the popup
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

            if "barracks" in building and (building + "_timer" in buildings_info): # if it's a barracks and it has a timer (it should always have a timer but just in case) then do this training code
                barrack_timer = buildings_info[building + "_timer"]
                #print(buildings_info[building + "_training"])
                if buildings_info[building + "_training"] != 0 and citizens_info[buildings_info[building + "_occupants"][0] + "_location"][0] - buildings_info[building + "_location"][0] < 2 and citizens_info[buildings_info[building + "_occupants"][0] + "_location"][1] - buildings_info[building + "_location"][1] < 2: # if there are people working there then increase the timer, and after a certain amount of time add a soldier to the citizens list and remove one from training
                    buildings_info[building + "_timer"] -= 1 

                #print(barrack_timer)
                if barrack_timer == 0 and buildings_info[building + "_training"] != 0: # THIS IS WHERE SOLDIERS GET ADDED SANTI
                    troop_cnt +=1
                    chosen_trainee = random.choice(training_citizens)
                    citizens.append(chosen_trainee)
                    training_citizens.remove(chosen_trainee)
                    buildings_info[building + "_timer"] = 100
                    buildings_info[building + "_training"] -= 1
                    if chosen_trainee in buildings_info[building + "_occupants"]:
                        buildings_info[building + "_occupants"].remove(chosen_trainee)
                    del occupied_citizens[chosen_trainee]
                    trained_soldiers.append(chosen_trainee)
                    citizens_info[chosen_trainee + "_soldier"] = True
                    print("running")
                
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
            if (citizen + "_soldier") not in citizens_info: 
                citizen_blit = pygame.image.load("images/" + citizens_info[citizen + "_type"] + ".png").convert_alpha()
            else:
                citizen_blit = pygame.image.load("images/" + "m_soldier1"   + ".png").convert_alpha()
            citizen_scaled = pygame.transform.scale(citizen_blit, (int(citizen_blit.get_width() * zoom * 2),int(citizen_blit.get_height()*zoom * 2)))
            citizen_blit_rect = citizen_scaled.get_rect()
            
            if citizen != "king" and citizen != chat_with: # if the citizen isn't the king or the one being talked to then do this movement code, otherwise they just stand still
                if citizens_info[citizen + "_resting"] != 0 and citizens_info[citizen + "_targetoffset"] == [0,0]:
                    citizens_info[citizen + "_resting"] = citizens_info[citizen + "_resting"] - 1
                    #print(citizens_info[citizen + "_resting"])
                if citizens_info[citizen + "_resting"] == 0 and citizens_info[citizen + "_targetoffset"] == [0,0]:
                    if citizen not in occupied_citizens:
                        citizens_info[citizen + "_targetoffset"] = [random.randint(-100, 100), random.randint(-100, 100)]
                    else:
                        if "barracks" not in occupied_citizens[citizen]: 
                            citizens_info[citizen + "_targetoffset"] = [random.randint(-10, 10), random.randint(-10, 10)]
                    if citizen in occupied_citizens and "barracks" not in occupied_citizens[citizen]:
                        if citizen in occupied_citizens:
                            move_back = random.randint(1,3)
                            if move_back == 3: # making them walk back to farm either randomly or if they get too far
                                citizens_info[citizen + "_targetoffset"] = [int(buildings_info[occupied_citizens[citizen] + "_location"][0] - citizens_info[citizen + "_location"][0]), int(buildings_info[occupied_citizens[citizen] + "_location"][1] - citizens_info[citizen + "_location"][1])]
                            #print(buildings_info[occupied_citizens[citizen] + "_location"][0] - citizens_info[citizen + "_location"][0])
                            if buildings_info[occupied_citizens[citizen] + "_location"][0] - citizens_info[citizen + "_location"][0] > 40 or buildings_info[occupied_citizens[citizen] + "_location"][0] - citizens_info[citizen + "_location"][0] < -40:
                                citizens_info[citizen + "_targetoffset"] = [int(buildings_info[occupied_citizens[citizen] + "_location"][0] - citizens_info[citizen + "_location"][0]), int(buildings_info[occupied_citizens[citizen] + "_location"][1] - citizens_info[citizen + "_location"][1])]
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
                if citizen in occupied_citizens and "barracks" in occupied_citizens[citizen] and citizens_info[citizen + "_targetoffset"] == [0,0]: # if the citizen works at the barracks and isn't currently moving somewhere then have them move towards the farm to simulate going to work, and then after a certain amount of time have them move back to the barracks to simulate going back from work
                    citizens.remove(citizen) # remove them for now so they dont show on screen
                    training_citizens.append(citizen)

            if "king" in citizens and citizen != "king": # if king is on the map do this stuff for the dialogue options
                 
                dx = abs(citizens_info[citizen + "_location"][0] - citizens_info["king_location"][0])
                dy = abs(citizens_info[citizen + "_location"][1] - citizens_info["king_location"][1])

                distance_from_king = dx + dy

                proximity = 15
                if dx <= proximity and dy <= proximity:
                    SMALLER_pixel_font = pygame.font.Font('all_fonts/VCR_OSD_MONO_1.001.ttf', 15)
                    screen.blit(SMALLER_pixel_font.render("Press E to talk", True, (255,255,255)), (townbg_rect.left + citizens_info[citizen + "_location"][0] * zoom - 60, townbg_rect.top  + citizens_info[citizen + "_location"][1] * zoom - 25))
                    # proximity already computed before input; no assignment needed here
                
            world_x, world_y = citizens_info[citizen + "_location"]
            citizen_blit_rect.center = (townbg_rect.left + world_x * zoom, townbg_rect.top  + world_y * zoom) # simply scaling with zoom then adding the offset from the townbgs left and top         
            screen.blit(citizen_scaled, citizen_blit_rect)
        
        night_overlay = pygame.Surface((screen.get_width(), screen.get_height()))
        night_overlay.fill((0, 0, 0))
        
        if timer < 1700:
            night_overlay.set_alpha(timer / 10)
        else:
            night_overlay.set_alpha(1700 / 10)

        screen.blit(night_overlay, (0, 0))

        for building, building_rect in hovered_buildings_to_draw:
    
            square_surf = pygame.Surface((building_rect.width, building_rect.height))
            square_surf.set_alpha(50)
            square_surf.fill((0, 0, 0))
            screen.blit(square_surf, building_rect)
            SMALLER_pixel_font = pygame.font.Font('all_fonts/VCR_OSD_MONO_1.001.ttf', 35)

            if "farmland" not in building:
                screen.blit(build_popup, build_popup_rect)
            if "farmland" in building:
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
            if "barracks" in building:
                screen.blit(barracks_popup, barracks_popup_rect)
                screen.blit(build_popup3, build_popup3_rect)
                barracks_open = True
                if (building + "_training") not in buildings_info:
                    buildings_info[building + "_training"] = 0
                    buildings_info[building + "_timer"] = 100
                    buildings_info[building + "_occupants"] = []
                screen.blit(smaller_pixel_font.render(str(buildings_info[building + "_training"]) + "/5", True, (255,255,255)), (493, 785))
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

        SMALLER_pixel_font = pygame.font.Font('all_fonts/VCR_OSD_MONO_1.001.ttf', 15)
        if hovered_tobuild != "":
            screen.blit(SMALLER_pixel_font.render("Costs: " + str(building_costs[hovered_tobuild]), True, (255,255,255)), (mouse_x - 50, mouse_y + 20))
            
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
        if in_chat == False:
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
            smaller_pixel_font = pygame.font.Font('all_fonts/VCR_OSD_MONO_1.001.ttf', 50)
            screen.blit(smaller_pixel_font.render("Day " + str(day), True, (255,255,255)), (880, 50))

        for text in text_popups:
            popup_pixel_font = pygame.font.Font('all_fonts/VCR_OSD_MONO_1.001.ttf', 35)
            popup_surface = popup_pixel_font.render(text_popupsinfo[text + "_text"], True, (255,255,255))
            popup_surface.set_alpha(text_popupsinfo[text + "_alpha"])
            screen.blit(popup_surface, (text_popupsinfo[text + "_location"][0], text_popupsinfo[text + "_location"][1]))
            text_popupsinfo[text + "_alpha"] -= 10
            if text_popupsinfo[text + "_alpha"] <= 0:
                text_popups.remove(text)
                del text_popupsinfo[text + "_text"]
                del text_popupsinfo[text + "_alpha"]
                del text_popupsinfo[text + "_location"]
                break # brreak to prevent errors

        if in_chat == False:
            moneyandfood_pixel_font = pygame.font.Font('all_fonts/VCR_OSD_MONO_1.001.ttf', 15)
            screen.blit(moneyandfood_pixel_font.render(str(money), True, (255,255,255)), (1859, 1060))
            screen.blit(moneyandfood_pixel_font.render(str(food), True, (255,255,255)), (1859, 1036))
            screen.blit(moneyandfoodicons, moneyandfoodicons_rect)

        # king stuff and turning king to walkable citizen

        if king_transforming == False and king_landed == False:
            screen.blit(king_scaled, king_portrait_rect)
        if king_transforming == True and king_landed == False:
            #print(king_transform_frame)
             
            small_king = pygame.image.load("images/m_king1.png")
            small_king_scaled = pygame.transform.scale(small_king, (small_king.get_width() * zoom * 2, small_king.get_height() * zoom * 2))
            small_king_rect = small_king_scaled.get_rect()
            small_king_rect.center = (mouse_x, mouse_y)
            screen.blit(small_king_scaled, small_king_rect)
            screen.blit(moneyandfood_pixel_font.render("Right click to cancel", True, (255,255,255)), (mouse_x - 90, mouse_y + 50))

            king_anim = pygame.image.load("images/kingtosmall" + str(king_transform_frame) + ".png")
            king_animscaled = pygame.transform.scale(king_anim, (king_anim.get_width() / 3, king_anim.get_height() / 3))
            king_anim_rect = king_animscaled.get_rect()
            king_anim_rect.center = (mouse_x,mouse_y)
            if king_transform_frame != 25:
                king_transform_frame += 1
            screen.blit(king_animscaled, king_anim_rect)
        
        # dialogues tuff

        if in_chat:
            if dialogue_stage != "closing":
                screen.blit(dialogue_ui, dialogue_ui_rect)
            else:
                screen.blit(dialogue_closing, dialogue_closing_rect)

            citizen_portrait = pygame.image.load("images/" + citizens_info[chat_with + "_type"] + "_dialogue.png").convert_alpha()
            citizen_portrait_scaled = pygame.transform.scale(citizen_portrait, (citizen_portrait.get_width() * 2.5, citizen_portrait.get_height() * 2.5))
            citizen_portrait_rect = citizen_portrait_scaled.get_rect()
            citizen_portrait_rect.center = (960, 350)
            screen.blit(citizen_portrait_scaled, citizen_portrait_rect)
            SMALLER_pixel_font = pygame.font.Font('all_fonts/VCR_OSD_MONO_1.001.ttf', 15)
            line_height = SMALLER_pixel_font.get_height() + 2
            max_width = 250
            
            if dialogue_stage != "closing":
                if dialogue_stage == "default":
                    screen.blit(smaller_pixel_font.render(onscreen_dialogue[0], True, (255,255,255)), (750, 775))
                    screen.blit(smaller_pixel_font.render(onscreen_dialogue[1], True, (255,255,255)), (1030, 775))
                    screen.blit(smaller_pixel_font.render(onscreen_dialogue[2], True, (255,255,255)), (715, 910))
                    screen.blit(smaller_pixel_font.render(onscreen_dialogue[3], True, (255,255,255)), (1030, 910))
                else:
                    
                    lines0 = wrap_text(onscreen_dialogue[0], SMALLER_pixel_font, max_width)
                    for i, line in enumerate(lines0):
                        screen.blit(SMALLER_pixel_font.render(line, True, (255,255,255)), (750, 775 + i * line_height))
                    lines1 = wrap_text(onscreen_dialogue[1], SMALLER_pixel_font, max_width)
                    for i, line in enumerate(lines1):
                        screen.blit(SMALLER_pixel_font.render(line, True, (255,255,255)), (1020, 775 + i * line_height))
                    lines2 = wrap_text(onscreen_dialogue[2], SMALLER_pixel_font, max_width)
                    for i, line in enumerate(lines2):
                        screen.blit(SMALLER_pixel_font.render(line, True, (255,255,255)), (715, 910 + i * line_height))
                    lines3 = wrap_text(onscreen_dialogue[3], SMALLER_pixel_font, max_width)
                    for i, line in enumerate(lines3):
                        screen.blit(SMALLER_pixel_font.render(line, True, (255,255,255)), (1030, 910 + i * line_height))

            if current_dialogue == "" and dialogue_stage == "default" and citizens_info[chat_with + "_likeness_meter"] < 70:
                current_dialogue = random.choice(default_dialogues)
            if current_dialogue == "" and citizens_info[chat_with + "_likeness_meter"] >= 70 and dialogue_stage == "default":
                current_dialogue = random.choice(flirtatious_dialogues)
            text_surface = SMALLER_pixel_font.render(current_dialogue, True, (255,255,255))
            text_rect = text_surface.get_rect(center=(960, 650))
            # draw black bg
            bg_rect = text_rect.copy()
            bg_rect.width += 20
            bg_rect.height += 10
            bg_rect.center = text_rect.center
            pygame.draw.rect(screen, (0, 0, 0), bg_rect)
            screen.blit(text_surface, text_rect)
            
            if dialogue_stage == "closing":
                closing_counter += 1

            if dialogue_stage == "closing" and closing_counter == 50:
                in_chat = False
                chat_with = ""
                dialogue_hover = ""
                dialogue_stage = "default"
                onscreen_dialogue = default_start_options.copy()
                current_dialogue = ""  
                closing_counter = 0

        if trade_menu == True:
         
            screen.blit(trade_offer, trade_offer_rect)

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

        # -----------------------
        # Portraits
        # -----------------------
        king_scaled = pygame.transform.scale(king_portrait, (480, 270))
        queen_scaled = pygame.transform.scale(queen_portrait, (480, 270))

        # center portraits inside their boxes
        king_pos = (KING_BOX.x + (KING_BOX.width - 480) // 2, KING_BOX.y + (KING_BOX.height - 270) // 2)
        queen_pos = (QUEEN_BOX.x + (QUEEN_BOX.width - 480) // 2, QUEEN_BOX.y + (QUEEN_BOX.height - 270) // 2)

        # draw box backgrounds (optional)
        pygame.draw.rect(screen, (0, 0, 0), KING_BOX)
        pygame.draw.rect(screen, (0, 0, 0), QUEEN_BOX)

        # box outlines
        pygame.draw.rect(screen, (255, 255, 255), KING_BOX, 4)
        pygame.draw.rect(screen, (255, 255, 255), QUEEN_BOX, 4)

        screen.blit(king_scaled, king_pos)
        screen.blit(queen_scaled, queen_pos)

        # highlight selected
        if role_selected == "KING":
            pygame.draw.rect(screen, (255, 255, 255), KING_BOX, 10)
        if role_selected == "QUEEN":
            pygame.draw.rect(screen, (255, 255, 255), QUEEN_BOX, 10)

        # labels
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
                fancy_back_arrow = pygame.transform.scale(fancy_back_arrow, (375, 180))

                map_text_color = (255,255,255)
                if all_mission_maps[map][0][0] > 100:
                    screen.blit(pygame.font.Font('all_fonts/VCR_OSD_MONO_1.001.ttf', 30).render(map.upper(), True, (map_text_color)), (all_mission_maps[map][0][0] * 4 - (25 * len(list(map))), all_mission_maps[map][0][1] * 4 + 100))
                else:
                    screen.blit(pygame.font.Font('all_fonts/VCR_OSD_MONO_1.001.ttf', 30).render(map.upper(), True, (map_text_color)), (all_mission_maps[map][0][0] * 4 + (25 * len(list(map))) + 20, all_mission_maps[map][0][1] * 4 + 100))

                screen.blit(map_img, (all_mission_maps[map][0][0] * 4, all_mission_maps[map][0][1] * 4))
                screen.blit(fancy_back_arrow, (150, 850))

                #checking when you are hovering over a map and then drawing the inner and outer circle for a nice animation for hovering 
                if map == outlined: 
                    map_text_color = (255,78,0)
                    outer_radius_length, inner_radius_length = draw_circles(map, map_img.get_height(), map_img.get_width())
                    pygame.draw.circle(screen, (255,255,255), (all_mission_maps[map][0][0] * 4 + map_img.get_width()//2, all_mission_maps[map][0][1] * 4 + map_img.get_height()//2), inner_radius_length, 5)
                    pygame.draw.circle(screen, (255,255,255), (all_mission_maps[map][0][0] * 4 + map_img.get_width()//2, all_mission_maps[map][0][1] * 4 + map_img.get_height()//2), outer_radius_length, 5)
        else:
            if not reached_middle:
                if original_map_set_x > 1920/2:
                    direction = "right"
                else:
                    direction = "left"

                if original_map_set_y > 200:
                    scale = "down"
                else:
                    scale = "up"

                send_towards_mid(subtown_selected, 180, direction, scale) #constantly moving the map towards the middle of the screen when you click on a map
            
            map_img = pygame.image.load("maps/" + subtown_selected + "_map.png")
            map_img = pygame.transform.scale(map_img, (map_set_width, map_set_height))
            roads = pygame.image.load("maps/" + subtown_selected + "_roads.png")
            roads = pygame.transform.scale(roads, (map_set_width, map_set_height))
            cities = pygame.image.load("maps/" + subtown_selected + "_cities.png")
            cities = pygame.transform.scale(cities, (map_set_width, map_set_height))

            if inner_town_selected:
                screen.blit(troop_allocation, (1300, 200))
                screen.blit(quick_actions, (200, 450))
                screen.blit(pygame.font.Font('all_fonts/VCR_OSD_MONO_1.001.ttf', 40).render(str.upper(inner_town_selected), True, (255,255, 255)), (1550 - (len(inner_town_selected)//2 * 25), 150)) #positioning the string in the middle of the img (1300 + 250 which 250 is half the width), then moving the string to the left by half its width * each letter pixel size so its centered

                #filling all of the information for the troop allocation page/menu
                #all of the random numbers that will be added will be the original offsets in the drawing software im using, so for ex, a text was placed on x coordinate 283, now i need to add 283 onto the 1300 offset i already have.
                town_info = town_information_store[subtown_selected][inner_town_selected]
                
                screen.blit(pygame.font.Font('all_fonts/VCR_OSD_MONO_1.001.ttf', 20).render(str(town_info["activity_level"]), True, (0,0, 0)), (1300 + 258, 200 + 214))
                screen.blit(pygame.font.Font('all_fonts/VCR_OSD_MONO_1.001.ttf', 20).render(str(town_info["stationed_troops"]), True, (0,0, 0)), (1300 + 305, 200 + 241))
                screen.blit(pygame.font.Font('all_fonts/VCR_OSD_MONO_1.001.ttf', 20).render(str(town_info["significance_level"]), True, (0,0, 0)), (1300 + 316, 200 + 269))
                screen.blit(pygame.font.Font('all_fonts/VCR_OSD_MONO_1.001.ttf', 20).render(str(int(town_info["happiness"])), True, (0,0, 0)), (1300 + 283, 200 + 301))
                screen.blit(pygame.font.Font('all_fonts/VCR_OSD_MONO_1.001.ttf', 20).render(str(town_info["troops_allocated"]), True, (0,0, 0)), (1300 + 313, 200 + 398))
                screen.blit(pygame.font.Font('all_fonts/VCR_OSD_MONO_1.001.ttf', 20).render(str(town_info["tax_level"]), True, (0,0, 0)), (1300 + 202, 200 + 433))
                screen.blit(pygame.font.Font('all_fonts/VCR_OSD_MONO_1.001.ttf', 20).render(str(town_info["base_income"]), True, (0,0, 0)), (1300 + 273, 200 + 459))
                screen.blit(pygame.font.Font('all_fonts/VCR_OSD_MONO_1.001.ttf', 20).render(str(town_info["citizens_gained"]), True, (0,0, 0)), (1300 + 272, 200 + 493))

        # smaller_pixel_font = pygame.font.Font('all_fonts/VCR_OSD_MONO_1.001.ttf', 50)
        # screen.blit(smaller_pixel_font.render("PLAY", True, play_text_btn_color), (1200, 550))

            screen.blit(map_img, (map_set_x, map_set_y))
            screen.blit(roads, (map_set_x, map_set_y))
            screen.blit(cities, (map_set_x, map_set_y))
            screen.blit(fancy_back_arrow, (150, 850))

            #if they are about to go to war
            if war_prompt:
                screen.blit(prompt_for_war_img, (700, 200))
            
            if tax_menu_open:
                screen.blit(tax_control, (700, 200))

    if current_screen == "control_room":
        screen.blit(pygame.transform.scale(control_room, (control_room.get_width() * 4, control_room.get_height() * 4)), (0,0))
        if role_selected == "KING":
            screen.blit(pygame.transform.scale(king_standing, (king_standing.get_width() * 4, king_standing.get_height() * 4)), (0,0))
        else:
            screen.blit(pygame.transform.scale(queen_standing, (queen_standing.get_width() * 4, queen_standing.get_height() * 4)), (0,0))

    if current_screen == "execution":
        spike = pygame.image.load("images/spike.png").convert_alpha()
        spike_scaled = pygame.transform.scale(spike, (spike.get_width() * 2, spike.get_height() * 2))
        spike_rect = spike_scaled.get_rect()
        screen.blit(spike_scaled, (960 - spike_scaled.get_width() // 2, 580))

        falling_man = pygame.image.load("images/man_falling.png").convert_alpha()
        if falling_man_y < ground_y:
            falling_man_y += falling_speed
        
        falling_man_scaled = pygame.transform.scale(falling_man, (falling_man.get_width() * 2, falling_man.get_height() * 2))
        screen.blit(falling_man_scaled, (960 - falling_man_scaled.get_width() // 2, falling_man_y))

        execution_timer += 1
        
        if falling_man_y >= ground_y:
            blood_frame = pygame.image.load("images/blood_frame" + str(blood_counter) + ".png").convert_alpha()
            blood_frame_scaled = pygame.transform.scale(blood_frame, (blood_frame.get_width() * 2, blood_frame.get_height() * 2))

            screen.blit(blood_frame_scaled, (960 - spike_scaled.get_width() // 2, ground_y))
            if blood_counter != 6:
                blood_counter += 1

        if execution_timer == 300:
            current_screen = "town"
            execution_timer = 0
            dragging = False
            falling_man_y = -200
            blood_counter = 1
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

    #drawing the decision panel
    if deciding_random_event:
        screen.blit(daily_event, (600, 200))

        # event title
        title_font = pygame.font.Font('all_fonts/VCR_OSD_MONO_1.001.ttf', 30)
        screen.blit(
            title_font.render(random_event_chosen["title"], True, (0,0,0)),
            (900 - 10 * len(random_event_chosen["title"]), 200 + 200)
        )

        # event description
        font = pygame.font.Font('all_fonts/VCR_OSD_MONO_1.001.ttf', 15)
        description = random_event_chosen["description"]

        box_left = 600
        box_width = daily_event.get_width()
        padding = 140

        text_x = box_left + padding
        max_width = box_width - padding * 2

        words = description.split(" ")
        lines = []
        current_line = ""

        for word in words:
            test_line = current_line + word + " "
            if font.size(test_line)[0] <= max_width:
                current_line = test_line
            else:
                lines.append(current_line)
                current_line = word + " "

        lines.append(current_line)

        y = 200 + 300
        for line in lines:
            text_surface = font.render(line, True, (0,0,0))
            screen.blit(text_surface, (text_x, y))
            y += 20

        button_font = pygame.font.Font('all_fonts/VCR_OSD_MONO_1.001.ttf', 18)

        # mvoing buttons
        choice1_rect = pygame.Rect(720, 580, 360, 55)  # was 520
        choice2_rect = pygame.Rect(720, 655, 360, 55)  # was 590

        mouse_pos = pygame.mouse.get_pos()

        # brown color for buttons
        brown = (139, 69, 19)
        hover_brown = (160, 82, 45)  # slightly lighter when hovered

        color1 = hover_brown if choice1_rect.collidepoint(mouse_pos) else brown
        color2 = hover_brown if choice2_rect.collidepoint(mouse_pos) else brown

        pygame.draw.rect(screen, color1, choice1_rect)
        pygame.draw.rect(screen, color2, choice2_rect)

        choice1_text = random_event_chosen["choices"][0]["text"]
        choice2_text = random_event_chosen["choices"][1]["text"]

        screen.blit(
            button_font.render(choice1_text, True, (0,0,0)),
            (choice1_rect.x + 10, choice1_rect.y + 18)
        )

        screen.blit(
            button_font.render(choice2_text, True, (0,0,0)),
            (choice2_rect.x + 10, choice2_rect.y + 18)
        )

    #time progression for days
    if current_screen != "main_menu" and current_screen != "role_select" and not deciding_random_event:
        if timer_reversed == False:
            timer+=1
        else:
            timer-=1

    #every half day, present a random event
    if timer % 1000 == 0:
        timer += 1
        deciding_random_event = True
        random_event_chosen = random.choice(all_random_events["events"])

    if timer % 50 == 0:
        towns_to_remove_owned = []
        towns_to_remove_war = []
        #for towns that are currently owned, edit their values and reap income
        for value in owned_towns:
            town, subtown = value

            #if taxes are low, increase happiness, if they are high, decrease (of couse more money though.)
            if town_information_store[subtown][town]["tax_level"] <= 15: #low tax levels
                town_information_store[subtown][town]["happiness"] += 1 - min(1, random.uniform(0, 1) * (town_information_store[subtown][town]["tax_level"] * 0.08))
                if town_information_store[subtown][town]["happiness"] > 100:
                    town_information_store[subtown][town]["happiness"] = 100
            else:
                town_information_store[subtown][town]["happiness"] -= random.uniform(0, 0.5) * (town_information_store[subtown][town]["tax_level"] * 0.08)
                if town_information_store[subtown][town]["happiness"] < 0:
                    town_information_store[subtown][town]["happiness"] = 0
 
            #there is a chance for citizens to come over to your kingdom depending on if a colony really likes you and has max happiness
            chance = (town_information_store[subtown][town]["happiness"] - 50) / 50 * 0.01
            
            if random.random() < chance:
                town_information_store[subtown][town]["citizens_gained"] += 1
                citizens.append("citizen" + str(population + 1))
                valid_workers.append("citizen" + str(population + 1))

                population = len(citizens)

                citizens_info["citizen" + str(population) + "_location"] = [random.randint(1900, 2000), random.randint(1100,1300)]
                citizens_info["citizen" + str(population) + "_targetoffset"] = [0,0]
                citizens_info["citizen" + str(population) + "_resting"] = random.randint(1, 200)
                citizens_info["citizen" + str(population) + "_type"] = random.choice(citizen_types)

            #chances for revolution can begin below 50, of course, they will be extremely low directly below 50 but as we approach 20 get higher
            if town_information_store[subtown][town]["happiness"] < 50:
                happiness = town_information_store[subtown][town]["happiness"]
                troops = town_information_store[subtown][town]["troops_allocated"]

                #0 represents low chance, and 1 represents a high chance
                unhappiness_factor = (50 - happiness) / 50

                # more troops = smaller factor
                troop_factor = 1 / (1 + troops / 200)

                revolt_chance = 0.10 * unhappiness_factor * troop_factor
    
                if random.random() < revolt_chance:
                    towns_to_remove_owned.append(value)
                    town_information_store[subtown][town]["activity_level"] = "ENGAGED IN WAR"
                    town_information_store[subtown][town]["stationed_troops"] = random.randint(int(troops * 0.3), int(troops * 1.3))
                    towns_in_war_with.append(value)
                    
        for removing in towns_to_remove_owned:
            owned_towns.remove(removing)

        #for towns at war with, progress the war
        for value in towns_in_war_with:
            town, subtown = value
            friendly_troops = town_information_store[subtown][town]["troops_allocated"]
            enemy_troops = town_information_store[subtown][town]["stationed_troops"]
            if abs(friendly_troops - enemy_troops) < 30:
                enemy_troops *= 1.02
            
            extra_friendly_power = 1
            extra_enemy_power = 1

            if friendly_troops < enemy_troops:
                extra_friendly_power = 1 + 0.09 * abs(enemy_troops - friendly_troops)
            else:
                extra_enemy_power = 1 + 0.09 * abs(enemy_troops - friendly_troops)

            f_copy = friendly_troops
            total_friendly_troops_lost = random.uniform(0.4, 1.6) * enemy_troops * extra_enemy_power * 0.15
            friendly_troops -= total_friendly_troops_lost
            friendly_troops = max(0, friendly_troops)
            enemy_troops -= random.uniform(0.4, 1.6) * f_copy * extra_friendly_power * 0.15
            enemy_troops = max(0, enemy_troops)

            town_information_store[subtown][town]["troops_allocated"] = round(friendly_troops)
            total_friendly_troops_lost = f_copy - town_information_store[subtown][town]["troops_allocated"]
            town_information_store[subtown][town]["stationed_troops"] = round(enemy_troops)

            for troop in range(round(total_friendly_troops_lost)):
                chosen_soldier = random.choice(trained_soldiers)
                trained_soldiers.remove(random.choice(chosen_soldier))
                citizens.remove(chosen_soldier)

            if enemy_troops == 0:
                town_information_store[subtown][town]["activity_level"] = "OWNED"
                owned_towns.append([town, subtown])
                towns_to_remove_war.append(value)
        
        for removing in towns_to_remove_war:
            towns_in_war_with.remove(removing)
     
    if timer % 200 == 0:
        for town in owned_towns:
            pass

    #each new day print new day
    if timer >= 2000:
        timer_reversed = True
        timer = 1999

    if timer == -300 and timer_reversed == True: # new day!
        print("New day")
        day +=1
        timer_reversed = False

        # Calculate surplus food before consumption
        surplus = food - population * 5
        if surplus > 0:
            birth_count = int(population / 3)
        else:
            birth_count = 0

        # Consume food
        food -= population * 5
        if food < 0:
            death_count = -food // 5
            food = 0
        else:
            death_count = 0

        for person in range(birth_count):
                
            citizens.append("citizen" + str(population + 1))
            valid_workers.append("citizen" + str(population + 1))
            population = len(citizens)
            citizens_info["citizen" + str(population) + "_location"] = [random.randint(1900, 2000), random.randint(1100,1300)]
            citizens_info["citizen" + str(population) + "_targetoffset"] = [0,0]
            citizens_info["citizen" + str(population) + "_resting"] = random.randint(1, 200)
            citizens_info["citizen" + str(population) + "_type"] = random.choice(citizen_types)

        for person in range(death_count):
            if len(citizens) != 0:
                chosen_citizen = random.choice(citizens)
                print(chosen_citizen + " has died of starvation")
                citizens.remove(chosen_citizen)
                if chosen_citizen in valid_workers:
                    valid_workers.remove(chosen_citizen)
                if chosen_citizen in occupied_citizens:
                    del occupied_citizens[chosen_citizen]

    pygame.display.flip()
    print(timer)

    clock.tick(60)