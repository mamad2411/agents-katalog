---
name: git-version-control
description: Use git to version-control local research/EDA iterations with reproducible checkpoints, clear commit/tag structure, and explicit per-version differentiation records. Use when users ask to create baselines, compare versions, snapshot experiment states, prepare rollback points, or document each version's characteristics and distinguishing deltas.
---

# Git Version Control

## When to use

Use this skill when the user asks to create baselines, compare versions, snapshot experiment states, prepare rollback points, or document each version's distinguishing characteristics.

## Shared Capability Boundary

This skill is the direct workflow owner for git-coupled versioning tasks.
It owns:
- repository state inspection for versioning,
- commit/tag/checkpoint preparation,
- human-readable version-log traceability.

It does not own:
- repo-wide governance policy,
- artifact cleanup policy,
- execution orchestration outside the versioning task itself.

`workflow-scoped-execution` is not the default wrapper here. Use it only if a larger workflow delegates one bounded execution stage that must end in a git snapshot.

## Expected Downstream Consumers

Typical consumers include:
- `eda-method-implementer` after implementation milestones,
- `workflow-research-chain` during versioned development stages,
- execution skills that need an explicit rollback point after a governed run.

## Inputs

Provide or derive:
1. version scope and changed-file set,
2. desired version identity style,
3. whether a tag is required,
4. comparison baseline and version-log destination.

## Outputs

Return or update:
- commit/tag or checkpoint identity,
- version-log entry under `docs/versioning/` or equivalent topic log,
- explicit baseline and differentiator record,
- explicit statement of whether `workflow-scoped-execution` was `not_used` or the versioning step was delegated from another workflow.

## Knowledge And Tool Interaction

1. Use existing project version logs or checkpoint notes as the local knowledge base for baseline selection and version naming continuity.
2. If a task needs a shared tool-reuse lookup before adding versioning helpers, delegate that lookup to `eda-context-accessor`.
3. Write version facts back into the human-readable project log so git metadata is paired with experiment meaning.

## Hard Rules

1. Inspect repository state before creating a new version artifact.
2. Avoid touching unrelated dirty files.
3. Never use destructive reset/checkout unless user explicitly requests.
4. Every version artifact must be traceable through git metadata plus a human-readable log entry.
5. Do not route routine versioning work through `workflow-scoped-execution` unless the parent workflow explicitly delegates a bounded execution stage that ends in version capture.

## Operational References

1. Load `references/workflow-owner-usage.md` when deciding whether versioning is the direct workflow owner task or a delegated substage inside another workflow.
2. Load `references/state-and-identity.md` when inspecting repository state or defining the version token, naming, and commit-title convention.
3. Load `references/commit-tag-and-traceability.md` when preparing the actual commit/tag sequence, version-log fields, or post-commit traceability checks.
4. Load `references/version-log-template.md` when writing or updating the human-readable per-version log entry.
