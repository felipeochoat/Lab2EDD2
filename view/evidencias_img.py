"""
evidencias_img.py
Genera imágenes realistas (mockups) de evidencias digitales para mostrar
en el tooltip de la pantalla de recolección.

Cada función recibe los metadatos del caso (víctima, agresor, plataforma, etc.)
y devuelve un pygame.Surface listo para blittear.
"""

import pygame
import random

# ── Paleta interna ─────────────────────────────────────────────────────────────
_BG_PHONE   = (18, 18, 28)
_BG_SCREEN  = (12, 16, 26)
_BG_CHAT    = (22, 28, 44)
_WHITE      = (240, 245, 255)
_GRAY       = (140, 150, 170)
_GRAY_DIM   = (70, 80, 100)
_BLUE_MSG   = (30, 90, 200)
_GREEN_MSG  = (25, 130, 60)
_RED        = (200, 50, 60)
_YELLOW     = (240, 190, 50)
_CYAN       = (60, 190, 240)
_PHONE_BEZEL= (28, 32, 48)

_FONT_CACHE = {}

def _f(size, bold=False):
    key = (size, bold)
    if key not in _FONT_CACHE:
        try:
            _FONT_CACHE[key] = pygame.font.SysFont("consolas", size, bold=bold)
        except Exception:
            _FONT_CACHE[key] = pygame.font.SysFont(None, size, bold=bold)
    return _FONT_CACHE[key]

def _text(surf, txt, size, color, x, y, bold=False, centerx=None):
    f = _f(size, bold)
    s = f.render(str(txt), True, color)
    if centerx is not None:
        x = centerx - s.get_width() // 2
    surf.blit(s, (x, y))
    return s.get_height()

def _wrap(txt, size, max_w):
    """Divide texto en líneas que caben en max_w px."""
    f = _f(size)
    words = txt.split()
    lines, cur = [], ""
    for w in words:
        test = (cur + " " + w).strip()
        if f.size(test)[0] <= max_w:
            cur = test
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines

def _multiline(surf, txt, size, color, x, y, max_w, spacing=4):
    h = _f(size).get_height() + spacing
    for line in _wrap(txt, size, max_w):
        _text(surf, line, size, color, x, y)
        y += h
    return y

# ── Helpers de forma ──────────────────────────────────────────────────────────

def _rrect(surf, color, rect, radius=6, border=0, border_color=None):
    pygame.draw.rect(surf, color, rect, border_radius=radius)
    if border and border_color:
        pygame.draw.rect(surf, border_color, rect, border, border_radius=radius)

def _burbuja_chat(surf, texto, x, y, max_w, lado="derecha", size=11):
    """Dibuja una burbuja de chat. lado='derecha' (agresor azul) o 'izquierda' (víctima gris)."""
    f = _f(size)
    lines = _wrap(texto, size, max_w - 20)
    lh = f.get_height() + 2
    bh = lh * len(lines) + 12
    bw = max(min(max_w, max(f.size(l)[0] for l in lines) + 20), 60)

    col = _BLUE_MSG if lado == "derecha" else (50, 55, 75)
    bx = x - bw if lado == "derecha" else x

    _rrect(surf, col, (bx, y, bw, bh), radius=8)

    ty = y + 6
    for line in lines:
        _text(surf, line, size, _WHITE, bx + 10, ty)
        ty += lh
    return y + bh + 6


# ══════════════════════════════════════════════════════════════════════════════
#  MOCKUP 1: CELULAR CON CHAT (captura de pantalla / historial)
# ══════════════════════════════════════════════════════════════════════════════

def mockup_celular_chat(agresor, victima, plataforma, mensajes, W=320, H=420):
    """
    Dibuja un celular vertical con burbujas de chat realistas.
    mensajes: lista de (lado, texto)  lado='derecha'|'izquierda'
    """
    surf = pygame.Surface((W, H), pygame.SRCALPHA)

    # Bisel del celular
    _rrect(surf, _PHONE_BEZEL, (0, 0, W, H), radius=22)
    # Pantalla
    screen_rect = (8, 28, W - 16, H - 56)
    _rrect(surf, _BG_CHAT, screen_rect, radius=14)

    sx, sy, sw, sh = screen_rect

    # Barra de estado (hora + batería)
    _text(surf, "22:47", 9, _GRAY, sx + 8, sy + 6)
    _text(surf, "▊▊▊ 78%", 9, _GRAY, sx + sw - 68, sy + 6)

    # Cabecera de la app de chat
    _rrect(surf, (25, 32, 55), (sx, sy, sw, 38), radius=0)
    pygame.draw.circle(surf, _GRAY, (sx + 22, sy + 19), 11)          # avatar
    pygame.draw.circle(surf, (60, 200, 100), (sx + 30, sy + 27), 4)  # indicador online
    _text(surf, agresor[:16], 11, _WHITE, sx + 38, sy + 8, bold=True)
    _text(surf, plataforma, 9, _GRAY, sx + 38, sy + 22)
    # Botón atrás
    _text(surf, "◀", 11, _CYAN, sx + 4, sy + 13)

    # Área de mensajes
    my = sy + 48
    cx_right = sx + sw - 12   # ancla derecha
    cx_left  = sx + 12        # ancla izquierda
    for lado, msg in mensajes:
        if my > sy + sh - 40:
            break
        if lado == "derecha":
            my = _burbuja_chat(surf, msg, cx_right, my, sw - 24, "derecha")
        else:
            my = _burbuja_chat(surf, msg, cx_left, my, sw - 24, "izquierda")

    # Barra de input
    _rrect(surf, (30, 36, 60), (sx, sy + sh - 32, sw, 32), radius=0)
    _rrect(surf, (40, 48, 80), (sx + 8, sy + sh - 26, sw - 56, 20), radius=10)
    _text(surf, "Escribe un mensaje…", 9, _GRAY_DIM, sx + 14, sy + sh - 22)
    pygame.draw.circle(surf, _CYAN, (sx + sw - 18, sy + sh - 16), 10)
    _text(surf, "▶", 9, _WHITE, sx + sw - 23, sy + sh - 20)

    # Notch / cámara frontal
    _rrect(surf, _PHONE_BEZEL, (W // 2 - 18, 10, 36, 10), radius=5)
    pygame.draw.circle(surf, (40, 40, 60), (W // 2, 15), 4)

    # Botón home
    pygame.draw.circle(surf, (40, 44, 64), (W // 2, H - 16), 8)
    pygame.draw.circle(surf, (55, 60, 85), (W // 2, H - 16), 6, 2)

    return surf


# ══════════════════════════════════════════════════════════════════════════════
#  MOCKUP 2: PANTALLA DE RED SOCIAL (post viral / perfil)
# ══════════════════════════════════════════════════════════════════════════════

def mockup_red_social_post(agresor, victima, plataforma, contenido,
                            compartidos=0, likes=0, W=320, H=380):
    surf = pygame.Surface((W, H), pygame.SRCALPHA)
    _rrect(surf, _BG_SCREEN, (0, 0, W, H), radius=10)

    # Barra superior de la app
    _rrect(surf, (20, 24, 42), (0, 0, W, 36), radius=0)
    _text(surf, plataforma.upper(), 12, _CYAN, 0, 10, bold=True, centerx=W // 2)

    # Tarjeta del post
    card_y = 44
    _rrect(surf, (26, 32, 52), (8, card_y, W - 16, H - 52), radius=8,
           border=1, border_color=(50, 60, 90))

    cy = card_y + 10

    # Cabecera del post: avatar + nombre
    pygame.draw.circle(surf, _RED, (26, cy + 14), 13)       # avatar agresor
    _text(surf, "X", 12, _WHITE, 22, cy + 8, bold=True)     # placeholder foto
    _text(surf, agresor[:18], 11, _WHITE, 44, cy + 4, bold=True)
    _text(surf, "• hace 2 horas", 9, _GRAY, 44, cy + 18)
    # Badge "FALSO"
    _rrect(surf, _RED, (W - 58, cy + 6, 46, 16), radius=4)
    _text(surf, "⚠ FALSO", 8, _WHITE, W - 56, cy + 9, bold=True)
    cy += 36

    # Separador
    pygame.draw.line(surf, (40, 50, 75), (16, cy), (W - 16, cy))
    cy += 8

    # Contenido del post
    cy = _multiline(surf, contenido, 11, _WHITE, 16, cy, W - 32, spacing=3)
    cy += 8

    # Imagen de placeholder en el post
    img_h = min(80, H - cy - 80)
    if img_h > 20:
        _rrect(surf, (35, 42, 68), (16, cy, W - 32, img_h), radius=4)
        _text(surf, "[ imagen adjunta ]", 9, _GRAY_DIM, 0, cy + img_h // 2 - 6,
              centerx=W // 2)
        cy += img_h + 8

    # Separador
    pygame.draw.line(surf, (40, 50, 75), (16, cy), (W - 16, cy))
    cy += 6

    # Métricas
    _text(surf, f"♥  {likes or random.randint(200,800)}", 10, _RED, 16, cy)
    _text(surf, f"↗  {compartidos or random.randint(50,500)} compartidos", 10, _YELLOW,
          W // 2 - 40, cy)
    cy += 20

    # Botones de acción
    btn_w = (W - 32) // 3
    for i, (icon, label) in enumerate([("♥","Me gusta"), ("💬","Comentar"), ("↗","Compartir")]):
        bx = 16 + i * btn_w
        _rrect(surf, (32, 40, 65), (bx, cy, btn_w - 4, 24), radius=4)
        _text(surf, f"{icon} {label}", 9, _GRAY, bx + 4, cy + 6)
    cy += 30

    # Barra inferior de navegación
    _rrect(surf, (16, 20, 36), (0, H - 36, W, 36), radius=0)
    for i, ico in enumerate(["🏠", "🔍", "＋", "🔔", "👤"]):
        _text(surf, ico, 14, _GRAY, 0, H - 28, centerx=16 + i * (W // 5) + W // 10)

    return surf


# ══════════════════════════════════════════════════════════════════════════════
#  MOCKUP 3: PANTALLA DE PERFIL FALSO / SUPLANTACIÓN
# ══════════════════════════════════════════════════════════════════════════════

def mockup_perfil_falso(victima, agresor, plataforma, W=320, H=380):
    surf = pygame.Surface((W, H), pygame.SRCALPHA)
    _rrect(surf, _BG_SCREEN, (0, 0, W, H), radius=10)

    # Fondo de portada (banner)
    _rrect(surf, (30, 50, 90), (0, 0, W, 90), radius=10)
    # Líneas decorativas del banner
    for i in range(5):
        pygame.draw.line(surf, (40, 65, 110), (0, 18 * i), (W, 18 * i), 1)

    # Foto de perfil (doble para indicar que es copia)
    pygame.draw.circle(surf, (60, 80, 130), (W // 2, 88), 38)        # sombra
    pygame.draw.circle(surf, (90, 120, 180), (W // 2, 88), 34)       # foto base
    _text(surf, victima[0].upper(), 22, _WHITE, 0, 72, bold=True, centerx=W // 2)

    # Sello de FALSO
    _rrect(surf, _RED, (W // 2 + 20, 60, 50, 20), radius=4)
    _text(surf, "FALSO", 9, _WHITE, W // 2 + 22, 65, bold=True)
    # Cruz roja superpuesta
    pygame.draw.line(surf, (*_RED, 180), (W // 2 - 34, 54), (W // 2 + 34, 122), 3)
    pygame.draw.line(surf, (*_RED, 180), (W // 2 + 34, 54), (W // 2 - 34, 122), 3)

    cy = 132
    _text(surf, victima + " [CUENTA CLONADA]", 11, _WHITE, 0, cy, bold=True, centerx=W // 2)
    cy += 18
    _text(surf, "@" + victima.lower().replace(" ", "_") + "_real2", 10, _CYAN,
          0, cy, centerx=W // 2)
    cy += 16
    _text(surf, f"📍 Mismo colegio • {plataforma}", 9, _GRAY, 0, cy, centerx=W // 2)
    cy += 20

    # Stats del perfil falso
    for label, val in [("Publicaciones", "12"), ("Seguidores", "847"), ("Siguiendo", "203")]:
        pass  # se dibuja abajo en fila

    pygame.draw.line(surf, (40, 50, 75), (16, cy), (W - 16, cy))
    cy += 8
    col_w = (W - 32) // 3
    for i, (label, val) in enumerate([("Posts", "12"), ("Seguidores", "847"), ("Siguiendo", "203")]):
        cx_col = 16 + i * col_w + col_w // 2
        _text(surf, val, 13, _WHITE, 0, cy, bold=True, centerx=cx_col)
        _text(surf, label, 8, _GRAY, 0, cy + 16, centerx=cx_col)
    cy += 36

    pygame.draw.line(surf, (40, 50, 75), (16, cy), (W - 16, cy))
    cy += 8

    # Último post del perfil falso
    _text(surf, "Última publicación:", 9, _GRAY, 16, cy)
    cy += 14
    contenido_falso = f"Hola soy {victima}, manden mgs 👋"
    _multiline(surf, contenido_falso, 10, _WHITE, 16, cy, W - 32)
    cy += 28

    # Advertencia
    _rrect(surf, (60, 20, 20), (8, H - 52, W - 16, 40), radius=6,
           border=1, border_color=_RED)
    _text(surf, "⚠ Cuenta reportada como suplantación", 9, _RED, 16, H - 44)
    _text(surf, "IP: 181.xx.xx.xx  •  Creada hace 3 días", 9, _GRAY_DIM, 16, H - 30)

    return surf


# ══════════════════════════════════════════════════════════════════════════════
#  MOCKUP 4: PANTALLA DE METADATA / IP
# ══════════════════════════════════════════════════════════════════════════════

def mockup_metadata_ip(agresor, plataforma, W=320, H=360):
    surf = pygame.Surface((W, H), pygame.SRCALPHA)
    _rrect(surf, (8, 12, 20), (0, 0, W, H), radius=10)

    # Cabecera terminal
    _rrect(surf, (20, 28, 44), (0, 0, W, 32), radius=8)
    pygame.draw.circle(surf, (220, 60, 60), (14, 16), 5)
    pygame.draw.circle(surf, _YELLOW, (26, 16), 5)
    pygame.draw.circle(surf, (60, 200, 80), (38, 16), 5)
    _text(surf, "ANÁLISIS FORENSE – METADATA", 9, _GRAY, 50, 11, bold=True)

    cy = 40
    _text(surf, "$ extract-metadata --platform " + plataforma, 10, (0, 255, 0), 10, cy)
    cy += 16
    _text(surf, "> Procesando...", 9, _GRAY, 10, cy)
    cy += 14

    pygame.draw.line(surf, (30, 40, 60), (8, cy), (W - 8, cy))
    cy += 8

    ip = f"181.{random.randint(50,200)}.{random.randint(1,254)}.{random.randint(1,254)}"
    datos = [
        ("IP origen",       ip),
        ("Proveedor",       "Claro Colombia"),
        ("Ciudad aprox.",   "Barranquilla, CO"),
        ("Dispositivo",     "Android 13 – Chrome"),
        ("User-Agent",      "Mozilla/5.0 Mobile"),
        ("Timestamp",       "2024-09-12  22:47:03"),
        ("Plataforma",      plataforma),
        ("Cuenta objetivo", "perfil de " + agresor[:12]),
        ("Acción",          "Publicación / envío msg"),
        ("Hash MD5",        "a3f9b2...c041"),
    ]
    for key, val in datos:
        if cy > H - 24:
            break
        _text(surf, key + ":", 9, _CYAN, 12, cy)
        _text(surf, val, 9, (0, 255, 0), 120, cy)
        cy += 14

    pygame.draw.line(surf, (30, 40, 60), (8, cy), (W - 8, cy))
    cy += 6
    _text(surf, "✔ Evidencia vinculada a: " + agresor[:16], 9, _YELLOW, 12, cy, bold=True)

    return surf


# ══════════════════════════════════════════════════════════════════════════════
#  MOCKUP 5: LOGS DE ACTIVIDAD (terminal verde)
# ══════════════════════════════════════════════════════════════════════════════

def mockup_logs_actividad(agresor, num_cuentas=3, num_semanas=2, W=320, H=360):
    surf = pygame.Surface((W, H), pygame.SRCALPHA)
    _rrect(surf, (4, 10, 4), (0, 0, W, H), radius=10)

    _rrect(surf, (10, 20, 10), (0, 0, W, 30), radius=8)
    _text(surf, "◉ SYSTEM LOG — ACCESS RECORDS", 9, (0, 220, 0), 10, 10, bold=True)

    cy = 36
    horas = ["08:12", "10:45", "13:22", "16:08", "19:33", "21:47", "22:58", "23:41"]
    acciones = [
        f"LOGIN  cuenta_{agresor[:6]}_1",
        f"POST   mensaje_ofensivo.txt → víctima",
        f"LOGIN  cuenta_{agresor[:6]}_2",
        f"POST   imagen_editada.jpg → feed",
        f"LOGIN  cuenta_{agresor[:6]}_3",
        f"SEND   DM masivo × 47 usuarios",
        f"DELETE log_anterior.db",
        f"LOGOUT (sesión {num_semanas}w continua)",
    ]
    cols = [(0, 200, 0), (200, 60, 60), (0, 200, 0), (200, 140, 0),
            (0, 200, 0), (200, 60, 60), (200, 60, 60), (0, 160, 0)]

    for i, (h, acc, col) in enumerate(zip(horas, acciones, cols)):
        if cy > H - 20:
            break
        _text(surf, h, 9, (0, 140, 0), 8, cy)
        _text(surf, acc[:32], 9, col, 52, cy)
        cy += 13

    pygame.draw.line(surf, (0, 80, 0), (8, cy + 2), (W - 8, cy + 2))
    cy += 8
    _text(surf, f"TOTAL: {num_cuentas} cuentas  |  {num_semanas} semanas activo", 9,
          _YELLOW, 8, cy, bold=True)
    cy += 14
    _text(surf, f"FINGERPRINT ÚNICO → {agresor[:14]}", 9, _YELLOW, 8, cy, bold=True)

    # Cursor parpadeante (estático)
    _text(surf, "█", 10, (0, 255, 0), 8, cy + 14)

    return surf


# ══════════════════════════════════════════════════════════════════════════════
#  MOCKUP 6: TESTIMONIO / DECLARACIÓN
# ══════════════════════════════════════════════════════════════════════════════

def mockup_testimonio(victima, agresor, num_testimonios=3, W=320, H=360):
    surf = pygame.Surface((W, H), pygame.SRCALPHA)
    _rrect(surf, (20, 18, 30), (0, 0, W, H), radius=10)

    _rrect(surf, (30, 26, 48), (0, 0, W, 34), radius=8)
    _text(surf, "📋 TESTIMONIOS RECOPILADOS", 10, _YELLOW, 0, 11, bold=True, centerx=W // 2)

    cy = 42
    nombres = ["Estudiante A", "Compañero B", "Testigo C", "Docente D", "Amigo E"]
    textos = [
        f"Vi cuando {agresor[:10]} publicó eso. Era mentira.",
        f"{agresor[:10]} lo hacía casi todos los días en el grupo.",
        f"El perfil de {victima} fue copiado, yo lo reporté.",
        f"Tuve que intervenir por el daño a {victima}.",
        f"Guardé captura antes de que borrara el post.",
    ]
    for i in range(min(num_testimonios, 4)):
        if cy > H - 30:
            break
        # Burbuja de declaración
        _rrect(surf, (30, 36, 58), (8, cy, W - 16, 56), radius=8,
               border=1, border_color=(60, 70, 100))
        # Mini avatar
        pygame.draw.circle(surf, (80 + i * 20, 100, 160), (24, cy + 18), 11)
        _text(surf, nombres[i][0], 10, _WHITE, 0, cy + 12, bold=True, centerx=24)
        # Nombre
        _text(surf, nombres[i], 10, _CYAN, 40, cy + 6, bold=True)
        # Declaración
        _multiline(surf, f'"{textos[i]}"', 9, _WHITE, 40, cy + 20, W - 52)
        cy += 64

    pygame.draw.line(surf, (40, 50, 75), (8, cy), (W - 8, cy))
    cy += 6
    _text(surf, f"✔ {num_testimonios} declaraciones verificadas", 9, (60, 220, 80), 10, cy, bold=True)

    return surf


# ══════════════════════════════════════════════════════════════════════════════
#  MOCKUP 7: ANÁLISIS DE MÚLTIPLES CUENTAS
# ══════════════════════════════════════════════════════════════════════════════

def mockup_analisis_cuentas(agresor, num_cuentas=4, W=320, H=380):
    surf = pygame.Surface((W, H), pygame.SRCALPHA)
    _rrect(surf, (12, 10, 22), (0, 0, W, H), radius=10)

    _rrect(surf, (22, 18, 40), (0, 0, W, 34), radius=8)
    _text(surf, "🔍 ANÁLISIS DE CUENTAS VINCULADAS", 9, (160, 80, 255), 0, 11,
          bold=True, centerx=W // 2)

    cy = 42
    sufijos = ["_alt", "_2", "_real", "_xd", "_bk", "_res", "_v2", "_3"]
    for i in range(min(num_cuentas, 6)):
        if cy > H - 50:
            break
        nombre_cuenta = agresor[:8] + sufijos[i]
        activa = i % 3 != 0   # algunas eliminadas
        col_estado = (60, 200, 80) if activa else _RED
        estado_txt  = "ACTIVA" if activa else "ELIMINADA"

        _rrect(surf, (26, 22, 45), (8, cy, W - 16, 42), radius=6,
               border=1, border_color=(60, 50, 90))
        pygame.draw.circle(surf, (120 + i * 15, 80, 200 - i * 20), (24, cy + 20), 10)
        _text(surf, str(i + 1), 8, _WHITE, 0, cy + 15, bold=True, centerx=24)
        _text(surf, "@" + nombre_cuenta, 10, _WHITE, 38, cy + 6, bold=True)
        _text(surf, f"Creada: 2024-0{i+1}-{random.randint(1,28):02d}", 8, _GRAY, 38, cy + 20)
        _rrect(surf, col_estado, (W - 76, cy + 10, 64, 16), radius=4)
        _text(surf, estado_txt, 8, _WHITE, W - 74, cy + 13, bold=True)
        cy += 50

    pygame.draw.line(surf, (50, 40, 80), (8, cy), (W - 8, cy))
    cy += 8
    _text(surf, f"Patrón: mismo dispositivo · mismo horario", 9, _YELLOW, 10, cy)
    cy += 14
    _text(surf, f"→ Vinculadas a: {agresor[:16]}", 9, (160, 80, 255), 10, cy, bold=True)

    return surf


# ══════════════════════════════════════════════════════════════════════════════
#  MOCKUP 8: HISTORIAL ESCOLAR / DOCUMENTO
# ══════════════════════════════════════════════════════════════════════════════

def mockup_historial_escolar(agresor, victima, colegio, W=320, H=380):
    surf = pygame.Surface((W, H), pygame.SRCALPHA)
    _rrect(surf, (240, 232, 210), (0, 0, W, H), radius=8)

    # Encabezado institucional
    _rrect(surf, (30, 60, 140), (0, 0, W, 50), radius=8)
    _text(surf, "INSTITUCIÓN EDUCATIVA", 10, _WHITE, 0, 8, bold=True, centerx=W // 2)
    _text(surf, colegio.replace("el ", "").replace("la ", "")[:28],
          9, (200, 220, 255), 0, 22, centerx=W // 2)
    _text(surf, "REPORTE DE INCIDENTE", 9, _YELLOW, 0, 36, centerx=W // 2)

    cy = 58
    pygame.draw.line(surf, (180, 160, 120), (10, cy), (W - 10, cy))
    cy += 6

    campos = [
        ("Fecha de reporte",  "12 de Septiembre, 2024"),
        ("Tipo de incidente", "Conflicto / Acoso escolar"),
        ("Alumno implicado",  agresor),
        ("Afectado/a",        victima),
        ("Institución",       colegio[:24]),
        ("Docente reporta",   "Prof. Rodríguez M."),
        ("Observaciones",     "Agresiones verbales previas"),
        ("Estado",            "⚠ En seguimiento activo"),
    ]
    for label, val in campos:
        if cy > H - 50:
            break
        _text(surf, label + ":", 9, (80, 60, 40), 12, cy, bold=True)
        _text(surf, val, 9, (30, 30, 30), 12, cy + 12)
        pygame.draw.line(surf, (200, 185, 155), (12, cy + 24), (W - 12, cy + 24))
        cy += 30

    # Sello
    _rrect(surf, (200, 30, 30), (W - 90, H - 70, 76, 56), radius=6)
    _text(surf, "CONFIDENCIAL", 7, _WHITE, 0, H - 58, bold=True, centerx=W - 52)
    _text(surf, "Uso Interno", 7, _WHITE, 0, H - 46, centerx=W - 52)
    _text(surf, "Folio #" + str(random.randint(100, 999)), 7, _WHITE, 0, H - 34,
          centerx=W - 52)

    return surf


# ══════════════════════════════════════════════════════════════════════════════
# ══════════════════════════════════════════════════════════════════════════════
#  MOCKUP NUEVO: HISTORIAL DE CHAT (frecuencia de ataques, gráfico + lista)
# ══════════════════════════════════════════════════════════════════════════════

def mockup_historial_chat(agresor, victima, plataforma, num_mensajes=18, num_dias=7, W=320, H=420):
    """
    Muestra cuántas veces el acosador ha escrito a la víctima:
    - Gráfico de barras por día
    - Lista de mensajes recientes con timestamps
    - Contador total resaltado
    """
    surf = pygame.Surface((W, H), pygame.SRCALPHA)

    # Fondo tipo tablet/reporte forense
    _rrect(surf, (10, 14, 28), (0, 0, W, H), radius=12)
    _rrect(surf, (22, 30, 55), (0, 0, W, H), radius=12, border=2, border_color=(60, 120, 220))

    # Cabecera
    _rrect(surf, (18, 28, 60), (0, 0, W, 46), radius=10)
    pygame.draw.line(surf, (60, 120, 220), (0, 46), (W, 46), 1)
    _text(surf, "📊 HISTORIAL DE MENSAJES", 11, (80, 200, 255), 0, 8, bold=True, centerx=W // 2)
    _text(surf, f"{plataforma}  •  {num_dias} días registrados", 9, (140, 160, 200), 0, 28, centerx=W // 2)

    cy = 56

    # ── Contador total destacado ──────────────────────────
    _rrect(surf, (30, 20, 50), (10, cy, W - 20, 38), radius=8,
           border=1, border_color=(220, 60, 80))
    _text(surf, str(num_mensajes), 22, (220, 60, 80), 0, cy + 4, bold=True, centerx=60)
    _text(surf, "mensajes ofensivos", 10, (200, 220, 255), 72, cy + 6)
    _text(surf, f"de  {agresor}  →  {victima}", 9, (140, 160, 200), 72, cy + 22)
    cy += 48

    # ── Gráfico de barras por día ─────────────────────────
    _text(surf, "Actividad por día:", 9, (140, 160, 200), 12, cy)
    cy += 14

    chart_h = 55
    chart_w = W - 24
    chart_x = 12

    # Datos aleatorios pero deterministas basados en num_mensajes
    dias_labels = ["L", "M", "X", "J", "V", "S", "D"]
    base_vals = [0.3, 0.5, 1.0, 0.7, 0.9, 0.4, 0.2]
    # Normalizar para que la suma sea num_mensajes aprox
    total_base = sum(base_vals[:num_dias])
    vals = [int(v / total_base * num_mensajes) for v in base_vals[:num_dias]]
    # Ajustar para que sume exacto
    diff = num_mensajes - sum(vals)
    if vals:
        vals[2] += diff

    max_val = max(vals) if vals else 1
    bar_w = chart_w // len(vals) - 2

    for i, (label, v) in enumerate(zip(dias_labels[:len(vals)], vals)):
        bx = chart_x + i * (chart_w // len(vals))
        bar_h = int((v / max_val) * chart_h) if max_val > 0 else 0
        by = cy + chart_h - bar_h

        # Barra de fondo
        pygame.draw.rect(surf, (30, 35, 60), (bx + 1, cy, bar_w, chart_h), border_radius=3)
        # Barra de valor
        intensity = v / max_val if max_val > 0 else 0
        col = (
            int(60 + 160 * intensity),
            int(120 - 80 * intensity),
            int(200 - 140 * intensity),
        )
        if bar_h > 0:
            pygame.draw.rect(surf, col, (bx + 1, by, bar_w, bar_h), border_radius=3)
        # Número encima
        if v > 0:
            _text(surf, str(v), 8, (200, 220, 255), bx + bar_w // 2, by - 12, centerx=bx + bar_w // 2 + 1)
        # Label día
        _text(surf, label, 8, (140, 160, 200), bx + bar_w // 2, cy + chart_h + 3, centerx=bx + bar_w // 2 + 1)

    cy += chart_h + 18

    # ── Separador ──────────────────────────────────────────
    pygame.draw.line(surf, (40, 55, 90), (10, cy), (W - 10, cy))
    cy += 8

    # ── Últimos mensajes con timestamp ────────────────────
    _text(surf, "Últimos mensajes:", 9, (140, 160, 200), 12, cy)
    cy += 14

    horas = ["22:47", "22:51", "23:05", "08:12", "08:14", "14:33"]
    msgs  = [
        f"eres un fracaso {victima[:8]}",
        "todos saben la verdad",
        "deja de quejarte jajaj",
        "nadie te quiere aquí",
        "deberías desaparecer",
        f"eres lo peor {victima[:8]}",
    ]
    for hora, msg in zip(horas, msgs):
        if cy > H - 28:
            break
        _rrect(surf, (20, 26, 48), (10, cy, W - 20, 22), radius=4)
        _text(surf, hora, 8, (80, 120, 180), 14, cy + 6)
        _text(surf, msg[:30], 9, (200, 220, 255), 54, cy + 6)
        # Punto de color = mensaje enviado
        pygame.draw.circle(surf, (220, 60, 80), (W - 16, cy + 11), 4)
        cy += 26

    # ── Footer ─────────────────────────────────────────────
    pygame.draw.line(surf, (40, 55, 90), (10, H - 22), (W - 10, H - 22))
    _text(surf, f"⚠ Patrón de acoso detectado – {num_dias} días continuos", 8,
          (220, 60, 80), 0, H - 16, bold=True, centerx=W // 2)

    return surf


# ══════════════════════════════════════════════════════════════════════════════
#  MOCKUP NUEVO: PERFIL REAL DEL AGRESOR (tarjeta de red social, no chat)
# ══════════════════════════════════════════════════════════════════════════════

def mockup_perfil_agresor(agresor_user, agresor_nombre, plataforma, victima, W=320, H=420):
    """
    Muestra el perfil real del agresor en red social:
    - Avatar, nombre de usuario, nombre real
    - Estadísticas (posts, seguidores, siguiendo)
    - Badge de 'ACOSADOR IDENTIFICADO'
    - Últimas publicaciones ofensivas
    - Datos de IP / dispositivo
    """
    surf = pygame.Surface((W, H), pygame.SRCALPHA)

    # Fondo
    _rrect(surf, (10, 12, 22), (0, 0, W, H), radius=12)

    # Banner superior degradado
    for i in range(72):
        t = i / 72
        col = (int(30 + 20 * t), int(20 + 40 * t), int(80 + 60 * t))
        pygame.draw.line(surf, col, (0, i), (W, i))
    _rrect(surf, (0, 0, 0, 0), (0, 0, W, 72), radius=12)  # Recorte esquinas

    # Líneas decorativas en banner
    for i in range(6):
        pygame.draw.line(surf, (60, 80, 160, 80), (0, 12 * i), (W, 12 * i + 20), 1)

    # Avatar del agresor (rojo - peligro)
    pygame.draw.circle(surf, (40, 20, 20), (W // 2, 68), 36)          # sombra
    pygame.draw.circle(surf, (160, 40, 50), (W // 2, 68), 32)         # fondo rojo
    pygame.draw.circle(surf, (200, 60, 70), (W // 2, 68), 28, 2)      # borde
    _text(surf, agresor_user[1].upper() if agresor_user.startswith("@") else agresor_user[0].upper(),
          20, (255, 255, 255), 0, 54, bold=True, centerx=W // 2)

    # Badge "IDENTIFICADO"
    _rrect(surf, (180, 30, 30), (W // 2 + 18, 44, 80, 18), radius=4)
    _text(surf, "⚠ ACOSADOR", 8, (255, 255, 255), W // 2 + 20, 50, bold=True)

    cy = 108

    # Nombre de usuario y nombre real
    _text(surf, agresor_user, 13, (80, 200, 255), 0, cy, bold=True, centerx=W // 2)
    cy += 18
    _text(surf, agresor_nombre, 10, (160, 180, 220), 0, cy, centerx=W // 2)
    cy += 14
    _text(surf, f"📍 {plataforma}", 9, (120, 140, 180), 0, cy, centerx=W // 2)
    cy += 18

    # Separador
    pygame.draw.line(surf, (40, 55, 90), (16, cy), (W - 16, cy))
    cy += 10

    # Estadísticas del perfil
    col_w = (W - 32) // 3
    for i, (label, val) in enumerate([("Posts", "147"), ("Seguidores", "302"), ("Siguiendo", "89")]):
        cx_col = 16 + i * col_w + col_w // 2
        _text(surf, val, 13, (200, 220, 255), 0, cy, bold=True, centerx=cx_col)
        _text(surf, label, 8, (120, 140, 180), 0, cy + 16, centerx=cx_col)

    cy += 36

    # Separador
    pygame.draw.line(surf, (40, 55, 90), (16, cy), (W - 16, cy))
    cy += 8

    # Publicaciones recientes del agresor
    _text(surf, "Publicaciones ofensivas detectadas:", 9, (220, 60, 80), 12, cy, bold=True)
    cy += 14

    publicaciones = [
        f"¿Vieron a {victima[:10]}? Que pena ajena 🤣",
        f"Alguien sabe dónde vive {victima[:10]}?",
        f"Hagan RT si creen que {victima[:10]} es mentirosa 👇",
    ]
    for pub in publicaciones:
        if cy > H - 50:
            break
        _rrect(surf, (20, 24, 44), (10, cy, W - 20, 28), radius=4,
               border=1, border_color=(60, 40, 70))
        _text(surf, pub[:38], 9, (200, 220, 255), 14, cy + 9)
        cy += 32

    # Footer con datos de identificación
    pygame.draw.line(surf, (40, 55, 90), (10, H - 30), (W - 10, H - 30))
    _rrect(surf, (20, 14, 30), (10, H - 28, W - 20, 22), radius=4)
    ip = f"181.{random.randint(50,200)}.{random.randint(1,254)}.xx"
    _text(surf, f"IP: {ip}  •  Barranquilla, CO", 8, (140, 100, 200), 0, H - 22, centerx=W // 2)

    return surf


# ══════════════════════════════════════════════════════════════════════════════
#  DISPATCHER: dado el sprite_key y los metadatos del nivel, genera el mockup
# ══════════════════════════════════════════════════════════════════════════════

def generar_imagen_evidencia(sprite_key: str, nivel_data: dict) -> pygame.Surface:
    """
    Devuelve un pygame.Surface (320×420 aprox.) con el mockup apropiado.
    nivel_data es el dict devuelto por _nivel_X_... en niveles.py
    """
    ag_user  = nivel_data.get("_agresor_user",   "@usuario")
    ag_nom   = nivel_data.get("_agresor_nombre", "Agresor")
    victima  = nivel_data.get("_victima",        "Víctima")
    plat     = nivel_data.get("_plataforma",     "Red social")
    colegio  = nivel_data.get("_colegio",        nivel_data.get("_colegios", "el Colegio"))

    # ---------- captura de pantalla: celular con mensajes ofensivos ----------
    if sprite_key == "captura":
        mensajes_ofensivos = [
            ("derecha", f"eres un fracaso {victima}"),
            ("izquierda", "por favor para…"),
            ("derecha", "no me hagas reír jajaj"),
            ("derecha", "todos saben que eres un problema"),
            ("izquierda", "¿por qué me haces esto?"),
            ("derecha", f"deja de quejarte {victima}"),
        ]
        return mockup_celular_chat(ag_user, victima, plat, mensajes_ofensivos)

    # ---------- historial de chat: gráfico de frecuencia de ataques ----------
    elif sprite_key == "chat":
        num_mensajes = nivel_data.get("_num_mensajes", 18)
        num_dias     = nivel_data.get("_num_dias",     7)
        return mockup_historial_chat(ag_user, victima, plat, num_mensajes, num_dias)

    # ---------- post viral ----------
    elif sprite_key == "post":
        contenido = f"{victima} es una ladrona, no confíen en ella. Comparte para que todos sepan."
        return mockup_red_social_post(ag_user, victima, plat, contenido,
                                      compartidos=random.randint(120, 500),
                                      likes=random.randint(80, 400))

    # ---------- perfil falso ----------
    elif sprite_key == "perfil_falso":
        return mockup_perfil_falso(victima, ag_user, plat)

    # ---------- perfil del agresor: tarjeta real de red social ----------
    elif sprite_key == "perfil":
        return mockup_perfil_agresor(ag_user, ag_nom, plat, victima)

    # ---------- metadata / IP ----------
    elif sprite_key in ("metadata", "ip"):
        return mockup_metadata_ip(ag_nom, plat)

    # ---------- logs ----------
    elif sprite_key == "logs":
        nc = nivel_data.get("_num_cuentas", 3)
        ns = nivel_data.get("_num_semanas", 2)
        return mockup_logs_actividad(ag_user, nc, ns)

    # ---------- testimonio / testigo / denuncia ----------
    elif sprite_key in ("testimonio", "testigo", "denuncia"):
        nt = nivel_data.get("_num_testimonios", 3)
        return mockup_testimonio(victima, ag_user, nt)

    # ---------- análisis de cuentas ----------
    elif sprite_key == "analisis":
        nc = nivel_data.get("_num_cuentas", 4)
        return mockup_analisis_cuentas(ag_user, nc)

    # ---------- historial escolar ----------
    elif sprite_key == "historial":
        return mockup_historial_escolar(ag_nom, victima, colegio)

    # ---------- horario de ataques ----------
    elif sprite_key == "horario":
        return mockup_logs_actividad(ag_user,
                                     nivel_data.get("_num_cuentas", 3),
                                     nivel_data.get("_num_semanas", 2))

    # ---------- dispositivo ----------
    elif sprite_key == "dispositivo":
        return mockup_metadata_ip(ag_nom, plat)

    # ---------- cuenta eliminada ----------
    elif sprite_key == "cuenta_borrada":
        return mockup_perfil_falso(victima, ag_user, plat)

    # ---------- fallback genérico ----------
    else:
        surf = pygame.Surface((320, 380), pygame.SRCALPHA)
        _rrect(surf, _BG_SCREEN, (0, 0, 320, 380), radius=10)
        _text(surf, "[ Evidencia digital ]", 12, _GRAY, 0, 180, centerx=160)
        return surf
