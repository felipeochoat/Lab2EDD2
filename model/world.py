# model/world.py
import random
import math
from model.constants import (
    SCREEN_W, GAME_PANEL_Y, GAME_PANEL_H, GROUND_Y,
    C_BLACK, C_DARK, C_BLUE, C_RED, C_GREEN, C_PURPLE, C_YELLOW
)
from model.npc import NPC


WORLD_WIDTH = SCREEN_W * 4  # scrollable world


class Building:
    def __init__(self, x, w, h, color, windows=True):
        self.x = x
        self.w = w
        self.h = h
        self.color   = color
        self.windows = windows
        self.win_color = random.choice([C_YELLOW, C_BLUE, C_GREEN, (40, 40, 60)])

    @property
    def top(self):
        return GROUND_Y - self.h


class RainDrop:
    def __init__(self, world_w):
        self.x = random.uniform(0, world_w)
        self.y = random.uniform(GAME_PANEL_Y, GROUND_Y)
        self.speed = random.uniform(3, 8)
        self.length = random.randint(4, 14)
        self.alpha  = random.randint(30, 90)


class Particle:
    def __init__(self, x, y, vx, vy, color, life=40, radius=2):
        self.x = x; self.y = y
        self.vx = vx; self.vy = vy
        self.color  = color
        self.life   = life
        self.max_life = life
        self.radius = radius

    def update(self):
        self.x  += self.vx
        self.y  += self.vy
        self.vy += 0.15
        self.life -= 1

    @property
    def alive(self):
        return self.life > 0

    @property
    def alpha(self):
        return int(255 * self.life / self.max_life)


class GameWorld:
    """Side-scrolling game world: buildings, rain, particles, NPC placement."""

    def __init__(self, graph):
        random.seed(7)
        self.width    = WORLD_WIDTH
        self.buildings = []
        self.rain      = []
        self.particles = []
        self.npcs      = []
        self.cam_x     = 0.0
        self._build_buildings()
        self._build_rain()
        self._place_npcs(graph)

    def _build_buildings(self):
        palette = [
            (12, 18, 32), (8, 14, 26), (16, 24, 40),
            (10, 20, 35), (14, 10, 28), (6, 16, 30),
        ]
        x = -100
        while x < self.width + 200:
            w = random.randint(60, 160)
            h = random.randint(60, 220)
            col = random.choice(palette)
            self.buildings.append(Building(x, w, h, col))
            x += w + random.randint(4, 20)

    def _build_rain(self):
        for _ in range(120):
            self.rain.append(RainDrop(self.width))

    def _place_npcs(self, graph):
        spacing = self.width / (len(graph.nodes) + 1)
        for i, node in enumerate(graph.nodes):
            wx = spacing * (i + 1)
            npc = NPC(node.id, node.name, wx, node.node_type)
            npc.patrol_min = wx - 100
            npc.patrol_max = wx + 100
            self.npcs.append(npc)

    def update(self, player):
        # Camera follows player (smooth)
        target_cam = player.x - SCREEN_W / 2
        target_cam = max(0, min(self.width - SCREEN_W, target_cam))
        self.cam_x += (target_cam - self.cam_x) * 0.10

        # Rain
        for r in self.rain:
            r.y += r.speed
            if r.y > GROUND_Y:
                r.y = GAME_PANEL_Y
                r.x = random.uniform(self.cam_x, self.cam_x + SCREEN_W)

        # NPCs
        for npc in self.npcs:
            npc.update()

        # Particles
        self.particles = [p for p in self.particles if p.alive]
        for p in self.particles:
            p.update()

    def spawn_particles(self, x, y, color, count=12, spread=4):
        import random
        for _ in range(count):
            vx = random.uniform(-spread, spread)
            vy = random.uniform(-spread * 0.8, 0)
            r  = random.randint(2, 4)
            self.particles.append(Particle(x, y, vx, vy, color, life=random.randint(25, 55), radius=r))

    def npc_near_player(self, player_x, threshold=60):
        for npc in self.npcs:
            if abs(npc.x - player_x) < threshold:
                return npc
        return None
