import pygame
import random

# Initialize Pygame
pygame.init()

# Constants
WINDOW_WIDTH, WINDOW_HEIGHT = 1280, 720
RECT_SIZE = 100
RECT_GAP = 20
GRID_SIZE = 9
NUM_RECTS_1 = 9
NUM_RECTS_2 = 8
NUM_RECTS_3 = 9

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
    pygame.display.set_caption("Resizable Colorful Rows of Rectangles")

    clock = pygame.time.Clock()

    # Load the background image
    background_img = pygame.image.load("resources/background/galaxy.jpg")
    background_img = pygame.transform.scale(background_img, (WINDOW_WIDTH, WINDOW_HEIGHT))
    
    Icon = pygame.image.load('resources/icon/telescope.png')
    pygame.display.set_icon(Icon)

    # Calculate the starting y-coordinate for all rows of rectangles
    start_y = (WINDOW_HEIGHT - 3 * RECT_SIZE - 2 * RECT_GAP) // 2

    # Function to change the color of the clicked rectangle randomly
    def change_color(i):
        if colors[i] == (255, 255, 0):
            r, g, b = random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)
            new_color = (r, g, b)
            while new_color == (255, 255, 0) or new_color in colors[:i]:  # Ensure the new color is not yellow and not used before
                r, g, b = random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)
                new_color = (r, g, b)
            colors[i] = new_color

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
    colors = [(255, 255, 0)] * (NUM_RECTS_1 + NUM_RECTS_2 + NUM_RECTS_3)
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
            if colors[i] != (255, 255, 0):
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
