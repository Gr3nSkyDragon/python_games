import pygame
import sys
import random
import os
from paths import resource, editable

# Window boilerplate
pygame.init()
pygame.display.set_caption('Cowboy Numbers v.1.6')

# Load window icon
icon_path = resource('icon', 'cowboy_hat.png')
Icon = pygame.image.load(icon_path)
pygame.display.set_icon(Icon)

pygame.font.init()
screen_width, screen_height = 1280, 720
screen = pygame.display.set_mode((screen_width, screen_height), pygame.RESIZABLE)
clock = pygame.time.Clock()
running = True

# Button colors, taken from the background picture
button_color = (191, 45, 7)         # the darkest part of the rocks
button_hover_color = (150, 35, 5)    # a deeper rock shade for hovering, so the text stays readable
button_text_color = (254, 159, 38)   # the darker sand on the dune under the rocks
background = (40, 40, 120)
background_image_original = pygame.image.load(resource('background', 'desert_background.jpg'))  # Image by pikisuperstar on Freepik

def layout():
    """Size and place everything for the current window size."""
    global background_image, game_font, reveal_button, shoot_button, reveal_text, shoot_text
    # Always scale from the original, so repeated resizing doesn't blur the picture
    background_image = pygame.transform.scale(background_image_original, (screen_width, screen_height))
    game_font = pygame.font.SysFont('Calistoga', int(0.75 * screen_height))

    # Buttons: 20% of the window wide and 10% high, near the bottom corners
    button_width = int(0.2 * screen_width)
    button_height = int(0.1 * screen_height)
    reveal_button = pygame.Rect(int(0.1 * screen_width), int(0.8 * screen_height), button_width, button_height)
    shoot_button = pygame.Rect(int(0.9 * screen_width) - button_width, int(0.8 * screen_height),
                               button_width, button_height)

    smallfont = pygame.font.SysFont('Corbel', int(0.1 * screen_height))
    reveal_text = smallfont.render('Reveal', True, button_text_color)
    shoot_text = smallfont.render('Shoot!', True, button_text_color)

layout()

# Game engine
def numbergen(previous=None):
    """A random number from cowboy.txt, never the same as the previous one (when there's a choice)."""
    with open(editable('cowboy', 'cowboy.txt'), "r") as file:
        numbers = [line.strip() for line in file.readlines() if line.strip()]
    if not numbers:  # Handle empty file case
        return "00"  # Or some default value
    # Compare by value, so a number listed twice in the file can't repeat either
    choices = [n for n in numbers if n != previous] or numbers
    return random.choice(choices)

# Event handling function
def handle_events():
    global running, number_game, hide_toggle, screen, screen_width, screen_height

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Handle window resizing
        if event.type == pygame.VIDEORESIZE:
            screen_width, screen_height = event.w, event.h
            screen = pygame.display.set_mode((screen_width, screen_height), pygame.RESIZABLE)
            layout()

        if event.type == pygame.MOUSEBUTTONDOWN:
            # Reveal button click
            if reveal_button.collidepoint(event.pos):
                hide_toggle = 1 - hide_toggle

            # Shoot button click
            if shoot_button.collidepoint(event.pos):
                number_game = numbergen(previous=number_game)
                hide_toggle = 0

    return True

def draw_button(rect, text, mouse):
    color = button_hover_color if rect.collidepoint(mouse) else button_color
    pygame.draw.rect(screen, color, rect)
    # Center the visible letters, not the font's full line height (which leaves room for g, y, etc.)
    ink = text.get_bounding_rect()
    screen.blit(text, (rect.centerx - ink.centerx, rect.centery - ink.centery))

# Main game loop
hide_toggle = 0
number_game = numbergen()
hidden_number_game = '??'

while running:
    if not handle_events():
        break

    # fills the screen with a color
    screen.fill(background)
    screen.blit(background_image, (0, 0))

    # stores the (x,y) coordinates into
    # the variable as a tuple
    mouse = pygame.mouse.get_pos()

    draw_button(reveal_button, reveal_text, mouse)
    draw_button(shoot_button, shoot_text, mouse)

    # Draw numbers
    if hide_toggle == 1:
        text_surface = game_font.render(number_game, False, (110, 170, 70))
    else:
        text_surface = game_font.render(hidden_number_game, False, (110, 170, 70))

    # Center the numbers on the screen
    screen.blit(text_surface, text_surface.get_rect(center=screen.get_rect().center))

    # flip() the display to put your work on screen
    pygame.display.flip()

    clock.tick(60)  # limits FPS to 60

pygame.quit()
