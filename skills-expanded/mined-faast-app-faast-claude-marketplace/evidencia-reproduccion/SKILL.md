---
name: evidencia-reproduccion
description: Como el QA de negocio de la Mesa de Servicios reproduce lo que reporta un cliente en el ambiente real con el Playwright MCP y lo graba TODO - traza navegable (DOM, red y consola por accion), video con acciones superpuestas y capitulos por paso, capturas resaltadas y anotadas por paso, snapshot de accesibilidad, sidecars de consola y red - para emitir un veredicto explicito (REPRODUCIDO consistente o intermitente, NO REPRODUCIDO, BLOQUEADO) con un informe en lenguaje de negocio que acompaña al documento BUG y al ticket, mas las capturas de "como funciona hoy" para proyectos y cotizaciones, la regla de no debuggear, la primera falla se reporta, y la entrega embebida de la evidencia al lead o al PO. Cargala al reproducir un reporte o capturar el estado actual de una pantalla.
---

# Evidencia de reproduccion — QA de negocio (Mesa de Servicios)

Un bug reportado por un cliente llega como relato ("a veces se duplican las operaciones"). La
Mesa lo convierte en un hecho verificado: lo reproduce en el ambiente real, graba cada paso y
emite un veredicto con evidencia que cualquiera (lead, PO, el propio cliente) puede ver sin
reconstruir nada. Asi el ticket que llega al equipo de desarrollo ya viene con la prueba, y
la Mesa deja de ser "el que repite lo que dijo el cliente".

Mismo rigor que el equipo QA del dev-team, con una diferencia de foco: aqui todo se expresa en
**lenguaje de negocio** y el objetivo es DOCUMENTAR y ENTREGAR, no validar criterios de una
historia. Si el plugin dev-team esta instalado, la skill `dev-team:visual-evidence` aplica
tambien; esta es su version para la Mesa.

## Regla cero
- **Ambiente valido y acordado**: se reproduce donde se acordo (produccion solo si el cliente y
  el lead lo autorizan y con cuentas de prueba; preferente ambiente de pruebas/QA). Se anota
  version/estado del ambiente si es conocible.
- **Cuentas de prueba**: nombres de variable de `.mesa/accesos.env` (gitignored); nunca el
  valor en el chat, el informe ni la evidencia.
- **No se debuggea**: no se lee codigo, no se busca causa, no se propone arreglo. Se reproduce,
  se documenta, se reporta.
- **A la primera falla, se reporta**: si no se puede llegar al punto del bug (no entra el login,
  el ambiente no responde, falta un dato), es BLOQUEADO con la evidencia de ese primer intento.
  Sin reintentos, sin atajos, sin tocar datos para "hacerlo andar".
- **Un intento por paso**, mas una segunda corrida completa solo si se reprodujo, para clasificar
  consistente (2/2) o intermitente (1/2).

## Las tres capas (siempre las tres)
1. **Traza navegable** — `browser_start_tracing` al inicio, **justo despues de encender el
   video**, y `browser_stop_tracing` al final (`.zip`). Es la herramienta de ANALISIS: por cada
   accion guarda el estado de la pantalla, las llamadas de red y los mensajes de consola. Se abre
   con `npx playwright show-trace`.
2. **Video analizable** — `browser_start_video` + `browser_video_show_actions` (los clics y lo
   que se escribe quedan superpuestos) + `browser_video_chapter` por paso + `browser_stop_video`.
   El video se mira completo; los capitulos lo hacen navegable, no se salta nada. Se graba a
   tamaño real con la secuencia de abajo.
3. **Capturas ancladas** — en cada paso, `browser_highlight` sobre lo relevante (y
   `browser_annotate` si hace falta explicar) antes de `browser_take_screenshot`; la captura del
   resultado va con la verificacion explicita (`browser_verify_text_visible`,
   `browser_verify_list_visible`, `browser_verify_value`…) que AFIRMA lo obtenido.

Complementos: `browser_snapshot` (estado de la pantalla en texto inspeccionable),
`browser_console_messages` → `NN-consola.txt`, `browser_network_requests` → `NN-red.txt`
(secretos y tokens redactados). Viewport declarado (1280x720; 375x812 si es movil).

## Video a tamaño real (regla dura, verificada)
Playwright usa UNA sola captura de pantalla por pagina para la traza y el video, y el tamaño lo
fija quien la enciende primero. La traza la enciende reducida a 800 px: si arranca antes que el
video, o si hubo cualquier traza antes en la misma sesion del navegador, el video sale con la
pantalla chica en una esquina, el resto gris y el texto borroso. Secuencia obligatoria:
1. **Navegador limpio**: si ya se uso traza o video en esta sesion, `browser_close` y volver a entrar.
2. `browser_resize` al viewport (1280x720; 375x812 si es movil).
3. `browser_start_video` con `size` **igual al viewport** (`{"width":1280,"height":720}`).
4. `browser_video_show_actions`, y recien entonces `browser_start_tracing`.
5. Los pasos con `browser_video_chapter`; sin cambiar el viewport a mitad de grabacion.
6. `browser_stop_tracing` y luego `browser_stop_video`. Un video por sesion de navegador
   (la segunda corrida va en otro navegador limpio).
7. Verificar y preparar la entrega:
   ```bash
   python3 <carpeta-de-esta-skill>/scripts/normalizar_video.py .mesa/solicitudes/{ID}/evidencia/reproduccion.webm
   ```
   `OK` deja `reproduccion.mp4` (se abre en QuickTime, Teams y GitHub; el `.webm` no se abre en
   QuickTime) y `reproduccion-portada.png`. `REPARADO` significa que la grabacion salio mal: el
   `.mp4` ocupa la pantalla completa pero sigue borroso, se anota en `INDEX.md` y, si es la prueba
   del bug, se regraba. El `.webm` original no se toca. Al ticket va la portada embebida con link
   al `.mp4`.

## Carpeta y nombres
```
.mesa/solicitudes/{ID}/evidencia/
├── 00-ANTES-datos-y-ambiente.md     que se va a hacer, con que cuenta (nombre de variable), que dato, que ambiente
├── 01-{accion}.png … NN-{accion}.png capturas numeradas por paso (fallas: NN-BLOQUEANTE-*.png)
├── reproduccion.trace.zip
├── reproduccion.webm                 original (no se toca)
├── reproduccion.mp4 · reproduccion-portada.png   para entregar (normalizar_video.py)
├── NN-consola.txt · NN-red.txt
├── INDEX.md                          2-4 lineas por archivo: que muestra y donde esta el punto clave
└── reproduccion.md                   el informe con el veredicto
```
El MCP escribe en `~/.faast-mcp/mesa-servicios/` (staging fuera de los repos); al cerrar se mueve a la carpeta de la
solicitud con su numeracion. Nada queda en temporales. Carpeta `evidencia/` en `.gitignore`.

## El informe (`reproduccion.md`) — en lenguaje de negocio
```markdown
# Reproduccion {ID} — {que ve mal el usuario, en una frase}
**Veredicto:** ✅ REPRODUCIDO (consistente 2/2) | ✅ REPRODUCIDO (intermitente 1/2) | ❌ NO REPRODUCIDO | ⛔ BLOQUEADO
**Ambiente:** {pruebas|produccion} · **Fecha/hora:** {ts} · **Perfil usado:** {rol} · **Viewport:** 1280x720

## Pasos exactos, como usuario
| # | Que hice | Que paso | Captura |
|---|---|---|---|
| 1 | Entre como analista y abri "Operaciones pendientes" | Listado con 20 operaciones | 01-listado.png |
| 2 | Presione "Siguiente" | Aparecen 5 operaciones que ya estaban en la pagina anterior | 02-repetidas.png |

**Esperado:** operaciones distintas en cada pagina · **Obtenido:** 5 repetidas
**Verificacion:** las 5 operaciones aparecen en ambas paginas → CONFIRMADO
**Consola/red:** 0 errores · 1 llamada con respuesta inesperada (ver 02-red.txt)
**Traza:** reproduccion.trace.zip · **Video:** reproduccion.webm (18 s, 2 capitulos)
**Impacto observado:** {que proceso se frena, a quien afecta, segun lo visto}
**Pendiente / lo que falta para reintentar:** {si NO REPRODUCIDO o BLOQUEADO}
```
Veredictos:
- **REPRODUCIDO** → el BUG se documenta y registra con esta evidencia; el ticket llega al
  equipo de desarrollo "con la prueba hecha".
- **NO REPRODUCIDO** → no se inventa el bug: se informa al cliente que se intento, con los pasos
  y lo que SI funciono, y se pide lo que falta (otro usuario, dato, hora, navegador). Se puede
  registrar como "No reproducible — requiere informacion", nunca como bug confirmado.
- **BLOQUEADO** → se reporta el bloqueo al lider de mesa (acceso, ambiente, dato) y se reintenta
  cuando se destrabe.

## "Como funciona hoy" (para PRY y CTZ)
Cuando un proyecto o cotizacion cambia una pantalla existente, el QA de negocio captura el
**estado actual** (3-6 capturas resaltadas con `INDEX.md`) para que el documento y la
propuesta muestren "hoy" junto a la maqueta de "mañana". Sin veredicto; solo contexto.

## Entrega de la evidencia (al lead o al PO)
- `INDEX.md` encabeza la carpeta y cuenta la historia en 10 lineas.
- Al ticket va **embebida**, nunca como link suelto: en GitHub, rama huerfana `evidence` del
  repo configurado (`config.json` → `evidencia.repo`), subida desde un worktree aparte, y cada
  captura `![](…/raw/evidence/…)` + link `blob` de respaldo; en Azure DevOps, attachment +
  `<img>` en el HTML del item. Misma convencion que el dev-team, para que el lead y el PO la
  encuentren donde siempre.
- En el documento BUG, la seccion "Evidencia" incluye el veredicto, la tabla de pasos y las
  capturas clave (3-6) con pie de foto; traza y video se referencian.
- Secretos, tokens y datos personales redactados en texto e imagenes antes de entregar.
- Siempre se cita ambiente, fecha y perfil: una evidencia sin eso no es concluyente.

## Checklist de una reproduccion bien hecha
- [ ] Ambiente acordado y cuentas de prueba por nombre de variable
- [ ] `00-ANTES` escrito antes de tocar nada
- [ ] Navegador limpio, video con `size` = viewport, traza DESPUES del video
- [ ] Traza + video con acciones y capitulos + capturas resaltadas con verificacion
- [ ] `normalizar_video.py` en OK (o REPARADO anotado / regrabado) → `.mp4` + portada
- [ ] Consola y red guardadas y correlacionadas
- [ ] Segunda corrida si se reprodujo (consistente/intermitente)
- [ ] `INDEX.md` + `reproduccion.md` con veredicto explicito, en lenguaje de negocio
- [ ] Entregada embebida, redactada, con ambiente/fecha/perfil
