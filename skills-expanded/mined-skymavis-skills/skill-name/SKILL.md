---
name: skill-name
description: >-
  One sentence on what this skill does, then when to use it. The description is the trigger surface
  an agent matches against, so be specific and write it in the third person. Rename this skill's
  folder and set name to match (kebab-case).
---

# Skill name

A one-paragraph overview of what this skill provides and the problem it solves. Keep this file lean
(under 500 lines) and push depth into `references/` — the body is the entry point, not the manual.

## When to use

- Trigger or task #1 this skill is for.
- Trigger or task #2.

## How it works

- Executable logic lives in `scripts/`.
- Deeper docs an agent loads on demand live in `references/`.
- Files or templates the skill emits live in `assets/`.
- Tests live in `tests/` (a `conftest.py` puts `scripts/` on the path).

## Layout

```
skill-name/
  SKILL.md            # this file — entry point + when-to-use
  scripts/            # the runnable tool(s)
  references/         # depth, loaded on demand
  assets/             # templates / files the skill emits
  tests/              # pytest suite
  requirements-dev.txt
```
