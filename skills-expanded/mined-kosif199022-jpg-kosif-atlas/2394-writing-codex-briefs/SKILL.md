---
name: writing-codex-briefs
description: Use when composing the task brief and acceptance criteria for a Codex dispatch (invoked from dispatching-to-codex). Covers the self-contained brief format and how to write acceptance checks that actually protect you — weak checks are the sneakiest way a dispatch goes wrong.
---

# Writing Codex Briefs

Codex sees **zero** chat history. The brief is the only channel. Anything not in it does not exist for Codex.

## The Acceptance File — `.codex/ACCEPTANCE.md`

Written and committed BEFORE dispatch. This is the frozen bar the judge will enforce.

```
GOAL: <one sentence: what "done" means>

CHECKS (all must pass, exact commands):
- `<command>` exits 0 and prints <expected>
- `<build/typecheck command>` exits 0
- `<specific test command>` exits 0

CONSTRAINTS:
- Only edit <files/dirs>. Do not modify <test files / this file / unrelated code>.
```

**Writing checks that protect you** (the judge is only as strong as these):
- Prefer commands with **exit codes** over "the code should look right".
- Include at least one check that **fails before the work is done** (red → green) — a check that passes on the untouched repo proves nothing.
- Name the *specific* tests, not "run the tests" (slow suites make the judge cry wolf; flaky checks are worse than none).
- Vacuous bars ("typecheck passes") let bad work through with a green light. Ask: *could a lazy stub pass these checks?* If yes, tighten them.

## The Brief

```
GOAL: <same one sentence — must match ACCEPTANCE.md>
CONTEXT: <repo path, key files, constraints — everything Codex needs, it cannot ask you>
DO: <numbered, concrete steps>
VERIFY: <run the exact CHECKS above and show their real output>
REPORT: <what to return: diff summary + which checks passed>
DO NOT: commit anything; touch .codex/ACCEPTANCE.md; edit unrelated files;
        delete or weaken tests; add silent fallbacks or fake/stubbed results.
```

The `DO NOT` block is mandatory and always includes those five items — they are the exact ways executor models paper over failure.

## Common Mistakes

- **Context by reference** ("as discussed above") — Codex has no "above". Inline it.
- **Goal drift** — brief GOAL ≠ ACCEPTANCE GOAL means the judge enforces a different bar than Codex aimed at.
- **Kitchen-sink briefs** — one dispatch, one goal. Two unrelated goals = two dispatches.
