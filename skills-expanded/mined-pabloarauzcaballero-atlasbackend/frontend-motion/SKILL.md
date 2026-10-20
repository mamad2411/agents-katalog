---
name: frontend-motion
description: Principios y técnica de animación de interfaz — CSS transitions/keyframes, View Transitions API, animaciones nativas de Angular (`animate.enter`/`animate.leave`) y la librería Motion vanilla (motion.dev) usada desde Angular con guardas de SSR. Usar al animar entradas/salidas, transiciones de ruta, listas, gestos, animación ligada al scroll o cualquier microinteracción — para decidir duración, easing y herramienta sin romper accesibilidad, SSR ni performance.
---

<!-- ESPEJO GENERADO por AtlasPromptManager/tools/install_skills.py - NO EDITAR A MANO -->
<!-- La fuente es AtlasPromptManager/.claude/skills/. Lo que edites aca se pierde. -->

# Movimiento de interfaz

El movimiento comunica, no decora. Cada animación existe para: (1) mostrar jerarquía
(qué apareció, qué es importante), (2) explicar causa-efecto (esto pasó porque tocaste
eso), o (3) dar continuidad espacial (de dónde vino, a dónde va este elemento). Si una
animación no cumple ninguna de las tres, sacala.

## 1. Elegí la herramienta correcta

| Necesitás | Usá |
|---|---|
| Hover/focus, cambio de estado de un elemento que ya está en el DOM | CSS `transition` |
| Secuencia con pasos, loop acotado (skeleton, spinner) | CSS `@keyframes` |
| Entrada/salida de un nodo que se monta/desmonta (`@if`, `@for`) | Angular `animate.enter` / `animate.leave` + clases CSS |
| Transición entre rutas o entre dos estados completos de una vista | View Transitions API (`withViewTransitions()` en el router) |
| Springs, stagger calculado, animación ligada al scroll o a un gesto, secuencias imperativas | Motion vanilla (`animate`, `stagger`, `scroll`, `inView` de `"motion"`) |

CSS primero: menos JS, el navegador anima en el hilo de composición y funciona igual
bajo SSR. Subí a JS solo cuando necesitás física, progreso de scroll o coordinar varios
elementos con valores calculados en runtime.

## 2. Duraciones y easing por tipo de interacción

| Interacción | Duración | Easing |
|---|---|---|
| Micro (hover, toggle, ripple) | 100–150ms | `ease-out` |
| Entrada de elemento (aparece, se expande) | 200–300ms | `ease-out` (rápido al empezar, se asienta) |
| Salida de elemento (desaparece, colapsa) | 150–200ms | `ease-in` (acelera al irse) — más corta que la entrada |
| Transición de layout/página | 300–500ms | `ease-in-out` o spring suave |
| Elementos grandes o que cubren la pantalla (modal, drawer) | 300–400ms | spring con `bounce` bajo o `ease-in-out` |

Son valores de partida de la casa, no un estándar: ajustalos mirando la interacción real.
Regla: la salida es siempre más corta o igual que la entrada. Nunca superes ~500ms para
algo que el usuario disparó a propósito: se siente lento, no elegante. Guardá duraciones
y curvas como tokens (`--motion-fast`, `--ease-out`) — ver `frontend-design-system`.

## 3. CSS: transiciones, keyframes y `@starting-style`

```css
.card {
  transition: transform var(--motion-fast) var(--ease-out),
              box-shadow var(--motion-fast) var(--ease-out);
}
.card:hover { transform: translateY(-2px); }

@media (prefers-reduced-motion: reduce) {
  .card { transition: none; }
}
```

Listá las propiedades una por una: `transition: all` anima cosas que no querías (layout,
color) y complica el reduced-motion. Para animar con `transition` un elemento que recién
entra al DOM, el estado inicial se declara con `@starting-style` (verificá soporte de
navegadores en MDN antes de depender de él sin fallback).

## 4. Angular: `animate.enter` y `animate.leave`

`@angular/animations` está **deprecado desde Angular v20.2**; el reemplazo oficial es CSS
nativo con `animate.enter`/`animate.leave`, que son sintaxis del compilador (no
directivas: no se importan). No podés mezclarlos con animaciones legadas en el mismo
componente.

```html
@if (open()) {
  <aside class="panel" animate.enter="panel-in" animate.leave="panel-out">…</aside>
}
```

```css
.panel-in  { animation: panel-in 240ms var(--ease-out); }
.panel-out { animation: panel-out 180ms ease-in; }

@keyframes panel-in  { from { opacity: 0; transform: translateY(8px); } }
@keyframes panel-out { to   { opacity: 0; transform: translateY(8px); } }
```

- Angular quita el nodo cuando termina la animación o transición más larga de la clase
  de salida. También aceptan binding (`[animate.enter]="claseSignal()"`).
- Un `animate.leave` en un hijo solo dispara si el nodo que se remueve está en el mismo
  template; no dispara dentro de componentes anidados cuando se remueve el padre.
- En tests, `TestBed` deshabilita las animaciones por defecto (`animationsEnabled: true`
  para activarlas).

## 5. View Transitions para rutas

```ts
provideRouter(routes, withViewTransitions())
```

Es mejora progresiva: sin soporte del navegador, el router navega sin animar. El default
es un crossfade; se personaliza con `view-transition-name` en el elemento compartido y
los pseudo-elementos `::view-transition-old()` / `::view-transition-new()`. Con
`onViewTransitionCreated` podés llamar `transition.skipTransition()` (por ejemplo cuando
solo cambian query params). Desactivá o reducí las transiciones bajo
`prefers-reduced-motion`.

## 6. Motion vanilla desde Angular (con guardas de SSR)

Motion toca el DOM: nunca corre en el servidor. Ejecutalo dentro de `afterNextRender`
(solo corre en navegador) y cancelá al destruir.

```ts
import { afterNextRender, Component, DestroyRef, ElementRef, inject, viewChild } from '@angular/core';
import { animate, stagger } from 'motion';

@Component({ selector: 'app-result-list', template: `<ul #list>…</ul>` })
export class ResultList {
  private list = viewChild.required<ElementRef<HTMLElement>>('list');

  constructor() {
    const destroyRef = inject(DestroyRef);
    afterNextRender(() => {
      if (matchMedia('(prefers-reduced-motion: reduce)').matches) return;
      const controls = animate(
        this.list().nativeElement.querySelectorAll('li'),
        { opacity: [0, 1], transform: ['translateY(6px)', 'translateY(0)'] },
        { duration: 0.24, delay: stagger(0.05) },
      );
      destroyRef.onDestroy(() => controls.stop());
    });
  }
}
```

- Motion mide en **segundos**; CSS en ms. No los mezcles al copiar valores.
- Springs: `animate(el, { transform: 'translateX(100px)' }, { type: spring, stiffness: 400 })`
  con `spring` importado de `"motion"`. Usalos para lo que el usuario arrastra o suelta
  (se interrumpen bien); curvas de tiempo para lo que debe terminar sincronizado.
- Scroll: `scroll(animate(el, { opacity: [0, 1] }))` liga la animación al progreso del
  scroll; `scroll()` devuelve una función de cancelación — llamala en `onDestroy`.
- Las controls son *thenable*: `await controls` espera el fin de la animación.
- Para una salida con JS, usá el evento: `(animate.leave)="onLeave($event)"` y llamá
  `event.animationComplete()` al terminar; si no lo llamás, Angular remueve el nodo
  recién al vencer `MAX_ANIMATION_TIMEOUT`.

React: el mismo paquete expone componentes declarativos en `motion/react` (`motion.*`,
`AnimatePresence`, `layout`). No aplica al stack de la casa; si un proyecto usa React,
verificá la API en motion.dev.

## 7. Performance

- Animá solo `transform` y `opacity`: el compositor las mueve sin recalcular layout ni
  pintar. Animar `width`, `top/left`, `margin` o `box-shadow` dispara layout/paint por frame.
- `will-change` solo en el elemento que va a animar y solo mientras dure la interacción.
- No escribas signals ni dispares change detection en cada frame de un gesto o del
  scroll; dejá que la librería o el CSS muevan el DOM directamente.
- En listas largas animá solo lo visible o lo nuevo; nunca miles de filas.
- Reservá el espacio del elemento que entra para no mover CLS (ver `frontend-performance`).

## 8. Anti-patrones

- Misma duración/easing para todo "porque queda parejo" — cada interacción tiene su peso (§2).
- Loops decorativos infinitos: gastan batería y no comunican nada tras el primer ciclo.
- Ignorar `prefers-reduced-motion`: mareo real para personas con trastornos vestibulares
  (ver `frontend-accessibility`).
- Parallax o scroll-jacking que le quita al usuario el control del scroll nativo.
- Código nuevo con `@angular/animations` (`trigger`, `state`, `transition`).
- Tocar `window`/`document` para animar fuera de `afterNextRender` (rompe SSR — ver
  el render del servidor).

## Checklist

- [ ] Cada animación tiene un propósito (jerarquía, causa-efecto o continuidad); si no, se elimina.
- [ ] Se eligió la herramienta más simple que alcanza (CSS → Angular nativo → View Transitions → Motion).
- [ ] Duración de salida ≤ duración de entrada; nada disparado por el usuario pasa de ~500ms.
- [ ] Solo se anima `transform`/`opacity`; sin `transition: all`.
- [ ] `prefers-reduced-motion` respetado en CSS y en el código JS.
- [ ] Todo código de animación JS corre en `afterNextRender` y se cancela al destruir.
- [ ] `animate.leave` por evento llama siempre a `animationComplete()`.
- [ ] Duraciones y curvas salen de tokens, no de literales sueltos.
