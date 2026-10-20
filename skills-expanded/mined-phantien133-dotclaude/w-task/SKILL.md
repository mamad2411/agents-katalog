---
description: Orchestrate a full feature dev workflow with browser and acceptance verification (intake → context → plan → impact → UI → TDD → browser-verify → docs → acceptance-verify → PR). Uses a CodeGraph index when available to explore and analyse impact cheaply, gates UI work on a localhost browser check via Chrome DevTools MCP, then proves every ticket requirement is delivered in a bounded fix loop before opening the PR. Reads project config from .claude/workflow.yaml.
argument-hint: <issue-url | #N | title>
allowed-tools: Bash, Read, Write, Edit, Skill
---

# w-task

Full feature development workflow with browser verification. State-machine with explicit
gates — advances only when the developer runs `/w-task`.

**First run:** `$ARGUMENTS` is an issue reference or free title → starts Phase 0.  
**Subsequent runs:** `$ARGUMENTS` empty or `continue` → reads `state.yaml`, advances to next phase.

Two gates make this workflow more than a task runner:

- **Phase 4c — Browser Verify**: after TDD green and checks pass, Claude starts the local
  dev server, uses Chrome DevTools MCP to verify UI changes at `localhost` only, then waits
  for developer confirmation before committing.
- **Phase 5b — Acceptance Verify**: after docs are persisted, every requirement from the
  ticket is traced to evidence and — for UI work — the implementation is compared against
  the Figma export. Findings are fixed, committed and re-documented in a bounded loop
  (default 3 iterations) before the PR is opened.

When a **CodeGraph** index (`.codegraph/`) is available, Phases 0b, 2 and 4 query the graph
instead of grepping the tree — same answers, far fewer file reads. Everything degrades to
the git-grep path when it is not.

---

## ⚠️ Invocation gate — read on every run

The workflow advances **only** when the developer explicitly runs `/w-task`.

- During a gate pause: freely chat, ask questions, request edits — **do NOT advance the phase**.
- A phase transition happens **only** at the moment this skill is invoked with empty / `continue`.
- If `$ARGUMENTS` is anything other than empty / `continue` / issue ref / title: treat as a
  question or correction — respond and stay in the current phase.
- Never infer "the developer is done" from context. Wait for the explicit signal.

```
$ARGUMENTS present (URL / #N / title)?
  └─ Yes → First run: start Phase 0
  └─ No (empty or "continue") →
       state.yaml exists?
         └─ No  → Ask for issue reference or title
         └─ Yes → Read phase + status, advance
```

---

## Setup check

Before Phase 0, read config:

```bash
cat .claude/workflow.yaml 2>/dev/null
```

If file missing: say "Run `/w-setup` first to configure this project." Stop.

Extract and store for this session:
- `issue_tracker.*` — how to fetch ticket data
- `workflow.state_root` → where `state.yaml` + per-task md files live.
  Default `.workflow` (gitignored) for flat layout. Under the **streaming-docs
  convention** this is `<docs_root>/workflow` (committed alongside docs).
- `workflow.docs_root` → null means skip Phase 5
- `workflow.module_docs_root`, `feature_records_subdir`, `api_docs_filename`,
  `workflow_links_filename` — drive Phase 0b context load + Phase 5 doc persistence
- `workflow.db_docs_root`, `diagrams_root`, `master_erd_path` — drive Phase 5 DB pipeline
- `workflow.oq_docs_path`, `adr_docs_path` — drive OQ surfacing (Phase 0b) + ADR generation (Phase 2)
- `project.test_command`, `.typecheck_command`, `.lint_command`
- `project.module_glob`, `schema_paths.{prisma,graphql}`, `test_layers` — drive
  Phase 0b module detection, Phase 2 impact analysis, Phase 4 test stubs
- `project.dev_server_command`, `project.dev_server_port` — drive Phase 4c browser verify.
  If `dev_server_command` is null, Phase 4c is not applicable and is recorded as such.
- `project.codegraph.{enabled, auto_index, sync_phases}` — drive the CodeGraph fast path
  in Phases 0b / 2 / 4. Absent or `enabled: false` → every phase uses its git-grep fallback.
- `verify.{acceptance, visual, max_loops, browser_wait_seconds}` — drive Phase 5b and the
  MCP contention protocol. Absent → acceptance `true`, visual `auto`, max_loops `3`,
  browser_wait_seconds `180`.
- `repos[]` — the repos this workflow operates on, each `{path, default_branch, remote}`.
  `path: "."` is the main workspace; other entries are git submodules. Each repo has
  its **own** default branch (they may differ — `main` vs `master`). Drives Phase 6
  per-repo branch sync + PR.
- `pr.draft`, `.template`, `.default_branch`

**Resolving `repos`** (config may be v1 or v2):

```
if config has top-level `repos:` (version 2):
    REPOS = config.repos                       # use as-is
else (version 1 / no repos):
    REPOS = [{ path: ".",
               default_branch: pr.default_branch or "main",
               remote: "origin" }]             # synthesize single main-workspace repo
```

Store `REPOS` for Phase 6. A single-repo project has exactly one entry (`.`).

**Config version.** This skill reads schema **v3**. A v1/v2 file still works — every v3
field is optional and falls back to the default above — but say so once, in one line:
`workflow.yaml is version <N>; run /w-setup to migrate to 3 and enable codegraph +
acceptance verify.` Do not migrate the file yourself and do not repeat the notice.

**CodeGraph probe.** Once per task, at the setup check, invoke skill `w-codegraph detect`
and store the result in `state.yaml` as `codegraph: ready|stale|not-indexed|unavailable|disabled`.
Phases 0b/2/4 read that value instead of re-probing. On `not-indexed`, `w-codegraph ensure`
asks the developer once whether to build the index — the answer is recorded and never asked
again within this task.

**Path convention — streaming-docs vs flat layout**

State and docs are two **separate** concerns. They MAY share a parent (the
streaming-docs convention puts them as siblings under `<docs_root>/`) but they
are configured independently — w-task always uses the explicit config fields,
never inference.

| Concern | Config field | Streaming-docs example | Flat-layout example |
|---|---|---|---|
| State (this task's working files) | `state_root` | `streaming-docs/workflow` | `.workflow` |
| Module docs | `module_docs_root` | `streaming-docs/documents/modules` | `docs/modules` |
| DB docs | `db_docs_root` | `streaming-docs/documents/database` | `docs/database` |
| OQ doc | `oq_docs_path` | `streaming-docs/documents/overview/open-questions.md` | `docs/open-questions.md` |
| ADR doc | `adr_docs_path` | `streaming-docs/documents/overview/architecture-overview.md` | `docs/adr.md` |

For task `CISTREAMIN-11-sign-up-api` on a streaming-docs-convention project, 
creates these paths:
- State: `streaming-docs/workflow/CISTREAMIN-11-sign-up-api/{intake,context,plan,impact,tests,verify,pr}.md` + `state.yaml`
- Module docs touched (Phase 5):
  - `streaming-docs/documents/modules/01-auth/README.md` (update Implementation Status)
  - `streaming-docs/documents/modules/01-auth/features/sign-up.md` (create or append)
  - `streaming-docs/documents/modules/01-auth/api.md` (append SignUp mutation)
  - `streaming-docs/documents/modules/01-auth/workflow-links.md` (append task row)

**Per-phase helper skills** (invoked when the relevant config fields are set;
silently skipped otherwise):

| Phase | Helper skills |
|-------|---------------|
| setup | `w-codegraph detect` |
| 0b | `w-context-load`, `w-oq-check`, `w-codegraph context` |
| 2 | `w-impact-analyzer`, `w-adr`, `w-codegraph impact` |
| 4 | `w-test-stubs`, `w-codegraph affected` |
| 4c | Chrome DevTools MCP (external — must be configured in settings.json) |
| 5 | `w-feature-record`, `w-api-doc`, `w-db-doc` |
| 5b | `w-acceptance-verify`, `figma-verify-parity` |
| 6 | `w-doc-gate` (called from `/w-pr` — see Phase 6) |

---

## Phase 0 — Intake (INTERACTIVE → GATE 0)

**Goal:** understand what we're building before touching any code.

### 0.1 Resolve issue

Parse `$ARGUMENTS` based on `issue_tracker.type`:

**github:**
- URL (`github.com/.*/issues/\d+`): extract N → `gh issue view <N> --json title,body --repo <org/repo>`
- `#N` or bare number: `gh issue view <N> --json title,body`
- Free text: use as-is.
- If `gh` fails: proceed with $ARGUMENTS as title.

**plane (mcp_available: true):**
- URL matching configured `url` or identifier (e.g. `PROJ-42`):
  call `mcp__plane__retrieve_work_item_by_identifier`
- Free text: use as-is.

**plane (mcp_available: false) / jira / linear:**
- URL or identifier: ask developer to paste the ticket description.
- Free text: use as-is.

**none:** always use $ARGUMENTS as-is.

### 0.2 Derive task-slug

- Issue with ID: `<ID>-<short-slug>` (kebab-case, max 25 chars for slug part)
- Free title: kebab-case, max 40 chars.

Create directory `<state_root>/<task-slug>/`.

### 0.3 Write intake.md

```markdown
# Intake — <title>

## Source
- Input: <URL / identifier / "free title">
- Issue ID: <ID or n/a>
- Fetched: <yes / no>

## Title
<title>

## Description
<description from issue, or "— not provided —">
```

### 0.4 UI signal detection (before pause card)

Scan intake.md title + description for signals — do this automatically, no output yet.

```
UI_SIGNALS    = /\bUI\b|screen|page|design|component|button|form|modal|dialog|
                 layout|frontend|style\b|CSS|figma\.com|\bicon\b|sidebar|navbar/i

BACKEND_ONLY  = /\bAPI\b|endpoint|migration|cron|queue|webhook|schema|
                 \bdatabase\b|\bDB\b|prisma|resolver|mutation(?! UI)/i

FIGMA_URL     = https?://(www\.)?figma\.com/
```

Decision logic:
- `figma_url` present in description → `has_ui: true`, extract `figma_url`
- `UI_SIGNALS` match AND no `BACKEND_ONLY` → `has_ui: true`
- `BACKEND_ONLY` match AND no `UI_SIGNALS` → `has_ui: false`
- Both signals or neither → `has_ui: unknown`

### 0.5 Pause (conditional)

Show summary card with targeted questions based on `has_ui`:

**has_ui: true — figma URL found:**
```
Please confirm before we proceed:

1. Title: <title> — correct?
2. Figma URL detected: <url>
   Is this the right design for this task? (confirm or paste correct URL)
3. Any additional constraints or context?

Run /w-task when ready.
```

**has_ui: true — no figma URL in intake:**
```
Please confirm before we proceed:

1. Title: <title> — correct?
2. UI changes detected. Do you have a Figma design URL for this task?
   (paste URL, or reply "no Figma" to proceed without design snapshot)
3. Any additional constraints or context?

Run /w-task when ready.
```

**has_ui: false:**
```
Please confirm before we proceed:

1. Title: <title> — correct?
2. This looks like a backend-only change — confirm, or let me know if UI is involved.

Run /w-task when ready.
```

**has_ui: unknown:**
```
Please confirm before we proceed:

1. Title: <title> — correct?
2. Does this task include UI / frontend changes?
   (yes — provide Figma URL if available / no)
3. If the description above is incomplete, paste the correct one now.

Run /w-task when ready.
```

Write `state.yaml`:
```yaml
task: <task-slug>
phase: "0"
status: gate_pending
intake_confirmed: false
has_ui: <true|false|unknown>
figma_url: <url or null>
figma_engine: <official|legacy|none|null>   # resolved at Phase 0b step 5
started_at: <timestamp>
last_updated: <timestamp>
```

**GATE 0:** developer replies in chat → runs `/w-task`.

---

## Phase 0b — Codebase Snapshot (AUTO, runs immediately after GATE 0)

*Triggers when `phase: "0"` + `status: gate_pending` and developer runs `/w-task`.*

Read developer's reply from GATE 0. Update `intake.md` with any corrections.

Update `state.yaml` from developer's reply:
- If developer confirmed/corrected Figma URL → update `figma_url`
- If developer said "no Figma" → set `figma_url: null`
- If developer confirmed UI involvement → set `has_ui: true`
- If developer confirmed backend-only → set `has_ui: false`

**CodeGraph fast path (runs first when `state.yaml.codegraph` is `ready` or `stale`):**

1. `w-codegraph sync` — cheap, keeps the graph matching the tree.
2. `w-codegraph context "<title> — <one-line description from intake.md>"` — returns the
   relevant symbols, their files and the code that matters, in one bounded call.

Treat that output as the file inventory for this task: it replaces `git ls-files` +
per-keyword `git grep` below, and the follow-up `Read` of each hit. Read a file directly
only when the task needs something the graph did not surface. The module-aware doc load
below still runs — the graph knows the code, the module docs know the decisions.

**If `workflow.module_docs_root` is SET → use module-aware context load:**

1. **Invoke skill** `w-context-load <task-slug>`:
   - Reads `<module_docs_root>/<NN>-<module>/README.md` to get Implementation Status
   - Reads `<module_docs_root>/<NN>-<module>/<feature_records_subdir>/*.md` to surface
     prior constraints
   - Auto-invokes `w-oq-check <module>` to flag blocker OQs
   - Reads code scoped by README "✅ Complete" list
   - Writes `context.md` with structured sections (Task Summary, Module Snapshot,
     Relevant Files, Patterns Observed, Available Utilities, Previous Feature
     Decisions, Known Constraints, Suggested Approach)
   - Creates/updates `workflow-links.md` row

   If `w-oq-check` returns non-zero (blocker found): pause, write
   `state.yaml.status: blocked`, surface the OQ, and wait for developer.

**If `workflow.module_docs_root` is NULL → generic code load:**

*With CodeGraph ready, steps 1–3 are already answered by the `context` call above — go
straight to step 4. Without it, fall back to git-grep:*

1. **File inventory:**
   ```bash
   git ls-files | head -300
   ```
2. **Keyword grep:** extract 3-5 keywords, run `git grep -l "<keyword>"` per keyword.
3. **Read top 3-5** relevant files (scope by `project.src_dirs` if set).
4. **Write context.md** with the minimal generic template (Task Summary, Relevant
   Files, Patterns Observed, Suggested Approach — no module-specific sections).

**In both branches:**

5. **UI design pre-fetch (conditional).** If `state.yaml.has_ui: true` AND `figma_url`
   is set, pre-fetch the design now so Phase 1 scopes UI work against the real
   screens/components/states instead of a bare URL — the main reason plans under-scope UI.

   First resolve the Figma engine and record it in `state.yaml` as `figma_engine`:

   | Available MCP tools | `figma_engine` | Path |
   |---|---|---|
   | `mcp__figma__get_design_context` | `official` | Figma's own MCP server — preferred |
   | only `mcp__figma__get_file*` | `legacy` | REST `@figma/mcp` — fallback |
   | neither | `none` | no extraction possible |

   - `official` → spawn the `figma-context-extractor` agent with `figma_url` and output
     path `<state_root>/<task-slug>/figma-spec.md`. It also writes `figma-screens/`.
   - `legacy` → invoke skill `f-extract <figma_url> --task <task-slug>`, which writes
     `<state_root>/<task-slug>/figma-snapshot.md`.
   - `none` → log a one-line warning and continue.

   On failure, log one line and continue — Phase 3.1 retries. Skip silently when `has_ui`
   is `false`/`unknown` or `figma_url` is null.

6. Update `state.yaml`:
   ```yaml
   phase: "1"
   status: gate_pending
   intake_confirmed: true
   module: <name or null>
   last_updated: <timestamp>
   ```

Output: "Context loaded. Run `/w-task` to start planning."

---

## Phase 1 — Plan (INTERACTIVE → GATE 1)

*Triggers when `phase: "1"` + `status: gate_pending`.*

1. Read `intake.md` + `context.md`.

2. Write `questions.md`:
   ```markdown
   # Questions — <title>

   ## What I understood
   <summary — developer corrects misunderstandings here>

   ## Clarifying questions
   <edge cases, acceptance criteria, abnormal flows, integration points>

   ## Suggested scenarios that may be missing
   <AI-identified gaps>
   ```

3. **Pause** — say: "Fill answers in `questions.md`, then run `/w-task`."

4. Update `state.yaml`: `status: gate_pending`.

**GATE 1:** developer fills `questions.md` → runs `/w-task`.

*After developer runs `/w-task`:*

5. Read answered `questions.md`.

6. **Spawn `planner` agent** — pass as brief:
   - `intake.md` full content
   - `context.md` § Relevant Files + § Patterns Observed
   - Answered `questions.md`
   - `figma-spec.md` (official engine) or `figma-snapshot.md` (legacy), whichever Phase 0b
     pre-fetched — the planner must scope UI work (screens, components, states, edge
     cases) against this design, not just the textual description.
   - Instruction: produce a plan with sections — Feature scope, Implementation approach per layer, Out of scope, Dependencies, Risks. When Figma design data is present, the Feature scope and Implementation approach must enumerate the concrete UI surfaces it reveals.

7. Write `plan.md` from agent output.

8. Update `state.yaml`: `gates.1: plan_written`, `status: gate_pending`.

Output: "Review plan.md. Run `/w-task` to approve and proceed."

**GATE 1b:** developer reviews `plan.md` → runs `/w-task`.

---

## Phase 2 — Impact & Design (AUTO → GATE 2)

*Triggers when `phase: "1"` + `status: gate_pending` + `gates.1: plan_written`.*

1. Read `context.md` + `plan.md`.

2. **CodeGraph blast radius (when `state.yaml.codegraph` is `ready`/`stale`).** Before
   the analyzer runs, resolve the symbols `plan.md` says will change and query the graph:

   ```bash
   codegraph impact "<symbol>" --depth 2 --json     # everything affected downstream
   codegraph callers "<symbol>" --json              # who breaks on a signature change
   ```

   The graph's file set is authoritative for § Affected Files — it catches indirect
   callers that a name grep misses. Pass it to the analyzer as a starting set rather
   than letting the analyzer rediscover it.

3. **Invoke skill** `w-impact-analyzer <task-slug>` — produces structured
   `impact.md` with layer-aware sections:
   - § Affected Files (always)
   - § Dependencies, § Risks, § Sequence Diagram (always)
   - § Database Changes (if `schema_paths.prisma` set and plan touches DB)
   - § GraphQL Schema Changes (if `schema_paths.graphql` set and plan touches API)
   - § Async / Queue Impact (heuristic — BullMQ/Kafka/etc. detected)
   - § Cache / State Impact (heuristic — Redis/Cache detected)
   - § Cross-cutting (config, auth, logging)
   - Auto-generates extra Mermaid diagrams when triggers met (>3 services,
     state machine logic, new data models).

   The analyzer may auto-invoke `w-adr` if it detects a non-trivial architectural
   decision (e.g. DB schema change touching >2 tables, new cross-module async
   contract).

4. **Manual ADR opportunity** — if a decision surfaced during the impact analysis
   that wasn't auto-captured, invoke `w-adr <task-slug> "<decision-title>"`
   to append it to `adr_docs_path`.

5. Update `state.yaml`: `phase: "2"`, `status: gate_pending`.

Output:
```
impact.md is ready. Before approving:
• Challenge assumptions — does the sequence diagram match your mental model?
• Update the design — if something is wrong, say so in chat and I'll revise.

This is the last checkpoint before implementation shape is committed.
Run /w-task when satisfied.
```

**GATE 2:** developer discusses / approves → runs `/w-task`.

Update `state.yaml`: `phase: "3"`, `status: gate_pending`.

---

## Phase 3 — UI / Figma (CONDITIONAL → GATE 3)

*Triggers when `phase: "3"` + `status: gate_pending`.*

### 3.0 — Decide whether to run

Read `state.yaml.has_ui` and `state.yaml.figma_url`.
Read `plan.md` + `impact.md` for UI-related content.

**Skip conditions** (any of these → `gates.3: skipped`, advance to Phase 4):
- `has_ui: false`
- `has_ui: unknown` AND `plan.md` / `impact.md` contain no UI keywords (screen, page, component, button, form, modal, CSS, frontend)
- `has_ui: true` AND `figma_url: null` AND plan has no UI scope worth implementing (pure copy/icon swap only)

If skipping:
```
Update state.yaml: gates.3: skipped, phase: "4", status: gate_pending.
Output: "No UI scope detected. Run /w-task to start TDD."
```

**GATE 3 (skipped):** developer runs `/w-task` → Phase 4.

---

### 3.1 — Extract the design

*Only runs when NOT skipped.*

Read `state.yaml.figma_url` and `state.yaml.figma_engine`. If `figma_engine` is null
(Phase 0b never resolved it), resolve it now using the table in Phase 0b step 5.

**`figma_engine: official`** — the Figma MCP server exposing `get_design_context`.

Reuse `<state_root>/<task-slug>/figma-spec.md` if Phase 0b already wrote it. Otherwise
spawn the `figma-context-extractor` agent with `figma_url` and that output path.

Then, in parallel where possible:
- spawn `figma-asset-fetcher` with the spec path → downloads every icon/image into the
  project and writes `figma-assets.md`,
- spawn `figma-design-system-mapper` with the spec path → writes `figma-mapping.md`.

Read the three result files. **Resolve the extractor's gap list and the mapper's
"No equivalent" table with the developer before writing any code.** A gap is a question;
answering it with a plausible value is how implementations drift from designs.

**`figma_engine: legacy`** — REST-only `@figma/mcp`.

Reuse `<state_root>/<task-slug>/figma-snapshot.md` if it exists; otherwise invoke skill
`f-extract <figma_url> --task <task-slug>`. Warn once, in one line, that the legacy engine
has no rendered reference and no asset endpoint, so Phase 3.4 parity checking is limited
and assets require manual export.

**Extraction failed, or `figma_engine: none`:**
```
⚠️ Figma extraction unavailable: <reason>
Options:
  [1] Configure the official Figma MCP server, then re-run
      claude mcp add --transport http figma https://mcp.figma.com/mcp
  [2] Continue without design data — implementation will follow plan.md only,
      and UI accuracy will be limited

Reply with your choice, then run /w-task.
```
Wait for developer. On [2]: set `figma_url: null`, proceed to 3.2 with no design data.

**If `figma_url` is null:** proceed to 3.2 with no design data, after saying so plainly.

---

### 3.2 — Implement UI

**`figma_engine: official`** — invoke skill `figma-implement-design` with:
- `figma-spec.md`, `figma-assets.md`, `figma-mapping.md` from 3.1,
- `<state_root>/<task-slug>/plan.md` for scope.

The `figma-fidelity` rules bind this step: real exported assets only, exact values only,
reuse existing components, no rounding, no invented colours or icons. Assets still
unresolved after `figma-asset-fetcher` are marked `TODO(figma-asset): <node-id>` in the
code and carried into 3.3 — never replaced with generated SVG or an icon-pack glyph.

**`figma_engine: legacy` or none** — invoke skill `f-implement`:
- with snapshot: `f-implement <state_root>/<task-slug>/figma-snapshot.md --plan <state_root>/<task-slug>/plan.md`
- without: `f-implement --plan <state_root>/<task-slug>/plan.md` (plan-only mode)

Do not advance Phase 3 until the implementing skill reaches its summary step.

---

### 3.3 — Asset resolution gate

*Only runs if `figma-assets.md` has unresolved entries (official) or `ASSET_PLACEHOLDER`
comments remain (legacy).*

If everything resolved: skip to 3.4.

Output:
```
## UI assets needed

<N> assets could not be exported automatically.
See figma-assets.md for Figma links and target paths.

Export each from Figma and save to the listed path.
Run /w-task when done — I will wire them in.
```

Update `state.yaml`: `status: gate_pending`, `gates.3a: assets_pending`.

**GATE 3a:** developer exports assets → runs `/w-task`.

On resume: re-read `figma-assets.md`, check each `target_path` exists, wire up the
resolved ones (replacing `TODO(figma-asset)` markers / `ASSET_PLACEHOLDER` comments),
re-show only what is still missing. When all resolved: proceed to 3.4.

---

### 3.4 — Visual parity gate

*Skipped only when `figma_engine` is `none`, or when `workflow.dev_server_command` is
unset. Record the skip explicitly — never let it read as a pass.*

Invoke skill `figma-verify-parity` for each screen implemented, passing the route and
`figma-spec.md`. It renders the page, diffs computed styles against the spec, verifies
every asset resolves to a real file, and writes `figma-parity-report.md`.

- **PASS** → record `gates.3c: parity_pass` and continue to 3.5.
- **FAIL** → fix the listed blockers and majors, then re-run. Do not advance on a FAIL,
  and do not reason that a fix must have worked — only a fresh PASS closes the gate.
- **NOT RUN** → record `gates.3c: parity_not_run` with the reason and surface it in the
  Phase 3 summary so it reaches the PR description.

On `figma_engine: legacy`, run the gate anyway if a dev server exists — the computed-style
pass still catches spacing, colour and font drift; only the screenshot comparison degrades.

---

### 3.5 — Finalize Phase 3

Update `state.yaml`: `gates.3: ui_verified`, `phase: "4"`, `status: gate_pending`.

Output: "UI implementation complete (parity: <PASS|NOT RUN>). Run `/w-task` to start TDD."

**GATE 3b:** developer runs `/w-task` → Phase 4.

---

## Phase 4 — TDD (AUTO → GATE 4a)

*Triggers when `phase: "4"` + `status: gate_pending`.*

0. **Existing coverage (when `state.yaml.codegraph` is `ready`/`stale`).**

   ```bash
   codegraph affected <files from impact.md § Affected Files> --quiet
   ```

   Any test file returned here already covers code in scope: **extend it, never
   shadow it with a new stub**. Pass the list to `w-test-stubs` so it skips those
   paths. Without CodeGraph, `w-test-stubs` uses its layer-glob conventions.

1. **Invoke skill** `w-test-stubs <task-slug>` — classifies each affected file
   by layer (unit / graphql / bullmq / nestjs / nextjs / integration) and writes
   layer-appropriate test boilerplate with correct imports, mocking setup, and
   intentionally failing assertions (RED).

   The skill respects `project.test_layers` from workflow.yaml and skips layers
   not enabled. If a test file already exists, it is preserved (never overwritten).

2. **Spawn `tdd-guide` agent** — pass:
   - The skeletons just written by `w-test-stubs`
   - `impact.md § Affected Files`
   - `plan.md`
   - Instruction: enrich the assertions with missing edge cases, stack-specific
     mocking strategies, and integration scenarios. Do NOT rewrite the import
     boilerplate — w-test-stubs already chose the right layer per file.

3. **Resolve test command** from config (`project.test_command`, expand `auto`).
   
   Run tests → confirm RED:
   ```bash
   <test_command> 2>&1 | tail -30
   ```

4. Write `tests.md`:
   ```markdown
   # Tests — <title>

   ## Test files
   <list>

   ## Coverage plan
   <what each test covers, based on impact.md>

   ## State: RED ✗
   <failing output snippet>
   ```

5. Update `state.yaml`: `status: gate_pending`.

Output: "Review tests.md — confirm test structure covers impact.md scope. Run `/w-task` to approve."

**GATE 4 (mini):** developer confirms → runs `/w-task`.

6. **Run `w-checkpoint RED <task-slug>`** — checkpoint before implementation.

7. **Invoke `tdd-workflow` skill** — pass `plan.md` + `tests.md` as context for RED→GREEN→refactor.

8. Run tests → confirm GREEN. With CodeGraph available, iterate on the
   `codegraph affected` set for speed, then run the **full** suite once before the
   gate — the affected set narrows the loop, it never replaces the final run.

9. **Run `w-checkpoint GREEN <task-slug>`** — checkpoint after GREEN.

10. **Inline checks** — in order, report each result:

    Resolve commands from config (expand `auto`):
    - Typecheck: `<typecheck_command>` on whole project
    - Lint: `<lint_command>` on affected files from `impact.md`
    - Tests with coverage (if test command supports it)

11. **Code review — language-aware agent routing.** Scope: affected files from
    `impact.md § Affected Files` only. **Do not default to a single generic
    reviewer.** Group the affected files by language and, for each group, spawn
    the reviewer agent that matches that language. Use the specific agent only if
    it is available in this project (check installed agents); otherwise fall back
    to the generic `code-reviewer` for that group.

    | Changed files (match by extension / path) | Reviewer agent | Build / compile resolver |
    |---|---|---|
    | `*.dart`, or mobile paths (`lib/`, `mobile/`, `app/`, `*mobile*/`) | `flutter-reviewer` | `dart-build-resolver` |
    | `*.ts`, `*.tsx` (NestJS / Next.js) | `typescript-reviewer` | `react-build-resolver` |
    | `*.py` | `python-reviewer` (or `django-reviewer` / `fastapi-reviewer`) | `django-build-resolver` |
    | `*.go` | `go-reviewer` | `go-build-resolver` |
    | `*.rs` | `rust-reviewer` | `rust-build-resolver` |
    | `*.java` | `java-reviewer` | `java-build-resolver` |
    | `*.kt` | `kotlin-reviewer` | `kotlin-build-resolver` |
    | `*.swift` | `swift-reviewer` | `swift-build-resolver` |
    | `*.cs` | `csharp-reviewer` | — |
    | `*.cpp`, `*.cc`, `*.h`, `*.hpp` | `cpp-reviewer` | `cpp-build-resolver` |
    | `*.sql`, `*.prisma`, migration files | `database-reviewer` | — |
    | anything else / no specific reviewer installed | `code-reviewer` | `build-error-resolver` |

    Routing rules:
    - **One reviewer invocation per language group**, each scoped to that group's
      files only. If the change spans Dart + TypeScript, spawn `flutter-reviewer`
      for the `.dart` files AND `typescript-reviewer` for the `.ts/.tsx` files.
    - If a preferred agent is not installed in this project, use `code-reviewer`
      for that group (never silently skip review).
    - For each invocation: resolve CRITICAL/HIGH issues immediately, then re-run
      tests to confirm still GREEN.
    - Document MEDIUM items in `tests.md § Code Review Notes`, one subsection per
      language group (e.g. "Flutter / Dart review", "TypeScript review").
    - The `flutter-reviewer` agent may additionally apply the
      `flutter-dart-code-review` skill checklist when that skill is installed.

    **Build / compile failures during the inline checks (step 10) route the same
    way:** a `.dart` compile error → `dart-build-resolver`, a TS/React build
    error → `react-build-resolver`, etc., falling back to `build-error-resolver`
    when no language-specific resolver is installed.

12. Write `verify.md`:
    ```markdown
    # Verify — <title>

    | Check | Result | Notes |
    |-------|--------|-------|
    | typecheck | ✅/❌ | |
    | lint | ✅/❌ | |
    | tests | ✅/❌ | |
    | code review | ✅/❌ | reviewer agent(s) used per language; CRITICAL/HIGH resolved |
    ```

    List which reviewer agent ran for each language group in the Notes column
    (e.g. "flutter-reviewer (.dart), typescript-reviewer (.ts)").

13. Update `tests.md`: add RED→GREEN record + reference `verify.md`.
14. Update `state.yaml`: `status: gate_pending`, `gates.4a: checks_green`.

Output: "Code is GREEN and checks pass. Review verify.md and diff. Run `/w-task` to proceed to browser verify."

**GATE 4a:** developer reviews verify.md + diff → runs `/w-task`.

---

## Phase 4c — Browser Verify (AUTO → GATE 4c)

*Triggers when `phase: "4"` + `status: gate_pending` + `gates.4a: checks_green` and
`gates.4c` is unset or `browser_contended` (re-entry after the contention gate).*

### When this phase does not run

Three outcomes, and they are **not** interchangeable. Only the first two are decided
without a human.

| Outcome | Condition | `gates.4c` | Advance? |
|---|---|---|---|
| **Not applicable** | `plan.md` has no UI change — no frontend / component / page / CSS / style scope | `browser_not_applicable` | yes, immediately |
| **Not available** | the `chrome-devtools` MCP is not configured at all, or `project.dev_server_command` is null — the check *cannot* be set up here | `browser_unavailable` | yes, but the reason ships in the PR description |
| **Contended** | the MCP tools exist but are busy, locked, or held by another Claude session | see the protocol below | **no — never on your own** |

Output for the first two: `Browser verify not run (<not applicable | not available>: <reason>). Run /w-task to commit.`

Never record a contended run as skipped, unavailable, or passed. A check that could
have run and did not is a decision for the operator, not a default.

---

### MCP contention protocol

Symptoms: a `chrome-devtools` tool call fails with busy / locked / target-in-use /
connection-refused, or the browser is visibly driven by another session.

1. **Retry with backoff** for up to `verify.browser_wait_seconds` (default **180s**):
   attempt at 0s, then every 15s. Report progress on one rewritten line —
   `Browser MCP busy — retrying (<elapsed>s / <limit>s)` — not one line per attempt.
2. **Acquired within the window** → continue to Execution below as normal.
3. **Still blocked at the limit** → stop retrying, kill any dev server started, and
   open the confirm gate:

   ```
   ⚠️ Browser verify could not start — the chrome-devtools MCP has been busy for <limit>s.
      Likely another Claude session is holding the browser.

   This task has UI changes, so the check is meaningful. Choose:
     [w] wait — retry for another <limit>s (repeat as needed)
     [s] skip — record `browser_skipped_by_operator` and continue to commit
     [a] abort — stay at this gate; free the browser, then run /w-task

   Reply with w / s / a.
   ```

   Set `gates.4c: browser_contended`, `status: gate_pending`, and record the elapsed
   wait in `notes`. **GATE 4c-contended.**

   - **w** → run another retry window, then re-show this gate if still blocked.
   - **s** → set `gates.4c: browser_skipped_by_operator`, note who decided and why,
     and carry that line into the PR description.
   - **a** → leave state as is and stop. `/w-task` re-enters at step 1.

The same protocol governs the visual verification step in Phase 5b.

---

### ⚠️ Browser safety constraints — enforce on every action in this phase

- Use `navigate_page` **only** to `http://localhost:<port>` where `<port>` is taken
  from the dev server startup output or `project.dev_server_port` in `workflow.yaml`.
- **Never** navigate to any URL outside `localhost` / `127.0.0.1`, even if a link
  on the page points elsewhere.
- **Never** submit forms or fire requests to external endpoints.
- **Never** log, quote, store, or reference credentials, tokens, or personal data
  visible in the browser — treat them as ephemeral noise.
- **Never** follow redirects that leave `localhost`.
- Kill the dev server process immediately after verification completes (pass or fail).

---

### Execution

1. Resolve `dev_server_command` and `dev_server_port` from `workflow.yaml`.

2. Start dev server in background, capture PID:
   ```bash
   <dev_server_command> > /tmp/devserver-<task-slug>.log 2>&1 &
   SERVER_PID=$!
   echo $SERVER_PID > /tmp/devserver-<task-slug>.pid
   ```

3. Poll until ready (max 60s):
   ```bash
   for i in $(seq 1 30); do
     curl -s -o /dev/null -w "%{http_code}" http://localhost:<port>/ | grep -q "200\|304" && break
     sleep 2
   done
   ```
   If timeout: kill server, set `gates.4c: browser_error`, output error, proceed to GATE 4c.

4. For each UI path listed in `plan.md § UI Changes` (or `§ Acceptance criteria`):

   a. Navigate: `navigate_page` → `http://localhost:<port><path>`

   b. Assert with `evaluate_script` — return a JSON object, one call per path:
      ```js
      ({
        url: location.href,
        title: document.title,
        targetExists: !!document.querySelector('<main selector from plan>'),
        errorBanners: document.querySelectorAll('[data-error], .error, .alert-error').length,
        consoleErrors: (window.__cdp_errors ?? []).length
      })
      ```
      Use the minimal selector needed — do NOT dump the full DOM.

   c. Fetch console errors: `get_console_messages` (filter `level: error`).

   d. Save screenshot to file:
      ```
      <state_root>/<task-slug>/browser-<path-slug>.png
      ```
      Use `take_screenshot` with `savePath` set — do NOT inline image into context.

5. Stop dev server:
   ```bash
   kill $(cat /tmp/devserver-<task-slug>.pid) 2>/dev/null
   wait $(cat /tmp/devserver-<task-slug>.pid) 2>/dev/null
   rm /tmp/devserver-<task-slug>.pid /tmp/devserver-<task-slug>.log
   ```

6. Append `## Browser Verify (localhost)` section to `verify.md`:
   ```markdown
   ## Browser Verify (localhost)

   | Path | Check | Result | Notes |
   |------|-------|--------|-------|
   | /... | element exists / error count / title | ✅/❌ | ... |

   Console errors: <N>
   Screenshots: <state_root>/<task-slug>/browser-*.png
   Server: localhost:<port> — killed after verification
   ```

7. Update `state.yaml`: `gates.4c: browser_verified` (or `browser_error` on failure).
   Keep `status: gate_pending`.

Output: "Browser verify complete. Review verify.md § Browser Verify and screenshots. Run `/w-task` to commit."

**GATE 4c:** developer reviews browser verify results → runs `/w-task`.

---

15. **Commit the implementation**:
    ```bash
    git add <files from impact.md § Affected Files>
    git commit -m "feat(<scope>): <one-line summary from plan.md>"
    ```
    Do NOT use `git add -A` — stage only files listed in `impact.md`.

16. `w-codegraph sync` — the graph should match the tree the next phase reasons about.

17. Update `state.yaml`: `phase: "5"`, `status: gate_pending`, `gates.4b: committed`.

Output: "Implementation committed. Run `/w-task` to proceed to doc persistence."

**GATE 4b:** developer runs `/w-task` → Phase 5.

---

## Phase 5 — Persist Docs (CONDITIONAL → GATE 5)

*Triggers when `phase: "5"` + `status: gate_pending`.*

Read doc-related fields from `workflow.yaml`.

**If `docs_root` is null AND `module_docs_root` is null:** skip entirely.
Update `state.yaml`: `gates.5: skipped`, `phase: "5b"`, `status: gate_pending`.
Output: "Doc roots not configured — skipping. Run `/w-task` to run acceptance verification."

**Otherwise — invoke per-target helper skills (each skill is a no-op if its
own config field is null):**

1. **Feature record** — if `module_docs_root` + `feature_records_subdir` set:
   - Derive `<feature-name>` from intake.md (kebab-case, capability not ticket
     ID). Pause once to let developer confirm if ambiguous.
   - Invoke `w-feature-record <task-slug> <feature-name>` → creates or appends
     `<module_docs_root>/<NN>-<module>/features/<feature-name>.md`.

2. **Module README update** — if `module_docs_root` set:
   - Update Implementation Status: move items completed in this task from
     ⏳ Deferred → ✅ Complete; add new ⏳ Deferred items introduced.
   - Update Depends on / Blocks if cross-module deps changed.
   - (No dedicated helper skill — this is an inline edit of the existing README.)

3. **API doc** — if `module_docs_root` + `api_docs_filename` set AND impact.md
   has § GraphQL Schema Changes / § REST API Changes:
   - Invoke `w-api-doc <task-slug>` → appends/replaces operation sections in
     `<module_docs_root>/<NN>-<module>/<api_docs_filename>`.

4. **DB docs + sub-ERD + master ERD** — if `db_docs_root` set AND impact.md
   has § Database Changes:
   - Invoke `w-db-doc <task-slug>` → writes module schema doc, sub-ERD, and
     **mandatorily** syncs the master ERD. If `master_erd_path` is null while
     `diagrams_root` is set, the skill aborts with an error — fix workflow.yaml.

5. **Stage doc changes** — add all written files to the staging area in a
   separate commit:
   ```bash
   git add <module_docs_root>/<NN>-<module>/ <db_docs_root>/<NN>-<module>.md \
           <diagrams_root>/<NN>-<module>-erd.puml <master_erd_path> \
           <adr_docs_path> <oq_docs_path>
   git commit -m "docs(<module>): persist <feature-name> design from <task-slug>"
   ```
   Doc commit is separate from code commit (Phase 4b) so reviewers can read
   them independently, but both ship in the same PR.

Update `state.yaml`: `gates.5: docs_written`, `status: gate_pending`.

Output: "Docs persisted and committed. Review changes, then run `/w-task` — Phase 5b
verifies every ticket requirement against the delivered code, tests, docs and UI."

**GATE 5:** developer reviews + runs `/w-task`.

Update `state.yaml`: `phase: "5b"`, `status: gate_pending`.

---

## Phase 5b — Acceptance Verify (AUTO, LOOPING → GATE 5b)

*Triggers when `phase: "5b"` + `status: gate_pending`.*

Phases 4 and 4c proved the code works. This phase proves it is **the thing that was
asked for** — every requirement in the ticket traced to evidence, and, for UI work,
the implementation compared against the design export so a redrawn icon or an eyeballed
colour cannot reach the PR.

Skipped entirely when `verify.acceptance: false` AND `verify.visual: false` — set
`gates.5b: skipped`, `phase: "6"`, and say so.

### 5b.1 — Verify

**Invoke skill** `w-acceptance-verify <task-slug> --iteration <N>` (N starts at 1).

It builds the requirement matrix from `intake.md`, `questions.md`, `plan.md` and the
Figma spec, fans out independent adversarial verifiers, runs visual comparison against
the design export, and writes `acceptance.md`. Its **exit code drives this phase**:

- **exit 0** — no blocker, no major → go to 5b.3.
- **exit non-zero** — go to 5b.2.

The visual step drives the same browser MCP as Phase 4c and inherits its
**contention protocol** — retry up to `verify.browser_wait_seconds`, then gate on the
operator. Never self-record a contended visual check as NOT RUN.

### 5b.2 — Fix, commit, re-document (one iteration)

For each blocker and major in `acceptance.md § Findings`, in severity order:

1. Make the **smallest change that closes the finding**. A finding about a wrong asset
   is closed by using the real exported asset — never by adjusting the check.
2. Re-run the test suite → must be GREEN. A fix that breaks a test is not a fix.
3. **Commit it** — one commit per finding so the PR reads as a sequence of closures:
   ```bash
   git add <files changed by this fix>
   git commit -m "fix(<scope>): <finding title> [<finding-id>]"
   ```
4. **Re-persist docs** for anything the fix changed — re-invoke the Phase 5 helpers
   (`w-feature-record`, `w-api-doc`, `w-db-doc`) and commit the doc change in the same
   iteration:
   ```bash
   git commit -m "docs(<module>): sync <feature-name> after <finding-id>"
   ```
   Docs must never lag the fix — `w-doc-gate` at Phase 6 enforces exactly this.
5. `w-codegraph sync` so later queries see the fixed tree.

Then increment the iteration and return to 5b.1.

**Loop bound:** `verify.max_loops` (default **3**). Iterations are recorded in
`state.yaml.gates.5b_iteration`. Never exceed the bound — re-running the same failing
fix a fourth time is not progress, it is a decision the operator has not been given.

### 5b.3 — Pass

Update `state.yaml`: `gates.5b: accepted`, `phase: "6"`, `status: gate_pending`.

Output:
```
Acceptance verified — <R> requirements, <N> fix iteration(s), visual: <PASS|NOT RUN (reason)>.
Minor findings carried to the PR description: <m>
Run /w-task to create the PR.
```

**GATE 5b:** developer runs `/w-task` → Phase 6.

### 5b.4 — Loop exhausted

When iteration `> max_loops` and blockers or majors remain, stop fixing. The skill
writes `open-issues.md` — a one-screen, plain-language account of what is still wrong,
what was tried, why it did not close, and what would unblock it.

Update `state.yaml`: `status: blocked`, `gates.5b: open_issues`.

Output:
```
⚠️ <N> issue(s) survived <max_loops> fix attempts — see open-issues.md.

Everything else is complete: code committed, tests GREEN, docs persisted.

  [c] continue to Phase 6 and open the PR with these known gaps documented
  [p] re-plan — return to Phase 1 with open-issues.md as input
  [f] you fix it — I stay at this gate; run /w-task when done

Reply with c / p / f.
```

- **c** → carry `open-issues.md` verbatim into the PR description under
  **Known gaps**, set `gates.5b: accepted_with_gaps`, `phase: "6"`.
- **p** → `phase: "1"`, `status: gate_pending`, keep `open-issues.md` as planner input.
- **f** → stay put. On re-entry, restart at 5b.1 with the iteration counter reset to 1.

---

## Phase 6 — PR (AUTO, **terminal**)

*Triggers when `phase: "6"` + `status: gate_pending`.*

Phase 6 is the **final** phase and runs fully automatically when the developer runs
`/w-task`. No manual `/w-pr` invocation needed. It works across **every repo in
`REPOS`** (main workspace + submodules), opening one PR per repo that has commits,
each against that repo's own default branch.

**Terminal contract:** once all PRs exist, w-task performs a **single** final state
write (`status: complete`), then 6.3 commits and pushes that record into the PR branch.
After that, `state.yaml` is final — it is never updated again, and a subsequent
`/w-task` is a no-op that just reprints the PR URLs (see § "Re-running a complete
task"). The workflow never ends with uncommitted state.

---

### 6.0 — Branch sync (before everything, per repo)

*Skip if `gates.6a: synced` already set (idempotent re-entry after conflict resolution).*

For **each repo in `REPOS`** (submodules first, then the main workspace `.`), run the
sync inside that repo's working dir with `git -C <path>` and that repo's own
`default_branch` + `remote`:

1. Fetch: `git -C <path> fetch <remote>`
2. Check for new commits: `git -C <path> log HEAD..<remote>/<default_branch> --oneline`
3. **No new commits** → repo is in sync, continue to next repo.
4. **New commits found** → merge: `git -C <path> merge <remote>/<default_branch> --no-edit`
   - **Clean (exit 0):** log `Merged <remote>/<default_branch> into <path> (<N> commits).`
   - **Conflict (exit non-zero):**
     ```
     ⚠️ Merge conflict in <path> with <remote>/<default_branch>.

     Conflicting files:
     <list from git -C <path> status>

     Resolve in <path>, then `git -C <path> add <files>` + `git -C <path> merge --continue`.
     Run /w-task when every repo's merge is complete.
     ```
     Set `gates.6a: conflict_pending`, `status: gate_pending`, and record which repo
     in `notes`. **GATE 6-conflict.** On re-entry: re-check every repo's tree; only
     set `gates.6a: synced` when ALL repos are clean and merged.

When all repos are synced: set `gates.6a: synced`, proceed to 6.1.

---

### 6.1 — Doc gate

*Triggers when `gates.6a: synced`.*

**Invoke skill** `w-doc-gate <task-slug>`.

The gate verifies:
- Every module touched (code changes under `module_glob`) has corresponding doc updates in the branch diff.
- If `master_erd_path` is configured: any sub-ERD change is accompanied by a master ERD update.

**Gate passes (exit 0):** set `gates.6b: doc_gate_passed`, proceed to 6.2.

**Gate fails (exit non-zero):**
- Print the violation report from `w-doc-gate`.
- Output:
  ```
  ⚠️ Doc gate blocked. Missing docs for the modules listed above.
  Run /w-task to return to Phase 5 and persist the missing docs.
  ```
- Update `state.yaml`: `phase: "5"`, `status: gate_pending`, `gates.5: pending`.
- Stop — developer must fix docs, then run `/w-task` to retry Phase 5 → 6.

---

### 6.2 — Create PRs (AUTO, one per changed repo) — **then stop**

*Triggers when `gates.6b: doc_gate_passed`.*

Determine which repos changed: a repo in `REPOS` needs a PR when it has commits on
the current branch not yet on its `default_branch`
(`git -C <path> log <remote>/<default_branch>..HEAD --oneline` is non-empty).

**Order matters for submodules:** open submodule PRs **before** the main workspace
PR, so the superproject commit that bumps submodule pointers references branches
that already exist on the remote.

For **each changed repo** (submodules first, then `.`):

**Invoke skill** `w-pr <task-slug> --repo <path> --target <default_branch> --skip-doc-gate`
(gate already passed in 6.1). `w-pr` will, for that repo:
- Build the MR title + body from `plan.md` + `impact.md` (scoped to that repo's files)
- Show a **preview** (repo path, title, target branch, draft status)
- Create the MR via `glab mr create` inside `<path>` and capture the URL

Collect each `{repo, url}` pair.

**Finalize (single terminal write):** after every changed repo's PR is created,
write `state.yaml` ONCE:
```yaml
phase: "6"
status: complete
prs:
  - repo: apps/api
    url: <mr-url>
    target: master
  - repo: "."
    url: <mr-url>
    target: main
last_updated: <timestamp>
```

Then run 6.3 — the workflow does not end with a dirty tree.

---

### 6.3 — Ship the final state (AUTO, last action)

A completed task used to leave `state.yaml` and the task's markdown modified but
uncommitted, so the PR carried an implementation whose own record was missing. Close
that: the terminal write is committed and pushed into the PR that was just opened.

1. **Is the state tracked?** `state_root` under a gitignored path (the default
   `.workflow`) is ephemeral scratch — nothing to commit:
   ```bash
   git check-ignore -q <state_root> && echo ephemeral
   ```
   If ephemeral: say `State root is gitignored — nothing to commit.` and stop here.

2. **Commit the task record** in the repo that holds it (normally the main workspace `.`):
   ```bash
   git -C <repo> add <state_root>/<task-slug>/
   git -C <repo> commit -m "chore(<task-slug>): finalize workflow state"
   ```
   Stage the task folder only — never `git add -A`. This picks up `state.yaml` plus
   every artefact the run produced: `intake.md`, `context.md`, `questions.md`, `plan.md`,
   `impact.md`, `tests.md`, `verify.md`, `acceptance.md`, `open-issues.md`, `pr.md`,
   and the browser / parity screenshots.

3. **Push to the PR branch** — a plain fast-forward push to the branch the PR was opened
   from, so the PR updates in place:
   ```bash
   git -C <repo> push <remote> HEAD:<current-branch>
   ```
   **Never `--force`, never `--force-with-lease`, never rewrite history here.** The PR
   may already have review comments anchored to these commits.

   If the push is rejected as non-fast-forward, someone else pushed to the branch:
   ```bash
   git -C <repo> pull --rebase=false <remote> <current-branch>   # merge, do not rebase
   git -C <repo> push <remote> HEAD:<current-branch>
   ```
   If it still fails, report it plainly and leave the commit local — a stuck push is a
   thing to tell the operator, not to force past.

4. If several repos carry task state (rare — a submodule with its own `state_root`),
   repeat 2–3 per repo, submodules first.

Then output and **stop** — no further state writes, nothing more to advance:
```
✓ Task complete. <N> PR(s) created:
  apps/api → master   <url>
  .        → main      <url>

Final state committed and pushed to <branch> — the PR carries the full task record.
Docs ship with code — no post-merge sync needed.
state.yaml is final; the workflow has stopped.
```

If step 3 could not push:
```
✓ PR(s) created, but the final state commit is still local:
  <reason>
  Push it with: git -C <repo> push <remote> HEAD:<branch>
```

---

### Re-running a complete task

If `/w-task` is invoked while `state.yaml.status: complete`: do **not** advance or
rewrite anything. Reprint the stored `prs:` URLs and say the task is already
complete. This keeps Phase 6 strictly terminal.

---

## State transitions summary

| phase | status | gates key | Next `/w-task` triggers |
|-------|--------|-----------|---------------------------|
| "0" | gate_pending | — | Phase 0b (context load + figma_url update) |
| "1" | gate_pending | — | Write questions.md → GATE 1 |
| "1" | gate_pending | plan_written | Phase 2 (impact) |
| "2" | gate_pending | — | Phase 3 (UI / Figma) |
| "3" | gate_pending | skipped | Phase 4 (TDD) |
| "3" | gate_pending | assets_pending | Asset resolution loop |
| "3" | gate_pending | ui_verified | Phase 4 (TDD) |
| "4" | gate_pending | — | GREEN + checks cycle |
| "4" | gate_pending | checks_green | Phase 4c (browser verify AUTO) |
| "4" | gate_pending | browser_verified | Commit → Phase 5 |
| "4" | gate_pending | browser_not_applicable | Commit → Phase 5 (no UI scope) |
| "4" | gate_pending | browser_unavailable | Commit → Phase 5 (reason ships in PR) |
| "4" | gate_pending | browser_contended | Operator replies w / s / a → retry, skip, or hold |
| "4" | gate_pending | browser_skipped_by_operator | Commit → Phase 5 (decision noted) |
| "4" | gate_pending | browser_error | Commit → Phase 5 (with error noted) |
| "5" | gate_pending | pending | Phase 5 doc persist or skip |
| "5" | gate_pending | docs_written | Phase 5b AUTO (acceptance verify) |
| "5" | gate_pending | skipped | Phase 5b AUTO (acceptance verify) |
| "5b" | gate_pending | — | Phase 5b.1: run `w-acceptance-verify` |
| "5b" | gate_pending | accepted | Phase 6 AUTO (branch sync → doc gate → PR) |
| "5b" | gate_pending | accepted_with_gaps | Phase 6 AUTO, `open-issues.md` in PR body |
| "5b" | gate_pending | skipped | Phase 6 AUTO |
| "5b" | **blocked** | open_issues | Operator replies c / p / f → PR with gaps, re-plan, or hold |
| "6" | gate_pending | — | Phase 6.0: per-repo fetch + merge each repo's default branch |
| "6" | gate_pending | conflict_pending | Developer resolves conflicts in flagged repo → runs `/w-task` |
| "6" | gate_pending | synced | Phase 6.1: doc gate |
| "6" | gate_pending | doc_gate_passed | Phase 6.2: one PR per repo → 6.3 commit + push state → `status: complete` |
| "6" | **complete** | — | **Terminal** — no-op; reprints stored `prs:` URLs |

---

## Error recovery

If `state.yaml` shows `status: blocked`:
- Read `notes` field for blocker description.
- Surface to developer, wait for resolution before advancing.

If state.yaml is missing or corrupt: treat as first run, require `<issue-url-or-title>`.
