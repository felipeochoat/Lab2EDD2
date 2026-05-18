# view/effects.py
import pygame
import random
import math


class GlitchEffect:
    """Horizontal scanline glitch effect."""

    def __init__(self, screen):
        self.screen  = screen
        self.active  = False
        self.timer   = 0
        self.duration= 0
        self.intensity = 1.0

    def trigger(self, duration=45, intensity=1.0):
        self.active    = True
        self.timer     = 0
        self.duration  = duration
        self.intensity = intensity

    def update_draw(self):
        if not self.active:
            return
        self.timer += 1
        if self.timer >= self.duration:
            self.active = False
            return

        W, H = self.screen.get_size()
        progress = self.timer / self.duration

        # Random horizontal slices displaced
        num_slices = int(6 * self.intensity * (1 - progress * 0.5))
        for _ in range(num_slices):
            y     = random.randint(0, H)
            h     = random.randint(2, 14)
            shift = random.randint(-30, 30)
            try:
                sub = self.screen.subsurface(pygame.Rect(0, y, W, min(h, H - y)))
                self.screen.blit(sub, (shift, y))
            except Exception:
                pass

        # Red/blue chromatic channel offset
        if random.random() < 0.4 * self.intensity:
            ca = pygame.Surface((W, H), pygame.SRCALPHA)
            ca.fill((255, 0, 0, 18))
            self.screen.blit(ca, (random.randint(-4, 4), 0))
            ca.fill((0, 0, 255, 18))
            self.screen.blit(ca, (random.randint(-4, 4), 0))

        # Occasional full-screen flash
        if self.timer < 4 and self.intensity > 0.8:
            flash = pygame.Surface((W, H), pygame.SRCALPHA)
            flash.fill((255, 30, 50, 60))
            self.screen.blit(flash, (0, 0))


class ScanlineEffect:
    """Subtle CRT scanline overlay."""

    def __init__(self, screen):
        self.surface = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
        W, H = screen.get_size()
        for y in range(0, H, 3):
            pygame.draw.line(self.surface, (0, 0, 0, 28), (0, y), (W, y))

    def draw(self, screen):
        screen.blit(self.surface, (0, 0))


class DigitalRain:
    """Matrix-style falling character columns (background ambiance)."""

    CHARS = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789@#$%&*"

    def __init__(self, screen, panel_rect):
        self.screen = screen
        self.rect   = panel_rect
        self.font   = pygame.font.SysFont("consolas", 10)
        W, H = panel_rect.width, panel_rect.height
        self.cols   = W // 12
        self.drops  = [random.randint(0, H // 12) for _ in range(self.cols)]
        self.chars  = [[random.choice(self.CHARS) for _ in range(H // 12 + 2)]
                       for _ in range(self.cols)]
        self.timer  = 0

    def update(self):
        self.timer += 1
        if self.timer % 4 == 0:
            for i in range(self.cols):
                self.drops[i] += 1
                H = self.rect.height // 12
                if self.drops[i] > H + 4:
                    self.drops[i] = 0
                # Randomise a character in the trail
                row = random.randint(0, len(self.chars[i]) - 1)
                self.chars[i][row] = random.choice(self.CHARS)

    def draw(self):
        rx, ry = self.rect.left, self.rect.top
        for col_i in range(self.cols):
            drop = self.drops[col_i]
            for row_i, ch in enumerate(self.chars[col_i]):
                y = ry + row_i * 12
                if y < ry or y > ry + self.rect.height:
                    continue
                if row_i == drop:
                    color = (200, 255, 220)
                elif drop - 1 <= row_i <= drop:
                    color = (0, 255, 120, 200)
                else:
                    alpha = max(0, 160 - (drop - row_i) * 18)
                    color = (0, int(180 * alpha / 160), int(80 * alpha / 160))
                surf = self.font.render(ch, True, color)
                self.screen.blit(surf, (rx + col_i * 12, y))


def draw_neon_circle(surface, color, cx, cy, radius, width=2, alpha=180, glow_radius=0):
    """Draw a circle with optional glow halo."""
    if glow_radius > 0:
        glow = pygame.Surface((glow_radius * 2 + 4, glow_radius * 2 + 4), pygame.SRCALPHA)
        r, g, b = color
        for gr in range(glow_radius, 0, -2):
            a = int(alpha * (1 - gr / glow_radius) * 0.5)
            pygame.draw.circle(glow, (r, g, b, a), (glow_radius + 2, glow_radius + 2), gr)
        surface.blit(glow, (cx - glow_radius - 2, cy - glow_radius - 2))
    pygame.draw.circle(surface, color, (int(cx), int(cy)), radius, width)


def draw_neon_line(surface, color, p1, p2, width=1, alpha=200):
    """Draw a line with glow."""
    r, g, b = color
    # Outer glow (thicker, dimmer)
    glow_col = (r, g, b, max(0, alpha - 120))
    temp = pygame.Surface(surface.get_size(), pygame.SRCALPHA)
    pygame.draw.line(temp, (*color, alpha - 60), p1, p2, width + 2)
    pygame.draw.line(temp, (*color, alpha),      p1, p2, width)
    surface.blit(temp, (0, 0))


def pulse_value(t, speed=2.0, lo=0.5, hi=1.0):
    """Sine-wave pulsing value."""
    return lo + (hi - lo) * (0.5 + 0.5 * math.sin(t * speed))
