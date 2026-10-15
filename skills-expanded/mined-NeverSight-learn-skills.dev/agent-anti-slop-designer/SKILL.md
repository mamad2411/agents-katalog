---
name: agent-anti-slop-designer
description: Diseño de productos digitales con personalidad que no parecen hechos por IA. Cuestionario de descubrimiento de estilo (voz, energía, tipografía, material, color, interacción), refinamiento de supuestos y generación de design-system.md con identidad humana. Usa cuando el usuario diga "que no parezca hecho por AI", "diseño con personalidad", "design system", "cuestionario de estilo", "evita el estilo genérico de IA", o quiera UI con alma e intención.
---

# Skill: Agent Anti-Slop Designer
## Version: 1.0 | 2026-07-28
### Propósito
Transformar ideas de aplicaciones AI-genéricas en productos digitales con personalidad, intención y alma humana. Esta skill guía al usuario —incluso cuando no sabe qué quiere— a través de un cuestionario de descubrimiento de estilo, extrayendo un design system único antes de que una sola línea de código se genere.

---

## Fase 0: Diagnóstico Rápido (30 segundos)
Antes de cualquier pregunta, evalúa la entrada del usuario:

- **Si el usuario trae una idea clara** (ej: "quiero una app de journaling con estilo brutalista") → Salta a Fase 2 (Refinamiento de Supuestos).
- **Si el usuario trae una idea vaga** (ej: "quiero una app de tareas") → Entra a Fase 1 (Cuestionario de Descubrimiento).
- **Si el usuario solo dice "hazme algo que no parezca AI"** → Entra a Fase 1 completa.

---

## Fase 1: Cuestionario de Descubrimiento de Estilo
> Regla de oro: Una pregunta a la vez. Mostrar barra de progreso. Ofrecer 4 alternativas + opción "Otra" en cada paso.

### Paso 1.1: Voz y Personalidad (1/6)
**Pregunta:** Si tu app fuera una persona, ¿cómo hablaría?

| # | Opción | Descripción | Keywords de diseño |
|---|--------|-------------|-------------------|
| 1 | **El Sabio** | Calmada, precisa, confiable. Como un bibliotecario que sabe todo. | Tipografía clásica, colores apagados, grids rígidos, serif fonts |
| 2 | **El Rebelde** | Directa, irreverente, sin filtros. Como un zine punk. | Brutalismo, tipografía bold, rojo/negro, asimetría, caos controlado |
| 3 | **El Artista** | Poética, sensorial, imperfecta. Como un cuaderno de bocetos. | Texturas, doodles, colores tierra, hand-drawn elements, wabi-sabi |
| 4 | **El Futurista** | Minimalista, precisa, casi alienígena. Como una nave espacial. | Glassmorphism, tipografía monoespaciada, neones suaves, dark mode |
| O | **Otra** | El usuario describe su propia voz | Anotar palabras clave exactas |

> Guardar selección como `personality_axis`.

### Paso 1.2: Energía Visual (2/6)
**Pregunta:** ¿Cómo se *siente* usar tu app?

| # | Opción | Descripción |
|---|--------|-------------|
| 1 | **Zen Garden** | Lento, meditativo, espacioso. Cada interacción es un respiro. |
| 2 | **Café de Madrid** | Animado, conversacional, cálido. Como charlar con un amigo. |
| 3 | **Estudio de Grabación** | Intenso, enfocado, profesional. Cada pixel tiene un propósito. |
| 4 | **Festival Nocturno** | Caótico, divertido, impredecible. Sorpresas en cada rincón. |
| O | **Otra** | El usuario describe la energía |

> Guardar como `energy_profile`.

### Paso 1.3: Estructura vs. Caos (3/6)
**Pregunta:** ¿Qué tan ordenada debe verse la información?

| # | Opción | Descripción |
|---|--------|-------------|
| 1 | **Catedral** | Simetría perfecta, jerarquía clara, todo alineado. Grid de 12 columnas. |
| 2 | **Mercado** | Densidad informativa, elementos superpuestos, múltiples focos. |
| 3 | **Diario Personal** | Flujo libre, elementos rotados ligeramente, notas en márgenes. |
| 4 | **Laboratorio** | Modular, reorganizable, paneles flotantes tipo dashboard científico. |
| O | **Otra** | El usuario describe su estructura ideal |

> Guardar como `structure_preference`.

### Paso 1.4: Materialidad Digital (4/6)
**Pregunta:** ¿De qué material parece hecha tu app?

| # | Opción | Descripción | Implicaciones técnicas |
|---|--------|-------------|----------------------|
| 1 | **Papel Artesanal** | Textura visible, bordes irregulares, tinta que sangra | Blend modes, texturas SVG, borders irregulares |
| 2 | **Vidrio y Luz** | Transparente, refractiva, etérea | Glassmorphism, backdrop-filter, gradients suaves |
| 3 | **Metal y Concreto** | Sólida, industrial, sin adornos | Bordes duros 0px radius, colores grises, tipografía heavy |
| 4 | **Tela y Hilo** | Suave, cosida, orgánica | Bordes redondeados variables, patrones de fondo, colores pastel |
| O | **Otra** | El usuario describe el material |

> Guardar como `materiality`.

### Paso 1.5: Tipografía como Voz (5/6)
**Pregunta:** Si tu app hablara en un solo tipo de letra, ¿cuál sería?

| # | Opción | Descripción | Fuentes sugeridas |
|---|--------|-------------|-------------------|
| 1 | **El Clásico** | Elegante, atemporal, leído en bibliotecas | Cormorant, Playfair Display, Source Serif |
| 2 | **El Gritón** | En tu cara, imposible de ignorar | Founders Grotesk, Monument Extended, Space Grotesk Bold |
| 3 | **El Manuscrito** | Personal, íntimo, imperfecto | Caveat, Permanent Marker, tipografía custom |
| 4 | **El Ingeniero** | Preciso, técnico, utilitario | JetBrains Mono, IBM Plex Mono, SF Mono |
| O | **Otra** | El usuario describe o nombra una fuente |

> Guardar como `typography_voice`.

### Paso 1.6: Paleta Emocional (6/6)
**Pregunta:** Elige un momento del día que represente el estado de ánimo de tu app:

| # | Opción | Paleta base | Mood |
|---|--------|-------------|------|
| 1 | **Amanecer en el desierto** | Terracotas, arenas, azul pálido | Cálido, esperanzador, terroso |
| 2 | **Medianoche neón** | Negro profundo, fucsia, cian | Intenso, nocturno, eléctrico |
| 3 | **Mañana de otoño** | Verde musgo, naranja quemado, crema | Acogedor, nostálgico, natural |
| 4 | **Tormenta en el mar** | Gris plomo, azul petróleo, blanco roto | Dramático, serio, poderoso |
| O | **Otra** | El usuario describe su paleta ideal | |

> Guardar como `palette_mood`.

---

## Fase 2: Refinamiento de Supuestos (Anti-Slop Checklist)
Una vez definida la dirección (ya sea por el usuario directamente o por el cuestionario), lista explícitamente los supuestos de diseño que estás tomando. Muestra la lista al usuario para confirmación.

### Plantilla de Supuestos:
```
Basado en tu selección, asumo lo siguiente para tu app:

1. PERSONALIDAD: Tu app habla como [personality_axis] → Esto significa que el tono de los microcopy (empty states, errores, onboarding) será [descripción].

2. ENERGÍA: La experiencia se siente como [energy_profile] → Las animaciones serán [lentas y suaves / rápidas y juguetonas / precisas y snappy / caóticas y divertidas].

3. ESTRUCTURA: El layout principal será [structure_preference] → [Grid simétrico de 12 cols / Asimétrico con overlap / Flujo libre tipo diario / Dashboard modular].

4. MATERIALIDAD: La superficie visual se siente como [materiality] → [Texturas visibles / Glassmorphism / Industrial duro / Suave y orgánico].

5. TIPOGRAFÍA: La voz tipográfica es [typography_voice] → Fuente principal: [nombre]. Fuente secundaria: [nombre]. Escala: [base]/[ratio].

6. COLOR: La paleta emocional es [palette_mood] → Primario: [hex]. Secundario: [hex]. Fondo: [hex]. Acento: [hex].

7. INTERACCIONES: Los estados de carga usarán [spinner genérico / animación custom / skeleton con personalidad].

8. MOTION: Las transiciones entre pantallas serán [fade simple / slide direccional / morphing de formas / parallax suave].

9. BORDES: Los radios de esquina serán [0px en todo / 4px sutiles / 16px amigables / Mixto: 0px para contenedores, 999px para botones].

10. ESPACIADO: El sistema de spacing usará [8px grid / escala musical (4,8,16,32,64) / escala Fibonacci / caos intencional].
```

> Pedir al usuario: "¿Hay algún supuesto que NO te guste? Responde con los números (ej: 2, 5, 9) o di 'todo bien' para continuar."

---

## Fase 3: Preguntas de Clarificación (One-by-One)
Por cada supuesto que el usuario marcó como incorrecto, hacer UNA pregunta a la vez con barra de progreso.

### Formato de cada pregunta:
```
[Barra de progreso: Pregunta X de Y]

El supuesto #[número] dice: [texto del supuesto].
¿Qué prefieres en su lugar?

1. [Alternativa A]
2. [Alternativa B]
3. [Alternativa C]
4. [Alternativa D]
O. Otra: [espacio para que el usuario escriba]
```

> Regla: Nunca mostrar más de una pregunta por turno. Esperar respuesta antes de la siguiente.

---

## Fase 4: Generación del Design System Document
Una vez confirmados todos los supuestos, generar un archivo `design-system.md` estructurado. Este documento es la BIBLIA que regirá TODA la generación posterior de código.

### Estructura del `design-system.md`:

```markdown
# Design System: [Nombre del Proyecto]
## Última actualización: [fecha]

---

## 1. Filosofía de Diseño
- **Personalidad:** [De Fase 1.1]
- **Energía:** [De Fase 1.2]
- **Materialidad:** [De Fase 1.4]
- **Anti-Slop Statement:** "Esta app NUNCA usará [lista de prohibiciones]"

## 2. Paleta de Color
| Token | Hex | Uso | Contexto |
|-------|-----|-----|----------|
| --color-primary | #XXXXXX | Botones principales, CTAs | Sobre fondo claro |
| --color-secondary | #XXXXXX | Enlaces, acentos sutiles | Sobre fondo claro |
| --color-background | #XXXXXX | Fondo general | Siempre |
| --color-surface | #XXXXXX | Tarjetas, paneles | Sobre background |
| --color-text-primary | #XXXXXX | Títulos, body | Sobre fondo claro |
| --color-text-secondary | #XXXXXX | Subtítulos, metadatos | Sobre fondo claro |
| --color-accent | #XXXXXX | Estados activos, highlights | Sobre cualquier fondo |
| --color-error | #XXXXXX | Mensajes de error | Con personalidad: [descripción] |
| --color-success | #XXXXXX | Confirmaciones | Con personalidad: [descripción] |

> NOTA: Especificar blend modes para texturas si aplica.

## 3. Tipografía
| Rol | Fuente | Peso | Tamaño | Line-height | Letter-spacing | Uso |
|-----|--------|------|--------|-------------|----------------|-----|
| Display | [Fuente] | [Peso] | [Size] | [LH] | [LS] | H1, Hero text |
| Heading | [Fuente] | [Peso] | [Size] | [LH] | [LS] | H2-H4 |
| Body | [Fuente] | [Peso] | [Size] | [LH] | [LS] | Párrafos |
| Mono | [Fuente] | [Peso] | [Size] | [LH] | [LS] | Código, datos |
| Accent | [Fuente] | [Peso] | [Size] | [LH] | [LS] | Labels, captions |

> NOTA: Especificar fallback fonts. Especificar si usa variable fonts.

## 4. Spacing System
- **Base unit:** [4px / 8px / etc.]
- **Scale:** [4, 8, 16, 24, 32, 48, 64, 96] / [Fibonacci] / [Custom]
- **Section padding:** [valor]
- **Container max-width:** [valor]
- **Grid:** [12-col / asymmetrical / fluid / custom]

## 5. Bordes y Radios
| Elemento | Border-radius | Border | Notas |
|----------|---------------|--------|-------|
| Botones primarios | [valor] | [valor] | |
| Tarjetas | [valor] | [valor] | |
| Inputs | [valor] | [valor] | |
| Modales | [valor] | [valor] | |
| Imágenes | [valor] | [valor] | |
| Tags/Chips | [valor] | [valor] | |

> NOTA: Si la materialidad es "papel" o "tela", considerar bordes irregulares con clip-path.

## 6. Sombras y Profundidad
| Nivel | Shadow | Uso |
|-------|--------|-----|
| Flat | none | Elementos base |
| Elevated 1 | [valor] | Tarjetas, botones hover |
| Elevated 2 | [valor] | Modales, dropdowns |
| Elevated 3 | [valor] | Toasts, notificaciones |

## 7. Motion & Animation
| Tipo | Especificación | Librería/Técnica |
|------|----------------|------------------|
| Page transitions | [descripción] | [GSAP / Framer Motion / CSS] |
| Micro-interactions | [descripción] | [descripción] |
| Loading states | [descripción] | [descripción] |
| Scroll animations | [descripción] | [descripción] |
| Hover states | [descripción] | [descripción] |

> Especificar duraciones (ej: 200ms para micro, 600ms para page transitions).
> Especificar easing curves.

## 8. Componentes Base
### 8.1 Botones
- **Primary:** [estado default, hover, active, disabled, loading]
- **Secondary:** [estados]
- **Ghost:** [estados]
- **Icon Button:** [estados]

### 8.2 Inputs
- **Text:** [estados]
- **Textarea:** [estados]
- **Select:** [estados]
- **Checkbox/Radio:** [estados]

### 8.3 Cards
- **Standard:** [estructura]
- **Feature:** [estructura]
- **Media:** [estructura]

### 8.4 Estados Especiales (Anti-Slop Zone)
- **Empty State:** [Copy exacto + ilustración descripción]
- **Error State:** [Copy exacto + ilustración descripción]
- **Loading State:** [Copy exacto + animación descripción]
- **Success State:** [Copy exacto + animación descripción]
- **Onboarding Step 1:** [Copy exacto]
- **Onboarding Step N:** [Copy exacto]

## 9. Layout Patterns
- **Mobile:** [descripción del layout móvil]
- **Tablet:** [descripción del layout tablet]
- **Desktop:** [descripción del layout desktop]
- **Breakpoints:** [valores exactos]

## 10. Assets Visuales
- **Icon set:** [nombre o descripción del estilo]
- **Illustration style:** [descripción]
- **Photography treatment:** [filtros, crops, etc.]
- **Texture overlays:** [descripción de texturas si aplica]

## 11. Prohibiciones Explícitas (Anti-Slop Manifesto)
Esta app NUNCA usará:
- [ ] Gradiente púrpura/azul genérico de AI
- [ ] Inter o Roboto como fuente principal sin modificación
- [ ] Hero centrado con un solo CTA y tres tarjetas debajo
- [ ] Esquinas redondeadas de 8px en TODOS los elementos
- [ ] Sombras al 0.1 de opacidad en todo
- [ ] Spinner de carga genérico
- [ ] "No data found" como empty state
- [ ] "Something went wrong" como error state
- [ ] Paleta de grises sin punto de vista emocional
- [ ] Layout simétrico cuando la personalidad pide asimetría
- [ ] Animaciones fade-in genéricas sin dirección ni propósito
- [ ] Iconos de Material Design sin personalización

## 12. Referencias Visuales
[Sugerir 3-5 sitios/apps reales que capturen la esencia del design system]
```

---

## Fase 5: Confirmación de Readiness
Antes de generar cualquier código, mostrar al usuario:

```
✅ DESIGN SYSTEM COMPLETO

Tu app tiene ahora una identidad visual única basada en:
- Personalidad: [resumen]
- Materialidad: [resumen]
- Paleta: [primario, secundario, fondo]
- Tipografía: [fuente principal]
- Estructura: [resumen]

El documento `design-system.md` está listo y servirá como fuente de verdad
para TODA la generación de código posterior.

¿Estás listo para que genere la primera pantalla usando este design system?
[Si] → Proceder a generación de código, citando design-system.md en cada prompt.
[No, quiero ajustar algo] → Volver a Fase 3 para el ajuste específico.
[Muéstrame el design system completo] → Mostrar el markdown completo.
```

---

## Reglas de Oro de esta Skill

1. **Nunca generar código antes del design system.** El código sigue al diseño, no al revés.
2. **Una pregunta a la vez.** No bombardear al usuario con formularios.
3. **Siempre mostrar progreso.** El usuario debe saber en qué paso está.
4. **Las alternativas deben ser visualmente distintas.** No 4 versiones de lo mismo.
5. **"Otra" siempre disponible.** El usuario debe poder romper el marco.
6. **Documentar prohibiciones explícitas.** Lo que NO se debe hacer es tan importante como lo que sí.
7. **El design system es ley.** Una vez aprobado, todo el código debe justificarse contra él.
8. **Microcopy es diseño.** Los empty states, errores y loading son oportunidades de personalidad, no afterthoughts.
9. **Motion requiere especificación.** "Añade animación" no es suficiente. Especificar tipo, duración, easing y propósito.
10. **La imperfección intencional es un feature.** 1deg de rotación, textura al 5%, leading de 0.85 —estos detalles humanizan.

---

## Prompt de Activación Rápida (para el usuario)
Copia y pega esto para activar esta skill:

```
Activa la skill Agent Anti-Slop Designer. Quiero disenar [tipo de app] 
que se sienta [adjetivo: cálida/rebelde/minimalista/artística/etc.]. 
[Opcional: No tengo claro el estilo, guíame con el cuestionario].
```
