---
name: superforge-debug
description: >
  Root-cause-first debugging with FailForward learning memory, which recalls
  past failures before diagnosing and records new ones after, in a committed
  docs/failforward.md that survives the session. Forbids trial-and-error
  patching and dummy fallbacks that mask symptoms. Covers the bugs the protocol
  cannot start on — what to do when it will not reproduce, how to bisect "it
  used to work", and when to stop debugging and ship a recorded mitigation
  instead. Use when the user says "bug", "error", "it crashes", "build fails",
  "test is failing", "not working", "why does this happen", "still broken",
  "can't reproduce", "only in production", "intermittent", "バグ", "エラー",
  "動かない", "落ちる", "直らない", "なぜか失敗する", "再現しない", "たまに落ちる",
  or runs /superforge-debug.
license: MIT
metadata:
  author: Takao Umehara
  version: "3.0"
compatibility: >
  Standalone.
  Writes docs/failforward.md. The failforward CLI is optional; without it, the file is the memory.
---

# Superforge Debug — Systematic Debugging & FailForward Memory Engine

Use this skill whenever an error, bug, test failure, or unexpected behavior occurs. NEVER apply trial-and-error edits or mask symptoms with dummy fallbacks.

---

## 1. FailForward Memory Pre-Flight (Mandatory)

Before forming diagnostic hypotheses, read the project's failure log:

**`docs/failforward.md`** — committed, in the repository. This is the memory,
and it works whether or not any CLI is installed. Thirty seconds of reading it
before hypothesising is the entire reason it exists, because the thing it
records is not the list of past fixes but the list of **past wrong first
guesses**, and those repeat.

If the local FailForward CLI is available, query it as well:

```bash
failforward recall "<error keyword or component name>"
```

If a relevant past failure is recalled:
- Apply the verified lesson immediately.
- Mark as useful via `failforward useful <id>`.

The file's entry format, and why the `Looked like` line is the one that pays →
**`references/failforward.md`**.

---

## 2. 4-Phase Empirical Debugging Protocol

### Phase 1 — Log Extraction & Inspection
- Read the FULL, un-truncated log or stack trace.
- Extract exact error symbols, line numbers, and file locations.

### Phase 2 — Reproduce & Isolate
- Isolate the minimal reproduction case.
- Trace upstream data flow to pinpoint where the contract was broken.
- **If it will not reproduce, do not proceed to Phase 3** — a fix formulated
  without a reproduction cannot be verified. Narrow what "sometimes" means,
  match the environment one variable at a time, or instrument and wait
  (`references/failforward.md` §2). For "it used to work", stop reasoning about
  the code and bisect (§3 there).

### Phase 3 — Root-Cause Fix Formulation
- Diagnose based strictly on empirical log evidence.
- Fix the underlying contract failure. Never swallow exceptions or bypass assertions.

### Phase 4 — Verification & FailForward Recording
- Run tests to confirm clean success — **and re-run the original reproduction**,
  not only the new test.
- Append the entry to `docs/failforward.md`, including `Looked like` and
  `Locked by` (write 無し deliberately if no test locks it).
- If the CLI is present, record it there too:
  ```bash
  failforward record \
    --category <build|type|test|lint|logic|debug|other> \
    --severity <p0|p1|p2|p3> \
    --symptom "<What happened>" \
    --cause "<Why it happened>" \
    --fix "<How it was fixed>" \
    --context "<File/function>" \
    --scope project
  ```

---

## When the failforward CLI is unavailable

Nothing is lost. `docs/failforward.md` is the memory; the CLI is an index over
it. Skip recall and record the entry in the file as normal. Never let a missing
tool stop the diagnosis, and never let it stop the recording either — the tool
was always the replaceable half.

---

## Deeper reference

**`references/failforward.md`** — where the memory lives and the entry format
(including `Looked like`, the field that makes the log compound), the ordered
procedure for a bug that will not reproduce, `git bisect` for "it used to work"
and the two ways it goes wrong, the elapsed-time table for when to stop
debugging, and the two rules the four phases assume but never state: change one
thing at a time, and never leave a "fix" you cannot explain.

---

## 3. Production Incident Resilience & Post-Mortem Engine (PIR Engine)

For production outages or major system failures:
- Conduct a 5-Whys Root Cause Analysis.
- Document Chronological Timeline and Time to Recovery (TTR).
- Produce a blameless post-mortem report in **`docs/postmortem.md`**.

See post-mortem structure & guidelines → **`references/postmortem-guide.md`**.

---

## Artifact

**`docs/failforward.md`** — one entry per bug that took more than a few
minutes, appended, never deleted. For production incidents, also generate **`docs/postmortem.md`**.

A fix nobody can find again will be rediscovered the hard way. This file is
also carried forward by `superforge-handoff`, so what a session learned about
the codebase survives the session.

## Delegate when a sharper skill is installed

`systematic-debugging` (root-cause process) · `failforward` (failure memory) ·
`swiftui-debugging`, `profiling`, `concurrency-patterns` (platform).
