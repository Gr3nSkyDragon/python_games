import pygame
import sys
import random
import os

# Window boilerplate
pygame.init()
pygame.display.set_caption('Cowboy Numbers v.1.2')
Icon = pygame.image.load('resources/icon/cowboy_hat.png')
pygame.display.set_icon(Icon)
pygame.font.init()
game_font_size = int(0.5 * pygame.display.Info().current_h)
game_font = pygame.font.SysFont('Calistoga', game_font_size)
screen_width, screen_height = 1280, 720
screen = pygame.display.set_mode((screen_width, screen_height), pygame.RESIZABLE)
clock = pygame.time.Clock()
running = True

# Button variables# white color
color = (255, 255, 255)
color_light = (170, 170, 170)
color_dark = (100, 100, 100)
background = (40, 40, 120)
background_image = pygame.image.load('resources/background/desert_background.jpg')  # Image by pikisuperstar on Freepik
background_image = pygame.transform.scale(background_image, (screen_width, screen_height))

# Draw buttons with relative positions
reveal_button_width = int(0.2 * screen_width)  # 20% of the screen width
reveal_button_height = int(0.1 * screen_height)  # 10% of the screen height
reveal_button_x = int(0.1 * screen_width)
reveal_button_y = int(0.8 * screen_height)

shoot_button_width = int(0.2 * screen_width)  # 20% of the screen width
shoot_button_height = int(0.1 * screen_height)  # 10% of the screen height
shoot_button_x = int(0.9 * screen_width) - shoot_button_width
shoot_button_y = int(0.8 * screen_height)

# defining a font
smallfont_size = int(0.1 * screen_height)
smallfont = pygame.font.SysFont('Corbel', smallfont_size)
reveal_text = smallfont.render('Reveal', True, color)
shoot_text = smallfont.render('Shoot!', True, color)

# Game engine
def numbergen():
    with open("resources/cowboy/cowboy.txt", "r") as file:
        number = [line.strip() for line in file.readlines()]
    rand_number = random.randint(0, 9)
    number_test = number[rand_number]
    return number_test

# Event handling function
def handle_events():
    global running, number_game, hide_toggle, reveal_button_x, reveal_button_y, reveal_button_width, reveal_button_height
    global shoot_button_x, shoot_button_y, shoot_button_width, shoot_button_height, background_image

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
        # Handle window resizing
        if event.type == pygame.VIDEORESIZE:
            screen_width, screen_height = event.w, event.h
            screen = pygame.display.set_mode((screen_width, screen_height), pygame.RESIZABLE)
            background_image = pygame.transform.scale(background_image, (screen_width, screen_height))
            game_font_size = int(0.5 * screen_height)
            game_font = pygame.font.SysFont('Calistoga', game_font_size)
            smallfont_size = int(0.1 * screen_height)
            smallfont = pygame.font.SysFont('Corbel', smallfont_size)
            reveal_text = smallfont.render('Reveal', True, color)
            shoot_text = smallfont.render('Shoot!', True, color)
            
            reveal_button_width = int(0.2 * screen_width)  # 20% of the screen width
            reveal_button_height = int(0.1 * screen_height)  # 10% of the screen height
            reveal_button_x = int(0.1 * screen_width)
            reveal_button_y = int(0.8 * screen_height)

            shoot_button_width = int(0.2 * screen_width)  # 20% of the screen width
            shoot_button_height = int(0.1 * screen_height)  # 10% of the screen height
            shoot_button_x = int(0.9 * screen_width) - shoot_button_width
            shoot_button_y = int(0.8 * screen_height)

            # Recalculate text position on window resize
            text_x = (screen_width - text_rect.width) // 2
            text_y = (screen_height - text_rect.height) // 2

        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = event.pos
            
            # Reveal button click
            if reveal_button_x <= mouse_x <= reveal_button_x + reveal_button_width and reveal_button_y <= mouse_y <= reveal_button_y + reveal_button_height:
                hide_toggle = 1 - hide_toggle

            # Shoot button click
            if shoot_button_x <= mouse_x <= shoot_button_x + shoot_button_width and shoot_button_y <= mouse_y <= shoot_button_y + shoot_button_height:
                number_game = numbergen()
                hide_toggle = 0

    return True

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

    # Draw reveal button
    if reveal_button_x <= mouse[0] <= reveal_button_x + reveal_button_width and reveal_button_y <= mouse[1] <= reveal_button_y + reveal_button_height:
        pygame.draw.rect(screen, color_light, [reveal_button_x, reveal_button_y, reveal_button_width, reveal_button_height])
    else:
        pygame.draw.rect(screen, color_dark, [reveal_button_x, reveal_button_y, reveal_button_width, reveal_button_height])

    # superimposing the text onto the reveal button
    screen.blit(reveal_text, (reveal_button_x + int(0.032 * screen_width), reveal_button_y + int(0.01 * screen_height)))

    # Draw shoot button
    if shoot_button_x <= mouse[0] <= shoot_button_x + shoot_button_width and shoot_button_y <= mouse[1] <= shoot_button_y + shoot_button_height:
        pygame.draw.rect(screen, color_light, [shoot_button_x, shoot_button_y, shoot_button_width, shoot_button_height])
    else:
        pygame.draw.rect(screen, color_dark, [shoot_button_x, shoot_button_y, shoot_button_width, shoot_button_height])

    # superimposing the text onto the shoot button
    screen.blit(shoot_text, (shoot_button_x + int(0.032 * screen_width), shoot_button_y + int(0.01 * screen_height)))

    # Draw numbers
    if hide_toggle == 1:
        text_surface = game_font.render(number_game, False, (110, 170, 70))
    else:
        text_surface = game_font.render(hidden_number_game, False, (110, 170, 70))

    # Get the dimensions of the text surface
    text_rect = text_surface.get_rect()

    # Recalculate the center position on the screen after resizing
    text_x = (screen.get_width() - text_rect.width) // 2
    text_y = (screen.get_height() - text_rect.height) // 2

    # blit the text onto the screen
    screen.blit(text_surface, (text_x, text_y))
    
    # updates the frames of the game
    pygame.display.update()

    # flip() the display to put your work on screen
    pygame.display.flip()

    clock.tick(60)  # limits FPS to 60

pygame.quit()