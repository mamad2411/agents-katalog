---
name: investigate
description: >-
  The Infiquetra systematic-debugging engine. Find the ROOT CAUSE of a bug, test
  failure, error, or unexpected behavior BEFORE any fix — trace the full
  trigger→symptom causal chain with no gaps, ground every hypothesis in observed
  evidence, and only then apply a GATED, trivial-scope, self-verified fix.
  Diagnosis is the primary deliverable: it writes an agent-consumable DEBUG
  REPORT, routes real implementation work to /work via a mission-control issue, design
  problems to /brainstorm, and trackable defects to mission-control. READ-ONLY on the
  world and the saga; never commits, pushes, opens a PR, or deploys. Triggers on
  "investigate", "debug this", "why is this failing", "trace this error", "root
  cause", a pasted stack trace / error message / issue ref, or a /qa
  hand-in for a deep failure.
---

# Investigate

`/investigate` answers **"What is the ROOT CAUSE — and is there a fix small enough to apply safely here?"**
It investigates a bug systematically, traces the full causal chain from trigger to symptom **before**
proposing anything, and treats the **diagnosis as the deliverable**. The fix is optional, gated, and
deliberately small; real implementation work routes to `/work`.

This engine is a faithful 3-source merge. The **spine** — investigate-before-fixing, the causal-chain
gate, and predictions-for-uncertain-links — is a PORT of **CE `ce-debug`**. The **pattern-signature
table** and the enum'd **DEBUG REPORT** status (`DONE` / `DONE_WITH_CONCERNS` / `BLOCKED`) are GRAFTS
from **gstack `investigate`**. The **Iron Law** ("no fixes without root-cause investigation first") and
the **multi-component boundary instrumentation** technique are BORROWED from superpowers
`systematic-debugging` (self-contained here — superpowers is **not** a runtime dependency).

## Position in the lifecycle

`/investigate` is **OFF-CHAIN** (like `/doc-review` and `/founder-review`): it is **not** a
lifecycle phase, it does **not** advance `lifecycle_phase`, and it writes **no** saga tick. It is a
**routed diagnostic lens** reachable three ways:

- **(a) directly** — `/investigate <error | test | issue# | description>`;
- **(b) via `/qa`** — when a functional test meets a failure that wants root-cause work;
- **(c) via `/qa`** — `/qa` routes deep **post-merge** failures here for root-cause analysis (`/qa`'s
  Phase 6.2 routes deep post-merge root-cause failures here).

It is not on the linear spine. Its outputs route **back** onto the
spine: an applied trivial fix ships through `/work` or `/code-review`; a real fix becomes a `mission-control`
issue that `/work` then executes; a design problem goes to `/brainstorm`.

## Core principles

1. **Investigate before fixing — the IRON LAW.** NO FIX until you can explain the **full causal chain**
   from trigger to symptom with **no gaps**. "Somehow X leads to Y" is a gap. The causal-chain GATE
   (Phase 2) is the enforcement: you do not enter Phase 3 until the chain is complete. Fixing a symptom
   creates whack-a-mole debugging; every symptom patch makes the next bug harder to find.
2. **Predictions for uncertain links.** For each **uncertain or non-obvious** link in the chain, form a
   prediction — something in a **different code path or scenario** that must also be true if the link is
   correct. A wrong prediction with a fix that "works" means you found a **symptom, not the cause** — the
   real cause is still active. When the chain is obvious (missing import, explicit null deref), the chain
   explanation itself is the gate; a prediction is for uncertain links only, never a ritual.
3. **Evidence before hypothesis.** Run an **assumption audit** first — list every "this must be true"
   belief and mark it *verified* (you read the code, checked state, or ran it) or *assumed*; assumptions
   are the most common source of stuck debugging. Then **instrument the boundaries**: capture the
   **actual** values at each component boundary, never assumed ones. "X seems off" is not evidence;
   "X equals null at `file:42` because Y was never initialized under condition Z" is.
4. **One change at a time; when stuck, diagnose why.** No shotgun debugging — one hypothesis, one change,
   one test. When stuck, do not try harder; diagnose **why** you are stuck. Two **distinct** numeric
   gates govern this (kept separate — see below): the Phase 2 **hypothesis-exhaustion** gate and the
   Phase 3 **3-failed-fix-attempts** gate.
5. **Diagnosis-PRIMARY; the fix is GATED, trivial-scope, and self-verified.** The **DEBUG REPORT** is the
   deliverable. The user chooses fix-vs-diagnosis. Only a **trivial / single-concern** fix is applied
   inline (test-first + the engine's **own** verification); any real implementation work **routes to
   `/work`**. `/investigate` never commits, pushes, opens a PR, or deploys.
6. **Read-only on the world and the saga.** `gh` and `saga.py` are used **read-only** (`restore` /
   `ticks` for evidence; never mint, never `save`). Real fixes route to `/work`; trackable defects route
   to `mission-control`; design problems route to `/brainstorm`. Large or parallel read-only investigation is
   **offered** a backend (operator-choice), never auto-launched.
7. **Leave the system smarter.** The deliverable is an **agent-consumable DEBUG REPORT** a future agent
   can act on cold. A **non-obvious** root cause is promoted (gated, selective) to the engineering
   journal `LEARNINGS.md`; a localized mechanical fix with no generalizable insight is skipped silently.

## The two distinct numeric gates

These are **two separate counters** — do **not** merge them into one "3-strike" rule:

- **Phase 2 — HYPOTHESIS-EXHAUSTION gate.** When **2-3 hypotheses are exhausted** without confirmation,
  STOP and run the **smart-escalation table** (`references/methodology.md`). This is the gstack
  "if 3 hypotheses fail → STOP, this may be architectural" numeric form. It counts **hypotheses**.
- **Phase 3 — 3-FAILED-FIX-ATTEMPTS gate.** After **3 applied fixes fail**, question the **architecture**
  and return to root-cause (Phase 2). This counts **applied fix attempts**, not hypotheses. A failed fix
  with a wrong root cause is a Phase-2 problem wearing a Phase-3 costume.

## Interaction method

Use `AskUserQuestion` for choices from a known set (fix-vs-diagnosis-vs-rethink, an execution backend for
large/parallel read-only investigation, the trivial-bug fast-path apply/skip). Call `ToolSearch` with
`select:AskUserQuestion` first if its schema is not loaded; a pending schema load is not a reason to fall
back. Ask one question per turn; never silently skip a question. Do not ask questions **by default** —
investigate first (read code, run tests, trace). Ask only when a genuine ambiguity **blocks**
investigation and cannot be resolved by reading code or running tests.

In a channel session (`redis-channel` active), `AskUserQuestion` cannot be called — inline the choices in
your reply text instead, following the canonical channel-inline convention in
`saga/skills/brainstorm/SKILL.md` (do not duplicate its wording here).

<!-- gate-record: id=investigate-interaction absence=HALT transport=ask-user-question -->
**Operator-absence contract (#371).** Every known-set gate above declares what happens on
silence, and the declaration above this line is the contract. `HALT` here: stop and wait. A timeout,
a widget error, or a dropped session is never consent — do not proceed on a default and do not
invent an answer. Ask one question at a time and read the decision from the operator's actual
answer, never from a widget's raw return value.

Use repo-relative paths in every generated document. Absolute paths break portability across machines and
worktrees. (The one exception is a saga `--saga-id` value — a derived id, not a path.)

---

## Phase 0 — Triage

Parse the input and reach a clear problem statement. The input is an **error message**, a **test path**,
a **GitHub issue ref**, or a **free-text description of broken behavior**. Take it from command arguments
or the active artifact.

**Issue reference** (`#N`, `org/repo#N`, a github.com URL): fetch it **read-only** and read the **full
comment thread**, not just the opening post:

```bash
gh issue view <N> --json title,body,comments,labels
```

Comments frequently carry updated repro steps, narrowed scope, prior failed attempts, or a pivot to a
different suspected cause; treating the opening post as the whole picture sends the investigation the
wrong way. Everything else (stack traces, test paths, error messages, descriptions) **is** the problem
statement.

**Trivial-bug fast-path.** If the cause is immediately readable from the input (single-file typo, missing
import, obvious null deref / off-by-one with a one-line fix) and verification needs no deep tracing,
present the cause and the proposed one-line fix, then run the Phase 2 **fix-vs-diagnosis gate** before
editing — the fast-path saves investigation ceremony, not the user's choice. If the user picks fix, run
Phase 3's workspace/branch check, apply it, self-verify (fresh-reproduce), and skip to the Phase 4 DEBUG
REPORT. If diagnosis-only, write the report and stop. **When in doubt, run the full framework** — a wrong
root cause costs more than the ceremony.

**Prior-attempt awareness.** Only when the user signals prior failure ("keeps failing", "I've been
trying", "stuck"), ask what they already tried before investigating — this avoids repeating dead ends and
is one of the few cases where asking first is right.

**Saga evidence (READ-ONLY).** If a work-thread saga exists for this change, read it for evidence —
**never** mint or write it:

```bash
python3 plugins/saga/scripts/saga.py restore --saga-id <issue-N|task-slug>
python3 plugins/saga/scripts/saga.py ticks --saga-id <issue-N|task-slug>
```

Then proceed to Phase 1.

---

## Phase 1 — Investigate (read-only on the world)

See `references/methodology.md` for the full recipes.

**1.1 Reproduce.** Confirm the bug exists and understand its behavior — run the test, trigger the error,
follow the reported steps. For a UI surface, drive the running app with the installed
chrome-devtools / playwright MCP (read console + network). If it does not reproduce after 2-3 attempts,
use the intermittent-bug techniques in the reference; if it cannot reproduce at all here, document what
was tried and what conditions appear missing.

**1.2 Environment sanity.** Before deep tracing, confirm the environment is what you think — branch,
dependencies installed/up-to-date, expected runtime version, required env vars present, no stale build
artifacts, dependent local services running *when the bug plausibly involves them*. Stale `node_modules`
/ artifacts are a frequent false lead. The full checklist is in `references/methodology.md`.

**1.3 Trace backward.** Trace data flow **backward** from the symptom to where valid state **first became
invalid**. Read the stack trace **bottom-to-top** (the bottom frame is the symptom; the cause is
upstream), then **instrument the boundaries** around the first frame with invalid data to capture the
**actual** values. For a bug crossing subsystems, use **multi-component boundary instrumentation** — log
what enters and exits **every** boundary in one run and read the log linearly; the boundary where data
first stops matching expectation is the failing layer. Do not stop at the first function that looks
wrong — the cause is where bad state **originates**.

**1.4 Recent changes + evidence.** As you trace, check recent changes (`git log --oneline -10 -- <file>`,
`git blame`). If the bug is a regression ("it worked before"), use `git bisect` (recipe in the
reference). Harvest evidence from `gh` (issue/PR/check output, read-only), application logs, the saga
ticks from Phase 0, and any prior-session skeletons — all read-only.

---

## Phase 2 — Root cause

*Reminder: investigate before fixing. No fix until the full causal chain has no gaps.*

**Assumption audit (first).** List every "this must be true" belief your understanding depends on and
mark each *verified* or *assumed* (principle 3). Many "wrong hypotheses" are correct hypotheses tested
against a wrong assumption.

**Pattern-signature match.** Check the symptom against `references/pattern-taxonomy.md` — gstack's 6
signatures (race / null / state-corruption / integration / config-drift / stale-cache) **plus** the
infiquetra serverless row (cold-start / IAM-permission / eventual-consistency-DynamoDB / throttling /
env-or-SSM-drift). Pattern-matching is cheap and points the trace at the right place first.

**Form hypotheses**, ranked by likelihood. For each:

- **what** is wrong and **where** (`file:line`);
- **≥1 concrete observation** that supports it — a runtime value, a log line, an instrumented boundary
  capture, a behavior delta against a working case. "X seems off" is theorizing; go back to Phase 1 and
  instrument;
- the **step-by-step causal chain** from trigger to symptom;
- **for uncertain links** — a prediction (principle 2). Obvious chains skip the prediction.

**Causal-chain GATE.** Do **not** proceed to Phase 3 until the full chain — trigger through every step to
symptom — has **no gaps**. The user may explicitly authorize proceeding with the best-available
hypothesis if investigation is stuck.

**Hypothesis-exhaustion gate (Phase 2's numeric gate).** When 2-3 hypotheses are exhausted, STOP and run
the **smart-escalation table** (`references/methodology.md`): different-subsystem scatter → design
problem (suggest `/brainstorm`); self-contradicting evidence → wrong mental model, re-read without
assumptions; works-locally-fails-elsewhere → environment problem; fix-works-but-prediction-wrong →
symptom, keep investigating.

**Parallel read-only sub-agents (offer).** When hypotheses are **evidence-bottlenecked across clearly
independent subsystems**, run read-only probes in parallel — `inline` is the only backend since
issue #1030 archived the others, so there is nothing to offer — to dispatch
read-only probes in parallel — each with one explicit hypothesis and a structured evidence-return
format, **no edits**. Never auto-spawn; skip when hypotheses depend on each other. Parallel sub-agents
use **generic** `Explore` / `Task` agents (this plugin has no `agents/` dir for probe-specific
personas), each read-only and each in its own disposable worktree, so a probe can run commands
without its `git checkout` reaching the tree under investigation.

**Present findings + the gate.** Present the root cause (causal-chain summary with `file:line`), the
proposed fix and which files would change, the recommended regression test, and whether existing tests
should have caught it. Then run the **fix-vs-diagnosis-vs-rethink gate** via `AskUserQuestion`:

<!-- gate-record: id=investigate-fix-vs-diagnosis absence=HALT transport=ask-user-question -->
This gate is a durable gate-record (`investigate-fix-vs-diagnosis-<run-id>`) under the
Interaction-method contract above: open before prompting, satisfy on answer, `resolve-absent` on
silence (`HALT`).

1. **Fix it now** — proceed to Phase 3 (only applies the fix if it is trivial/single-concern; else
   diagnose + route to `/work`).
2. **Diagnosis only — I'll take it from here** — skip Phase 3, write the report (Phase 4), stop.
3. **Rethink the design** — only when the root cause reveals a **design problem** (a wrong responsibility
   or interface, wrong/incomplete requirements, or every fix is a workaround). Route to `/brainstorm`.
   Size alone never makes a bug a design problem.

Gate-divergence telemetry (optional, issue #399): record via `gate_id`
`investigate-fix-vs-diagnosis`, recorded in the run record --
the offered default is whichever option the presented findings most directly recommend.

---

## Phase 3 — Fix (GATED, optional, trivial-scope, own verification)

Run this phase **only** if the user chose "Fix it now" **and** the fix is **trivial / single-concern**.
If the proper fix is real implementation work, **diagnose and route to `/work`** instead — do not grind a
big change in here.

*Reminder: one change at a time.*

**Workspace / branch check.** Before editing: `git status` — if the user has uncommitted work in files
that need changing, confirm before editing. If on the default branch, ask whether to create a feature
branch (detect the default via `main` / `master` / `git rev-parse --abbrev-ref origin/HEAD` with the
`origin/` prefix stripped).

**Test-first.** (1) Write a **failing regression test** that captures the bug; (2) verify it fails for
the **RIGHT reason** — the root cause, not unrelated setup; (3) implement the **minimal, root-cause-only**
fix — no drive-by refactors, formatting, or unrelated cleanup; (4) the test passes; (5) run the **full**
suite for regressions; (6) self-review the diff.

**Own minimal verification.** Fresh-**reproduce the original bug** and confirm it is fixed — this is the
engine's **own** verification, not optional. `/investigate` does **NOT** route to `/qa` to verify; the
acceptance gate is a separate, downstream concern.

**On a failed fix.** Return to Phase 2 and **explicitly INVALIDATE the current hypothesis first** — state
what evidence ruled it out — then form a new one with its own grounding observation and prediction. Do
not retry variants of the same theory (the rationalization spiral).

**3-failed-fix-attempts gate (Phase 3's numeric gate, separate from Phase 2's).** After **3 applied fixes
fail**, the root-cause identification was likely wrong: question the **architecture** and return to
Phase 2.

**Blast-radius FLAG.** A fix touching **>5 files** is a **FLAG** — surface the blast radius to the user
and offer a backend — **not** the inline-vs-route discriminator. The discriminator is
**trivial/single-concern vs real implementation work**; a 6-file mechanical rename can still be trivial,
and a 1-file change can still be real work that belongs in `/work`.

**Conditional defense-in-depth.** When the root-cause pattern exists in **3+ other files** (grep the
signature) or the bug would have been catastrophic in production, add guards at the appropriate layers
(entry validation / invariant check / environment guard / diagnostic breadcrumb) per
`references/methodology.md`. Skip for a one-off with no realistic recurrence path.

`/investigate` **never** commits, pushes, opens a PR, or deploys — even after a successful self-verified
fix. Shipping is `/work` / `/code-review`'s job.

---

## Phase 4 — Report + route

**4.1 Emit the DEBUG REPORT.** Write the agent-consumable report to:

```
docs/investigations/<slug>-<date>.md
```

Use the enum'd shape in `references/debug-report.md`: **Symptom** / **Root cause** (causal chain with
`file:line`) / **Fix** (or "diagnosis only") / **Evidence** / **Regression-test path** / **Related** /
**Status** (`DONE` / `DONE_WITH_CONCERNS` / `BLOCKED`).

**4.2 Learning capture — BOTH-SPLIT.** Two distinct sinks, by what was found:

- **Non-obvious root cause → journal `LEARNINGS.md`** (gated, **selective**): append a new learning when
  the lesson is generalizable (a wrong assumption about a shared dependency, a pattern in 3+ locations).
  Skip silently when the fix is mechanical with no insight. Promotion is a pure append per the journal
  rules; offer it neutrally when the lesson is one sentence.
- **Trackable confirmed defect → `mission-control`** (as a **defect-type SDLC issue**, `--issue-type defect`):
  the report is **agent-consumable EVIDENCE**, not a handoff source. Open the defect by **describing the
  bug** with the report **LINKED** as evidence inside the issue. **NEVER pass the report path to
  `handoff_envelope`'s classifier** — `infer_maturity` keys on `docs/plans/` / `docs/brainstorms/` etc.
  and does not recognize `docs/investigations/`, so it would fall through to `requirements-ready` and
  mis-classify the report. See `references/debug-report.md`.

**4.3 Route** to the command that owns what the investigation found:

- **inline fix applied + self-verified** → `/work` or `/code-review` to **SHIP** it via a PR (the fix is
  on a branch; `/investigate` does not push it);
- **real fix needed** → `mission-control` → SDLC issue → `/work` executes it (NOT by handing `/work` a
  `docs/investigations/` path — `/work` consumes a plan path, a GitHub issue, or a resume request);
- **design problem** → `/brainstorm`;
- **diagnosis-only** → stop.

There is **NO saga write** — `/investigate` is off-chain and saga READ-ONLY.

---

## Hard boundary

`/investigate` investigates, diagnoses, optionally applies a trivial self-verified fix, writes the DEBUG
REPORT, and routes — then stops. It does **NOT**:

- mutate the world or the saga — `gh` / `git` / `saga.py` are **READ-ONLY** (`restore` / `ticks` for
  evidence only; never `save`, never mint);
- **commit, push, open / update / merge a PR, or deploy** — even after a successful fix;
- **file SDLC issues** — `mission-control` owns the SDLC, and defects route through it;
- **route to `/qa` to verify** — it does its **own** fresh-reproduce verification; the acceptance gate is
  downstream and separate;
- **write the saga** — off-chain, no `lifecycle_phase` advance, no tick;
- do **real implementation work inline** — that routes to `/work`; only trivial/single-concern fixes
  apply here;
- **path-classify the DEBUG REPORT** — never pass `docs/investigations/...` to `handoff_envelope`; link
  it as evidence in a described DEFECT instead.

`fix` is this engine's identity verb — gated-allowed, trivial-scope, self-verified. It is never the
default action; the diagnosis is.

---

## Reference files

- `references/methodology.md` — the full procedure: triage (trivial fast-path + prior-attempt);
  investigate (env-sanity checklist + backward-trace recipe + multi-component instrumentation +
  git bisect); root-cause (assumption audit + hypotheses-with-evidence + predictions + causal-chain
  gate + smart-escalation table + the hypothesis-exhaustion gate + parallel read-only sub-agent dispatch
  via `../../../references/operator-choice.md`); fix (workspace/branch check + test-first + minimal-diff +
  own minimal verification + failed-fix invalidation + the 3-failed-fix-attempts gate + the >5-file
  blast-radius FLAG + conditional defense-in-depth).
- `references/pattern-taxonomy.md` — gstack's 6 bug signatures + the infiquetra serverless addition with
  a symptom→suspect map, and the anti-patterns catalog (shotgun debugging, confirmation bias, "it works
  now move on", prediction quality bad-vs-good, rationalization-spiral red flags).
- `references/debug-report.md` — the DEBUG REPORT template (the gstack enum'd shape), the journal-
  LEARNINGS promotion template, and the `mission-control` defect-routing note (report = evidence, fix reaches
  `/work` via a `mission-control` ISSUE, never via the report path through the classifier).
- `../../references/operator-choice.md` — the execution-backend contract; one value, `inline`,
  since issue #1030 archived the others.
- `../brainstorm/SKILL.md` — the canonical channel-inline convention (cite, never duplicate).
- `../../references/saga-spec.md` — the saga contract (`restore` / `ticks`; `/investigate` is read-only).
