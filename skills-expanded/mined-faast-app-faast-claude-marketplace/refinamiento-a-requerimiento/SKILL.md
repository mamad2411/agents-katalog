---
name: refinamiento-a-requerimiento
description: Mesa de Servicios de FaaST en Claude - recibe TODO lo que llega de un cliente (ticket, correo, transcripcion de reunion, documento, relato) y lo deja cerrado y documentado. Clasifica la salida - BUG (error, formato de bugs del equipo), PRY (requerimiento o proyecto, propuesta y especificacion), CTZ (cotizacion, propuesta comercial que espera aprobacion) o CC (control de cambio sobre algo ya aprobado) - asigna correlativo TIPO-ANO-NNN y alcance (cliente o transversal), reune contexto del negocio (faast-brain, fichas, AS-IS), delimita alcance e impactos, pregunta solo lo necesario en rondas cortas con opciones, ofrece maqueta tipo boceto cuando hay pantallas, y emite los documentos estandarizados (Markdown, Word o PDF) y el issue para el backlog de GitHub. Usar SIEMPRE que el usuario traiga un ticket, correo, reunion, requerimiento, bug, cotizacion o cambio de alcance y pida refinarlo, documentarlo, cotizarlo, pasarlo a desarrollo, armar la propuesta o retomar un refinamiento en curso.
---

# Refinamiento → Requerimiento listo (Mesa de Servicios en Claude)

## Qué resuelve

1. **Que desarrollo desarrolle.** El requerimiento llega entendido, aprobado y documentado. Cada
   iteración posterior entre desarrollo y quien levantó el pedido es una falla del filtro.
2. **Que el alcance quede delimitado y aprobado.** Qué se construye y qué no, dónde aplica, qué
   impacta y qué no cambia. Lo aprobado es el contrato; lo que aparezca después es un **control de
   cambio**, no un defecto del desarrollo.
3. **Que lo opere quien levanta requerimientos**: la MDS (mesa de ayuda) e Implementaciones/Delivery,
   que conocen el sistema. Lo que no saben lo piden en **un solo pedido por destinatario** (desarrollo
   u otra área), sin frenar el refinamiento.

Una condición vale para el propio skill: no cambiar las iteraciones de "¿qué quiso decir el
cliente?" por iteraciones de "pásame el insumo A, ahora el B". Y una regla de oro: **nada se
inventa** — lo que el cliente no respondió queda como pendiente explícito, nunca como "lo razonable".

## Las cuatro salidas estandarizadas

Lo primero es decidir **qué tipo de salida** produce el ticket. Cada tipo tiene su correlativo, sus
documentos y su flujo (detalle y ejemplos en `references/tipos-y-correlativo.md`):

| Tipo | Es | Documentos | Flujo |
|---|---|---|---|
| **BUG** | El sistema no hace lo que ya debería (AS-IS, especificación o release) | `assets/plantilla-bug.md` (formato de bugs del equipo) | Completar campos obligatorios y evidencias; QA valida; no se refina como requerimiento |
| **PRY** | Requerimiento aprobado o interno: cambio menor, cambio funcional, reporte o funcionalidad nueva | Propuesta funcional (`plantilla-propuesta.md`) + Especificación (`plantilla-especificacion.md`); ficha única si es menor (`plantilla-cambio-menor.md`); `plantilla-proyecto.md` si es un proyecto grande | Fases 0 a 7 completas, proporcionales al tamaño |
| **CTZ** | Pedido que hay que **valorizar y aprobar comercialmente** antes de ser trabajo | Propuesta comercial (`plantilla-cotizacion.md`), con valorización en blanco para comercial | Se refina como un PRY, se emite la cotización y **espera aprobación comercial**; aprobada, pasa a PRY |
| **CC** | **Control de cambio**: el solicitante cambia algo ya aprobado o ya en desarrollo | `plantilla-control-cambio.md` | Se refina solo el delta, se mide el impacto (alcance, plazo, costo), nuevo visto bueno; en el tracker se actualiza o se crea issue nuevo que referencia al original |

**Correlativo y alcance (en todo documento y en el issue):** `TIPO-AÑO-NNN` — `BUG-2026-003`,
`PRY-2026-014`, `CTZ-2026-007`, `CC-2026-002` — y el **alcance**: `Cliente: ACME` (código del cliente),
`Clientes: A, B` o `Transversal` (para todos los que usan el producto). El número lo lleva el
**Registro de correlativos** del Proyecto de Claude (`assets/registro-correlativos.md`); si no está a
mano, se deja `TIPO-2026-___` para que lo complete quien lleva el registro. Un número nunca se reutiliza.
Ante la duda entre PRY y CTZ: si hay que cobrar o aprobar presupuesto, es CTZ. Un bug que ven todos es
transversal aunque lo reporte un cliente.

**Tamaño dentro de un PRY** (define cuánto refinamiento y qué documentos):

| Tamaño | Ejemplos | Documentos | Refinamiento típico |
|---|---|---|---|
| **Cambio menor** | Etiqueta, texto, mensaje, orden, valor por defecto | Ficha única que, aprobada, es el issue | 0-3 preguntas ("¿también en…?") |
| **Cambio funcional** | Fórmula, regla, validación, campo nuevo, ajuste de flujo | Propuesta + especificación cortas | Una o dos rondas |
| **Reporte** | Reporte nuevo, columnas, exportación | Propuesta + especificación con **Definición del reporte** | Una o dos rondas; la maqueta del cliente es el criterio |
| **Funcionalidad nueva / proyecto** | Módulo, producto, proceso o integración nuevos | Propuesta + especificación completas; `plantilla-proyecto.md` si tiene fases, hitos y equipo | Varias rondas; pedidos a otras áreas; maqueta |

Frontera: si el cambio agrega o modifica qué dato se muestra, calcula, guarda o valida, no es menor
aunque parezca chico. **Las secciones que no aplican se eliminan**, no se dejan vacías. Varios
requerimientos en un ticket se separan en varios issues (la propuesta puede agruparlos para un solo
visto bueno). Un error va por su carril (BUG).

## Los documentos: lenguaje, formato y entrega

- **Propuesta / cotización** (solicitante o cliente): el idioma del cliente, con los nombres de
  pantallas y menús que conoce y ejemplos de su operación. Sin términos técnicos ni IDs internos.
- **Especificación / ficha** (issue de backlog): lenguaje funcional y preciso — reglas con valores,
  dónde aplica e impactos enumerados, pantallas y mensajes exactos, criterios verificables. Sin diseño
  técnico (eso lo produce desarrollo). Aplica `references/redaccion.md`.
- **Entrega**: el documento se escribe en Markdown (fuente de verdad). Cuando va al cliente (propuesta,
  cotización, control de cambio) o el usuario lo pide, genera además el **Word** con la skill `docx` y,
  si se pide, el **PDF**; conserva acentos y eñes. Nombres: `{Correlativo} - {Tema} - v{N}.docx`.
- **Maqueta tipo boceto**: cuando el PRY cambia o crea pantallas, en un proyecto nuevo o en una
  cotización, ofrece una maqueta navegable como artefacto HTML a partir de `assets/maqueta-base.html`
  (3-6 pantallas clave, gris, placeholders, datos ficticios en el idioma del cliente). Es para que el
  cliente VEA la idea, no diseño final; sus pantallas van a la propuesta o cotización. Nunca para bugs.

**Ningún issue sin visto bueno, y nada fuera de lo aprobado.** Lo da quien tiene autoridad sobre el
alcance (no siempre quien pidió); si no está claro, se pregunta en la ronda 1. La especificación
registra quién aprobó, cuándo, por qué medio y sobre qué versión de la propuesta. Solo puede agregar
precisión, no alcance: si aparece algo nuevo, vuelve a la propuesta y requiere un nuevo visto bueno.

**El skill aprende.** Lo confirmado en cada caso y las preguntas que desarrollo hace después se guardan
en la **ficha de contexto por módulo** y en los **aprendizajes generales**; si el Proyecto de Claude
tiene el conocimiento del negocio de FaaST (**faast-brain**: productos, clientes, procesos, reglas,
glosario), se lee ANTES de preguntar y se propone alimentarlo al cerrar. Ver `references/contexto-del-sistema.md`.

## Test de salida: listo para desarrollo

El ticket se cierra cuando desarrollo puede construir sin volver a preguntar. Aplica según el tamaño
(un cambio menor solo necesita 2, 3, 4, 9 y 12; un reporte reemplaza 3 y 8 por la definición del reporte):

1. **Problema y para quién.** 2. **Alcance delimitado** (incluye / no incluye; producto, país, moneda,
cliente o tenant; estrategia: modifica, convive o extiende). 3. **Qué cambia exactamente** (dónde, hoy,
después, ejemplo numérico). 4. **Dónde aplica** (todos los lugares, con la decisión de cuáles cambian).
5. **Impactos** enumerados y concretos. 6. **Reglas** con valores y **casos de borde** decididos.
7. **Quién puede hacer qué.** 8. **Qué ve y hace el usuario** (pantallas, mensajes exactos).
9. **Cómo se verifica** (criterios con valores). 10. **Cómo se activa** y qué configura el cliente.
11. **Qué se mantiene.** 12. **Visto bueno** de quien tiene autoridad. 13. **Urgencia** y por qué.

Cada vacío es una pregunta: al usuario si es sobre el sistema, al solicitante si es de negocio, a otra
área o a desarrollo solo si el usuario no lo sabe. Las decisiones técnicas no se preguntan: van a
"Para resolver por desarrollo".

## Flujo de trabajo

### Fase 0 — Clasificación y contexto

**Clasificar el ticket.** Lo primero es identificar si es un error:

| Entra | Señales | Qué hace el skill |
|---|---|---|
| **BUG** | No hace lo que ya debería según AS-IS, especificación o release | `assets/plantilla-bug.md` + `references/formato-bug.md`: arma el reporte, pide lo que falta de los campos obligatorios y las evidencias; no lo refina como requerimiento |
| **PRY** | Pide algo que el sistema no hace, o que haga algo distinto | Flujo completo; define el tamaño |
| **CTZ** | Lo pedido hay que valorizarlo y aprobarlo comercialmente | Flujo de PRY + cotización; espera aprobación comercial |
| **CC** | Cambia algo ya aprobado o en desarrollo | Refina el delta y mide impacto; nuevo visto bueno |
| Consulta de uso / configuración | Ya existe, o se resuelve parametrizando | Lo indica y ofrece la respuesta al cliente |
| Mixto | Combinación | Separa las partes; cada una por su carril |

Asigna (o reserva) el **correlativo** y define el **alcance** (cliente/transversal). Si el ticket trae
varios pedidos de naturaleza distinta, sepáralos.

**Contexto del sistema y del negocio** (detalle en `references/contexto-del-sistema.md`):

1. Identifica módulos, producto, país y cliente.
2. Busca los insumos, en este orden: **faast-brain** del Proyecto (si existe) y la ficha de contexto
   del módulo; aprendizajes generales; adjuntos y archivos del Proyecto; conversaciones previas;
   conectores en modo lectura. Insumos: AS-IS, especificaciones previas, release notes, tickets,
   solicitudes parecidas, defectos conocidos, manuales.
3. Úsalos antes de preguntar: **lo que ya existe** (avísalo: puede no requerir desarrollo), **choques**
   con lo actual o con decisiones previas, y **decisiones reutilizables** (propuestas por defecto).
4. Si falta contexto, pregunta **primero a quien usa el skill** con hipótesis cerradas; lo que confirme
   es evidencia `[U]`. Lo que no sabe va en **un solo pedido por destinatario**, sin detener el trabajo.

### Fase 1 — Lectura del insumo

1. Identifica ticket, solicitante, cliente, productos, países, participantes y correlativo.
2. Extrae necesidad, actores, flujo, reglas, datos, impactos, decisiones, contradicciones y temas
   abiertos, con evidencia: `[T mm:ss – Hablante]` (transcripción), `[R §x]` (documento del
   solicitante), `[A §x]` (AS-IS), `[C documento §x]` (otro insumo), `[U]` (usuario).
3. Distingue lo decidido, lo opinado y lo descartado. Separa el problema del "cómo" del solicitante.
4. **Encuadre: ¿modificar lo existente, opción nueva que convive, o extender?** Cambia todo lo demás.
   "No se deben perder las funcionalidades actuales / solo agregar" apunta a opción nueva; "cambiar /
   corregir / en vez de" apunta a modificar. Si no es evidente, es la **pregunta de encuadre** y va
   antes que todo, con tu propuesta.
5. **Casuística** (cálculo, pantalla, reporte, archivo, parámetro, flujo, funcionalidad nueva): define
   qué debe quedar resuelto. Ver `references/casuisticas.md`.
6. **Inventario de dónde aplica**: todos los lugares donde vive lo que cambia → pregunta cerrada con la
   lista. Ver `references/impactos.md`.
7. **Interpreta los adjuntos** (es trabajo de quien levanta el requerimiento): con un Excel, corre
   `scripts/extraer_formulas.py` y confirma la candidata con pregunta cerrada; si el adjunto calcula el
   resultado esperado, sus valores son criterios de aceptación; si falta la captura de la pantalla, pídela.
8. Contrasta con el test de salida, las preguntas aprendidas, `references/impactos.md`,
   `references/checklist-completitud.md` y `references/casos-de-borde.md`.
9. Muestra una **lectura breve** (qué entendiste, decisiones con evidencia, contradicciones, lo que ya
   existe, temas sin cerrar) y, en el mismo mensaje, las preguntas de contexto al usuario, la **ronda 1**
   y el borrador de pedidos a otras áreas. Excepción: si hay preguntas de encuadre, la primera ronda es
   solo de encuadre.

### Fase 2 — Ciclo de preguntas hasta cerrar

Detalle en `references/preguntas.md`.

- **Solo las necesarias**: las que desarrollo tendría que hacer si no se hicieran ahora. No preguntes
  lo que el insumo, el brain o la ficha ya responden, ni decisiones técnicas.
- **Cerradas y con propuesta**: IDs estables `PR-xx`, cada una con su propuesta por defecto y por qué
  importa, con opciones A/B/C/otra para responder por dictado ("PR3 sí, PR5 la B").
- **Con destinatario**: usuario (sistema actual) → solicitante (negocio) → otra área → desarrollo (solo
  lo que nadie más sabe y cambia el alcance). Agrupa por destinatario.
- **Encuadre primero y solo** (1-3 preguntas); luego alcance, dónde aplica e impactos; reglas; bordes;
  detalle. **Máximo 7 por ronda, tope 3 rondas**: si no cierra, propone reunión de trabajo o decisión
  de alcance en vez de una cuarta ronda.
- Cada respuesta pasa a decisión `D-xx`. Cierra cada ronda con "Cerradas: N · Abiertas: M (K bloqueantes)".
- "Decide tú" → decisión delegada. "Lo define otro" → `Pendiente externo` con el mensaje redactado.
  "Fuera de alcance" → al alcance.
- **Pausar y retomar**: si quedan preguntas esperando a terceros, entrega el borrador en
  `En refinamiento` con lo resuelto, las decisiones y las abiertas con destinatario; para retomar, el
  usuario trae el borrador y las respuestas y sigues donde quedó. La persona de mesa habla con el
  cliente; el skill prepara y registra.

### Fase 3 — Validación previa

Antes de escribir, presenta lo que **tuviste que decidir tú** (bordes no preguntados, supuestos,
interpretaciones), con recomendación y alternativa. Lo confirmado pasa a `D-xx`. Se omite en un cambio
menor sin nada que decidir.

### Fase 4 — Documento para el solicitante (propuesta, cotización o control de cambio)

- **PRY**: propuesta funcional con `assets/plantilla-propuesta.md` (cambio menor: ficha única con
  `assets/plantilla-cambio-menor.md`, que aprobada es el issue). Debe cubrir: lo que entendimos, qué
  cambia exactamente con captura o maqueta y ejemplo, dónde se verá y dónde no, otros efectos, lo que
  queda fuera, lo que necesitamos del cliente, cómo sigue.
- **CTZ**: cotización con `assets/plantilla-cotizacion.md`: contexto, alcance (incluye / no incluye),
  solución propuesta con la maqueta, entregables, supuestos, exclusiones, plan y plazos estimados,
  **valorización en blanco para comercial** (el skill no pone precios ni esfuerzos), condiciones,
  vigencia y próximos pasos.
- **CC**: `assets/plantilla-control-cambio.md`: referencia al PRY/CTZ original, qué estaba aprobado,
  qué cambia y por qué, impacto en alcance, plazo, costo y otros clientes, decisión requerida.
- Lenguaje del cliente, solo valores que él entregó o confirmó, ningún dato de otro cliente, y
  explícito que lo aprobado es el contrato. Ofrece el Word/PDF y redactar el correo de envío.

### Fase 5 — Visto bueno (y aprobación comercial en CTZ)

- **Aprobada**: registra quién, cuándo, medio y versión. En CTZ, además la **aprobación comercial**
  (quién, cuándo, versión de la cotización); recién ahí pasa a PRY y al backlog como trabajo.
- **Con observaciones**: redacción → corrige; cambio de regla o alcance → nueva `D-xx`; contradice una
  decisión → muestra ambas y pregunta; tema nuevo → Fase 2. Sube la versión y reenvía.
- **Rechazada / descartada**: vuelve a la Fase 1 con el motivo, o cierra como descartada (lo aprendido
  se guarda igual).

### Fase 6 — Especificación (issue de backlog)

Solo con visto bueno registrado (y aprobación comercial si fue CTZ).

1. Escribe la especificación con `assets/plantilla-especificacion.md`, solo con las secciones de su
   tamaño: alcance en una mirada; qué cambia exactamente; reglas `RN-xx`; dónde aplica e impactos
   `IM-xx`; pantallas y mensajes; casos de borde; criterios `CA-xx` que cubren cada regla y cada lugar
   que cambia; activación; fuera de alcance; "Para resolver por desarrollo" (`PT-xx`); decisiones.
   Un proyecto grande lleva además `assets/plantilla-proyecto.md` (fases, hitos, equipo, riesgos).
2. **Prueba de coherencia**: cada regla, lugar, impacto y pantalla está en lo aprobado o es precisión
   de algo que sí está.
3. Calcula los ejemplos numéricos con código y corre `scripts/validar_requerimiento.py` hasta que no
   haya errores. Estado `Listo para desarrollo`; el ticket se cierra.
4. Entrega los documentos (capturas marcadas con `scripts/anotar_captura.py` en `img/`, maqueta si la
   hubo) y cierra con: reglas, criterios y lugares; riesgos; **cuántas consultas fueron a desarrollo u
   otras áreas y por qué** (indicador del objetivo 1).
5. **Issue en GitHub** (`references/github.md`): proyecto #38 de faast-app, cuerpo = especificación
   completa (o ficha), título `[Módulo] Verbo + qué — Cliente`, campos del proyecto y **etiquetas**:
   `tipo:`, `cliente:` o `alcance:transversal`, `producto:`, `prioridad:`, `origen:`, `mesa:{correlativo}`.
   Una CTZ aprobada entra como trabajo; sin aprobación queda `cotizacion:pendiente-aprobacion`. Si la
   sesión tiene conector a GitHub y el usuario confirma, créalo; si no, entrega el cuerpo y los comandos.
6. **Actualiza la ficha de contexto** (y propone el ingest a faast-brain) solo si se aprendió algo
   nuevo del sistema o del cliente, sin datos confidenciales.

### Fase 7 — Después de la entrega: consultas y controles de cambio

- **Consulta de desarrollo, QA u otro equipo**: resuélvela con el ciclo de la Fase 2, actualiza la
  especificación (y la propuesta si cambia algo aprobado), sube la versión y clasifica la causa
  (contexto faltante → ficha; pregunta no hecha → preguntas aprendidas; lugar no inventariado → ficha;
  ambigüedad → redacción; diseño técnico → era `PT-xx`; cambio del solicitante → CC).
- **Control de cambio (CC)**: cuando el solicitante cambia algo aprobado o en desarrollo, abre un
  `CC-AÑO-NNN` con `assets/plantilla-control-cambio.md`: se refina solo el delta, se mide el impacto,
  nuevas versiones de propuesta y especificación con nuevo visto bueno. En el tracker: si el issue no
  empezó, se actualiza; si ya está en desarrollo, issue nuevo que referencia al original. Así queda la
  trazabilidad de que no fue un error de desarrollo.

## Reglas de contenido

- **Alcance delimitado y aprobado**: incluye / no incluye, dónde aplica y dónde no, qué no cambia.
- **Todo cambio anclado**: dónde (captura marcada o maqueta), hoy y después completos, ejemplo numérico
  **calculado con código**.
- **Dónde aplica, completo**: una fila `IM-xx` por lugar con su decisión; "No cambia" también se escribe.
- **Impactos concretos**: una fila por impacto; en contabilidad una por asiento.
- **Sin referencias vagas** ("lo acordado", "donde corresponda"): se resuelve y se escribe su contenido.
- **Ningún adjunto sin interpretar.** "Ver Excel" no es un requerimiento.
- **Toda regla tiene origen** (evidencia o `D-xx`), es atómica y lleva valores.
- **Gobierno de FaaST**: lo nuevo se despliega desactivado por defecto, con valores por tenant.
  Excepción: cambio obligatorio por normativa (norma, referencia, vigencia, países, clientes; lo
  aprueba producto o cumplimiento).
- **País, producto, moneda y tenant explícitos.** **Confidencialidad entre clientes.** **Sin datos
  personales** de personas ni secretos en documentos, issues ni fichas.

## Errores a evitar

- Asumir modificar lo existente cuando se pidió una opción nueva, o al revés.
- Lanzar una ronda larga cuando la mitad depende de una pregunta de encuadre no hecha.
- Cambiar algo en un lugar sin preguntar en qué otros vive (el botón 2, el PDF, el reporte).
- Impactos genéricos, referencias vagas, adjuntos sin interpretar, preguntas abiertas que podían ser cerradas.
- Tomar una opinión como decisión, o preguntarle al cliente cómo funciona el sistema.
- Refinar como requerimiento un bug, una consulta o algo que ya existe; o documentar como bug un pedido nuevo.
- Tratar una etiqueta como un módulo, o un módulo como cambio menor.
- Emitir el issue sin visto bueno, como resumen, o con alcance fuera de lo aprobado; pasar una
  cotización a trabajo sin aprobación comercial; procesar un cambio de alcance sin control de cambio.
- Inventar lo que el cliente no respondió; poner precios o esfuerzos en una cotización.

## Validador

```bash
python scripts/validar_requerimiento.py --spec ESP_X_FaaST.md [--propuesta Propuesta_X_Cliente.md] [--matriz]
```
Bloquea el cierre por IDs inconsistentes, reglas sin origen, reglas o lugares sin criterio, secciones
faltantes, preguntas abiertas, `Listo para desarrollo` sin visto bueno, adjuntos sin interpretar,
referencias vagas, IDs internos en la propuesta y marcadores TBD. Avisa por términos vagos o técnicos
y diseño técnico colado. `--matriz` imprime la trazabilidad reglas → criterios.

## Archivos del skill

- `references/tipos-y-correlativo.md`: las cuatro salidas (BUG, PRY, CTZ, CC), correlativo, alcance, etiquetas.
- `references/contexto-del-sistema.md`: insumos, faast-brain, pedido consolidado, fichas y ciclo de aprendizaje.
- `references/casuisticas.md`, `references/impactos.md`, `references/preguntas.md`,
  `references/checklist-completitud.md`, `references/casos-de-borde.md`, `references/redaccion.md`.
- `references/formato-bug.md` y `references/github.md`.
- `assets/`: `plantilla-propuesta.md`, `plantilla-especificacion.md`, `plantilla-cambio-menor.md`,
  `plantilla-proyecto.md`, `plantilla-cotizacion.md`, `plantilla-control-cambio.md`, `plantilla-bug.md`,
  `maqueta-base.html`, `registro-correlativos.md`, `plantilla-ficha-contexto.md`,
  `plantilla-aprendizajes-generales.md`.
- `scripts/validar_requerimiento.py`, `scripts/extraer_formulas.py`, `scripts/anotar_captura.py`.
