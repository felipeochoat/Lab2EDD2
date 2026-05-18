# model/npc.py
import random
import math


class NPC:
    """
    NPC = a node in the social graph made physical in the game world.
    Each NPC patrols the level and can be talked to by the player.
    """

    DIALOGUE = {
        "victim": [
            "Recibo mensajes crueles todos los días...",
            "No sé quién está detrás de todo esto.",
            "Gracias por intentar ayudar.",
            "El acoso se propagó muy rápido en la red.",
        ],
        "bully": [
            "No sé de qué hablas.",
            "Todos lo hacen, yo solo sigo la corriente.",
            "Déjame en paz, investigador.",
        ],
        "follower": [
            "Solo compartí lo que vi en mi feed...",
            "No sabía que hacía daño.",
            "Creo que empezó en el nodo central.",
        ],
        "ally": [
            "Estoy aquí para ayudar a quien lo necesite.",
            "He visto el acoso propagarse. Hay un patrón.",
            "Juntos podemos reconstruir la red.",
        ],
        "observer": [
            "Vi todo pero no dije nada. Lo lamento.",
            "El origen está más profundo en la red.",
            "Hay conexiones que no son obvias.",
        ],
        "bot": [
            "ERROR: respuesta_no_definida",
            "PROPAGANDO: contenido_toxico...",
            "No soy lo que parezco.",
        ],
        "origin": [
            "... (silencio)",
            "¿Cómo llegaste hasta aquí?",
            "Fui yo. Lo siento.",
        ],
        "neutral": [
            "¿Qué está pasando en la red?",
            "He notado cosas extrañas últimamente.",
            "Espero que puedas resolverlo.",
        ],
    }

    def __init__(self, node_id, name, world_x, node_type="neutral"):
        self.node_id   = node_id
        self.name      = name
        self.node_type = node_type

        self.x         = float(world_x)
        self.patrol_min= world_x - 80
        self.patrol_max= world_x + 80
        self.vx        = random.choice([-0.5, 0.5])
        self.facing    = 1 if self.vx > 0 else -1

        self.talked_to  = False
        self.revealed   = False   # True after visited by algorithm
        self.emotion    = "neutral"

        # Visual
        self.anim_frame = 0
        self.anim_timer = 0
        self.bob        = random.uniform(0, math.pi * 2)

    def update(self, dt=1):
        self.x += self.vx
        if self.x <= self.patrol_min or self.x >= self.patrol_max:
            self.vx *= -1
            self.facing = 1 if self.vx > 0 else -1

        self.anim_timer += 1
        if self.anim_timer >= 10:
            self.anim_frame = (self.anim_frame + 1) % 4
            self.anim_timer = 0

        self.bob += 0.05

    def get_dialogue(self):
        lines = self.DIALOGUE.get(self.node_type, self.DIALOGUE["neutral"])
        return random.choice(lines)

    def distance_to_player(self, player_x, player_y):
        return math.hypot(self.x - player_x, 0)

    def reveal(self):
        self.revealed = True

    def __repr__(self):
        return f"NPC({self.node_id}, {self.name}, {self.node_type})"
