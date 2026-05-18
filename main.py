# main.py
"""
NetGuardian — Videojuego educativo de ciberacoso y algoritmos de grafos
Universidad del Norte · Estructura de Datos II · 2026

Ejecutar:  python main.py
Requiere:  pip install pygame
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from controller.game import Game


if __name__ == "__main__":
    game = Game()
    game.run()
