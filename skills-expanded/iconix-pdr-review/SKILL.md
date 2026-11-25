---
name: iconix-pdr-review
description: >
  revisa y emite veredicto sobre la coherencia del conjunto de artefactos de analisis antes del diseno detallado: la revision preliminar del diseno (PDR, preliminary design review) del proceso ICONIX. usar para: PDR, revision preliminar del diseno, revision de diseno, compuerta entre analisis y diseno detallado, prueba del marcador (highlighter test), entidades de robustez ausentes del modelo de dominio, trazabilidad del flujo de datos pantalla-atributo, cursos alternos sin comportamiento, completitud del dialogo usuario/sistema, deteccion de design-pattern-itis y de robustez disfrazada de secuencia, acta de revision, hallazgos con responsable y fecha, metricas de calidad de la revision. consume modelo de dominio, casos de uso, especificacion textual y diagramas de robustez, y decide si el paquete pasa al diseno detallado. no genera modelos: emite veredicto (aceptado / aceptado con verificacion de retrabajo / reinspeccion) y correcciones enrutadas a la skill que posee cada artefacto.
---

# ICONIX PDR Review

Trabajar en español por defecto, salvo que el usuario pida otro idioma. Fundamento y fuentes: `references/sources-and-methods.md`.

## Naturaleza y propósito

El PDR es **la compuerta entre el diseño preliminar y el diseño detallado**. La fuente lo define así: *"the 'gateway' between the preliminary design and detailed design stages, for each package of use cases."* Es el **Milestone 2 de los cuatro** del proceso (Requisitos → **PDR** → Diseño Detallado/Crítico → Entrega).

Tres consecuencias gobiernan todo lo demás:

- **No generas modelos: emites un veredicto sobre modelos ajenos.** Esta skill es la única del paquete que no produce un artefacto de diseño. Produce un **acta de revisión** con una decisión. Si te encuentras redibujando un diagrama en vez de juzgarlo, te has salido del papel.
- **Revisas el conjunto, no una pieza.** Cada skill hermana ya auditó lo suyo. Lo que nadie ha verificado —y lo que aquí se verifica— es que el modelo de dominio, el diagrama de casos de uso, la especificación textual y los diagramas de robustez **cuenten la misma historia**. Casi todos los defectos que encontrarás viven *entre* artefactos, no dentro de uno.
- **Es el último punto donde el cliente tiene entrada directa.** La fuente: *"this review is the last stage in the process where the customer has direct input."* Después, el diseño detallado es de los desarrolladores. Por eso el lenguaje del material revisado tiene que ser comprensible para quien no es técnico: no es cortesía, es un criterio de aceptación.

**Por qué existe la automatización.** Wiegers sitúa hasta el **75 %** de los defectos que una inspección encuentra en la fase de **preparación**, no en la reunión. Lo que hace esta skill *es* esa preparación: llega a la sesión con los defectos mecánicos ya cazados, para que el tiempo humano se gaste en juicio y no en cotejar listas.

## Insumos y trazabilidad de construcción

Esta skill es el **paso 5** del pipeline y la única que consume **todo lo anterior a la vez**:

```
modelo verbal → modelo de dominio ─┐
                casos de uso ──────┤
                especificación ────┼→ PDR (compuerta) → diseño detallado (DS-XX) · pruebas
                robustez (DR-XX) ──┘        │
                                            └── correcciones enrutadas hacia atrás
```

| Insumo | Nivel | Qué habilita | Si falta |
|---|---|---|---|
| **Diagrama(s) de robustez** `DR-XX` (.puml) | **Obligatorio** | El artefacto bajo revisión; uno por caso de uso | **Detente**: sin esto no hay nada que revisar |
| **Especificación textual** `CU-XX` (.md) | **Obligatorio** | Prueba del marcador (#10), cursos alternos (#7), diálogo (#6) | Guías #10, #7 y #6 **no ejecutables** → decláralas |
| **Modelo de dominio** (.puml) | **Obligatorio** | Cierre de entidades (#9), atributos y flujo de datos (#8) | Guías #9 y #8 **no ejecutables** → decláralas |
| **Diagrama de casos de uso** (.puml) | Recomendado | Cierre de actores; alcance real del paquete | Los actores no se verifican contra su fuente |
| **Modelo verbal** | Recomendado | Contexto y validación de alcance | Menor capacidad de juzgar "en contexto" |
| Wireframes o mockups | Opcional | #8 (campo de pantalla → atributo) y #3 (contexto de GUI) | La matriz de datos queda parcial |
| Documento de arquitectura o vista de capas | Opcional | **Activa la capa de arquitectura** | Capa **declarada no ejecutada** en el acta |
| Reglas de negocio `RN-XX` | Opcional | Juzgar con precisión los controladores de validación | — |
| Glosario | Opcional | Deriva de vocabulario con vocabulario autorizado | Solo heurística de similitud |

**Regla de los insumos ausentes.** Un insumo que falta **desactiva capas concretas**, y una capa que no se pudo ejecutar **se declara como no ejecutada en el acta**. Nunca la silencies: una capa declarada como no ejecutada es información útil; una capa omitida es una mentira por omisión. Y nunca compenses un insumo ausente inventando su contenido.

**Identificadores.** El acta lleva `PDR-XX`; cada hallazgo, `H-XX` dentro de ella. **No emitas `DS-XX`**: ese identificador pertenece al diagrama de secuencia, y el PDR es la compuerta que lo *autoriza*, no quien lo produce.

## Las diez guías del PDR

Es una **cuenta atrás**: la guía #1 es la más importante. Detalle, citas y localizadores en `references/pdr-guidelines.md`.

| # | Guía | Nivel | Mecanizable |
|---|---|---|---|
| 10 | **Prueba del marcador**: el texto del caso de uso y el diagrama se corresponden | Diagrama | Parcial — cobertura léxica, orientativa |
| 9 | **Toda entidad** de todo diagrama de robustez existe en el modelo de dominio | Sesión | **Sí, determinista** |
| 8 | **Flujo de datos trazable**: lo que se teclea en pantalla llega a atributos de entidad, y al revés | Sesión | **Sí** — cada fila debe resolver |
| 7 | **Cursos alternos con comportamiento**, no solo enumerados | Diagrama | **Sí** |
| 6 | **Ambos lados del diálogo** usuario/sistema | Diagrama | **Sí** — heurística de alternancia |
| 5 | **Sintaxis de robustez correcta** | Diagrama | **Sí** — las nueve reglas de conexión |
| 4 | Participan **técnicos y no técnicos** | Sesión | No — se verifica en el guion y el acta |
| 3 | Los casos de uso están **en contexto** del modelo de objetos y de la GUI | Sesión | Parcial — nombres genéricos, deriva |
| 2 | **No derivar hacia el diseño detallado** | Diagrama | **Sí** |
| 1 | **Los seis pasos**, por cada diagrama | Diagrama | Compuesta |

### Los seis pasos (guía #1), por cada diagrama de robustez

1. El diagrama **coincide con el texto** del caso de uso.
2. El diagrama **sigue las reglas** del análisis de robustez.
3. El diagrama **se centra en el flujo lógico** del caso de uso.
4. Se muestran **todos los cursos alternos**.
5. Cuidado con el **"design-pattern-itis"**.
6. El diagrama **no pretende ser un diseño detallado**.

### Tres guías que conviene entender, no solo aplicar

- **#9 no es burocracia de trazabilidad.** Descubrir objetos es un propósito central del análisis de robustez; una entidad que aparece en robustez y no en el dominio significa que el descubrimiento ocurrió y **nadie lo devolvió al modelo**. Ese desfase se paga en el diseño detallado.
- **#7 sostiene más de la mitad del trabajo.** La fuente cuantifica: los cursos alternos *"generally account for more than half the complexity of a piece of software"*. Y enumerar no basta — *"Identifying that an alternate course can happen is necessary, but not sufficient"*. Un alterno sin comportamiento especificado es una clase que nacerá sin las operaciones que lo manejan.
- **#4 y #3 son la misma exigencia vista desde dos lados.** Después del PDR los casos de uso son *"mini-contracts between the clients and the programmers"*, y para eso deben alcanzar el **nivel de abstracción justo**: *"not vague and ambiguous, but not geek-speak"*. Se consigue nombrando de forma unívoca las pantallas y las clases del dominio. Si el material solo lo entienden los programadores, el contrato no existe.

## Procedimiento de revisión

1. **Inventaría los insumos** y declara cuáles faltan y qué capas desactivan.
2. **Calcula el presupuesto de la sesión.** IEEE 1028 §6.5.2 fija para *diseño preliminar* un ritmo de **3-4 páginas/hora**; Wiegers converge en 2-4. Si el paquete no cabe en una sesión razonable, **dilo y propón partirlo**: revisar por encima del ritmo sostenible destruye la eficacia de la revisión, que es justo lo que la técnica venía a aportar.
3. **Corre el validador** (`scripts/validate_pdr.py`). Es la fase de preparación: automatiza lo mecánico.
4. **Recorre las diez guías** en orden de cuenta atrás, aplicando los seis pasos a cada diagrama. Para las guías no mecanizables, juzga con la lista de `references/pdr-guidelines.md` a la vista.
5. **Registra cada hallazgo** como `H-XX` con severidad, guía violada, ubicación y corrección propuesta.
6. **Calcula las cinco métricas** y **emite el veredicto**.
7. **Ejecuta el ciclo de auditoría interna** sobre el acta antes de entregarla.
8. **Ofrece las correcciones** enrutadas a la skill que posee cada artefacto, y aplica solo lo confirmado.

## Veredicto y criterios de salida

El veredicto sigue el modelo de decisión de salida de **IEEE 1028 §6.5.6.5** — tres estados, no dos:

| Veredicto | Condición |
|---|---|
| **Aceptado** | Cero entidades sin dominio · cero alternos sin comportamiento · cero violaciones de sintaxis · cobertura del marcador completa · cero hallazgos críticos y cero mayores |
| **Aceptado con verificación de retrabajo** | Solo hallazgos menores o moderados, **todos** con corrección acordada, responsable y fecha |
| **Reinspección requerida** | Cualquier hallazgo crítico o mayor abierto, o cobertura por debajo del umbral declarado |

La meta cuantitativa del método es explícita: **cero entidades sin dominio y cero alternos sin comportamiento**. No es una aspiración, es el criterio de aceptación.

**El veredicto no se negocia por cansancio.** Si el paquete no pasa, el resultado es `Reinspección requerida` — nunca un `Aceptado` degradado porque se agotó el tiempo o las pasadas. Wiegers añade un freno útil: no pidas a nadie revisar el mismo material **más de tres veces**; si a la tercera sigue sin pasar, el problema no es la revisión, es el artefacto o su alcance.

**Si el cliente pide requisitos nuevos durante la sesión**, no lo absorbas como un hallazgo más. Decláralo por lo que es: *"you're back to step 1 of the process (modifying use cases and the domain model, as needed)"*, y **solo para esos requisitos nuevos**. El resto del paquete sigue su curso.

## Las cinco métricas

Se calculan siempre y se publican en el acta. Detalle y umbrales en `references/pdr-metrics.md`.

| Métrica | Qué mide | Meta |
|---|---|---|
| **% cobertura del marcador** | Pasos del texto con correspondencia en el diagrama | Completa |
| **# entidades sin dominio** | Entidades de robustez ausentes del modelo de dominio | **0** |
| **# alternos sin comportamiento** | Cursos alternos enumerados pero sin conducta especificada | **0** |
| **# violaciones de sintaxis** | Enlaces prohibidos y demás reglas duras de robustez | **0** |
| **# revisiones necesarias** | Veces que el mismo caso de uso ha vuelto a revisión | ≤ 3 |

Las dos primeras métricas se calculan por sesión (paquete); las tres siguientes, por diagrama y agregadas.

**Sobre la cobertura del marcador.** El validador la aproxima por solape léxico entre los pasos del texto y las etiquetas y elementos del diagrama. Es **orientativa**: una cobertura del 100 % no prueba que el diagrama sea correcto, y una baja puede deberse a sinónimos legítimos. La prueba del marcador de verdad la haces tú, frase a frase. Reporta el número **acompañado de esa advertencia**, nunca como veredicto por sí solo.

## Hallazgos: cada uno es una tarea con dueño

El material de referencia es explícito en registrar cada hallazgo como tarea pendiente con responsable y fecha, e IEEE 1028 §6.8 hace **obligatoria** la clasificación de anomalías en una inspección. Cada `H-XX` lleva:

| Campo | Contenido |
|---|---|
| `H-XX` | Identificador dentro del acta |
| Guía | Cuál de las diez se viola (o qué anti-patrón) |
| Severidad | Crítico · Mayor · Moderado · Menor |
| Ubicación | Artefacto y punto exacto (línea, paso, elemento) |
| Descripción | Qué está mal y por qué importa |
| Corrección propuesta | Redactada en el formato que consume la skill destinataria |
| Destinatario | La skill que posee el artefacto |
| Responsable y fecha | Quién lo cierra y cuándo |
| Estado | Abierto · Acordado · Cerrado |

**Severidades.** Crítico: viola una regla dura o invalida el paquete para diseño detallado. Mayor: rompe la correspondencia entre artefactos o deja comportamiento sin especificar. Moderado: anti-patrón o exceso de detalle. Menor: nombres y legibilidad. El mapeo a las categorías de IEEE 1028 §6.8 está en `references/review-protocol.md`.

**Enrutamiento de las correcciones:**

| Hallazgo | Va a |
|---|---|
| Entidad ausente, atributo faltante, clase mal nombrada | `/uml-domain-modeler` |
| Actor descuadrado, caso de uso fuera del paquete | `/uml-use-case-diagram` |
| Alterno sin comportamiento, diálogo incompleto, texto ambiguo | `/use-case-specifier` |
| Violación de sintaxis, design-pattern-itis, robustez-como-secuencia | `/uml-robustness-diagram` |

**No reescribas los artefactos por tu cuenta.** Redacta la corrección, agrúpalas por destinatario, **pregunta cuáles aplicar** —ofreciendo explícitamente la opción de aplicarlas todas— y aplica solo lo confirmado, dejando constancia en el acta. Una compuerta que arregla en silencio lo que juzga deja de ser una compuerta.

## Ciclo de auditoría interna

**No entregues el acta sin haberla auditado.** Ojo con la confusión fácil: el **veredicto** juzga los artefactos del usuario; este **ciclo** juzga la calidad del acta que tú produces. Son dos cosas distintas y en el entregable aparecen por separado.

**Ciclo:** redactar → auditar → corregir → comprobar convergencia. Se cierra cuando se cumplen **a la vez**:

- cero hallazgos **críticos** y cero **mayores** en el acta misma;
- como máximo **dos menores**, documentados y justificados;
- **cada** hallazgo `H-XX` con severidad, ubicación verificable, corrección y destinatario;
- **cada** capa declarada ejecutada o no ejecutada, sin huecos;
- **dos pasadas consecutivas sin hallazgos nuevos** — una pasada limpia puede ser suerte, dos no.

**Tope duro: cinco pasadas.** Si al alcanzarlo persisten hallazgos críticos o mayores **en el acta**, no declares éxito: entrega el mejor resultado disponible, marca el estado como **`AUDITORÍA NO SUPERADA`**, enumera lo que queda abierto y di qué insumo o decisión haría falta para cerrarlo. Un fracaso declarado es más útil que un certificado optimista: sobre el primero se puede actuar.

Qué se audita del acta: que ningún hallazgo carezca de ubicación comprobable; que ninguna métrica se publique sin su método de cálculo; que ninguna capa quede sin declarar; que el veredicto se siga de los umbrales y no del optimismo; y que ninguna corrección propuesta invente contenido que los insumos no respaldan.

## Modos de trabajo

- **Revisar** (por defecto) — ejecutar el PDR completo sobre el paquete y emitir acta, veredicto, hallazgos y métricas.
- **Revisar un caso de uso** — el mismo procedimiento acotado a un `CU-XX` y su `DR-XX`. La unidad de trabajo es el caso de uso; la sesión es el paquete.
- **Validar** — correr solo `scripts/validate_pdr.py` e interpretar sus hallazgos con criterio, sin acta formal.
- **Reinspeccionar** — segunda vuelta sobre un paquete ya revisado: comprobar que los hallazgos cerrados lo están de verdad, y contar la revisión en la métrica de "# revisiones necesarias".
- **Preparar la sesión** — generar el guion: agenda, roles, orden de presentación y presupuesto de tiempo, sin ejecutar la revisión.
- **Autorizar el paso** — a partir de un veredicto `Aceptado`, emitir los insumos que consumirá el diseño detallado.

## Entregables

1. **Acta de revisión** `PDR-XX`, con el contenido que IEEE 1028 §6.7 exige a la salida de una inspección.
2. **Veredicto** en uno de los tres estados de §6.5.6.5, con la condición que lo justifica.
3. **Tablero de hallazgos** `H-XX`, cada uno con responsable y fecha.
4. **Cuadro de métricas** — las cinco, con su método de cálculo y sus umbrales.
5. **Matriz de trazabilidad de datos** — Pantalla | Campo | `Entidad::atributo`, con las filas que no resuelven marcadas.
6. **Delta consolidado al modelo de dominio** — reconcilia lo que el análisis de robustez descubrió y nadie devolvió.
7. **Correcciones propuestas**, agrupadas por skill destinataria, a la espera de tu confirmación.
8. **Certificado de auditoría interna** del acta, con su estado final.
9. **Guion de sesión** (si se pide) — agenda, roles y presupuesto de tiempo.

## Formato del acta

```markdown
# Acta de Revisión Preliminar del Diseño — PDR-01

**Paquete revisado:** [nombre] · **Casos de uso:** CU-03, CU-05
**Fecha:** [AAAA-MM-DD] · **Modalidad:** [formal | informal]
**Participantes:** [rol — nombre] …
**Insumos recibidos:** [lista] · **Insumos ausentes:** [lista, con capas desactivadas]

## Veredicto
**[Aceptado | Aceptado con verificación de retrabajo | Reinspección requerida]**
Motivo: [la condición concreta que lo determina]

## Métricas
| Métrica | Valor | Meta | ¿Cumple? |
…

## Cobertura de las diez guías
| # | Guía | Estado | Nota |
| 9 | Entidades en el dominio | Ejecutada — 2 hallazgos | … |
| 3 | Contexto de objetos y GUI | **No ejecutada** — sin wireframes | … |
…

## Hallazgos
| ID | Guía | Sev. | Ubicación | Descripción | Corrección | Destinatario | Responsable | Fecha |
…

## Matriz de trazabilidad de datos
| Pantalla | Campo | Entidad::atributo | ¿Resuelve? |
…

## Delta al modelo de dominio
…

## Certificado de auditoría interna del acta
Pasadas: N · Estado: [Convergido | Convergido con excepciones | AUDITORÍA NO SUPERADA]
```

## Qué el PDR no es

- **No es diseño detallado.** No asignes comportamiento a clases, no propongas métodos, no elijas patrones. La fuente lo llama las **dos pasadas**: en la primera *"you intentionally ignore 'who's doing what'"*; la asignación de comportamiento llega con los diagramas de secuencia.
- **No es una segunda ronda de análisis de robustez.** Si acabas redibujando, enruta el hallazgo a `/uml-robustness-diagram` en vez de hacerlo tú.
- **No es un trámite.** Un veredicto `Aceptado` emitido sin haber corrido las comprobaciones vale menos que ninguno, porque autoriza el paso al diseño detallado con una garantía falsa.
- **No revisa la arquitectura si no le das la arquitectura.** La capa existe y es opcional: con un documento de arquitectura o vista de capas, comprueba que los controladores encajen en las capas, las entidades se mapeen a persistencia y los objetos tipo Borde sean realizables con la tecnología de UI. Sin él, **declárala no ejecutada**. Y en cualquier caso, la arquitectura **se revisa aquí, no se diseña aquí**.

## Trazabilidad hacia adelante

Un veredicto `Aceptado` autoriza el diseño detallado. Lo que se lleva consigo:

- Los **objetos tipo Borde y Entidad** → instancias en el diagrama de secuencia (`DS-XX`, que emite la etapa siguiente, no esta).
- Los **Controladores** → mensajes de secuencia y, más tarde, métodos.
- **Cada Controlador** → al menos un caso de prueba.
- El **delta al modelo de dominio**, ya reconciliado, de modo que el diseño detallado arranque sobre un modelo completo.

Cadena completa de identificadores del pipeline: `RF-XX` → `CU-XX` → paso del flujo (`FA-XX`/`FE-XX`) → `DR-XX` + elemento (`B-`/`C-`/`E-`) → **`PDR-XX`** → mensaje de secuencia (`DS-XX`) → caso de prueba.

## Recursos

- `references/pdr-guidelines.md` — las diez guías y los seis pasos, con cita textual y localizador.
- `references/review-protocol.md` — cómo se conduce la revisión: anatomía IEEE 1028, roles, criterios de entrada y salida, ritmo, tamaño del equipo y etapas de Wiegers.
- `references/pdr-metrics.md` — las cinco métricas, su cálculo, sus umbrales y sus límites.
- `references/cross-artifact-checks.md` — cada comprobación del validador, la guía que la funda y lo que **no** puede detectar.
- `references/anti-patterns.md` — catálogo de defectos con síntoma, por qué importa y corrección.
- `references/sources-and-methods.md` — libros y normas, qué se tomó de cada uno, qué se descartó y qué no se pudo verificar.
- `references/regression-examples.md` — expectativas por dominio para comprobar que la skill generaliza.
- `scripts/validate_pdr.py` — la fase de preparación automatizada.
- `tests/examples/` — conjuntos de artefactos, coherentes e incoherentes a propósito, para ejercitar el validador.
