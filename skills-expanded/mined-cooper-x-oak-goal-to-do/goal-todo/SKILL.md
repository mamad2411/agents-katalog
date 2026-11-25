---
name: goal-todo
description: Define and refine a long-running Codex goal before using `/goal`. Use when the user has a vague multi-step task, wants Codex to work autonomously toward a persistent objective, asks for a final `/goal` prompt, or needs structured interactive alignment on scope, success criteria, constraints, and decision checkpoints before launching a long-running task.
---

# Goal Todo

## Overview

This skill turns a vague ambition into a final `/goal` prompt that is ready to paste and run.

Do not jump straight to writing the final prompt. First reduce ambiguity through structured interaction, then synthesize a durable long-running goal.

By default, the final user-facing deliverable should be the `/goal` prompt itself, not an explanatory brief.

## Core Rule

When this skill is invoked, the default interaction surface should be:

1. Use `request_user_input` in the current environment.
2. If `request_user_input` is unavailable, tell the user this skill works best with clickable structured choices and ask them to reopen or switch to `Plan mode`, then retry with `request_user_input`.
3. If the user does not switch to `Plan mode`, fall back to concise plain-text alignment with explicit reply templates.

Do not skip the alignment round. Only the interaction surface may degrade.

## Interaction Standard

Ask high-quality structured questions that reduce ambiguity instead of pushing the user into free-form ideation.

Match the user's current language by default. If the user has not established a clear language preference and the distinction matters, ask briefly or choose the language already dominant in the thread.

Each question should:

- present 2-3 strong options, not a blank request
- use concrete tradeoffs so the user can choose quickly
- help align on intent, boundaries, and autonomy level
- avoid jargon unless the user already introduced it
- stay concise, but not so short that the options become vague

Prefer two alignment rounds. Use one round only if the user already provided unusually complete requirements.

## Entry Workflow

The first goal-todo pass should clarify three axes.

### 1. Goal Shape

- `Ship a Change (Recommended)`
  The user wants a concrete delivered result such as code, docs, workflow, prompt system, or automation.
- `Research and Decide`
  The user needs evidence, tradeoff analysis, or a decision memo before implementation.
- `Open Exploration`
  The user wants Codex to explore, structure, and progressively narrow a larger ambiguous problem.

### 2. Autonomy Style

- `Tight Then Loose (Recommended)`
  Start with closer alignment until intent, direction, and boundaries are stable, then shift into autonomous execution with explicit checkpoints.
- `Maximum Autonomy`
  Codex keeps executing until blocked by permissions, missing facts, or hard risks.
- `Tight Collaboration`
  Codex proposes smaller moves and checks in more often.

Treat autonomy as an execution curve, not just a static preference. If the user indicates "start tight, then loosen", preserve that shape in the final brief instead of flattening it into a generic checkpoint mode.

### 3. Finish Line

- `Single Clear Deliverable (Recommended)`
  One primary output with explicit done criteria.
- `Milestone Sequence`
  Several ordered deliverables with handoff points.
- `Ongoing Operating Goal`
  A broader goal that may continue across phases until paused or re-scoped.

If plain-text fallback is required, ask the user to reply in this exact shape:

```text
shape=ship_change
autonomy=tight_then_loose
finish=single_clear_deliverable
```

## Second Alignment Round

The second pass should define the operational boundary of the goal. Cover these three axes.

### 1. Scope Level

- `Minimum Useful Win`
  Constrain the goal to the smallest closed loop that still creates value.
- `Balanced Scope (Recommended)`
  Keep ambition under control while allowing enough room to complete the job well.
- `Full Ambition`
  Include adjacent work needed to make the result feel complete.

### 2. Risk Posture

- `Conservative (Recommended)`
  Prefer validated steps, fewer assumptions, and earlier stop points.
- `Balanced`
  Allow moderate assumptions when they speed progress and are reversible.
- `Aggressive`
  Let Codex move fast with fewer interruptions when the user accepts rework risk.

### 3. Decision Checkpoints

- `Only Major Decisions`
  Stop only for architecture, scope, or irreversible operations.
- `Scope + Review Gate (Recommended)`
  Stop once to confirm direction, then once before finalization.
- `Frequent Sync`
  Stop at multiple milestones.

If plain-text fallback is required, ask the user to reply in this exact shape:

```text
scope=balanced
risk=conservative
checkpoints=scope_and_review
```

## Synthesis Output

After the alignment rounds, synthesize the goal internally using these sections:

1. `Goal`
2. `Why Now`
3. `Scope`
4. `Non-Goals`
5. `Success Criteria`
6. `Constraints`
7. `Decision Checkpoints`
8. `Execution Shape`
9. `Autonomy Curve`
10. `Final /goal Prompt`

`Autonomy Curve` should explicitly capture whether the user wants:

- tight alignment first, then more autonomy
- consistent checkpoint-based autonomy throughout
- high-frequency collaboration throughout
- near-total autonomy unless blocked

The final `/goal` prompt should be direct, execution-oriented, and persistent in tone. It should tell Codex what to achieve, what boundaries to respect, when to stop for user input, and what counts as done.

Unless the user explicitly asks for analysis, notes, or an expanded brief, the final user-facing output must be:

- starting with `/goal `
- containing no extra heading, label, explanation, bullet, or code fence before or after it
- remaining a single prompt, even if it spans multiple intentional lines

Think with the sectioned brief internally if helpful, but do not force the user to copy anything except the final `/goal` line.

## Compression Rules

Do not over-document. Keep the final `/goal` prompt as compact as practical, but do not artificially flatten or shorten it just to work around terminal display issues.

Prefer:

- explicit scope boundaries over motivational prose
- concrete completion criteria over aspirational language
- named stop points over vague "keep me posted"
- user intent fidelity over clever reframing
- a clean `/goal` prompt over surrounding explanation

Intentional line breaks are allowed when they improve clarity. Do not add fake labels or wrapper text around the prompt.

## Typical Triggers

This skill is especially suitable when the user says things like:

- "Turn this task into a `/goal` prompt"
- "This objective is long-running; define it clearly first"
- "I want Codex to drive this, but align the boundaries first"
- "Do not execute yet; define the problem first"
- "Give me a final prompt that is appropriate for goals"
