import pygame
import os
import random
import string
import pyttsx3
import sys

# Build EXE command: 
#pyinstaller --clean --onefile --icon=resources/icon/star.ico 
#--add-data "resources/icon/star.ico;icon" 
#--add-data "resources/icon/star.jpg;icon" 
#--add-data "resources/star/wrong_sound.mp3;resources/star" 
#--add-data "resources/star/hooray_sound.mp3;resources/star" 
#--noconsole star_cvc.py

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

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

# Initialize Pygame
pygame.init()
pygame.mixer.init()
pygame.display.set_caption('Star CVC v.2.2')
clock = pygame.time.Clock()
tts_engine = init_tts()

# Load icon
try:
    icon_path = resource_path(os.path.join('resources', 'icon', 'star.jpg'))
    Icon = pygame.image.load(icon_path)
    pygame.display.set_icon(Icon)
except Exception as e:
    print(f"Couldn't load icon: {e}")

# Set up display
screen_width = 1280
screen_height = 720
screen = pygame.display.set_mode((screen_width, screen_height), pygame.RESIZABLE)

# Dynamic resource location
def get_resource_base():
    if getattr(sys, 'frozen', False):
        return os.path.dirname(sys.executable)
    return os.path.dirname(os.path.abspath(__file__))

def get_phonics_folder():
    base_path = get_resource_base()
    possible_paths = [
        os.path.join(base_path, "resources", "star", "families"),
        os.path.join(base_path, "families"),
    ]
    for path in possible_paths:
        if os.path.exists(path):
            return path
    return None

phonics_words_folder = get_phonics_folder()

if phonics_words_folder is None:
    print("Warning: Could not find phonics words folder")
    folder_names = []
else:
    try:
        folder_names = [name for name in os.listdir(phonics_words_folder) 
                       if os.path.isdir(os.path.join(phonics_words_folder, name))]
    except Exception as e:
        print(f"Error reading phonics folders: {e}")
        folder_names = []

# Game state variables
index = 0
selected_folder_name = folder_names[index] if folder_names else "No folders found"
selected_subfolder_path = os.path.join(phonics_words_folder, selected_folder_name) if folder_names else ""
image = None
image_first_letter = ""
current_word = ""  # Track the complete word
hidden_word = ""    # Track the word with hidden letters
revealed = False    # Track if word is fully revealed

# Load sounds
try:
    wrong_sound = pygame.mixer.Sound(resource_path(os.path.join('resources', 'star', 'wrong_sound.mp3')))
    hooray_sound = pygame.mixer.Sound(resource_path(os.path.join('resources', 'star', 'hooray_sound.mp3')))
except Exception as e:
    print(f"Couldn't load sound files: {e}")
    wrong_sound = None
    hooray_sound = None

# Colors and font
white = (162, 228, 184)
black = (0, 0, 0)
red = (255, 0, 0)
green = (0, 255, 0)
gray_blue = (173, 216, 230)
game_font_size = int(0.26 * pygame.display.Info().current_h)
font = pygame.font.Font(None, game_font_size)

# UI positions
text_y_percent = 0.64
image_y_percent = 0.3
button_y_percent = 0.8
button_width_percent = 0.15
button_height_percent = 0.08

class Button:
    def __init__(self, x, y, text, color=gray_blue):
        self.rect = pygame.Rect(x, y, 
                               screen_width * button_width_percent, 
                               screen_height * button_height_percent)
        self.text = text
        self.color = color
    
    def draw(self):
        pygame.draw.rect(screen, self.color, self.rect)
        btn_font = pygame.font.Font(None, int(game_font_size * 0.3))
        text_surface = btn_font.render(self.text, True, black)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

def generate_random_consonant(exclude_letter, used_letters):
    """Generate a random consonant that hasn't been used yet"""
    consonants = [c for c in string.ascii_uppercase 
                 if c not in 'AEIOU' 
                 and c != exclude_letter
                 and c not in used_letters]
    return random.choice(consonants) if consonants else 'B'  # Fallback

def load_random_image():
    global image, image_first_letter, current_word, hidden_word, revealed
    try:
        image_filenames = [name for name in os.listdir(selected_subfolder_path) 
                          if name.lower().endswith(('.png', '.jpg', '.jpeg', '.gif'))]
        if image_filenames:
            selected_image_filename = random.choice(image_filenames)
            current_word = os.path.splitext(selected_image_filename)[0]  # Store the complete word
            hidden_word = current_word[1:]  # Hide first letter by default
            revealed = False
            
            image_path = os.path.join(selected_subfolder_path, selected_image_filename)
            original_image = pygame.image.load(image_path)
            max_image_size = int(min(screen_width * 0.6, screen_height * 0.5))
            image = pygame.transform.scale(original_image, (max_image_size, max_image_size))
            image_first_letter = selected_image_filename[0].upper()
            return selected_image_filename
    except Exception as e:
        print(f"Couldn't load image: {e}")
    return ""

def create_consonant_buttons():
    buttons = []
    button_spacing = (screen_width - 4 * (screen_width * button_width_percent)) / 5
    used_letters = []  # Track which letters we've already used
    
    # Generate 3 unique random letters (excluding the correct one)
    for _ in range(3):
        new_letter = generate_random_consonant(image_first_letter, used_letters)
        used_letters.append(new_letter)
    
    # Add the correct letter to our pool
    used_letters.append(image_first_letter)
    
    # Randomize the order
    random.shuffle(used_letters)
    
    # Create buttons with all letters
    for i in range(4):
        x = button_spacing * (i + 1) + (screen_width * button_width_percent) * i
        y = screen_height * button_y_percent - (screen_height * button_height_percent) / 2
        buttons.append(Button(x, y, used_letters[i]))
    
    # Find which button has the correct answer
    correct_button_index = used_letters.index(image_first_letter)
    
    return buttons, correct_button_index

def update_folder(index):
    global selected_folder_name, selected_subfolder_path, image_first_letter, image
    selected_folder_name = folder_names[index]
    selected_subfolder_path = os.path.join(phonics_words_folder, selected_folder_name)
    load_random_image()
    return create_consonant_buttons()

# Initialize game
selected_image_filename = load_random_image()
random_consonant_buttons, random_button_index = create_consonant_buttons()

# Navigation buttons
prev_button = Button(screen_width * 0.05, screen_height * 0.1, "<", color=(200, 200, 200))
next_button = Button(screen_width * 0.15, screen_height * 0.1, ">", color=(200, 200, 200))

# Replace your current next_image_button initialization with:
def create_next_button():
    return Button(
        screen_width - (screen_width * button_width_percent) - 20,
        screen_height - (screen_height * button_height_percent) - 20,
        "Next"
    )

# Initialize it
next_image_button = create_next_button()

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            
            if image and image.get_rect(topleft=(screen_width / 2 - image.get_width() / 2, 
                                               screen_height * image_y_percent - image.get_height() / 2)).collidepoint(mouse_pos):
                if tts_engine:
                    try:
                        tts_engine.say(current_word)
                        tts_engine.runAndWait()
                    except Exception as e:
                        print(f"Error with text-to-speech: {e}")
            
            elif prev_button.rect.collidepoint(mouse_pos) and index > 0:
                index -= 1
                random_consonant_buttons, random_button_index = update_folder(index)
                
            elif next_button.rect.collidepoint(mouse_pos) and index < len(folder_names) - 1:
                index += 1
                random_consonant_buttons, random_button_index = update_folder(index)
                
            elif next_image_button.rect.collidepoint(mouse_pos):
                selected_image_filename = load_random_image()
                random_consonant_buttons, random_button_index = create_consonant_buttons()
                
            else:
                for button in random_consonant_buttons:
                    if button.rect.collidepoint(mouse_pos):
                        if button.text == image_first_letter:
                            button.color = green
                            revealed = True  # Reveal the full word
                            if hooray_sound:
                                hooray_sound.play()
                        else:
                            button.color = red
                            if wrong_sound:
                                wrong_sound.play()
                                
        elif event.type == pygame.VIDEORESIZE:
            screen_width, screen_height = event.w, event.h
            screen = pygame.display.set_mode((screen_width, screen_height), pygame.RESIZABLE)
            random_consonant_buttons, random_button_index = create_consonant_buttons()
            next_image_button = create_next_button() 
    
    # Render
    screen.fill(white)
    
    if image:
        image_x = screen_width / 2 - image.get_width() / 2
        image_y = screen_height * image_y_percent - image.get_height() / 2
        screen.blit(image, (image_x, image_y))
    
    # Display either the full word or hidden word based on 'revealed' state
    display_word = current_word if revealed else f"-{hidden_word}"
    text_surface = font.render(display_word, True, black)
    text_x = screen_width / 2 - text_surface.get_width() / 2
    text_y = screen_height * text_y_percent - text_surface.get_height() / 2
    screen.blit(text_surface, (text_x, text_y))
    
    # Draw buttons
    for button in random_consonant_buttons:
        button.draw()
    
    prev_button.draw()
    next_button.draw()
    next_image_button.draw()
    
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()