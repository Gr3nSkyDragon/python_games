import pygame
import sys
import random
import math
from pygame import gfxdraw

# Initialize pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Random Wheel Spinner")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
RED = (255, 0, 0)

# Wheel properties
WHEEL_CENTER = (WIDTH // 2, HEIGHT // 2)
WHEEL_RADIUS = 200
WHEEL_BORDER = 5

# Font
font = pygame.font.SysFont('Arial', 20)
large_font = pygame.font.SysFont('Arial', 36, bold=True)

class WheelSpinner:
    def __init__(self, segments):
        self.segments = segments
        self.colors = self.generate_colors(len(segments))
        self.angle = 0
        self.spinning = False
        self.deceleration = 0
        self.final_angle = 0
        self.result = None
        self.spin_time = 0
        self.max_spin_time = 3000  # 3 seconds max spin time
        self.show_result = False
        # self.run_test_cases()  # Verify calculations immediately
        
    def generate_colors(self, count):
        colors = []
        for i in range(count):
            hue = (i * 360 / count) % 360
            saturation = 80 + random.randint(0, 20)
            value = 80 + random.randint(0, 20)
            rgb = self.hsv_to_rgb(hue, saturation, value)
            colors.append(rgb)
        return colors
    
    def hsv_to_rgb(self, h, s, v):
        h = h / 60
        s = s / 100
        v = v / 100
        
        c = v * s
        x = c * (1 - abs((h % 2) - 1))
        m = v - c
        
        if h < 1:
            r, g, b = c, x, 0
        elif h < 2:
            r, g, b = x, c, 0
        elif h < 3:
            r, g, b = 0, c, x
        elif h < 4:
            r, g, b = 0, x, c
        elif h < 5:
            r, g, b = x, 0, c
        else:
            r, g, b = c, 0, x
            
        return (int((r + m) * 255), int((g + m) * 255), int((b + m) * 255))
    
    def spin(self):
        if not self.spinning:
            # print("Debug - Spin triggered")
            self.spinning = True
            self.show_result = False
            self.deceleration = random.uniform(0.3, 0.6)
            self.spin_time = 0
            self.result = None
            # Ensure positive rotation (clockwise) only
            self.final_angle = abs(random.uniform(9, 23)) * 360  
            # print(f"Debug - Final target angle: {self.final_angle:.2f} (Clockwise)")

    def update(self, dt):
        if self.spinning:
            self.spin_time += dt
            progress = min(self.spin_time / self.max_spin_time, 1.0)
            
            remaining_angle = self.final_angle - self.angle
            if progress < 1.0:
                speed = remaining_angle * 0.03 * (1 - progress)
                self.angle += speed
                # print(f"Debug - Progress: {progress:.2f}, Remaining: {remaining_angle:.2f}, Angle: {self.angle:.2f}")
            else:
                # print("Debug - Spin complete!")
                self.spinning = False
                self.calculate_result()
                self.show_result = True
    
    def calculate_result(self):
        normalized_angle = -self.angle % 360
        segment_size = 360 / len(self.segments)
        
        # For clockwise rotation with pointer at top (270°):
        # Winning segment is at (360 - normalized_angle + 180) % 360
        winning_angle = (630 - normalized_angle) % 360
        winning_index = int(winning_angle // segment_size) % len(self.segments)
        self.result = self.segments[winning_index]
        
        """print(f"""
        # FINAL WINNER CALCULATION:
        #    Wheel angle: {normalized_angle:.1f}°
        #    Pointer position: 270° (top)
        #    Winning angle: {winning_angle:.1f}°
        #    Segment size: {segment_size:.1f}°
        #    Winning index: {winning_index}
        #    Winner: {self.result}
        """)"""
    
    # def run_test_cases(self):
    #    test_angles = [0, 30, 90, 180, 270]
    #    original_angle = self.angle
        
    #    for angle in test_angles:
    #        self.angle = angle
    #        self.calculate_result()
            
            # Expected winner is at (450 - angle) % 360
    #        expected_index = int((630 - angle) // (360/len(self.segments))) % len(self.segments)
    #        expected_result = self.segments[expected_index]
            
    #        print(f"\nTEST CASE: Angle={angle}°")
    #        print(f"Expected: {expected_result} (Index {expected_index})")
    #        print(f"Actual: {self.result}")
    #        print("STATUS: ✓ PASS" if self.result == expected_result else "STATUS: ✗ FAIL")
        
    #    self.angle = original_angle

    def draw(self, surface):
        angle_to_draw = -self.angle % 360  # Rotation logic

        # Draw wheel background first
        pygame.draw.circle(surface, WHITE, WHEEL_CENTER, WHEEL_RADIUS + WHEEL_BORDER)

        # Draw all segments first
        segment_angle = 360 / len(self.segments)
        segment_points = []
        
        for i, (segment, color) in enumerate(zip(self.segments, self.colors)):
            start_angle = math.radians(angle_to_draw + i * segment_angle)
            end_angle = math.radians(angle_to_draw + (i + 1) * segment_angle)
            
            points = [WHEEL_CENTER]
            for angle in [start_angle, end_angle]:
                points.append((
                    WHEEL_CENTER[0] + WHEEL_RADIUS * math.cos(angle),
                    WHEEL_CENTER[1] + WHEEL_RADIUS * math.sin(angle)
                ))
            
            pygame.draw.polygon(surface, color, points)
            pygame.draw.polygon(surface, BLACK, points, WHEEL_BORDER)
            segment_points.append(points)  # Save for label placement

        # Then draw all labels in a second pass
        for i, (segment, points) in enumerate(zip(self.segments, segment_points)):
            mid_angle = angle_to_draw + (i + 0.5) * segment_angle
            label_radius = WHEEL_RADIUS * 0.7  # Slightly larger radius
            label_pos = (
                WHEEL_CENTER[0] + label_radius * math.cos(math.radians(mid_angle)),
                WHEEL_CENTER[1] + label_radius * math.sin(math.radians(mid_angle))
            )
            
            text_surf = font.render(segment, True, BLACK)
            text_rect = text_surf.get_rect(center=label_pos)
            surface.blit(text_surf, text_rect)
        
        pygame.draw.circle(surface, WHITE, WHEEL_CENTER, WHEEL_RADIUS * 0.1)
        pygame.draw.circle(surface, BLACK, WHEEL_CENTER, WHEEL_RADIUS * 0.1, 2)
        
        # Pointer at top pointing downward
        pointer_points = [
            (WHEEL_CENTER[0], WHEEL_CENTER[1] - WHEEL_RADIUS + 20),
            (WHEEL_CENTER[0] - 15, WHEEL_CENTER[1] - WHEEL_RADIUS - 10),
            (WHEEL_CENTER[0] + 15, WHEEL_CENTER[1] - WHEEL_RADIUS - 10)
        ]
        pygame.draw.polygon(surface, RED, pointer_points)
        
        # 1. Actual pointer position (red) - should match visual pointer
        # pygame.draw.line(surface, (255,0,0), WHEEL_CENTER, 
        #                (WHEEL_CENTER[0], WHEEL_CENTER[1] - WHEEL_RADIUS), 3)

        # In draw(), replace the green line calculation with:
        # winning_angle = (360 - self.angle) % 360
        # winning_x = WHEEL_CENTER[0] + WHEEL_RADIUS * math.cos(math.radians(winning_angle))
        # winning_y = WHEEL_CENTER[1] + WHEEL_RADIUS * math.sin(math.radians(winning_angle))
        # pygame.draw.line(surface, (0,255,0), WHEEL_CENTER, (winning_x, winning_y), 3)
        
        # Enhanced result display
        if self.show_result and self.result:
            # Dark overlay
            overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 180))
            surface.blit(overlay, (0, 0))
            
            # Result box
            box_width, box_height = 350, 200
            box_rect = pygame.Rect(
                (WIDTH - box_width) // 2,
                (HEIGHT - box_height) // 2,
                box_width,
                box_height
            )
            pygame.draw.rect(surface, WHITE, box_rect, border_radius=15)
            pygame.draw.rect(surface, (0, 100, 0), box_rect, 3, border_radius=15)
            
            # Winner text
            winner_text = large_font.render(f"WINNER:", True, BLACK)
            winner_rect = winner_text.get_rect(center=(WIDTH//2, HEIGHT//2 - 30))
            surface.blit(winner_text, winner_rect)
            
            result_text = large_font.render(self.result, True, (0, 100, 0))
            result_rect = result_text.get_rect(center=(WIDTH//2, HEIGHT//2 + 30))
            surface.blit(result_text, result_rect)
            
            # Close button
            close_rect = pygame.Rect(
                (WIDTH - 120) // 2,
                HEIGHT//2 + 70,
                120,
                40
            )
            pygame.draw.rect(surface, (200, 50, 50), close_rect, border_radius=5)
            pygame.draw.rect(surface, BLACK, close_rect, 2, border_radius=5)
            close_text = font.render("CLOSE", True, WHITE)
            close_text_rect = close_text.get_rect(center=close_rect.center)
            surface.blit(close_text, close_text_rect)

# Segments
segments = ["Option 1", "Option 2", "Option 3", "Option 4", 
            "Option 5", "Option 6", "Option 7", "Option 8",
            "Option 9"]

spinner = WheelSpinner(segments)
spin_button_rect = pygame.Rect(WIDTH // 2 - 100, HEIGHT - 100, 200, 50)

clock = pygame.time.Clock()
running = True

while running:
    dt = clock.tick(60)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            if not spinner.spinning:
                if spin_button_rect.collidepoint(mouse_pos):
                    spinner.spin()
                elif spinner.show_result:
                    close_rect = pygame.Rect(
                        (WIDTH - 120) // 2,
                        HEIGHT//2 + 70,
                        120,
                        40
                    )
                    if close_rect.collidepoint(mouse_pos):
                        spinner.show_result = False
    
    spinner.update(dt)
    screen.fill(WHITE)
    spinner.draw(screen)
    
    if not spinner.spinning and not spinner.show_result:
        pygame.draw.rect(screen, (50, 150, 50), spin_button_rect, border_radius=10)
        pygame.draw.rect(screen, BLACK, spin_button_rect, 2, border_radius=10)
        text = large_font.render("SPIN!", True, WHITE)
        screen.blit(text, (spin_button_rect.centerx - text.get_width() // 2, 
                          spin_button_rect.centery - text.get_height() // 2))
    
    pygame.display.flip()

pygame.quit()
sys.exit()