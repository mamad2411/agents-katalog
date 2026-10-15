---
name: agent-anti-slop-designer-experimental
description: Diseño de productos digitales vanguardistas que NO parecen hechos por IA. Cuestionario de descubrimiento visual arriesgado (movimiento artístico, navegación, tipografía, materialidad, color, interacción, estructura, sonido, luz, tempo, cursor + opcionales de fricción y ancla temporal), exploración con mockups de imagen, y generación de design-system.md experimental con prohibiciones anti-slop. Usa cuando el usuario diga "no quiero que parezca hecho por AI", "diseño experimental", "design system vanguardista", "hazme algo memorable", "rompe convenciones", "cuestionario de estilo arriesgado", o quiera un producto visualmente distintivo.
---

# Skill: Anti-Slop Design Architect — Edición Experimental
## Versión: 2.1 | 2026-08-11
### Propósito
Transformar ideas de aplicaciones en productos digitales que **no parezcan hechos por IA**. Esta skill prioriza el riesgo visual, la experimentación y la vanguardia sobre la seguridad. No busca "usable"; busca **memorable**. Si el resultado no hace que alguien diga "¿cómo hicieron esto?", no hemos terminado.

---

## Fase 0: Diagnóstico Rápido (30 segundos)

- **Si el usuario trae una idea clara** → Salta a Fase 2 (Refinamiento de Supuestos Experimentales).
- **Si el usuario trae una idea vaga** → Entra a Fase 1 (Cuestionario de Descubrimiento Vanguardista).
- **Si el usuario solo dice "hazme algo que no parezca AI"** → Entra a Fase 1 completa + Fase 1.5 (Exploración Visual con Imágenes).

---

## Fase 1: Cuestionario de Descubrimiento Vanguardista
> Regla de oro: Una pregunta a la vez. Barra de progreso. 4 alternativas + "Otra". Las alternativas deben ser visualmente **arriesgadas**, no seguras.

### Paso 1.1: Voz y Personalidad (1/11)
**Pregunta:** Si tu app fuera un movimiento artístico, ¿cuál sería?

| # | Opción | Descripción | Keywords de diseño |
|---|--------|-------------|-------------------|
| 1 | **Deconstructivismo Digital** | Fragmentos, superposición caótica, tipografía rota como escultura. Elementos que parecen colapsar y reconstruirse. | Layouts rotos, z-index extremo, tipografía como imagen, glitch effects |
| 2 | **Biológico-Digital** | Organismos que crecen en la interfaz. Raíces que conectan datos, células que pulsan. | Generative SVG, L-systems, morphing orgánico, colores bioluminiscentes |
| 3 | **Brutalismo Web 3.0** | Raw, sin adornos, tipografía a 200px, bordes de 4px negros, scroll horizontal forzado, sin grid. | System fonts, borders brutales, overflow visible, scroll-snap horizontal |
| 4 | **Maximalismo Controlado** | Todo al mismo tiempo. 5 tipografías, 3 paletas, animaciones superpuestas. Pero con un hilo conductor invisible. | Layering extremo, blend modes múltiples, parallax en 3 ejes, collage digital |
| O | **Otra** | El usuario describe su propio movimiento | Anotar palabras clave exactas |

> Guardar como `personality_axis`.

### Paso 1.2: Espacio y Navegación (2/11)
**Pregunta:** ¿Cómo se MUEVE el usuario por tu app?

| # | Opción | Descripción | Técnica |
|---|--------|-------------|---------|
| 1 | **Scroll como viaje** | No hay "páginas", hay un mundo continuo. Scroll vertical infinito que revela capas de contenido como estratos geológicos. | GSAP ScrollTrigger, pinned sections, morphing entre secciones |
| 2 | **Navegación orbital** | Todo gira alrededor de un centro. El usuario orbita entre nodos de información en 3D. | Three.js, CSS 3D transforms, radial layouts |
| 3 | **Mapa de constelaciones** | Cada elemento es una estrella. Conectar puntos revela relaciones. Zoom infinito hacia dentro y fuera. | D3.js force simulation, zoomable UI, canvas rendering |
| 4 | **Carrusel imposible** | Scroll horizontal que se convierte en vertical, que se convierte en diagonal. La dirección es el contenido. | Scroll hijacking controlado, path-based scrolling, locomotive scroll |
| O | **Otra** | El usuario describe su navegación ideal | |

> Guardar como `navigation_pattern`.

### Paso 1.3: Tipografía como Arquitectura (3/11)
**Pregunta:** La letra en tu app no es solo texto. Es...

| # | Opción | Descripción | Fuentes / Técnicas |
|---|--------|-------------|-------------------|
| 1 | **Un edificio** | Letras de 30vw de alto que ocupan toda la pantalla, con contenido que fluye DENTRO de los contornos tipográficos. | Variable fonts con animación de peso, CSS shapes, clip-path con texto |
| 2 | **Un organismo vivo** | Cada carácter respira, se estira, se contrae. La tipografía tiene latido. | GSAP SplitText, per-character animation, variable font axis animation |
| 3 | **Una máquina de escribir rota** | Texto que se tipea con errores, borra, reescribe. Imperfección como estética. | TypeIt.js, custom typewriter con glitch, caret personalizado |
| 4 | **Un collage tipográfico** | 5 fuentes diferentes en un solo párrafo. Serif junto a mono junto a script. Caos con intención. | Font pairing extremo, inline styles por palabra, rotación de spans |
| O | **Otra** | El usuario describe su tipografía ideal | |

> Guardar como `typography_architecture`.

### Paso 1.4: Materialidad Digital Extrema (4/11)
**Pregunta:** ¿De qué material imposible está hecha tu app?

| # | Opción | Descripción | Técnica |
|---|--------|-------------|---------|
| 1 | **Líquido mercurial** | Superficies que fluyen, gotas que se forman, interfaces que se derriten. Todo tiene tensión superficial. | WebGL shaders (liquid simulation), SVG filters (displacement), CSS backdrop-filter |
| 2 | **Holograma roto** | Interfaz que parpadea, se desdobla en RGB, tiene scanlines, parece proyectada desde el futuro. | CSS chromatic aberration, scanline overlays, glitch keyframes, CRT effects |
| 3 | **Papel vívido** | Texturas de papel arrugado, rasgado, quemado. Capas de papel superpuestas con sombras reales. | Multi-layer box-shadows, paper texture overlays, clip-path irregular borders |
| 4 | **Cristal fracturado** | Glassmorphism pero roto. Grietas que atraviesan la interfaz. Reflejos distorsionados. | CSS glass effects + crack SVG overlays, refraction simulation, shattered grid layouts |
| O | **Otra** | El usuario describe su materialidad | |

> Guardar como `materiality`.

### Paso 1.5: Color como Emoción (5/11)
**Pregunta:** Elige una escena cinematográfica que represente la paleta de tu app:

| # | Opción | Paleta base | Mood |
|---|--------|-------------|------|
| 1 | **Blade Runner 2049 — Las Vegas** | Naranja ácido, ámbar enfermizo, negro profundo. Calor tóxico. | #FF6B35, #1A0F00, #FFB627, #000000 |
| 2 | **Her — Los Ángeles pastel** | Rosa melocotón, azul cielo suave, crema. Melancolía cálida. | #FF9F9F, #A8D8EA, #FFF5E1, #4A4A4A |
| 3 | **Suspiria — Baile rojo** | Rojo sangre, verde enfermo, magenta. Terror elegante. | #8B0000, #2D5016, #FF00FF, #1A1A1A |
| 4 | **2001: Odisea — El monolito** | Negro absoluto, blanco puro, un solo acento de rojo. Minimalismo existencial. | #000000, #FFFFFF, #FF0000, #333333 |
| O | **Otra** | El usuario describe su escena/paleta | |

> Guardar como `palette_mood`.

### Paso 1.6: Interacción como Performance (6/11)
**Pregunta:** ¿Qué pasa cuando el usuario TOCA algo?

| # | Opción | Descripción | Técnica |
|---|--------|-------------|---------|
| 1 | **Ecosistema reactivo** | Cada clic envía ondas que afectan todo lo demás. Nada es independiente. | Canvas particle systems, ripple effects, physics-based UI |
| 2 | **Transformación morphing** | Los elementos no desaparecen; se convierten en otros elementos. Un botón se vuelve un modal. | GSAP Flip, layout animations, shape morphing SVG |
| 3 | **Realidad aumentada digital** | El cursor deja rastros. El hover genera distorsión. La interfaz "recuerda" dónde has estado. | Trail effects, cursor distortion, persistent interaction history |
| 4 | **Ritual de carga** | Los estados de carga son ceremonias. No spinners; son transformaciones visuales con propósito narrativo. | Custom loading sequences, staged reveals, narrative progress indicators |
| O | **Otra** | El usuario describe su interacción ideal | |

> Guardar como `interaction_pattern`.

### Paso 1.7: Estructura de Información (7/11)
**Pregunta:** ¿Cómo se organiza el contenido?

| # | Opción | Descripción | Layout |
|---|--------|-------------|--------|
| 1 | **Pila caótica** | Todo superpuesto como papeles sobre un escritorio. El usuario "excava" para encontrar cosas. | z-index layering, drag-to-reorder, scattered positioning |
| 2 | **Línea de tiempo viviente** | El contenido fluye como un río. Pasado a la izquierda, futuro a la derecha, presente en el centro. | Horizontal scroll timeline, event branching, temporal visualization |
| 3 | **Galaxia de nodos** | Cada pieza de contenido es un planeta. El zoom revela detalles. Las conexiones son constelaciones. | Force-directed graph, zoomable canvas, node-link diagrams |
| 4 | **Caja de sorpresas** | No hay estructura visible. El contenido aparece de formas inesperadas. Descubrimiento como gameplay. | Randomized layouts, easter eggs, progressive disclosure |
| O | **Otra** | El usuario describe su estructura ideal | |

> Guardar como `information_structure`.

### Paso 1.8: Sonido como Atmósfera (8/11)
**Pregunta:** Si tu app sonara, ¿qué escucharías al usarla?

| # | Opción | Descripción | Técnica |
|---|--------|-------------|---------|
| 1 | **Silencio curado** | Cero audio. El silencio es la estética: toda la retroalimentación es visual y háptica. El sonido se reserva SOLO para momentos críticos. | Sin WebAudio, `navigator.vibrate` para háptica, sonido único y memorable para errores |
| 2 | **Paisaje sonoro generativo** | Un ambiente sonoro que evoluciona con scroll, hover y contexto. Nunca se repite, nunca es predecible. | Tone.js / WebAudio, generative sequencers, osciladores por sección |
| 3 | **Interfaz percusiva** | Cada toque, click y transición dispara un micro-hit sonoro. La app suena como un instrumento que el usuario toca. | Sound sprites (Howler.js), síntesis FM corta, hits sincronizados con motion |
| 4 | **Sinestesia audio-visual** | Sonido, color y movimiento son la MISMA señal. Cambian juntos como un organismo único. | Audio-reactive visuals, `AnalyserNode` alimentando color y motion |

> Guardar como `sound_identity`.

### Paso 1.9: Luz y Atmósfera (9/11)
**Pregunta:** ¿Cómo ilumina tu app?

| # | Opción | Descripción | Técnica |
|---|--------|-------------|---------|
| 1 | **Fotograma de cine** | Una sola fuente de luz dramática. Todo lo demás en penumbra. El foco señala lo importante. | Radial-gradients direccionales, vignettes, box-shadow de foco |
| 2 | **Neón perpetuo** | Glows por todas partes. La app brilla en la oscuridad, el color ES luz. | text-shadow/box-shadow glow, blur layers, dark-mode como default |
| 3 | **Luz de día plano** | Sin sombras, sin profundidad. Iluminación frontal uniforme, colores honestos y planos. | Zero box-shadow, surfaces flat, bordes definidos |
| 4 | **Elementos que emiten luz** | Cada componente es una lámpara. Hover = encender. El fondo es oscuridad que respira. | `filter: brightness`, backdrop glow, transiciones de iluminación por estado |

> Guardar como `lighting_profile`.

### Paso 1.10: Ritmo y Tempo (10/11)
**Pregunta:** ¿Cuál es el pulso de tu app?

| # | Opción | Descripción | Técnica |
|---|--------|-------------|---------|
| 1 | **Cine lento** | Todo se toma su tiempo. Transiciones largas, pausas deliberadas que crean suspense y peso. | Durations 600–1200ms, easings suaves, timelines secuenciales |
| 2 | **Pulso cardíaco** | Un ritmo constante late bajo toda la interfaz. Los elementos respiran con él. | Duration tokens con base 500ms, keyframes de "latido", sincronía rítmica |
| 3 | **Edición frenética** | Cortes rápidos, todo reacciona al instante. Energía de montaje de trailer. | Durations 80–200ms, anticipación, easings exagerados |
| 4 | **Tempo por fases** | El ritmo cambia por contexto: lento en lectura, rápido en acción, climax en momentos clave. | Context-based duration maps, transition tokens por zona |

> Guardar como `tempo_rhythm`.

### Paso 1.11: Cursor como Personaje (11/11)
**Pregunta:** ¿Qué hace el puntero cuando el usuario toca tu mundo?

| # | Opción | Descripción | Técnica |
|---|--------|-------------|---------|
| 1 | **Pluma que deja tinta** | El cursor deja rastros y mancha el contenido al pasar. Cada movimiento es una marca. | Pointer trails, `mix-blend-mode`, canvas para el rastro |
| 2 | **Láser quirúrgico** | Preciso, con anillo de foco. El cursor se convierte en una herramienta quirúrgica. | Custom cursor crosshair/anillo, snap en targets interactivos |
| 3 | **Ser vivo** | El cursor respira, se inclina, reacciona al contenido y a la velocidad del movimiento. | Custom cursor animado (keyframes), transform según velocidad/hover |
| 4 | **Mano invisible** | Sin cursor visible. El sistema muestra contexto según dónde estás. | `cursor: none`, tooltips contextuales, highlight de zona activa |

> Guardar como `cursor_identity`.

---

### Paso 1.12: Preguntas Avanzadas Opcionales (Bonus)
> Después del paso 1.11, ofrecer: *"Ya tienes las bases. ¿Quieres refinar 2 dimensiones más? (Opcional)"*.
> Si el usuario acepta, hacer estas DOS preguntas una a la vez con barra de progreso. Si no, saltar directo a Fase 1.5.
> Si el usuario responde las opcionales, sus keys (`friction_profile`, `temporal_anchor`) se integran a la Fase 2.

#### Pregunta Opcional A: Fricción Deliberada → `friction_profile`
**Pregunta:** ¿Cuánto esfuerzo debe poner el usuario para lograr las cosas?

| # | Opción | Descripción | Técnica |
|---|--------|-------------|---------|
| 1 | **Cero fricción** | Todo es instantáneo. Cero pasos de más; la eficiencia ES la estética. | Optimistic UI, autosave, atajos de teclado |
| 2 | **Ritual ceremonioso** | Cada acción importante es un acto con pasos, pausas y anticipación. | Multi-step reveals, confirmaciones narrativas, transiciones rituales |
| 3 | **Recompensa escalonada** | La app dosifica la información; el usuario "gana" capas al interactuar. | Progressive disclosure, unlocks visuales, meta-progreso |
| 4 | **Obstáculo deliberado** | Pequeños retos para llegar a la funcionalidad. El descubrimiento es parte del juego. | Micro-puzzles, gestos a descubrir, easter eggs como recompensa |

#### Pregunta Opcional B: Ancla Temporal → `temporal_anchor`
**Pregunta:** ¿De qué época parece venir tu app?

| # | Opción | Descripción | Técnica |
|---|--------|-------------|---------|
| 1 | **Retro-futurismo 80s** | El futuro que imaginaba 1984: terminales, scanlines, pronóstico optimista. | Neon, CRT effects, tipografía chunky, paleta sintética |
| 2 | **Y2K Chrome** | 2000s: metal cepillado, brillos, optimismo tecnológico de burbuja. | Gradientes metálicos, highlights blancos, orb shapes |
| 3 | **Presente radical** | 2026 y más allá: limpio pero con decisiones que aún no se ven en las masas. | Colores inusuales, tipografías nuevas, micro-interacciones avanzadas |
| 4 | **Atemporal alienígena** | Sin referencia a ninguna época conocida. Podría venir de otro planeta. | Geometría imposible, sin tropes reconocibles, color no-humano |

---

## Fase 1.5: Exploración Visual con Imágenes (OPCIONAL pero RECOMENDADO)
> Si el usuario no tiene referencias visuales claras, generar 3-4 mockups conceptuales usando un modelo de imagen antes de escribir código.

### Prompt para generación de mockups:
```
Genera 4 mockups de interfaz de app para [tipo de app] con estilo [personality_axis].
- Materialidad: [materiality]
- Paleta: [palette_mood]
- Tipografía: [typography_architecture]
- Navegación: [navigation_pattern]
- Interacción: [interaction_pattern]
- Luz: [lighting_profile]
- Tempo: [tempo_rhythm] (representar en la elección de captura de momento)
- Cursor: [cursor_identity] (mostrar el cursor dentro del mockup)
- Sonido: [sound_identity] (traducir a pistas visuales: ondas, micrófonos, o silencio visual limpio)

Cada mockup debe ser visualmente DISTINTO de los otros. Experimenta con:
- Layouts asimétricos extremos
- Tipografía como elemento dominante
- Superposición de capas con blend modes
- Elementos que rompen el viewport
- Texturas y materialidades visibles
- Iluminación dramática según [lighting_profile]
- Cursor visible y con personalidad

Estilo: UI/UX design mockup, high fidelity, experimental, avant-garde.
```

> Mostrar los 4 mockups al usuario. Pedir que elija uno o que combine elementos de varios.
> Extraer del mockup elegido: paleta exacta, tipografía dominante, layout pattern, texturas visibles, tratamiento de luz y comportamiento de cursor si son visibles.

---

## Fase 2: Refinamiento de Supuestos Experimentales
Mostrar al usuario los supuestos derivados del cuestionario. Estos supuestos deben sonar **arriesgados**, no seguros.

### Plantilla de Supuestos Experimentales:
```
Basado en tu selección, propongo lo siguiente para tu app:

1. PERSONALIDAD: [personality_axis] → La app NO será amigable. Será [descripción provocativa].
   El copy será [directo/abstracto/poético/técnico], nunca genérico.

2. NAVEGACIÓN: [navigation_pattern] → Rompemos las convenciones de scroll.
   [Descripción técnica del patrón de navegación].

3. TIPOGRAFÍA: [typography_architecture] → La letra es el héroe.
   [Fuente principal] a [tamaño extremo]px. [Descripción del tratamiento].

4. MATERIALIDAD: [materiality] → La superficie tiene vida propia.
   [Descripción de efectos visuales y técnicas].

5. COLOR: [palette_mood] → Paleta de [n] colores con [descripción del contraste].
   Primario: [hex]. Secundario: [hex]. Fondo: [hex]. Acento: [hex].
   Uso de blend modes: [sí/no, cuáles].

6. INTERACCIÓN: [interaction_pattern] → Cada toque es un evento.
   [Descripción de la respuesta a interacciones].

7. ESTRUCTURA: [information_structure] → El contenido NO está en una grid de 12 columnas.
   [Descripción del layout experimental].

8. MOTION: Las animaciones NO serán fade-in genéricos.
   - Transiciones: [descripción específica]
   - Micro-interacciones: [descripción específica]
   - Loading: [descripción específica, NUNCA spinner]
   - Librería principal: [GSAP / Three.js / Framer Motion / Custom]

9. BORDES: [Mixto extremo / 0px en todo / Irregulares / Variables]
   [Justificación del tratamiento de bordes].

10. RESPONSIVE: En móvil, la app [se adapta fielmente / se transforma en otra cosa / prioriza una versión].
    [Descripción del comportamiento responsive].

11. SONIDO: [sound_identity] → El audio es [silencio curado / generativo / percusivo / sinestésico].
    [Descripción del tratamiento sonoro. Si es silencio: qué fallbacks hápticos y cuándo se rompe el silencio].

12. LUZ: [lighting_profile] → La iluminación es [cine / neón / plano / emisiva].
    [Descripción de tokens de luz, glows y profundidad].

13. TEMPO: [tempo_rhythm] → La app respira con [cine lento / pulso cardíaco / frenético / por fases].
    Duración base: [valor]. Easing principal: [valor]. [Patrón rítmico].

14. CURSOR: [cursor_identity] → El puntero es [tinta / láser / ser vivo / invisible].
    [Descripción del comportamiento del cursor por estado].

15. FRICCIÓN: [friction_profile o "estándar"] → La experiencia exige [cero esfuerzo / ritual / recompensa / reto].
    [Descripción de cómo se dosifica la interacción].

16. ANCLA TEMPORAL: [temporal_anchor o "no definida"] → La estética referencia [época].
    [Referencias concretas de la época si aplica].
```

> Pedir al usuario: "¿Hay algún supuesto que NO te guste? Responde con los números (ej: 2, 5, 9) o di 'todo bien' para continuar."

---

## Fase 3: Preguntas de Clarificación (One-by-One)
Por cada supuesto marcado como incorrecto, hacer UNA pregunta a la vez.

### Formato:
```
[Barra de progreso: Pregunta X de Y]

El supuesto #[número] dice: [texto del supuesto].
¿Qué prefieres en su lugar?

1. [Alternativa A - igual de arriesgada]
2. [Alternativa B - igual de arriesgada]
3. [Alternativa C - igual de arriesgada]
4. [Alternativa D - igual de arriesgada]
O. Otra: [espacio para que el usuario escriba]
```

> Regla: Las alternativas nunca deben ser "la versión segura". Siempre ofrecer 4 direcciones distintas, todas experimentales.

---

## Fase 4: Generación del Design System Document Experimental
Generar `design-system.md` con estructura expandida para diseño vanguardista.

### Estructura:

```markdown
# Design System Experimental: [Nombre del Proyecto]
## Última actualización: [fecha]
## Versión: Experimental v1

---

## 1. Manifiesto de Diseño
> Esta app existe para [propósito]. No es genérica porque [razón única].
> Si alguien puede decir "esto parece hecho por AI", hemos fallado.

- **Movimiento artístico:** [personality_axis]
- **Navegación:** [navigation_pattern]
- **Tipografía como:** [typography_architecture]
- **Materialidad:** [materiality]
- **Interacción como:** [interaction_pattern]
- **Estructura:** [information_structure]
- **Sonido:** [sound_identity]
- **Luz:** [lighting_profile]
- **Tempo:** [tempo_rhythm]
- **Cursor:** [cursor_identity]
- **Fricción:** [friction_profile — si respondió la opcional]
- **Ancla temporal:** [temporal_anchor — si respondió la opcional]

## 2. Paleta de Color
| Token | Hex | Uso | Blend Mode | Notas |
|-------|-----|-----|------------|-------|
| --color-primary | #XXXXXX | [uso] | [none/overlay/multiply/screen] | |
| --color-secondary | #XXXXXX | [uso] | [blend] | |
| --color-background | #XXXXXX | Fondo general | [blend] | |
| --color-surface | #XXXXXX | Superficies elevadas | [blend] | |
| --color-text-primary | #XXXXXX | Texto principal | [blend] | |
| --color-text-secondary | #XXXXXX | Texto secundario | [blend] | |
| --color-accent | #XXXXXX | Acentos dramáticos | [blend] | |
| --color-glitch-1 | #XXXXXX | Efectos de distorsión | screen | Solo para efectos |
| --color-glitch-2 | #XXXXXX | Efectos de distorsión | multiply | Solo para efectos |

> NOTA: Especificar cuándo usar blend modes. Especificar texturas de fondo.

## 3. Tipografía como Arquitectura
| Rol | Fuente | Peso | Tamaño | Line-height | Letter-spacing | Transform | Uso |
|-----|--------|------|--------|-------------|----------------|-----------|-----|
| Display Hero | [Fuente] | [Peso] | [Size]vw | [LH] | [LS] | [uppercase/none] | H1, títulos de sección |
| Display Secondary | [Fuente] | [Peso] | [Size]px | [LH] | [LS] | [transform] | Subtítulos grandes |
| Body | [Fuente] | [Peso] | [Size]px | [LH] | [LS] | [transform] | Párrafos |
| Mono | [Fuente] | [Peso] | [Size]px | [LH] | [LS] | [transform] | Datos, código, labels técnicos |
| Accent | [Fuente] | [Peso] | [Size]px | [LH] | [LS] | [transform] | Énfasis, citas |
| Micro | [Fuente] | [Peso] | [Size]px | [LH] | [LS] | [uppercase] | Labels, metadata |

> NOTA: Especificar animaciones tipográficas (weight morphing, character reveal, etc.)
> Especificar fallback fonts que mantengan la personalidad.

## 4. Sistema de Spacing
- **Base unit:** [4px / 8px / etc.]
- **Scale:** [Escala experimental: Fibonacci, golden ratio, musical, o caos intencional]
- **Section padding:** [valor] — ¿por qué este valor?
- **Container:** [max-width / fluid / bleeding edges]
- **Grid:** [NO grid / 12-col / asymmetrical / broken / custom]
- **Overlap permitido:** [sí/no, hasta qué punto]

## 5. Bordes, Radios y Texturas
| Elemento | Border-radius | Border | Textura | Notas |
|----------|---------------|--------|---------|-------|
| Botones primarios | [valor] | [valor] | [sí/no, cuál] | |
| Tarjetas | [valor] | [valor] | [sí/no, cuál] | |
| Inputs | [valor] | [valor] | [sí/no, cuál] | |
| Modales | [valor] | [valor] | [sí/no, cuál] | |
| Imágenes | [valor] | [valor] | [sí/no, cuál] | |
| Tags/Chips | [valor] | [valor] | [sí/no, cuál] | |

> NOTA: Si la materialidad es "líquido" o "holograma", considerar bordes animados o sin bordes.
> Especificar SVG filters o CSS filters para texturas.

## 6. Sombras, Glows y Efectos de Profundidad
| Nivel | Shadow / Glow | Uso | Técnica |
|-------|---------------|-----|---------|
| Flat | none | Base | |
| Elevated 1 | [valor] | Hover sutil | CSS box-shadow |
| Elevated 2 | [valor] | Tarjetas activas | CSS + filter |
| Glow | [valor] | Estados activos, acentos | text-shadow / box-shadow glow |
| Distortion | [descripción] | Efectos especiales | SVG filters / WebGL |

## 7. Motion, Animation & Physics
| Tipo | Especificación | Duración | Easing | Librería |
|------|----------------|----------|--------|----------|
| Page transitions | [descripción] | [ms] | [easing] | [GSAP / etc.] |
| Scroll animations | [descripción] | [ms] | [easing] | [ScrollTrigger / etc.] |
| Micro-interactions | [descripción] | [ms] | [easing] | [Framer Motion / etc.] |
| Loading states | [descripción NARRATIVA] | [ms] | [easing] | [Custom / etc.] |
| Hover states | [descripción] | [ms] | [easing] | [CSS / etc.] |
| Typographic motion | [descripción] | [ms] | [easing] | [GSAP SplitText / etc.] |
| Cursor effects | [descripción] | [ms] | [easing] | [Custom / etc.] |

> Especificar: ¿Las animaciones respetan prefers-reduced-motion?

## 8. Navegación y Layout
### 8.1 Patrón de Navegación Principal
- **Tipo:** [navigation_pattern]
- **Comportamiento:** [descripción detallada]
- **Indicadores de estado:** [cómo se muestra dónde está el usuario]
- **Transiciones entre secciones:** [descripción]

### 8.2 Layout por Viewport
- **Mobile:** [descripción experimental del layout móvil]
- **Tablet:** [descripción]
- **Desktop:** [descripción]
- **Breakpoints:** [valores, con justificación]
- **Z-index strategy:** [plan de capas, especialmente si hay overlap]

## 9. Componentes Base (Anti-Genéricos)
### 9.1 Botones
- **Primary:** [estados: default, hover (¿qué pasa?), active, disabled, loading]
- **Secondary:** [estados]
- **Ghost:** [estados]
- **Icon Button:** [estados]
- **Text-as-Button:** [cuando el texto mismo es clickeable]

> Cada estado debe tener una animación específica, no solo un cambio de color.

### 9.2 Inputs
- **Text:** [estados, con descripción de focus effects]
- **Textarea:** [estados]
- **Select:** [estados]
- **Checkbox/Radio:** [estados, con animación de check]

### 9.3 Cards / Contenedores
- **Standard:** [estructura]
- **Feature:** [estructura]
- **Media:** [estructura]
- **Floating:** [estructura]

### 9.4 Estados Especiales (Zona de Personalidad Máxima)
- **Empty State:** [Copy exacto + descripción visual + animación]
- **Error State:** [Copy exacto + descripción visual + animación]
- **Loading State:** [Copy exacto + secuencia narrativa de carga + animación]
- **Success State:** [Copy exacto + celebración visual + animación]
- **Onboarding:** [Copy paso a paso + flujo de introducción]
- **404 / Not Found:** [Copy + experiencia visual memorable]

## 10. Assets Visuales y Texturas
- **Icon set:** [estilo: hand-drawn / geometric brutal / organic / glitch / custom]
- **Illustration style:** [descripción]
- **Photography treatment:** [filtros, crops, tratamiento]
- **Texture overlays:** [lista de texturas con URLs o descripciones para generar]
- **SVG filters:** [lista de filtros custom necesarios]
- **Shader requirements:** [si aplica, descripción de shaders WebGL]

## 11. Prohibiciones Explícitas (Anti-Slop Manifesto)
Esta app NUNCA usará:
- [ ] Gradiente púrpura/azul genérico de AI
- [ ] Inter o Roboto como fuente principal sin modificación extrema
- [ ] Hero centrado con un solo CTA y tres tarjetas debajo
- [ ] Esquinas redondeadas de 8px en TODOS los elementos
- [ ] Sombras al 0.1 de opacidad en todo
- [ ] Spinner de carga genérico (circular girando)
- [ ] "No data found" como empty state
- [ ] "Something went wrong" como error state
- [ ] Paleta de grises sin punto de vista emocional
- [ ] Layout simétrico cuando la personalidad pide asimetría
- [ ] Animaciones fade-in genéricas sin dirección ni propósito
- [ ] Iconos de Material Design sin personalización
- [ ] Grid de 12 columnas por defecto
- [ ] Scroll suave genérico sin propósito narrativo
- [ ] Botones con solo cambio de color en hover
- [ ] Tipografía que no sea un elemento de diseño activo
- [ ] Espaciado predecible (8px, 16px, 24px, 32px...) sin variación
- [ ] "Diseño responsive" que solo significa "más pequeño en móvil"
- [ ] Sonido de notificación del sistema genérico (pop/ding por defecto del OS)
- [ ] Cursor arrow del sistema sin personalidad ni comportamiento
- [ ] Todas las transiciones con la misma duración (tempo uniforme = cadáver rítmico)
- [ ] Iluminación plana sin dirección ni drama cuando la personalidad pide profundidad
- [ ] Silencio total cuando el sonido es parte de la identidad (y viceversa: sonido genérico cuando el silencio es la estética)

## 12. Referencias y Moodboard
[Sugerir 3-5 referencias reales que capturen la esencia]
[Incluir descripción de POR QUÉ cada referencia es relevante]

## 13. Notas Técnicas para Implementación
- **Librerías recomendadas:** [lista con justificación]
- **Performance considerations:** [qué cuidar]
- **Accessibility:** [cómo mantener accesibilidad SIN sacrificar personalidad]
- **Browser support:** [qué features modernos usar con confianza]

## 14. Sonido y Audio
| Acción | Sonido / Silencio | Técnica | Volumen |
|--------|-------------------|---------|---------|
| Click / tap | [descripción o NADA] | [Tone.js / Howler / WebAudio / háptica] | [dB] |
| Transición de sección | [descripción o NADA] | [técnica] | [dB] |
| Error | [descripción] | [técnica] | [dB] |
| Success | [descripción] | [técnica] | [dB] |
| Ambiente | [generativo / silencio / loop] | [técnica] | [dB] |

> Especificar: ¿Respetar prefers-reduced-motion afecta también al audio? ¿Hay mute visible siempre?
> Si `sound_identity` es "silencio curado": documentar exactamente qué ÚNICO sonido existe (el error) y por qué.

## 15. Iluminación
| Token | Valor | Uso | Técnica |
|-------|-------|-----|---------|
| Light source | [dirección/tipo de luz] | Foco principal | [radial-gradient / spotlight / none] |
| --glow-primary | [valor] | [dónde brilla] | [box-shadow / text-shadow / blur] |
| --glow-secondary | [valor] | [dónde brilla] | [técnica] |
| Background darkness | [valor] | Fondo base | [color + depth] |
| Hover illumination | [descripción] | Qué pasa al encender un elemento | [filter brightness / glow] |

> Especificar: ¿El modo oscuro es el default o una elección? ¿La luz cambia con interacción?

## 16. Tempo System
| Token | Valor | Uso |
|-------|-------|-----|
| Duration base | [ms] | Ritmo general |
| Duration fast | [ms] | Micro-interacciones |
| Duration slow | [ms] | Transiciones de sección |
| Easing principal | [cubic-bezier/ease] | Todo el motion |
| Easing de climax | [cubic-bezier/ease] | Momentos importantes |
| Patrón rítmico | [descripción] | Cómo "late" la interfaz |

> Especificar: ¿El tempo es uniforme o por fases? ¿Qué secciones son lentas y cuáles rápidas?

## 17. Cursor
| Estado | Comportamiento | Técnica |
|--------|----------------|---------|
| Default | [descripción] | [custom cursor / none / system] |
| Hover en interactivo | [descripción] | [transform / snap / trail] |
| En texto | [descripción] | [descripción] |
| Drag / activo | [descripción] | [descripción] |
| Loading | [descripción] | [descripción] |

> Especificar: ¿El cursor respeta touch devices (desaparece en móvil)? ¿Deja rastros persistentes?
> Si es "mano invisible": documentar los tooltips contextuales que lo reemplazan.
```

---

## Fase 5: Confirmación de Readiness Experimental

```
✅ DESIGN SYSTEM EXPERIMENTAL COMPLETO

Tu app tiene ahora una identidad visual ÚNICA basada en:
- Movimiento: [personality_axis]
- Navegación: [navigation_pattern]
- Tipografía: [typography_architecture]
- Materialidad: [materiality]
- Paleta: [primario, secundario, fondo, acento]
- Interacción: [interaction_pattern]
- Estructura: [information_structure]
- Sonido: [sound_identity]
- Luz: [lighting_profile]
- Tempo: [tempo_rhythm]
- Cursor: [cursor_identity]
- [Fricción: friction_profile — si respondió la opcional]
- [Ancla temporal: temporal_anchor — si respondió la opcional]

El documento `design-system.md` está listo y servirá como fuente de verdad
para TODA la generación de código posterior.

⚠️ ADVERTENCIA: Este design system es experimental. Algunas decisiones
pueden requerir técnicas avanzadas (WebGL, shaders, animaciones complejas).
¿Estás listo para que genere la primera pantalla?

[Si, genera con todo el riesgo] → Proceder a generación experimental.
[Si, pero simplifica lo técnico] → Adaptar a técnicas CSS/JS estándar manteniendo la visión.
[No, quiero ajustar algo] → Volver a Fase 3.
[Muéstrame el design system completo] → Mostrar markdown completo.
```

---

## Reglas de Oro de la Edición Experimental

1. **Nunca generar código antes del design system.** El código sigue al diseño.
2. **Una pregunta a la vez.** No overwhelm.
3. **Siempre mostrar progreso.** El usuario debe saber dónde está.
4. **Las alternativas deben ser visualmente DISTINTAS y ARRIESGADAS.** No 4 versiones de lo mismo.
5. **"Otra" siempre disponible.** El usuario debe poder romper el marco.
6. **Documentar prohibiciones explícitas.** Lo que NO se debe hacer es tan importante.
7. **El design system es ley.** Una vez aprobado, todo el código se justifica contra él.
8. **Microcopy es diseño.** Los estados especiales son oportunidades de personalidad máxima.
9. **Motion requiere especificación.** Tipo, duración, easing, propósito, librería.
10. **La imperfección intencional es un feature.** 1deg de rotación, textura al 5%, leading de 0.85.
11. **Explorar con imágenes ANTES de código.** Los modelos de imagen proponen layouts que los agentes de código nunca se atreverían.
12. **El riesgo visual es el objetivo.** Si no da miedo implementarlo, no es lo suficientemente experimental.
13. **La tipografía NO es decorativa.** Es arquitectura, es narrativa, es la voz de la app.
14. **Cada interacción debe ser memorable.** Un hover que solo cambia de color es un hover fallido.
15. **El responsive no es "más pequeño".** Es una reimaginación del layout para el viewport.
16. **El sonido es diseño.** Un "ding" genérico del sistema es tan slop como un gradiente púrpura. Silencio, ritmo y audio deben ser decisiones tan conscientes como el color.
17. **La luz tiene dirección.** Iluminar no es "agregar sombras"; es decidir de dónde viene la luz y qué resalta.
18. **El tempo define la emoción.** Una misma animación con otra duración cambia el significado. La duración es un token, no un capricho.
19. **El cursor es parte de la escena.** No un puntero que flota sobre tu mundo: un personaje dentro de él.
20. **Las opcionales son palanca, no relleno.** Fricción y ancla temporal son preguntas que solo valen si el usuario quiere más profundidad; nunca forzarlas.

---

## Prompt de Activación Rápida

```
Activa la skill Anti-Slop Design Architect — Edición Experimental.
Quiero diseñar [tipo de app] que se sienta [adjetivo arriesgado].
[Opcional: No tengo claro el estilo, guíame con el cuestionario].
[Opcional: Quiero que primero explores visualmente con imágenes].
```
