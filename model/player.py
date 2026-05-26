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
        self.mission_xp = 0   # XP acumulada en la misión actual (se resetea al avanzar)
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

    def handle_input(self, keys_held, left_key=None, right_key=None):
        """
        Procesa el input del jugador.
        - J1: llama sin left_key/right_key → usa solo A y D de keys_held
        - J2: llama con left_key=K_LEFT, right_key=K_RIGHT y su propio keys_held
        """
        import pygame
        speed = PLAYER_SPEED * (PLAYER_RUN_MULT if self.running else 1)

        self.running = keys_held.get(pygame.K_LSHIFT, False) or keys_held.get(pygame.K_RSHIFT, False)

        if left_key is not None:
            # J2: usa solo las teclas explícitas pasadas
            go_left  = bool(keys_held.get(left_key))
            go_right = bool(keys_held.get(right_key))
        else:
            # J1: solo A y D (las flechas son exclusivas del J2)
            go_left  = bool(keys_held.get(pygame.K_a))
            go_right = bool(keys_held.get(pygame.K_d))

        moving = False
        if go_left:
            self.vx = -speed
            self.facing = -1
            moving = True
        elif go_right:
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
        self.mission_xp += pts

    def reset_mission_xp(self):
        """Llamar al avanzar de misión."""
        self.mission_xp = 0
