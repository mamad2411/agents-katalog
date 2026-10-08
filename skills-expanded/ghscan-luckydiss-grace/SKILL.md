---
name: protocol-grace-patch-safety
description: Canonical GRACE protocol for semantic patch safety using anchor-bounded mutation instead of line-number-driven edits.
---

# Skill: protocol-grace-patch-safety

## Purpose
Prevent unsafe edits in long-context or RAG-driven patch workflows.

## MANDATORY RULES
- Treat `MC-*`, `FC-*`, and `BA-*` ids as the primary patch coordinates.
- For non-trivial edits, mutate code only within the approved semantic region.
- Prefer anchor-bounded replacements over line-number-driven replacements.
- If a requested patch would cross semantic boundaries unexpectedly, stop and escalate.

## Safety heuristic
- Small local edit: may target a single `BA-*`
- Behavioral edit: must account for owning `FC-*`
- Contract or boundary edit: must account for owning `MC-*` and linked artifacts
