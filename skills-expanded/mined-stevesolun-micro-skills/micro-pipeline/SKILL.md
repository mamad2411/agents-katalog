---
name: micro-pipeline
description: "Gated micro-skill pipeline system. Auto-triggers when building, generating, or creating any multi-step output (documents, code, presentations, reports). Enforces a Scope-Plan-Build-Check-Deliver pipeline where each step has a pass/fail gate. Use this whenever the output quality matters and the task has more than one component."
---

# Micro-Skill Pipeline

When this skill triggers, execute the following gated pipeline.
One step at a time. Do NOT skip ahead.

## Pipeline

1. **Scope** -- Read `references/01-scope.md`. Extract constraints from the request.
2. **Plan** -- Read `references/02-plan.md`. Design the approach. Map components.
3. **Build** -- Read `references/03-build.md`. Execute with micro-checks per component.
4. **Check** -- Read `references/04-check.md`. Answer every gate question YES or NO. Any NO = fix before proceeding.
5. **Deliver** -- Read `references/05-deliver.md`. Finalize and present output.

## Failure Log

Look for a `failure-log.md` in the current project root or skill directory.
If it exists, read it before starting. Every listed pattern is a mandatory check constraint.

## Rules

- Read each reference file when you reach that step, not all at once.
- Step 4 (Check) is the hard gate. "Mostly yes" counts as NO.
- On Check failure: fix, re-run full checklist, then append a one-line pattern to `failure-log.md`.
- For simple single-component tasks, collapse Scope+Plan into one step but never skip Check.
