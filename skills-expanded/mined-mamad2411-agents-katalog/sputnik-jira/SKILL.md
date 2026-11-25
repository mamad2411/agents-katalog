---
name: sputnik-jira
description: Sube una tabla de cotización del equipo Sputnik a Jira como issues, usando los conectores de Atlassian disponibles. Toma como entrada una tabla con columnas Capa / Nombre Proyecto / Req. / Nombre Actividad / Estructura Descriptiva / Puntos / Justificación (generada por sputnik-core) y crea un issue por cada fila respetando proyecto destino, tipo de issue y campo de puntos (story points). Soporta agrupación en épicas, vinculación entre capas y detección de duplicados. Úsala cuando tras una estimación con sputnik-core el usuario diga "sube los issues a Jira", "crea los tickets", "pasa la estimación a Jira", o "carga la cotización a Jira". Pregunta siempre proyecto destino y confirma antes de crear masivamente.
disable-model-invocation: true
---

# Sputnik Jira — Issues desde estimación

Convierte una tabla de cotización Sputnik en issues de Jira usando las herramientas de Atlassian disponibles (típicamente vía Atlassian Rovo MCP). La tabla es generada por `sputnik-core`.

## Input esperado

Una tabla (en chat, pegada por el usuario, o generada por la skill `sputnik-core`) con estas columnas:

| Capa | Nombre Proyecto | Req. | Nombre Actividad | Estructura Descriptiva | Puntos | Justificación |

Las filas de SUBTOTAL y TOTAL GENERAL se ignoran al crear issues.

## Workflow

### Paso 1: Validar herramientas disponibles

Confirma que tienes acceso a las herramientas de Jira: `search_jira_issues`, `get_visible_jira_projects`, `get_jira_issue`, `get_jira_issue_type_fields`. Si no están disponibles, dile al usuario que instale la extensión Atlassian MCP (`~/.pi/agent/extensions/atlassian-mcp/`) y configure las variables de entorno `ATLASSIAN_BASE_URL`, `ATLASSIAN_USERNAME`, `ATLASSIAN_API_TOKEN`.

### Paso 2: Resolver destino (en orden)

Pregunta al usuario lo siguiente (en un solo mensaje, no uno por uno):

1. **Cloud ID o URL del site de Jira** — si no lo sabe, usa la herramienta `getAccessibleAtlassianResources` para listar los sites disponibles y déjalo elegir.
2. **Project key** destino (ej. `SPK`, `ITSEG`) — si no lo sabe, usa `get_visible_jira_projects` para listar.
3. **Tipo de issue** (default: `Task`). Pregunta si prefieren `Story` o algún tipo custom.
4. **Campo para los puntos**: por default `customfield_10016` (Story Points en muchas instancias). Si el usuario sabe el ID custom de su workspace, úsalo. Si no, usa `get_jira_issue_type_fields` para encontrar el campo correcto en su proyecto.
5. **¿Agrupar bajo una épica?** Si hay 5+ tareas para un mismo módulo/proyecto, sugiere crear una épica padre y las tareas como issues hijos (campo `parent`). Si el usuario acepta, primero crea la épica, luego cada tarea con `parent: { key: "EPIC-KEY" }`.
6. **¿Vincular issues relacionados entre capas?** Sugiere crear `issuelinks` tipo `relates to` entre el SP de SQL, su endpoint de Backend y su pantalla de Frontend que comparten la misma Estructura Descriptiva. Esto da trazabilidad en Jira.

### Paso 3: Verificar duplicados y Confirmar

Antes de crear, busca en Jira si ya existen issues con el mismo summary o estructura descriptiva:

```
project = [PROJECT_KEY] AND summary ~ "[estructura_descriptiva]"
```

Si encuentras coincidencias, notifica al usuario: "Encontré 3 issues que podrían ser duplicados: KEY-001, KEY-002, KEY-003. ¿Saltar estos o crear de todos modos?"

Luego muestra un resumen ANTES de crear:

```
Voy a crear N issues en [PROJECT_KEY] (site [SITE]):
- M en capa SQL
- M en capa Backend
- M en capa Frontend
Total de puntos: X
Tipo de issue: Task
Campo de puntos: customfield_XXXXX

¿Confirmas que proceda?
```

**Espera confirmación explícita** ("sí", "confirmo", "procede") antes de crear. No procedas con "ok" ambiguo.

### Paso 4: Crear issues

Para cada fila de datos (omitiendo subtotales/total):

- **Summary**: `[Capa] Nombre Actividad — Estructura Descriptiva`
  - Ejemplo: `[SQL] Se realiza SP — ItinerarioSeguridadDB.ins.usp_AltaRecorrido`
- **Description**: incluye el Req., la justificación y la estructura descriptiva en formato markdown legible.
- **Issue Type**: el elegido en paso 2.
- **Labels**: añadir `sputnik`, `cotizacion`, y la capa en minúscula (`sql`, `backend`, `frontend`).
- **Story Points**: el valor de la columna Puntos, en el campo custom elegido.
- **Project**: el project key elegido.

Crea los issues uno por uno usando directo la Jira REST API (POST `/rest/api/3/issue`) vía axios o fetch. Si una creación falla, anótalo pero sigue con las demás — no abortes todo.

### Paso 5: Vincular issues entre capas

Si el usuario aceptó vinculación en Paso 2, para cada grupo de issues que comparten la misma Estructura Descriptiva (SP SQL → Endpoint Backend → Pantalla Frontend):

```json
POST /rest/api/3/issueLink
{
  "type": { "name": "Relates" },
  "inwardIssue": { "key": "SPK-100" },
  "outwardIssue": { "key": "SPK-105" }
}
```

Esto crea una relación visible en ambos issues, dando trazabilidad completa de la feature a través de las capas.

### Paso 6: Reportar resultado

Al terminar, devuelve un resumen:

```
✅ Creados: N issues
❌ Fallidos: M (con razón)
🔗 Links: lista de los keys generados (SPK-123, SPK-124, ...)
```

## Manejo de tareas divididas `[DIVISION]`

Las tareas con prefijo `[DIVISION]` se crean como issues normales (no como subtasks automáticamente), porque comparten la misma Estructura Descriptiva y eso ya las relaciona visualmente.

Si el usuario pide explícitamente que las `[DIVISION]` sean subtasks de un issue padre, primero crea el padre con la Estructura Descriptiva completa (sin puntos), luego crea las divisiones como subtasks usando el campo `parent`.

## Errores comunes y cómo manejarlos

- **Campo de story points no encontrado**: el ID varía por instancia. Usa `get_jira_issue_type_fields` para listar campos del tipo de issue elegido y busca uno con nombre "Story Points" o "Puntos de historia". Pide al usuario que confirme el ID antes de continuar.
- **Project key inválido**: lista los proyectos disponibles con `get_visible_jira_projects` y pide que elija.
- **Permisos insuficientes**: reporta al usuario qué permiso falta (típicamente "Create Issues" en ese proyecto) y detente.

## Lo que NO debes hacer

- No crees issues sin confirmación explícita del usuario.
- No inventes el `customfield_XXXXX` de Story Points — confírmalo o detéctalo.
- No subas filas de SUBTOTAL o TOTAL GENERAL como issues.
- No abortes toda la operación si una sola creación falla; sigue con las demás y reporta al final.
- No modifiques los puntos al subirlos: respeta los valores exactos de la tabla.
