import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Screen settings
width, height = 1280, 720
screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)
pygame.display.set_caption("Guess the Letters!")

# Colors
color_light = (170, 170, 170)
color_dark = (100, 100, 100)
color = (255, 255, 255)
background = (40, 120, 50)

# Fonts
game_font = pygame.font.Font(None, 50)
button_font = pygame.font.Font(None, 30)

# Image dictionary
image_dict = {
    'a': pygame.image.load('rustic_alphabet/a.png'),
    'b': pygame.image.load('rustic_alphabet/b.png'),
    'c': pygame.image.load('rustic_alphabet/c.png'),
    'd': pygame.image.load('rustic_alphabet/d.png'),
    'e': pygame.image.load('rustic_alphabet/e.png'),
    'f': pygame.image.load('rustic_alphabet/f.png'),
    'g': pygame.image.load('rustic_alphabet/g.png'),
    'h': pygame.image.load('rustic_alphabet/h.png'),
    'i': pygame.image.load('rustic_alphabet/i.png'),
    'j': pygame.image.load('rustic_alphabet/j.png'),
    'k': pygame.image.load('rustic_alphabet/k.png'),
    'l': pygame.image.load('rustic_alphabet/l.png'),
    'm': pygame.image.load('rustic_alphabet/m.png'),
    'n': pygame.image.load('rustic_alphabet/n.png'),
    'o': pygame.image.load('rustic_alphabet/o.png'),
    'p': pygame.image.load('rustic_alphabet/p.png'),
    'q': pygame.image.load('rustic_alphabet/q.png'),
    'r': pygame.image.load('rustic_alphabet/r.png'),
    's': pygame.image.load('rustic_alphabet/s.png'),
    't': pygame.image.load('rustic_alphabet/t.png'),
    'u': pygame.image.load('rustic_alphabet/u.png'),
    'v': pygame.image.load('rustic_alphabet/v.png'),
    'w': pygame.image.load('rustic_alphabet/w.png'),
    'x': pygame.image.load('rustic_alphabet/x.png'),
    'y': pygame.image.load('rustic_alphabet/y.png'),
    'z': pygame.image.load('rustic_alphabet/z.png'),
    '?': pygame.image.load('question2.png'),
    # Add more images for other letters
}

# Generate random letters for the game
def lettergen():
    alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
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
    
# Game loop variables
running = True
clock = pygame.time.Clock()

# Button positions and difficulty values
button_positions = {
    'blast': (width * 0.25, height * 0.8),
    'reveal': (width * 0.5, height * 0.8),
    'easy': (width * 0.1, height * 0.1),
    'medium': (width * 0.3, height * 0.1),
    'hard': (width * 0.5, height * 0.1),
    'mad': (width * 0.7, height * 0.1)
}

# Colors for difficulty buttons
color_easy = (60,250,60)    # Green
color_medium = (230,250,60)  # Yellow
color_hard = (250,160,60)      # Orange
color_mad = (250,60,60)       # Red

difficulty_values = {
    'easy': 1,
    'medium': 2,
    'hard': 3,
    'mad': 5
}

hide_toggle = 0
set_difficulty = 3
letter_game = lettergen()
hidden_letter_game = letter_game.copy()
hidden_letter_game = engine(hidden_letter_game, set_difficulty)

# Main game loop
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            for button, pos in button_positions.items():
                if pos[0] - 10 <= mouse_x <= pos[0] + 190 and pos[1] - 10 <= mouse_y <= pos[1] + 40:
                    if event.button == 1:  # Left mouse button
                        if button == 'blast':
                            hide_toggle = 1
                            letter_game = lettergen()
                            hidden_letter_game = letter_game.copy()
                            letter_game = engine(letter_game, set_difficulty)
                        elif button == 'reveal':
                            hide_toggle = 1 - hide_toggle
                        elif button in difficulty_values:
                            set_difficulty = difficulty_values[button]

    screen.fill(background)

   # Calculate the size for each picture based on the number of letters
    picture_size = min((width * 0.8) // len(letter_game), height * 0.4)

    # Draw hidden letters/images if hide_toggle is 0
    if hide_toggle == 0:
        for i, letter in enumerate(hidden_letter_game):
            pygame.draw.rect(screen, background, (width * 0.1 + picture_size * i, height * 0.35, picture_size, picture_size))
            hidden_image = pygame.transform.scale(image_dict[letter], (int(picture_size), int(picture_size)))
            screen.blit(hidden_image, (width * 0.1 + picture_size * i, height * 0.35))

    # Draw revealed letters/images if hide_toggle is 1
    if hide_toggle == 1:
        for i, letter in enumerate(letter_game):
            pygame.draw.rect(screen, background, (width * 0.1 + picture_size * i, height * 0.35, picture_size, picture_size))
            revealed_image = pygame.transform.scale(image_dict[letter], (int(picture_size), int(picture_size)))
            screen.blit(revealed_image, (width * 0.1 + picture_size * i, height * 0.35))
            
    # Draw buttons
    for button, pos in button_positions.items():
        if button == 'blast':
            if hide_toggle == 1:
                pygame.draw.rect(screen, color_light, (pos[0] - 10, pos[1] - 10, 140, 40))
            else:
                pygame.draw.rect(screen, color_dark, (pos[0] - 10, pos[1] - 10, 140, 40))
            screen.blit(button_font.render(button.capitalize(), True, (0, 0, 0)), (pos[0] + 30, pos[1] + 10))
        elif button == 'reveal':
            pygame.draw.rect(screen, color_light, (pos[0] - 10, pos[1] - 10, 140, 40))
            screen.blit(button_font.render(button.capitalize(), True, (0, 0, 0)), (pos[0] + 20, pos[1] + 10))
        elif button in difficulty_values:
            if button == 'easy':
                color = color_easy
            elif button == 'medium':
                color = color_medium
            elif button == 'hard':
                color = color_hard
            elif button == 'mad':
                color = color_mad

            if set_difficulty == difficulty_values[button]:
                pygame.draw.rect(screen, color, (pos[0] - 10, pos[1] - 10, 100, 40))
            else:
                pygame.draw.rect(screen, color_light, (pos[0] - 10, pos[1] - 10, 100, 40))
            screen.blit(button_font.render(button.capitalize(), True, (0, 0, 0)), (pos[0] + 10, pos[1] + 10))


    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()