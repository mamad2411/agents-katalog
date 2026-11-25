---
name: pipeline-failure-triage-and-recovery
description: >
  Diagnoses and recovers a failed or flaky CI run — distinguishing a real
  regression from a flaky/environmental failure, choosing the right re-run
  strategy (single job vs. full pipeline vs. targeted re-run), clearing
  cache/dependency corruption, and quarantining a confirmed-flaky test
  without silently hiding real failures. Use when the user asks "why did
  this pipeline/build fail," "is this test actually flaky or a real bug,"
  "should I just re-run CI," "the pipeline fails intermittently on the same
  commit," "clear the CI cache," or "quarantine this flaky test."
license: Apache-2.0
compatibility: "Claude Code, GitHub Copilot, OpenAI Codex, Cursor, Gemini CLI"
metadata:
  domain: devops
  maturity: stable
---

# Pipeline Failure Triage and Recovery

## Purpose

A failed CI run is a decision point, not just a red X: is this a real
regression that must be fixed before merging, a flaky test that fails
intermittently regardless of the code change, or an environmental problem
(a corrupted cache, a transient network blip to a package registry, a
rate-limited external dependency) that has nothing to do with the code at
all? Treating every failure as "just re-run it" trains engineers to ignore
CI, while treating every failure as a real regression wastes hours chasing
a bug that doesn't exist. This skill covers triaging a failed run
methodically, choosing the narrowest safe recovery action, and fixing the
underlying cause of recurring flakiness or corruption instead of only
re-running around it.

## When to use

- A pipeline run fails and it's unclear whether the failure is caused by
  the change under test, a flaky test, or CI infrastructure/environment.
- The same commit passes on re-run with no code change, suggesting
  flakiness rather than a real bug.
- A build fails with dependency-resolution errors, missing packages, or
  "works on my machine but not in CI" symptoms that point at a corrupted
  or stale cache.
- Deciding whether to re-run a single failed job, the whole pipeline, or
  only specific downstream stages.
- A specific test or job fails often enough that people have started
  reflexively re-running CI without investigating, or have started
  ignoring red pipelines altogether.

## Prerequisites & environment

- Read access to the CI platform's run logs and, ideally, per-step timing
  and cache-hit metadata (GitHub Actions run logs and `actions/cache`
  hit/miss output, GitLab CI job traces and cache job artifacts, Jenkins
  console output and workspace state).
- The ability to re-run a single job/stage in isolation, not only the
  entire pipeline from scratch — this is a platform capability, not
  something to build ad hoc (GitHub Actions "Re-run failed jobs", GitLab
  "Retry" per job, Jenkins "Replay"/stage restart where supported).
- A test-flakiness or quarantine mechanism appropriate to the test
  framework (a `@flaky`/quarantine tag, a separate flaky-test job that
  doesn't block merge, or a test-management tool that tracks flake rate
  per test) — see
  [ci-cd-pipeline-design](../ci-cd-pipeline-design/SKILL.md) for where
  quality gates sit in the overall pipeline.
- Enough historical run data (last 10-20 runs of the same job) to tell a
  one-off blip from a pattern; most CI platforms retain this by default.

## Step-by-step guidance

1. **Read the actual failure, not just the red status.** Open the failed
   step's log and find the first error, not the last one — a cascade of
   downstream errors (e.g., "server not reachable" repeated 40 times) is
   usually caused by one earlier failure (e.g., "port already in use" or
   "npm ERR! 403 Forbidden"). Scrolling to the bottom of a long log and
   reacting to the last line is a common way to misdiagnose the real
   cause.

2. **Classify the failure before deciding on a recovery action:**
   - **Real regression** — the failure is a deterministic assertion/
     compile/lint error directly traceable to lines changed in this diff.
     Fix the code; do not re-run.
   - **Flaky** — the *same commit*, unchanged, fails intermittently across
     multiple re-runs with a non-deterministic symptom (race condition,
     timing-dependent assertion, order-dependent test state). Confirm by
     re-running the specific failed job (not the whole pipeline) 2-3
     times; if it passes without any code change, it's flaky.
   - **Environmental/infrastructure** — package registry timeout, runner
     out of disk space, transient network error to an external service,
     Docker daemon not ready yet. Usually has a recognizable
     infrastructure-level error message (`ECONNRESET`, `429 Too Many
     Requests`, `no space left on device`) rather than an assertion
     failure.
   - **Cache/dependency corruption** — a stale or partially-written cache
     (e.g., a `node_modules`/`.venv`/Maven local repo cache saved mid-
     install, or a lockfile/cache-key mismatch after a dependency bump)
     causes a build to fail in CI with an error that doesn't reproduce
     locally with a clean install. Symptom: errors like "Cannot find
     module X" for a package that is definitely declared, or version
     mismatches between what's declared and what's actually resolved.

3. **Re-run at the narrowest scope that actually re-tests the failure.**
   Re-running the entire pipeline from Source when only one downstream
   test job failed wastes time and CI minutes, and — worse — can mask a
   real intermittent failure by giving it more chances to pass by luck.
   - GitHub Actions: `gh run rerun <run-id> --failed` re-runs only failed
     jobs.
   - GitLab CI: retry the specific failed job from the pipeline UI/API
     (`POST /projects/:id/jobs/:job_id/retry`), not "Run pipeline" again.
   - Jenkins (declarative): use `Restart from Stage` for a specific stage
     when the plugin supports it, rather than re-triggering the whole
     build.

4. **For suspected cache/dependency corruption, invalidate the cache
   deliberately rather than guessing.** Bump the cache key (most CI caches
   are keyed off a lockfile hash) so the next run rebuilds from a clean
   state:
   ```yaml
   # GitHub Actions actions/cache — bump the key suffix to force a miss
   - uses: actions/cache@v4
     with:
       path: ~/.npm
       key: npm-${{ hashFiles('package-lock.json') }}-v2   # was -v1
   ```
   If the corruption recurs across multiple unrelated commits, the root
   cause is usually a cache key that doesn't fully capture what changes
   the cache's validity (e.g., keyed on `package.json` but not
   `package-lock.json`, so a lockfile-only change doesn't bust a stale
   cache) — fix the key, don't just clear the cache once and move on.

5. **Confirm flakiness quantitatively before quarantining a test**, not
   after a single failed run. Re-run the specific test/job in isolation
   3-5 times; a test that fails 1-2 times out of 5 with no code change is
   flaky, a test that fails once and then passes 10/10 afterward was more
   likely a genuine environmental blip that day.
   ```bash
   # pytest example: re-run only the failed test, several times, in isolation
   pytest tests/test_checkout.py::test_concurrent_orders --count=5
   ```

6. **Quarantine confirmed-flaky tests visibly, with an owner and a
   deadline** — move them to a non-blocking "flaky" job/tag rather than
   silently skipping or deleting them, and file a ticket to actually fix
   the race condition:
   ```yaml
   # pytest.ini / marker-based quarantine, run separately and non-blocking
   markers =
     flaky: known-flaky test, tracked in JIRA-1234, does not block merge
   ```
   ```bash
   pytest -m "not flaky"          # blocking CI job
   pytest -m "flaky" || true      # separate, non-blocking, still visible
   ```

7. **If the same job flakes repeatedly across many PRs/commits, treat it
   as a pipeline reliability problem worth root-causing** — a shared
   test-order dependency, an unpinned external service being hit
   directly instead of mocked, or a resource limit on the runner (memory,
   file descriptors) — rather than accepting "CI is just flaky" as a
   permanent state. This is the CI-specific instance of the toil this
   causes: engineers re-running CI reflexively instead of trusting it.

## Best practices

- Track flake rate per test/job over time (most CI platforms or test
  dashboards surface this); a rising flake rate is an early warning sign
  worth acting on before it becomes "just re-run it twice."
- Never silently delete or comment out a failing test to make CI green —
  quarantine it visibly with an owner and a tracking ticket (step 6), so
  the underlying bug it may be catching isn't lost.
- Prefer re-running the narrowest failed unit (single job/stage) over the
  whole pipeline; if the platform doesn't support that, treat "add
  per-job re-run" as a pipeline improvement worth investing in.
- Key caches on the actual input that determines validity (lockfile hash,
  not just a manifest file that doesn't capture transitive version
  changes) so corruption from a stale cache doesn't recur.
- Distinguish "the pipeline is flaky" from "this one test is flaky" —
  infrastructure-level flakiness (runner capacity, network to a shared
  dependency) needs a different fix than a race condition in one test.
- Keep a lightweight log (even just linked tickets) of quarantined flaky
  tests and their fix status — an unowned quarantine list grows forever
  and quietly erodes test coverage.

## Common pitfalls

- **Symptom:** A build fails in CI with a dependency error that doesn't
  reproduce when run locally with a fresh checkout.
  **Fix:** Suspect a stale/corrupted cache before suspecting the code —
  bump the cache key and re-run (step 4); if it passes clean, the cache
  key doesn't capture something that changed (usually a lockfile not
  included in the key).

- **Symptom:** Engineers reflexively click "re-run" on every red pipeline
  without reading the log, and a real regression eventually merges because
  it happened to pass on the second or third try.
  **Fix:** Require reading the actual failed step's log and classifying
  the failure (step 2) before re-running; if a test needs 2-3 re-runs to
  pass "normally," that is itself evidence of flakiness that should be
  quarantined and fixed, not treated as routine.

- **Symptom:** A test is marked `@skip` or deleted after a few flaky
  failures, and months later a real bug it would have caught reaches
  production.
  **Fix:** Quarantine, don't delete — move it to a non-blocking job with a
  tracked ticket and an owner (step 6), so the coverage isn't silently
  lost and someone is accountable for fixing the underlying race
  condition.

- **Symptom:** The same job has flaked on unrelated PRs for months, and
  each time someone just re-runs it and moves on.
  **Fix:** Treat repeated flakiness on the same job as a reliability
  problem to root-cause (step 7) — check for shared/leaked state between
  tests, unmocked calls to a real external service, or runner resource
  exhaustion, instead of accepting indefinite manual re-runs as normal.

- **Symptom:** A cache-clearing fix works once, but the same corruption
  comes back a few weeks later after an unrelated dependency bump.
  **Fix:** The cache key almost certainly doesn't hash the right input
  (e.g. it's keyed on a directory listing or a manifest file instead of
  the lockfile) — fix the key to reflect everything that actually
  invalidates the cache, not just clear it reactively each time.

## Worked example

**Scenario:** A GitHub Actions job `test-integration` fails on a PR with
`Error: connect ECONNRESET` from a call to an external payments sandbox
API, while the `test-unit` job in the same run passes.

1. **Read the log**: the first error is `ECONNRESET` from an HTTP call in
   `tests/integration/test_payment_capture.py`, not an assertion failure —
   this looks environmental, not a regression in the diff (the diff only
   touches an unrelated `checkout` module).
2. **Classify**: no code in this PR touches payment integration; check
   history — this same job flaked with the identical error on two other
   unrelated PRs in the last week. Pattern points to environmental
   flakiness (the sandbox API itself is rate-limiting or intermittently
   unavailable), not a real regression.
3. **Narrow re-run**: `gh run rerun <run-id> --failed` re-runs only
   `test-integration`. It passes clean on retry with no code change,
   confirming flakiness rather than a real failure.
4. **Root-cause instead of accepting the re-run as routine**: the
   integration test calls the real sandbox API directly with no retry/
   backoff and no circuit breaker; three flakes in a week is a pattern,
   not a coincidence. File a ticket to add a retry-with-backoff wrapper
   around the sandbox call and, in the meantime, mark the specific test
   `@pytest.mark.flaky(reruns=2, reruns_delay=5)` so isolated sandbox
   blips don't block unrelated PRs while the real fix is pending —
   visible in CI output, tracked, not silently hidden.
5. **Merge is not blocked further**: the PR's actual diff (checkout
   module) had a clean `test-unit` run and the flaky integration test is
   now quarantined with a tracked fix, so the team isn't stuck re-running
   CI on every unrelated PR that happens to touch this suite.

## Cross-references

- [ci-cd-pipeline-design](../ci-cd-pipeline-design/SKILL.md) — where
  quality gates and required checks sit in the overall pipeline; this
  skill covers what to do when one of those gates fails or flakes.
- [artifact-and-dependency-management](../artifact-and-dependency-management/SKILL.md) —
  lockfile/version-pinning discipline that prevents the dependency-drift
  class of cache corruption covered in step 4.
- [devops-delivery-metrics-and-dora-analysis](../devops-delivery-metrics-and-dora-analysis/SKILL.md) —
  a rising rate of pipeline re-runs/flakiness quietly inflates lead time
  for changes; tracking flake rate feeds directly into that metric.
- [github-actions-single-repo-workflows](../../../cicd-tooling/skills/github-actions-single-repo-workflows/SKILL.md) —
  platform-specific job/cache syntax referenced in steps 3-4.
