# Example file showing a basic pygame "game loop"
import pygame
import sys
import random

#Window boilerplate
pygame.init()
pygame.display.set_caption('Alphabet Blaster v.1.5')
Icon = pygame.image.load('resources/icon/apple.png')
pygame.display.set_icon(Icon)
pygame.font.init()
game_font_size = int(0.2 * pygame.display.Info().current_h)
game_font = pygame.font.SysFont('Comic Sans MS', game_font_size)
screen_width, screen_height = 1280, 720
screen = pygame.display.set_mode((screen_width, screen_height),pygame.RESIZABLE)
clock = pygame.time.Clock()
running = True

#Button variables
color = (255,255,255)
color_light = (170,170,170)
color_dark = (100,100,100)
background = (115,150,190)

width = screen.get_width()
height = screen.get_height()

# Initial width and height for reference in the resize event
old_width, old_height = width, height

# Button properties (x, y, width, height, active_color, inactive_color)
buttons = [
    (width * 0.75, height * 0.75, 140, 40, color_light, color_dark),  # Blast
    (width * 0.10, height * 0.75, 140, 40, color_light, color_dark),  # Reveal
    (width * 0.9, height * 0.05, 40, 40, (170, 0, 230), (190,0,250)),  # Case Change
    (width * 0.05, height * 0.05, 40, 40, (50, 230, 50), (60,250,60)),    # Difficulty 1
    (width * 0.05 + 40, height * 0.05, 40, 40, (215, 235, 50), (230,250,60)),  # Difficulty 2
    (width * 0.05 + 80, height * 0.05, 40, 40, (235, 145, 50), (250,160,60)),  # Difficulty 3
    (width * 0.05 + 120, height * 0.05, 40, 40, (230, 50, 50), (250,60,60)),  # Difficulty 4
]
  
# defining a font
smallfont = pygame.font.SysFont('Corbel',35)
text = smallfont.render('Blast!' , True , color)
answer_text = smallfont.render('Reveal', True, color)

#Game engine
def lettergen(case):
    alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
    if case == 1:
        alphabet = [letter.upper() for letter in alphabet]        
    rand_letters = random.randint(0,20)
    letter_test = alphabet[rand_letters:rand_letters+6]
    return letter_test

def engine(engine_letter,difficulty):
    while difficulty > 0:
        setter = random.randint(0,5)
        if engine_letter[setter] == '?':
            difficulty += 1
        engine_letter[setter] = '?'
        difficulty -= 1
    return engine_letter

#Initialize game
hide_toggle = 0
letter_case = 0
set_difficulty = 3    
letter_game = lettergen(letter_case)
hidden_letter_game = letter_game.copy()
engine(letter_game,set_difficulty)

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
        # Handle window resizing
        if event.type == pygame.VIDEORESIZE:
            width, height = event.w, event.h
            screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)
            game_font_size = int(0.2 * height)
            game_font = pygame.font.SysFont('Comic Sans MS', game_font_size)
            smallfont_size = int(0.05 * height)
            smallfont = pygame.font.SysFont('Corbel', smallfont_size)
            text = smallfont.render('Blast!', True, color)
            answer_text = smallfont.render('Reveal', True, color)
            
            # Update the button properties with new width and height
            for i, button in enumerate(buttons):
                x, y, w, h, _, _ = button
                buttons[i] = (
                    width * x / old_width,
                    height * y / old_height,
                    width * w / old_width,
                    height * h / old_height,
                    button[4],  # active_color
                    button[5],  # inactive_color
                )

            # Update old_width and old_height with the new values
            old_width, old_height = width, height
            
        #mouse click    
        if event.type == pygame.MOUSEBUTTONDOWN:          
            # Get the relative coordinates of the mouse click within the current screen size
            mouse = pygame.mouse.get_pos()
            mouse_x, mouse_y = mouse[0], mouse[1]

            # Determine which button was clicked based on the last element of the buttons array
            for i, button in enumerate(buttons):
                btn_x, btn_y, btn_w, btn_h, _, _ = button
                if btn_x <= mouse_x <= btn_x + btn_w and btn_y <= mouse_y <= btn_y + btn_h:
                    button_type = buttons[i][5]  # Get the last element of the button array
                    if button_type == color_dark:  
                        if i == 0:
                            letter_game = lettergen(letter_case)
                            hidden_letter_game = letter_game.copy()
                            engine(letter_game, set_difficulty)
                            hide_toggle = 0
                        elif i == 1:
                            hide_toggle = 1 - hide_toggle
                    elif button_type == (190,0,250):
                        letter_case = 1 - letter_case
                    elif button_type == (60,250,60):
                        set_difficulty = 1
                    elif button_type == (230,250,60):
                        set_difficulty = 2
                    elif button_type == (250,160,60):
                        set_difficulty = 3
                    elif button_type == (250,60,60):
                        set_difficulty = 5
                        
                 
    # fills the screen with a color
    screen.fill(background)
      
    # stores the (x,y) coordinates into
    # the variable as a tuple
    mouse = pygame.mouse.get_pos()
      
    # if mouse is hovered on a button it
    # changes to lighter shade
    
    # Loop through the buttons and draw them
    for btn in buttons:
        x, y, w, h, active_color, inactive_color = btn
        if x <= mouse[0] <= x + w and y <= mouse[1] <= y + h:
            pygame.draw.rect(screen, active_color, [x, y, w, h])
        else:
            pygame.draw.rect(screen, inactive_color, [x, y, w, h])
        
    # superimposing the text onto our button
    screen.blit(text , (width*0.75+32,height*0.75+5))
    screen.blit(answer_text, (width*0.10+29,height*0.75+5))
    
    #Draw letters
    if hide_toggle == 0:
        text_surface = game_font.render(letter_game[0] + ' ' + letter_game[1] + ' ' +  letter_game[2] + ' ' +  letter_game[3] + ' ' +  letter_game[4] + ' ' +  letter_game[5], False, (229, 229, 19))
        screen.blit(text_surface, (width/5,height/3))
        
    elif hide_toggle == 1:
        text_surface = game_font.render(hidden_letter_game[0] + ' ' + hidden_letter_game[1] + ' ' +  hidden_letter_game[2] + ' ' +  hidden_letter_game[3] + ' ' +  hidden_letter_game[4] + ' ' +  hidden_letter_game[5], False, (229, 229, 19))
        screen.blit(text_surface, (width/5,height/3))
        
    else:
        text_surface = game_font.render('You broke something, nerd')
    
    # updates the frames of the game
    pygame.display.update()
    
    # flip() the display to put your work on screen
    pygame.display.flip()

    clock.tick(60)  # limits FPS to 60

pygame.quit()