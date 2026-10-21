import pygame
import random
import colorsys
from paths import resource

# Initialize Pygame
pygame.init()

# Load window icon
icon_path = resource('icon', 'telescope.png')
Icon = pygame.image.load(icon_path)
pygame.display.set_icon(Icon)

# Constants
WINDOW_WIDTH, WINDOW_HEIGHT = 1280, 720
RECT_SIZE = 100
RECT_GAP = 20
GRID_SIZE = 9
NUM_RECTS_1 = 9
NUM_RECTS_2 = 8
NUM_RECTS_3 = 9

HIDDEN_COLOR = (255, 255, 0)  # Yellow tiles haven't been revealed yet

def luminance(color):
    """Relative luminance, from 0 (black) to 1 (white), as used to measure text contrast."""
    def channel(c):
        c /= 255
        return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4
    r, g, b = (channel(c) for c in color)
    return 0.2126 * r + 0.7152 * g + 0.0722 * b

def random_tile_color(used):
    """A random color light enough for the black letter to read clearly (contrast of at least 7:1),
    and not yellowish, so a revealed tile never looks like a hidden one.

    The hue is picked evenly around the color wheel and then lightened just enough to be readable,
    so reds, blues and purples come up as often as greens (rejecting dark colors outright left
    mostly greens, which look brightest)."""
    while True:
        hue = random.random()
        if 45 / 360 <= hue <= 75 / 360:
            continue  # Too close to the yellow of hidden tiles
        saturation = random.uniform(0.45, 0.9)
        lightness = random.uniform(0.45, 0.7)
        while lightness < 0.95:
            color = tuple(round(c * 255) for c in colorsys.hls_to_rgb(hue, lightness, saturation))
            if luminance(color) >= 0.3:
                break
            lightness += 0.02  # Lighten only as much as needed
        if luminance(color) >= 0.3 and color not in used:
            return color

# Function to get the corresponding letter for a given index
def get_letter(index):
    if index < 9:
        return chr(ord('A') + index)
    elif index < 17:
        return chr(ord('J') + index - 9)
    else:
        return chr(ord('R') + index - 17)

# Main function
def main():
    global WINDOW_WIDTH, WINDOW_HEIGHT  # Marking variables as global

    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.RESIZABLE)
    pygame.display.set_caption("Alphabet Galaxy v.1.1")

    clock = pygame.time.Clock()

    # Load the background image
    background_img = pygame.image.load(resource('background', 'galaxy.jpg'))
    background_img = pygame.transform.scale(background_img, (WINDOW_WIDTH, WINDOW_HEIGHT))

    # Calculate the starting y-coordinate for all rows of rectangles
    start_y = (WINDOW_HEIGHT - 3 * RECT_SIZE - 2 * RECT_GAP) // 2

    # Function to change the color of the clicked rectangle randomly
    def change_color(i):
        if colors[i] == HIDDEN_COLOR:
            colors[i] = random_tile_color(used=colors)

    # Calculate the positions and sizes of rectangles
    def calculate_rectangles():
        total_rects_width_1 = NUM_RECTS_1 * RECT_SIZE + (NUM_RECTS_1 - 1) * RECT_GAP
        total_rects_width_2 = NUM_RECTS_2 * RECT_SIZE + (NUM_RECTS_2 - 1) * RECT_GAP
        total_rects_width_3 = NUM_RECTS_3 * RECT_SIZE + (NUM_RECTS_3 - 1) * RECT_GAP

        start_x_1 = (WINDOW_WIDTH - total_rects_width_1) // 2
        start_x_2 = (WINDOW_WIDTH - total_rects_width_2) // 2
        start_x_3 = (WINDOW_WIDTH - total_rects_width_3) // 2

        # Adjust rectangle size based on the new window dimensions
        rect_size = min(RECT_SIZE, (WINDOW_HEIGHT - 2 * RECT_GAP) // 3)

        rectangles = []
        for i in range(NUM_RECTS_1 + NUM_RECTS_2 + NUM_RECTS_3):
            if i < NUM_RECTS_1:
                rect_x = start_x_1 + i * (rect_size + RECT_GAP)
                rect_y = start_y
            elif i < NUM_RECTS_1 + NUM_RECTS_2:
                rect_x = start_x_2 + (i - NUM_RECTS_1) * (rect_size + RECT_GAP)
                rect_y = start_y + rect_size + RECT_GAP
            else:
                rect_x = start_x_3 + (i - NUM_RECTS_1 - NUM_RECTS_2) * (rect_size + RECT_GAP)
                rect_y = start_y + 2 * (rect_size + RECT_GAP)

            rectangles.append(pygame.Rect(rect_x, rect_y, rect_size, rect_size))

        return rectangles

    # Main game loop
    running = True
    colors = [HIDDEN_COLOR] * (NUM_RECTS_1 + NUM_RECTS_2 + NUM_RECTS_3)
    rectangles = calculate_rectangles()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for i, rect in enumerate(rectangles):
                    if rect.collidepoint(event.pos):
                        change_color(i)

            # Handle resizing events
            elif event.type == pygame.VIDEORESIZE:
                WINDOW_WIDTH, WINDOW_HEIGHT = event.w, event.h
                screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.RESIZABLE)
                background_img = pygame.transform.scale(background_img, (WINDOW_WIDTH, WINDOW_HEIGHT))
                rectangles = calculate_rectangles()

        # Draw the background image
        screen.blit(background_img, (0, 0))

        # Draw the rows of rectangles with their respective colors and labels
        font = pygame.font.Font(None, 36)
        for i, rect in enumerate(rectangles):
            pygame.draw.rect(screen, colors[i], rect)
            if colors[i] != HIDDEN_COLOR:
                letter = font.render(get_letter(i), True, (0, 0, 0))
                screen.blit(letter, (rect.x + rect.width // 2 - letter.get_width() // 2,
                                     rect.y + rect.height // 2 - letter.get_height() // 2))

        # Update the display
        pygame.display.flip()

        # Limit frames per second
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()
