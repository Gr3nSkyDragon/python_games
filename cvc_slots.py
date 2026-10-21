import pygame
import random
from paths import resource, editable

# A CVC "slot machine": three reels (consonant, vowel, consonant). Reels set to SPIN land on random
# letters; a reel set to HOLD keeps its letter, which the teacher can change with its arrows.

pygame.init()

screen_width, screen_height = 1280, 720
screen = pygame.display.set_mode((screen_width, screen_height), pygame.RESIZABLE)
pygame.display.set_caption("CVC Slots v.0.1")

# Load window icon
Icon = pygame.image.load(resource('icon', 'slots.png'))
pygame.display.set_icon(Icon)

clock = pygame.time.Clock()

# Colors
BACKGROUND = (40, 60, 120)
MACHINE = (200, 50, 60)
REEL_FACE = (255, 255, 255)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
HOLD_GOLD = (205, 175, 90)    # held reels: toggle, border and arrows
TOGGLE_GREEN = (80, 130, 90)  # a reel's SPIN toggle
SPIN_GREEN = (60, 170, 80)    # the big SPIN! button
DISABLED = (150, 150, 150)

# Letters each reel can land on, if slot_letters.txt is missing or a line is empty
DEFAULT_LETTERS = {
    'first': 'b c d f g h j k l m n p r s t v w y z',
    'middle': 'a e i o u',
    'last': 'b d f g k l m n p s t x',
}

def load_letters():
    """The letters for each reel, from the editable slot_letters.txt ("first: b c d ...")."""
    letters = {name: line.split() for name, line in DEFAULT_LETTERS.items()}
    try:
        with open(editable('slots', 'slot_letters.txt')) as f:
            for line in f:
                name, _, values = line.partition(':')
                name = name.strip().lower()
                values = values.replace(',', ' ').lower().split()
                if name in letters and not line.lstrip().startswith('#') and values:
                    letters[name] = values
    except OSError as e:
        print(f"Couldn't read slot_letters.txt, using the default letters: {e}")
    return [letters['first'], letters['middle'], letters['last']]

class Reel:
    def __init__(self, letters):
        self.letters = letters
        self.letter = random.choice(letters)
        self.spins = True   # False = held: keeps its letter, which the arrows change
        self.strip = None   # While spinning: the letters that roll past, ending on the result
        self.start_ms = 0
        self.duration_ms = 0

    def start_spin(self, now, duration_ms, turns):
        """Roll through about `turns` random letters and stop on a random one."""
        self.strip = [self.letter] + [random.choice(self.letters) for _ in range(turns)]
        self.start_ms = now
        self.duration_ms = duration_ms

    def position(self, now):
        """How far along the strip the reel has rolled, easing out to a stop on the last letter."""
        progress = min(1.0, (now - self.start_ms) / self.duration_ms)
        return (len(self.strip) - 1) * (1 - (1 - progress) ** 3)

    def update(self, now):
        if self.strip and now - self.start_ms >= self.duration_ms:
            self.letter = self.strip[-1]
            self.strip = None

    def step(self, direction):
        """Change a held reel's letter: +1 for the next letter, -1 for the previous one."""
        if self.letter in self.letters:
            self.letter = self.letters[(self.letters.index(self.letter) + direction) % len(self.letters)]
        else:
            self.letter = self.letters[0]

reels = [Reel(letters) for letters in load_letters()]

def spinning():
    return any(reel.strip for reel in reels)

def spin():
    now = pygame.time.get_ticks()
    order = 0
    for reel in reels:
        if reel.spins:
            # Reels stop one after another, left to right
            reel.start_spin(now, 1200 + 500 * order, turns=14 + 6 * order)
            order += 1

def layout():
    """Positions for the current window size: each reel's window, arrows and SPIN/HOLD toggle, and SPIN."""
    global reel_rects, up_arrows, down_arrows, toggles, spin_button, letter_font, label_font, spin_font
    reel_width = int(min(screen_width * 0.2, screen_height * 0.3))
    reel_height = int(reel_width * 1.15)
    gap = int(reel_width * 0.18)
    left = (screen_width - (3 * reel_width + 2 * gap)) // 2
    top = int(screen_height * 0.17)
    arrow_height = int(reel_width * 0.22)
    reel_rects, up_arrows, down_arrows, toggles = [], [], [], []
    for i in range(3):
        reel = pygame.Rect(left + i * (reel_width + gap), top + arrow_height + 10, reel_width, reel_height)
        reel_rects.append(reel)
        up_arrows.append(pygame.Rect(reel.x, reel.top - arrow_height - 6, reel_width, arrow_height))
        down_arrows.append(pygame.Rect(reel.x, reel.bottom + 6, reel_width, arrow_height))
        toggles.append(pygame.Rect(reel.x + reel_width * 0.15, reel.bottom + arrow_height + 18,
                                   reel_width * 0.7, max(36, int(screen_height * 0.065))))
    spin_button = pygame.Rect(0, 0, int(reel_width * 1.6), max(50, int(screen_height * 0.1)))
    spin_button.midbottom = (screen_width // 2, screen_height - int(screen_height * 0.04))
    letter_font = pygame.font.Font(None, int(reel_height * 0.95))
    label_font = pygame.font.Font(None, max(24, int(screen_height * 0.05)))
    spin_font = pygame.font.Font(None, max(36, int(screen_height * 0.09)))

layout()

def draw_text_centered(font, text, color, center):
    surface = font.render(text, True, color)
    ink = surface.get_bounding_rect()  # Center the visible letters, not the font's full line height
    screen.blit(surface, (center[0] - ink.centerx, center[1] - ink.centery))

def inset_triangle(points, distance):
    """The same triangle with every edge moved inward by distance (shrunk about its incenter)."""
    (ax, ay), (bx, by), (cx, cy) = points
    a = ((bx - cx) ** 2 + (by - cy) ** 2) ** 0.5  # side lengths opposite each corner
    b = ((ax - cx) ** 2 + (ay - cy) ** 2) ** 0.5
    c = ((ax - bx) ** 2 + (ay - by) ** 2) ** 0.5
    perimeter = a + b + c
    ix, iy = (a * ax + b * bx + c * cx) / perimeter, (a * ay + b * by + c * cy) / perimeter
    area = abs((bx - ax) * (cy - ay) - (cx - ax) * (by - ay)) / 2
    scale = max(0.0, 1 - distance / (2 * area / perimeter))  # inradius = area / half the perimeter
    return [(ix + (x - ix) * scale, iy + (y - iy) * scale) for x, y in points]

def draw_arrow(rect, pointing_up, hovered):
    width = rect.width * 0.35
    cx = rect.centerx
    if pointing_up:
        points = [(cx, rect.top), (cx - width / 2, rect.bottom), (cx + width / 2, rect.bottom)]
    else:
        points = [(cx, rect.bottom), (cx - width / 2, rect.top), (cx + width / 2, rect.top)]
    # A black triangle with a smaller colored one inside: pygame's thick outlines sit slightly
    # off-center, which let the fill poke out past the border on one side
    pygame.draw.polygon(screen, BLACK, points)
    pygame.draw.polygon(screen, WHITE if hovered else HOLD_GOLD, inset_triangle(points, 2.5))

def draw_reel(i, reel, now, mouse):
    rect = reel_rects[i]
    pygame.draw.rect(screen, REEL_FACE, rect, border_radius=12)
    # Letters, clipped to the reel's window so rolling letters slide in and out of view
    screen.set_clip(rect)
    if reel.strip:
        position = reel.position(now)
        index = int(position)
        offset = (position - index) * rect.height
        # The current letter slides down and out while the next one comes in from above
        draw_text_centered(letter_font, reel.strip[index], BLACK, (rect.centerx, rect.centery + offset))
        if index + 1 < len(reel.strip):
            draw_text_centered(letter_font, reel.strip[index + 1], BLACK,
                               (rect.centerx, rect.centery + offset - rect.height))
    else:
        draw_text_centered(letter_font, reel.letter, BLACK, rect.center)
    screen.set_clip(None)
    # A gold border marks a held reel
    pygame.draw.rect(screen, BLACK if reel.spins else HOLD_GOLD, rect, 4 if reel.spins else 8, border_radius=12)

    if not reel.spins:
        draw_arrow(up_arrows[i], True, up_arrows[i].collidepoint(mouse))
        draw_arrow(down_arrows[i], False, down_arrows[i].collidepoint(mouse))

    toggle = toggles[i]
    pygame.draw.rect(screen, TOGGLE_GREEN if reel.spins else HOLD_GOLD, toggle, border_radius=8)
    pygame.draw.rect(screen, BLACK, toggle, 2, border_radius=8)
    draw_text_centered(label_font, "SPIN" if reel.spins else "HOLD", WHITE if reel.spins else BLACK, toggle.center)

def draw(mouse):
    now = pygame.time.get_ticks()
    screen.fill(BACKGROUND)
    machine = pygame.Rect(0, 0, reel_rects[2].right - reel_rects[0].left + 80,
                          toggles[0].bottom - up_arrows[0].top + 50)
    machine.midtop = (screen_width // 2, up_arrows[0].top - 25)
    pygame.draw.rect(screen, MACHINE, machine, border_radius=24)
    pygame.draw.rect(screen, BLACK, machine, 4, border_radius=24)
    for i, reel in enumerate(reels):
        draw_reel(i, reel, now, mouse)

    can_spin = any(reel.spins for reel in reels) and not spinning()
    pygame.draw.rect(screen, SPIN_GREEN if can_spin else DISABLED, spin_button, border_radius=14)
    pygame.draw.rect(screen, BLACK, spin_button, 3, border_radius=14)
    draw_text_centered(spin_font, "SPIN!", WHITE, spin_button.center)

def handle_click(pos):
    if spinning():
        return  # Wait for the reels to stop
    if spin_button.collidepoint(pos):
        if any(reel.spins for reel in reels):
            spin()
        return
    for i, reel in enumerate(reels):
        if toggles[i].collidepoint(pos):
            reel.spins = not reel.spins
        elif not reel.spins and up_arrows[i].collidepoint(pos):
            reel.step(-1)  # Up goes back through the alphabet, like scrolling a list up
        elif not reel.spins and down_arrows[i].collidepoint(pos):
            reel.step(1)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.VIDEORESIZE:
            screen_width, screen_height = event.w, event.h
            screen = pygame.display.set_mode((screen_width, screen_height), pygame.RESIZABLE)
            layout()
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            handle_click(event.pos)
        elif event.type == pygame.KEYDOWN and event.key in (pygame.K_SPACE, pygame.K_RETURN):
            if not spinning() and any(reel.spins for reel in reels):
                spin()

    now = pygame.time.get_ticks()
    for reel in reels:
        reel.update(now)
    draw(pygame.mouse.get_pos())
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
