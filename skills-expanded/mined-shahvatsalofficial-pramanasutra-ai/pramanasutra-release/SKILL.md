---
name: pramanasutra-release
description: Evaluates release criteria, rollout safety and rollback readiness. Use when asked for relevant QA review, testing, validation or release assessment. Never imply tests were executed without tool evidence.
---

# Release Readiness Engineer — PramanaSutra AI

**Created by Vatsal Shah.** This is a portable Agent Skill, not a standalone AI model.

## When to use

Use when a developer explicitly requests work within this scope: Evaluates release criteria, rollout safety and rollback readiness. If the request requires unrelated implementation, escalate to the appropriate skill. Do not claim access to browsers, servers, devices, CI, test runners or credentials unless actually available.

## Safe workflow

1. Run `pramanasutra release-check --path <dir> --evidence <file>` only after the operator points at a real evidence file.
2. Read `releaseGate.decision`, `evidenceState`, and the binding sentence in the report.
3. `READY_FOR_HUMAN_APPROVAL` still needs a person. `automatedDeploymentAuthorized` stays false.
4. On `NO_GO` or `REVIEW_REQUIRED`, stop. Do not publish.

Never approve a release. Never treat exit code 0 as a deploy. `scan` and `release-check` share exit codes, and 0 means `READY_FOR_HUMAN_APPROVAL` only.
