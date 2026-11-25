---
name: carousel-instagram
description: "Crear carruseles de Instagram en HTML con slides personalizados (1080x1350px), exportacion PNG. Elige tu propio handle/marca de agua. Incluye todo el sistema de diseno — colores, tipografia, componentes y plantilla lista. NO necesita explicar colores ni estructura."
---

# Skill: Carrusel Instagram

Genera carruseles de Instagram en formato HTML listo para abrir en el navegador y exportar como PNG. Usa la plantilla bundled en `assets/carousel-template.html` como base, rellena con el contenido indicado por el usuario, y guarda el resultado como un nuevo archivo `.html` en la carpeta del proyecto.

---

## Flujo de trabajo

1. **Preguntar** cuántos slides quiere antes de generar (ver sección abajo)
2. **Leer** `assets/carousel-template.html` (la plantilla base con todos los estilos)
3. **Generar** los slides según la cantidad indicada, manteniendo siempre el slide 01 (portada) y el último como CTA final
4. **Guardar** como `[tema]-slides.html` en la carpeta de trabajo activa del usuario (workspace folder conectada en Cowork)
5. **Compartir** el link al archivo para que el usuario lo abra

---

## Cantidad de slides — SIEMPRE preguntar primero

Antes de generar cualquier carrusel, preguntarle al usuario cuántos slides quiere. El mínimo es 3 (portada + 1 contenido + CTA final). No hay máximo.

Ejemplo de pregunta:
> "¿Cuántos slides querés para este carrusel? El mínimo es 3. Por defecto son 7, pero podés pedir los que necesites."

Si el usuario ya especificó la cantidad en su mensaje (ej. "hacé un carrusel de 10 slides"), no preguntar — usar ese número directamente.

### Cómo adaptar la cantidad

- **Slide 01** (portada) y **slide final** (CTA) son SIEMPRE fijos, independientemente del total
- Los slides de contenido del medio se agregan o quitan según la cantidad pedida
- El `id` de cada slide va en orden: `slide-0`, `slide-1`, ..., `slide-N`
- El slide CTA final siempre tiene el `id` del último (ej. para 10 slides: `id="slide-9"`)
- Actualizar la variable `total` en el JS: `let cur = 0, total = N;`
- Actualizar el texto del botón export: `⬇ Exportar N slides PNG`
- El CSS de `#slide-6` (slide final) debe cambiarse al id correcto del último slide

### Ejemplo: carrusel de 10 slides

```
slide-0  → Portada
slide-1  → Contenido 1
slide-2  → Contenido 2
slide-3  → Contenido 3
slide-4  → Contenido 4
slide-5  → Contenido 5
slide-6  → Contenido 6
slide-7  → Contenido 7
slide-8  → Contenido 8
slide-9  → CTA Final (background: #0d0b2a)
```

CSS a ajustar:
```css
#slide-9 { justify-content: flex-start; padding: 0; background: #0d0b2a; }
```

JS a ajustar:
```js
let cur = 0, total = 10;
```

---

## Datos fijos — NUNCA cambiar

| Variable | Valor |
|---|---|
| Handle | El handle de Instagram del usuario (ej. @tu-cuenta o el que indique el usuario) |
| Formato | 1080 × 1350 px |
| Slides | Variable (preguntar al usuario, mínimo 3) |
| Idioma | Español rioplatense (voseo: "usás", "hacés") |
| Exportar | Botón PNG via html-to-image (jsDelivr CDN) |

---

## Paleta de colores

| Uso | Valor |
|---|---|
| Fondo body | `#0a0920` |
| Fondo slide | `#131139` |
| Fondo slide final (07) | `#0d0b2a` |
| Overlay imagen | `linear-gradient(to top, #131139 35%, rgba(19,17,57,0.55) 70%, rgba(19,17,57,0.3) 100%)` |
| Acento degradado | `linear-gradient(90deg, #FA743F 0%, #A406E9 100%)` |
| Divider | `linear-gradient(90deg, #FA743F, #A406E9)` |
| Texto principal | `#fff` |
| Texto desc/secundario | `#94a3b8` |
| Texto cards | `#7c8da4` |
| Handle | `rgba(255,255,255,0.88)` |

---

## Tipografía

| Clase CSS | Tamaño | Peso | Uso |
|---|---|---|---|
| `.h-hero` | `clamp(104px,14vw,168px)` | 900 | Título portada |
| `.h-main` | `clamp(96px,13vw,156px)` | 800 | Títulos slides 02–06 |
| `.h-final` | `clamp(106px,14vw,172px)` | 900 | Título CTA final |
| `.desc-hero` | `clamp(32px,4vw,48px)` | 400 | Descripción portada |
| `.desc` | `clamp(33px,4.2vw,48px)` | 400 | Descripción slides internos |
| `.card h3` | `clamp(34px,4vw,50px)` | 700 | Título card |
| `.card p` | `clamp(26px,3vw,36px)` | 400 | Texto card |

- Font: `'Segoe UI', system-ui, -apple-system, sans-serif`
- Letter-spacing títulos: `-0.025em` a `-0.035em`
- Line-height títulos: `1.05`–`1.08`

---

## Handle / Marca de agua

Siempre dentro del `<div class="slide">`, antes del contenido:
```html
<div class="handle">[HANDLE_USUARIO]</div>
```
- Donde `[HANDLE_USUARIO]` es el handle de Instagram configurado por el usuario (ej: `@mi_usuario`). Si el usuario no especifica su handle, usar `@tu-cuenta` por defecto.
- Slides 02–06: `font-size: 28px` (definido en CSS global)
- Slide 01 portada: `font-size: 40px` (override `#slide-0 .handle`)
- Posición: `top: 46px; right: 60px`

---

## Label de producto (opcional por slide)

Aparece top-left en slides que lo necesitan. NO poner si el slide está muy cargado de contenido.

```html
<div style="position: absolute; top: 52px; left: 60px; z-index: 5; display: flex; align-items: center; gap: 10px; pointer-events: none; white-space: nowrap;">
  <div style="width: 22px; height: 22px; border-radius: 6px; background: linear-gradient(135deg,#FA743F,#A406E9); flex-shrink: 0;"></div>
  <span style="font-size: 22px; font-weight: 900; letter-spacing: -0.01em; color: rgba(255,255,255,0.85); white-space: nowrap;">
    Marca <span style="background: linear-gradient(90deg,#FA743F,#A406E9); -webkit-background-clip:text; -webkit-text-fill-color:transparent; background-clip:text;">Producto</span>
  </span>
</div>
```

---

## Componentes disponibles (ya en la plantilla CSS)

### 2 columnas de cards
```html
<div class="cols">
  <div class="card">
    <div class="ico ico-orange sm"><svg viewBox="0 0 24 24">...</svg></div>
    <h3>Título</h3>
    <p>Descripción</p>
  </div>
  <div class="card">...</div>
</div>
```

### 3 columnas
```html
<div class="cols-3">
  <div class="card">...</div>
</div>
```

### Pills (tags)
```html
<div class="pills">
  <div class="pill blue">Texto</div>
  <div class="pill purple">Texto</div>
  <div class="pill green">Texto</div>
</div>
```

### Números grandes
```html
<div class="bcard hi">
  <div class="bnum">95%</div>
  <div class="blabel">Descripción corta</div>
</div>
```

### Divider decorativo
```html
<div class="divider"></div>
```

### Colores de iconos
`ico-blue` | `ico-purple` | `ico-orange` | `ico-green` | `ico-teal` | `ico-pink`
Tamaños: `.ico` (normal) | `.ico.sm` (pequeño) | `.ico.xl` (grande)

---

## Estructura de cada slide

### Slide 01 — Portada
- `id="slide-0"`, `class="slide active"`
- Layout: `justify-content: flex-end` (contenido abajo-izquierda)
- Título con `.h-hero` + `.accent` en la parte más impactante
- Descripción: `.desc-hero`, max-width 680px
- Imagen de fondo opcional: usar patrón de overlay (ver sección abajo) — NO usar `mask-image`

### Slides 02–06 — Contenido
- `id="slide-1"` a `id="slide-5"`, `class="slide"`
- Layout: `justify-content: flex-end`, padding `52px 60px 64px`
- Siempre incluir `<div class="glow"></div>` para el halo superior
- Si el slide tiene imagen abajo + contenido arriba: usar `justify-content: flex-start` con `padding-top` adecuado en CSS

### Slide 07 — CTA Final
- `id="slide-6"`, `class="slide"`, `background: #0d0b2a`
- Estructura FIJA — no modificar el layout:
  - `.final-top`: pregunta principal + subtítulo motivador
  - `.final-bar`: "Seguinos para más contenido" + el handle del usuario + íconos GUARDA/COMPARTE/COMENTA
- Sin badges de número, sin emojis decorativos

---

## Reglas de contenido

- **Sin badges** de número de slide (ej. "04 / 07") — eliminados definitivamente
- **Sin emojis** decorativos en slide final
- **Acento** (degradado naranja→morado) siempre en la palabra/frase más impactante del título
- **Máximo 2 cards** por slide en layout de 2 columnas para que respiren
- Imágenes de producto: siempre con overlay encima para legibilidad
- Slide 01: pregunta directa o dato fuerte que genere curiosidad
- `white-space: nowrap` en textos del label de producto y follow-label para evitar que se partan en 2 líneas al exportar

---

## Imagen de fondo portada (slide 01) — patrón con overlay

**IMPORTANTE:** NO usar `mask-image` — no es compatible con exportadores de PNG.
En su lugar, usar dos divs: la imagen sin máscara + un overlay gradient encima que simula el fade.

```html
<!-- Imagen esquina derecha con fade lateral — compatible con export PNG -->
<div style="position: absolute; right: 0; top: 0; width: 780px; height: 1350px; z-index: 1; pointer-events: none; overflow: hidden;">
  <!-- Imagen sin máscara -->
  <div style="width: 100%; height: 100%;
    background: url('URL_IMAGEN') center top/cover no-repeat;">
  </div>
  <!-- Overlay que simula el fade (reemplaza mask-image) -->
  <div style="position: absolute; inset: 0;
    background: linear-gradient(to right,
      #131139 0%, #131139 2%,
      rgba(19,17,57,0.92) 12%,
      rgba(19,17,57,0.65) 30%,
      rgba(19,17,57,0.25) 55%,
      transparent 80%, transparent 100%);">
  </div>
</div>
<div style="position: absolute; inset: 0; background: radial-gradient(ellipse at 70% 40%, rgba(19,17,57,0) 0%, rgba(19,17,57,0.55) 55%, #131139 80%); z-index: 2; pointer-events: none;"></div>
```

Para imágenes externas (Cloudinary u otras URLs), usar directamente la URL en `background: url('...')`.

---

## Exportación (ya configurada en la plantilla)

- **Librería:** `html-to-image` desde jsDelivr CDN
  - `https://cdn.jsdelivr.net/npm/html-to-image@1.11.11/dist/html-to-image.min.js`
- **Por qué html-to-image en vez de dom-to-image o html2canvas:**
  - Soporta `-webkit-background-clip: text` → texto degradado correcto en PNG
  - Soporta overlays, radial-gradient y CSS moderno
  - Maneja imágenes externas (Cloudinary) via fetch con CORS
- Resolución: 1080 × 1350 px exactos (`pixelRatio: 1`)
- Nombre archivos: `[tema]-slide-01.png` ... `[tema]-slide-07.png`
- UI (flechas, nav, contador, botón export) se excluyen con `filter` durante export
- El handle del usuario SÍ aparece en el export (está dentro del slide)

---

## Escala en pantalla

```js
const s = Math.min(window.innerWidth / 1080, window.innerHeight / 1350);
wrapper.style.transform = `scale(${s})`;
```
