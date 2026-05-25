# view/mission_intro.py
"""
NetGuardian — Pantallas cinemáticas de introducción entre misiones.
Cada misión arranca con una pantalla narrativa fullscreen antes de entrar al gameplay.
Duración: ~8 segundos o hasta que el jugador presione SPACE/ENTER.
"""

import pygame
import math
import random

from model.constants import (
    SCREEN_W, SCREEN_H,
    C_BLACK, C_DARK, C_BLUE, C_GREEN, C_RED, C_YELLOW,
    C_WHITE, C_PURPLE, C_ORANGE, C_GREY,
)


# ══════════════════════════════════════════════════════════════════════════════
#  DATOS NARRATIVOS DE CADA MISIÓN
# ══════════════════════════════════════════════════════════════════════════════

MISSION_INTRO_DATA = [
    # ─── MISIÓN 0 — Rastros del Acoso ─────────────────────────────────────
    {
        "mission_number": "MISIÓN 01",
        "title":     "RASTROS DEL ACOSO",
        "subtitle":  "Cada mensaje tiene un origen.",
        "accent":    C_RED,
        "accent2":   C_YELLOW,
        "narrative": [
            "Alguien en la red está sufriendo en silencio.",
            "Mensajes de odio comenzaron a aparecer hace 48 horas y ya se han",
            "propagado a decenas de usuarios. La víctima está paralizada.",
            "",
            "No actúan solos. El acoso viaja de nodo en nodo como una infección",
            "digital — cada usuario infectado lo reenvía al siguiente.",
            "",
            "Tu trabajo: trazar ese camino. Seguir el rastro hasta el inicio.",
            "Hasta quien encendió la mecha.",
        ],
        "algo_text": [
            "HERRAMIENTA ACTIVA:  RASTREO POR CAPAS  [1]  y  RASTREO PROFUNDO  [2]",
            "",
            "El rastreo por capas explora la red desde el centro hacia afuera,",
            "como ondas en el agua — perfecto para mapear qué tan lejos llegó el odio.",
            "El rastreo profundo sigue una cadena hasta el fondo antes de explorar",
            "otras rutas — ideal para descubrir quién inició todo.",
        ],
        "objective": "OBJETIVO:  Identifica el nodo origen del acoso antes de que más usuarios sean afectados.",
        "button":    "INICIAR INVESTIGACIÓN",
        "final_line":"El silencio también deja rastros.",
        "node_color": C_RED,
        "bg_tint":   (255, 20, 50, 8),
        "algo_keys": ["BFS", "DFS"],
    },

    # ─── MISIÓN 1 — Ruta Segura ───────────────────────────────────────────
    {
        "mission_number": "MISIÓN 02",
        "title":     "RUTA SEGURA",
        "subtitle":  "No toda conexión es segura.",
        "accent":    C_BLUE,
        "accent2":   C_GREEN,
        "narrative": [
            "La víctima está completamente aislada.",
            "Cada conexión directa ha sido contaminada por mensajes tóxicos.",
            "Mandarle apoyo por la ruta equivocada podría exponerla aún más.",
            "",
            "Hay aliados en la red — usuarios que quieren ayudar — pero están",
            "dispersos. Algunos caminos son más peligrosos que otros.",
            "",
            "Necesitas encontrar el camino más seguro. El que minimice el riesgo",
            "y lleve apoyo emocional hasta ella antes de que sea demasiado tarde.",
        ],
        "algo_text": [
            "HERRAMIENTA ACTIVA:  NAVEGACIÓN DE MENOR RIESGO  [3]",
            "",
            "Esta herramienta evalúa cada ruta posible y calcula cuál acumula",
            "menos toxicidad en el camino. Considera el peso de cada conexión —",
            "cuánto odio fluye por ella — y elige el trayecto más limpio.",
            "Como un GPS que evita zonas peligrosas.",
        ],
        "objective": "OBJETIVO:  Encuentra el camino de menor riesgo emocional hasta la víctima.",
        "button":    "TRAZAR RUTA SEGURA",
        "final_line":"El apoyo llega más lejos por el camino correcto.",
        "node_color": C_BLUE,
        "bg_tint":   (0, 100, 255, 8),
        "algo_keys": ["DIJKSTRA"],
    },

    # ─── MISIÓN 2 — Reconstruir la Red ───────────────────────────────────
    {
        "mission_number": "MISIÓN 03",
        "title":     "RECONSTRUIR LA RED",
        "subtitle":  "Confiar de nuevo cuesta. Hazlo posible.",
        "accent":    C_GREEN,
        "accent2":   C_BLUE,
        "narrative": [
            "El acoso no solo lastima personas. Destruye comunidades.",
            "Vínculos que tardaron meses en construirse se rompieron en días.",
            "Usuarios que eran amigos ahora se bloquean entre sí.",
            "",
            "La red social está fragmentada. Hay grupos aislados que no pueden",
            "comunicarse ni recibir apoyo. La desconfianza se extiende.",
            "",
            "Tu misión: reconstruir los puentes. Restaurar conexiones usando",
            "los mínimos recursos necesarios. Cada enlace que reconstruyas",
            "es una persona que vuelve a sentir que no está sola.",
        ],
        "algo_text": [
            "HERRAMIENTA ACTIVA:  RECONSTRUCCIÓN MÍNIMA  [4]",
            "",
            "Esta herramienta selecciona solo los vínculos más esenciales para",
            "mantener conectada toda la comunidad — sin malgastar recursos en",
            "conexiones redundantes. Priorizando las relaciones más valiosas,",
            "reconstruye la red con el menor costo social posible.",
        ],
        "objective": "OBJETIVO:  Restaura la red comunitaria usando la menor cantidad de conexiones posibles.",
        "button":    "RECONSTRUIR CONEXIONES",
        "final_line":"La confianza se reconstruye un vínculo a la vez.",
        "node_color": C_GREEN,
        "bg_tint":   (0, 255, 100, 6),
        "algo_keys": ["KRUSKAL"],
    },

    # ─── MISIÓN 3 — Control del Impacto ──────────────────────────────────
    {
        "mission_number": "MISIÓN 04",
        "title":     "CONTROL DEL IMPACTO",
        "subtitle":  "Corta el flujo. Detén la marea.",
        "accent":    C_PURPLE,
        "accent2":   C_RED,
        "narrative": [
            "La toxicidad está desbordada.",
            "Bots, cuentas falsas y acosadores coordinados han abierto canales",
            "de odio a través de toda la red. El volumen es insostenible.",
            "",
            "Pero no puedes cerrar todo — algunos canales son legítimos.",
            "Necesitas identificar exactamente por dónde fluye MÁS odio",
            "y cortar esos puntos estratégicos sin destruir la red entera.",
            "",
            "Una intervención quirúrgica. Precisa. Calculada.",
            "Cada segundo que pasa, más usuarios son dañados.",
        ],
        "algo_text": [
            "HERRAMIENTA ACTIVA:  ANÁLISIS DE FLUJO MÁXIMO  [5]",
            "",
            "Esta herramienta mide cuánta toxicidad puede viajar entre dos puntos",
            "de la red usando todos los canales disponibles. Al conocer el flujo",
            "máximo, identifies los cuellos de botella — los puntos donde si",
            "intervienes, cortas la mayor cantidad de odio posible de un golpe.",
        ],
        "objective": "OBJETIVO:  Calcula el flujo máximo de toxicidad y neutraliza los canales críticos.",
        "button":    "NEUTRALIZAR AMENAZA",
        "final_line":"El odio también tiene puntos débiles.",
        "node_color": C_PURPLE,
        "bg_tint":   (150, 0, 255, 8),
        "algo_keys": ["FORD-FULKERSON"],
    },

    # ─── MISIÓN 4 — Red Segura: Misión Final ─────────────────────────────
    {
        "mission_number": "MISIÓN 05  ◆  FINAL",
        "title":     "RED SEGURA",
        "subtitle":  "Todo lo que aprendiste. Úsalo ahora.",
        "accent":    C_YELLOW,
        "accent2":   C_GREEN,
        "narrative": [
            "La red está colapsando.",
            "Un ataque coordinado de gran escala ha desencadenado ciberacoso masivo,",
            "desinformación viral y el bloqueo de canales de apoyo simultáneamente.",
            "",
            "No hay tiempo para estrategias parciales. Necesitas desplegar TODO",
            "tu arsenal de investigación digital — cada herramienta que usaste",
            "en las misiones anteriores — de forma coordinada.",
            "",
            "Esta es la operación final. Si fallas, la red cae.",
            "Si tienes éxito, miles de usuarios estarán seguros.",
            "NetGuardian depende de ti.",
        ],
        "algo_text": [
            "TODAS LAS HERRAMIENTAS ACTIVAS  [1] [2] [3] [4] [5]",
            "",
            "Rastreo por capas y profundo para localizar los focos de origen.",
            "Navegación segura para llegar a las víctimas aisladas.",
            "Reconstrucción mínima para restaurar la comunidad.",
            "Análisis de flujo para cortar los canales tóxicos.",
            "Usa cada herramienta cuando la situación lo exija.",
        ],
        "objective": "OBJETIVO:  Ejecuta los 5 algoritmos y restaura el ecosistema digital por completo.",
        "button":    "INICIAR OPERACIÓN FINAL",
        "final_line":"La red no se protege sola. Tú eres NetGuardian.",
        "node_color": C_YELLOW,
        "bg_tint":   (255, 200, 0, 8),
        "algo_keys": ["BFS", "DFS", "DIJKSTRA", "KRUSKAL", "FF"],
    },
]


# ══════════════════════════════════════════════════════════════════════════════
#  PARTÍCULAS DE FONDO
# ══════════════════════════════════════════════════════════════════════════════

class IntroParticle:
    def __init__(self, accent_color):
        self.accent = accent_color
        self.reset()

    def reset(self):
        self.x    = random.uniform(0, SCREEN_W)
        self.y    = random.uniform(0, SCREEN_H)
        self.vx   = random.uniform(-0.6, 0.6)
        self.vy   = random.uniform(-1.2, -0.2)
        self.size = random.randint(1, 3)
        self.life = random.randint(80, 240)
        self.max_life = self.life
        self.col  = random.choice([self.accent, C_WHITE, (60, 90, 140)])

    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.life -= 1
        if self.life <= 0 or self.y < -10:
            self.reset()


class IntroNode:
    """Nodo flotante decorativo en el fondo de la pantalla intro."""
    def __init__(self, accent_color):
        self.x     = random.uniform(0, SCREEN_W)
        self.y     = random.uniform(80, SCREEN_H - 80)
        self.vx    = random.uniform(-0.5, 0.5)
        self.vy    = random.uniform(-0.5, 0.5)
        self.r     = random.randint(3, 10)
        self.col   = random.choice([accent_color, (40, 60, 100), (20, 40, 80)])
        self.phase = random.uniform(0, math.pi * 2)

    def update(self):
        self.x = (self.x + self.vx) % SCREEN_W
        self.y = (self.y + self.vy) % SCREEN_H


# ══════════════════════════════════════════════════════════════════════════════
#  CLASE PRINCIPAL: MissionIntroScreen
# ══════════════════════════════════════════════════════════════════════════════

class MissionIntroScreen:
    """
    Pantalla cinemática fullscreen de introducción a una misión.
    Se muestra ANTES de entrar al gameplay de la misión.

    Uso:
        intro = MissionIntroScreen(screen, mission_id=0)
        # en el game loop:
        result = intro.handle_event(event)   # devuelve "continue" o None
        intro.update()
        intro.draw()
    """

    DURATION = 600       # ~10 segundos a 60fps (auto-skip)
    FADE_IN  = 40        # frames de fade-in
    SKIP_AFTER = 120     # el jugador puede saltar después de 2 segundos

    def __init__(self, screen: pygame.Surface, mission_id: int):
        self.screen     = screen
        self.mission_id = max(0, min(mission_id, len(MISSION_INTRO_DATA) - 1))
        self.data       = MISSION_INTRO_DATA[self.mission_id]
        self.t          = 0
        self.done       = False

        # Particles & bg nodes
        accent = self.data["accent"]
        self.particles  = [IntroParticle(accent) for _ in range(60)]
        self.bg_nodes   = [IntroNode(accent) for _ in range(22)]

        # Connections between nearby nodes
        self._node_pairs = []

        # Fonts
        self.f_mission = pygame.font.SysFont("consolas", 13, bold=True)
        self.f_title   = pygame.font.SysFont("consolas", 52, bold=True)
        self.f_sub     = pygame.font.SysFont("consolas", 17, bold=True)
        self.f_body    = pygame.font.SysFont("consolas", 14)
        self.f_algo    = pygame.font.SysFont("consolas", 13, bold=True)
        self.f_obj     = pygame.font.SysFont("consolas", 14, bold=True)
        self.f_btn     = pygame.font.SysFont("consolas", 16, bold=True)
        self.f_final   = pygame.font.SysFont("consolas", 18, bold=True)
        self.f_tiny    = pygame.font.SysFont("consolas", 10)

        # Scanline surface (cached)
        self._scanlines = pygame.Surface((SCREEN_W, SCREEN_H), pygame.SRCALPHA)
        for y in range(0, SCREEN_H, 3):
            pygame.draw.line(self._scanlines, (0, 0, 0, 22), (0, y), (SCREEN_W, y))

        # Glitch state
        self._glitch_t = 0

    # ── PUBLIC API ────────────────────────────────────────────────────────

    def handle_event(self, event: pygame.event.Event):
        """Returns 'continue' when the player wants to proceed."""
        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_RETURN, pygame.K_SPACE, pygame.K_e):
                if self.t >= self.SKIP_AFTER:
                    self.done = True
                    return "continue"
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.t >= self.SKIP_AFTER:
                # Check button rect
                btn_rect = self._get_btn_rect()
                if btn_rect.collidepoint(event.pos):
                    self.done = True
                    return "continue"
        return None

    def update(self):
        self.t += 1
        for p in self.particles:
            p.update()
        for n in self.bg_nodes:
            n.update()
        if self.t >= self.DURATION:
            self.done = True

    def draw(self):
        s = self.screen
        d = self.data
        t = self.t

        # ── 1. BACKGROUND GRADIENT ────────────────────────────────────────
        self._draw_bg(s, d)

        # ── 2. BG NODES & CONNECTIONS ────────────────────────────────────
        self._draw_bg_network(s, d)

        # ── 3. PARTICLES ─────────────────────────────────────────────────
        self._draw_particles(s)

        # ── 4. SCANLINES ─────────────────────────────────────────────────
        s.blit(self._scanlines, (0, 0))

        # ── 5. GLITCH burst at start ──────────────────────────────────────
        if t < 30:
            self._draw_glitch(s, t)

        # ── 6. FADE IN ────────────────────────────────────────────────────
        if t < self.FADE_IN:
            alpha = int(255 * (1 - t / self.FADE_IN))
            ov = pygame.Surface((SCREEN_W, SCREEN_H), pygame.SRCALPHA)
            ov.fill((0, 0, 0, alpha))
            s.blit(ov, (0, 0))
            return  # don't draw UI until fade done

        # ── 7. MISSION NUMBER TAG ─────────────────────────────────────────
        self._draw_reveal(s, self.f_mission, d["mission_number"],
                          color=(100, 130, 180), x=60, y=60,
                          reveal_at=self.FADE_IN, speed=2)

        # Horizontal rule
        if t >= self.FADE_IN + 8:
            line_alpha = min(255, (t - self.FADE_IN - 8) * 12)
            ls = pygame.Surface((SCREEN_W - 120, 1), pygame.SRCALPHA)
            ls.fill((*d["accent"], line_alpha))
            s.blit(ls, (60, 84))

        # ── 8. TITLE ──────────────────────────────────────────────────────
        self._draw_title_glow(s, d, t)
        self._draw_reveal(s, self.f_title, d["title"],
                          color=d["accent"], x=SCREEN_W // 2, y=95,
                          reveal_at=self.FADE_IN + 10, speed=3,
                          center=True)

        # ── 9. SUBTITLE ───────────────────────────────────────────────────
        self._draw_reveal(s, self.f_sub, d["subtitle"],
                          color=d["accent2"], x=SCREEN_W // 2, y=165,
                          reveal_at=self.FADE_IN + 22, speed=3,
                          center=True)

        # ── 10. SEPARATOR ─────────────────────────────────────────────────
        sep_y = 198
        if t >= self.FADE_IN + 35:
            sep_alpha = min(255, (t - self.FADE_IN - 35) * 10)
            ds = pygame.Surface((SCREEN_W - 200, 2), pygame.SRCALPHA)
            ds.fill((40, 60, 100, sep_alpha))
            s.blit(ds, (100, sep_y))

        # ── 11. NARRATIVE TEXT ────────────────────────────────────────────
        narrative_y = 220
        reveal_start = self.FADE_IN + 45
        for i, line in enumerate(d["narrative"]):
            self._draw_reveal_line(s, self.f_body, line,
                                   color=(170, 200, 240) if line else C_BLACK,
                                   x=90, y=narrative_y + i * 20,
                                   reveal_at=reveal_start + i * 6, speed=4)

        # ── 12. ALGO PANEL ────────────────────────────────────────────────
        algo_panel_y = narrative_y + len(d["narrative"]) * 20 + 18
        self._draw_algo_panel(s, d, t, algo_panel_y)

        # ── 13. OBJECTIVE ─────────────────────────────────────────────────
        obj_y = algo_panel_y + len(d["algo_text"]) * 18 + 55
        self._draw_objective(s, d, t, obj_y)

        # ── 14. CTA BUTTON ───────────────────────────────────────────────
        btn_y = obj_y + 54
        self._draw_button(s, d, t, btn_y)

        # ── 15. FINAL LINE ────────────────────────────────────────────────
        self._draw_final_line(s, d, t, btn_y + 60)

        # ── 16. PROGRESS BAR ─────────────────────────────────────────────
        bar_w = int(SCREEN_W * min(1.0, t / self.DURATION))
        pygame.draw.rect(s, (20, 30, 50), (0, SCREEN_H - 4, SCREEN_W, 4))
        pygame.draw.rect(s, d["accent"], (0, SCREEN_H - 4, bar_w, 4))

        # Skip hint
        if t >= self.SKIP_AFTER:
            hint_alpha = min(200, (t - self.SKIP_AFTER) * 6)
            hint = self.f_tiny.render("SPACE / ENTER  para continuar", True,
                                      (*d["accent"], hint_alpha))
            hs = pygame.Surface((hint.get_width(), hint.get_height()), pygame.SRCALPHA)
            hs.blit(hint, (0, 0))
            hs.set_alpha(hint_alpha)
            s.blit(hs, (SCREEN_W - hs.get_width() - 12, SCREEN_H - 16))

    # ── PRIVATE DRAW HELPERS ──────────────────────────────────────────────

    def _draw_bg(self, s, d):
        """Dark gradient with subtle tint based on mission accent."""
        r0, g0, b0 = 4, 6, 12
        tint = d["bg_tint"]
        ar, ag, ab = tint[0], tint[1], tint[2]
        for y in range(SCREEN_H):
            ratio = y / SCREEN_H
            r = int(r0 + ar * ratio * 0.3)
            g = int(g0 + ag * ratio * 0.3)
            b = int(b0 + ab * ratio * 0.4 + 20 * ratio)
            pygame.draw.line(s, (r, g, b), (0, y), (SCREEN_W, y))

        # Grid lines
        grid_surf = pygame.Surface((SCREEN_W, SCREEN_H), pygame.SRCALPHA)
        for x in range(0, SCREEN_W, 60):
            pygame.draw.line(grid_surf, (255, 255, 255, 5), (x, 0), (x, SCREEN_H))
        for y in range(0, SCREEN_H, 60):
            pygame.draw.line(grid_surf, (255, 255, 255, 5), (0, y), (SCREEN_W, y))
        s.blit(grid_surf, (0, 0))

    def _draw_bg_network(self, s, d):
        """Floating network nodes and connections in the background."""
        ns = self.bg_nodes
        line_surf = pygame.Surface((SCREEN_W, SCREEN_H), pygame.SRCALPHA)
        for i, n in enumerate(ns):
            for j, m in enumerate(ns):
                if j <= i:
                    continue
                dist = math.hypot(n.x - m.x, n.y - m.y)
                if dist < 200:
                    alpha = int(55 * (1 - dist / 200))
                    pygame.draw.line(line_surf, (*d["accent"], alpha),
                                     (int(n.x), int(n.y)), (int(m.x), int(m.y)), 1)
        s.blit(line_surf, (0, 0))

        pulse_t = self.t * 0.04
        for n in ns:
            pulse = 0.5 + 0.5 * math.sin(pulse_t + n.phase)
            r = int(n.r + pulse * 4)
            col_alpha = pygame.Surface((r * 2 + 2, r * 2 + 2), pygame.SRCALPHA)
            pygame.draw.circle(col_alpha, (*n.col, 80), (r + 1, r + 1), r)
            s.blit(col_alpha, (int(n.x) - r, int(n.y) - r))
            pygame.draw.circle(s, n.col, (int(n.x), int(n.y)), max(2, r - 2), 1)

    def _draw_particles(self, s):
        for p in self.particles:
            alpha = int(200 * p.life / p.max_life)
            ps = pygame.Surface((p.size * 2 + 2, p.size * 2 + 2), pygame.SRCALPHA)
            pygame.draw.circle(ps, (*p.col, alpha), (p.size + 1, p.size + 1), p.size)
            s.blit(ps, (int(p.x) - p.size, int(p.y) - p.size))

    def _draw_glitch(self, s, t):
        """Brief glitch effect at screen open."""
        num = max(0, 8 - t)
        for _ in range(num):
            y  = random.randint(0, SCREEN_H)
            h  = random.randint(2, 18)
            shift = random.randint(-20, 20)
            try:
                W = SCREEN_W
                h = min(h, SCREEN_H - y)
                if h > 0:
                    sub = s.subsurface(pygame.Rect(0, y, W, h))
                    s.blit(sub, (shift, y))
            except Exception:
                pass
        if t < 8:
            fl = pygame.Surface((SCREEN_W, SCREEN_H), pygame.SRCALPHA)
            fl.fill((self.data["accent"][0], 0, 0, 45))
            s.blit(fl, (0, 0))

    def _draw_title_glow(self, s, d, t):
        """Glow halo behind the mission title."""
        if t < self.FADE_IN + 10:
            return
        alpha = min(60, (t - self.FADE_IN - 10) * 3)
        gw, gh = 900, 90
        gsurf = pygame.Surface((gw, gh), pygame.SRCALPHA)
        for gr in range(40, 0, -2):
            ga = int(alpha * (1 - gr / 40))
            pygame.draw.rect(gsurf, (*d["accent"], ga),
                             (gw // 2 - gr * 10, gh // 2 - gr, gr * 20, gr * 2))
        s.blit(gsurf, (SCREEN_W // 2 - gw // 2, 98))

    def _draw_reveal(self, s, font, text, color, x, y,
                     reveal_at, speed, center=False):
        """Fade-in a single line of text."""
        t = self.t
        if t < reveal_at:
            return
        alpha = min(255, (t - reveal_at) * speed * 12)
        surf = font.render(text, True, color)
        tmp  = pygame.Surface(surf.get_size(), pygame.SRCALPHA)
        tmp.blit(surf, (0, 0))
        tmp.set_alpha(alpha)
        if center:
            s.blit(tmp, (x - surf.get_width() // 2, y))
        else:
            s.blit(tmp, (x, y))

    def _draw_reveal_line(self, s, font, text, color, x, y,
                          reveal_at, speed):
        """Reveal a body text line."""
        t = self.t
        if t < reveal_at or not text:
            return
        alpha = min(255, (t - reveal_at) * speed * 8)
        surf = font.render(text, True, color)
        tmp  = pygame.Surface(surf.get_size(), pygame.SRCALPHA)
        tmp.blit(surf, (0, 0))
        tmp.set_alpha(alpha)
        s.blit(tmp, (x, y))

    def _draw_algo_panel(self, s, d, t, panel_y):
        """Holographic panel displaying the algorithm explanation."""
        reveal_at = self.FADE_IN + 90

        if t < reveal_at - 10:
            return

        panel_alpha = min(180, (t - (reveal_at - 10)) * 10)
        # Panel background
        panel_w = SCREEN_W - 140
        panel_h = len(d["algo_text"]) * 18 + 24
        panel_surf = pygame.Surface((panel_w, panel_h), pygame.SRCALPHA)
        panel_surf.fill((*d["accent"], 12))
        pygame.draw.rect(panel_surf, (*d["accent"], 90),
                         pygame.Rect(0, 0, panel_w, panel_h), 1)
        # Left accent bar
        pygame.draw.rect(panel_surf, (*d["accent"], 200),
                         pygame.Rect(0, 0, 3, panel_h))
        panel_surf.set_alpha(panel_alpha)
        s.blit(panel_surf, (70, panel_y))

        # Lines
        for i, line in enumerate(d["algo_text"]):
            line_reveal = reveal_at + i * 8
            if not line:
                continue
            color = d["accent"] if i == 0 else (140, 170, 210)
            if i == 0:
                font = self.f_algo
            else:
                font = self.f_body
            self._draw_reveal_line(s, font, line, color,
                                   x=85, y=panel_y + 12 + i * 18,
                                   reveal_at=line_reveal, speed=3)

    def _draw_objective(self, s, d, t, obj_y):
        """HUD-style objective box."""
        reveal_at = self.FADE_IN + 130
        if t < reveal_at - 10:
            return
        alpha = min(255, (t - (reveal_at - 10)) * 8)

        box_w = SCREEN_W - 140
        box_surf = pygame.Surface((box_w, 36), pygame.SRCALPHA)
        box_surf.fill((255, 200, 0, 15))
        pygame.draw.rect(box_surf, (255, 200, 0, 100),
                         pygame.Rect(0, 0, box_w, 36), 1)
        box_surf.set_alpha(alpha)
        s.blit(box_surf, (70, obj_y))

        self._draw_reveal(s, self.f_obj, d["objective"],
                          color=C_YELLOW, x=86, y=obj_y + 10,
                          reveal_at=reveal_at, speed=3)

    def _draw_button(self, s, d, t, btn_y):
        """Animated CTA button."""
        reveal_at = self.SKIP_AFTER
        if t < reveal_at:
            return
        alpha = min(255, (t - reveal_at) * 8)

        pulse = 0.6 + 0.4 * math.sin(self.t * 0.08)
        btn_rect = self._get_btn_rect(btn_y)

        btn_surf = pygame.Surface((btn_rect.width, btn_rect.height), pygame.SRCALPHA)
        btn_surf.fill((*d["accent"], int(40 * pulse)))
        pygame.draw.rect(btn_surf, (*d["accent"], int(200 * pulse)),
                         pygame.Rect(0, 0, btn_rect.width, btn_rect.height), 2)
        btn_surf.set_alpha(alpha)
        s.blit(btn_surf, (btn_rect.x, btn_rect.y))

        label = self.f_btn.render(f"►  {d['button']}", True, d["accent"])
        la = pygame.Surface(label.get_size(), pygame.SRCALPHA)
        la.blit(label, (0, 0))
        la.set_alpha(alpha)
        s.blit(la, (btn_rect.centerx - label.get_width() // 2,
                    btn_rect.centery - label.get_height() // 2))

    def _draw_final_line(self, s, d, t, y):
        """The cinematic final line shown last."""
        reveal_at = self.SKIP_AFTER + 20
        if t < reveal_at:
            return
        alpha = min(255, (t - reveal_at) * 5)
        pulse = 0.7 + 0.3 * math.sin(self.t * 0.05)
        col_r, col_g, col_b = d["accent2"]
        col = (int(col_r * pulse), int(col_g * pulse), int(col_b * pulse))
        surf = self.f_final.render(f'"{d["final_line"]}"', True, col)
        tmp = pygame.Surface(surf.get_size(), pygame.SRCALPHA)
        tmp.blit(surf, (0, 0))
        tmp.set_alpha(alpha)
        s.blit(tmp, (SCREEN_W // 2 - surf.get_width() // 2, y))

    def _get_btn_rect(self, btn_y=None):
        """Returns the CTA button Rect. btn_y is auto-calculated if None."""
        if btn_y is None:
            # Estimate position based on content
            d = self.data
            narrative_y = 220
            algo_panel_y = narrative_y + len(d["narrative"]) * 20 + 18
            obj_y = algo_panel_y + len(d["algo_text"]) * 18 + 55
            btn_y = obj_y + 54
        bw, bh = 340, 44
        bx = SCREEN_W // 2 - bw // 2
        return pygame.Rect(bx, btn_y, bw, bh)
