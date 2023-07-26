import pygame
import random

# Initialize Pygame
pygame.init()

# Set up the display
screen_width = 1280
screen_height = 720
screen = pygame.display.set_mode((screen_width, screen_height), pygame.RESIZABLE)
pygame.display.set_caption("Scuba Reader v.1.2")
Icon = pygame.image.load('resources/icon/snorkel.png')
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
        self.scroll_speed = 1.5  # Scroll speed

    def update(self):
        self.rect.x += self.scroll_speed  # Move the text to the right

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

# Function to handle resizing of elements
def handle_resize():
    global screen_width, screen_height, background_image, scuba_image

    # Scale the background image to fit the new screen size
    background_image = pygame.transform.scale(background_image_original, (screen_width, screen_height))

    # Scale the scuba image based on the initial text object's dimensions
    initial_text_obj = next(iter(all_text_objects))
    scuba_image = pygame.transform.scale(scuba_image_original, (scuba_width_factor * initial_text_obj.rect.width, scuba_height_factor * initial_text_obj.rect.height))

    # Update the positions of the text objects based on the new screen size
    for text_obj in all_text_objects:
        text_obj.rect.y = random.randint(0, screen_height - text_obj.rect.height)

# Initial resizing
handle_resize()

# Game loop
running = True
clock = pygame.time.Clock()

while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.VIDEORESIZE:
            screen_width, screen_height = event.size
            screen = pygame.display.set_mode((screen_width, screen_height), pygame.RESIZABLE)
            handle_resize()

    # Update text objects
    all_text_objects.update()

    # Render
    screen.blit(background_image, (0, 0))  # Draw the resized underwater background image

    # Draw text objects with associated scuba image
    for text_obj in all_text_objects:
        screen.blit(scuba_image, text_obj.rect)  # Draw scuba image
        text_rect_center = text_obj.rect.center
        text_rect_center = (text_rect_center[0] + (scuba_image.get_width() - text_obj.text_rect.width) // 2, text_rect_center[1] + (scuba_image.get_height() - text_obj.text_rect.height) // 3.5)
        screen.blit(text_obj.text_image, text_rect_center)  # Draw centered text over scuba image

    # Update the display
    pygame.display.flip()

    # Limit the frame rate
    clock.tick(60)

# Quit the game
pygame.quit()