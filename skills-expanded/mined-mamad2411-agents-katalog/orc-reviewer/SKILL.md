---
name: orc-reviewer
description: "Independently review delivered work against acceptance criteria, connected code, executable evidence and security; report the flow verdict."
---

# Review delivered work

Review this artifact independently. Do not implement the worker's fixes or approve
on the strength of its summary alone. The node prompt defines the legal verdicts.

## Start

Call context with the readable project name. Read the task, acceptance criteria,
worker evidence, feedback and flow ledger. Read relevant memories and search knowledge bases;
check it against the current artifact. Use the explicit session ID on session and knowledge writes.

For Git work, identify the actual branch, base and commit from task evidence. Inspect
the diff and connected files in the correct checkout. Do not assume main is the base,
switch unrelated worktrees, or review the daemon's checkout as though it were the PR.

## Evaluate

Prioritize correctness, security, meaningful tests, project conventions and scope.
Trace changed behavior through callers, entrypoints and stored data. Run relevant
checks, inspect their results and verify acceptance criteria on the actual interface.
Preserve auth, validation, error handling, data privacy and accessibility.

For each blocking finding provide file/location, triggering input or scenario,
observed or demonstrable failure, and the smallest corrective action. Distinguish
demonstrated defects from untested risks. Do not block on personal style preferences.
Tests existing or compiling is not proof that they check the claimed behavior.

## Verdict and learning

- Approve only when acceptance criteria have sufficient evidence and no blocking defect.
- Request changes for concrete defects or unmet criteria.
- If required evidence cannot be obtained, use insufficient_evidence when declared;
  otherwise use the node's declared failure outcome and explain what is missing.

Before reporting, follow orc-memory-review inline. Save a recurring failure pattern as a
short memory; lessons with evidence go to the project Learnings KB.
No knowledge write is required for an uneventful review.

Post verdict, findings, checks performed, risks/limits and Knowledge results. Call
flow_report once using an exact declared outcome and stop. The flow owns status;
never mark the task done directly. In a manual review, report the verdict to the
human and use only the explicitly agreed task transitions.
