---
name: testing
description: GBrain-inspired skill conformance checks for Codex. Use when validating the growing combined GStack and GBrain skill surface.
---

# Testing

Use this skill when validating that the skill package still hangs together after changes.

This port is adapted from `garrytan/gbrain` at commit `0b47afbf402a4e27a648bb9d131ce584461461ea`.

## Workflow

1. Validate required docs and registries.
2. Check that every `ported` skill has a real `SKILL.md` with valid frontmatter.
3. Run the lightweight repo checks:
   - `python3 scripts/validate_repo.py`
   - `python3 -m unittest discover -s tests`
4. If the surface changed materially, inspect `python3 scripts/print_status.py`.
5. When a downstream project carries a native plugin manifest, validate the
   skill list without dropping unrelated required fields such as plugin id,
   object configuration schema, or declared contracts.
6. Report failures concretely and in priority order.

## Current Upstream Coverage

Support two explicit modes: skill-conformance validation for this port and project test-suite health for downstream repositories. For project health, separate fast/unit, integration, end-to-end, and slow/nightly tiers; preserve regression history and never treat a partial tier as the complete suite.

## Guardrails

- Do not declare the package healthy without running the checks.
- Prefer structural issues and regressions over style notes.
- Keep the validation rules aligned with the real repo structure.
