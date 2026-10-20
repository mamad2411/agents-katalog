---
name: fx-workflow-authoring
description: Factory-internal meta-skill for authoring CC-native pipeline workflows (`.claude/skills/tk-*/`) and their thin slash commands. Invoked when creating a new `tk-*` or refactoring phases.
family: factory-internal
model: opus
authoring_time: true
runtime: false
last-verified: 2026-04-29
---

# fx-workflow-authoring — CC-native workflow authoring doctrine

> **Propósito:** capturar la doctrina de autoría de workflows CC-native — patterns, contratos, checkpoints, artifacts y subprocess delegation — para que cada workflow nuevo aplique las mismas decisiones sin drift silencioso.
>
> **Aplica a:** autoría nueva de un `tk-*` y refactor de un `tk-*` existente.
>
> **NO es runtime.** Este skill no se carga cuando un workflow se ejecuta — se carga cuando **lo estás creando o refactorizando**.

---

## ¿Cuándo se auto-carga?

Routing semántico (CC.md §1.1). Triggers típicos:

- "autorar workflow", "crear skill tk-\*", "refactor phase del tk-\*", "nuevo comando para pipeline"
- "split SKILL.md", "diseñar checkpoint", "subprocess delegation pattern"
- Edición de archivos en `.claude/skills/tk-*/`, `.claude/skills/fx-*/`, `.claude/commands/`

**NO se carga cuando:**

- Estás ejecutando un workflow — eso es runtime, lo cubre el skill `tk-*` mismo.
- Estás autorando un `kb-*` / `sk-*` / `doc-*` — distinto dominio, no estructura de workflow.
- Estás escribiendo una rule (`.claude/rules/*.md`) — declarativa, no procedural.
- Estás autorando un agent (`.claude/agents/*.md`) standalone — diferente primitiva.

---

## §1 Framing CC-native authoring

Este skill es la **doctrina de autoría de workflows CC-native** — patterns, contratos, checkpoints, artifacts y subprocess delegation. No es guía de port desde otros runtimes.

Cuando un `tk-*` nuevo necesita autoría, este skill responde sin handwaving:

- ¿Qué frontmatter? → §5
- ¿Qué secciones del SKILL.md? → §6
- ¿CP1 inline o CP2 Plan Mode? → §7
- ¿Necesito templates/, methodology, CHANGELOG? → §11 decision tree
- ¿Cómo nombro subprocesses? → §8
- ¿Cómo escribo el thin wrapper? → §12
- ¿Qué evito en el body? → `anti-patterns.md §7`
- ¿Cómo invoco mis subprocesses? → §9 skill grounding
- ¿Qué pasa si llega info post-CP? → §10 invalidation handling
- ¿Cómo cierro y cleanup? → §6 + lifecycle final phase
- ¿Está completo? → §14 checklist

Si alguna respuesta es "depende" o "quizá" → gap a cubrir antes de autorar.

---

## §2 Ontology table

Agents NO son "quién hace qué" (persona, roleplay). Son **subprocesos aislados** lanzables en paralelo o serie con contexto propio. Su valor es aislamiento + control de carga + paralelismo.

| Primitiva                                         | Propósito                                                                                                                                                              | Naturaleza  |
| ------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------- |
| **Rules** (`.claude/rules/*.md`)                  | Constraints always-on                                                                                                                                                  | Declarativa |
| **Skills** (`.claude/skills/*/`)                  | Conocimiento / procedimiento reusable                                                                                                                                  | Estática    |
| **tk-\*** (`.claude/skills/tk-*/`)                | Workflow / orquestador                                                                                                                                                 | Procedural  |
| **Agents** (subprocesses) (`.claude/agents/*.md`) | Subprocesses aislados lanzables en paralelo/serie. Contexto propio, input acotado, output esperado. Valor = aislamiento + control de carga + paralelismo (no roleplay) | Subprocess  |
| **Commands** (`.claude/commands/*.md`)            | Thin wrappers de invocación                                                                                                                                            | Pegamento   |
| **Templates** (`templates/*.template.md`)         | Shape obligatorio de artefactos generados                                                                                                                              | Schema      |
| **CHANGELOG** (`CHANGELOG.md`)                    | Historia interna de evolución del workflow                                                                                                                             | Audit trail |

Un workflow que trata a sus agents como "personas con personalidad" tiende a darles tareas vagas y context completo. Un workflow que los trata como subprocesos los acota: input contract, output esperado, return summary.

---

## §3 9 principios

1. **Foco por fase + gates duros.** Ejecutar la fase actual con su contexto explícito. No saltar checkpoints. No operar de memoria. Implementación posible: SKILL.md monolítico + turn boundaries explícitos, o phase files separados con Read on-demand. La disciplina importa, no el split. **Progressive loading clásico (phase files) es técnica disponible, no requisito universal.**
2. **Checkpoints son stops reales.** Emitir opciones numeradas (1/2/3) y esperar respuesta numérica. Nunca "el usuario probablemente quiere continuar".
3. **Batch boundaries previenen saturación cuando aplica** (volúmenes grandes de inputs / outputs). Sub-batches dinámicos para volumen impredecible.
4. **Entender antes de modificar** (Chesterton's Fence). Leer file + dependencias + porqué de su diseño antes de cambiar.
5. **Conocer arquitectura ≠ autorización para saltar.** Aunque sepas que la fase 3 viene después, solo ejecutas lo cargado en la sesión actual (CC.md §7).
6. **Trust the harness — no duplicar gates con reglas manuales.** CC runtime gestiona auto-compact context, Plan Mode formal, hooks, ToolSearch deferred loading. NO replicar primitivas runtime compartidas en cada workflow. Si CC ya lo hace, no lo agregamos como check manual.
7. **Fundamentar en skills, no inventar.** Si una regla ya vive en un skill/rule del kit, citarla. No reimplementar inline. No proponer mecanismo paralelo cuando ya hay uno.
8. **Skill body es ahistórico.** Decisiones de evolución, calibración, casos específicos viven en `CHANGELOG.md` per-heavy. El body refleja behavior actual; la historia va al CHANGELOG. NO mencionar otros skills por nombre como "el que está bien hecho" o "el que está stale" — el body es manual, no biografía.
9. **Quality > speed.** Preservar información sobre comprimir. Templates obligatorios. Procesar todo source. Challenge passes. Gates cuantitativos.

---

## §4 Estructura de archivos canónica per workflow

```
.claude/skills/tk-{name}/
├── SKILL.md                           ← Entry monolítico (sin LOC limit; ver §6)
├── methodology.md                     ← Companion conceptual (OPCIONAL — solo si schemas formales)
├── CHANGELOG.md                       ← Audit trail (heavy workflows; ver §11)
└── templates/                         ← OBLIGATORIO si genera ≥1 artifact con shape fijo
    ├── {{artifact-1}}.template.md     ← (regla "no template, no artifact" — §11)
    └── {{artifact-2}}.template.md

.claude/agents/                        ← Subprocesses propios viven aquí (FLAT, no dentro del skill folder)
├── {{prefix}}-{{name-1}}.md           ← prefix scoped al workflow (ver §8)
└── {{prefix}}-{{name-2}}.md

.claude/commands/{{name}}.md           ← Thin wrapper (ver §12)
```

---

## §5 Frontmatter shape (9 fields)

```yaml
---
name: tk-{workflow-name} # kebab-case, match directorio
description: { 1-line EN trigger surface } # EN-only, no enumeración wall-of-text
family: coding | documentation | factory-internal # Agrupa workflows por dominio
model: opus | sonnet | haiku # Opus default para workflows críticos
parallelism_unit: none | batch | pass # Solo si aplica
concurrency_cap: 1 # Pipeline workflows: siempre 1
merge_strategy: orchestrator-merge # Si hay subprocess outputs a consolidar
auditor_step: true | false # true si Phase final activa quality-engineer u otro auditor
last-verified: YYYY-MM-DD # Convención del kit (no-std YAML) — skill-lint staleness check
---
```

**Campos obligatorios:** `name`, `description` (EN-only, single-line), `family`, `model`.
**Campos opcionales:** `parallelism_unit`, `concurrency_cap`, `merge_strategy`, `auditor_step`, `last-verified`.

**`parallelism_unit` valores:**

- **`none`** — workflow lineal sin batching (caso típico de pipelines simples).
- **`batch`** — fases procesan items en batches paralelos (ej: ≤5 files per subprocess invocation).
- **`pass`** — fases completas en paralelo como pasadas independientes (ej: 3 reviewers).

---

## §6 SKILL.md sections en orden

11 secciones canónicas. Cada una con criterio de aplicabilidad — **NO marker UNIVERSAL/CONDITIONAL binario**, sino "aplica si workflow tiene X característica". El template `templates/tk-skill.template.md` las trae con instrucciones inline.

| #   | Sección                                             | Aplica si...                          |
| --- | --------------------------------------------------- | ------------------------------------- |
| 1   | Propósito + Architectural principle (>)             | Siempre                               |
| 2   | Tone guidance                                       | Workflow es conversacional con humano |
| 3   | Anti-Drift / Quality Rules numeradas                | Workflow tiene reglas no-negociables  |
| 4   | Turn boundaries table                               | Workflow es multi-turn iterativo      |
| 5   | TodoWrite obligatorio (mention)                     | 3+ phases                             |
| 6   | Flow overview (ASCII diagram)                       | 3+ phases                             |
| 7   | Phase N — Propósito + Acciones                      | Siempre (1 por fase)                  |
| 8   | Checkpoints (CP1 inline + CP2 Plan Mode)            | Workflow tiene gates intermedios      |
| 9   | Output files lifecycle (durable/audit/transitional) | Produce >2 artifacts                  |
| 10  | Invalidation handling cross-phase                   | Cualquier checkpoint                  |
| 11  | Subprocess delegation summary table                 | Workflow tiene subprocesses propios   |

**Sin LOC limit.** Un SKILL.md monolítico funciona si está bien escrito (turn boundaries explícitos, sub-secciones con H2/H3 navegables). Partir solo si secciones temáticamente separables o se quiere permitir Read parcial — no por número de líneas.

---

## §7 CP1 vs CP2 doctrine

| Checkpoint | Mecanismo                                                          | Cuándo                                                                                                     | Output template                             |
| ---------- | ------------------------------------------------------------------ | ---------------------------------------------------------------------------------------------------------- | ------------------------------------------- |
| **CP1**    | Inline + STOP (compact 3-4 líneas críticas) + tabla 1/2/3          | Conversational review post-context-load. LOW-MEDIUM risk reversible. Verbose mode opt-in vía flag command. | `templates/checkpoint-inline.template.md`   |
| **CP2**    | Plan Mode formal (entry/exit según runtime) + structured synthesis | Synthesis multi-fuente crítica. HIGH risk (CC.md §3). Output durable bloquea writes hasta approval.        | `templates/checkpoint-planmode.template.md` |

**Ambos checkpoints DEBEN emitir tabla numerada de opciones (1/2/3)** y esperar respuesta numérica del user. NO aceptar "ok"/"sí"/"procede" libres — re-presentar opciones si el user responde texto libre.

> **Pre-load nota:** si las primitivas de Plan Mode son deferred en el runtime actual (ej: requieren tool-loading explícito antes de invocarse), el orchestrator debe cargarlas antes de CP2. El mecanismo concreto vive en docs del runtime; este skill solo establece el requisito.

> **Verbose mode:** opcional, activado vía flag en `$ARGUMENTS` (ej: `verbose=true`). Por default los CPs son compact (3-4 líneas). Verbose amplía con coverage map + plan detallado + invalidation rules.

---

## §8 Subprocess delegation policy

**Definición:** subprocess = agent aislado lanzable en paralelo o serie. Contexto propio, input acotado, output esperado. Valor = aislamiento + control de carga + paralelismo.

### Usar subprocess cuando

- **Input grande contaminaría el main context.** Ej: procesar N PDFs / transcripts no debe contaminar al orchestrator.
- **Tarea con contrato cerrado input/output.** Inputs definidos, output schema definido, sin diálogo intermedio.
- **Varias tareas independientes pueden correr en paralelo.** N batches simultáneos sobre items independientes.
- **Output puede persistirse como artifact y mergearse luego.** Subprocess escribe a path pre-calculado; orchestrator concatena/consolida post-completion.

### NO usar subprocess cuando

- **Decisiones globales de orquestación.** Eso vive en main loop, no se delega.
- **Main loop ya tiene todo el contexto y trabajo es lineal.** No hay valor en aislar.
- **Output depende de conversación inmediata con user.** Caso CP1 / CP2 — orchestrator-direct.
- **Subprocess tendría que redescubrir medio workflow para operar.** Si el contract no es cerrable, no es candidato.

### Naming convention

Prefix scoped al workflow: `{prefix}-*` donde `{prefix}` deriva del workflow name (ej: workflow `tk-foobar` → prefix `fb-*` o `foo-*`). Documenta el prefix en `SKILL.md §11 Subprocess delegation summary` para que sea grep-able.

Generic agents (cross-workflow, ej: `architect`, `product-owner`, `project-planner`, `quality-engineer`) NO llevan prefix workflow-scoped y viven sin prefix en `.claude/agents/`.

### Tools allowlist

**Restrictivo en frontmatter, NO default = todas.**

Default sugerido por rol:

| Rol                                                      | tools allowlist                |
| -------------------------------------------------------- | ------------------------------ |
| **Writer / extractor** (persiste artifact directo)       | `Read, Grep, Glob, Write`      |
| **Auditor / reviewer** (findings inline al orchestrator) | `Read, Grep, Glob` (sin Write) |
| **Test runner** (ejecuta comandos, no persiste)          | `Read, Grep, Glob, Bash`       |

**Anti-pattern:** subprocess sin `tools:` declarado (default = todas, peligroso). Subprocess auditor con `Write` (rol es solo análisis).

### Model selection per agent

Default: `model: inherit` (subprocess hereda el modelo del orchestrator).

> **Sintaxis del campo `model`:** el frontmatter de subagent acepta solo aliases — `sonnet`, `opus`, `haiku`, `inherit`. NUNCA model IDs completos (`claude-sonnet-4-6`, `claude-opus-4-7`). El alias mapea al latest del runtime CC.

Override a `sonnet` cuando aplica TODO lo siguiente:

- **Massively parallel:** N≥5 spawn simultáneo del mismo agent.
- **Structured-output:** sigue un template fijo (schema templated, no synthesis abierta).
- **Reasoning/extraction ratio bajo:** mostly templating + classification, sin cross-source synthesis denso.

Mantener `inherit` (Opus si el orchestrator es Opus) cuando aplica al menos uno:

- Single-call con multi-source synthesis.
- Adversarial review (architect, security-auditor, project-planner).
- Reasoning denso requerido sobre inputs heterogéneos.

**Rationale:** Sonnet es ~3-5× más rápido que Opus para structured-text masivamente paralelo, sin pérdida material de calidad. Pero el orchestrator y los agents que hacen synthesis cross-fuente sí pagan calidad si bajan a Sonnet — mantener Opus en esos.

### Input contract section (obligatoria en cada agent .md)

```markdown
## Input contract

El orchestrator invoca el subprocess con:

- **`{param-1}`** — descripción + tipo
- **`{param-2}`** — descripción
- **`output_path`** — path pre-calculado por orchestrator
- **`{project_slug or batch_id}`** — para naming
```

### Return summary (obligatoria)

5-8 líneas máximo. **NO retornar el output completo inline** — el orchestrator lee el file post-completion.

### "Cuándo NO usar este subprocess" section

Cada agent .md debe listar 3-4 casos donde NO es responsable. Boundary enforcement, previene mission creep.

---

## §9 Skill grounding rule (CC.md §2 codification)

**Regla:** cuando orchestrator invoca subprocess y el dominio del task matchea ≥1 skill del kit, DEBE citar paths repo-relative en el prompt del Agent call.

**Razón:** subprocesses NO reciben listing por description injection. Sin paths citados, el subprocess opera sin el kit (`sk-*`/`kb-*`/`doc-*`).

**Format obligatorio:**

```
consulta antes de empezar:
- .claude/skills/{name}/SKILL.md
- .claude/skills/{name2}/SKILL.md
```

**Paths repo-relative**, no absolutos — `<absolute-user-path>/...` no debe aparecer en docs tracked.

**Anchor:** `CC.md §2`.

---

## §10 Invalidation handling rule

Cada workflow heavy DEBE declarar qué pasa si llega información nueva después de un checkpoint. Sin esto, los workflows iterativos producen state inconsistente.

**Opciones para declarar:**

- **Patch incremental** — orchestrator hace edits localizados al artifact afectado.
- **Regen completo** — re-corre la fase que produjo el artifact.
- **Backtrack a fase anterior** — vuelve a una fase upstream y re-corre intermedias.
- **User choice con threshold** — debajo de cierto delta (ej: <30%), patch; por encima, prompt al user con opciones.

El threshold concreto y la mezcla de opciones es decisión del workflow; lo no negociable es **declarar la política explícitamente** en una sección dedicada del SKILL.md.

**Anti-pattern:** workflow heavy sin esta sección → state inconsistente garantizado en runs reales.

---

## §11 Companions decision tree

Cuándo necesitas cada companion file:

| Característica del workflow                                     | Companion necesario                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                | Skeleton                                                                 |
| --------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------ |
| Schemas formales (taxonomies, confidence tags, factory-tickets) | Default: `methodology.md` (single file, ≤500 LOC). Split a `methodology/{topic}.md` sub-folder cuando el contenido es sectionable per agent invocation Y aplica al menos uno: (a) ≥3 topics distintos consumidos por subprocesses distintos, (b) algún topic excede 150 LOC, o (c) `methodology.md` total excede 500 LOC. Al split, mantener `methodology.md` como **thin index** que apunta a cada sub-file (no eliminar — preserva discoverability + back-compat con refs viejos). Subprocess prompts citan el sub-file específico cuando split. | (domain-specific, no skeleton)                                           |
| Itera y calibra (3+ runs sistémicos)                            | `CHANGELOG.md`                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     | `templates/workflow-changelog.template.md`                               |
| Produce ≥1 artifact con shape fijo                              | `templates/*.template.md` (regla **"no template, no artifact"** — hard)                                                                                                                                                                                                                                                                                                                                                                                                                                                                            | `templates/` shape convention                                            |
| Subprocesses propios                                            | Naming `{prefix}-*` + tools allowlist + input contract + return summary                                                                                                                                                                                                                                                                                                                                                                                                                                                                            | `templates/subprocess-prompt.template.md`                                |
| Conversacional multi-turn                                       | Tone guidance + turn boundaries + verbose flag                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     | `templates/tk-skill.template.md` (sections 2, 4)                         |
| Synthesis multi-fuente HIGH-risk                                | CP2 Plan Mode formal                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               | `templates/checkpoint-planmode.template.md`                              |
| >2 artifacts                                                    | Output lifecycle 3-tier (durable / audit / transitional)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           | `templates/tk-skill.template.md` (section 9)                             |
| 3+ phases con checkpoints                                       | TodoWrite + thin wrapper + flow overview ASCII                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     | `templates/tk-skill.template.md` + `templates/slash-command.template.md` |
| Cualquier checkpoint                                            | Invalidation handling explícito (§10)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              | inline en SKILL.md                                                       |

> Definición operable de heavy vs ligero: ver §13.

> **Hard rule "no template, no artifact":** si el workflow va a generar `foo.md`, primero crea `templates/foo.template.md`. Sin template, no se genera. Improvisar shape produce drift entre runs y entre proyectos derivados.

> **Why keep `methodology.md` as thin index after split:** human reads y stale instructions siguen resolviendo. Cost ~10 LOC; benefit zero broken refs across the kit (incl. otros agents y skills que pudieran citar `methodology.md` por costumbre).

---

## §12 Wrapper rules (thin slash command)

**Anatomía:** thin wrapper. `Read` del SKILL.md → parse `$ARGUMENTS` → TodoWrite obligatorio si 3+ phases → delegate a skill.

**Regla operativa:** "wrapper no duplica semántica del skill". El conteo de líneas es guideline (~30-40 típicamente), no constraint hard.

**Mode detection:**

- Parámetros sin prefijo (ej: `nuevo`, `con-docs`, `validar`) → modo principal del workflow.
- Flags con `--` (ej: `--next`, `--plan`) → comportamiento secundario.
- `verbose=true` → activa CP verbose mode.
- Si `$ARGUMENTS` vacío → Phase 0 del skill pregunta el modo.

**3 reglas duras:**

- ❌ Wrapper NO duplica fases del skill. (No enumerar Phase 1, 2, 3 en el wrapper — eso vive en SKILL.md.)
- ❌ Wrapper NO contradice checkpoints del skill. (Si el skill define un mecanismo concreto para CP1, el wrapper no puede decir lo contrario.)
- ❌ Wrapper NO redefine semantics. (No introducir modos no documentados en el skill.)

**Skeleton:** `templates/slash-command.template.md`.

---

## §13 Heavy vs ligero — definición operable

- **Heavy workflow** = 3+ phases con artifacts durables / schemas formales / subprocesses propios.
  - Necesita: SKILL.md + templates/ + (methodology.md si schemas) + CHANGELOG.md + thin wrapper + agents prefix-scoped.
- **Ligero workflow** = 1-2 phases sin artifacts. Caso típico: utilidad de transición de sesión / utility tooling sin output durable.
  - Mínimo: SKILL.md + frontmatter + thin wrapper + anti-pattern grep.

---

## §14 Heavy workflow checklist (12 items SÍ/NO/N/A)

Aplicar antes de cerrar la autoría. Si algún item es NO sin justificación → gap a cubrir.

- [ ] Frontmatter con los 9 fields universales (§5)
- [ ] SKILL.md sigue las 11 secciones invariables en orden (§6)
- [ ] CP1 + CP2 con doctrina explícita (§7) — ambos con tabla 1/2/3
- [ ] `templates/` folder con `*.template.md` por artifact (regla "no template no artifact" — §11)
- [ ] `methodology.md` si hay schemas formales (§11)
- [ ] `CHANGELOG.md` con `[Unreleased]` + buckets (§11)
- [ ] Thin wrapper command sigue las 3 reglas (§12) — no duplica, no contradice, no redefine
- [ ] Subprocesses prefix-scoped `{prefix}-*` con tools allowlist apropiado por rol (§8)
- [ ] Subprocess model selection (§8) — overrides a `sonnet` justificados (parallel structured-output); `inherit` para single-call denser-reasoning agents
- [ ] Skill body ahistórico (no client names, no journey narrative — `anti-patterns.md §7`)
- [ ] Invalidation handling explícito (§10)
- [ ] Subprocess prompts citan paths repo-relative de skills (§9, CC.md §2)
- [ ] Anti-patterns greps pasan vacío (`anti-patterns.md §14`)

---

## §15 Verificación funcional

**Caso de prueba:** un workflow heavy hipotético del pipeline (cualquiera que no exista todavía). Aplicar este skill a "diseña ese workflow" y confirmar que responde sin handwaving en las 12 preguntas del checklist (§14). Si alguna es "depende" / "quizá" → gap a cubrir.

Si el meta-skill entrega respuestas concretas en las 12, cumplió su objetivo.

---

## §16 Boundary

| Si vas a autorar...                                        | NO uses este skill — usa...                                |
| ---------------------------------------------------------- | ---------------------------------------------------------- |
| Un `kb-*` (Next.js, Drizzle, Tailwind, testing)            | El dominio técnico directo (no hay meta-skill para `kb-*`) |
| Un `sk-*` (kit-shipped system)                             | Inventario directo + `kb-*` correspondiente                |
| Un `doc-*` (knowledge documental)                          | Conocimiento documental directo                            |
| Un agent `.claude/agents/*.md` standalone (cross-workflow) | Leer otros agents + `CC.md §6` como referencia             |
| Una rule `.claude/rules/*.md`                              | Cada rule es ad-hoc — no hay patrón replicable             |
| Un slash command sin skill detrás                          | `templates/slash-command.template.md` (aquí mismo sirve)   |

---

## §17 Post-change validation

Antes de commit de un workflow nuevo o refactor:

- [ ] Frontmatter válido (`name`, `description` EN-only single-line, `family`, `model`)
- [ ] Todos los Read-refs resuelven (paths existen)
- [ ] Phase files (si hay split) auto-contenidos (no dependen de variables del padre)
- [ ] Checkpoints emiten tabla 1/2/3 de opciones
- [ ] No hay carry-overs AG residuales (greps en `anti-patterns.md §14`)
- [ ] No hay paths absolutos `<absolute-user-path>/...` (dev-specific va en `settings.local.json`)
- [ ] CHANGELOG actualizado si workflow heavy
- [ ] Templates folder presente si genera artifacts
- [ ] Subprocesses prefix-scoped con tools allowlist apropiado por rol
- [ ] Wrapper no contradice skill (test funcional: leer SKILL §Checkpoints + leer wrapper, confirmar que coinciden)
- [ ] Skill body ahistórico (greps en `anti-patterns.md §14`)
- [ ] Skill-lint pasa (`pnpm skill:lint`)

---

_TimeKast Factory — fx-workflow-authoring (CC-native authoring doctrine, factory-internal)_
