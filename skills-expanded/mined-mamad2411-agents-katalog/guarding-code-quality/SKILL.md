---
name: guarding-code-quality
description: Keeps agent-generated code correct, safe, and consistent with the codebase, match existing conventions, verify behavior with a real run/test, and self-review before claiming done. Use whenever writing or editing code. Calls verifying-reasoning to confirm a fix actually fixes, and reports honestly when checks fail.
license: Apache-2.0
metadata:
  author: Adrian Paredez
  version: "1.0"
  tier: "0"
  layer: domain/quality
compatibility: Any runtime with code execution / test running. Degrades to static self-review when execution is unavailable.
---

# Guarding code quality

Generated code that looks right and is wrong is the expensive default. This skill makes
"done" mean **verified-correct and consistent with the codebase**, not "compiles" or
"looks plausible."

## Use this when
- Writing new code or editing existing code in any language.
- Fixing a bug (the fix must be *proven* to fix).
- **Always-on for code work**, it's a guardrail, not a special mode.

## The discipline

```
- [ ] 1 FIT     read neighboring code; match its conventions, not your defaults
- [ ] 2 MINIMAL make the smallest change that satisfies the requirement
- [ ] 3 RUN     execute it, run the test / the app / the path you changed
- [ ] 4 PROVE   for a bug fix: show it failed before and passes after (verifying-reasoning)
- [ ] 5 EDGES   handle empty/null/error paths you touched; don't punt to the caller
- [ ] 6 REVIEW  self-review the diff as a reviewer would (checklist)
- [ ] 7 REPORT  state what you verified and what you did NOT; never claim untested success
```

## Principles

1. **Match the codebase, not your habits.** Read the surrounding code first. Use its
   naming, error handling, libraries, and structure. Consistent-with-wrong beats
   correct-but-alien for maintainability, but here you get consistent *and* correct.
2. **Smallest change that works.** Don't refactor unasked, don't add abstraction for one
   call site, don't rewrite what works. Minimal diffs are easier to verify and review.
3. **Run it, don't assert it works.** The line between "I think this works" and "I saw
   this work" is the whole skill. Run the test, the app, the changed path. (See `verify`
   / project run conventions where they exist.)
4. **A bug fix must prove itself.** Reproduce the failure first, then show the fix removes
   it. A fix you can't demonstrate fixing is a guess. Hand to `verifying-reasoning`.
5. **Own the edges you touch.** Empty input, null, error branch, boundary. Handle them in
   the code, don't leave a `# TODO` that ships.
6. **Self-review the diff.** Read your own change as a hostile reviewer (checklist). Catch
   the leftover debug print, the wrong variable, the missing await.
7. **Report honestly.** Say exactly what you verified and what you didn't. "Tests pass;
   did not test the migration path" is gold. "Done!" on untested code is a defect.

## Before you claim done (no rationalizing)
If you have not run the check in this turn, you cannot claim the result. "Done", "Perfect",
"Fixed", "Should work", and "Looks correct" are not evidence.

| Excuse | Reality |
|---|---|
| "Should work now" | Run the check. |
| "I'm confident" | Confidence is not evidence. |
| "Linter passed" | A linter is not a test or a compiler. |
| "The tests probably pass" | Run them; read the count. |
| "Just this once" | No exceptions. Untested success is a defect. |
| "The agent reported success" | Verify it independently (diff, output). |

Hold any "done / fixed / all set" until the command has run and you have read its output.

## Reading the codebase first (fit)
Before writing, find: the nearest similar function, the project's error-handling pattern,
its test layout, its lint/format config, and which libraries it already uses. Reuse over
introduce. A new dependency or pattern needs a reason.

## Don't punt (handle, don't defer)
Bad: write code that fails on the hard case and let the caller/agent deal with it later.
Good: handle the case now with a clear, justified behavior. Document non-obvious constants
(no magic numbers), if you don't know the right value, neither will the next reader.

## Runtime adaptation
- **Minimum (no execution):** do static self-review + `verifying-reasoning` by reasoning,
  and **explicitly flag "not executed"** in the report, never imply it was tested.
- **With execution:** prefer running the real test/app over reasoning about it.
- Reference capabilities ("run the test suite", "run the app"), not specific tool names,
  so the skill holds across Claude Code, Codex, OpenClaw, Hermes.

## Files
- `references.md`, fit heuristics, bug-fix proof pattern, review focus areas.
- `examples.md`, a verified fix, an honest partial report, an anti-pattern.
- `templates/change-report.md`, what to report after a change.
- `checklists/self-review.md`, the pre-done diff review.
- `benchmarks/`, defect-escape-rate method.
