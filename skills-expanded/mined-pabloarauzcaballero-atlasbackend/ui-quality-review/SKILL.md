---
name: ui-quality-review
description: Gate de revisión de calidad visual de una pantalla ya construida — rúbrica puntuable (jerarquía, alineación, espaciado, consistencia con el sistema, contraste, densidad, estados, pulido), catálogo "anti-slop" de señales de UI genérica o hecha por IA, severidad por hallazgo y evidencia antes/después. Usar como pasada final antes de dar una pantalla por terminada, al revisar un PR que agrega o cambia UI, o para diagnosticar por qué una interfaz "correcta" se ve barata o templada.
allowed-tools: Read Grep Glob Bash
effort: high
---

<!-- ESPEJO GENERADO por AtlasPromptManager/tools/install_skills.py - NO EDITAR A MANO -->
<!-- La fuente es AtlasPromptManager/.claude/skills/. Lo que edites aca se pierde. -->

# Revisión de calidad de UI — gate visual

No es una opinión ("me gusta / no me gusta"): es una rúbrica con evidencia. Esta skill
audita una pantalla **terminada** contra criterios medibles. La construcción la cubren
`frontend-ui-design` (estructura), `frontend-beautiful-ui` (pulido) y `visual-hierarchy-composition`
(dirigir la mirada); acá se **puntúa y se decide** si pasa.

> Requiere ver la pantalla real. Una revisión sin capturas por viewport es inválida —
> ver `visual-proof`.

## 1. Rúbrica (0 = ausente, 1 = con defectos, 2 = correcto)

| # | Dimensión | Qué se mira | Pasa con |
|---|---|---|---|
| 1 | Jerarquía | Un único foco primario; el orden visual coincide con el de importancia | 2 |
| 2 | Alineación y grilla | Todo sobre una grilla; sin bordes que bailan por 1-3 px | 2 |
| 3 | Espaciado | Escala consistente (4/8); el espacio agrupa y separa a propósito | 2 |
| 4 | Consistencia con el sistema | Usa tokens y componentes existentes, no valores sueltos | 2 |
| 5 | Contraste / accesibilidad | Texto 4.5:1, UI y texto grande 3:1; no depende solo del color | 2 |
| 6 | Densidad | Ni ahogada ni desértica; medida de línea legible (~45-75 car.) | ≥1 |
| 7 | Estados | Vacío, carga, error y sin-permiso resueltos, no solo el feliz | 2 |
| 8 | Pulido | Sombras en capas, radios anidados, alineación óptica, tipografía fina | ≥1 |

Puntaje: **suma / 16**. Regla de la casa: dimensiones 1, 4, 5 y 7 **deben** dar 2 para
aprobar (son bloqueantes); el resto suma para el veredicto pero un 0 ahí es un hallazgo.

## 2. Catálogo anti-slop (señales de UI genérica / hecha por IA)

Cada una es un hallazgo, no un detalle. Buscalas activamente:

- Todo al mismo peso: ninguna acción claramente primaria; tres botones idénticos.
- Espaciado arbitrario: 13px acá, 17px allá — no hay escala; `grep` de valores px sueltos.
- Card genérica repetida: mismo `border-radius` grande + sombra difusa única + gradiente violeta.
- Emojis como iconos, o iconos de otro set/grosor mezclados.
- Placeholder que quedó ("Lorem ipsum", "Card title", avatares de stock idénticos).
- Centrado universal: todo centrado porque "así no hay que decidir alineación".
- Copy hueco: "Bienvenido a tu dashboard", "Gestioná todo en un solo lugar".
- Estados faltantes: solo existe la vista con datos perfectos.
- Contraste bajo "estético": gris claro sobre blanco que no pasa AA.
- Dark mode = colores invertidos, con sombras negras invisibles sobre fondo oscuro.
- Movimiento decorativo sin causa (todo hace fade-in al entrar).

## 3. Severidad de cada hallazgo

- **Bloqueante**: rompe uso o accesibilidad (contraste < AA, sin estado de error, foco
  perdido, acción primaria irreconocible). No se cierra la pantalla con uno abierto.
- **Mayor**: se nota y baja la percepción de calidad (grilla rota, densidad mala,
  inconsistencia con el sistema).
- **Menor / nit**: pulido (una sombra plana, un radio que no anida).

## 4. Cómo revisar (procedimiento)

1. Capturá la pantalla en móvil / tablet / desktop, tema claro y oscuro, en cada estado.
2. `grep` en el código del componente: valores hex y px literales (deberían ser tokens),
   `!important`, `role=`/`aria-` sospechosos, `onclick` en `div`.
3. Recorré la rúbrica dimensión por dimensión sobre las capturas reales.
4. Pasá el catálogo anti-slop.
5. Anotá cada hallazgo con dimensión, severidad, ubicación y el fix concreto.

## Evidencia / Definition of Done

Un veredicto sin esto es inválido:

```
VEREDICTO:  APROBADA | APROBADA CON NITS | RECHAZADA
Puntaje:    N/16  (bloqueantes 1,4,5,7 = 2/2/2/2)
Capturas:   <rutas: móvil/tablet/desktop × claro/oscuro × estados>
Hallazgos:  [severidad] dimensión — ubicación — fix
No cubierto: <lo que no se pudo ver (flujo sin datos de prueba, etc.)>
```

No se aprueba con un bloqueante abierto. Adjuntá las capturas, no las describas.

## Checklist

- [ ] Vi la pantalla real por viewport y tema, no solo el código.
- [ ] Rúbrica puntuada; dimensiones 1, 4, 5 y 7 en 2.
- [ ] Pasé el catálogo anti-slop entero.
- [ ] Cada hallazgo tiene severidad, ubicación y fix.
- [ ] Los estados (vacío/carga/error/sin-permiso) existen y los vi (`frontend-ux-states`).
- [ ] Veredicto con evidencia pegada (`visual-proof`).
