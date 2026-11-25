---
name: use-case-specifier
description: especifica, completa, revisa y refactoriza casos de uso de software en markdown a partir de modelos verbales, modelos de dominio, diagramas uml/plantuml, reglas, prototipos o requisitos. usar para documentacion funcional rup use-case driven, uml, iconix, trazabilidad modelo de dominio-casos de uso-especificacion-robustez-secuencia, revision de requisitos, flujos basicos/alternativos/excepcion, criterios de aceptacion y plantillas verificables.
---

# Use Case Specifier

## Objetivo

Producir especificaciones de casos de uso claras, verificables, no ambiguas y trazables para proyectos de software, alineadas con RUP, UML e ICONIX. Trabajar en español por defecto, salvo que el usuario pida otro idioma. Fundamento y fuentes: `references/sources-and-methods.md`.

La especificación es la parte **sustantiva** del análisis de casos de uso: el diagrama es apenas un índice, y el peso real está en el texto de cada caso de uso. Ese texto es el puente hacia el análisis de robustez, los diagramas de secuencia y las pruebas.

## Insumos y trazabilidad de construcción

Esta skill es el **paso 3** de un pipeline. Cada paso alimenta al siguiente y la especificación debe ser **trazable hacia atrás** a sus insumos:

`modelo verbal` + `modelo de dominio` (de /uml-domain-modeler) + `diagrama de casos de uso` (de /uml-use-case-diagram) → **especificación** → robustez / secuencia / pruebas.

Identificar y usar los insumos disponibles:

- **Requeridos (mínimo para trabajar):** modelo verbal (fuente del comportamiento); caso de uso seleccionado (ID + nombre); actor primario.
- **Recomendados (productos del pipeline — habilitan vocabulario y trazabilidad):**
  - **Modelo de dominio** → controla el vocabulario. Alimenta los conceptos y el control terminológico (§7 de la plantilla), la columna "concepto del dominio" de cada paso de flujo, los datos/objetos manipulados y las postcondiciones. Escribir el texto *en el contexto del modelo de dominio*: los sustantivos del texto deben ser conceptos del dominio.
  - **Diagrama de casos de uso** → aporta actores (primario, secundarios, sistemas externos), las relaciones `<<include>>`/`<<extend>>`/generalización (§8) y confirma el límite/alcance del caso de uso seleccionado.

    **Derivación del identificador.** El diagrama nombra sus casos de uso con alias de PlantUML (`CU_SolicitarPrestamo`), mientras que la especificación y su validador usan identificadores numerados (`CU-01`). No hay conversión automática, así que **numera explícitamente y deja constancia**: el caso de uso dominante recibe `CU-01` y el resto sigue el orden de declaración del diagrama. Registra la correspondencia alias ↔ `CU-NN` en la sección de trazabilidad; sin ella, el número parece arbitrario y se pierde el rastro hacia el diagrama.
- **Opcionales:** reglas de negocio, requisitos funcionales/especiales, restricciones, prototipos/GUI, decisiones conocidas.

Si falta un insumo, **no bloquear**: avanzar con supuestos explicitados y registrar la incertidumbre en la sección de riesgos/ambigüedades; marcar como supuesto todo término no sustentado. Preguntar solo cuando falte un dato que cambie el alcance (el sistema bajo análisis o el caso de uso objetivo).

**Trazabilidad hacia atrás (se verifica en el loop de auditoría):** cada concepto del texto existe en el modelo de dominio; cada actor y cada relación include/extend coinciden con el diagrama; cada flujo rastrea a una frase del modelo verbal. Toda inconsistencia es un hallazgo.

## Forma de la especificación: lean por defecto, completa cuando el contexto lo exige

El corazón de todo caso de uso es la **regla de dos párrafos** (estilo ICONIX): un curso básico (escenario soleado) y sus cursos alternativos/de excepción, escritos como diálogo actor↔sistema. Escribir *siempre* ese núcleo primero; si no cabe en dos párrafos, probablemente son dos casos de uso (y el caso de uso completo debe poder caber en un solo diagrama de secuencia).

- **Forma lean (por defecto):** el núcleo de dos párrafos más lo mínimo indispensable (actor, disparador, precondición, postcondición, criterios de aceptación). Las plantillas largas "hacen más lento" el trabajo y tienden a mezclar requisitos con la narrativa; prefiérela para trabajo ágil/iterativo o cuando el usuario pida brevedad.
- **Plantilla completa (`references/use-case-specification-template.md`):** las 24 secciones. Úsala cuando el contexto lo justifique — entregable formal RUP/académico, dominio regulado, caso de uso complejo con muchas reglas/requisitos especiales, o cuando el usuario la pida. Aun en este caso, el núcleo de dos párrafos manda: las demás secciones lo **envuelven** (trazabilidad, reglas, requisitos especiales, riesgos), no lo reemplazan.

Ante la duda, escribe el núcleo lean y ofrece expandir a la plantilla completa.

## Modos de trabajo

1. **Crear especificación (lean o completa):** elegir la forma según la sección anterior; con la plantilla completa, cargar `references/use-case-specification-template.md`.
2. **Revisar especificación existente:** evaluar con `references/review-rubric.md` y los "Ocho pasos" (`references/sources-and-methods.md`); reportar defectos por severidad y proponer correcciones.
3. **Refactorizar:** corregir nombres, actores, flujos, reglas, trazabilidad y criterios sin cambiar el alcance funcional salvo que el usuario lo pida.
4. **Preparar trazabilidad ICONIX:** asegurar consistencia entre modelo de dominio, casos de uso, especificación, análisis de robustez y diagramas de secuencia.

## Flujo para crear una especificación

1. **Normalizar vocabulario con el modelo de dominio**; no introducir sinónimos ambiguos (los sustantivos del texto = conceptos del dominio).
2. Verificar que el **actor primario** sea externo al sistema y persiga un objetivo funcional observable (tomarlo del diagrama de casos de uso si existe).
3. Confirmar que el caso de uso tenga **un único objetivo** de usuario/negocio a nivel de usuario; no convertir pasos de interfaz, validaciones, cálculos, persistencia ni arquitectura en casos de uso.
4. Nombrar el caso de uso con **verbo en infinitivo + objeto funcional** del dominio (p. ej. `Registrar solicitud de servicio`).
5. Definir alcance, límite del sistema, propósito, resultado observable, precondiciones y disparador.
6. **Escribir el curso básico** como escenario soleado completo, en presente, voz activa, alternando actor/sistema — como pares *acción del usuario → respuesta del sistema* (estilo event/response). Ver reglas de escritura abajo.
7. Escribir **cursos alternativos** para variaciones válidas del negocio y **flujos de excepción** para errores/eventos inesperados; cada uno debe engancharse a un paso concreto del curso básico.
8. Separar reglas de negocio, requisitos especiales, restricciones y detalles de interfaz **fuera** del flujo narrativo.
9. Declarar **postcondiciones verificables**, datos/objetos manipulados y efectos visibles (las postcondiciones se satisfacen justo al final del curso básico — "staying in bounds": pasos extra sobran).
10. Completar **trazabilidad** hacia requisitos, reglas, pruebas, dominio, diagrama de casos de uso, robustez, secuencia e iteración RUP, cuando existan (etiquetas únicas y persistentes por elemento).
11. Formular **criterios de aceptación** en estilo Dado/Cuando/Entonces derivados de los flujos (Dado = precondición, Cuando = paso/evento, Entonces = postcondición/respuesta).
12. Ejecutar el **loop de auditoría** (abajo) antes de entregar.

## Reglas de escritura de flujos

Estas reglas hacen el texto verificable y directamente derivable a robustez/secuencia:

- **Event/response, voz activa, presente:** cada paso es un par *el [Actor] hace X → el Sistema responde Y*. Evitar voz pasiva (una forma de "ser/estar" + participio suele delatarla).
- **Nombrar los objetos de frontera y del dominio en el texto:** "el Sistema muestra la **página de Pago**", no "muestra una página"; "el Cliente selecciona la **Habitación**", no "selecciona una opción". Los sustantivos nombrados se convierten en objetos boundary/entity del análisis de robustez (un controlador sin sustantivo correspondiente en el texto es un "rogue controller").
- **Noun-verb-noun:** sustantivo (objeto) – verbo (mensaje) – sustantivo (objeto). Ese patrón es lo que luego aparece como mensajes en el diagrama de secuencia.
- **Un escenario concreto, no "woolly":** el curso básico describe un camino exitoso concreto, no intenta cubrir todos los casos a la vez.
- **Sin precondiciones superfluas** que oculten la acción inicial real; sin exceso de detalle de presentación (los campos de un formulario son atributos del dominio, no pasos del flujo).

## Reglas metodológicas obligatorias

- Mantener el sistema bajo análisis como **caja negra funcional**; no incluir controladores internos, tablas, frameworks, clases de diseño, SQL, APIs internas ni decisiones de arquitectura ("el Sistema presenta opciones", no "muestra un dropdown"; las definiciones de datos van al diccionario de datos, no al flujo).
- Usar `<<include>>` solo para comportamiento obligatorio reutilizable y `<<extend>>` solo para comportamiento opcional/condicionado; justificar cada relación y mantenerlas consistentes con el diagrama de casos de uso.
- No modelar autenticación, autorización o selección de pantalla como caso de uso incluido por defecto; tratarlas como precondición, requisito especial o regla, salvo que sean objetivos funcionales reales de un actor.
- No mezclar reglas de negocio ni requisitos no funcionales dentro de los pasos; referenciarlas por ID y desarrollarlas en su sección.
- Usar términos oficiales del modelo de dominio para conceptos y objetos manipulados.
- **No forzar cada requisito dentro de un caso de uso:** los casos de uso revelan la mayoría — no todos — los requisitos funcionales; los que no encajan van al SRS/lista de requisitos y se trazan.
- Vigilar los **"traps"**: explosión de casos de uso (si hay demasiados, probablemente están al nivel de abstracción equivocado) y flujos con más de ~10–15 pasos (confirmar que describen un solo escenario).
- Preferir resultados observables y verificables sobre frases vagas como "gestiona información", "procesa datos" o "muestra pantalla".

## Loop de auditoría

No entregar el primer borrador. Iterar hasta converger en una especificación limpia, mínima pero suficiente:

1. **Refinar** la especificación (núcleo de dos párrafos + secciones aplicables).
2. **Auditar** contra, en orden: (a) los **Ocho pasos para un mejor caso de uso** y la rúbrica (`references/review-rubric.md`, `references/sources-and-methods.md`); (b) los atributos de calidad (no ambiguo, completo, verificable) y los "traps" de Wiegers; (c) la **trazabilidad hacia atrás** a los insumos (cada concepto ∈ modelo de dominio; cada actor/relación ∈ diagrama; cada flujo ∈ modelo verbal); (d) la coherencia forward hacia robustez/secuencia/pruebas.
3. **Corregir** cada hallazgo o dejar constancia del porqué si se conserva.
4. **Converger (criterio cuantificado):** el ciclo se cierra cuando se cumplen a la vez: **cero hallazgos críticos y cero mayores**; **como máximo dos menores**, documentados y justificados; **100 % de los flujos** (básico, alternativos y de excepción) con postcondición verificable y criterio de aceptación asociado; y **dos pasadas consecutivas sin hallazgos nuevos** — una pasada limpia puede ser suerte, dos no. **Tope duro: cinco pasadas.** Si al alcanzarlo persisten hallazgos críticos o mayores, **no declares éxito**: entrega el mejor resultado disponible, marca el estado como **`AUDITORÍA NO SUPERADA`**, enumera los hallazgos abiertos y di qué insumo o decisión del usuario cerraría cada uno. Un fracaso declarado es más útil que un visto bueno optimista, porque sobre él se puede actuar. El tope es además metodológico: la especificación busca ser mínima pero suficiente, y si sigue creciendo en la tercera vuelta suele ser señal de que **el caso de uso debe partirse**. Los trade-offs genuinos se registran en riesgos/ambigüedades, no se iteran sin fin.

## Salidas

Para una especificación **lean**, entregar el caso de uso en dos párrafos (curso básico + alternativos/excepciones) más actor, disparador, precondiciones, postcondiciones verificables y criterios de aceptación Dado/Cuando/Entonces.

Para una especificación **completa**, preservar la estructura de `references/use-case-specification-template.md` y completar todas las secciones aplicables; usar `No aplica` cuando esté justificado y `[Pendiente]` cuando falte información (registrando la razón en riesgos/ambigüedades).

Para una **revisión**, entregar: diagnóstico ejecutivo; hallazgos por severidad (crítico/mayor/menor); checklist cumple/no cumple/parcial; correcciones o versión refactorizada; y riesgos de trazabilidad hacia dominio, diagrama, robustez, secuencia y pruebas.

Salidas de traza forward (bajo pedido o en modo ICONIX):

- **Requisitos funcionales derivados** del caso de uso, en forma "el sistema deberá [respuesta]" (una por paso/regla relevante), trazados al caso de uso.
- **Insumos para robustez:** objetos boundary (interfaces nombradas), entity (conceptos del dominio) y control (coordinadores del flujo) candidatos.
- **Mensajes de secuencia** derivados de los pasos (preservando alternativas/excepciones).
- **Pruebas/criterios de aceptación** que cubran curso básico, alternativos y excepciones.

## Recursos

- `references/sources-and-methods.md`: fundamento en las fuentes (Fowler; Rosenberg & Stephens; Rosenberg, Stephens & Collins-Cope; Wiegers & Beatty), los "Ocho pasos para un mejor caso de uso", el estilo event/response, la regla de dos párrafos, los "traps" y la derivación Dado/Cuando/Entonces.
- `references/use-case-specification-template.md`: plantilla completa (24 secciones) para la forma completa.
- `references/review-rubric.md`: compuerta de calidad para revisión.
- `references/minimal-examples.md`: ejemplos breves de estilo de salida.
