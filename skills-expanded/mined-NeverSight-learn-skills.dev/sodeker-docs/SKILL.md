---
name: sodeker-docs
description: Genera documentación de proyectos de software con identidad visual Sódeker (blanco + turquesa + sans-serif) y diagramas/figuras interactivas estilo Distill. Cubre resumen funcional, documentación técnica, instalación, soporte y manual de usuario. Salida HTML por defecto, Markdown bajo petición. Layout con contenido a la izquierda y sidebar de navegación a la derecha.
user-invocable: true
---

# Sódeker Docs

Skill para producir documentación de software con estética Sódeker (landing page corporativa minimalista en blanco + turquesa) combinada con la mecánica de figuras y controles interactivos de Distill.

## Cuándo activarse

Invocar cuando el usuario pida:
- Documentar un módulo, servicio, sistema o feature.
- Crear documentación técnica o funcional.
- Construir una guía de instalación, runbook de soporte o manual de usuario.
- Generar un portal de documentación para un proyecto.

Frases gatillo: "documenta este proyecto", "crea la documentación de…", "necesito un manual de usuario para…", "haz un runbook de soporte de…", "documentación técnica de…", "/sodeker-docs".

## Qué produce

Documentación organizada en hasta 6 bloques:

1. **Resumen funcional** — objetivo, problema, usuarios, funcionalidades, reglas de negocio, casos de uso, restricciones.
2. **Documentación técnica** — arquitectura, stack, estructura, patrones, decisiones, integraciones, dependencias, configs, diagramas (arquitectura, BD, despliegue, flujos).
3. **Instalación y configuración** — requisitos, variables, comandos, ejecución local, pruebas, datos seed, troubleshooting.
4. **Soporte** — errores comunes, logs, alertas, métricas, reinicio de servicios, estado del sistema, contactos, procedimientos ante incidentes, FAQs. **Escrito en lenguaje accesible para personas no técnicas.**
5. **Manual de usuario** (cuando aplica) — login, funciones principales, capturas, errores comunes, FAQs, guías paso a paso.

Formato de salida:
- **HTML** (por defecto) — interactivo, sidebar a la derecha, figuras estilo Distill.
- **Markdown** (a petición) — `git-friendly`, diagramas Mermaid, bloques HTML embebidos cuando el renderer los soporta.

## Cómo invocar

```
/sodeker-docs [módulo o proyecto] [--md|--html]
/sodeker-docs documentar el módulo de inventarios
/sodeker-docs en markdown — sistema de facturación
```

## Flujo de trabajo (paso a paso obligatorio)

Cuando se invoca la skill, ejecutar este flujo:

### 1. Descubrir el contexto
Hacer preguntas focalizadas (máximo 5–6) antes de generar nada:
- Nombre y propósito del proyecto/módulo.
- Usuarios principales (roles).
- Stack principal (lenguajes, frameworks, base de datos, infraestructura).
- ¿Existe repo? Si sí, ¿ruta? — para extraer estructura real y `package.json`/`requirements.txt`/etc.
- ¿Qué secciones aplican? (a veces no hay manual de usuario, a veces no hay soporte aún).
- Formato preferido (HTML/Markdown).

### 2. Detectar el formato
- Por defecto: **HTML**.
- Cambiar a Markdown si el usuario menciona: "markdown", ".md", "README", "para el repo", "para Git", "para GitHub", "para GitLab".

### 3. Cargar las referencias internas de la skill
**Antes de escribir cualquier output**, leer:
- `style/sodeker.css` — tokens visuales. Nunca inventar colores ni fuentes.
- `content-spec/00-principios.md` — reglas globales de redacción.
- `content-spec/0{N}-*.md` — qué debe responder cada sección que vas a generar.
- `templates/html/shell.html` y `templates/html/components.html` — estructura base y snippets de componentes.
- `templates/markdown/shell.md` — estructura base markdown.
- `examples/` — output de referencia para calibrar estilo.

### 4. Generar la documentación
- **HTML**: un único `index.html` con todas las secciones + `sodeker.css` copiado al lado. El layout DEBE usar `.doc-layout` con contenido a la izquierda y `<nav class="doc-nav">` a la derecha (sticky, scroll independiente).
- **Markdown**: un archivo `.md` por sección dentro de una carpeta `docs/`, más un `README.md` que actúa como índice.

### 5. Verificar visualmente
- HTML: abrir el archivo en el navegador con la herramienta apropiada. Confirmar que el sidebar está a la derecha, los colores son turquesa/blanco/gris (nunca crema o coral), y no hay muros de texto.
- Markdown: confirmar que Mermaid renderiza, las tablas se ven limpias, y no hay bloques HTML rotos.

## Reglas inviolables

### Identidad visual (Sódeker)
- Color acento único: `#0097A7` (turquesa). Nunca coral, púrpura, degradados, ni tonos cálidos.
- Fondo: blanco (`#FFFFFF` o `#FCFCFD`). Nunca crema cálido tipo Distill.
- Tipografía: sans-serif (Inter, Manrope). Nunca serif para el cuerpo.
- Títulos mixtos: parte en negro + palabra clave en turquesa. Usar `<span class="accent">` o equivalente.
- Layout: contenido a la izquierda, sidebar `<nav>` **a la derecha** (sticky). NADA arriba, NADA en la columna izquierda.

### Principios de contenido
- **Cero muros de texto.** Siempre cards, tablas, callouts, métricas, o bloques visuales.
- Cada sección abre con: badge pequeño turquesa → título grande → subtítulo gris → bloques de contenido.
- **Usa analogías** para explicar conceptos complejos. El lector objetivo aprende mejor con gráficos y ejemplos.
- Mantén vocabulario técnico, pero **explícalo siempre**. No asumas que el lector es el desarrollador original.
- La sección de Soporte se escribe en **lenguaje accesible para no desarrolladores** (analista de soporte, QA, mesa de ayuda). Sin jerga sin contexto.
- **Diagrama por cada concepto, flujo o transformación**. Si algo se puede expresar como "X → Y → Z", debe tener un SVG al lado. No basta con describirlo en texto. Ej: comando → job → job → importer.
- **Consistencia en card-grids**: dentro de un mismo `.card-grid`, todas las cards usan la misma variante (`card`, `card--accent` o `card--accent-left`). No mezclar dentro del mismo grupo conceptual.
- **Métricas solo con datos reales**: `metric-grid` solo cuando represente cifras verificables (capacidad, latencia, volumen, KPIs). Nunca como decoración tipo dashboard en guías conceptuales.
- Sentence case en titulares, etiquetas y botones (no Title Case ni MAYÚSCULAS).

### Elementos interactivos (Distill)
- Figuras: borde hairline (`1px solid var(--ink-100)` o `--border-hair`), nunca sombras pesadas.
- Conectores: flechas grises delgadas (~1.5px) con curvas bezier suaves.
- Elementos interactivos (sliders, drag): badge "mano" turquesa (`assets/interactive-hand.svg`) para señalarlos.
- Animaciones cortas (120–360ms), respeta `prefers-reduced-motion`. Sin bounces.
- Diagramas de flujo: tarjetas conectadas + flechas, numeradas, breves.

### Lo que NUNCA hacer
- No usar emojis (Distill no los usa, Sódeker tampoco).
- No usar degradados, fondos oscuros dominantes, sombras pesadas Material Design.
- No usar Bootstrap, Tailwind utility classes, ni frameworks de UI por encima. Usar solo `sodeker.css`.
- No inventar colores fuera de la paleta de tokens.
- No copiar literalmente texto del repo del usuario. Siempre parafrasear con voz Sódeker.

## Archivos de la skill

```
documentation-skill/
├── SKILL.md                           ← este archivo
├── README.md                          ← readme público (GitHub)
├── LICENSE                            ← MIT
├── style/
│   └── sodeker.css                    ← tokens + componentes + layout
├── content-spec/                      ← qué debe responder cada sección
│   ├── 00-principios.md
│   ├── 01-resumen-funcional.md
│   ├── 02-documentacion-tecnica.md
│   ├── 03-instalacion-configuracion.md
│   ├── 04-soporte.md
│   └── 05-manual-usuario.md
├── templates/
│   ├── html/
│   │   ├── shell.html                 ← layout base con sidebar derecho
│   │   └── components.html            ← snippets reutilizables
│   └── markdown/
│       └── shell.md                   ← estructura base markdown
├── examples/
│   ├── ejemplo-inventarios.html       ← output de referencia
│   └── ejemplo-inventarios.md
└── assets/
    └── interactive-hand.svg           ← badge mano turquesa
```

## Notas finales

- Si el usuario no especifica algo (ej. qué módulo, qué stack), **pregunta** — no inventes.
- Si el repo del proyecto está disponible, léelo para extraer hechos verificables (estructura, dependencias, variables de entorno reales). Nunca documentes algo que no se pueda verificar.
- Cuando termines de generar, dile al usuario qué archivo abrir y qué revisar primero.
