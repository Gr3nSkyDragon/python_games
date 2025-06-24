import pygame
import random

# Initialize Pygame
pygame.init()

# Set up the display
screen_width = 1280
screen_height = 720
screen = pygame.display.set_mode((screen_width, screen_height), pygame.RESIZABLE)
pygame.display.set_caption("Scuba Reader v.1.2.5")

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
icon_path = resource_path('resources/icon/snorkel.png')
Icon = pygame.image.load(icon_path)
pygame.display.set_icon(Icon)

# Load the underwater background image
background_image = pygame.image.load("resources/background/underwater.png")
background_image_original = background_image.copy()

# Define text object class
class TextObject(pygame.sprite.Sprite):
    def __init__(self, text, font, color, offset):
        super().__init__()
        self.font = font
        self.color = color
        self.text = text
        self.text_image = self.font.render(self.text, True, self.color)
        self.text_rect = self.text_image.get_rect()
        self.rect = self.text_rect.copy()
        self.rect.x = -self.rect.width + offset  # Start the text off-screen on the left with offset
        self.rect.y = random.randint(0, screen_height - self.rect.height)  # Random Y position
        self.scroll_speed = 0.25  # Scroll speed

    def update(self):
        self.rect.x += self.scroll_speed # Move the text to the right

        if self.rect.left > screen_width:  # If the text goes off the screen on the right
            self.rect.x = -self.rect.width  # Reset its position to the left
            self.rect.y = random.randint(0, screen_height - self.rect.height)  # Random Y position
            self.text = random.choice(texts)  # Randomly select a new text
            self.text_image = self.font.render(self.text, True, self.color)  # Render the new text
            self.text_rect = self.text_image.get_rect()

# Create a group to hold the text objects
all_text_objects = pygame.sprite.Group()

# Read texts from the .txt file
with open("resources/scuba/scuba_words.txt", "r") as file:
    texts = [line.strip() for line in file.readlines()]

# Define the font
font = pygame.font.SysFont("Arial", 28)

# Define the number of objects and the stagger offset
num_objects = len(texts)
stagger_offset = 100

# Create text objects with staggered offsets and add them to the group
for i in range(num_objects):
    color = (65, 240, 100)  # Green text color
    text_obj = TextObject(texts[i], font, color, i * stagger_offset)
    all_text_objects.add(text_obj)

# Load and resize the scuba image
scuba_image = pygame.image.load("resources/scuba/scuba.png")
scuba_image_original = scuba_image.copy()

# Scaling factors for scuba image
scuba_width_factor = 6
scuba_height_factor = 3

# Define initial scroll speed and change in scroll speed
scroll_speed = 1.75
scroll_speed_change = 0.25

# Define the initial size of the buttons relative to the screen width and height
button_size_factor = 0.06

# Calculate button size and spacing
button_size = int(min(screen_width, screen_height) * button_size_factor)
button_spacing = int(button_size * 0.5)

# Function to handle resizing of elements
def handle_resize():
    global screen_width, screen_height, background_image, scuba_image, button_size, button_spacing

    # Scale the background image to fit the new screen size
    background_image = pygame.transform.scale(background_image_original, (screen_width, screen_height))

    # Scale the scuba image based on the initial text object's dimensions
    initial_text_obj = next(iter(all_text_objects))
    scuba_image = pygame.transform.scale(scuba_image_original, (scuba_width_factor * initial_text_obj.rect.width, scuba_height_factor * initial_text_obj.rect.height))

    # Update the positions of the text objects based on the new screen size
    for text_obj in all_text_objects:
        text_obj.rect.y = random.randint(0, screen_height - text_obj.rect.height)

    # Update button size and spacing based on the screen size
    button_size = int(min(screen_width, screen_height) * button_size_factor)
    button_spacing = int(button_size * 0.5)


# Initial resizing
handle_resize()

# Create buttons surfaces with a light blue background
button_color_light_blue = (173, 216, 230, 200)  # Light blue color with transparency
plus_button = pygame.Surface((button_size, button_size), pygame.SRCALPHA)
minus_button = pygame.Surface((button_size, button_size), pygame.SRCALPHA)

# Fill the button surfaces with the light blue color
plus_button.fill(button_color_light_blue)
minus_button.fill(button_color_light_blue)

# Render "+" and "-" symbols on buttons
plus_text = font.render("+", True, (65, 240, 100))  # Green text color
minus_text = font.render("-", True, (65, 240, 100))

# Blit the symbols on the buttons (with an outline)
plus_button.blit(plus_text, (button_size // 2 - plus_text.get_width() // 2, button_size // 2 - plus_text.get_height() // 2))
minus_button.blit(minus_text, (button_size // 2 - minus_text.get_width() // 2, button_size // 2 - minus_text.get_height() // 2))

# Function to display current scroll speed and buttons
def display_scroll_speed():
    # Draw "-" button with an outline
    minus_button_rect = minus_button.get_rect(center=(screen_width - button_size * 2.4 - button_spacing * 1.5, 30))  # Adjusted position
    pygame.draw.rect(screen, (0, 0, 0), minus_button_rect, 2)
    screen.blit(minus_button, minus_button_rect)

    # Draw speed text without an outline
    speed_text = font.render(f"{scroll_speed - 0.25:.2f}x", True, (65, 240, 100))
    speed_rect = speed_text.get_rect(center=(screen_width - button_size * 1.4 - button_spacing, 30))  # Adjusted position
    screen.blit(speed_text, speed_rect)

    # Draw "+" button with an outline
    plus_button_rect = plus_button.get_rect(center=(screen_width - button_size * 0.125 - button_spacing, 30))  # Adjusted position
    pygame.draw.rect(screen, (0, 0, 0), plus_button_rect, 2)
    screen.blit(plus_button, plus_button_rect)

# Game loop
running = True
clock = pygame.time.Clock()

while running:
    button_clicked = False

    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.VIDEORESIZE:
            screen_width, screen_height = event.size
            screen = pygame.display.set_mode((screen_width, screen_height), pygame.RESIZABLE)
            handle_resize()
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            # Check if the mouse clicked on the plus or minus button
            if screen_width - button_size * 3 - button_spacing * 1.5 < event.pos[0] < screen_width - button_size * 2 - button_spacing * 0.5:
                if 10 < event.pos[1] < 10 + button_size:  # Minus button clicked
                    if scroll_speed != 0.25:
                        scroll_speed -= scroll_speed_change
                    button_clicked = True
            elif screen_width - button_size * 2 - button_spacing * 1.5 < event.pos[0] < screen_width - button_spacing // 2:
                if 10 < event.pos[1] < 10 + button_size:  # Plus button clicked
                    scroll_speed += scroll_speed_change
                    button_clicked = True

    # Update text objects with new scroll speed
    for text_obj in all_text_objects:
        text_obj.scroll_speed = scroll_speed

    # Update text objects positions
    all_text_objects.update()

    # Render
    screen.blit(background_image, (0, 0))  # Draw the resized underwater background image

    # Draw text objects with associated scuba image
    for text_obj in all_text_objects:
        screen.blit(scuba_image, text_obj.rect)  # Draw scuba image
        text_rect_center = text_obj.rect.center
        text_rect_center = (
            text_rect_center[0] + (scuba_image.get_width() - text_obj.text_rect.width) // 2,
            text_rect_center[1] + (scuba_image.get_height() - text_obj.text_rect.height) // 3.5,
        )
        screen.blit(text_obj.text_image, text_rect_center)  # Draw centered text over scuba image

    # Display current scroll speed and buttons
    display_scroll_speed()

    # Update the display
    pygame.display.flip()

    # Limit the frame rate
    clock.tick(60)

# Quit the game
pygame.quit()