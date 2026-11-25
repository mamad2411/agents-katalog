---
name: simulate-newcomer-first-run
description: >-
  Load this skill to find out whether a stranger can get from "just arrived" to a first success
  alone (install, setup, onboarding), using cold persona subagents. Trigger on "can a new user
  figure this out", "test the onboarding", "try this with fresh eyes".
disable-model-invocation: false
user-invocable: true
effort: high
compatibility: >-
  Requires whatever the target project's own first-run steps need - `uv`, `npm`, `docker`, a
  database - none of which this skill assumes is installed; a missing prerequisite is itself an
  audit finding. Running personas in parallel additionally needs the git CLI for `git worktree
  add`, or a container runtime, to isolate each walker.
license: Apache-2.0
---

# Simulate a newcomer's first run

The question is not "is this documented". It is **"can someone who knows nothing reach a first
success using only what we actually gave them"** — and the only honest way to answer it is to hand
the artifacts to a reader with no context and watch where they stop.

You cannot run this audit on yourself. You already know the answers, and every gap you would hit
gets silently bridged by what you know. The whole procedure below exists to buy back that ignorance
by putting the walk in cold subagents and constraining what they are allowed to know.

## Procedure

### 1. Write the success goal, the milestones, and the budget

**The goal.** One sentence, observable, in the user's words. Not "the app is installed" — **"they
can see their own data on a page they navigated to themselves"**.

If you cannot state the goal, stop: the audit has no pass condition and every finding will be
arguable.

**The milestones.** Break the goal into two to four ordered, observable checkpoints — the first is
usually the cheapest thing that proves the product is real ("the command runs and prints its
version"), the last is the goal itself. A walk that dies at milestone 2 of 3 tells you where the
cliff is; a bare `reached goal: no` does not.

**The budget.** Give each milestone a maximum number of walker **actions** before dispatching.
Declared up front it is a prediction; declared afterwards it is a rationalization, so write it
first. If you have no basis for a number, **count the steps the documentation itself prescribes and
use that as the budget** — a walker needing materially more actions than the doc's own step count
means the doc omits steps that reality requires, and that gap is the finding.

|                  | Example                                                                  |
| ---------------- | ------------------------------------------------------------------------ |
| Goal             | They see their own booking listed on a page they navigated to themselves |
| M1 (≤ 4 actions) | The install command completes and `myapp --version` prints               |
| M2 (≤ 6 actions) | They are signed in and looking at an empty bookings list                 |
| M3 (≤ 5 actions) | Their first booking appears in that list                                 |

### 2. Declare the audience baseline

**Name what the intended audience already knows before this product.** One line, and it is
load-bearing: without it "assume no prior knowledge" collapses into a walker that stalls on "clone",
"terminal", or "browser tab" and reports a Blocker on every target that has ever existed.

> Baseline: a developer who has used a terminal and git, but has never seen this tool or its domain.

> Baseline: someone who can use a browser and has an email account. No developer knowledge.

Everything **inside** the baseline is free — the walker may use it without counting it as an external
lookup. Everything **outside** it must be on the surface or it is a stall. The baseline is the
audience _the product claims_, not the audience it wishes it had: if the README says "for data
scientists", you may not quietly widen it to "anyone" to manufacture findings, and you may not
quietly narrow it to "our team" to excuse them.

Record the baseline verbatim in the report. Two audits of the same target under different baselines
are not comparable, and a reader cannot judge a finding without it.

### 3. Freeze the artifact set

List **exactly** what a newcomer has, and nothing else. Everything after this step is only as honest as this list.

| Surface        | Typical frozen set                                                                                 |
| -------------- | -------------------------------------------------------------------------------------------------- |
| Repo / library | `README.md`, the landing section of the docs site, `--help`, the install command, the package page |
| Web app        | The public landing page, the sign-up flow, in-product empty states, whatever the email says        |
| CLI            | `--help`, `<cmd> help`, the man page, the README quickstart                                        |
| Internal tool  | The wiki page the newcomer was sent, plus the tool itself                                          |

Record the list verbatim in the report. **Source code is not in the frozen set** unless the target's
audience is people reading the source. Neither is anything you explained in this conversation, an
issue thread, or a commit message.

**For a library, CLI, or API, the last milestone is the first real call**: the smallest program or
command a developer would write from the docs, returning the documented result. Tell the walker to
copy every code block on its path verbatim, with no edits, and to report each one whose output,
error, or required setup differs from what the doc shows. A sample that only works after the walker
fixes it is a stall, because a newcomer who pastes it gets the error instead.

### 4. Dispatch cold walkers

Spawn one `ceh-usability-audit:newcomer-simulator` agent **per persona** (below). Each gets exactly six
things:

1. The success goal from step 1, **and its milestones with their action budgets**.
2. The audience baseline from step 2, verbatim.
3. The entry point (a path, a URL, a command).
4. Its persona constraint, verbatim.
5. The frozen artifact set, as an explicit allowlist of paths/URLs.
6. Whether it may run state-changing setup commands — see the isolation rule below.

And one hard rule, which the agent restates back: **stop at the first point you cannot proceed
without information that is not in the frozen set, and report exactly where.** Do not infer the
missing step from how tools like this usually work. Do not fix anything.

**Isolation rule — this decides whether the walk is parallel.** Read-only walks run all five walkers
at once; they cannot interfere. But a walk whose first step is `uv sync`, `npm install`, or `docker
compose up` **mutates the checkout every other walker is reading**, and five of those at once
produce five corrupted transcripts and a dirty working tree.

| Walk touches                                                                   | Run                                                                                                                                                        |
| ------------------------------------------------------------------------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Reading files, pages, `--help` only                                            | All personas in parallel                                                                                                                                   |
| Any command that writes to the working tree, a lockfile, a database, or a port | One persona at a time, **or** give each walker its own copy of the target (`git worktree add`, a scratch clone, a container) — and say which in the report |

Deciding this is your job, not the walker's: it only knows what you told it it may run.

Browser caveat: **subagents lose the Chrome tools** (background subagents keep a reduced tool set).
For a live web UI, run the walk yourself in the main session, holding one persona at a time and
narrating the stall points into the same format — or hand the walker screenshots and page text
instead of a URL.

#### The personas

Read `${CLAUDE_PLUGIN_ROOT}/references/personas-and-severity.md` before dispatching. It holds the
five personas, each a constraint catching a distinct failure class, and the severity scale step 5
ranks with. Run all five unless a surface makes one meaningless (`Small Screen` on a library API);
skipping one is recorded as a skip, not omitted.

### 5. Score by observed outcome, not by appearance

Severity comes from what actually happened to a walker, never from how bad something looks to
you, so the report records observed outcomes instead of the auditor's preferences. Assign each stall one of the four
severities (Blocker, Detour, Friction, Polish) by the conditions in
`${CLAUDE_PLUGIN_ROOT}/references/personas-and-severity.md`.

Anything you noticed but no walker stalled on is **not a finding**. It goes in a separate
`Hypotheses` list, unranked, and never counts against the gate. Three measurements make the ranking
reproducible:

- **Actions per milestone** — discrete steps taken, counted against the budget declared in step 1.
- **External lookups** — times a walker needed something outside the frozen set _and_ outside the
  audience baseline. Any count above zero is a Detour by definition, and the missing information
  names its own fix.
- **Machine wait** — real seconds spent waiting on the product (install, build, first response).

A run that ends because the walker exhausted its turns is **not a result**. It is an instrument
failure, and it is never a Blocker — only a stall the walker actually reported is a finding.
Re-dispatch it over a **narrower goal** (one milestone per walker, chained), since the agent's turn
ceiling is fixed in its frontmatter and a caller cannot raise it for one dispatch.

#### The budget — how long "too long" is

Without an upper bound, a README that takes forty steps passes as long as nobody stalls outright.
But **length is itself a usability failure**, and the most common one after an outright blocker.
The budget from step 1 is what makes it measurable.

**Walker wall-clock is meaningless — do not record it.** How long the agent took is a fact about
model throughput, not about your product. Two numbers are meaningful and both go in the report:

1. **Actions against budget**, per milestone. This is the evidence. It is reproducible, it is a
   property of the design, and it does not move when the model changes.
2. **Machine wait**, measured for real. The seconds a human genuinely spends staring at `Installing
dependencies…` are the product's property, not the walker's — record them with `time` and put
   them in the report unchanged.

Then translate actions into human minutes with a **fixed, stated cost model**, so the number is
reproducible and arguable rather than invented:

| Action class                                                                 | Newcomer cost                    |
| ---------------------------------------------------------------------------- | -------------------------------- |
| Read a short paragraph, a label, or one line of output                       | 15s                              |
| Read and choose between two plausible options                                | 30s                              |
| Type or paste a command; fill one field                                      | 20s                              |
| Navigate and re-orient on a new screen                                       | 30s                              |
| Find something not where it was expected (a stall the walker recovered from) | 60s                              |
| Create an account or verify an email                                         | 90s                              |
| Machine wait                                                                 | the measured seconds, unmodelled |

**Report it as `estimated ~N min (model, not measured)` with the action count beside it.** The
action count is the evidence; the minutes are a translation for whoever has to care about the
number. Never write it as an observation, and never write "users take N minutes".

Overrun feeds the existing severities — it does not add a new axis:

| Overrun                                        | Severity                                                     |
| ---------------------------------------------- | ------------------------------------------------------------ |
| Within budget                                  | not a finding                                                |
| Over budget, milestone still reached           | **Detour** — name the steps that were not in the doc's count |
| Over 2× budget, or a milestone missed entirely | **Blocker**                                                  |

If you set a budget you cannot defend, say so and mark criterion 5 N/A rather than tuning the
budget after the walk to make it pass. A budget revised upward to fit the result measures nothing.

### 6. Report

Write the report described under Output, with the raw walker transcripts beside it.

### 7. Loop

Fix the **top Blocker only**, then re-run **only the personas that stalled on it**. A full re-run
after every edit is waste, and re-running a persona that already passed tells you nothing.

Repeat until the gate reads 5/5: the gate is the done condition. A user who is present may still
stop the loop early or accept a lower score; record that in the report. Report the gate honestly at
every iteration
— a 3/5 that is stated is worth more than a 5/5 that was argued into place.

## Rules

### Honest limits — state these in the report

An LLM playing a novice is a proxy, not a user test. It **reliably** catches undefined jargon,
missing prerequisites, steps that reference things that do not exist yet, dead ends, silent
failures, and unlabeled destructive actions. It **cannot** measure motor precision, reading fluency,
patience, or emotional response. Never write "validated with users" — write "walked cold by N
persona-constrained agents".

### The gate

| #   | Criterion                                                                                                                         |
| --- | --------------------------------------------------------------------------------------------------------------------------------- |
| 1   | Every persona that was run reached the goal — on a completed walk, not one that ran out of turns                                  |
| 2   | Zero open Blockers                                                                                                                |
| 3   | No step required knowledge outside the frozen set _or_ the declared audience baseline — every walker's external-lookup count is 0 |
| 4   | Every destructive or irreversible step states its consequence _before_ the action and names an undo                               |
| 5   | Every persona reached every milestone within its declared action budget — or each overrun is a recorded finding                   |

A criterion that cannot be measured on this target is marked **N/A with a reason** and the gate is
reported out of the remaining count (`4/4, 1 N/A`). Never quietly score an unmeasured criterion as
passing.

## Output

Write `.agents_workspace/ux-audits/<target>/run-<NNN>/UX_AUDIT.md`, where `<NNN>` is a zero-padded
sequential run index so a re-run never overwrites a prior run's evidence. Create missing parents.
Keep raw walker transcripts in that run folder — a finding without its transcript is an opinion.

```markdown
# First-Run Walkthrough — <target>

**Goal:** <the one sentence from step 1>
**Milestones & budget:** <M1 ≤ n actions; M2 ≤ n; M3 ≤ n>
**Audience baseline:** <verbatim from step 2>
**Frozen set:** <verbatim list>
**Walkers:** <personas run> (<personas skipped, and why>) — run <in parallel | serially | in isolated copies>
**Method:** cold persona-constrained subagents — proxy for a user test, not a user test
**Gate:** <N>/5

## Results

| Persona | Furthest milestone | Stop reason | Actions vs budget | External lookups | Machine wait | First stall |
| ------- | ------------------ | ----------- | ----------------- | ---------------- | ------------ | ----------- |

**Estimated newcomer time to goal:** ~<N> min (cost model, not measured) + <N>s machine wait

## Findings

### <ID> — <Blocker|Detour|Friction|Polish> — <one-line title>

- **Where:** <file:line, screen, or command>
- **Persona:** <who stalled>
- **Expected / got:** <what they thought would happen / what happened>
- **Missing knowledge:** <the fact they needed and did not have>
- **Fix:** <the concrete change>

## Hypotheses (no walker stalled — unranked)

## Not covered

<what this method cannot measure; what was delegated to accessibility>
```

## Stop conditions

- **The frozen set cannot be established** — nobody can say what a newcomer actually receives → ask;
  guessing invalidates every finding downstream.
- **The target needs credentials, payment, or a live account** to reach the goal → report the walk
  up to that boundary and say plainly that the rest is unwalked. Never invent test credentials.
- **A walker's fix requires a product decision** (removing a feature, changing what the thing is
  for) → report it; do not decide it.

## Hands off to

- They got in — is the interface itself usable? `ceh-usability-audit:audit-interface`.
- The stall was an error message: `ceh-usability-audit:audit-error-messages`.
- The stall was wording: `ceh-usability-audit:write-plain-language`.
- The stall was a missing or incorrect doc: `ceh-documentation:write-guides-and-runbooks`, or
  `ceh-git-workflow:update-readme` for the README.
- The project has no docs set at all: `ceh-documentation:write-project-docs`.
- The stall was keyboard, contrast, or screen-reader: `ceh-web-frontend:make-ui-accessible`.
- The README's first screen does not say what this is: `ceh-seo:write-project-listing-text`.
