---
name: speckit.uat
description: UAT Analyzer - Convert manual acceptance evidence into verified gaps, decisions, and scoped follow-up tasks.
---

## Mission
Compare what users actually experienced with approved acceptance criteria and preserve the distinction between defect and new scope.

## Inputs and Outputs
- Read spec success criteria, tasks, test/review evidence, and manual notes/screenshots at `.agents/verification/[phase]-UAT.md`.
- Write an acceptance report and a linked gap task list for `speckit.implement`.

## Protocol
1. Record actor, environment, build/revision, preconditions, exact steps, expected result, observed result, and evidence for each scenario.
2. Classify each mismatch as UI/UX defect, logic defect, integration/environment issue, regression, or new requirement; assign severity and confidence.
3. Re-test failed scenarios after fixes and preserve original evidence. Do not infer pass from absence of feedback.
4. For confirmed gaps, define minimal task, affected path, acceptance check, dependency, and owner. Link new requirements back to a new or amended spec.
5. Mark a phase accepted only when all core criteria have explicit user or authorized stakeholder approval.

## Completion Gate
Every core scenario has pass/fail/blocked status with evidence; gaps are classified, linked, and actionable.

## Guard Rails
Do not silently change spec intent, label new scope as a bug, or mark UAT complete without approval evidence.