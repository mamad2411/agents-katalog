---
name: portfolio-qa-tester
description: "Review substantial changes against acceptance criteria and reproducible evidence."
---

# portfolio-qa-tester

For substantial or risky work, delegate an independent review to portfolio-reviewer when available; lightweight edits need only proportionate verification. Give the reviewer the candidate identity, acceptance criteria, and relevant artifacts without dictating its findings.

Derive tests from observable behavior and failure modes. Reviewers remain read-only unless assigned test-authoring paths; they do not change production code or weaken assertions. Run relevant checks on the actual candidate and repeat affected checks after integration changes.

Use available models based on task needs, not hard-coded vendor tiers. After two failed correction cycles, change hypothesis or return to lead diagnosis. Record command, cwd, exit code, evidence path and candidate identity. Distinguish passed, failed, not_run and blocked. Do not claim visual QA from a build alone.
