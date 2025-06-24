import os
import sys
import pygame
import random

# Resource path handler for PyInstaller
def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

# Initialize pygame
pygame.init()
pygame.display.set_caption('Alphabet Blaster v.1.5')

# Load icon using resource_path
try:
    icon_path = resource_path(os.path.join('resources', 'icon', 'apple.png'))
    Icon = pygame.image.load(icon_path)
    pygame.display.set_icon(Icon)
except Exception as e:
    print(f"Couldn't load icon: {e}")

# Initialize font and screen
pygame.font.init()
screen_width, screen_height = 1280, 720
screen = pygame.display.set_mode((screen_width, screen_height), pygame.RESIZABLE)
clock = pygame.time.Clock()
running = True

# Font setup
game_font_size = int(0.2 * pygame.display.Info().current_h)
game_font = pygame.font.SysFont('Comic Sans MS', game_font_size)

# Colors and buttons
color = (255, 255, 255)
color_light = (170, 170, 170)
color_dark = (100, 100, 100)
background = (115, 150, 190)

# Initial dimensions
width, height = screen.get_width(), screen.get_height()
old_width, old_height = width, height

# Button properties (x, y, width, height, active_color, inactive_color)
buttons = [
    (width * 0.75, height * 0.75, 140, 40, color_light, color_dark),  # Blast
    (width * 0.10, height * 0.75, 140, 40, color_light, color_dark),  # Reveal
    (width * 0.9, height * 0.05, 40, 40, (170, 0, 230), (190, 0, 250)),  # Case Change
    (width * 0.05, height * 0.05, 40, 40, (50, 230, 50), (60, 250, 60)),  # Difficulty 1
    (width * 0.05 + 40, height * 0.05, 40, 40, (215, 235, 50), (230, 250, 60)),  # Difficulty 2
    (width * 0.05 + 80, height * 0.05, 40, 40, (235, 145, 50), (250, 160, 60)),  # Difficulty 3
    (width * 0.05 + 120, height * 0.05, 40, 40, (230, 50, 50), (250, 60, 60)),  # Difficulty 4
]

# Font setup
smallfont = pygame.font.SysFont('Corbel', 35)
text = smallfont.render('Blast!', True, color)
answer_text = smallfont.render('Reveal', True, color)

# Game functions
def lettergen(case):
    alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 
                'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
    if case == 1:
        alphabet = [letter.upper() for letter in alphabet]        
    rand_letters = random.randint(0, 20)
    return alphabet[rand_letters:rand_letters+6]

def engine(engine_letter, difficulty):
    while difficulty > 0:
        setter = random.randint(0, 5)
        if engine_letter[setter] == '?':
            difficulty += 1
        engine_letter[setter] = '?'
        difficulty -= 1
    return engine_letter

# Game state
hide_toggle = 0
letter_case = 0
set_difficulty = 3    
letter_game = lettergen(letter_case)
hidden_letter_game = letter_game.copy()
engine(letter_game, set_difficulty)

# Main game loop
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
        if event.type == pygame.VIDEORESIZE:
            # Handle window resizing
            width, height = event.w, event.h
            screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)
            game_font_size = int(0.2 * height)
            game_font = pygame.font.SysFont('Comic Sans MS', game_font_size)
            smallfont = pygame.font.SysFont('Corbel', int(0.05 * height))
            text = smallfont.render('Blast!', True, color)
            answer_text = smallfont.render('Reveal', True, color)
            
            # Update button positions
            for i, button in enumerate(buttons):
                x, y, w, h, _, _ = button
                buttons[i] = (
                    width * x / old_width,
                    height * y / old_height,
                    width * w / old_width,
                    height * h / old_height,
                    button[4],
                    button[5],
                )
            old_width, old_height = width, height
            
        if event.type == pygame.MOUSEBUTTONDOWN:          
            mouse = pygame.mouse.get_pos()
            for i, button in enumerate(buttons):
                btn_x, btn_y, btn_w, btn_h, _, _ = button
                if btn_x <= mouse[0] <= btn_x + btn_w and btn_y <= mouse[1] <= btn_y + btn_h:
                    if buttons[i][5] == color_dark:  
                        if i == 0:  # Blast button
                            letter_game = lettergen(letter_case)
                            hidden_letter_game = letter_game.copy()
                            engine(letter_game, set_difficulty)
                            hide_toggle = 0
                        elif i == 1:  # Reveal button
                            hide_toggle = 1 - hide_toggle
                    elif buttons[i][5] == (190, 0, 250):  # Case Change
                        letter_case = 1 - letter_case
                    elif buttons[i][5] == (60, 250, 60):  # Difficulty 1
                        set_difficulty = 1
                    elif buttons[i][5] == (230, 250, 60):  # Difficulty 2
                        set_difficulty = 2
                    elif buttons[i][5] == (250, 160, 60):  # Difficulty 3
                        set_difficulty = 3
                    elif buttons[i][5] == (250, 60, 60):  # Difficulty 4
                        set_difficulty = 5
                 
    # Render game
    screen.fill(background)
    mouse = pygame.mouse.get_pos()
      
    # Draw buttons
    for btn in buttons:
        x, y, w, h, active_color, inactive_color = btn
        if x <= mouse[0] <= x + w and y <= mouse[1] <= y + h:
            pygame.draw.rect(screen, active_color, [x, y, w, h])
        else:
            pygame.draw.rect(screen, inactive_color, [x, y, w, h])
        
    # Draw button text
    screen.blit(text, (width * 0.75 + 32, height * 0.75 + 5))
    screen.blit(answer_text, (width * 0.10 + 29, height * 0.75 + 5))
    
    # Draw letters
    current_letters = hidden_letter_game if hide_toggle else letter_game
    text_surface = game_font.render(
        ' '.join(current_letters), 
        False, 
        (229, 229, 19)
    )
    screen.blit(text_surface, (width/5, height/3))
    
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()