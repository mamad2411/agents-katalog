---
name: test-define
description: 'Crear casos de prueba (TC-XXX) a partir de los criterios de aceptación de cualquier artefacto de especificación que los tenga con identificador codificado: una historia de usuario (US-XXX), un work item (WI-XXX), un feature ya implementado (FT-XXX) o cualquier otro documento de especificación cuyos criterios estén numerados o codificados (AC-001, 1.1, R-3, etc.), siguiendo el estándar IEEE 29119-4. Activar cuando el usuario pida "definir test cases", "crear casos de prueba", "generar TCs", "pruebas para la US/WI/FT", "pruebas para este spec/documento", "documentar pruebas", "casos de prueba para los criterios de aceptación", o cualquier variante que implique producir documentación de prueba a partir de requisitos ya especificados. También activar cuando el usuario mencione "test-define" o "/test-define".'
license: MIT
---

# Skill: Definir casos de prueba

Genera **casos de prueba documentados** (`TC-XXX`) a partir de los criterios de aceptación de un artefacto ya especificado, siguiendo la estructura IEEE 29119-4. Como guía de cobertura mínima, cada criterio se analiza desde tres perspectivas —**happy path**, **error** y **límite**—, generando los TCs que el criterio requiera (una perspectiva puede omitirse si no aplica; ver Paso 3).

> **Requisito único sobre el artefacto:** que sus criterios de aceptación tengan un **identificador codificado y único** dentro del documento. El **formato del identificador es indiferente** (`AC-001`, `1.1`, `2.4`, `R-3`, `CA-07`…) y el artefacto **no necesita pertenecer a este plugin**: puede ser una US/WI/FT del repo o cualquier otro documento de especificación, sea cual sea su origen, herramienta o formato. Ver [Selección del artefacto](#selección-del-artefacto) y Paso 1.

> **Solo documentación de prueba:** este skill produce archivos `TC-XXX-{slug}.md` más un índice `test-cases/README.md`. No implementa código de prueba ni ejecuta tests. La única modificación permitida sobre el artefacto origen es agregar, bajo cada criterio de aceptación, la lista de casos de prueba que lo cubren (ver Paso 5); no altera ningún otro contenido del artefacto ni otros archivos existentes.

## Mapa de referencias

Carga el archivo correspondiente cuando vayas a ejecutar la tarea; el detalle íntegro vive en `references/`.

| Necesitas… | Archivo |
| ---------- | ------- |
| Integración condicional con un sistema de seguimiento externo: detalle específico de cada sistema (creación de work items, campos, IDs, vinculación al artefacto padre) | `references/<sistema>.md` (p. ej. [`references/azure-devops.md`](references/azure-devops.md) para Azure DevOps) — leer solo si el repo está vinculado (ver [Integración con un sistema de seguimiento externo](#integración-con-un-sistema-de-seguimiento-externo-condicional)) |
| Estructura del archivo de un caso de prueba | [`assets/test-case-template.md`](assets/test-case-template.md) |

---

## Cómo preguntar al usuario

Toda pregunta al usuario va por la **herramienta de preguntas estructuradas** (opciones tappables), no como prosa libre. Reglas:

- Opciones cortas y mutuamente excluyentes (2-4 por pregunta).
- No repreguntar lo que ya conste en el artefacto o en la conversación.
- Si el cliente no expone la herramienta, formular en prosa con opciones enumeradas.

---

## Resolución de idioma

Redactar los TCs y los mensajes al usuario en el idioma del artefacto origen. Si hay conflicto o ambigüedad, preguntar al usuario antes de generar.

---

## Integración con un sistema de seguimiento externo (condicional)

La sincronización con un sistema de seguimiento de trabajo externo (Azure DevOps, Jira u otro) es transversal a la generación de TCs, pero **solo aplica si el repositorio está vinculado a uno**. Este skill solo resuelve **si** hay vinculación y **qué** referencia cargar; todo el detalle propio de cada sistema (herramienta MCP, campos, tipo de work item, configuración de conexión, límites de formato) vive exclusivamente en su archivo de `references/`. Para no cargar contexto innecesario:

1. **Detectar** la vinculación leyendo `.agents/MEMORY.md` (raíz del repo): buscar la señal `work_item_tracking: <sistema>` con valor no vacío (p. ej. `azure_devops`).
2. **Si NO hay señal** → el repo no usa un tracker externo. Continuar con la numeración local secuencial (ver [Numeración y nombres de archivo](#numeración-y-nombres-de-archivo)); **no** leer ninguna referencia de tracker.
3. **Si hay señal** → cargar `references/<sistema>.md` (p. ej. `references/azure-devops.md` para `work_item_tracking: azure_devops`) y seguir **únicamente** sus pasos antes de guardar cualquier archivo local (Paso 4). Algunos sistemas exigen resolver una jerarquía propia (p. ej. un plan y una suite de pruebas) antes de crear el work item del caso de prueba; esos pasos, si aplican, viven íntegramente en el archivo de referencia del sistema. Si no existe un archivo de referencia para el sistema indicado, informar al usuario y continuar con numeración local secuencial.

**Regla de fidelidad (transversal a cualquier sistema):** toda la información del TC debe quedar representada en el work item externo — los pasos de ejecución en un campo dedicado si el sistema lo expone, el resto en la descripción si no lo expone. Ninguna sección del `.md` puede omitirse al sincronizar; el objetivo es poder reconstruir el TC completo a partir del work item si el archivo local se perdiera. Qué campo usa cada sistema para qué sección es detalle de su archivo de referencia.

---

## Selección del artefacto

El usuario indica un artefacto: puede ser un identificador conocido del repo (`US-XXX`, `WI-XXX`, `FT-XXX`) **o una ruta/nombre de cualquier otro documento** de especificación. La única condición para procesarlo es la del Paso 1: que tenga criterios de aceptación con identificador codificado. Si el artefacto es ambiguo (varios candidatos, o no está clara la ruta), **preguntar** antes de continuar.

| Tipo | Ubicación del artefacto | Ubicación de los TCs |
|------|------------------------|----------------------|
| Historia de usuario | `docs/specs/user-stories/US-XXX-{nombre}/README.md` | `docs/specs/user-stories/US-XXX-{nombre}/test-cases/` |
| Work item | `docs/specs/work-items/WI-XXX-{kebab-case}/README.md` | `docs/specs/work-items/WI-XXX-{kebab-case}/test-cases/` |
| Feature (funcionalidad ya implementada) | `docs/specs/features/FT-XXX-{slug}/README.md` | `docs/specs/features/FT-XXX-{slug}/test-cases/` |
| **Cualquier otro artefacto** de especificación, sea cual sea su origen o formato | La ruta que indique el usuario (buscarla en el repo si solo da un nombre) | `test-cases/` dentro de la carpeta que contiene el artefacto; si el artefacto es un archivo suelto, `test-cases/` junto a él. Confirmar la ruta con el usuario antes de escribir. |

> La carpeta `test-cases/` se crea si no existe; el archivo del artefacto permanece donde está.

### Feature (`FT-XXX`) — funcionalidad ya implementada

Un `FT-XXX` es el registro de una funcionalidad **ya implementada**, que vive en
`docs/specs/features/`. Puede nacer del flujo «Analizar legado» de `work-research` —feature
inferido de código— o documentar funcionalidad existente en general; en ambos casos
`test-define` lo trata **igual** que una US o un WI: lee los criterios de la sección
**Criterios de aceptación** del `README.md` —con el identificador que usen, normalmente `AC-XXX`—
y verifica el estado si el artefacto lo declara (`Estado: Ready`), sigue el
flujo normal (entrevista, perspectivas happy/error/límite, índice, trazabilidad del Paso
5) y guarda los TCs bajo `docs/specs/features/FT-XXX-{slug}/test-cases/`. Particularidad: los
criterios del feature describen el comportamiento **ya implementado**, así que los TCs son
la **red de seguridad** para cubrirlo; cuando un TC valide un comportamiento que el
discovery marcó como posible bug preservado, anotarlo para trazabilidad.

---

## Paso 1 — Leer y extraer criterios

1. **Ubicar y leer el artefacto completo**, sea cual sea su formato. Localizar la sección de criterios de aceptación: normalmente titulada «Criterios de aceptación» / «Acceptance Criteria», pero puede llamarse «Requisitos», «Requirements», «Comportamiento esperado» o similar. En artefactos del repo:
   - **US / WI / FT:** el `README.md` del artefacto; los criterios están en la sección **Criterios de aceptación**.
   - **Cualquier otro artefacto:** la sección equivalente dentro del documento indicado por el usuario. Si hay dudas sobre cuál sección contiene los criterios, preguntar en vez de asumir.
2. **Verificar el estado del artefacto — solo si el artefacto declara un campo de estado** (`Estado:` / `Status:`). Es un campo propio de los artefactos de este plugin; **su ausencia no es un motivo para parar** y no debe pedirse al usuario que lo agregue.
   - Sin campo de estado → continuar (el artefacto es externo al plugin).
   - `Estado: Ready` → continuar.
   - `Estado: Draft` → parar: el artefacto no está listo para producir TCs.
   - `Estado: Obsolete` → parar: el artefacto fue descartado; no generar TCs sobre él.
   - Cualquier otro estado → parar e informar: "El artefacto tiene estado [X], que no es soportado. Solo se procesan artefactos en estado `Ready`."
3. Si no hay criterios de aceptación definidos (sección ausente o vacía), **parar** e indicar que el artefacto necesita criterios antes de poder generar TCs.
4. **Verificar que cada criterio tenga un identificador codificado y único dentro del documento.** El requisito es la **existencia** del identificador, **no su formato**: `AC-001`, `AC-1`, `1.1`, `2.4`, `R-3`, `CA-07` y equivalentes son todos válidos mientras identifiquen unívocamente al criterio. **No exigir el formato `AC-XXX`** ni rechazar un artefacto por no seguir las convenciones de este plugin.
   - Registrar el **esquema de identificación detectado** (p. ej. «numérico jerárquico `N.M`») y **usarlo tal cual** en todo el resto del flujo: los TCs referencian el identificador **verbatim**, sin renombrarlo ni normalizarlo.
   - Si el documento numera los criterios de forma implícita (lista ordenada sin código escrito, viñetas sin marca), eso **no** cuenta como identificador codificado: aplica el error de abajo.
   - Si uno o más criterios carecen de identificador, **parar** e informar al usuario:

   ```
   ERROR Trazabilidad incompleta:
   Los siguientes criterios no tienen identificador: [lista].
   Cada criterio de aceptación debe tener un identificador único (en el formato que use
   el documento) antes de generar TCs.
   Agrégalos en el artefacto y reinicia el proceso.
   ```

   No continuar hasta que todos los criterios tengan identificador. No asignar identificadores automáticamente.
5. Listar los criterios encontrados (con su identificador tal como aparece y su título) y pedir confirmación al usuario antes de continuar.

---

## Paso 2 — Entrevista de clarificación

Antes de generar ningún TC, resolver las dudas que puedan afectar la calidad de los casos. Las preguntas a continuación son el conjunto estándar; **omitir las que ya estén respondidas en el artefacto o en la conversación** para no interrogar innecesariamente al usuario.

Preguntar usando la herramienta de preguntas estructuradas sobre:

1. **Alcance**: ¿TCs para todos los criterios o para un subconjunto? Opciones: [Todos] / [Seleccionar criterios].
2. **Entorno de referencia**: ¿desarrollo, staging o producción? Afecta URLs, datos de prueba y configuraciones.
3. **Roles de usuario involucrados**: si el artefacto no los especifica, listar los inferidos y confirmar.
4. **Datos de prueba**: ¿hay juegos de datos ya definidos o se proponen dentro del TC? Opciones: [Ya existen] / [Proponer en el TC].
5. **Escenarios de error críticos**: ¿el negocio prioriza algún error específico que el artefacto no detalla?

No avanzar al Paso 3 hasta recibir respuesta a las preguntas que apliquen.

---

## Paso 3 — Generar casos de prueba

Por cada criterio en el alcance, analizar cuántos TCs son necesarios según la información del artefacto, las respuestas del usuario en la entrevista y la complejidad del escenario. No hay un número fijo: un criterio simple puede requerir un solo TC; uno complejo puede necesitar varios. Las tres perspectivas sirven como guía de cobertura mínima, no como límite:

| Perspectiva | Qué cubre | Ejemplo de slug |
|-------------|-----------|-----------------|
| **Happy path** | Flujo exitoso con datos válidos; el criterio se cumple completamente. | `login-credenciales-validas-happy` |
| **Error** | Entrada inválida, permiso denegado, servicio caído, o cualquier desvío que el sistema debe manejar con un error controlado. | `login-password-incorrecto-error` |
| **Límite** | Valores en el borde del dominio: máximo/mínimo permitido, longitud exacta, fecha límite, concurrencia, campo vacío. | `nombre-255-caracteres-limite` |

Si dentro de una perspectiva hay múltiples escenarios distintos que vale la pena distinguir (p. ej., dos tipos de error con comportamientos diferentes), crear un TC por escenario en lugar de agruparlos. Si una perspectiva no aplica al criterio, omitirla sin necesidad de justificar salvo que sea evidente que debería existir y se descarta por alguna razón concreta.

### Numeración y nombres de archivo

- **Sin tracker externo vinculado**: el secuencial `XXX` (tres dígitos: 001, 002, …) es por artefacto padre, siguiendo el orden criterio-a-criterio (happy → error → límite). Si la carpeta `test-cases/` ya existe con TCs previos, leer los archivos presentes, determinar el número más alto y continuar desde el siguiente.
- **Con tracker externo vinculado**: `XXX` es el identificador que asigna ese sistema al work item «Test Case» creado; su formato exacto (numérico, con o sin padding, etc.) lo define el archivo de referencia del sistema. Ver [Integración con un sistema de seguimiento externo](#integración-con-un-sistema-de-seguimiento-externo-condicional).
- No regenerar TCs ya existentes salvo instrucción explícita del usuario.
- Nombre de archivo: `TC-XXX-{slug}.md`, donde el slug sigue el patrón `{criterio-resumido}-{perspectiva}` (ver columna Ejemplo arriba). Un TC por archivo.
- El nombre completo del archivo (`TC-XXX-{slug}.md`) y, si hay un tracker externo vinculado, el título usado al crear el work item deben respetar cualquier límite de longitud propio de ese sistema (ver su archivo de referencia); si el título GWT completo lo supera, usar una versión abreviada como título del work item y conservar el título completo en el encabezado del TC (`# TC-{{XXX}} — ...`).

### Estructura de cada TC

Usar `assets/test-case-template.md` para todos los campos. Reglas de llenado:

- **Perspectiva:** registrar la perspectiva de cobertura del caso (`Happy Path`, `Error` o `Límite`), coherente con el sufijo del slug del archivo. No confundir con el o los tipos de prueba del campo Tipo de prueba (Unit/Integration/E2E…).
- **Título descriptivo:** redactarlo en formato Given–When–Then (GWT), **respetando el idioma del artefacto origen**: en español usar `Dado {{contexto/precondición}}, Cuando {{acción/evento}}, Entonces {{resultado esperado}}`; en inglés usar `Given {{context/precondition}}, When {{action/event}}, Then {{expected result}}`. Debe describir el escenario concreto que valida el TC, coherente con las precondiciones, los pasos y el resultado esperado final.
- **Criterio de aceptación:** referenciar el identificador del criterio **exactamente como aparece en el artefacto origen** (`AC-012`, `1.3`, `R-3`…). **No normalizar ni reescribir** el identificador a otro formato: el vínculo de trazabilidad debe ser buscable literalmente en el artefacto. Este campo no puede estar vacío ni ser genérico.
- **Tipo de prueba:** declarar la **intención de diseño** del caso, no su estado de ejecución. Como los TC se escriben **antes de implementar**, el valor es `Manual` (no se automatiza, requiere ejecución humana por diseño) **o** uno o varios tipos de entre `Unit`, `Integration`, `API Test`, `Visual Test`, `E2E`, separados por coma y ordenados de menor a mayor nivel (p. ej. `Unit, E2E`) — ver la tabla siguiente para inferirlos. `Manual` no se combina con tipos. Este campo es la fuente que consume `trace-validate` para distinguir "manual por diseño" de "pendiente de automatizar"; no dejarlo vacío. Ante la duda entre `Manual` y automatizable, o sobre qué tipo(s) asignar, preguntar al usuario.
  - Para determinar el o los tipos de prueba (cuando el valor no es `Manual`), recorrer esta tabla de arriba hacia abajo **evaluando cada fila de forma independiente** — a diferencia de una tabla de decisión que se detiene en la primera coincidencia, aquí se **acumulan todos los tipos cuya pregunta aplique**: un mismo TC puede necesitar más de un tipo (p. ej. una API que conviene cubrir tanto a nivel de unidad como end-to-end).

    | Pregunta | ¿Aplica? → agrega |
    |----------|--------------------|
    | ¿Puede probarse de forma aislada, sin dependencias externas ni servicios reales? | Unit |
    | ¿Necesita verificar la interacción real entre dos o más componentes/servicios (DB, colas, otros servicios)? | Integration |
    | ¿Solo verifica el contrato de un endpoint (request/response), sin recorrer la lógica interna completa? | API Test |
    | ¿Solo valida la apariencia visual (layout, estilos, snapshots)? | Visual Test |
    | ¿Debe validar la experiencia completa del usuario de punta a punta? | E2E |

    El valor final del campo es la lista de tipos marcados como aplicables, escrita de menor a mayor nivel según el orden de la tabla (`Unit, Integration, API Test, Visual Test, E2E`). Si ninguna pregunta aplica, reconsiderar si el caso es en realidad `Manual`. Para los TC `Manual` no aplica ningún tipo (el campo queda solo en `Manual`).
- **Work Item (<sistema>):** enlace markdown al work item creado — solo si el TC se creó vía el tracker vinculado (etiqueta y formato exactos en su archivo de referencia, p. ej. `Work Item (ADO)` en `references/azure-devops.md`); omitir la línea si no aplica.
- **Prioridad:** derivar del impacto del criterio en el negocio: Alta si el criterio es bloqueante o afecta seguridad/datos; Media si es funcional importante; Baja si es edge case o cosmético. Si no hay suficiente contexto, preguntar al usuario.
- **Creado por:** usar `git config user.name` del repositorio. Si no está disponible, dejar el campo vacío.
- **Precondiciones:** ser específico — incluir estado del sistema, datos existentes y permisos requeridos.
- **Datos de prueba:** usar los confirmados en el Paso 2; si se proponen, marcarlos con `[propuesto]`.
- **Pasos:** acciones atómicas y observables; cada fila incluye actor + acción + resultado esperado del paso.
- **Resultado esperado final:** estado observable del sistema (UI, código HTTP, mensaje, evento publicado), no estado interno.

---

## Paso 4 — Guardar y reportar

1. Crear la carpeta `test-cases/` si no existe. Si el repo tiene un tracker externo vinculado (ver [Integración con un sistema de seguimiento externo](#integración-con-un-sistema-de-seguimiento-externo-condicional)), los work items ya deben estar creados y sus identificadores resueltos antes de este paso.
2. Escribir cada `TC-XXX-{slug}.md` en la ruta correcta según la tabla de Selección del artefacto. Guardar cada TC con `Estado: Ready` salvo que el usuario indique lo contrario.
3. Crear o actualizar el índice `test-cases/README.md` con una tabla que liste **todos** los TCs de la carpeta (los recién creados más los que ya existieran), ordenados por número de TC. La tabla lleva estas columnas:

   | TC | Perspectiva | Tipo de prueba | Prioridad | Criterio de aceptación |
   |----|-------------|----------------|-----------|------------------------|
   | [TC-001](./TC-001-{slug}.md) | Happy Path | Unit, E2E | Alta | AC-001 |

   Reglas del índice:
   - **TC:** ID enlazado por ruta relativa a su archivo `TC-XXX-{slug}.md`.
   - **Perspectiva**, **Tipo de prueba** y **Prioridad:** copiar el valor tal como quedó en el encabezado del TC (Tipo de prueba se copia tal cual, con todos los tipos separados por coma si son varios).
   - **Criterio de aceptación:** mostrar **solo el identificador** tal como aparece en el artefacto (`AC-001`, `1.1`, …), sin el título. (En el encabezado del TC sí va identificador **+ título corto**; el índice se queda en el identificador para que la columna sea legible y comparable.)
   - Regenerar el índice completo en cada corrida para reflejar el estado actual de la carpeta; redactarlo en el idioma del artefacto origen.
4. Mostrar al usuario un resumen:
   - Criterios procesados.
   - TCs generados: ID · título · perspectiva.
   - TCs omitidos con justificación.
5. Preguntar si el usuario acepta el resultado:
   - **Acepta** → cerrar; el skill termina.
   - **Ajuste puntual** (campo incorrecto, dato de prueba erróneo) → aplicar la corrección y volver a este paso para confirmar.
   - **Cambio estructural** (nuevos criterios, redefinición del alcance) → reiniciar desde el Paso 1.

---

## Paso 5 — Actualizar el artefacto origen con la trazabilidad

Una vez guardados y aceptados los TCs, editar el artefacto origen (el `README.md` de la US, del WI o del FT, **o el archivo del artefacto externo procesado**) para dejar registrada la trazabilidad directa: bajo cada criterio de aceptación, agregar la lista de los casos de prueba que lo cubren.

> Si el artefacto no pertenece al repo (documento externo, spec de otra herramienta, archivo de solo lectura), **pedir confirmación al usuario antes de modificarlo**; si no autoriza la edición, omitir este paso y reportar la trazabilidad en el resumen y en el índice `test-cases/README.md`.

Reglas:

- La **única** modificación permitida sobre el artefacto es agregar esta línea de trazabilidad. No reescribir, reordenar ni alterar el texto de los criterios ni ninguna otra sección.
- Para cada criterio, inmediatamente debajo de su enunciado, agregar una línea `Casos de prueba:` con los TCs que lo referencian, enlazados por ruta relativa a la carpeta `test-cases/`. Separar múltiples TCs con ` · `. Respetar el estilo y la indentación del documento origen (si los criterios son ítems de una lista anidada, la línea va al mismo nivel del ítem).
- El texto del enlace es el ID del TC (`TC-XXX`); el destino es el archivo `TC-XXX-{slug}.md` correspondiente.
- Si un criterio no tiene TCs (perspectiva omitida por completo), no agregar la línea o dejarla como `Casos de prueba: —` según convenga a la legibilidad.
- Si el criterio ya tenía una línea `Casos de prueba:` de una corrida anterior, reemplazarla por la lista completa y actualizada (no duplicar).

Formato (ejemplo):

```
AC-008 (Observabilidad): El logging estructurado con Pino está activo y registra al menos el inicio del servidor y los errores de autenticación.
Casos de prueba: [TC-019](./test-cases/TC-019-log-arranque-servidor-happy.md) · [TC-020](./test-cases/TC-020-log-error-autenticacion-error.md)
```

Tras editar, informar al usuario qué criterios quedaron enlazados con qué TCs.

---

## Trazabilidad

Cada TC referencia exactamente un criterio de aceptación en el campo **Criterio de aceptación** del encabezado. Un TC sin ese campo completo es inválido.

La trazabilidad inversa (de un criterio a sus TCs) se obtiene buscando el identificador del criterio —en el formato del artefacto origen— en los archivos de la carpeta `test-cases/` del artefacto. La trazabilidad directa (de un criterio a sus TCs) queda registrada en el propio artefacto origen mediante la línea `Casos de prueba:` que se agrega en el Paso 5.

---

## Anti-patterns

- Generar TCs sin haber completado la entrevista del Paso 2 (incluso si parece obvio).
- Crear un TC que cubra más de un criterio de aceptación.
- Omitir una perspectiva que evidentemente debería existir sin dejar constancia del motivo (una perspectiva que no aplica al criterio puede omitirse sin justificación; ver Paso 3).
- Dejar el campo **Criterio de aceptación** vacío o con un valor genérico ("criterio 1").
- Reutilizar un número de secuencia ya existente en `test-cases/`.
- Dejar el índice `test-cases/README.md` desactualizado tras crear o regenerar TCs (debe reflejar siempre todos los TCs de la carpeta).
- Regenerar TCs existentes sin instrucción explícita del usuario.
- Modificar el artefacto origen más allá de agregar la línea `Casos de prueba:` bajo cada criterio en el Paso 5; cualquier otro cambio al texto de los criterios o a otras secciones está prohibido.
- **Rechazar un artefacto por no seguir las convenciones de este plugin** (nombre `US-XXX`/`WI-XXX`/`FT-XXX`, ubicación en `docs/specs/`, campo `Estado:`, identificadores en formato `AC-XXX`). El único requisito es que los criterios tengan identificador codificado; el formato es indiferente.
- **Renombrar o normalizar los identificadores de criterio** del artefacto origen (p. ej. convertir `1.1` en `AC-001`) al escribir los TCs o el índice: se referencian verbatim.
- Pedir al usuario que agregue un campo `Estado:` a un artefacto que no pertenece al plugin.
- Escribir código de prueba (Jest, Cypress, etc.); ese trabajo corresponde a `work-implement` (tipos `TC-XXX` / `FT-XXX`, ejecutados bajo `quality-specialist`).
- Continuar si el artefacto **declara** un estado distinto de `Ready`, o si no tiene criterios de aceptación.
- Asignar identificadores de criterio automáticamente; si faltan, parar y pedirle al usuario que los agregue en el artefacto.
- Lanzar preguntas como prosa libre cuando el cliente expone herramienta de preguntas estructuradas.
- Crear el archivo TC local con ID secuencial cuando el repo tiene un tracker externo vinculado y su herramienta MCP está disponible — siempre crear el work item en el tracker primero y usar su identificador (ver el archivo de referencia del sistema).
- Omitir el campo `Work Item (<sistema>)` en el encabezado del TC cuando fue creado vía MCP.
- Ignorar los límites de formato (p. ej. longitud de título) que imponga el sistema vinculado; ver su archivo de referencia.