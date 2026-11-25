---
name: audit-deck
description: Audit an existing medical slide deck (HTML or PPTX) for AI-slop patterns, wrong numbers, unverifiable references and patient identifiers.
disable-model-invocation: true
---

Ask for the deck file if it was not given, and for the source papers if the user has them.

Then call the Skill tool twice: once with "slop-audit" and once with "evidence-audit". Run them
as two independent subagents if your harness can. If there is no Skill tool, read each
skill's `SKILL.md` and follow it.

Report blocking findings first, then advisory ones, then which sources you could not check.
