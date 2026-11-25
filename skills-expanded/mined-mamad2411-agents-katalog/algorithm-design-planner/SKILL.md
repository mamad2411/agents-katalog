---
name: algorithm-design-planner
description: Turn a promising ML/AI research idea into a precise algorithm or method design before implementation. Use this skill whenever the user has an idea or project direction and wants to design the actual method, objective, architecture, inference procedure, assumptions, failure modes, ablations, implementation handoff, or method section plan before coding or experiment design.
argument-hint: "[project-dir] [--idea <idea>] [--mode method|objective|architecture|theory|system|revision]"
allowed-tools: Read, Write, Edit, Bash, Glob, WebSearch, WebFetch
---

# Algorithm Design Planner

Convert a validated research idea into a concrete method design that can be implemented, ablated, evaluated, and explained in a paper.

Use this skill when:

- an idea has passed early validation and needs an actual algorithm
- a method, loss, architecture, inference procedure, or training recipe is underspecified
- the user needs a method design document before coding
- a project needs assumptions, failure modes, ablations, and implementation boundaries
- early results suggest revising the algorithm rather than only rerunning experiments
- a paper's method section is hard to write because the method itself is not precise

Do not use this skill to launch experiments. Pair it with `experiment-design-planner` after the design is specific enough to test.

Pair this skill with:

- `research-project-memory` when the design changes claims, assumptions, risks, actions, or worktree purpose
- `research-idea-validator` before this skill if the idea itself may not be worth pursuing
- `literature-review-sprint` when the closest prior method is unclear
- `experiment-design-planner` after the method produces testable hypotheses and ablations
- `run-experiment` only after implementation and experiment design are ready
- `conference-writing-adapter` when translating the final design into paper prose

## Skill Directory Layout

```text
<installed-skill-dir>/
├── SKILL.md
└── references/
    ├── ablation-implications.md
    ├── design-rubric.md
    ├── failure-mode-map.md
    ├── implementation-handoff.md
    ├── method-spec-template.md
    └── paper-method-bridge.md
```

## Progressive Loading

- Always read `references/design-rubric.md` and `references/method-spec-template.md`.
- Read `references/failure-mode-map.md` when assumptions, edge cases, or negative results matter.
- Read `references/ablation-implications.md` when the method has components, losses, objectives, schedules, architectures, or inference changes.
- Read `references/implementation-handoff.md` before producing coding tasks or worktree plans.
- Read `references/paper-method-bridge.md` when the design must become a method section.
- If novelty depends on current methods or baselines, verify with web search or user-provided papers.

## Core Principles

- Design the mechanism before designing the experiment.
- Separate the problem, method, claim, and evidence plan.
- Make the smallest method that could test the core idea.
- State assumptions and invariants explicitly.
- Identify what is genuinely new relative to the closest baseline.
- Every method component should have a reason, an ablation, and a failure mode.
- Avoid adding knobs that cannot be justified, tuned fairly, or explained to reviewers.
- Produce an implementation handoff that prevents hidden design decisions from being made during coding.

## Step 1 - Recover Context

Collect:

- validated idea or project direction
- current decision from `research-idea-validator`, if available
- target paper claim
- target model/task/domain
- closest baseline or prior method
- available codebase and implementation constraints
- known experiments or negative results
- project memory IDs such as `CLM-###`, `RSK-###`, or `ACT-###`, if present

If the idea is still vague, rewrite it into:

```text
For [problem/setting], modify [baseline] by [mechanism] so that [expected property] improves because [assumption].
```

If this sentence cannot be written, route back to `research-idea-validator` or `literature-review-sprint`.

## Step 2 - Choose Design Mode

Classify the design:

- `method`: new algorithm, training recipe, or inference procedure
- `objective`: new loss, regularizer, constraint, reward, or optimization criterion
- `architecture`: new module, representation, layer, routing, memory, or parameterization
- `theory`: formal method derived from assumptions, theorem, bound, or principle
- `system`: pipeline, infrastructure, scheduling, retrieval, data, or tooling design
- `revision`: method update after negative or ambiguous results

Use one primary mode and optional secondary modes.

## Step 3 - Build the Method Spec

Read `references/design-rubric.md` and `references/method-spec-template.md`.

Define:

- problem formulation
- inputs and outputs
- baseline being modified
- core mechanism
- training objective or loss, if any
- inference or sampling procedure, if any
- architecture or module changes, if any
- assumptions and invariants
- hyperparameters and schedules
- computational cost
- expected behavior
- what stays unchanged from the baseline

Use math, pseudocode, or structured bullets as appropriate. Do not hide important design decisions in prose.

## Step 4 - Check Novelty and Minimality

Ask:

- What is the irreducible difference from the closest baseline?
- Which part is necessary for the claim?
- Which part is convenience, engineering, or tuning?
- Can the first implementation test a smaller version?
- Could a reviewer call this a minor tweak?

If the new idea depends on multiple changes, separate core design from optional extensions.

## Step 5 - Map Failure Modes

Read `references/failure-mode-map.md`.

List:

- assumptions that may be false
- data or task regimes where the method should fail
- optimization or stability risks
- metric mismatch risks
- computational risks
- confounds that could explain gains
- signs that the design should be revised, parked, or killed

Negative outcomes should map to decisions, not vague concern.

## Step 6 - Derive Ablations and Diagnostics

Read `references/ablation-implications.md`.

For each method component, define:

- why it exists
- what happens if removed
- what diagnostic tests its mechanism
- what hyperparameter or schedule must be swept
- what baseline or control separates the mechanism from tuning or compute

This output should feed directly into `experiment-design-planner`.

## Step 7 - Prepare Implementation Handoff

Read `references/implementation-handoff.md`.

Produce:

- files/modules likely to change
- public interfaces or config names
- minimal prototype plan
- unit/smoke tests
- logging requirements
- worktree or branch purpose
- exit condition: merge, continue, park, or kill
- risks that coding should not decide silently

If no codebase exists, define a minimal scaffold or prototype boundary instead of a full engineering plan.

## Step 8 - Bridge to Paper Method Section

Read `references/paper-method-bridge.md` when useful.

Produce:

- method name, if needed
- method-section outline
- algorithm box contents
- equations or definitions required
- assumptions to state
- reviewer-facing explanation of why the mechanism should work
- claims to avoid until evidence exists

## Step 9 - Write the Design Document

If saving to a project and no path is given, use:

```text
docs/designs/algorithm_design_YYYY-MM-DD_<short-name>.md
```

Use this structure:

```markdown
# Algorithm Design: [Name]

## Design Context
## Target Claim
## Design Decision
## Problem Formulation
## Method Specification
## Assumptions and Invariants
## Relation to Baseline and Prior Work
## Failure Modes
## Ablations and Diagnostics
## Implementation Handoff
## Experiment Handoff
## Paper Method Bridge
## Project Memory Writeback
```

## Step 10 - Write Back to Project Memory

If the project uses `research-project-memory`, update:

- `memory/decision-log.md`: durable design choices and why
- `memory/claim-board.md`: method claims that are planned, revised, weakened, or cut
- `memory/risk-board.md`: mechanism, implementation, baseline, tuning, compute, and evaluation risks
- `memory/action-board.md`: implementation, ablation, diagnostic, literature, or experiment-design actions
- `memory/evidence-board.md`: planned diagnostics or experiment families when concrete enough
- worktree `.agent/worktree-status.md`: purpose, linked claims, linked experiments, and exit condition for implementation branches

Use `planned` for evidence and `inferred` for failure modes until observed.

## Final Sanity Check

Before finalizing:

- problem, baseline, and method are explicit
- core mechanism is distinguishable from optional engineering
- assumptions and invariants are stated
- every new component has an ablation or diagnostic
- implementation handoff is concrete enough for coding
- experiment handoff is concrete enough for `experiment-design-planner`
- paper-method bridge does not overclaim beyond planned evidence
- project memory is updated when present
