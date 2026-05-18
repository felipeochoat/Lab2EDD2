# view/tilemap.py
"""
Renders the side-scrolling game world.
NPCs and player are drawn as pixel-art persons (no images needed).
Each NPC type has a distinct silhouette / color scheme.
"""
import pygame
import math
import random
from model.constants import (
    SCREEN_W, GAME_PANEL_Y, GAME_PANEL_H, GROUND_Y,
    C_BLACK, C_DARK, C_DARK2, C_BLUE, C_RED, C_GREEN,
    C_PURPLE, C_YELLOW, C_ORANGE, C_WHITE, C_GREY2,
    NODE_COLORS,
)
from view.effects import pulse_value


NPC_COLORS = {
    "victim":   (0,   180, 255),
    "bully":    (255, 42,  74),
    "follower": (160, 60,  220),
    "ally":     (0,   220, 110),
    "observer": (220, 200, 60),
    "bot":      (130, 0,   210),
    "origin":   (255, 0,   30),
    "neutral":  (80,  120, 180),
}

# Skin tones per type (head color)
NPC_SKIN = {
    "victim":   (200, 220, 255),
    "bully":    (255, 180, 160),
    "follower": (220, 180, 255),
    "ally":     (180, 255, 210),
    "observer": (255, 240, 180),
    "bot":      (180, 180, 220),
    "origin":   (255, 160, 160),
    "neutral":  (190, 210, 230),
}


def _draw_person(surf, cx, foot_y, col, skin, facing=1, anim=0, scale=1.0,
                 hat=False, hood=False, antenna=False, cape=False, revealed=False):
    """
    Draw a pixel-art person at (cx, foot_y).
    foot_y = y coordinate of the feet.
    scale  = size multiplier (1.0 = normal NPC, 1.3 = player)
    anim   = walk frame 0-3
    """
    s = scale
    # Body proportions (all relative to foot_y, pixel-snapped)
    leg_h   = int(10 * s)
    body_h  = int(10 * s)
    head_r  = int(5  * s)
    shoulder_w = int(7 * s)
    body_w  = int(6 * s)
    leg_w   = int(3 * s)

    # Walk offsets for legs
    walk_offsets = [(0, 0), (3, -2), (0, 0), (-3, -2)]
    lo = walk_offsets[anim % 4]
    leg_l = (int(cx - leg_w // 2 - 1), foot_y - leg_h + lo[0])
    leg_r = (int(cx + leg_w // 2 - 1), foot_y - leg_h - lo[0])

    # Arm swing
    arm_swing = [2, -1, -2, 1][anim % 4]

    # ── Glow halo ──────────────────────────────────────────────────────────────
    gw = int(40 * s)
    gh = int(50 * s)
    gsurf = pygame.Surface((gw * 2, gh), pygame.SRCALPHA)
    r, g, b = col
    pygame.draw.ellipse(gsurf, (r, g, b, 25), (0, gh // 4, gw * 2, gh // 2))
    surf.blit(gsurf, (cx - gw, foot_y - gh + 10))

    # ── Cape (origin) ──────────────────────────────────────────────────────────
    if cape:
        cape_pts = [
            (cx, foot_y - leg_h - body_h),
            (cx - int(shoulder_w * 1.4) * facing, foot_y - leg_h - body_h // 3),
            (cx - int(shoulder_w * 1.2) * facing, foot_y),
        ]
        pygame.draw.polygon(surf, (140, 0, 20), cape_pts)

    # ── Legs ───────────────────────────────────────────────────────────────────
    lc = tuple(max(0, c - 40) for c in col)
    # Left leg
    pygame.draw.rect(surf, lc,
        (cx - int(leg_w * 1.1), foot_y - leg_h + lo[0], leg_w, leg_h))
    # Right leg
    pygame.draw.rect(surf, lc,
        (cx + int(leg_w * 0.1), foot_y - leg_h - lo[0], leg_w, leg_h))

    # ── Body ───────────────────────────────────────────────────────────────────
    body_top = foot_y - leg_h - body_h
    body_x   = cx - body_w // 2
    pygame.draw.rect(surf, col, (body_x, body_top, body_w + 1, body_h))
    # Chest highlight
    hl = tuple(min(255, c + 60) for c in col)
    pygame.draw.rect(surf, hl, (body_x + 1, body_top + 1, body_w - 1, 3))

    # ── Arms ───────────────────────────────────────────────────────────────────
    arm_y = body_top + 2
    arm_c = tuple(max(0, c - 20) for c in col)
    # Left arm
    pygame.draw.line(surf, arm_c,
        (cx - body_w // 2, arm_y),
        (cx - body_w // 2 - int(4 * s), arm_y + int(6 * s) + arm_swing * facing), int(2 * s))
    # Right arm
    pygame.draw.line(surf, arm_c,
        (cx + body_w // 2, arm_y),
        (cx + body_w // 2 + int(4 * s), arm_y + int(6 * s) - arm_swing * facing), int(2 * s))

    # ── Head ───────────────────────────────────────────────────────────────────
    head_cx = cx
    head_cy = body_top - head_r
    pygame.draw.circle(surf, skin, (head_cx, head_cy), head_r)
    # Eyes
    eye_offset = int(2 * s) * facing
    eye_y = head_cy - int(1 * s)
    pygame.draw.circle(surf, (20, 20, 30), (head_cx + eye_offset, eye_y), max(1, int(1.5 * s)))
    # Mouth
    if revealed:
        pygame.draw.arc(surf, (200, 80, 80),
            pygame.Rect(head_cx - int(3*s), head_cy, int(6*s), int(3*s)), 0, math.pi, 1)
    else:
        pygame.draw.line(surf, (100, 100, 130),
            (head_cx - int(2*s), head_cy + int(2*s)),
            (head_cx + int(2*s), head_cy + int(2*s)), 1)

    # ── Accessories ────────────────────────────────────────────────────────────
    # Hat (bully)
    if hat:
        hat_col = tuple(max(0, c - 60) for c in col)
        pygame.draw.rect(surf, hat_col,
            (head_cx - head_r - 1, head_cy - head_r - int(5*s), (head_r + 1) * 2, int(5*s)))
        pygame.draw.rect(surf, hat_col,
            (head_cx - head_r - int(3*s), head_cy - head_r, (head_r + int(3*s)) * 2, int(3*s)))

    # Hood (observer)
    if hood:
        hood_col = tuple(max(0, c - 30) for c in col)
        pygame.draw.circle(surf, hood_col, (head_cx, head_cy - int(1*s)), head_r + int(2*s), int(2*s))

    # Antenna (bot)
    if antenna:
        ant_x = head_cx + int(2*s) * facing
        ant_top = head_cy - head_r - int(8*s)
        pygame.draw.line(surf, (180, 180, 255),
            (ant_x, head_cy - head_r), (ant_x, ant_top), 1)
        pygame.draw.circle(surf, (200, 200, 255), (ant_x, ant_top), int(2*s))

    # ── Border / outline pass (1px dark outline for readability) ───────────────
    # (skip for performance; the glow + contrast is enough)


def _pill_label(surf, font, text, cx, y, text_col, bg_alpha=175, pad=4):
    """Render text with a dark rounded-rectangle background."""
    ts  = font.render(text, True, text_col)
    tw, th = ts.get_size()
    pill = pygame.Surface((tw + pad * 2, th + pad), pygame.SRCALPHA)
    pill.fill((0, 0, 0, bg_alpha))
    surf.blit(pill, (cx - tw // 2 - pad, y - pad // 2))
    surf.blit(ts,   (cx - tw // 2,       y))


class WorldRenderer:
    def __init__(self, screen):
        self.screen  = screen
        self.t       = 0.0
        self.font_sm = pygame.font.SysFont("consolas", 9)
        self.font_md = pygame.font.SysFont("consolas", 11, bold=True)
        self.font_lg = pygame.font.SysFont("consolas", 14, bold=True)
        self.scanline_surf = pygame.Surface((SCREEN_W, GAME_PANEL_H), pygame.SRCALPHA)
        for y in range(0, GAME_PANEL_H, 3):
            pygame.draw.line(self.scanline_surf, (0, 0, 0, 20), (0, y), (SCREEN_W, y))

    def draw(self, world, player, near_npc=None):
        self.t += 1
        cam_x = world.cam_x
        clip  = pygame.Rect(0, GAME_PANEL_Y, SCREEN_W, GAME_PANEL_H)
        self.screen.set_clip(clip)
        surf  = self.screen

        # Sky gradient
        for yy in range(GAME_PANEL_H):
            ratio = yy / GAME_PANEL_H
            r = int(6  + 10  * ratio)
            g = int(10 + 14  * ratio)
            b = int(18 + 30  * ratio)
            pygame.draw.line(surf, (r, g, b),
                             (0, GAME_PANEL_Y + yy), (SCREEN_W, GAME_PANEL_Y + yy))

        # Stars / distant lights
        random.seed(99)
        for _ in range(60):
            sx = int((random.randint(0, SCREEN_W * 4) - cam_x * 0.15) % SCREEN_W)
            sy = GAME_PANEL_Y + random.randint(0, GAME_PANEL_H // 2)
            col = random.choice([(0,180,255),(0,255,120),(255,220,60),(200,100,255)])
            pygame.draw.circle(surf, col, (sx, sy), 1)
        random.seed(None)

        # Buildings
        for b in world.buildings:
            bx = int(b.x - cam_x * 0.8)
            bt = GROUND_Y - b.h
            if bx + b.w < 0 or bx > SCREEN_W:
                continue
            pygame.draw.rect(surf, b.color, (bx, bt, b.w, b.h))
            if b.windows:
                for wy in range(bt + 8, GROUND_Y - 8, 14):
                    for wx in range(bx + 6, bx + b.w - 4, 12):
                        wc = b.win_color
                        if (self.t + wx * 3 + wy) % 97 < 5:
                            wc = (220, 220, 220)
                        pygame.draw.rect(surf, wc, (wx, wy, 5, 7))
            hue = (bx // 20) % 4
            nc = [C_BLUE, C_GREEN, C_PURPLE, C_RED][hue]
            pygame.draw.line(surf, nc, (bx, bt), (bx + b.w, bt), 1)
            if b.h > 140:
                pygame.draw.line(surf, (30, 50, 70),
                                 (bx + b.w//2, bt), (bx + b.w//2, bt - 20), 1)
                pr = int(pulse_value(self.t * 0.06, speed=1, lo=2, hi=5))
                pygame.draw.circle(surf, C_RED, (bx + b.w//2, bt - 20), pr)

        # Ground
        pygame.draw.rect(surf, (8, 14, 26), (0, GROUND_Y, SCREEN_W, GAME_PANEL_H))
        pygame.draw.line(surf, (20, 40, 80), (0, GROUND_Y), (SCREEN_W, GROUND_Y), 2)
        for gx in range(0, SCREEN_W, 50):
            offset = int(cam_x * 0.2) % 50
            lx = gx - offset
            pygame.draw.line(surf, (12, 22, 40), (lx, GROUND_Y), (lx, GROUND_Y + 28), 1)

        # Rain
        rain_surf = pygame.Surface((SCREEN_W, GAME_PANEL_H), pygame.SRCALPHA)
        for r in world.rain:
            rx = int(r.x - cam_x) % SCREEN_W
            ry = int(r.y)
            if GAME_PANEL_Y <= ry <= GROUND_Y:
                pygame.draw.line(rain_surf, (0, 160, 255, r.alpha),
                                 (rx, ry), (rx - 1, ry + r.length))
        surf.blit(rain_surf, (0, GAME_PANEL_Y))

        # ── NPCs ──────────────────────────────────────────────────────────────
        for npc in world.npcs:
            nx = int(npc.x - cam_x)
            foot_y = GROUND_Y - 2
            if nx < -60 or nx > SCREEN_W + 60:
                continue

            col  = NPC_COLORS.get(npc.node_type, (80, 120, 180))
            skin = NPC_SKIN.get(npc.node_type, (200, 210, 230))
            bob  = int(math.sin(npc.bob) * 2)
            anim = npc.anim_frame

            # Accessories by type
            hat      = npc.node_type == "bully"
            hood     = npc.node_type == "observer"
            antenna  = npc.node_type == "bot"
            cape     = npc.node_type == "origin"

            _draw_person(surf, nx, foot_y + bob, col, skin,
                         facing=npc.facing, anim=anim, scale=1.0,
                         hat=hat, hood=hood, antenna=antenna, cape=cape,
                         revealed=npc.revealed)

            # Name tag
            name_col = (255, 255, 255) if npc.revealed else (160, 200, 255)
            _pill_label(surf, self.font_md, npc.name, nx, foot_y - 52 + bob,
                        name_col, bg_alpha=180, pad=4)

            # [E] HABLAR prompt
            if near_npc and near_npc.node_id == npc.node_id:
                _pill_label(surf, self.font_md, "[E] HABLAR", nx, foot_y - 68 + bob,
                            C_YELLOW, bg_alpha=200, pad=4)

            # ✓ revealed badge
            if npc.revealed:
                chk = self.font_md.render("✓", True, C_GREEN)
                surf.blit(chk, (nx + 16, foot_y - 44 + bob))

        # ── PLAYER ────────────────────────────────────────────────────────────
        px         = int(player.x - cam_x)
        foot_y     = GROUND_Y - 2
        jump_off   = min(0, int(player.vy * 1.2)) if not player.on_ground else 0
        walk_anim  = int(player.anim_frame)

        # Player is cyan/blue with a white-ish skin, slightly larger scale
        player_col  = (0, 160, 240)
        player_skin = (220, 240, 255)

        _draw_person(surf, px, foot_y + jump_off, player_col, player_skin,
                     facing=player.facing, anim=walk_anim, scale=1.3,
                     hat=False, hood=False, antenna=False, cape=False,
                     revealed=True)

        # GUARDIAN label
        _pill_label(surf, self.font_md, "GUARDIAN", px, foot_y + jump_off - 58,
                    (140, 215, 255), bg_alpha=170, pad=4)

        # ── Particles ─────────────────────────────────────────────────────────
        for p in world.particles:
            palpha = int(255 * p.life / p.max_life)
            pc = p.color + (palpha,)
            psurf = pygame.Surface((p.radius * 2 + 2, p.radius * 2 + 2), pygame.SRCALPHA)
            pygame.draw.circle(psurf, pc, (p.radius + 1, p.radius + 1), p.radius)
            surf.blit(psurf, (int(p.x - cam_x) - p.radius, int(p.y) - p.radius))

        # Scanlines
        surf.blit(self.scanline_surf, (0, GAME_PANEL_Y))
        self.screen.set_clip(None)
