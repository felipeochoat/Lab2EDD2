# view/menus.py
"""
Main menu, pause screen, and cinematic intro for NetGuardian.
"""
import pygame
import math
import random
from model.constants import (
    SCREEN_W, SCREEN_H,
    C_BLACK, C_DARK, C_BLUE, C_GREEN, C_RED, C_YELLOW, C_WHITE, C_PURPLE
)
from view.effects import pulse_value


class MenuParticle:
    def __init__(self):
        self.reset()

    def reset(self):
        self.x = random.uniform(0, SCREEN_W)
        self.y = random.uniform(0, SCREEN_H)
        self.vx = random.uniform(-0.4, 0.4)
        self.vy = random.uniform(-0.8, -0.2)
        self.col = random.choice([C_BLUE, C_GREEN, C_PURPLE, (100, 0, 200)])
        self.size = random.randint(1, 3)
        self.life = random.randint(60, 200)
        self.max_life = self.life

    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.life -= 1
        if self.life <= 0 or self.y < 0:
            self.reset()


class MainMenu:
    OPTIONS = ["NUEVA PARTIDA", "CONTINUAR", "CONFIGURACION", "SALIR"]

    def __init__(self, screen):
        self.screen   = screen
        self.selected = 0
        self.t        = 0
        self.particles= [MenuParticle() for _ in range(80)]
        self.font_xl  = pygame.font.SysFont("consolas", 42, bold=True)
        self.font_lg  = pygame.font.SysFont("consolas", 22, bold=True)
        self.font_md  = pygame.font.SysFont("consolas", 14)
        self.font_sm  = pygame.font.SysFont("consolas", 11)
        # Floating nodes for bg
        self.bg_nodes = [
            {"x": random.uniform(0, SCREEN_W),
             "y": random.uniform(0, SCREEN_H),
             "vx": random.uniform(-0.3, 0.3),
             "vy": random.uniform(-0.3, 0.3),
             "r":  random.randint(4, 12),
             "col": random.choice([C_BLUE, C_GREEN, C_PURPLE, C_RED]),
             "phase": random.uniform(0, math.pi*2)}
            for _ in range(20)
        ]

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_UP, pygame.K_w):
                self.selected = (self.selected - 1) % len(self.OPTIONS)
            elif event.key in (pygame.K_DOWN, pygame.K_s):
                self.selected = (self.selected + 1) % len(self.OPTIONS)
            elif event.key in (pygame.K_RETURN, pygame.K_SPACE):
                return self.OPTIONS[self.selected]
        if event.type == pygame.MOUSEBUTTONDOWN:
            for i in range(len(self.OPTIONS)):
                oy = SCREEN_H // 2 + i * 48 - 40
                rect = pygame.Rect(SCREEN_W//2 - 150, oy - 4, 300, 36)
                if rect.collidepoint(event.pos):
                    return self.OPTIONS[i]
        if event.type == pygame.MOUSEMOTION:
            for i in range(len(self.OPTIONS)):
                oy = SCREEN_H // 2 + i * 48 - 40
                rect = pygame.Rect(SCREEN_W//2 - 150, oy - 4, 300, 36)
                if rect.collidepoint(event.pos):
                    self.selected = i
        return None

    def update(self):
        self.t += 1
        for p in self.particles:
            p.update()
        for n in self.bg_nodes:
            n["x"] = (n["x"] + n["vx"]) % SCREEN_W
            n["y"] = (n["y"] + n["vy"]) % SCREEN_H

    def draw(self):
        s = self.screen
        s.fill(C_BLACK)

        # Gradient bg
        for y in range(SCREEN_H):
            ratio = y / SCREEN_H
            r = int(4 + 8  * ratio)
            g = int(6 + 10 * ratio)
            b = int(12 + 22 * ratio)
            pygame.draw.line(s, (r, g, b), (0, y), (SCREEN_W, y))

        # BG nodes + connections
        for i, n in enumerate(self.bg_nodes):
            for j, m in enumerate(self.bg_nodes):
                if j <= i:
                    continue
                dist = math.hypot(n["x"]-m["x"], n["y"]-m["y"])
                if dist < 180:
                    alpha = int(80 * (1 - dist/180))
                    ls = pygame.Surface((SCREEN_W, SCREEN_H), pygame.SRCALPHA)
                    col = (*n["col"], alpha)
                    pygame.draw.line(ls, col, (int(n["x"]), int(n["y"])), (int(m["x"]), int(m["y"])))
                    s.blit(ls, (0,0))
            pulse = pulse_value(self.t * 0.04 + n["phase"])
            r = int(n["r"] + pulse * 3)
            pygame.draw.circle(s, n["col"], (int(n["x"]), int(n["y"])), r)
            pygame.draw.circle(s, (255,255,255), (int(n["x"]), int(n["y"])), r, 1)

        # Particles
        for p in self.particles:
            alpha = int(200 * p.life / p.max_life)
            ps = pygame.Surface((p.size*2+2, p.size*2+2), pygame.SRCALPHA)
            pygame.draw.circle(ps, (*p.col, alpha), (p.size+1, p.size+1), p.size)
            s.blit(ps, (int(p.x)-p.size, int(p.y)-p.size))

        # Scanlines
        sl = pygame.Surface((SCREEN_W, SCREEN_H), pygame.SRCALPHA)
        for y in range(0, SCREEN_H, 4):
            pygame.draw.line(sl, (0, 0, 0, 18), (0, y), (SCREEN_W, y))
        s.blit(sl, (0,0))

        # --- LOGO ---
        cy = SCREEN_H // 2 - 130
        pulse_title = pulse_value(self.t * 0.03, lo=0.7, hi=1.0)

        # Glow behind logo
        gsurf = pygame.Surface((700, 80), pygame.SRCALPHA)
        for gr in range(40, 0, -2):
            ga = int(30 * (1 - gr/40))
            pygame.draw.rect(gsurf, (0, 180, 255, ga), (350-gr*8, 40-gr, gr*16, gr*2))
        s.blit(gsurf, (SCREEN_W//2 - 350, cy - 20))

        t1 = self.font_xl.render("NET", True, C_BLUE)
        t2 = self.font_xl.render("GUARDIAN", True, C_GREEN)
        total_w = t1.get_width() + t2.get_width() + 8
        s.blit(t1, (SCREEN_W//2 - total_w//2, cy))
        s.blit(t2, (SCREEN_W//2 - total_w//2 + t1.get_width() + 8, cy))

        sub = self.font_md.render("Investigación de Ciberacoso — Algoritmos de Grafos", True, (50, 80, 130))
        s.blit(sub, (SCREEN_W//2 - sub.get_width()//2, cy + 50))

        # --- OPTIONS ---
        for i, opt in enumerate(self.OPTIONS):
            oy  = SCREEN_H // 2 + i * 48 - 40
            sel = (i == self.selected)
            bg  = (8, 20, 40) if sel else (4, 10, 20)
            bc  = C_BLUE if sel else (20, 40, 70)
            pygame.draw.rect(s, bg, (SCREEN_W//2 - 150, oy - 4, 300, 36))
            pygame.draw.rect(s, bc, (SCREEN_W//2 - 150, oy - 4, 300, 36), 1)
            col = C_YELLOW if sel else (60, 100, 160)
            ts = self.font_lg.render(opt, True, col)
            s.blit(ts, (SCREEN_W//2 - ts.get_width()//2, oy + 2))

        # Footer
        footer = self.font_sm.render("Universidad del Norte · Estructura de Datos II · 2026", True, (20, 38, 65))
        s.blit(footer, (SCREEN_W//2 - footer.get_width()//2, SCREEN_H - 22))


class VictoryScreen:
    def __init__(self, screen, score):
        self.screen = screen
        self.score  = score
        self.t      = 0
        self.font_xl= pygame.font.SysFont("consolas", 38, bold=True)
        self.font_lg= pygame.font.SysFont("consolas", 20, bold=True)
        self.font_md= pygame.font.SysFont("consolas", 14)

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN and event.key in (pygame.K_RETURN, pygame.K_ESCAPE):
            return "menu"
        return None

    def update(self):
        self.t += 1

    def draw(self):
        s = self.screen
        s.fill((4, 10, 20))
        ov = pygame.Surface((SCREEN_W, SCREEN_H), pygame.SRCALPHA)
        ov.fill((0, 200, 100, 15))
        s.blit(ov, (0, 0))

        p = pulse_value(self.t * 0.04)
        col = tuple(int(c * (0.7 + 0.3 * p)) for c in C_GREEN)
        t1 = self.font_xl.render("🌐 RED RESTAURADA", True, col)
        s.blit(t1, (SCREEN_W//2 - t1.get_width()//2, SCREEN_H//2 - 80))
        t2 = self.font_lg.render(f"PUNTUACIÓN FINAL: {self.score} XP", True, C_YELLOW)
        s.blit(t2, (SCREEN_W//2 - t2.get_width()//2, SCREEN_H//2))
        t3 = self.font_md.render("El ciberacoso fue detenido. La red social es segura.", True, (100, 180, 140))
        s.blit(t3, (SCREEN_W//2 - t3.get_width()//2, SCREEN_H//2 + 40))
        t4 = self.font_md.render("[ENTER] Volver al menú", True, (40, 80, 100))
        s.blit(t4, (SCREEN_W//2 - t4.get_width()//2, SCREEN_H//2 + 80))
