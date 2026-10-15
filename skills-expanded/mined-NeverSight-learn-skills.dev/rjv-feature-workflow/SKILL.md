---
name: rjv-feature-workflow
description: "Use when starting, scoping, or RESUMING a feature/task — invoke with a feature name ('pick up X', 'where were we', 'what's the status') to hydrate its plan + linked docs and resume. Per-feature plans (.plans/) vs docs as source-of-truth, roadmap contract, reconcile-on-open, Cast section. Multiple features in flight, each independently resumable."
---

# Feature Workflow

Working memory that survives sessions, agents, and parallel features. One
line: **plans hold the work; docs hold the truth.**

- `.plans/<name>.md` = working memory for ONE piece of work. Live,
  brainstorm-friendly, ephemeral. Deleted when shipped.
- `_docs/` = source of truth. How the system works today, third-party API
  behavior, established patterns. Durable, authoritative.
- Plans **link** to docs, never duplicate them. A durable fact discovered
  while working gets **promoted** into `_docs/` before the plan is deleted.
  Never let truth die with the plan.
- A plan is **thin working memory**, not an archive: keep it under **~400
  lines / ~20KB**. It is re-read on every resume — an unbounded plan is a
  recurring token tax that compounds each turn. Over the ceiling means facts
  that belonged in `_docs/` never graduated: promote them and compress (see
  reconcile-on-open, and `rjv-gated-build` §5 for the collapse recipe).

Tool-agnostic: the same files serve Claude Code, Codex, or any agent
(reference this procedure from AGENTS.md so every agent follows it).

## Entry point — invoked with a feature name

When asked to start or resume work on `<feature>` (e.g. "rjv-feature-workflow
risk-profiling", "pick up the bottom-nav work"), hydrate in this order —
do not touch code before step 5:

1. `cat .plans/RESUME.md` — the fixed top-level pointer (see Resume
   mechanism below). It names the active plan(s) and their paths. If a
   feature name was given, take its plan; else take the most-recent
   Active line.
2. `grep -A6 ">>> RESUME HERE <<<" .plans/<name>.md` — land on the exact
   resume block. Then read the whole plan.
3. `_docs/features/<feature>/roadmap.md` — items, statuses, debt. Create
   it if starting something new (and set the item `[in-progress]` linked
   to the plan).
4. Every doc the plan's **Source of Truth** section links.
5. **Run reconcile-on-open** (below). Only then act.
6. Report to the human: current state, drift found, next step about to be
   taken.

## Plan format

```
# Plan: <name>
Status: brainstorm | approved | in-progress | blocked | shipped
Last reconciled: <date> — <matches reality? what drifted?>

## Goal
## Cast               ← who builds this: agents, models, approver (see below)
## Decisions          ← locked choices + why (crystallized brainstorm)
## Open Questions     ← still-live brainstorm (resolve → move to Decisions)
## Current State      ← VERIFIED ground truth now, not assumed
## Next Steps         ← ordered resume point; carries the RESUME HERE block
## Regression Guard   ← how to avoid breaking existing behavior
## Out of Scope
## Source of Truth    ← links to _docs/, API docs, key file:line
```

The **Next Steps** section always contains the literal marker block (see
Resume mechanism):

```
## Next Steps
>>> RESUME HERE <<<
Step: <id> — <status>
Do next: <one imperative — the exact next action>
Must-read first: <file:line, …>
<<< END RESUME >>>
1. …ordered steps after the current one…
```

**Cast section** — the agent lineup is a locked decision, not a
per-session improvisation. Record it at plan creation; every resume
(any agent, any session) reads it and plays its role without
re-negotiating:

```
## Cast
Orchestrator: claude-code @ fable        ← holds this plan, integrates
Author:       claude (main session)      ← or: codex · qwen3.6:35b via rjv-ollama-delegate
Reviewer:     codex via codex:rescue     ← explicit APPROVED gates each step
Subagents:    haiku = sweeps/forwarders · sonnet = routine code
Human gates:  spec sign-off · USER-flagged decisions · live/prod switches
```

Recasting mid-build is allowed but is a logged Decision (with why), not
a drift. If a session starts under a different agent than the Cast
names (e.g. Codex opens a claude-authored plan), it says so and either
plays the role the Cast gives it or asks the human to recast.

Task lists, test cases, data models slot under Next Steps / Current State.
One-line, actionable, agent-register (terse facts, file:line — plans are
agent-read; docs for humans stay prose).

## Reconcile-on-open — never stale

The resume guarantee is a cheap ritual, not "the agent remembers":

```
read plan → VERIFY each "done" claim against real code/db → note drift in
Current State → rewrite Next Steps → stamp Last reconciled →
if over ~400 lines / ~20KB, promote durable facts to _docs/ + compress → then act
```

Never trust a checkbox. A plan whose "done" you haven't verified is a
rumor. **During work**: update the plan in the same turn as the change,
never batched for later. **On stop/handoff**: rewrite the `>>> RESUME
HERE <<<` block AND `.plans/RESUME.md`'s Active line to the exact resume
point; no `done` that isn't.

## Resume mechanism — deterministic, do not reinvent

Two fixed anchors so ANY agent lands on the exact resume point without
guessing or inventing its own convention. **The strings are literal —
never paraphrase them**, or the grep breaks and the mechanism is lost.

**1. `.plans/RESUME.md`** — ONE top-level pointer at a fixed path, read
first on every resume. Names the currently-active plan(s):

```
# RESUME
Active: <feature> → .plans/<name>.md
(one line per concurrently-active plan, most-recently-touched first)
```

**2. The `>>> RESUME HERE <<<` block** — inside each plan's Next Steps,
a greppable landing point:

```
>>> RESUME HERE <<<
Step: <id> — <status>
Do next: <one imperative — the exact next action>
Must-read first: <file:line, …>
<<< END RESUME >>>
```

Mechanical ritual (fixed commands, not judgment):

```
cat .plans/RESUME.md                                 # active plan path(s)
grep -A6 ">>> RESUME HERE <<<" .plans/<name>.md      # land on the block
→ reconcile-on-open (verify done-claims) → act
→ at END of every step: rewrite the block + RESUME.md Active line
```

Why literal markers, not "find the Next Steps section": a fixed string
is a deterministic landing (`grep` finds it every time, survives header
drift, disambiguates which of N plans is live) — a semantic section is
something each agent re-locates and each session re-invents. The
mechanism is the point; freezing it is what makes the skill improvable.

## Brainstorm in the plan

The plan is where thinking out loud lives — options weighed, discussion
recorded. Keep it from rotting: resolved → one-line **Decision** with the
why; unresolved → **Open Questions**; loose musing either crystallizes or
dies.

## Roadmap contract

Every plan implements a roadmap item:

1. Find (or create) `_docs/features/<feature>/roadmap.md`
2. Set the item `[in-progress]` and link it: `→ .plans/<name>.md`
3. On ship: `[shipped]`, remove the plan link, promote durable facts,
   delete the plan
4. On abandon: revert to `[planned]`, delete the plan

Tech debt and product debt live in the same roadmap.md under their own
sections — one place per feature, not a separate debts folder.
Cross-cutting infra debt → `_docs/architecture/roadmap.md`.

## Don't invent

Before touching a third-party integration or existing subsystem, read its
`_docs/` entry — it is authoritative. If docs and reality disagree,
**reality wins**: fix the docs and cite the source (API URL, file:line,
commit) so the correction is verifiable, not another invention.

## With rjv-gated-build

For high-stakes adversarial builds (see the `rjv-gated-build` skill), the
feature's plan file IS that build's anchor document — the grill trail,
evidence ledger, and tombstones live as sections inside it. Multiple
concurrent gated builds = multiple plans, each hydrated by name through
the entry point above.

---

*Provenance: production workflow from a live Laravel/fintech monorepo
(mfstack), where multiple concurrent features + two agents (Claude Code,
Codex) share the same plans and docs.*
