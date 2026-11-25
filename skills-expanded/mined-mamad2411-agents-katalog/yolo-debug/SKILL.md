---
name: yolo-debug
description: Use when a reported problem, failure, or bug needs a systematic root-cause investigation — reproduce → isolate → fix → verify — recorded as one durable artifact. Triggers on "fix the 500 on login", "X is broken", "why is Y failing?", "debug this", "track down this bug".
---

# yolo-debug

Find the *true cause* of a failure and fix it with evidence — not by guessing. A stateless
investigation act: it produces ONE debug record plus the fix, and stores no session state.

## Inputs
A bug report or failing behaviour. Derive a kebab-case `slug` for the record filename — there
is **no brief** (a debug is not a feature). Run on the **current branch** (see
`.claude/yolo/conventions.md` — a debug record never touches status derivation). If the work
turns out to add new capability rather than restore intended behaviour, **hand off to
`yolo-feature`**.

## Procedure
Work the arc in order; each step's output feeds the record.
1. **Reproduce** — get a deterministic repro (a failing test, a command, exact steps). No repro → no confirmed bug yet; say so rather than guessing.
2. **Hypothesize** — list candidate causes; rank by likelihood and cost-to-check.
3. **Isolate** — trace to the true cause with a concrete **evidence chain** (`file:line` → observed value → why it's wrong). Bisect or instrument as needed.
4. **Fix** — make the **minimal** change that addresses the root cause, not the symptom. Note the over-scope traps you avoided.
5. **Verify** — the failing reproducer now passes, the symptom is gone, and the wider suite stays green.

**The Iron Law:** no root-cause claim without a `file:line` evidence chain; no fix without a
failing reproducer that the fix flips to green; never patch the symptom while the cause stands.
Failing-test-first is the default — if a bug is genuinely not unit-testable (config, perf,
flake, environment), record *why* in the artifact and substitute the strongest available
evidence (a before/after command, a metric, a log excerpt).

## Discipline (the traps that end investigations early)
- "It's probably X" without checking is a guess, not a cause — confirm before you fix.
- The first plausible cause is not always the cause — confirm it explains the symptom *fully*.
- A green fix with no reproducer proves nothing — you may have moved the bug, not killed it.
- Red flags to stop and re-examine: the fix touches unrelated files; the bug "can't be reproduced but is fixed"; the explanation needs a "this should never happen".

## Output
Write exactly ONE artifact — `workspace/debug/<YYYY-MM-DD>-<slug>.md` (`mkdir -p` its dir) —
with: symptom + reproducer, the evidence chain (`file:line`), a one-sentence root cause +
confidence, the fix (files, the minimal change, over-scope avoided), and verification evidence.
Commit the record `yolo: debug <slug>`; the fix lands as ordinary descriptive commit(s) on the
current branch.

## Constraints
- Cite `.claude/yolo/conventions.md` for the commit form and the standalone-record rules; do
  not restate trailer strings. A debug record carries no trailer, no brief, no tracked state.
- Stateless: no persistent session or run-state files — the committed record plus the fix
  commit are the entire trail.
- Hand off to `yolo-feature` the moment the work becomes new capability rather than a fix.
