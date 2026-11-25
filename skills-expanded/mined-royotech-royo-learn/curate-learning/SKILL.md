---
name: curate-learning
description: Review captured learning, compare it with existing knowledge and Engram, validate evidence, reject noise, resolve duplicates or conflicts, and approve an exact destination. Curating never writes Skills or AGENTS.md.
license: MIT
metadata:
  author: RoyoTech
  version: "3.0.0"
  mcp_profile: agent
---

# Curate Learning

## Workflow

1. Load the candidate with `learning_get`.
2. Search related learnings and Engram.
3. Identify relation: new, duplicate, extends, supersedes, contradicts, narrows, related.
4. Validate using tests, diffs, documentation, reproduction, or independent cases.
5. Decide exactly one:
   - reject;
   - needs evidence;
   - merge;
   - approve project/shared knowledge;
   - approve new/update Skill;
   - approve AGENTS rule;
   - approve regression test.
6. Define exact destination, acceptance checks and rollback condition.
7. Call `learning_curate`.

## Destination rules

- project facts and status → project knowledge or Engram;
- repeatable procedure → Skill;
- short mandatory invariant → AGENTS.md;
- evidence too weak → needs evidence;
- duplicate → merge/reject;
- preference → personal/project unless user explicitly universalizes it.

A universal rule requires stronger evidence than a project note.

Do not publish.
