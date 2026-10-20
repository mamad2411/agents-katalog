---
name: frontend-responsive-layout
description: Layout responsivo mobile-first para cualquier UI web — breakpoints guiados por contenido, tipografía fluida con clamp(), container queries, layouts intrínsecos con Grid/Flex, imágenes responsivas y unidades de viewport modernas. Usar al maquetar cualquier pantalla o componente nuevo, al adaptar uno existente a más anchos, o al revisar por qué algo se rompe entre mobile y desktop.
---

<!-- ESPEJO GENERADO por AtlasPromptManager/tools/install_skills.py - NO EDITAR A MANO -->
<!-- La fuente es AtlasPromptManager/.claude/skills/. Lo que edites aca se pierde. -->

# Layout responsivo

Objetivo: que el layout se adapte al espacio disponible sin que cada pantalla nueva
sea un breakpoint nuevo hardcodeado. Complementa a `frontend-ux-states` (qué mostrar)
y `frontend-accessibility` (targets táctiles, zoom).

## 1. Mobile-first, siempre

- Escribí el CSS base para el viewport más chico; agregá complejidad con `min-width`
  a medida que crece el espacio. Nunca al revés (`max-width` desde desktop) — termina
  en overrides acumulados y CSS más pesado de lo necesario.
- El contenido y la interacción táctil mandan en el diseño base; el mouse y el espacio
  extra son la mejora progresiva, no la referencia.

```css
/* ✅ mobile-first: base simple, se enriquece hacia arriba */
.card-grid { display: grid; grid-template-columns: 1fr; gap: 1rem; }

@media (min-width: 48rem) {
  .card-grid { grid-template-columns: repeat(2, 1fr); }
}
@media (min-width: 64rem) {
  .card-grid { grid-template-columns: repeat(3, 1fr); }
}
```

## 2. Breakpoints guiados por contenido, no por dispositivo

- No diseñes para "iPhone" o "iPad": diseñá para el punto donde TU contenido se ve mal
  (texto que se aprieta, tarjetas que se aplastan, tabla que no entra) y ponés el
  breakpoint ahí. Los dispositivos cambian de tamaño constantemente; el contenido es
  la referencia estable.
- Un set chico y consistente de breakpoints reusados en todo el sistema (ej. ~30rem,
  48rem, 64rem, 80rem) es mejor que uno por componente — facilita mantenimiento y
  coherencia visual entre secciones.
- Usá unidades relativas (`rem`/`em`) en los breakpoints, no `px`: así respetan el
  zoom de fuente del usuario en vez de romperse a un tamaño de texto fijo.

## 3. Container queries: adaptar el componente, no la página

- Un componente reusado en distintos contextos (sidebar angosto, grid ancho, modal)
  no puede depender del viewport global — depende del espacio que le da SU contenedor.
  Para eso son las container queries, no un breakpoint más de media query.
- Declará el contenedor con `container-type` (`inline-size` para consultar solo el
  ancho, `size` para ancho y alto) y opcionalmente `container-name`; consultá con `@container`.

```css
.card-wrapper { container-type: inline-size; container-name: card; }

@container card (min-width: 24rem) {
  .card { grid-template-columns: auto 1fr; } /* imagen + texto lado a lado */
}
```

- Regla práctica: `@media` para decisiones de layout de página completa (columnas
  globales, nav colapsado); `@container` para cómo se comporta un componente dentro
  del espacio que le tocó.

## 4. Tipografía fluida con `clamp()`

- `clamp(mínimo, preferido, máximo)` interpola el tamaño entre dos extremos sin saltos
  de breakpoint — el valor preferido normalmente usa `vw` para escalar con el viewport.
- Usalo para tamaños de fuente y espaciados grandes (títulos, hero, padding de secciones);
  para texto de cuerpo, un tamaño fijo legible suele ser más predecible.

```css
h1 { font-size: clamp(1.75rem, 1.2rem + 2.5vw, 3rem); }
```

## 5. Layouts intrínsecos: dejá que el contenido decida

- Preferí que el propio contenido determine cuántas columnas entran antes que fijar
  un número de columnas por breakpoint:

```css
/* Grid que auto-ajusta columnas según el ancho disponible, sin media queries */
.grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(16rem, 1fr));
  gap: 1rem;
}
```

- Flexbox con `flex-wrap` + `flex-basis` para filas que se acomodan solas
  (`flex: 1 1 16rem`) cuando no necesitás alineación en dos ejes.
- Evitá anchos fijos en `px` para contenedores de contenido; usá `max-width` +
  `width: 100%` para que se encoja en pantallas chicas.

## 6. Unidades de viewport modernas

- `100vh` mide el viewport ignorando las barras de navegador móviles que aparecen/
  desaparecen al hacer scroll — produce layouts que "saltan" o cortan contenido.
- `dvh` (dynamic viewport height) se ajusta en vivo al espacio real visible; `svh`
  (small) asume las barras del navegador siempre visibles; `lvh` (large) asume que
  están ocultas. Para pantallas completas en mobile, `100dvh` es la opción segura.

```css
.full-screen-modal { min-height: 100dvh; } /* no 100vh en mobile */
```

## 7. Imágenes y medios responsivos

- `srcset` + `sizes` para que el navegador elija la resolución correcta según el
  viewport real, en vez de servir siempre la imagen más grande.
- `<picture>` con `<source>` cuando necesitás arte dirigido (recorte distinto según
  ancho, no solo resolución distinta).
- `width`/`height` (o `aspect-ratio` en CSS) siempre presentes para reservar espacio
  y evitar layout shift mientras carga — ver `frontend-performance` (CLS).

```html
<img
  src="foto-800.jpg"
  srcset="foto-400.jpg 400w, foto-800.jpg 800w, foto-1200.jpg 1200w"
  sizes="(min-width: 64rem) 33vw, 100vw"
  width="800" height="600" alt="Descripción del contenido de la imagen"
/>
```

## 8. Targets táctiles y safe areas

- En viewports táctiles, todo elemento interactivo respeta el mínimo de 24×24px de
  `frontend-accessibility` — el espacio "responsivo" no es excusa para achicar botones.
- En dispositivos con notch/gestos, respetá los safe areas con
  `env(safe-area-inset-top|right|bottom|left)` en elementos fijos a los bordes
  (headers, bottom nav, FABs).

## 9. Matriz de testing mínima

Probá cada pantalla tocada en, como mínimo:

| Ancho aprox. | Qué mirar |
|---|---|
| ~360px (mobile chico) | nada se corta ni desborda horizontalmente; texto legible sin zoom |
| ~768px (tablet / mobile grande apaisado) | transición de 1 a 2 columnas sin huecos raros |
| ~1024–1280px (desktop chico) | densidad de contenido, nav completo si corresponde |
| ~1920px (desktop grande) | contenido no se estira a un ancho ilegible (usar `max-width`) |
| Con zoom de texto al 200% | layout no rompe (WCAG 1.4.4 — ver `frontend-accessibility`) |

## Anti-patrones

- `max-width` desktop-first con overrides acumulados hacia abajo.
- Breakpoints ad hoc por componente (`@media (max-width: 897px)`) sin relación con
  el resto del sistema.
- `100vh` para pantallas completas en mobile.
- Anchos fijos en `px` para contenedores de texto/tarjetas.
- Servir siempre la imagen más pesada porque "así se ve bien en desktop".
- Ocultar contenido en mobile con `display: none` en vez de reordenar/priorizar
  (si la info importa, tiene que estar en algún lado accesible).

## Checklist

- [ ] CSS base mobile-first; complejidad agregada con `min-width`.
- [ ] Breakpoints elegidos por dónde se rompe el contenido, en `rem`, reusados del sistema.
- [ ] Componentes reusados en distintos contenedores usan container queries, no solo media queries.
- [ ] Tipografía/espaciado grande con `clamp()` donde tiene sentido escalar.
- [ ] Grid/Flex intrínsecos (`auto-fit`/`minmax`, `flex-basis`) antes que columnas fijas por breakpoint.
- [ ] `dvh`/`svh` en vez de `vh` para pantallas completas en mobile.
- [ ] Imágenes con `srcset`/`sizes` y `width`/`height` o `aspect-ratio` reservado.
- [ ] Targets táctiles ≥24×24px; safe areas respetados en elementos fijos a bordes.
- [ ] Probado en la matriz de anchos mínima, incluido zoom de texto 200%.
