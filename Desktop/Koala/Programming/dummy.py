import pygame
import os
import random

pygame.init()
pygame.display.set_caption('Letter Pop v.1.0')
Icon = pygame.image.load('resources/icon/balloon.png')
pygame.display.set_icon(Icon)

# Set up display
screen_width = 1280
screen_height = 720
screen = pygame.display.set_mode((screen_width, screen_height), pygame.RESIZABLE)

# Load the background image
background_img = pygame.image.load("resources/background/sky.png")
background_img = pygame.transform.scale(background_img, (screen_width, screen_height))

# Variables
blue = (0, 160, 255)
pop_sound = pygame.mixer.Sound('resources/letter_pop/pop_sound.mp3')

# Function to read letters from file
def read_letters_from_file(file_path):
    with open(file_path, 'r') as file:
        letters = file.read().splitlines()
    return letters

# Function to generate blue circles with unique letters
def generate_blue_circles(letters):
    circles = []
    for letter in letters:
        radius = 30
        while True:
            x = random.randint(radius, screen_width - radius)
            y = random.randint(radius, screen_height - radius)
            # Check for collisions with existing circles
            collision = False
            for other_circle in circles:
                other_x, other_y = other_circle["position"]
                other_radius = other_circle["radius"]
                distance = ((x - other_x)**2 + (y - other_y)**2)**0.5
                if distance < radius + other_radius:
                    collision = True
                    break
            if not collision:
                circles.append({"position": (x, y), "radius": radius, "letter": letter})
                break
    return circles

# Main loop
running = True

# Load letters from file
letters = read_letters_from_file("resources/letter_pop/poppers.txt")

# Generate blue circles with unique letters
blue_circles = generate_blue_circles(letters)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()

            # Check if the mouse click is within any circle
            for circle_data in blue_circles:
                x, y = circle_data["position"]
                radius = circle_data["radius"]
                if (x - mouse_pos[0])**2 + (y - mouse_pos[1])**2 <= radius**2:
                    # Remove the clicked circle from the list
                    blue_circles.remove(circle_data)
                    pop_sound.play()
                    break  # Stop searching for other circles
        elif event.type == pygame.VIDEORESIZE:
            screen_width, screen_height = event.size
            screen = pygame.display.set_mode((screen_width, screen_height), pygame.RESIZABLE)
            background_img = pygame.transform.scale(background_img, (screen_width, screen_height))
            # Recalculate the positions of the circles when the window is resized
            blue_circles = generate_blue_circles(letters)

    # Draw blue circles with letters on the screen
    screen.fill((255, 255, 255))  # Fill screen with white
    screen.blit(background_img, (0, 0))
    for circle_data in blue_circles:
        x, y = circle_data["position"]
        radius = circle_data["radius"]
        letter = circle_data["letter"]

        # Draw the blue circle
        pygame.draw.circle(screen, blue, (x, y), radius)

        # Draw the letter in the center of the circle
        font = pygame.font.Font(None, 50)
        text = font.render(letter, True, (255, 255, 255))
        text_rect = text.get_rect(center=(x, y))
        screen.blit(text, text_rect)

    # Update the display
    pygame.display.flip()

pygame.quit()
