# model/constants.py
import os

# --- WINDOW ---
SCREEN_W = 1280
SCREEN_H = 720
FPS = 60
TITLE = "NetGuardian"

# --- PATHS ---
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ASSET_DIR = os.path.join(BASE_DIR, "assets")
DATA_DIR  = os.path.join(BASE_DIR, "data")

# --- COLOR PALETTE (cyberpunk emotional) ---
C_BLACK      = (6,   10,  18)
C_DARK       = (10,  16,  30)
C_DARK2      = (14,  22,  40)
C_PANEL      = (8,   14,  24)

# Emotional colors
C_RED        = (255, 42,  74)    # toxicity
C_BLUE       = (0,   180, 255)   # hope
C_GREEN      = (0,   255, 136)   # support
C_PURPLE     = (180, 78,  255)   # manipulation
C_YELLOW     = (255, 228, 74)    # investigation
C_ORANGE     = (255, 140, 0)     # warning
C_WHITE      = (220, 235, 255)
C_GREY       = (40,  60,  90)
C_GREY2      = (20,  32,  52)

# Node type colors
NODE_COLORS = {
    "victim":   C_BLUE,
    "bully":    C_RED,
    "follower": C_PURPLE,
    "ally":     C_GREEN,
    "observer": C_YELLOW,
    "bot":      (120, 0, 200),
    "origin":   C_RED,
    "neutral":  C_GREY,
}

# --- GRAPH PANEL ---
GRAPH_PANEL_H = 220
GAME_PANEL_Y  = GRAPH_PANEL_H
GAME_PANEL_H  = SCREEN_H - GRAPH_PANEL_H - 160
UI_PANEL_Y    = GAME_PANEL_Y + GAME_PANEL_H
UI_PANEL_H    = 160

# --- PLAYER ---
PLAYER_SPEED    = 4
PLAYER_RUN_MULT = 1.8
PLAYER_JUMP     = -14
GRAVITY         = 0.55
GROUND_Y        = GAME_PANEL_Y + GAME_PANEL_H - 50

# --- ALGORITHM SPEEDS ---
BFS_DELAY   = 0.45   # seconds per step
DFS_DELAY   = 0.40
DIJKSTRA_DELAY = 0.25
MST_DELAY   = 0.30
FF_DELAY    = 0.35

# --- MISSIONS ---
MISSION_NAMES = [
    "M1 – Rastros del Acoso",
    "M2 – Ruta Segura",
    "M3 – Reconstruir la Red",
    "M4 – Control del Impacto",
    "FINAL – Red Segura",
]

MISSION_ALGOS = [
    "BFS / DFS",
    "Dijkstra",
    "Kruskal",
    "Ford-Fulkerson",
    "Integración",
]
