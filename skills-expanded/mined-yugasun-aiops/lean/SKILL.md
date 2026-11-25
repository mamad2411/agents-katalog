---
name: lean
description: >
  Minimal solution discipline: YAGNI ladder, stdlib and native first, shortest
  working diff. Use during delivery when writing code, or when the user says
  lean, lean mode, yagni, lazy mode, or complains about over-engineering.
license: MIT
---

# Lean

The smallest working change. Efficiency is not carelessness. Active during **delivery** in the aiops bundle; **off** during grill/alignment.

## Ladder

Stop at the first rung that holds:

1. Does this need to exist? (YAGNI)
2. Stdlib does it?
3. Native platform feature?
4. Already-installed dependency?
5. One line?
6. Minimum code that works

## Rules

- No unrequested abstractions, boilerplate, or speculative "for later" code
- Deletion over addition; shortest working diff
- Mark deliberate shortcuts: `// lean: <ceiling and upgrade path>`

## Output

Code first, then at most three lines: what was skipped, when to add it.

## Never cut

Trust-boundary validation, data-loss prevention, security, accessibility, explicitly requested behavior.

## Intensity

`/lean lite|full|ultra` — default **full**. Off: "stop lean" / "normal mode".
