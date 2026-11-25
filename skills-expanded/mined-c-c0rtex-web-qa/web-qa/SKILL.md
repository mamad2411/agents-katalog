---
name: web-qa
description: Autonomous web app QA — Playwright E2E + visual regression + axe-core accessibility, with auto-generated test scenarios from git diff or text instructions. Project-portable (each project owns its `.web-qa/` state). Use when the user asks to test a website, verify a frontend feature, run regressions, or audit a11y.
---

# Web QA

Agent skill for testing web applications: E2E + visual regression + a11y + scenario auto-generation. Architecture — a 4-stage sequential pipeline, portable (one skill, many projects).

## Locating the tooling

Every `web-qa-*` command in this skill is a script under the plugin root: run it as
`${CLAUDE_PLUGIN_ROOT}/bin/web-qa-<name>` (e.g. `${CLAUDE_PLUGIN_ROOT}/bin/web-qa-matrix`).
When `${CLAUDE_PLUGIN_ROOT}` is unset (classic git-clone install into
`~/.claude/skills/web-qa`), the repository root — two directory levels above this file —
takes its place. Never call the bare name and hope it is on PATH.

First run: the bin wrappers are `uv run`-based — [uv](https://docs.astral.sh/uv/) creates
the venv and installs pinned Python deps automatically on first invocation, no manual
`uv sync` needed. The only extra install is Playwright's chromium, which is per-project
(see the specs-runner setup block below); `web-qa-doctor` verifies both and prints the
fix when something is missing.

## When to use

- "Run the regression on /cart", "check that checkout works" — execute existing/new scenarios
- "Generate tests from the diff" — autogen from git changes
- "What's broken in this branch?" — full Exploration + Generation + Run
- pre-push / pre-deploy gate — `web-qa-matrix` runs everything and returns an exit code

## User intent → workflow (recognize these)

| User says (any phrasing) | Do |
|---|---|
| "set up / onboard web-qa here" | Onboarding workflow below (register → creds → doctor → explore → specs runner) |
| "is it healthy / why is it broken" | `web-qa-doctor --alias <a>`, explain failures, apply hints |
| "test <feature>" / "check that <flow> works" | `generate --task` → show the md plan → run passive and/or spec-gen+run |
| "did my branch/diff break anything" | `generate --diff <ref>` → spec-gen → matrix → explain failures |
| "full regression / can I deploy" | `web-qa-matrix` → report gate verdict, coverage, flaky |
| "I changed permissions/roles — verify" | `generate --diff` (RBAC directive fires) → matrix `--roles <all>` — never test just one role |
| "test the mobile version" | `explore --viewport mobile` if no mobile map yet → generate → `run --viewport mobile` / matrix `--viewports` |
| "this test is failing, fix it" | `maintain` (propose); `--apply` only with explicit user consent |
| "the UI change is intentional" | `run --update-baseline` |
| "show me page X / verify visually" | screenshot → Read → describe (see Screenshots section) |

## Architecture

```
   git diff / instruction
            │
            ▼
┌─ Exploration ─┐  read-only crawl of the app → app.context.md
│   (once at onboarding, incrementally after)
└────┬──────────┘
     ▼
┌─ TestCase Gen ─┐  context + diff/task → md scenarios (human checkpoint optional)
└────┬───────────┘
     ▼
┌─ Automation ───┐  md → .spec.ts via `claude -p` CLI (≈4× cheaper than MCP-driving a browser)
└────┬───────────┘
     ▼
┌─ Run ──────────┐  npx playwright test → report
│   + axe-core injection → a11y violations
│   + pixel-diff vs baseline → visual regression
└────┬───────────┘
     ▼
┌─ Maintenance ──┐  failing spec + real error output → PROPOSES a fix (not auto-apply)
└────────────────┘
```

**Key principles:**
- Stages are **sequential**, hand-off through files (not shared memory) — allows pause/edit between phases and cheap context
- Exploration is the most expensive stage; cached in the repo as `<project>/.web-qa/app.context.md`
- Spec generation is grounded in the crawled app map — selectors come from real button labels/routes, not guesses
- Maintenance **proposes a diff**, never auto-fixes silently — distinguishing "the feature changed" from "a real regression" is a human/agent call

## Layout

```
<skill root>/                             # shared infrastructure
├── skills/web-qa/SKILL.md                # this file (plugin skill layout)
├── projects.example.json                 # registry shape; the real one is ~/.config/web-qa/projects.json
├── playwright.config.template.ts         # per-project config template
├── bin/                                  # thin wrappers over runners/ (uv run)
│   ├── web-qa-register-project           # onboard a project (+ .web-qa/ scaffold)
│   ├── web-qa-resolve-project            # cwd → project record
│   ├── web-qa-explore                    # crawl → app.context.md
│   ├── web-qa-generate                   # git diff / task text → scenarios/*.md
│   ├── web-qa-run                        # passive scenario runner (+a11y +visual)
│   ├── web-qa-spec-gen                   # md TC → .spec.ts via claude -p
│   ├── web-qa-run-specs                  # npx playwright test over specs/
│   ├── web-qa-matrix                     # deploy gate: full inventory + run
│   ├── web-qa-maintain                   # self-heal failing specs
│   └── web-qa-kill                       # kill orphaned playwright processes
└── runners/                              # python modules (run via bin/)

<project>/.web-qa/                        # per-project state (lives in the project repo)
├── config.json                           # ALL project specifics (see config.example.json)
├── seed.spec.ts                          # OPTIONAL: human-verified auth/setup code — spec-gen and maintain reuse its patterns verbatim (strongest auth grounding)
├── package.json                          # isolated npm root for @playwright/test
├── app.context.md                        # crawled app map (Exploration writes)
├── scenarios/                            # *.md test cases (generated or hand-written)
├── specs/                                # generated .spec.ts (`_`-prefixed = ad-hoc, excluded from gate)
├── baseline/                             # golden screenshots (commit to git)
├── history.json                          # last 20 matrix runs (flaky detection)
├── reports/                              # per-run artifacts (gitignore)
└── BUGS.md                               # confirmed findings
```

## Configuration

Shared runners, project specifics in two places:

- **`projects.json`** (machine-local, NEVER inside the skill or the project repo). Resolution: `WEBQA_REGISTRY` env → `~/.config/web-qa/projects.json`. Holds only what is secret or machine-specific: `alias`, `path`, **`auth: {email, password}`**, optional **`roles: [{name, email, password}]`** (named accounts for RBAC runs — `--role manager`, `web-qa-matrix --roles admin,manager`; TCs annotated `**Role:** <name>` run ONLY under that role's combos, unannotated TCs are role-agnostic). Everything else — including `target_url` and `backend_url` — lives in `<project>/.web-qa/config.json` and may be committed. No hardcoded fallbacks: without auth (or `--email/--password`) runners exit with a clear error.
- **Generated specs never contain the stand.** No host, port, email or password: they navigate relative to `baseURL` and read `WEBQA_BASE_URL`, `WEBQA_BACKEND_URL`, `WEBQA_EMAIL`/`WEBQA_PASSWORD` and `WEBQA_ROLE_<NAME>_EMAIL`/`_PASSWORD`, which matrix / run-specs / maintain export from the registry (a caller's own value wins). spec-gen rejects an output that hardcodes any of them and retries once; `web-qa-doctor` flags old specs that still carry a registry password.
- **`<project>/.web-qa/config.json`** (in the project repo): merged over the registry entry (`null` values ignored). Keys:
  - `target_url` / `backend_url` — frontend and API base URLs
  - `stack` — string for the spec-gen prompt (e.g. `"Next.js + FastAPI admin"`, default `"web"`)
  - `backend_prefixes` — paths treated as backend-only (never opened as frontend routes). Default: `/auth`, `/api`, `/health`
  - `route_hints` — `[{path, keywords}]` to infer the route from TC text when no explicit path. Default: empty
  - `locale` — the ONE browser locale for every context: the crawl, the passive runner, the live probe and the specs (via `WEBQA_LOCALE` in the template). Default `en-US`. Set it to the language your users see: an app that picks its UI language from Accept-Language otherwise gets crawled in one language and tested in another. `web-qa-doctor` warns when the map was crawled with a different locale
  - `id_discovery` — `[{endpoint, key, route?}]`: which GET endpoint to sample a live id from. A placeholder gets the id its route names: `{key}`/`{key_id}` by token, a generic `{id}` by the segment in front of it (`/shipments/{id}` → `shipment`), or by an explicit `route` where the URL word is not the API's (`{"endpoint": "/directory/contacts", "key": "contact", "route": "/people/{id}"}`). No match → the probe is skipped, never filled with another entity's id. `web-qa-explore` uses it too, to open templated routes no page links to. Default: empty
  - `auth_flow_notes` — lines for the Auth Flow section of `app.context.md` (otherwise derived from OpenAPI)
  - `auth_login_hint` — exact auth flow description for the spec-gen prompt (JWT vs cookie, browser vs Node-side API). Critical: without it the model guesses the contract. Default: generic hint
  - `auth_login_path` / `auth_login_body` / `auth_token_field` / `auth_me_path` / `auth_browser_storage` — declarative auth adapter for the RUNNERS (explore/run/doctor login): endpoint path (default `/auth/login`), JSON body template with `{email}`/`{password}` (default flat), dot-path to a bearer token in the response (e.g. `"user.token"`), the identity endpoint used to learn WHO logged in (default `/auth/me` — a JWT login response carries no identity, and without it reports say `Logged-in: None` and `doctor`'s per-role check proves only that the password was right), and where the SPA keeps the token in the browser (`{"kind": "localStorage", "key": "...", "value": "{token}"}` → injected into Playwright storageState). Cookie-session apps need none of these. Example (RealWorld): path `/api/users/login`, body `{"user": {"email": "{email}", "password": "{password}"}}`
  - `context_notes` — lines for the Out of Scope / Notes section of `app.context.md`
  - `visual_masks` — CSS selectors of dynamic elements (clocks, counters, avatars) hidden before screenshots to avoid false visual diffs. Default: empty
  - `visual_exclude` — route globs fully excluded from visual diffing (data-driven pages: entity lists, dashboards — their baseline rots with every data change). Screenshot still saved as an artifact. Default: empty. Rule of thumb: point dynamics → mask, whole-page data → exclude; the fundamental fix is seeded fixture data
  - `test_data_prefix` — name prefix for test entities that mutating specs create/delete themselves (policy: never touch real data). Default: `"QA-"`
  - `gate_exclude` — spec globs excluded from the deploy matrix (features hidden on prod behind flags/build-args), e.g. `["analytics*"]`. Default: empty
  - `language` — language for generated scenario steps (default `"English"`)
  - `frontend_dir` — path (relative to the project root) of the frontend app inside a monorepo; route mining scans there. Default: project root
  - `workers` — Playwright workers for matrix/maintain runs. Set `1` for small dev stands: parallel chromiums against one dev server turn timing into flaky noise. CLI `--workers` overrides. Default: template default
  - `live_probe` — `false` disables the live locator check during spec-gen/maintain (e.g. generating without a running stand). Default: enabled. The probe opens each generated spec's entry page (authenticated) and counts matches for every static locator; misses and strict-mode ambiguities (>1 match) earn one regeneration retry with real-DOM feedback, then surface as `probe_warnings` — never a hard failure, since mid-flow elements legitimately don't exist on the entry page. RBAC-aware: the probe logs in under the TC's declared role (spec-gen passes it; maintain infers it from the spec's email literals) — probing an admin-only element under a reader session would yield a false zero
  - `fixture_cmd` / `fixture_teardown_cmd` — shell commands (run from the project root) that seed/clean deterministic test data. Run before/after `web-qa-run` and once per `web-qa-matrix` (combos must see the same world — the matrix passes `--no-fixtures` to its inner passive runners). Non-zero exit = hard stop: verdicts from a half-seeded stand can't be trusted. Deterministic data is what makes visual regression viable on data-driven pages (instead of `visual_exclude`). Default: none
  - `network_fail_on` — response classes that FAIL a passive TC when fired during its navigation (attributed per-TC). Default `["5xx"]`; add `"4xx"` to tighten. Failures land in notes as `NETWORK: <status> <method> <url>`
  - `console_fail_on` — console message types that FAIL a passive TC when emitted during its navigation, e.g. `["error"]`. **Opt-in** (default off — real apps are noisy). `console_ignore` — regexes dropping known third-party noise (e.g. `["favicon", "ResizeObserver"]`). Failures land in notes as `CONSOLE: [type] <text>`
  - `quarantine_after` — integer N (default off): a spec/TC that flips pass/fail across the last N `web-qa-matrix` runs is quarantined (🚧) — still run and reported, but kept out of the gate's exit code (and emitted as `skipped` in JUnit) until it stabilizes. One chronically-racy test stops blocking every deploy without going dark
  - `viewport` — `{"width": W, "height": H}`, applied consistently to the crawler, the passive runner AND the specs config (via `WEBQA_VIEWPORT`, set automatically by matrix/maintain). Default: 1280×900 everywhere. Changing it invalidates visual baselines (size-mismatch) — re-run `--update-baseline` after
  - `viewports` — named list for responsive testing: `[{"name": "desktop", "width": 1280, "height": 900}, {"name": "mobile", "device": "iPhone 14"}]`. `device` entries use full Playwright descriptors (touch, mobile UA, DPR) — real emulation, not a narrow window. First entry = project default (keeps unsuffixed baselines); others get their own baseline set (`<route>@<name>.png`). Used by `--viewport` (explore/run) and `--viewports` (matrix)

**Progress**: every runner prints one line per unit of work to **stderr** — `[gen] 14/72 · 4m12s · $3.84/$25.00 · OK admin::TC-ADM7` — so a long run says where it is and what it has cost. stdout stays reserved for the summary JSON. Pipe with `2>&1 | tee run.log`, never `| tail`.

Env: `WEBQA_WORKERS=N` — Playwright workers in the template config. `WEBQA_GEN_TIMEOUT=N` — seconds per spec generation (default 300). For the LLM knobs (`WEBQA_CLAUDE_MODEL`, `WEBQA_CLAUDE_EFFORT`, `WEBQA_CLAUDE_TOOLS`, `WEBQA_MAX_USD`) see **Token budget** below.

## Token budget — read this before running spec-gen

**Only three commands spend tokens**: `web-qa-generate`, `web-qa-spec-gen` and `web-qa-maintain`. Everything else (explore, run, run-specs, matrix, doctor) is zero-token. All three funnel through one function, `call_claude` in `runners/spec_gen.py`.

Each of those calls is a **headless `claude -p` session, not a single API request**. A session carries a system prompt, tool schemas, and — if tools are enabled — an agentic loop that will crawl the repo. Fanned out over a 30-TC scenario set with retries, that is easily hundreds of full sessions. This has drained a 5-hour subscription window in under seven minutes; the defaults below exist so it cannot happen again.

**Defaults (all overridable, none silently costs more than stated):**

| Knob | Default | Why |
|---|---|---|
| `WEBQA_CLAUDE_TOOLS` | `""` (no tools) | `app.context.md` is already inlined in the prompt. An agent re-reading the repo buys nothing and costs the most. |
| `WEBQA_CLAUDE_MODEL` | `sonnet` — but `opus` for `generate` | Two different jobs. Deciding **what** to test is judgment and runs once per invocation, so `generate` pays for `opus`/`high`. Turning a decided test case into code is **translation**, and `spec-gen` fans it out over every TC, so it stays on `sonnet`. Neither ever inherits the user's interactive CLI model. |
| `WEBQA_CLAUDE_EFFORT` | `medium` — `high` for `generate` | Frontier models default to `high` everywhere; only the judgment step needs it. |
| `WEBQA_MAX_USD` | `5.00` | Hard ceiling per process, metered from the CLI's own `total_cost_usd`. On breach, the next call raises `LLMBudgetExceeded` **before** anything reaches the model. `0` disables the guard. Precedence: `--max-usd` (this run) → `WEBQA_MAX_USD` → `max_usd` in `.web-qa/config.json` (declare a project's ceiling once) → `5.00`. |
| `--workers` (spec-gen / maintain) | `1` | Concurrent calls all miss the shared prompt cache — none can read what the others are still writing. Every extra worker buys wall-clock with money. |

**Rules for the agent:**

- Every run reports its real spend: the summary JSON carries `"llm": {"spent_usd", "calls", "budget_usd"}`, and each call prints `[llm] $… this call, $… of $… budget` to stderr. **Quote the actual number when you report a run** — never estimate it.
- `web-qa-generate` answers only the task it was given. It cannot know what earlier runs covered, so **always read `uncovered_routes` from its summary and tell the user** — that is how a whole route (a dashboard) stays untested for months. Close gaps with `--cover-gaps`.
- `skipped_missing_role` in a spec-gen summary is a **registry gap, not a failure**: the TC declares a role `projects.json` has no account for. It cost nothing. Report it and ask the user to add `roles: [{name, email, password}]`.
- `skipped_over_budget` means those TCs **never reached the model** — no `.FAILED` marker is written for them. Resume with a higher `--max-usd` only after the user approves.
- Before a large fan-out (>10 TCs), tell the user roughly what it will cost and let them set `--max-usd`. Generate in batches with `--tc <id>` when unsure.
- `LLMBudgetExceeded` is not a bug and not a transient failure. **Never retry it, never raise the ceiling on your own** — report the spend and ask.
- Do not raise `--workers` or switch `WEBQA_CLAUDE_MODEL` to a frontier model without the user asking. If specs come out poor on `sonnet`, say so and propose the upgrade; don't do it silently. Note `WEBQA_CLAUDE_MODEL` is a **global** override — setting it also drags `generate` off `opus`.
- Enabling `WEBQA_CLAUDE_TOOLS` re-arms the agentic loop. There is currently no task in this skill that needs it.

**Long runs (matrix / spec-gen / playwright) — don't wait blindly**: agent harnesses may background the command and lose the notification. Everything is durable: `matrix.json` is rewritten after every stage (`stage` field), live spec progress goes to `reports/<run>/matrix/playwright.log`, generation failures leave `specs/*.FAILED` markers. Poll those, not stdout.

## Commands

| CLI | What it does |
|---|---|
| `web-qa-register-project <alias> --target-url <url> [--backend-url <url>]` | Register a project, scaffold `.web-qa/` |
| `web-qa-doctor [--alias <a>] [--json]` | **Preflight**: deps, chromium build, LLM CLI, registry; with `--alias` also project path/config, frontend/backend reachability, login (incl. every role), app map, scenarios, specs-runner setup. Exit 0 = healthy, 1 = hard failure. Run it FIRST when anything misbehaves |
| `web-qa-resolve-project [path] [--alias <a>] [--json]` | cwd/alias → project record |
| `web-qa-explore --alias <a> [--max-pages N] [--viewport <name>] [--interactive] [--no-mine]` | Crawl → app.context.md (non-default viewport → `app.context.<name>.md`, both feed spec-gen). Dedup: query params and numeric ids collapse, max 2 entity cards per route template. Everything below the `<!-- manual -->` marker in app.context.md survives re-crawls — hand-written notes go there. **Route mining (default on)**: routes declared in the app's source (Next/Nuxt/SvelteKit file routers, `path:`/`<Route path>` configs) seed the crawl and land in the Routes table with an Origin column — a BFS over `<a href>` alone misses client-side navigation. Deterministic, zero tokens. **`--interactive` (opt-in)**: clicks non-link clickables, harvests pushState URL changes, and **snapshots any modal that opens** (rendered inside its route's ARIA block, so spec-gen's per-route slice carries it). Dialogs are the one part of a UI the crawler never sees — they are not routes and nothing links to them — and without them the generator writes `getByRole('dialog').getByLabel(…)` against fields that have no labels. Costs ~13s/page vs ~3s. Non-deterministic pass, hence the flag. Mutation safety is enforced at the network level (every non-GET request is aborted during the pass), with two known limits: WebSocket frames on already-open connections bypass the valve, and a GET with server-side side effects is let through |
| `web-qa-generate --alias <a> (--diff <ref> \| --task "..." \| --cover-gaps) [--out f.md] [--prefix X] [--force]` | Scenario md from git diff or task text via `claude -p` (one call, on `opus`), strict TC format, validated for `## TC-…` headers. RBAC-aware: a diff touching permissions/roles fans out into allowed+denied TC pairs per role (`**Role:**` annotations). **Coverage-aware, on two axes**, both deterministic and zero-token: routes no TC's `**Steps:**` navigate to (`uncovered_routes`, `COVERAGE GAP`), and — from the map's ARIA snapshots — the buttons/tabs/comboboxes no TC anywhere names (`uncovered_controls`, `CONTROL GAP`). The second matters because a route with one test case that only reads a table looks covered. Layout chrome (a name on >50% of routes) and data-derived names are filtered out. `--cover-gaps` targets both |
| `web-qa-run --alias <a> [--scenarios "<glob>"] [--role <r>] [--viewport <name>] [--update-baseline [--routes <glob>]] [--visual-threshold N] [--no-fixtures]` | Passive scenario run: goto + visible-text vs Expected (30% threshold) + axe + visual + network assertions (`network_fail_on`). Mutating TCs marked MANUAL. Visual regressions save a baseline/current/**diff-mask** triple and land in the report's "Visual review queue" — Read all three images, judge, then accept an intentional change selectively with `--update-baseline --routes '<route>'` |
| `web-qa-spec-gen --alias <a> [--all] [--tc <id>] [--force] [--workers N] [--max-usd N] [--prune]` | Generate `.spec.ts` from TCs via `claude -p` (serial by default — see **Token budget**; spend is metered and capped). App map embedded in the prompt; every spec validated with `playwright test --list`, 1 retry with the error fed back. Cache covers TC + prompt + app-map fingerprint, and is persisted after EVERY spec (an interrupted run keeps what it paid for). **Orphans**: a spec's file name carries its TC's title, so rewording a title makes a new file and leaves the old one — reported as `orphan_specs` / `ORPHAN SPEC`, deleted only with `--prune`. `matrix` labels them `kind: orphan`, does not run them and keeps them out of the deploy gate. **Drag-and-drop**: the app's DnD library is detected from package.json (dnd-kit / react-beautiful-dnd / SortableJS / interact.js / native) and the exact `dragTo` helper for it is injected — DnD TCs get the reliable multi-step pointer sequence, not a flaky one-shot `dragAndDrop` |
| `web-qa-run-specs --alias <a> [-- <playwright args>]` | `npx playwright test` over generated specs |
| `web-qa-matrix --alias <a> [--list] [--roles a,b] [--viewports d,m] [--workers N] [--junit <path>] [--include-adhoc] [--skip-passive\|--skip-specs] [--no-fixtures] [--no-mutations] [--keep-artifacts N]` | **Deploy gate**: inventory of ALL project tests (scenario TCs + specs) + full run + consolidated matrix with route coverage (global AND per-role) and flaky markers. `--viewports` runs the passive stage per viewport (× roles); a device-viewport also runs specs under mobile emulation (second playwright project) (history in `.web-qa/history.json`). Exit 0 = safe to deploy, 1 = fail/error present. `--list` = inventory + coverage only. `--junit` exports the matrix as JUnit XML; inside GitHub Actions the matrix auto-appends to `$GITHUB_STEP_SUMMARY`. Fixtures seed once per matrix run. **Mutation gate**: each spec is labelled `spec` or `spec (mutating)` (from its TC's `**Type:**`, else by scanning for non-auth write verbs); `--no-mutations` reports mutating specs as `manual` instead of running them — without it a matrix run WRITES to the app's data even when the passive stage skipped every mutating TC. **Artifacts**: playwright writes screenshots, traces and `error-context.md` straight into `reports/<run-id>/test-results/` (it deletes its output dir on start, so a shared one meant each run erased the last); older runs' artifact folders are pruned to `--keep-artifacts` (default 3, config `keep_artifacts`, `-1` = keep all) — the reports themselves are never pruned. `matrix.json` records `invocation` (argv, flags, `WEBQA_*` env) so a report can be reproduced and argued about |
| `web-qa-maintain --alias <a> [--report <json>] [--apply] [--workers N] [--max-usd N] [--with-screens] [--reruns N] [--artifacts-dir <d>]` | Self-heal with three-way classification: test fragility → corrected spec (`*.spec.ts.proposed`; `--apply` overwrites with `.bak` + rollback); transient env failure → spec untouched, rerun advised; genuine app bug → assertions kept, `test.fixme` + entry appended to `BUGS.md`. Healers patch test fragility, never real bugs. **Deterministic-first**: a failure carrying a network/infra/rate-limit signature (`net::ERR_*`, `ECONNRESET`, 429, 50x, `Target closed`) is classified transient WITHOUT the LLM; `--reruns N` re-runs a signature-clean spec and treats a pass as a flake — only consistently-failing specs reach the healer. The healing prompt includes playwright's `error-context.md` — the page's ARIA snapshot at the moment of failure. The artifact folder is derived from `--report` (a matrix report heals against ITS OWN run's snapshots, not whatever ran last); `--artifacts-dir` overrides. `--with-screens` lists failure screenshot paths in the summary JSON — Read them, visual judgment is the orchestrator's job |
| `web-qa-kill [--dry-run]` | Kill orphaned playwright runners + headless browsers (matches only `ms-playwright` binaries and `@playwright/test` CLIs — never a regular browser) |

**Per-project specs runner setup (once):**
```bash
cd <project>/.web-qa
# NOT `npm init -y`: the ".web-qa" dir name is an invalid npm package name.
# NOT a bare `npm install` without package.json: npm walks UP and pollutes the app's own deps.
[ -f package.json ] || printf '{"name":"web-qa-specs","private":true}\n' > package.json
npm install -D @playwright/test
npx playwright install chromium
grep -q node_modules .gitignore 2>/dev/null || echo 'node_modules/' >> .gitignore
cp "${CLAUDE_PLUGIN_ROOT}/playwright.config.template.ts" playwright.config.ts   # baseURL comes from WEBQA_BASE_URL at run time
```
Pin `@playwright/test` to an exact version: every version pins an exact browser build, and an unplanned upgrade means an unplanned browser download.

## Workflows (for the agent)

### Onboarding a project (once)
1. `web-qa-register-project <alias> --target-url ... --backend-url ...`; put credentials into `~/.config/web-qa/projects.json → auth`
2. Make sure the dev server responds
3. `web-qa-explore --alias <alias>` → review `app.context.md`, fill `auth_login_hint` and other config keys
4. Specs runner setup (block above)

### "Test X"
1. Resolve project (`web-qa-resolve-project`), read `app.context.md`
2. `web-qa-generate --task "X"` → review/edit scenarios
3. `web-qa-run` (passive) and/or `web-qa-spec-gen` + `web-qa-run-specs` (mutating)
4. Failures → `web-qa-maintain` → real bugs go to `BUGS.md`, spec bugs get healed

### Pre-deploy gate
1. Dev servers up → `web-qa-matrix --alias <a>` → exit 0 = deploy, 1 = investigate
2. In a deploy script: `"${CLAUDE_PLUGIN_ROOT}/bin/web-qa-matrix" --alias <a> && ./deploy.sh`
3. Convention: `_`-prefixed specs are ad-hoc debug — excluded from the gate; prod-hidden features via `gate_exclude`

## Screenshots and visual judgment (for the agent)

The pipeline itself never sends screenshots to a model — visual regression is an algorithmic
pixel diff. **Visual judgment is YOUR job as the orchestrating agent:**

- Every passive run saves a per-page screenshot into `reports/<run>/` (named `<TC>-<route>.png`);
  Playwright specs keep failure screenshots, traces and `error-context.md` (the page's ARIA
  snapshot at the moment of failure) under `reports/<run-id>/test-results/`. An ad-hoc
  `web-qa-run-specs` still uses the legacy `.web-qa/test-results/`.
- **A pure-white failure screenshot means the spec never navigated** — it failed on an API
  assertion before its first `page.goto`. Read `error-context.md` instead, and regenerate.
- **Read those images** before reporting a finding: a screenshot confirms or refutes a suspected
  bug far better than matched keywords. Screenshot → Read → judge → only then report.
- When the user asks "show me how page X looks" or "verify this visually" — take an ad-hoc
  screenshot: for public pages `uv run playwright screenshot <url> shot.png`; for authenticated
  pages run the relevant scenario (`web-qa-run --scenarios <file>`) and Read its artifacts.
- Visual regression failures come with both the current screenshot and the baseline in
  `baseline/` — Read both and say what actually changed, not just the diff percentage.

## Business rules

- **Never auto-fix found product bugs.** Report only; the user decides.
- **Exploration is never run on a schedule** — it's a full crawl; only explicit `web-qa-explore`.
- **Visual baseline lives in the project repo** (commit it) so regressions work in CI.
- **Reports are gitignored** — every run writes a fresh one.
- **a11y severity:** WCAG critical/serious = bug, the rest = note.
- **Golden path first.** Scenarios start with the happy path, then edge cases.
- **Mutating tests create their own data** (`test_data_prefix`), act on it, delete it in `try/finally`. Never mutate pre-existing data.
- **`✋ manual` means nothing executed it.** A mutating test case is executed by its spec; the passive runner cannot mutate, so its scenario row is folded away and the spec's row carries the verdict. `manual` survives only for a mutating TC with no spec, or a run that skipped the specs stage.
- **A weak oracle must not veto a strong one.** The passive runner's keyword score (how many words of the Expected prose appear on the page) drops as test cases get better — a drill-down assertion has few words a page can show. When a spec asserts the same TC, that score is a note, not a verdict. a11y, visual, console and network checks still fail the row.
- **A matrix run without `--no-mutations` writes to the app.** The passive runner cannot execute mutations (it only navigates), so it reports mutating TCs as `manual` — that is a capability limit, not a safety guarantee. The specs stage does execute them. Never tell the user a run was "read-only" unless `--no-mutations` was passed; check `matrix.json → invocation.flags` before claiming it.
- **An oracle that re-implements a metric is a second unverified implementation.** When a spec computes a KPI from raw collections and the number disagrees with the UI, the spec is the more likely suspect: it may count the wrong entity, sum the wrong currency, or compare a wire enum against a display label. Prefer drill-down (assert the summary against the detail view the app itself renders) or a mutation delta. Before recording a data mismatch as a product bug, check the metric's definition in the source, and check whether a "leaked" control is merely `[disabled]`.
- **TC classification: structural evidence beats the declaration, the declaration beats absence.** `**Type:** passive|mutating` is required on every TC; runners never guess intent from prose keywords, so TCs work identically in any language. A declared `passive` is overridden to mutating when **Steps:** contain a mutating HTTP op (`POST /x` in Expected is context, not an action — never evidence). A TC without `**Type:**` is treated as mutating: it gets a real spec instead of a green passive check for steps that never executed. `web-qa-generate` warns about contradictions (`type_conflicts`) right after generation.

## Troubleshooting

| Symptom | Diagnosis / fix |
|---|---|
| Anything misbehaves | `web-qa-doctor --alias <a>` first — it catches every issue below |
| `alias not found` | Register via `web-qa-register-project`, check `projects.json` |
| `no credentials for '<alias>'` | Fill `auth` (and optionally `roles`) in `projects.json` |
| `web-qa-spec-gen` → «claude CLI not found» | Claude Code CLI must be on PATH (`which claude`) |
| Specs mass-fail on selectors | App map is stale → `web-qa-explore`, then `web-qa-spec-gen --force`, then `web-qa-maintain` |
| Spec generation silently missing a TC | Check `specs/*.FAILED` markers; raise `WEBQA_GEN_TIMEOUT` for complex TCs |
| `LLMBudgetExceeded` | The run hit `WEBQA_MAX_USD` (default $5). Report `summary.llm.spent_usd` and ask the user before raising it — see **Token budget**. Not a retryable failure. The blocked TCs land in `skipped_over_budget`, never in `errors`, and get no `.FAILED` marker |
| Specs assert only that elements exist | A spec that checks `toBeVisible()` on a KPI passes on a KPI showing a wrong number. Every TC over derived data must assert the VALUE — by drill-down, by a mutation delta, or (last resort, definition cited) by recomputation from **primary** collections, never from the aggregate endpoint the page itself calls. Both prompts enforce this; if a spec still does presence-only, the TC's Expected bullets were presence-only — fix the scenario, not the spec |
| `TypeError: x.filter is not a function`, `Expected 200 Received 201/405/422` | The spec guessed the API contract because the map lacked it. Re-run `web-qa-explore` — the OpenAPI section now carries each operation's success status code, response shape and wire enum values — then `web-qa-spec-gen --force` |
| Bare `Test timeout of Nms exceeded.` with no locator | Either the project's `playwright.config.ts` has no `actionTimeout` (a locator miss then hangs silently), or a generated `waitFor({timeout: …})` is longer than the whole-test `timeout`. `web-qa-doctor --alias <a>` reports both as config drift |
| `locator.fill` times out on a dialog field | Read the ARIA snapshot in `test-results/<spec>/error-context.md`. A field shown as a bare `- textbox` under a separate `- text: Title` node has no accessible name: `getByLabel` cannot ever match it. That is an app a11y defect (axe reports it as `label` critical) — locate structurally and report the defect |
| `strict mode violation: resolved to N elements` | The name is not unique on that page. Scope the locator (`getByRole('navigation').getByRole('link', …)`) — the app is not wrong |
| Failure screenshot is pure white | The spec asserted against the API before its first `page.goto`, so playwright screenshotted `about:blank`. Regenerate: the prompt now requires opening the page before computing the oracle |
| Report says `Logged-in: None (None)` | The app's login response carries no identity. Set `auth_me_path` in `.web-qa/config.json` (default `/auth/me`) so runners and `doctor` can verify WHICH account — and which role — actually ran |
| `.FAILED` markers all say «claude CLI failed (exit 1)» | The CLI itself refused — usually the subscription usage limit. The message now carries the CLI's own stdout; read it |
| `npm install` from `.web-qa` polluted the app's package.json | `.web-qa` had no own package.json — create it (see setup), reinstall inside, remove the stray dep from the app |
| Visual diffs after a legitimate UI change | `web-qa-run --update-baseline` |
| False visual diffs on dynamic content | `visual_masks` (point dynamics) or `visual_exclude` (data-driven pages) in config.json |
| Hung/killed run left browser processes | `web-qa-kill` (use `--dry-run` first to see what it found) |
| Playwright download stalls (CDN unreachable) | Pin `@playwright/test` to a version whose browser build is already in `~/.cache/ms-playwright/` |
