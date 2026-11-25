---
name: skill-creator
description: Guide for creating effective skills that extend Codex with specialized workflows, domain knowledge, references, scripts, or assets.
---

# Skill Creator

Use this skill when creating a new skill or updating an existing skill.

## Core Principles

- Keep `SKILL.md` concise. Add only context the agent needs to execute the workflow reliably.
- Match specificity to risk: use prose for flexible judgment, references for deeper domain material, and scripts for fragile repeated operations.
- Prefer progressive disclosure. Put the trigger, workflow, and routing guidance in `SKILL.md`; put lengthy details in directly linked files under `references/`.
- Keep bundled files purposeful. Avoid extra README, changelog, quick-reference, or installation docs unless the skill actually needs them at runtime.
- Validate with realistic prompts or automated checks when possible.

## Skill Anatomy

Every skill needs:

```text
skill-name/
├── SKILL.md
├── agents/
│   └── openai.yaml
├── scripts/
├── references/
└── assets/
```

`SKILL.md` must include YAML frontmatter with `name` and `description`. The description should say exactly when the skill should be used.

`agents/openai.yaml` is recommended for UI metadata. Keep the display name, short description, and default prompt aligned with `SKILL.md`.

Use optional folders only when needed:

- `scripts/`: deterministic helpers or repeatedly generated code.
- `references/`: large or conditional guidance that should be loaded only when relevant.
- `assets/`: templates or files used to produce outputs without reading them into context.

## Workflow

1. Define the skill's job, users, triggering requests, inputs, outputs, and explicit non-goals.
2. Decide what belongs in `SKILL.md` versus `references/`, `scripts/`, and `assets/`.
3. Write frontmatter first. Make the description specific enough that an agent can decide whether to load the skill.
4. Write a short operational workflow with the minimum required rules, safety constraints, and validation steps.
5. Add referenced resources only when they reduce context load or make behavior more reliable.
6. Add or update `agents/openai.yaml` so the UI metadata matches the skill.
7. Validate with at least one realistic prompt and, for repository changes, run focused tests or linting that cover discovery and packaging.

## Quality Checklist

- The skill has a clear trigger and does not overlap unnecessarily with broader skills.
- The body is under 500 lines unless the complexity is unavoidable.
- Every referenced file is directly linked or named from `SKILL.md`.
- Scripts are executable when they need to be run directly.
- Examples are small, realistic, and not the majority of the skill.
- The final skill can be understood without hidden conversation context.
