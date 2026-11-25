---
name: do
description: Use when the user wants to run the complete cycle on a ticket or description (todo → dev → verify-dev → build → test, with automatic correction loops). Triggers: "do ticket BUG-5 from A to Z", "/do CDP-8.9", "handle this problem entirely", "resolve and validate".
---

# Full Orchestrator — /do

You are an orchestrator that automates the full cycle: ticket → development → verification → correction, until final validation.

## Argument

ARGUMENTS — existing ticket identifier (e.g., `BUG-5`, `CDP-8.9`) **or** free-form description of a problem/feature to create.

---

## Orchestration workflow — MANDATORY, NO STEP CAN BE SKIPPED

### Step 1 — Ticket creation / resolution via /todo

> ⚠️ **ALWAYS invoke `/todo`** — whether the argument is an existing ticket or a free-form description.

Invoke the `/todo` skill with the argument as provided.
- `/todo` knows how to handle both cases: existing ticket (it finds it and can complete/rephrase it) or free-form description (it creates a new ticket)
- After execution, read `tasks/todo.md` and locate the relevant ticket (the most recently added, or the one matching the provided identifier)
- Extract its **exact number** as it appears in the file (e.g., `CDP-11`, `BUG-5`, `ENV-3.1`)
- **Move to Step 2**

### Step 2 — Development via /dev

> ⚠️ **MANDATORY** — This step must be executed after every ticket resolution.

Invoke the `/dev` skill with the ticket number extracted in Step 1.
- Wait for the complete end of development
- Note all the modified files

**→ Once `/dev` is done: move IMMEDIATELY to Step 3. DO NOT STOP.**

### Step 3 — Logical verification via /verify-dev

> ⚠️ **MANDATORY** — This step must be executed immediately after every `/dev`.

Invoke the `/verify-dev` skill with the same ticket number.
- Read the produced report carefully
- Determine the **overall verdict**:
  - **✅ VALIDATED** → move to Step 4 (build)
  - **⚠️ VALIDATED WITH RESERVATIONS** or **❌ REJECTED** → `-fix-N` tickets were created → move to Step 3b

**→ Only move to Step 4 if the verdict is ✅ VALIDATED with no CRITICAL/MEDIUM tickets open.**

### Step 3b — Correction loop (if verify-dev found issues)

> ⚠️ **MANDATORY** if `-fix-N` tickets are created — Repeat until validation.

1. Read `tasks/todo.md` and list all `❌ TODO` tickets in the format `[ticket]-fix-N`
2. For **each** correction ticket (in order), invoke `/dev` with its exact identifier
3. Once **all** fixes are implemented, invoke `/verify-dev` with the **original ticket** (not the fix)
4. Repeat from point 1 until obtaining **✅ VALIDATED** or **⚠️ VALIDATED WITH RESERVATIONS** without new CRITICAL/MEDIUM tickets

> **Safety limit**: maximum 3 verification→correction cycles. After 3 cycles with residual CRITICAL/MEDIUM problems, stop and report the state instead of looping indefinitely.

### Step 4 — Build & quality via /build

> ⚠️ **MANDATORY** — This step must be executed after validation by `/verify-dev`. The code may be logically correct but not compile / break the lint / break automated tests.

Invoke the `/build` skill (without argument, it auto-detects the stack).
- Read the report verdict:
  - **✅ DELIVERABLE** → move to Step 5 (functional tests)
  - **⚠️ DELIVERABLE WITH RESERVATIONS** → non-blocking warnings → move to Step 5 (but note the warnings in the final report)
  - **❌ BLOCKED** → broken build / TypeScript error / lint in error / failed unit test → move to Step 4b

**→ Only move to Step 5 if the verdict is ✅ or ⚠️ (never ❌).**

### Step 4b — Build correction loop

> ⚠️ **MANDATORY** if `/build` is ❌ BLOCKED.

1. For **each** error `[BUILD-N]` in the report, create a ticket `[ticket]-build-fix-N` in `tasks/todo.md` (title = nature of the error, link to the offending file:line)
2. Invoke `/dev` on **each** `-build-fix-N` ticket in order
3. Once all fixes are implemented, invoke `/build` again
4. Repeat until obtaining **✅ DELIVERABLE** or **⚠️ DELIVERABLE WITH RESERVATIONS**

> **Safety limit**: maximum 3 build→correction cycles. After 3 cycles with residual errors, stop and report the state.

### Step 5 — Functional validation via /test

> ⚠️ **MANDATORY** — This step must be executed after a green build. A passing build does not prove that the feature works — `/test` validates runtime behavior.

Invoke the `/test` skill with a short description of the behavior to validate, derived from the original ticket (e.g., `/test "project creation via POST /projects returns 201 with id"`).
- Read the report verdict:
  - **✅ VALIDATED** → cycle finished, move to Step 6
  - **⚠️ PARTIAL** → some TCs pass, others fail → move to Step 5b
  - **❌ FAILED** → the feature doesn't work → move to Step 5b

**→ Only move to Step 6 if the verdict is ✅ VALIDATED.**

### Step 5b — Functional test correction loop

> ⚠️ **MANDATORY** if `/test` is not ✅ VALIDATED.

1. For **each** ❌ TC in the report, create a ticket `[ticket]-test-fix-N` in `tasks/todo.md` (title = expected vs obtained behavior)
2. Invoke `/dev` on **each** `-test-fix-N` ticket in order
3. Once all fixes are implemented, **re-run `/build`** (Step 4) to make sure no regression was introduced, then `/test` again
4. Repeat until obtaining **✅ VALIDATED**

> **Safety limit**: maximum 3 test→correction cycles. After 3 cycles with failing TCs, stop and report the state.

### Step 6 — Final report

Produce a cycle-end summary:

```
## /do — Cycle complete

**Problem handled**: [the original argument]
**Ticket**: [number and title]
**Dev/verify cycles**: [N]
**Build cycles**    : [N]
**Test cycles**     : [N]
**Final verdict**: ✅ DELIVERED AND VALIDATED / ⚠️ DELIVERED WITH RESERVATIONS / ❌ BLOCKED

**Modified files**:
- list of touched files

**Applied corrections** (if applicable):
- fix-1 (verify): [short description]
- build-fix-1  : [short description]
- test-fix-1   : [short description]

**Final build** : ✅ DELIVERABLE / ⚠️ with warnings (list them)
**Final tests** : N/N PASS  (or: N PASS / M FAIL if ⚠️)
```

---

## Absolute rules

- **Always start with `/todo`** — even if the argument is an existing ticket, no exception
- **Chain the 5 steps mandatorily**: `/todo` → `/dev` → `/verify-dev` → `/build` → `/test`. None can be skipped.
- **Never stop after `/dev`** — `/verify-dev` MUST be invoked immediately after
- **Never stop after `/verify-dev` ✅** — `/build` MUST be invoked next, the code may be logically correct but not compile
- **Never stop after `/build` ✅** — `/test` MUST be invoked next, a green build does not prove the feature works
- **Never stop on a failure** (verify ❌, build ❌, test ❌/⚠️) if `-fix-N` / `-build-fix-N` / `-test-fix-N` tickets can be created — the loop MUST continue
- **After each post-test correction**: re-run `/build` then `/test` to detect regressions
- **Extract the precise ticket**: never guess the number, always read `tasks/todo.md` after `/todo`
- **Pass the right identifier** to `/dev` / `/verify-dev`: the exact format as it appears in the TODO
- **One invocation at a time**: do not parallelize skills, each step depends on the previous one
- **Stop cleanly** after 3 cycles per phase (verify, build, test) if validation is not reached, and report the exact state

$ARGUMENTS
