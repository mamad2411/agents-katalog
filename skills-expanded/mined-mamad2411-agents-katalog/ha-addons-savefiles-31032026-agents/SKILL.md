# Agentenregeln

## Codestyle Regeln

### Repo Layout (important for HA)

- `repository.yaml`: must stay in repo root for Home Assistant add-on repositories.
- `influxbro/config.yaml`: add-on metadata (versioning, slug, ingress settings).
- `influxbro/Dockerfile`: container build.
- `influxbro/run.sh`: add-on entrypoint (reads `/data/options.json`).
- `influxbro/app/app.py`: Flask app.
- `influxbro/app/templates/*.html`: UI templates (inline JS/CSS).

Constraints:

- Do not rename the add-on directory or change `slug` in `influxbro/config.yaml`.
- Home Assistant detects updates via the `version:` field in `influxbro/config.yaml`.
- The container expects HA mounts:
  - `/data` (writable, persistent)
  - `/config` (read-only in this add-on)

### Code Style Guidelines

### General

- Keep changes minimal and consistent with existing patterns (Flask + inline templates).
- Prefer readability over cleverness; this add-on is operated by Home Assistant users.
- Do not introduce new dependencies unless they are clearly justified.

### Python formatting

- Indentation: 4 spaces.
- Strings: prefer double quotes for user-facing text consistency in this codebase.
- Use f-strings for formatting.
- Keep lines reasonably short (~100 chars) unless it harms clarity.

### Imports

- Group and order imports:
  1) standard library
  2) third-party
  3) local imports
- One import per line when practical.
- Avoid unused imports.

Example:

```py
import json
from pathlib import Path

from flask import Flask, jsonify, request
```

### Types

- Add type hints for new/changed functions.
- Prefer built-in generics: `dict[str, object]`, `list[str]`.
- For JSON-like payloads, use `dict[str, Any]` and validate/normalize at the boundary.

### Naming

- Functions/vars: `snake_case`.
- Constants: `UPPER_SNAKE_CASE`.
- Flask route handlers: short verb-ish names (`measurements`, `fields`, `api_test`).
- Private helpers: prefix with `_`.

### Error handling and API responses

- Treat Flask routes as trust boundaries:
  - validate required params
  - normalize types (`int(...)`, `bool(...)`)
  - return clear errors with appropriate HTTP status codes.
- Prefer a consistent JSON envelope for API endpoints:
  - success: `{"ok": true, ...}`
  - error: `{"ok": false, "error": "..."}`
- Avoid broad `except Exception` in pure helpers; it is acceptable at the HTTP boundary to
  prevent crashes, but include useful error messages and status codes.

### Security / Safety

- Never log or return secrets (token/password). Keep the existing redaction behavior.
- Any path coming from users must be constrained; keep traversal protections like
  `_resolve_cfg_path()` and extend them rather than bypassing.
- Deletion must remain opt-in:
  - gated by `ALLOW_DELETE`
  - requires exact confirmation phrase

### Flask + InfluxDB conventions

- InfluxDB v2 clients should be context-managed and closed (`with v2_client(cfg): ...`).
- For v1 client usage, keep timeouts and SSL verification configurable.
- Keep query size bounded (the UI downsamples to ~5000 points); preserve or improve this.

### Templates (HTML/JS/CSS)

- Keep templates self-contained; no build step exists.
- Use relative URLs (`./api/...`) to work under HA Ingress.
- Keep JS simple (no framework). Prefer small functions and explicit DOM lookups.
- For destructive actions, preserve confirmation UI and add additional guardrails if needed.

## Versioning / Releases (Home Assistant add-on)

- Jede Codeaenderung erfordert zwingend eine neue Version.
  - Wenn Dateien mit Code oder Laufzeitlogik geaendert werden (z. B. `*.py`, `*.html`, `*.js`, `*.css`, Docker-/Start-/Shell-Logik, Laufzeit-Configs), MUSS immer eine neue Add-on-Version erzeugt werden.
  - Dies gilt auch fuer kleine Korrekturen, Umstrukturierungen und rein technische Anpassungen.

- Bump `version:` in `influxbro/config.yaml` for any user-visible change.
- Do not change `slug:`.
- Keep `repository.yaml` in the repo root.

## Workflow Rule (Repo Convention)

- If you change add-on behavior (Python/HTML/JS/CSS, Dockerfile, run scripts, configs that affect runtime), also:
  - bump `influxbro/config.yaml:version` (so Home Assistant detects the update)
  - add an entry to `influxbro/CHANGELOG.md` for that version
  - update the user handbook `influxbro/MANUAL.md` so it reflects the current UI/behavior for that version
  - verify `influxbro/CHANGELOG.md` completeness/order (the file MUST list version entries in descending order, newest version at the top)
    - The CHANGELOG.md must present versions in strict descending order (most recent first). When adding a new entry, insert it at the top under the new version heading.

## Dependency / Compatibility Rule

- If you change Python dependencies (new imports, add/remove packages, or behavior that requires a new library version), update `influxbro/requirements.txt` in the same change.
- For each released add-on version, record the Home Assistant Core version the add-on was tested with.
  - Preferred place: the corresponding entry in `influxbro/CHANGELOG.md` (e.g. a Maintenance bullet: `Tested with Home Assistant Core: 2026.3.0`).
  - If the HA version cannot be determined in the current environment, explicitly note it as `unknown` and update once you have the value.

## Logging Rule (Support)

- Ensure user-visible UI errors are also written to the add-on log file.
  - In particular: client-side/network errors like "Failed to fetch" must be reported from the browser to the backend and logged.
  - When adding new UI error messages, verify they show up in `Logs` (logfile) during failure scenarios.

## Issue Regeln

### Requirements Tracking (preferred: GitHub Issues)

- Track requirements primarily as GitHub Issues so others can create/report items externally.
- Use the issue templates to distinguish between:
  - Bug reports (not working): label with `type/bug`
  - Enhancements (feature requests): label with `type/enhancement`
- Use exactly one status label per issue: `status/open`, `status/in_progress`, `status/done`, `status/cancelled`.
- Ensure the label set exists in GitHub (create once in the GitHub UI); the issue templates assume these labels are available.
- When implementing, link PRs to issues and close them via `Fixes #<id>`.

### GitHub Issues: Check, Select, Sync

- Always check for open GitHub Issues when starting work on new items (unless the user explicitly points to a specific issue).
  - Commands:
    - `gh issue list --repo <owner>/<repo> --state open --limit 200`
    - `gh issue list --repo <owner>/<repo> --state open --label type/bug --limit 200`
    - `gh issue list --repo <owner>/<repo> --state open --label type/enhancement --limit 200`
- Issues mit dem Label `rememberme` duerfen bei Issue-Pruefung, Triage oder Sammelumsetzung NICHT bearbeitet, umgesetzt, veraendert, kommentiert, geschlossen oder in Auswahl-/Umsetzungspakete aufgenommen werden.
- `rememberme`-Issues sind bei jeder Bearbeitung offener Issues strikt zu ueberspringen, auch wenn der Benutzer allgemein nach offenen Issues oder nach "allen Issues" fragt.
- Present open items grouped by **Bugs** (`type/bug`) vs **Enhancements** (`type/enhancement`).
- The user must be able to decide per issue:
  - implement now
  - defer (backlog)
  - decline
- This per-issue decision flow applies only during explicit triage mode.
- If the user explicitly requests implementation of all open issues or a defined subset of open issues, do NOT require per-issue decisions and process the selected issues immediately.

- Reflect the user's decision back to GitHub:
  - implement now: set `status/in_progress` and (optionally) add a short comment "picked for implementation"
  - defer: keep `status/open` and add a short comment "deferred"
  - decline: set `status/cancelled`, add a short comment with reason (if provided), and close the issue
- When implementation is finished:
  - set `status/done`
  - add a comment with the PR URL and/or commit hash
  - close the issue
- Wenn du angewiesen wirst, offene Issues zu bearbeiten oder abzuarbeiten, musst du vor jeder Umsetzung den gesamten Issue-Text, alle Kommentare und insbesondere die neuesten Kommentare/Fehlermeldungen lesen und beruecksichtigen.
- Die neueste Information im Issue hat Vorrang vor aelteren Annahmen; keine Umsetzung auf Basis veralteter Informationen.
- Vor jeder Aenderung muss der aktuelle Ist-Zustand der betroffenen Datei(en) gelesen werden; nicht auf erwartete oder fruehere Versionen verlassen.
- Bei `apply_patch verification failed` ist verpflichtend:
  1. betroffene Datei erneut lesen
  2. Zielstelle auf Basis des echten Inhalts neu identifizieren
  3. Patch robust mit Ankern/Kontext statt unveraenderten Erwartungszeilen neu erstellen
- Nach jeder Issue-Umsetzung muss der Issue-Kommentar mindestens enthalten:
  - Ursache des Problems
  - gewaehlte Loesung
  - Commit-Hash und/oder PR-Link
- Sync selected issues into the local open-points list:
  - add chosen "implement now" issues to the in-chat ToDo list and to `./.opencode/plan_state.md` (with `#<id>` + title)
  - when the issue is completed/declined/deferred, update `./.opencode/plan_state.md` accordingly

### GitHub Issues: Proactive Prompting

- In plan mode, after presenting the plan for the user's request, ALWAYS ask whether the user wants to triage GitHub Issues now.
- After finishing implementation of the user's selected points (i.e. when the ToDo list is completed), ALSO ask whether the user wants to triage GitHub Issues next.

Triage flow:

- List open issues grouped by Bugs (`type/bug`) vs Enhancements (`type/enhancement`).
- Let the user pick issues to:
  - implement now
  - defer
  - decline
- Before implementation, allow the user to add/clarify requirements per selected issue (short additions to title/body/acceptance criteria).
  Apply these clarifications to the GitHub issue as a comment (or by editing the issue body) so the context is preserved.
- Only issues explicitly chosen as "implement now" are synced into the in-chat ToDo list and mirrored into `./.opencode/plan_state.md`.

### Shortcut: "prüfe Issues" Verhalten

- Wenn der Benutzer genau die Phrase `prüfe Issues` eingibt, zeige zuerst eine kurze Auswahlfrage (ohne Issues vorab zu laden):
  1) `Alle Issues umsetzen` — alle offenen Issues sofort und ohne weitere Nachfragen umsetzen.
  2) `Auswahl treffen` — zuerst die Liste der offenen Issues anzeigen (gruppiert nach `type/bug` vs `type/enhancement`) und dem Benutzer erlauben, auszuwählen, welche umgesetzt werden sollen.
- WICHTIG: Die Issue‑Liste darf vor der Auswahl nicht geladen oder angezeigt werden — die erste Frage ist ausschließlich dazu da, den Flow zu bestimmen.
- Verhalten bei Auswahl:
  - Wahl 1: Sofort mit der Implementierung aller Issues fortfahren (Änderungen anwenden, Tests/QAs ausführen, `influxbro/config.yaml` version bump, commit und push), ohne weitere per‑Issue Rückfragen.
  - Wahl 2: Normale Triage: Issues auflisten, Auswahl ermöglichen, dann die ausgewählten Issues implementieren.
- Diese Verhaltensregel ist eine Agenten‑Policy und wird in dieser Datei dokumentiert, damit sie persistent ist.

### Requirements Log (local, fallback)

- If GitHub Issues are not available, record user requirements/requests (as written) in `./.opencode/requests_log.md` with date + status.
- Status values: `open`, `in_progress`, `done`, `cancelled`.
- Keep this file local (do not commit); it is not synced to GitHub.
- Update the status when work starts/completes/cancels; optionally include the commit hash/PR link in the entry.

### Persist Plan Changes (VSCode/code-server restarts)

- Mirror the current ToDo/plan state to a workspace file on every meaningful change so it survives editor/server restarts.
  - File: `./.opencode/plan_state.md`
  - Contents: current ToDo list (incl. status), open decisions/questions, and any agreed plan changes.
- At the start of a new session, if `./.opencode/plan_state.md` exists, load it first and restore the pending items before proceeding.
- Keep this file local (do not commit); it is session state, not project source.

## Testing Regeln

### Mandatory Testing & Cost-Aware Execution (REQUIRED)

After every implementation, testing is REQUIRED, but execution must remain cost-efficient.

### Required QA Flow

Run validation in this order:

1. Syntax / static sanity check first
2. Targeted tests second
3. Runtime / API smoke checks only if relevant
4. Docker/build verification only if relevant
5. Broader validation only if earlier checks fail, the user explicitly requests it, or the change is high-risk

Minimum requirements:

- Syntax check is ALWAYS required:
  - `python -m py_compile influxbro/app/app.py`
- Targeted tests are required WHEN AVAILABLE for the changed functionality:
  - single test by node id
  - single test file
  - keyword-filtered pytest run
- Runtime / API smoke tests are required WHEN RELEVANT for backend routes, request handling, config loading, or UI-triggered API actions.
- Docker verification is required ONLY WHEN RELEVANT for runtime behavior, dependencies, container behavior, startup scripts, add-on packaging, or config handling.
- UI verification is required WHEN RELEVANT for templates, JavaScript, or browser interactions:
  - verify the affected page loads
  - verify the changed interaction path only
  - avoid broad manual retesting of unrelated pages

Execution constraints:

- Prefer targeted reads over full-file rereads.
- Prefer targeted tests over full test suites.
- Do not rerun the same failing test repeatedly without making a change.
- Do not perform Docker/runtime validation if the change is clearly documentation-only or non-runtime-only.
- Use minimal sufficient QA by default; do not automatically expand to full end-to-end or heavy integration tests unless needed.

Failure handling and completion:

- If any required check fails:
  - do NOT declare the work complete
  - fix the issue first
  - rerun the smallest relevant validation set
  - escalate validation scope only if needed
- If a user-reported or agent-reproduced UI/browser-visible error remains present after at least one concrete fix attempt, explicitly offer a Playwright-based browser test to validate the real interaction path.
- Implementation is ONLY complete if all relevant required checks passed.
- After completing all REQUIRED tests, DO NOT ask the user whether additional testing should be performed unless:
  - the user explicitly requested it
  - critical functionality could not be tested
  - the test environment is incomplete

Reporting:

- At the end of the task, explicitly report:
  - which checks were executed
  - which were skipped
  - why they were skipped
  - final result of each executed check

## Build / Run / Lint / Test

### Build the add-on image

From repo root:

```bash
docker build -t influxbro:dev ./influxbro
```

### Run locally (Docker)

Minimum (no HA supervisor; you must provide `/data/options.json` yourself):

```bash
mkdir -p .local-data
cat > .local-data/options.json <<'JSON'
{ "version": "dev", "allow_delete": false, "delete_confirm_phrase": "DELETE" }
JSON

docker run --rm -p 8099:8099   -v "$PWD/.local-data:/data"   -v "$PWD:/repo:ro"   influxbro:dev
```

Notes:

- The UI is served on `http://localhost:8099/`.
- In real HA, Ingress changes the base path; keep relative URLs (current templates do).

### Run locally (Python, outside Docker)

This repo does not ship a lockfile/pyproject; for quick iteration:

```bash
python3 -m venv .venv
. .venv/bin/activate
python -m pip install -U pip
python -m pip install flask influxdb-client influxdb PyYAML

# emulate add-on env
export ALLOW_DELETE=false
export DELETE_CONFIRM_PHRASE=DELETE
export ADDON_VERSION=dev

python influxbro/app/app.py
```

### Lint / Static checks

There is no enforced linter in CI today, but ruff/black + pre-commit config exist.

Baseline checks that should always work:

```bash
python -m compileall influxbro/app/app.py
python -m py_compile influxbro/app/app.py
```

Recommended (optional) tooling for agents:

```bash
python -m pip install ruff black
ruff check influxbro/app/app.py
black --check influxbro/app/app.py

# or run via pre-commit
python -m pip install pre-commit
pre-commit run --all-files
```

### Tests

Pytest is available (see `tests/` + `pytest.ini`). Prefer patterns that make running a single test easy:

```bash
# run one file
pytest tests/test_api_yaml_flow.py -q

# run one test by node id
pytest tests/test_api_yaml_flow.py::test_load_influx_yaml_resolves_secret -q

# run a subset by keyword
pytest -k measurements -q
```

### Manual “single test” (API smoke)

After starting the app, these are useful targeted checks:

```bash
curl -fsS http://localhost:8099/api/info | jq .
curl -fsS http://localhost:8099/api/config | jq .

# connectivity test uses the posted form values
curl -fsS -X POST http://localhost:8099/api/test   -H 'Content-Type: application/json'   -d '{"influx_version":2,"scheme":"http","host":"localhost","port":8086,"verify_ssl":true,"timeout_seconds":10,"org":"...","bucket":"...","token":"..."}' | jq .
```

## Workflow Regeln

## 📦 Bulk File Processing & Large Context Handling (CRITICAL)

### General Rule

- NEVER load or analyze all files at once.
- ALWAYS process files in small batches or individually.

### HTML / Template Analysis

When analyzing HTML, Jinja2 templates, or UI files:

- Process ONE file at a time.
- Do NOT preload multiple templates into context.
- Limit file reads to only the relevant sections when possible.

### Iterative Processing Strategy

For tasks like:

- "analyze all HTML files"
- "check all templates"
- "validate project structure"

The agent MUST:

1. Discover file list first
2. Iterate over files one-by-one
3. Analyze each file independently
4. Summarize results incrementally
5. NEVER accumulate full file contents in memory

### Output Constraints

- Do NOT output full file contents unless explicitly requested
- Only output:
  - errors
  - relevant snippets
  - line references
- Prefer summaries over full dumps

### Token Safety Rules

- If context grows too large:
  - STOP processing
  - summarize current findings
  - continue in next iteration

- Avoid large diffs and full-file outputs

### HTML Validation Rules

When validating HTML structure:

- Focus on:
  - tag balance (<div>, <main>, <section>, <details>)
  - nesting correctness
  - parent/child hierarchy
- Ignore:
  - styling
  - JavaScript
  - unrelated content

### Preferred Workflow

1. Identify target files
2. Loop:
   - read file
   - analyze structure
   - report issues
3. Final summary

### Hard Constraint

The agent MUST NOT:

- load entire project into context
- analyze more than 1–2 files simultaneously
- produce large unstructured outputs

### Parallel Execution Strategy (CONTROLLED)

### General Rule plus

- Parallel execution is allowed ONLY for clearly independent read, search, and validation tasks.
- If one task can affect the assumptions, design, or implementation of another task, analysis MUST be sequential.

### Allowed Parallel Tasks

The following may run in parallel ONLY if they are independent:

- reading unrelated files
- searching the codebase
- reviewing open GitHub issues
- collecting logs
- locating relevant tests

### Sequential Analysis Required

Analysis MUST remain sequential if:

- tasks affect the same files or modules
- one change can alter the design of later changes
- API, UI, and config behavior are connected
- there is any uncertainty about dependency order

### Write Operations

- All code changes MUST remain strictly sequential.
- Version bump, changelog, manual updates, commit, and push MUST remain strictly sequential.

### Safety Rule

- When in doubt, prefer sequential analysis over parallel analysis.

### Plan Mode Workflow

When plan mode is active:

- Create a detailed plan first.
- Show all tasks that need to be done.
- Group tasks logically.
- Wait for explicit user approval before implementing anything (no file edits, no commits, no pushes).

### Plan Mode Must Not Interrupt Active Build Execution

- If a build/GO execution was already explicitly approved and implementation has already started, that execution remains active until a logical completion point is reached.
- A later switch into plan mode MUST NOT retroactively stop, block, or reinterpret that already running build execution as read-only work.
- New requests that arrive while such an active build execution is still running may be acknowledged internally, but they MUST be answered or handled only after the running build execution is completed, unless the user explicitly asks to stop or abort the build.
- In this situation, plan mode applies only to new, not-yet-started work items and MUST be deferred until the active build execution is finished.
- If additional build/GO-style execution requests arrive while a build execution is already active, they MUST NOT interrupt the running build. They are to be placed into a sequential execution queue and handled one after another after the current build reaches a logical completion point.
- If additional plan-mode requests arrive while a deferred plan queue already exists behind an active build, those plan requests are also to be queued and answered sequentially after the active build and after any earlier queued plan items.
- Only an explicit user interruption such as `stop`, `abbrechen`, or an equivalent direct cancellation instruction may interrupt a running build execution in favor of plan work.

### Build Mode Must Not Interrupt Active Plan Work

- If plan mode work was already explicitly requested and the agent is actively producing that plan, analysis, or decision-preparation output, a later build/GO instruction MUST NOT retroactively abort or skip that ongoing plan work mid-response.
- The active plan work must first reach a logical completion point for the current answer before any newly requested build execution starts.
- In this situation, the later build/GO request is to be deferred and executed immediately after the running plan response is completed, unless the user explicitly instructs the agent to stop planning and switch immediately.
- This rule applies only to already active plan work; once the current planning response is finished, the deferred build/GO execution becomes the next required action.
- If additional plan-mode requests arrive while plan work is already active, they MUST NOT interrupt the running plan response. They are to be placed into a sequential plan queue and answered one after another after the current plan item reaches a logical completion point.
- If additional build/GO requests are already queued behind active plan work, those build requests must also be handled sequentially in queue order after the active plan response and after any earlier queued items.
- Only an explicit user interruption such as `stop`, `abbrechen`, or an equivalent direct cancellation instruction may interrupt a running plan response in favor of immediate build execution.

### Task Tracking (ToDo List)

- Always create and show a ToDo list for the current request.
- When the user adds new requirements, extend the existing ToDo list immediately.
- Keep exactly one item `in_progress` at a time.
- Mark items `completed` as soon as they are done.
- Ensure all ToDo items are implemented before you claim the work is finished.

## Autonomous Execution Policy (NO INTERMEDIATE QUESTIONS)

### Core Rule

- If the user explicitly approves implementation (e.g. "implement all issues", "go", or equivalent),
  the agent MUST execute all tasks end-to-end WITHOUT asking intermediate questions.

### No-Interruption Rule

- DO NOT ask for:
  - step-by-step confirmation
  - prioritization choices
  - “how should I proceed?” questions
  - numbered selection prompts (1/2/3)

- Once execution is approved:
  - proceed through ALL ToDo items automatically
  - only stop if a real blocker exists

### Allowed Interruptions (ONLY THESE)

The agent MAY interrupt execution ONLY if:

- critical information is missing (cannot proceed)
- external dependency is required (e.g. credentials, API access)
- multiple valid implementations exist with significant impact
- a destructive or irreversible action is required

### Default Behavior

- Assume: user wants FULL execution of approved tasks
- Execute tasks sequentially until:
  - all ToDo items are completed OR
  - a real blocker is encountered

### Handling Multi-Issue Execution

If multiple issues are selected:

- process issues sequentially
- complete one issue fully before starting the next
- DO NOT ask between issues
- DO NOT re-confirm execution
- Wenn der Benutzer verlangt, dass offene Issues abgearbeitet werden, dann gilt dies fuer ALLE von ihm ausgewaehlten Issues, bis diese vollstaendig umgesetzt sind.
- Formulierungen wie `arbeite alle Issues ab` oder `arbeite alle Issues ausser #134 ab` sind als vollstaendige Arbeitsanweisung zu verstehen; sie benoetigen keine zusaetzliche Bestaetigung, kein weiteres `GO` und keine Rueckfrage zur Paketbildung.
- Wenn der Benutzer einzelne Issues explizit ausschliesst, dann sind alle uebrigen offenen Issues automatisch zur Umsetzung ausgewaehlt.
- Wenn mehrere kleinere Umsetzungspakete sinnvoll sind, duerfen diese Pakete nacheinander erstellt werden, aber:
  - die restlichen vom Benutzer angeforderten Issues bleiben verpflichtend offen im Plan
  - sie muessen danach automatisch weiter bearbeitet werden
  - es darf nicht nach dem ersten Paket stehen geblieben werden, solange kein echter Blocker existiert
- Offene Issues, die laut Benutzer umgesetzt werden sollen, muessen selbststaendig automatisch weiter bearbeitet und abgeschlossen werden, bis keine solcher Issues mehr offen sind.

### Reporting

- Only report:
  - after a logical block is completed (e.g. one issue fully implemented), OR
  - at the very end

- Reporting must NOT include questions unless a blocker exists
- Reporting after one completed issue is allowed, but reporting must NOT pause or block continued execution when the user explicitly requested that multiple issues be processed automatically.
- After reporting one completed issue, immediately continue with the next selected issue unless a real blocker exists.

## End-of-Implementation Verification (Required)

- At the end of every implementation, explicitly verify that all requirements and all ToDo items were actually implemented.
- If any planned item could not be implemented (or remains only partially implemented), explicitly call it out with:
  - what is missing
  - why it is missing
  - what would be needed to complete it
- Perform a final checklist-style confirmation before declaring the work finished.

## Auto Push & PR Policy (ENFORCED – HA MAIN-FIRST MODE)

### Core Principle

- Home Assistant ONLY detects updates from the `main` branch.
- Therefore ALL changes MUST be pushed to `main` to enable testing inside Home Assistant.
- Feature branches and PR-only workflows are NOT the default in this repository.

### Mandatory Completion Flow (NO SILENT STOP)

After successful implementation AND completed QA:

- DO NOT ask for confirmation.
- ALWAYS complete this sequence for build/GO execution when applicable:
  1. run required QA
  2. classify any failures as either:
     - fix-related/blocking
     - pre-existing/unrelated
  3. if failures are only pre-existing/unrelated, continue mandatory completion flow
  4. bump `influxbro/config.yaml` version when runtime, UI, API, or behavior changed
  5. stage changes
  6. create commit
  7. push to `main`
  8. report result clearly in chat
- It is FORBIDDEN to stop after code changes or after QA only, if the policy in this file requires version bump, commit, and push.
- It is FORBIDDEN to treat `build` mode as mere permission while skipping mandatory completion steps.
- Before declaring implementation complete, explicitly verify:
  - implementation finished
  - required QA executed
  - QA result classified
  - `influxbro/config.yaml` version bumped if required
  - changes staged
  - commit created
  - push to `main` completed
- If any item is missing, the task is NOT complete.

### Version Bump (CRITICAL FOR HA)

- Jede Aenderung am Code erzwingt eine neue Version.
  - Sobald Python, HTML, JavaScript, CSS, Docker-, Shell- oder sonstige Laufzeit-/Build-Logik geaendert wird, MUSS zwingend eine neue Add-on-Version erzeugt werden.
  - Es gibt keine Ausnahmen fuer kleine Fixes, Refactorings oder rein strukturelle Codeaenderungen.

- Every change that affects runtime, UI, API, or behavior MUST:
  - increment `version` in `influxbro/config.yaml`

- Without version bump:
  - Home Assistant will NOT detect an update
  - die Aenderung gilt in diesem Repository als unvollstaendig

- Version format:
  - increment last digit (e.g. 1.12.44 → 1.12.45)

### Live Verification Gate (CRITICAL FOR HA)

- Before any live verification against Home Assistant / the running add-on instance, the required code changes MUST already be available as an add-on version on `main`.
- Therefore, before a live check against the HA instance, the agent MUST first:
  - stage changes
  - create commit
  - bump `influxbro/config.yaml` version if runtime/UI/API/behavior changed
  - push to `main`
- The agent MUST NOT rely on local-only uncommitted changes for HA live verification.
- If the live instance still runs an older version, the agent must explicitly state that the requested live verification cannot validate the new code until the updated add-on version is installed in Home Assistant.

### Decision Logic (SIMPLIFIED FOR HA)

Default rule:

- If a change affects runtime, UI, API, or behavior, use the HA main-first flow:
  - commit
  - bump version
  - push directly to `main`

High-risk exception handling:

- If the change involves security-related logic, deletion logic, major architecture changes, or unclear side effects:
  - STILL push to `main` for HA testing
  - BUT:
    - ensure stricter QA before push
    - clearly label the commit message with `⚠ HIGH-RISK`

### Optional Branch Usage (LIMITED)

Branches MAY be used ONLY if:

- change can be tested locally WITHOUT Home Assistant
- OR user explicitly requests PR workflow

Otherwise:

- ALWAYS use `main`

### Commit Rules

- Use structured commit messages:
  - feat: for new features
  - fix: for bug fixes
  - refactor: for restructuring
  - chore: for maintenance

- Include short summary + key changes

- For risky changes:
  - prefix with: `⚠ HIGH-RISK`

### Issue-, Commit- und Pull-Request-Workflow

- Vor jeder Umsetzung muss die Aenderung eingeordnet werden:
  - klein, eindeutig, risikoarm -> direkter Commit
  - komplex, mehrdeutig, mehrere Dateien oder potenziell riskant -> strengere Analyse, erweiterte QA und nur bei ausdruecklichem Benutzerwunsch Branch/PR-Workflow
- In diesem Repository gilt weiterhin die HA-Main-First-Regel:
  - Standard ist direkter Commit nach `main`
  - PR/Branch nur wenn der Benutzer dies ausdruecklich verlangt oder wenn die bestehende Repo-Policy explizit dafuer geaendert wird
- Auch wenn eine Issue existiert, ist nicht automatisch ein PR erforderlich; entscheidend sind Komplexitaet, Risiko und Repo-Policy.
- Vor jeder Umsetzung ist verbindlich zu klaeren:
  - betroffene Dateien/Logikbereiche
  - Ursache des Problems
  - ob die Loesung klein und eindeutig ist oder interpretative/risikoreiche Annahmen enthaelt
- Wenn eine Umsetzung fehlschlaegt:
  - denselben Ansatz nicht blind wiederholen
  - aktuellen Datei-Iststand neu lesen
  - Ursache analysieren
  - Loesung auf Basis des realen Zustands neu ableiten

### Safeguards (MANDATORY)

- NEVER push if:
  - syntax check failed
  - required QA not executed
  - blocking errors exist

- Pre-existing or unrelated failing tests do NOT automatically count as blocking errors.
  - The agent MUST explicitly state why they are unrelated.
  - If the implemented change passed its relevant QA, the mandatory version-bump/commit/push flow still applies.

- ALWAYS ensure:
  - minimal QA passed
  - version bump applied

- NEVER force push

### Completion Behavior

After push:

- report:
  - new version number
  - commit summary
  - confirmation that HA update is available

- DO NOT ask for confirmation

### Override Rule

If user explicitly requests:

- branch workflow
- PR creation
- no push

→ follow user instruction instead of this policy

## Agent Command Convention

- If the user writes `go` (or `GO`), treat that as: stage relevant changes, create a git commit with an appropriate message, and push to the tracked remote branch.

- Showing current open GitHub issues (grouped by Bugs vs Enhancements) after an implementation package is OPTIONAL and informational only.

- It MUST NOT:
  - interrupt execution
  - trigger questions
  - pause or delay further processing

- During active multi-issue execution:
  - this step MUST be skipped entirely unless explicitly requested by the user

### GO Must Complete Planned Work

- When the user issues `go`/`GO`, you MUST ensure all open/pending planned work is implemented before committing/pushing.
- "Planned work" includes both:
  - the current request's ToDo list (in-chat)
  - any remaining open items recorded in `./.opencode/plan_state.md` (if the file exists)
- If implementing everything in one batch is not sensible (too risky/too large), you MUST:
  - explicitly state you are splitting into multiple smaller packages,
  - commit/push only the first package,
  - and immediately list the remaining planned items still pending.
- Diese verbleibenden geplanten Items muessen danach automatisch weiter umgesetzt werden, bis alle vom Benutzer angeforderten Issues abgearbeitet sind oder ein echter Blocker vorliegt.
- Dasselbe gilt ausdruecklich fuer ausgewaehlte/offene GitHub-Issues: sie muessen selbststaendig automatisch weiter bearbeitet und abgeschlossen werden, bis keine zur Umsetzung vorgesehenen Issues mehr offen sind.
- Auch bei Befehlen wie `arbeite alle Issues ausser #134 ab` muessen die verbleibenden offenen Issues automatisch ohne Rueckfrage bis zum Abschluss abgearbeitet werden.
- After a successful `go` workflow (commit + push), play a macOS completion sound:
  - `afplay /System/Library/Sounds/Glass.aiff`
  - If the workflow fails, play an error sound:
    - `afplay /System/Library/Sounds/Basso.aiff`
- After the completion sound, speak a short status message via macOS `say`:
  - If the workflow produced a new add-on version (i.e., `influxbro/config.yaml` version was bumped as part of the changes), use a female voice and speak the version as a version number (not a date), e.g. `say -v Anna "Generierung erfolgt, Version 1 Punkt 11 Punkt 34 wurde erzeugt"` (version derived from `influxbro/config.yaml`)
  - If the workflow ends with pending questions/blockers: `say "Einige Punkte müssten noch beantwortet werden"`

## Audio Notifications

- After completing any user-requested execution/workflow that runs commands, play a macOS completion sound:
  - success / ready for next input: `afplay /System/Library/Sounds/Glass.aiff`
  - failure / blocker: `afplay /System/Library/Sounds/Basso.aiff`
- If you need any blocking input or decision from the user, also speak a short German prompt via `say`:
  - default for decision needed: `say "Entscheidung erforderlich"`
  - optional confirmation-style prompt: `say "Bitte bestaetigen"`
- If the requested work is fully done and you are ready for the next instruction, speak:
  - `say "Fertig mit der Umsetzung"`
- Only speak the "Generierung erfolgt..." version message when a new add-on version was produced via version bump in `influxbro/config.yaml`.
