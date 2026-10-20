---
description: AparadhKavach governing conventions for aparadhkavach-data-generator
globs:
alwaysApply: true
---

# Source of truth

`AGENTS.md` at this repo's root is authoritative — pipeline order,
demographic independence as a product requirement, legal-code derivation,
date realism, and which Notion sections to fetch, derived from ADR-008/015
and Section 4. Read it before modifying any script. This file adds
Cursor-specific behaviors only.

# Working behaviors specific to this repo

- **Notion MCP access is read-only by token config, and must never be
  treated as writable regardless of what's asked.** Fetch fresh each
  session per AGENTS.md's section list; treat content as authoritative.
- **Never loosen a guardrail_validator.py threshold to make a run "pass."**
  If a chi-square check is failing, the fix is in `generate_entities.py` or
  `weave_relationships.py`'s sampling logic, not in the validator's threshold.
  Flag a persistent failure explicitly rather than adjusting the bar.
- **Don't add demographic correlation logic "for realism."** If asked to make
  the dataset "feel more natural," achieve that through narrative variety or
  event-context modeling (already-approved patterns), not by correlating
  demographic fields — that directly undermines the IP-004 patent claim.
- **This repo has no CI/CD pipeline by design** — don't add one, and don't
  suggest one as a "best practice" improvement.