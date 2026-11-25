---
name: ia-workflow
description: >
  Crear, auditar y mantener una carpeta /ia como sistema de contexto estructurado para agentes LLM.
  Usar al inicializar proyectos nuevos, revisar que /ia cumple su contrato, reorganizar contexto,
  definir archivos 00-08, o separar tareas, progreso, ADRs, issues y retrospectivas.
---

# IA Workflow

## Propósito

Crear y validar una carpeta `/ia` portable para cualquier proyecto. La estructura convierte el conocimiento del proyecto en contexto navegable para agentes LLM sin obligarlos a leer todo en cada sesión.

El skill cubre dos escenarios:
* Inicializar `/ia` desde cero en un proyecto nuevo, junto con las plantillas, prompts y skills de workflow que lo operan.
* Auditar una carpeta `/ia` existente y proponer correcciones cuando no cumple el contrato.

Tambien puede guiar la evolucion de un MCP local para que funcione como orquestador de workflow: el usuario pide acciones de alto nivel en lenguaje natural y el MCP valida, enruta y documenta usando `/ia` como contrato.

## Contrato para instrucciones de asistentes con MCP

Cuando el proyecto habilita el MCP `iaWorkflow`, los archivos de instrucciones generados para GitHub Copilot, Claude y Codex deben declarar que el MCP es la interfaz operativa obligatoria de `/ia`:

* Para cualquier tarea, consulta, planificación, diagnóstico, revisión, implementación o cierre, empezar con `ia_validate` e `ia_get_context` según la intención.
* Para una tarea concreta, usar `work_task` antes de editar y `finish_task` al cerrarla; usar las demás acciones MCP para el ciclo de vida correspondiente.
* Usar `ia_inspect` únicamente para lecturas puntuales enrutadas por el contexto MCP o necesarias para el trabajo actual.
* No indicar que el LLM debe abrir directamente `ia/README.md` ni recorrer manualmente `/ia` para reconstruir contexto. El README permanece como documentación y punto de navegación humano.

La referencia [local-mcp-vscode.md](references/local-mcp-vscode.md) mantiene el catálogo vigente,
incluye `close_issue` para resolver issues, `delete_task` para eliminar tareas que ya no se van a
trabajar, y documenta `ia_inspect(action: "metrics")` como consulta opcional para métricas y forecast
por lote.

Si el proyecto no instala ni expone `iaWorkflow`, las instrucciones pueden usar `ia/README.md` como fallback explícito. No mezclar ambos contratos en un proyecto que sí tiene el MCP configurado.

## Política de idioma

Las referencias internas de este skill usan español como idioma de mantenimiento. Todo contenido
que el skill cree o normalice dentro de `/ia` debe usar el **idioma del proyecto**. Detectarlo
desde las instrucciones del repositorio, el README de `/ia` existente o la mayoría de los archivos
de contexto. Si se detecta contenido nuevo en otro idioma sin justificación, reportarlo como gap de
auditoría antes de ampliarlo.

## Cuándo usar

Usar este skill cuando:

* El usuario quiera crear una estructura `/ia` en un proyecto nuevo.
* El usuario pida revisar, auditar, compactar o normalizar `/ia`.
* Un README de `/ia` esté creciendo demasiado y haya que separar schemas, tasks, progress o history.
* Se necesite definir archivos `00_context.md` a `08_retrospective.md`.
* Se necesite convertir conocimiento suelto en contexto operativo para agentes.

No usar este skill cuando:

* La tarea sea implementar código dentro de una TASK ya existente. Usa el skill del área técnica correspondiente.
* Solo se vaya a crear, actualizar o archivar una TASK. Usa el skill de gestión de tareas del proyecto, si existe.
* Solo se cierre una sesión de trabajo. Usa el skill de cierre de sesión del proyecto, si existe.

## Estructura objetivo

```text
ia/
├── README.md
├── SCHEMAS.md
├── 00_context.md
├── 01_requirements.md          ← índice cuando el contenido crece por feature/área
├── 01_requirements/            ← opcional: detalle por feature/área (≥ 24 K chars)
│   └── {feature-o-area}.md
├── 02_architecture.md          ← índice cuando el dominio crece
├── 02_architecture/            ← opcional: detalle por dominio (≥ 24 K chars)
│   └── {dominio}.md
├── 03_plan.md
├── 03_plan/                    ← opcional: historial de fases completadas
│   └── historial.md
├── 04_tasks.md
├── 04_tasks/
│   ├── current.md
│   ├── backlog.md
│   ├── blocked.md
│   ├── tasks/
│   └── done/
├── 05_progress.md
├── 05_progress/
│   ├── current.md
│   ├── by-component/
│   └── archive/
├── 06_decisions.md
├── 06_decisions/
│   ├── ADR-01-example-decision.md
│   ├── ADR-02-example-decision.md
│   └── ADR-03-example-decision.md
├── 07_issues.md
├── 07_issues/
│   ├── current.md
│   ├── open/
│   └── archive/
├── 08_retrospective.md
├── assets/                     ← opcional: imágenes y material de referencia
├── templates/
│   ├── task-template.md
│   ├── adr-template.md
│   ├── issue-template.md
│   └── skill-template.md
└── prompts/
```

Adaptar los nombres de carpetas solo cuando el proyecto tenga una razón sólida. Mantener estables los números de archivo del `00` al `08` porque los agentes los usan como anclajes de navegación.

## Referencias de componentes

Usar estos archivos de referencia como material fuente al crear o auditar cada componente:

| Componente | Referencia |
|-----------|----------|
| `README.md` | [references/readme.md](references/readme.md) |
| `SCHEMAS.md` | [references/schemas.md](references/schemas.md) |
| `00_context.md` | [references/00-context.md](references/00-context.md) |
| `01_requirements.md` y `01_requirements/` | [references/01-requirements.md](references/01-requirements.md) |
| `02_architecture.md` y `02_architecture/` | [references/02-architecture.md](references/02-architecture.md) |
| `03_plan.md` y `03_plan/` | [references/03-plan.md](references/03-plan.md) |
| `04_tasks.md` y `04_tasks/` | [references/04-tasks.md](references/04-tasks.md) |
| `05_progress.md` y `05_progress/` | [references/05-progress.md](references/05-progress.md) |
| `06_decisions.md` y `06_decisions/` | [references/06-decisions.md](references/06-decisions.md) |
| `07_issues.md` y `07_issues/` | [references/07-issues.md](references/07-issues.md) |
| `08_retrospective.md` | [references/08-retrospective.md](references/08-retrospective.md) |

## Assets de workflow

La carpeta `/ia` es operada por tres skills de workflow más templates y prompts compartidos. Usar estas referencias al crearlos o auditarlos en un proyecto nuevo:

| Asset | Referencia |
|-------|----------|
| Skill de gestión de tareas | [references/skill-task-management.md](references/skill-task-management.md) |
| Skill de revisión de código | [references/skill-code-review.md](references/skill-code-review.md) |
| Skill de cierre de sesión | [references/skill-session-closeout.md](references/skill-session-closeout.md) |
| `templates/` | [references/templates.md](references/templates.md) |
| `prompts/` | [references/prompts.md](references/prompts.md) |
| Archivos de instrucciones de asistentes | [references/assistant-instructions.md](references/assistant-instructions.md) |
| MCP local para VS Code/Codex | [references/local-mcp-vscode.md](references/local-mcp-vscode.md) |

## Flujo de trabajo delegado

Cuando `/ia` es operado a través de MCP, exponer primero las acciones públicas y tratar las tools
de bajo nivel como bloques internos. El contrato de acciones públicas vive en
[references/local-mcp-vscode.md](references/local-mcp-vscode.md); el ciclo de vida, los estados,
el riesgo y la aprobación de tareas tienen una única fuente en
[references/04-tasks.md](references/04-tasks.md).

Las tareas que esperan información externa deben pasar a `Bloqueada` mediante `work_task` con
`transition: "blocked"` y `reason`. Para continuar, usar `transition: "resumed"`. El historial V2
conserva el primer `startedAt`; `cycleTimeMs`, `blockedTimeMs` y `activeTimeMs` se calculan por
separado a partir de los eventos.

### Evolución de transiciones MCP

Si el ciclo de vida requiere una transición legítima que el MCP no expone, crear o ampliar una tool
MCP específica antes de alterar la tarea. La tool debe validar los estados de origen, requerir el
motivo cuando sea relevante, generar preview por defecto, aplicar solo con `apply: true`, conservar
un evento V2 auditable y sincronizar todos los índices afectados. No editar manualmente `/ia` ni
usar `duplicate_task`, cierre o archivado como workaround para simular una transición.

Después de cambiar un skill canónico bajo `.agents/skills/`, ejecutar el skill `sync-agent-skills`:
primero su dry-run y luego `scripts/sync-skills.ps1 -Apply -AutoBase` para actualizar `.claude` y
`.codex` desde la base canónica.

### Secciones vacías de tareas

`04_tasks/current.md` es consumido por las transiciones públicas `approve_task`, `work_task` y
`finish_task`. Para que una sección vacía sea estable y legible, usar siempre este formato
canónico con una sola línea en blanco antes del marcador:

```markdown
## En progreso

Sin tareas registradas.
```

Aplicar el mismo marcador a `Lista` y `Bloqueadas` cuando no tengan entradas.
`Borradores` conserva su tabla aunque no tenga filas. Nunca representar una sección operativa
vacía solo mediante una cantidad variable de saltos de línea.

Al implementar el MCP, el helper que inserta entradas en una sección, como
`replaceEmptySection`, debe aceptar tanto el marcador canónico como una sección compuesta solo
por espacios o saltos de línea. Después de retirar la última entrada, debe restaurar el marcador
canónico. Así las transiciones no dependen de un formato frágil ni fallan con "No se encontró la
sección".

## Procedimiento: inicializar /ia

1. Leer el README del proyecto, los archivos de build/paquetes, los nombres de carpetas de código fuente y la documentación existente.
2. Identificar el propósito del proyecto, stack, límites, componentes activos, flujos de trabajo conocidos y comandos de validación.
3. Crear la estructura objetivo si no existe.
4. Crear un `ia/README.md` conciso como punto de entrada usando [references/readme.md](references/readme.md). Debe enrutar agentes, no duplicar cada esquema.
5. Crear `ia/SCHEMAS.md` para templates completos y reglas de reconstrucción usando [references/schemas.md](references/schemas.md).
6. Crear `00_context.md` hasta `08_retrospective.md` usando las referencias de componentes anteriores. Escribir todo el contenido generado en el idioma del proyecto. Si el volumen de requisitos de negocio supera 24 000 chars desde el inicio, crear directamente `01_requirements/` como carpeta de detalle y dejar `01_requirements.md` como índice compacto con tabla de enlaces a `{feature-o-area}.md`. Si el plan de fases contiene fases ya completadas que superan los 20 000 chars totales de `03_plan.md`, archivar las fases completadas en `03_plan/historial.md` desde el principio.
7. Crear `04_tasks/current.md`, `04_tasks/backlog.md`, `04_tasks/blocked.md`, `05_progress/current.md`, `07_issues/current.md` y `07_issues/open/` incluso cuando empiecen mayormente vacíos. Inicializar las secciones operativas vacías de `current.md` con `Sin tareas registradas.` conforme a [references/04-tasks.md](references/04-tasks.md).
8. Agregar templates bajo `ia/templates/` para tareas, ADRs, issues y skills usando [references/templates.md](references/templates.md).
9. Agregar prompts reutilizables para los momentos del workflow usando [references/prompts.md](references/prompts.md).
10. Crear los tres skills de workflow que operan `/ia` usando [references/skill-task-management.md](references/skill-task-management.md), [references/skill-code-review.md](references/skill-code-review.md) y [references/skill-session-closeout.md](references/skill-session-closeout.md).
11. Crear o actualizar los archivos de instrucciones de asistentes para GitHub Copilot, Claude y Codex usando [references/assistant-instructions.md](references/assistant-instructions.md). Si `iaWorkflow` está habilitado, generar obligatoriamente el contrato MCP de contexto y tareas; no indicar lectura directa de `ia/README.md`.
12. Si el proyecto quiere que clientes LLM locales operen `/ia` a través de MCP, agregar el servidor opcional `.mcp/ia-workflow` y ejemplos para VS Code/Codex usando [references/local-mcp-vscode.md](references/local-mcp-vscode.md). Al implementar `validateIa`, incluir obligatoriamente checks de tamaño para los cuatro archivos de contexto: `00_context.md` (> 20 000 chars), `01_requirements.md` (> 24 000 chars), `02_architecture.md` (> 24 000 chars) y `03_plan.md` (> 20 000 chars); cada warning debe indicar el conteo actual y la acción correctiva específica. Todo parámetro con `type: "array"` debe publicar `items` con el schema de sus elementos. Para una tool con variantes mutuamente excluyentes, publicar un schema `oneOf` discriminado por una propiedad con `const` (por ejemplo, `action` u `outcome`); el validador debe resolver el discriminante de forma genérica antes de validar propiedades, obligatorios y enumeraciones. La lectura de una tarea por ID debe resolver primero `04_tasks/tasks/{id}.md` y, si no existe, buscar secciones exactas en todos los archivos de `04_tasks/done/` desde el mes más reciente al más antiguo; la respuesta histórica debe marcar `archived: true` e informar la ruta mensual de origen. El smoke test debe partir de `En progreso` y `Lista` vacías, validar el ciclo `create_task` -> `approve_task` -> `work_task` y verificar que el helper de secciones acepta tanto el marcador canónico como contenido vacío heredado.
13. Mantener los hechos específicos del proyecto en los archivos de componentes y skills del proyecto, no en este skill.
14. Si los flujos de trabajo delegados están habilitados, aplicar el ciclo de vida de tareas de [references/04-tasks.md](references/04-tasks.md).

## Procedimiento: auditar /ia

1. Verificar que `ia/README.md` sigue [references/readme.md](references/readme.md), se mantiene pequeño y funciona como enrutador.
2. Verificar que los esquemas largos viven en `ia/SCHEMAS.md`, siguen [references/schemas.md](references/schemas.md), y no están duplicados en el README.
3. Confirmar que cada archivo del `00` al `08` existe y tiene un límite de propiedad claro.
4. Confirmar que el trabajo activo vive en `04_tasks/current.md` y archivos individuales de tarea, no solo en notas de prosa.
5. Confirmar que el ciclo de vida de tareas cumple [references/04-tasks.md](references/04-tasks.md).
6. Confirmar que las secciones operativas vacías de `04_tasks/current.md` usan `Sin tareas registradas.` y que el MCP tolera secciones heredadas vacías al aprobar, iniciar, revisar o completar una tarea. Reportar como gap importante cualquier transición que dependa de una cantidad específica de saltos de línea.
7. Confirmar que el header de `04_tasks/current.md` no acumula más de 5 líneas `> **Completado`. Si hay más, reportarlo como gap de limpieza (la corrección es agregar `trimCompletedHeaderLines` al MCP — ver `references/local-mcp-vscode.md`). Si contiene un segundo encabezado `# 04 —` o una tabla `## Cola activa` junto a las secciones operativas nuevas, reportarlo como gap importante y ejecutar la limpieza descrita en la misma referencia.
7. Confirmar que decisiones, issues y progreso usan archivos separados y no se duplican entre sí.
8. Confirmar que `06_decisions.md` es solo un índice y que cada detalle de ADR vive en un solo archivo bajo `06_decisions/{ADR-ID}-{slug}.md`, no agrupado en archivos por dominio.
8. Verificar que los archivos de contexto principales no superan sus umbrales de tamaño (aplicados automáticamente por `ia_validate` cuando el MCP está instalado):
   - `00_context.md` > 20 000 chars: mover secciones históricas o estables a archivos de soporte; conservar solo constantes del proyecto.
   - `01_requirements.md` > 24 000 chars: dividir por feature/área en `01_requirements/{feature-o-area}.md` y dejar `01_requirements.md` como índice con tabla de enlaces.
   - `02_architecture.md` > 24 000 chars: separar el detalle por dominio en `02_architecture/{dominio}.md`; el archivo raíz debe funcionar como índice compacto con enlaces y contratos esenciales.
   - `03_plan.md` > 20 000 chars: archivar fases completadas en `03_plan/historial.md` y conservar solo las fases activas o próximas.
   Reportar cada archivo que supera su umbral como gap de limpieza.
10. Confirmar que el contenido de `/ia` usa el idioma del proyecto de forma consistente. Marcar el contenido nuevo en otro idioma como un gap importante, salvo que sea un identificador externo literal, símbolo de código o fuente citada.
11. Confirmar que los skills o procedimientos reutilizables están referenciados por propósito, no copiados en `/ia`.
12. Confirmar que `ia/templates/` cubre tareas, ADRs, issues y skills, siguiendo [references/templates.md](references/templates.md).
13. Confirmar que cada momento del workflow tiene un prompt, siguiendo [references/prompts.md](references/prompts.md).
14. Confirmar que los skills de gestión de tareas, revisión de código y cierre de sesión existen y coinciden con sus referencias.
15. Confirmar que los archivos de instrucciones de GitHub Copilot, Claude y Codex existen o están intencionalmente ausentes, siguiendo [references/assistant-instructions.md](references/assistant-instructions.md). Si existe `iaWorkflow`, marcar como gap importante cualquier instrucción que mande a leer directamente `ia/README.md` o recorrer `/ia` en lugar de usar el MCP.
16. Si existe un MCP local para `/ia`, auditarlo con [references/local-mcp-vscode.md](references/local-mcp-vscode.md) y el skill `mcp-vscode`.
17. Si existe un MCP local para `/ia` y el proyecto quiere que usuarios no técnicos deleguen el desarrollo, confirmar que expone acciones de workflow de alto nivel (`create_task`, `approve_task`, `work_task`, `finish_task`) o prompts equivalentes, y que las tools de bajo nivel están documentadas como bloques internos de construcción.
18. Reportar los gaps como correcciones accionables agrupadas por severidad: bloqueante, importante, limpieza.

### Checklist de auditoría

* [ ] El README, esquemas, componentes `00` a `08` y carpetas operativas existen y respetan sus límites.
* [ ] Las tareas, ADRs, issues y progreso viven en sus ubicaciones canónicas.
* [ ] El ciclo de vida de tareas cumple `references/04-tasks.md`.
* [ ] Las secciones vacías de tareas usan el marcador canónico y las transiciones MCP toleran contenido vacío heredado.
* [ ] El contenido nuevo de `/ia` usa el idioma del proyecto.
* [ ] Los templates, prompts y skills de workflow requeridos existen y están enlazados.
* [ ] Las instrucciones de asistentes usan el contrato MCP cuando `iaWorkflow` está disponible.
* [ ] El MCP local, si existe, cumple `references/local-mcp-vscode.md` y pasa su smoke test.
* [ ] Cada parámetro MCP de tipo `array` declara `items`, y cada variante `oneOf` se selecciona por su discriminante `const` sin acoplarse a un nombre de propiedad.
* [ ] Los gaps están agrupados en bloqueantes, importantes y de limpieza.

## Límites de contenido

* `README.md` enruta a los agentes al archivo correcto. Mantenerlo conciso.
* `SCHEMAS.md` almacena esquemas completos de archivos y templates de reconstrucción.
* `00_context.md` almacena identidad estable, stack y constantes críticas. Mantenerlo bajo 20 000 chars; cuando supera ese umbral, mover secciones históricas o estables a archivos de soporte y conservar solo las constantes del proyecto.
* `01_requirements.md` almacena comportamiento del negocio e invariantes. Cuando supera 24 000 chars, dividir por feature/área en `01_requirements/` y dejar este archivo como índice.
* `02_architecture.md` almacena flujo técnico y contratos de componentes. Cuando el archivo supera 24 000 caracteres, separar el detalle por dominio en `02_architecture/{dominio}.md` y convertir el archivo raíz en índice compacto con enlaces y contratos esenciales (mismo patrón que `06_decisions.md` → `06_decisions/`).
* `03_plan.md` almacena la dirección a nivel de fases. Sus filas de componentes se actualizan automáticamente cuando `finish_task` cierra tareas que aparecen en el plan. Cuando supera 20 000 chars, archivar fases completadas en `03_plan/` y conservar solo las fases activas o próximas.
* `04_tasks/` almacena trabajo accionable.
* Los archivos de tarea son el contrato entre humano y agente; poseen objetivo, alcance, exclusiones, criterios de aceptación, riesgo, plan, validación y rollback.
* `05_progress/` almacena estado actual e histórico.
* `06_decisions.md` almacena solo el índice de ADRs.
* `06_decisions/` almacena un archivo por ADR y el historial arquitectónico.
* `07_issues/` almacena bugs y limitaciones conocidas.
* `08_retrospective.md` almacena aprendizajes de fases completadas.

## Reglas de seguridad

* No incluir secretos, tokens, cadenas de conexión, contraseñas ni claves privadas.
* No inventar hechos arquitectónicos. Marcar los desconocidos como pendientes de confirmación.
* No mover contenido histórico de forma destructiva. Archivar o resumir primero.
* No convertir `/ia/README.md` en un repositorio de conocimiento. Es el punto de entrada.
* No almacenar reglas de implementación específicas del proyecto dentro de este skill. Crear un skill de proyecto en su lugar.
* No crear contenido nuevo de `/ia` en un idioma que contradiga el idioma del proyecto.
* No implementar tareas `Borrador`. Pedir aprobación o mover a `Lista` solo cuando los campos requeridos estén completos.
* No implementar tareas de riesgo alto sin aprobación explícita del usuario.

## Salida esperada

Al inicializar:

* Una carpeta `/ia` completa con punto de entrada, esquemas, archivos de componentes, carpetas operativas y templates.
* Marcadores claros donde el proyecto aún no tiene información suficiente.

Al auditar:

* Un reporte que lista archivos faltantes, contenido mal ubicado, secciones demasiado grandes, referencias desactualizadas y movimientos recomendados.
* Parches opcionales que normalizan la estructura preservando el conocimiento existente del proyecto.
