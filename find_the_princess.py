import math
import os
import pygame
import random
from paths import resource, editable

pygame.init()

# Font size
FONT_SIZE = 80

# Screen dimensions
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720

# Colors
BACKGROUND = (140, 235, 255)  #Clicked Rectangle Color
RED = (210, 50, 70)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
CONFETTI_COLORS = [(255, 70, 90), (255, 200, 40), (60, 200, 90), (60, 140, 255), (190, 90, 255), (255, 140, 200)]

# Grid dimensions
GRID_ROWS = 3
GRID_COLS = 6

# Celebration when the princess is found: she pulses three times, each pulse smaller,
# never more than 15% bigger, and settles at her normal size
PULSE_MS = 1800
PULSES = 3
PULSE_GROW = 0.15

# Initialize Pygame screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption('Find the Princess v.2.0')

# Load window icon
icon_path = resource('icon', 'princess_icon.png')
Icon = pygame.image.load(icon_path)
pygame.display.set_icon(Icon)

clock = pygame.time.Clock()

# Everyone who can be hidden: every picture in resources/princess (add a .png there to add one)
character_images = [pygame.image.load(resource('princess', name)).convert_alpha()
                    for name in sorted(os.listdir(resource('princess'))) if name.lower().endswith('.png')]
chosen_image = None  # The original of the picked character; princess_img is it sized for a tile

def fit(image, width, height):
    """Scale an image to fit inside width x height, keeping its proportions."""
    scale = min(width / image.get_width(), height / image.get_height())
    return pygame.transform.smoothscale(image, (max(1, int(image.get_width() * scale)),
                                                max(1, int(image.get_height() * scale))))

def resize_game(width, height):
    global RECT_WIDTH, RECT_HEIGHT, princess_img, SCREEN_WIDTH, SCREEN_HEIGHT

    SCREEN_WIDTH = width
    SCREEN_HEIGHT = height
    RECT_WIDTH = SCREEN_WIDTH // GRID_COLS
    RECT_HEIGHT = SCREEN_HEIGHT // GRID_ROWS
    if chosen_image:
        princess_img = fit(chosen_image, RECT_WIDTH - 10, RECT_HEIGHT - 10)

def read_lines(folder, filename, count):
    """Exactly count lines from an editable text file (padded with blanks if it's short)."""
    with open(editable(folder, filename)) as f:
        lines = f.read().splitlines()
    return (lines + [''] * count)[:count]

def new_board():
    """Shuffle the words and hidden letters from the text files and hide the princess among them."""
    global hidden_letters, rectangles_labels, princess_index
    # Load the hidden letters from the text file (one tile is left for the princess)
    hidden_letters = read_lines('princess', 'hidden_content.txt', GRID_ROWS * GRID_COLS - 1)

    # Shuffle the hidden letters and place the princess randomly among them
    random.shuffle(hidden_letters)
    princess_index = random.randint(0, GRID_ROWS * GRID_COLS - 1)
    hidden_letters.insert(princess_index, 'princess')

    # Load the labels from the text file, shuffled
    rectangles_labels = read_lines('princess', 'rectangle_content.txt', GRID_ROWS * GRID_COLS)
    random.shuffle(rectangles_labels)

new_board()

def tile_rect(index):
    """A tile's area. Edges are spread proportionally, so the tiles fill the window exactly
    (dividing evenly left a strip of background showing when the size didn't divide by 6 or 3)."""
    row, col = divmod(index, GRID_COLS)
    left = col * SCREEN_WIDTH // GRID_COLS
    top = row * SCREEN_HEIGHT // GRID_ROWS
    return pygame.Rect(left, top, (col + 1) * SCREEN_WIDTH // GRID_COLS - left,
                       (row + 1) * SCREEN_HEIGHT // GRID_ROWS - top)

def tile_at(pos):
    """The index of the tile at a window position."""
    col = min(GRID_COLS - 1, pos[0] * GRID_COLS // SCREEN_WIDTH)
    row = min(GRID_ROWS - 1, pos[1] * GRID_ROWS // SCREEN_HEIGHT)
    return row * GRID_COLS + col

def draw_grid(rectangles_clicked, celebrating):
    for i in range(GRID_ROWS * GRID_COLS):
        tile = tile_rect(i)

        pygame.draw.rect(screen, BLACK, tile, 2)  # Black border

        if not rectangles_clicked[i]:
            pygame.draw.rect(screen, RED, tile.inflate(-4, -4))
            draw_text(rectangles_labels[i], tile, FONT_SIZE)  # Use the label from princess_content with larger font size
        else:
            content = hidden_letters[i]
            if content == 'princess':
                if not celebrating:  # While celebrating, she's drawn pulsing on top instead
                    screen.blit(princess_img, princess_img.get_rect(center=tile.center))
            else:
                draw_text(content, tile, FONT_SIZE)  # Use the label from hidden_letters with even larger font size

def draw_text(text, tile, font_size):
    if text:
        font = pygame.font.Font(None, font_size)
        text_surface = font.render(text, True, WHITE)  # Letters in white color
        screen.blit(text_surface, text_surface.get_rect(center=tile.center))

def play_again_button():
    button = pygame.Rect(0, 0, max(220, SCREEN_WIDTH // 5), max(56, SCREEN_HEIGHT // 10))
    button.midbottom = (SCREEN_WIDTH // 2, SCREEN_HEIGHT - SCREEN_HEIGHT // 20)
    return button

def draw_play_again(mouse):
    button = play_again_button()
    pygame.draw.rect(screen, (0, 0, 0), button.move(4, 5), border_radius=14)  # Shadow, so it stands out
    pygame.draw.rect(screen, (60, 170, 80) if not button.collidepoint(mouse) else (80, 195, 100), button,
                     border_radius=14)
    pygame.draw.rect(screen, BLACK, button, 3, border_radius=14)
    label = pygame.font.Font(None, int(button.height * 0.6)).render("Play again", True, WHITE)
    screen.blit(label, label.get_rect(center=button.center))

# Choosing who to find, before the board is set up
def chooser_cards():
    """A card rect for each character, in a grid that fits the window."""
    count = len(character_images)
    columns = min(count, 6 if SCREEN_WIDTH / SCREEN_HEIGHT > 1.4 else 3)
    rows = math.ceil(count / columns)
    top = int(SCREEN_HEIGHT * 0.2)
    gap = max(12, int(SCREEN_HEIGHT * 0.03))
    card_width = min((SCREEN_WIDTH - gap * (columns + 1)) // columns, int(SCREEN_HEIGHT * 0.4))
    card_height = min((SCREEN_HEIGHT - top - gap * (rows + 1)) // rows, int(card_width * 2))
    # Center the cards in the space under the title
    left = (SCREEN_WIDTH - (columns * card_width + (columns - 1) * gap)) // 2
    top += (SCREEN_HEIGHT - top - (rows * card_height + (rows - 1) * gap)) // 2
    for i in range(count):
        row, col = divmod(i, columns)
        yield i, pygame.Rect(left + col * (card_width + gap), top + row * (card_height + gap),
                             card_width, card_height)

def draw_chooser(mouse):
    title = pygame.font.Font(None, max(40, int(SCREEN_HEIGHT * 0.1))).render("Who do you want to find?", True, BLACK)
    screen.blit(title, title.get_rect(center=(SCREEN_WIDTH // 2, int(SCREEN_HEIGHT * 0.11))))
    for i, card in chooser_cards():
        hovered = card.collidepoint(mouse)
        pygame.draw.rect(screen, WHITE, card, border_radius=12)
        pygame.draw.rect(screen, RED if hovered else BLACK, card, 5 if hovered else 2, border_radius=12)
        picture = fit(character_images[i], card.width - 20, card.height - 20)
        screen.blit(picture, picture.get_rect(center=card.center))

# Celebration
confetti = []  # [x, y, x speed, y speed, size, color, angle, spin], positions in pixels, speeds per second

def burst_confetti(center):
    size = max(6, int(min(SCREEN_WIDTH, SCREEN_HEIGHT) * 0.012))
    for _ in range(160):
        confetti.append([center[0], center[1], random.uniform(-450, 450), random.uniform(-1000, -300),
                         random.uniform(size * 0.6, size * 1.4), random.choice(CONFETTI_COLORS),
                         random.uniform(0, 360), random.uniform(-540, 540)])

def update_and_draw_confetti(seconds):
    for piece in confetti:
        piece[0] += piece[2] * seconds
        piece[1] += piece[3] * seconds
        piece[3] += 1400 * seconds  # gravity
        piece[2] *= 0.99            # a little air resistance
        piece[6] += piece[7] * seconds
        x, y, size, color, angle = piece[0], piece[1], piece[4], piece[5], math.radians(piece[6])
        # A small rectangle turned to its current angle
        corners = [(-size / 2, -size / 4), (size / 2, -size / 4), (size / 2, size / 4), (-size / 2, size / 4)]
        pygame.draw.polygon(screen, color, [(x + cx * math.cos(angle) - cy * math.sin(angle),
                                             y + cx * math.sin(angle) + cy * math.cos(angle)) for cx, cy in corners])
    confetti[:] = [p for p in confetti if p[1] < SCREEN_HEIGHT + 40]

def pulse_scale(elapsed_ms):
    """1 = normal size. Grows and shrinks back PULSES times, each pulse smaller, then stays at 1."""
    if elapsed_ms >= PULSE_MS:
        return 1.0
    progress = elapsed_ms / PULSE_MS
    return 1 + PULSE_GROW * abs(math.sin(math.pi * PULSES * progress)) * (1 - progress)

def main():
    global RECT_WIDTH, RECT_HEIGHT, princess_img, chosen_image

    RECT_WIDTH = SCREEN_WIDTH // GRID_COLS
    RECT_HEIGHT = SCREEN_HEIGHT // GRID_ROWS

    running = True
    rectangles_clicked = [False] * (GRID_ROWS * GRID_COLS)
    found_at = None  # When the princess was found (ms)

    while running:
        seconds = clock.tick(60) / 1000
        now = pygame.time.get_ticks()
        celebrating = found_at is not None and now - found_at < PULSE_MS
        can_play_again = found_at is not None and not celebrating  # The button pops up once she's settled

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.VIDEORESIZE:
                resize_game(event.w, event.h)

            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if chosen_image is None:
                    # Picking who to find sets up the board
                    for i, card in chooser_cards():
                        if card.collidepoint(event.pos):
                            chosen_image = character_images[i]
                            resize_game(SCREEN_WIDTH, SCREEN_HEIGHT)
                    continue

                if can_play_again and play_again_button().collidepoint(event.pos):
                    # Back to choosing who to find, with a freshly shuffled board
                    new_board()
                    chosen_image = None
                    rectangles_clicked = [False] * (GRID_ROWS * GRID_COLS)
                    found_at = None
                    confetti.clear()
                    continue

                # Mark the rectangle as clicked; finding the princess starts the celebration
                index = tile_at(event.pos)
                if index == princess_index and not rectangles_clicked[index]:
                    found_at = now
                    burst_confetti(tile_rect(index).center)
                rectangles_clicked[index] = True

        screen.fill(BACKGROUND)  # Fill the screen with soft yellow
        if chosen_image is None:
            draw_chooser(pygame.mouse.get_pos())
        else:
            draw_grid(rectangles_clicked, celebrating)
            if celebrating:
                scale = pulse_scale(now - found_at)
                pulsing = pygame.transform.smoothscale(
                    princess_img, (int(princess_img.get_width() * scale), int(princess_img.get_height() * scale)))
                screen.blit(pulsing, pulsing.get_rect(center=tile_rect(princess_index).center))
            update_and_draw_confetti(seconds)
            if can_play_again:
                draw_play_again(pygame.mouse.get_pos())
        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()
