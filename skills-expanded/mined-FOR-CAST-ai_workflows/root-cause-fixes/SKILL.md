---
name: root-cause-fixes
description: Fix defects where they live -- name the root cause as file:line, fix it in the package or helper that owns it with a regression test, never stack workarounds, and reuse the project's existing mechanisms. Use before proposing or making any fix.
when_to_use: Fixing a bug, a failing test, a wrong number or a broken run; a symptom in a script, report or target traced into a package or shared helper; about to add a guard, na.rm, tryCatch or a local copy of a function at the call site; a deadline pushing toward a quick patch; a first fix did not hold.
---

# Root causes, not patches

Fix the defect where it lives. If it is in a package, fix it in the package, with a
regression test -- even when one project script is the only thing hurting. A
workaround in the calling script is not a fix: it leaves the defect for the next
caller, and hides it from the tests that would have caught it.

Name the root cause as `file:line` before proposing a fix. If you cannot point at the
line, you have not found it.

Never stack a patch on a patch. A second workaround for one symptom means stop and
find the cause.

Before inventing a mechanism, look for the project's existing one -- test helpers,
conventions, utilities, options. Reaching for a new dependency or a subprocess usually
means the existing idiom went unread.

## In practice

- State it first: "Root cause: `R/fire.R:42` -- burned cells are counted with
  `severity > 0`, which includes every active cell."
- A co-developed package changes through `package-change-workflow` in
  `r-package-dev`. A project helper is fixed once, not at each caller.
- The regression test is part of the fix. Write it with the suite's existing fixtures
  (`tests/testthat/helper-*.R`), watch it fail, fix, watch it pass. A pre-existing
  failure that stops it passing is the next defect: fix it, or ask.
- Short on time: the package fix is usually as small as the patch. Make it, with its
  test, then ask the user how to ship it in time. Never choose a call-site copy
  yourself.

| Thought | Reality |
| --- | --- |
| "Don't overthink it" / "no time" | The package fix is one line too. |
| "Add a test later" | Later, the next caller finds the bug instead. |
| "The new test fails, but not because of my fix" | Then it tests nothing yet. That failure is a defect too. |
| "One more guard and it holds" | That is the second workaround. |

Proving the fix is right, not just that it ran: `verification-method` in
`r-code-review`.
