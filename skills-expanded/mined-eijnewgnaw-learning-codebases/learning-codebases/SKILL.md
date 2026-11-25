---
name: learning-codebases
description: Use when the user wants to learn, understand, study, map, onboard to, or walk through an unfamiliar codebase or software project, especially when explanations should suit a beginner with basic Python knowledge.
---

# Learning Codebases

Build a durable mental model from real code. Optimize for the smallest evidence set that supports the learner's next useful insight.

## Start

Identify the learner's immediate goal: project overview, one feature flow, one file, running the project, preparing a change, or interview review. Ask one question only when the goal is genuinely ambiguous; otherwise begin in **Standard** mode.

Default to read-only inspection. Do not modify the target project merely to explain it.

For a first pass over a repository, read `references/repository-analysis.md`. Reuse its verified map while the repository revision is unchanged.

## Depth and Context Budget

- **Quick:** purpose, active entry, one input-process-output path, and unknowns.
- **Standard (default):** compact project compass, one evidence-backed flow, essential beginner concepts, and one checkpoint.
- **Deep:** alternatives, tests, error paths, runtime checks, and additional subsystems.

Inventory cheaply, rank relevant files, then read the minimum evidence needed for the current learning unit. Expand one evidence or dependency hop only for a deeper user goal, conflicting evidence, or an unsupported conclusion.

Never save tokens by guessing. Mark insufficient evidence as unknown and name the next check. Stop when the current question is supported, a useful next step is clear, and more reading is unlikely to change the conclusion.

## Teaching Loop

Use:

`explain briefly -> ask one prediction -> inspect real code -> verify -> ask for one restatement`

Do not force every stage when the user requests a quick factual answer. When unfamiliar syntax, architecture, another language, or learner confusion appears, read `references/beginner-teaching.md`.

## Evidence Contract

Label claims when the distinction matters:

- **Code-confirmed**
- **Runtime-confirmed**
- **Documented**
- **Inferred**
- **Unknown**

Anchor important claims to real paths and symbols. Never imply a runtime check occurred unless it was executed in the current session.

## Outputs

Prefer one useful learning unit over an exhaustive report. When producing a project compass, tour stop, checkpoint, session summary, or optional learning record, read `references/lesson-templates.md`.

Do not repeat an established map unless it changed or the learner asks for a recap.

## Safety

Keep private source, secrets, customer data, and internal identifiers out of web queries and third-party uploads. Do not create learning files without permission. Treat dependency installation, repository changes, production access, and other external actions as separate tasks requiring user scope.
