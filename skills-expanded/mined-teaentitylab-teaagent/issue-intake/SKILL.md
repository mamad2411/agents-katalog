---
name: issue-intake
description: Parse a GitHub-style issue into a structured task, detect ambiguity by category, and generate an acceptance checklist and command suggestions. Documents the deterministic intake owned by the harness.
---

# Issue Intake

Reviewed procedure asset for `teaagent.domain.issue_intake` (ADR-0041 Phase 2).
Issue parsing, ambiguity categorization, and checklist generation are
**deterministic** and fully tested, so they remain in the harness; this skill
documents the procedure as a reviewed supply-chain asset. The optional GitHub
fetch is gated by `GITHUB_AVAILABLE` and the intake API boundary stays in the
harness.

## Procedure

1. **Parse** the issue (title + body) into a structured task. When the GitHub
   library is available and configured, fetch by number; otherwise accept raw
   text.
2. **Detect ambiguity** by `AmbiguityCategory` (e.g. unclear scope, missing
   acceptance criteria, undefined terms) and emit an `AmbiguityReport`.
3. **Generate** an `AcceptanceChecklist` of concrete, checkable criteria.
4. **Suggest** candidate commands/next steps for the resolved task.

## Contract

The deterministic implementation in `teaagent.domain.issue_intake` is the source
of truth, exercised by `tests/test_issue_intake.py` and
`tests/acceptance/test_issue_to_plan_acceptance_flow.py`. This skill is the
reviewed documentation of the intake procedure, not a runtime replacement.
