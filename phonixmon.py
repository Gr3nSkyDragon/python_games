import pygame
import sys
import random
import os
import string
import pyttsx3
import pickle
from pygame.time import Clock

# Initialize pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Colors
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165, 0)
GRAY = (128, 128, 128)
BLACK = (0, 0, 0)
PINK = (255, 182, 193)
NAVY_BLUE = (0, 0, 128)

#Scrollbar settings
SCROLLBAR_COLOR = (100, 100, 255, 150)  # Blue with transparency
SCROLLBAR_WIDTH = 10

# Button properties
grass_size = 150
small_btn_size = 60
vertical_spacing = 50

# Set up the display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Phonixmon")
clock = Clock()
icon = pygame.image.load('resources/icon/phonics.png').convert_alpha()
pygame.display.set_icon(icon)

# Game data
ball_count = 5
item_collect_amount = 0
current_encounter_image = None
current_encounter_name = ""
current_letter_buttons = []
current_correct_letters = []
current_display_name = ""
letters_revealed = 0
letters_to_reveal = 1  # 1, 2, or 3
dictionary_items = []
dictionary_scroll_offset = 0
dictionary_drag_start_y = None
dictionary_item_height = 50  # Height of each item in the list
dictionary_scroll_dragging = False
SAVE_FILE = 'phonixmons_save.dat'

# Initialize text-to-speech engine
def init_tts():
    try:
        engine = pyttsx3.init()
        voices = engine.getProperty('voices')
        engine.setProperty('rate', 170)
        engine.setProperty('volume', 0.9)
        engine.setProperty('voice', voices[1].id)
        return engine
    except Exception as e:
        print(f"Error initializing text-to-speech: {e}")
        return None

# Load images
try:
    if not os.path.exists('resources'):
        os.makedirs('resources')
    if not os.path.exists('resources/mon'):
        os.makedirs('resources/mon')
    if not os.path.exists('resources/mon/encounters/cvc'):
        os.makedirs('resources/mon/encounters/cvc')
    
    # Load all images
    grass_img = pygame.image.load('resources/mon/grass.png').convert_alpha()
    grass_img = pygame.transform.scale(grass_img, (150, 150))
    background_img = pygame.image.load('resources/mon/main_background.png').convert_alpha()
    background_img = pygame.transform.scale(background_img, (SCREEN_WIDTH, SCREEN_HEIGHT))
    backpack_img = pygame.image.load('resources/mon/backpack.png').convert_alpha()
    backpack_img = pygame.transform.scale(backpack_img, (60, 60))
    battle_bg_img = pygame.image.load('resources/mon/battle_background.png').convert()
    battle_bg_img = pygame.transform.scale(battle_bg_img, (SCREEN_WIDTH, SCREEN_HEIGHT))
    dictionary_img = pygame.image.load('resources/mon/dictionary.png').convert_alpha()
    dictionary_img = pygame.transform.scale(dictionary_img, (100, 100))
    inventory_bg_img = pygame.image.load('resources/mon/inventory_background.png').convert()
    inventory_bg_img = pygame.transform.scale(inventory_bg_img, (SCREEN_WIDTH, SCREEN_HEIGHT))
    ball_img = pygame.image.load('resources/mon/ball.png').convert_alpha()
    ball_img = pygame.transform.scale(ball_img, (100, 100))
    player_img = pygame.image.load('resources/mon/player.png').convert_alpha()
    player_img = pygame.transform.scale(player_img, (120, 120))
    player_img_flipped = pygame.transform.flip(player_img, True, False)
    collect_bg_img = pygame.image.load('resources/mon/collect_background.png').convert()
    collect_bg_img = pygame.transform.scale(collect_bg_img, (SCREEN_WIDTH, SCREEN_HEIGHT))
    dictionary_bg_img = pygame.image.load('resources/mon/dictionary_background.png').convert()
    dictionary_bg_img = pygame.transform.scale(dictionary_bg_img, (SCREEN_WIDTH, SCREEN_HEIGHT))
    exit_button_img = pygame.image.load('resources/mon/exit_button.png').convert_alpha()
    exit_button_img = pygame.transform.scale(exit_button_img, (60, 60))
    save_button_img = pygame.image.load('resources/mon/save_button.png').convert_alpha()
    save_button_img = pygame.transform.scale(save_button_img, (100, 100))
    
    # Environment-specific buttons
    shroom_img = pygame.image.load('resources/mon/shroom.png').convert_alpha()
    shroom_img = pygame.transform.scale(shroom_img, (grass_size, grass_size))
    ring_img = pygame.image.load('resources/mon/ring.png').convert_alpha()
    ring_img = pygame.transform.scale(ring_img, (grass_size, grass_size))
    crate_img = pygame.image.load('resources/mon/crate.png').convert_alpha()
    crate_img = pygame.transform.scale(crate_img, (grass_size, grass_size))
    cactus_img = pygame.image.load('resources/mon/cactus.png').convert_alpha()
    cactus_img = pygame.transform.scale(cactus_img, (grass_size, grass_size))
    
    # Arrow images
    arrow_img = pygame.image.load('resources/mon/arrow.png').convert_alpha()
    arrow_img = pygame.transform.scale(arrow_img, (small_btn_size, small_btn_size))
    arrow_right = pygame.transform.flip(arrow_img, True, False)
    arrow_down = pygame.transform.rotate(arrow_img, 90)
    arrow_up = pygame.transform.rotate(arrow_img, -90)
    
    # Environment backgrounds
    ocean_bg = pygame.image.load('resources/mon/ocean_background.png').convert()
    ocean_bg = pygame.transform.scale(ocean_bg, (SCREEN_WIDTH, SCREEN_HEIGHT))
    forest_bg = pygame.image.load('resources/mon/forest_background.png').convert()
    forest_bg = pygame.transform.scale(forest_bg, (SCREEN_WIDTH, SCREEN_HEIGHT))
    desert_bg = pygame.image.load('resources/mon/desert_background.png').convert()
    desert_bg = pygame.transform.scale(desert_bg, (SCREEN_WIDTH, SCREEN_HEIGHT))
    factory_bg = pygame.image.load('resources/mon/factory_background.png').convert()
    factory_bg = pygame.transform.scale(factory_bg, (SCREEN_WIDTH, SCREEN_HEIGHT))
    caught_img = pygame.image.load('resources/mon/caught.png').convert_alpha()
    caught_img = pygame.transform.scale(caught_img, (40, 40))  # Same size as other icons
    
except Exception as e:
    print(f"Error loading images: {e}")
    # Fallback colored surfaces
    grass_img = pygame.Surface((150, 150))
    grass_img.fill(GREEN)
    background_img = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    background_img.fill((0, 0, 255))
    backpack_img = pygame.Surface((60, 60))
    backpack_img.fill(RED)
    battle_bg_img = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    battle_bg_img.fill(GREEN)
    dictionary_img = pygame.Surface((100, 100))
    dictionary_img.fill(GRAY)
    inventory_bg_img = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    inventory_bg_img.fill(PURPLE)
    ball_img = pygame.Surface((100, 100))
    ball_img.fill(WHITE)
    player_img = pygame.Surface((120, 120))
    player_img.fill((200, 100, 100))
    player_img_flipped = pygame.transform.flip(player_img, True, False)
    collect_bg_img = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    collect_bg_img.fill(PINK)
    dictionary_bg_img = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    dictionary_bg_img.fill(WHITE)
    exit_button_img = pygame.Surface((60, 60))
    exit_button_img.fill(ORANGE)
    save_button_img = pygame.Surface((100, 100))
    save_button_img.fill((0, 200, 0))
    arrow_img = pygame.Surface((small_btn_size, small_btn_size), pygame.SRCALPHA)
    pygame.draw.polygon(arrow_img, (0, 100, 200), [(0, small_btn_size//2), (small_btn_size, 0), (small_btn_size, small_btn_size)])
    arrow_right = pygame.transform.flip(arrow_img, True, False)
    arrow_up = pygame.transform.rotate(arrow_img, -90)
    arrow_down = pygame.transform.rotate(arrow_img, 90)
    ocean_bg = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    ocean_bg.fill((0, 100, 200))
    forest_bg = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    forest_bg.fill((0, 150, 0))
    desert_bg = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    desert_bg.fill((200, 180, 100))
    factory_bg = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    factory_bg.fill((100, 100, 100))
    shroom_img = pygame.Surface((grass_size, grass_size))
    shroom_img.fill((200, 100, 200))
    ring_img = pygame.Surface((grass_size, grass_size))
    ring_img.fill((200, 200, 0))
    crate_img = pygame.Surface((grass_size, grass_size))
    crate_img.fill((150, 75, 0))
    cactus_img = pygame.Surface((grass_size, grass_size))
    cactus_img.fill((0, 200, 0))

# Game states
STATE_MAIN = 0
STATE_ENCOUNTER = 1
STATE_INVENTORY = 2
STATE_DICTIONARY = 3
STATE_ITEM_COLLECT = 4
STATE_OCEAN = 5
STATE_FOREST = 6
STATE_DESERT = 7
STATE_FACTORY = 8
current_state = STATE_MAIN
previous_state_before_encounter = STATE_MAIN
previous_state_before_item_collect = STATE_MAIN
previous_state_before_inventory = STATE_MAIN
tts_engine = init_tts()

# Positions (main screen)
grass1_pos = (SCREEN_WIDTH // 3 - grass_size // 2, SCREEN_HEIGHT // 3 - grass_size // 2 - vertical_spacing//2)
grass2_pos = (SCREEN_WIDTH * 2 // 3 - grass_size // 2, SCREEN_HEIGHT // 3 - grass_size // 2 - vertical_spacing//2)
grass3_pos = (SCREEN_WIDTH // 3 - grass_size // 2, SCREEN_HEIGHT * 2 // 3 - grass_size // 2 + vertical_spacing//2)
grass4_pos = (SCREEN_WIDTH * 2 // 3 - grass_size // 2, SCREEN_HEIGHT * 2 // 3 - grass_size // 2 + vertical_spacing//2)
backpack_pos = (SCREEN_WIDTH - small_btn_size - 20, 20)

# Arrow positions
arrow_left_pos = (20, SCREEN_HEIGHT//2 - small_btn_size//2)
arrow_right_pos = (SCREEN_WIDTH - small_btn_size - 20, SCREEN_HEIGHT//2 - small_btn_size//2)
arrow_up_pos = (SCREEN_WIDTH//2 - small_btn_size//2, 20)
arrow_down_pos = (SCREEN_WIDTH//2 - small_btn_size//2, SCREEN_HEIGHT - small_btn_size - 20)

# Environment exit positions
ocean_exit_pos = arrow_right_pos
forest_exit_pos = arrow_left_pos
desert_exit_pos = arrow_down_pos
factory_exit_pos = arrow_up_pos

# Encounter screen positions
battle_exit_pos = (SCREEN_WIDTH - small_btn_size - 20, SCREEN_HEIGHT - small_btn_size - 20)
battle_inventory_pos = (SCREEN_WIDTH - small_btn_size*2 - 30, SCREEN_HEIGHT - small_btn_size - 20)
player_pos = (20, SCREEN_HEIGHT - 140)
encounter_img_pos = (SCREEN_WIDTH - 150 - 20, 20)
encounter_img_size = (150, 150)

# Health bars
health_bar_height = 30
health_bar_border = 2
health_bar_start_x = 20
health_bar_start_y = 20

# Option buttons
option_btn_width = 120
option_btn_height = 60
option_btn_spacing = 20
option_btn_y = SCREEN_HEIGHT // 2 + 100
option_btn_total_width = (option_btn_width * 4) + (option_btn_spacing * 3)
option_btn_start_x = (SCREEN_WIDTH - option_btn_total_width) // 2
option_btn_positions = [
    (option_btn_start_x, option_btn_y),
    (option_btn_start_x + option_btn_width + option_btn_spacing, option_btn_y),
    (option_btn_start_x + (option_btn_width + option_btn_spacing)*2, option_btn_y),
    (option_btn_start_x + (option_btn_width + option_btn_spacing)*3, option_btn_y)
]

# Inventory positions
inventory_ball_pos = (SCREEN_WIDTH // 2 - 100 // 2, SCREEN_HEIGHT // 3 - 100 // 2)
inventory_dict_pos = (SCREEN_WIDTH // 2 - 100 // 2, SCREEN_HEIGHT // 2 - 100 // 2)
inventory_save_pos = (SCREEN_WIDTH // 2 - 100 // 2, SCREEN_HEIGHT * 2 // 3 - 100 // 2)
inventory_exit_pos = (SCREEN_WIDTH - small_btn_size - 20, SCREEN_HEIGHT - small_btn_size - 20)

# Item collect
item_collect_ball_pos = (SCREEN_WIDTH // 2 - 100 // 2, SCREEN_HEIGHT // 2 - 100 // 2)

# Dictionary
dictionary_exit_pos = (SCREEN_WIDTH - small_btn_size - 20, SCREEN_HEIGHT - small_btn_size - 20)

# Fonts
large_font = pygame.font.SysFont('Arial', 36)
medium_font = pygame.font.SysFont('Arial', 24)
button_font = pygame.font.SysFont('Arial', 32, bold=True)
encounter_name_font = pygame.font.SysFont('Arial', 72, bold=True)

def generate_letter_buttons(word):
    global current_letter_buttons, current_correct_letters, current_display_name, letters_to_reveal, letters_revealed
    
    if not word:
        return []
    
    letters_revealed = 0
    # For 4+ letter words, can hide 1, 2, or 3 letters
    if len(word) >= 4:
        letters_to_reveal = random.choice([1, 2, 3])
    else:
        letters_to_reveal = random.choice([1, 2])
    
    current_correct_letters = random.sample(list(word), min(letters_to_reveal, len(word)))
    current_display_name = word
    for letter in current_correct_letters:
        current_display_name = current_display_name.replace(letter, '?', 1)
    
    letters = []
    while len(letters) < 4 - letters_to_reveal:
        random_letter = random.choice(string.ascii_lowercase)
        if random_letter not in current_correct_letters and random_letter not in letters:
            letters.append(random_letter)
    
    letters.extend(current_correct_letters)
    random.shuffle(letters)
    current_letter_buttons = letters

def update_display_name():
    """Update the displayed name with revealed letters"""
    global current_display_name
    
    # Create a list version of the display name to modify
    display_list = list(current_display_name.lower())
    original_list = list(current_encounter_name.lower())
    
    # Find and reveal only the correct letters that have been selected
    for i, (display_char, original_char) in enumerate(zip(display_list, original_list)):
        if display_char == '?' and original_char in current_letter_buttons and original_char not in current_correct_letters:
            display_list[i] = original_char
    
    current_display_name = ''.join(display_list)

def load_random_encounter_image():
    global current_encounter_image, current_encounter_name, letters_revealed
    
    try:
        if current_state == STATE_MAIN:
            folder = 'cvc'
        elif current_state == STATE_DESERT:
            folder = 'cvce'
        elif current_state == STATE_OCEAN:
            folder = 'ccvc'
        elif current_state == STATE_FOREST:
            folder = 'cvcc'
        elif current_state == STATE_FACTORY:
            folder = random.choice(['cvc', 'cvce', 'ccvc', 'cvcc'])
        
        # Get all possible encounters for this state
        possible_encounters = [k for k in preloaded_images.keys() if k[1] == current_state or 
                             (current_state == STATE_FACTORY and k[1] in [STATE_MAIN, STATE_DESERT, STATE_OCEAN, STATE_FOREST])]
        
        if possible_encounters:
            name, state = random.choice(possible_encounters)
            current_encounter_name = name
            current_encounter_image = preloaded_images[(name, state)]
            generate_letter_buttons(current_encounter_name.lower())
        else:
            raise ValueError("No preloaded encounters found")
            
    except Exception as e:
        print(f"Error loading encounter: {e}")
        current_encounter_image = pygame.Surface(encounter_img_size)
        current_encounter_image.fill((200, 150, 150))
        current_encounter_name = "error"
        generate_letter_buttons("abc")

def draw_health_bars():
    word_length = len(current_encounter_name)
    num_bars = min(word_length, 4)  # Cap at 4 bars
    if num_bars == 0:
        num_bars = 3  # Fallback
        
    total_width = 200  # Target total width
    bar_width = total_width // num_bars
    health_bar_overlap = health_bar_border
    
    # Determine how many bars to show and their colors
    if letters_to_reveal == 1:
        # Single letter hidden cases
        if letters_revealed == 0:
            # Show all green bars
            bars_to_show = num_bars
            colors = [GREEN] * num_bars
        else:
            # After revealing single letter, show one red bar
            bars_to_show = 1
            colors = [RED]
    else:
        # Multiple letters hidden cases
        if letters_revealed == 0:
            # Initial state - all green bars
            bars_to_show = num_bars
            colors = [GREEN] * num_bars
        elif letters_revealed == 1:
            # After first correct letter
            if letters_to_reveal == 2:
                # For two hidden letters, show two yellow bars
                bars_to_show = 2
                colors = [YELLOW] * bars_to_show
            elif letters_to_reveal == 3:
                # For three hidden letters, show three green bars (remove one)
                bars_to_show = 3
                colors = [GREEN] * bars_to_show
            else:
                bars_to_show = num_bars - 1
                colors = [YELLOW] * bars_to_show
        elif letters_revealed == 2:
            # After second correct letter
            if letters_to_reveal == 2:
                bars_to_show = 1
                colors = [RED]
            elif letters_to_reveal == 3:
                bars_to_show = 2
                colors = [YELLOW] * bars_to_show
            else:
                bars_to_show = 1
                colors = [RED]
        elif letters_revealed >= 3:
            # After third correct letter (only for 3+ letters_to_reveal)
            bars_to_show = 1
            colors = [RED]
    
    # Draw the bars
    for i in range(bars_to_show):
        pos = (health_bar_start_x + (bar_width - health_bar_overlap)*i, health_bar_start_y)
        pygame.draw.rect(screen, colors[i], (*pos, bar_width, health_bar_height))
        pygame.draw.rect(screen, BLACK, (*pos, bar_width, health_bar_height), health_bar_border)
        
def load_dictionary_items():
    global dictionary_items
    dictionary_items = []
    
    # Define the encounter folders to scan
    encounter_folders = [
        'resources/mon/encounters/cvc',
        'resources/mon/encounters/cvce',
        'resources/mon/encounters/ccvc',
        'resources/mon/encounters/cvcc'
    ]
    
    # Load all image files from all encounter folders
    for folder in encounter_folders:
        try:
            if os.path.exists(folder):
                for file in os.listdir(folder):
                    if file.lower().endswith(('.png', '.jpg', '.jpeg')):
                        name = os.path.splitext(file)[0]
                        dictionary_items.append({
                            'name': name,
                            'image_path': 'resources/mon/missing.png',  # Default to missing image
                            'caught': False  # For future catching functionality
                        })
        except Exception as e:
            print(f"Error loading dictionary items from {folder}: {e}")
    
    # Sort alphabetically
    dictionary_items.sort(key=lambda x: x['name'])

def save_game():
    save_data = {
        'ball_count': ball_count,
        'caught_words': [item['name'] for item in dictionary_items if item['caught']]
    }
    
    try:
        with open(SAVE_FILE, 'wb') as f:
            pickle.dump(save_data, f)
        print("Game saved successfully!")
    except Exception as e:
        print(f"Error saving game: {e}")
        
def load_game():
    global ball_count
    
    if not os.path.exists(SAVE_FILE):
        print("No save file found, starting fresh")
        return
    
    try:
        with open(SAVE_FILE, 'rb') as f:
            save_data = pickle.load(f)
        
        # Update ball count
        ball_count = save_data.get('ball_count', 0)
        
        # Update caught status in dictionary
        caught_words = save_data.get('caught_words', [])
        for word in caught_words:
            for item in dictionary_items:
                if item['name'].lower() == word.lower():
                    item['caught'] = True
                    # Update image path to the actual image
                    if current_state == STATE_MAIN:
                        folder = 'cvc'
                    elif current_state == STATE_DESERT:
                        folder = 'cvce'
                    elif current_state == STATE_OCEAN:
                        folder = 'ccvc'
                    elif current_state == STATE_FOREST:
                        folder = 'cvcc'
                    elif current_state == STATE_FACTORY:
                        for possible_folder in ['cvc', 'cvce', 'ccvc', 'cvcc']:
                            path = f'resources/mon/encounters/{possible_folder}/{word.lower()}.png'
                            if os.path.exists(path):
                                folder = possible_folder
                                break
                    item['image_path'] = f'resources/mon/encounters/{folder}/{word.lower()}.png'
                    break
                    
        print("Game loaded successfully!")
    except Exception as e:
        print(f"Error loading save file: {e}")

def draw_main_screen():
    screen.blit(background_img, (0, 0))
    screen.blit(arrow_img, arrow_left_pos)
    screen.blit(arrow_right, arrow_right_pos)
    screen.blit(arrow_up, arrow_up_pos)
    screen.blit(arrow_down, arrow_down_pos)
    screen.blit(grass_img, grass1_pos)
    screen.blit(grass_img, grass2_pos)
    screen.blit(grass_img, grass3_pos)
    screen.blit(grass_img, grass4_pos)
    screen.blit(backpack_img, backpack_pos)

def draw_encounter_screen():
    screen.blit(battle_bg_img, (0, 0))
    draw_health_bars()
    screen.blit(player_img_flipped, player_pos)
    
    if current_encounter_image:
        screen.blit(current_encounter_image, encounter_img_pos)
    
    # Use the larger font for the name display
    name_text = encounter_name_font.render(current_display_name, True, BLACK)
    name_rect = name_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 - 50))
    screen.blit(name_text, name_rect)
    
    for i, pos in enumerate(option_btn_positions[:4]):
        if i < len(current_letter_buttons):
            pygame.draw.rect(screen, NAVY_BLUE, (*pos, option_btn_width, option_btn_height))
            letter_text = button_font.render(current_letter_buttons[i].upper(), True, WHITE)
            letter_rect = letter_text.get_rect(center=(pos[0] + option_btn_width//2, pos[1] + option_btn_height//2))
            screen.blit(letter_text, letter_rect)
    
    screen.blit(exit_button_img, battle_exit_pos)
    screen.blit(backpack_img, battle_inventory_pos)
    
def draw_ocean_screen():
    screen.blit(ocean_bg, (0, 0))
    screen.blit(ring_img, grass1_pos)
    screen.blit(ring_img, grass2_pos)
    screen.blit(ring_img, grass3_pos)
    screen.blit(ring_img, grass4_pos)
    screen.blit(backpack_img, backpack_pos)
    screen.blit(arrow_right, ocean_exit_pos)

def draw_forest_screen():
    screen.blit(forest_bg, (0, 0))
    screen.blit(shroom_img, grass1_pos)
    screen.blit(shroom_img, grass2_pos)
    screen.blit(shroom_img, grass3_pos)
    screen.blit(shroom_img, grass4_pos)
    screen.blit(backpack_img, backpack_pos)
    screen.blit(arrow_img, forest_exit_pos)

def draw_desert_screen():
    screen.blit(desert_bg, (0, 0))
    screen.blit(cactus_img, grass1_pos)
    screen.blit(cactus_img, grass2_pos)
    screen.blit(cactus_img, grass3_pos)
    screen.blit(cactus_img, grass4_pos)
    screen.blit(backpack_img, backpack_pos)
    screen.blit(arrow_down, desert_exit_pos)

def draw_factory_screen():
    screen.blit(factory_bg, (0, 0))
    screen.blit(crate_img, grass1_pos)
    screen.blit(crate_img, grass2_pos)
    screen.blit(crate_img, grass3_pos)
    screen.blit(crate_img, grass4_pos)
    screen.blit(backpack_img, backpack_pos)
    screen.blit(arrow_up, factory_exit_pos)
    
def draw_inventory_screen():
    screen.blit(inventory_bg_img, (0, 0))
    screen.blit(ball_img, inventory_ball_pos)
    count_text = large_font.render(f"x {ball_count}", True, WHITE)
    screen.blit(count_text, (inventory_ball_pos[0] + 110, inventory_ball_pos[1] + 30))
    screen.blit(dictionary_img, inventory_dict_pos)
    screen.blit(save_button_img, inventory_save_pos)
    screen.blit(exit_button_img, inventory_exit_pos)

def draw_dictionary_screen():
    global dictionary_scroll_offset
    
    screen.blit(dictionary_bg_img, (0, 0))
    screen.blit(exit_button_img, dictionary_exit_pos)
    
    # Calculate visible area
    visible_top = 100
    visible_bottom = SCREEN_HEIGHT - 50
    visible_height = visible_bottom - visible_top
    total_height = len(dictionary_items) * dictionary_item_height
    
    # Draw title
    title_text = large_font.render("Dictionary", True, BLACK)
    screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, 50))
    
    # Draw scrollbar background
    scrollbar_bg = pygame.Surface((SCROLLBAR_WIDTH, visible_height), pygame.SRCALPHA)
    pygame.draw.rect(scrollbar_bg, (0, 0, 0, 30), (0, 0, SCROLLBAR_WIDTH, visible_height), border_radius=5)
    screen.blit(scrollbar_bg, (5, visible_top))
    
    # Calculate scrollbar thumb position and size
    if total_height > visible_height:
        scrollbar_ratio = visible_height / total_height
        scrollbar_height = max(20, int(visible_height * scrollbar_ratio))
        scrollbar_pos_ratio = dictionary_scroll_offset / (total_height - visible_height)
        scrollbar_y = visible_top + int((visible_height - scrollbar_height) * scrollbar_pos_ratio)
        
        # Draw scrollbar thumb
        scrollbar_thumb = pygame.Surface((SCROLLBAR_WIDTH, scrollbar_height), pygame.SRCALPHA)
        pygame.draw.rect(scrollbar_thumb, SCROLLBAR_COLOR, (0, 0, SCROLLBAR_WIDTH, scrollbar_height), border_radius=5)
        screen.blit(scrollbar_thumb, (5, scrollbar_y))
    
    # Try to load missing.png once at the start
    try:
        missing_icon = pygame.image.load('resources/mon/missing.png').convert_alpha()
        missing_icon = pygame.transform.scale(missing_icon, (40, 40))
    except:
        missing_icon = pygame.Surface((40, 40))
        missing_icon.fill(GRAY)
    
    # Draw each dictionary item
    for i, item in enumerate(dictionary_items):
        item_y = visible_top + (i * dictionary_item_height) - dictionary_scroll_offset
        
        # Only draw if within visible area
        if item_y + dictionary_item_height >= visible_top and item_y <= visible_bottom:
            # Draw number (shifted right by scrollbar width)
            num_text = medium_font.render(f"{i+1}.", True, BLACK)
            screen.blit(num_text, (40 - num_text.get_width() + SCROLLBAR_WIDTH + 5, item_y))
            
            # Draw the word's image if caught, otherwise missing.png
            if item['caught']:
                # Find the preloaded image for this word
                img = None
                for state in [STATE_MAIN, STATE_DESERT, STATE_OCEAN, STATE_FOREST]:
                    if (item['name'].lower(), state) in preloaded_images:
                        img = preloaded_images[(item['name'].lower(), state)]
                        break
                
                if img is None:
                    # Fallback if not found in preloaded images
                    try:
                        img = pygame.image.load(item['image_path']).convert_alpha()
                    except:
                        img = pygame.Surface((40, 40))
                        img.fill(GRAY)
            else:
                # Not caught - show missing.png
                img = missing_icon
            
            # Scale the image to 40x40
            img = pygame.transform.scale(img, (40, 40))
            screen.blit(img, (50 + SCROLLBAR_WIDTH + 5, item_y))
            
            # Draw the name (green if caught, black ?'s if not)
            if item['caught']:
                name_text = medium_font.render(item['name'], True, GREEN)
                # Draw caught icon after the name
                caught_icon = pygame.transform.scale(caught_img, (40, 40))
                screen.blit(caught_icon, (50 + SCROLLBAR_WIDTH + 5 + 40 + 10 + name_text.get_width(), item_y))
            else:
                name_text = medium_font.render("?" * len(item['name']), True, BLACK)

            # Draw the name text
            screen.blit(name_text, (100 + SCROLLBAR_WIDTH + 5, item_y))
            
def draw_item_collect_screen():
    screen.blit(collect_bg_img, (0, 0))
    screen.blit(ball_img, item_collect_ball_pos)
    if item_collect_amount > 0:
        amount_text = large_font.render(f"x {item_collect_amount}", True, WHITE)
        screen.blit(amount_text, (item_collect_ball_pos[0] + 110, item_collect_ball_pos[1] + 30))

def check_click(pos, rect_pos, width, height):
    x, y = pos
    rx, ry = rect_pos
    return rx <= x <= rx + width and ry <= y <= ry + height
    
def show_loading_screen(progress=0, message="Loading..."):
    """Show loading screen with progress bar"""
    screen.fill(BLACK)
    
    # Loading text
    loading_text = large_font.render(message, True, WHITE)
    screen.blit(loading_text, (SCREEN_WIDTH//2 - loading_text.get_width()//2, 
                              SCREEN_HEIGHT//2 - loading_text.get_height()//2 - 30))
    
    # Progress bar background
    bar_width = 400
    bar_height = 30
    bar_x = SCREEN_WIDTH//2 - bar_width//2
    bar_y = SCREEN_HEIGHT//2 + 10
    pygame.draw.rect(screen, (50, 50, 50), (bar_x, bar_y, bar_width, bar_height))
    
    # Progress bar fill
    fill_width = int(bar_width * progress)
    pygame.draw.rect(screen, WHITE, (bar_x, bar_y, fill_width, bar_height))
    
    pygame.display.flip()

def preload_resources():
    """Preload all game resources with progress updates"""
    global preloaded_images
    
    # Initialize empty dictionary for preloaded images
    preloaded_images = {}
    
    # Show initial loading screen
    show_loading_screen(0, "Initializing...")
    
    # Create required directories if they don't exist
    required_dirs = [
        'resources',
        'resources/mon',
        'resources/mon/encounters/cvc',
        'resources/mon/encounters/cvce',
        'resources/mon/encounters/ccvc',
        'resources/mon/encounters/cvcc'
    ]
    
    for i, dir_path in enumerate(required_dirs):
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)
        show_loading_screen(i/len(required_dirs), "Creating directories...")
    
    # Define what to preload
    encounter_folders = [
        ('cvc', STATE_MAIN),
        ('cvce', STATE_DESERT),
        ('ccvc', STATE_OCEAN),
        ('cvcc', STATE_FOREST)
    ]
    
    total_images = 0
    loaded_images = 0
    
    # First count all images to get total for progress bar
    for folder, state in encounter_folders:
        folder_path = f'resources/mon/encounters/{folder}'
        if os.path.exists(folder_path):
            total_images += len([f for f in os.listdir(folder_path) 
                               if f.lower().endswith(('.png', '.jpg', '.jpeg'))])
    
    # Now actually load the images
    for folder, state in encounter_folders:
        try:
            folder_path = f'resources/mon/encounters/{folder}'
            if os.path.exists(folder_path):
                for file in os.listdir(folder_path):
                    if file.lower().endswith(('.png', '.jpg', '.jpeg')):
                        name = os.path.splitext(file)[0]
                        img_path = os.path.join(folder_path, file)
                        
                        # Update loading screen
                        loaded_images += 1
                        progress = loaded_images / total_images if total_images > 0 else 0
                        show_loading_screen(progress, f"Loading {folder} images...")
                        
                        # Load and scale the image
                        try:
                            img = pygame.image.load(img_path).convert_alpha()
                            img = pygame.transform.scale(img, encounter_img_size)
                            preloaded_images[(name.lower(), state)] = img
                        except Exception as e:
                            print(f"Error loading {img_path}: {e}")
                            # Create fallback image
                            fallback = pygame.Surface(encounter_img_size)
                            fallback.fill((200, 150, 150))
                            preloaded_images[(name.lower(), state)] = fallback
                            
                        # Process events to keep window responsive
                        pygame.event.pump()
        except Exception as e:
            print(f"Error preloading {folder} images: {e}")

# Show loading screen before starting to load
show_loading_screen(0, "Starting...")

# Now preload all resources
preload_resources()

# Load initial random encounter image
load_random_encounter_image()
load_dictionary_items()
load_game()

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            if current_state == STATE_MAIN:
                if (check_click(event.pos, grass1_pos, grass_size, grass_size) or 
                    check_click(event.pos, grass2_pos, grass_size, grass_size) or
                    check_click(event.pos, grass3_pos, grass_size, grass_size) or
                    check_click(event.pos, grass4_pos, grass_size, grass_size)):
                    if random.random() < 0.75:
                        previous_state_before_encounter = current_state
                        load_random_encounter_image()
                        current_state = STATE_ENCOUNTER
                    else:
                        previous_state_before_item_collect = current_state
                        rand = random.random()
                        if rand < 0.7:
                            item_collect_amount = 5
                        elif rand < 0.875:
                            item_collect_amount = 10
                        else:
                            item_collect_amount = 25
                        current_state = STATE_ITEM_COLLECT
                 
                elif check_click(event.pos, arrow_left_pos, small_btn_size, small_btn_size):
                    current_state = STATE_OCEAN
                elif check_click(event.pos, arrow_right_pos, small_btn_size, small_btn_size):
                    current_state = STATE_FOREST
                elif check_click(event.pos, arrow_up_pos, small_btn_size, small_btn_size):
                    current_state = STATE_DESERT
                elif check_click(event.pos, arrow_down_pos, small_btn_size, small_btn_size):
                    current_state = STATE_FACTORY        
                        
                elif check_click(event.pos, backpack_pos, small_btn_size, small_btn_size):
                    previous_state_before_inventory = current_state
                    current_state = STATE_INVENTORY
            
            elif current_state == STATE_ENCOUNTER:
                if check_click(event.pos, battle_exit_pos, small_btn_size, small_btn_size):
                    current_state = previous_state_before_encounter
                elif check_click(event.pos, battle_inventory_pos, small_btn_size, small_btn_size):
                    previous_state_before_inventory = current_state
                    current_state = STATE_INVENTORY
                elif (current_encounter_image and 
                      check_click(event.pos, encounter_img_pos, *encounter_img_size)):
                    if tts_engine and current_encounter_name:
                        try:
                            tts_engine.say(current_encounter_name)
                            tts_engine.runAndWait()
                        except Exception as e:
                            print(f"Error with text-to-speech: {e}")
                for i, pos in enumerate(option_btn_positions[:4]):
                    if i < len(current_letter_buttons) and check_click(event.pos, pos, option_btn_width, option_btn_height):
                        if current_letter_buttons[i] in current_correct_letters:
                            print(f"Correct letter selected: {current_letter_buttons[i]}")
                            letters_revealed += 1
                            current_correct_letters.remove(current_letter_buttons[i])
                            update_display_name()  # Update display immediately after correct selection
                        else:
                            print(f"Incorrect letter selected: {current_letter_buttons[i]}")
            
            elif current_state == STATE_INVENTORY:
                if check_click(event.pos, inventory_exit_pos, small_btn_size, small_btn_size):
                    current_state = previous_state_before_inventory
                elif check_click(event.pos, inventory_dict_pos, 100, 100):
                    current_state = STATE_DICTIONARY
                elif check_click(event.pos, inventory_save_pos, 100, 100):
                    save_game()
                elif (check_click(event.pos, inventory_ball_pos, 100, 100) and 
                      previous_state_before_inventory == STATE_ENCOUNTER and 
                      ball_count > 0):
                    # Determine catch probability based on health bars
                    catch_probability = 0.01  # Default for green (1%)
                    
                    if letters_revealed >= letters_to_reveal:  # All letters revealed (red)
                        catch_probability = 0.95
                    elif letters_revealed > 0:  # Some letters revealed (yellow)
                        catch_probability = 0.5
                    
                    # Always consume a ball
                    ball_count -= 1
                    
                    if random.random() < catch_probability:
                        # Successful catch - return to environment
                        try:
                            # Determine the correct folder
                            folder = None
                            if previous_state_before_encounter == STATE_MAIN:
                                folder = 'cvc'
                            elif previous_state_before_encounter == STATE_DESERT:
                                folder = 'cvce'
                            elif previous_state_before_encounter == STATE_OCEAN:
                                folder = 'ccvc'
                            elif previous_state_before_encounter == STATE_FOREST:
                                folder = 'cvcc'
                            elif previous_state_before_encounter == STATE_FACTORY:
                                # For factory, search all folders
                                for possible_folder in ['cvc', 'cvce', 'ccvc', 'cvcc']:
                                    test_path = f'resources/mon/encounters/{possible_folder}/{current_encounter_name.lower()}.png'
                                    if os.path.exists(test_path):
                                        folder = possible_folder
                                        break
                            
                            if folder is None:
                                raise ValueError(f"Couldn't determine folder for {current_encounter_name}")
                            
                            image_path = f'resources/mon/encounters/{folder}/{current_encounter_name.lower()}.png'
                            
                            # Verify the image exists
                            if not os.path.exists(image_path):
                                raise FileNotFoundError(f"Image not found at {image_path}")
                            
                            # Update dictionary entry
                            for i, item in enumerate(dictionary_items):
                                if item['name'].lower() == current_encounter_name.lower():
                                    dictionary_items[i]['image_path'] = image_path
                                    dictionary_items[i]['caught'] = True
                                    print(f"Caught {current_encounter_name}! Updated dictionary with image: {image_path}")
                                    break
                            
                            # Return to original environment after successful catch
                            current_state = previous_state_before_encounter
                            
                        except Exception as e:
                            print(f"Error updating dictionary: {e}")
                            # Fallback - stay in encounter if we had any errors
                            current_state = STATE_ENCOUNTER
                    else:
                        # Failed catch - stay in encounter
                        current_state = STATE_ENCOUNTER            
            if current_state == STATE_DICTIONARY:
                # Calculate visible area
                visible_top = 100
                visible_bottom = SCREEN_HEIGHT - 50
                visible_height = visible_bottom - visible_top
                
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if check_click(event.pos, dictionary_exit_pos, small_btn_size, small_btn_size):
                        current_state = STATE_INVENTORY
                    else:
                        # Check if click is on scrollbar
                        if 5 <= event.pos[0] <= 5 + SCROLLBAR_WIDTH and visible_top <= event.pos[1] <= visible_bottom:
                            dictionary_scroll_dragging = True
                            # Jump to clicked position
                            total_height = len(dictionary_items) * dictionary_item_height
                            visible_height = (SCREEN_HEIGHT - 50) - 100
                            if total_height > visible_height:
                                click_y = event.pos[1] - visible_top
                                scroll_ratio = click_y / visible_height
                                dictionary_scroll_offset = scroll_ratio * (total_height - visible_height)
                        else:
                            dictionary_drag_start_y = event.pos[1]
                            dictionary_scroll_start_offset = dictionary_scroll_offset
                
                elif event.type == pygame.MOUSEBUTTONUP:
                    dictionary_drag_start_y = None
                    dictionary_scroll_dragging = False
                
                elif event.type == pygame.MOUSEMOTION:
                    if dictionary_scroll_dragging:
                        # Scrollbar dragging
                        total_height = len(dictionary_items) * dictionary_item_height
                        visible_height = (SCREEN_HEIGHT - 50) - 100
                        if total_height > visible_height:
                            mouse_y = max(visible_top, min(event.pos[1], visible_bottom))
                            scroll_ratio = (mouse_y - visible_top) / visible_height
                            dictionary_scroll_offset = scroll_ratio * (total_height - visible_height)
                    elif dictionary_drag_start_y is not None:
                        # Regular content dragging
                        drag_distance = dictionary_drag_start_y - event.pos[1]
                        dictionary_scroll_offset = dictionary_scroll_start_offset + drag_distance
                        
                        # Clamp scroll offset
                        total_height = len(dictionary_items) * dictionary_item_height
                        max_scroll = max(0, total_height - visible_height)
                        dictionary_scroll_offset = max(0, min(dictionary_scroll_offset, max_scroll))
                
                elif event.type == pygame.MOUSEWHEEL:
                    scroll_amount = event.y * 20
                    dictionary_scroll_offset -= scroll_amount
                    
                    # Clamp scroll offset
                    total_height = len(dictionary_items) * dictionary_item_height
                    visible_height = (SCREEN_HEIGHT - 50) - 100
                    max_scroll = max(0, total_height - visible_height)
                    dictionary_scroll_offset = max(0, min(dictionary_scroll_offset, max_scroll))
                    
            elif current_state == STATE_ITEM_COLLECT:
                if check_click(event.pos, item_collect_ball_pos, 100, 100):
                    ball_count += item_collect_amount
                    current_state = previous_state_before_item_collect
            
            elif current_state in [STATE_OCEAN, STATE_FOREST, STATE_DESERT, STATE_FACTORY]:
                if (check_click(event.pos, grass1_pos, grass_size, grass_size) or 
                    check_click(event.pos, grass2_pos, grass_size, grass_size) or
                    check_click(event.pos, grass3_pos, grass_size, grass_size) or
                    check_click(event.pos, grass4_pos, grass_size, grass_size)):
                    if random.random() < 0.75:
                        previous_state_before_encounter = current_state
                        load_random_encounter_image()
                        current_state = STATE_ENCOUNTER
                    else:
                        previous_state_before_item_collect = current_state
                        rand = random.random()
                        if rand < 0.7:
                            item_collect_amount = 5
                        elif rand < 0.875:
                            item_collect_amount = 10
                        else:
                            item_collect_amount = 25
                        current_state = STATE_ITEM_COLLECT
                
                elif check_click(event.pos, backpack_pos, small_btn_size, small_btn_size):
                    previous_state_before_inventory = current_state
                    current_state = STATE_INVENTORY
                
                elif current_state == STATE_OCEAN and check_click(event.pos, ocean_exit_pos, small_btn_size, small_btn_size):
                    current_state = STATE_MAIN
                elif current_state == STATE_FOREST and check_click(event.pos, forest_exit_pos, small_btn_size, small_btn_size):
                    current_state = STATE_MAIN
                elif current_state == STATE_DESERT and check_click(event.pos, desert_exit_pos, small_btn_size, small_btn_size):
                    current_state = STATE_MAIN
                elif current_state == STATE_FACTORY and check_click(event.pos, factory_exit_pos, small_btn_size, small_btn_size):
                    current_state = STATE_MAIN
    
    # Draw the appropriate screen
    if current_state == STATE_MAIN:
        draw_main_screen()
    elif current_state == STATE_ENCOUNTER:
        draw_encounter_screen()
    elif current_state == STATE_INVENTORY:
        draw_inventory_screen()
    elif current_state == STATE_DICTIONARY:
        draw_dictionary_screen()
    elif current_state == STATE_ITEM_COLLECT:
        draw_item_collect_screen()
    elif current_state == STATE_OCEAN:
        draw_ocean_screen()
    elif current_state == STATE_FOREST:
        draw_forest_screen()
    elif current_state == STATE_DESERT:
        draw_desert_screen()
    elif current_state == STATE_FACTORY:
        draw_factory_screen()
    
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()