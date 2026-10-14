import pygame
import pygame.gfxdraw
import os
import json
import math
import random
import string
import pyttsx3
import sys
from paths import resource, local

# Volume settings, saved next to the exe so they're remembered between sessions
SETTINGS_FILE = local('star_cvc_settings.json')
DEFAULT_SETTINGS = {'sfx_volume': 1.0, 'voice_volume': 0.9}

def load_settings():
    try:
        with open(SETTINGS_FILE) as f:
            saved = json.load(f)
        return {key: min(1.0, max(0.0, float(saved.get(key, default))))
                for key, default in DEFAULT_SETTINGS.items()}
    except (OSError, ValueError, TypeError, AttributeError):
        return dict(DEFAULT_SETTINGS)

def save_settings():
    try:
        with open(SETTINGS_FILE, 'w') as f:
            json.dump(settings, f, indent=2)
    except OSError as e:
        print(f"Couldn't save settings: {e}")

settings = load_settings()

# Initialize text-to-speech engine
def init_tts():
    try:
        engine = pyttsx3.init()
        voices = engine.getProperty('voices')
        engine.setProperty('rate', 170)
        engine.setProperty('volume', settings['voice_volume'])
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
    icon_path = resource('icon', 'star.jpg')
    Icon = pygame.image.load(icon_path)
    pygame.display.set_icon(Icon)
except Exception as e:
    print(f"Couldn't load icon: {e}")

# Set up display
screen_width = 1280
screen_height = 720
screen = pygame.display.set_mode((screen_width, screen_height), pygame.RESIZABLE)

phonics_words_folder = resource('star', 'families')
IMAGE_TYPES = ('.png', '.jpg', '.jpeg', '.gif')

def populated_families():
    """Word-family folders that contain at least one picture, in alphabetical order."""
    families = []
    try:
        for name in sorted(os.listdir(phonics_words_folder)):
            path = os.path.join(phonics_words_folder, name)
            if os.path.isdir(path) and any(f.lower().endswith(IMAGE_TYPES) for f in os.listdir(path)):
                families.append(name)
    except OSError as e:
        print(f"Error reading phonics folders: {e}")
    return families

folder_names = populated_families()

# Game state variables
on_menu = True  # Start on the main menu; picking a word family switches to the game
selected_folder_name = ""
selected_subfolder_path = ""
image = None
image_first_letter = ""
current_word = ""  # Track the complete word
hidden_word = ""    # Track the word with hidden letters
revealed = False    # Track if word is fully revealed

# Load sounds
try:
    wrong_sound = pygame.mixer.Sound(resource('star', 'wrong_sound.mp3'))
    hooray_sound = pygame.mixer.Sound(resource('star', 'hooray_sound.mp3'))
except Exception as e:
    print(f"Couldn't load sound files: {e}")
    wrong_sound = None
    hooray_sound = None

def apply_volumes():
    """SFX covers both the hooray and the wrong-answer buzzer; Voice is text-to-speech."""
    for sound in (wrong_sound, hooray_sound):
        if sound:
            sound.set_volume(settings['sfx_volume'])
    if tts_engine:
        tts_engine.setProperty('volume', settings['voice_volume'])

apply_volumes()

def speak(text):
    if tts_engine:
        try:
            tts_engine.say(text)
            tts_engine.runAndWait()
        except Exception as e:
            print(f"Error with text-to-speech: {e}")

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
                          if name.lower().endswith(IMAGE_TYPES)]
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

def choose_family(name):
    """Start the game with the chosen word family."""
    global selected_folder_name, selected_subfolder_path, on_menu
    selected_folder_name = name
    selected_subfolder_path = os.path.join(phonics_words_folder, name)
    on_menu = False
    load_random_image()
    return create_consonant_buttons()

# No word family yet: the game starts on the main menu
random_consonant_buttons, random_button_index = [], None

# Returns to the main menu
def create_menu_button():
    return Button(screen_width * 0.05, screen_height * 0.1, "Menu", color=(200, 200, 200))

menu_button = create_menu_button()

# Replace your current next_image_button initialization with:
def create_next_button():
    return Button(
        screen_width - (screen_width * button_width_percent) - 20,
        screen_height - (screen_height * button_height_percent) - 20,
        "Next"
    )

# Initialize it
next_image_button = create_next_button()

# Settings: a cog in the top-right corner opens volume sliders
SLIDERS = [('sfx_volume', 'SFX'), ('voice_volume', 'Voice')]
settings_open = False
dragging_slider = None  # settings key of the slider being dragged

def cog_rect():
    size = max(32, int(min(screen_width, screen_height) * 0.07))
    margin = size // 3
    return pygame.Rect(screen_width - size - margin, margin, size, size)

def draw_cog(rect):
    cx, cy = rect.center
    outer = rect.width / 2
    inner = outer * 0.72
    teeth = 8
    points = []
    for i in range(teeth * 4):
        # Each tooth is two points on the outer edge between two on the inner edge
        radius = outer if i % 4 in (1, 2) else inner
        angle = 2 * math.pi * (i + 0.5) / (teeth * 4)
        points.append((cx + radius * math.cos(angle), cy + radius * math.sin(angle)))
    cog_color = (70, 70, 70)
    pygame.gfxdraw.aapolygon(screen, points, cog_color)
    pygame.gfxdraw.filled_polygon(screen, points, cog_color)
    hole = int(outer * 0.3)
    pygame.gfxdraw.aacircle(screen, cx, cy, hole, white)
    pygame.gfxdraw.filled_circle(screen, cx, cy, hole, white)

def settings_layout():
    """The panel under the cog, and a slider track for each setting."""
    cog = cog_rect()
    row_height = max(44, int(screen_height * 0.075))
    panel = pygame.Rect(0, 0, max(300, int(screen_width * 0.28)), row_height * len(SLIDERS) + row_height // 2)
    panel.topright = (cog.right, cog.bottom + 8)
    label_width = panel.width * 0.25
    value_width = panel.width * 0.22
    knob_room = 16  # keeps the knob clear of the label and percentage at either end
    tracks = {}
    for i, (key, _) in enumerate(SLIDERS):
        y = panel.y + row_height // 4 + row_height * i + row_height // 2
        tracks[key] = pygame.Rect(panel.x + label_width + knob_room, y - 4,
                                  panel.width - label_width - value_width - 2 * knob_room, 8)
    return panel, tracks

def draw_settings():
    panel, tracks = settings_layout()
    pygame.draw.rect(screen, (245, 245, 245), panel, border_radius=10)
    pygame.draw.rect(screen, (70, 70, 70), panel, 2, border_radius=10)
    label_font = pygame.font.Font(None, max(26, int(panel.height / len(SLIDERS) * 0.55)))
    for key, label in SLIDERS:
        track = tracks[key]
        value = settings[key]
        text = label_font.render(label, True, black)
        screen.blit(text, text.get_rect(midleft=(panel.x + 15, track.centery)))
        pygame.draw.rect(screen, (190, 190, 190), track, border_radius=4)
        filled = pygame.Rect(track.x, track.y, int(track.width * value), track.height)
        pygame.draw.rect(screen, (60, 140, 220), filled, border_radius=4)
        knob = (int(track.x + track.width * value), track.centery)
        pygame.draw.circle(screen, (60, 140, 220), knob, 12)
        pygame.draw.circle(screen, black, knob, 12, 2)
        percent = label_font.render(f"{round(value * 100)}%", True, black)
        screen.blit(percent, percent.get_rect(midright=(panel.right - 15, track.centery)))

def set_slider(key, x):
    _, tracks = settings_layout()
    track = tracks[key]
    settings[key] = round(min(1.0, max(0.0, (x - track.x) / track.width)), 2)  # whole percents
    apply_volumes()

def handle_settings_click(pos, mouse_button):
    """Return True if the click belongs to the cog or settings panel, so the game ignores it."""
    global settings_open, dragging_slider
    if cog_rect().collidepoint(pos):
        settings_open = not settings_open
        return True
    if not settings_open:
        return False
    panel, tracks = settings_layout()
    if panel.collidepoint(pos):
        for key, track in tracks.items():
            if mouse_button == 1 and track.inflate(24, 30).collidepoint(pos):
                dragging_slider = key
                set_slider(key, pos[0])
        return True
    settings_open = False  # Clicking anywhere else closes the panel
    return True

def finish_slider_drag():
    global dragging_slider
    key = dragging_slider
    dragging_slider = None
    save_settings()
    # Play a preview at the new volume
    if key == 'sfx_volume' and hooray_sound:
        hooray_sound.play()
    elif key == 'voice_volume':
        speak(current_word or "Voice")

# Main menu: word-family buttons in two columns, in a list that scrolls when it doesn't fit
MENU_COLUMNS = 2
SCROLLBAR_WIDTH = 16
menu_scroll = 0      # How far down the list is scrolled, in pixels
scroll_drag = None   # (mouse y, menu_scroll) when the scrollbar handle was grabbed
menu_fonts = {}

def menu_font(size):
    if size not in menu_fonts:
        menu_fonts[size] = pygame.font.Font(None, size)
    return menu_fonts[size]

def menu_layout():
    """The visible list area, the button size and gap, and the height of the whole list."""
    top = int(screen_height * 0.2)
    area = pygame.Rect(int(screen_width * 0.12), top,
                       int(screen_width * 0.76), screen_height - top - int(screen_height * 0.05))
    gap = max(10, int(screen_height * 0.025))
    button_width = (area.width - SCROLLBAR_WIDTH - gap - gap * (MENU_COLUMNS - 1)) // MENU_COLUMNS
    button_height = max(48, int(screen_height * 0.1))
    rows = math.ceil(len(folder_names) / MENU_COLUMNS)
    list_height = max(0, rows * (button_height + gap) - gap)
    return area, button_width, button_height, gap, list_height

def max_menu_scroll():
    area, _, _, _, list_height = menu_layout()
    return max(0, list_height - area.height)

def scroll_menu_to(position):
    global menu_scroll
    menu_scroll = min(max(0, position), max_menu_scroll())

def menu_buttons():
    """(family name, rect) for every word-family button, at its scrolled position."""
    area, button_width, button_height, gap, _ = menu_layout()
    for i, name in enumerate(folder_names):
        row, column = divmod(i, MENU_COLUMNS)
        yield name, pygame.Rect(area.x + column * (button_width + gap),
                                area.y + row * (button_height + gap) - menu_scroll,
                                button_width, button_height)

def scrollbar_rects():
    """The scrollbar track and its draggable handle, or None when everything fits."""
    area, _, _, _, list_height = menu_layout()
    max_scroll = max_menu_scroll()
    if max_scroll == 0:
        return None
    track = pygame.Rect(area.right - SCROLLBAR_WIDTH, area.y, SCROLLBAR_WIDTH, area.height)
    handle_height = max(30, int(track.height * area.height / list_height))
    handle_y = track.y + (track.height - handle_height) * menu_scroll / max_scroll
    return track, pygame.Rect(track.x, handle_y, SCROLLBAR_WIDTH, handle_height)

def draw_menu():
    title = menu_font(max(36, int(screen_height * 0.09))).render("Choose a word family", True, black)
    screen.blit(title, title.get_rect(center=(screen_width / 2, screen_height * 0.1)))

    area, _, button_height, _, _ = menu_layout()
    if not folder_names:
        message = menu_font(max(28, int(screen_height * 0.05))).render(
            "No word families with pictures found", True, black)
        screen.blit(message, message.get_rect(midtop=area.midtop))
        return

    # Only draw inside the list area, so buttons scrolled partly out of view are cut off cleanly
    screen.set_clip(area)
    label_font = menu_font(int(button_height * 0.6))
    for name, rect in menu_buttons():
        if rect.colliderect(area):
            pygame.draw.rect(screen, gray_blue, rect, border_radius=8)
            pygame.draw.rect(screen, black, rect, 2, border_radius=8)
            label = label_font.render(name, True, black)
            screen.blit(label, label.get_rect(center=rect.center))
    screen.set_clip(None)

    bar = scrollbar_rects()
    if bar:
        track, handle = bar
        pygame.draw.rect(screen, (200, 200, 200), track, border_radius=8)
        pygame.draw.rect(screen, (90, 90, 90), handle, border_radius=8)

def handle_menu_click(pos):
    """Scroll if the scrollbar was clicked; return the family name if a family button was."""
    global scroll_drag
    bar = scrollbar_rects()
    if bar:
        track, handle = bar
        if handle.collidepoint(pos):
            scroll_drag = (pos[1], menu_scroll)
            return None
        if track.collidepoint(pos):
            # Clicking the track above or below the handle jumps a page that way
            area = menu_layout()[0]
            scroll_menu_to(menu_scroll + (area.height if pos[1] > handle.centery else -area.height))
            return None
    area = menu_layout()[0]
    if area.collidepoint(pos):
        for name, rect in menu_buttons():
            if rect.collidepoint(pos):
                return name
    return None

def drag_scrollbar(mouse_y):
    bar = scrollbar_rects()
    if not bar:
        return  # The window grew and the list fits now
    track, handle = bar
    start_y, start_scroll = scroll_drag
    # Moving the handle the whole free length of the track scrolls the whole list
    free_length = track.height - handle.height
    if free_length > 0:
        scroll_menu_to(start_scroll + (mouse_y - start_y) * max_menu_scroll() / free_length)

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button in (4, 5):
                continue  # Mouse wheel; scrolling is handled by MOUSEWHEEL, not as a click
            mouse_pos = pygame.mouse.get_pos()

            if handle_settings_click(mouse_pos, event.button):
                pass  # The cog or settings panel used this click

            elif on_menu:
                family = handle_menu_click(mouse_pos)
                if family:
                    random_consonant_buttons, random_button_index = choose_family(family)

            elif image and image.get_rect(topleft=(screen_width / 2 - image.get_width() / 2,
                                                 screen_height * image_y_percent - image.get_height() / 2)).collidepoint(mouse_pos):
                speak(current_word)

            elif menu_button.rect.collidepoint(mouse_pos):
                on_menu = True

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

        elif event.type == pygame.MOUSEWHEEL and on_menu and not settings_open:
            # One notch scrolls about half a row
            _, _, button_height, gap, _ = menu_layout()
            scroll_menu_to(menu_scroll - event.y * (button_height + gap) // 2)

        elif event.type == pygame.MOUSEMOTION and dragging_slider:
            set_slider(dragging_slider, event.pos[0])

        elif event.type == pygame.MOUSEMOTION and scroll_drag:
            drag_scrollbar(event.pos[1])

        elif event.type == pygame.MOUSEBUTTONUP and dragging_slider:
            finish_slider_drag()

        elif event.type == pygame.MOUSEBUTTONUP and scroll_drag:
            scroll_drag = None

        elif event.type == pygame.VIDEORESIZE:
            screen_width, screen_height = event.w, event.h
            screen = pygame.display.set_mode((screen_width, screen_height), pygame.RESIZABLE)
            if not on_menu:
                random_consonant_buttons, random_button_index = create_consonant_buttons()
            next_image_button = create_next_button()
            menu_button = create_menu_button()
            scroll_menu_to(menu_scroll)  # Keep the list in range for the new size

    # Render
    screen.fill(white)

    if on_menu:
        draw_menu()
    else:
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

        menu_button.draw()
        next_image_button.draw()

    draw_cog(cog_rect())
    if settings_open:
        draw_settings()

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
