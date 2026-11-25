---
name: power-platform
description: "Use when a Power Platform project task (Power Apps Canvas, Power Automate, SQL Server, Dataverse) calls for method or touches more than one layer: starting a new app, \"I want to build an app\", an app idea, \"where did I stop\", \"what is the next step\", the /pp-en pipeline, an end-to-end feature (screen + flow + database), \"the number does not match\", \"a user from one unit sees another unit's data\", \"it is slow\", auditing the whole app, the GOAL.md queue, parallel subagents, promoting DEV/HML/PRD (solution, environment variable, pac CLI) or \"is it ready?\". Coordinates the guided new-app pipeline (/pp-en:new through /pp-en:publish, one session per stage, STATE.md; then /pp-en:change) and, on an existing app, routes to the domain skill and closes with validators and evidence. Do not use for a one-off formula question or a single screen tweak (use `powerapps-canvas`), an isolated flow (use `power-automate`), an isolated procedure or DDL (use `sql-procedures`) or table modeling (use `dataverse`)."
argument-hint: "[new|where-am-i|feature|investigate|audit|promote|ready] [target]"
user-invocable: true
---

# power-platform — orchestrator

Two jobs. **New app:** coordinates the guided `/pp-en:*` pipeline, from idea to published app, one
stage per session, with `STATE.md` saying where the project is and what the next command is.
**Existing app:** decides what to load, who executes and when it is done on work that spans more
than one layer. The knowledge of Power Fx, YAML, flows, procedures and tables lives in the domain skills.

## Non-negotiable rules

1. **Read the project before acting** (step 1). Do not write a screen, flow or procedure without an
   active track and known environment names.
   Why: guessed column and procedure names were the no. 1 cause of rework in the reference projects.
2. **One pipeline stage per session, in order.** `estado.py` checks the order and gives the next
   command; you do not invent another one or move on to the next stage in the same conversation.
   Why: everything the next stage needs is on disk, and a clean context does not drag old decisions along.
3. **One data track per project.** Switching tracks requires an ADR (`assets/adr-template.md`).
   Why: the "frozen" track got edited and the "active" one fell weeks behind.
4. **Dependency order: data → (frontend ∥ automation) → QA.** No screen starts before its
   table/procedure exists and is in `AS-BUILT-NAMES`.
   Why: the screen is the consumer; writing the consumer first locks in names that do not exist yet.
5. **✅ without evidence does not count.** Every completed task carries command + output + date.
   Evidence expires when the file changes after it.
   Why: a ✅ task had regressed because a generator was rewritten and wiped out the fix.
6. **Green only counts if the validator proved it can fail.** `0 error(s)` from a validator that did
   not read the file format is a false green (`references/final-gate.md`).
   Why: a validator returned `0 error(s)` on plain-YAML screens because it only read fenced blocks.
7. **A generator never writes over the baseline.** Generator output goes to `dist/`; the file pasted
   into the designer is the baseline.
   Why: regenerating erased the only environment evidence that existed.
8. **A decided default is not reopened silently.** What is in `references/default-decisions.md`
   stands; diverging requires an ADR.
   Why: without a record, the technology changed several times and nobody knew why.
9. **An agent's delivery is a hypothesis until you check it.** Run the validator, open the file,
   reproduce the strongest findings before moving on or reporting.
   Why: "the backend is empty" and "the variable is never initialized" both came back as fact, and both were false.
10. **No environment, server, `dev*` table or literal GUID in any artifact.** Environment variable +
    connection reference (`references/alm-environments.md`).
    Why: a development source mixed with production made the KPI diverge from the gallery.

## Workflow

### Step 1 — Read the project

1. **`STATE.md`** (searched from the current folder upward). If it exists, the project is in the
   pipeline. Run `python "${CLAUDE_PLUGIN_ROOT}/skills/power-platform/scripts/estado.py" mostrar` before anything else.
2. `power-platform.config.json` (format in `docs/CONFIG.md` of the plugin repository): note
   `trilha_dados`, `pastas`, `nomes_as_built`. No config outside the pipeline: say "running with
   defaults" and offer to create one from `assets/power-platform.config.example.json`.
3. `00-READ-ME-FIRST.md`: the active track per layer. If it contradicts the config, **stop and resolve**
   before editing.
4. `references/default-decisions.md`; the `GOAL.md` queue, if any (check on disk which folder is
   actually being edited, not just what the document says); `AS-BUILT-NAMES`, if the task touches data.

### Step 2 — Route

| Signal in the request | Do | Who executes |
|---|---|---|
| "I want to build an app", an app idea, starting from scratch | explain the pipeline in 4 lines and tell them to run `/pp-en:new <idea>` | the user runs the command |
| "where did I stop", "what is the next step", "continue" with `STATE.md` | `estado.py mostrar` and return the "Next step" block | you |
| a request for one stage (brainstorm, design, mockups, prototype, architecture, build, test, uat, publish) | point to the `/pp-en:<stage>` command in a new session; `estado.py` says whether it is in order | the user runs the command |
| a list of changes on an app already published by the kit (or with the kit's config) | point to `/pp-en:change <list>` in a new session | the user runs the command |
| "how do I", "which formula", a screen, pasteable YAML | skill `powerapps-canvas` and answer directly | you |
| empty gallery, "2,000" counter, `CountRows`, date filter | SQL → `powerapps-canvas` (+ `sql-procedures`); Dataverse → `dataverse` | you |
| "paste this flow", Try/Catch, HTTP, `$batch`, log | `power-automate` (+ `powerapps-canvas` on the app side) | you |
| procedure, DDL, computed column, DBA | `sql-procedures` | you |
| table, Choice, Lookup, security role, `AS-BUILT-NAMES` | `dataverse` | you |
| "the number does not match", "it is slow", "it does not refresh" | `references/investigate-mode.md` **before proposing code** | you |
| "a user from one unit sees another unit's data" | `references/investigate-mode.md`; SQL → `power-automate` + `sql-procedures`; Dataverse → `dataverse` | you |
| a feature that touches screen + flow + database (existing app) | `references/protocol.md` | 1 agent per layer, if worth it |
| "audit the whole app", ≥ 3 screens | `references/subagents.md` + `prompts/*.md` | fan-out by discipline |
| `GOAL.md` queue outside the pipeline, "next task" | `references/goal-queue-mode.md` | you, in a loop |
| "promote to HML/PRD", solution, `pac` | `references/alm-environments.md` | you + a human in the environment |
| "is it ready?", "can we deliver?" | `references/final-gate.md` | you |
| "why did we do it this way", a process lesson | `references/safeguards.md` | you |

### Step 3 — The new-app pipeline

Detail, diagram and files of each stage: `references/pipeline.md`. Banner, checkpoint and next-step
format, the same in all: `references/output-format.md`.

| # | Command | Who executes | Delivers |
|---|---|---|---|
| 1 | `/pp-en:new` | Orchestrator | folder, git, config, `STATE.md` |
| 2 | `/pp-en:brainstorm` | Brainstorm Agent (the session talks) | requirements, features and MVP (`prd.md`) |
| 3 | `/pp-en:design` | Branding Designer Agent (the session talks) | colors, fonts, components, identity (`ux-design-system.md`) |
| 4 | `/pp-en:mockups` | subagent `pp-en:mockups-agent` + script | screens, navigation, loading, errors, empty states; images |
| 5 | `/pp-en:prototype` | subagent `pp-en:prototype-agent` | clickable prototype; approved or back to design |
| 6 | `/pp-en:architecture` | `pp-en:architecture-agent`, then `pp-en:sql-agent` ∥ (SQL track) | data model, permissions, integrations, procedures, `GOAL.md` |
| 7 | `/pp-en:build [app\|flows]` | `pp-en:canvas-agent` ∥ `pp-en:automate-agent`, one per file group | screens, flows and the integration, one wave per session |
| 8 | `/pp-en:test` | subagent `pp-en:qa-agent` | validators + script to run in the environment; a failure goes back to build |
| 9 | `/pp-en:uat` | Orchestrator, with the user | UAT and sign-off from real users |
| 10 | `/pp-en:publish` | Orchestrator | production, manual and technical guide |

`/pp-en:progress` shows the panel at any time. Stages only run by the user's command (they do not
invoke themselves): outside them, your role is to say which command to run.

### Step 4 — Protocol (existing app, task with more than one step)

Map → Plan → Execute → **Validate** → Report (`references/protocol.md`). Map with the command that
found each thing; plan in up to 5 steps saying what will **not** be done; execute in dependency
order with a template and canonical block; validate at the final gate; report what changed, how to
apply it, the warnings and what was left out.

### Step 5 — Modes

- **Investigate** (`references/investigate-mode.md`): chain screen → formula → source → flow →
  procedure → data, one hypothesis at a time, proof before the fix.
- **`GOAL.md` queue** (`references/goal-queue-mode.md`): the next 🟢 whose previous wave closed; on a 🔴,
  stop and say what to do in the environment. In the pipeline, `/pp-en:build` is what walks the queue.
- **Promote** (`references/alm-environments.md`): what goes by paste × by solution.

### Step 6 — Subagents

From the pipeline: the `pp-en:*-agent` agents, called by the stages. Outside it: open a subagent only
when the work is **independent** and needs **wide reading**; disjoint scopes, all in one message, the
one who delegates collects and checks. A subagent does not talk to the user. Detail: `references/subagents.md`.

### Step 7 — Final gate

Run **all** the validators of the layers touched and the checklist in `references/final-gate.md`.
Screen or flow changed: the final proof is pasting into Studio/the designer, or recording 🔴 for the human.

## References

| File | When to read |
|---|---|
| `references/pipeline.md` | new app: the diagram, the 10 stages, the loops back, `/pp-en:change` after publishing, where each file lives |
| `references/output-format.md` | every `/pp-en:*` stage: banner, checkpoint, next step |
| `references/default-decisions.md` | step 1, always: decided defaults (A/C/T/F/B/N/P) |
| `references/brainstorm-modes.md` | `/pp-en:brainstorm`: the 4 modes (interview, people, problem, round table) and the personas |
| `references/brainstorm.md` | `/pp-en:brainstorm`: how to run it and the question script (blocks 0 to 11) |
| `references/navigation.md` | `/pp-en:design`: the 5 navigation patterns, previews and which to recommend |
| `references/design-system-and-screens.md` | `/pp-en:design`, `/pp-en:mockups`: design system, inventory, frame |
| `references/mockups.md` | `/pp-en:mockups`: OpenAI key, variable model, spec, errors |
| `references/technology-matrix.md` | `/pp-en:architecture`: Dataverse × SQL Server, Power BI, SharePoint |
| `references/mockup-load.md` | `/pp-en:architecture`: mockup load of the tables (`.xlsx` for Dataverse to infer the types, `INSERT` for the DEV SQL) and checking the types Dataverse created |
| `references/dataverse-builder.md` | `/pp-en:architecture`, Dataverse: the flow that creates tables, typed columns, relationships and the mockup load through the Web API (`--flow`) |
| `references/protocol.md` | existing app: multi-layer feature, phase exit criterion |
| `references/goal-queue-mode.md` | `GOAL.md` queue, states, evidence, gates per wave |
| `references/investigate-mode.md` | "the number does not match", slowness, "it does not refresh" |
| `references/subagents.md` | before opening any subagent; judging the delivery (accepted, revision, escalated) |
| `references/models.md` | model profiles (who thinks, who executes), how to switch and how to measure |
| `references/visual-verification.md` | `/pp-en:design`, `/pp-en:prototype`: photograph the page and look before showing it |
| `references/alm-environments.md` | solution, DEV/HML/PRD, environment variable, `pac`; `/pp-en:uat`, `/pp-en:publish` |
| `references/safeguards.md` | track, environment, generator × baseline, evidence, doc × disk, Git |
| `references/final-gate.md` | before saying "ready"; known false greens |
| `prompts/ux.md` `dev.md` `performance.md` `data.md` `flow.md` `sql.md` | audit of an existing app (fan-out, each as `pp-en:research-agent`) |
| `assets/*-template.*` | templates the stages copy: raw idea, PRD, design system, inventory, mockups, prototype, mockup load, architecture, ADR, `GOAL.md`, `00-READ-ME-FIRST.md`, config; `assets/dataverse-builder.json` is the builder flow |

## Scripts

Run from the project root. Without `power-platform.config.json`, the validators warn that they use defaults.

| Command | What it does | Exit |
|---|---|---|
| `scripts/estado.py <command> [stage]` | pipeline state in `STATE.md`: stage order and next command | 0 ok, 1 stage out of order, 2 usage or file |
| `scripts/desenhar-mockups.py <spec> --simular` | validates the mockups spec (M001–M007) and shows the prompts, no network; without `--simular` it generates the PNGs (`OPENAI_API_KEY`) | 0, 1, 2 |
| `scripts/verificar-prototipo.py <folder> --mockups <spec>` | HTML prototype contract (V001–V013): screens, catalog, offline, tokens, origin in the mockups | 0, 1, 2 |
| `scripts/montar-carga-mockup.py <spec> --saida <folder>` | mockup load (C001–C015): `.xlsx` with one sheet per table in load order and, on SQL, `carga-mockup.sql`; `--flow` writes the plan and the Dataverse builder flow (C016–C018); `--conferir <export.json>` compares the types created in Dataverse with the model (C101–C105) | 0, 1, 2 |
| `validar-telas.py` (skill `powerapps-canvas`) | screen YAML, PA2108, literal `RGBA(`, `;;` in YAML, control version | 0, 1, 2 |
| `verificar-fluxo.py` (skill `power-automate`) | envelope, orphan references, `Catch` with `Skipped`, 4-field Response, environment literal, paste symptoms (F001–F023) | 0, 1, 2 |
| `lint-procedure.py` (skill `sql-procedures`) | `NOCOUNT`, `XACT_ABORT`, transaction, return with the 4 columns | 0, 1, 2 |
| `python tools/lint_skills.py` (plugin repository) | skill standard and sanitization | 0, 1 |

Each has `--help`. What each validator does **not** cover: `references/final-gate.md`.

## Definition of done (global)

- [ ] Step 1 done: `STATE.md` (in the pipeline), config and active track cited in the report.
- [ ] Table, column and procedure names checked against `AS-BUILT-NAMES` (or marked "inferred").
- [ ] Every applicable validator ran: `N error(s), M warning(s)` pasted, with `0 error(s)` and files read > 0.
- [ ] Screen or flow changed and pasted into Studio/the designer, or 🔴 with the exact step.
- [ ] App↔flow contract respected: `{status, description, id, url}`, `.Run()` inside `IfError`.
- [ ] No environment literal in any delivery artifact.
- [ ] Queue updated: each ✅ with Evidence; `STATE.md` updated by `estado.py`.
- [ ] Agent delivery checked by you before it goes into the report.
- [ ] Pipeline stage closed with the script's "Next step" block.

## Pitfalls (the costliest)

1. Moving to the next stage in the same session, or inventing the next command: [output-format.md](references/output-format.md).
2. Running only one of the validators and declaring green: [final-gate.md](references/final-gate.md).
3. Regenerating over the pasted baseline: [safeguards.md](references/safeguards.md).
4. Writing a screen against the plan instead of `AS-BUILT-NAMES`: [default-decisions.md](references/default-decisions.md).
5. Calling the image API without the user's "go ahead and generate": [mockups.md](references/mockups.md).
6. Treating "the number does not match" as a formula bug before checking source and environment: [investigate-mode.md](references/investigate-mode.md).
7. Trusting a queue "✅" without Evidence: [goal-queue-mode.md](references/goal-queue-mode.md).
8. A subagent for one screen, or two on the same file: [subagents.md](references/subagents.md).
9. Hardcoding the environment so it cannot be promoted: [alm-environments.md](references/alm-environments.md).
10. Ending the turn "waiting" on subagents: [subagents.md](references/subagents.md).
