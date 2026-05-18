# view/graph_view.py
"""
Renders the live social network graph in the top panel.
Changes:
  - Graph shifted down so top names aren't clipped
  - Node name labels: bigger font, bright color, dark shadow pill behind text
  - Weight / distance labels also more readable
"""
import pygame
import math
import random
from model.constants import (
    SCREEN_W, GRAPH_PANEL_H,
    C_BLACK, C_DARK, C_GREY, C_WHITE,
    C_RED, C_BLUE, C_GREEN, C_PURPLE, C_YELLOW, C_ORANGE,
    NODE_COLORS,
)
from view.effects import draw_neon_circle, pulse_value

# Push the graph circle down so top labels aren't clipped
GRAPH_Y_OFFSET = 22   # extra pixels from top


STATE_COLORS = {
    'visited':  C_GREEN,
    'in_queue': C_YELLOW,
    'in_path':  C_GREEN,
    'in_mst':   (0, 220, 120),
    'active':   C_BLUE,
    'origin':   C_RED,
    'default':  (18, 30, 52),
}


class EdgeParticle:
    def __init__(self, edge, graph, color):
        self.edge  = edge
        self.graph = graph
        self.t     = 0.0
        self.speed = random.uniform(0.008, 0.018)
        self.color = color
        self.size  = random.randint(2, 3)

    def update(self):
        self.t += self.speed
        return self.t < 1.0

    def position(self):
        a = self.graph.nodes[self.edge.a]
        b = self.graph.nodes[self.edge.b]
        x = a.x + (b.x - a.x) * self.t
        y = a.y + (b.y - a.y) * self.t
        return int(x), int(y)


def _draw_label(surf, font, text, cx, cy, text_color, bg_alpha=160, padding=3):
    """Draw text with a dark semi-transparent pill behind it for readability."""
    ts = font.render(text, True, text_color)
    tw, th = ts.get_size()
    # Dark background pill
    pill = pygame.Surface((tw + padding * 2, th + padding), pygame.SRCALPHA)
    pill.fill((0, 0, 0, bg_alpha))
    bx = cx - tw // 2 - padding
    by = cy - th // 2 - padding // 2
    surf.blit(pill, (bx, by))
    surf.blit(ts, (cx - tw // 2, cy - th // 2))


class GraphView:
    def __init__(self, screen, graph):
        self.screen  = screen
        self.graph   = graph
        self.surface = pygame.Surface((SCREEN_W, GRAPH_PANEL_H))
        self.t       = 0.0
        self.particles: list[EdgeParticle] = []

        # Fonts — bigger and bolder than before
        self.font_xs  = pygame.font.SysFont("consolas", 9)
        self.font_sm  = pygame.font.SysFont("consolas", 10, bold=True)
        self.font_md  = pygame.font.SysFont("consolas", 12, bold=True)   # node names
        self.font_lg  = pygame.font.SysFont("consolas", 13, bold=True)   # origin marker / HUD

        # Shift every node's y coordinate down once at init
        self._apply_y_offset()

    def _apply_y_offset(self):
        """Shift all node positions down so labels at the top aren't clipped."""
        for node in self.graph.nodes:
            node.y += GRAPH_Y_OFFSET

    def spawn_particles(self, edge, color=None, count=3):
        col = color or C_BLUE
        for _ in range(count):
            self.particles.append(EdgeParticle(edge, self.graph, col))

    def _node_color(self, node):
        if node.node_type == 'origin' and node.visited:
            return C_RED
        if node.visited:
            return NODE_COLORS.get(node.node_type, C_BLUE)
        if node.in_queue:
            return C_YELLOW
        if node.highlighted:
            return C_ORANGE
        return STATE_COLORS['default']

    def _edge_color(self, edge):
        if edge.in_mst:
            return C_GREEN
        if edge.in_path:
            return C_GREEN
        if edge.active or edge.lit > 0.3:
            return (0, 100, int(200 * edge.lit))
        return (20, 35, 60)

    def update(self, dt=1/60):
        self.t += dt * 60
        for e in self.graph.edges:
            if e.lit > 0:
                e.lit = max(0.0, e.lit - 0.015)
        self.particles = [p for p in self.particles if p.update()]

    def draw(self, mission=0, algo_label=""):
        surf = self.surface
        surf.fill(C_BLACK)

        # Grid
        for y in range(0, GRAPH_PANEL_H, 30):
            pygame.draw.line(surf, (12, 20, 36), (0, y), (SCREEN_W, y))
        for x in range(0, SCREEN_W, 40):
            pygame.draw.line(surf, (12, 20, 36), (x, 0), (x, GRAPH_PANEL_H))

        # ── Edges ──────────────────────────────────────────────────────────────
        temp = pygame.Surface((SCREEN_W, GRAPH_PANEL_H), pygame.SRCALPHA)
        for e in self.graph.edges:
            a = self.graph.nodes[e.a]
            b = self.graph.nodes[e.b]
            col  = self._edge_color(e)
            r, g, bv = col
            alpha = 190 if (e.active or e.in_mst or e.in_path) else 80
            if e.lit > 0.2 or e.in_mst or e.in_path:
                pygame.draw.line(temp, (r, g, bv, min(255, int(alpha * 0.4))),
                                 (int(a.x), int(a.y)), (int(b.x), int(b.y)), 4)
            pygame.draw.line(temp, (r, g, bv, alpha),
                             (int(a.x), int(a.y)), (int(b.x), int(b.y)), 1)

            # Weight label (missions 1+) — bright with shadow
            if mission >= 1:
                mx, my = int((a.x + b.x) / 2), int((a.y + b.y) / 2)
                _draw_label(surf, self.font_xs, str(e.weight), mx, my,
                            (160, 200, 255), bg_alpha=140, padding=2)

            # Flow label (mission 3)
            if mission == 3 and e.flow > 0:
                mx, my = int((a.x + b.x) / 2), int((a.y + b.y) / 2)
                _draw_label(surf, self.font_xs, f"{e.flow}/{e.capacity}", mx, my + 10,
                            C_RED, bg_alpha=150, padding=2)

        surf.blit(temp, (0, 0))

        # ── Particles ──────────────────────────────────────────────────────────
        for p in self.particles:
            px, py = p.position()
            draw_neon_circle(surf, p.color, px, py, p.size, width=0, glow_radius=6)

        # ── Nodes ──────────────────────────────────────────────────────────────
        for node in self.graph.nodes:
            pulse  = pulse_value(self.t * 0.04 + node.pulse, speed=1.0, lo=0.0, hi=3.5)
            base_r = node.radius
            col    = self._node_color(node)
            nx, ny = int(node.x), int(node.y)

            # Glow ring
            if node.visited or node.in_queue or node.node_type in ('victim', 'origin'):
                draw_neon_circle(surf, col, node.x, node.y,
                                 base_r + pulse + 5, width=1,
                                 glow_radius=int(base_r + pulse + 10))

            # Circle fill
            draw_r = base_r + int(pulse * 0.4)
            pygame.draw.circle(surf, col, (nx, ny), draw_r)

            # Border
            border_col = (
                C_RED    if node.node_type in ('origin', 'bully') else
                C_BLUE   if node.node_type == 'victim' else
                C_GREEN  if node.node_type == 'ally' else
                (30, 50, 80)
            )
            pygame.draw.circle(surf, border_col, (nx, ny), draw_r, 2)

            # ── Name label — always visible ────────────────────────────────────
            name = node.name if (node.node_type != 'origin' or node.visited) else "???"
            # Bright white when visited, lighter grey otherwise (never dark)
            name_col = (255, 255, 255) if node.visited else (180, 210, 255)
            label_y  = ny - draw_r - 10   # just above the node circle
            _draw_label(surf, self.font_md, name, nx, label_y,
                        name_col, bg_alpha=170, padding=4)

            # Origin warning badge
            if node.node_type == 'origin' and node.visited:
                warn_y = ny - draw_r - 24
                _draw_label(surf, self.font_lg, "⚠ ORIGEN", nx, warn_y,
                            C_RED, bg_alpha=200, padding=4)

            # Distance label (Dijkstra mission)
            if node.dist != float('inf') and mission == 1:
                dist_y = ny + draw_r + 10
                _draw_label(surf, self.font_xs, f"d={node.dist}", nx, dist_y,
                            C_YELLOW, bg_alpha=150, padding=3)

        # ── HUD ────────────────────────────────────────────────────────────────
        # Algo label top-left with shadow
        _draw_label(surf, self.font_lg, f"ALGORITMO: {algo_label}",
                    10 + self.font_lg.size(f"ALGORITMO: {algo_label}")[0] // 2,
                    10, (60, 120, 200), bg_alpha=130, padding=4)

        # Visited count bottom-left
        vis   = self.graph.visited_count()
        total = len(self.graph.nodes)
        pct   = int(vis / total * 100)
        vis_text = f"Nodos visitados: {vis}/{total} ({pct}%)"
        _draw_label(surf, self.font_sm, vis_text,
                    10 + self.font_sm.size(vis_text)[0] // 2,
                    GRAPH_PANEL_H - 12, (80, 140, 200), bg_alpha=140, padding=3)

        self.screen.blit(surf, (0, 0))
