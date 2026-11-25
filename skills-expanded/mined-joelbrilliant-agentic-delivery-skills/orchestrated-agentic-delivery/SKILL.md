---
name: orchestrated-agentic-delivery
description: Formalises orchestrator, builder, reviewer, reviewer-fix, and final signoff workflows across agent harnesses, coding agents, and subagents. Use when coordinating multi-agent delivery, writing briefs, assigning builders or reviewers, deciding whether reviewers may fix issues, or final-signing production-bound work.
---

# Orchestrated Agentic Delivery

## Overview

Use this skill to run agentic work as a real delivery lane instead of a pile of helpful model outputs.

The roles are separate:

- **Orchestrator**: frames the task, controls scope, routes work, judges final evidence.
- **Builder**: implements the approved slice and owns the primary diff until review.
- **Reviewer**: adversarially reviews the builder's work and may enter an explicit fix pass.
- **Final judge**: the orchestrator signs off against the brief, diff, review, fixes, and evidence.

Runtime does not matter. The builder or reviewer can be any coding agent, chat agent, custom harness, or subagent. Accountability follows the role, not the tool.

## When to Use

Use this skill for:

- production-bound features or bug fixes with more than one role;
- work where an orchestrator dispatches builders or reviewers;
- multi-agent workflows across coding agents or subagents;
- reviewer-fix flows where the reviewer is allowed to repair findings;
- final signoff after build plus review;
- any task where same-model builder and reviewer echo-chamber risk matters.

Do not use this for one-off answers, throwaway scripts, or prototypes with no review gate.

## Mandatory Companion

Load `bulletproof-building-and-review` during:

- production-bound building self-signoff;
- adversarial review;
- reviewer-fix mode;
- closing findings as non-issues;
- final orchestrator signoff.

This skill defines **who does what**. `bulletproof-building-and-review` defines **how to prove it is not bullshit**.

## Core Rules

1. **One slice, one primary builder.** Extra builders are allowed only for independent slices with non-overlapping write sets.
2. **Reviewer is not a stealth co-builder.** Reviewer fixes only after writing findings and entering explicit reviewer-fix mode.
3. **Final signoff belongs to the orchestrator.** Builders and reviewers provide evidence. They do not self-merge by vibes.
4. **Design approval gates stay real.** If design or spec is in scope, get signoff before implementation.
5. **Fix root causes.** Do not layer workarounds unless the brief explicitly accepts that tradeoff.
6. **Runtime is not authority.** Every model and harness needs the same evidence discipline.
7. **No invisible work.** When the platform supports visible run IDs, tasks, PRs, commits, or transcripts, use them.

## Standard Workflow

### 1. Orchestrator frames the slice

The orchestrator writes a brief with:

- goal and non-goals;
- owner and role assignments;
- allowed files or surfaces;
- success criteria;
- required tests and runtime proof;
- design approval status, if relevant;
- known risks and stop conditions.

If the framing is muddy, fix the brief before dispatching.

### 2. Builder implements

The builder:

- works only inside the approved slice;
- preserves unrelated work;
- commits or otherwise provides a concrete review surface;
- reports changed files, tests, build, runtime checks, and known limitations;
- does not ask the reviewer to infer scope from the diff.

### 3. Reviewer reviews adversarially

The reviewer loads `bulletproof-building-and-review` and produces:

- PASS, HOLD, or REQUEST CHANGES;
- findings with severity and file:line evidence;
- regression analysis for every finding;
- closed non-issues with test/file evidence;
- required-test mapping against the brief.

### 4. Reviewer-fix mode, if authorised

Reviewer-fix mode is allowed only when explicit.

The reviewer must:

1. write findings first;
2. declare they are entering reviewer-fix mode;
3. fix only documented findings;
4. avoid unrelated cleanup or product/design changes;
5. rerun the relevant verification;
6. report the fix diff and evidence separately from the original review.

If a fix requires changing scope, design direction, architecture, or user-visible behaviour beyond the finding, stop and return to the orchestrator.

### 5. Orchestrator final signoff

The orchestrator checks:

- brief and non-goals;
- builder diff and evidence;
- reviewer findings and closed items;
- reviewer fixes, if any;
- tests/build/runtime proof;
- production-shaped data path where relevant;
- git state, commit SHA, PR, task payload, or equivalent handoff artefact.

Final signoff is not a rubber stamp. If evidence is missing, send it back.

## Handoff Contract

Every role handoff must include:

- role and owner;
- scope completed;
- changed files or artefacts;
- tests and exact commands run;
- runtime/browser/API proof where relevant;
- known limitations;
- unresolved decisions;
- commit SHA, PR, task/run ID, or transcript handle when available.

## Subagent Rules

- A subagent can be a builder only for a clearly isolated slice.
- A subagent can be a reviewer only if given the full brief, diff surface, and required evidence standard.
- The parent orchestrator must verify externally visible claims before reporting success.
- If a subagent writes files or causes side effects, verify the file, commit, URL, or status yourself.

## Anti-patterns

Stop if you see:

- two builders editing the same slice without explicit ownership split;
- reviewer quietly patching unrelated code;
- orchestrator accepting "tests pass" without mapping tests to requirements;
- final signoff before review evidence exists;
- invisible background work used as proof when visible run/commit/task evidence is available;
- same-model builder and reviewer treated as independent judgement without adversarial evidence.
