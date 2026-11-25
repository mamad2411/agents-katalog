---
name: pr-merge-gate
description: Apply a strict pull-request review and merge gate using diffs, tests, and validation truth. Use when deciding whether a branch is ready to merge.
---

# pr-merge-gate

Read diff and tests. Apply quality, security, performance, concurrency, API, database, DX, and supply-chain personas as needed. Produce pass/fail/blocked verdict with evidence.

Primary prompts:

- `prompts/31_pull_request_review_and_merge_gate.md`
- `prompts/26_code_review_quality_gate.md`
