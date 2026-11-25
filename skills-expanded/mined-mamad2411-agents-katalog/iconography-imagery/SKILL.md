---
name: iconography-imagery
description: Uso de iconos e imágenes en la interfaz — set de iconos consistente (grosor, tamaño, grid), nombre accesible, cuándo icono solo vs icono con texto, ilustraciones y estados vacíos con propósito, imágenes optimizadas con alt correcto, avatares y placeholders, y coherencia de estilo. Usar al agregar un icono a un botón o menú, al elegir o incorporar un set de iconos, al insertar imágenes o ilustraciones, al diseñar un empty state, o al revisar por qué la UI se ve dispareja o pesada.
---

<!-- ESPEJO GENERADO por AtlasPromptManager/tools/install_skills.py - NO EDITAR A MANO -->
<!-- La fuente es AtlasPromptManager/.claude/skills/. Lo que edites aca se pierde. -->

# Iconografía e imágenes

Los iconos y las imágenes aceleran el reconocimiento o lo entorpecen. La regla base: son
**apoyo** del texto y del contenido, casi nunca su reemplazo.

## 1. Set de iconos consistente

- **Un solo set** en todo el producto. Mezclar dos librerías (distinto grosor, distinto
  redondeo) es una de las señales más claras de UI hecha a pedazos.
- Grosor de trazo, tamaño de grid (p. ej. 24) y estilo (línea vs relleno) uniformes. Si
  necesitás un icono que no está, dibujalo en el mismo grid y grosor, no lo traigas de otro set.
- Tamaños desde la escala: alineá el icono a la altura de la línea de texto que acompaña
  (`width: 1em; height: 1em` para que escale con el texto).
- Color por token (`currentColor` o `--color-text-muted`), nunca hex fijo dentro del SVG.

```html
<!-- ✅ el icono hereda color y tamaño del texto -->
<button class="btn">
  <svg width="1em" height="1em" fill="currentColor" aria-hidden="true">…</svg>
  Guardar
</button>
```

## 2. Nombre accesible

- Icono **decorativo** (acompaña a un texto que ya dice lo mismo): `aria-hidden="true"` y sin
  `alt`, para que el lector de pantalla no lo repita.
- Icono **con significado propio** (botón solo-icono): necesita nombre accesible —
  `aria-label` en el botón, o texto visualmente oculto. Sin eso, el botón es mudo.
- No metas información en el icono que no esté también en texto o en su nombre accesible.

```html
<!-- ✅ botón solo-icono con nombre -->
<button aria-label="Cerrar"><svg aria-hidden="true">…</svg></button>
```

Detalle completo de nombres accesibles y foco: `frontend-accessibility`.

## 3. Icono solo vs icono + texto

- Acciones importantes o ambiguas: **icono + texto**. Un icono solo rara vez es universal
  (el disquete, el engranaje y poco más).
- Icono solo: reservalo para acciones muy convencionales y con poco espacio (cerrar, buscar,
  menú), siempre con `aria-label` y, si ayuda, tooltip accesible por teclado.
- No inventes metáforas: si tenés que explicar el icono, poné la palabra.

## 4. Ilustraciones y estados vacíos con propósito

- Las ilustraciones sirven para dar tono en momentos concretos (onboarding, empty states,
  error), no para decorar cada pantalla.
- Un empty state es ilustración discreta + una frase de qué es esto + **la acción** para
  llenarlo. La ilustración no reemplaza el texto de ayuda (ver `frontend-ux-states`).
- Mismo estilo de ilustración en todo el producto; no mezcles flat, 3D y foto.

## 5. Imágenes optimizadas

Las imágenes suelen ser el mayor peso de una página y golpean el LCP (ver `frontend-performance`).

- Formatos modernos (AVIF/WebP) con fallback; comprimí.
- `width`/`height` o `aspect-ratio` **siempre**, para reservar el espacio y evitar CLS.
- Responsivas con `srcset`/`sizes`; no sirvas una imagen de 2000px a un thumbnail.
- `loading="lazy"` fuera del viewport inicial; la imagen del hero, con prioridad, no lazy.
- `alt` que describe la función/contenido; `alt=""` si es puramente decorativa (que no la
  anuncie el lector). No pongas "imagen de …" en el alt.

```html
<img src="doctor.avif" width="96" height="96"
     alt="Foto de perfil de la Dra. Salinas" loading="lazy">
```

## 6. Avatares y placeholders

- Avatar con fallback determinista (iniciales sobre color derivado del nombre) cuando no hay
  foto; nunca un roto ni un genérico distinto cada vez.
- Placeholder con la forma y proporción final (para no saltar al cargar); skeleton, no vacío.
- Recortá con `object-fit: cover` y `aspect-ratio` fijo para que la grilla no se deforme.

## 7. Nunca imagen donde va texto

El texto dentro de una imagen no se traduce, no se busca, no se lee con lector de pantalla, no
escala y pixela. Titulares, precios y etiquetas van como **texto real** sobre la imagen, no
horneados en el JPG.

## Anti-patrones

- Dos librerías de iconos con grosores distintos en la misma pantalla.
- Botón solo-icono sin `aria-label`.
- Icono decorativo sin `aria-hidden` (el lector lo repite).
- Imagen sin `width`/`height` → salto de layout.
- Servir la imagen a resolución completa para un thumbnail.
- Texto importante horneado dentro de una imagen.
- Empty state que es solo un dibujo sin acción.

## Checklist

- [ ] Un único set de iconos; grosor, grid y estilo uniformes; color por `currentColor`/token.
- [ ] Iconos decorativos con `aria-hidden`; iconos con significado con nombre accesible.
- [ ] Acciones ambiguas con icono **+** texto; solo-icono únicamente si es convencional.
- [ ] Imágenes en formato moderno, con `width`/`height` o `aspect-ratio`, `srcset` y `alt` correcto.
- [ ] `loading="lazy"` fuera del viewport; hero con prioridad.
- [ ] Avatares y placeholders con fallback determinista y proporción fija.
- [ ] Ningún texto crítico horneado dentro de una imagen.

Nombres accesibles y foco: `frontend-accessibility`. Peso y LCP: `frontend-performance`.
Empty states: `frontend-ux-states`. Coherencia visual: `frontend-beautiful-ui`.
