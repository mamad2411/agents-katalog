---
name: spec-to-tasks
description: Breaks a specified ticket into approved, self-contained implementation tasks with executor classifications, parent relationships, and blocking edges. Use when a ticket specification is ready to become executable tracker tasks.
disable-model-invocation: true
---

# Spec to Tasks

Turn one specified ticket into executable child tasks. Read [REFERENCE.md](REFERENCE.md) completely before drafting.

## Gather context

Read `docs/agents/bb-skills.md`. If it is missing or inconsistent, stop and direct the user to `$setup-bb-skills`.

Resolve the parent ticket from the user's reference or current conversation. Read its full body and comments. The parent must contain a specification; do not synthesize one here.

Explore relevant repository instructions, domain docs, ADRs, code, and prior tests. Use project vocabulary and respect existing decisions.

## Draft tasks

Break the specification into tracer-bullet tasks using the rules in the reference. Each task must:

- fit a fresh context window;
- be understandable without the originating conversation;
- state enough parent and plan context for agent replacement or safe parallel work;
- declare its blockers and what later work it enables;
- have externally verifiable acceptance criteria.

Assign the configured agent executor when the work can be completed autonomously with available tools and access. Assign the configured human executor when implementation requires human-only judgment, access, physical action, or manual validation. Every task receives exactly one executor classification.

## Review

Present a numbered breakdown. For each task show:

- title;
- executor;
- blocked by;
- what it delivers.

Ask whether granularity, executor choices, and blocking edges are correct and whether tasks should be merged or split. Iterate until approved.

## Publish

After approval:

1. Inspect for existing equivalent child tasks.
2. Publish new tasks in dependency order.
3. Apply configured task and executor classifications.
4. Attach every task to the parent using the configured relationship.
5. Apply release grouping according to the contract.
6. Create configured blocking relationships and retain readable blocker references.
7. Verify every task, classification, parent edge, and blocker edge.

Do not close or rewrite the parent ticket or close any task. Stop on partial failure and report exactly what was created and which relationships remain incomplete.
