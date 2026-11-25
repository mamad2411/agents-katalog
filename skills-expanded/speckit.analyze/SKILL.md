---
name: speckit.analyze
description: Consistency Checker - Audit spec, plan, tasks, constitution, and evidence for gaps and conflicts.
---

## Mission
Produce a reproducible, read-only consistency audit before implementation.

## Inputs and Outputs
- Read `spec.md`, `plan.md`, `tasks.md`, constitution, and referenced artifacts.
- Write `.agents/memory/analyze-report.md` and print a gap table with coverage score.

## Protocol
1. Validate files, headings, IDs, user-story links, paths, and dependency references; report malformed inputs.
2. Map every requirement and scenario to a plan section and task. Mark missing, ambiguous, conflicting, or unverified links.
3. Compare technical choices and gates against constitution, security, Docker, ENV, and scope rules.
4. Reconcile data models, contracts, migrations, tests, and operational tasks; calculate `matched / total * 100`.
5. Classify gaps as Critical/High/Medium/Low and propose the smallest corrective artifact without editing source files.

## Completion Gate
Coverage is complete only when every requirement has a traceable plan and task, all conflicts are listed, and the report states its evidence limits.

## Guard Rails
Read-only. Never silently infer missing requirements or edit spec, plan, tasks, or code.