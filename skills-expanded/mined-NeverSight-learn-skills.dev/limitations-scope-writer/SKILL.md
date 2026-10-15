---
name: limitations-scope-writer
description: Draft ML/AI limitations, scope, failure cases, ethics, and conclusion caveats. Use to control claim boundaries and reduce overclaiming.
argument-hint: "[paper-dir] [--mode plan|draft|revise] [--section limitations|scope|ethics|conclusion]"
allowed-tools: Read, Write, Edit, Bash, Glob
---

# Limitations Scope Writer

Write limitations and scope as claim-boundary control. This skill helps the paper acknowledge real constraints, explain their impact, and preserve the valid contribution.

Use this skill for:

- drafting limitations sections
- writing scope statements and failure-case paragraphs
- calibrating conclusion caveats
- turning negative or mixed results into honest boundaries
- writing ethics, broader impact, and deployment caveats when required
- reducing overclaiming without weakening supported claims

Do not use this skill for hostile review. Use `paper-reviewer-simulator` for reviewer critique. Use `experiment-story-writer` for mixed-result results prose. Use `paper-writing-memory-manager` to propagate scope changes to title, abstract, intro, results, captions, and conclusion. Use `paper-draft-consistency-editor` for full-draft consistency.

## Skill Directory Layout

```text
<installed-skill-dir>/
├── SKILL.md
├── references/
│   ├── limitation-patterns.md
│   └── ethics-and-scope.md
└── templates/
    └── limitations-scope-plan.md
```

## Progressive Loading

- Always read `references/limitation-patterns.md`.
- Read `references/ethics-and-scope.md` when writing ethics, broader impact, deployment caveats, data/model risks, or human-subject/domain caveats.
- Use `templates/limitations-scope-plan.md` when creating `paper/.agent/limitations-scope-plan.md`.
- Read local `paper/.agent/writing-contract.md`, `paper/.agent/writing-memory/`, `paper/.agent/paper-evidence-board.md`, `paper/.agent/experiment-story-plan.md`, `paper/.agent/provisional-results.md`, review-risk notes, and current draft sections when present.

## Core Principles

- A limitation should define the boundary of the claim, not apologize for the paper existing.
- Be specific about affected settings, assumptions, data, metrics, compute, users, or deployment contexts.
- Pair each limitation with its consequence for interpretation.
- Do not bury limitations that contradict a main claim; narrow the claim or route to diagnosis.
- Do not invent mitigations, future work, or ethics safeguards that the project does not support.
- Scope language should appear wherever the paper might otherwise overclaim: abstract, intro, results, limitations, and conclusion.
- Limitations should be consistent with the evidence board and writing contract.

## Step 1 - Build Scope Snapshot

Extract:

```markdown
## Limitations Scope Snapshot
- Target venue:
- Paper archetype:
- Main claims:
- Supported scope:
- Known limitations:
- Failure cases:
- Mixed or negative results:
- Dataset/benchmark constraints:
- Compute/system constraints:
- Human/domain/deployment risks:
- Ethics or broader-impact requirements:
- Claims needing downgrade:
```

If a limitation undermines the primary claim, route to `result-diagnosis`, `paper-positioning-planner`, or `paper-evidence-board` before writing final text.

## Step 2 - Classify Limitations

Read `references/limitation-patterns.md` and classify each limitation:

- data or benchmark scope
- model or method assumption
- metric or evaluation scope
- compute or scale constraint
- generalization boundary
- failure mode
- human/domain/deployment constraint
- theoretical assumption
- artifact or reproducibility constraint

For each limitation, decide whether it requires:

- local wording only
- claim downgrade
- new experiment
- related-work repositioning
- ethics/broader-impact text
- reviewer-risk follow-up

## Step 3 - Create Scope Plan

Create or update:

```text
paper/.agent/limitations-scope-plan.md
```

If there is no `paper/` directory and the current directory is the paper repo, save to:

```text
.agent/limitations-scope-plan.md
```

Use `templates/limitations-scope-plan.md`.

For each limitation, record:

- affected claim
- evidence source
- wording consequence
- paper locations needing scope language

## Step 4 - Draft or Revise Limitation Text

For each limitation paragraph:

- state the limitation concretely
- identify the affected scope
- explain how it changes interpretation
- preserve what the paper still establishes
- optionally name a realistic future direction

Avoid vague phrases such as "more work is needed" unless the needed work is specified.

## Step 5 - Propagate Scope

Limitations often require edits outside the limitations section. Check:

- title
- abstract
- contribution bullets
- introduction claims
- result interpretation
- captions
- conclusion

If a scope correction affects top-level prose, route to `abstract-title-contribution-writer` or `paper-draft-consistency-editor`.

## Step 6 - Final Checks

Before finalizing:

- limitations are specific and evidence-grounded
- no limitation silently contradicts the main claim
- scope language appears in all high-risk locations
- failure cases are explained rather than hidden
- ethics/broader-impact text does not overpromise safeguards
- future work is realistic and not used to cover missing required evidence
- reviewer-risk follow-ups are explicit
- scope and limitation changes are written back through `paper-writing-memory-manager`
