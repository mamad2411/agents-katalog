---
name: documentation-maintenance
description: Keep repository-visible docs current, concise, and aligned with implementation and validation evidence.
---

# Documentation Maintenance

## Purpose
Keep docs accurate without turning them into a parallel source of truth.

## Read
- `AGENTS.md`
- project grounding file
- relevant design docs
- relevant implementation and validation evidence

## Do
1. Update docs only where the implementation or contract changed.
2. Keep wording concise and factual.
3. Preserve authority boundaries between docs and runtime code.
4. Match terminology across docs and implementation.
5. Remove stale references and duplicate explanations.

## Outputs
- Doc deltas tied to behavior changes
- Stale references removed
- Consistency gaps called out

## Rules
- Do not pad docs with speculative detail.
- Do not let docs drift from validated behavior.
