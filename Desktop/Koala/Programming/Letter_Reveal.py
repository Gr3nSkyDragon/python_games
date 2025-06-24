import pygame
import os
import random

pygame.init()
pygame.display.set_caption('Letter Reveal v.1.0')

# Get the correct path for bundled data
def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)
    
# Load icon using resource_path
icon_path = resource_path('resources/icon/reveal.png')
Icon = pygame.image.load(icon_path)
pygame.display.set_icon(Icon)

clock = pygame.time.Clock()

# Set up display
screen_width = 1280
screen_height = 720
screen = pygame.display.set_mode((screen_width, screen_height), pygame.RESIZABLE)

letter_index = 0
scaler = 1
background = (132, 148, 131)
hide_color = (255, 219, 88)

# Load letters from the text file
with open("resources/reveal/letters.txt", "r") as file:
    letters = [char.upper() for char in file.read() if char.isalpha()]

# Load alphabet pictures and resize them to fit the whole square
square_size = min(screen_width, screen_height) // int(scaler)  # Size of the whole square
alphabet_images = {}
for letter in letters:
    image_path = os.path.join("resources/rustic_alphabet", f"{letter}.png")
    image = pygame.image.load(image_path)
    image = pygame.transform.scale(image, (square_size, square_size))  # Resize the image
    alphabet_images[letter] = image

# Set up rectangles
rect_count = 3  # Number of rectangles in each direction
hide_rectangles = []

# Create "Next" button
next_button = pygame.Rect(screen_width - 150, 10, 140, 50)

# Create "+/-" button
case_change_button = pygame.Rect(10, 10, 140, 50)

def setup_rectangles(square_size):
    rect_size = square_size // rect_count
    return [
        pygame.Rect(x, y, rect_size, rect_size)
        for x in range(screen_width // 2 - square_size // 2, screen_width // 2 + square_size // 2, rect_size)
        for y in range(screen_height // 2 - square_size // 2, screen_height // 2 + square_size // 2, rect_size)
    ]

def update_alphabet_images():
    for letter in letters:
        image = pygame.image.load(current_image_path + f"/{letter}.png")
        image = pygame.transform.scale(image, (square_size, square_size))
        alphabet_images[letter] = image

def game_function():
    screen.fill(background)
    
    # Draw image
    current_letter = letters[letter_index]
    image = alphabet_images[current_letter]
    image_rect = image.get_rect(center=(screen_width // 2, screen_height // 2))
    screen.blit(image, image_rect.topleft)
    
    # Draw hide rectangles with black border
    border_width = 2  # Adjust this value as needed
    for rect in hide_rectangles:
        pygame.draw.rect(screen, (0, 0, 0), rect)  # Draw black border
        pygame.draw.rect(screen, hide_color, rect.inflate(-border_width, -border_width))  # Draw inner rectangle
    
    # Draw next button
    pygame.draw.rect(screen, (0, 128, 128), next_button)
    font = pygame.font.Font(None, 36)
    text = font.render("Next", True, (250, 243, 221))
    text_rect = text.get_rect(center=next_button.center)
    screen.blit(text, text_rect.topleft)
    
    # Draw case change button
    pygame.draw.rect(screen, (0, 128, 128), case_change_button)
    text = font.render("+/-", True, (250, 243, 221))
    text_rect = text.get_rect(center=case_change_button.center)
    screen.blit(text, text_rect.topleft)
    
    pygame.display.flip()
    
    clock.tick(60)

# Main loop
running = True
hide_rectangles = setup_rectangles(square_size)
current_image_path = "resources/rustic_alphabet"

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            
            for rect in hide_rectangles:
                if rect.collidepoint(mouse_pos):
                    hide_rectangles.remove(rect)
                    break  # Only remove one rectangle per click
            
            if next_button.collidepoint(mouse_pos):
                letter_index = (letter_index + 1) % len(letters)
                hide_rectangles = setup_rectangles(square_size)  # Update hide_rectangles
            
            if case_change_button.collidepoint(mouse_pos):
                if current_image_path == "resources/rustic_alphabet":
                    current_image_path = "resources/red_alphabet"
                else:
                    current_image_path = "resources/rustic_alphabet"
                update_alphabet_images()
                
        elif event.type == pygame.VIDEORESIZE:
            # Update screen dimensions
            screen_width = event.w
            screen_height = event.h
            screen = pygame.display.set_mode((screen_width, screen_height), pygame.RESIZABLE)
            square_size = min(screen_width, screen_height) // int(scaler)
            hide_rectangles = setup_rectangles(square_size)  # Update hide_rectangles
            next_button = pygame.Rect(screen_width - 150, 10, 140, 50)  # Update next_button position
            case_change_button = pygame.Rect(10, 10, 140, 50)  # Update case_change_button position
    
    game_function()
    
pygame.quit()