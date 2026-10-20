---
name: team-build
description: 'Run a virtual engineering team (build-triage, build-planner, test-author, implementer, verifier, reviewer, build-lead) over an approved plan to actually BUILD it — on any project. Use when: a team-intake technical-plan and a team-qa test-plan exist and the work now needs to be implemented; you want code written test-first and proven red→green before it is declared done; you have an approved change to build and want it built without re-litigating the design; or a project has its own recurring-defect catalog and you want any durable structural cure actually applied instead of an inline shortcut. Produces a reviewable green diff in an isolated per-effort git worktree plus a build-report, and remembers when a build re-takes a shortcut so the team stops shipping the same regression — when the project has a defect catalog configured to remember it in.'
---

# Team Build

**Argument:** path to the completed intake folder (the one holding
`intake/.../technical-plan.md` and `qa/.../test-plan.md`). A `build/`
subfolder is created inside it for the build artifacts. If not given, ask for
it (see Step 0).

Runs a small **virtual engineering team** over an *already-approved* plan and
actually implements it. It is the third team in the trilogy — it closes the
loop:

- **`team-intake`** plans *what to change* → `technical-plan.md`.
- **`team-qa`** plans *what tests must go red-then-green* → `test-plan.md`.
- **`team-build`** writes those tests, implements to green, and **proves it** →
  a reviewable diff in an isolated worktree + **`build-report.md`** (the doc
  the user reads).

It exists because the build step is the one place a project's chronic
regressions are actually *introduced or prevented*: a durable cure gets
applied or someone takes the inline shortcut and ships green-but-broken. This
team is built to make any known cure **non-skippable when a project has one
configured** — the planner marks it mandatory, the implementer is forbidden
the shortcut, the verifier won't sign off without the guard, and the reviewer
adversarially hunts for exactly those traps. Everything project-specific (a
recurring-defect catalog, repo conventions) is optional and loaded from that
project's own `PROJECT-CONTEXT.md` if it has one — this team runs generically,
just without those extra guardrails, on a project that doesn't.

Unlike `team-intake` and `team-qa` — read-only planners that fan out four
agents in parallel — **`team-build` mutates product code**, and its core is a
**sequential red-first loop, not a fan-out**. This is an **orchestration**: you
(the main agent) run the phases below and delegate each role to a subagent.
You are the build lead.

> **This team is destructive by design — it edits a working tree in place.**
> That tree is an **isolated per-effort git worktree** (one checkout per repo
> the plan touches, on its own branch — see `build-triage`), never the single
> shared checkout, so two builds running around the same time can't blend into
> each other's uncommitted work. The first agent provisions that worktree set
> (+ a namespaced Docker stack, if the project has one) and records the
> starting commit(s) so the whole run stays a reviewable diff with a
> one-command back-out per repo. It **stops at green + report**: it does NOT
> commit, push, or open a PR, and it does NOT tear the worktree/stack down.
> Those are the user's call.

## The team (first-class subagents, installed at `~/.gemini/config/plugins/delivery-team/agents/`)
| Agent | Role |
|-------|------|
| `build-triage` | Confirm the two plans exist + are buildable; discover the project's repo layout; provision an isolated per-effort git worktree set + namespaced Docker stack (if the project has one); gate on a clean tree per repo; record the starting commit(s); write the build brief |
| `build-planner` | Turn technical-plan + test-plan into one ordered, dependency-correct task list; mark any project-specific **durable-cure** steps MANDATORY |
| `build-test-author` | Write the test-plan's tests and **prove each RED** before any product code changes |
| `build-implementer` | Apply the change set to GREEN, applying any MANDATORY durable cure — **no inline shortcuts** |
| `build-verifier` | Run all relevant suites, prove red→green per test, run the DoD checklist + any project-specific standing guards; gate |
| `build-reviewer` | Adversarial diff review against this project's known traps (if it has a defect catalog) plus ordinary correctness/simplification |
| `build-lead` | Sequence/reconcile the loop, write `build-report.md`, update build memory + this project's defect catalog if it has one |

> **Path note (plugin install):** this file was written assuming a standalone
> install (`~/.gemini/config/plugins/delivery-team/skills/team-build/` + `~/.gemini/config/plugins/delivery-team/agents/`). If
> you installed this as a plugin instead, every
> `~/.gemini/config/plugins/delivery-team/skills/team-build/...` path below means "the same-named
> folder bundled alongside this `SKILL.md`", and each agent under
> `~/.gemini/config/plugins/delivery-team/agents/<name>/agent.md` means "the matching agent folder in
> this plugin's own `agents/` folder" — same relative layout, different root.

> **How to invoke each role:** these are registered subagents. Delegate to one
> either by explicit mention — `@build-implementer <task>` — or by letting
> automatic delegation match the task to the subagent's `description` field.
> Always give the agent: the `build-brief.md` path, the output dir, the paths
> to `technical-plan.md` and `test-plan.md`, and (once known) the ordered task
> list. (If a subagent by that name isn't available, fall back to a plain
> instruction and paste the role brief from `~/.gemini/config/plugins/delivery-team/agents/<name>/agent.md`
> directly into the request.)

## Process

### Step 0 — Get the approved plans and the output location
team-build needs **the technical-plan** (what to build) and **the test-plan**
(what to prove). Both normally live inside a completed intake folder:
- If the user gave a path to a completed intake folder, use it. The plans are
  at `<intake-dir>/intake/.../technical-plan.md` and
  `<intake-dir>/qa/.../test-plan.md` (or directly inside it). Locate both.
- **If nothing was given, STOP and ask:** "Point me at the completed intake
  folder — the one holding the `technical-plan.md` and the `test-plan.md`.
  I'll build it in an isolated worktree and write the build report next to
  them."
- **If only the technical-plan exists (no test-plan), STOP and ask** whether
  to run `team-qa` first. Strict red-first TDD needs the test-plan; do not
  build blind.
- Do not invent a plan or a location.

**Output location:** write under `<intake-dir>/build/<YYYY-MM-DD>-<slug>/`
(reuse the intake slug; create a `supporting/` subfolder). Use today's date.
**Never write build artifacts to a repo root.**

### Step 0.5 — Version bump check (only if the project has one)
Check whether this project has a version-bump convention — `PROJECT-CONTEXT.md`
names it if so. **If it does, always ask the user whether to bump before this
build starts** — every time, regardless of whether a bump already happened
earlier in the same session, and regardless of how obviously due a bump seems.
This is a standing rule for any project with a configured bump mechanism, not
a judgment call to skip.
- Ask the user directly: "Should we bump the version before building?" with
  options along the lines of *not yet* / *bump now (build/patch/minor/major)*
  / *no bump needed for this change*.
- Follow the mechanism `PROJECT-CONTEXT.md` names exactly (script, files it
  updates, commit convention).
- If the project has **no** version-bump convention configured, skip this step
  entirely — don't invent one.
- If the user says not yet / no bump needed, proceed straight to Step 1.

### Step 1 — Triage + safety gate (gate)
Run `build-triage`. It confirms both plans are present and buildable,
discovers the project's repo layout (checking `PROJECT-CONTEXT.md` first, else
discovering it), **provisions a per-effort worktree for every repo in that
layout** (new branch off its base branch for repos the plan touches,
base-branch HEAD for untouched ones), generates a namespaced Docker compose
stack if the project has one, **confirms each worktree is clean**, records the
**starting commit per repo**, registers the effort if this project has a
registry configured, writes `build-brief.md`, and returns a `READY` /
`BLOCKED` verdict.
- If **BLOCKED** — a plan is missing/incomplete, or **a worktree is dirty** —
  surface it to the user directly and wait. A dirty worktree is a hard gate:
  do not blend the build into uncommitted work. Offer to stash/commit first or
  proceed on a named clean base.
- **Log every clarifying/blocking question and its answer** (see "Decision
  logging").

### Step 2 — Plan the build
Run `build-planner`. It reads `technical-plan.md` + `test-plan.md` + the brief
and writes `build-task-list.md`: one **ordered, dependency-correct** task list,
with each step independently checkable. It marks every **durable-cure** step
this project's defect catalog (if configured) calls for as **MANDATORY — not
optional**, citing the catalog id. Capture the ordered list — the next steps
follow it.

### Step 3 — Author the tests, red-first (gate)
Run `build-test-author`. It writes the tests named in `test-plan.md`, runs
them, and **proves each one RED** against the current (unbuilt) code in this
effort's worktree, recording the exact failing output. It changes test files
only — **no product code**.
- If a test that should be red passes green already, that's a signal the plan
  is wrong or the behavior already exists — **surface it and pause**; do not
  paper over it. A test that can't be made red can't prove the fix.

### Step 4 — Implement to green (sequential)
Run `build-implementer`. It works `build-task-list.md` **in order**, applying
the change set from `technical-plan.md` to make the red tests pass, inside
this effort's worktree. Hard rules it carries:
- Apply any structural cure the plan marked MANDATORY; do not substitute an
  inline patch.
- One implementer, sequential — no parallel edits to the same files.
- Keep changes scoped to the task list; if it discovers the plan is wrong
  mid-build, it stops and reports rather than improvising a different design.

### Step 5 — Verify (gate)
Run `build-verifier`. It brings up this effort's own isolated Docker stack (if
the project has one and the plan's scope needs it), runs the **full relevant
suites**, confirms **each new test went red→green**, and runs the Definition
of Done from the plans plus any standing guards this project's defect catalog
calls for. It records the green evidence.
- If anything is **red** or a **DoD item fails**, loop back to **Step 4**
  (implementer fixes), bounded — after ~3 fix attempts without convergence,
  stop and report to the user rather than thrashing. Never edit a test to make
  it pass.

### Step 6 — Adversarial review
Run `build-reviewer`. It reviews the **diff since the starting commit**, per
touched repo, against this project's known traps (if it has a defect catalog
configured) plus ordinary correctness/simplification. A real defect loops back
to **Step 4**.

### Step 7 — Synthesize + report
Run `build-lead`. It writes `build-report.md`, updates the build run-log, and
— if the build had to re-apply a known cure, took (or was tempted to take) a
shortcut, or exposed a new repeatable build trap, and this project has a
defect catalog configured — updates it. If you have a cross-project time/cost
ledger skill installed and configured, `build-lead` may also refresh it and
flag that a dashboard needs republishing (it can't publish it itself — it only
touches files on disk). Capture its headline, including that flag.

### Step 7.5 — Republish a time-ledger dashboard, if you have one and it was flagged
This step only applies if your own setup includes a time-ledger dashboard
skill. If `build-lead` reports the ledger was refreshed, republish the
dashboard yourself (however your setup serves it — e.g. re-running its own
publish step) **at its existing URL/location** (do not mint a new one) — this
is the one step in team-build only the orchestrator (you) can do; `build-lead`
updates the files, you publish them. Skip silently if `build-lead` flagged the
refresh as failed/skipped/not-installed, or if you don't have this integration
at all — non-blocking, don't hold up the build report over it.

### Step 8 — Report back (stop at green)
Summarize for the user in chat:
- **What was built** and the **change verdict** (GREEN / GREEN-WITH-CAVEATS /
  BLOCKED).
- **Red→green evidence** — the new tests, observed red-before / green-after.
- **DoD checklist status** + whether any durable cure was applied or deferred.
- **Where the diff lives** (this effort's worktree paths — not any shared
  checkout) and the **one-command back-out per repo**
  (`git -C <worktree-path> reset --hard <starting-commit>`).
- Any **PENDING / PARKED decisions** still open (from `decisions.md`).
- Links to `build-report.md`, `build-task-list.md`, and `decisions.md`.
- Confirmation the time-ledger dashboard was republished (or why it wasn't).
Then **stop** — do not commit, push, or open a PR. Ask whether the user wants
to commit or hand it back for changes.

> **After the release ships:** when this build (and any others) are committed
> and a version is cut, run **`team-release`** to produce client-facing
> release notes bundling everything in the version, fact-checked against the
> actual shipped commits. That is the outward-facing end of the pipeline;
> team-build stays internal.

## Decision logging
Whenever a clarifying or blocking question goes to the user — at the Step 1
gate, a red-that-came-up-green at Step 3, a non-converging fix loop at Step 5,
or anywhere a decision is genuinely the user's to make — record it so the team
keeps a readable history. Two places:
1. **Per build:** `<output-dir>/decisions.md` (from `templates/decision-log.md`)
   — the full readable record: the question, "where we're coming from" (dated
   context), the options, and the decision. Mirror how it's presented in chat.
2. **Global:** the build run-log captures the run; if a decision maps to an
   entry in this project's defect catalog (if configured), note the reference
   there.

Write the entry as `PENDING` *before* asking; flip to `DECIDED` (or `PARKED`)
once answered.

## Conventions
- **Version bump: always ask, every time, only if this project has a
  configured mechanism (Step 0.5).** Never decide unilaterally — ask the user,
  even if a bump already happened earlier in the same session.
- **Inputs:** a completed intake folder holding `technical-plan.md` +
  `test-plan.md`; if omitted, the skill asks. Do not build without both.
- **Output per build:** `<intake-dir>/build/<date>-<slug>/` containing
  `build-brief.md`, `build-task-list.md`, `build-report.md`, `decisions.md`,
  and `supporting/*.md` (red/green evidence logs).
- **Templates:** `~/.gemini/config/plugins/delivery-team/skills/team-build/templates/`.
- **Memory:** the build run-log location comes from `PROJECT-CONTEXT.md` if
  the project names one; otherwise falls back to
  `~/.gemini/config/plugins/delivery-team/skills/team-build/memory/build-run-log.md` (a cross-project
  log — less useful than a project-specific one, but available). A project's
  own recurring-defect catalog, if it has one, is **its own** — read it, update
  it when a build re-takes a shortcut or re-applies a cure, never fork it into
  this skill's global memory.
- **This skill mutates a tree in place, sequentially, one implementer, no
  parallel edits to the same files within a build.** It gates on a clean tree
  per repo, records the starting commit(s), builds **strict red-first**, and
  **stops at green + report** — no commit/push/PR, and no automatic teardown
  of the worktree/stack either.
- **Every build runs in its own isolated git worktree set** (+ a namespaced
  Docker stack, if the project has one), provisioned by `build-triage`.
  Teardown is manual, run by whoever merges — never automatic, since an
  unmerged branch is still live work.
- **Repo layout is project-specific — discover it, don't assume one.** Check
  `PROJECT-CONTEXT.md` first; a project may be a single repo or contain
  several independent ones.

## The recurring trap this skill exists to catch
**The build is where a durable cure is applied or skipped.** On any project
with a recurring-defect catalog configured, every chronic regression shipped
because, at build time, someone hand-edited a point-fix instead of the
structural cure the catalog calls for — and the green suite hid it.
team-build must **apply the structural cure the plan specified (when one is
called for), prove every new test red→green, and never declare done on a
green suite that doesn't cover the new surface.** No inline shortcut, no
editing a test to make it pass, no "it's green so it's fine." On a project
with no catalog configured, this team still enforces the general discipline
(red-first, no test-weakening, adversarial review) — just without
project-specific guardrails to check against.
