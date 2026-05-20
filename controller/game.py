# controller/game.py
"""
Main game controller (MVC: Controller layer).
Fixes:
  - NPC XP spam: cooldown por NPC, máximo 1 XP por NPC por misión
  - Flujo guiado: siempre sabes qué hacer a continuación
  - Cinemática dramática al encontrar el origen
  - Post-algoritmo: instrucción clara de qué sigue
"""
import pygame
import sys
import math

from model.constants import (
    SCREEN_W, SCREEN_H, FPS, TITLE,
    C_BLACK, C_RED, C_BLUE, C_GREEN, C_YELLOW, C_PURPLE,
    BFS_DELAY, DFS_DELAY, DIJKSTRA_DELAY, MST_DELAY, FF_DELAY,
)
from model.graph       import SocialGraph
from model.player      import Player
from model.world       import GameWorld
from model.algorithms  import bfs, dfs, dijkstra, kruskal, ford_fulkerson

from view.graph_view   import GraphView
from view.tilemap      import WorldRenderer
from view.ui           import UIPanel
from view.menus        import MainMenu, VictoryScreen, SettingsScreen
from view.effects      import GlitchEffect, ScanlineEffect

from controller.state_manager    import StateManager, GameState
from controller.mission_manager  import MissionManager
from controller.dialogue_manager import DialogueManager
from controller.save_manager     import SaveManager


# ─── Instrucciones guiadas por misión y condición ────────────────────────────
GUIDED_STEPS = {
    0: {
        "start":    ("🔎 MISIÓN 1 — RASTROS DEL ACOSO",
                     "Mensajes de acoso se propagan. Camina con [A/D] y habla con NPCs [E] para reunir pistas. "
                     "Cuando estés listo, activa BFS [1] (expansión por niveles) o DFS [2] (cadenas profundas)."),
        "talked_3": ("💬 PISTAS SUFICIENTES — ¡HORA DE ACTUAR!",
                     "Has reunido pistas de varios usuarios. "
                     "Pulsa [1] BFS para rastrear por niveles o [2] DFS para seguir cadenas. "
                     "Observa cómo el algoritmo recorre el grafo arriba."),
        "algo_done":("⚠ ORIGEN IDENTIFICADO — MISIÓN 1 COMPLETA",
                     "¡El nodo origen fue expuesto! El grafo reveló la cadena completa de propagación. "
                     "Espera un momento... la red se prepara para la Misión 2."),
    },
    1: {
        "start":    ("🛡 MISIÓN 2 — RUTA SEGURA",
                     "El acoso continúa. La víctima necesita apoyo urgente. "
                     "Cada arista tiene un PESO (riesgo emocional). "
                     "Pulsa [3] para activar DIJKSTRA y encontrar el camino más seguro hasta la víctima."),
        "algo_done":("✅ RUTA MÍNIMA ENCONTRADA — MISIÓN 2 COMPLETA",
                     "¡Dijkstra calculó el camino de menor riesgo! La ruta verde es la más segura. "
                     "Misión 2 completa. Siguiente: reconstruir la red dañada con Kruskal."),
    },
    2: {
        "start":    ("💚 MISIÓN 3 — RECONSTRUIR LA RED",
                     "El acoso destruyó la confianza entre usuarios. Hay que reconstruir. "
                     "Pulsa [4] para activar KRUSKAL: conecta todos los nodos con el menor costo social posible "
                     "(Árbol de Expansión Mínima)."),
        "algo_done":("🌱 RED RECONSTRUIDA — MISIÓN 3 COMPLETA",
                     "¡MST calculado! Las aristas verdes forman la red óptima de menor costo. "
                     "Misión 3 completa. Última misión: controlar el flujo tóxico con Ford-Fulkerson."),
    },
    3: {
        "start":    ("🚫 MISIÓN 4 — CONTROL DEL IMPACTO",
                     "El contenido dañino satura la red. Debemos calcular cuánto puede propagarse. "
                     "Pulsa [5] para activar FORD-FULKERSON: calcula el flujo máximo de toxicidad "
                     "desde el origen hasta la víctima."),
        "algo_done":("🔒 FLUJO CONTROLADO — MISIÓN 4 COMPLETA",
                     "¡Flujo máximo calculado! Ahora sabemos la capacidad máxima de daño. "
                     "Todos los algoritmos aplicados. Preparando MISIÓN FINAL..."),
    },
    4: {
        "start":    ("🌐 MISIÓN FINAL — RED SEGURA",
                     "La red colapsa completamente. Debes aplicar TODOS los algoritmos en orden. "
                     "BFS [1] → Dijkstra [3] → Kruskal [4] → Ford-Fulkerson [5]. "
                     "¡El ecosistema social depende de ti!"),
        "algo_done":("🏆 RED RESTAURADA — ¡VICTORIA!",
                     "Todos los algoritmos aplicados correctamente. "
                     "El ciberacoso fue detenido. La red social es segura. ¡Misión cumplida!"),
    },
}


class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption(TITLE)
        self.screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))
        self.clock  = pygame.time.Clock()

        self.state_mgr   = StateManager()
        self.mission_mgr = MissionManager()
        self.save_mgr    = SaveManager()

        self.graph  = SocialGraph(n=12, seed=42)
        self.player = Player(x=200, y=400)
        self.world  = GameWorld(self.graph)

        self.graph_view = GraphView(self.screen, self.graph)
        self.world_rend = WorldRenderer(self.screen)
        self.ui         = UIPanel(self.screen)
        self.main_menu  = MainMenu(self.screen)
        self.settings   = SettingsScreen(self.screen)
        self.victory    = None

        self.glitch   = GlitchEffect(self.screen)
        self.scanline = ScanlineEffect(self.screen)
        self.dlg      = DialogueManager(self.ui)

        # Algorithm state
        self.algo_gen     = None
        self.algo_name    = ""
        self.algo_timer   = 0.0
        self.algo_delay   = BFS_DELAY
        self.algo_running = False
        self.origin_found = False

        # Input
        self.keys_held = {}

        # NPC anti-spam: talked_set = node_ids ya recompensados esta misión
        self.talked_set   = set()
        self.talked_count = 0
        # cooldown por NPC: node_id -> frames restantes
        self.npc_cooldown     = {}
        self.NPC_COOLDOWN_F   = 80   # ~1.3 s a 60fps

        # Cinematic state
        self.cinematic_active   = False
        self.cinematic_timer    = 0
        self.CINEMATIC_DURATION = 260
        self.cinematic_node     = None

        # Mission-advance timer (frames)
        self._advance_timer = 0

        self._show_step("start")

    # ── LOOP ──────────────────────────────────────────────────────────────────
    def run(self):
        while True:
            dt = self.clock.tick(FPS) / 1000.0
            self._handle_events()
            self._update(dt)
            self._draw()
            pygame.display.flip()

    # ── EVENTS ────────────────────────────────────────────────────────────────
    def _handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()

            if self.state_mgr.is_menu():
                r = self.main_menu.handle_event(event)
                if r == "NUEVA PARTIDA": self._new_game()
                elif r == "CONTINUAR":   self._load_game()
                elif r == "CONFIGURACION": self.state_mgr.transition(GameState.SETTINGS)
                elif r == "SALIR":       pygame.quit(); sys.exit()
                continue

            if self.state_mgr.is_settings():
                r = self.settings.handle_event(event)
                if r == "menu":
                    self.state_mgr.transition(GameState.MENU)
                continue

            if self.state_mgr.is_victory():
                r = self.victory.handle_event(event)
                if r == "menu": self.state_mgr.transition(GameState.MENU)
                continue

            if self.state_mgr.is_playing():
                if self.cinematic_active:
                    if event.type == pygame.KEYDOWN and event.key in (
                            pygame.K_RETURN, pygame.K_SPACE, pygame.K_e):
                        self._end_cinematic()
                    continue

                if event.type == pygame.KEYDOWN:
                    self.keys_held[event.key] = True
                    self._handle_keydown(event.key)
                if event.type == pygame.KEYUP:
                    self.keys_held[event.key] = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self._handle_click(event.pos)

    def _handle_keydown(self, key):
        if key == pygame.K_ESCAPE:
            self.state_mgr.transition(GameState.MENU)
        if key in (pygame.K_SPACE, pygame.K_UP, pygame.K_w):
            self.player.jump()
        if key == pygame.K_e:
            self._interact_with_npc()
        if key == pygame.K_1: self._start_algo("bfs")
        if key == pygame.K_2: self._start_algo("dfs")
        if key == pygame.K_3: self._start_algo("dijkstra")
        if key == pygame.K_4: self._start_algo("kruskal")
        if key == pygame.K_5: self._start_algo("ff")
        if key == pygame.K_m: self._advance_mission()  # debug skip

    def _handle_click(self, pos):
        btn = self.ui.get_button_at(pos)
        if btn: self._start_algo(btn)

    # ── UPDATE ────────────────────────────────────────────────────────────────
    def _update(self, dt):
        if self.state_mgr.is_menu():
            self.main_menu.update(); return
        if self.state_mgr.is_settings():
            self.settings.update(); return
        if self.state_mgr.is_victory():
            self.victory.update(); return

        # Cinematic freeze
        if self.cinematic_active:
            self.cinematic_timer += 1
            if self.cinematic_timer >= self.CINEMATIC_DURATION:
                self._end_cinematic()
            return

        # Mission advance timer (counts down after mission complete)
        if self._advance_timer > 0:
            self._advance_timer -= 1
            if self._advance_timer == 1:   # fire on 1→0 transition
                self._advance_mission()
                return

        # Player
        self.player.handle_input(self.keys_held)
        self.player.update(self.world.width)

        # World
        self.world.update(self.player)

        # Near NPC
        near = self.world.npc_near_player(self.player.x, threshold=70)
        self.player.near_npc = near.node_id if near else None

        # NPC cooldowns
        for k in list(self.npc_cooldown):
            self.npc_cooldown[k] -= 1
            if self.npc_cooldown[k] <= 0:
                del self.npc_cooldown[k]

        # Graph view
        self.graph_view.update(dt)

        # UI
        self.ui.update(self.graph, self.player, self.mission_mgr.current)
        self.ui.tick_popups()

        # Algorithm step
        if self.algo_running and self.algo_gen:
            self.algo_timer -= dt
            if self.algo_timer <= 0:
                self.algo_timer = self.algo_delay
                self._step_algo()

        # Prompt to run algo after talking to 3 unique NPCs in mission 0
        if (self.talked_count >= 3 and not self.algo_running
                and not self.origin_found
                and self.mission_mgr.current == 0
                and not self.ui.dlg_name.startswith("💬")):
            self._show_step("talked_3")

    # ── ALGORITHM STEPPING ────────────────────────────────────────────────────
    def _step_algo(self):
        try:
            event_type, payload = next(self.algo_gen)
            self._handle_algo_event(event_type, payload)
        except StopIteration:
            self.algo_running = False
            self.algo_gen     = None

    def _handle_algo_event(self, event_type, payload):
        g = self.graph
        if event_type == 'visit':
            node = g.nodes[payload]
            node.visited = True
            self.dlg.algo_step('visit', node=node)
            for e in g._adj[payload]:
                self.graph_view.spawn_particles(e, color=C_BLUE, count=2)
            for npc in self.world.npcs:
                if npc.node_id == payload:
                    npc.reveal()
                    self.world.spawn_particles(npc.x, 370, C_GREEN, count=8)
            if node.node_type == 'origin' and not self.origin_found:
                self.origin_found = True
                self._on_origin_found(payload)

        elif event_type == 'done':
            if isinstance(payload, int) and 0 <= payload < len(g.nodes):
                n = g.nodes[payload]
                if n.node_type == 'origin' and not self.origin_found:
                    self.origin_found = True
                    self._on_origin_found(payload)
            self.dlg.algo_step('done', value=payload)
            self._complete_algo()

        elif event_type == 'exhausted':
            self._complete_algo()

        elif event_type == 'queue':
            self.dlg.algo_step('queue', node=g.nodes[payload])

        elif event_type == 'edge':
            self.graph_view.spawn_particles(payload, color=C_YELLOW, count=1)

        elif event_type == 'relax':
            self.dlg.algo_step('relax', node=g.nodes[payload])

        elif event_type == 'path':
            if isinstance(payload, list):
                self.dlg.algo_step('path', value=payload)
                self._complete_algo()
            else:
                for (a, b) in payload:
                    e = g.edge_between(a, b) or g.edge_between(b, a)
                    if e:
                        self.graph_view.spawn_particles(e, color=C_RED, count=2)

        elif event_type == 'consider':
            payload.lit = 0.6

        elif event_type == 'accept':
            self.dlg.algo_step('accept', edge=payload)
            self.graph_view.spawn_particles(payload, color=C_GREEN, count=3)

        elif event_type == 'reject':
            self.dlg.algo_step('reject', edge=payload)

        elif event_type == 'augment':
            self.dlg.algo_step('augment', value=payload)

    # ── ORIGIN FOUND ──────────────────────────────────────────────────────────
    def _on_origin_found(self, node_id):
        node = self.graph.nodes[node_id]
        node.visited = True
        node.highlighted = True
        self.player.add_score(80)
        for npc in self.world.npcs:
            if npc.node_id == node_id:
                self.world.spawn_particles(npc.x, 360, C_RED, count=40, spread=8)
        self.glitch.trigger(duration=120, intensity=1.5)
        self.cinematic_active = True
        self.cinematic_timer  = 0
        self.cinematic_node   = node

    def _end_cinematic(self):
        self.cinematic_active = False
        self.cinematic_timer  = 0
        mid = self.mission_mgr.current
        if self._advance_timer == 0 and self.mission_mgr.is_mission_complete(mid):
            self.ui.set_dialogue(
                "✅ MISIÓN COMPLETA",
                f"¡Misión {mid + 1} completada! Cargando siguiente misión en 3 segundos..."
            )
            self._advance_timer = 180
        else:
            self._show_step("algo_done")

    # ── ALGO / MISSION COMPLETE ───────────────────────────────────────────────
    def _complete_algo(self):
        self.algo_running = False
        self.algo_gen     = None
        self.ui.btn_states[self.algo_name] = 'done'
        mid = self.mission_mgr.current
        self.mission_mgr.complete_algo(mid, self.algo_name)
        self.player.add_score(self.mission_mgr.reward(mid) // 2)

        if not self.cinematic_active:
            self._show_step("algo_done")

        # Only start advance timer if not already counting and mission is now complete
        if self._advance_timer == 0 and self.mission_mgr.is_mission_complete(mid):
            self.player.add_score(self.mission_mgr.reward(mid))
            self.glitch.trigger(40, 0.6)
            # Show big "mission complete" message then advance
            self.ui.set_dialogue(
                "✅ MISIÓN COMPLETA",
                f"¡Misión {mid + 1} completada! +{self.mission_mgr.reward(mid)} XP. "
                "Cargando siguiente misión en 3 segundos..."
            )
            self._advance_timer = 180   # 3 s at 60 fps

    def _advance_mission(self):
        advanced = self.mission_mgr.advance()
        if advanced:
            import random; random.seed(42 + self.mission_mgr.current)
            self.graph      = SocialGraph(n=12, seed=42 + self.mission_mgr.current)
            self.world      = GameWorld(self.graph)
            self.graph_view = GraphView(self.screen, self.graph)
            self.ui.btn_states = {}
            self.talked_set    = set()
            self.talked_count  = 0
            self.npc_cooldown  = {}
            self.origin_found  = False
            self._show_step("start")
        else:
            self._trigger_victory()

    def _trigger_victory(self):
        self.save_mgr.save(self.player, self.mission_mgr)
        self.state_mgr.transition(GameState.VICTORY)
        self.victory = VictoryScreen(self.screen, self.player.score)

    # ── ALGO STARTERS ─────────────────────────────────────────────────────────
    def _start_algo(self, algo_id):
        if self.algo_running:
            self.ui.set_dialogue("⚠ ESPERA",
                "Un algoritmo ya está ejecutándose. Observa el grafo arriba y espera a que termine.")
            return
        self.graph.reset_algo_state()
        self.origin_found = False
        self.algo_name    = algo_id
        self.algo_running = True
        # Keep 'done' states, reset others
        self.ui.btn_states = {k: ('done' if v == 'done' else 'normal')
                              for k, v in self.ui.btn_states.items()}
        self.ui.btn_states[algo_id] = 'active'
        g = self.graph

        if algo_id == "bfs":
            self.algo_gen   = bfs(g, start=0)
            self.algo_delay = BFS_DELAY
            self.ui.set_dialogue("⚡ BFS ACTIVO",
                "Expansión por NIVELES: primero visita vecinos directos, "
                "luego los vecinos de vecinos. Observa las 'olas' azules en el grafo. "
                "El algoritmo se detiene al encontrar el ORIGEN (nodo rojo).")
        elif algo_id == "dfs":
            self.algo_gen   = dfs(g, start=0)
            self.algo_delay = DFS_DELAY
            self.ui.set_dialogue("🔍 DFS ACTIVO",
                "Descenso en PROFUNDIDAD: sigue una cadena hasta el fondo "
                "antes de retroceder. Ideal para rastrear relaciones directas. "
                "Observa cómo el algoritmo 'bucea' por ramas del grafo.")
        elif algo_id == "dijkstra":
            self.algo_gen   = dijkstra(g, src=0, dst=g.victim_id)
            self.algo_delay = DIJKSTRA_DELAY
            self.ui.set_dialogue("🛡 DIJKSTRA ACTIVO",
                "Buscando el CAMINO MÁS SEGURO hasta la víctima (nodo azul). "
                "Los números en las aristas son el riesgo emocional. "
                "La ruta verde final minimiza el daño total del recorrido.")
        elif algo_id == "kruskal":
            self.algo_gen   = kruskal(g)
            self.algo_delay = MST_DELAY
            self.ui.set_dialogue("💚 KRUSKAL ACTIVO",
                "Construyendo el ÁRBOL DE EXPANSIÓN MÍNIMA. "
                "Ordena aristas por costo y acepta las más baratas sin crear ciclos. "
                "Verde = aceptada al MST. Rojo = rechazada por crear ciclo.")
        elif algo_id == "ff":
            self.algo_gen   = ford_fulkerson(g, source=g.origin_id, sink=g.victim_id)
            self.algo_delay = FF_DELAY
            self.ui.set_dialogue("🚫 FORD-FULKERSON ACTIVO",
                "Calculando el FLUJO MÁXIMO de toxicidad del origen a la víctima. "
                "Encuentra rutas aumentantes repetidamente hasta saturar los canales. "
                "El resultado = cuánto daño máximo puede propagarse.")
        self.algo_timer = 0.0

    # ── NPC INTERACTION (con anti-spam) ───────────────────────────────────────
    def _interact_with_npc(self):
        near = self.world.npc_near_player(self.player.x, threshold=70)
        if not near:
            return
        nid = near.node_id

        # Cooldown activo → ignorar silenciosamente
        if nid in self.npc_cooldown:
            return

        # Activar cooldown
        self.npc_cooldown[nid] = self.NPC_COOLDOWN_F

        # Mostrar diálogo
        self.dlg.npc_say(near)
        near.talked_to = True
        self.world.spawn_particles(near.x, 360, C_BLUE, count=6)

        # XP solo si es la primera vez con este NPC esta misión
        if nid not in self.talked_set:
            self.talked_set.add(nid)
            self.talked_count += 1
            self.player.add_score(5)
            self.ui.show_xp_popup("+5 XP", near.x - self.world.cam_x, 355)

    # ── GUIDED STEP ───────────────────────────────────────────────────────────
    def _show_step(self, condition_key):
        mid   = self.mission_mgr.current
        steps = GUIDED_STEPS.get(mid, {})
        if condition_key in steps:
            title, body = steps[condition_key]
            self.ui.set_dialogue(title, body)
        else:
            self.ui.set_dialogue("SISTEMA",
                "Explora con [A/D], habla con NPCs [E], activa algoritmos con [1-5].")

    # ── NEW / LOAD ─────────────────────────────────────────────────────────────
    def _new_game(self):
        self.graph   = SocialGraph(n=12, seed=42)
        self.player  = Player(x=200, y=400)
        self.world   = GameWorld(self.graph)
        self.graph_view    = GraphView(self.screen, self.graph)
        self.mission_mgr   = MissionManager()
        self.ui.btn_states = {}
        self.talked_set    = set()
        self.talked_count  = 0
        self.npc_cooldown  = {}
        self.origin_found  = False
        self._advance_timer= 0
        self._show_step("start")
        self.state_mgr.transition(GameState.PLAYING)

    def _load_game(self):
        data = self.save_mgr.load()
        if data:
            self.player.score = data.get("score", 0)
            self.mission_mgr.current   = data.get("mission", 0)
            self.mission_mgr.completed = set(data.get("completed", []))
            self.graph = SocialGraph(n=12, seed=42 + self.mission_mgr.current)
            self.world = GameWorld(self.graph)
            self.graph_view = GraphView(self.screen, self.graph)
        self._show_step("start")
        self.state_mgr.transition(GameState.PLAYING)

    # ── DRAW ──────────────────────────────────────────────────────────────────
    def _draw(self):
        self.screen.fill(C_BLACK)

        if self.state_mgr.is_menu():
            self.main_menu.draw(); return
        if self.state_mgr.is_settings():
            self.settings.draw(); return
        if self.state_mgr.is_victory():
            self.victory.draw(); return

        self.graph_view.draw(
            mission=self.mission_mgr.current,
            algo_label=self.algo_name.upper() if self.algo_name else "—"
        )
        pygame.draw.line(self.screen, (20, 40, 80), (0, 220), (SCREEN_W, 220), 2)

        near = self.world.npc_near_player(self.player.x, threshold=70)
        self.world_rend.draw(self.world, self.player, near_npc=near)

        self.ui.draw(
            algo_label=self.algo_name.upper() if self.algo_name else "—",
            algo_callbacks={}
        )

        self.glitch.update_draw()

        if self.cinematic_active:
            self._draw_cinematic()

        self.scanline.draw(self.screen)
        self._draw_top_hud()
        self.ui.draw_xp_popups(self.screen)

    # ── CINEMATIC ─────────────────────────────────────────────────────────────
    def _draw_cinematic(self):
        s = self.screen
        t = self.cinematic_timer

        font_xl = pygame.font.SysFont("consolas", 34, bold=True)
        font_lg = pygame.font.SysFont("consolas", 17, bold=True)
        font_md = pygame.font.SysFont("consolas", 13)

        # Phase 1 (0-35): fade to black
        if t < 35:
            alpha = int(t / 35 * 230)
            ov = pygame.Surface((SCREEN_W, SCREEN_H), pygame.SRCALPHA)
            ov.fill((0, 0, 0, alpha))
            s.blit(ov, (0, 0))
            return

        # Dark background
        ov = pygame.Surface((SCREEN_W, SCREEN_H), pygame.SRCALPHA)
        ov.fill((0, 0, 0, 215))
        s.blit(ov, (0, 0))

        # Phase 2 (35-70): glitch lines
        if t < 70:
            import random
            for _ in range(int((t - 35) / 1.5)):
                y  = random.randint(0, SCREEN_H)
                hh = random.randint(2, 14)
                bar = pygame.Surface((SCREEN_W, hh), pygame.SRCALPHA)
                bar.fill((random.randint(180, 255), 0, 0, 55))
                s.blit(bar, (0, y))

        # Pulsing red glow
        pulse = 0.55 + 0.45 * math.sin(t * 0.14)
        glow = pygame.Surface((900, 140), pygame.SRCALPHA)
        glow.fill((int(255 * pulse), 0, 0, 28))
        s.blit(glow, (SCREEN_W // 2 - 450, SCREEN_H // 2 - 70))

        # Main title (fade in after phase 2)
        if t >= 55:
            title_a = min(255, (t - 55) * 9)
            title_s = font_xl.render("⚠  ORIGEN DEL ACOSO IDENTIFICADO  ⚠", True, C_RED)
            ta = title_s.copy()
            ta.set_alpha(title_a)
            s.blit(ta, (SCREEN_W // 2 - ta.get_width() // 2, SCREEN_H // 2 - 75))

        # Node info
        if t >= 90 and self.cinematic_node:
            node = self.cinematic_node
            name_s = font_lg.render(
                f"NODO: {node.name}   TIPO: {node.node_type.upper()}   ID: {node.id}",
                True, C_YELLOW)
            s.blit(name_s, (SCREEN_W // 2 - name_s.get_width() // 2, SCREEN_H // 2 - 22))

        # Explanation lines
        if t >= 120:
            lines = [
                ("El algoritmo trazó TODAS las rutas de propagación", C_GREEN),
                ("y encontró el nodo que inició el ciberacoso.", C_GREEN),
                ("", C_BLACK),
                ("Cada nodo visitado representa un usuario afectado.", (100, 150, 200)),
                ("La red reveló la estructura oculta del acoso.", (100, 150, 200)),
                ("", C_BLACK),
                ("[SPACE] o [ENTER] para continuar", (60, 100, 160)),
            ]
            for i, (ln, col) in enumerate(lines):
                ls = font_md.render(ln, True, col)
                s.blit(ls, (SCREEN_W // 2 - ls.get_width() // 2, SCREEN_H // 2 + 16 + i * 17))

        # Progress bar
        bar_w = int(SCREEN_W * min(1.0, t / self.CINEMATIC_DURATION))
        pygame.draw.rect(s, (35, 0, 0),  (0, SCREEN_H - 5, SCREEN_W, 5))
        pygame.draw.rect(s, C_RED,       (0, SCREEN_H - 5, bar_w, 5))
        hint_s = pygame.font.SysFont("consolas", 9).render(
            "Espera o presiona SPACE/ENTER", True, (40, 20, 20))
        s.blit(hint_s, (SCREEN_W - hint_s.get_width() - 8, SCREEN_H - 16))

    # ── TOP HUD ───────────────────────────────────────────────────────────────
    def _draw_top_hud(self):
        s    = self.screen
        font = pygame.font.SysFont("consolas", 11, bold=True)
        from model.constants import MISSION_NAMES
        tab_w = (SCREEN_W - 110) // len(MISSION_NAMES)
        for i, name in enumerate(MISSION_NAMES):
            tx   = i * tab_w
            cur  = (i == self.mission_mgr.current)
            done = (i in self.mission_mgr.completed)
            bg   = (8, 20, 42) if cur else (4, 10, 20)
            bc   = C_BLUE if cur else (C_GREEN if done else (15, 30, 55))
            pygame.draw.rect(s, bg, (tx, 0, tab_w - 2, 16))
            pygame.draw.rect(s, bc, (tx, 0, tab_w - 2, 16), 1)
            label = ("✓ " if done else "") + name[:18]
            col   = C_YELLOW if cur else (C_GREEN if done else (30, 55, 90))
            s.blit(font.render(label, True, col), (tx + 4, 2))

        # Score
        sc = font.render(f"XP: {self.player.score}", True, C_GREEN)
        s.blit(sc, (SCREEN_W - sc.get_width() - 8, 2))

        # Algo running indicator (pulsing)
        if self.algo_running:
            pulse = int(180 + 75 * math.sin(pygame.time.get_ticks() * 0.008))
            ind = font.render(f"▶ {self.algo_name.upper()} EJECUTANDO...", True, (pulse, pulse, 0))
            s.blit(ind, (SCREEN_W // 2 - ind.get_width() // 2, 2))
