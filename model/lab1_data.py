# model/lab1_data.py
"""
Datos del Lab1 adaptados para uso en el minijuego de Lab2.
6 tipos de caso × 3 variantes de historia = 18 combinaciones únicas.
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
    "Valentina", "Fernanda", "Laura", "Jimena", "Paula",
]
_AGRESORES_USUARIO = [
    "@shadow99", "@dark_wolf", "@ghost_fx", "@neon_viper",
    "@ctrl_alt_evil", "@byte_hater", "@null_ptr", "@xX_toxic_Xx",
    "@anon_storm", "@pixel_rage", "@void_striker", "@netcrawler7",
]
_AGRESORES_NOMBRE = [
    "Andrés M.", "Carlos R.", "Diego F.", "Sebastián L.",
    "Mateo G.", "Nicolás H.", "Julián P.", "Santiago V.",
    "Camilo T.", "Esteban A.",
]
_PLATAFORMAS = [
    "Instagram", "TikTok", "Twitter/X", "Facebook",
    "WhatsApp", "Discord", "Snapchat", "Telegram", "YouTube", "Reddit",
]
_COLEGIOS = [
    "el Colegio Distrital Simón Bolívar",
    "la I.E. Técnica Industrial",
    "el Colegio Nacional San José",
    "la Institución Educativa La Esperanza",
    "el Colegio Cooperativo del Norte",
    "la Institución Educativa Fe y Alegría",
]
_RANGOS_GRAVEDAD = [(1, 3), (4, 5), (6, 7), (8, 10)]


# ─────────────────────────────────────────────────────────────
#  CASO 1 — Injuria
# ─────────────────────────────────────────────────────────────
def _nivel_injuria(victima, agresor_user, agresor_nombre, plataforma, colegio, gravedad):
    num_mensajes = random.randint(8, 30)
    num_dias     = random.randint(3, 14)
    historia = random.choice([
        (f"{victima} comienza a recibir mensajes ofensivos en {plataforma}.\n"
         f"Al principio parecen bromas, pero {agresor_user} lleva\n"
         f"{num_dias} días enviando {num_mensajes} insultos."),
        (f"En el grupo de {colegio}, {agresor_user}\n"
         f"publica comentarios hirientes sobre {victima} durante\n"
         f"{num_dias} días consecutivos."),
        (f"{victima} descubre que {agresor_user} lleva semanas\n"
         f"enviando mensajes ofensivos desde {plataforma}.\n"
         f"Ya acumula {num_mensajes} insultos documentados."),
    ])
    evidencias_disponibles = [
        {"id": "ev1_1", "nombre": "Captura de pantalla",
         "descripcion": f"Mensaje ofensivo de {agresor_user} hacia {victima}.",
         "sprite": "captura", "posicion": (200, 280)},
        {"id": "ev1_2", "nombre": "Historial de chat",
         "descripcion": f"Registro de {num_mensajes} mensajes en {num_dias} días.",
         "sprite": "chat",    "posicion": (440, 240)},
        {"id": "ev1_3", "nombre": "Perfil del agresor",
         "descripcion": f"Usuario {agresor_user} identificado.",
         "sprite": "perfil",  "posicion": (680, 300)},
    ]
    return {
        "titulo": "Misión de Emergencia – Injuria Digital",
        "historia": historia,
        "objetivo": "Recolecta las capturas e identifica el tipo de agresión.",
        "evidencias_disponibles": evidencias_disponibles,
        "evidencias_requeridas": {"ev1_1", "ev1_2", "ev1_3"},
        "pregunta": {
            "texto": "¿Qué tipo de delito cometió el agresor?",
            "opciones": ["Injuria (Art. 220 C.P.)", "Calumnia (Art. 221 C.P.)",
                         "Suplantación – Ley 1273", "Hostigamiento digital"],
            "correcta": 0,
            "explicacion": (
                f"Injuria: ofender el honor de alguien mediante palabras o hechos.\n"
                f"Art. 220 del Código Penal Colombiano.\n"
                f"{agresor_user} envió {num_mensajes} mensajes ofensivos a {victima}."
            ),
        },
        "caso": NodoCaso(
            f"CASO-{random.randint(1000,9999)}", "Injuria digital", gravedad,
            [f"Capturas de {num_mensajes} mensajes", f"Historial en {plataforma}", f"Perfil {agresor_user}"],
            "Art. 220 Código Penal Colombiano", "Multa de 1 a 3 SMLV",
            f"Mensajes ofensivos de {agresor_user} contra {victima} en {plataforma}.",
        ),
        "color_acento": (80, 200, 255),
        "_victima": victima, "_agresor_user": agresor_user, "_agresor_nombre": agresor_nombre,
        "_plataforma": plataforma, "_colegio": colegio, "_gravedad": gravedad,
        "_num_mensajes": num_mensajes, "_num_dias": num_dias,
    }


# ─────────────────────────────────────────────────────────────
#  CASO 2 — Calumnia
# ─────────────────────────────────────────────────────────────
def _nivel_calumnia(victima, agresor_user, agresor_nombre, plataforma, colegio, gravedad):
    num_compartidos = random.randint(50, 500)
    num_testimonios = random.randint(2, 6)
    tipo_rumor = random.choice([
        f"acusaciones falsas de robo contra {victima}",
        f"fotos editadas que difaman a {victima}",
        f"historia inventada que implica a {victima} en una pelea",
        f"capturas falsas de conversaciones de {victima}",
    ])
    historia = random.choice([
        (f"Un post con {tipo_rumor} circula en {plataforma}\n"
         f"con {num_compartidos}+ compartidos. {agresor_nombre}\n"
         f"es señalado como origen del rumor."),
        (f"{agresor_user} publica {tipo_rumor} en {plataforma}.\n"
         f"El post se viraliza con {num_compartidos} compartidos\n"
         f"antes de que {victima} pueda reaccionar."),
        (f"Compañeros de {colegio} comparten masivamente\n"
         f"{tipo_rumor} iniciado por {agresor_user},\n"
         f"acumulando {num_compartidos} interacciones."),
    ])
    evidencias_disponibles = [
        {"id": "ev2_1", "nombre": "Post original",
         "descripcion": f"Publicación falsa con {num_compartidos}+ compartidos.",
         "sprite": "post", "posicion": (180, 260)},
        {"id": "ev2_2", "nombre": "Metadata del post",
         "descripcion": f"IP rastreada a {agresor_nombre}.",
         "sprite": "metadata", "posicion": (440, 220)},
        {"id": "ev2_3", "nombre": "Testimonios",
         "descripcion": f"{num_testimonios} compañeros confirman que es falso.",
         "sprite": "testimonio", "posicion": (700, 290)},
        {"id": "ev2_4", "nombre": "Cuenta eliminada",
         "descripcion": f"{agresor_user} borró su cuenta tras la viralización.",
         "sprite": "cuenta_borrada", "posicion": (340, 380)},
    ]
    return {
        "titulo": "Misión de Emergencia – Calumnia Viral",
        "historia": historia,
        "objetivo": "Identifica la publicación original y rastrea quién inició el rumor.",
        "evidencias_disponibles": evidencias_disponibles,
        "evidencias_requeridas": {"ev2_1", "ev2_2", "ev2_3"},
        "pregunta": {
            "texto": "¿Cuál es el delito principal cometido?",
            "opciones": ["Injuria (Art. 220 C.P.)", "Calumnia (Art. 221 C.P.)",
                         "Acceso abusivo – Ley 1273", "Amenaza digital"],
            "correcta": 1,
            "explicacion": (
                f"Calumnia: imputar falsamente a alguien una conducta delictiva.\n"
                f"Art. 221 del Código Penal Colombiano.\n"
                f"{agresor_user} difundió {tipo_rumor}."
            ),
        },
        "caso": NodoCaso(
            f"CASO-{random.randint(1000,9999)}", "Calumnia en redes", gravedad,
            [f"Post viral ({num_compartidos})", f"Metadata: {agresor_nombre}", f"{num_testimonios} testimonios"],
            "Art. 221 Código Penal Colombiano", "Multa de 2 a 5 SMLV",
        ),
        "color_acento": (255, 200, 60),
        "_victima": victima, "_agresor_user": agresor_user, "_agresor_nombre": agresor_nombre,
        "_plataforma": plataforma, "_colegio": colegio, "_gravedad": gravedad,
        "_num_compartidos": num_compartidos, "_num_testimonios": num_testimonios,
    }


# ─────────────────────────────────────────────────────────────
#  CASO 3 — Suplantación
# ─────────────────────────────────────────────────────────────
def _nivel_suplantacion(victima, agresor_user, agresor_nombre, plataforma, colegio, gravedad):
    num_victimas_sec = random.randint(3, 12)
    tipo_contenido = random.choice([
        f"insultos dirigidos a compañeros de {colegio}",
        "fotos editadas ofensivas",
        "mensajes de odio hacia otros usuarios",
        "solicitudes de dinero a conocidos de la víctima",
    ])
    historia = random.choice([
        (f"Aparece un perfil falso usando la foto de {victima} en {plataforma}.\n"
         f"Publica {tipo_contenido}, atacando a {num_victimas_sec} usuarios."),
        (f"{agresor_user} crea una cuenta clonada de {victima}\n"
         f"en {plataforma} y comienza a publicar {tipo_contenido}.\n"
         f"{num_victimas_sec} personas ya han recibido ataques."),
        (f"Una cuenta idéntica a la de {victima} aparece en {plataforma}.\n"
         f"Detrás está {agresor_nombre}, publicando {tipo_contenido}\n"
         f"y afectando a {num_victimas_sec} usuarios."),
    ])
    evidencias_disponibles = [
        {"id": "ev3_1", "nombre": "Perfil falso",
         "descripcion": f"Cuenta en {plataforma} con foto de {victima}.",
         "sprite": "perfil_falso", "posicion": (160, 250)},
        {"id": "ev3_2", "nombre": "IP de creación",
         "descripcion": f"IP registrada vinculada a {agresor_nombre}.",
         "sprite": "ip", "posicion": (420, 210)},
        {"id": "ev3_3", "nombre": "Logs de actividad",
         "descripcion": "Registro de accesos y publicaciones del perfil falso.",
         "sprite": "logs", "posicion": (680, 270)},
        {"id": "ev3_4", "nombre": "Denuncia de víctimas",
         "descripcion": f"{num_victimas_sec} usuarios presentaron denuncia.",
         "sprite": "denuncia", "posicion": (300, 370)},
    ]
    return {
        "titulo": "Misión de Emergencia – Suplantación",
        "historia": historia,
        "objetivo": "Analiza el perfil falso y rastrea quién está detrás.",
        "evidencias_disponibles": evidencias_disponibles,
        "evidencias_requeridas": {"ev3_1", "ev3_2", "ev3_3", "ev3_4"},
        "pregunta": {
            "texto": "¿Qué ley aplica para la suplantación de identidad digital?",
            "opciones": ["Art. 220 Código Penal", "Ley 1273 de 2009 – Delitos informáticos",
                         "Art. 221 Código Penal", "Ley 1098 de 2006"],
            "correcta": 1,
            "explicacion": (
                "La Ley 1273 de 2009 tipifica delitos informáticos en Colombia,\n"
                "incluyendo la suplantación de identidad digital.\n"
                f"Penas de hasta 8 años. {agresor_nombre} creó perfil falso de {victima}."
            ),
        },
        "caso": NodoCaso(
            f"CASO-{random.randint(1000,9999)}", "Suplantación de identidad", gravedad,
            [f"Perfil falso en {plataforma}", f"IP: {agresor_nombre}", f"{num_victimas_sec} denuncias"],
            "Ley 1273 de 2009 – Art. 9", "4 a 8 años + multa",
        ),
        "color_acento": (255, 80, 120),
        "_victima": victima, "_agresor_user": agresor_user, "_agresor_nombre": agresor_nombre,
        "_plataforma": plataforma, "_colegio": colegio, "_gravedad": gravedad,
        "_num_testimonios": num_victimas_sec,
    }


# ─────────────────────────────────────────────────────────────
#  CASO 4 — Hostigamiento
# ─────────────────────────────────────────────────────────────
def _nivel_hostigamiento(victima, agresor_user, agresor_nombre, plataforma, colegio, gravedad):
    num_cuentas  = random.randint(3, 8)
    num_semanas  = random.randint(2, 6)
    tipo_ataque = random.choice([
        "mensajes de amenaza y hostigamiento",
        "ataques organizados con insultos coordinados",
        "campañas de desprestigio con noticias falsas",
        "spam masivo y reporte falso de cuentas",
    ])
    historia = random.choice([
        (f"{num_cuentas} cuentas distintas atacan a {victima} en {plataforma}\n"
         f"con {tipo_ataque} durante {num_semanas} semanas.\n"
         f"Todas pertenecen a {agresor_nombre}."),
        (f"{agresor_user} creó {num_cuentas} perfiles para coordinar\n"
         f"{tipo_ataque} contra {victima}.\n"
         f"La campaña lleva {num_semanas} semanas activa."),
        (f"En {plataforma}, {num_cuentas} cuentas lanzan {tipo_ataque}\n"
         f"contra {victima} simultáneamente durante {num_semanas} semanas.\n"
         f"El rastreo apunta a {agresor_nombre} como autor."),
    ])
    evidencias_disponibles = [
        {"id": "ev4_1", "nombre": "Análisis de cuentas",
         "descripcion": f"{num_cuentas} cuentas con el mismo patrón.",
         "sprite": "analisis", "posicion": (130, 230)},
        {"id": "ev4_2", "nombre": "Horario de ataques",
         "descripcion": f"Activas en los mismos horarios ({num_semanas} semanas).",
         "sprite": "horario", "posicion": (360, 190)},
        {"id": "ev4_3", "nombre": "Dispositivo único",
         "descripcion": f"Mismo fingerprint en las {num_cuentas} cuentas.",
         "sprite": "dispositivo", "posicion": (600, 250)},
        {"id": "ev4_4", "nombre": "Historial escolar",
         "descripcion": f"Conflicto previo entre {agresor_nombre} y {victima}.",
         "sprite": "historial", "posicion": (250, 350)},
        {"id": "ev4_5", "nombre": "Testigo digital",
         "descripcion": f"Un usuario vio a {agresor_user} crear las cuentas.",
         "sprite": "testigo", "posicion": (500, 350)},
    ]
    return {
        "titulo": "Misión de Emergencia – Hostigamiento",
        "historia": historia,
        "objetivo": "Encuentra el patrón que conecta todas las cuentas.",
        "evidencias_disponibles": evidencias_disponibles,
        "evidencias_requeridas": {"ev4_1", "ev4_2", "ev4_3", "ev4_4", "ev4_5"},
        "pregunta": {
            "texto": "¿Cuál es el delito más grave cometido?",
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
        "caso": NodoCaso(
            f"CASO-{random.randint(1000,9999)}", "Hostigamiento coordinado", gravedad,
            [f"{num_cuentas} cuentas del mismo agresor", f"{num_semanas} semanas", "Fingerprint único"],
            "Ley 1273/2009 + hostigamiento", "Proceso penal + medidas de protección",
        ),
        "color_acento": (180, 80, 255),
        "_victima": victima, "_agresor_user": agresor_user, "_agresor_nombre": agresor_nombre,
        "_plataforma": plataforma, "_colegio": colegio, "_gravedad": gravedad,
        "_num_cuentas": num_cuentas, "_num_semanas": num_semanas,
    }


# ─────────────────────────────────────────────────────────────
#  CASO 5 — Grooming / Acoso a menor  ← NUEVO
# ─────────────────────────────────────────────────────────────
def _nivel_grooming(victima, agresor_user, agresor_nombre, plataforma, colegio, gravedad):
    num_semanas = random.randint(3, 8)
    tipo_engaño = random.choice([
        "fingió ser un adolescente de la misma edad",
        "se presentó como un famoso influencer",
        "usó un perfil falso con foto de estudiante",
        "se hizo pasar por un reclutador de talentos",
    ])
    historia = random.choice([
        (f"{agresor_nombre} {tipo_engaño} en {plataforma}.\n"
         f"Ganó la confianza de {victima} durante {num_semanas} semanas\n"
         f"antes de solicitar información personal comprometedora."),
        (f"A través de {plataforma}, {agresor_user} {tipo_engaño}.\n"
         f"Después de {num_semanas} semanas de conversación,\n"
         f"comenzó a enviar contenido inapropiado a {victima}."),
        (f"{victima} reporta que alguien que {tipo_engaño}\n"
         f"en {plataforma} la contactó por {num_semanas} semanas\n"
         f"y finalmente la presionó para compartir datos privados."),
    ])
    evidencias_disponibles = [
        {"id": "ev5_1", "nombre": "Conversación inicial",
         "descripcion": f"Primeros mensajes donde {agresor_user} {tipo_engaño}.",
         "sprite": "chat", "posicion": (160, 240)},
        {"id": "ev5_2", "nombre": "Perfil falso del agresor",
         "descripcion": f"Cuenta fraudulenta de {agresor_user} en {plataforma}.",
         "sprite": "perfil_falso", "posicion": (400, 210)},
        {"id": "ev5_3", "nombre": "Registro de semanas",
         "descripcion": f"Logs de {num_semanas} semanas de contacto progresivo.",
         "sprite": "logs", "posicion": (650, 260)},
        {"id": "ev5_4", "nombre": "IP del agresor",
         "descripcion": f"Dirección IP rastreada a {agresor_nombre}.",
         "sprite": "ip", "posicion": (290, 360)},
    ]
    return {
        "titulo": "Misión de Emergencia – Grooming Digital",
        "historia": historia,
        "objetivo": "Documenta el contacto progresivo y la identidad falsa del agresor.",
        "evidencias_disponibles": evidencias_disponibles,
        "evidencias_requeridas": {"ev5_1", "ev5_2", "ev5_3", "ev5_4"},
        "pregunta": {
            "texto": "¿Qué tipo de delito describe mejor esta situación?",
            "opciones": [
                "Injuria digital (Art. 220 C.P.)",
                "Grooming – Ley 1336 de 2009 (acto sexual con menor)",
                "Calumnia en redes (Art. 221 C.P.)",
                "Suplantación de identidad – Ley 1273",
            ],
            "correcta": 1,
            "explicacion": (
                "El grooming es el proceso por el que un adulto gana la confianza de\n"
                "un menor con fines de abuso sexual. En Colombia lo tipifica la Ley 1336/2009.\n"
                f"{agresor_nombre} {tipo_engaño} durante {num_semanas} semanas."
            ),
        },
        "caso": NodoCaso(
            f"CASO-{random.randint(1000,9999)}", "Grooming digital", gravedad,
            [f"Conversación de {num_semanas} semanas", f"Perfil falso: {agresor_user}", f"IP: {agresor_nombre}"],
            "Ley 1336 de 2009", "8 a 15 años de prisión",
        ),
        "color_acento": (255, 140, 0),
        "_victima": victima, "_agresor_user": agresor_user, "_agresor_nombre": agresor_nombre,
        "_plataforma": plataforma, "_colegio": colegio, "_gravedad": gravedad,
        "_num_semanas": num_semanas,
    }


# ─────────────────────────────────────────────────────────────
#  CASO 6 — Extorsión / Sextorsión  ← NUEVO
# ─────────────────────────────────────────────────────────────
def _nivel_extorsion(victima, agresor_user, agresor_nombre, plataforma, colegio, gravedad):
    monto = random.randint(50, 500) * 1000
    tipo_amenaza = random.choice([
        "publicar fotos privadas de la víctima",
        "enviar capturas comprometedoras a su familia",
        "difundir información personal en grupos masivos",
        "hackear sus otras cuentas si no pagaba",
    ])
    historia = random.choice([
        (f"{agresor_user} amenazó con {tipo_amenaza}\n"
         f"si {victima} no transfería ${monto:,} COP.\n"
         f"Usó {plataforma} para enviar las amenazas."),
        (f"Tras obtener acceso a imágenes privadas de {victima},\n"
         f"{agresor_nombre} exigió ${monto:,} COP amenazando con\n"
         f"{tipo_amenaza} a través de {plataforma}."),
        (f"{victima} denuncia que {agresor_user} la contactó por {plataforma}\n"
         f"amenazando con {tipo_amenaza}.\n"
         f"La extorsión incluía una demanda de ${monto:,} COP."),
    ])
    evidencias_disponibles = [
        {"id": "ev6_1", "nombre": "Mensaje de amenaza",
         "descripcion": f"Mensaje de {agresor_user} exigiendo ${monto:,} COP.",
         "sprite": "captura", "posicion": (160, 250)},
        {"id": "ev6_2", "nombre": "Captura del material",
         "descripcion": "Material que el agresor amenazó con publicar.",
         "sprite": "post", "posicion": (400, 220)},
        {"id": "ev6_3", "nombre": "Historial de transferencias",
         "descripcion": "Registro de intentos de pago forzados.",
         "sprite": "historial", "posicion": (650, 270)},
        {"id": "ev6_4", "nombre": "IP del agresor",
         "descripcion": f"IP rastreada a {agresor_nombre}.",
         "sprite": "ip", "posicion": (280, 370)},
    ]
    return {
        "titulo": "Misión de Emergencia – Extorsión Digital",
        "historia": historia,
        "objetivo": "Documenta las amenazas y rastrea al extorsionista.",
        "evidencias_disponibles": evidencias_disponibles,
        "evidencias_requeridas": {"ev6_1", "ev6_2", "ev6_3", "ev6_4"},
        "pregunta": {
            "texto": "¿Cuál es el delito primario en este caso?",
            "opciones": [
                "Calumnia (Art. 221 C.P.)",
                "Extorsión (Art. 244 C.P.) + Violación de datos – Ley 1273",
                "Injuria digital (Art. 220 C.P.)",
                "Hostigamiento digital",
            ],
            "correcta": 1,
            "explicacion": (
                "La extorsión digital combina el Art. 244 del Código Penal (extorsión)\n"
                "con la Ley 1273 de 2009 (delitos informáticos: interceptación de datos).\n"
                f"{agresor_nombre} exigió ${monto:,} COP amenazando con {tipo_amenaza}."
            ),
        },
        "caso": NodoCaso(
            f"CASO-{random.randint(1000,9999)}", "Extorsión digital", gravedad,
            [f"Mensaje de amenaza", f"Exigencia de ${monto:,}", f"IP: {agresor_nombre}"],
            "Art. 244 C.P. + Ley 1273/2009", "6 a 15 años de prisión",
        ),
        "color_acento": (255, 60, 200),
        "_victima": victima, "_agresor_user": agresor_user, "_agresor_nombre": agresor_nombre,
        "_plataforma": plataforma, "_colegio": colegio, "_gravedad": gravedad,
        "_monto": monto,
    }


# ── Función principal ────────────────────────────────────────────────────────

# Pool de generadores — se rota para evitar repetir el mismo caso dos veces seguidas
_GEN_POOL = [
    _nivel_injuria, _nivel_calumnia, _nivel_suplantacion,
    _nivel_hostigamiento, _nivel_grooming, _nivel_extorsion,
]
_last_gen = None


def generar_caso_minijuego():
    """Genera un caso aleatorio del Lab1 para usar como minijuego en Lab2.
    Evita repetir el mismo tipo de caso dos veces seguidas."""
    global _last_gen
    pool = [g for g in _GEN_POOL if g is not _last_gen]
    gen = random.choice(pool)
    _last_gen = gen

    victima      = random.choice(_VICTIMAS)
    agresor_user = random.choice(_AGRESORES_USUARIO)
    agresor_nom  = random.choice(_AGRESORES_NOMBRE)
    plataforma   = random.choice(_PLATAFORMAS)
    colegio      = random.choice(_COLEGIOS)
    gravedad     = random.randint(*random.choice(_RANGOS_GRAVEDAD))

    return gen(victima, agresor_user, agresor_nom, plataforma, colegio, gravedad)
