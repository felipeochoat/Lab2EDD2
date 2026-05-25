# 🌐 NetGuardian — Diseño Narrativo de Pantallas Cinemáticas
> Universidad del Norte · Estructura de Datos II · Laboratorio 2 · 2026  
> Director narrativo / Diseñador UX · Documento de referencia

---

# MISIÓN 1 — Rastros del Acoso

## Título Cinemático
**RASTROS DEL ACOSO**

## Subtítulo
*"Cada mensaje tiene un origen."*

## Narrativa
Alguien en la red está sufriendo en silencio.

Mensajes de odio comenzaron a aparecer hace 48 horas y ya se han propagado a decenas de usuarios. La víctima está paralizada, sin saber de dónde viene el ataque ni cómo detenerlo.

No actúan solos. El acoso viaja de nodo en nodo como una infección digital — cada usuario infectado lo reenvía al siguiente, amplificando el daño. Lo que empezó en un solo punto ya es una red entera contaminada.

Tu trabajo: trazar ese camino. Seguir el rastro hasta el inicio. Hasta quien encendió la mecha.

## Cómo se usa el algoritmo en esta misión

**Rastreo por capas [1]:** Imagina arrojar una piedra al agua — las ondas se expanden en círculos. Así funciona esta herramienta: parte del punto de investigación y explora la red por niveles, todos los usuarios directamente conectados primero, luego los de ellos, luego los de ellos. Perfecta para mapear qué tan lejos llegó el odio y encontrar su centro.

**Rastreo profundo [2]:** En lugar de expandirse, esta herramienta elige un camino y lo sigue hasta el fondo antes de explorar otro. Como seguir un hilo hasta el final del ovillo. Ideal para descubrir cadenas específicas de propagación — quién le pasó el mensaje a quién.

## Objetivo
`OBJETIVO: Identifica el nodo origen del acoso antes de que más usuarios sean afectados.`

## Texto del botón
**INICIAR INVESTIGACIÓN**

## Dirección artística
**Composición:** Pantalla dividida conceptualmente en dos zonas — la mitad superior muestra una red de nodos flotando en un espacio cibernético oscuro, con conexiones pulsantes en rojo. La mitad inferior contextualiza la narrativa con texto tipográfico en capas.

**Iluminación:** Fondo casi negro (`#06080A`), con fuentes de luz puntual roja emanando de un nodo central — el origen del acoso, oculto entre los demás. Las conexiones entre nodos brillan en rojo intermitente, como cables de alta tensión.

**Colores:** Rojo dominante (`#FF2A4A`) como color del peligro y la toxicidad. Amarillo dorado (`#FFE44A`) para los textos de alerta y objetivo. Azules oscuros para el fondo. Partículas blancas frías flotando hacia arriba.

**Interfaz holográfica:** El número de misión aparece en la esquina superior izquierda como etiqueta de sistema (`MISIÓN 01`) en tipografía monoespaciada, con una línea horizontal que lo separa del contenido — estética de terminal de hacking.

**Nodos de red:** 18–22 nodos flotantes en el fondo, de tamaño variable (3–10px), con conexiones translúcidas entre los más cercanos. Uno de ellos pulsa más intensamente en rojo — insinúa sin revelar el origen.

**Glitch:** Al abrir la pantalla, 0.5 segundos de glitch horizontal intenso — barras de ruido rojo desplazadas — que se estabilizan rápidamente, como si el sistema detectara una amenaza.

**Cámara:** Estática, pero con micro-movimiento de los nodos flotantes. Sensación de red viva pero amenazante.

## Animaciones y efectos
- **Fade in negro:** 40 frames (~0.67s) de oscuridad total que se abre gradualmente.
- **Glitch de apertura:** 8 frames de barras horizontales desplazadas aleatoriamente en rojo con baja opacidad. Establece la tensión inmediatamente.
- **Reveal del título:** El texto `RASTROS DEL ACOSO` aparece letra a letra (o en fade rápido) con un halo de glow rojo detrás que se expande y luego se estabiliza.
- **Texto narrativo:** Cada línea se revela en secuencia con un fade-in suave, con retardo de ~6 frames entre líneas. Da sensación de que la IA del sistema está "escribiendo" el briefing en tiempo real.
- **Nodos de fondo:** Movimiento lento y continuo. Las conexiones entre nodos cercanos pulsan con opacidad variable — efecto de red viva.
- **Panel de algoritmo:** Aparece con borde izquierdo en rojo (barra vertical de acento) y fondo rojo translúcido muy sutil. Las líneas de texto se revelan en secuencia.
- **Botón CTA:** Pulsa suavemente (escala o brillo) con frecuencia de ~0.08 rad/frame. Borde rojo animado.
- **Barra de progreso:** Línea horizontal en la parte inferior que crece de izquierda a derecha durante los ~10s de duración.
- **Partículas:** 60 partículas pequeñas (1–3px) en blanco frío y rojo tenue flotando hacia arriba lentamente.

## Sonido y música
- **Ambiente base:** Drone electrónico bajo y tenso. Frecuencia de ~60Hz con modulación lenta — sensación de sistema sobrecargado.
- **Apertura:** Sonido de interferencia digital corto (0.3s) — coincide con el glitch visual.
- **Aparición del título:** Sintetizador de ataque suave, nota grave en Re menor.
- **Reveal de texto:** Blips de terminal muy suaves (tipo "tick" de código) para cada línea que aparece.
- **Bucle de fondo:** Música ambient cyberpunk de tensión media — sintetizadores oscuros, pulsos de bajo, sin percusión agresiva. Estilo: Perturbator, Carpenter Brut (sección de build-up).
- **Hover del botón:** Clic digital corto y limpio.
- **Transición al juego:** Fade out de 1.5s + sonido de "conexión establecida" — como abrir una puerta digital.

## Frase final
*"El silencio también deja rastros."*

---

# MISIÓN 2 — Ruta Segura

## Título Cinemático
**RUTA SEGURA**

## Subtítulo
*"No toda conexión es segura."*

## Narrativa
La víctima está completamente aislada.

Cada conexión directa ha sido contaminada por mensajes tóxicos. Mandarle apoyo por la ruta equivocada podría exponerla aún más — los acosadores monitorean las rutas obvias.

Hay aliados en la red — usuarios que quieren ayudar, que tienen los mensajes correctos, la empatía necesaria — pero están dispersos. Entre ella y ellos hay caminos llenos de obstáculos. Algunos mucho más peligrosos que otros.

Necesitas encontrar el camino más seguro. El que minimice el riesgo y lleve apoyo emocional hasta ella antes de que sea demasiado tarde. Cada segundo que pasa, el aislamiento se profundiza.

## Cómo se usa el algoritmo en esta misión

**Navegación de menor riesgo [3]:** Como un GPS que no solo busca el camino más corto, sino el más seguro. Esta herramienta evalúa cada posible ruta hasta la víctima y le asigna un "costo" basado en cuánta toxicidad hay en cada conexión. Luego calcula cuál es el trayecto que acumula menos peligro. No siempre es el más directo — a veces el camino más largo es el más limpio.

## Objetivo
`OBJETIVO: Encuentra el camino de menor riesgo emocional hasta la víctima.`

## Texto del botón
**TRAZAR RUTA SEGURA**

## Dirección artística
**Composición:** Red de nodos con un nodo azul prominente (la víctima) en el centro-derecha de la pantalla, rodeado de conexiones en rojo tenue. En el fondo izquierdo, nodos verdes (aliados) esperan con un brillo cálido. El espacio entre ellos es oscuro, lleno de conexiones potencialmente peligrosas.

**Iluminación:** Azul dominante (`#00B4FF`) como color de esperanza. Verde (`#00FF88`) como color de apoyo y alivio. El contraste crea una sensación de "luz al final del túnel". El fondo permanece oscuro pero con un gradiente sutil hacia el azul oscuro.

**Interfaz holográfica:** Los nodos del fondo muestran "pesos" numéricos en sus conexiones — pequeños valores flotantes que representan el nivel de riesgo. Estética de mapa de calor digital.

**Atmósfera:** Más serena que la Misión 1 pero con urgencia latente. La víctima está en peligro, pero hay esperanza. La paleta fría transmite tanto la frialdad del aislamiento como la claridad del objetivo.

## Animaciones y efectos
- **Fade in:** Igual que Misión 1 pero en azul oscuro en lugar de negro puro.
- **Glitch de apertura:** Más suave. Barras azules frías, cortas, que se estabilizan rápido.
- **Red de fondo:** Nodos verdes y azules en movimiento lento. Las conexiones entre nodos lejanos muestran pulsos de energía que viajan a lo largo de las líneas — como señales de datos.
- **Reveal del título:** En azul con halo de glow azul expandiéndose.
- **Panel de algoritmo:** Borde izquierdo en azul, con pequeños íconos de ">" indicando dirección de rutas.
- **Partículas:** Color azul-blanco, flotando hacia arriba con movimiento más ordenado que en M1 — menos caótico, más esperanzador.
- **Botón:** Pulso suave en azul-verde degradado.

## Sonido y música
- **Ambiente:** Más limpio que M1. Pulsos suaves de sintetizador, casi meditativo pero con tensión.
- **Apertura:** Interferencia corta, luego silencio de 0.5s antes de que entre la música — el silencio representa el aislamiento de la víctima.
- **Música de fondo:** Electrónica ambient con esperanza. Arpegio lento en escala mayor. Algo parecido a la atmósfera de "Journey" (el videojuego) pero con estética más oscura.
- **Blips de texto:** Más suaves y espaciados que en M1. Transmite calma calculada.

## Frase final
*"El apoyo llega más lejos por el camino correcto."*

---

# MISIÓN 3 — Reconstruir la Red

## Título Cinemático
**RECONSTRUIR LA RED**

## Subtítulo
*"Confiar de nuevo cuesta. Hazlo posible."*

## Narrativa
El acoso no solo lastima personas. Destruye comunidades.

Vínculos que tardaron meses en construirse se rompieron en días. Usuarios que eran amigos ahora se bloquean entre sí. Grupos enteros de personas que compartían intereses, apoyo mutuo y conversaciones sanas, ahora están fragmentados por el miedo y la desconfianza.

La red social está rota. Hay comunidades aisladas que no pueden comunicarse ni recibir apoyo. Los aliados no pueden llegar a las víctimas. Los testigos no pueden hablar.

Tu misión: reconstruir los puentes. Restaurar conexiones usando los mínimos recursos necesarios — porque cada vínculo que reconstruyas requiere tiempo, esfuerzo y confianza. Cada enlace que restaures es una persona que vuelve a sentir que no está sola.

## Cómo se usa el algoritmo en esta misión

**Reconstrucción mínima [4]:** Piensa en una ciudad después de un desastre. No puedes reconstruir todas las carreteras a la vez — necesitas identificar cuáles son las rutas mínimas para que cada barrio quede conectado con el resto, usando los materiales justos. Esta herramienta hace exactamente eso: selecciona los vínculos más esenciales para mantener conectada toda la comunidad, sin malgastar recursos en conexiones redundantes.

## Objetivo
`OBJETIVO: Restaura la red comunitaria usando la menor cantidad de conexiones posibles.`

## Texto del botón
**RECONSTRUIR CONEXIONES**

## Dirección artística
**Composición:** Red inicialmente fragmentada — grupos de nodos aislados entre sí, con espacios vacíos que representan las conexiones perdidas. Verde dominante, con nodos que "esperan" ser conectados. La composición es más "abierta" que las misiones anteriores — más espacio vacío para enfatizar la desconexión.

**Iluminación:** Verde como color principal de esperanza y restauración (`#00FF88`). Azul secundario para los nodos de víctimas esperando apoyo. El verde es más cálido aquí — hay algo de alivio, de reconstrucción, no solo de investigación.

**Animación especial:** En el fondo, algunas conexiones rotas se ven como líneas discontinuas o puntos flotantes que no llegan a unirse — representan visualmente lo que el jugador necesita reparar.

**Atmósfera:** Esperanzadora pero nostálgica. Hay pérdida, pero también posibilidad. La paleta verde-azul transmite recuperación en proceso.

## Animaciones y efectos
- **Fade in:** Verde oscuro emergiendo del negro.
- **Glitch de apertura:** Mínimo — solo 3–4 frames de interferencia verde suave. Esta misión es menos agresiva visualmente.
- **Red de fondo:** Nodos en grupos aislados. Entre los grupos, las "conexiones rotas" se representan como líneas punteadas o partículas que no logran unirse — visual muy específico y cargado de significado.
- **Reveal del título:** Verde puro con glow expansivo.
- **Partículas:** Verde y azul, algunas de ellas "buscándose" entre sí con movimiento errático.
- **Botón:** Verde con pulso de energía que se expande hacia afuera — como enviar una señal de conexión.

## Sonido y música
- **Ambiente:** Más cálido. Piano digital suave mezclado con sintetizadores — humanidad dentro de la tecnología.
- **Apertura:** Sin glitch de audio fuerte. Silencio breve, luego entrada gradual de música.
- **Música:** Electrónica ambient con ciertos momentos melódicos reconocibles — transmite que aquí hay personas reales, no solo datos.
- **Blips:** Sonidos de "conexión establecida" suaves — como notificaciones positivas.

## Frase final
*"La confianza se reconstruye un vínculo a la vez."*

---

# MISIÓN 4 — Control del Impacto

## Título Cinemático
**CONTROL DEL IMPACTO**

## Subtítulo
*"Corta el flujo. Detén la marea."*

## Narrativa
La toxicidad está desbordada.

Bots, cuentas falsas y acosadores coordinados han abierto canales de odio a través de toda la red simultáneamente. El volumen de contenido dañino es insostenible — miles de mensajes por hora atravesando la red en todas direcciones.

Pero no puedes cerrar todo. Cerrar canales legítimos destruiría la comunidad que intentas proteger. Necesitas algo más preciso: identificar exactamente por dónde fluye MÁS odio y cortar esos puntos estratégicos sin colapsar la red entera.

Una intervención quirúrgica. Precisa. Calculada. Cada segundo que pasa, más usuarios son dañados por la inundación de toxicidad.

## Cómo se usa el algoritmo en esta misión

**Análisis de flujo máximo [5]:** Imagina una red de tuberías donde el agua es el odio. Esta herramienta calcula cuánto "odio" puede fluir entre el origen del acoso y la víctima, usando todos los canales disponibles simultáneamente. Al conocer ese número máximo de flujo, también identifies los "cuellos de botella" — los puntos donde si intervienes, cortas la mayor cantidad de toxicidad de un solo golpe sin tocar los canales limpios.

## Objetivo
`OBJETIVO: Calcula el flujo máximo de toxicidad y neutraliza los canales críticos.`

## Texto del botón
**NEUTRALIZAR AMENAZA**

## Dirección artística
**Composición:** La pantalla más visualmente intensa de las cinco. Rojo y púrpura dominan — toxicidad máxima. Los nodos de la red están conectados por múltiples líneas de flujo pulsantes, como corrientes de lava digital moviéndose en tiempo real. El centro de la pantalla muestra el "cuello de botella" — un punto donde todas las líneas convergen, brillando intensamente.

**Iluminación:** Púrpura oscuro (`#B44EFF`) como color principal de manipulación y flujo masivo. Rojo como acento de toxicidad. Las líneas de flujo muestran un gradiente rojo→púrpura animado que se mueve en dirección del flujo.

**Interfaz holográfica:** Números de "capacidad" flotando sobre las conexiones — como indicadores de ancho de banda en un monitor de red. Algunos parpadean en rojo cuando están al máximo.

**Glitch:** El más intenso de todas las misiones — la red está bajo ataque. Múltiples glitches durante los primeros frames, incluyendo interferencia de color (chromatic aberration exagerada en rojo/azul).

**Atmósfera:** Urgencia máxima. Es una crisis activa. El jugador siente que no hay tiempo que perder.

## Animaciones y efectos
- **Glitch de apertura:** El más fuerte. 15 frames de interferencia intensa, barras de desplazamiento horizontal grandes, flash de color rojo completo en frames 2–4.
- **Red de fondo:** Las líneas entre nodos muestran flujo animado — partículas pequeñas viajando a lo largo de las conexiones en dirección roja→púrpura. Como ver el tráfico en tiempo real.
- **Reveal del título:** Púrpura con destellos rojo en el glow. El texto tiembla ligeramente (micro-glitch) antes de estabilizarse.
- **Panel de algoritmo:** Fondo púrpura translúcido con borde en púrpura. Las líneas de texto aparecen como si fueran datos de un monitor de red.
- **Partículas:** Rojas y púrpuras, moviéndose más rápido que en otras misiones — urgencia visual.
- **Botón:** "NEUTRALIZAR AMENAZA" en rojo, con efecto de pulso agresivo — como una alarma.

## Sonido y música
- **Ambiente:** El más tenso de todas las misiones. Bass pesado, frecuencias bajas, como el zumbido de servidores sobrecargados.
- **Apertura:** Sonido de alarma digital corta + glitch de audio (distorsión de 0.5s).
- **Música:** Electrónica oscura con BPM más alto (~120 BPM). Percusión industrial suave. Estilo: HEALTH, NIN.
- **Blips:** Más rápidos, más agresivos — como notificaciones de sistema crítico.
- **Efectos de flujo:** Sonido sutil de "datos fluyendo" — ruido blanco muy filtrado y modulado.

## Frase final
*"El odio también tiene puntos débiles."*

---

# MISIÓN 5 — Red Segura: Misión Final

## Título Cinemático
**RED SEGURA**

## Subtítulo
*"Todo lo que aprendiste. Úsalo ahora."*

## Narrativa
La red está colapsando.

Un ataque coordinado de gran escala ha desencadenado ciberacoso masivo, desinformación viral y el bloqueo de canales de apoyo simultáneamente. No es un incidente aislado — es una operación orquestada para destruir la comunidad desde adentro.

No hay tiempo para estrategias parciales. No puedes solo rastrear, o solo reconstruir, o solo cortar flujos. Necesitas desplegar TODO tu arsenal de investigación digital — cada herramienta que dominaste en las misiones anteriores — de forma coordinada, en el orden correcto, contra múltiples amenazas al mismo tiempo.

Esta es la operación final. Si tienes éxito, miles de usuarios estarán seguros. La red social podrá seguir siendo un espacio de conexión humana real. Si fallas, el ecosistema digital colapsa.

NetGuardian depende de ti.

## Cómo se usa el algoritmo en esta misión

**Arsenal completo activado [1] [2] [3] [4] [5]:**

Usa el **rastreo por capas y profundo** para localizar los múltiples focos de origen del ataque coordinado. Usa la **navegación segura** para crear rutas de apoyo hacia todas las víctimas identificadas. Usa la **reconstrucción mínima** para restaurar los vínculos comunitarios destruidos. Usa el **análisis de flujo** para cortar los canales de toxicidad masiva.

Cada herramienta tiene su momento. Leer la situación y elegir la correcta es parte de la misión.

## Objetivo
`OBJETIVO: Ejecuta los 5 algoritmos y restaura el ecosistema digital por completo.`

## Texto del botón
**INICIAR OPERACIÓN FINAL**

## Dirección artística
**Composición:** La pantalla más épica del juego. Amarillo dorado (`#FFE44A`) dominante — el color de la investigación activa y el triunfo inminente. La red de fondo es la más densa y compleja — docenas de nodos de diferentes colores (rojo, azul, verde, púrpura) todos interconectados, representando el caos que hay que resolver.

**Iluminación:** Dorado como color principal de resolución y dominio. Verde como secundario de esperanza. El fondo tiene un gradiente sutil de negro a azul marino muy oscuro — la oscuridad que está a punto de ceder.

**Interfaz holográfica:** Los 5 íconos de herramientas aparecen en el panel de algoritmo, cada uno con su color correspondiente, como un arsenal de herramientas listo para ser desplegado. Pequeñas animaciones de cada algoritmo (onda BFS, rama DFS, ruta Dijkstra, árbol Kruskal, flujo Ford-Fulkerson) en íconos miniatura.

**Atmósfera:** Épica. El momento culminante. Hay urgencia pero también confianza — el jugador ha llegado hasta aquí, sabe lo que hace. La paleta dorada transmite que la victoria es posible.

**Cámara:** Por primera vez, un micro-movimiento lento (casi imperceptible) de toda la red de fondo — como si respirara.

## Animaciones y efectos
- **Fade in:** Dorado-negro. El más lento de todos (~50 frames) — el momento pide ser saboreado.
- **Glitch de apertura:** Corto pero multicromático — barras rojas, azules y verdes simultáneamente. Refleja el caos de todos los tipos de amenaza activos a la vez.
- **Red de fondo:** La más densa. Nodos de todos los colores en movimiento. Algunas conexiones pulsan en rojo (activas y peligrosas), otras en verde (aliadas), otras en azul (víctimas).
- **Reveal del título:** Dorado puro, el glow más grande del juego — se expande hasta casi tocar los bordes de la pantalla.
- **Íconos de herramientas:** Aparecen en secuencia, cada uno con su animación característica miniatura — refuerza el arsenal acumulado.
- **Partículas:** Multicolor — de todos los algoritmos anteriores mezclados. El caos visual se convierte en poesía.
- **Botón:** "INICIAR OPERACIÓN FINAL" en dorado, con el pulso más lento y solemne de todos — no hay prisa, pero la decisión es irreversible.

## Sonido y música
- **Ambiente:** Silencio durante 2 segundos al abrir. Luego, entrada gradual de la música más compleja del juego.
- **Apertura:** Silencio → nota grave de piano → construcción lenta de la música.
- **Música:** Electrónica épica con elementos orquestales sutiles. BPM medio (~90). Sensación de última misión en un videojuego narrativo — mezcla de tensión, esperanza y determinación. Referencia: "The Last of Us" soundtrack mezclado con electrónica de Kavinsky.
- **Blips:** Los más variados — un blip diferente por cada herramienta que se menciona en el texto, representando su "sonido" característico.
- **Transición al juego:** El fade out más largo y dramático. Un acorde final antes de que empiece el gameplay.

## Frase final
*"La red no se protege sola. Tú eres NetGuardian."*

---

## Implementación técnica

Las pantallas están implementadas en `view/mission_intro.py` como la clase `MissionIntroScreen`.

**Uso desde el controlador:**
```python
from view.mission_intro import MissionIntroScreen

intro = MissionIntroScreen(screen, mission_id=0)  # 0–4

# En el event loop:
result = intro.handle_event(event)   # devuelve "continue" o None
if result == "continue" or intro.done:
    # entrar al gameplay

# En update:
intro.update()

# En draw:
intro.draw()
```

**Integración en `game.py`:**
- `_show_mission_intro()` crea la instancia al iniciar nueva partida, cargar partida y al avanzar de misión.
- `_end_mission_intro()` la destruye y lanza `_show_step("start")` + música de juego.
- El event handler y el update/draw loop detectan `self.mission_intro is not None` y le dan prioridad sobre el resto del renderizado.

**Duración por defecto:** 10 segundos (`DURATION = 600` frames). El jugador puede saltar después de 2 segundos (`SKIP_AFTER = 120` frames) con `SPACE`, `ENTER` o clic en el botón CTA.
