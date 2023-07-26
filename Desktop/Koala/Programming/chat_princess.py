import pygame
import random

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

# Grid dimensions
GRID_ROWS = 3
GRID_COLS = 6

# Load the princess image
princess_img = pygame.image.load('resources/princess/princess.png')

# Initialize Pygame screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption('Find the Princess!')
Icon = pygame.image.load('resources/icon/princess_icon.png')
pygame.display.set_icon(Icon)

def resize_game(width, height):
    global RECT_WIDTH, RECT_HEIGHT, princess_img, SCREEN_WIDTH, SCREEN_HEIGHT

    SCREEN_WIDTH = width
    SCREEN_HEIGHT = height
    RECT_WIDTH = SCREEN_WIDTH // GRID_COLS
    RECT_HEIGHT = SCREEN_HEIGHT // GRID_ROWS
    princess_img = pygame.image.load('resources/princess/princess.png')  # Reload the original image
    princess_img = pygame.transform.scale(princess_img, (RECT_WIDTH - 10, RECT_HEIGHT - 10))

def center_text(surface, x, y):
    # Get the width and height of the surface (text)
    text_width, text_height = surface.get_size()

    # Calculate the position to center the text within the given (x, y) position
    center_x = x + (RECT_WIDTH - text_width) // 2
    center_y = y + (RECT_HEIGHT - text_height) // 2

    return center_x, center_y

# Load the hidden letters from the text file
with open('resources/princess/hidden_content.txt') as f:
    hidden_letters = f.read().splitlines()

# Shuffle the hidden letters and place the princess randomly among them
random.shuffle(hidden_letters)
hidden_letters.insert(random.randint(0, GRID_ROWS * GRID_COLS - 1), 'princess')

# Load the labels from the text file
with open('resources/princess/rectangle_content.txt') as f:
    labels = f.read().splitlines()

# Shuffle the labels and assign them to rectangles
random.shuffle(labels)
rectangles_labels = [labels.pop() for _ in range(GRID_ROWS * GRID_COLS)]

def draw_grid(rectangles_clicked):
    for i in range(GRID_ROWS * GRID_COLS):
        row = i // GRID_COLS
        col = i % GRID_COLS
        rect_x = col * RECT_WIDTH
        rect_y = row * RECT_HEIGHT

        pygame.draw.rect(screen, BLACK, (rect_x, rect_y, RECT_WIDTH, RECT_HEIGHT), 2)  # Black border

        if not rectangles_clicked[i]:
            pygame.draw.rect(screen, RED, (rect_x + 2, rect_y + 2, RECT_WIDTH - 4, RECT_HEIGHT - 4))
            content = rectangles_labels[i]
            x = rect_x + 5
            y = rect_y + 5
            draw_text(content, x, y, FONT_SIZE)  # Use the label from princess_content with larger font size
        else:
            content = hidden_letters[i]
            if content == 'princess':
                x = rect_x + RECT_WIDTH // 2 - princess_img.get_width() // 2
                y = rect_y + RECT_HEIGHT // 2 - princess_img.get_height() // 2
                screen.blit(princess_img, (x, y))
            else:
                x = rect_x + 5
                y = rect_y + 5
                draw_text(content, x, y, FONT_SIZE)  # Use the label from hidden_letters with even larger font size

def draw_text(text, x, y, font_size):
    font = pygame.font.Font(None, font_size)
    text_surface = font.render(text, True, WHITE) if text else pygame.Surface((0, 0))  # Letters in white color
    text_width, text_height = text_surface.get_size()

    # Calculate the position to center the text within the given (x, y) position
    center_x = x + (RECT_WIDTH - text_width) // 2
    center_y = y + (RECT_HEIGHT - text_height) // 2

    screen.blit(text_surface, (center_x, center_y))
    return text_surface

def main():
    global RECT_WIDTH, RECT_HEIGHT, princess_img

    RECT_WIDTH = SCREEN_WIDTH // GRID_COLS
    RECT_HEIGHT = SCREEN_HEIGHT // GRID_ROWS
    princess_img = pygame.image.load('resources/princess/princess.png')  # Load the original image
    princess_img = pygame.transform.scale(princess_img, (RECT_WIDTH - 10, RECT_HEIGHT - 10))

    running = True
    rectangles_clicked = [False] * (GRID_ROWS * GRID_COLS)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.VIDEORESIZE:
                resize_game(event.w, event.h)

            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                # Check if a rectangle is clicked
                x, y = event.pos
                col = x // RECT_WIDTH
                row = y // RECT_HEIGHT
                index = row * GRID_COLS + col

                # Mark the rectangle as clicked
                rectangles_clicked[index] = True

        screen.fill(BACKGROUND)  # Fill the screen with soft yellow
        draw_grid(rectangles_clicked)
        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()
