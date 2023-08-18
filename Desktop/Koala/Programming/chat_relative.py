import pygame
import os
import random
import string
import sys

# Initialize Pygame
pygame.init()
pygame.display.set_caption('Star CVC v.1.0')
Icon = pygame.image.load('resources/icon/star.jpg')
pygame.display.set_icon(Icon)

# Set up display
screen_width = 1280
screen_height = 720
screen = pygame.display.set_mode((screen_width, screen_height), pygame.RESIZABLE)  # Make the screen resizable

# Get the path to the folder containing this script
#script_folder = os.path.dirname(os.path.abspath(__file__))
script_folder = os.getcwd()

absolute_path = os.path.abspath(__file__)
print("Absolute path:", absolute_path)

# Specify the folder containing phonics words
phonics_words_folder = os.path.join(sys._MEIPASS, "resources/star/phonics words")

# Get a list of folder names in the "phonics words" folder
folder_names = [name for name in os.listdir(phonics_words_folder) if os.path.isdir(os.path.join(phonics_words_folder, name))]

# Choose the first folder name
if folder_names:
    selected_folder_name = folder_names[0]
else:
    selected_folder_name = "No folders found"

# Get the path to the selected sub-folder
selected_subfolder_path = os.path.join(phonics_words_folder, selected_folder_name)

# Get a list of image filenames in the selected sub-folder
image_filenames = [name for name in os.listdir(selected_subfolder_path) if name.lower().endswith(('.png', '.jpg', '.jpeg', '.gif'))]

# Choose a random image filename
if image_filenames:
    selected_image_filename = random.choice(image_filenames)
    image_path = os.path.join(selected_subfolder_path, selected_image_filename)
    original_image = pygame.image.load(image_path)
    max_image_size = int(min(screen_width * 0.6, screen_height * 0.5))  # Limit to 60% width or 50% height
    image = pygame.transform.scale(original_image, (max_image_size, max_image_size))
    image_first_letter = selected_image_filename[0].upper()  # Get the first letter of the image filename
else:
    image = None

# Define colors
white = (162,228,184)
black = (0, 0, 0)
red = (255, 0, 0)
green = (0, 255, 0)
gray_blue = (173, 216, 230)  # A shade of blue-gray

# Define folder index
index = 0

# Load font
game_font_size = int(0.26 * pygame.display.Info().current_h)
font = pygame.font.Font(None, game_font_size)

# Define relative dimensions
text_y_percent = 0.64
image_y_percent = 0.3
button_y_percent = 0.8
next_button_y_percent = 1.0

# Calculate text position
text_surface = font.render(selected_folder_name, True, black)
text_rect = text_surface.get_rect()
text_x = screen_width / 2 - text_rect.width / 2
text_y = screen_height * text_y_percent - text_rect.height / 2

# Calculate image position
if image:
    image_x = screen_width / 2 - image.get_width() / 2
    image_y = screen_height * image_y_percent - image.get_height() / 2

class Button:
    def __init__(self, x, y, text, color=gray_blue):
        self.rect = pygame.Rect(x, y, button_width, button_height)
        self.text = text
        self.color = color
    
    def draw(self):
        pygame.draw.rect(screen, self.color, self.rect)
        font = pygame.font.Font(None, int(game_font_size * 0.3))
        text_surface = font.render(self.text, True, black)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)
        
# Calculate button positions and dimensions
button_width_percent = 0.15
button_height_percent = 0.08
next_button_height_percent = 0.1

button_width = screen_width * button_width_percent
button_height = screen_height * button_height_percent
next_button_height = screen_height * next_button_height_percent
button_spacing = (screen_width - 4 * button_width) / 5

button_y = screen_height * button_y_percent - button_height / 2

# Calculate the initial position of the next button
next_button_rect = pygame.Rect(screen_width - button_width - int(screen_width * 0.025), screen_height - next_button_height - int(screen_height * 0.025), button_width, next_button_height)
next_button = Button(next_button_rect.x, next_button_rect.y, "Next")

# Generate random consonant excluding the image's first letter
def generate_random_consonant(exclude_letter):
    consonants = ''.join([c for c in string.ascii_uppercase if c not in 'AEIOU' and c != exclude_letter])
    return random.choice(consonants)
    
# Create a list of random consonants
random_letters = [generate_random_consonant(image_first_letter) for _ in range(3)]

# Create buttons with original 80% height for random consonant buttons
random_consonant_buttons = [
    Button(button_spacing, button_y, random_letters[0]),
    Button(button_spacing * 2 + button_width, button_y, random_letters[1]),
    Button(button_spacing * 3 + button_width * 2, button_y, random_letters[2]),
    Button(button_spacing * 4 + button_width * 3, button_y, generate_random_consonant(image_first_letter))
]

# Randomly select a button index to replace its content with the image letter
random_button_index = random.randint(0, 3)
random_consonant_buttons[random_button_index] = Button(
    random_consonant_buttons[random_button_index].rect.x,
    button_y,
    image_first_letter,
    color=gray_blue
)

# Create the "<" and ">" buttons
prev_button = Button(screen_width * 0.05, screen_height * 0.1 - button_height / 2, "<")
next_folder_index = min(index + 1, len(folder_names) - 1)
inc_button = Button(screen_width * 0.15, screen_height * 0.1 - button_height / 2, ">")

random_button_index = random.randint(0, 3)  # Initialize random_button_index outside the function

def update_folder_and_image(selected_folder_name, folder_names, index, selected_subfolder_path, image_first_letter, random_consonant_buttons, button_y, selected_image_filename, random_button_index):
    if folder_names:
        selected_folder_name = folder_names[index]
        selected_subfolder_path = os.path.join(phonics_words_folder, selected_folder_name)
        image_filenames = [name for name in os.listdir(selected_subfolder_path) if name.lower().endswith(('.png', '.jpg', '.jpeg', '.gif'))]

        if image_filenames:
            selected_image_filename = random.choice(image_filenames)
            image_path = os.path.join(selected_subfolder_path, selected_image_filename)
            original_image = pygame.image.load(image_path)
            image = pygame.transform.scale(original_image, (max_image_size, max_image_size))
            image_first_letter = selected_image_filename[0].upper()

            # Update the positions of the random consonant buttons
            for i, button in enumerate(random_consonant_buttons):
                if i == random_button_index:
                    button.text = image_first_letter
                else:
                    placeholder_consonant = generate_random_consonant(image_first_letter)
                    while placeholder_consonant == image_first_letter:
                        placeholder_consonant = generate_random_consonant(image_first_letter)
                    button.text = placeholder_consonant

                # Update the button positions based on the new screen dimensions
                button.rect.x = button_spacing * (i + 1) + button_width * i
                button.rect.y = button_y

            # Reset button colors
            for button in random_consonant_buttons:
                button.color = gray_blue

            # If the image letter button is not already in place
            if random_consonant_buttons[random_button_index].text != image_first_letter:
                # Replace a random button with the image letter button
                random_replace_index = random.randint(0, 3)
                random_consonant_buttons[random_replace_index] = Button(
                    random_consonant_buttons[random_replace_index].rect.x,
                    button_y,
                    image_first_letter,
                    color=gray_blue
                )
                random_button_index = random_replace_index

        else:
            image = None

    else:
        selected_folder_name = "No folders found"
        image = None

    return selected_folder_name, selected_subfolder_path, image_first_letter, image, selected_image_filename

def update_ui_positions():
    global text_x, text_y, image_x, image_y, button_width, button_height, button_spacing, button_y, next_button_rect, random_button_index

    text_x = screen_width / 2 - text_rect.width / 2
    text_y = screen_height * text_y_percent - text_rect.height / 2

    if image:
        image_x = screen_width / 2 - image.get_width() / 2
        image_y = screen_height * image_y_percent - image.get_height() / 2

    button_width = screen_width * button_width_percent
    button_height = screen_height * button_height_percent
    next_button_height = screen_height * next_button_height_percent
    button_spacing = (screen_width - 4 * button_width) / 5

    button_y = screen_height * button_y_percent - button_height / 2

    # Update next button position and dimensions
    next_button_rect = pygame.Rect(screen_width - button_width, screen_height - next_button_height, button_width, next_button_height)
    next_button.rect = next_button_rect

    # Calculate next button position 10% away from both bottom and right edges
    next_button.rect.x -= int(screen_width * 0.025)
    next_button.rect.y -= int(screen_height * 0.025)

    # Update random consonant button positions and dimensions
    for i, button in enumerate(random_consonant_buttons):
        button.rect.y = button_y
        button.rect.x = button_spacing * (i + 1) + button_width * i
        button.rect.width = button_width
        button.rect.height = button_height

    # Update image letter button position and dimensions
    random_consonant_buttons[random_button_index].rect.y = button_y
    random_consonant_buttons[random_button_index].rect.x = button_spacing * (random_button_index + 1) + button_width * random_button_index
    random_consonant_buttons[random_button_index].rect.width = button_width
    random_consonant_buttons[random_button_index].rect.height = button_height

update_ui_positions()
    
# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            
            # Check if "<" button is clicked
            if prev_button.rect.collidepoint(mouse_pos):
                index = max(index - 1, 0)
                selected_folder_name, selected_subfolder_path, image_first_letter, image, selected_image_filename = update_folder_and_image(
                    selected_folder_name, folder_names, index, selected_subfolder_path, image_first_letter, random_consonant_buttons, button_y, selected_image_filename, random_button_index
                )
                random_button_index = random.randint(0, 3)  # Update random_button_index after folder change
                update_ui_positions()  # Update UI element positions after folder change
            
            # Check if ">" button is clicked
            elif inc_button.rect.collidepoint(mouse_pos):
                index = min(index + 1, len(folder_names) - 1)
                selected_folder_name, selected_subfolder_path, image_first_letter, image, selected_image_filename = update_folder_and_image(
                    selected_folder_name, folder_names, index, selected_subfolder_path, image_first_letter, random_consonant_buttons, button_y, selected_image_filename, random_button_index
                )
                random_button_index = random.randint(0, 3)  # Update random_button_index after folder change
                update_ui_positions()  # Update UI element positions after folder change

            # Check if "Next" button is clicked
            elif next_button.rect.collidepoint(mouse_pos):
                random_button_index = random.randint(0, 3)  # Randomly select a new button index
                random_consonant_buttons[random_button_index] = Button(
                    random_consonant_buttons[random_button_index].rect.x,
                    button_y,
                    image_first_letter,
                    color=gray_blue
                )
                selected_folder_name, selected_subfolder_path, image_first_letter, image, selected_image_filename = update_folder_and_image(
                    selected_folder_name, folder_names, index, selected_subfolder_path, image_first_letter, random_consonant_buttons, button_y, selected_image_filename, random_button_index
                )
                update_ui_positions()  # Update UI element positions after button replacement

            # Check if any other button is clicked
            for button in random_consonant_buttons:
                if button.rect.collidepoint(mouse_pos):
                    if button.text == image_first_letter:
                        button.color = green  # Change button color to green when clicked
                        selected_folder_name = selected_image_filename.split('.')[0]  # Use image name as folder name
                    else:
                        button.color = red  # Change button color to red when clicked
                        
        elif event.type == pygame.VIDEORESIZE:
            # Update screen dimensions
            screen_width = event.w
            screen_height = event.h
            screen = pygame.display.set_mode((screen_width, screen_height), pygame.RESIZABLE)
            update_ui_positions()  # Update UI element positions when resizing

    screen.fill(white)  # Clear the screen with white background
    
    if image:
        screen.blit(image, (image_x, image_y))  # Blit the image
    
    text_surface = font.render(selected_folder_name, True, black)  # Update the text surface with folder name
    screen.blit(text_surface, (text_x, text_y))  # Blit the text
    
    for button in random_consonant_buttons:
        button.draw()  # Draw the random consonant buttons
    
    next_button.draw()  # Draw the "Next" button
    
    # Draw the "<" and ">" buttons
    prev_button.draw()
    inc_button.draw()
    
    pygame.display.flip()  # Update the display

# Quit Pygame
pygame.quit()