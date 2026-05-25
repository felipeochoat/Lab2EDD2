# model/lab1_data.py
"""
Datos del Lab1 adaptados para uso en el minijuego de Lab2.
Incluye NodoCaso, los 4 generadores de nivel y generar_caso_minijuego().
Incluye TODOS los campos extra (_victima, _agresor_user, _num_mensajes, etc.)
para que evidencias_img.py pueda generar los mockups correctamente.
"""
import random


# ── NodoCaso ────────────────────────────────────────────────────────────────
class NodoCaso:
    def __init__(self, id_caso, tipo_acoso, gravedad, evidencias, ley, pena, descripcion=""):
        self.id_caso     = id_caso
        self.tipo_acoso  = tipo_acoso
        self.gravedad    = gravedad
        self.evidencias  = evidencias
        self.ley         = ley
        self.pena        = pena
        self.descripcion = descripcion
        self.izquierdo   = None
        self.derecho     = None
        self.altura      = 1

    def __repr__(self):
        return f"Caso({self.id_caso}, grav={self.gravedad})"


# ── Bancos de datos ─────────────────────────────────────────────────────────
_VICTIMAS = [
    "Valeria", "Sofía", "Daniela", "Camila", "Luciana",
    "Mariana", "Isabella", "Natalia", "Gabriela", "Alejandra",
]
_AGRESORES_USUARIO = [
    "@shadow99", "@dark_wolf", "@ghost_fx", "@neon_viper",
    "@ctrl_alt_evil", "@byte_hater", "@null_ptr", "@xX_toxic_Xx",
    "@anon_storm", "@pixel_rage",
]
_AGRESORES_NOMBRE = [
    "Andrés M.", "Carlos R.", "Diego F.", "Sebastián L.",
    "Mateo G.", "Nicolás H.", "Julián P.", "Santiago V.",
]
_PLATAFORMAS = [
    "Instagram", "TikTok", "Twitter/X", "Facebook",
    "WhatsApp", "Discord", "Snapchat", "Telegram",
]
_COLEGIOS = [
    "el Colegio Distrital Simón Bolívar",
    "la I.E. Técnica Industrial",
    "el Colegio Nacional San José",
    "la Institución Educativa La Esperanza",
    "el Colegio Cooperativo del Norte",
]
_RANGOS_GRAVEDAD = [(1, 3), (4, 5), (6, 7), (8, 10)]


# ── Generador Nivel 1: Injuria ───────────────────────────────────────────────
def _nivel_injuria(victima, agresor_user, agresor_nombre, plataforma, colegio, gravedad):
    num_mensajes = random.randint(8, 30)
    num_dias     = random.randint(3, 14)
    variantes = [
        (f"{victima} comienza a recibir mensajes ofensivos en {plataforma}.\n"
         f"Al principio parecen bromas, pero {agresor_user} lleva\n"
         f"{num_dias} días enviando {num_mensajes} insultos."),
        (f"En el grupo de {colegio}, {agresor_user}\n"
         f"publica comentarios hirientes sobre {victima} durante\n"
         f"{num_dias} días consecutivos."),
        (f"{victima} descubre que {agresor_user} lleva semanas\n"
         f"enviando mensajes ofensivos desde {plataforma}.\n"
         f"Ya acumula {num_mensajes} insultos documentados."),
    ]
    historia = random.choice(variantes)
    evidencias_disponibles = [
        {"id": "ev1_1", "nombre": "Captura de pantalla",
         "descripcion": f"Mensaje ofensivo de {agresor_user} hacia {victima}.",
         "sprite": "captura", "posicion": (200, 280)},
        {"id": "ev1_2", "nombre": "Historial de chat",
         "descripcion": f"Registro de {num_mensajes} mensajes en {num_dias} días.",
         "sprite": "chat",    "posicion": (440, 240)},
        {"id": "ev1_3", "nombre": "Perfil del agresor",
         "descripcion": f"Usuario {agresor_user} identificado como emisor.",
         "sprite": "perfil",  "posicion": (680, 300)},
    ]
    caso = NodoCaso(
        id_caso=f"CASO-{random.randint(1000,9999)}", tipo_acoso="Injuria digital",
        gravedad=gravedad,
        evidencias=[f"Capturas de {num_mensajes} mensajes", f"Historial en {plataforma}",
                    f"Perfil {agresor_user}"],
        ley="Art. 220 Código Penal Colombiano", pena="Multa de 1 a 3 SMLV",
        descripcion=f"Mensajes ofensivos de {agresor_user} contra {victima} en {plataforma}.",
    )
    return {
        "titulo":               "Misión de Emergencia – Injuria Digital",
        "historia":             historia,
        "objetivo":             "Recolecta las capturas e identifica el tipo de agresión.",
        "evidencias_disponibles": evidencias_disponibles,
        "evidencias_requeridas":  {"ev1_1", "ev1_2", "ev1_3"},
        "pregunta": {
            "texto":    "¿Qué tipo de delito cometió el agresor?",
            "opciones": ["Injuria (Art. 220 C.P.)", "Calumnia (Art. 221 C.P.)",
                         "Suplantación – Ley 1273", "Hostigamiento digital"],
            "correcta": 0,
            "explicacion": (
                f"Injuria: ofender el honor de alguien mediante palabras o hechos.\n"
                f"Art. 220 del Código Penal Colombiano.\n"
                f"{agresor_user} envió {num_mensajes} mensajes ofensivos a {victima}."
            ),
        },
        "caso":         caso,
        "color_acento": (80, 200, 255),
        # Campos extra para mockups
        "_victima":        victima,
        "_agresor_user":   agresor_user,
        "_agresor_nombre": agresor_nombre,
        "_plataforma":     plataforma,
        "_colegio":        colegio,
        "_gravedad":       gravedad,
        "_num_mensajes":   num_mensajes,
        "_num_dias":       num_dias,
    }


# ── Generador Nivel 2: Calumnia ──────────────────────────────────────────────
def _nivel_calumnia(victima, agresor_user, agresor_nombre, plataforma, colegio, gravedad):
    num_compartidos = random.randint(50, 500)
    num_testimonios = random.randint(2, 6)
    tipo_rumor = random.choice([
        f"acusaciones falsas de robo contra {victima}",
        f"fotos editadas que difaman a {victima}",
        f"historia inventada que implica a {victima} en una pelea",
        f"capturas falsas de conversaciones de {victima}",
    ])
    variantes = [
        (f"Un post con {tipo_rumor} circula en {plataforma}\n"
         f"con {num_compartidos}+ compartidos. {agresor_nombre}\n"
         f"es señalado como el origen del rumor."),
        (f"{agresor_user} publica {tipo_rumor} en {plataforma}.\n"
         f"El post se viraliza con {num_compartidos} compartidos\n"
         f"antes de que {victima} pueda reaccionar."),
        (f"Compañeros de {colegio} comparten masivamente\n"
         f"{tipo_rumor} iniciado por {agresor_user},\n"
         f"acumulando {num_compartidos} interacciones."),
    ]
    historia = random.choice(variantes)
    evidencias_disponibles = [
        {"id": "ev2_1", "nombre": "Post original",
         "descripcion": f"Publicación falsa con {num_compartidos}+ compartidos.",
         "sprite": "post",           "posicion": (180, 260)},
        {"id": "ev2_2", "nombre": "Metadata del post",
         "descripcion": f"IP aprox. rastreada a {agresor_nombre}.",
         "sprite": "metadata",       "posicion": (440, 220)},
        {"id": "ev2_3", "nombre": "Testimonios",
         "descripcion": f"{num_testimonios} compañeros confirman que el rumor es falso.",
         "sprite": "testimonio",     "posicion": (700, 290)},
        {"id": "ev2_4", "nombre": "Cuenta eliminada",
         "descripcion": f"{agresor_user} eliminó su cuenta tras la viralización.",
         "sprite": "cuenta_borrada", "posicion": (340, 380)},
    ]
    caso = NodoCaso(
        id_caso=f"CASO-{random.randint(1000,9999)}", tipo_acoso="Calumnia en redes",
        gravedad=gravedad,
        evidencias=[f"Post viral ({num_compartidos} compartidos)",
                    f"Metadata: {agresor_nombre}", f"{num_testimonios} testimonios"],
        ley="Art. 221 Código Penal Colombiano", pena="Multa de 2 a 5 SMLV",
        descripcion=f"Rumores falsos de {agresor_user} en {plataforma} afectando a {victima}.",
    )
    return {
        "titulo":               "Misión de Emergencia – Calumnia Viral",
        "historia":             historia,
        "objetivo":             "Identifica la publicación original y rastrea quién inició el rumor.",
        "evidencias_disponibles": evidencias_disponibles,
        "evidencias_requeridas":  {"ev2_1", "ev2_2", "ev2_3"},
        "pregunta": {
            "texto":    "¿Cuál es el delito principal cometido?",
            "opciones": ["Injuria (Art. 220 C.P.)", "Calumnia (Art. 221 C.P.)",
                         "Acceso abusivo – Ley 1273", "Amenaza digital"],
            "correcta": 1,
            "explicacion": (
                f"Calumnia: imputar falsamente a alguien una conducta delictiva.\n"
                f"Art. 221 del Código Penal Colombiano.\n"
                f"{agresor_user} difundió {tipo_rumor}."
            ),
        },
        "caso":         caso,
        "color_acento": (255, 200, 60),
        "_victima":         victima,
        "_agresor_user":    agresor_user,
        "_agresor_nombre":  agresor_nombre,
        "_plataforma":      plataforma,
        "_colegio":         colegio,
        "_gravedad":        gravedad,
        "_num_compartidos": num_compartidos,
        "_num_testimonios": num_testimonios,
    }


# ── Generador Nivel 3: Suplantación ─────────────────────────────────────────
def _nivel_suplantacion(victima, agresor_user, agresor_nombre, plataforma, colegio, gravedad):
    num_victimas_sec = random.randint(3, 12)
    tipo_contenido = random.choice([
        f"insultos dirigidos a compañeros de {colegio}",
        "fotos editadas ofensivas",
        "mensajes de odio hacia otros usuarios",
        "solicitudes de dinero a conocidos de la víctima",
        "contenido inapropiado en nombre de la víctima",
    ])
    variantes = [
        (f"Aparece un perfil falso usando la foto de {victima} en {plataforma}.\n"
         f"Publica {tipo_contenido}, atacando\n"
         f"a {num_victimas_sec} usuarios con su identidad."),
        (f"{agresor_user} crea una cuenta clonada de {victima}\n"
         f"en {plataforma} y comienza a publicar {tipo_contenido}.\n"
         f"{num_victimas_sec} personas ya han recibido ataques."),
        (f"Una cuenta idéntica a la de {victima} aparece en {plataforma}.\n"
         f"Detrás está {agresor_nombre}, publicando {tipo_contenido}\n"
         f"y afectando a {num_victimas_sec} usuarios inocentes."),
    ]
    historia = random.choice(variantes)
    evidencias_disponibles = [
        {"id": "ev3_1", "nombre": "Perfil falso",
         "descripcion": f"Cuenta en {plataforma} con foto de {victima}.",
         "sprite": "perfil_falso", "posicion": (160, 250)},
        {"id": "ev3_2", "nombre": "IP de creación",
         "descripcion": f"IP registrada vinculada a {agresor_nombre}.",
         "sprite": "ip",           "posicion": (420, 210)},
        {"id": "ev3_3", "nombre": "Logs de actividad",
         "descripcion": "Registro de accesos y publicaciones del perfil falso.",
         "sprite": "logs",         "posicion": (680, 270)},
        {"id": "ev3_4", "nombre": "Denuncia de víctimas",
         "descripcion": f"{num_victimas_sec} usuarios presentaron denuncia.",
         "sprite": "denuncia",     "posicion": (300, 370)},
    ]
    caso = NodoCaso(
        id_caso=f"CASO-{random.randint(1000,9999)}", tipo_acoso="Suplantación de identidad",
        gravedad=gravedad,
        evidencias=[f"Perfil falso en {plataforma}", f"IP: {agresor_nombre}",
                    "Logs de actividad", f"{num_victimas_sec} denuncias"],
        ley="Ley 1273 de 2009 – Art. 9", pena="4 a 8 años + multa",
        descripcion=f"Perfil falso de {victima} usado por {agresor_user}.",
    )
    return {
        "titulo":               "Misión de Emergencia – Suplantación",
        "historia":             historia,
        "objetivo":             "Analiza el perfil falso y rastrea quién está detrás.",
        "evidencias_disponibles": evidencias_disponibles,
        "evidencias_requeridas":  {"ev3_1", "ev3_2", "ev3_3", "ev3_4"},
        "pregunta": {
            "texto":    "¿Qué ley aplica para la suplantación de identidad digital?",
            "opciones": ["Art. 220 Código Penal", "Ley 1273 de 2009 – Delitos informáticos",
                         "Art. 221 Código Penal", "Ley 1098 de 2006"],
            "correcta": 1,
            "explicacion": (
                "La Ley 1273 de 2009 tipifica delitos informáticos en Colombia,\n"
                "incluyendo la suplantación de identidad digital.\n"
                f"Penas de hasta 8 años. {agresor_nombre} creó un perfil falso de {victima}."
            ),
        },
        "caso":         caso,
        "color_acento": (255, 80, 120),
        "_victima":         victima,
        "_agresor_user":    agresor_user,
        "_agresor_nombre":  agresor_nombre,
        "_plataforma":      plataforma,
        "_colegio":         colegio,
        "_gravedad":        gravedad,
        "_num_testimonios": num_victimas_sec,
    }


# ── Generador Nivel 4: Hostigamiento ────────────────────────────────────────
def _nivel_hostigamiento(victima, agresor_user, agresor_nombre, plataforma, colegio, gravedad):
    num_cuentas  = random.randint(3, 8)
    num_semanas  = random.randint(2, 6)
    tipo_ataque = random.choice([
        "mensajes de amenaza y hostigamiento",
        "ataques organizados con insultos coordinados",
        "campañas de desprestigio con noticias falsas",
        "spam masivo y reporte falso de cuentas",
    ])
    variantes = [
        (f"{num_cuentas} cuentas distintas atacan a {victima} en {plataforma}\n"
         f"con {tipo_ataque} durante {num_semanas} semanas.\n"
         f"Todas pertenecen a {agresor_nombre}."),
        (f"El detective descubre que {agresor_user} creó {num_cuentas} perfiles\n"
         f"para coordinar {tipo_ataque} contra {victima}.\n"
         f"La campaña lleva {num_semanas} semanas activa."),
        (f"En {plataforma}, {num_cuentas} cuentas lanzan {tipo_ataque}\n"
         f"contra {victima} simultáneamente durante {num_semanas} semanas.\n"
         f"El rastreo apunta a {agresor_nombre} como autor."),
    ]
    historia = random.choice(variantes)
    evidencias_disponibles = [
        {"id": "ev4_1", "nombre": "Análisis de cuentas",
         "descripcion": f"{num_cuentas} cuentas con el mismo patrón de escritura.",
         "sprite": "analisis",   "posicion": (130, 230)},
        {"id": "ev4_2", "nombre": "Horario de ataques",
         "descripcion": f"Todas activas en los mismos horarios ({num_semanas} semanas).",
         "sprite": "horario",    "posicion": (360, 190)},
        {"id": "ev4_3", "nombre": "Dispositivo único",
         "descripcion": f"Mismo fingerprint en las {num_cuentas} cuentas.",
         "sprite": "dispositivo","posicion": (600, 250)},
        {"id": "ev4_4", "nombre": "Historial escolar",
         "descripcion": f"Conflicto previo entre {agresor_nombre} y {victima}.",
         "sprite": "historial",  "posicion": (250, 350)},
        {"id": "ev4_5", "nombre": "Testigo digital",
         "descripcion": f"Un usuario vio a {agresor_user} crear las cuentas.",
         "sprite": "testigo",    "posicion": (500, 350)},
    ]
    caso = NodoCaso(
        id_caso=f"CASO-{random.randint(1000,9999)}", tipo_acoso="Hostigamiento coordinado",
        gravedad=gravedad,
        evidencias=[f"{num_cuentas} cuentas del mismo agresor",
                    f"Mismo horario ({num_semanas} semanas)", "Fingerprint único"],
        ley="Ley 1273/2009 + hostigamiento", pena="Proceso penal + medidas de protección",
        descripcion=f"Campaña de {agresor_nombre} con {num_cuentas} cuentas contra {victima}.",
    )
    return {
        "titulo":               "Misión de Emergencia – Hostigamiento",
        "historia":             historia,
        "objetivo":             "Encuentra el patrón que conecta todas las cuentas.",
        "evidencias_disponibles": evidencias_disponibles,
        "evidencias_requeridas":  {"ev4_1", "ev4_2", "ev4_3", "ev4_4", "ev4_5"},
        "pregunta": {
            "texto":    "¿Cuál es el delito más grave cometido?",
            "opciones": ["Injuria simple", "Calumnia leve",
                         "Hostigamiento y acoso reiterado digital",
                         "Daño informático – Ley 1273"],
            "correcta": 2,
            "explicacion": (
                "El hostigamiento reiterado y coordinado constituye acoso digital agravado.\n"
                "Puede conllevar proceso penal y medidas de protección inmediata.\n"
                f"{agresor_nombre} operó {num_cuentas} cuentas durante {num_semanas} semanas."
            ),
        },
        "caso":         caso,
        "color_acento": (180, 80, 255),
        "_victima":        victima,
        "_agresor_user":   agresor_user,
        "_agresor_nombre": agresor_nombre,
        "_plataforma":     plataforma,
        "_colegio":        colegio,
        "_gravedad":       gravedad,
        "_num_cuentas":    num_cuentas,
        "_num_semanas":    num_semanas,
    }


# ── Función principal ────────────────────────────────────────────────────────
def generar_caso_minijuego():
    """Genera un caso aleatorio del Lab1 para usar como minijuego en Lab2."""
    victima      = random.choice(_VICTIMAS)
    agresor_user = random.choice(_AGRESORES_USUARIO)
    agresor_nom  = random.choice(_AGRESORES_NOMBRE)
    plataforma   = random.choice(_PLATAFORMAS)
    colegio      = random.choice(_COLEGIOS)
    rango        = random.choice(_RANGOS_GRAVEDAD)
    gravedad     = random.randint(*rango)

    gen = random.choice([_nivel_injuria, _nivel_calumnia,
                         _nivel_suplantacion, _nivel_hostigamiento])
    return gen(victima, agresor_user, agresor_nom, plataforma, colegio, gravedad)
