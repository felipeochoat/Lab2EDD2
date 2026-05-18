# model/player.py
from model.constants import (
    PLAYER_SPEED, PLAYER_RUN_MULT, PLAYER_JUMP,
    GRAVITY, GROUND_Y, GAME_PANEL_Y, GAME_PANEL_H
)


class Player:
    """Player character — the NetGuardian investigator."""

    def __init__(self, x, y):
        self.x      = float(x)
        self.y      = float(y)
        self.vx     = 0.0
        self.vy     = 0.0
        self.w      = 20
        self.h      = 28
        self.on_ground = True
        self.facing    = 1       # 1 = right, -1 = left
        self.running   = False
        self.score     = 0
        self.missions_done = set()

        # Animation
        self.anim_frame = 0.0
        self.anim_timer = 0.0

        # Interaction
        self.near_npc   = None  # NPC id if close enough to talk
        self.interacting= False

    @property
    def ground(self):
        return GROUND_Y

    def handle_input(self, keys_held):
        import pygame
        speed = PLAYER_SPEED * (PLAYER_RUN_MULT if self.running else 1)

        self.running = keys_held.get(pygame.K_LSHIFT, False) or keys_held.get(pygame.K_RSHIFT, False)

        moving = False
        if keys_held.get(pygame.K_LEFT) or keys_held.get(pygame.K_a):
            self.vx = -speed
            self.facing = -1
            moving = True
        elif keys_held.get(pygame.K_RIGHT) or keys_held.get(pygame.K_d):
            self.vx = speed
            self.facing = 1
            moving = True
        else:
            self.vx *= 0.75   # friction

        if moving:
            self.anim_timer += 1
            if self.anim_timer >= (4 if self.running else 7):
                self.anim_frame = (self.anim_frame + 1) % 4
                self.anim_timer = 0
        else:
            self.anim_frame = 0

    def jump(self):
        if self.on_ground:
            self.vy = PLAYER_JUMP
            self.on_ground = False

    def update(self, world_width):
        # Gravity
        self.vy += GRAVITY
        self.y  += self.vy
        self.x  += self.vx

        # Ground collision
        ground = self.ground
        if self.y + self.h / 2 >= ground:
            self.y        = ground - self.h / 2
            self.vy       = 0
            self.on_ground= True

        # World bounds
        self.x = max(12, min(world_width - 12, self.x))

    def rect(self):
        """Axis-aligned bounding box as (left, top, w, h)."""
        return (self.x - self.w/2, self.y - self.h/2, self.w, self.h)

    def add_score(self, pts):
        self.score += pts
