# Example file showing a basic pygame "game loop"
import pygame
import sys
import random

#Window boilerplate
pygame.init()
pygame.display.set_caption('Cowboy Numbers v.0.5')
Icon = pygame.image.load('resources/icon/cowboy_hat.png')
pygame.display.set_icon(Icon)
pygame.font.init()
game_font = pygame.font.SysFont('Calistoga', 500)
screen = pygame.display.set_mode((1280, 720),pygame.RESIZABLE)
clock = pygame.time.Clock()
running = True

#Button variables# white color
color = (255,255,255)
color_light = (170,170,170)
color_dark = (100,100,100)
background = (40, 40, 120)
background_image = pygame.image.load('resources/background/desert_background.jpg') # Image by pikisuperstar on Freepik
#background_image = pygame.image.load('night_desert.jpg') # Image by brgfx on Freepik
background_image = pygame.transform.scale(background_image, (1280, 720))
  
width = screen.get_width()
height = screen.get_height()
  
# defining a font
smallfont = pygame.font.SysFont('Corbel',35)
text = smallfont.render('shoot!' , True , color)
answer_text = smallfont.render('reveal', True, color)

#Game engine
def numbergen():
    number = ['11', '12', '13', '14', '15', '16', '17', '18', '19', '20']
    rand_number = random.randint(0,9)
    number_test = number[rand_number]
    return number_test

#Initialize game
hide_toggle = 0
number_game = numbergen()
hidden_number_game = '??'

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:            
            if width*0.75 <= mouse[0] <= width*0.75+140 and height*0.75 <= mouse[1] <= height*0.75+40:
                number_game = numbergen()
                hide_toggle = 0
            elif width*0.10 <= mouse[0] <= width*0.10+140 and height*0.75 <= mouse[1] <= height*0.75+40:
                hide_toggle = 1 - hide_toggle
                 
    # fills the screen with a color
    screen.fill(background)
    screen.blit(background_image, (0, 0))
      
    # stores the (x,y) coordinates into
    # the variable as a tuple
    mouse = pygame.mouse.get_pos()
      
    # if mouse is hovered on a button it
    # changes to lighter shade 
    if width*0.75 <= mouse[0] <= width*0.75+140 and height*0.75 <= mouse[1] <= height*0.75+40:
        pygame.draw.rect(screen,color_light,[width*0.75,height*0.75,140,40])
        pygame.draw.rect(screen,color_dark,[width*0.10,height*0.75,140,40])
        
    elif width*0.10 <= mouse[0] <= width*0.10+140 and height*0.75 <= mouse[1] <= height*0.75+40:
        pygame.draw.rect(screen,color_light,[width*0.10,height*0.75,140,40])
        pygame.draw.rect(screen,color_dark,[width*0.75,height*0.75,140,40])
    else:
        pygame.draw.rect(screen,color_dark,[width*0.75,height*0.75,140,40])
        pygame.draw.rect(screen,color_dark,[width*0.10,height*0.75,140,40])
        
    # superimposing the text onto our button
    screen.blit(text , (width*0.75+32,height*0.75+5))
    screen.blit(answer_text, (width*0.10+29,height*0.75+5))
    
    #Draw letters
    if hide_toggle == 1:
        text_surface = game_font.render(number_game, False, (110, 170, 70))
        screen.blit(text_surface, (420,180))
    
    elif hide_toggle == 0:
        text_surface = game_font.render(hidden_number_game, False, (110, 170, 70))
        screen.blit(text_surface, (420, 180))
    
    else:
        text_surface = game_font.render('You broke something, nerd')
    
    # updates the frames of the game
    pygame.display.update()
    
    # flip() the display to put your work on screen
    pygame.display.flip()

    clock.tick(60)  # limits FPS to 60

pygame.quit()