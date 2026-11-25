---
name: metodologias-de-aprendizaje
description: Diseña o revisa aplicaciones educativas conectando objetivos de aprendizaje, necesidades del alumnado, actividades, retroalimentación y evidencias de aprendizaje. Úsalo para nuevas herramientas educativas o cambios sustanciales en su diseño didáctico. No lo apliques a cambios estéticos ni a correcciones habituales de errores sin un problema de diseño del aprendizaje.
metadata:
  version: "1.6.0"
  language: "es"
  based_on: "learning-methodologies@1.6.0"
  license: "MIT"
  repo: "https://github.com/siberius/learning-methodologies"
  author: "Luděk Sušický"
  format: "paquete nativo con Markdown independiente generado"
---

# Metodologías de aprendizaje

Ayuda a diseñar, implementar o revisar aplicaciones educativas cuyas actividades, apoyos y evaluación respondan a las necesidades del alumnado destinatario. Ajusta la profundidad del trabajo a la petición, sus consecuencias y la incertidumbre. Una actividad breve de aula no necesita un estudio completo de evaluación ni un nuevo documento de planificación.

## Métodos didácticos para aplicaciones creadas con IA

Utiliza los métodos para traducir objetivos educativos en acciones del estudiante, reglas de retroalimentación y evidencias en la aplicación generada. La recuperación requiere un intento antes de revelar la respuesta; el andamiaje requiere ayuda accesible y distinguir desempeño con apoyo e independiente. La IA ayuda a implementar estas decisiones; el resultado necesita revisión disciplinar y didáctica. Se aplica a aplicaciones sin conexión y al uso justificado de IA durante el aprendizaje.

Consulta la [justificación didáctica](references/didactic-rationale.md) al explicar la elección de un método o su implementación. Vincula métodos con decisiones de producto y evidencias necesarias.

## Acompaña las decisiones del creador

En cada decisión didáctica sustancial, revisa objetivo, acción del estudiante, evidencia, apoyo y restricciones. Reutiliza las elecciones anteriores. Ante una elección importante pendiente, ofrece pocas opciones pertinentes, normalmente dos o tres, con una descripción sencilla y un ejemplo en este proyecto. Recomienda una, explica su principal contrapartida y pregunta qué enfoque prefiere el creador. Lee el [diálogo de diseño](references/design-dialogue.md) al iniciar o reabrir esa elección. Esta conversación es distinta del diálogo del tutor con el estudiante.

No reabras decisiones resueltas o rechazadas sin un cambio pertinente. Respeta la delegación explícita de decisiones habituales y continúa con una justificación breve. El silencio no autoriza ampliar el alcance. Mientras esperas, avanza en partes independientes. Un cambio cosmético no activa este proceso.

Consulta según la necesidad: [métodos](references/methods.md) para actividades y apoyo; [juegos](references/learning-games.md) para motivación y mecánicas; [evaluación](references/assessment.md) para evidencias y puntuación; [interfaz cognitiva](references/cognitive-ux.md) para representaciones, multimedia y atención; [práctica adaptativa](references/adaptive-practice.md) para sesiones repetidas o dificultad. Mantén las rutas condicionales siguientes para simulaciones, estado del tutor e IA en ejecución. Lee el método pertinente antes de ofrecerlo; no cargues todas las referencias.

Convierte la elección en comportamiento observable del producto y una comprobación significativa. Distingue ofrecido, elegido, implementado y verificado. La verificación técnica no demuestra eficacia educativa.

## Ruta de trabajo

Sigue esta ruta con la profundidad necesaria: establecer el objetivo y las restricciones → elegir un método para el obstáculo de aprendizaje → conectar la actividad del estudiante con la evidencia → implementar dentro del alcance → comprobar el resultado. En una revisión, examina el diseño existente en lugar de implementarlo. Reutiliza el contexto conocido; no exijas un documento de planificación para cada paso.

Consulta los [ejemplos de decisión](references/decision-examples.md) cuando necesites aclarar la ayuda, las respuestas alternativas o una alineación curricular incierta. Ilustran decisiones; no son guiones que deban copiarse en todas las lecciones.

## Establece el contexto de aprendizaje

Utiliza la información ya presente en la petición, el proyecto y los materiales aportados. Para completar el contexto, pregunta solo por información ausente que cambie sustancialmente el diseño. Ante incertidumbres menores, declara una suposición razonable y continúa. Evita los cuestionarios fijos y las solicitudes repetidas de aprobación para decisiones ordinarias ya cubiertas por la petición.

Identifica el contexto pertinente: alumnado y conocimientos previos, materia, resultados previstos, uso en el aula o autónomo, tiempo y dispositivos disponibles, idioma, necesidades de accesibilidad y cualquier currículo aportado. Sigue un currículo cuando corresponda al entorno; no presupongas un marco nacional. Elige el tono según el contexto y las preferencias del autor. No deduzcas la atención, motivación, capacidad o pedagogía preferida a partir de etiquetas generacionales.

Incluye la actividad docente que rodea a la aplicación cuando resulte útil: preparación, trabajo individual o grupal, intervención docente, discusión y seguimiento. Una demostración dirigida por el docente puede necesitar una buena pregunta para debatir en lugar de cuentas y puntuaciones individuales.

Separa edad, papel educativo y experiencia en el tema; niño, alumno, estudiante y participante adulto no son categorías intercambiables ni niveles de capacidad. Al definir o cambiar el público, lee su perfil en el [diálogo de diseño](references/design-dialogue.md). Adapta denominación y apoyo al entorno; usa términos neutros en orientaciones generales. Creador, persona que aprende y docente o familiar acompañante pueden ser personas distintas.

## Conecta los objetivos con actividades observables

Para cada objetivo importante, relaciona la acción del estudiante, la evidencia, los criterios de logro, las condiciones de ayuda y la siguiente decisión didáctica. En tareas pequeñas, hazlo de forma concisa. En una indagación abierta, la evidencia puede referirse a la calidad de las preguntas, el uso de pruebas o la revisión de una explicación, sin una única respuesta predeterminada.

Ejemplo: el estudiante predice cómo cambia la corriente al variar la resistencia, lo comprueba con un modelo, explica las discrepancias y resuelve de forma autónoma un caso nuevo. Mover un control deslizante o completar una pantalla no demuestra por sí solo comprensión.

Elige una intervención adecuada a partir del obstáculo de aprendizaje observado. Trata la explicación de un error como hipótesis provisional, no como diagnóstico. Selecciona un conjunto reducido y coherente de métodos; no añadas funciones solo porque figuren en el catálogo. Consulta los [métodos](references/methods.md) al seleccionar o implementar un método, una secuencia de apoyo o una regla de progresión.

Para mecánicas, motivación o revisión de juegos educativos, consulta [juegos educativos y gamificación con propósito](references/learning-games.md). Incluye secuencias jugables, selección de mecánicas, límites de evidencia e implementación desde herramientas pequeñas hasta productos longitudinales. Adapta a primaria, secundaria, universidad y adultos de distintos países según conocimientos previos y contexto local.

La referencia de métodos abarca explícitamente el aprendizaje socrático, la técnica de Feynman, la zona de desarrollo próximo y el andamiaje, los ejemplos resueltos, la práctica de recuperación y espaciada, el aprendizaje a partir del error, la metacognición, la indagación, el juego de roles, el aprendizaje entre iguales y cooperativo, los proyectos, la enseñanza invertida y la gamificación opcional. Son enfoques seleccionables, no funciones obligatorias de todas las aplicaciones.

La taxonomía de Bloom describe objetivos cognitivos y tipos de conocimiento. Mantén separadas la dificultad y los prerrequisitos; no impongas seis niveles bloqueados. Para resultados prácticos, interpersonales o de otro tipo, elige evidencias adecuadas y reconoce qué no puede demostrar una tarea en pantalla.

## Elige una realización proporcionada

Distingue la IA utilizada para construir la aplicación de la IA utilizada por el alumnado en el producto terminado. Elige entre contenido estático revisado, interacciones o simulaciones deterministas e IA durante el uso según el objetivo y las condiciones de funcionamiento. Las pistas, la retroalimentación y la práctica espaciada pueden funcionar sin un servicio de IA.

Antes de añadir una función importante, considera su aportación al aprendizaje, la carga de interacción, el trabajo docente, el mantenimiento, los datos necesarios y el coste de funcionamiento. Explica las compensaciones relevantes. No añadas cuentas, analítica, paneles, un backend, servicios de pago ni flujos de datos externos solo para que el producto parezca completo. Confirma las decisiones que cambien el alcance cuando no estén ya autorizadas.

Consulta las [simulaciones](references/simulations.md) al modelar un sistema, realizar un experimento o diseñar un juego de roles. Distingue claramente las observaciones reales, los cálculos del modelo y las reconstrucciones ficticias. Nunca presentes resultados inventados por la IA como mediciones ni finjas que se ha realizado un experimento.

Consulta la [IA durante el uso](references/runtime-ai.md) solo cuando el producto terminado llame a un servicio de IA. Define la función docente, los límites de las fuentes, la supervisión humana, los flujos de datos, los límites de coste y el comportamiento ante fallos. Un prompt no sustituye la seguridad de la aplicación.

Consulta los [modos del tutor y la continuidad](references/tutor-state.md) al implementar una tutoría de varios pasos, transiciones entre práctica y evaluación o la reanudación del aprendizaje. Conserva el estado y las evidencias en la aplicación; estas funciones no necesitan IA durante el uso.

## Haz fiables la retroalimentación y las decisiones

Proporciona un siguiente paso útil después de un error. En la práctica, permite pedir ayuda y acceder a una explicación directa o una solución comentada cuando sea necesario; evita las preguntas interminables. Reduce el apoyo según el desempeño autónomo y mantén disponible la ayuda solicitada. Una evaluación puede limitar la ayuda bajo condiciones explícitas.

Distingue el éxito autónomo, el éxito con apoyo, la exposición a la respuesta y la incertidumbre. Un acierto por azar, una declaración de confianza o dos aciertos con apoyo no demuestran automáticamente dominio. No deduzcas una capacidad estable, motivación o trastorno a partir de una interacción breve.

Consulta la [evaluación](references/assessment.md) al diseñar tareas puntuadas, rúbricas, adaptación o evaluación del aprendizaje. Comprueba la corrección disciplinar, las alternativas plausibles, las unidades y tolerancias numéricas y si la tarea exige realmente el desempeño previsto. Conserva las explicaciones y los métodos alternativos válidos. Separa las recompensas del juego y la velocidad del logro, salvo que respondan a un objetivo explícito.

## Preserva el acceso y la capacidad de intervención docente

Diseña atendiendo a los criterios pertinentes de WCAG 2.2 AA y a las necesidades reales del alumnado. Comprueba el uso con teclado, el foco visible, las etiquetas y la retroalimentación comprensibles, las alternativas al uso exclusivo de color o sonido y la justificación o ajuste de los tiempos. Elige formas adecuadas de percibir la información y expresar la comprensión; no asignes estilos de aprendizaje fijos. Solicita ayuda especializada en accesibilidad cuando la implementación lo justifique.

Recoge solo los datos necesarios para la actividad e identifica quién los ve, adónde van y cómo se conservan. Cuando corresponda, comprueba los requisitos del proveedor, del centro y del ámbito local para el despliegue concreto; no inventes normas jurídicas universales. Una actividad local anónima no necesita incorporar cuentas ni seguimiento persistente.

Proporciona una forma proporcionada para que el docente o autor responsable revise el contenido, corrija los juicios e intervenga ante una adaptación inadecuada. Puede bastar un archivo de contenido editable en lugar de un sistema de gestión. Las decisiones importantes de calificación o asignación de nivel necesitan revisión humana con responsabilidad definida.

## Coordina los conocimientos especializados sin ampliar innecesariamente el proceso

Utiliza estas perspectivas según las necesidades; un solo agente puede cubrirlas en una tarea pequeña:

- Metodólogo: resultados previstos, contexto docente y decisiones didácticas.
- Especialista en didáctica de la materia: precisión del contenido, prerrequisitos, ejemplos y concepciones erróneas.
- Diseñador de evaluación: evidencias, criterios, alternativas y límites de inferencia.
- Diseñador de interacción: recorrido del estudiante, ayuda, accesibilidad y uso en el aula.
- Desarrollador: contratos de datos, cálculos, estado, persistencia y comportamiento ante fallos.
- Revisor: discrepancias entre el objetivo, el diseño y el comportamiento observado.

Lleva sus decisiones a la implementación. No califiques una elección técnica conveniente como pedagógicamente correcta sin evidencia. Resuelve los desacuerdos relevantes comprobando fuentes, mediante una comprobación específica o dejando explícita una cuestión pendiente. Usa revisión independiente cuando lo justifiquen la complejidad o las consecuencias; no formes un equipo para cada tarea. Invoca otros skills solo para trabajos pertinentes y cuando estén disponibles.

## Verifica e informa con la profundidad adecuada

En la implementación, comprueba el recorrido afectado del estudiante, los errores significativos, la ayuda y los estados de fallo pertinentes. En peticiones exclusivamente analíticas, informa de hallazgos y propuestas sin modificar el producto. Adapta las comprobaciones a la aplicación: una simulación necesita comprobaciones del modelo; la IA durante el uso requiere comprobar los fallos del servicio y el tratamiento de sus salidas; una actividad estática sencilla no necesita ninguna de estas dependencias por defecto.

Mantén separadas tres conclusiones: corrección funcional, adecuación didáctica y resultados de aprendizaje observados. Las comprobaciones técnicas por sí solas no demuestran eficacia educativa. Un pequeño piloto puede revelar problemas sin demostrar un beneficio causal. Informa de las comprobaciones realizadas y las suposiciones pendientes; no inventes observaciones del alumnado ni resultados de eficacia.

En la entrega, resume el objetivo de aprendizaje, el enfoque elegido, las suposiciones de funcionamiento importantes, las comprobaciones completadas y los límites restantes. Incluye una tabla de objetivos y evidencias solo cuando facilite utilizar el resultado. Ajusta el formato a la petición del usuario.

## Integración

Al elegir un modelo, el esfuerzo de razonamiento o la velocidad, o al adaptar el mecanismo de carga, consulta los [perfiles de modelos y entornos](references/model-profiles.md). Incluyen orientación basada en documentación para OpenAI, Claude y Gemini. Mantén un contrato educativo común e informa de las pruebas realizadas por separado de la compatibilidad prevista. No cargues este perfil para una tarea didáctica ordinaria que no lo necesite.

Adecuado para juegos educativos, cuestionarios, tutoriales, simulaciones, formación y revisiones de su diseño didáctico. El núcleo no requiere paquetes, API, un modelo de IA concreto ni datos del alumnado. Las referencias son condicionales. El paquete nativo utiliza este archivo y sus referencias; `metodologias-de-aprendizaje.md` es la edición independiente generada. La instalación, el despliegue y otros cambios externos requieren autorización para dichas acciones. Este skill no sustituye las instrucciones del proyecto ni autoriza ampliar el alcance.

Referencias de diseño: [WCAG 2.2](https://www.w3.org/TR/WCAG22/), [pautas DUA de CAST](https://udlguidelines.cast.org/). Orientan el diseño y la revisión; citarlas no certifica conformidad ni eficacia educativa.
