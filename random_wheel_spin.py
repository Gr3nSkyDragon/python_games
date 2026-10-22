import pygame
import sys
import random
import math
from pygame import gfxdraw
from paths import resource

# Initialize pygame
pygame.init()

# Initial screen dimensions
INIT_WIDTH, INIT_HEIGHT = 1000, 600
screen = pygame.display.set_mode((INIT_WIDTH, INIT_HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("Random Wheel Spinner v.1.3")

# Randomness from the operating system, so spins can't fall into a repeatable pattern
rng = random.SystemRandom()

# Then modify your icon loading code:
icon_path = resource('icon', 'wheel.png')
icon = pygame.image.load(icon_path).convert_alpha()
pygame.display.set_icon(icon)

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
RED = (255, 0, 0)
WHEEL_BACKGROUND = (200, 200, 200)
SCREEN_BACKGROUND = (240, 240, 240)
TEXTBOX_COLOR_INACTIVE = pygame.Color('lightskyblue3')
TEXTBOX_COLOR_ACTIVE = pygame.Color('dodgerblue2')

# Font
font = None
large_font = None
result_font = None  # The winning entry in the result box

class TextBox:
    def __init__(self, x, y, w, h, text=''):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = TEXTBOX_COLOR_INACTIVE
        self.text = text
        self.active = False
        self.default_text = "Things to spin\nOne per line\n\nClick to edit"
        self.scroll_y = 0
        self.line_height = 25
        self.visible_lines = h // self.line_height
        self.scrollbar_width = 10
        self.scrollbar_rect = pygame.Rect(x + w - self.scrollbar_width, y, self.scrollbar_width, h)
        self.scrollbar_handle_rect = None
        self.scroll_dragging = False
        self.update_scrollbar()
        self.cursor_pos = 0  # Character position in text
        self.cursor_line = 0  # Line position
        self.cursor_visible = True
        self.cursor_blink_time = 500  # milliseconds
        self.last_cursor_toggle = 0
        self.cursor_x = 0
        self.cursor_y = 0

    def update_cursor_position(self):
        """Calculate cursor screen position based on cursor_pos"""
        lines = self.text.split('\n')
        current_line = 0
        chars_counted = 0
        
        for i, line in enumerate(lines):
            line_length = len(line) + 1  # +1 for the newline character
            if chars_counted + line_length > self.cursor_pos:
                self.cursor_line = i
                self.cursor_x = self.rect.x + 5 + font.size(line[:self.cursor_pos - chars_counted])[0]
                self.cursor_y = self.rect.y + 5 + (i - int(self.scroll_y)) * self.line_height
                break
            chars_counted += line_length
        else:
            # Cursor at end of text
            if lines:
                self.cursor_line = len(lines) - 1
                last_line = lines[-1]
                self.cursor_x = self.rect.x + 5 + font.size(last_line)[0]
                self.cursor_y = self.rect.y + 5 + (len(lines) - 1 - int(self.scroll_y)) * self.line_height
        
    def update_position(self, x, y, w, h):
        self.rect = pygame.Rect(x, y, w, h)
        self.visible_lines = h // self.line_height
        self.scrollbar_rect = pygame.Rect(x + w - self.scrollbar_width, y, self.scrollbar_width, h)
        self.update_scrollbar()
        
    def update_font(self):
        # Update the font when window is resized
        self.font = pygame.font.SysFont('Arial', int(20 * min(
            self.rect.width / 250, 
            self.rect.height / 300
        )))
        self.line_height = self.font.get_linesize()
        self.visible_lines = self.rect.height // self.line_height
        self.update_scrollbar()    
        
    def update_scrollbar(self):
        lines = self.text.split('\n') if self.text else self.default_text.split('\n')
        total_lines = len(lines)
        
        if total_lines <= self.visible_lines:
            self.scroll_y = 0
            self.scrollbar_handle_rect = None
            return
            
        # Calculate scrollbar handle size and position
        handle_height = max(20, int((self.visible_lines / total_lines) * self.rect.height))
        max_scroll = total_lines - self.visible_lines
        
        # Ensure scroll_y stays within bounds
        self.scroll_y = min(max(0, self.scroll_y), max_scroll)
        
        # Calculate handle position with perfect bottom alignment
        scroll_ratio = self.scroll_y / max_scroll
        available_height = self.rect.height - handle_height
        handle_y = self.rect.y + scroll_ratio * available_height
        
        self.scrollbar_handle_rect = pygame.Rect(
            self.rect.x + self.rect.width - self.scrollbar_width,
            handle_y,
            self.scrollbar_width,
            handle_height
        )
    
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.active = True
                if self.text == self.default_text:
                    self.text = ''
                # Check if clicking on scrollbar
                if (self.scrollbar_handle_rect and 
                    self.scrollbar_rect.collidepoint(event.pos)):
                    self.scroll_dragging = True
                    self.drag_start_y = event.pos[1]
                    self.drag_start_scroll = self.scroll_y
                    
                    # Jump to clicked position with perfect precision
                    if not self.scrollbar_handle_rect.collidepoint(event.pos):
                        click_pos = (event.pos[1] - self.rect.y) / self.rect.height
                        total_lines = len(self.text.split('\n')) if self.text else len(self.default_text.split('\n'))
                        max_scroll = max(1, total_lines - self.visible_lines)
                        self.scroll_y = int(click_pos * max_scroll)
                        self.update_scrollbar()
                # Calculate cursor position from click
                mouse_x, mouse_y = event.pos
                rel_y = mouse_y - self.rect.y - 5
                clicked_line = min(int(self.scroll_y + rel_y // self.line_height), len(self.text.split('\n')) - 1)
                
                lines = self.text.split('\n')
                clicked_line_text = lines[clicked_line] if clicked_line < len(lines) else ""
                
                # Find character position in line
                rel_x = mouse_x - self.rect.x - 5
                char_pos = 0
                width = 0
                for i, char in enumerate(clicked_line_text):
                    char_width = font.size(char)[0]
                    if width + char_width/2 > rel_x:  # Check if we've passed the click position
                        break
                    width += char_width
                    char_pos = i + 1
                
                # Calculate absolute cursor position
                line_lengths = [len(line)+1 for line in lines[:clicked_line]]  # +1 for newline
                self.cursor_pos = sum(line_lengths) + char_pos
                self.update_cursor_position()
                self.cursor_visible = True
                self.last_cursor_toggle = pygame.time.get_ticks()
        
        elif event.type == pygame.MOUSEMOTION and self.scroll_dragging:
            dy = event.pos[1] - self.drag_start_y
            total_lines = len(self.text.split('\n')) if self.text else len(self.default_text.split('\n'))
            max_scroll = max(1, total_lines - self.visible_lines)
            
            # Calculate scroll position based on drag distance
            scroll_delta = (dy / (self.rect.height - self.scrollbar_handle_rect.height)) * max_scroll
            self.scroll_y = min(max(0, self.drag_start_scroll + scroll_delta), max_scroll)
            self.update_scrollbar()
            
        elif event.type == pygame.MOUSEWHEEL:
            if self.active:
                self.scroll_y = max(0, self.scroll_y - event.y)
                total_lines = len(self.text.split('\n')) if self.text else len(self.default_text.split('\n'))
                self.scroll_y = min(self.scroll_y, max(0, total_lines - self.visible_lines))
                self.update_scrollbar()
                
        elif event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    self.text = self.text[:self.cursor_pos] + '\n' + self.text[self.cursor_pos:]
                    self.cursor_pos += 1
                elif event.key == pygame.K_BACKSPACE:
                    if self.cursor_pos > 0:
                        self.text = self.text[:self.cursor_pos-1] + self.text[self.cursor_pos:]
                        self.cursor_pos -= 1
                elif event.key == pygame.K_DELETE:
                    if self.cursor_pos < len(self.text):
                        self.text = self.text[:self.cursor_pos] + self.text[self.cursor_pos+1:]
                elif event.key == pygame.K_LEFT:
                    self.cursor_pos = max(0, self.cursor_pos - 1)
                elif event.key == pygame.K_RIGHT:
                    self.cursor_pos = min(len(self.text), self.cursor_pos + 1)
                elif event.key == pygame.K_UP:
                    # Move cursor up one line
                    lines = self.text[:self.cursor_pos].split('\n')
                    if len(lines) > 1:
                        prev_line_len = len(lines[-2])
                        self.cursor_pos = max(0, self.cursor_pos - prev_line_len - 1)
                    # Maintain existing scroll behavior
                    self.scroll_y = max(0, self.scroll_y - 1)
                elif event.key == pygame.K_DOWN:
                    # Move cursor down one line
                    lines = self.text[:self.cursor_pos].split('\n')
                    if len(lines) > 0 and len(self.text) > self.cursor_pos:
                        next_newline = self.text.find('\n', self.cursor_pos)
                        if next_newline == -1:
                            next_newline = len(self.text)
                        self.cursor_pos = min(len(self.text), self.cursor_pos + (next_newline - self.cursor_pos) + 1)
                    # Maintain existing scroll behavior
                    self.scroll_y = min(self.scroll_y + 1, max(0, len(self.text.split('\n')) - self.visible_lines))
                elif event.key == pygame.K_HOME:
                    # Move to start of line
                    lines = self.text[:self.cursor_pos].split('\n')
                    if lines:
                        self.cursor_pos -= len(lines[-1])
                elif event.key == pygame.K_END:
                    # Move to end of line
                    lines = self.text[:self.cursor_pos].split('\n')
                    if lines and len(self.text) > self.cursor_pos:
                        next_newline = self.text.find('\n', self.cursor_pos)
                        if next_newline == -1:
                            next_newline = len(self.text)
                        self.cursor_pos = next_newline
                else:
                    # Insert regular characters at cursor position
                    self.text = self.text[:self.cursor_pos] + event.unicode + self.text[self.cursor_pos:]
                    self.cursor_pos += 1
                
                # Update cursor and scroll positions
                self.update_cursor_position()
                self.update_scrollbar()
                self.cursor_visible = True
                self.last_cursor_toggle = pygame.time.get_ticks()
        return False

    def draw(self, screen):
        # Draw text box background
        pygame.draw.rect(screen, WHITE, self.rect)
        pygame.draw.rect(screen, self.color, self.rect, 2)
        
        # Get lines to display
        lines = self.text.split('\n') if self.text else []
        if not lines and not self.active:
            lines = self.default_text.split('\n')
        
        # Apply scroll offset
        start_line = int(self.scroll_y)
        end_line = min(start_line + self.visible_lines, len(lines))
        
        # Draw visible lines
        for i in range(start_line, end_line):
            line = lines[i]
            txt_surface = font.render(line, True, BLACK)
            screen.blit(txt_surface, 
                       (self.rect.x + 5, 
                        self.rect.y + 5 + (i - start_line) * self.line_height))
        
        # Draw scrollbar if needed
        total_lines = len(lines)
        if total_lines > self.visible_lines:
            # Scrollbar track
            pygame.draw.rect(screen, GRAY, self.scrollbar_rect)
            # Scrollbar handle with border for better visibility
            if self.scrollbar_handle_rect:
                pygame.draw.rect(screen, (150, 150, 150), self.scrollbar_handle_rect)
                pygame.draw.rect(screen, BLACK, self.scrollbar_handle_rect, 1)
        # Draw cursor if active
        current_time = pygame.time.get_ticks()
        if self.active and current_time - self.last_cursor_toggle > self.cursor_blink_time:
            self.cursor_visible = not self.cursor_visible
            self.last_cursor_toggle = current_time
        
        if self.active and self.cursor_visible:
            # Only draw cursor if it's within visible area
            lines = self.text.split('\n')
            if (self.cursor_line >= int(self.scroll_y) and 
                self.cursor_line < int(self.scroll_y) + self.visible_lines):
                pygame.draw.line(
                    screen, BLACK,
                    (self.cursor_x, self.cursor_y),
                    (self.cursor_x, self.cursor_y + self.line_height - 5),
                    2
                )

class WheelSpinner:
    def __init__(self, segments):
        self.segments = segments
        self.colors = self.generate_colors(len(segments))
        self.angle = 0
        self.spinning = False
        self.start_angle = 0
        self.spin_distance = 0
        self.spin_duration = 0
        self.result = None
        self.spin_time = 0
        self.show_result = False
        self.wheel_center = (0, 0)
        self.wheel_radius = 0
        self.spin_button_rect = None
        self.close_rect = None  # CLOSE button of the winner box, set when the box is drawn
        self.font_cache = {}
        self.labels = None  # Rendered segment labels; rebuilt when segments or wheel size change
        self.update_dimensions(INIT_WIDTH, INIT_HEIGHT)
        
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
    
    def update_segments(self, new_segments):
        filtered_segments = [s.strip() for s in new_segments if s.strip()]
        if filtered_segments:
            self.segments = filtered_segments
            self.colors = self.generate_colors(len(self.segments))
            self.angle = 0
            self.result = None
            self.show_result = False
            self.labels = None

    def update_dimensions(self, width, height):
        self.wheel_center = (width // 3, height // 2)
        self.wheel_radius = min(width, height) * 0.33
        # Scale the button with the window, like the UPDATE and RESET buttons
        width_ratio = width / INIT_WIDTH
        height_ratio = height / INIT_HEIGHT
        self.spin_button_rect = pygame.Rect(
            width // 3 - 100 * width_ratio,
            height - 100 * height_ratio,
            200 * width_ratio,
            50 * height_ratio
        )
        self.labels = None

    def spin(self):
        if not self.spinning:
            self.spinning = True
            self.show_result = False
            self.spin_time = 0
            self.result = None
            # Spin from wherever the wheel is now, in either direction: at least 3 full turns,
            # then stop at a uniformly random point so every segment is equally likely to win
            self.start_angle = self.angle
            direction = rng.choice((1, -1))
            self.spin_distance = direction * (rng.randint(3, 5) * 360 + rng.uniform(0, 360))
            self.spin_duration = rng.uniform(4000, 5500)

    def update(self, dt):
        if self.spinning:
            self.spin_time += dt
            progress = min(self.spin_time / self.spin_duration, 1.0)
            # Ease out: fast at first, slowing smoothly to stop exactly at the target
            eased = 1 - (1 - progress) ** 3
            self.angle = self.start_angle + self.spin_distance * eased
            if progress >= 1.0:
                self.angle %= 360
                self.spinning = False
                self.calculate_result()
                self.show_result = True
    
    def calculate_result(self):
        normalized_angle = -self.angle % 360
        segment_size = 360 / len(self.segments)
        winning_angle = (630 - normalized_angle) % 360
        winning_index = int(winning_angle // segment_size) % len(self.segments)
        self.result = self.segments[winning_index]

    def label_font(self, size):
        if size not in self.font_cache:
            self.font_cache[size] = pygame.font.SysFont('Arial', size, bold=True)
        return self.font_cache[size]

    def build_labels(self):
        """Render each segment's text once, sized to fill its wedge."""
        count = len(self.segments)
        r = self.wheel_radius
        # Labels run along the radius, so the text height has to fit across the wedge
        wedge_width = 2 * r * 0.45 * math.sin(math.pi / max(count, 2))
        base_size = max(8, int(min(wedge_width * 0.75, r * 0.16)))
        max_length = r * 0.68  # from just inside the rim to near the hub
        self.labels = []
        for text in self.segments:
            surf = self.label_font(base_size).render(text, True, BLACK)
            if surf.get_width() > max_length:
                size = max(8, int(base_size * max_length / surf.get_width()))
                surf = self.label_font(size).render(text, True, BLACK)
            self.labels.append(surf)

    def draw(self, surface, width, height):
        angle_to_draw = -self.angle % 360
        pygame.draw.circle(surface, WHEEL_BACKGROUND, self.wheel_center, self.wheel_radius + 5)

        segment_angle = 360 / len(self.segments)
        if self.labels is None:
            self.build_labels()

        for i, color in enumerate(self.colors):
            # Draw segment
            start_angle = angle_to_draw + i * segment_angle
            end_angle = angle_to_draw + (i + 1) * segment_angle
            
            points = [self.wheel_center]
            steps = max(3, int(segment_angle / 5))
            for step in range(steps + 1):
                angle = start_angle + (end_angle - start_angle) * step / steps
                rad_angle = math.radians(angle)
                points.append((
                    self.wheel_center[0] + self.wheel_radius * math.cos(rad_angle),
                    self.wheel_center[1] + self.wheel_radius * math.sin(rad_angle)
                ))
            
            pygame.draw.polygon(surface, color, points)
            pygame.draw.polygon(surface, BLACK, points, 1)

            # Label along the segment's middle, ending inside the rim clear of the pointer tip
            label = self.labels[i]
            mid_angle = (angle_to_draw + (i + 0.5) * segment_angle) % 360
            label_end = min(self.wheel_radius * 0.92, self.wheel_radius - 26)
            label_radius = label_end - label.get_width() / 2
            label_pos = (
                self.wheel_center[0] + label_radius * math.cos(math.radians(mid_angle)),
                self.wheel_center[1] + label_radius * math.sin(math.radians(mid_angle))
            )
            # Turn the text to follow the radius; on the left half, flip it so it isn't upside down
            rotation = 180 - mid_angle if 90 < mid_angle < 270 else -mid_angle
            rotated = pygame.transform.rotozoom(label, rotation, 1)
            surface.blit(rotated, rotated.get_rect(center=label_pos))
        
        # Draw center circle
        pygame.draw.circle(surface, WHITE, self.wheel_center, self.wheel_radius * 0.1)
        pygame.draw.circle(surface, BLACK, self.wheel_center, self.wheel_radius * 0.1, 2)
        
        # Draw pointer
        pointer_points = [
            (self.wheel_center[0], self.wheel_center[1] - self.wheel_radius + 20),
            (self.wheel_center[0] - 15, self.wheel_center[1] - self.wheel_radius - 10),
            (self.wheel_center[0] + 15, self.wheel_center[1] - self.wheel_radius - 10)
        ]
        pygame.draw.polygon(surface, RED, pointer_points)
                
    def draw_result(self, surface, width, height):
        """Winner box over a dimmed screen; drawn last so it covers everything."""
        if self.show_result and self.result:
            overlay = pygame.Surface((width, height), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 180))
            surface.blit(overlay, (0, 0))
            
            # Scale the box with the window by the same factor as the fonts
            scale = min(width / INIT_WIDTH, height / INIT_HEIGHT)
            winner_text = large_font.render("WINNER:", True, BLACK)
            result_text = result_font.render(self.result, True, (0, 100, 0))
            # A long result is shrunk to fit inside the window
            max_text_width = width - 20 - 40 * scale
            if result_text.get_width() > max_text_width:
                shrink = max_text_width / result_text.get_width()
                result_text = pygame.transform.smoothscale(
                    result_text, (int(max_text_width), max(1, int(result_text.get_height() * shrink))))

            # Widen the box for long results, but keep it inside the window
            box_width = min(width - 20, max(350 * scale, result_text.get_width() + 80 * scale))
            box_height = 260 * scale
            box_rect = pygame.Rect(0, 0, box_width, box_height)
            box_rect.center = (width // 2, height // 2)
            pygame.draw.rect(surface, WHEEL_BACKGROUND, box_rect, border_radius=int(15 * scale))
            pygame.draw.rect(surface, (0, 100, 0), box_rect, max(2, int(3 * scale)), border_radius=int(15 * scale))

            surface.blit(winner_text, winner_text.get_rect(center=(width // 2, height // 2 - 85 * scale)))
            surface.blit(result_text, result_text.get_rect(center=(width // 2, height // 2 - 5 * scale)))

            # Shared with the click handler so the clickable area always matches the drawing
            self.close_rect = pygame.Rect(0, 0, 120 * scale, 40 * scale)
            self.close_rect.center = (width // 2, height // 2 + 85 * scale)
            pygame.draw.rect(surface, (200, 50, 50), self.close_rect, border_radius=int(5 * scale))
            pygame.draw.rect(surface, BLACK, self.close_rect, 2, border_radius=int(5 * scale))
            close_text = font.render("CLOSE", True, WHITE)
            surface.blit(close_text, close_text.get_rect(center=self.close_rect.center))

def initialize_fonts():
    global font, large_font, result_font
    # Initialize fonts with default size
    font = pygame.font.SysFont('Arial', 20)
    large_font = pygame.font.SysFont('Arial', 36, bold=True)
    result_font = pygame.font.SysFont('Arial', 60, bold=True)

def scale_fonts(width_ratio, height_ratio):
    global font, large_font, result_font
    # Scale font sizes based on window dimensions
    base_font_size = int(20 * min(width_ratio, height_ratio))
    font = pygame.font.SysFont('Arial', base_font_size)
    large_font = pygame.font.SysFont('Arial', int(base_font_size * 1.8), bold=True)
    result_font = pygame.font.SysFont('Arial', int(base_font_size * 3), bold=True)

# Default segments
default_segments = ["Red", "Orange", "Yellow", "Green", 
                   "Lime", "Teal", "Blue", "Indigo", 
                   "Violet", "Fuschia", "Pink"]

# Initialize fonts
initialize_fonts()

# Create spinner and UI elements
spinner = WheelSpinner(default_segments.copy())
input_box = TextBox(INIT_WIDTH - 300, 50, 250, 300)
update_button_rect = pygame.Rect(INIT_WIDTH - 300, 370, 250, 40)
reset_button_rect = pygame.Rect(INIT_WIDTH - 300, 420, 250, 40)

clock = pygame.time.Clock()
running = True

while running:
    dt = clock.tick(60)
    current_width, current_height = screen.get_size()
    width_ratio = current_width / INIT_WIDTH
    height_ratio = current_height / INIT_HEIGHT
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.VIDEORESIZE:
            # Update all dimensions when window is resized
            new_width, new_height = event.size
            screen = pygame.display.set_mode((new_width, new_height), pygame.RESIZABLE)
            
            # Scale fonts proportionally
            scale_fonts(new_width/INIT_WIDTH, new_height/INIT_HEIGHT)
            
            # Update spinner dimensions
            spinner.update_dimensions(new_width, new_height)
            
            # Update text box position
            input_box.update_position(
                new_width - 300 * (new_width/INIT_WIDTH),
                50 * (new_height/INIT_HEIGHT),
                250 * (new_width/INIT_WIDTH),
                300 * (new_height/INIT_HEIGHT)
            )
            
            # Update button positions
            update_button_rect = pygame.Rect(
                new_width - 300 * (new_width/INIT_WIDTH),
                370 * (new_height/INIT_HEIGHT),
                250 * (new_width/INIT_WIDTH),
                40 * (new_height/INIT_HEIGHT)
            )
            reset_button_rect = pygame.Rect(
                new_width - 300 * (new_width/INIT_WIDTH),
                420 * (new_height/INIT_HEIGHT),
                250 * (new_width/INIT_WIDTH),
                40 * (new_height/INIT_HEIGHT)
            )
            
            # Update text surfaces
            input_box.update_font()
            
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            if not spinner.spinning:
                if spinner.show_result:
                    # The winner box covers everything; only its CLOSE button responds
                    if spinner.close_rect and spinner.close_rect.collidepoint(mouse_pos):
                        spinner.show_result = False
                elif spinner.spin_button_rect.collidepoint(mouse_pos):
                    spinner.spin()
                elif update_button_rect.collidepoint(mouse_pos):
                    new_segments = input_box.text.split('\n')
                    spinner.update_segments(new_segments)
                elif reset_button_rect.collidepoint(mouse_pos):
                    spinner.update_segments(default_segments.copy())
                    input_box.text = ""
            
            input_box.handle_event(event)
        
        elif event.type == pygame.KEYDOWN:
            input_box.handle_event(event)
    
    spinner.update(dt)
    screen.fill(SCREEN_BACKGROUND)
    spinner.draw(screen, current_width, current_height)
    
    # Draw the text box and buttons
    input_box.draw(screen)
    
    # Draw update button
    pygame.draw.rect(screen, (50, 150, 50), update_button_rect, border_radius=5)
    pygame.draw.rect(screen, BLACK, update_button_rect, 2, border_radius=5)
    update_text = font.render("UPDATE", True, WHITE)
    screen.blit(update_text, (update_button_rect.centerx - update_text.get_width() // 2, 
                            update_button_rect.centery - update_text.get_height() // 2))
    
    # Draw reset button
    pygame.draw.rect(screen, (150, 50, 50), reset_button_rect, border_radius=5)
    pygame.draw.rect(screen, BLACK, reset_button_rect, 2, border_radius=5)
    reset_text = font.render("RESET", True, WHITE)
    screen.blit(reset_text, (reset_button_rect.centerx - reset_text.get_width() // 2, 
                           reset_button_rect.centery - reset_text.get_height() // 2))
    
    if not spinner.spinning and not spinner.show_result:
        pygame.draw.rect(screen, (50, 150, 50), spinner.spin_button_rect, border_radius=10)
        pygame.draw.rect(screen, BLACK, spinner.spin_button_rect, 2, border_radius=10)
        text = large_font.render("SPIN!", True, WHITE)
        screen.blit(text, (spinner.spin_button_rect.centerx - text.get_width() // 2, 
                          spinner.spin_button_rect.centery - text.get_height() // 2))

    spinner.draw_result(screen, current_width, current_height)

    pygame.display.flip()

pygame.quit()
sys.exit()
