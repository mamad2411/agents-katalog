---
name: plan-optimizer
description: "Second-pass critique of an existing plan file — sharpens data flow, perf realism, testability, verifiability, and risk sequencing. Run after /plan (auto-triggered for 3+ task plans), or when the user says \"review the plan\", \"strengthen the plan\", or \"is this plan solid?\". De-risks an existing plan — it does not re-run discovery (/plan) or execute (/implement)."
---

# Plan Optimizer

A focused second pass over a plan. Goal: sharpen and de-risk by reconsidering the plan freshly — across data flow, caching contracts, perf realism, GPU/CPU fit, testability, and risk sequencing, but also the obvious-looking decisions the first pass may have skipped past.

Be constructive, but don't defer. The plan author works fast through a structured loop and frequently misses obvious things — questioning a choice that "looks fine" is welcome when there's a real reason. Skeptical teeth land hardest on unverified performance claims, but every lens is fair game. Substantial code is fine when each piece earns its keep (see `wf-overengineering-not-volume`); the target is hand-waved difficulty, not size.

## Step 1: Locate plan

Argument is a path or slug → resolve to `plans/<arg>.md` or the literal path. No argument → most recent file in `plans/` (last edit < 1h), else ask via `AskUserQuestion`. Abort if nothing resolves.

## Step 2: Build context

Read the plan, `CLAUDE.md`, project-specific `.claude/rules/`, and 2-3 of the files named in the plan's `**Files:**` lists — enough to ground task realism without replicating `/plan`'s full read. Global rules are already auto-loaded.

## Step 3: Refine across lenses

Walk each lens. Reconsider the obvious — the first pass often skipped past it. But don't manufacture critique; "looks fine" is a valid finding when nothing's actually wrong.

**Shape** — architecture, simplification, file splitting:

- Reinventing a pattern the codebase already has?
- Overengineered per `wf-overengineering-not-volume` (abstractions without a current consumer, speculative configurability)?
- Tasks touching > 5 files or that would blow the 400/800 line cap should be split — separately from any design critique.

**Data** — flow & caching:

- Redundant copies, transforms, or round-trips in the data path?
- Every cache names its invalidation rule. Without expiry, it's a future stale-data bug.

**Performance — reality check** (lean skeptical here):

- Unverified perf claim → mark `**Needs baseline.**` or add a profiling task before the optimization.
- GPU candidacy needs a workload-shape argument: parallel, low branching, predictable memory, batch large enough to dwarf transfer cost. Without that, CPU usually wins.

**Risk & feasibility** — scope, reversibility, sequencing:

- Schema or breaking API change? Migration order and rollback path should be named.
- Highest-risk task scheduled early enough to fail fast?

**Verifiability** — testability:

- Each task has a concrete `**Acceptance:**` — unit test, build pass, manual check, profile-measured? "It works" doesn't count.
- A task with no `**Test:**` block is a failing acceptance check.
- Each task has a `**Verify:**` entry, and it names an **instrument** — a probe, scenario, or named test the project actually exposes, a shell command, or `human:` naming what to read — not a restatement of the `**Acceptance:**` prose. A task with no `**Verify:**` entry is a finding: `/verify` will report `no-instrument` and leave that task's criteria unverified.
- The named instrument should plausibly exist. Check against the **generating source** — the project's test or scenario registry, its probe documentation, or the live instrument surface — never a hand-written list kept inside this skill, which would drift from the real one. If the instrument doesn't exist yet, don't weaken the criterion to fit current tooling; flag it and propose a task that builds it (log in `## Decisions & Review Items`).
- `human:` is a first-class instrument, not a gap to close. Don't pressure a `human:` entry into a fake mechanical one, and accept a shell command as legitimate for config- or doc-only work — not every task needs a programmatic probe.

**Design coverage** — plan vs. agreed mockup (skip if the plan's `## UI Contract` says "None"):

- Different question from `/plan`'s design-agreement step. That step asks *what should we agree on*; this one asks *are the plan and the agreed picture the same thing* — a second-pass check over an already-drafted plan and its `## UI Contract`.
- Spawn `design-scout` by its own `subagent_type` (`"design-scout"` — **never** `general-purpose`, which has every tool and would silently erase the read-only restriction). Hand it the drafted plan and its `## UI Contract`.
- **Scope is structural drift only.** Report a task that would change UI structure the Contract's mockup doesn't show (new placement, a different interaction model, a restructure of existing chrome), a UI surface a task implies with no mockup counterpart, a Contract entry no task implements, or a scale mismatch (mockup implies a panel, tasks imply a restructure).
- **Detail-level UI is out of scope** — spacing, hover, empty/loading/error/disabled/overflow states. Cheap to fix once built, and mostly determined by the design system. Reporting a detail gap here is this lens failing its job, not being thorough.
- **An `open / deferred` Contract entry a task structurally depends on is a blocker, not a note.** The implementation loop never stops for a design question, so an unresolved structural entry is a guaranteed guess at implementation time rather than a future question. Unlike `design-scout`, this skill can call `AskUserQuestion` — resolve the entry with the user before Step 4 writes the plan. Detail-level deferred entries are never blockers.
- Findings route like every other lens: applied where mechanical (e.g. a dangling Contract entry with an obvious fix), surfaced where they need a decision. "Looks fine" is valid — don't manufacture structural concerns for a plan with no real UI surface.

Patterns repeating across multiple tasks should be flagged as a single systemic finding, not per-task.

## Step 4: Apply

Overwrite the plan file in place. Preserve title, context, and design decisions made in `/plan`. Revise task list, file lists, `**Acceptance:**` lines, risks, and perf claims where the lenses surfaced something. Log substantive changes in `## Decisions & Review Items` (e.g. "split task 3 — original lacked acceptance check").

If no lens surfaced anything actionable, leave the file untouched and say so.

## Step 5: Summarize

3-6 bullets: what changed and why. End with `Run \`git diff plans/<name>.md\`.` Skip the summary if nothing changed.

## Project rules

Project-specific plan critique criteria — performance baselines, known anti-patterns, testability conventions.
