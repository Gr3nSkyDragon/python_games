import pygame
import random
import string

pygame.init()

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
INPUT_VC = (239, 239, 239)
GEN_CVC = (239,239,239)
BTN_COLOR = (216, 141, 14)

# Create the screen
screen_width, screen_height = 1280, 720
screen = pygame.display.set_mode((screen_width, screen_height), pygame.RESIZABLE)
Icon = pygame.image.load('robot.png')
pygame.display.set_icon(Icon)
background_image = pygame.image.load('television.jpg')  
background_image = pygame.transform.scale(background_image, (screen_width, screen_height))

# Function to generate a random consonant
def generate_consonant():
    consonants = ''.join(set(string.ascii_lowercase) - set('aeiou'))
    return random.choice(consonants)

# Function to validate user input (should be a vowel followed by a consonant)
def validate_input(input_text):
    if len(input_text) == 2:
        vowel, consonant = input_text.lower()
        if vowel in 'aeiou' and consonant in ''.join(set(string.ascii_lowercase) - set('aeiou')):
            return True
    return False

def main(font):
    running = True
    user_input = ""
    current_vc = ""
    generated_cvc = ""
    generate_cvc = False
    global background_image

    # Initial rendering of the text surfaces
    user_input_text = font.render("Input (V+C): -" + user_input, True, INPUT_VC)
    current_vc_text = font.render("Current -VC: -" + current_vc, True, BLACK)
    generated_cvc_font = pygame.font.SysFont(None, int(0.30 * screen.get_height()))
    generated_cvc_text = generated_cvc_font.render(generated_cvc, True, GEN_CVC)
    button_text_font = pygame.font.SysFont(None, int(0.1 * screen.get_height()))  # Increased font size for the button text
    button_text = small_font.render("New CVC", True, BLACK)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and validate_input(user_input):
                    current_vc = user_input.upper()
                    generate_cvc = True
                elif event.key == pygame.K_BACKSPACE:
                    user_input = user_input[:-1]
                else:
                    user_input += event.unicode

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if generate_cvc:
                    generated_cvc = generate_consonant().lower() + current_vc.lower()
                    generated_cvc_text = generated_cvc_font.render(generated_cvc, True, GEN_CVC)
                    generate_cvc = False

        # Clear the screen
        screen.fill(WHITE)
        screen_width, screen_height = pygame.display.get_surface().get_size()
        background_image = pygame.transform.scale(background_image, (screen_width, screen_height))
        screen.blit(background_image, (0, 0))

        # Get updated screen dimensions
        screen_width, screen_height = pygame.display.get_surface().get_size()
        

        # Calculate percentage-based coordinates for elements
        input_text_x = int(0.01 * screen_width)
        input_text_y = int(0.01 * screen_height)
        current_vc_text_x = int(0.99 * screen_width) - current_vc_text.get_width()
        current_vc_text_y = int(0.01 * screen_height)
        generated_cvc_x = int(0.43 * screen_width) - int(0.5 * generated_cvc_text.get_width())
        generated_cvc_y = int(0.45 * screen_height) - int(0.5 * generated_cvc_text.get_height())
        button_text_x = int(0.99 * screen_width) - button_text.get_width()
        button_text_y = int(0.99 * screen_height) - button_text.get_height()

        # Update the text surfaces
        user_input_text = font.render("Input (V+C): -" + user_input, True, INPUT_VC)
        current_vc_text = font.render("Current -VC: -" + current_vc, True, BLACK)
        generated_cvc_text = generated_cvc_font.render(generated_cvc, True, GEN_CVC)
        button_text = small_font.render("New CVC", True, INPUT_VC)

        # Render the user input
        screen.blit(user_input_text, (input_text_x, input_text_y))

        # Render the current VC word
        screen.blit(current_vc_text, (current_vc_text_x, current_vc_text_y))

        # Render the generated CVC word (with a bigger font)
        screen.blit(generated_cvc_text, (generated_cvc_x, generated_cvc_y))

        # Render the generate button
        pygame.draw.rect(screen, BTN_COLOR, (button_text_x - 5, button_text_y - 5, button_text.get_width() + 10, button_text.get_height() + 10))
        pygame.draw.rect(screen, BLACK, (button_text_x - 5, button_text_y - 5, button_text.get_width() + 10, button_text.get_height() + 10), 2)
        screen.blit(button_text, (button_text_x, button_text_y))

        # Check if the button is clicked
        mouse_pos = pygame.mouse.get_pos()
        if button_text.get_rect(topleft=(button_text_x, button_text_y)).collidepoint(mouse_pos):
            if pygame.mouse.get_pressed()[0]:  # Check for left mouse button press
                generate_cvc = True

        # Update the display
        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    # Set the initial font
    font = pygame.font.SysFont(None, int(0.07 * screen.get_height()))
    small_font = pygame.font.SysFont(None, int(0.1 * screen.get_height()))

    main(font)