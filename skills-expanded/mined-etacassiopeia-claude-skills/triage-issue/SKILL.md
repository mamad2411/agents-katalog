---
name: triage-issue
description: "Pre-flight for /fix-issue — read a GitHub issue and return two verdicts: whether it *should* be built (build / question-design / rejected-by-design), and which top-level model to launch /fix-issue on (Opus default, Fable for design-heavy, Sonnet for trivial). Cheap; run it BEFORE /fix-issue. Usage: /triage-issue <github-issue-number>"
user_invocable: true
argument-hint: "<issue-number>"
allowed-tools:
  - Bash(gh issue view:*)
  - Bash(git remote get-url:*)
  - Bash(ls:*)
  - Bash(git grep:*)
---

## Live Context (loaded at invocation)

- **Issue**: !`gh issue view "$ARGUMENTS" --json number,title,body,labels,comments 2>/dev/null`
- **Repo remote**: !`git remote get-url origin 2>/dev/null`
- **Project type**: !`ls Cargo.toml build.sbt package.json go.mod pyproject.toml 2>/dev/null || true`

---

# Triage Issue — Pre-Flight for /fix-issue

This skill returns **two verdicts**, in this order:

1. **Desirability** — *should this be built at all?* (Step 2)
2. **Model** — *if so, which top-level model builds it?* (Step 3)

The order matters: if an issue should not exist, which model implements it is a moot question, and
answering it anyway is how a wrong feature acquires momentum.

**Why the model verdict exists:** `/fix-issue` runs its whole main loop (design the gate,
write/integrate code, diagnose, triage, fix) on whatever top-level model you launched it on, and a
skill cannot change the top-level model mid-run. So the model choice must be made *before* launch.

**Why the desirability verdict exists:** without it, nothing in the `/fix-issue` → `/ship-issues`
pipeline ever asks whether a change *should* exist. Implementability and model routing are both
"can" questions. An issue can be well-specified, factually accurate in every claim, and still
describe something that should not be built — and it will then pass every gate and merge.

This is not hypothetical. `achird-labs/rift-cluster` #365 and #366 each specified a console panel
against machinery that was described **correctly**: the APIs named existed, the constraints cited
were real, the missing endpoints were genuinely missing. Both were rejected outright once a human
was asked, because the console must not change cluster membership or trigger the cluster's own
maintenance. A third, #359, had the same shape. Verifying facts does not verify intent.

Both verdicts are intentionally cheap: a short read, no worktree, no agents, no code. Run on any
model (even Haiku).

**The model recommendation picks the top-level model only.** `/fix-issue` already pins its
sub-agents (review → opus/sonnet, simplify/exploration → haiku, optional implementation → sonnet),
so this choice does not cascade into them.

---

## Step 1 — Read the issue

From the Live Context, extract: the stated **goal**, whether **acceptance criteria** are given
or must be derived, the **proposed solution shape** (is an exact API/spec supplied, or just a
problem?), and the **blast radius** (how many files/subsystems, new abstraction vs. localized
edit). If the body is thin, do ONE cheap `git grep` for the central symbol to gauge blast radius
— do not open a worktree or read broadly. This is a 30-second read, not Phase 2 of `/fix-issue`.

---

## Step 2 — Desirability: should this exist?

Ask this **before** touching the model rubric, and answer it about the issue's *intent*, not its
accuracy. The trap this step exists to catch is an issue whose every factual claim is true.

**Start from the right question.** An issue that says *"there is no route for X"*, *"X is not
reachable"*, or *"nothing exposes X"* has stated a **can**-fact and is using it as a **should**-
argument. Those are different claims. Re-read such an issue as: *given that X is absent — should it
be present?*

### Signals that a should-question is open

Any one of these is enough to stop and name it. They are heuristics for "a human's intent is load-
bearing here", not proof of a problem.

- **New capability, not a defect fix.** Bugs rarely raise should-questions — the desired behaviour
  is already agreed. New surface almost always does.
- **A new entry point into something with a trust or safety boundary**: cluster membership,
  authentication, admission, credentials, deletion, billing, anything that writes to a replicated
  or audited log. A second way in is a security question even when each way is individually sound.
- **It duplicates something the system already does automatically.** If the machinery already runs
  on its own, an operator control for it is at best redundant and at worst a way to break an
  invariant the automation maintains.
- **It moves an operation from lifecycle-driven or automated to human-triggered.** That is a change
  in operational posture, not a feature.
- **It descends from a design mockup, sketch, or prototype** rather than an observed need. Mockups
  describe a product; a product can be wrong. Treat a panel/screen/flow "the design draws" as a
  proposal, not a requirement.
- **It contradicts, or sits awkwardly beside, a principle already recorded** in the repo.

### Check the record before deciding

Cheap and usually decisive — the repo often already answers this. One or two `git grep`s over
design docs, ADRs/RFCs, and `CONTRIBUTING`-style files for the concept at issue:

```sh
git grep -il "<concept>" -- docs/ ADR* RFC* CONTRIBUTING*
```

Look specifically for a **"do not rebuild this"** section, a prior rejected issue, or a stated
invariant. If a recorded principle already settles it, say so and cite the file — that is the
difference between a verdict and an opinion.

**What counts as settling it, and what does not.** A *decision* settles it: a design doc or ADR that
states the intent, an explicit prior human approval, a documented invariant. **Existing partial
implementation does not.** A stub, a pending panel, a parameter the client already sends, a flag
documented as "awaiting backend" — these record that someone *started*, not that anyone *decided*.
Treating them as settlement is the same can/should confusion in a different costume, and it is the
one this step is most likely to fall for, because half-built scaffolding looks like consensus.

The console panels in `rift-cluster` #365/#366 were exactly this: drawn, wired to a `PendingPanel`,
their reasoning written out in the source — and wrong. If the only evidence that a thing should
exist is that part of it already does, the should-question is still open.

**An issue's own `## Should this exist?` section is an input, not a verdict.** `file-finding` asks
the agent filing a finding to mark the question `SETTLED` (with a citation) or `OPEN`. `OPEN` is
reliable — take it and go. `SETTLED` is a *claim*: follow the citation and judge it by the paragraph
above. A filer citing a stub, a mockup or a half-built panel has recorded the same can/should
confusion in a more confident voice, and confidence is not evidence.

### The three outcomes

| Verdict | When | What the caller does |
|---|---|---|
| **`build`** | No should-signal fires, or one fires and the record already settles it in favour | Proceed to Step 3 |
| **`question-design`** | A should-signal fires and nothing in the record settles it | **Do not implement.** Put the question to a human, in one sentence, before any code |
| **`rejected-by-design`** | It contradicts a recorded principle, or a human has already refused this shape | **Do not implement.** Recommend closing as *not planned*; if the repo has advertised the capability (a pending panel, a stub, a doc promise), recommend removing that too |

**Default to `build`.** This step is a tripwire, not a gate to argue past — most issues are fine and
should pass without ceremony. A `question-design` costs one sentence to a human; getting it wrong in
the other direction costs a merged feature that has to be removed later, plus whatever was built on
top of it in the meantime.

**Be specific or say nothing.** A `question-design` verdict must name the actual fork in one
sentence a human can answer yes/no to — *"should an operator be able to admit a node from the
console, or only by starting one?"* Vague unease ("this feels risky") is not a verdict; if you
cannot phrase the question, return `build`.

**Desirability is independent of quality.** A well-written, well-specified, correctly-researched
issue can be `rejected-by-design`, and a vague one can be `build`. Do not let the issue's polish
influence this verdict — that correlation is exactly what made #365/#366 slip through.

---

## Step 3 — Score against the rubric

Evaluate the three tiers **top-down**; take the first that matches.

### → Fable (design-first) — if ANY strong design signal is present
The deliverable is a *decision*, not just code; the main loop's own reasoning is the value.
- Acceptance criteria are absent or ambiguous — the issue states a **problem**, not a solution.
- **Multiple viable approaches with real trade-offs** (performance vs. faithfulness, simplicity
  vs. generality) and no clear winner — the #313 LocalSequencer "zero-overhead hybrid vs. literal
  spec" fork is the canonical case.
- Introduces a **new public abstraction / trait / API whose shape is a judgment call**, not
  dictated by the issue.
- **Cross-cutting**: changes a core data structure or ripples through many modules/signatures.
- An explicit **constraint in tension** ("no regression budget", strict back-compat, invariant
  preservation) that forces a design choice.
- Language like *redesign / rethink / architecture / how should we…*.

### → Sonnet (trivial) — only if ALL mechanical signals hold
- A **verbatim spec or exact API** is supplied (the issue hands you the signatures), OR it is a
  **bug with a clear repro and a stated fix direction**.
- **Localized**: one or two files, a clear target, no new abstraction.
- No cross-cutting change, no open design question.
- (#314 — full trait spec given — and #308 — bug with repro + fix direction — sit at the
  Sonnet/Opus boundary; when in doubt between these two, pick Opus.)

### → Opus (default) — everything else
Real implementation with non-trivial logic, moderate scope, or careful verification needed, but
the **goal and approach are clear enough** that no upfront design decision is required. This is
the common case; when a signal is genuinely borderline, prefer Opus over Fable (don't pay the
Fable premium unless a design decision is actually open) and prefer Opus over Sonnet (don't
under-power real logic).

---

## Step 4 — Output the verdict

### When desirability is `build`

```
## Triage: Issue #<N> — <title>

**Desirability: build** — <one line: no should-signal, or which signal fired and what settled it>

**Recommended top-level model: <Opus | Fable | Sonnet>**

Why:
- <signal 1, citing a specific from THIS issue — e.g. "exact RequestJournal API supplied → mechanical">
- <signal 2>
- <the deciding factor, if it was close>

Scope: <1-line blast-radius read — files/subsystems, new abstraction? y/n>
Open design question: <the fork the main loop must resolve, or "none — approach is dictated">

### Next step
Set the model (/model → <model>), then run:  /fix-issue <N>
```

### When desirability is `question-design` or `rejected-by-design`

Stop at the desirability verdict — **do not** also emit a model recommendation. Naming a model
implies the thing is going to be built, which is the impression this verdict exists to prevent.

```
## Triage: Issue #<N> — <title>

**Desirability: <question-design | rejected-by-design>**

The should-question: <ONE sentence a human can answer yes/no to>

Why it fires:
- <the signal, citing this issue — e.g. "adds a second admission path into replicated membership">
- <the recorded principle and where, if any — e.g. "docs/design/console/README.md says do not rebuild this">

What IS true: <briefly grant the issue's accurate claims, so the reader can see this is not a
factual objection — this is the part that stops the verdict being re-litigated>

### Next step
Do not run /fix-issue. Put the should-question to a human.
[rejected-by-design only] Recommend: close as *not planned*, and remove anything already
advertising the capability (<pending panel / stub / doc promise, if any>).
```

Keep it to that block. Do not start implementing, do not create a worktree, do not spawn agents
— this is advice only. If the issue number was invalid or the body empty, say so and stop.

---

## Notes

- **The two verdicts are independent.** `rejected-by-design` is not "too hard" and
  `question-design` is not "underspecified" — an issue can be perfectly specified and still be
  either. Likewise `build` says nothing about difficulty; that is the model verdict's job.
- **`question-design` vs. the model rubric's Fable signal.** They look similar and are not the same.
  Fable means *we should build this and the approach is an open decision*. `question-design` means
  *we have not established we should build this at all*. Fable is answered by the implementing
  model; `question-design` is answered by a person. When both seem to apply, desirability wins —
  it is upstream.
- **Do not use `rejected-by-design` to express disagreement.** It is for a contradiction with a
  *recorded* principle or an explicit prior human refusal. If the principle lives only in your
  judgement, that is `question-design`.
- **Bias:** Opus is the floor for real work; reserve Fable for a genuinely *open* design decision,
  not merely a "hard" implementation (hard-but-clear is Opus). Sonnet only for genuinely trivial,
  fully-specified work.
- If the issue bundles both a design fork AND mechanical follow-through, recommend **Fable** — the
  design decision gates everything downstream, and you can't upgrade the top-level model mid-loop.
- This mirrors the model policy documented in `/fix-issue`'s SKILL.md; keep the two in sync.
