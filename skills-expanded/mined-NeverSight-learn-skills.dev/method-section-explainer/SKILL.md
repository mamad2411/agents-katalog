---
name: method-section-explainer
description: Plan and draft ML/AI method sections. Use for notation flow, module ordering, algorithm boxes, overview figures, design rationale, and appendix boundaries.
argument-hint: "[paper-dir] [--mode plan|draft|revise] [--method-type algorithm|model|system|benchmark|theory]"
allowed-tools: Read, Write, Edit, Bash, Glob
---

# Method Section Explainer

Explain methods so reviewers can understand what is new, how it works, and why each design choice exists. This skill is for writing and structuring the method section, not inventing the algorithm.

Use this skill for:

- choosing method section structure
- introducing notation and problem setup
- writing method overview prose
- sequencing modules, losses, training/inference procedures, or system components
- deciding where algorithm boxes, equations, and overview figures belong
- explaining design rationales without overclaiming
- moving implementation details to appendix or experiment setup

Do not use this skill for designing a new algorithm. Use `algorithm-design-planner` for method design. Use `paper-writing-assistant` for broad prose. Use `paper-writing-memory-manager` to record notation, method terminology, overview-figure dependencies, and stale result/caption locations. Use `figure-results-review` for figure quality. Use `paper-draft-consistency-editor` after the section exists.

## Skill Directory Layout

```text
<installed-skill-dir>/
├── SKILL.md
├── references/
│   ├── method-structure-patterns.md
│   └── notation-and-rationale.md
└── templates/
    └── method-explanation-plan.md
```

## Progressive Loading

- Always read `references/method-structure-patterns.md`.
- Read `references/notation-and-rationale.md` when writing notation, equations, algorithm boxes, design rationale, or appendix boundaries.
- Use `templates/method-explanation-plan.md` when creating `paper/.agent/method-explanation-plan.md`.
- Read local `paper/.agent/writing-contract.md`, `paper/.agent/writing-memory/`, algorithm specs, design docs, method notes, `sections/method*.tex`, `sections/approach*.tex`, `figures/*.tex`, and appendix files when present.

## Core Principles

- Explain the method in the order the reader needs, not in the order it was implemented.
- Start with task/setup and method overview before low-level details.
- Introduce notation only when it will be used soon.
- Every module or equation should have a reason to exist.
- Overview figures should anchor the section; captions should not carry essential missing explanation.
- Separate conceptual method, training objective, inference procedure, and implementation details.
- Put reproducibility-critical details somewhere, but not necessarily in the main method section.
- Do not use method prose to make empirical claims that belong in results.

## Step 1 - Build Method Snapshot

Extract:

```markdown
## Method Explanation Snapshot
- Paper archetype:
- Method type:
- Target venue:
- Main method claim:
- Proposed object:
- Inputs/outputs:
- Key components:
- Training objective:
- Inference procedure:
- Overview figure:
- Algorithm box:
- Required notation:
- Appendix material:
- Reader confusion risks:
```

If the method itself is underspecified, route to `algorithm-design-planner` before drafting final prose.

## Step 2 - Select Structure Pattern

Read `references/method-structure-patterns.md` and choose one pattern:

- algorithmic method
- model architecture
- training objective or loss method
- benchmark or dataset construction
- system/tool
- theory/setup
- hybrid

The pattern determines subsection order and what belongs in the main text.

## Step 3 - Create Method Explanation Plan

Create or update:

```text
paper/.agent/method-explanation-plan.md
```

If there is no `paper/` directory and the current directory is the paper repo, save to:

```text
.agent/method-explanation-plan.md
```

Use `templates/method-explanation-plan.md`.

For each subsection, record:

- reader question answered
- concepts introduced
- notation introduced
- figure/equation/algorithm references
- appendix handoff

## Step 4 - Draft or Revise Method Prose

For each subsection:

- open with the subsection's purpose
- define inputs and outputs before transformations
- introduce one abstraction level at a time
- state design rationale after the design is understandable
- use equations to formalize, not replace explanation
- close with how the piece connects to the next component

When revising LaTeX, preserve labels, refs, citations, macros, and math unless they are part of the requested edit.

## Step 5 - Decide Main Text vs Appendix

Keep in main text:

- core mechanism
- essential notation
- training/inference logic needed to understand claims
- design rationale tied to novelty
- overview figure or algorithm if central

Move or defer to appendix:

- long proofs
- hyperparameter grids
- architecture minutiae not needed for the argument
- dataset preprocessing details
- engineering edge cases
- derivations that support but do not define the method

## Step 6 - Final Checks

Before finalizing:

- the method's novelty is visible
- notation appears before use and is not excessive
- modules are introduced in dependency order
- every equation has surrounding explanation
- design choices have rationale or are moved to implementation details
- overview figure, algorithm box, and text agree
- results claims are not smuggled into the method section
- appendix handoffs are explicit
- notation, terminology, and method-section status are written back through `paper-writing-memory-manager`
