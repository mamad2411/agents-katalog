---
name: iconix-cdr-review
description: >
  conduce la revision critica del diseno (CDR, critical design review) de ICONIX: la compuerta entre el diseno detallado y el codigo, el hito 3. usar para: CDR, revision critica del diseno, milestone 3, revisar el diseno antes de codificar, secuencia que no coincide con el texto del caso de uso, tecnica del resaltador, operaciones asignadas a la clase equivocada, clases sin responsabilidades o con personalidad multiple, clase envoltorio redundante, modelo de dominio anemico, trazar requisitos a casos de uso y clases, generar cabeceras de codigo, revisar el plan de pruebas del release, acta de revision tecnica con veredicto. consume secuencia, modelo de clases y especificaciones, y determina si el diseno pasa a implementacion. NO es el PDR, que audita el analisis: eso lo hace /iconix-pdr-review. nunca edita artefactos: presenta hallazgos con alternativas, decides tu, y enruta a la skill dueña de cada uno.
---

# ICONIX CDR Review

Trabajar en español por defecto, salvo que el usuario pida otro idioma. Fundamento y fuentes: `references/sources-and-methods.md`.

*Esta skill es autosuficiente: todas las citas que usa están transcritas en `references/`. No necesita acceso a ningún corpus, grafo ni norma externa para funcionar.*

## Naturaleza y propósito

El CDR es **la última parada antes del código**. Rosenberg lo sitúa así: *"There's just one last stop before code: the Critical Design Review (CDR)."*

Persigue tres objetivos, y todo lo demás son medios para ellos:

> *"The CDR helps you to achieve three important goals, before you begin coding: — Ensure that the "how" of detailed design matches up with the "what" specified in your requirements… — Review the quality of your design… — Check for continuity of messages."*

**Es una revisión técnica, no una inspección ni una revisión de gestión.** Lo dice la fuente del método —*"It's a technical review session"*— y lo confirma IEEE 1028, que lista *"Software design description"* entre los productos sujetos a revisión técnica. La consecuencia práctica: **el cliente no participa**. Validar contra lo que el cliente quiere fue trabajo del PDR; aquí se revisan patrones, clases, interfaces y responsabilidades.

**Quién decide.** IEEE 1028 §5.2.1 define el rol de *decision maker* como *"the person for whom the technical review is conducted"*, y le asigna determinar si los objetivos se cumplieron. **Ese es el usuario, no esta skill.** La skill conduce la revisión, registra y recomienda. Y §5.2 pone el límite que lo explica: *"no individual should act in all roles"* — si además decidiera, ocuparía los tres roles y esto dejaría de ser una revisión.

**Qué no es.** No es el PDR (`/iconix-pdr-review` audita el análisis, antes del diseño detallado). No genera ni modifica diagramas. No resincroniza el código con el diseño: eso es la revisión de código, posterior a esta compuerta.

## Insumos y trazabilidad de construcción

Esta skill es el **paso 8** del pipeline, y la compuerta que lo cierra:

```
modelo verbal → dominio → casos de uso → especificación → robustez → PDR
                                                                      ↓
                                          secuencia → modelo de clases → CDR → código
```

Cadena de identificadores: `RF-XX → CU-XX → FA-XX/FE-XX → DR-XX → PDR-XX → DS-XX → MC-XX → CP-XX → **CDR-XX**`

**Qué exige cada regla.** La tabla sale de mapear regla → artefacto, no de intuición:

| Insumo | Nivel | Reglas que habilita | Si falta |
|---|---|---|---|
| Diagramas de secuencia `DS-XX` (todos los del release) | **Obligatorio** | 10, 9, 8, 6 | **Detente**: es el criterio de entrada |
| Modelo de clases de diseño `MC-XX` | **Obligatorio** | 8, 7, 3, 2 | **Detente**: no hay diseño que juzgar |
| Especificaciones `CU-XX` | **Obligatorio** | 10, 9, 5 | Las reglas 10 y 9 quedan **no ejecutadas** → el veredicto **no puede pasar de** `No plenamente verificado` |
| Plan de pruebas / `CP-XX` | Recomendado | 1 | Regla #1 **no ejecutada** → declárala |
| Requisitos `RF-XX`/`RNF` o modelo verbal | Recomendado | 5 | Regla #5 **no ejecutada** → declárala |
| Modelo de dominio | Recomendado | 7 | Menor capacidad de juzgar anemia y deriva |
| Diagramas de robustez `DR-XX` | Recomendado | 6, 1, y el **recorrido** | Sin origen de los patrones, sin unidad para los casos de prueba, y sin checklist fino |
| Veredicto del PDR `PDR-XX` | Recomendado | Costura hacia atrás | **Advierte** si fue `Reinspección requerida` |
| Diagrama de casos de uso | Opcional | Alcance del release | El paquete no se verifica contra su alcance |
| Arquitectura · wireframes · glosario | Opcionales | Contexto | Capas declaradas no ejecutadas |

**Un insumo que falta desactiva reglas concretas, y una regla que no se pudo ejecutar se declara en el acta.** Nunca la silencies: una regla declarada como no ejecutada es información; una regla omitida es una mentira por omisión. IEEE 1028 §5.1 lo autoriza expresamente — *"The examination need not address all aspects of the product"* — pero autoriza no ejecutarla, no ocultarlo.

## Criterio de entrada: cuándo NO revisar

Antes de nada, comprueba esto. Si no se cumple, **no revises**: dilo, explica qué falta, y detente.

> *"You need to have completed all of the sequence diagrams for the use cases that you're planning to implement in the current release. You should also have updated the class diagrams so that all of the operations that you assigned during sequence diagramming are reflected in the static model. **Having to update the diagrams during the review would be too much of a distraction.**"*

IEEE 1028 §5.4.2 lo vuelve obligación: *"A technical review shall be conducted only when the required review inputs are available."*

Revisar material a medio terminar produce un acta que parece una revisión y no lo es — peor que no haberla hecho, porque genera confianza infundada.

## Las diez reglas

El núcleo. Desarrollo completo, con qué las satisface y qué las viola, en `references/cdr-rules.md`.

| # | Regla | Mecanizable |
|---|---|---|
| 10 | La secuencia coincide con el texto del caso de uso — **Técnica del Resaltador** | Parcial |
| 9 | Cursos básicos **y alternativos**, ambos | Sí |
| 8 | Operaciones asignadas a la clase correcta | Sí |
| 7 | Atributos y operaciones apropiados; cohesión | Parcial |
| 6 | El diseño real reflejado; **sin magia** | Parcial |
| 5 | Requisitos trazados a casos de uso y clases | Sí |
| 4 | Los programadores validan que es construible | **No** |
| 3 | Tipos, parámetros y retornos completos y precisos | Sí |
| 2 | Generar las cabeceras de código e inspeccionarlas | Genera sí; inspección no |
| 1 | Revisar el plan de pruebas del release | Parcial |

**Cómo se recorre el paquete.** No lo inventes: el método lo fija. El **recorrido grueso** son los títulos de los casos de uso; el **fino**, los controladores de los diagramas de robustez. Por eso la robustez es insumo aunque el CDR no la juzgue — se usa como índice.

**Las reglas #4 y #2 tienen una parte irreductiblemente humana.** La #4 entera: nadie sustituye a quien va a escribir el código diciendo si puede. La #2 en su inspección. Si no se cubren, se declaran no ejecutadas; fingirlas cubiertas sería el peor fallo de esta skill.

## Procedimiento: los tres actos

### Acto I · Revisar

1. **Comprueba el criterio de entrada.** Si falla, detente aquí.
2. **Calcula el presupuesto de sesión.** Tres ritmos según el material: diseño detallado 3-4 páginas/hora · plan de pruebas 5-7 · cabeceras 100. Si el paquete excede lo sostenible, **dilo y propón partirlo** — la norma autoriza varias sesiones, y la evidencia dice que revisar de más destruye la eficacia. Detalle y datos en `references/session-budget.md`.
3. **Ejecuta las diez reglas** siguiendo el recorrido. Cada hallazgo con **ubicación verificable** — un hallazgo que no se puede localizar no se puede comprobar, y es el error más grave posible aquí.
4. **Clasifica cada hallazgo** con las nueve categorías de anomalía de IEEE 1028 §6.8.2 (transcritas en `references/review-protocol.md`) y con la severidad del paquete. Presta atención a `Risk-prone`: es el estatus correcto de un anti-patrón, que no es un error demostrado.
5. **Declara toda regla o capa no ejecutada**, con su razón.
6. **Comprueba la propia revisión** contra la tasa base de 0,4 hallazgos/página. Si el paquete es grande y encontraste casi nada, lo más probable es que la revisión fallara, no que el diseño sea impecable. **Dilo.**

### Acto II · Deliberar

**No emitas veredicto todavía.** Emitirlo antes de esta conversación convertiría la deliberación en teatro.

Presenta los hallazgos **agrupados por destinatario** y ordenados por riesgo, y por cada grupo ofrece **las cuatro alternativas con una recomendación explícita y su razón**: corregir ahora · diferir con riesgo aceptado · reabrir el artefacto anterior · declarar falso positivo.

Esto no es cortesía: IEEE 1028 §5.1 atribuye a la revisión técnica *"the recommendation and examination of various alternatives"*, y §5.7 hace de las recomendaciones **contenido obligatorio del acta**.

**Pregunta aquí si generar las cabeceras de código** (regla #2). Siempre, sin deducir la respuesta del contexto.

Protocolo completo en `references/deliberation-protocol.md`.

### Acto III · Planificar la remediación

Con las decisiones del usuario:

1. **Construye la lista de puntos de acción**, cada uno con dueño y fecha, **destacando el riesgo** (§5.5.6: *"generate a list of action items, emphasizing risks"*).
2. **Enruta** cada punto a la skill que posee el artefacto.
3. **Registra el razonamiento y los supuestos** de cada decisión — es la salida (d) del proceso de gestión de decisiones de ISO 12207 §6.3.3, y lo que hace auditable la decisión meses después.
4. **Consigna el veredicto que el usuario determina**, en uno de los tres estados.

**No apliques ninguna corrección.** Ni las triviales. IEEE 1028 §5.5.6: *"assignment of action items is left to management follow-up"*. Una compuerta que arregla en silencio lo que juzga deja de ser una compuerta.

## Veredicto

Tres estados, vocabulario tomado de IEEE 1028 §6.5.6.5 —**préstamo declarado** de la cláusula de inspección, porque la de revisión técnica no ofrece escala propia—:

| Veredicto | Condición |
|---|---|
| **Aceptado** | Criterio de entrada cumplido · **todas** las reglas ejecutadas —incluidas la #4 y la inspección de la #2, que hace una persona— · cero críticos y cero mayores |
| **Aceptado con verificación de retrabajo** | Todas las reglas ejecutadas, y solo moderados o menores, **todos** con corrección acordada, responsable y fecha |
| **Reinspección requerida** | Cualquier crítico o mayor abierto |

**Y dos estados que no son disposiciones, sino la negativa a proponer una.** Existen porque proponer «Aceptado» sobre una revisión que no llegó a hacerse sería exactamente el fallo que esta compuerta previene:

| Estado | Cuándo | Qué significa |
|---|---|---|
| **No revisado — criterio de entrada incumplido** | Faltan secuencias del alcance, o alguna está vacía | La revisión **no se hizo**. No hay nada que disponer |
| **No plenamente verificado** | Alguna regla quedó **no ejecutada** por falta de insumos | La revisión se hizo **a medias**. Lo comprobado puede estar impecable y aun así no se sabe qué habrían encontrado las reglas que no corrieron |

**Por qué «Aceptado» exige todas las reglas ejecutadas.** Con solo el modelo de clases y una secuencia —lo mínimo que el validador acepta— quedan sin correr las reglas 1 y 5. Un veredicto favorable ahí afirmaría más de lo que se comprobó. Para llegar a `Aceptado` hay que aportar los insumos que faltan, o **declarar y aceptar por escrito** por qué esa regla no aplica a este release: la ausencia razonada sí permite el paso; la silenciosa, no.

**Y una precisión sobre lo que el validador puede proponer.** El script propone `ACEPTADO (sujeto a las dos reglas no mecanizables)`, nunca `Aceptado` a secas — porque la regla #4 y la inspección de las cabeceras de la #2 **no las cubre ninguna herramienta**. No degradan el veredicto, porque no son trabajo que se pudo hacer y no se hizo, sino trabajo que ninguna máquina puede hacer; pero tampoco pueden darse por satisfechas. **El `Aceptado` limpio solo existe cuando tú confirmas esas dos.**

**La skill propone; el usuario determina.** Y el veredicto no se negocia por cansancio: si el paquete no pasa, es `Reinspección requerida`, no un `Aceptado` degradado. Wiegers pone el freno complementario — no pidas a nadie revisar el mismo material más de **tres veces**; si a la tercera sigue sin pasar, el problema no es la revisión, es el artefacto o su alcance, y eso también es un hallazgo.

**Quien verifica el retrabajo no puede ser quien lo hizo** (§6.5.6.5: *"other than the author"*). Si las correcciones se aplican con las skills hermanas, la verificación vuelve aquí.

## Ciclo de auditoría interna

Antes de entregar el acta, audítala. **Ciclo:** redactar → auditar → corregir → comprobar convergencia.

Se cierra cuando se cumplen **a la vez**: cero hallazgos **críticos** y cero **mayores** en el acta misma; como máximo **dos menores**, documentados y justificados; **cada** hallazgo `H-XX` con severidad, categoría de anomalía, ubicación verificable, corrección y destinatario; **cada** regla declarada ejecutada o no ejecutada, sin huecos; y **dos pasadas consecutivas sin hallazgos nuevos** — una pasada limpia puede ser suerte, dos no.

**Tope duro: cinco pasadas.** Si al alcanzarlo persisten hallazgos críticos o mayores **en el acta**, no declares éxito: entrega el mejor resultado disponible, marca el estado como **`AUDITORÍA NO SUPERADA`**, enumera lo que queda abierto y di qué insumo o decisión haría falta para cerrarlo. Un fracaso declarado es más útil que un certificado optimista: sobre el primero se puede actuar.

## Modos de trabajo

- **Completo** — las diez reglas, con el ciclo de deliberación. Es el modo por defecto.
- **Ligero** — solo las reglas mecanizables, **declarando** las que se omiten. *Agile ICONIX* lo contempla: *"With a low-ceremony approach, the CDR might get skipped, or at least not be as rigorous."* Omitir sin declarar no es un modo ligero, es una revisión incompleta disfrazada.
- **Solo preparación** — ejecuta el validador y entrega los hallazgos mecánicos sin conducir la deliberación. Útil antes de convocar a la gente.
- **Solo presupuesto** — dimensiona el paquete y propone el reparto en sesiones, sin revisar.
- **Verificar retrabajo** — a partir de un `CDR-XX` previo con estado *Aceptado con verificación de retrabajo*, comprueba solo lo corregido.

## Entregables

1. **Acta `CDR-XX`** con el contenido que IEEE 1028 **§5.7** exige a una revisión técnica — incluidos los *management issues* y el estado de cada punto de acción con dueño y fecha.
2. **Determinación de las siete cuestiones de §5.5.6**, entre ellas la que define esta compuerta: si el producto está **listo para la siguiente actividad**.
3. **Veredicto** en uno de los tres estados, con la condición que lo justifica.
4. **Tablero de hallazgos `H-XX`** — categoría de anomalía, severidad, ubicación verificable, corrección, destinatario, responsable y fecha.
5. **Cobertura de las diez reglas** — cuál se ejecutó, cuál no y por qué.
6. **Matriz de trazabilidad** `RF-XX → CU-XX → DS-XX → MC-XX → CP-XX`, con huérfanos **en ambos sentidos**.
7. **Presupuesto y protocolo de sesión**, con el ritmo aplicado y su procedencia.
8. **Informe de decisiones** — alternativas, elección, razonamiento y supuestos.
9. **Plan de remediación enrutado**, como lista de puntos de acción con el riesgo destacado.
10. **Cabeceras de código**, *solo si el usuario lo autoriza*, marcadas como instrumento de revisión.
11. **Certificado de auditoría interna** con el criterio de parada.

Formato del acta y plantillas: `references/review-protocol.md`.

## Enrutamiento de correcciones

**No reescribas los artefactos.** Redacta la corrección, agrúpala por destinatario, presenta las alternativas, y deja que el usuario decida qué aplicar y con qué skill.

| Hallazgo | Va a |
|---|---|
| Operación sin procedencia, en la clase equivocada, firma incompleta, clase envoltorio, abstracción inestable sin declarar | `/uml-design-class-model` |
| Mensaje ausente, curso alterno sin fragmento, objeto sin mensajes, funcionalidad mágica, control centralizado | `/uml-sequence-diagram` |
| Texto que no casa con la secuencia, flujo sin especificar, requisito implícito sin documentar | `/use-case-specifier` |
| Entidad o atributo ausente del dominio | `/uml-domain-modeler` |
| Patrón sin origen en robustez, controlador sin caso de prueba | `/uml-robustness-diagram` |
| Caso de uso fuera del alcance del release | `/uml-use-case-diagram` |
| Insumo aprobado que ya no es vigente | `/iconix-pdr-review` |

## Verificación mecánica

```bash
python scripts/validate_cdr.py --clases modelo_clases_diseno.puml \
                               --secuencia caso_01_secuencia.puml \
                               [--spec caso_01_especificacion.md ...] \
                               [--robustez caso_01_robustez.puml ...] \
                               [--dominio modelo_dominio.puml] \
                               [--requisitos requisitos.md] \
                               [--pruebas plan_pruebas.md]
```

**Obligatorio para el script** son solo `--clases` y `--secuencia`; **obligatorio para un CDR completo** es además `--spec`, y de ahí la diferencia entre las dos columnas de la tabla de insumos. El script corre con menos para que puedas usarlo temprano; lo que no hace es fingir que la revisión fue completa. Cada insumo ausente **desactiva reglas concretas**, que se declaran en la salida y **topan el veredicto**.

Códigos: `0` sin errores · `1` hay errores, el diseño no pasa · `2` error de uso o archivo no encontrado.

El validador cubre la **preparación**, que es donde la evidencia dice que está el rendimiento — Wiegers: *"Up to 75 percent of the defects found by an inspection are discovered during preparation."* No sustituye la revisión: la prepara.

## Trazabilidad hacia adelante

Lo que sigue al `Aceptado` es **codificar**. El CDR autoriza esa flecha y nada más.

Mantener el modelo y el código sincronizados después es **otra actividad** —la revisión de código de la que habla *Agile ICONIX*—, y no es de esta skill. La diferencia se ve en las propias figuras del método: en el mapa del CDR la flecha del modelo al código va **en un sentido**; en el de la revisión de código es **bidireccional**.

## Recursos

- `references/cdr-rules.md` — las diez reglas verbatim y su desarrollo, con la Técnica del Resaltador y el algoritmo del recorrido.
- `references/review-protocol.md` — cómo se conduce: roles, entradas, precondiciones, las siete determinaciones, el acta y las escalas de anomalía y disposición.
- `references/session-budget.md` — la tabla de ritmos íntegra, los datos empíricos, el cálculo del presupuesto y la autocomprobación de la revisión.
- `references/deliberation-protocol.md` — el Acto II: alternativas, recomendación y registro de decisiones.
- `references/anti-patterns.md` — catálogo con síntoma, por qué importa, corrección y destinatario.
- `references/metrics-and-triage.md` — el triaje 5/20/80, las métricas CK, y qué umbrales **no** existen.
- `references/traceability-and-headers.md` — la matriz de trazabilidad y las cabeceras de código.
- `references/figure-notes.md` — qué demuestra cada figura del corpus, y por qué son catálogo de defectos y no modelos de lo correcto.
- `references/sources-and-methods.md` — fuentes, estado de verificación y qué no se encontró.
- `references/regression-examples.md` — expectativas por dominio para comprobar que generaliza.
- `scripts/validate_cdr.py` — verificación mecánica multi-artefacto.
- `scripts/generate_code_headers.py` — cabeceras para inspección, solo bajo autorización.
- `tests/examples/` — conjuntos de artefactos, coherentes e incoherentes a propósito.
