# Example file showing a basic pygame "game loop"
import pygame
import sys
import random

#Window boilerplate
pygame.init()
pygame.display.set_caption('Alphabet Blaster v.1.1')
Icon = pygame.image.load('apple.png')
pygame.display.set_icon(Icon)
pygame.font.init()
game_font = pygame.font.SysFont('Comic Sans MS', 120)
screen = pygame.display.set_mode((1280, 720),pygame.RESIZABLE)
clock = pygame.time.Clock()
running = True

#Button variables
color = (255,255,255)
color_light = (170,170,170)
color_dark = (100,100,100)
background = (115,150,190)
  
width = screen.get_width()
height = screen.get_height()
  
# defining a font
smallfont = pygame.font.SysFont('Corbel',35)
text = smallfont.render('blast!' , True , color)
answer_text = smallfont.render('reveal', True, color)

# Image dictionary
#image_dict = {
    #'a': pygame.image.load('rustic_alphabet/a.png'),
    #'b': pygame.image.load('rustic_alphabet/b.png'),
    #'c': pygame.image.load('rustic_alphabet/c.png'),
    #'d': pygame.image.load('rustic_alphabet/d.png'),
    #'e': pygame.image.load('rustic_alphabet/e.png'),
    #'f': pygame.image.load('rustic_alphabet/f.png'),
    #'g': pygame.image.load('rustic_alphabet/g.png'),
    #'h': pygame.image.load('rustic_alphabet/h.png'),
    #'i': pygame.image.load('rustic_alphabet/i.png'),
    #'j': pygame.image.load('rustic_alphabet/j.png'),
    #'k': pygame.image.load('rustic_alphabet/k.png'),
    #'l': pygame.image.load('rustic_alphabet/l.png'),
    #'m': pygame.image.load('rustic_alphabet/m.png'),
    #'n': pygame.image.load('rustic_alphabet/n.png'),
    #'o': pygame.image.load('rustic_alphabet/o.png'),
    #'p': pygame.image.load('rustic_alphabet/p.png'),
    #'q': pygame.image.load('rustic_alphabet/q.png'),
    #'r': pygame.image.load('rustic_alphabet/r.png'),
    #'s': pygame.image.load('rustic_alphabet/s.png'),
    #'t': pygame.image.load('rustic_alphabet/t.png'),
    #'u': pygame.image.load('rustic_alphabet/u.png'),
    #'v': pygame.image.load('rustic_alphabet/v.png'),
    #'w': pygame.image.load('rustic_alphabet/w.png'),
    #'x': pygame.image.load('rustic_alphabet/x.png'),
    #'y': pygame.image.load('rustic_alphabet/y.png'),
    #'z': pygame.image.load('rustic_alphabet/z.png'),
    #'?': pygame.image.load('question2.png'),
    # Add more images for other letters
#}

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
        if event.type == pygame.MOUSEBUTTONDOWN:            
            if width*0.75 <= mouse[0] <= width*0.75+140 and height*0.75 <= mouse[1] <= height*0.75+40:
                letter_game = lettergen(letter_case)
                hidden_letter_game = letter_game.copy()
                engine(letter_game,set_difficulty)
                hide_toggle = 0
            elif width*0.10 <= mouse[0] <= width*0.10+140 and height*0.75 <= mouse[1] <= height*0.75+40:
                hide_toggle = 1 - hide_toggle
            elif width*0.9 <= mouse[0] <= width*0.9+39 and height*0.05 <= mouse[1] <= height*0.05+40:   
                letter_case = 1 - letter_case
            elif width*0.05 <= mouse[0] <= width*0.05+39 and height*0.05 <= mouse[1] <= height*0.05+40:
                set_difficulty = 1
            elif width*0.05+40 <= mouse[0] <= width*0.05+79 and height*0.05 <= mouse[1] <= height*0.05+40:
                set_difficulty = 2
            elif width*0.05+80 <= mouse[0] <= width*0.05+119 and height*0.05 <= mouse[1] <= height*0.05+40:
                set_difficulty = 3
            elif width*0.05+120 <= mouse[0] <= width*0.05+159 and height*0.05 <= mouse[1] <= height*0.05+40:
                set_difficulty = 5
                 
    # fills the screen with a color
    screen.fill(background)
      
    # stores the (x,y) coordinates into
    # the variable as a tuple
    mouse = pygame.mouse.get_pos()
      
    # if mouse is hovered on a button it
    # changes to lighter shade
    #blast
    if width*0.75 <= mouse[0] <= width*0.75+140 and height*0.75 <= mouse[1] <= height*0.75+40:
        pygame.draw.rect(screen,color_light,[width*0.75,height*0.75,140,40])
        pygame.draw.rect(screen,color_dark,[width*0.10,height*0.75,140,40])
        pygame.draw.rect(screen,(190,0,250),[width*0.9,height*0.05,40,40])
        pygame.draw.rect(screen,(60,250,60),[width*0.05,height*0.05,40,40])
        pygame.draw.rect(screen,(230,250,60),[width*0.05+40,height*0.05,40,40])
        pygame.draw.rect(screen,(250,160,60),[width*0.05+80,height*0.05,40,40])
        pygame.draw.rect(screen,(250,60,60),[width*0.05+120,height*0.05,40,40])
    
    #reveal
    elif width*0.10 <= mouse[0] <= width*0.10+140 and height*0.75 <= mouse[1] <= height*0.75+40:
        pygame.draw.rect(screen,color_light,[width*0.10,height*0.75,140,40])
        pygame.draw.rect(screen,color_dark,[width*0.75,height*0.75,140,40])
        pygame.draw.rect(screen,(190,0,250),[width*0.9,height*0.05,40,40])
        pygame.draw.rect(screen,(60,250,60),[width*0.05,height*0.05,40,40])
        pygame.draw.rect(screen,(230,250,60),[width*0.05+40,height*0.05,40,40])
        pygame.draw.rect(screen,(250,160,60),[width*0.05+80,height*0.05,40,40])
        pygame.draw.rect(screen,(250,60,60),[width*0.05+120,height*0.05,40,40])
    #case change
    elif width*0.9 <= mouse[0] <= width*0.9+39 and height*0.05 <= mouse[1] <= height*0.05+39:
        pygame.draw.rect(screen,color_dark,[width*0.10,height*0.75,140,40])
        pygame.draw.rect(screen,color_dark,[width*0.75,height*0.75,140,40])
        pygame.draw.rect(screen,(170,0,230),[width*0.9,height*0.05,40,40])
        pygame.draw.rect(screen,(60,250,60),[width*0.05,height*0.05,40,40])
        pygame.draw.rect(screen,(230,250,60),[width*0.05+40,height*0.05,40,40])
        pygame.draw.rect(screen,(250,160,60),[width*0.05+80,height*0.05,40,40])
        pygame.draw.rect(screen,(250,60,60),[width*0.05+120,height*0.05,40,40])
    #difficulty buttons 
    elif width*0.05 <= mouse[0] <= width*0.05+39 and height*0.05 <= mouse[1] <= height*0.05+39:
        pygame.draw.rect(screen,color_dark,[width*0.75,height*0.75,140,40])
        pygame.draw.rect(screen,color_dark,[width*0.10,height*0.75,140,40])
        pygame.draw.rect(screen,(190,0,250),[width*0.9,height*0.05,40,40])
        pygame.draw.rect(screen,(50,230,50),[width*0.05,height*0.05,40,40])
        pygame.draw.rect(screen,(230,250,60),[width*0.05+40,height*0.05,40,40])
        pygame.draw.rect(screen,(250,160,60),[width*0.05+80,height*0.05,40,40])
        pygame.draw.rect(screen,(250,60,60),[width*0.05+120,height*0.05,40,40])
    
    elif width*0.05+40 <= mouse[0] <= width*0.05+79 and height*0.05 <= mouse[1] <= height*0.05+39:
        pygame.draw.rect(screen,color_dark,[width*0.75,height*0.75,140,40])
        pygame.draw.rect(screen,color_dark,[width*0.10,height*0.75,140,40])
        pygame.draw.rect(screen,(190,0,250),[width*0.9,height*0.05,40,40])
        pygame.draw.rect(screen,(60,250,60),[width*0.05,height*0.05,40,40])
        pygame.draw.rect(screen,(215,235,50),[width*0.05+40,height*0.05,40,40])
        pygame.draw.rect(screen,(250,160,60),[width*0.05+80,height*0.05,40,40])
        pygame.draw.rect(screen,(250,60,60),[width*0.05+120,height*0.05,40,40])
        
    elif width*0.05+80 <= mouse[0] <= width*0.05+119 and height*0.05 <= mouse[1] <= height*0.05+39:
        pygame.draw.rect(screen,color_dark,[width*0.75,height*0.75,140,40])
        pygame.draw.rect(screen,color_dark,[width*0.10,height*0.75,140,40])
        pygame.draw.rect(screen,(190,0,250),[width*0.9,height*0.05,40,40])
        pygame.draw.rect(screen,(60,250,60),[width*0.05,height*0.05,40,40])
        pygame.draw.rect(screen,(230,250,60),[width*0.05+40,height*0.05,40,40])
        pygame.draw.rect(screen,(235,145,50),[width*0.05+80,height*0.05,40,40])
        pygame.draw.rect(screen,(250,60,60),[width*0.05+120,height*0.05,40,40])
    
    elif width*0.05+120 <= mouse[0] <= width*0.05+159 and height*0.05 <= mouse[1] <= height*0.05+39:
        pygame.draw.rect(screen,color_dark,[width*0.75,height*0.75,140,40])
        pygame.draw.rect(screen,color_dark,[width*0.10,height*0.75,140,40])
        pygame.draw.rect(screen,(190,0,250),[width*0.9,height*0.05,40,40])
        pygame.draw.rect(screen,(60,250,60),[width*0.05,height*0.05,40,40])
        pygame.draw.rect(screen,(230,250,60),[width*0.05+40,height*0.05,40,40])
        pygame.draw.rect(screen,(250,160,60),[width*0.05+80,height*0.05,40,40])
        pygame.draw.rect(screen,(230,50,50),[width*0.05+120,height*0.05,40,40])
    
    else:
        pygame.draw.rect(screen,color_dark,[width*0.75,height*0.75,140,40])
        pygame.draw.rect(screen,color_dark,[width*0.10,height*0.75,140,40])
        pygame.draw.rect(screen,(190,0,250),[width*0.9,height*0.05,40,40])
        pygame.draw.rect(screen,(60,250,60),[width*0.05,height*0.05,40,40])
        pygame.draw.rect(screen,(230,250,60),[width*0.05+40,height*0.05,40,40])
        pygame.draw.rect(screen,(250,160,60),[width*0.05+80,height*0.05,40,40])
        pygame.draw.rect(screen,(250,60,60),[width*0.05+120,height*0.05,40,40])
        
    # superimposing the text onto our button
    screen.blit(text , (width*0.75+32,height*0.75+5))
    screen.blit(answer_text, (width*0.10+29,height*0.75+5))
    
    # Calculate the size for each picture based on the number of letters
    #picture_size = min((width * 0.8) // len(letter_game), height * 0.4)
    
    #Draw letters
    if hide_toggle == 0:
        text_surface = game_font.render(letter_game[0] + ' ' + letter_game[1] + ' ' +  letter_game[2] + ' ' +  letter_game[3] + ' ' +  letter_game[4] + ' ' +  letter_game[5], False, (229, 229, 19))
        screen.blit(text_surface, (340,280))
        #for i, letter in enumerate(letter_game):
            #pygame.draw.rect(screen, background, (width * 0.1 + picture_size * i, height * 0.35, picture_size, picture_size))
            #revealed_image = pygame.transform.scale(image_dict[letter], (int(picture_size), int(picture_size)))
            #screen.blit(revealed_image, (width * 0.1 + picture_size * i, height * 0.35))
    
    elif hide_toggle == 1:
        text_surface = game_font.render(hidden_letter_game[0] + ' ' + hidden_letter_game[1] + ' ' +  hidden_letter_game[2] + ' ' +  hidden_letter_game[3] + ' ' +  hidden_letter_game[4] + ' ' +  hidden_letter_game[5], False, (229, 229, 19))
        screen.blit(text_surface, (340,280))
        #for i, letter in enumerate(hidden_letter_game):
            #pygame.draw.rect(screen, background, (width * 0.1 + picture_size * i, height * 0.35, picture_size, picture_size))
            #hidden_image = pygame.transform.scale(image_dict[letter], (int(picture_size), int(picture_size)))
            #screen.blit(hidden_image, (width * 0.1 + picture_size * i, height * 0.35))
    
    else:
        text_surface = game_font.render('You broke something, nerd')
    
    # updates the frames of the game
    pygame.display.update()
    
    # flip() the display to put your work on screen
    pygame.display.flip()

    clock.tick(60)  # limits FPS to 60

pygame.quit()