---
name: mobile-ux-design
description: Diseño de experiencia para la app móvil (Flutter) — targets táctiles, navegación por gestos, safe areas y notch, manejo del teclado, estados offline/carga/error, feedback háptico, diferencias iOS/Android y accesibilidad móvil. Usar al diseñar o revisar cualquier pantalla, flujo o componente de la app nativa, al portar una vista web a móvil, o cuando algo "en el celular se siente incómodo" (se tapa con el teclado, cuesta tocar, no respeta el notch).
effort: high
---

<!-- ESPEJO GENERADO por AtlasPromptManager/tools/install_skills.py - NO EDITAR A MANO -->
<!-- La fuente es AtlasPromptManager/.claude/skills/. Lo que edites aca se pierde. -->

# UX móvil — Flutter

La app móvil no es la web en chico. El pulgar es el cursor, la conexión se corta y el
sistema operativo impone convenciones. Diseñá para la mano, no para el mouse.

## 1. Objetivos táctiles

- Área tocable mínima **48x48 dp** (Material) / ~44x44 pt (Apple HIG). Si el ícono es más
  chico, ampliá el área con `padding` o un `IconButton` (que ya trae área mínima), no el glifo.
- Separación entre objetivos tocables para no errar el dedo.
- Lo más usado, al alcance del pulgar (zona inferior). Acciones destructivas lejos de esa zona.
- Nada de hover como única vía: en móvil no existe. Todo estado debe alcanzarse por toque.

## 2. Navegación y gestos

- Usá los patrones del sistema: `Navigator`/rutas, `BottomNavigationBar`/`NavigationBar` para
  secciones, gesto de volver atrás (swipe en iOS). No reinventes el "back".
- Un gesto no puede ser la única forma de hacer algo importante: ofrecé también un control visible.
- Evitá gestos que choquen con los del sistema (swipe desde el borde = volver).
- `SafeArea` siempre alrededor del contenido de borde: respeta notch, barra de estado y home indicator.

## 3. Teclado

- El teclado tapa medio pantalla. Envolvé formularios en `SingleChildScrollView` /
  `Scaffold(resizeToAvoidBottomInset: true)` (default) para que el campo enfocado quede visible.
- `TextInputType` correcto por campo (`.emailAddress`, `.number`, `.phone`) y `textInputAction`
  (`.next`/`.done`) para encadenar campos.
- Botón de acción principal accesible con el teclado abierto, o que el scroll lo alcance.

## 4. Estados de pantalla

Toda vista que trae datos resuelve, como en web (ver `frontend-ux-states`):

| Estado | Tratamiento móvil |
|---|---|
| Carga | Skeleton o spinner; nunca pantalla en blanco congelada |
| Vacío | Mensaje + acción; no una lista vacía muda |
| Error | Mensaje claro + reintentar; distinguir "sin conexión" de "falló el server" |
| Offline | Banner persistente de estado de red; datos cacheados marcados como tales |
| Éxito parcial | Mostrar lo que hay + indicar lo que falta |

Offline es un estado de primera clase en móvil, no una excepción (ver `mobile-offline-sync`).

## 5. Feedback

- Háptico para acciones significativas: `HapticFeedback.lightImpact()` / `selectionClick()`
  (verificá la variante exacta en la API de `services`). Con moderación; no vibrar por todo.
- Feedback inmediato al toque (ripple en Android, opacidad en iOS): usá los widgets con
  `InkWell`/`InkResponse` o los `Cupertino*` según plataforma.
- Confirmá acciones destructivas; ofrecé deshacer donde se pueda (`SnackBar` con acción).

## 6. iOS vs Android

- Respetá las convenciones de cada uno donde importa: diálogos, selectores de fecha, el "back",
  tipografía del sistema. Material en Android; considerá widgets `Cupertino*` en iOS para
  controles muy convencionales.
- Un mismo tema de marca puede convivir con controles nativos por plataforma.
- Probá en ambos: lo que se ve bien en un emulador Android puede romperse con el notch de un iPhone.

## 7. Accesibilidad móvil

- `Semantics` con etiqueta en íconos y controles sin texto; `excludeSemantics` donde duplica.
- Respetá el tamaño de fuente del sistema (`MediaQuery.textScaler`): no fijes tamaños que
  se rompan al agrandar el texto. Probá con fuente grande.
- Contraste AA. No comuniques solo por color.
- Probá con TalkBack (Android) y VoiceOver (iOS), navegación por foco.

## Checklist
- [ ] Todo objetivo tocable ≥ 48dp y separado de sus vecinos.
- [ ] Contenido dentro de `SafeArea`; nada tapado por notch ni home indicator.
- [ ] El teclado no tapa el campo enfocado ni el botón de acción.
- [ ] Los cinco estados resueltos, con offline como banner explícito.
- [ ] Gestos con alternativa visible; no chocan con los del sistema.
- [ ] Háptico solo en acciones significativas.
- [ ] Probado en iOS y Android reales/emuladores, con fuente grande y lector de pantalla.
