# model/emotions.py

EMOTION_COLORS = {
    "happy":   (0,   255, 136),
    "sad":     (0,   180, 255),
    "angry":   (255, 42,  74),
    "scared":  (255, 228, 74),
    "neutral": (80,  110, 160),
}

EMOTION_ICONS = {
    "happy":   "◕",
    "sad":     "◔",
    "angry":   "◉",
    "scared":  "◎",
    "neutral": "○",
}


# model/quests.py (embedded here for simplicity)
MISSIONS = [
    {
        "id": 0,
        "name": "Rastros del Acoso",
        "algo": "BFS / DFS",
        "story": (
            "Mensajes de odio se propagan en la red. "
            "Investiga a los usuarios con BFS (por niveles) o DFS (en profundidad) "
            "para encontrar el nodo ORIGEN del acoso."
        ),
        "goal": "Encontrar el nodo origen.",
        "hint": "Habla con NPCs y activa BFS o DFS desde el panel inferior.",
        "reward": 50,
        "xp_required": 30,
    },
    {
        "id": 1,
        "name": "Ruta Segura",
        "algo": "Dijkstra",
        "story": (
            "El acoso fue identificado. Ahora debes llevar apoyo emocional "
            "a la víctima por el camino de menor riesgo. "
            "Cada arista tiene un peso (riesgo emocional)."
        ),
        "goal": "Encontrar el camino más seguro hasta la víctima.",
        "hint": "Activa DIJKSTRA desde el panel. La ruta verde es la más segura.",
        "reward": 60,
        "xp_required": 40,
    },
    {
        "id": 2,
        "name": "Reconstruir la Red",
        "algo": "Kruskal (MST)",
        "story": (
            "El acoso destruyó la confianza. "
            "Usa Kruskal para reconstruir las conexiones positivas "
            "con el menor costo social posible."
        ),
        "goal": "Crear el árbol de expansión mínima de la red.",
        "hint": "Activa KRUSKAL. Las aristas verdes son las seleccionadas.",
        "reward": 60,
        "xp_required": 40,
    },
    {
        "id": 3,
        "name": "Control del Impacto",
        "algo": "Ford-Fulkerson",
        "story": (
            "El contenido dañino intenta saturar la red. "
            "Calcula el flujo máximo de toxicidad para saber qué cortar. "
            "Fuente: nodo origen. Destino: víctima."
        ),
        "goal": "Calcular el flujo máximo y controlar la propagación.",
        "hint": "Activa FORD-FULKERSON. Las aristas rojas muestran el flujo tóxico.",
        "reward": 70,
        "xp_required": 50,
    },
    {
        "id": 4,
        "name": "Red Segura — Misión Final",
        "algo": "BFS + Dijkstra + Kruskal + Ford-Fulkerson",
        "story": (
            "La red completa está colapsando. "
            "Aplica todos los algoritmos aprendidos para restaurar el ecosistema social. "
            "¡El tiempo corre!"
        ),
        "goal": "Completar los 4 algoritmos y restaurar la red.",
        "hint": "Ejecuta los 4 algoritmos en orden. ¡Cada uno desbloquea el siguiente!",
        "reward": 150,
        "xp_required": 0,
    },
]
