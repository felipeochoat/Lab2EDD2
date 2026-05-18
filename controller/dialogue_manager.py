# controller/dialogue_manager.py
"""
Manages NPC dialogues and system messages shown in the UI panel.
"""


class DialogueManager:

    SYSTEM_MSGS = {
        "intro":    ("SISTEMA", "Bienvenido a NetGuardian. Los mensajes de acoso se propagan. Investiga la red."),
        "bfs_start":("SISTEMA [BFS]", "BFS activo: expansión por niveles. Rastreando propagación del acoso..."),
        "dfs_start":("SISTEMA [DFS]", "DFS activo: siguiendo cadenas profundas de interacción..."),
        "dijkstra_start":("SISTEMA [DIJKSTRA]", "Calculando ruta de menor riesgo hacia la víctima..."),
        "kruskal_start": ("SISTEMA [KRUSKAL]", "Reconstruyendo la red con el menor costo social posible..."),
        "ff_start":      ("SISTEMA [FORD-FULKERSON]", "Calculando flujo máximo de toxicidad. Define fuente y destino..."),
        "origin_found":  ("⚠ ALERTA CRÍTICA", "¡ORIGEN DEL ACOSO IDENTIFICADO! El nodo fuente ha sido expuesto."),
        "path_found":    ("SISTEMA [DIJKSTRA]", "Ruta segura calculada. Camino verde = menor riesgo emocional."),
        "mst_done":      ("SISTEMA [KRUSKAL]", "Red reconstruida con costo mínimo. La confianza se restaura."),
        "ff_done":       ("SISTEMA [F-F]", "Flujo máximo calculado. Canales de acoso identificados y limitados."),
        "mission_complete":("✅ MISIÓN COMPLETA", "Objetivo cumplido. Avanzando a la siguiente misión..."),
        "final_done":    ("🌐 RED RESTAURADA", "Todos los algoritmos aplicados. ¡La red social es segura!"),
    }

    def __init__(self, ui_panel):
        self.ui   = ui_panel
        self.queue= []   # list of (name, text, choices)

    def say(self, key, choices=None):
        """Show a system/predefined message."""
        name, text = self.SYSTEM_MSGS.get(key, ("SISTEMA", key))
        self.ui.set_dialogue(name, text, choices)

    def npc_say(self, npc):
        """Show an NPC's dialogue line."""
        line = npc.get_dialogue()
        name = npc.name
        self.ui.set_dialogue(name, line)

    def algo_step(self, event_type, node=None, edge=None, value=None):
        """Called each algorithm step to narrate what's happening."""
        if event_type == 'visit' and node:
            ntype = node.node_type
            msgs = {
                'victim':   f"💙 {node.name}: VÍCTIMA encontrada.",
                'bully':    f"⚠ {node.name}: conducta agresiva detectada.",
                'follower': f"△ {node.name}: seguidor del acosador.",
                'ally':     f"✓ {node.name}: aliado identificado.",
                'observer': f"○ {node.name}: testigo silencioso.",
                'bot':      f"🤖 {node.name}: BOT tóxico detectado.",
                'origin':   f"🔴 {node.name}: ¡NODO ORIGEN ENCONTRADO!",
                'neutral':  f"· {node.name}: usuario neutral.",
            }
            text = msgs.get(ntype, f"· Visitando {node.name}...")
            self.ui.set_dialogue("ALGORITMO", text)

        elif event_type == 'queue' and node:
            self.ui.set_dialogue("BFS COLA", f"Encolando nodo {node.name} para revisión...")

        elif event_type == 'relax' and node:
            self.ui.set_dialogue("DIJKSTRA", f"Relajando arista → {node.name}  d={node.dist}")

        elif event_type == 'accept' and edge:
            self.ui.set_dialogue("KRUSKAL", f"✓ Arista ({edge.a}↔{edge.b}) aceptada al MST. Peso={edge.weight}")

        elif event_type == 'reject' and edge:
            self.ui.set_dialogue("KRUSKAL", f"✗ Arista ({edge.a}↔{edge.b}) rechazada (formaría ciclo).")

        elif event_type == 'augment' and value is not None:
            self.ui.set_dialogue("FORD-FULKERSON", f"Ruta aumentante encontrada. Flujo += {value}")

        elif event_type == 'path' and value:
            self.ui.set_dialogue("DIJKSTRA", f"Camino mínimo reconstruido: {' → '.join(str(v) for v in value)}")

        elif event_type == 'done':
            self.ui.set_dialogue("SISTEMA", f"Algoritmo completado. Resultado: {value}")
