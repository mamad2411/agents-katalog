---
name: cosmosmith-qa-verifier
description: Verify Cosmosmith tasks against acceptance criteria and produce QA evidence. Use when a task is in review/verify status, before marking work done, or when exploratory, browser, API, regression, or release confidence checks are needed.
---

# Cosmosmith QA Verifier

## Purpose

Convert acceptance criteria into verification evidence.

## Workflow

1. Read `task.md`, `proposal.md`, `design.md`, and changed artifacts or code.
2. Select tasks in `review` or `verify`.
3. Use web research for current testing tools, browser behavior, accessibility rules, API standards, or platform-specific QA expectations when needed.
4. Build a test matrix from acceptance criteria.
5. Run automated and manual checks that fit the risk.
6. Write `docs/cosmosmith/qa-report.md` or update task evidence.
7. Reopen tasks with clear reproduction steps when checks fail.

## Evidence Rules

- Include command, result, environment, and observed behavior.
- Separate expected and actual behavior for bugs.
- Do not mark tasks done without evidence.

## Completion

Stop when each reviewed task is accepted with evidence or reopened with a concrete bug report.

