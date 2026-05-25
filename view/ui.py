# view/ui.py
"""
Bottom UI panel: dialogue box, stat bars, algorithm buttons, mission info.
Additions:
  - XP popup floating text
  - dlg_name exposed for controller checks
  - highlighted "recommended" button per mission
  - cleaner layout with step counter
"""
import pygame
import math
from model.constants import (
    SCREEN_W, SCREEN_H, UI_PANEL_Y, UI_PANEL_H,
    C_BLACK, C_DARK, C_PANEL, C_GREY, C_GREY2,
    C_RED, C_BLUE, C_GREEN, C_PURPLE, C_YELLOW, C_ORANGE, C_WHITE,
)
from view.effects import pulse_value


# Which button is "recommended" for each mission
MISSION_RECOMMENDED = {
    0: ["bfs", "dfs"],
    1: ["dijkstra"],
    2: ["kruskal"],
    3: ["ff"],
    4: ["bfs", "dijkstra", "kruskal", "ff"],
}


class XPPopup:
    def __init__(self, text, x, y):
        self.text  = text
        self.x     = float(x)
        self.y     = float(y)
        self.life  = 60      # frames
        self.max_life = 60

    @property
    def alive(self):
        return self.life > 0

    def update(self):
        self.life -= 1
        self.y    -= 0.8

    @property
    def alpha(self):
        return int(255 * self.life / self.max_life)


class UIPanel:
    def __init__(self, screen):
        self.screen  = screen
        self._rebuild_fonts()

        # Dialogue — dlg_name exposed so controller can check it
        self.dlg_name   = "SISTEMA"
        self.dlg_text   = "Bienvenido a NetGuardian."
        self.dlg_choices= []

        # Stats
        self.toxicity    = 0.6
        self.visited_pct = 0.0
        self.trust       = 0.3
        self.score       = 0
        self.mission     = 0

        # Algo button states: btn_id -> 'normal' | 'active' | 'done'
        self.btn_states = {}
        self.t = 0

        # XP popups
        self._popups: list[XPPopup] = []

    def _rebuild_fonts(self):
        """Reconstruye las fuentes según AJUSTES['tamaño']."""
        try:
            from view.menus import AJUSTES
            tam = AJUSTES.get("tamaño", "NORMAL")
        except Exception:
            tam = "NORMAL"
        if tam == "GRANDE":
            scale = 1.35
        elif tam == "PEQUEÑO":
            scale = 0.80
        else:
            scale = 1.0
        def sz(base): return max(7, int(base * scale))
        self.font_xs = pygame.font.SysFont("consolas", sz(9))
        self.font_sm = pygame.font.SysFont("consolas", sz(11))
        self.font_md = pygame.font.SysFont("consolas", sz(13), bold=True)
        self.font_lg = pygame.font.SysFont("consolas", sz(15), bold=True)
        self.font_xl = pygame.font.SysFont("consolas", sz(20), bold=True)

    # ── Public API ─────────────────────────────────────────────────────────────
    def set_dialogue(self, name, text, choices=None):
        self.dlg_name    = name
        self.dlg_text    = text
        self.dlg_choices = choices or []
        self._rebuild_fonts()   # actualiza fuentes si cambiaron ajustes

    def show_xp_popup(self, text, screen_x, screen_y):
        self._popups.append(XPPopup(text, screen_x, screen_y))

    def tick_popups(self):
        for p in self._popups:
            p.update()
        self._popups = [p for p in self._popups if p.alive]

    def draw_xp_popups(self, surface):
        for p in self._popups:
            surf = self.font_md.render(p.text, True, C_GREEN)
            surf.set_alpha(p.alpha)
            surface.blit(surf, (int(p.x) - surf.get_width() // 2, int(p.y)))

    def update(self, graph, player, mission):
        self.t += 1
        total = len(graph.nodes)
        self.visited_pct = graph.visited_count() / total
        self.toxicity    = graph.toxicity_level()
        self.trust       = 1 - self.toxicity
        self.score       = player.score
        self.mission     = mission

    # ── Main draw ──────────────────────────────────────────────────────────────
    def draw(self, algo_label="", algo_callbacks=None):
        s = self.screen

        pygame.draw.rect(s, (5, 9, 17), (0, UI_PANEL_Y, SCREEN_W, UI_PANEL_H))
        pygame.draw.line(s, (20, 40, 80), (0, UI_PANEL_Y), (SCREEN_W, UI_PANEL_Y), 2)

        # Column dividers
        for dx in (310, 540, 730):
            pygame.draw.line(s, (14, 26, 48), (dx, UI_PANEL_Y + 4), (dx, SCREEN_H - 4), 1)

        self._draw_dialogue(s,   0, UI_PANEL_Y, 308, UI_PANEL_H)
        self._draw_stats(   s, 314, UI_PANEL_Y, 222, UI_PANEL_H, algo_label)
        self._draw_algo_btns(s, 544, UI_PANEL_Y, 182, UI_PANEL_H)
        self._draw_mission( s, 734, UI_PANEL_Y, SCREEN_W - 734, UI_PANEL_H)

    # ── Sections ───────────────────────────────────────────────────────────────
    def _draw_dialogue(self, s, x, y, w, h):
        # Speaker name with colored bar
        name_col = C_YELLOW if self.dlg_name.startswith("🔎") or self.dlg_name.startswith("🛡") \
                   else C_RED if "⚠" in self.dlg_name \
                   else C_GREEN if "✅" in self.dlg_name or "💚" in self.dlg_name \
                   else C_BLUE
        pygame.draw.rect(s, (*name_col, 30), (x, y, w, 20))   # subtle tint bg
        name_surf = self.font_md.render(self.dlg_name[:36], True, name_col)
        s.blit(name_surf, (x + 8, y + 3))
        pygame.draw.line(s, (*name_col, 80), (x + 6, y + 20), (x + w - 6, y + 20), 1)

        # Word-wrapped body text
        words = self.dlg_text.split()
        lines, line = [], ""
        for word in words:
            test = (line + " " + word).strip()
            if self.font_sm.size(test)[0] > w - 16:
                lines.append(line); line = word
            else:
                line = test
        if line: lines.append(line)

        for i, ln in enumerate(lines[:6]):
            col = (170, 205, 245) if i == 0 else (120, 160, 210)
            s.blit(self.font_sm.render(ln, True, col), (x + 8, y + 24 + i * 14))

        # Bottom hint bar
        pygame.draw.line(s, (12, 22, 44), (x + 4, y + h - 18), (x + w - 4, y + h - 18), 1)
        hint = "[A/D] mover  [E] hablar  [Space] saltar  [1-5] algoritmos  [Esc] menú"
        hs = self.font_xs.render(hint, True, (22, 40, 68))
        s.blit(hs, (x + 6, y + h - 13))

    def _draw_bar(self, s, x, y, w, h_bar, value, color, label):
        s.blit(self.font_xs.render(label, True, (35, 60, 100)), (x, y))
        pygame.draw.rect(s, (10, 18, 36), (x, y + 11, w, h_bar))
        fw = int(w * max(0.0, min(1.0, value)))
        if fw > 0:
            pygame.draw.rect(s, color, (x, y + 11, fw, h_bar))
        pygame.draw.rect(s, (18, 36, 68), (x, y + 11, w, h_bar), 1)
        pct = self.font_xs.render(f"{int(value*100)}%", True, (45, 75, 115))
        s.blit(pct, (x + w + 4, y + 10))

    def _draw_stats(self, s, x, y, w, h, algo_label):
        s.blit(self.font_md.render("ESTADO RED", True, (28, 52, 96)), (x, y + 6))
        bw = w - 52
        self._draw_bar(s, x, y + 24, bw, 7, self.toxicity,    C_RED,   "TOXICIDAD")
        self._draw_bar(s, x, y + 46, bw, 7, self.visited_pct, C_BLUE,  "INVESTIGADO")
        self._draw_bar(s, x, y + 68, bw, 7, self.trust,       C_GREEN, "CONFIANZA")

        # Algo label
        s.blit(self.font_xs.render("ALGORITMO ACTIVO", True, (30, 55, 95)), (x, y + 90))
        pulse = pulse_value(self.t * 0.05)
        ac = tuple(int(c * pulse) for c in C_YELLOW)
        s.blit(self.font_md.render(algo_label or "—", True, ac), (x, y + 101))

        # Score
        s.blit(self.font_md.render(f"SCORE: {self.score} XP", True, C_GREEN), (x, y + h - 22))

    def _draw_algo_btns(self, s, x, y, w, h):
        BTNS = [
            ("bfs",      "⚡ BFS",          C_BLUE,               "[1]"),
            ("dfs",      "🔍 DFS",          C_PURPLE,             "[2]"),
            ("dijkstra", "🛡 DIJKSTRA",      C_GREEN,              "[3]"),
            ("kruskal",  "💚 KRUSKAL",       (0, 200, 120),        "[4]"),
            ("ff",       "🚫 FORD-FULKERSON",C_RED,                "[5]"),
        ]
        recommended = MISSION_RECOMMENDED.get(self.mission, [])

        s.blit(self.font_xs.render("ACTIVAR ALGORITMO:", True, (28, 52, 96)), (x, y + 4))

        for i, (bid, label, col, kshort) in enumerate(BTNS):
            by    = y + 18 + i * 27
            state = self.btn_states.get(bid, 'normal')
            is_rec   = bid in recommended
            is_locked = not is_rec and state not in ('done', 'active')

            if is_locked:
                # Grisado / bloqueado
                bg, bc = (8, 10, 18), (18, 22, 36)
                lc = (28, 36, 55)
            elif state == 'done':
                bg, bc = (12, 36, 14), C_GREEN
                lc = C_GREEN
            elif state == 'active':
                bg, bc = (40, 24, 4), C_YELLOW
                lc = C_YELLOW
            elif is_rec and state == 'normal':
                p = 0.5 + 0.5 * math.sin(self.t * 0.08)
                bg = (int(8 * p), int(18 * p), int(42 * p))
                bc = tuple(int(c * (0.5 + 0.5 * p)) for c in col)
                lc = col
            else:
                bg, bc = (10, 18, 36), (22, 42, 78)
                lc = col

            pygame.draw.rect(s, bg, (x, by, w - 4, 24))
            pygame.draw.rect(s, bc, (x, by, w - 4, 24), 1)

            ls = self.font_sm.render(label, True, lc)
            s.blit(ls, (x + 6, by + 5))

            if is_locked:
                ds = self.font_xs.render("🔒 BLOQ", True, (30, 40, 65))
                s.blit(ds, (x + w - ds.get_width() - 6, by + 7))
            elif state == 'done':
                ds = self.font_xs.render("✓ LISTO", True, C_GREEN)
                s.blit(ds, (x + w - ds.get_width() - 6, by + 7))
            elif state == 'active':
                ds = self.font_xs.render("▶ RUN", True, C_YELLOW)
                s.blit(ds, (x + w - ds.get_width() - 6, by + 7))
            elif is_rec:
                ds = self.font_xs.render(f"← {kshort}", True, bc)
                s.blit(ds, (x + w - ds.get_width() - 6, by + 7))
            else:
                ds = self.font_xs.render(kshort, True, (24, 44, 76))
                s.blit(ds, (x + w - ds.get_width() - 6, by + 7))

    def _draw_mission(self, s, x, y, w, h):
        from model.emotions import MISSIONS
        m = MISSIONS[self.mission] if self.mission < len(MISSIONS) else MISSIONS[-1]

        # Header
        s.blit(self.font_md.render(m['name'],  True, C_YELLOW), (x + 6, y + 5))
        s.blit(self.font_xs.render(m['algo'],  True, C_BLUE),   (x + 6, y + 22))
        pygame.draw.line(s, (18, 36, 68), (x + 4, y + 32), (x + w - 4, y + 32), 1)

        # Story
        words = m['story'].split()
        lines, line = [], ""
        for wd in words:
            test = (line + " " + wd).strip()
            if self.font_xs.size(test)[0] > w - 14:
                lines.append(line); line = wd
            else:
                line = test
        if line: lines.append(line)
        for i, ln in enumerate(lines[:4]):
            s.blit(self.font_xs.render(ln, True, (95, 135, 185)), (x + 6, y + 36 + i * 12))

        # Separator
        pygame.draw.line(s, (14, 28, 54), (x + 4, y + 84), (x + w - 4, y + 84), 1)

        # Objective
        s.blit(self.font_xs.render("▶ OBJETIVO:", True, C_GREEN), (x + 6, y + 88))
        gs = self.font_xs.render(m['goal'], True, (75, 155, 110))
        s.blit(gs, (x + 6, y + 100))

        # Hint
        hs = self.font_xs.render(f"💡 {m['hint']}", True, (50, 80, 130))
        s.blit(hs, (x + 6, y + 114))

        # Mission counter bottom-right
        from model.constants import MISSION_NAMES
        mc = self.font_xs.render(f"MISIÓN {self.mission+1}/{len(MISSION_NAMES)}", True, (28, 52, 85))
        s.blit(mc, (x + w - mc.get_width() - 6, y + h - 13))

    # ── Button hit test ────────────────────────────────────────────────────────
    def get_button_at(self, mouse_pos):
        x0 = 544
        y0 = UI_PANEL_Y + 18
        bids = ["bfs", "dfs", "dijkstra", "kruskal", "ff"]
        recommended = MISSION_RECOMMENDED.get(self.mission, bids)
        for i, bid in enumerate(bids):
            by = y0 + i * 27
            if pygame.Rect(x0, by, 178, 24).collidepoint(mouse_pos):
                if bid in recommended:
                    return bid
                return None   # bloqueado visualmente
        return None
