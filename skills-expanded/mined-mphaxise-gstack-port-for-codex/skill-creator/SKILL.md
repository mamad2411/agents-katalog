---
name: skill-creator
description: GBrain-inspired skill authoring for Codex. Use when creating or extending a skill in this repo while keeping the package coherent.
---

# Skill Creator

Use this skill when creating a new skill or expanding the current skill surface.

This port is adapted from `garrytan/gbrain` at commit `b7e3005b5b3f1b54082f9c5990482ebf81a4a807`.

## Workflow

1. Check whether the requested capability already belongs in an existing skill.
2. If a new skill is warranted:
   - create `skills/<slug>/SKILL.md`
   - add concise frontmatter with `name` and `description`
   - write the workflow and guardrails clearly
3. Update the relevant registry in `data/`.
4. Update resolver or compatibility docs if routing changed.
5. Run repo validation and tests.

## Guardrails

- Do not create overlapping skills when extending an existing one is cleaner.
- Keep the skill concise and Codex-native instead of copying upstream ceremony verbatim.
- Update the package metadata when the skill surface changes.
