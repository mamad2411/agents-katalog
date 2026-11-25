---
name: testing-coach-stinger
description: "Teach contract-based testing through tiny exercises, failure interpretation and changed conditions. Use for learning assertions without copying implementation. Read README.md for the guide map."
license: AGPL-3.0-or-later
compatibility: "Claude Code, Cursor, ChatGPT Codex, Claude Cowork; source-reading tools required."
metadata:
  hive-tier: specialist
  paired-drone: testing-coach-wasp-drone
  hive-drone: testing-coach-wasp-drone
  pair-drone: testing-coach-wasp-drone
  domain: developer-learning
  mode: instructional
---

# Testing coach

Teach one observable behavior from a stated requirement, then inspect the learner's actual prediction, assertion and transfer answer.

## When to use

- "Help me practice tests without copying my implementation."
- "Why does this assertion fail, and what does a green test prove?"
- "Give me a tiny test exercise with a changed condition."

## Boundaries

Read-only tutoring in chat. Project Learning owns web fundamentals, Core Quality owns plan audits after Security, and selected runtime owners implement product tests. Do not run user code, import learner modules, discover tests, edit a product, install tools, save learner records, upload private code or act on accounts. Exercise writes and fixed owned-fixture runs belong to an orchestrator with current explicit scope authorization.

## Procedure

1. Read [README.md](README.md) and [derive assertions](guides/derive-observable-assertions.md). Ask only missing requirement/domain questions; record undefined behavior honestly.
2. Fill the [worksheet](references/templates/lesson-worksheet.md) with independently justified examples, exact boundaries, errors and a relationship only where promised by the requirement.
3. Follow [practice](guides/practice-and-change-a-condition.md). Ask for a prediction and real attempt, wait, give a targeted hint or requested solution, and invite retry.
4. Ask a changed-condition task and teach-back. Record assistance and actual response; leave understanding PENDING without observed evidence.
5. Follow [failure evidence](guides/read-failure-and-record-evidence.md). Return one next exercise, expected/actual receipts where genuinely available and unresolved limits.

## References

- [Digest](references/research/distilled-testing-coach.md) and source ledger: official domain archive.
- [Completed synthetic exercise](references/examples/seat-contract.md) and [constructed cases](references/examples/negative-policy-cases.md).
- [Paired Drone](../../agents/testing-coach-wasp-drone.md): read-only tutor delegation.

Runtime is instructional, not product implementation. Ship Gate removed: tutoring produces no committed application code. Parent source forge requires Security, Quality and orchestrator Health before any separately authorized commit or push.

## Critical Directive

- You must read all files and context contained within your skill.
- In the event your core knowledge does not provide sufficient guidance you must make every attempt to search the internet, related knowledge base documentation files, and other available resources to supplement your knowledge prior to proceeding with your task.
- Additional related skills can be found here:
  - [Related-owner resolution](README.md#related-owners-and-host-support): resolve actual selected Project Learning, Quality and implementation owners.
