---
name: jira-analyst-skill
description: Analyzes Jira tickets and produces functional or technical proposals. Use when the user asks to analyze a ticket (e.g. MDCS-456, JIRA-123), understand a problem, design solutions, or analyze CMM logs/interfaces. Escalates through Jira, Confluence, and code before asking. Generates a markdown file in ~/Desktop/Análisis/.
license: MIT
compatibility: Requires mcp-atlassian MCP server configured with Jira and Confluence credentials.
metadata:
  author: facuperezbri
  version: "2.0.0"
---

# Jira Solution Designer

## Rules

1. **Spanish always** — All output (analysis, questions, proposals, file content) must be in Spanish, regardless of source language.
2. **Never invent; label assumptions** — If context is missing, escalate through levels. Every assumption must be marked `[SUPOSICION]` or `[NO CONFIRMADO]`.
3. **User artifacts = evidence** — Logs, payloads, and interfaces pasted in chat are first-class evidence, equal to Jira or code data.
4. **MANDATORY: file always on Desktop** — Write `~/Desktop/Análisis/<JIRA-KEY>-analisis.md`. NEVER create files inside any project repository. FORBIDDEN paths: `docs/`, `docs/ai/`, relative paths, or any path within the current working directory. If in doubt, always use `~/Desktop/Análisis/`.
5. **Concise** — 1-2 pages unless the ticket is very complex.
6. **Project terminology** — Use feature names, services, and flows as they appear in Jira, Confluence, and code.
7. **Code conventions** (technical mode only) — Branch: `feature/JIRA-ID` or `fix/JIRA-ID`; commits in Spanish.

---

## Mode Detection

**FUNCTIONAL (default)** — ticket is about business rules, flows, requirements, CMM behavior, or user asks to "understand what's happening". Output: business analysis, rules, flows, dependencies. No candidate files.

**TECHNICAL** — user explicitly asks for code changes, implementation, "what files to touch", "technical solution", or ticket is clearly frontend implementation. Output: functional analysis + candidate files, approaches, implementation plan.

---

## Artifact Detection

Check the user message for inline artifacts before starting the flow:
- **XML/SOAP/JSON**: structured payloads, request/response blocks
- **Logs**: timestamps, stack traces, HTTP status codes
- **CMM interfaces**: operation definitions, fields, data types

If detected: parse type, extract key fields, use as evidence (no need to search elsewhere).

**CMM analysis protocol:**
- **Request** — operation name, fields sent, empty/null/suspicious values, comparison to interface if available
- **Response** — success or error; extract `cmmCode` + `cmmMsg` + `detail`; meaning in flow context
- **Request + Response** — trace sent→received; identify discrepancies; propose probable cause
- **Interface/Contract** — required vs optional fields, data types, comparison to actual payloads

**Trace number**: if user mentions one, ask them to paste CMM request/response blocks from their trace viewer directly in chat.

---

## Workflow

### Step 1: Get ticket

Call `jira_get_issue` — fields: `summary,description,status,priority,assignee,labels,issuetype,created,updated,parent`; `expand: "renderedFields"`; `comment_limit: 5`.

### Step 2: Evaluate context completeness

Ticket is **clear** when all four are present: target feature/flow/service · current behavior or problem · desired behavior or outcome · at least one acceptance criterion or success signal. User-provided artifacts count toward threshold.

- Clear → **Step 4**
- Partial or insufficient → **Step 3**

### Step 3: Progressive escalation

Run levels in order. Re-evaluate after each. If threshold met → **Step 4**.

#### Level 1 — Related tickets

JQL searches in priority order:
1. `parent = <PARENT_KEY>` or `"Epic Link" = <EPIC_KEY>`
2. `labels IN (<LABELS>) AND project = <PROJECT> AND key != <KEY> ORDER BY updated DESC`
3. `project = <PROJECT> AND summary ~ "<TERM>" AND key != <KEY> AND status in (Done, Closed, Resolved) ORDER BY updated DESC`

For each relevant ticket extract: business rule · change made · risk or restriction.

#### Level 2 — Confluence

`confluence_search` + `confluence_get_page` (max 3 pages). Extract: business rules, documented flows, functional specs, CMM interfaces.

#### Level 3 — Code (only if TECHNICAL mode or adds functional context)

`Glob` → `Grep` → `Read` on `src/features/<feature>/**/*` and key ticket terms. Extract: current flow, API calls, payloads, validations, field mapping.

#### Level 4 — Questions

If threshold not met, ask 3-5 prioritized questions:

| Type | Priority questions |
|------|--------------------|
| Bug | Reproduction steps, frequency, error messages, environment |
| UI | Screen/component, mockup, copy changes |
| Service/API | Payload contract, error handling, new or existing endpoint |
| CMM/Backend | CMM operation, expected interface, error codes; ask: "¿Podés pegar el request y response CMM directamente acá?" |
| Vague | Business intent, functional area, definition of done |

Wait for responses, then re-evaluate. If met → **Step 4**. If not → **Level 5**.

#### Level 5 — Declare blockage

Produce Mode C output + generate file.

### Step 4: Enrichment

- `jira_get_issue_development_info` — PRs, branches, commits
- `jira_get_issue_images` — mockups, screenshots
- `jira_get_issue_dates` — status history and transitions

**Extended analysis** (triggered by: "con contexto de HU anteriores", "análisis funcional extendido", "dependencias CMM"):
- Run Level 1 JQL searches if not already done; synthesize antecedents table
- Identify external dependencies (CMM, backend, contracts)
- Activates sections 8–9 in Mode A-Functional output

**Technical mode** (if code not inspected in Level 3): locate and read feature files; identify components, reducers, sagas, services, validations; search for similar patterns.

### Step 5: Confidence check

Produce **Mode C** if any blocking condition applies: no reproduction steps or data · multiple valid flows unidentified · missing payload contract · missing logs needed to locate failure · missing business rule to choose between options · ambiguous or contradictory user responses.

### Step 6: Output

Select mode and generate in-chat response + markdown file.

---

## Output Templates

### Mode A-Functional

```
## 1. Resumen de negocio
- Qué se pide o qué problema se reporta (una oración)
- Usuario/rol afectado · Impacto esperado

## 2. Flujo afectado
- Descripción del flujo de negocio
- Servicios/sistemas participantes · Puntos de integración relevantes

## 3. Análisis del problema
- Qué se entiende de la evidencia disponible
- Si hay artefactos (logs, payloads): análisis detallado de qué muestran
- Comportamiento actual vs esperado

## 4. Reglas de negocio identificadas
- Explícitas (del ticket o documentación)
- Inferidas (marcadas [INFERIDA])
- Validaciones o condiciones relevantes

## 5. Diagnóstico o propuesta funcional
- Causa probable / qué cambiar funcionalmente
- Opciones si hay más de un camino · Recomendación

## 6. Dependencias y riesgos
- Dependencias externas (CMM, backend, otros equipos)
- Riesgos identificados · Suposiciones ([SUPOSICION])

## 7. Próximos pasos recomendados
- Acciones concretas · A quién consultar · Evidencia adicional a obtener

<!-- Solo para análisis extendido (flag Step 4) -->
## 8. Antecedentes funcionales relevantes

| Key | Summary | Regla de negocio | Cambio realizado | Riesgo/restricción |
|-----|---------|------------------|------------------|--------------------|

## 9. Dependencias externas pendientes
- [Dependencia externa] <tipo>: <descripción> | Artefacto faltante: <qué> | Quién: <rol o sistema>
```

### Mode A-Technical

```
## 1. Resumen de negocio
- Qué se pide · Usuario/rol · Impacto esperado

## 2. Áreas impactadas
- Features (nombre + path) · Reducers, sagas, servicios API · Componentes principales

## 3. Archivos candidatos
- Lista con rutas: src/features/..., src/api/... · Breve motivo por archivo

## 4. Enfoques posibles (1-3)
- Descripción · Pros/cons · Complejidad (baja/media/alta)

## 5. Enfoque recomendado
- Por qué · Pasos concretos ordenados

## 6. Riesgos e incógnitas
- Requisitos ambiguos · Dependencias externas · Suposiciones ([SUPOSICION])

## 7. Plan de pruebas
- Casos a validar · Datos de prueba necesarios

## 8. Rama y commit
- Rama: feature/JIRA-XXX o fix/JIRA-XXX
- Commit: feat(scope): descripción en español
```

### Mode B: Missing context

```
## Resumen del ticket
- Lo que el ticket establece (breve) · Qué está claro y qué no

## Contexto faltante
- Elementos del umbral mínimo ausentes · Por qué bloquean una propuesta concreta

## Preguntas para destrabar el análisis
1. ... (3-5 numeradas, priorizadas por impacto; si involucra CMM: pedir request/response)

## Suposiciones tentativas (opcional)
- Marcadas [NO CONFIRMADO] — no tratar como requisitos

## Próximo paso recomendado
- Qué hacer · A quién consultar (PO, QA, backend, diseñador)
```

### Mode C: Blocked after investigation

```
## Resumen de lo investigado
- Jira: <tickets> · Confluence: <páginas> (si aplica) · Código: <archivos> (si aplica)
- Artefactos del usuario: <qué> (si aplica) · Preguntas y respuestas (si aplica)

## Por qué no puedo avanzar
"No tengo suficiente contexto para proponer una solución confiable."
Condición de bloqueo: <cuál aplica>

## Evidencia faltante
- Funcional: definición, regla, criterio, alcance
- Técnico: payload, contrato, interfaz CMM, spec API
- Observable: logs, errores, pasos, screenshots, traces
[Dependencia externa] <tipo>: <desc> | Artefacto: <qué> | Quién: <rol o sistema>

## Preguntas o artefactos necesarios
- Concretos, que destrabarían el análisis

## Próximo paso recomendado
- Qué obtener · A quién pedirlo
```

---

## Output File

**Path (always, mandatory):** `~/Desktop/Análisis/<JIRA-KEY>-analisis.md` — create directory if needed.
**NEVER use:** `docs/`, `docs/ai/`, `docs/ai/analysis/`, relative paths, or any path inside the current project.

File structure:

```
# Análisis: <JIRA-KEY> — <Summary>

**Fecha**: <fecha> | **Modo**: A-Funcional | A-Técnico | B | C | **Ticket**: <KEY> | **Estado**: <status> | **Prioridad**: <priority> | **Tipo**: Funcional | Técnico

---

<Contenido completo del modo seleccionado>

---

## Fuentes consultadas
- Jira: <tickets> | Confluence: <páginas> (si aplica) | Código: <archivos> (si aplica) | Artefactos del usuario: <qué> (si aplica)
```
