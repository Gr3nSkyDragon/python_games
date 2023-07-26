import pygame
import random
import string

pygame.init()

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
INPUT_VC = (239, 239, 239)
GEN_CVC = (239, 239, 239)
MODE_BTN_COLOR = (180, 175, 170)  # Change this color to your desired color for the mode changing button
NEW_WORD_BTN_COLOR = (216, 141, 14)  # This color is for the "New Word" button

# Create the screen
screen_width, screen_height = 1280, 720
screen = pygame.display.set_mode((screen_width, screen_height), pygame.RESIZABLE)
pygame.display.set_caption('Word Maker v.2.0')
Icon = pygame.image.load('resources/icon/robot.png')
pygame.display.set_icon(Icon)
background_image = pygame.image.load('resources/background/television.jpg')  
background_image = pygame.transform.scale(background_image, (screen_width, screen_height))

# Function to generate a random vowel
def generate_vowel():
    vowels = 'aeiou'
    return random.choice(vowels)

# Function to generate a random consonant
def generate_consonant():
    consonants = ''.join(set(string.ascii_lowercase) - set('aeiou'))
    return random.choice(consonants)

# Function to validate user input for -VC mode
def validate_vc_input(input_text):
    if len(input_text) == 2:
        vowel, consonant = input_text.lower()
        if vowel in 'aeiou' and consonant in ''.join(set(string.ascii_lowercase) - set('aeiou')):
            return True
    return False

def validate_cc_input(input_text):
    if len(input_text) == 2:
        consonant1, consonant2 = input_text.lower()
        if consonant1 in ''.join(set(string.ascii_lowercase) - set('aeiou')) and consonant2 in ''.join(set(string.ascii_lowercase) - set('aeiou')):
            return True
    elif len(input_text) == 3:  # For three-letter input
        consonant1, consonant2, vowel = input_text.lower()
        if consonant1 in ''.join(set(string.ascii_lowercase) - set('aeiou')) and consonant2 in ''.join(set(string.ascii_lowercase) - set('aeiou')) and vowel in 'aeiou':
            return True
    return False

def validate_cc_input_reverse(input_text):
    if len(input_text) == 2:
        consonant1, consonant2 = input_text.lower()
        if consonant1 in ''.join(set(string.ascii_lowercase) - set('aeiou')) and consonant2 in ''.join(set(string.ascii_lowercase) - set('aeiou')):
            return True
    elif len(input_text) == 3:  # For three-letter input
        vowel, consonant1, consonant2 = input_text.lower()
        if vowel in 'aeiou' and consonant1 in ''.join(set(string.ascii_lowercase) - set('aeiou')) and consonant2 in ''.join(set(string.ascii_lowercase) - set('aeiou')):
            return True
    return False

def validate_tri_input(input_text):
    return len(input_text) == 3

def main(font):
    running = True
    user_input = ""
    current_vc = ""
    generated_cvc = ""
    mode = "-VC"
    global background_image

    # Initial rendering of the text surfaces
    user_input_text = font.render("Input " + mode + ": " + user_input, True, INPUT_VC)
    current_vc_text = font.render("Current " + mode + ": " + current_vc, True, BLACK)
    generated_cvc_font = pygame.font.SysFont(None, int(0.30 * screen.get_height()))
    generated_cvc_text = generated_cvc_font.render(generated_cvc, True, GEN_CVC)
    button_text_font = pygame.font.SysFont(None, int(0.1 * screen.get_height()))  # Increased font size for the button text
    new_word_button_text = small_font.render("New Word", True, BLACK)
    mode_switch_button_text = small_font.render(mode, True, BLACK)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if mode == "-VC":
                        if validate_vc_input(user_input):
                            current_vc = user_input.upper()
                            generated_cvc = generate_consonant().lower() + current_vc.lower()
                            generated_cvc_text = generated_cvc_font.render(generated_cvc, True, GEN_CVC)
                    elif mode == "CC-":
                        if len(user_input) == 2:  # For two-letter input (as before)
                            if validate_cc_input(user_input):  # Correct the validation function
                                current_vc = user_input.upper()
                                generated_cvc = user_input.lower() + generate_vowel() + generate_consonant().lower()
                                generated_cvc_text = generated_cvc_font.render(generated_cvc, True, GEN_CVC)
                        elif len(user_input) == 3:  # For three-letter input
                            consonant1, consonant2, vowel = user_input.lower()
                            if consonant1 in ''.join(set(string.ascii_lowercase) - set('aeiou')) and consonant2 in ''.join(set(string.ascii_lowercase) - set('aeiou')) and vowel in 'aeiou':
                                current_vc = user_input.upper()
                                generated_cvc = user_input.lower() + generate_consonant().lower()
                                generated_cvc_text = generated_cvc_font.render(generated_cvc, True, GEN_CVC)
                    elif mode == "-CC":
                        if len(user_input) == 2:  # For two-letter input (as before)
                            if validate_cc_input_reverse(user_input):  # Correct the validation function
                                current_vc = user_input.upper()
                                generated_cvc = generate_consonant().lower() + generate_vowel() + user_input.lower()
                                generated_cvc_text = generated_cvc_font.render(generated_cvc, True, GEN_CVC)
                        elif len(user_input) == 3:  # For three-letter input
                            vowel, consonant1, consonant2 = user_input.lower()
                            if vowel in 'aeiou' and consonant1 in ''.join(set(string.ascii_lowercase) - set('aeiou')) and consonant2 in ''.join(set(string.ascii_lowercase) - set('aeiou')):
                                current_vc = user_input.upper()
                                generated_cvc = generate_consonant().lower() + user_input.lower()
                                generated_cvc_text = generated_cvc_font.render(generated_cvc, True, GEN_CVC)
                    elif mode == "TRI-":
                        if validate_tri_input(user_input):
                            current_vc = user_input.upper()
                            generated_cvc = user_input.lower() + generate_vowel().lower() + generate_consonant().lower()
                            generated_cvc_text = generated_cvc_font.render(generated_cvc, True, GEN_CVC)

                    elif mode == "-TRI":
                        if validate_tri_input(user_input):
                            current_vc = user_input.upper()
                            consonant = generate_consonant().lower()
                            vowel = generate_vowel().lower()
                            generated_cvc = consonant + vowel + user_input.lower()
                            generated_cvc_text = generated_cvc_font.render(generated_cvc, True, GEN_CVC)
                elif event.key == pygame.K_BACKSPACE:
                    user_input = user_input[:-1]
                    # Update the user input text here
                    user_input_text = font.render("Input " + mode + ": " + user_input, True, INPUT_VC)

                else:
                    user_input += event.unicode
                    # Update the user input text here
                    user_input_text = font.render("Input " + mode + ": " + user_input, True, INPUT_VC)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Check if the "New Word" button is clicked
                if (
                    new_word_button_text_x <= event.pos[0] <= new_word_button_text_x + new_word_button_text.get_width()
                    and new_word_button_text_y <= event.pos[1] <= new_word_button_text_y + new_word_button_text.get_height()
                ):
                    if mode == "-VC":
                        current_vc = user_input.upper()
                        generated_cvc = generate_consonant().lower() + current_vc.lower()
                        generated_cvc_text = generated_cvc_font.render(generated_cvc, True, GEN_CVC)
                    elif mode == "CC-":
                        if len(user_input) == 2:  # For two-letter input (as before)
                            if validate_cc_input(user_input):  # Correct the validation function
                                current_vc = user_input.upper()
                                generated_cvc = user_input.lower() + generate_vowel() + generate_consonant().lower()
                                generated_cvc_text = generated_cvc_font.render(generated_cvc, True, GEN_CVC)
                        elif len(user_input) == 3:  # For three-letter input
                            consonant1, consonant2, vowel = user_input.lower()
                            if consonant1 in ''.join(set(string.ascii_lowercase) - set('aeiou')) and consonant2 in ''.join(set(string.ascii_lowercase) - set('aeiou')) and vowel in 'aeiou':
                                current_vc = user_input.upper()
                                generated_cvc = user_input.lower() + generate_consonant().lower()
                                generated_cvc_text = generated_cvc_font.render(generated_cvc, True, GEN_CVC)
                    elif mode == "-CC":
                        if len(user_input) == 2:  # For two-letter input (as before)
                            if validate_cc_input_reverse(user_input):  # Correct the validation function
                                current_vc = user_input.upper()
                                generated_cvc = generate_consonant().lower() + generate_vowel() + user_input.lower()
                                generated_cvc_text = generated_cvc_font.render(generated_cvc, True, GEN_CVC)
                        elif len(user_input) == 3:  # For three-letter input
                            vowel, consonant1, consonant2 = user_input.lower()
                            if vowel in 'aeiou' and consonant1 in ''.join(set(string.ascii_lowercase) - set('aeiou')) and consonant2 in ''.join(set(string.ascii_lowercase) - set('aeiou')):
                                current_vc = user_input.upper()
                                generated_cvc = generate_consonant().lower() + user_input.lower()
                                generated_cvc_text = generated_cvc_font.render(generated_cvc, True, GEN_CVC)
                    elif mode == "TRI-":
                        if validate_tri_input(user_input):
                            current_vc = user_input.upper()
                            generated_cvc = user_input.lower() + generate_vowel().lower() + generate_consonant().lower()
                            generated_cvc_text = generated_cvc_font.render(generated_cvc, True, GEN_CVC)

                    elif mode == "-TRI":
                        if validate_tri_input(user_input):
                            current_vc = user_input.upper()
                            consonant = generate_consonant().lower()
                            vowel = generate_vowel().lower()
                            generated_cvc = consonant + vowel + user_input.lower()
                            generated_cvc_text = generated_cvc_font.render(generated_cvc, True, GEN_CVC)


                # Check if the "Switch Mode" button is clicked
                elif (
                    mode_switch_button_text_x <= event.pos[0] <= mode_switch_button_text_x + mode_switch_button_text.get_width()
                    and mode_switch_button_text_y <= event.pos[1] <= mode_switch_button_text_y + mode_switch_button_text.get_height()
                ):
                    if mode == "-VC":
                        mode = "CC-"
                    elif mode == "CC-":
                        mode = "-CC"
                    elif mode == "-CC":
                        mode = "TRI-"
                    elif mode == "TRI-":
                        mode = "-TRI"
                    elif mode == "-TRI":
                        mode = "-VC"
                    user_input = ""
                    current_vc = ""
                    generated_cvc = ""
                    generated_cvc_text = generated_cvc_font.render(generated_cvc, True, GEN_CVC)
                    user_input_text = font.render("Input " + mode + ": " + user_input, True, INPUT_VC)
                    current_vc_text = font.render("Current " + mode + ": " + current_vc, True, BLACK)
                    mode_switch_button_text = small_font.render(mode, True, BLACK)
                    user_input = ""
                    current_vc = ""
                    generated_cvc = ""
                    generated_cvc_text = generated_cvc_font.render(generated_cvc, True, GEN_CVC)
                    user_input_text = font.render("Input " + mode + ": " + user_input, True, INPUT_VC)
                    current_vc_text = font.render("Current " + mode + ": " + current_vc, True, BLACK)

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
        new_word_button_text_x = int(0.85 * screen_width) - int(0.5 * new_word_button_text.get_width())
        new_word_button_text_y = int(0.99 * screen_height) - new_word_button_text.get_height()
        mode_switch_button_width = int(0.25 * new_word_button_text.get_width())  # Adjust size to a fourth of the "New Word" button
        mode_switch_button_height = int(0.25 * new_word_button_text.get_height())  # Adjust size to a fourth of the "New Word" button
        mode_switch_button_text_x = int(0.775 * screen_width) - int(0.5 * mode_switch_button_width)  # Move the button to about 60% from the left edge
        mode_switch_button_text_y = int(0.245 * screen_height) - int(0.5 * mode_switch_button_height)  # Move the button to about 40% down from the top edge


        # Update the text surfaces
        user_input_text = font.render("Input " + mode + ": " + user_input, True, INPUT_VC)
        current_vc_text = font.render("Current " + mode + ": " + current_vc, True, BLACK)
        generated_cvc_text = generated_cvc_font.render(generated_cvc, True, GEN_CVC)
        new_word_button_text = small_font.render("New Word", True, BLACK)
        mode_switch_button_text = small_font.render(mode, True, BLACK)

        # Render the user input
        screen.blit(user_input_text, (input_text_x, input_text_y))

        # Render the current VC word
        screen.blit(current_vc_text, (current_vc_text_x, current_vc_text_y))

        # Render the generated CVC word (with a bigger font)
        screen.blit(generated_cvc_text, (generated_cvc_x, generated_cvc_y))

        # Render the "New Word" button
        pygame.draw.rect(screen, NEW_WORD_BTN_COLOR, (new_word_button_text_x - 5, new_word_button_text_y - 5, new_word_button_text.get_width() + 10, new_word_button_text.get_height() + 10))
        pygame.draw.rect(screen, BLACK, (new_word_button_text_x - 5, new_word_button_text_y - 5, new_word_button_text.get_width() + 10, new_word_button_text.get_height() + 10), 2)
        screen.blit(new_word_button_text, (new_word_button_text_x, new_word_button_text_y))

        # Render the mode switch button
        pygame.draw.rect(screen, MODE_BTN_COLOR, (mode_switch_button_text_x - 5, mode_switch_button_text_y - 5, mode_switch_button_text.get_width() + 10, mode_switch_button_text.get_height() + 10))
        pygame.draw.rect(screen, BLACK, (mode_switch_button_text_x - 5, mode_switch_button_text_y - 5, mode_switch_button_text.get_width() + 10, mode_switch_button_text.get_height() + 10), 2)
        screen.blit(mode_switch_button_text, (mode_switch_button_text_x, mode_switch_button_text_y))

        # Update the display
        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    # Set the initial font
    font = pygame.font.SysFont(None, int(0.07 * screen.get_height()))
    small_font = pygame.font.SysFont(None, int(0.1 * screen.get_height()))

    main(font)
