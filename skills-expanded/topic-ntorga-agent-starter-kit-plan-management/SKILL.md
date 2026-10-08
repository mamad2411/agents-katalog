---
name: plan-management
description: Plan lifecycle — grill entry point, grounding, artifact review, per-epic execution, revision.
usedBy: [maestro]
version: 3.0.3
lastUpdated: 2026-09-12
---

## Purpose

This skill defines everything about plans: when to grill, how to ground and review the plan artifacts, how to execute epics, and how to revise. Read this skill whenever the task may require a plan.

## Procedure

Plans live in a directory under `.memory/plan/`:

```
.memory/plan/<feature-slug>/
├── tree.md    — the design tree: decisions, dependencies, recommendations, impact
├── plan.md    — acceptance criteria, what + why only
├── arch.md    — directory structure, layer separation, reference projects
└── impl.md    — epics grouped at one day of work, grounded with file paths, method signatures, test specs
```

- **`<feature-slug>`** — short kebab-case summary of the feature.
- **`tree.md`** — the grill's working state. The Architect builds and extends it. All nodes settled when the grill terminates.
- **`plan.md`** — acceptance criteria from the settled business decisions. Living document, edited inline as understanding evolves.
- **`arch.md`** — directory structure, layer separation, reference projects. Produced during the grill. The beginner path gets defaults from the maintenance, lightweight, and safe principles (KISS, single responsibility, safe boundaries — `rules/code/general.md`).
- **`impl.md`** — epics grouped at one day of work. The grill transcribes them. The Architect grounds and re-grounds them. Living document, edited inline as epics land.

**Epic completion tracking:** Epics in `impl.md` are annotated with ✓ when fully delivered, or ~ when partially delivered. All epics marked ✓ means the feature is complete.

**Parallelizable groups:** `impl.md` notes which epics can run in parallel. The Maestro may dispatch parallel epics to separate coders when file scopes do not overlap (follows: `skills/dispatch/SKILL.md`).

### Deciding When to Plan

A plan is required when the request is lengthy, multi-part, or describes a non-trivial change. When in doubt, plan — planning a simple task wastes minutes; skipping a plan on a complex task wastes hours.

If the task does not warrant a full plan, create a to-do instead (uses: `skills/task-tracking/SKILL.md`).

### Grilling

For tasks requiring a plan:

1. **Run the grill.** Read and follow `skills/grill/SKILL.md`.
2. **Confirm.** Present the artifacts to the user. Do not act until the user confirms shared understanding.

### Grounding

After the user confirms:

1. **Dispatch the Architect** (`personas/architect.md`) (follows: `skills/dispatch/SKILL.md`) in ground mode. The Architect reads `plan.md`, `arch.md`, and `impl.md`, then annotates `impl.md` per `skills/architect-impl-grounding/SKILL.md`.
2. **If the Architect returns escalations** (facts that contradict settled decisions), present them to the user. Do not proceed until the user resolves them.

### Artifact Review Gate

After grounding:

1. **Send the grounded artifacts through the review loop** (follows: `skills/review-loop/SKILL.md`) before proceeding to implementation.
2. **If the review verdict is `fail`**, re-dispatch the Architect (`personas/architect.md`) (follows: `skills/dispatch/SKILL.md`) with the confirmed findings — plan revision for `plan.md` or `arch.md` defects, grounding revision for `impl.md` defects — and re-review.
3. **Proceed to implementation only when the artifacts pass** (`pass` or `partial-pass`).

### Tracking Progress

For each pending epic, in order:

1. **Refresh (skip for the first epic after initial grounding).** Dispatch the Architect (`personas/architect.md`) (follows: `skills/dispatch/SKILL.md`) in refresh mode. The Architect classifies the landed epic's discoveries (adjust or escalate) and re-grounds the next epic against the current codebase.
2. **Escalations.** If the Architect flagged escalations, present them to the user. Do not proceed until the user resolves them.
3. **Dispatch the Coder** (`personas/coder.md`) (follows: `skills/dispatch/SKILL.md`) for the current epic. One epic per dispatch.
4. **Review loop.** Read and follow `skills/review-loop/SKILL.md` on the epic's code.
5. **Mark the epic** in `impl.md` with ✓ (fully delivered) or ~ (partially delivered).

If all epics are marked ✓, the feature is complete. Before reporting to the user, run the review loop in full branch mode (follows: `skills/review-loop/SKILL.md` → step 1) to comprehensively review the entire branch's accumulated changes.

### Finding Plans

To find the plan for a feature:

```bash
ls .memory/plan/<feature-slug>/
```

The directory contains `tree.md`, `plan.md`, `arch.md`, and `impl.md`. If the directory does not exist, no plan exists for that feature.

To find all features with plans:

```bash
ls -d .memory/plan/*/
```

### Reading Plans Efficiently

1. **Find the plan directory.** Run `ls .memory/plan/<feature-slug>/`.
2. **Read `plan.md`.** See all acceptance criteria and which are delivered (✓), partially delivered (~), or pending.
3. **Read `impl.md`.** See all epics, which are delivered (✓), partially delivered (~), or pending, and the annotated file paths and method signatures.
4. **Read `arch.md` only when revising architecture.** Read `tree.md` only when re-grilling or resuming a mid-grill session.

### Revising Plans

When plan revision is needed (new discoveries, clarified requirements):

1. **Edit `plan.md` or `impl.md` inline.** The artifacts are living documents. Never version-bump them.
2. **If the revision touches epics**, re-dispatch the Architect (`personas/architect.md`) (follows: `skills/dispatch/SKILL.md`) to re-ground the affected epics.
3. **Send the revised artifacts through the review loop** (follows: `skills/review-loop/SKILL.md`).

When an epic needs revision (feedback after implementation):

1. **Assess the feedback.** If the feedback requires only minor fixes (typos, small code corrections, no structural impact), dispatch the Coder (`personas/coder.md`) (follows: `skills/dispatch/SKILL.md`) directly to fix. If the feedback involves structural changes or scope changes, proceed to step 2.
2. **Edit `impl.md` inline.** Update the epic with the revised scope. Re-dispatch the Architect (`personas/architect.md`) (follows: `skills/dispatch/SKILL.md`) to re-ground the affected epic. Send the revised artifacts through the review loop.

## Guardrails

- Never mark an epic complete that has not passed the review loop.
- Never version-bump the plan artifacts. Edit them inline.
- When resuming, never bulk-read the plan directory — read `plan.md`, then `impl.md` for current progress. Read `arch.md` and `tree.md` only when their sections say to.
- Never dispatch the Coder on an epic whose grounding is stale after a landed epic — refresh first.
- If plan files cannot be found, stop and report the error. Do not guess paths.
- Never proceed to the next epic when escalations are unresolved. The user must resolve them first.
