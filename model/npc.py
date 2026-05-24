import random
import math


class NPC:
    """
    NPC = a node in the social graph made physical in the game world.
    Each NPC patrols the level and can be talked to by the player.
    """

    DIALOGUE = {
        "victim": [
            "Un usuario llamado bot719 me ha enviado 27 mensajes en las últimas dos semanas. Todos dicen lo mismo.",
            "Empezó con un comentario en mi publicación. Ahora son cinco cuentas distintas coordinadas contra mí.",
            "Bloqueé a @xX_darknode_Xx, pero creó una cuenta nueva al día siguiente. ¿Cómo detengo esto?",
            "Capturé las pantallas. Son 14 páginas de mensajes. ¿Eso es suficiente evidencia para ti?",
            "Lo peor no es lo que me dicen. Es que nadie en la red dijo nada. Solo miraron.",
            "Mi nivel de señal cayó a rojo hace tres días. Desde que empezaron los mensajes, nadie me contacta ya.",
        ],
        "bully": [
            "Ese mensaje lo envié hace meses. Ya ni lo recuerdo. No es para tanto.",
            "Éramos cuatro en el grupo. Yo solo reenvié lo que los demás escribieron primero.",
            "No tienes pruebas de que fui yo. Cualquiera pudo usar ese nodo.",
            "¿Acoso? Solo era un juego. La víctima debería aprender a ignorarlo.",
            "Mira, si me delatas, tú también quedas fuera de la red. Piénsalo bien.",
            "El grupo se llamaba 'Operación Silencio'. Yo era el de menor rango. Hay alguien más arriba.",
        ],
        "follower": [
            "Vi la publicación en mi feed y le di compartir sin leer bien. Cuando me di cuenta, ya tenía 80 reenvíos.",
            "Me dijeron que era una broma entre amigos. No sabía que la víctima era real y estaba leyendo todo.",
            "Compartí el meme tres veces en 48 horas. Después vi quién era el objetivo y lo borré, pero ya era tarde.",
            "El nodo central me etiquetó y sentí presión social. Si no participaba, me expulsaban del grupo.",
            "Fui manipulado. Me mostraron solo parte de la conversación. El contexto era completamente diferente.",
            "Borré mis reenvíos pero el daño ya estaba hecho. ¿Eso me hace culpable igual?",
        ],
        "ally": [
            "Detecté un patrón: los mensajes de acoso llegan siempre entre las 10 p.m. y la 1 a.m. Hay coordinación.",
            "Tres nodos distintos usaron exactamente la misma frase. Eso no es coincidencia, es una campaña organizada.",
            "La víctima necesita que alguien valide sus capturas. Sin eso, el sistema descarta la denuncia.",
            "He mapeado 11 conexiones entre el bully y los followers. El grafo no miente: hay una jerarquía.",
            "Si usas BFS desde la víctima, llegarás al nodo origen en cuatro saltos. Lo calculé anoche.",
            "Puedo ser testigo digital. Guardo logs de todo. Pero necesito que tú hagas el primer movimiento.",
        ],
        "observer": [
            "Vi el primer mensaje hace tres semanas. Pensé que se resolvería solo. Me equivoqué.",
            "Estaba en el grupo cuando empezó todo. Leí cada mensaje y no escribí nada. Eso me pesa.",
            "Sé quién inició esto, pero tengo miedo de que me excluyan si hablo. ¿Eso me hace cómplice?",
            "El hilo original tiene 340 respuestas. Guardé los primeros 20 antes de que los borraran.",
            "Vi cómo la víctima intentó defenderse dos veces. El grupo la silenciaron en segundos.",
            "No actué. Pero puedo darte acceso a los logs que conservo. Quizás eso sirva de algo ahora.",
        ],
        "bot": [
            "IDENTIFICADO: nodo_investigador. ALERTA enviada a: 3 destinatarios.",
            "TAREA EN CURSO: reenviar_mensaje[id=4471] a 12 nodos activos. Progreso: 67%.",
            "ERROR: memoria_emocional no encontrada. Ejecutando respuesta_simulada...",
            "CICLO DETECTADO: el investigador ha trazado mi ruta. Iniciando protocolo de evasión.",
            "Soy el nodo 6 de 9. Los otros ocho siguen activos. No me desactives solo a mí.",
            "No tengo motivaciones propias. Alguien me programó. Busca al operador, no a la máquina.",
        ],
        "origin": [
            "Pensé que nadie llegaría hasta aquí. ¿Cómo rastreaste el grafo completo?",
            "Empezó como una discusión. Un mensaje. No esperaba que se propagara a 40 nodos en tres días.",
            "Fui yo. Lo sé. He visto cómo cada reenvío llegó más lejos de lo que quise.",
            "¿Quieres saber por qué? Porque nadie me escuchó a mí primero. Eso no lo justifica. Lo sé.",
            "Sí, creé los bots. Sí, coordine el grupo. Pero cuando vi el daño real, no supe cómo detenerlo.",
            "Si me denuncias, entiendo. Solo quiero que sepas que... ya no soy la misma persona que lo hizo.",
        ],
        "neutral": [
            "He notado que tres nodos de mi red desaparecieron esta semana sin explicación.",
            "Alguien me pidió que me uniera a un grupo privado. Lo rechacé. Ahora me siento excluido de todo.",
            "Escuché que hay una campaña organizada en algún nodo profundo. No sé los detalles.",
            "Mi algoritmo de feed me muestra contenido cada vez más agresivo. ¿Eso es normal?",
            "Una cuenta nueva me envió una solicitud de conexión. El perfil parece falso. ¿La acepto?",
            "No me involucro en conflictos de red, pero últimamente es difícil ignorar lo que está pasando.",
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