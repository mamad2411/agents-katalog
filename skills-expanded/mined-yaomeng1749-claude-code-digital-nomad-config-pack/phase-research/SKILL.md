---
name: phase-research
description: Phase 1 of the software delivery workflow: understand a requested feature, bug fix, or technical change by searching existing implementations, reading project context, checking relevant docs, questioning requirements, and producing a research report before planning.
origin: ECC automation-pack
---

# Phase Research

Use this skill when the user asks for `/phase-research`, phase research, requirement understanding, implementation research, or the first stage of an automated software delivery flow.

## Purpose

Turn a request into grounded context before design or implementation.

## Workflow

1. Search for existing implementations in the current repo.
2. Search external examples when useful, preferring primary documentation and reputable source code.
3. Read project context: `AGENTS.md`, `CLAUDE.md`, `README`, package manifests, docs, and nearby code.
4. Check framework/library documentation when the request depends on specific APIs.
5. Question the requirement:
   - What user or system need does it satisfy?
   - Which parts are required now?
   - Which parts look like premature scope?
   - What is the simplest viable implementation?
6. Produce a concise research report.

## Output

Include:

- current repo findings
- relevant external references
- feasible implementation options
- recommended direction
- major risks and unknowns
- requirements that should be simplified, clarified, or removed

End with `PHASE_RESEARCH_DONE` when the report is complete. If research is blocked, output `PHASE_RESEARCH_BLOCKED` and list the blocker.
