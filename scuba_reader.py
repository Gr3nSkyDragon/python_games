import pygame
import random
from paths import resource, editable

# Initialize Pygame
pygame.init()

# Set up the display
screen_width = 1280
screen_height = 720
screen = pygame.display.set_mode((screen_width, screen_height), pygame.RESIZABLE)
pygame.display.set_caption("Scuba Reader v.1.4")

# Load window icon
icon_path = resource('icon', 'snorkel.png')
Icon = pygame.image.load(icon_path)
pygame.display.set_icon(Icon)

# Load the underwater background image
background_image = pygame.image.load(resource('background', 'underwater.png'))
background_image_original = background_image.copy()

# Read texts from the .txt file, skipping blank lines
with open(editable('scuba', 'scuba_words.txt'), "r") as file:
    texts = [line.strip() for line in file.readlines() if line.strip()]

# Define the fonts: the speed controls stay one size; the swimmers' words grow with the window
font = pygame.font.SysFont("Arial", 28)
WORD_FONT_SIZE = 38  # At the starting 1280x720 window
word_font = font  # Set for the window size in handle_resize()

# Load the scuba image; it's scaled in handle_resize()
scuba_image = pygame.image.load(resource('scuba', 'scuba.png'))
scuba_image_original = scuba_image.copy()

# Scaling factors for scuba image, relative to the first word's size
scuba_width_factor = 5
scuba_height_factor = 2.6

# Where the swimmer's body is in the scuba image (fractions of its width and height); words are centered there
BODY_CENTER = (0.615, 0.507)

# Minimum space between swimmers, in pixels
SWIMMER_GAP = 8

# Define text object class
class TextObject(pygame.sprite.Sprite):
    def __init__(self, text, font, color):
        super().__init__()
        self.font = font
        self.color = color
        self.set_text(text)
        self.rect = self.text_rect.copy()
        # Exact position; rect.x holds it rounded to whole pixels. Rounding each step instead
        # made swimmers move different amounts depending on where they were, so they could drift together.
        self.x = 0.0
        self.scroll_speed = 0.25  # Scroll speed
        self.waiting = False  # Waiting off-screen on the left for a clear spot to swim in

    def set_text(self, text):
        self.text = text
        self.text_image = self.font.render(self.text, True, self.color)
        self.text_rect = self.text_image.get_rect()
        self.ink = self.text_image.get_bounding_rect()  # The visible letters, for centering

    def box(self):
        """The area the whole swimmer covers on screen (the scuba image, not just the word)."""
        return pygame.Rect(self.rect.x, self.rect.y, scuba_image.get_width(), scuba_image.get_height())

    def update(self):
        if self.waiting:
            place_swimmer(self, self.x)
            return

        if self.scroll_speed <= 0.25:
            return  # The slowest setting, shown as 0.00x, pauses the swimmers

        self.x += self.scroll_speed  # Move the text to the right
        self.rect.x = round(self.x)

        if self.rect.left > screen_width:  # If the swimmer goes off the screen on the right
            self.set_text(random.choice(texts))  # Randomly select a new text
            # Come back in from just off the left edge, at a random height clear of other swimmers
            place_swimmer(self, -scuba_image.get_width())

def is_clear(swimmer, x, y):
    """True if the swimmer would fit at (x, y) on screen without touching any other swimmer."""
    width, height = scuba_image.get_size()
    if not 0 <= y <= max(0, screen_height - height):
        return False
    candidate = pygame.Rect(round(x), y, width, height)
    return not any(candidate.colliderect(other.box().inflate(SWIMMER_GAP * 2, SWIMMER_GAP * 2))
                   for other in all_text_objects
                   if other is not swimmer and not other.waiting)

def place_swimmer(swimmer, x, keep_y=False):
    """Put a swimmer at x, at a random clear height (or its current one if keep_y and it's still clear).

    If there's no room it waits off-screen on the left until a gap opens. Every swimmer moves
    the same distance each frame, so swimmers placed apart never run into each other later."""
    if keep_y and is_clear(swimmer, x, swimmer.rect.y):
        y = swimmer.rect.y
    else:
        clear = [y for y in range(max(0, screen_height - scuba_image.get_height()) + 1)
                 if is_clear(swimmer, x, y)]
        y = random.choice(clear) if clear else None
    if y is None:
        x = min(x, -scuba_image.get_width())
    swimmer.x = x
    swimmer.rect.x = round(x)
    if y is not None:
        swimmer.rect.y = y
    swimmer.waiting = y is None

# Create a group to hold the text objects
all_text_objects = pygame.sprite.Group()

# Define the number of objects and the stagger offset
num_objects = len(texts)
stagger_offset = 100

# Create a text object for each word
for i in range(num_objects):
    color = (65, 240, 100)  # Green text color
    text_obj = TextObject(texts[i], word_font, color)
    text_obj.waiting = True  # Not on screen until it's placed below
    all_text_objects.add(text_obj)

# Define initial scroll speed and change in scroll speed
scroll_speed = 1.75
scroll_speed_change = 0.25

# Define the initial size of the buttons relative to the screen width and height
button_size_factor = 0.06

# Calculate button size and spacing
button_size = int(min(screen_width, screen_height) * button_size_factor)
button_spacing = int(button_size * 0.5)

# Function to handle resizing of elements
def handle_resize(first_time=False):
    global screen_width, screen_height, background_image, scuba_image, button_size, button_spacing, word_font

    # Scale the background image to fit the new screen size
    background_image = pygame.transform.scale(background_image_original, (screen_width, screen_height))

    # Size the words for the window, so they're as easy to read full screen as in the starting window
    word_font = pygame.font.SysFont("Arial", max(20, round(WORD_FONT_SIZE * min(screen_width / 1280, screen_height / 720))))
    for text_obj in all_text_objects:
        text_obj.font = word_font
        text_obj.set_text(text_obj.text)

    # Scale the scuba image based on the first word's size
    word_width, word_height = word_font.size(texts[0] if texts else "word")
    scuba_image = pygame.transform.scale(scuba_image_original, (round(scuba_width_factor * word_width), round(scuba_height_factor * word_height)))

    if first_time:
        # Stagger the swimmers across the screen, each at a random height clear of the others
        for i, text_obj in enumerate(all_text_objects):
            place_swimmer(text_obj, -text_obj.rect.width + i * stagger_offset)
    else:
        # Keep each swimmer where it is if it still fits; otherwise find it a new clear height
        for text_obj in all_text_objects:
            if not text_obj.waiting:
                place_swimmer(text_obj, text_obj.x, keep_y=True)

    # Update button size and spacing based on the screen size
    button_size = int(min(screen_width, screen_height) * button_size_factor)
    button_spacing = int(button_size * 0.5)


# Initial resizing
handle_resize(first_time=True)

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
        if text_obj.waiting:
            continue  # Still off-screen, waiting for a clear spot
        screen.blit(scuba_image, text_obj.rect)  # Draw scuba image
        # Center the word's visible letters on the swimmer's body
        body_x = text_obj.rect.x + round(scuba_image.get_width() * BODY_CENTER[0])
        body_y = text_obj.rect.y + round(scuba_image.get_height() * BODY_CENTER[1])
        screen.blit(text_obj.text_image, (body_x - text_obj.ink.centerx, body_y - text_obj.ink.centery))

    # Display current scroll speed and buttons
    display_scroll_speed()

    # Update the display
    pygame.display.flip()

    # Limit the frame rate
    clock.tick(60)

# Quit the game
pygame.quit()
