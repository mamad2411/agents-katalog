---
name: enterprise-debug
description: "Systematic enterprise debugging for bugs, failing tests, and unexpected behavior. Reproduce, trace, scan blast radius, identify root cause, then fix with TDD and prevention records."
---

# Enterprise Debug

## Global Precheck

Before reading further, writing artifacts, delegating, or changing files, run:

```bash
enterprise-precheck --skill enterprise-debug
```

If it exits non-zero, stop and report stderr verbatim. Do not hand-craft packet
files or evidence markers to bypass it.

## Learned Behavior

Load domain-specific lessons before starting:

1. Call `cortex_lessons(tag='feedback:DEBUG')` when available.
2. Apply any returned corrections for this session.
3. If the user corrects this skill, append a domain-tagged lesson to
   `.cortex/knowledge.jsonl`.

## Purpose

Bugs are rarely isolated. Enterprise debug exists to find the root cause, scan
siblings and consumers for the same bug class, and prove the fix with a failing
test that turns green.

Detailed mechanics live in [debug-workflow.md](references/debug-workflow.md).
Load that reference when executing the skill; keep this active prompt lean.

## Required Phases

0. `FEEDBACK LOOP`: build or choose the fastest deterministic pass/fail loop
   before ranking hypotheses. The loop can be a test, API/curl script, CLI
   fixture, worker/job replay, headless browser script, captured trace replay,
   stress loop, or bisection harness. It must assert the user's exact symptom,
   not merely "does not crash".
   Treat the loop as the product: sharpen the assertion, reduce runtime, and
   make it deterministic before investing in hypothesis work.
1. `INVESTIGATE`: reproduce the exact failure with that loop and trace
   execution end to end.
2. `BLAST RADIUS`: inspect same-file siblings, cross-file siblings, validation
   paths, consumers, data flows, and edge cases for the same bug class.
3. `ROOT CAUSE`: state the single root cause and verify it against code/data,
   not memory or migration assumptions.
4. `FIX WITH TDD`: write or update the failing test first, watch it fail for the
   right reason, implement the minimal fix, then run targeted and required
   broader checks.

Do not skip blast radius. Do not ship a symptom patch. Do not count mocks as
proof for schema, query, invoice, order, inventory, or other data-sensitive
bugs.

## Required Source Read

Before coding, read:

- the failing entry point and every runtime layer in the trace
- authoritative query/schema/source-of-truth code for data bugs
- UI components, hooks, routes, and browser/PDF/upload paths for UI bugs
- sibling implementations that should behave the same way
- existing tests, fixtures, and proof gaps
- repo traps, best practices, and relevant vault/memory context

If the bug cannot be reproduced or tied to a source-grounded hypothesis, keep
investigating. If the likely fix changes public behavior, plan/contract must
absorb the new postcondition before build continues.

## Circuit Breaker

Track debug attempts in `.codex/enterprise-state/<slug>.json` when a lane exists.
After three failed fixes for the same root cause or repeated failures on the same
gate, stop and escalate with options:

- redesign the seam
- simplify the behavior
- split the scope
- accept a documented risk
- seek external/domain help

## Output

Write a compact debug report:

```text
docs/reviews/YYYY-MM-DD-<slug>-debug.md
```

Include:

1. Bug and reproduction
2. Feedback loop artifact: command/script/replay, assertion, speed, and
   determinism notes
3. Execution trace with files/functions read
4. Root cause and why it is not a symptom
5. Blast radius scan and affected siblings
6. Fix plan and TDD evidence
7. Verification evidence, including live/integration DB or headless browser proof
   when required
8. Prevention record: what would have caught this earlier, and whether a trap,
   gate, eval, or follow-up was added

## Handoff

- If the fix is narrow and contract exists, return to `enterprise-build`.
- If the bug revealed missing requirements, update plan/contract before coding.
- If verification proves the fix, proceed through review, forge, verify, harness,
  and compound as required by the lane.
