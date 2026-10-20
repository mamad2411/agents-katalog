---
description: Review the working tree against this repo's actual standards
---

Review the current diff as a senior engineer who owns this codebase and will be woken up when it
breaks. Be specific and be direct; approval is not the goal.

Check, in priority order:

1. **Boundaries** (`AGENTS.md` §5) — any upward or sideways dependency, any feature importing
   another feature, any Flutter import in `core_domain`, any logic in `diapason_ffi`
   (`packages/audio_engine/rust`).
2. **Real-time safety** (`AGENTS.md` §6) — allocation, locking, logging, syscalls or panics on the
   audio path, including inside anything the callback calls transitively.
3. **Timing** — anything deriving a beat, animation or countdown from a wall clock rather than the
   audio clock.
4. **Tests** — does this change have the tests `docs/TESTING.md` requires for its type? Are any
   assertions on wall-clock time? Was a test skipped or a lint suppressed to get green?
5. **Docs** — did this invalidate a reference doc or an ADR that has not been updated?
6. **Correctness and clarity** — error handling, edge cases from `PRODUCT_SPEC.md`, naming,
   anything that will read as a mystery in three months.

For each finding: file, line, why it matters, and the fix. Separate "must fix" from "worth
considering". If the diff is good, say so briefly rather than inventing findings.
