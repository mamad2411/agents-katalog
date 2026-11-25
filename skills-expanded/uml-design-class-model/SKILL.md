---
name: uml-design-class-model
description: >
  ensambla, revisa y valida el modelo de clases de DISENO en plantuml: el modelo estatico del diseno detallado ICONIX, con operaciones, tipos, visibilidad, multiplicidades, herencia, agregacion y composicion. usar para: diagrama de clases de diseno, modelo estatico, modelo de clases detallado, anadir las operaciones a las clases, llevar el modelo de dominio al diseno, clases del espacio de la solucion, consumir el delta de operaciones del diagrama de secuencia, refactorizacion del modelo (model refactoring), preparar el modelo para el critical design review. NO es el modelo del dominio conceptual: eso lo hace /uml-domain-modeler, y esta skill ni lo sustituye ni lo modifica. regla que la gobierna: cada elemento debe trazar a un artefacto de origen —las operaciones a los mensajes de secuencia, las relaciones al dominio, los atributos a la especificacion—; lo que no traza es un hallazgo, no licencia para inventar. cada entregable pasa por un ciclo interno de auditoria con reglas verificables por script.
---

# UML Design Class Model

Trabajar en español por defecto, salvo que el usuario pida otro idioma. Fundamento y fuentes: `references/sources-and-methods.md`.

*Las citas de Fowler se dan normalizadas: el archivo del corpus tiene corrupción de OCR (`dass`→class, `an`→on, `1`→I). Detalle en `references/notation-rules.md`.*

## Naturaleza y propósito

Es **el modelo estático del diseño detallado**: dónde converge todo el pipeline. Agile ICONIX lo define sin rodeos: *"The static model is the grittier, more detailed version of the domain model, and it contains more implementation details."*

**No se crea *desde* el modelo de dominio.** Es una **convergencia con reparto explícito de trabajo** (Rosenberg & Stephens, 4363):

> *"The operations on each class are taken directly from the messages we drew on the sequence diagrams. The relationships between each class are also derived from the relationships in the domain model and from the operations. The attributes on each class are derived from the detail in the use cases and any supplementary specs…"*

| Qué | De dónde |
|---|---|
| **Operaciones** | Los mensajes del diagrama de secuencia |
| **Relaciones** | Las del dominio, más las que imponen las operaciones |
| **Atributos** | El detalle de los casos de uso y sus especificaciones complementarias |
| **Clases nuevas** | El espacio de la **solución**, descubierto al diseñar |

Y el marco conceptual (4286): *"The two spaces are now converging during detailed design."* El modelo de dominio muestra **solo el espacio del problema**; aquí se le suma el de la solución, y ambos convergen.

**Dos artefactos separados, no uno.** Agile ICONIX es explícito en mantenerlos aparte: *"The domain model reflects our current understanding of the business domain (i.e., it's an analysis-level artifact), whereas the fleshed-out class diagrams … are collectively a detailed design artifact."* Por eso esta skill **emite un archivo nuevo y no toca el de dominio**.

## La regla que gobierna todo lo demás

De la misma fuente, y es lo único que hay que recordar si se olvida el resto:

> *"It's tempting to add detail to the class diagram because you think it might be needed, but… it's better fill in the detail while drawing the sequence diagrams. If… the static model still appears to be missing some detail, then you should revisit the sequence diagrams (and possibly even the robustness diagrams and use cases)… use it as an indication that you need to revisit your previous diagrams, not that you need to second-guess yourself and add detail arbitrarily."*

**Nada entra al modelo que no se haya descubierto aguas arriba.** Si falta algo, la respuesta es **volver atrás**, no inventar. Esta skill no es un generador creativo: es un **ensamblador con procedencia obligatoria**. Cada elemento traza a su origen, y lo que no traza es un hallazgo que se reporta — nunca un hueco que se rellena a ojo.

Agile ICONIX describe la cadena ideal: *"the operations on the classes on the static model should have gotten there by message arrows drawn on sequence diagrams, and the source code headers should have been generated from these class diagrams."*

## Insumos y trazabilidad de construcción

Esta skill es el **paso 7** del pipeline:

```
dominio ──────────────────────────────┐
casos de uso → especificación ────────┤
robustez (DR-XX) → PDR ───────────────┤
secuencia (DS-XX) + delta ────────────┴→ MODELO DE CLASES (MC-XX, esta skill)
        ↑                                            │
        └──── delta de refactorización ──────────────┘
                                                     ↓
                                        CDR (Milestone 3) · CP-XX · código
```

| Insumo | Nivel | Qué aporta | Si falta |
|---|---|---|---|
| **Diagrama(s) de secuencia** `DS-XX` **+ delta de operaciones** | **Obligatorio** | **Las operaciones**, tomadas directamente de los mensajes. El delta trae además la clase receptora, la justificación y si es del problema o de la solución | **Detente**: sin esto sería un modelo de dominio con adornos |
| **Modelo de dominio** (.puml) | **Obligatorio** | El **esqueleto del espacio del problema**: clases y relaciones conceptuales | **Detente**: se pierde la trazabilidad al problema, que es el punto de ICONIX |
| **Especificación(es)** `CU-XX` (.md) | **Obligatorio** | **Los atributos**, y las `RN-XX` como invariantes y restricciones | Los atributos no tendrían procedencia verificable |
| **Diagrama(s) de robustez** `DR-XX` | Recomendado | Procedencia B/C/E de cada clase; comprobar que el delta de entidades aterrizó | No se verifica que el descubrimiento de robustez llegó |
| **Veredicto del PDR** `PDR-XX` | Recomendado | Confirma que se diseña sobre material aprobado | **Advierte** si el veredicto fue `Reinspección requerida` |
| Wireframes o mockups | Opcional | La fuente los nombra como *supplementary specs* de atributos; *"Fields on screens often imply attributes on entity classes"* | La matriz de atributos queda parcial |
| Arquitectura o framework | Opcional | Asignación a capas; **activa la capa de arquitectura** | Capa declarada **no ejecutada** |
| Modelo verbal | Opcional | Contexto y alcance | — |

**El diagrama de casos de uso NO es insumo.** Los actores no se vuelven clases de diseño; lo que aportan llega por la especificación. Se dice para que nadie lo exija sin motivo.

**Regla de los insumos ausentes.** Lo que falta **desactiva capas concretas**, y una capa que no se pudo ejecutar **se declara como no ejecutada** en el certificado. Nunca se silencia, y **la degradación llega hasta el veredicto** — no basta con imprimirla.

**Identificador `MC-XX`.** Es **nuevo**: a diferencia de `DS-XX` y `CP-XX`, que la plantilla de `use-case-specifier` reservaba desde el principio, nadie había previsto un identificador para este artefacto. La cadena queda:

`RF-XX` → `CU-XX` → `FA-XX`/`FE-XX` → `DR-XX` + `B-`/`C-`/`E-` → `PDR-XX` → `DS-XX` → **`MC-XX`** → `CP-XX` → CDR

## Procedimiento

1. **Inventaría los insumos**; declara los que falten y qué capas desactivan. Si el veredicto del PDR no fue favorable, **dilo antes de empezar**.
2. **Copia el esqueleto del dominio**: clases del espacio del problema con sus relaciones. Es el punto de partida, no el resultado.
3. **Vuelca el delta de operaciones**: cada operación a su clase receptora, conservando la justificación. Es la aportación primaria.
4. **Añade los atributos** desde la especificación y los prototipos, no de memoria.
5. **Declara las clases del espacio de la solución** — andamiaje, infraestructura, *helpers* — **marcándolas como tales**. Mezclarlas en silencio con las del dominio destruye la trazabilidad que justifica todo el método.
6. **Limpia el modelo** (ver abajo).
7. **Registra la procedencia** de cada elemento a medida que lo añades, no al final.
8. **Corre el validador** y ejecuta el ciclo de auditoría interna.
9. **Ofrece las correcciones** de los artefactos de entrada, enrutadas a su skill, y aplica solo lo confirmado.

## Limpiar el modelo antes del CDR

Es la guía #1 de la lista de diagramas de secuencia —*"Clean up the static model before proceeding to the CDR"*— y la fuente dice qué significa: *"tidying up the design, resolving real-world design issues, identifying useful design patterns that can be factored in to improve the design"*, con esta lista:

- Usar clases de **infraestructura y andamiaje**.
- Usar **patrones de diseño** donde mejoren el diseño.
- **Encajar el diseño con los frameworks** de la aplicación.
- **Completar las listas de parámetros** de las operaciones.

Y dos cautelas de la misma fuente: *"plan on finalizing your class model during detailed design"*, y sobre la presentación, *"try not to spend hours tinkering with the layout"* — el diagrama existe *"about showing a structural overview of the code you're about to write"*.

## Qué se dibuja y qué no

**Sin *getters* ni *setters*.** La fuente lo desaconseja explícitamente: *"Our advice is to avoid adding them to your model. For now, just add the attributes as private fields and utilize encapsulation."* La razón es práctica: se generan solos desde los atributos y solo producen un diagrama recargado. Fowler llega al mismo sitio desde otro lado: *"You should be very afraid of classes that are nothing but a collection of fields and their accessors."*

**Multiplicidades: útiles, no obligatorias.** Rosenberg matiza que para diagramas de clases son *"much less important—optional, even"* comparado con los modelos de datos relacionales, con una excepción que sí importa: **usarlas para indicar reglas de validación**. Agile ICONIX añade cuándo ponerlas — cuando ya hay evidencia, no antes: en su caso de estudio se añadieron solo tras tener un prototipo, porque *"we would have been guessing"*.

**Agregación y composición: distinguir aquí, no antes.** El método pide no discutir la diferencia mientras se construye el modelo de dominio (*"it's too early to worry about this distinction"*, guía #9 de la revisión de requisitos), lo que la difiere hasta esta etapa. La prueba que usa Agile ICONIX es de dependencia existencial: *"Building a HotelCluster without Hotels would be like building a brick house without bricks"* → composición. **Aviso de fuente encontrada:** Fowler discrepa de plano y recomienda **ignorar la agregación** — *"Aggregation is strictly meaningless; as a result, I recommend that you ignore it in your own diagrams"*. Esta skill sigue a ICONIX porque es el método del pipeline, **y declara la discrepancia** en `references/notation-rules.md` en vez de esconderla.

**Visibilidad.** Se marca, porque el modelo va camino del código. Fowler avisa de que *"their definitions vary subtly from those in other languages"* y de que conviene usar *"the rules of the language in which you are working"*.

**Métodos privados de bajo nivel: fuera.** Agile ICONIX los omite deliberadamente porque *"they may be a bit too low level to warrant showing on the class diagram"*, y advierte de que incluirlos ata el modelo al código *"too tightly"*.

**Detalle: el suficiente, no todo.** Fowler es tajante: *"comprehensiveness is the enemy of comprehensibility"*, y *"I don't show every operation on every class. I show only the important features"*. El diagrama *"acts as a graphical table of contents"*.

## Espacio del problema y espacio de la solución

Es la distinción que hace auditable este artefacto, y hay que sostenerla explícitamente:

- **Clases del problema** — vienen del modelo de dominio. Su nombre y su significado no cambian sin declararlo.
- **Clases de la solución** — nacen aquí o en las secuencias: andamiaje, infraestructura, *helpers*, clases que impone un framework. La fuente avisa de que aparecerán: *"don't be surprised if you start to see lots of new classes appear on the static model that were never there on the domain model"*.

**Cada clase de solución se declara como tal.** No es burocracia: es lo que permite al CDR y a cualquier revisor saber qué parte del modelo responde al problema y qué parte a la tecnología elegida. Y hay una razón de fondo, de la propia fuente: conviene *"base the key abstractions in the code on true statements about the problem domain, because the problem domain winds up being the most stable"*.

## Anti-patrones

Detalle en `references/anti-patterns.md`. Los que la fuente nombra por su cuenta:

- **Modelo de dominio anémico** — *"a design where the domain classes are all data and no behavior"*. Es el resultado de asignar todo el comportamiento a controladores y dejar las entidades como contenedores. La fuente cita a Fowler: *"so contrary to the basic idea of object-oriented design"*.
- **Enjambre de clases diminutas** — *"it's possible to 'overnormalize' the design and end up with hundreds of tiny classes flying around"*. El equilibrio está entre eso y las clases monolíticas de mil líneas.
- **Clase con personalidad esquizofrénica** — conjuntos de operaciones sin relación entre sí. Es la misma prueba de los *atributos discordantes* que usa la asignación de comportamiento.
- **Clase sin responsabilidades** — la fuente la llama *"rather impoverished"*. Una entidad que solo tiene atributos y ninguna operación es sospechosa.
- **Entidad sin atributos** — *"If you know that a class needs an attribute, add it to the class diagram! It's your last chance to do so before coding."*
- **Patronización prematura** — un patrón introducido porque suena bien, no porque el diseño lo pida. *"A SessionFactory is clearly part of the solution space, not the problem space."*

## Ciclo de auditoría interna

**No entregues sin haber pasado por él.** Se cierra cuando se cumplen **a la vez**: cero hallazgos **críticos** y cero **mayores**; como máximo **dos menores** documentados; **cada elemento con procedencia declarada**; **cada capa declarada** ejecutada o no ejecutada; y **dos pasadas consecutivas sin hallazgos nuevos** — una pasada limpia puede ser suerte, dos no.

**Tope duro: cinco pasadas.** Si al alcanzarlo persisten críticos o mayores, no declares éxito: entrega lo mejor disponible, marca el estado **`AUDITORÍA NO SUPERADA`**, enumera lo abierto y di qué insumo o decisión haría falta. Un fracaso declarado es más útil que un certificado optimista.

## Modos de trabajo

- **Ensamblar** (por defecto) — construir el modelo desde los insumos, con procedencia.
- **Revisar** — auditar un modelo existente sin reemplazarlo; hallazgos por severidad.
- **Refactorizar el modelo** — *model refactoring*: *"changing the design at the object modeling stage, prior to coding, without changing the functionality"*. Explica cada movimiento con su criterio.
- **Validar** — solo el script, interpretado con criterio.
- **Preparar el CDR** — emitir el paquete que la revisión crítica consumirá.
- **Trazar hacia adelante** — insumos estructurados para generación de código.

## Contrato de salida PlantUML

- Abre con `@startuml` y cierra con `@enduml`.
- `skinparam classAttributeIconSize 0`, `skinparam linetype ortho`, `skinparam shadowing false`.
- **No** `hide methods` — este modelo **sí** las lleva. Es lo que lo distingue del modelo de dominio.
- Atributos con visibilidad y tipo: `-nombre : String`. Operaciones con firma completa: `+registrar(placa : String) : Tiquete`.
- **Clases de la solución marcadas** con estereotipo `<<solucion>>`; las del problema van sin marca, porque son el caso por defecto.
- Relaciones con multiplicidad cuando aporte; composición con `*--`, agregación con `o--`, herencia con `<|--`.
- Nombre de archivo: `modelo_clases_diseno.puml`, identificado `MC-XX`.

## Entregables

1. **Modelo de clases de diseño** `MC-XX` en PlantUML.
2. **Matriz de procedencia** — elemento ↔ artefacto de origen ↔ localizador. Es lo que hace verificable la regla de esta skill.
3. **Delta de refactorización al modelo de dominio** — lo que el diseño descubrió y el conceptual debería incorporar, enrutado a `/uml-domain-modeler`.
4. **Informe de elementos sin procedencia** — con la instrucción de la fuente: volver a las secuencias, no inventar.
5. **Certificado de auditoría interna** con el estado final.
6. **Paquete para el CDR** — lo que la revisión crítica necesita.
7. **Insumos estructurados para código** — clase, atributos, operaciones con firma, capa. **Esta skill no genera código.**

## Enrutamiento de correcciones

| Hallazgo | Va a |
|---|---|
| Clase o atributo del dominio ausente o mal nombrado | `/uml-domain-modeler` |
| Operación sin mensaje que la origine; comportamiento mal asignado | `/uml-sequence-diagram` |
| Atributo sin respaldo en el texto; regla de negocio ausente | `/use-case-specifier` |
| Entidad que robustez descubrió y nadie devolvió | `/uml-robustness-diagram` |
| Incoherencia entre artefactos de entrada | `/iconix-pdr-review` |

**No reescribas los artefactos ajenos.** Redacta la corrección, agrúpala por destinatario, **pregunta cuáles aplicar** —con opción de todas— y aplica solo lo confirmado.

## Trazabilidad hacia adelante

Lo que sigue es el **Critical Design Review** (Milestone 3), cuya lista de comprobación este modelo debe poder satisfacer. Tres de sus diez guías apuntan directamente aquí: *"Review the classes on your class diagrams to make sure they all have an appropriate set of attributes and operations"*, *"Make sure all your attributes are typed correctly, and that return values and parameter lists on your operations are complete and correct"*, y *"Generate the code headers for your classes, and inspect them closely"*.

Y una técnica que conviene conocer porque funciona en sentido inverso: *"You can find most sequence diagram errors by looking at the class diagram"* — una operación en la clase equivocada delata una flecha mal dibujada en la secuencia.

## Recursos

- `references/static-model-guidelines.md` — la limpieza del modelo, la convergencia de los dos espacios y las guías del CDR que este artefacto debe satisfacer, con cita y localizador.
- `references/notation-rules.md` — atributos, operaciones, multiplicidad, visibilidad, agregación y composición, con las discrepancias entre fuentes declaradas.
- `references/provenance-rules.md` — qué traza a qué, cómo se declara y qué hacer con lo que no traza.
- `references/anti-patterns.md` — catálogo con síntoma, por qué importa y corrección.
- `references/sources-and-methods.md` — libros, normas e investigación, con el estado de verificación de cada cita.
- `references/regression-examples.md` — expectativas por dominio para comprobar que la skill generaliza.
- `scripts/validate_design_class_puml.py` — verificación mecánica multi-artefacto.
- `tests/examples/` — conjuntos de artefactos, coherentes e incoherentes a propósito.
