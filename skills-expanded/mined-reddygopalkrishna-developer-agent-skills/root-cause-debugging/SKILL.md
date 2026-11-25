---
name: root-cause-debugging
description: Finds the real cause of a bug before changing code, using a minimal reproduction, ranked hypotheses, one-variable experiments and bisection (git bisect, input bisection). Use when something is broken, failing, crashing, flaky, intermittent, behaving differently between environments, a test fails for unclear reasons, or an earlier fix did not work. Not for performance tuning without a defect or for designing new features.
license: MIT
---

# Root-Cause Debugging

Never change code to fix a bug you cannot explain. Reproduce it, find the cause with evidence, and prove the fix with a test that failed before the fix and passes after it.

## When to use

- An error, exception, crash, wrong output, failing test or regression.
- "Works on my machine", or works in one environment but not another.
- Intermittent or flaky failures.
- A fix was already tried and the bug came back or moved.

Not for: production outages where mitigation must come first (stabilize, then come back here), or performance work where nothing is actually wrong.

## Workflow

1. **Capture the exact failure.** Copy the full error message, stack trace, exit code, relevant log lines, and the exact command, request or steps that produced them. Write down expected vs actual behavior.
2. **Read the whole stack trace.** Include every `Caused by:` / inner exception / wrapped error. The top frame is often library code; the first frame in the project's own code is usually where to start. The line where an error surfaces is where a bad value was *used*, not necessarily where it was *produced*.
3. **Reproduce it.** Get a command that fails every time. Then shrink it: smallest input, fewest steps, a single test, for example:
   - `pytest tests/test_orders.py::test_refund -x`
   - `npx vitest run src/cart.test.ts -t "applies discount"`
   - `go test -run '^TestRefund$' ./orders`
   - `dotnet test --filter "FullyQualifiedName~RefundTests"`

   If you cannot reproduce it, do not guess. Collect more data (step 7) or ask the user for environment details, logs and exact steps.
4. **Check the boring causes first** (table below). A large share of "impossible" bugs are stale builds, wrong branches, wrong config or a different dependency version.
5. **Write ranked hypotheses.** List 2-5 candidate causes. For each: evidence for, evidence against, and the cheapest experiment that would confirm or rule it out. Start with the one that is most likely *and* cheapest to test.
6. **Experiment one variable at a time.** Predict the result before running. If the result surprises you, your model of the system is wrong: update it before continuing. Revert experiments that did not help.
7. **Narrow by bisection** when the search space is large:
   - **History:** if it worked at some earlier commit, use `git bisect` (automate it with `git bisect run`). See [references/git-bisect.md](references/git-bisect.md).
   - **Input:** halve the input file, payload, dataset or list of tests until you find the minimal failing case.
   - **Code path:** disable half of the suspect code (early return, feature flag, stub) and see which half matters.
   - **Environment:** diff a working and a failing environment (versions, env vars, config, OS, data) and apply half of the differences at a time.
8. **Instrument where you are blind.** Add logs at boundaries with a unique prefix (e.g. `DBG-1234`), log types and lengths as well as values, use breakpoints and conditional breakpoints, or attach a tracer. See [references/debugging-tools.md](references/debugging-tools.md) for per-language tools. Never log secrets or personal data.
9. **State the root cause as a mechanism.** "The cache key omits `tenant_id`, so tenant B reads tenant A's entry" — not "bug in cache.py". Keep asking "why?" until you reach something you can fix that prevents this class of bug, not just this instance.
10. **Write a failing regression test** at the lowest level that still shows the bug. Run it and confirm it fails *for the right reason* (the assertion you expect, not an import or setup error).
11. **Fix the cause,** then run the new test and the surrounding suite. Search the codebase for the same pattern (same call, same misuse) and fix or report the other places.
12. **Clean up and report.** Remove temporary instrumentation. Tell the user: symptom, root cause, evidence, fix, regression test, other places affected, and anything you could not verify.

## Check assumptions first

| Assumption | How to verify |
|---|---|
| You are running the code you think you are | Add a temporary log line and confirm it prints. Check `git status`, `git branch --show-current`, `git log -1`. Rebuild. Check which binary or interpreter runs: `which`/`command -v` (POSIX), `where` (Windows), `python -c "import sys; print(sys.executable)"`. |
| Dependency versions match | Read the lockfile. `npm ls <pkg>`, `pip show <pkg>`, `go list -m all`, `mvn dependency:tree`, `./gradlew dependencies`, `dotnet list package`, `cargo tree`. |
| Config and env vars are what you expect | Print the *effective* config at startup (redacted). Check precedence: defaults, files, env vars, CLI flags, remote config. |
| Nothing is cached or stale | Clean build (delete build/output dirs), rebuild containers with `--no-cache`, clear package caches, browser cache, CDN, service worker, memoization layers. |
| The data is what you think | Query the actual record or message. Do not reason from what the data "should" be. |
| Time, timezone and locale | UTC vs local, DST transitions, month-end, leap days, locale-specific number and date parsing. |
| Network path | DNS resolution, proxies, TLS, which host and port is actually hit (`curl -v`). |
| Permissions and identity | File permissions, OS user, service account, IAM role, token scopes. |

## The three-strike rule

If three fixes in a row have not worked, stop editing code. Each failed fix is evidence that your hypothesis is wrong.

1. Revert the failed attempts.
2. Re-read the original evidence and the full stack trace.
3. Write down every assumption you are making and verify each one.
4. Ask whether the design itself is the problem (shared mutable state, wrong abstraction, hidden coupling).
5. Tell the user what you have ruled out and what you plan to try next.

## Intermittent bugs

| Symptom | Likely causes | Technique |
|---|---|---|
| Fails only under load or in parallel | Race condition, shared mutable state, pool exhaustion, missing lock or transaction | Repeat with parallelism: `go test -race -count=100 ./...`, `pytest -n 8` (pytest-xdist) with `--count=50` (pytest-repeat). Use race detectors: Go `-race`, ThreadSanitizer (`-fsanitize=thread`) for C/C++. |
| Depends on test order | State leaking between tests (globals, DB rows, env vars, singletons, mocks not reset) | Run in random order: pytest-randomly, `jest --randomize`, `vitest --sequence.shuffle`, `go test -shuffle=on`. Run the failing test alone, then with its neighbors. |
| Fails after hours or days | Memory, file handle, socket or connection leak; counter overflow; token or certificate expiry | Track resource counts over time; heap snapshots; check what expires. |
| Fails only in CI | Different OS, CPU count, timezone, locale, missing secrets, slower machine hitting timeouts, parallel jobs sharing resources | Diff the environments; run the CI container image locally; print env (redacted) in the CI job. |
| Disappears with logging or a debugger | Timing-sensitive race | Use low-overhead instrumentation (in-memory ring buffer dumped on failure), stress runs, race detectors. |
| Fails at certain times | Midnight, month or year boundaries, DST, leap years, cron overlap | Inject a clock and test with fixed times around the boundary. |

For an intermittent bug, "fixed" means the reproduction passes many repetitions (e.g. 100+ runs or a stress run) that previously failed at a known rate.

## Anti-patterns

- **Shotgun debugging** — changing several things at once. When it starts working you do not know why, and you may have added new bugs.
- **Fixing the symptom** — swallowing the exception, adding a null check without knowing why the value is null, adding a retry or `sleep` to hide a race, raising a timeout. These move the bug, they do not remove it.
- **Trusting the error location** — the crash site is where the bad value was used. Trace the value backwards to where it was produced.
- **Reasoning instead of running** — reading code for an hour when a 30-second experiment would answer the question.
- **Blaming the platform first** — compiler, library and OS bugs exist but are rare. Rule out your own code and config first, and get a minimal reproduction before claiming one.
- **Declaring victory early** — the symptom disappeared once, so it must be fixed. Re-run the reproduction, and for flaky bugs, re-run it many times.
- **Leaving debris** — debug logs, commented-out code, disabled tests, temporary flags.

## Done when

- You can state the root cause as a mechanism and point to the evidence.
- A regression test failed before the fix and passes after it.
- For intermittent bugs, the reproduction passes many repeated runs that failed before.
- The same pattern was searched for elsewhere and handled or reported.
- Temporary instrumentation is removed and the relevant test suite passes.

## References

- [references/git-bisect.md](references/git-bisect.md) — read when the bug is a regression (it worked at some earlier commit or version).
- [references/debugging-tools.md](references/debugging-tools.md) — read when you need a debugger, thread or heap dump, tracer, sanitizer or network tool for a specific language or runtime.
