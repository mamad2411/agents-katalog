---
name: tk-discovery
description: Documentation-family workflow that extracts project truth from stakeholder interviews and source documents, preserving firm decisions and detecting drift, to produce a high-fidelity Discovery Brief and project-config as SSOT for downstream phases. Primary invocation is the `/discovery [nuevo|con-docs|validar]` slash command; do not run this skill directly outside that command.
family: documentation
model: opus
parallelism_unit: pass
concurrency_cap: 1
merge_strategy: orchestrator-merge
auditor_step: true
last-verified: 2026-04-24
---

# /discovery — Product Discovery Workflow

> **Propósito:** entender correctamente un proyecto y producir un Discovery Brief (§1-§11) + project-config confiables como SSOT para `/proposal`, `/docs`, `/design`, `/backlog`, `/implement`.
> **Architectural principle:** consumer de los artifacts es Claude AI (no humanos). Optimizar para info preservation > compaction; single-pass per archivo en su purpose; zero duplication entre artifacts (project-config always-on cubre identity/commercial/ops; brief cubre QUÉ construir; freeze-map cubre F-codes canónicos; deep-dive cubre per-feature spec con BR/F-code refs inline-resolved).
> **Anterior:** — (entry point del pipeline)
> **Siguiente:** `/docs` (typically tight-coupled) → `/design` → `/backlog (con SP)` → `/proposal` → `/implement`

---

## Principio rector

> **Info preservation > Discover > Compact.**
>
> Un brief con 13/13 secciones ricas vale más que uno compacto con info perdida. El costo de re-discovery en /docs es peor que un brief largo. Compactación solo aplica a features **objetivamente triviales** (SK-shipped end-to-end). Todo lo demás se documenta completo en Discovery.

---

## Tone guidance (user-facing)

Este workflow habla con un humano durante 8 fases. No con una máquina.

- **Prosa antes que tabla.** Cuando presentes findings, checkpoints, batches — explica por qué importa antes de tirar la tabla. Las tablas son estructura, no reemplazo de comunicación.
- **Checkpoints conversacionales, no auditoría.** CP1 y CP2 abren espacio para conversación; no fuerces `1=sí, 2=no` inmediato si el user quiere clarificar en medio.
- **Compact default, verbose opt-in.** CPs presentan 3-4 líneas críticas por default. Si el user declaró `/discovery con-docs verbose=true` en Phase 0, ampliar con coverage map + plan detallado + invalidation rules.
- **Batch checkpoint con opción de sub-ronda.** Cada batch cierra con `1=continuar / 2=revisar OQs / 3=ahondar en FT-X`. La opción 3 es parte normal del flujo, no edge case.
- **Explicar reasoning.** Si descartas una option, di por qué. Si flaggeas un risk, di el impacto concreto. No asumas que el user lee en ceros y unos.

---

## 🔴 6 Anti-Drift Rules (no negociables)

1. **NUNCA** cambiar stakeholder, deadline, scope, ownership sin autorización explícita del user.
2. **NUNCA** reinterpretar exclusiones del source package ("esto está out of scope" se mantiene out).
3. **NUNCA** mergear o renombrar entidades sin declararlo y confirmarlo.
4. **NUNCA** llenar gaps con contenido plausible — marcar como `[INFERRED]` o `[OQ]`.
5. **NUNCA** tratar Reference/Legacy/Context como SoT — respetar la jerarquía.
6. **NUNCA** procesar attachments parcialmente en silencio ("silent sampling" prohibido).

**Source Hierarchy:** `SoT > Reference > Legacy > Context`. Detalle en [methodology/source-classification.md](methodology/source-classification.md).

**Confidence Tags:** `Confirmed` (default, sin marker) / `[INFERRED]` / `[ASSUMPTION]` / `[OQ]`. **Inline en la prosa** es obligatorio, no basta tabla Assumptions. Detalle en [methodology/freeze-map.md §4](methodology/freeze-map.md).

---

## Turn boundaries (contrato con el usuario)

Multi-turn iterativo NO significa "corre lo que puedas en cada turn". Cada turn cierra con **punto de espera explícito**. No avanzar sin respuesta del user.

| Turn      | Fases que ejecuta               | Cierra con                                                                                 |
| --------- | ------------------------------- | ------------------------------------------------------------------------------------------ |
| **1**     | Phase 0 + Phase 1 Intake        | Bootstrap batch. STOP.                                                                     |
| **2**     | Phase 2 Freeze Map → CP1        | Plan inline + STOP. Puede durar N turns si user itera plan.                                |
| **3**     | Phase 3 Gap Interview           | Gap batch. STOP.                                                                           |
| **4a**    | Phase 4a Tiering pass           | Tiering presentation. STOP para user approval.                                             |
| **4b..N** | Phase 4b batches Tier S/M       | BATCH CHECKPOINT. STOP entre batches.                                                      |
| **4c.K**  | Phase 4c Tier L dedicated       | 1 FT per turn con sub-ronda clarificación obligatoria.                                     |
| **N+1**   | Phase 5 + Phase 6 + Phase 7     | Procesamiento silencioso encadenado.                                                       |
| **N+2**   | Phase 7 Gap Round 2 (si aplica) | Mini-batch stakeholder decisions post-Challenge. STOP.                                     |
| **N+3**   | CP2                             | `EnterPlanMode` + structured synthesis (CP2.synthesis template) + `ExitPlanMode` (formal). |
| **N+4**   | Phase 8 Close (post-approval)   | Escribe archivos finales. FIN.                                                             |

**Violaciones:** ejecutar Phase 2 + Phase 3 mismo turn. Ejecutar CP1/CP2 sin aprobación + saltar. Tomar decisiones stakeholder tácitamente en CP2 sin Gap Round 2.

**Excepción:** Turn N+1 encadena 5→6→7 porque (a) Phase 5 dispatch a `dsc-kit-analyst` corre sin input del user, (b) Phase 6 es orchestrator-direct sin pause natural, (c) Phase 7 architect/PO/planner corren paralelo sin input.

---

## TodoWrite obligatorio

Al iniciar (Turn 1), crear TodoWrite con items para Phase 0-8 + CP1 + CP2 + Gap Round 2. Un solo `in_progress` a la vez.

---

## Flow overview

```
Phase 0 (detect) → Phase 1 (intake + cross-file recon) → Phase 2 (freeze map) → 🛑 CP1
  → Phase 3 (gaps) → Phase 4a (tiering) → Phase 4b (Tier S/M batches parallel) → Phase 4c (Tier L dedicated)
  → Phase 5 (sk-leverage if SK_ACTIVE) → Phase 6 (synthesis) → Phase 7 (challenge pass + Gap Round 2) → 🛑 CP2
  → Phase 8 (close)
```

---

## Phase 0 — Mode Detection

**Acciones:**

1. **Parse slash arg:**
   - Mode: `nuevo` (from scratch) / `con-docs` (con docs) / `validar` (validate existing). Si vacío → preguntar al user.
   - `verbose=true` flag (opcional): activa CP verbose mode. Default compact.
2. **SK_ACTIVE detect + version drift:**
   - `jq -r '.factoryVersion // empty' <target-repo>/package.json` → `target_factory_version`
   - `jq -r '.factoryVersion // empty' <factory-repo>/package.json` → `current_factory_version` (factory repo = TimeKast-Factory submodule path o env-config)
   - `SK_ACTIVE = target_factory_version != ""`
   - **Drift flag:** if `SK_ACTIVE=true AND target_factory_version != current_factory_version` → set `factory_version_drift = true` para surface en Phase 1.1 P1 (item 5b).
3. **Anunciar estado** al user: mode + SK_ACTIVE + verbose si aplica.

---

## Phase 1 — Intake (bootstrap + cross-file reconciliation)

**Propósito:** capturar contexto mínimo viable + procesar source package.

### 1.0 Pre-read lightweight (D1 only — skip si D0)

**Si mode = D0 (from scratch sin source package):** skip 1.0, ir directo a 1.1 (path D0).

**Si mode = D1 (con source package):** antes de preguntarle al user a ciegas, leer `INDEX.md` (si existe) + headers de cada source file + first ~50 lines del archivo principal del package. Objetivo: identificar qué bootstrap items (de los 12 de 1.1) son source-answerable vs gaps reales. NO procesar a fondo — eso es 1.2 formal intake con `dsc-intake-analyst`.

**Output mental del orchestrator:** mapping `{item_index → source-answer-status}` con tags `[from {file} §{X}]` / `[INFERRED]` / `[OQ]` para cada uno de los 12 items.

> **Rationale:** preguntar 12 Qs ciegos cuando el source ya responde N de ellos desperdicia turns + degrada calidad (bootstrap derived del source > bootstrap improvisado por user). Mismo principio que el pre-question check estricto de Phase 3.

### 1.1 Bootstrap (1 ronda — D0 conversacional / D1 derivation+confirm)

Los 12 items de bootstrap son los mismos en ambos modos:

1. Problema / North Star (dolor, audiencia, métrica de éxito)
2. **Stakeholders** (decisores) — rol + nombre + scope
3. **Team members** (ejecutores) — rol + nombre + responsabilidades
4. Deadline objetivo
5. **Si SK_ACTIVE=true:** SKIP plataforma (PWA default). Else preguntar web / PWA / mobile / API.
   5b. **Factory version effective (mandatory si SK_ACTIVE=true):** target project's pinned `factoryVersion` vs current Factory version (capturados en Phase 0). - Si match → confirmable como Firm sin pregunta extra. - Si drift detected (`factory_version_drift=true` from Phase 0) → user decide upfront: - **(a) Migrate target to current pre-discovery** (recommended si target stale por meses) - **(b) Stay pinned + run Phase 5 vs target's pinned version inventory** (preserve target snapshot) - **(c) Advisory mode** (run vs current Factory, accept findings as advisory — useful when target SK version is significantly stale and full migration is out of scope for this discovery cycle) - Decision **MUST be captured before Phase 1.2** — drives Phase 5 `target_repo` config + downstream re-run flag (si user elige b o c, Phase 8 close emite `re-run Phase 5 pre-Wave-3` action item).
6. Known constraints (stack preferido, integraciones obligatorias, compliance). **NO preguntar budget/currency — eso vive en `/proposal`.**
7. Docs disponibles (paths si D1)
   - **7.1 Origen del material:** ¿crudo (apuntes, transcripciones, emails, docs originales) o polished-by-LLM (rewrite, "polish")? Si pasaron por LLM y conservas los crudos → comparte ambos (el agent hace cross-verification).
8. **JTBD por persona:** para cada rol de usuario final, 1 línea `como {rol}, quiero {acción} para {resultado}`.
9. **Kit divergence flag:** stack SK completo / parcial / custom. Alimenta §8.3/§8.4 del brief.
10. **Design System Strategy:** SK default / Custom via Claude Design / Client DS. Alimenta §11.2.
11. **Delivery structure:** commercial type (fixed-scope / T&M / milestones / internal) + infra ownership + stakeholder authority sobre scope/deadline. **NO currency — eso es `/proposal`.**
12. **Support Context:** si hay overrides del default TimeKast (chatbot feedback + push a tech lead + no SLA formal), capturar. Si no → default aplica.

🔴 **NO preguntar "calidad vs deadline"** — es dogma hardcoded (`BR-PROJECT-001`).

#### Path D0 (from scratch)

Pregunta los 12 items en prosa conversacional, no como lista seca. Agrupa por tema cuando tenga sentido. STOP al cierre — esperar respuesta del user antes de 1.2.

#### Path D1 (con source package)

Presentar al user el bootstrap **derivado** del pre-read (1.0):

1. **Items confirmados** — `[from {file} §{X}]` con cita literal: pedir confirmación rápida (`OK / ajustar`).
2. **Items inferred** — `[INFERRED]` con razonamiento: pedir confirmación más explícita.
3. **Gaps reales** — `[OQ]`: lista compact de los items que el source NO responde. **Solo estos requieren respuesta del user.**

Format example:

```
He leído el source package y derivé el bootstrap. Confirma o ajusta:

## Confirmados (de docs)
1. Problema/North Star — [from {{source}}.md §1] "{{1-line problem statement}}". OK?
2. Stakeholders — [from {{source}}.md §2] {{Name}} (PO), {{Name}} (tech lead). OK?
5b. Factory version — [from {{target-repo}}/package.json] target = {{target_factory_version}}; current = {{current_factory_version}}.
   {{si drift detected}} ⚠️ Drift detected. ¿(a) migrate target / (b) stay pinned + Phase 5 vs target / (c) advisory mode?
... (N items)

## Inferred (no explícito pero el source sugiere)
N. Kit divergence — [INFERRED] SK completo (no veo override). OK?

## Gaps reales (necesito tu input)
M. Support Context — el source no menciona. ¿Default TimeKast (chatbot + push a tech lead + no SLA) o tienes overrides?
```

STOP al cierre. User responde gaps + confirma/ajusta. El bootstrap validado pasa a 1.2.

> **Rationale:** turns reducidos (user solo responde gaps reales), bootstrap quality eleva (derivado del source, no improvisado), consistente con pre-question check de Phase 3.

### 1.2 Procesamiento silencioso tras respuesta

#### 1.2.1 Media-type classification pre-pass

- Por cada file del source: detect extension + magic bytes heuristic
- Agrupar por strategy [methodology/intake.md §2.1](methodology/intake.md): Tier 1 (structured text / transcript / visual) / Tier 2 (`.docx`/`.pdf`/`.xlsx`/unknown → drift ticket)

#### 1.2.2 Batch planning (determinístico + adaptive single-source)

**Adaptive single-source short-circuit:** if `N(source files) == 1` AND the file is Tier 1 structured-text or transcript (not visual / not Tier 2), the orchestrator performs **inline extraction directly** per `methodology/intake.md §10` schema and writes the per-file report to `discovery-artifacts/explore-pass/001-{slug}.md`. NO agent dispatch. Skip Phase 1.2.5 cross-file reconciliation entirely (no pairs to reconcile with a single source). Proceed directly to Phase 1.3 asset sweep.

For all other cases (`N >= 2`, visual sources, mixed-media packages), apply the standard agent-dispatch flow below:

Per-agent caps (lo primero que se cumpla):

- ≤5 text files
- ≤10 images
- ≤300KB agregado

Reglas:

- **Images > 10** → auto-split en sub-batches ≤10. Cada sub-batch = 1 `dsc-intake-analyst` paralelo. No user-interrupt.
- **Text files > 5 O >300KB** → split análogo.
- Text + images del mismo source se pueden mezclar respetando caps.
- **Circuit breaker:** si math requiere **>20 agents parallel** → flag al user pre-dispatch: "Source package requiere N agents (excede heurística 20); ¿procesar todo en paralelo, partir en passes secuenciales, o recortar scope?". Único user-interrupt de Phase 1. Rationale: image batches lightweight + Anthropic API maneja 20+ concurrent sin issue empírico; cap conservador de 10 perdía paralelismo en source packages grandes.

#### 1.2.3 Spawn `dsc-intake-analyst`(s)

Single message, N tool calls. **Cada prompt DEBE anteponer:**

```
Consulta antes de empezar:
- .claude/skills/tk-discovery/methodology/intake.md (Tier 1 strategies + media-type classification + per-file output schema §10)
```

- Cada agent recibe: `file_paths` + `batch_id` + `slug` + `output_path` + `project_slug`
- output_path: `discovery-artifacts/explore-pass/{batch_id}-{slug}.md`
- Tier 2 / unknown → `intake-drift` factory-ticket a `project/factory/intake-drift-{YYYY-MM-DD}-{project-slug}-{NNN}.md`
- Ver [`.claude/agents/dsc-intake-analyst.md`](../../agents/dsc-intake-analyst.md) para contract completo.

#### 1.2.4 Post-dispatch concatenation

- Main orchestrator lee `discovery-artifacts/explore-pass/*.md`
- Orchestrator concatena los outputs per-batch y escribe `discovery-artifacts/explore-pass.md` consolidado via Write tool
- Si drift tickets emitidos (count ≥1) → surface al user; count ≥3 → escalation per [methodology/intake.md §2.1](methodology/intake.md)

#### 1.2.5 Cross-file reconciliation pass (main orchestrator)

**Skip condition:** if Phase 1.2.2 short-circuited due to `N(source files) == 1`, skip this sub-step entirely — there are no file pairs to reconcile.

**Responsabilidad del orchestrator, NO del agent.** Después del concat (cuando N ≥ 2):

1. Read `explore-pass.md` consolidado
2. Detectar contradicciones cross-file:
   - Estilo-C drift (polished docs hardening or amplifying claims relative to their raw counterparts, e.g., a polished plan document vs a raw notes/brain-dump source)
   - Decisions en file A vs file B
   - Tensions que `dsc-intake-analyst` flaggeó como hints pero no resolvió (cross-file está fuera de su scope)
3. Persistir a `discovery-artifacts/cross-file-reconciliation.md` con estructura:
   - **Contradictions detected:** pares (file A §N: claim X) vs (file B §M: claim Y) + propuesta de resolución (default firm vs Phase 3 batch)
   - **Estilo-C drift:** si hay par crudo+polished, listar 3-5 puntos donde polished endurece/amplía crudo
   - **Cross-file patterns:** patterns repetidos que sugieren decisión consolidada
4. Este archivo se vuelve input adicional para Phase 2 `dsc-freeze-map-extractor`

### 1.3 Asset sweep (siempre, independiente del mode)

```bash
# Imágenes/iconos/logos del target repo:
# (-prune corta entrada a node_modules/.next/.git/dist/build; -not -path filtra después de descender → más lento)
find <target-repo> \( -path "*/node_modules" -o -path "*/.next" -o -path "*/.git" -o -path "*/dist" -o -path "*/build" \) -prune \
  -o -type f \( -name "*.svg" -o -name "*.png" -o -name "*.jpg" -o -name "*.ico" -o -name "*.webp" \) -print | head -50

# Tokens / Tailwind / theme:
find <target-repo> \( -path "*/node_modules" -o -path "*/.next" -o -path "*/.git" -o -path "*/dist" -o -path "*/build" \) -prune \
  -o -type f \( -name "tailwind.config.*" -o -name "globals.css" -o -name "theme.ts" -o -name "theme.tsx" \) -print
```

Reportar resultados como input para §9 Branding y §11 Visual Direction. Hex colors detectados en tokens → freeze como `D{N} Paleta detectada en {path}: {hex}` (reversibility Low).

**Bulk attachments rule:** procesar TODO material relevante. Ver [methodology/intake.md §2](methodology/intake.md).

---

## Phase 2 — Freeze Map (delegated to `dsc-freeze-map-extractor`)

**Propósito:** extraer 5 buckets (Firm / Open / Contradictions / Recommendations / Post-MVP) desde explore-pass + bootstrap + cross-file-reconciliation.

**Acciones del orchestrator:**

1. Compose agent input:
   - `explore_pass_path` = `discovery-artifacts/explore-pass.md`
   - `cross_file_recon_path` = `discovery-artifacts/cross-file-reconciliation.md`
   - `bootstrap_answers` = dict con respuestas Phase 1
   - `asset_sweep_summary` = output del sweep §1.3
   - `template_path` = `.claude/skills/tk-discovery/templates/freeze-map.template.md`
   - `output_path` = `discovery-artifacts/freeze-map.md`
   - `project_slug`

2. Spawn `dsc-freeze-map-extractor` (1 Agent call, serial — no paralelo). **El prompt DEBE anteponer:**

   ```
   Consulta antes de empezar:
   - .claude/skills/tk-discovery/methodology/freeze-map.md (5-bucket schema + confidence tags + anti-drift rules)
   ```

   Ver [`.claude/agents/dsc-freeze-map-extractor.md`](../../agents/dsc-freeze-map-extractor.md) para contract.

3. Orchestrator lee el output para context propio (usará en CP1 presentation).

> **Schema canónico:** ver [methodology/freeze-map.md §3](methodology/freeze-map.md) para detalle de 5 buckets.

---

## 🛑 CHECKPOINT 1 — Post-Intake Review (inline + STOP)

**Mecanismo:** presentar plan de continuación inline en formato compact (template abajo) + STOP explícito. Esperar approval verbal del user antes de avanzar.

> **Por qué inline + STOP aquí (no Plan Mode):** CP1 es **review conversacional post-intake** — top 3 critical signals + plan corto. Ceremony de Plan Mode aquí no agrega valor; user lee + responde rápido. Reservamos Plan Mode formal para CP2 (donde la synthesis multi-fuente justifica la pausa).

**Compact mode (default):**

```markdown
## 🛑 CP1 — Post-Intake Review

### Critical signals (top 3 max)

- {signal 1 con impacto concreto}
- {signal 2}
- {signal 3}

### Plan de continuación

Phase 3 Gap Interview ({N questions). Phase 4a Tiering. Phase 4b/c per-tier. Phase 5 {SK / skip}. Phase 6+7 encadenados. CP2.

### Opciones

| #   | Acción                                          |
| --- | ----------------------------------------------- |
| 1   | continuar a Phase 3 Gap Interview               |
| 2   | ajustar Freeze Map antes de continuar           |
| 3   | ahondar en {{signal-id}} (sub-ronda focalizada) |
```

**Verbose mode** (solo si user declaró `verbose=true`): agregar coverage map 13 filas + plan detallado con subagents + invalidation rules + output expected paths.

### 🔴 Regla de invalidación del intake

Si durante CP1 el user aporta info que invalida el intake, regresar a la fase correspondiente ANTES de re-presentar plan:

- **Docs nuevos** → Phase 1 (re-clasifica) → Phase 2 → re-presenta CP1
- **Stakeholder/constraint no capturado** → actualiza intake → re-ejecuta Phase 2
- **Contradicción nueva sobre firm** → actualiza Freeze Map
- **Decisión sobre opciones del plan** → resuelve en CP1 sin rebote

Solo tras respuesta numérica explícita del user (`1`, `2` o `3`) → orchestrator ejecuta la opción correspondiente. Texto libre (`procede`, `continúa`, `ok`) NO cuenta como aprobación — re-presentar las opciones.

---

## Phase 3 — Gap Interview

**Propósito:** cerrar gaps reales con preguntas targeted.

**Reglas:**

- Mínimo: `max(3, 🟡_sections + contradictions)`. **NUNCA 0 para D1.** Input rico = mejores preguntas, no menos.
- Agrupadas por impacto (Alto / Medio / Bajo).
- UNA batch única — no trickle.

### 🔴 Pre-question check (estricto)

Para cada OQ candidata, ANTES de incluirla en la batch:

1. Buscar en `freeze-map.md §Firm Decisions` + `explore-pass.md` si source tiene respuesta explícita (cita literal).
2. **Si hay respuesta explícita:** NO ofrecer alternativas. Presentar como:
   > "El source dice: `{cita literal con path §X}`. ¿Confirmo como Firm o ajustas?"
3. **Si respuesta parcial:** presentar la parcial + preguntar solo el complement.
4. **Solo si source no dice nada:** ofrecer alternativas `(a)/(b)/(c)/(d)`.

Violar este check es **workflow error**.

### Tension sweep al cerrar cada sub-batch

Después de registrar las resoluciones de un sub-batch, ejecutar checklist **silencioso**:

1. Para cada par (Fa, Fb) dentro del sub-batch: ¿compatibles bajo todas las transiciones del sistema?
2. Para cada Fc, cruzarla con firm decisions existentes {F1..Fn}: ¿contradicción implícita o edge case no cubierto?
3. Si tensión no resuelta → clasificar como `OQ-D{N} derivada` + presentar al user mismo turn.
4. Documentar en `freeze-map.md §Derived OQs`.

**Regla:** no declarar sub-batch completo sin correr tension sweep. Si una tensión llega a Phase 7, es workflow error.

---

## Phase 4 — Feature Deep-Dive (3 sub-phases: tiering → Tier S/M parallel → Tier L dedicated)

### Phase 4a — Tiering pass (main orchestrator, 1 turn interactivo)

**Propósito:** clasificar N features en S/M/L usando criterios objetivos antes de procesar.

**Criterios objetivos:**

- **Tier S (SK-trivial, Configure-only):** feature-flag level, kit ships end-to-end, `sk-features-index` lista la feature. Acción Configure. Ejemplos: auth providers base, email templates transaccionales, notifications infra base.
- **Tier M (Extend):** kit ships + requiere custom fields/wrappers/integrations. `sk-*` skill referenciable, acción Extend. Ejemplos: RBAC role extension, invite flow custom, audit log con fields específicos.
- **Tier L (Build custom, irreversible):** kit no ships, schema-level decisions, domain-specific mechanics. Acción Build. Ejemplos: scoring engines, polymorphic schemas, domain automation, complex state machines.

**Acciones:**

1. Read `freeze-map.md` + preliminary feature list del explore-pass
2. Classify cada FT con tier + razón
3. Presentar al user tabla tier classification (compact prose + tabla) y esperar approval
4. User puede re-tier features si el agent fue demasiado conservador/agresivo

**Output:** `tier_classification` dict (FT → S/M/L) que alimenta Phase 4b/4c.

### Phase 4b — Batch sweep Tier S/M (parallel, delegated to `dsc-feature-specer`)

**Propósito:** producir specs per-feature para Tier S/M en paralelo, **todos los batches en una sola message** — wall-clock = `max(batch time)`, no `sum(batches)`.

**Acciones del orchestrator:**

1. Agrupar Tier S/M features en batches ≤5 FTs each. Asignar `batch_id` por batch (`b1`, `b2`, …).
2. Per batch, compose input contract:
   - `freeze_map_path`, `explore_pass_path`, `batch_id`, `batch_features`, `tier_classification`, `template_path` = `deep-dive.template.md`, `output_path` = `discovery-artifacts/deep-dive-batch-{batch_id}.md`
3. **Single-message multi-Agent dispatch:** spawn TODOS los batches en paralelo en una sola message — N `dsc-feature-specer` Agent calls simultáneos (uno por batch). **NO Tier L en estos batches** (el agent aborta si recibe uno). Cada prompt DEBE anteponer:

   ```
   Consulta antes de empezar:
   - .claude/skills/sk-features-index/SKILL.md (mapping canónico Tier S → sk-{skill})
   ```

   **Concurrency rules:**
   - Cap concurrente: 10 specers simultáneos.
   - Si `N(batches) > 10`: partir en 2 waves seriales internamente, sin user checkpoint entre waves (la 2nd wave dispara automáticamente al cerrar la 1st).
   - Si `N(features Tier S/M) > 50` (raro): flag al user pre-dispatch igual que el circuit breaker de Phase 1.2.2.

4. Al completar todos los batches (wave única o multi-wave), orchestrator concatena los outputs per-batch y escribe `discovery-artifacts/deep-dive.md` consolidado via Write tool.
5. **Single post-all checkpoint** (no per-batch checkpoints): `[total] features done across N batches. 1=continuar a Phase 4c Tier L / 2=revisar OQs por feature / 3=ahondar en FT-X`.

> **Rationale:** per-batch checkpoints producían `sum(batches)` wall-clock por user round-trip entre cada uno. Single-message dispatch + single checkpoint hace que un set de 20 features Tier S/M (4 batches) baje de ~32 min serial a ~8 min paralelo. Si user necesita revisar mid-flight, la opción `3=ahondar en FT-X` post-todos cubre el caso sin romper el paralelismo.

Ver [`.claude/agents/dsc-feature-specer.md`](../../agents/dsc-feature-specer.md) para contract.

### Phase 4c — Tier L dedicated sessions (main orchestrator, interactive)

**Propósito:** capturar specs detallados + sub-ronda clarificación con user para features Build-custom irreversibles.

**Por cada Tier L feature:**

1. Main orchestrator produce 7-fields entry en prosa extendida (no delegar al agent — requiere back-and-forth).
2. **Sub-ronda obligatoria:** preguntar al user **minimum 2 clarificaciones específicas, no upper bound — ask until the feature's architectural surface is resolved**.
3. **Reversibility annotation per sub-ronda Q:** orchestrator annotate cada sub-ronda question con `[reversibility: high|medium|low]` ANTES de presentar al user. Heurística:
   - **HIGH:** schema-level (column shape, polymorphism, JSONB structure) · state machine transitions (multi-state lockdown invariants, irreversible status flips) · idempotency / recomputation contract · cross-source consistency (multi-API reconciliation) · audit / versioning strategy
   - **MEDIUM:** UI exposure decisions (wizard knob vs hidden) · default values per scope (per format vs per instance)
   - **LOW:** copy strings · operational ergonomics (logs format, retry params within bounded ranges)
4. **Auto-emit `ADR-required` al lock decision:** cuando user responde a un sub-ronda con `reversibility: high` → orchestrator immediately appends row a `discovery-artifacts/adr-queue.md` (template `adr-queue.template.md`). NO defer a Phase 7 architect. **Phase 7 architect agent reads `adr-queue.md` como input** — su trabajo se vuelve validación + tradeoff articulation, NO discovery.
5. Flag `needs /docs state-machine elaboration` en el entry (no ASCII state machines aquí — solo bullets de alto nivel).
6. Append a `discovery-artifacts/deep-dive.md` en la sección Tier L.
7. Batch checkpoint `1=siguiente Tier L / 2=revisar` entre sessions.

**Cluster rule (architectural blast radius):** when two Tier L features share data model, state machine, or vendor surface (e.g., features that consume the same JSONB economics blob, or features that share an idempotency / state-machine contract), they may be addressed in a single turn. Present the union of their sub-ronda questions together. Each feature retains its full sub-ronda question count and depth. If a hard dependency requires locking one feature's decisions before posing the next feature's questions, partition the turn into sub-batches; do not split into separate turns unless the user requests it.

**Cluster vs solo guidance:**

- Foundation features (multi-role architecture, RBAC structure) — typically solo (everything inherits)
- Schema + math features that share data shape — may cluster
- Engine features that share state-machine + idempotency + vendor surface — may cluster
- Compliance / regulatory features — typically solo (regulatory complexity)

**Regla:** NO se puede saltar Phase 4c. Cada Tier L feature necesita su sub-ronda — clustering is about turn structure, not question count.

### Workflow-drift candidates (post-Phase-4)

Si al cerrar Phase 4 un FT Tier L tiene Edge bucket >500 chars, O ≥2 FTs Tier L sugieren el schema 7-fields no basta → surface como `workflow-drift` factory-ticket candidate (orchestrator surfacea al user en Phase 8 close, user decide emitir).

> **Schema canónico + tiering rules:** ver [methodology/deep-dive.md §11](methodology/deep-dive.md).

---

## Phase 5 — SK Leverage Analysis (CONDICIONAL)

**Si `SK_ACTIVE=false` → SKIP.**

**Si `SK_ACTIVE=true`:**

1. Compose input contract para `dsc-kit-analyst`:
   - `freeze_map_path`, `deep_dive_path`, `target_repo`, `template_path` = `sk-leverage.template.md`, `output_path` = `discovery-artifacts/sk-leverage.md`, `project_slug`
2. Spawn `dsc-kit-analyst` (1 Agent call, serial). **El prompt DEBE anteponer:**

   ```
   Consulta antes de empezar:
   - .claude/skills/sk-features-index/SKILL.md (catálogo canónico de sistemas shipped por el kit)
   - .claude/skills/tk-discovery/methodology/kit-leverage.md (SK leverage analysis schema)
   ```

3. Agent escribe output directo (tiene `Write` tool). Orchestrator lee el output post-completion.
4. SK Drift Tickets → `project/factory/sk-drift-{YYYY-MM-DD}-{project-slug}-{NNN}.md`

Ver [`.claude/agents/dsc-kit-analyst.md`](../../agents/dsc-kit-analyst.md) + [methodology/kit-leverage.md](methodology/kit-leverage.md).

---

## Phase 6 — Synthesis (orchestrator-direct, no agent spawn)

**Propósito:** ensamblar brief completo (§1-§11) escribiendo directo a path canónico desde el primer write — sin draft intermedio, sin agent spawn.

**Por qué orchestrator-direct:** post-Phase 5, el orchestrator ya tiene en context `freeze-map.md` + `deep-dive.md` + `sk-leverage.md` + `cross-file-reconciliation.md` (+ `challenge-pass.md` si se re-synth post-Phase 7). Re-ensamble cross-secciones es Write tool work + structure templates — NO requiere fresh-agent reasoning. Spawn agent acá costaba ~40 min + double-context (agent + orchestrator) sin ganancia.

**Phase 6 corre dos veces a lo largo del workflow.** First-pass (6.1) precede a Phase 7 Challenge Pass; re-synth (6.2) corre solo si Gap Round 2 introdujo cambios materiales. Mismas mecanismos (Write tool, quantitative gate), distintos inputs y momento.

### 6.1 First-pass synthesis

**Inputs:**

- `discovery-artifacts/freeze-map.md`
- `discovery-artifacts/deep-dive.md`
- `discovery-artifacts/sk-leverage.md` (si SK_ACTIVE)
- `discovery-artifacts/cross-file-reconciliation.md` (si Phase 1.2.5 corrió)
- Template: `.claude/skills/tk-discovery/templates/00_DISCOVERY_BRIEF.template.md`

**Acciones:**

1. **Write canónico directo:** `project/{discovery-dir}/00_DISCOVERY_BRIEF.md` (NO draft path). Orchestrator usa Write tool, ensambla §1-§11 según template.
2. **Quantitative gate inline post-write:** contar FT/BR/entities/pantallas vs WIP esperado. Threshold ≥90%. Si FAIL → orchestrator re-ensambla la sección afectada (Write tool sobreescribe in-place), re-gate. NO re-spawn de agent.

**Output:** brief canónico v1 — input para Phase 7 Challenge Pass.

### 6.2 Re-synth post-Phase-7 (condicional, single source of truth)

> **Spec note:** Phase 7.5 referencia esta sub-fase. Toda la mecánica del re-synth post-GR2 vive aquí — no duplicar en Phase 7. Phase 7.5 simplemente delega a Phase 6.2.

**Trigger:** solo si Gap Round 2 (Phase 7.4) introdujo **cambios materiales** al brief.

**"Cambios materiales" = ANY de:**

- ≥3 firms modificados respecto al brief v1
- ≥1 firm que afecta §1 (Problem/North Star), §3 (Scope MVP), §6 (Data model / entidades) o §8 (Delivery / commercial / tiering) del brief
- ≥1 reclasificación MoSCoW (M ↔ S ↔ C ↔ W)

Si ninguna de las anteriores aplica → skip 6.2, brief v1 sigue siendo canonical.

**Inputs:** los de 6.1 + `discovery-artifacts/challenge-pass.md` (now persisted) + GR2 resolutions.

**Strategy selection (Edit-in-place vs Write completo):**

Calcular `delta_pct = LOC_changed_lines / LOC_total_brief` (estimación rápida, no exact).

| Condición                                                                                                       | Strategy                                                                                                                             |
| --------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------ |
| `delta_pct < 30%` AND no architectural-firm change (no §6 data model, no §1 problem statement, no §3 MVP scope) | **Edit** (sección por sección, Edit tool sobre el path canónico) — 5-10× más rápido en output tokens, menor risk de regresión del v1 |
| `delta_pct >= 30%` OR architectural-firm change                                                                 | **Write completo** (re-ensamble §1-§11) sobre `project/{discovery-dir}/00_DISCOVERY_BRIEF.md`                                        |

**Acciones:**

1. Determinar strategy per la tabla de arriba.
2. Aplicar Edit (sección por sección) O Write (full re-synth).
3. Mismo quantitative gate que 6.1 (FT/BR/entities/pantallas ≥90%). Si gate FAIL post-edit → re-ensamble de la sección afectada.

**Output:** brief canónico v2 — sobreescribe v1 in-place.

> **Note:** Phase 8 does NOT copy a draft to a canonical path — the canonical brief is written directly to `project/{discovery-dir}/00_DISCOVERY_BRIEF.md` from Phase 6. No intermediate draft path exists.

> **Edge case CP2 reject:** canónico queda con data del run rechazado. Mitigación: re-correr `/discovery` sobreescribe. Scenario raro, reversible.

---

## Phase 7 — Challenge Pass (3 agents PARALELO + persist + Gap Round 2)

### 7.1 Parallel dispatch

Single message, 3 `Agent` tool calls en paralelo + 1 `ToolSearch` call para pre-cargar primitivas de Plan Mode (CP2 las requiere). **Cada prompt DEBE citar paths explícitos de skills relevantes** (CC.md §2 — subagents no reciben el listado de skills por description injection).

**Pre-dispatch:** orchestrator escanea el brief draft para identificar dominios mencionados (crons, PWA, tokens, MCP, etc.) y agrega los `kb-*` condicionales a la lista del `architect`.

**Co-dispatch tool pre-load:** en la misma message del Phase 7 dispatch, agregar `ToolSearch select:EnterPlanMode,ExitPlanMode`. Para cuando los 3 agents terminan + GR2 procesa, las primitivas de Plan Mode ya están cargadas → CP2 entra inmediatamente sin "waiting for tools". Ahorra latencia menor pero elimina UX gap entre fin de Phase 7 y entrada a CP2.

```
Agent(subagent_type=architect, prompt="
Consulta antes de empezar (paths repo-relative):
- .claude/skills/sk-features-index/SKILL.md (baseline kit shipped)
- .claude/skills/kb-ssot-registries/SKILL.md (registry/SSOT patterns)
- .claude/skills/kb-db/SKILL.md (data model risks)
- .claude/skills/kb-api/SKILL.md (action/route patterns)
- .claude/skills/kb-security/SKILL.md (auth/RBAC/Zod risks)
[Condicional según dominios del brief — el orchestrator decide pre-dispatch:]
- .claude/skills/kb-cron-jobs/SKILL.md (si scope toca crons/jobs)
- .claude/skills/kb-pwa/SKILL.md (si scope toca PWA / SW)
- .claude/skills/kb-design-tokens/SKILL.md (si scope toca tokens/DS)
- .claude/skills/kb-mcp/SKILL.md (si scope toca MCP servers)

Audit <draft path> for irreversible architectural decisions, tech risks, constraints bypassed. Don't produce ADR — flag risks only.
")

Agent(subagent_type=product-owner, prompt="
Consulta antes de empezar:
- .claude/skills/sk-features-index/SKILL.md (qué shippa el kit — para distinguir scope genuino nuevo vs feature-flag toggle del kit)

Review <draft path> for user-intent preservation, scope drift, MVP boundary integrity, MoSCoW soundness.
")

Agent(subagent_type=project-planner, prompt="
Consulta antes de empezar:
- .claude/skills/sk-features-index/SKILL.md (kit-shipped systems aceleran timeline; features Build-from-scratch tier L pesan en estimación)
- .claude/skills/tk-discovery/methodology/deep-dive.md (semantics de Tier S/M/L para validar realismo del descope plan)

Review <draft path> for timeline realism, hidden dependencies, premature commitments, rollback paths.
")
```

### 7.2 Persist findings

Orchestrator consolida los 3 outputs en `discovery-artifacts/challenge-pass.md` con 3 sub-secciones (architect / PO / planner verdicts + findings HIGH/MED/LOW). Esto permite que el orchestrator lo consuma como input explícito post-Gap-Round-2 al re-ensamblar el brief (Phase 7.5).

### 7.3 Gate de veredicto (pre-Gap-Round-2)

Si hay cualquier `🔴`:

1. **architect 🔴** → ADRs requeridos. Listar en CP2 §"ADRs pendientes pre-backlog" con deadline per ADR.
2. **product-owner 🔴** → escalar findings High como "PB{N} pre-backlog renegotiation". Bloquean `/backlog`.
3. **project-planner 🔴** → **bloquear CP2** hasta que draft contenga §8.7 Descope Plan aterrizado (tiering S/M/L + triggers) + §8.8 Post-MVP milestones.

Re-correr gate cuantitativo post-edit si se re-sintetiza.

### 7.4 Gap Round 2 (stakeholder decisions)

**🔴 OBLIGATORIO si agents surfacean HIGH findings que requieren decisión del stakeholder.**

Filtrar HIGH findings en 2 buckets:

- **(a) Stakeholder decisions** (requieren el user, no implementation): ej ADR architectural preference, descope strategy under timeline pressure, North Star quantitative metric, vendor selection between committed alternatives
- **(b) Implementation decisions** (ADRs, gates, patterns — orchestrator/tech lead los resuelve): ej domain engine golden-fixture test gate pre-release, idempotency strategy, partitioning policy

Compose mini-Gap-Round-2 batch único con bucket (a) questions. Pre-question check estricto (no ofrecer alternativas si source responde). User responde → orchestrator updatea brief draft + freeze-map Phase 3 Resolutions section + persiste a `discovery-artifacts/`.

**CP2 es estrictamente "approve close"**, nunca aprobar decisiones tácitas que debieron ser Gap Round 2.

Si no hay HIGH stakeholder decisions → skip Round 2, ir directo a CP2.

### 7.5 Re-synthesize if needed → see Phase 6.2

Si Gap Round 2 introdujo cambios materiales al brief, el re-synth se ejecuta per **Phase 6.2 Re-synth post-Phase-7 (condicional, single source of truth)** — esa sub-fase es el SSOT del re-synth path (criterio de "cambios materiales", strategy Edit-vs-Write, quantitative gate). No duplicar mecánica acá.

---

## 🛑 CHECKPOINT 2 — Pre-Close Review (Plan Mode formal)

**Mecanismo:** **Plan Mode FORMAL obligatorio.** Orchestrator invoca `EnterPlanMode` (cargar tool si deferred), redacta synthesis estructurada (§CP2.synthesis abajo) en plan buffer, luego `ExitPlanMode` para approval del user.

> **Por qué Plan Mode aquí (no inline + STOP):** CP2 = **synthesis multi-fuente crítica** — consolida `challenge-pass.md` (3 agentes) + Gap Round 2 + freeze-map updates + descope plan + drift report. La pausa formal del Plan Mode forza al agente a dejar de generate-and-go y producir synthesis genuina (vs checklist perfunctorio). Este es el último gate antes de close — la ceremony se gana el costo.

> **Pre-load:** ya realizado en Phase 7.1 dispatch (co-dispatch tool pre-load). Si por algún motivo Phase 7 no se ejecutó este turn, cargar acá: `ToolSearch select:EnterPlanMode,ExitPlanMode`.

### CP2.synthesis — structured plan content (rich, NOT checklist)

El plan buffer en Plan Mode debe contener **synthesis genuina**, no checklist mecánico. Estructura mínima (6 secciones):

#### 1. Findings synthesis (¿qué surfaced y qué importa?)

Lectura interpretativa de los 3 agentes + GR2:

- **Architect HIGH** → ¿qué decisions schema-level quedaron blindadas vs cuáles necesitan ADRs? Agrupa por blast radius.
- **PO HIGH** → ¿user-intent preservado? ¿scope drift catched? ¿MVP boundary íntegra post-GR2?
- **Planner HIGH** → ¿timeline aterrizable post-descope? ¿critical path libre de single-thread bottlenecks?

NO repetir verdicts table — interpretar.

#### 2. Cross-cutting impacts

Identificar findings que se afectan mutuamente (ej: "ADR-001 monolithic JSONB bloquea L1 + L4 + L6 docs entries simultáneamente — sequencing dependency"). Listar 3-5 cross-impacts críticos.

#### 3. Sequencing rationale

¿En qué orden se deben atacar los ADRs + remaining OQs en `/docs`? ¿Por qué? Justificar dependencies.

#### 4. Risk-weighted prioritization

Top 3 risks post-discovery con mitigation status (firm in brief vs deferred a `/docs` vs unresolved).

#### 5. Handoff packets per downstream phase

Qué necesita cada fase downstream:

- **`/proposal`:** scope locked + commercial terms ready?
- **`/docs`:** ADR queue + Tier L state-spec hints + golden fixtures list
- **`/design`:** §11 Visual Direction Seeds + design system strategy + reference assets inventory
- **`/backlog`:** SK leverage % + descope plan triggers + critical path features first

#### 6. Plan de cierre Phase 8 (action items — compact default)

```markdown
## 🛑 CP2 — Pre-Close Review

### Quantitative gate

FT {X/Y} · BR {X/Y} · Entities {X/Y} · Pantallas {X/Y} — ✅ / 🔴

### Challenge Pass + Gap Round 2

architect {✅/⚠️/🔴} · PO {✅/⚠️/🔴} · planner {✅/⚠️/🔴}
Stakeholder decisions resolved: {N/M}
ADRs identificados: {N}

### Drift Report

{items vs source: harmless / risky / unauthorized count}

### Plan de cierre

1. Brief canónico ya existe (escrito directo en Phase 6) — verificar path
2. Generar `project-config.md` con BR-PROJECT-001 hardcoded
3. Cleanup transitionals (batch files + explore-pass/ subdirectory)
4. Retention durable consolidados en `discovery-artifacts/`
5. Surface factory-tickets si hay
6. Offer user: recopilar notas externas para factory-tickets
7. NO commit (GIT.md §2 requiere autorización explícita)
```

**Verbose mode:** ampliar cada sección con detalle (debugging / deep-review only).

---

## Phase 8 — Close (post-approval)

**Pre-requisito:** CP2 aprobado via `ExitPlanMode` (Plan Mode formal — ver CP2 §Mecanismo).

**Acciones:**

1. **Brief canónico ya escrito en Phase 6** (`project/{discovery-dir}/00_DISCOVERY_BRIEF.md`) — verificar que existe + último contenido refleja CP2 approved. Si Phase 7.5 corrió post-CP2 (raro), re-write una vez más in-place.

2. **GR2-traceability check (precondición pre-stripping):** for every Gap Round 2 stakeholder decision resolved during Phase 7.4, verify it is reflected as a Firm in the brief proper (in §1, §3, §6, etc.) AND/OR as a Firm row in `freeze-map.md`. If any GR2 decision exists ONLY in the brief's `§Resolved During Discovery` section (journey form) → elevate it to Firm form FIRST. Without this check, the next stripping step would erase the decision.

3. **Strip workflow-history narrative from durable artifacts** (post-CP2-approval, pre-archival):
   - **Brief:** delete the entire `§Resolved During Discovery` section. Audit trail of how decisions arrived is preserved in git log + `challenge-pass.md` (now archived per step 5).
   - **`freeze-map.md`:** collapse `§Phase 3 Resolutions` and `§Phase 7 GR2 Resolutions` into a single line: `> Last canonical update: {date} post {phase}. Full audit trail in challenge-pass.md (archived).`
   - **`adr-queue.md`:** drop the "Phase 4c session" column from the table. Keep `(ADR-NN, Topic, Locked decision, Why ADR, Status)`.
   - **`deep-dive.md` Tier L entries:** drop the `> Sub-ronda captured: Q1=A · Q2=A · Q3=C` header lines. Replace with `> ADRs flagged: ADR-X, ADR-Y, ADR-Z` if ADRs were emitted; otherwise drop entirely.

4. **Generar project-config.md** usando template:
   - §8.1 Stakeholders + §8.2 Team members OBLIGATORIOS
   - §10 incluye `BR-PROJECT-001` hardcoded
   - §14 Delivery Model **sin currency** (eso es `/proposal`)
   - Pipeline Status: Discovery ✅, resto ⬜

5. **Archive audit-only artifacts + cleanup transitional artifacts** (orchestrator ejecuta inline post-step-3 stripping):
   - Orchestrator mueve los 3 audit artifacts (`challenge-pass.md`, `cross-file-reconciliation.md`, `explore-pass.md`) a `project/{discovery-dir}/discovery-artifacts/_audit/` (audit trail preservado, fuera del path consumido por downstream phases).
   - Orchestrator elimina los batch intermedios `deep-dive-batch-*.md` (ya concatenados a `deep-dive.md`).
   - Orchestrator elimina el subdirectory `discovery-artifacts/explore-pass/` (per-agent reports ya consolidados a `_audit/explore-pass.md`).

6. **Retention policy:** durables consumed by downstream phases (`/docs`, `/design`, `/backlog`, `/implement`) live in `discovery-artifacts/` top-level. Audit-only artifacts live in `discovery-artifacts/_audit/` (preserved for retroactive audit but not loaded by downstream agents).

7. **Factory-tickets surface:** si hay `intake-drift` / `sk-drift` / `workflow-drift` candidates en `project/factory/` → mostrar resumen al user ("📩 N tickets en `project/factory/*.md`"). Workflow-drift candidates requieren confirmation explícita del user antes de emitir.

8. **Offer notes harvest:** preguntar al user "¿Quieres compartir tus notas externas para factory-ticketizar gaps reales del workflow?" — opt-in. Si sí → user pasa notas inline → orchestrator las procesa y emite tickets correspondientes.

9. **NO auto-commit.** Sugerir commit con autorización explícita del user (`GIT.md §2`).

---

## Archivos de output

### Durable — consumed by downstream phases (`/docs`, `/design`, `/backlog`, `/implement`)

| Path                                                         | Lifecycle                                                                                                        |
| ------------------------------------------------------------ | ---------------------------------------------------------------------------------------------------------------- |
| `project/{discovery-dir}/00_DISCOVERY_BRIEF.md`              | **Durable** — SSOT primario para `/docs` (escrito directo en Phase 6)                                            |
| `project/{discovery-dir}/project-config.md`                  | **Durable** — config always-on                                                                                   |
| `project/{discovery-dir}/discovery-artifacts/freeze-map.md`  | **Durable** — firm decisions trazables                                                                           |
| `project/{discovery-dir}/discovery-artifacts/deep-dive.md`   | **Durable** — 7-fields FT specs consumidas por `/docs` + `/backlog`                                              |
| `project/{discovery-dir}/discovery-artifacts/sk-leverage.md` | **Durable** — kit leverage map para `/backlog` (solo si SK_ACTIVE)                                               |
| `project/{discovery-dir}/discovery-artifacts/adr-queue.md`   | **Durable** — ADRs flagged at Phase 4c sub-ronda time (reversibility=high), consumed by `/docs` for ADR drafting |
| `project/factory/*.md`                                       | **Durable** — factory-tickets (`intake-drift`, `sk-drift`, `workflow-drift`)                                     |

### Audit-only — archived at Phase 8 close (preserved for retroactive audit, NOT loaded by downstream agents)

| Path                                                                              | Lifecycle                                                                                   |
| --------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------- |
| `project/{discovery-dir}/discovery-artifacts/_audit/challenge-pass.md`            | **Audit-only** — Phase 7 findings + 3-agent verdicts (moved here at Phase 8 step 5)         |
| `project/{discovery-dir}/discovery-artifacts/_audit/cross-file-reconciliation.md` | **Audit-only** — Phase 1.2.5 polished-vs-raw drift detection (moved here at Phase 8 step 5) |
| `project/{discovery-dir}/discovery-artifacts/_audit/explore-pass.md`              | **Audit-only** — consolidated per-file extraction trail (moved here at Phase 8 step 5)      |

### Transitional — cleaned at Phase 8 close

| Path                                                               | Lifecycle                                                                     |
| ------------------------------------------------------------------ | ----------------------------------------------------------------------------- |
| `project/{discovery-dir}/discovery-artifacts/explore-pass/*`       | **Transitional** — per-agent intake reports (eliminados al cierre de Phase 8) |
| `project/{discovery-dir}/discovery-artifacts/deep-dive-batch-*.md` | **Transitional** — batch intermedios (eliminados al cierre de Phase 8)        |

---

## Invalidation handling cross-phase

### Source-arrival post-CP1 (incremental intake)

If new source material arrives after CP1 has been presented (e.g., the user obtains additional documents from a stakeholder mid-Phase-3), the orchestrator computes the impact on the existing freeze-map BEFORE deciding how to incorporate it:

1. **Compute delta:**
   - `new_firms_to_add` + `firms_to_modify` + `firms_to_remove`
   - `new_OQs_introduced` + `OQs_to_resolve` (from new evidence)
   - `new_contradictions` + `contradictions_to_resolve`
   - `delta_pct = total_changes / current_freeze_map_firm_count`

2. **Apply threshold-based decision:**
   - **`delta_pct < 30%`** → orchestrator does in-place patch (`Edit` tool on `freeze-map.md` directly): append new Firms, move resolved OQs to a new `§Phase 3 Resolutions` row, update specific Contradictions. No agent re-dispatch. Typical cost: 2-3 minutes orchestrator work.
   - **`delta_pct >= 30%`** → STOP and prompt the user:

     ```
     Source nuevo afecta {X%} del freeze-map (umbral 30%).
     Above this threshold, in-place patches risk inconsistencies between Firms.

     Recommend re-running Phase 2 from scratch (`dsc-freeze-map-extractor` regen, ~10 min agent compute) for a coherent freeze-map.

     Procedo con regeneración completa, o prefieres patch incremental (con riesgo de inconsistencia)?
     ```

   - User decides. The threshold (30%) is heuristic; the user override is authoritative.

3. **After patch or regen:** re-run cross-file reconciliation (Phase 1.2.5) ONLY if `N(source files)` is now ≥ 2. Update `cross-file-reconciliation.md` accordingly.

### Firm-vs-resolution invalidation

Si orchestrator detecta que una resolution downstream invalida un Firm upstream (ej: Phase 4 Tier L sub-ronda revela Firm F-N del Freeze Map era incorrecto):

**Detección objetiva:** re-read del Firm citado vs nueva resolution. Si contradicen literal → invalidation confirmed.

**Prompt al user (nunca automático):**

```
⚠️ Contradicción detectada entre Firm F{N} (Phase 2) y resolution en Phase {X}.

F{N}: {quote}
Phase {X} reveals: {evidence}

Opciones:
1. Backtrack → regresar a Phase 2, update Firm F{N}, re-run Phase 3-{X}
2. Override → mantener Firm, documentar dissent en §Drift Report del brief
3. Resolve now → proponer nueva Firm F{N}', re-run solo Phase {X} con contexto actualizado
```

User decide. Si backtrack → orchestrator salta a Phase 2 con invalidation flag + cambios aplicados + re-corre phases intermedias.

---

## Subagent delegation (resumen)

| Fase | Subagent                                          | Paralelismo                                                | Cuándo                                                                                   |
| ---- | ------------------------------------------------- | ---------------------------------------------------------- | ---------------------------------------------------------------------------------------- |
| 1    | `dsc-intake-analyst` (N parallel ≤10)             | Paralelo (cap 10) — batching determinístico per-agent caps | Siempre                                                                                  |
| 2    | `dsc-freeze-map-extractor`                        | Serial                                                     | Siempre                                                                                  |
| 4b   | `dsc-feature-specer` (N parallel per batch)       | Paralelo                                                   | Siempre (Tier S/M only)                                                                  |
| 5    | `dsc-kit-analyst`                                 | Serial                                                     | Solo si SK_ACTIVE=true                                                                   |
| 6    | _(none — orchestrator-direct Write)_              | —                                                          | Synthesis sin agent spawn                                                                |
| 7    | `architect` + `product-owner` + `project-planner` | Paralelo                                                   | Siempre · `architect` consume `adr-queue.md` como input — valida en lugar de redescubrir |

**Agents scoped a `/discovery` tienen prefix `dsc-*`** per convención de taxonomy (ver CLAUDE.md §Convenciones). Generic agents (architect/PO/planner) no llevan prefix.

---

_TimeKast Factory — tk-discovery workflow (documentation family)_
