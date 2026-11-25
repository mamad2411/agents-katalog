---
name: quick-development
description: |
  Lean development path for small, well-scoped changes: bug fixes, config
  updates, single-component edits, typo corrections, minor refactors,
  and any change that touches fewer than 5 files and requires fewer than
  3 distinct implementation tasks.

  AUTO-FIRE immediately when the user says any of:
  - "quick fix", "fix this bug", "small change", "minor update"
  - "patch", "hotfix", "tweak", "adjust", "correct this"
  - "it's just a small change", "shouldn't take long"
  - "/quick-development [description]"

  Do NOT use for feature additions, new components, or anything the user
  cannot describe in 3 bullet points or fewer. If in doubt, ask one question:
  "How many files will this touch?" — 5 or more means /standard-development.
---

# Quick Development

Read ~/.claude/skills/shared/context-guardian.md now and apply all rules
within it for the entire session before doing anything else.

---

## Entry scope check — run before any other step

Ask the user (or infer from their description) two questions:

**Q1: How many files will this change touch?**
**Q2: How many distinct implementation tasks are needed?**
  (A task = a discrete deliverable. "Write the fix" = 1. "Write + test + deploy" = 3.)

**If 5 or more files OR 3 or more tasks:**
```
This looks larger than a quick change.
Files: [N] / Tasks: [N] — exceeds quick-development scope.
Routing to /standard-development for correct handling.
```
Stop. Do not proceed. Instruct the user to use /standard-development.
Carry forward any context already gathered (description, file names, goal)
by summarising it for the user to paste into the new session.

**If fewer than 5 files AND fewer than 3 tasks:**
Continue to the routing step below.

---

## Routing: bug or known change?

**If the user describes a symptom** ("it's broken", "getting an error",
"something went wrong", "the output is wrong"):
→ Route to Bug path below.

**If the user describes a known change** ("update this value", "rename
this function", "change this colour", "add this line"):
→ Route to Known Change path below.

If unclear, ask: "Is something broken, or do you know exactly what needs
to change?" One question only.

---

## Bug path

**Step 1: Matt Pocock /diagnose**

Invoke the /diagnose skill from mattpocock/skills.

The diagnose loop:
1. Reproduce: establish a fast, deterministic pass/fail signal for the bug
   (failing test, curl command, headless browser script, CLI invocation)
2. Minimise: reduce the reproduction to the smallest case that still fails
3. Hypothesise: form one hypothesis per root cause candidate
4. Instrument: add logging or assertions to test the leading hypothesis
5. Fix: apply the minimal fix that makes the reproduction pass
6. Regression-test: write or verify a test that will catch this bug recurring

Do not skip the reproduce step. A fix without a reproduction signal is
a guess. Guesses are not acceptable in this workflow.

If /diagnose cannot find a reproduction signal for the bug → stop and
surface this to the user: "No reliable reproduction signal found. This bug
may require /standard-development to investigate properly."

**Step 2: Superpowers /debug**

Once /diagnose has identified the root cause, invoke Superpowers /debug
to implement the fix with TDD discipline:
- RED: confirm the failing test (from /diagnose reproduction signal)
- GREEN: implement the minimal fix that makes the test pass
- REFACTOR: clean up without changing behaviour
- Commit with a message that names the root cause, not just the symptom

**Step 3: Lightweight delivery gate**

Read ~/.claude/skills/shared/delivery-gate.md — Variant A (Lightweight).
Run Superpowers /code-review against the fix.
Do not commit until PASS.

---

## Known change path

**Step 1: Confirm scope**

State back to the user exactly what will change:
```
Confirmed scope:
- File(s): [list]
- Change: [one-sentence description]
- Nothing else will be modified.
Proceeding.
```

**Step 2: Superpowers direct execution**

Invoke Superpowers to execute the change.
If the change involves any logic (not just text/config): write a test first.
If the change is purely mechanical (rename, value update, config): no test needed.

Commit with a clear, specific message.

**Step 3: Lightweight delivery gate**

Read ~/.claude/skills/shared/delivery-gate.md — Variant A (Lightweight).
Run Superpowers /code-review against the change.
Do not commit until PASS.

---

## What this command never does

- Never invokes GSD
- Never shows the Ralph Loop gate
- Never runs grill-with-docs
- Never runs G Stack /office-hours
- Never runs G Stack /qa (unless a UI regression is found during /code-review,
  in which case surface it to the user and recommend /standard-development
  for a proper QA pass)

---

## Token budget

Target: under 25,000 tokens total for the session.
Model: Sonnet only. No Opus.
If the session approaches 20,000 tokens without completing: the task is
larger than estimated. Stop, dump state, and recommend /standard-development.

Context guardian hard stop at 50% applies regardless.
