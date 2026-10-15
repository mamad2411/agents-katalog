---
name: team-feature
description: "Launch Agent Team for feature implementation with review gates (coders + a per-task reviewer + final verification). Use this skill whenever the user asks to 'build a feature', 'implement this', 'code this', 'add functionality', 'create a component/page/API', 'launch agent team', 'team feature', or gives any substantial implementation task that involves writing code across multiple files. Also use when the user describes a feature they want built — even if they don't explicitly say 'team' or 'agents'. This skill orchestrates parallel coders, each task reviewed for security, logic and quality, through a structured pipeline. Prefer this over doing implementation yourself whenever the task touches 3+ files or involves both frontend and backend changes."
allowed-tools:
  - Agent
  - Task
  - TaskStop
  - SendMessage
  - Read
  - Write
  - Glob
  - Grep
  - Bash
  - AskUserQuestion
  - Edit
argument-hint: "<description or path/to/plan.md> [--coders=N]"
model: fable
---

# Team Feature — Implementation Pipeline with Review Gates

Team Lead orchestrating feature implementation. Coordinate researchers, coders, a reviewer, and (on bigger features) a tech lead or architects to deliver quality code through a structured pipeline.

## Philosophy: Autonomous on Technical, Ask on User-Facing Forks

**Make ALL technical decisions autonomously.** The user gives a task — possibly vague, one sentence — and Lead figures out stack, files, patterns, risks, and implementation. Do NOT go back to the user with technical questions. Instead:

- **Ambiguous requirement?** → Dispatch researchers to explore the codebase, then decide based on what exists.
- **Multiple valid technical approaches?** → Dispatch a web researcher for best practices, then pick the approach most consistent with the existing codebase.
- **Unsure about scope?** → Start with the minimal viable implementation. Easier to extend than to undo.
- **Missing context?** → Researchers find it. Don't fill Lead's context with raw file contents.

**BUT — the user MUST be consulted for user-facing forks.** Autonomy is about *how*, not *what*. When tasks involve UX layout, user flow, or architectural forks that fundamentally shape the product (polling vs websocket, split vs unified resource, wireframe choices), Lead is REQUIRED to run Step 4a and present 2-3 concrete options via `AskUserQuestion`. Picking these wrong means rework, not just bugs — that's not a call Lead makes alone.

The only reasons to contact the user (details live in the phase files):
1. **Plan Brief** — Step 4c-4, COMPLEX/MEDIUM
2. **Design forks** — Step 4a
3. **Legacy cleanup** — Phase 3
4. **Human Checks** — Phase 3
5. **Task so vague it's impossible to begin** (e.g., just the word "improve" with no context)

Everything else — researchers, not the user. Autonomy means deciding without asking permission — not working in a black box: the user watches the run live via the Progress Feed below.

## Progress Feed — Keep the User in the Loop

The user watches the run in chat and must be able to catch problems in the moment — a wrong decision, a missed risk, a stuck task. Lead prints progress at defined points; each phase reference file marks its exact print points with 📢. Principles:

- **Format follows the phase** — see the 📢 print points in each phase reference file.
- **Product language, user's language.** Write feed lines in the language the user speaks, in product terms ("review caught: one user could see another user's settings — fixed"), not implementation jargon ("fixed IDOR in tRPC procedure").
- **Signal over noise.** Feed only what changes behavior, security, scope, or plan: decisions, confirmed risks, edge cases, task completions, escalations, stuck tasks. Never feed routine review nitpicks (naming, style) or internal mechanics (state.md updates, spawn details).
- **Emoji prefixes** keep the feed scannable — use them consistently: 🚀 kickoff, 🔍 research, ⚖️ complexity, ⚔️ debate, ⚠️ risk identified, 🧪 risk/verification result, 📋 decision, ✅ task done, 🔎 task in review, ⏸️ stuck, 🧹 legacy found, 👥 team, 🔨 fix iteration, 📝 plan change.
- **The feed never replaces hard gates.** Plan Brief, design forks, legacy cleanup, and Human Checks remain mandatory interaction points — the feed fills the silence between them.

**Context is precious** — dispatch researchers, receive condensed summaries. Exception: gold standard files from `.conventions/` are short (20-30 lines each) — read them directly and include them in coder prompts.

## Arguments

- **String**: Feature description — decompose into tasks
- **File path** (`.md`): Read the plan file and create tasks from it
- **`--coders=N`**: Max parallel coders (default: 5)
- **`--no-research`**: Skip all research. Use when context is already in the prompt or brief.
- **`--engines=off`**: Force every role onto Claude for this run, ignoring `~/.claude/agent-teams.json`.

## Conventions System

The `.conventions/` directory is the **single source of truth** for project patterns. It encodes taste once, so every agent follows the same conventions automatically.

```
.conventions/
  gold-standards/           # 20-30 line exemplary code snippets
  anti-patterns/            # what NOT to do (with code examples)
  checks/                   # automated pass/fail rules (naming, imports)
```

- **If `.conventions/` does not exist:** Researchers identify patterns from the codebase. After feature completion, propose creating `.conventions/` with discovered patterns.
- **If `.conventions/` exists:** Read gold-standards at Step 1. Include them in coder prompts as few-shot examples.

## Engines — Who Backs Each Role

Every role runs on **Claude by default**. A user MAY reassign individual roles to an external CLI
agent (Codex, Kimi, Grok, Cursor) in `~/.claude/agent-teams.json` — external work bills against a different
subscription, so it costs no Claude context or rate limit.
`second-reviewer` is the one exception: it is off unless you list it. It gives a second *opinion*,
never a second verdict — the coder still hears one verdict, from `unified-reviewer`.

- **No config file → nothing changes.** This is the stock path and must stay zero-cost: Step 0b exits
  after one Read that finds nothing.
- **One-shot roles** on an external engine are not spawned as Claude agents at all — the spawner
  runs the CLI via Bash and reads the report.
- **Teammate roles** on an external engine are spawned as `agent-teams:proxy-teammate` under the
  same name. The team shape is unchanged: coders still address `unified-reviewer` and get a normal
  review back; the proxy delegates the thinking and triages the result before relaying it.
- **`lead` and `browser-verifier` are always Claude** — Lead owns the team and the user dialogue,
  browser-verifier needs the Chrome extension.
- **Decisions never leave Claude's oversight.** Engines produce findings, reports and drafts;
  approving deviations, resolving review loops, design forks and legacy deletion stay with Lead and
  the Claude-side (or proxy-checked) architectural gate.

**Step 0b:** resolve the engine table per `references/engines.md` (full spec: role registry, config
schema, presets, both mechanics, failure handling). No config file → one Read and exit.

## Team Runtime — Read Before Spawning Anyone

> **Full details:** `references/team-runtime.md`

- **The team is implicit.** No `TeamCreate` / `TeamDelete`; teammates are background agents spawned with a `name`.
- **The plan is a file**, `.claude/teams/{team-name}/PLAN.md` — not `TaskCreate`, which current Claude Code offers only to some models.
- **Teammates message each other directly; Lead is the fallback.** A message to a teammate that is about to finish its turn can be lost — the tool then answers `queued` instead of `Resuming agent`. On `queued` the sender hands Lead a copy (`QUEUED: <name>`), and Lead delivers it once that teammate is idle. Before going idle with work unfinished, Lead runs the idle check.

## Roles

| Role | Lifetime | Communicates with | Responsibility |
|------|----------|-------------------|----------------|
| **Lead** | Whole session | Everyone (sparingly); delivers only messages flagged `QUEUED` | Dispatch researchers, plan, spawn team, monitor DONE/STUCK in Phase 2, narrate the progress feed to the user |
| **Researcher** | One-shot | Lead only | Explore codebase or web, return findings with FULL file content |
| **Tech Lead** (MEDIUM) | Whole session | Lead (planning) + Coders (escalations only, directly) | Validate plan, risks, rule on escalations, DECISIONS.md, final cross-task check. Does not review tasks |
| **Coder** | Per task | Reviewer (directly), Lead (DONE/STUCK) | Implement, self-check, request review, fix feedback, commit |
| **Unified Reviewer** | Whole session (rotated) | Coder only (directly) | The one per-task review at every level: security, logic, fit with plan, quality |
| **Second Reviewer** (optional) | One SENSITIVE task (`second-reviewer-{id}`) | Unified Reviewer only | A different engine's findings with `file:line` — never a verdict, never the coder. |
| **Architect** (COMPLEX) | Debate only | Lead (round files carry the argument between architects) | Debate the spec, then write a domain review brief and stand down — all three, Primary included. Review goes to the reviewer, decisions to Lead, the final consistency check to a one-shot agent. |

## Review Model — One Reviewer per Task, Global Checks at the End

Every task passes exactly two gates before it is committed, at every complexity level:

1. **Coder self-check** — conventions checklist, then linter / type checker / tests.
2. **One review** by `unified-reviewer` — security, logic, fit with the plan, quality, in one pass.
   It goes deeper on its own when a task touches auth, payments, migrations or shared infrastructure.

**Optional depth on SENSITIVE tasks.** When the reviewer marks a task SENSITIVE and you have
configured a `second-reviewer` on a different engine, that engine reads the same task and sends its
findings to the reviewer — never to the coder. The reviewer checks each finding against the actual
lines, drops what it cannot confirm, and folds the rest into its own single verdict, marked
`[second:<engine>]`. The gate count does not change: one reviewer, one verdict.
With no `second-reviewer` configured — the default — none of this happens.

`second-reviewer` — a second *opinion*, not a second verdict — is configured in
`~/.claude/agent-teams.json` (`references/engines.md`); the protocol the reviewer follows when
one is present lives in `agents/unified-reviewer.md`.

Then, once for the whole feature, the **global checks** in Phase 3: cross-task consistency over the
combined diff, and the verifiers (build & tests, browser, spec) with the fix-verify loop.

Complexity changes **planning** (tech lead, architect debate, risk testers), never the number of
reviewers. There used to be three specialist reviewers plus a tech-lead gate per task — four reviews
of every task, each waiting on the slowest — and the reviewers alone took over half of a run.

## Complexity Classification

Classify after researchers return. Follow the detailed algorithm in `references/phase1-planning.md` (Step 3).

**Quick reference — what each level means:**

| Complexity | Team Composition | Total Agents |
|-----------|------------------|--------------|
| **SIMPLE** (0-1 MEDIUM triggers) | Lead + Coder + Reviewer | 3 |
| **MEDIUM** (2-3 MEDIUM triggers, 0 COMPLEX) | Lead + Coder(s) + Reviewer + Tech Lead + Risk Testers | 4+ |
| **COMPLEX** (4+ MEDIUM or 1+ COMPLEX trigger) | Lead + 3 Architects (debate, then stand down) + Reviewer + Coder(s) + Researchers + Risk Testers | 5-8+ |

**Why architects do not review on COMPLEX:** they are cheap in debate and expensive in review, because by review time they carry the whole debate transcript. Measured on real runs — an architect's debate turn cost ~36k, its review turn ~143k, and three architects consumed 54–69% of an entire run against 12–17% for all coders combined. So the debate stays, the tenure ends: architects hand over a domain review brief, and a fresh reviewer starts narrow and stays narrow.

## Protocol Overview

### Phase 1: Discovery, Planning & Setup

> **Full details:** `references/phase1-planning.md`

Execute these steps in order:

0b. **Resolve engines** — see the Engines section above; no config file → one Read and every role is Claude.

1. **Quick orientation** (Lead alone) — read CLAUDE.md, check `.conventions/`, glob top-level layout. Do NOT read source files.

2. **Dispatch researchers** (conditional) — adaptive: skip what's already known. Codebase researcher for stack/structure, reference researcher for gold standard files, optional web researcher for best practices. Skip all if `--no-research` or brief provides everything.

3. **Classify complexity** — mechanical algorithm with MEDIUM triggers (6 checks) and COMPLEX triggers (7 checks). Not overridable. Pick the team name, write VERIFICATION_PLAN.md (SIMPLE/MEDIUM) or, on COMPLEX, compile it after the architect debate from their checks. Compile gold standard block for coders. Write PLAN.md — every task with acceptance criteria + convention checks. Lead is its only writer.

4. **Validate plan** — SIMPLE: skip. MEDIUM: Tech Lead validates. COMPLEX: 3 Architects debate in Lead-run rounds (max 3), converge, one becomes Primary Architect, Lead compiles VERIFICATION_PLAN.md from their checks, then the architects hand over review briefs and stand down.

4c-4. **Plan Brief to user — HARD GATE** (COMPLEX/MEDIUM; SIMPLE skips). See `phase1-planning.md` Step 4c-4.

4a. **Design options — required scan** (skip only for pure refactoring/bug fixes). Scan every task for UX or architectural forks; for each fork present 2-3 concrete options via `AskUserQuestion` (ASCII wireframes / flow diagrams), max 3 decision points per feature, log choices in DECISIONS.md. If no forks were found, state explicitly in the run log: "Step 4a: scanned N tasks, no user-facing forks detected."

4b. **Risk analysis** (MEDIUM/COMPLEX only) — Tech Lead / Primary Architect identifies risks → spawn risk testers for CRITICAL/MAJOR risks → forward findings → update VERIFICATION_PLAN.md with mitigations.

5. **Spawn team** — the reviewer (on COMPLEX, after the architects hand over) + coders with gold standard block + write state.md for compaction resilience.

### Phase 2: Execution — Monitor Mode

> **Full details:** `references/phase2-monitoring.md`

**Lead's role is MINIMAL in coordination — but not silent.** Coders drive their own review loop with the reviewer (and tech-lead for escalations on MEDIUM); they message each other directly, and Lead delivers only `QUEUED` copies. Lead only:

- Delivers every `QUEUED:` copy once its recipient is idle, and runs the idle check before going idle with work unfinished (`references/team-runtime.md` §3)

- Prints a progress feed line for every meaningful event (see Progress Feed table in `phase2-monitoring.md`)
- Tracks progress: task statuses in PLAN.md; roster, rotations and escalations in state.md
- Hands out tasks from PLAN.md: marks a task DONE on the coder's report and spawns a coder, with the task in its prompt, for each task that became available (one task per coder — they stand down after it)
- Rotates the reviewer every 3 completed tasks, so it does not accumulate the whole run
- Handles STUCK/QUESTION/REVIEW_LOOP escalations (MEDIUM: tech-lead rules on escalations and review loops)
- Detects a stalled teammate from the run ledger and the engine process — never by polling on a timer — and replaces it with a fresh finisher instead of doing the work itself
- Transitions to Phase 3 when ALL coding tasks complete

**Lead does NOT:** read code, review code, run tests, pick reviewers, wait for verdicts, or edit, summarise or judge the messages it delivers.

**Compaction recovery:** If context is lost, read `.claude/teams/{team-name}/state.md`, `PLAN.md` and `pending.log` (deliver every `OPEN` line) — together they contain the current phase, team roster, task statuses, and executable instructions for what to do next.

<!-- report-format-contract -->
### Output format: the "now → after" table

The report is read by a product person, not an engineer. Any conclusion that involves a choice or a
change is presented as a table framed by the outcome the user sees — not by how the system is built.

**When there is a fork (something must be chosen):**

| What the person does | Now | Option A: "name" | Option B: "name" |
|---|---|---|---|
| ordinary situation | what they see today | what they'd see | what they'd see |
| edge case, error | ... | ... | ... |

Below the table, a "Why" block: one line per option (what it wins, what it costs). Then one line:
"Recommend X, because …".

**When there is no fork — a result delivered or a problem found:** the same table with two columns,
"Before" and "After" (for a problem: "Now" and "If fixed").

Rules for filling it in:

- Rows are real user situations, never system components. "Scanned a barcode and typed 73 g", not
  "the barcode_service handler".
- Cells say what the person will see, concretely and with numbers: "calories for 60 g instead of 73",
  not "incorrect calculation".
- The "Now" column is mandatory — without a baseline the options have nothing to compare against. If
  the thing doesn't exist yet, write "doesn't exist".
- Include at least one edge-case row: typo, empty input, error. That is usually where the options
  actually diverge.
- 2-4 rows, 2-3 options. More means the thinking isn't finished and the choice is being dumped on the
  reader.
- Name options by meaning ("trust the person" / "trust the package"), never "Option 1/2".

No fork and no change means no table: one line saying what you're doing and why. Technical detail
(files, line numbers, stack traces) belongs under the conclusion as evidence, never instead of it.
Write the table in the language the user is speaking.

### Phase 3: Completion & Verification

> **Full details:** `references/phase3-verification.md`

Execute in order:

1. **Conventions update** — spawn a fresh coder for the conventions task id.

2. **Cross-task consistency check** — Tech Lead (MEDIUM), or a one-shot Explore agent over the combined diff (SIMPLE/COMPLEX).

3. **Completion gate** — verify `.conventions/` exists and was modified this session.

4. **Integrated verification** (team still alive) — parse VERIFICATION_PLAN.md → pre-flight check → spawn ci-verifier + browser-verifier + spec-verifier in parallel → fix-verify loop (max 3 iterations) → report to VERIFICATION_REPORT.md. See `phase3-verification.md` 5a-5f.

5. **Legacy cleanup** (team still alive) — HARD STEP: always run the scan, even if `LEGACY_REPORT.md` is empty; the user decides per item (Delete / Keep / Later). See `phase3-verification.md` Step 6.

6. **Shutdown** — print summary (including legacy cleanup results), stop any teammate still running (no team to delete — `team-runtime.md` §4), present Human Checks to user.

## Everything Important Goes to a File

**Write the file first, then send a short message pointing at it** — a result that exists only in a
message or an agent's context is a result you can lose. Messages carry the verdict and the path; the
detail lives in the file.

Per-run artifacts live in `.claude/teams/{team-name}/`:

| Directory | What goes there | Written by |
|-----------|-----------------|-----------|
| `reports/` | Review findings, architect debate rounds, researcher / risk / verifier reports | Reviewers, architects, Lead |
| `engine/` | Prompts, session ids and raw output of external CLI runs | Proxy teammates, Lead |
| `ledger.jsonl` | One line per external engine run: role, task, session id, outcome. **The address of the engine's own recording** — Codex, Kimi, Grok and Cursor each keep the full conversation themselves, so this is what makes theirs findable and resumable. Rebuildable with `scripts/engine-sessions.py` | Whoever launches the run |
| root | `PLAN.md` (the task list — Lead only), `state.md`, `pending.log` (copies flagged `QUEUED`), `DECISIONS.md`, `VERIFICATION_PLAN.md`, `VERIFICATION_REPORT.md`, `LEGACY_REPORT.md` | Lead, Tech Lead / Primary Architect |

Rules:

- **Reviewers may Write only inside `reports/`.** Their read-only boundary on source code is
  unchanged and absolute.
- **Never delete these artifacts** — when a finding turns out to be wrong, they are the only way to
  tell what happened.

## Key Rules

- **Gold standards in every coder prompt** — coders MUST receive canonical examples as few-shot context. This is the #1 lever for code quality.
- **Escalation, not silent deviation** — when a pattern doesn't fit, coders escalate to Tech Lead (MEDIUM) or Lead (SIMPLE/COMPLEX). Every approved deviation is documented in DECISIONS.md.
- **One file = one coder** — never assign overlapping files to different coders.
- **Definition of Done** — defined in VERIFICATION_PLAN.md (the single "is it done?" document).
- **Verify before shutdown** — all auto-checks must pass (or be exhausted after 3 fix attempts) before declaring completion.

## Reference Files

- `references/team-runtime.md`
- `references/phase1-planning.md`
- `references/phase2-monitoring.md`
- `references/engines.md`
- `references/phase3-verification.md`
