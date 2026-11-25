---
name: senior-debugging
description: Use when a test, build or runtime behavior fails, a feature regressed, behavior is flaky, a previous fix did not hold, or a report of wrong output or data comes in, even one that names the function to fix. Not for explaining code that works or reviewing a change without a reported failure.
---

# Debugging

**Core rule:** no fix until the cause is backed by evidence you observed.

## Process

1. **Define the failure** — exact symptom, expected behavior, environment.
2. **Reproduce** — the smallest reliable reproduction you can get. If it does not reproduce, gather more data instead of guessing.
3. **Collect evidence** — full error output and stack trace, failing test, logs, recent diff.
4. **Trace the path** — follow the execution or data path back to where the bad value or state originates; fix there, not where it surfaces. Reproduce through the real entry points the data goes through (import, sign-up, API), not only the function the report names: a report describes a symptom, and the same cause usually breaks other paths.
5. **Rank hypotheses** — two or three falsifiable explanations, most likely first.
6. **Test one hypothesis at a time** — targeted inspection or temporary instrumentation; change one variable per experiment.
7. **State the root cause** — separate the confirmed cause from contributing factors.
8. **Fix minimally, at the cause** — no opportunistic refactoring. When the cause is in another module than the one reported, fix it there in this change; that is the bug, not extra scope. Ask first only before rewriting data already stored, or another destructive step; say which records stay wrong until then.
9. **Check every reader before patching one** — if your fix filters, falls back or converts stored records inside one function, stop and search the whole repository for the field or value it handles (`git grep -n "<field>"`). Name each other module that reads it (billing, APIs, pages, feeds, exports, jobs) in your report under **Other readers**, each marked *fixed* or *right as is, because…*. If another reader sees the same bad records, the cause is how they are written: fix the writer so every reader agrees, and do not keep the patch in the reader; records already saved follow step 8.
   - **Changing the writer is code, not a data change:** do it now, without asking, even when a reader is billing, access or a public API. When another path does the same action correctly (a member removed in the admin UI, an address saved by web checkout), make the bad records look exactly like the ones it writes; that path already answers how billing, lists and lookups should treat them. Fix every path that sets or clears the field (create, update, undo, reactivate, import), not only the one in the report.
10. **Prove the fix catches the bug** — a regression test that fails without the fix and passes with it. With the `senior` CLI, run `senior prove --regression --test "<command for that test>" --expect-failure "<regex matching the original failure>"` (add `--base <ref>` once the fix is committed): it reverts only the fix, watches the test fail, restores the fix byte-for-byte and re-runs. Without the CLI, do it in one shell command, not one step per turn: run the test with the fix stashed, then restored (for example `git stash push -- <fixed files> && <test>; git stash pop && <test>`), and read the full output rather than a filtered one. Without the fix, the test must fail with the original symptom; a failure from setup, imports or syntax proves nothing.
11. **Re-run the original reproduction** and the relevant suite.

In systems with several components (CI → build → deploy, API → service → database), log what enters and leaves each boundary once before theorizing; it shows which layer breaks.

## Regression check

When something used to work, inspect the working-tree changes, recent commits on the failing path, dependency/lockfile changes, migrations, configuration and environment differences. Do not assume the newest commit is guilty without evidence.

Once a commit is implicated, read its **whole** diff (`git show <sha>`), not only the lines the failing test points at. List every behavior it changed (defaults, error handling, validation, header or case handling, return values) and decide for each one whether the change was intended. A failing test usually exposes one regression out of several in the same commit; restore every unintended change and cover each with a test. When the commit message says a change was intended (a new threshold, a renamed field), keep it and update the stale test instead.

## When fixes keep failing

After three fixes that did not hold, stop patching. Repeated failures in different places usually mean the design or an assumption is wrong. Summarize what each attempt showed and discuss the structure with the user before a fourth attempt.

## Red flags

| If you notice yourself thinking… | Do this instead |
|---|---|
| "I know what this is, I've seen it before" | Reproduce it first; similar symptoms often have different causes |
| "Adding a retry/timeout will make it go away" | Find out why the operation fails |
| "I'll change these few things together to save time" | One change per experiment, or you won't know which one worked |
| "The test is wrong, I'll relax the assertion" | Prove the test is wrong from the requirements before touching it |
| "The failing test passes now, so the regression is fixed" | Re-read the guilty commit's full diff for other unintended changes |
| "The report says fix this function, so the cause elsewhere is out of scope" | Fix the cause; ask only before rewriting data already stored |
| "I'll filter or convert the bad records in the function the report names" | Search every reader of that field; if another one sees the same bad records, fix the writer |
| "Fixing the writer changes billing or access, so I'll list it and ask" | Fix it: the working path for the same action shows the right behavior; ask only before rewriting saved records |
| "The error is gone, so it's fixed" | Re-run the original reproduction and the regression test |
| "Production is down, there's no time to investigate" | Mitigate visibly (rollback, flag) if needed, then find the cause |

## Exit criteria

Close debugging only when the root cause is explained with evidence, the other readers are named, each fixed or shown right as it is, when the fix filters or converts stored records in one reader, the original failure no longer reproduces, the regression test has been seen failing and passing, relevant verification passes, and remaining uncertainty is stated.
