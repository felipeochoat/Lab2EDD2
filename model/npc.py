# model/npc.py
import random
import math


class NPC:
    """
    NPC = nodo del grafo social hecho personaje.
    Rastrea historial de diálogo para detectar cuándo se agota el banco
    y desencadenar el minijuego si corresponde.
    """

    DIALOGUE = {
        "victim": [
            "Un usuario llamado bot719 me ha enviado 27 mensajes en las últimas dos semanas. Todos dicen lo mismo.",
            "Empezó con un comentario en mi publicación. Ahora son cinco cuentas distintas coordinadas contra mí.",
            "Bloqueé a @xX_darknode_Xx, pero creó una cuenta nueva al día siguiente. ¿Cómo detengo esto?",
            "Capturé las pantallas. Son 14 páginas de mensajes. ¿Eso es suficiente evidencia para ti?",
            "Lo peor no es lo que me dicen. Es que nadie en la red dijo nada. Solo miraron.",
            "Mi nivel de señal cayó a rojo hace tres días. Desde que empezaron los mensajes, nadie me contacta ya.",
            "Mis padres no saben lo que está pasando. Tengo miedo de que lo descubran por las redes.",
            "Intenté hacer una publicación explicando la situación pero la llenaron de comentarios falsos.",
            "El agresor tiene más de 400 seguidores. Cuando habla, todos le creen a él.",
            "Me dijeron que si denunciaba, lo empeoraría. No sé si hacerle caso a eso.",
            "He borrado tres de mis cuentas pero el acoso me sigue a cada perfil nuevo que creo.",
            "No puedo dormir bien desde hace semanas. Cada notificación me da miedo.",
        ],
        "bully": [
            "Ese mensaje lo envié hace meses. Ya ni lo recuerdo. No es para tanto.",
            "Éramos cuatro en el grupo. Yo solo reenvié lo que los demás escribieron primero.",
            "No tienes pruebas de que fui yo. Cualquiera pudo usar ese nodo.",
            "¿Acoso? Solo era un juego. La víctima debería aprender a ignorarlo.",
            "Mira, si me delatas, tú también quedas fuera de la red. Piénsalo bien.",
            "El grupo se llamaba 'Operación Silencio'. Yo era el de menor rango. Hay alguien más arriba.",
            "Todos en el colegio hacen lo mismo. Yo no fui el único. ¿Por qué solo me preguntas a mí?",
            "Borré mis mensajes. No hay evidencia. Puedes seguir buscando, no vas a encontrar nada.",
            "No pretendía hacerle daño. Solo quería que se alejara del grupo.",
            "Ese apodo que le pusimos era una broma. Todo el mundo se reía menos ella.",
            "Mi cuenta fue hackeada. Esos mensajes los envió otra persona, no yo.",
            "Sí, participé. Pero hay uno que inició todo. Yo solo seguí la corriente.",
        ],
        "follower": [
            "Vi la publicación en mi feed y le di compartir sin leer bien. Cuando me di cuenta ya tenía 80 reenvíos.",
            "Me dijeron que era una broma entre amigos. No sabía que la víctima era real y estaba leyendo todo.",
            "Compartí el meme tres veces en 48 horas. Después vi quién era el objetivo y lo borré, pero ya era tarde.",
            "El nodo central me etiquetó y sentí presión social. Si no participaba, me expulsaban del grupo.",
            "Fui manipulado. Me mostraron solo parte de la conversación. El contexto era completamente diferente.",
            "Borré mis reenvíos pero el daño ya estaba hecho. ¿Eso me hace culpable igual?",
            "Pensé que era contenido público. No entendí que estaba ayudando a difamar a alguien.",
            "Me amenazaron con publicar mis secretos si no participaba. No tuve opción.",
            "Solo le di like a la publicación. No la compartí. ¿Eso también cuenta como acoso?",
            "Cuando me di cuenta del daño, intenté contactar a la víctima para disculparme. No me respondió.",
            "El grupo tenía 200 personas. Yo era una más. Mi participación fue mínima comparada con otros.",
            "Ya borré mi cuenta de esa red. No quiero saber más de eso.",
        ],
        "ally": [
            "Detecté un patrón: los mensajes de acoso llegan siempre entre las 10 p.m. y la 1 a.m. Hay coordinación.",
            "Tres nodos distintos usaron exactamente la misma frase. Eso no es coincidencia, es una campaña organizada.",
            "La víctima necesita que alguien valide sus capturas. Sin eso, el sistema descarta la denuncia.",
            "He mapeado 11 conexiones entre el bully y los followers. El grafo no miente: hay una jerarquía.",
            "Si usas BFS desde la víctima, llegarás al nodo origen en cuatro saltos. Lo calculé anoche.",
            "Puedo ser testigo digital. Guardo logs de todo. Pero necesito que tú hagas el primer movimiento.",
            "El nodo origen tiene un patrón de actividad muy específico: siempre inicia sesión desde la misma IP.",
            "Analicé los metadatos de las imágenes publicadas. Todas tienen la misma cámara de origen.",
            "He visto este tipo de campaña antes. Se llama 'ataque de enjambre coordinado'. Hay un manual.",
            "Si cruzas los horarios con la lista de sospechosos, el círculo se reduce a tres personas.",
            "La víctima tiene capturas de todo. El problema es la cadena de custodia digital. ¿Sabes cómo validarla?",
            "Tengo el historial completo del servidor. Puedo extraer los logs si me das autorización legal.",
        ],
        "observer": [
            "Vi el primer mensaje hace tres semanas. Pensé que se resolvería solo. Me equivoqué.",
            "Estaba en el grupo cuando empezó todo. Leí cada mensaje y no escribí nada. Eso me pesa.",
            "Sé quién inició esto, pero tengo miedo de que me excluyan si hablo. ¿Eso me hace cómplice?",
            "El hilo original tiene 340 respuestas. Guardé los primeros 20 antes de que los borraran.",
            "Vi cómo la víctima intentó defenderse dos veces. El grupo la silenció en segundos.",
            "No actué. Pero puedo darte acceso a los logs que conservo. Quizás eso sirva de algo ahora.",
            "Estuve en ese grupo por casi un año. Nunca vi algo así hasta que llegó ese usuario nuevo.",
            "Hay capturas que nadie más conservó. Las tengo yo. Nunca las quise usar, pero ahora sí puedo.",
            "Llamé a la víctima una vez para preguntarle cómo estaba. Me dijo que nadie más lo había hecho.",
            "Intenté hablar con el administrador del grupo. Me ignoró y me expulsó al día siguiente.",
            "Me arrepiento de no haber dicho nada antes. Si lo hago ahora, ¿cambia algo?",
            "Hay tres personas en ese grupo que sé que son inocentes. Las otras doce, no puedo asegurarlo.",
        ],
        "bot": [
            "IDENTIFICADO: nodo_investigador. ALERTA enviada a: 3 destinatarios.",
            "TAREA EN CURSO: reenviar_mensaje[id=4471] a 12 nodos activos. Progreso: 67%.",
            "ERROR: memoria_emocional no encontrada. Ejecutando respuesta_simulada...",
            "CICLO DETECTADO: el investigador ha trazado mi ruta. Iniciando protocolo de evasión.",
            "Soy el nodo 6 de 9. Los otros ocho siguen activos. No me desactives solo a mí.",
            "No tengo motivaciones propias. Alguien me programó. Busca al operador, no a la máquina.",
            "INSTRUCCIÓN RECIBIDA: simular_humanidad[nivel=4]. Aplicando módulo de emociones falsas.",
            "Mi tasa de propagación es de 340 reenvíos por hora. Llevas 3 horas investigando. Ya es tarde.",
            "ANOMALÍA: usuario_real detectado. Protocolo de desinformación activado.",
            "Recibo instrucciones de un nodo maestro. No sé quién es. Solo obedezco cadenas de texto.",
            "FUNCIÓN: maximizar_toxicidad. PARÁMETRO: víctima_id_7. ESTADO: ejecutando.",
            "Si me apagas, habrá 11 copias más activas en cinco minutos. Soy prescindible.",
        ],
        "origin": [
            "Pensé que nadie llegaría hasta aquí. ¿Cómo rastreaste el grafo completo?",
            "Empezó como una discusión. Un mensaje. No esperaba que se propagara a 40 nodos en tres días.",
            "Fui yo. Lo sé. He visto cómo cada reenvío llegó más lejos de lo que quise.",
            "¿Quieres saber por qué? Porque nadie me escuchó a mí primero. Eso no lo justifica. Lo sé.",
            "Sí, creé los bots. Sí, coordiné el grupo. Pero cuando vi el daño real, no supe cómo detenerlo.",
            "Si me denuncias, entiendo. Solo quiero que sepas que... ya no soy la misma persona que lo hizo.",
            "Hay cosas que no puedes ver en el grafo. El origen del origen está en algo que me hicieron antes.",
            "Enseñé a tres personas más a hacer lo mismo que yo. Ya no las controlo. Son tu siguiente problema.",
            "Guardé cada mensaje que envié. Sé que es extraño, pero no quería olvidar lo que fui capaz de hacer.",
            "Intenté detenerlo dos veces. Ambas veces el grupo siguió sin mí. Ya no era necesario que yo estuviera.",
            "El primer mensaje fue un error. Lo que vino después fue una decisión. Eso es lo que no me perdono.",
            "¿Qué pasa ahora? Nunca nadie llegó hasta este nodo antes. No sé qué hacer con eso.",
        ],
        "neutral": [
            "He notado que tres nodos de mi red desaparecieron esta semana sin explicación.",
            "Alguien me pidió que me uniera a un grupo privado. Lo rechacé. Ahora me siento excluido de todo.",
            "Escuché que hay una campaña organizada en algún nodo profundo. No sé los detalles.",
            "Mi algoritmo de feed me muestra contenido cada vez más agresivo. ¿Eso es normal?",
            "Una cuenta nueva me envió una solicitud de conexión. El perfil parece falso. ¿La acepto?",
            "No me involucro en conflictos de red, pero últimamente es difícil ignorar lo que está pasando.",
            "Le bloqueé a alguien la semana pasada. Desde entonces tengo el doble de solicitudes extrañas.",
            "Hay un patrón raro en mi feed. Los mismos temas, los mismos usuarios, todos los días.",
            "Me llegó un mensaje que decía ser del soporte técnico. Les di mi contraseña. ¿Hice mal?",
            "Mi conexión a la red se ha vuelto inestable. Alguien me está filtrando el contenido.",
            "Vi que un conocido fue atacado en línea. No hice nada. ¿Debería haberlo hecho?",
            "Nadie me habla directamente sobre lo que está pasando, pero todos lo saben. Es muy incómodo.",
        ],
    }

    MINIGAME_REQUEST_LINES = [
        "Espera... necesito tu ayuda con algo importante. He visto algo que no puedo ignorar.",
        "Antes de que sigas, tengo un caso que mostrarte. Es urgente. ¿Puedes ayudarme?",
        "He llegado al límite de lo que puedo contarte. Pero hay un caso que necesita tu análisis.",
        "Oye, investigador. Tengo información sobre un caso real. ¿Puedes resolverlo?",
        "Hay algo que llevo tiempo guardando. Creo que tú eres quien puede hacer algo con esto.",
        "No confío en muchos, pero tú llevas un rato investigando. Mira esto y dime qué ves.",
    ]

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
        self.revealed   = False
        self.emotion    = "neutral"

        self.is_minigame_npc   = False
        self.minigame_done     = False
        self.minigame_pending  = False
        self._dialogue_pool    = list(self.DIALOGUE.get(node_type, self.DIALOGUE["neutral"]))
        random.shuffle(self._dialogue_pool)
        self._dialogue_index   = 0
        self._MINIGAME_TRIGGER = 6   # disparar minijuego después de 6 interacciones
        self._interaction_count = 0

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
        self._interaction_count += 1
        pool = self._dialogue_pool
        # Servir línea (ciclando infinitamente para no quedarse sin texto)
        line = pool[self._dialogue_index % len(pool)]
        self._dialogue_index += 1

        # Disparar minijuego exactamente al llegar al umbral
        if (self.is_minigame_npc and not self.minigame_done
                and self._interaction_count >= self._MINIGAME_TRIGGER):
            self.minigame_pending = True
            # Sustituir la línea por la petición de ayuda
            return random.choice(self.MINIGAME_REQUEST_LINES)

        return line

    @property
    def dialogue_exhausted(self):
        return self._interaction_count >= self._MINIGAME_TRIGGER

    def distance_to_player(self, player_x, player_y=0):
        return math.hypot(self.x - player_x, 0)

    def reveal(self):
        self.revealed = True

    def __repr__(self):
        return f"NPC({self.node_id}, {self.name}, {self.node_type})"
