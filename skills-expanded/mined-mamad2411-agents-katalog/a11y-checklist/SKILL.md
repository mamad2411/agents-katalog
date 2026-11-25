---
name: a11y-checklist
description: Checklist de accesibilidad WCAG 2.2 AA para diseño y maquetacion en dev-team - contraste, tipografia, foco y teclado, targets, formularios, movimiento, estructura semantica, imagenes y 3D/canvas, con como verificar cada punto (browser_snapshot, axe). Cargala al diseñar, maquetar o auditar cualquier pantalla.
---

# Accesibilidad WCAG 2.2 AA — checklist operativa (dev-team)

Marca cada punto con evidencia (captura, snapshot o resultado de axe). Sin evidencia,
no esta cumplido.

## Percepcion
- [ ] Contraste texto ≥ 4.5:1 (≥ 3:1 en texto ≥ 24 px o 19 px bold); UI y bordes de
      campos ≥ 3:1. Calculado, no estimado.
- [ ] Nada se comunica SOLO por color (estado, error, seleccion): icono, texto o forma.
- [ ] Texto real, nunca texto dentro de imagenes. Imagenes con `alt` util (o `alt=""`
      si son decorativas). Ilustraciones SVG con `role="img"` + `aria-label` o `aria-hidden`.
- [ ] Zoom 200 % sin perdida de contenido; texto fluido con `clamp()`, sin alturas fijas.
- [ ] `prefers-reduced-motion` respetado; `prefers-color-scheme` respetado si hay modo oscuro.

## Operacion
- [ ] Todo se puede usar con teclado: orden de tabulacion logico, sin trampas de foco,
      atajos sin colisiones.
- [ ] **Foco visible** siempre (anillo ≥ 2 px, contraste ≥ 3:1), no `outline: none` sin reemplazo.
- [ ] Targets ≥ 24x24 CSS px (WCAG 2.2 2.5.8) — en dev-team exigimos **≥ 44 px** en tactil.
- [ ] Arrastrar/soltar tiene alternativa sin arrastre (2.5.7).
- [ ] Nada parpadea > 3 veces/seg; autoplay controlable; sin limites de tiempo ocultos.

## Comprension
- [ ] Idioma declarado (`lang`); textos en lenguaje del usuario; errores dicen QUE paso y
      COMO resolverlo, asociados al campo (`aria-describedby`).
- [ ] Etiquetas visibles en formularios (placeholder NO es etiqueta); ayuda consistente
      en el mismo lugar (3.2.6); no pedir re-tipear lo ya ingresado (3.3.7).
- [ ] Autenticacion accesible: sin pruebas cognitivas obligatorias (3.3.8); pegar permitido.

## Robustez y estructura
- [ ] Un `h1` por pantalla; jerarquia de encabezados sin saltos; landmarks
      (`header/nav/main/aside/footer`).
- [ ] Componentes con roles/estados ARIA correctos (tabs, dialog, menu, listbox, switch);
      preferir elementos nativos (`button`, `a`, `select`).
- [ ] Mensajes dinamicos con `aria-live` (toasts `role="status"`, errores `role="alert"`).
- [ ] Canvas/3D: `aria-hidden`, informacion equivalente en HTML, fallback 2D.

## Como verificar
- Exploratorio: Playwright MCP `browser_snapshot` (arbol de accesibilidad: roles,
  nombres, estados), `browser_take_screenshot` con foco visible, `browser_resize` a 375.
- Automatico: `@axe-core/playwright` en la suite E2E (`tests/a11y/`), 0 violaciones
  `critical`/`serious` (puerta 5 de QA).
- Contraste: calcular (formula WCAG) y anotar en `design-spec.md`.
