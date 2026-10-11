import pygame
import os
import sys

pygame.init()
pygame.display.set_caption('Letter Reveal v.1.0')
pygame.event.set_allowed([pygame.QUIT, pygame.MOUSEBUTTONDOWN, pygame.VIDEORESIZE])

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

# Initialize display
screen_width, screen_height = 1280, 720
screen = pygame.display.set_mode((screen_width, screen_height), pygame.RESIZABLE)
clock = pygame.time.Clock()
font = pygame.font.Font(None, 36)

# Load resources
icon = pygame.image.load(resource_path('resources/icon/reveal.png')).convert_alpha()
pygame.display.set_icon(icon)

# Load letters
with open("resources/reveal/letters.txt", "r") as file:
    letters = [char.upper() for char in file.read() if char.isalpha()]

# Load and cache alphabet images
def load_alphabet_images(folder):
    images = {}
    for letter in letters:
        image = pygame.image.load(resource_path(f"{folder}/{letter}.png")).convert_alpha()
        images[letter] = image
    return images

rustic_images = load_alphabet_images("resources/rustic_alphabet")
red_images = load_alphabet_images("resources/red_alphabet")
current_images = rustic_images

# Game state
letter_index = 0
scaler = 1
background = (132, 148, 131)
hide_color = (255, 219, 88)
rect_count = 3
square_size = min(screen_width, screen_height) // int(scaler)

# Pre-render button surfaces
def create_button_surface(text, width, height):
    surf = pygame.Surface((width, height))
    surf.fill((0, 128, 128))
    text_surf = font.render(text, True, (250, 243, 221))
    surf.blit(text_surf, text_surf.get_rect(center=(width//2, height//2)))
    return surf

next_button = pygame.Rect(screen_width - 150, 10, 140, 50)
next_button_surf = create_button_surface("Next", 140, 50)
case_button = pygame.Rect(10, 10, 140, 50)
case_button_surf = create_button_surface("+/-", 140, 50)

def setup_rectangles(size):
    rect_size = size // rect_count
    square_x = screen_width // 2 - size // 2
    square_y = screen_height // 2 - size // 2
    return [
        pygame.Rect(
            square_x + x * rect_size, 
            square_y + y * rect_size, 
            rect_size, 
            rect_size
        )
        for x in range(rect_count)
        for y in range(rect_count)
    ]

hide_rectangles = setup_rectangles(square_size)

def game_function():
    global dirty_rects, force_full_redraw
    
    # If we need a full redraw (first frame or after resize)
    if force_full_redraw:
        screen.fill(background)
        dirty_rects = [screen.get_rect()]
        force_full_redraw = False
    
    # Process dirty rectangles
    update_rects = []
    
    # 1. Handle background updates for dirty areas
    for rect in dirty_rects:
        # Fill dirty areas with background color
        screen.fill(background, rect)
        update_rects.append(rect)
    
    # 2. Draw current letter (always in center)
    current_letter = letters[letter_index]
    scaled_image = pygame.transform.scale(current_images[current_letter], (square_size, square_size))
    image_rect = scaled_image.get_rect(center=(screen_width//2, screen_height//2))
    screen.blit(scaled_image, image_rect)
    update_rects.append(image_rect)
    
    # 3. Draw hide rectangles
    border_width = 2
    for rect in hide_rectangles:
        pygame.draw.rect(screen, (0, 0, 0), rect)
        pygame.draw.rect(screen, hide_color, rect.inflate(-border_width, -border_width))
        update_rects.append(rect)
    
    # 4. Draw buttons (always in same position)
    screen.blit(next_button_surf, next_button.topleft)
    screen.blit(case_button_surf, case_button.topleft)
    update_rects.extend([next_button, case_button])
    
    # Update only the changed areas
    pygame.display.update(update_rects)
    pygame.display.flip()  # Force full screen sync
    
    # Reset dirty rectangles for next frame
    dirty_rects = []
    clock.tick(30)
    
# Main loop variables
force_full_redraw = True
dirty_rects = []
state_changed = False

# Main loop
running = True
while running:
    state_changed = False  # Reset at start of each frame
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            state_changed = True
            
            if next_button.collidepoint(mouse_pos):
                letter_index = (letter_index + 1) % len(letters)
                hide_rectangles = setup_rectangles(square_size)
            
            elif case_button.collidepoint(mouse_pos):
                current_images = red_images if current_images == rustic_images else rustic_images
            
            else:
                for rect in hide_rectangles[:]:
                    if rect.collidepoint(mouse_pos):
                        hide_rectangles.remove(rect)
                        break
        
        elif event.type == pygame.VIDEORESIZE:
            screen_width, screen_height = event.w, event.h
            screen = pygame.display.set_mode((screen_width, screen_height), pygame.RESIZABLE)
            square_size = min(screen_width, screen_height) // int(scaler)
            hide_rectangles = setup_rectangles(square_size)
            next_button = pygame.Rect(screen_width - 150, 10, 140, 50)
            case_button = pygame.Rect(10, 10, 140, 50)
            force_full_redraw = True
    
    # Mark areas that need updates if state changed
    if state_changed:
        dirty_rects = [
            pygame.Rect(screen_width//2 - square_size//2, screen_height//2 - square_size//2, 
                       square_size, square_size),
            next_button,
            case_button
        ]
    
    game_function()

pygame.quit()