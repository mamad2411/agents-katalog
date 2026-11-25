---
description: Orchestrate a full feature dev workflow with browser verification (intake → context → plan → impact → UI → TDD → browser-verify → docs → PR). Adds Phase 4c localhost browser verification via Chrome DevTools MCP after TDD green. Reads project config from .claude/workflow.yaml.
argument-hint: <issue-url | #N | title>
allowed-tools: Bash, Read, Write, Edit, Skill
---

# w-task-v2

Full feature development workflow with browser verification. State-machine with explicit
gates — advances only when the developer runs `/w-task-v2`.

**First run:** `$ARGUMENTS` is an issue reference or free title → starts Phase 0.  
**Subsequent runs:** `$ARGUMENTS` empty or `continue` → reads `state.yaml`, advances to next phase.

Extends `w-task` with **Phase 4c — Browser Verify**: after TDD green and checks pass,
Claude starts the local dev server, uses Chrome DevTools MCP to verify UI changes at
`localhost` only, then waits for developer confirmation before committing.

---

## ⚠️ Invocation gate — read on every run

The workflow advances **only** when the developer explicitly runs `/w-task-v2`.

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
  If `dev_server_command` is null, Phase 4c is skipped entirely.
- `pr.default_branch`, `.draft`, `.template`

**Path convention — streaming-docs vs flat layout**

State and docs are two **separate** concerns. They MAY share a parent (the
streaming-docs convention puts them as siblings under `<docs_root>/`) but they
are configured independently — w-task-v2 always uses the explicit config fields,
never inference.

| Concern | Config field | Streaming-docs example | Flat-layout example |
|---|---|---|---|
| State (this task's working files) | `state_root` | `streaming-docs/workflow` | `.workflow` |
| Module docs | `module_docs_root` | `streaming-docs/documents/modules` | `docs/modules` |
| DB docs | `db_docs_root` | `streaming-docs/documents/database` | `docs/database` |
| OQ doc | `oq_docs_path` | `streaming-docs/documents/overview/open-questions.md` | `docs/open-questions.md` |
| ADR doc | `adr_docs_path` | `streaming-docs/documents/overview/architecture-overview.md` | `docs/adr.md` |

For task `CISTREAMIN-11-sign-up-api` on a streaming-docs-convention project, w-task-v2
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
| 0b | `w-context-load`, `w-oq-check` |
| 2 | `w-impact-analyzer`, `w-adr` |
| 4 | `w-test-stubs` |
| 4c | Chrome DevTools MCP (external — must be configured in settings.json) |
| 5 | `w-feature-record`, `w-api-doc`, `w-db-doc` |
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

Run /w-task-v2 when ready.
```

**has_ui: true — no figma URL in intake:**
```
Please confirm before we proceed:

1. Title: <title> — correct?
2. UI changes detected. Do you have a Figma design URL for this task?
   (paste URL, or reply "no Figma" to proceed without design snapshot)
3. Any additional constraints or context?

Run /w-task-v2 when ready.
```

**has_ui: false:**
```
Please confirm before we proceed:

1. Title: <title> — correct?
2. This looks like a backend-only change — confirm, or let me know if UI is involved.

Run /w-task-v2 when ready.
```

**has_ui: unknown:**
```
Please confirm before we proceed:

1. Title: <title> — correct?
2. Does this task include UI / frontend changes?
   (yes — provide Figma URL if available / no)
3. If the description above is incomplete, paste the correct one now.

Run /w-task-v2 when ready.
```

Write `state.yaml`:
```yaml
task: <task-slug>
phase: "0"
status: gate_pending
intake_confirmed: false
has_ui: <true|false|unknown>
figma_url: <url or null>
started_at: <timestamp>
last_updated: <timestamp>
```

**GATE 0:** developer replies in chat → runs `/w-task-v2`.

---

## Phase 0b — Codebase Snapshot (AUTO, runs immediately after GATE 0)

*Triggers when `phase: "0"` + `status: gate_pending` and developer runs `/w-task-v2`.*

Read developer's reply from GATE 0. Update `intake.md` with any corrections.

Update `state.yaml` from developer's reply:
- If developer confirmed/corrected Figma URL → update `figma_url`
- If developer said "no Figma" → set `figma_url: null`
- If developer confirmed UI involvement → set `has_ui: true`
- If developer confirmed backend-only → set `has_ui: false`

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

**If `workflow.module_docs_root` is NULL → fall back to generic git-grep load:**

1. **File inventory:**
   ```bash
   git ls-files | head -300
   ```
2. **Keyword grep:** extract 3-5 keywords, run `git grep -l "<keyword>"` per keyword.
3. **Read top 3-5** relevant files (scope by `project.src_dirs` if set).
4. **Write context.md** with the minimal generic template (Task Summary, Relevant
   Files, Patterns Observed, Suggested Approach — no module-specific sections).

**In both branches:**

5. Update `state.yaml`:
   ```yaml
   phase: "1"
   status: gate_pending
   intake_confirmed: true
   module: <name or null>
   last_updated: <timestamp>
   ```

Output: "Context loaded. Run `/w-task-v2` to start planning."

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

3. **Pause** — say: "Fill answers in `questions.md`, then run `/w-task-v2`."

4. Update `state.yaml`: `status: gate_pending`.

**GATE 1:** developer fills `questions.md` → runs `/w-task-v2`.

*After developer runs `/w-task-v2`:*

5. Read answered `questions.md`.

6. **Spawn `planner` agent** — pass as brief:
   - `intake.md` full content
   - `context.md` § Relevant Files + § Patterns Observed
   - Answered `questions.md`
   - Instruction: produce a plan with sections — Feature scope, Implementation approach per layer, Out of scope, Dependencies, Risks.

7. Write `plan.md` from agent output.

8. Update `state.yaml`: `gates.1: plan_written`, `status: gate_pending`.

Output: "Review plan.md. Run `/w-task-v2` to approve and proceed."

**GATE 1b:** developer reviews `plan.md` → runs `/w-task-v2`.

---

## Phase 2 — Impact & Design (AUTO → GATE 2)

*Triggers when `phase: "1"` + `status: gate_pending` + `gates.1: plan_written`.*

1. Read `context.md` + `plan.md`.

2. **Invoke skill** `w-impact-analyzer <task-slug>` — produces structured
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

3. **Manual ADR opportunity** — if a decision surfaced during the impact analysis
   that wasn't auto-captured, invoke `w-adr <task-slug> "<decision-title>"`
   to append it to `adr_docs_path`.

4. Update `state.yaml`: `phase: "2"`, `status: gate_pending`.

Output:
```
impact.md is ready. Before approving:
• Challenge assumptions — does the sequence diagram match your mental model?
• Update the design — if something is wrong, say so in chat and I'll revise.

This is the last checkpoint before implementation shape is committed.
Run /w-task-v2 when satisfied.
```

**GATE 2:** developer discusses / approves → runs `/w-task-v2`.

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
Output: "No UI scope detected. Run /w-task-v2 to start TDD."
```

**GATE 3 (skipped):** developer runs `/w-task-v2` → Phase 4.

---

### 3.1 — Extract Figma design snapshot

*Only runs when NOT skipped.*

Read `state.yaml.figma_url`.

**If `figma_url` is set:**

Invoke skill `f-extract <figma_url> --task <task-slug>`.

This writes `<state_root>/<task-slug>/figma-snapshot.md`.

If `f-extract` fails (MCP unavailable, URL invalid):
```
⚠️ Figma extraction failed: <reason>
Options:
  [1] Retry with a different URL or after configuring MCP (/f-setup)
  [2] Continue without snapshot — implementation will be based on plan.md only

Reply with your choice, then run /w-task-v2.
```
Wait for developer. If [2]: set `figma_url: null`, proceed to 3.2 without snapshot.

**If `figma_url` is null:**
```
No Figma URL available. Proceeding to implementation based on plan.md only.
UI accuracy may be limited without a design snapshot.
```
Proceed to 3.2 without snapshot.

---

### 3.2 — Implement UI

Invoke skill `f-implement`:
- With snapshot: `f-implement <state_root>/<task-slug>/figma-snapshot.md --plan <state_root>/<task-slug>/plan.md`
- Without snapshot: `f-implement --plan <state_root>/<task-slug>/plan.md` (plan-only mode — f-implement reads plan.md for UI scope)

`f-implement` will:
- Generate components and screens
- Use `ASSET_PLACEHOLDER` for all icons/images
- Gate on developer when design is unclear (shows Figma link + requests PNG)
- Write `figma-assets.md` if any assets are unresolved

Do not advance Phase 3 until `f-implement` reaches its summary step.

---

### 3.3 — Asset resolution gate

*Only runs if `figma-assets.md` exists and has unresolved entries.*

Read `<state_root>/<task-slug>/figma-assets.md`.

If all assets resolved: skip to 3.4.

Output:
```
## UI assets needed

<N> assets require export from Figma before implementation is complete.
See figma-assets.md for Figma links and target paths.

Export each asset from Figma and place at the listed path.
Run /w-task-v2 when done — I will replace the ASSET_PLACEHOLDER comments.
```

Update `state.yaml`: `status: gate_pending`, `gates.3a: assets_pending`.

**GATE 3a:** developer exports assets → runs `/w-task-v2`.

When developer runs `/w-task-v2` with `gates.3a: assets_pending`:
- Re-read `figma-assets.md`
- For each asset: check if file exists at `target_path`
- Replace all `ASSET_PLACEHOLDER` comments for resolved assets
- If any still missing: re-show only the remaining entries, wait again
- When all resolved: proceed to 3.4

---

### 3.4 — Finalize Phase 3

Update `state.yaml`: `gates.3: ui_verified`, `phase: "4"`, `status: gate_pending`.

Output: "UI implementation complete. Run `/w-task-v2` to start TDD."

**GATE 3b:** developer runs `/w-task-v2` → Phase 4.

---

## Phase 4 — TDD (AUTO → GATE 4a)

*Triggers when `phase: "4"` + `status: gate_pending`.*

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

Output: "Review tests.md — confirm test structure covers impact.md scope. Run `/w-task-v2` to approve."

**GATE 4 (mini):** developer confirms → runs `/w-task-v2`.

6. **Run `w-checkpoint RED <task-slug>`** — checkpoint before implementation.

7. **Invoke `tdd-workflow` skill** — pass `plan.md` + `tests.md` as context for RED→GREEN→refactor.

8. Run tests → confirm GREEN.

9. **Run `w-checkpoint GREEN <task-slug>`** — checkpoint after GREEN.

10. **Inline checks** — in order, report each result:

    Resolve commands from config (expand `auto`):
    - Typecheck: `<typecheck_command>` on whole project
    - Lint: `<lint_command>` on affected files from `impact.md`
    - Tests with coverage (if test command supports it)

11. **Spawn `code-reviewer` agent** — scope: affected files from `impact.md` only:
    - Resolve CRITICAL/HIGH issues immediately, re-run tests to confirm still GREEN.
    - Document MEDIUM items in `tests.md § Code Review Notes`.

12. Write `verify.md`:
    ```markdown
    # Verify — <title>

    | Check | Result | Notes |
    |-------|--------|-------|
    | typecheck | ✅/❌ | |
    | lint | ✅/❌ | |
    | tests | ✅/❌ | |
    | code review | ✅/❌ | CRITICAL/HIGH resolved |
    ```

13. Update `tests.md`: add RED→GREEN record + reference `verify.md`.
14. Update `state.yaml`: `status: gate_pending`, `gates.4a: checks_green`.

Output: "Code is GREEN and checks pass. Review verify.md and diff. Run `/w-task-v2` to proceed to browser verify."

**GATE 4a:** developer reviews verify.md + diff → runs `/w-task-v2`.

---

## Phase 4c — Browser Verify (AUTO → GATE 4c)

*Triggers when `phase: "4"` + `status: gate_pending` + `gates.4a: checks_green` + no `gates.4c`.*

**Skip conditions (set `gates.4c: browser_skipped` and proceed to GATE 4c immediately):**
- `project.dev_server_command` is null or unset in `workflow.yaml`
- `plan.md` contains no UI changes (no frontend/component/page/CSS/style mentions)
- `chrome-devtools` MCP tools are unavailable

If skipping: output "Browser verify skipped (<reason>). Run `/w-task-v2` to commit."

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

Output: "Browser verify complete. Review verify.md § Browser Verify and screenshots. Run `/w-task-v2` to commit."

**GATE 4c:** developer reviews browser verify results → runs `/w-task-v2`.

---

15. **Commit the implementation**:
    ```bash
    git add <files from impact.md § Affected Files>
    git commit -m "feat(<scope>): <one-line summary from plan.md>"
    ```
    Do NOT use `git add -A` — stage only files listed in `impact.md`.

16. Update `state.yaml`: `phase: "5"`, `status: gate_pending`, `gates.4b: committed`.

Output: "Implementation committed. Run `/w-task-v2` to proceed to doc persistence."

**GATE 4b:** developer runs `/w-task-v2` → Phase 5.

---

## Phase 5 — Persist Docs (CONDITIONAL → GATE 5)

*Triggers when `phase: "5"` + `status: gate_pending`.*

Read doc-related fields from `workflow.yaml`.

**If `docs_root` is null AND `module_docs_root` is null:** skip entirely.
Update `state.yaml`: `gates.5: skipped`, `phase: "6"`, `status: gate_pending`.
Output: "Doc roots not configured — skipping. Run `/w-task-v2` to create the PR."

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

Output: "Docs persisted and committed. Review changes, then run `/w-task-v2` to
create the PR (which will trigger w-doc-gate)."

**GATE 5:** developer reviews + runs `/w-task-v2`.

Update `state.yaml`: `phase: "6"`, `status: gate_pending`.

---

## Phase 6 — PR

*Triggers when `phase: "6"` + `status: gate_pending`.*

`/w-pr` (Phase 6) will internally invoke `w-doc-gate <task-slug>` before
opening the PR. The doc gate verifies:
- Every module touched (code changes under `module_glob`) has a corresponding
  doc update in the branch diff
- If `master_erd_path` is configured, any sub-ERD change is accompanied by
  a master ERD update in the same branch

If the gate fails, `/w-pr` blocks PR creation and prints the missing doc paths
— developer must return to Phase 5 (`/w-task-v2`) to fill the gap.

Output: "Run `/w-pr <task-slug>` to create the PR (w-doc-gate runs first)."

**GATE 6:** developer runs `/w-pr <task-slug>`.

Update `state.yaml`: `phase: "6"`, `status: complete`, `last_updated: <timestamp>`.

Output: "Task complete. Docs ship with code in this PR — no post-merge sync needed."

---

## State transitions summary

| phase | status | gates key | Next `/w-task-v2` triggers |
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
| "4" | gate_pending | browser_skipped | Commit → Phase 5 |
| "4" | gate_pending | browser_error | Commit → Phase 5 (with error noted) |
| "5" | gate_pending | pending | Phase 5 doc persist or skip |
| "5" | gate_pending | docs_written | Phase 6 (PR) |
| "6" | gate_pending | — | Dev runs `/w-pr <task-slug>` → complete |

---

## Error recovery

If `state.yaml` shows `status: blocked`:
- Read `notes` field for blocker description.
- Surface to developer, wait for resolution before advancing.

If state.yaml is missing or corrupt: treat as first run, require `<issue-url-or-title>`.
