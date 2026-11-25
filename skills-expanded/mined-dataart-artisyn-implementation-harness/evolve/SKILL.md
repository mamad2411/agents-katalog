---
name: evolve
metadata:
  internal: true
description: Improve harness skills, agents, workflows, and conventions from observed friction or a concrete improvement request. Supports reflect, triage, validate, and adopt; use for harness improvements rather than ordinary product changes.
---

# Evolve

Turn observed practice into a validated, integrated harness improvement.

Route $ARGUMENTS with [the stage router](references/00-router.md). Load only the
current stage, its required interfaces, and relevant source files. Bare /evolve
triages pending reflections; clarify the candidate
when several match. Reflect is a capture-only operation. An explicit stage runs
that stage only. Triage includes drafting and stops with inactive candidates by
default. Validation and adoption run when requested. There is no session-continuation
or automatic phase-resumption protocol.

For candidate work, apply [native task tracking](patterns/task-tracking.md). Record decisions and evidence in
the candidate report before a handoff. File presence alone does not prove completion.

Existing user authorization governs execution. Request acceptance of the concrete
candidate before adoption unless already authorized. Preserve project-specific
instructions and respect the selected provider's paths and root instruction file.

The lifecycle ends with verified local adoption.
