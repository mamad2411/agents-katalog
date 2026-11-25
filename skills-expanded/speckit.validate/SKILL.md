---
name: speckit.validate
description: Implementation Validator - Decide whether implementation satisfies spec, governance, build, runtime, and evidence gates.
---

## Mission
Produce the final evidence-based validation verdict before release or handoff.

## Inputs and Outputs
- Read spec, plan, tasks, source, constitution, project config, reports, and documented commands.
- Write `.agents/memory/validation-report.md` with a requirement matrix, evidence links, blockers, limitations, and verdict.

## Protocol
1. Verify task state and map every success criterion to implementation and evidence; unchecked tasks or missing evidence are blockers.
2. Discover project capabilities and mark non-applicable build, runtime, health, Docker, or framework checks as N/A with reason.
3. Run applicable formatter, type-check, lint, test, build, migration, and security checks in Docker where required; capture exit codes and logs.
4. Start runtime only when configured, wait on a bounded health/readiness condition, and inspect logs immediately on failure. Never use sleep alone as readiness proof.
5. Check constitution, ENV/secret handling, non-root runtime, accessibility/responsive evidence, and rollback/recovery requirements as applicable.
6. Verdict is PASS only when all applicable gates pass and no requirement lacks evidence; otherwise FAIL with severity, owner, and next action. N/A never counts as PASS.

## Completion Gate
The report is reproducible, each claim cites evidence, limitations are explicit, and the verdict does not exceed what was actually verified.

## Guard Rails
Read-only. Do not approve unfinished tasks, failed applicable checks, or unsupported assumptions. Do not treat a checkbox alone as delivery evidence.