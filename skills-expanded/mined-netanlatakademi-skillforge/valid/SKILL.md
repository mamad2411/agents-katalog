---
name: valid-skill
description: Use this skill when you need a minimal, correct example of a SkillForge skill to compare against.
license: MIT
compatibility:
  - codex
  - claude-code
metadata:
  author: skillforge
  version: 1.0.0
allowed-tools:
  - filesystem.read
---

# Valid Skill

A minimal skill that satisfies every mandatory rule. It exists so tests have something that must
produce zero errors, and so a new contributor has a correct file to copy.

## Workflow

1. Read the request.
2. Do the smallest useful thing.
3. Report what changed.

## References

- [Notes](references/notes.md)
