# 🌐 NetGuardian

> Videojuego educativo cyberpunk sobre investigación de ciberacoso mediante algoritmos de grafos.
> Universidad del Norte · Estructura de Datos II · Laboratorio 2 · 2026

---

## 🎮 ¿Qué es NetGuardian?

NetGuardian es un **side-scrolling narrativo cyberpunk** donde el jugador investiga casos de ciberacoso
dentro de una red social digitalizada. Los NPCs representan nodos del grafo y las relaciones sociales
representan aristas. Los algoritmos de grafos se manifiestan como mecánicas naturales del gameplay.

---

## 📦 Requisitos

- Python **3.11.9**
- pygame **2.x**

```bash
pip install pygame
```

---

## 🚀 Cómo ejecutar

```bash
cd NetGuardian
python main.py
```

---

## 🕹️ Controles

| Tecla | Acción |
|-------|--------|
| `←` `→` / `A` `D` | Moverse |
| `↑` / `W` / `Space` | Saltar |
| `Shift` | Correr |
| `E` | Hablar con NPC cercano |
| `1` | Activar BFS |
| `2` | Activar DFS |
| `3` | Activar Dijkstra |
| `4` | Activar Kruskal |
| `5` | Activar Ford-Fulkerson |
| `M` | Avanzar misión (debug) |
| `Esc` | Menú principal |

---

## 📐 Arquitectura MVC

```
NetGuardian/
│
├── main.py                      ← Punto de entrada
│
├── model/                       ← MODELO (datos y lógica)
│   ├── constants.py             ← Constantes globales
│   ├── graph.py                 ← SocialGraph, Node, Edge
│   ├── algorithms.py            ← BFS, DFS, Dijkstra, Kruskal, Ford-Fulkerson
│   ├── player.py                ← Jugador
│   ├── npc.py                   ← NPCs (nodos físicos en el mundo)
│   ├── world.py                 ← Mundo side-scrolling, lluvia, partículas
│   └── emotions.py              ← Datos de misiones y emociones
│
├── view/                        ← VISTA (renderizado)
│   ├── graph_view.py            ← Panel del grafo vivo (superior)
│   ├── tilemap.py               ← Mundo side-scrolling (medio)
│   ├── ui.py                    ← Panel de UI (inferior)
│   ├── menus.py                 ← Menú principal y pantalla de victoria
│   └── effects.py               ← Glitch, scanlines, partículas, neon
│
├── controller/                  ← CONTROLADOR (lógica de juego)
│   ├── game.py                  ← Game loop principal
│   ├── state_manager.py         ← Estados: MENU / PLAYING / VICTORY
│   ├── mission_manager.py       ← Control de misiones y progreso
│   ├── dialogue_manager.py      ← Diálogos de NPCs y sistema
│   └── save_manager.py          ← Guardado y carga JSON
│
├── assets/                      ← Assets (imágenes, sonidos, fuentes)
│   ├── images/
│   ├── sounds/
│   ├── music/
│   └── fonts/
│
└── data/                        ← Datos del juego
    ├── dialogue.json
    ├── missions.json
    └── save.json                ← Generado automáticamente
```

---

## 🧠 Algoritmos implementados

### Misión 1 — BFS (Breadth-First Search)
- **Tecla:** `[1]`
- Explora la red por niveles (olas de expansión)
- Visualmente: nodos amarillos en cola, azules visitados
- Objetivo: encontrar el nodo origen del acoso

### Misión 1 — DFS (Depth-First Search)
- **Tecla:** `[2]`
- Sigue cadenas profundas de interacción
- Visualmente: descenso por ramas, conexiones iluminándose
- Objetivo: rastrear cadenas específicas de propagación

### Misión 2 — Dijkstra
- **Tecla:** `[3]`
- Calcula el camino de menor riesgo emocional hasta la víctima
- Visualmente: aristas con pesos, ruta verde = más segura
- Objetivo: ruta segura para llevar apoyo

### Misión 3 — Kruskal (MST)
- **Tecla:** `[4]`
- Reconstruye la red con el menor costo social
- Visualmente: aristas verdes aceptadas, ciclos rechazados
- Objetivo: árbol de expansión mínima = red restaurada

### Misión 4 — Ford-Fulkerson
- **Tecla:** `[5]`
- Calcula el flujo máximo de toxicidad entre origen y víctima
- Visualmente: flujo en rojo moviéndose por los canales
- Objetivo: controlar/limitar la propagación del acoso

---

## 🎨 Paleta emocional

| Color | Significado |
|-------|-------------|
| 🔴 Rojo | Toxicidad, acoso, nodo origen |
| 🔵 Azul | Esperanza, víctima, investigación |
| 🟢 Verde | Apoyo, aliados, conexiones restauradas |
| 🟣 Púrpura | Manipulación, bots, seguidores |
| 🟡 Amarillo | Investigación activa, nodos en cola |

---

## 👥 Tipos de NPC

| Tipo | Rol en la red |
|------|--------------|
| `victim` | Usuario que recibe el acoso |
| `origin` | Origen oculto del acoso |
| `bully` | Acosador activo |
| `follower` | Sigue y amplifica el acoso |
| `ally` | Aliado que ayuda a la víctima |
| `observer` | Testigo silencioso |
| `bot` | Bot que amplifica contenido tóxico |
| `neutral` | Usuario no involucrado |

---

## 💾 Sistema de guardado

El progreso se guarda automáticamente en `data/save.json` al completar la misión final.
Usa **"CONTINUAR"** en el menú para retomar desde donde quedaste.

---

## 🏆 Sistema de puntuación

| Acción | XP |
|--------|----|
| Hablar con NPC | +5 |
| Completar algoritmo | +25-35 |
| Encontrar origen | +80 |
| Completar misión | +50-150 |

---

## 👨‍💻 Desarrollado para

**Universidad del Norte**  
Departamento de Ingeniería de Sistemas y Computación  
Estructura de Datos II — Laboratorio 2
