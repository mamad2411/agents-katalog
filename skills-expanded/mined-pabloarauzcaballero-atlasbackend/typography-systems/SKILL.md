---
name: typography-systems
description: Sistema tipográfico de producto — escala modular, medida de línea (45–75 caracteres), interlineado por tamaño, jerarquía con peso/tamaño/color, emparejar como máximo dos familias, números tabulares para tablas y dinero, `text-wrap` para títulos y párrafos, y carga de fuentes performante (font-display, subsetting, preload). Usar al definir la escala tipográfica de un producto, al maquetar texto largo o tablas numéricas, al elegir o cargar una fuente, o al revisar por qué un texto se ve apretado, ilegible o "de plantilla".
---

<!-- ESPEJO GENERADO por AtlasPromptManager/tools/install_skills.py - NO EDITAR A MANO -->
<!-- La fuente es AtlasPromptManager/.claude/skills/. Lo que edites aca se pierde. -->

# Sistemas tipográficos

La tipografía carga el 90% del contenido y buena parte de la jerarquía. Las **escalas** viven
como tokens en `frontend-design-system`; esta skill decide qué valores tienen y cómo se aplican
para que el texto sea legible y la jerarquía se lea sin adornos.

## 1. Escala modular

Definí una escala con una razón fija (p. ej. 1.20–1.25) desde un tamaño base de cuerpo
(típicamente 16px). No inventes tamaños sueltos por pantalla: elegís de la escala.

```css
:root {
  --font-size-base: 1rem;      /* 16px — cuerpo */
  --font-size-sm:   0.833rem;
  --font-size-lg:   1.25rem;
  --font-size-xl:   1.5rem;
  --font-size-2xl:  1.953rem;  /* razón ~1.25 */
}
```

- Usá `rem` para tamaños (respeta el zoom de fuente del usuario); `px` solo para hairlines.
- Cuerpo mínimo ~16px en web; por debajo se pierde legibilidad y en iOS dispara zoom en inputs.
- Tipografía fluida para titulares con `clamp()` (ver `frontend-responsive-layout`), no una
  cascada de media queries por tamaño.

## 2. Medida de línea (longitud)

La línea de texto corrido va de **45 a 75 caracteres** (~66 ideal). Más largo, el ojo pierde
el renglón; más corto, el ritmo se corta.

```css
.prose { max-width: 66ch; }   /* ch ata la medida a los caracteres, no a px */
```

No pongas párrafos a todo el ancho de un monitor. En columnas anchas, limitá con `max-width`
en `ch` o `rem`.

## 3. Interlineado por tamaño

El interlineado (`line-height`) es inverso al tamaño: texto chico necesita más aire relativo,
los títulos grandes menos.

- Cuerpo: `line-height: 1.5`–1.6 (unidad sin, no px, para que escale).
- Títulos grandes: 1.1–1.25.
- Nunca `line-height` con unidad fija en un contenedor que hereda a varios tamaños.

## 4. Jerarquía con peso, tamaño y color

Tres palancas, en este orden de preferencia: **tamaño** y **peso** primero, **color** (texto
primario vs `--color-text-muted`) para el matiz. No abuses de mayúsculas ni de negrita para
"gritar" jerarquía.

- Máximo 3–4 niveles visibles por pantalla; más es ruido.
- El contraste entre niveles tiene que ser evidente: si `h2` y `h3` casi no se distinguen,
  colapsá uno.
- Mayúsculas solo en etiquetas cortas (kickers, encabezados de tabla), con `letter-spacing`
  leve; nunca en párrafos.

## 5. Emparejar familias

Como máximo **dos** familias (p. ej. una para títulos, una para cuerpo/UI), o una sola bien
usada con sus pesos. Más familias = incoherencia y peso de descarga.

- Si dudás, una sola familia con dos o tres pesos resuelve casi todo.
- Elegí fuentes con buen set de pesos y números; una fuente sin `600`/`700` te deja sin
  jerarquía de peso.

## 6. Números tabulares

En tablas, precios, montos, contadores y cualquier columna de números que se alinea o cambia,
usá cifras de ancho fijo para que no "bailen":

```css
.amount, td.num { font-variant-numeric: tabular-nums; }
```

Para dinero: alineá a la derecha, tabular-nums, y no mezcles la moneda con el número en el
mismo bloque alineado. (Formato y locale: `frontend-i18n-l10n`.)

## 7. `text-wrap` para cortes prolijos

- `text-wrap: balance` reparte las líneas de un **título** corto de forma pareja (evita la
  última palabra huérfana). El navegador lo limita a pocas líneas, así que es para titulares,
  no para párrafos largos.
- `text-wrap: pretty` mejora el corte de **párrafos** (evita huérfanas/viudas). **Verificá el
  soporte por navegador en la doc oficial (MDN/caniuse)** antes de depender de él; degradá con
  gracia si no está.

```css
h1, h2, .card-title { text-wrap: balance; }
p { text-wrap: pretty; } /* progresivo: si no hay soporte, corta normal */
```

## 8. Carga de fuentes (performance)

La fuente entra en la ruta crítica del render y afecta LCP y CLS (ver `frontend-performance`).

- `font-display: swap` para que el texto sea visible mientras carga; contené el salto con una
  fuente de respaldo de métricas parecidas (`size-adjust`, `ascent-override`).
- Autohospedá `.woff2` y `preload` solo la fuente del texto crítico (above the fold); no
  precargues seis pesos.
- **Subset**: incluí solo los rangos de caracteres que usás (latín + los acentos del idioma).
- Bajo SSR, definí las @font-face en CSS servido; no cargues fuentes por JS que llegue tarde.

## Anti-patrones

- Tamaños sueltos fuera de la escala.
- Párrafos a 120+ caracteres de ancho.
- `line-height` en px heredado por varios tamaños.
- Cuatro familias tipográficas "para dar variedad".
- Números proporcionales en tablas y montos (columnas que bailan).
- Cargar todos los pesos de una fuente y matar el LCP.
- Mayúsculas y negrita como única jerarquía.

## Checklist

- [ ] Tamaños salen de una escala modular en `rem`; cuerpo ≥ ~16px.
- [ ] Texto corrido entre 45 y 75 caracteres (`max-width` en `ch`).
- [ ] `line-height` sin unidad; ~1.5 cuerpo, más ajustado en títulos.
- [ ] Máximo dos familias; 3–4 niveles de jerarquía por pantalla.
- [ ] `tabular-nums` en tablas, montos y contadores.
- [ ] `font-display: swap`, `.woff2` subseteado, `preload` solo lo crítico.
- [ ] `text-wrap: pretty` verificado por soporte y con degradación.

Escalas como tokens: `frontend-design-system`. Aplicación en composición: `frontend-ui-design`,
`frontend-beautiful-ui`. Impacto en carga: `frontend-performance`. Formato numérico y locale:
`frontend-i18n-l10n`.
