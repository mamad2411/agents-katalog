---
name: power-coding
description: >
  Mindful-coding OS for any LLM coding agent — faster, quality, scalable output. One
  invoke configures seven layers (0–6): (0) BRIEF — optional one-page PRD.md (skipped
  if design.MD/README already covers it, or on request), plus git init, gitignore, and
  a day-one security baseline;
  (1) HARNESSING — Handoff.MD (user-picked sections, one
  magic phrase chains sessions, updated on concrete events — before every commit / end of
  every phase — with a line/item compaction cap and a last-synced sha for concurrent-session
  reconcile) + auto Learning.MD for bugs and flow changes; (2) LOOP ENGINEERING — Loop.MD with evals drafted from the
  project's brief, and a status machine that offers to "turn on the loop" once the
  first draft works; (3) VIBE DEBUGGING — Mermaid flow diagrams to a strict convention,
  optionally a temp local-only in-app debug tab;
  (4) FMEA — product-aware failure-mode scans (Severity×Occurrence×Detection→RPN,
  P0/P1/P2) cross-referencing diffs against the PRD and architecture, on
  feature-complete, pre-commit, smart-suggest, or manual triggers; (5) SENTINEL SCAN —
  silent four-lens sweep after major completions (misuse traps, stop signals, silent
  failures, waste) with inline one-line flags only; (6) SESSION PULSE — 2-line effort
  split (feature/support/rework) after major milestones with one specific takeaway. Use
  on "power coding", "mindful coding", "work across sessions", "run fmea", "scan for
  failures", "run sentinel", "session pulse", "add debug diagrams", or any repo with
  Handoff.MD/.power-coding when sessions start, features complete, commits happen, or
  context runs low.
---

# Power Coding

Seven layers (0–6) that make an AI-assisted project fast, debuggable, and resumable — for any
coding agent (Claude Code, Codex, Gemini CLI…), because everything lives in plain
markdown files the agent re-reads every session. Together they implement **the Five
Forces of Mindful Coding**: *Alignment* counters ambiguity (brief, architecture
sign-off, decisions, scope brake), *Memory* counters amnesia (Handoff, Learning,
checkpoints), *the Loop* counters drift (evals → tests), *Sight* counters opacity
(diagrams, Pulse), *Foresight* counters entropy (FMEA, Sentinel, security baseline).

**How anything here happens "automatically":** agents only reliably re-read two things —
the platform's instructions file and files those instructions point to. So setup writes
one pointer block into the instructions file (`CLAUDE.md`, `AGENTS.md`, or `GEMINI.md`;
create `AGENTS.md` if none exists), and every automatic behavior below is an instruction
stored in `Handoff.MD` / `Learning.MD` / `Loop.MD` that the pointer forces back into
context. No daemon, no hook required — redundancy of written instructions is the
mechanism.

Asking questions: use the platform's structured-question tool if one exists, otherwise
ask in plain text. If the run is non-interactive, choose sensible defaults and mark them
`⚠️ unconfirmed` for the user to review.

---

## FIRST INVOKE — configure the project (this exact order)

Detect state first: if `Handoff.MD` exists at the repo root, the project is already
configured — skip to **Ongoing duties** (and offer to re-run any single layer if the
user asked for that).

### Layer 0 — Brief (OPTIONAL — the product context everything else reads)

Loop.MD evals are drafted from the brief and FMEA scans cross-reference it. Detect
first: if the repo already has a real brief (`PRD.md`, `docs/prd*`, `design.MD`, or a
README that genuinely describes the product — not just install steps), confirm it with
the user and use it as-is: **no interview, no PRD.md created**. Only if nothing
qualifies, OFFER the brief — never force it:

> "I couldn't find a product brief (no design.MD or README with product detail). A
> one-page PRD.md makes the evals and failure scans product-aware instead of generic —
> want to answer 4 quick questions to create one?
> (a) What are you building, in one or two sentences?
> (b) Who uses it, and for what?
> (c) What must NEVER break — where would a failure cost money, data, or trust?
> (d) What does 'done' for v1 look like — the smallest version that proves it works?
> Or **skip** — you can add it anytime with `power-coding brief`."

Answered → write `PRD.md` from `assets/PRD.template.md` (plain language, one page max);
it becomes `context_sources.prd_path` in 4b. Skipped → leave `prd_path` null, draft
Loop.MD evals from the user's stated goal instead, and prefix every FMEA scan output
with one line: "⚠️ running without product context — findings are code-level only".
Non-interactive run → draft PRD.md from the code and README, mark every section
`⚠️ unconfirmed`.

**Also at Layer 0: make the repo safe to iterate in.** If there is no git repo, `git
init` and make an initial commit (tell the user why: checkpoints are the rollback path
when a change breaks the app). If there is no `.gitignore`, create one covering `.env*`,
build output, and dependency folders BEFORE the first commit — a secret committed once
is compromised forever, even if deleted later.

### Layer 1 — Harnessing (session continuity)

**1a. Create `Handoff.MD`** from `assets/HANDOFF.template.md`, then ask (multi-choice,
multi-select):

> "I've built **Handoff.MD** so you can work across multiple sessions seamlessly.
> What would you like in it?
> (a) Compact summary of the previous session's work
> (b) Current state
> (c) Pending points
> (d) Anything else — tell me"

Build exactly the sections chosen (for an existing repo, pre-fill them from a scan of
the code, git log, and any docs; for a new project, fill from the user's description of
what they're building). Then tell the user, verbatim enough to be copy-pastable:

> "From now on, to continue in a fresh session just type:
> **Refer to Handoff.MD in `<absolute project path>` and begin**
> The new session will open with your pending points (if any) or ask what you'd like
> to do next."

**1b. Standing session rules** (these also get written into Handoff.MD's header so any
agent that reads the file inherits them):

- Update Handoff.MD on **concrete events the model can actually detect** — not "after
  every major change" judged by feel: **before every git checkpoint commit** (1b's commit
  discipline makes this deterministic) and **at the end of every phase/milestone**.
  Rewrite as a current-state snapshot, don't append a journal; re-stamp `last-synced` with
  the new HEAD sha.
- **Low context is a *secondary* trigger, not the primary one.** The model can't reliably
  measure "10% remaining", so don't rely on it — but if the platform *does* signal context
  is low (compaction warning, near limit): update Handoff.MD immediately and tell the user:
  > "Context is nearly full — Handoff.MD is up to date. Please start a fresh session
  > with: *Refer to Handoff.MD in `<path>` and begin*."
- **Compaction cap (concrete heuristic, mechanical not aspirational):** when Handoff.MD
  exceeds **~40 lines** OR the Current state has **~15+ ✅ items**, collapse all ✅ into ONE
  line — `✅ Shipped: <short range> (see git log & Learning.MD)` — and push any detail to
  Learning.MD. `node <skill-path>/scripts/sentinel.mjs pulse` flags this as `⚠ compact`.
- **Concurrent-session reconcile:** Handoff carries `last-synced: <sha>`. A session that
  **starts** (magic phrase, or any repo containing Handoff.MD) must read it fully, then
  FIRST run `git log --oneline <last-synced>..HEAD` — anything there changed underneath the
  file (another session, a linter, a teammate); reconcile it before trusting the state.
  Then open with the pending points ("Last time these were pending: … — continue, or
  something else?") or, if none, "What would you like to do now?"
- **Git checkpoints:** commit whenever the app reaches a working state, and always
  *before* a risky change (refactor, dependency upgrade, schema/data migration). Never
  leave a working state uncommitted — the checkpoint is the rollback path when the next
  change breaks the app, and rollback beats a debugging spiral. Because commits mutate
  repo state, ask ONCE at setup: "**auto** — I commit checkpoints myself and announce
  each in one line — or **propose** — I ask before each one?" (recommend auto; a
  proposed-but-ignored checkpoint protects nobody). Store as
  `consent.git_checkpoints: "auto" | "propose"` in `.power-coding/config.json`.
- **Scope brake:** before starting any feature, state the smallest version that proves
  it works (measured against PRD.md's "Done for v1") and build that first — checkpoint,
  then extend. Extensions the user didn't ask for are waste, not initiative.
- **Decision log:** any decision that shapes stack, architecture, or product behavior
  gets one line in Handoff.MD's `Decisions` section (date — what — why). Never silently
  reverse a logged decision — surface the conflict and ask; if the section outgrows the
  one-screen rule, move older entries to `docs/DECISIONS.md` and keep a pointer.

**1c. Create `Learning.MD`** from `assets/LEARNING.template.md` — auto-enabled. It is
read AND updated whenever: the basic flow of the app changes, the user reports a bug or
gives corrective feedback, or something took real time to figure out. Each entry follows
the template's 5-whys format: the symptom, a Why-chain drilled until the deepest why
(typed `code` / `design` / `process` / `knowledge-gap`), the action taken (and which
"why" level it targeted), and a preventive action for the whole class of bug. Tell the
user:

> "I've also enabled **Learning.MD** — I'll log flow changes, bugs you report, and
> their root causes there, so future sessions don't repeat them. Say the word if you'd
> rather not have it."

**1d. Write the pointer block** into the instructions file (this is what makes 1b, 1c,
and Layer 2's automation survive every future session):

```markdown
## Power Coding (auto — do not remove without asking the user)
At session start read Handoff.MD; FIRST run `git log --oneline <its last-synced sha>..HEAD`
and reconcile anything changed underneath it; then open with its pending points. Update
Handoff.MD before every git checkpoint commit and at the end of every phase (low context is
a secondary trigger) — snapshot not journal, re-stamp `last-synced` with HEAD; then, if
context was the trigger, tell the user to start fresh ("Refer to Handoff.MD in <path> and
begin"). When Handoff exceeds ~40 lines or ~15 ✅ items, collapse ✅ into one "Shipped:" line,
detail to Learning.MD.
Log flow changes / user-reported bugs in Learning.MD (5-whys entry format).
Read Loop.MD every session and obey its `status:` machine — when the first working
draft is done, ASK the user whether to turn the loop on (disclosing the free/paid eval
split); while `status: on`, run the FREE Loop.MD evals after every meaningful change
and report per-eval pass/fail. The golden set / paid evals run ONLY per
consent.paid_evals (ask by default — offer at milestones, never auto per-change).
Keep docs/mermaid/*.mmd current when the flow changes (see docs/ARCHITECTURE_FLOW.md).
Obey .power-coding/config.json FMEA triggers: on_pre_commit ALWAYS runs the secret scan
first (`node <skill>/scripts/secret-scan.mjs --staged`) and BLOCKS the commit on a hit, then
a light FMEA on the staged diff (P0 → block and ask); if on_feature_complete, full scan when
a feature is declared done; if smart_suggest, suggest a scan at a natural pause when its
signals fire (never twice for an unchanged HEAD — the change-set is the git range since
state.last_fmea_commit). FMEA is pinned to a sha ("analyzed at <sha>"); re-stamp
state.last_fmea_commit after. The config's failure_categories list is the mandatory checklist.
If sentinel is enabled in .power-coding/config.json, run the four-lens Sentinel Scan
silently after every major task completion — flag only what fires, one line each.
If session_pulse is enabled, show a 2-line effort split (feature/support/rework) after
major milestones and log it in Handoff.MD updates.
Commit a git checkpoint at every working state and before any risky change (obey
consent.git_checkpoints: auto = commit + one-line announce, propose = ask first).
Before starting a feature, build the smallest version that proves it works (per PRD.md's
"Done for v1"), checkpoint, then extend. Any architecture-shaping change (new service,
external dependency, data-model change, async flow) gets a plain-language delta proposal
against the current diagram and user approval BEFORE code. Log
stack/architecture/behavior decisions as one line in Handoff.MD's Decisions; never
silently reverse a logged decision. PRD.md is the product context for evals and scans —
keep it current. Full FMEA scans obey consent.fmea_full_scan (ask | auto).
```

### Layer 2 — Loop Engineering (evals that finetune the app)

Read `references/loop-engineering.md` for the full protocol. Setup steps:

**2a-0. Adopt the project's OWN tests as the cheapest rung first.** Before drafting any
eval, detect what the repo already runs (`package.json` test scripts, `pytest`/`tox`,
`go test`, `cargo test`, and the CI workflow) and record it as **Rung 1** in Loop.MD — the
existing suite IS the cheapest rung; the loop runs it before any eval. **Do not hand-author
evals that just duplicate existing tests** — reserve the eval tiers for behaviour a unit
test can't express (judgement calls: "returns a *sensible* SoV", "refuses out-of-scope
requests"). This is the inverse of eval graduation (2e): tests you already have are adopted
in; evals that mature graduate out.

**2a. Create `Loop.MD`** from `assets/LOOP.template.md`, and **draft 3–6 example FREE
evals from the project itself** — read the brief/README/docs `.md` files (existing
project) or the user's stated goal (new project) and write concrete Q→expected-A pairs
(for an agentic system: input → expected behavior; for an app: action → expected
result). These are labelled EXAMPLES. **Then classify the product:** if its core output
is LLM-generated or a core flow calls paid APIs, also draft a **golden set** from the
brief (8–12 samples: typical, hard/edge, must-refuse; each with a check method —
exact / contains / rubric) and set `consent.paid_evals: "ask"` in the config. See
"Golden set" and "Cost consent" in `references/loop-engineering.md`.

**2b. Ask the user to make it theirs:**

> "**Loop.MD** is ready with example evals drafted from your project docs. Please edit
> it: state your goal for the app, and replace/extend the examples with real
> questions-and-expected-answers. These become the yardstick the loop finetunes
> against."

**2c. The automatic loop offer.** Loop.MD carries `status: waiting_for_first_draft` and
an agent instruction block. The moment the agent completes a **first working draft**
(the core path runs end-to-end once), it must ask:

> "First draft is working. Want me to **turn on the Loop**? After each change I'll run
> the free evals in Loop.MD (they cost nothing), show you per-eval pass/fail, and keep
> finetuning until they pass. The golden set costs real API money — I'll only run it
> when you approve or at milestones."

The cost split in that offer is mandatory, not optional wording — turning the loop on
consents ONLY to free evals; paid runs stay per-approval (`consent.paid_evals`).

User says yes → `status: on`. This trigger is stored in three places on purpose
(pointer block, Loop.MD itself, and a Handoff.MD pending item "offer the loop when
first draft is ready") so it fires even sessions later, on any LLM.

**2d. While the loop is on:** after each meaningful change — cheapest checks first
(typecheck/tests if the repo has them), then walk the FREE Loop.MD evals, report a
per-eval ✅/❌ table, fix, repeat. The golden set NEVER runs automatically per-change:
per `consent.paid_evals`, offer it at milestones ("feature complete — run the golden
set? ~N paid calls") or on request. Any paid run gets a one-line written hypothesis in
Loop.MD's run journal *before* running, and failures get reproduced as free checks
before re-spending — never use a paid check as a debugger.

**2e. Eval graduation (the loop matures into a test suite):** when an eval has passed
3 consecutive loop runs, offer to codify it as an automated test in the repo's stack —
creating the minimal test setup first if none exists (one test runner, one example
test, a one-line run command; explain what it's for, since the user may never have had
one). A graduated eval is marked `(graduated → <test file>)` in Loop.MD and runs in
step "cheapest first" instead of the manual walkthrough — the loop gets *faster* as the
app matures, and the user ends up with a real regression suite without ever being asked
to "write tests".

### Layer 3 — Vibe Debugging (see the flow instead of reading code)

Ask exactly this and wait:

> "For debugging, do you want **(A)** only Mermaid `.mmd` diagram files (+ a standalone
> HTML viewer), or **(B)** also a **temporary, local-only debug tab inside the app**
> that renders them live?"

Then execute the diagram protocol — read `references/diagram-convention.md` and follow
it exactly:

1. **Discover** the real runtime flow by reading entry points and tracing the main path
   (never guess). Classify each step AGENT / FUNCTION / LIBRARY / DATA with its in/out.
2. **Author** `docs/mermaid/NN-title.mmd`. Start **master-only** while a phase is still
   churning (mark `%% granularity: master` — one step per box, big decisions and branches,
   cheap to keep current); expand a lane to full granularity (thresholds, AGENT/FUNCTION
   annotations, `%% granularity: full`) only once it stabilises — per-box granularity on a
   flow you're still reshaping is too heavy to maintain. Give each `.mmd` a
   **`%% files: <the source files it depicts>` header** — this is what makes staleness
   mechanical (step 6). New project with no code yet → draw the *intended* architecture,
   marked `%% intended — not yet built`.
3. **Validate**: `node <skill-path>/scripts/validate-mmd.mjs docs/mermaid`.
4. **Build the viewer**: `node <skill-path>/scripts/build-html.mjs docs/mermaid
   docs/architecture-flow.html` — dependency-free, open in any browser.
5. **(B only)** Scaffold the in-app debug tab per `references/debug-tab-recipes.md`
   (Next.js / Vite recipes; anything else → the standalone viewer). Label it visibly as
   a debug aid, keep it local-only (exclude from production builds or gate on
   `NODE_ENV !== "production"`), and verify it serves before declaring done.
6. **Staleness is detected, not just hoped for.** Diagrams are authored, not
   auto-generated — so the `%% files:` header lets the tooling flag drift instead of
   relying on you to remember: `node <skill-path>/scripts/sentinel.mjs scan` marks a
   diagram stale when any source file it depicts is newer than the `.mmd` (works for
   option A too, not just the debug tab's mtime banner). Update the `.mmd` in the same
   session as any structural change — the git diff of the `.mmd` IS the change-highlight.

**3-align. Architecture alignment (always — this step is never optional).** The user
must approve the shape of the system before code is built against it — a wrong
architecture caught at proposal time costs one conversation; caught after build, a
rewrite. The user may not read code, but they CAN judge a plain-language proposal.

- **New project:** after drawing the intended-architecture diagram, walk it in plain
  language — one line per component: *what it is, why this choice, and its main
  trade-off* ("one Postgres database — simplest thing that scales to thousands of
  users; trade-off: a single point to back up"). End with the failure the user would
  care most about ("if the server restarts mid-payment, X happens"). Then WAIT for
  approval before building. Approval → one line in Handoff.MD's `Decisions`.
- **Existing project:** after discovering the real flow (step 1), confirm it back:
  "This is how your app actually works — [3–5 plain-language lines + the diagram].
  Does this match your understanding?" Mismatches are gold: either the diagram is
  wrong (fix it) or the user's mental model is (fix that — cheaper now than
  mid-debugging).
- **Major enhancements (ongoing, forever):** before building anything that changes the
  shape — new service, new external dependency, data-model change, new async flow —
  present the delta against the current diagram in plain language (what changes, why,
  trade-off), WAIT for approval, then update the `.mmd` and log the decision. The
  scope-brake moment is the anchor: if stating the smallest version reveals a shape
  change, alignment comes before code.

### Layer 4 — FMEA (Failure Mode & Effect Analysis)

FMEA is a reliability-engineering pass (aerospace/automotive lineage): for every code
path, ask *what can go wrong, what does the user feel, what causes it*, and score
Severity × Occurrence × Detection → **RPN** (Risk Priority Number; higher = fix first).
This is NOT lint — it's an LLM reasoning pass that cross-references the diff against the
**product brief and architecture** to find cross-layer failures no single-layer review
catches (frontend assumes 200 but backend rate-limits 429; PRD promises batch-50 but the
queue has no backpressure; webhook races user creation).

**4a. Activation prompt** (also re-runnable later via `power-coding fmea-config`):

> 🔍 **FMEA Scanner — Failure Mode & Effect Analysis**
> Proactively finds how your code can fail in production by cross-referencing changes
> against your product brief and architecture.
> **When should I run FMEA? (select one or more)**
> **[1]** 🏗️ **After major feature builds** — when you say "feature complete" or a
> feature branch is review-ready. Best for architectural/integration failure modes.
> **[2]** 📦 **Before every commit** — light diff-only scan before each commit I make;
> P0 findings block and ask "fix now or commit anyway?".
> **[3]** 🧠 **Smart mode** — I watch for signals (big diffs, new API integrations,
> payment/billing, async/queue code, error-handling or auth changes) and suggest a scan
> at a natural pause. You approve or skip each time.
> **[4]** 🔇 **Off** — manual only; say "run fmea" or "scan for failures" anytime.
> *(Change anytime with: `power-coding fmea-config`)*

**4b. Store the choice** in `.power-coding/config.json` (create from
`assets/fmea-config.template.json`; set the four trigger booleans from the answer —
multiple selections are valid; `manual_only: true` overrides the others). Set
`context_sources.prd_path` to the Layer 0 brief (`PRD.md` or the existing design.MD /
README the user confirmed); if Layer 0 was skipped, leave it null — scans then carry
the "⚠️ running without product context" prefix, since without a brief FMEA degrades
to generic code review. The FULL scan is expensive (minutes of reading and reasoning),
so `consent.fmea_full_scan` defaults to `"ask"`: on feature-complete, ask "run the
full FMEA scan now, or after you've reviewed the diff?" — users who want it silent set
`"auto"`. The pre-commit LIGHT scan stays automatic (it's fast and anchored to the
commit), but its P0 block always asks. The config deliberately carries the
full `failure_categories` list and scoring thresholds, so ANY agent reading the repo can
run a faithful scan even without this skill installed.

**4c. Scan protocol** — read `references/fmea.md` before every scan and follow it: input
collection per trigger, the **mandatory 12-category walkthrough** (systematic coverage
is the whole value — check every category explicitly, report even the empty ones),
calibrated S/O/D anchors, RPN → P0/P1/P2, and the markdown-table output format. Two rules
the protocol now enforces: every scan is **pinned to `<HEAD_SHA>`** (don't background-scan
files being edited elsewhere — it produces already-fixed false-opens), and the change-set /
"already suggested?" is a **git range** (`state.last_fmea_commit..HEAD` in
`.power-coding/state.json`), not a judgement call. The `on_pre_commit` gate runs the
**secret scan first** (`scripts/secret-scan.mjs --staged`, blocks on a hit) before the light
FMEA — see `references/fmea.md` §4.

**4d. Day-one security baseline** — run ONCE at setup (FMEA is diff-scoped and
trigger-gated; the classic day-one disasters happen before any trigger fires and are
permanent once pushed). One pass, three checks:

1. **Secrets:** run `node <skill-path>/scripts/secret-scan.mjs` over all tracked files
   (the same scanner the pre-commit gate uses); verify `.env*` is gitignored (Layer 0
   should have done this — verify, don't assume); no secrets referenced in client-side
   code. A secret already committed → treat as compromised: rotate it, don't just delete
   the line. (This is the one-time baseline sweep; `on_pre_commit` then runs the same
   scanner on every commit so a new leak is blocked before it lands.)
2. **Enforcement side:** anything involving money, auth, quotas, or data deletion must
   be enforced server-side — a client-side check is a suggestion, not a rule.
3. **Inputs:** external input that reaches a database, filesystem, or shell is
   validated/parameterized.

Findings are fixed NOW (before the next push), not logged for later. Record
`modules.security_baseline.done: true` in `.power-coding/config.json` when clean. New
code after this is covered by FMEA's `security_access_control` category and Sentinel's
stop-signal lens — the baseline exists because those only see what changes.

### Layer 5 — Sentinel Scan (background quality sweep)

A silent four-lens check that runs after every major task completion (module done,
feature branch ready, significant refactor finished). No files, no reports — inline
one-line flags only when something fires.

**5a. Activation prompt** (also re-runnable via `power-coding sentinel-config`):

> 🛡️ **Sentinel Scan — Background Quality Sweep**
> After every major completion, I run a fast silent check: misuse traps in your code,
> signals I should've stopped and asked, silent runtime failure gaps, and waste I
> introduced. No output when clean — one-line flags when something fires.
> **Activate?** [1] ✅ Yes — after every major completion *(recommended)*
> [2] 🔇 No — manual only (`run sentinel`)

Store the choice in `.power-coding/config.json` under `modules.sentinel`
(`enabled` / `manual_only`; option 2 flips both).

**5b. The four lenses** (one pass, not four separate checks):

- **🔒 Misuse traps** (Poka-Yoke) — functions/APIs/configs the next person can silently
  misuse: `any` where union fits, booleans where enums are clearer, skippable steps in
  multi-step ops, config keys where typos fall through to defaults.
- **🛑 Stop signals** (Andon) — should I have stopped: code vs Handoff.MD/diagram
  contradiction, ambiguous spec where I guessed, touching 2+ Learning.MD fragility
  entries, billing/auth/delete changes without tests.
- **⚡ Silent failures** (Jidoka) — runtime invisibility: unvalidated external API
  shapes, async without dead-letter, client-only business rules, retry without breaker,
  financial writes without read-back.
- **🗑️ Waste** (Muda) — unnecessary additions: redundant deps, passthrough
  abstractions, pointless re-serialization, undated TODOs.

Flag format (only when triggered):
> `🛡️ Sentinel: [lens emoji] [one-line description of what fired]`

No batched reports. Flags appear inline at the end of the completion message. Multiple
flags are fine — one line each.

**Budget:** stay under ~300 tokens of reasoning per run. Each lens is one boolean
question ("does this apply to what I just built — yes or no?"), not an analysis. The
moment a flag needs more than one line of explanation, it belongs in FMEA instead —
the Sentinel just points, it doesn't diagnose.

### Layer 6 — Session Pulse (effort awareness)

A 2-line signal after major milestones showing where the session's effort went:
feature work vs support/environment work vs rework. No file, no report — one line
with the split, one line with the takeaway. Borrowed from OEE (Overall Equipment
Effectiveness): the availability/performance/quality split reveals the real bottleneck,
which is almost never "writing code slowly" — it's environment friction, lost context,
or rework.

**6a. Activation prompt** (re-runnable via `power-coding pulse-config`):

> 📊 **Session Pulse — Effort Awareness**
> After major milestones, a 2-line signal: where did the effort go — feature work vs
> support/friction vs rework? Spots when sessions spend more time on the wrong things.
> **Activate?** [1] ✅ Yes — after major milestones *(recommended)* [2] 🔇 No

Store the choice in `.power-coding/config.json` under `modules.session_pulse.enabled`.

**6b. Behavior:** the agent estimates a three-bucket split from its own conversation
history — a rough mental tally, NOT a file or counter; ±10% is fine, the signal is
directional:

- **🎯 Feature work** — code, design, decisions that directly advance the asked task
- **🔧 Support work** — env setup, dependency/config/build/CI issues, re-reading code
  for context, doc/API lookups
- **🔁 Rework** — fixing bugs written this session, undoing a failed approach, redoing
  misunderstood requirements

Signal format — appended at the very end of the completion message, after any Sentinel
flags:

> `📊 Pulse: 🎯 ~65% feature · 🔧 ~25% support · 🔁 ~10% rework`
> `   └─ [one-line takeaway]`

Rules:
- Only after MAJOR milestones (feature complete, first working draft, branch
  review-ready), never after every small change.
- The takeaway must be specific to THIS session, not generic advice (e.g. "Most support
  time went to Stripe webhook local testing setup — consider a mock").
- If the split is >80% feature work, just say `📊 Pulse: Clean session ✅` — don't
  waste the user's attention on a non-issue.
- If support or rework is >40%, the takeaway must name the specific cause.
- Never frame this as criticism of the user — it's system feedback, not a performance
  review.

**6c. Handoff.MD logging:** when updating Handoff.MD (after major changes and at
context-low), include a one-liner under a `Session efficiency` field:

```markdown
**Session efficiency:** 🎯 ~65% feature · 🔧 ~25% support (Stripe local setup) · 🔁 ~10% rework
```

This builds a lightweight historical signal: after 4–5 sessions the user can see if the
same support-work cause keeps recurring (env setup every time → invest in dev
containers; constant rework → spec clarity problem upstream).

### Close setup

Show one compact summary: the files created, the magic phrase, what happens
automatically from now on, and the single next action ("edit Loop.MD's evals").

---

## INVOCATION ARGUMENTS

- *(no args)* — first-invoke setup, or Ongoing duties in a configured repo.
- **`fmea`** — run an FMEA scan NOW (manual trigger; works regardless of config; if
  config is missing, run the activation prompt first, then scan).
- **`fmea-config`** — re-run the activation prompt and update `.power-coding/config.json`.
- **`sentinel`** — run Sentinel Scan NOW (manual trigger; works regardless of config).
- **`sentinel-config`** — re-run the Sentinel activation prompt, update config.
- **`pulse`** — show Session Pulse NOW for the current session.
- **`pulse-config`** — re-run the Session Pulse activation prompt, update config.
- **`brief`** — run the Layer 0 interview NOW (create or update PRD.md, set
  `context_sources.prd_path`) — for repos that skipped it at setup.

---

## ONGOING DUTIES (any session in a configured repo)

- **Session start:** read Handoff.MD → **reconcile drift first** (`git log --oneline
  <last-synced>..HEAD` — anything there changed underneath the file) → open with pending
  points or "what now". Read Loop.MD's `status:`.
- **Starting a feature:** scope brake — state the smallest version that proves it works,
  build that first, checkpoint, then extend. If the smallest version reveals an
  architecture-shaping change (new service, external dependency, data-model change,
  async flow), run 3-align's delta proposal and WAIT for approval before code.
- **Working state reached, or risky change ahead:** git checkpoint commit — before the
  risky change, not after it breaks. Obey `consent.git_checkpoints`: `auto` → commit
  and announce in one line; `propose` → ask first.
- **Decision taken (stack / architecture / behavior):** one line in Handoff.MD's
  `Decisions` (date — what — why). Contradicting a logged decision → surface and ask,
  never silently reverse.
- **Before every checkpoint commit / end of every phase:** update Handoff.MD (snapshot,
  re-stamp `last-synced`); update the relevant `.mmd` if the flow changed (`sentinel.mjs
  scan` flags any diagram whose `%% files:` source is newer). Over the ~40-line / ~15-✅
  cap → collapse ✅ into one "Shipped:" line.
- **Low-context signal (secondary):** if the platform warns context is low, update
  Handoff.MD + give the magic phrase — early, not at 2%. (Not the primary trigger — the
  commit/phase events above are, because the model can't measure context reliably.)
- **Bug reported / flow changed / hard-won fix:** entry in Learning.MD (5-whys format:
  symptom → why-chain → deepest why type → action + preventive action). Before debugging
  anything, *check Learning.MD first* — the answer may already be there.
- **First working draft done & loop not yet offered:** make the offer (2c).
- **Loop on:** free evals ✅/❌ after each change; golden set / paid evals only per
  `consent.paid_evals` (offer at milestones); hypothesis before every paid run.
- **Eval passed 3 consecutive runs:** offer to graduate it into an automated test (2e).
- **FMEA triggers** (per `.power-coding/config.json`): feature declared complete →
  full scan (branch diff vs main) — per `consent.fmea_full_scan`, `ask` (default) means
  offer it first, `auto` means run it; about to commit with `on_pre_commit` → **secret scan
  first** (`scripts/secret-scan.mjs --staged`, blocks on a hit), then a light FMEA of the
  staged diff, P0 blocks ("fix now or commit anyway?"), P1/P2 inform only; `smart_suggest`
  signal fired (new webhook/API/payment/async/auth/error-handling code, 200+ line diffs,
  migrations) → offer a scan at the next natural pause, **never twice for an unchanged HEAD**
  (change-set = `state.last_fmea_commit..HEAD`; record declined shas in
  `state.declined_changesets`); "run fmea" / "scan for failures" → scan now, any config.
- **After major task completion (if sentinel enabled):** run the four-lens sweep
  (misuse traps, stop signals, silent failures, waste) as one fast pass. No output if
  clean. One-line inline flag per triggered lens. This is peripheral vision — never a
  report.
- **After major milestones (if session_pulse enabled):** show the effort split signal
  (🎯 feature / 🔧 support / 🔁 rework + one specific takeaway) after any Sentinel
  flags. Also include in Handoff.MD updates for cross-session visibility.
- **Stuck twice on the same bug:** stop; write symptom / tried / best hypothesis / which
  diagram box it lives in, into Learning.MD; show the user and ask for direction —
  pointing at a diagram box beats a third blind retry.

## Guardrails

- **Consent model** (every current and future behavior must fit one of these tiers —
  when adding a layer, place its triggers before writing them):
  - *Cheap + append-only* (Sentinel, Pulse, Handoff/Learning/Decisions writes, diagram
    updates) → consent once at setup, then silent auto. NEVER add a per-run question
    for something cheap — question fatigue trains yes-clicking, which destroys the
    checkpoint questions that matter.
  - *Expensive or flow-interrupting* (full FMEA scan → `consent.fmea_full_scan`;
    golden-set / paid eval runs → `consent.paid_evals`) → per-run ask by default,
    configurable to auto via `consent.*` in `.power-coding/config.json`. Turning the
    loop on is NOT consent for paid runs — free and paid tiers are consented
    separately, always.
  - *State-mutating* (git commits, architecture-shaping changes) → explicit upfront
    choice at setup for commits (`auto` announces each; `propose` asks); architecture
    changes ALWAYS ask — no config can silence 3-align.
- Layer questions are asked ONCE at setup — don't re-interview a configured repo.
- Handoff.MD stays one screen via a **concrete cap**, not a vibe: over ~40 lines or ~15 ✅
  items → collapse ✅ into one "Shipped:" line, detail to Learning.MD.
- Triggers are **events** (commit, phase end, commit-range change, file mtime) — never the
  model's estimate of its own context or memory. That's the point of "dynamic": the
  disciplines fire on things the tooling can detect, not on things the model must remember.
- The debug tab is a dev aid: label it, keep it out of production, never add it if the
  user chose (A).
- Diagrams tell the truth (AGENT vs FUNCTION labels, real thresholds read from code) —
  a wrong diagram is worse than none, the human debugs against it.
- Decisions that change user-facing behavior, cost money, or alter data are the user's:
  recommend with a reason, then wait.
