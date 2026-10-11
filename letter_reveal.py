import pygame
from paths import resource, editable

pygame.init()
pygame.display.set_caption('Letter Reveal v.1.1')

# Largest the window can get; letter images never need to be bigger than this
desktop_size = min(pygame.display.get_desktop_sizes()[0])

# Set up display
screen_width = 1280
screen_height = 720
screen = pygame.display.set_mode((screen_width, screen_height), pygame.RESIZABLE)

# Load window icon
Icon = pygame.image.load(resource('icon', 'reveal.png'))
pygame.display.set_icon(Icon)

letter_index = 0
background = (132, 148, 131)
hide_color = (255, 219, 88)
button_color = (0, 128, 128)
button_text_color = (250, 243, 221)
rect_count = 3  # Number of hide rectangles in each direction

# Load letters from the text file
with open(editable('reveal', 'letters.txt'), "r") as file:
    letters = [char.upper() for char in file.read() if char.isalpha()]

def load_alphabet(folder):
    """Load each letter once, converted for fast drawing and shrunk to at most desktop size.

    The red alphabet PNGs are 4096px; keeping them full size costs ~64 MB per letter.
    """
    images = {}
    for letter in letters:
        image = pygame.image.load(resource(folder, f"{letter}.png")).convert_alpha()
        if max(image.get_size()) > desktop_size:
            image = pygame.transform.smoothscale(image, (desktop_size, desktop_size))
        images[letter] = image
    return images

alphabets = [load_alphabet('rustic_alphabet'), load_alphabet('red_alphabet')]
alphabet_index = 0  # 0 = rustic, 1 = red; toggled by the "+/-" button

# Button labels are rendered once, not every frame
font = pygame.font.Font(None, 36)
next_text = font.render("Next", True, button_text_color)
case_text = font.render("+/-", True, button_text_color)

def layout():
    """Recalculate sizes and positions for the current window size."""
    global square_size, scaled_images, next_button, case_change_button
    square_size = min(screen_width, screen_height)
    # Scale the current alphabet to the window once, instead of every frame
    scaled_images = {letter: pygame.transform.smoothscale(image, (square_size, square_size))
                     for letter, image in alphabets[alphabet_index].items()}
    next_button = pygame.Rect(screen_width - 150, 10, 140, 50)
    case_change_button = pygame.Rect(10, 10, 140, 50)

def setup_rectangles():
    rect_size = square_size // rect_count

    # Calculate the top-left corner of the square
    square_x = screen_width // 2 - square_size // 2
    square_y = screen_height // 2 - square_size // 2

    # Generate exactly rect_count x rect_count rectangles
    return [
        pygame.Rect(
            square_x + x * rect_size,
            square_y + y * rect_size,
            rect_size,
            rect_size
        )
        for x in range(rect_count)
        for y in range(rect_count)
    ]

def draw():
    # Always clear first: the letter images have soft transparent edges, and drawing them
    # over the previous frame without clearing makes those edges smear and darken
    screen.fill(background)

    # Draw image
    image = scaled_images[letters[letter_index]]
    screen.blit(image, image.get_rect(center=(screen_width // 2, screen_height // 2)))

    # Draw hide rectangles with black border
    border_width = 2
    for rect in hide_rectangles:
        pygame.draw.rect(screen, (0, 0, 0), rect)  # Draw black border
        pygame.draw.rect(screen, hide_color, rect.inflate(-border_width, -border_width))  # Draw inner rectangle

    # Draw buttons
    for button, text in ((next_button, next_text), (case_change_button, case_text)):
        pygame.draw.rect(screen, button_color, button)
        screen.blit(text, text.get_rect(center=button.center))

    pygame.display.flip()

layout()
hide_rectangles = setup_rectangles()
draw()

# Main loop: the picture only changes on clicks and resizes, so wait for events
# instead of redrawing 60 times a second. This keeps old machines nearly idle.
running = True
while running:
    event = pygame.event.wait()
    if event.type == pygame.QUIT:
        running = False
    elif event.type == pygame.MOUSEBUTTONDOWN:
        if next_button.collidepoint(event.pos):
            letter_index = (letter_index + 1) % len(letters)
            hide_rectangles = setup_rectangles()
        elif case_change_button.collidepoint(event.pos):
            alphabet_index = 1 - alphabet_index
            layout()
        else:
            for rect in hide_rectangles:
                if rect.collidepoint(event.pos):
                    hide_rectangles.remove(rect)
                    break  # Only remove one rectangle per click
        draw()
    elif event.type == pygame.VIDEORESIZE:
        screen_width = event.w
        screen_height = event.h
        screen = pygame.display.set_mode((screen_width, screen_height), pygame.RESIZABLE)
        layout()
        hide_rectangles = setup_rectangles()
        draw()
    elif event.type in (pygame.WINDOWEXPOSED, pygame.WINDOWRESTORED):
        draw()  # Repaint after the window was covered or minimized

pygame.quit()
