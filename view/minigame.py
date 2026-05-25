# view/minigame.py
"""
MinijuegoScreen — Integra el Lab1 (evidencias + pregunta) como minijuego
dentro de Lab2. Adaptado a resolución 1280×720 y al estilo visual de NetGuardian.
"""
import pygame
import random
import math


# ──────────────────────────────────────────────────────────
#  PALETA LOCAL (compatible con Lab2)
# ──────────────────────────────────────────────────────────
_C = {
    "fondo":       (6,  10, 18),
    "panel":       (12, 18, 30),
    "borde":       (40, 60, 100),
    "acento":      (0,  180, 255),
    "acento2":     (255, 228, 74),
    "verde":       (0,  220, 120),
    "rojo":        (255, 50,  80),
    "lila":        (180, 80, 255),
    "texto":       (210, 230, 255),
    "texto_dim":   (100, 130, 170),
    "ev_bg":       (16, 28, 52),
    "ev_hover":    (28, 50, 90),
    "boton_n":     (24, 44, 80),
    "boton_h":     (44, 80, 140),
    "boton_ok":    (30, 130, 70),
    "boton_bad":   (140, 30, 50),
}


def _font(size, bold=False):
    return pygame.font.SysFont("consolas", size, bold=bold)


def _draw_text_centered(surf, text, font, color, cx, cy):
    s = font.render(text, True, color)
    surf.blit(s, (cx - s.get_width() // 2, cy - s.get_height() // 2))


def _draw_text_left(surf, text, font, color, x, y):
    s = font.render(text, True, color)
    surf.blit(s, (x, y))


def _wrap(text, font, max_w):
    words = text.split(" ")
    lines, cur = [], ""
    for w in words:
        test = cur + (" " if cur else "") + w
        if font.size(test)[0] <= max_w:
            cur = test
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def _draw_multiline(surf, text, font, color, x, y, max_w, spacing=4):
    lines = []
    for par in text.split("\n"):
        lines.extend(_wrap(par, font, max_w))
    h = font.get_height() + spacing
    for i, l in enumerate(lines):
        _draw_text_left(surf, l, font, color, x, y + i * h)
    return len(lines) * h


# ──────────────────────────────────────────────────────────
#  TARJETA DE EVIDENCIA (auto-contenida, sin sprites)
# ──────────────────────────────────────────────────────────
CARD_W, CARD_H = 210, 130

_ICONOS = {
    "captura":      "📱", "chat":        "💬", "perfil":      "👤",
    "post":         "📢", "perfil_falso":"🎭", "metadata":    "🌐",
    "logs":         "📋", "testimonio":  "🗣", "analisis":    "🔍",
    "historial":    "📄", "ip":          "🌐", "denuncia":    "⚖️",
    "cuenta_borrada":"🗑️", "horario":    "🕐", "dispositivo": "💻",
    "testigo":      "👁️",
}


class _EvidCard:
    def __init__(self, ev_data, x, y):
        self.ev         = ev_data
        self.rect       = pygame.Rect(x, y, CARD_W, CARD_H)
        self.collected  = False
        self.hover      = False
        self._tick      = 0
        self._font_sm   = _font(12)
        self._font_ico  = None
        self._mockup    = None   # generado lazy al primer hover

    def _get_icon_font(self):
        if self._font_ico is None:
            for name in ["Segoe UI Emoji", "Apple Color Emoji", "Noto Color Emoji",
                         "Symbola", "DejaVu Sans"]:
                try:
                    f = pygame.font.SysFont(name, 24)
                    self._font_ico = f
                    break
                except Exception:
                    pass
            if self._font_ico is None:
                self._font_ico = _font(14)
        return self._font_ico

    def _get_mockup(self, nivel_data):
        """Genera/cachea el mockup visual para el tooltip."""
        if self._mockup is not None:
            return self._mockup
        try:
            from view.evidencias_img import generar_imagen_evidencia
            sprite_key = self.ev.get("sprite", "")
            self._mockup = generar_imagen_evidencia(sprite_key, nivel_data)
        except Exception as e:
            # Fallback: superficie vacía
            s = pygame.Surface((320, 380), pygame.SRCALPHA)
            pygame.draw.rect(s, (12, 16, 26), (0, 0, 320, 380), border_radius=10)
            self._mockup = s
        return self._mockup

    def update(self, mouse_pos, nivel_data=None):
        self.hover = self.rect.collidepoint(mouse_pos) and not self.collected
        if self.hover:
            self._tick += 1
            if nivel_data:
                self._get_mockup(nivel_data)   # pre-calentar
        else:
            self._tick = 0

    def was_clicked(self, event):
        return (event.type == pygame.MOUSEBUTTONDOWN and
                event.button == 1 and
                self.rect.collidepoint(event.pos) and
                not self.collected)

    def draw(self, surf):
        # Colors
        if self.collected:
            bg, brd = (20, 60, 35), _C["verde"]
        elif self.hover:
            bg, brd = _C["ev_hover"], _C["acento"]
        else:
            bg, brd = _C["ev_bg"], _C["borde"]

        # Shadow
        if not self.collected:
            sh = pygame.Surface((CARD_W + 6, CARD_H + 6), pygame.SRCALPHA)
            sh.fill((0, 0, 0, 55))
            surf.blit(sh, (self.rect.x + 4, self.rect.y + 4))

        # Glow on hover
        if self.hover:
            pulse = abs((self._tick % 24) - 12) / 12.0
            gs = int(3 + 4 * pulse)
            gr = pygame.Rect(self.rect.x - gs, self.rect.y - gs,
                             CARD_W + gs * 2, CARD_H + gs * 2)
            pygame.draw.rect(surf, _C["acento"], gr, 2, border_radius=10)

        # Background
        pygame.draw.rect(surf, bg, self.rect, border_radius=8)
        pygame.draw.rect(surf, brd, self.rect, 2, border_radius=8)

        # Accent top bar
        if not self.collected:
            pygame.draw.rect(surf, brd,
                             pygame.Rect(self.rect.x, self.rect.y, CARD_W, 4),
                             border_radius=8)

        # Icon
        ico_txt = _ICONOS.get(self.ev.get("id", ""), "📁")
        try:
            f_ico = self._get_icon_font()
            ico_s = f_ico.render(ico_txt, True, (200, 220, 255))
            surf.blit(ico_s, (self.rect.x + 8, self.rect.y + 8))
        except Exception:
            pass

        # Name
        nm_col = _C["verde"] if self.collected else (_C["acento"] if self.hover else _C["texto"])
        nm_s = self._font_sm.render(self.ev["nombre"][:24], True, nm_col)
        surf.blit(nm_s, (self.rect.x + 8, self.rect.y + 76))

        # Status
        if self.collected:
            st = self._font_sm.render("✔ RECOLECTADA", True, _C["verde"])
        elif self.hover:
            p2 = abs((self._tick % 30) - 15) / 15.0
            br = int(200 + 55 * p2)
            st = self._font_sm.render("► CLIC PARA RECOGER", True, (br, br, 50))
        else:
            desc = self.ev.get("descripcion", "")[:28]
            st = self._font_sm.render(desc, True, _C["texto_dim"])
        surf.blit(st, (self.rect.x + 8, self.rect.y + 96))

    def draw_tooltip(self, surf, nivel_data, screen_w=1280, screen_h=720):
        """Dibuja el mockup visual de la evidencia al hacer hover."""
        if not self.hover or self.collected or self._tick < 8:
            return
        mock = self._get_mockup(nivel_data)
        if mock is None:
            return
        mw, mh = mock.get_size()
        # Escalar si es muy grande
        max_h = 380
        if mh > max_h:
            ratio = max_h / mh
            mw, mh = int(mw * ratio), max_h
            mock = pygame.transform.smoothscale(mock, (mw, mh))
        # Posición: preferir arriba de la tarjeta, ajustar si se sale
        tx = self.rect.centerx - mw // 2
        ty = self.rect.top - mh - 12
        tx = max(8, min(screen_w - mw - 8, tx))
        ty = max(8, min(screen_h - mh - 8, ty))
        # Fondo panel con borde
        panel = pygame.Surface((mw + 8, mh + 8), pygame.SRCALPHA)
        panel.fill((6, 10, 20, 230))
        surf.blit(panel, (tx - 4, ty - 4))
        pygame.draw.rect(surf, _C["acento"], (tx - 4, ty - 4, mw + 8, mh + 8), 2,
                         border_radius=10)
        # Nombre encima
        fn = _font(11, bold=True)
        ns = fn.render(self.ev["nombre"], True, _C["acento"])
        surf.blit(ns, (tx + mw // 2 - ns.get_width() // 2, ty - 18))
        surf.blit(mock, (tx, ty))


# ──────────────────────────────────────────────────────────
#  PANTALLA DE EVIDENCIAS (Lab1 en Lab2)
# ──────────────────────────────────────────────────────────

class EvidenciasScreen:
    W, H = 1280, 720

    def __init__(self, nivel_data):
        self.data     = nivel_data
        self.cards    = []
        self.collected = set()
        self.msg       = ""
        self.msg_tick  = 0
        self.tick      = 0
        self.acento    = nivel_data.get("color_acento", _C["acento"])

        self._font_title = _font(26, bold=True)
        self._font_sub   = _font(18, bold=True)
        self._font_md    = _font(15)
        self._font_sm    = _font(13)

        # Build cards — layout in two rows
        evs = nivel_data["evidencias_disponibles"]
        n = len(evs)
        # Center them in the play area (y: 120..580)
        cols = min(n, 4)
        rows = (n + cols - 1) // cols
        total_w = cols * (CARD_W + 20) - 20
        start_x = (self.W - total_w) // 2
        start_y = 160 if rows == 1 else 140
        for i, ev in enumerate(evs):
            col = i % cols
            row = i // cols
            x = start_x + col * (CARD_W + 20)
            y = start_y + row * (CARD_H + 20)
            # Use the evidencia's built-in position shifted to 1280-space
            ex, ey = ev.get("posicion", (x, y))
            # scale from 1100→1280 and 700→720
            ex_scaled = int(ex * 1280 / 1100)
            ey_scaled = int(ey * 720  / 700) + 80
            self.cards.append(_EvidCard(ev, ex_scaled, ey_scaled))

        # Continue button
        btn_y = self.H - 80
        self._btn_rect = pygame.Rect(self.W - 240, btn_y, 220, 50)
        self._btn_hover = False

        # Particles
        self._parts = [
            {"x": random.uniform(0, self.W), "y": random.uniform(0, self.H),
             "vx": random.uniform(-0.4, 0.4), "vy": random.uniform(-0.6, -1.2),
             "r": random.randint(1, 3), "alpha": random.randint(40, 130)}
            for _ in range(25)
        ]

    def _all_required(self):
        return self.data["evidencias_requeridas"].issubset(self.collected)

    def update(self, events, mouse_pos):
        self.tick     += 1
        self.msg_tick += 1
        self._btn_hover = self._btn_rect.collidepoint(mouse_pos)
        # Particles
        for p in self._parts:
            p["x"] += p["vx"]; p["y"] += p["vy"]
            if p["y"] < -5:
                p["y"] = self.H + 5
                p["x"] = random.uniform(0, self.W)
        # Cards
        for card in self.cards:
            card.update(mouse_pos, self.data)
        # Events
        for ev in events:
            for card in self.cards:
                if card.was_clicked(ev):
                    card.collected = True
                    self.collected.add(card.ev["id"])
                    self.msg = f"✔  {card.ev['nombre']} recolectada"
                    self.msg_tick = 0
            if (ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 1
                    and self._btn_rect.collidepoint(ev.pos)):
                if self._all_required():
                    return "pregunta"
                else:
                    self.msg = "⚠  Faltan evidencias clave"
                    self.msg_tick = 0
        return None

    def draw(self, surf):
        surf.fill(_C["fondo"])
        ac = self.acento

        # Scanlines
        sc = pygame.Surface((self.W, self.H), pygame.SRCALPHA)
        for sy in range(0, self.H, 4):
            pygame.draw.line(sc, (0, 0, 0, 30), (0, sy), (self.W, sy))
        surf.blit(sc, (0, 0))

        # Particles
        for p in self._parts:
            ps = pygame.Surface((p["r"] * 2, p["r"] * 2), pygame.SRCALPHA)
            pygame.draw.circle(ps, (*ac, p["alpha"]), (p["r"], p["r"]), p["r"])
            surf.blit(ps, (int(p["x"]) - p["r"], int(p["y"]) - p["r"]))

        # HUD header
        hud = pygame.Surface((self.W, 110), pygame.SRCALPHA)
        hud.fill((6, 10, 20, 220))
        surf.blit(hud, (0, 0))
        pygame.draw.line(surf, ac, (0, 110), (self.W, 110), 2)
        pygame.draw.rect(surf, ac, (0, 0, 4, 110))
        pygame.draw.rect(surf, ac, (self.W - 4, 0, 4, 110))

        # Glitch effect on title
        glitch = (self.tick % 90) < 3
        tc = _C["rojo"] if glitch else ac
        ox = 2 if glitch else 0
        _draw_text_centered(surf, "⚡  RECOLECTA LAS EVIDENCIAS  ⚡",
                            self._font_title, tc, self.W // 2 + ox, 30)

        # Objetivo genérico (sin revelar tipo de delito)
        objetivo = self.data.get("objetivo", "Recoge todas las evidencias para analizar el caso.")
        _draw_text_centered(surf, objetivo,
                            self._font_sm, _C["texto_dim"], self.W // 2, 60)

        # Progress bar
        req = self.data["evidencias_requeridas"]
        got = len(self.collected & req)
        tot = len(req)
        prog_col = _C["verde"] if got == tot else _C["acento2"]
        _draw_text_centered(surf, f"▣ EVIDENCIAS  {got} / {tot}",
                            self._font_md, prog_col, self.W // 2, 88)
        bw, bx, by = 400, self.W // 2 - 200, 100
        pygame.draw.rect(surf, (16, 26, 46), (bx, by, bw, 8), border_radius=4)
        if tot > 0 and got > 0:
            fw = int(bw * got / tot)
            pygame.draw.rect(surf, prog_col, (bx, by, fw, 8), border_radius=4)
        pygame.draw.rect(surf, _C["borde"], (bx, by, bw, 8), 1, border_radius=4)

        # Historia (brief)
        historia = self.data.get("historia", "")
        if historia:
            hist_bg = pygame.Surface((self.W - 40, 72), pygame.SRCALPHA)
            hist_bg.fill((10, 16, 32, 180))
            surf.blit(hist_bg, (20, 116))
            pygame.draw.rect(surf, ac, (20, 116, self.W - 40, 72), 1, border_radius=6)
            _draw_multiline(surf, historia, self._font_sm, _C["texto_dim"],
                            32, 122, self.W - 64, spacing=3)

        # Cards
        for card in self.cards:
            card.draw(surf)

        # Tooltips mockup (encima de todo para no quedar tapados)
        for card in self.cards:
            card.draw_tooltip(surf, self.data, self.W, self.H)

        # Floating message
        if self.msg_tick < 130:
            alpha = min(255, (130 - self.msg_tick) * 4)
            is_err = "⚠" in self.msg
            mc = _C["rojo"] if is_err else _C["verde"]
            ms = self._font_md.render(self.msg, True, mc)
            mx, my = 20, self.H - 130
            mbg = pygame.Surface((ms.get_width() + 24, ms.get_height() + 14), pygame.SRCALPHA)
            mbg.fill((40 if is_err else 10, 10, 40 if not is_err else 10, 200))
            mbg.set_alpha(alpha)
            surf.blit(mbg, (mx - 12, my - 6))
            pygame.draw.rect(surf, mc, (mx - 12, my - 6,
                                        ms.get_width() + 24, ms.get_height() + 14), 2, border_radius=4)
            ms.set_alpha(alpha)
            surf.blit(ms, (mx, my))

        # Continue button
        btn_c = ac if self._all_required() else _C["borde"]
        btn_bg = _C["boton_h"] if (self._btn_hover and self._all_required()) else _C["boton_n"]
        pygame.draw.rect(surf, btn_bg, self._btn_rect, border_radius=8)
        pygame.draw.rect(surf, btn_c, self._btn_rect, 2, border_radius=8)
        lbl = "► ANALIZAR" if self._all_required() else f"({len(self.collected & req)}/{len(req)}) Recolecta más"
        lbl_s = self._font_md.render(lbl, True, btn_c)
        surf.blit(lbl_s, (self._btn_rect.centerx - lbl_s.get_width() // 2,
                          self._btn_rect.centery - lbl_s.get_height() // 2))


# ──────────────────────────────────────────────────────────
#  PANTALLA DE PREGUNTA (Lab1 en Lab2)
# ──────────────────────────────────────────────────────────

class PreguntaScreen:
    W, H = 1280, 720

    # Breve explicación de cada ley/opción tipo que puede aparecer
    _LEY_INFO = {
        "Art. 220": "Injuria: ofender el honor o dignidad de una persona mediante palabras, actos o signos. Pena: multa 1-3 SMLV.",
        "Art. 221": "Calumnia: imputar falsamente a alguien una conducta tipificada como delito. Pena: multa 2-5 SMLV.",
        "Ley 1273": "Ley de delitos informáticos (Colombia 2009). Cubre acceso abusivo, daño informático y suplantación. Penas: 4-8 años.",
        "Ley 1098": "Código de Infancia y Adolescencia. Protege a menores. Se aplica cuando víctima o agresor es menor de 18 años.",
        "Hostigamiento": "Acoso reiterado y sistemático. Puede sumarse a otros delitos. Genera medidas de protección + proceso penal.",
        "Injuria": "Ofensa verbal o escrita al honor de alguien. No requiere que sea falsa, basta con que sea humillante.",
        "Calumnia": "Acusación falsa de un delito. Debe ser específica y falsa para distinguirse de la injuria.",
        "Acceso abusivo": "Ingresar sin autorización a sistemas informáticos. Ley 1273 Art. 269A. Pena: 4-8 años.",
        "Amenaza": "Intimidación para causar temor. Puede constituir constreñimiento ilegal (Art. 182 C.P.).",
        "Daño informático": "Destruir, dañar o alterar datos o sistemas informáticos. Ley 1273 Art. 269D. Pena: 48-96 meses.",
        "Suplantación": "Hacerse pasar por otra persona en medios digitales. Ley 1273 Art. 269F.",
    }

    def _get_ley_info(self, opcion_texto):
        """Devuelve la descripción breve de la ley mencionada en la opción."""
        for key, desc in self._LEY_INFO.items():
            if key.lower() in opcion_texto.lower():
                return desc
        return "Consulta el Código Penal Colombiano o la Ley 1273 de 2009 para más detalles."

    def __init__(self, nivel_data):
        self.data      = nivel_data
        self.pregunta  = nivel_data["pregunta"]
        self.acento    = nivel_data.get("color_acento", _C["acento"])
        self.selection = None
        self.result    = None
        self.tick      = 0
        self.btn_done  = None

        self._font_title = _font(24, bold=True)
        self._font_sub   = _font(18, bold=True)
        self._font_md    = _font(16)
        self._font_sm    = _font(13)
        self._font_xs    = _font(11)

        cx = self.W // 2
        self._opt_rects  = []
        self._opt_states = []   # None / 'correct' / 'wrong'
        opts = self.pregunta["opciones"]
        for i, op in enumerate(opts):
            y = 280 + i * 74
            r = pygame.Rect(cx - 330, y, 660, 56)
            self._opt_rects.append(r)
            self._opt_states.append(None)

        self._hover_opt  = -1
        self._hover_tick = 0   # para mostrar tooltip con delay
        self._done_rect  = None
        self._done_hover = False

    def update(self, events, mouse_pos):
        self.tick += 1
        self._hover_opt = -1
        for i, r in enumerate(self._opt_rects):
            if r.collidepoint(mouse_pos) and self.result is None:
                self._hover_opt = i
        if self._hover_opt >= 0:
            self._hover_tick += 1
        else:
            self._hover_tick = 0
        if self._done_rect:
            self._done_hover = self._done_rect.collidepoint(mouse_pos)

        for ev in events:
            if ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 1:
                if self.result is None:
                    for i, r in enumerate(self._opt_rects):
                        if r.collidepoint(ev.pos):
                            self.selection = i
                            correct_idx = self.pregunta["correcta"]
                            self.result = (i == correct_idx)
                            self.tick   = 0
                            # Mark states
                            self._opt_states[correct_idx] = 'correct'
                            if not self.result:
                                self._opt_states[i] = 'wrong'
                            # Create done button
                            self._done_rect = pygame.Rect(
                                self.W - 280, self.H - 90, 260, 56)
                            return None
                else:
                    if self._done_rect and self._done_rect.collidepoint(ev.pos):
                        return "done"
        return None

    def draw(self, surf):
        surf.fill(_C["fondo"])
        ac = self.acento

        # Scanlines
        sc = pygame.Surface((self.W, self.H), pygame.SRCALPHA)
        for sy in range(0, self.H, 4):
            pygame.draw.line(sc, (0, 0, 0, 30), (0, sy), (self.W, sy))
        surf.blit(sc, (0, 0))

        # Header
        hud = pygame.Surface((self.W, 90), pygame.SRCALPHA)
        hud.fill((6, 10, 20, 220))
        surf.blit(hud, (0, 0))
        pygame.draw.line(surf, ac, (0, 90), (self.W, 90), 2)
        pygame.draw.rect(surf, ac, (0, 0, 4, 90))
        pygame.draw.rect(surf, ac, (self.W - 4, 0, 4, 90))
        _draw_text_centered(surf, "⚖  CLASIFICA EL DELITO  ⚖",
                            self._font_title, ac, self.W // 2, 28)
        _draw_text_centered(surf, "Lee cada opción con atención antes de elegir.",
                            self._font_sm, _C["texto_dim"], self.W // 2, 60)

        # Question box
        q_box = pygame.Surface((self.W - 80, 80), pygame.SRCALPHA)
        q_box.fill((10, 16, 28, 200))
        surf.blit(q_box, (40, 100))
        pygame.draw.rect(surf, ac, (40, 100, self.W - 80, 80), 1, border_radius=8)
        _draw_multiline(surf, self.pregunta["texto"], self._font_sub,
                        _C["texto"], 60, 112, self.W - 120)

        # Options
        for i, (r, st) in enumerate(zip(self._opt_rects, self._opt_states)):
            if st == 'correct':
                bg, brd = _C["boton_ok"], _C["verde"]
            elif st == 'wrong':
                bg, brd = _C["boton_bad"], _C["rojo"]
            elif i == self._hover_opt:
                bg, brd = _C["boton_h"], ac
            else:
                bg, brd = _C["boton_n"], _C["borde"]

            pygame.draw.rect(surf, bg, r, border_radius=8)
            pygame.draw.rect(surf, brd, r, 2, border_radius=8)

            prefix = "✔ " if st == 'correct' else ("✘ " if st == 'wrong' else f"{i+1}. ")
            txt = prefix + self.pregunta["opciones"][i]
            tc = _C["verde"] if st == 'correct' else (_C["rojo"] if st == 'wrong' else _C["texto"])
            _draw_text_centered(surf, txt, self._font_md, tc, r.centerx, r.centery)

        # Result feedback
        if self.result is not None and self.tick > 10:
            col = _C["verde"] if self.result else _C["rojo"]
            msg = "✔ ¡RESPUESTA CORRECTA!" if self.result else "✘ RESPUESTA INCORRECTA"
            _draw_text_centered(surf, msg, self._font_sub, col, self.W // 2, 590)
            _draw_multiline(surf, self.pregunta["explicacion"], self._font_sm,
                            _C["texto_dim"], 80, 618, self.W - 160)

        # Tooltip de ley al hacer hover sobre una opción (sólo antes de responder)
        elif self._hover_opt >= 0 and self._hover_tick > 12 and self.result is None:
            r = self._opt_rects[self._hover_opt]
            opcion_txt = self.pregunta["opciones"][self._hover_opt]
            info = self._get_ley_info(opcion_txt)
            # Panel tooltip
            tip_lines = _wrap(info, self._font_xs, 680)
            tip_h = len(tip_lines) * 16 + 18
            tip_y = r.bottom + 6
            if tip_y + tip_h > self.H - 20:
                tip_y = r.top - tip_h - 6
            tip_bg = pygame.Surface((700, tip_h), pygame.SRCALPHA)
            tip_bg.fill((8, 14, 28, 220))
            surf.blit(tip_bg, (self.W // 2 - 350, tip_y))
            pygame.draw.rect(surf, ac,
                             (self.W // 2 - 350, tip_y, 700, tip_h), 1, border_radius=6)
            # Icon + title
            _draw_text_left(surf, "📖  ", self._font_xs, ac,
                            self.W // 2 - 344, tip_y + 4)
            for li, ln in enumerate(tip_lines):
                _draw_text_left(surf, ln, self._font_xs, _C["texto"],
                                self.W // 2 - 330, tip_y + 4 + li * 16)

        # Done button
        if self._done_rect:
            brc = _C["verde"] if self.result else _C["acento2"]
            bgc = _C["boton_h"] if self._done_hover else _C["boton_n"]
            pygame.draw.rect(surf, bgc, self._done_rect, border_radius=8)
            pygame.draw.rect(surf, brc, self._done_rect, 2, border_radius=8)
            lbl = "► COMPLETAR" if self.result else "► TERMINAR"
            ls = self._font_md.render(lbl, True, brc)
            surf.blit(ls, (self._done_rect.centerx - ls.get_width() // 2,
                           self._done_rect.centery - ls.get_height() // 2))


# ──────────────────────────────────────────────────────────
#  POP-UP DE RESULTADO
# ──────────────────────────────────────────────────────────

class ResultPopup:
    """Pop-up que muestra si el minijuego fue ganado o perdido."""

    def __init__(self, won: bool, xp_gained: int = 0):
        self.won  = won
        self.xp   = xp_gained
        self.tick = 0
        self.W, self.H = 1280, 720

        self._font_xl  = _font(34, bold=True)
        self._font_lg  = _font(20, bold=True)
        self._font_md  = _font(15)
        self._btn_rect = pygame.Rect(self.W // 2 - 120, self.H // 2 + 110, 240, 52)
        self._btn_hover = False

        # Particles for win effect
        self._particles = []
        if won:
            for _ in range(40):
                self._particles.append({
                    "x": random.uniform(0, self.W),
                    "y": random.uniform(self.H // 2 - 100, self.H // 2 + 20),
                    "vx": random.uniform(-3, 3),
                    "vy": random.uniform(-5, -1),
                    "col": random.choice([_C["verde"], _C["acento"], _C["acento2"]]),
                    "r": random.randint(3, 7),
                    "life": random.randint(40, 90),
                    "max_life": 90,
                })

    def update(self, events, mouse_pos):
        self.tick += 1
        self._btn_hover = self._btn_rect.collidepoint(mouse_pos)
        # Update particles
        for p in self._particles:
            p["x"] += p["vx"]; p["y"] += p["vy"]; p["vy"] += 0.1; p["life"] -= 1
        self._particles = [p for p in self._particles if p["life"] > 0]

        for ev in events:
            if (ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 1
                    and self._btn_rect.collidepoint(ev.pos)):
                return "close"
            if ev.type == pygame.KEYDOWN and ev.key in (pygame.K_RETURN, pygame.K_SPACE):
                return "close"
        return None

    def draw(self, surf):
        # Dark overlay
        ov = pygame.Surface((self.W, self.H), pygame.SRCALPHA)
        ov.fill((0, 0, 0, 160))
        surf.blit(ov, (0, 0))

        # Particles (win only)
        for p in self._particles:
            a = int(255 * p["life"] / p["max_life"])
            ps = pygame.Surface((p["r"] * 2, p["r"] * 2), pygame.SRCALPHA)
            pygame.draw.circle(ps, (*p["col"], a), (p["r"], p["r"]), p["r"])
            surf.blit(ps, (int(p["x"]) - p["r"], int(p["y"]) - p["r"]))

        # Panel
        pw, ph = 700, 320
        px, py = self.W // 2 - pw // 2, self.H // 2 - ph // 2
        ac = _C["verde"] if self.won else _C["rojo"]

        panel = pygame.Surface((pw, ph), pygame.SRCALPHA)
        panel.fill((8, 14, 26, 240))
        surf.blit(panel, (px, py))

        # Pulsing border
        pulse = 0.6 + 0.4 * math.sin(self.tick * 0.12)
        bc = tuple(int(c * pulse) for c in ac)
        pygame.draw.rect(surf, bc, (px, py, pw, ph), 3, border_radius=14)

        # Top accent line
        pygame.draw.rect(surf, ac, (px, py, pw, 6), border_radius=14)

        cx = self.W // 2

        if self.won:
            _draw_text_centered(surf, "🏆  MISIÓN COMPLETADA", self._font_xl, _C["verde"], cx, py + 55)
            _draw_text_centered(surf, f"¡Identificaste el delito correctamente!",
                                self._font_lg, _C["texto"], cx, py + 110)
            if self.xp > 0:
                _draw_text_centered(surf, f"+{self.xp} XP  ganados",
                                    self._font_lg, _C["acento2"], cx, py + 148)
            _draw_text_centered(surf, "El investigador avanza en la red de protección digital.",
                                self._font_md, _C["texto_dim"], cx, py + 188)
        else:
            _draw_text_centered(surf, "✘  MISIÓN FALLIDA", self._font_xl, _C["rojo"], cx, py + 55)
            _draw_text_centered(surf, "La respuesta fue incorrecta.",
                                self._font_lg, _C["texto"], cx, py + 110)
            _draw_text_centered(surf, "No se obtiene XP. ¡Inténtalo de nuevo en otro momento!",
                                self._font_md, _C["texto_dim"], cx, py + 148)
            _draw_text_centered(surf, "El agresor sigue libre... por ahora.",
                                self._font_md, (180, 80, 80), cx, py + 180)

        # Button
        bgc = _C["boton_h"] if self._btn_hover else _C["boton_n"]
        pygame.draw.rect(surf, bgc, self._btn_rect, border_radius=8)
        pygame.draw.rect(surf, ac, self._btn_rect, 2, border_radius=8)
        lbl = self._font_md.render("► CONTINUAR", True, ac)
        surf.blit(lbl, (self._btn_rect.centerx - lbl.get_width() // 2,
                        self._btn_rect.centery - lbl.get_height() // 2))


# ──────────────────────────────────────────────────────────
#  CONTROLADOR DEL MINIJUEGO COMPLETO
# ──────────────────────────────────────────────────────────

class MinigameController:
    """
    Orquesta las tres fases del minijuego:
      fase 0 → EvidenciasScreen
      fase 1 → PreguntaScreen
      fase 2 → ResultPopup
    Devuelve 'done' con self.won cuando termina.
    """
    MINIGAME_XP = 30

    def __init__(self, nivel_data):
        self.nivel_data = nivel_data
        self.fase       = 0
        self.won        = False
        self._evidencias = EvidenciasScreen(nivel_data)
        self._pregunta   = None
        self._popup      = None

    def update(self, events, mouse_pos):
        """Retorna 'done' cuando el minijuego termina, None en otro caso."""
        if self.fase == 0:
            r = self._evidencias.update(events, mouse_pos)
            if r == "pregunta":
                self._pregunta = PreguntaScreen(self.nivel_data)
                self.fase = 1
        elif self.fase == 1:
            r = self._pregunta.update(events, mouse_pos)
            if r == "done":
                self.won = (self._pregunta.result is True)
                xp = self.MINIGAME_XP if self.won else 0
                self._popup = ResultPopup(self.won, xp)
                self.fase = 2
        elif self.fase == 2:
            r = self._popup.update(events, mouse_pos)
            if r == "close":
                return "done"
        return None

    def draw(self, surf):
        if self.fase == 0:
            self._evidencias.draw(surf)
        elif self.fase == 1:
            self._pregunta.draw(surf)
        elif self.fase == 2:
            # Draw whatever was last visible as background, then popup
            if self._pregunta:
                self._pregunta.draw(surf)
            self._popup.draw(surf)

    @property
    def xp_reward(self):
        return self.MINIGAME_XP if self.won else 0
