---
name: debug-ci-pipeline-failure
description: Debugs a red CI job to root cause instead of blind-rerunning — reproduce locally in the SAME image (`act -j <job>`, `gitlab-runner exec`, `circleci local execute`, or `docker run` the exact pinned digest), read the full log + the real exit code (124=timeout, 137=OOM/SIGKILL, 143=SIGTERM, 139=segfault), then classify into flaky / env-drift / poisoned-or-stale cache / resource-OOM / missing-secret / timeout / test-ordering / network, and confirm with a targeted experiment — diff local-vs-CTRL env (`printenv | sort`, tool `--version`, lockfile hash), run clean (no cache, `--no-cache`/clear key) vs cached, isolate ONE matrix leg, bisect with `git bisect run`, re-run with debug logging (`ACTIONS_STEP_DEBUG=true`, `CI_DEBUG_TRACE=true`, `set -x`) or open an interactive runner (`tmate`/`debug with SSH`/`--privileged` shell) — and fix the cause (pin the digest, scope the cache key, raise the limit, randomize then fix test order) not the symptom.
when_to_use: A CI/CD job that passes locally is red on the runner, fails intermittently, or broke without a relevant code change — green-on-my-machine/red-on-CI, an OOM/timeout/exit-137, a cache or matrix-only failure, or you're tempted to just hit "Re-run job". Distinct from cicd-pipeline-author (designs/authors the pipeline YAML from scratch; this debugs an existing one that's failing) and debug-flaky-tests (fixes the nondeterministic TEST itself — one of several causes here; this skill first classifies whether flakiness, env drift, cache, or limits is even the cause).
---

## When to Use

Reach for this skill when a CI job is failing and you need to find out WHY before touching anything:

- "It's green locally but red on CI" / "passes on my machine, fails on the runner"
- "The job got killed — exit 137 / OOM / 'Process completed with exit code 137'"
- "It only fails sometimes — re-running makes it go green" (don't stop there — classify it)
- "One matrix leg (py3.12 / arm64 / windows) fails, the rest pass"
- "Nothing in my diff touches this — it broke on its own" (env/cache/upstream drift)
- "The job hangs and gets cancelled after N minutes" (timeout vs deadlock)
- "I keep hitting Re-run and hoping" — STOP, reproduce and root-cause instead

NOT this skill:
- Authoring the pipeline YAML, stages, caching strategy, runners from scratch → cicd-pipeline-author (this skill debugs the pipeline it produced)
- Fixing the nondeterministic test itself (shared state, time/random, async races, order-dependence) once you've confirmed flakiness is the cause → debug-flaky-tests (this skill decides *whether* it's a flaky test vs env/cache/limit, then hands off)
- General "why does this code crash" root-causing unrelated to CI → debug-root-cause (this skill is CI-runner-specific: images, caches, runners, matrices)
- Choosing/pinning the toolchain & language versions as a deliverable → pin-toolchain-versions (this skill *detects* version drift as a cause and tells you to pin)
- Designing the cache key/layers/TTL as a strategy → caching-strategy (this skill *invalidates* a poisoned cache to confirm it's the cause)
- Debugging a failing K8s pod/job workload (not a CI runner) → k8s-debug-workload
- A missing secret that's really a vault/rotation/scoping problem → secrets-management (this skill detects "secret empty on CI" as a class; that one fixes how secrets are stored/injected)
- Standing up a reproducible local dev container to match CI → compose-local-dev-stack / setup-devcontainer-env
- A production incident/postmortem (not a build) → incident-response-sre

## Steps

1. **Read the log top-to-bottom and grab the REAL exit code before theorizing.** The first red line is rarely the cause — scroll up to the first error, and check the process exit code, which names the failure class:

   | Exit code | Means | Likely cause |
   |---|---|---|
   | `1` / `2` | generic failure / misuse | real test/build error — read the actual assertion |
   | `124` | command timed out (`timeout` wrapper) | step exceeded its time budget |
   | `137` | `128+9` = SIGKILL | **OOM-killed** (almost always memory limit) or job cancelled |
   | `139` | `128+11` = SIGSEGV | native segfault (bad binary/arch mismatch) |
   | `143` | `128+15` = SIGTERM | timeout/cancel signalled gracefully |
   | `125` | docker run failed | image/entrypoint problem, not your code |

   In GitHub Actions add `--rerun-failed-jobs` only AFTER you know why. Download the raw log (`gh run view <id> --log-failed`, GitLab "Complete Raw") — the web UI truncates and folds groups.

2. **Reproduce locally in the SAME image, not your laptop.** "Green on my machine" proves nothing if your machine isn't the runner. Run the actual job in its actual container:

   | CI | Local reproduce |
   |---|---|
   | GitHub Actions | `act -j <job> --container-architecture linux/amd64` (use the runner image: `-P ubuntu-latest=catthehacker/ubuntu:act-latest`) |
   | GitLab CI | `gitlab-runner exec docker <job>` or `glab ci run`; pull the exact `image:` |
   | CircleCI | `circleci local execute --job <job>` |
   | any | `docker run --rm -it <image>@<digest>` then run the steps by hand |

   Pin the image by **digest** (`@sha256:…`), not a moving tag — `ubuntu-latest`/`node:20` drift between your pull and the runner's. If it reproduces in the container but not on your host, the delta IS the bug (next step).

3. **Diff the environment — env-drift is the #1 silent cause.** Inside the reproduced container vs your host, compare:
   ```bash
   printenv | sort > /tmp/ci.env          # capture on CI (add `printenv|sort` as a debug step)
   <tool> --version                       # node/python/go/java/gcc — exact patch
   sha256sum package-lock.json poetry.lock go.sum   # lockfile parity
   uname -m && cat /etc/os-release        # arch (arm64 vs amd64!) + distro
   locale && echo $TZ                      # LANG/LC_ALL/TZ change sort & date tests
   ```
   Classic drifts: tool tag floated (`actions/setup-node@v4` with no exact version), `npm ci` vs `npm install` (lockfile ignored), `$PATH` ordering picks a different binary, `TZ`/`LANG` unset on the runner breaks date/sort tests, CI sets `CI=true` which flips test behavior. Fix = **pin** (digest + lockfile + exact tool version) → pin-toolchain-versions.

4. **Classify the failure — match symptom to cause, then run ONE experiment to confirm.** Don't guess and re-run; prove it:

   | Class | Tell-tale | Confirm by |
   |---|---|---|
   | **Flaky test** | passes on re-run, no code change, intermittent | re-run the SAME commit 10×; randomize order → debug-flaky-tests |
   | **Env/version drift** | green local, red CI; broke with no relevant diff | the env diff in step 3 |
   | **Poisoned/stale cache** | broke after a dep bump or cache-key collision; "works in clean checkout" | run with cache disabled (step 5) |
   | **Resource / OOM** | exit 137, "Killed", slow then dead | raise mem / lower parallelism; watch RSS |
   | **Missing/empty secret** | only on fork PRs, only on protected branches, `***` blank | `echo "len=${#SECRET}"` (never the value) |
   | **Timeout / deadlock** | exit 124/143, "cancelled after Nm" | run with `timeout` + thread dump on hang |
   | **Test-ordering** | fails only in CI's shard/order, passes in isolation | run that ONE test alone; then full suite |
   | **Network/flaky registry** | `ETIMEDOUT`/`ECONNRESET`/429 to npm/pypi/ghcr | retry; check it's not a hard dep on a live service |

5. **Run clean-vs-cached to convict the cache.** A poisoned or stale cache makes "works in a fresh checkout, fails in CI" — because CI restored a bad layer. Force a clean run and compare:
   - **GitHub Actions:** bump the cache `key` (e.g. `-v2`), or `gh cache delete <key>`, or set `actions/cache` to a key that won't hit. Re-run with `ACTIONS_STEP_DEBUG=true`.
   - **GitLab:** `CACHE_DISABLE=true` / clear via "Clear runner caches"; or change `cache:key`.
   - **Docker layer cache:** `docker build --no-cache --pull`; suspect a stale base layer if a `RUN apt-get`/`pip install` silently uses old pins.
   - **Package managers:** `npm ci` (not `install`), `pip install --no-cache-dir`, `go clean -cache`.

   If clean is green and cached is red → the cache is the cause: the key is too coarse (not keyed on lockfile hash) or restores across incompatible refs → caching-strategy to re-scope the key. If BOTH fail, the cache is innocent — move on.

6. **Isolate ONE matrix leg.** A matrix-only failure (only `windows-latest`, only `py3.12`, only `arm64`) is a portability bug, not a flake. Temporarily pin the matrix to the failing leg (`include:` just that combo) so you iterate on one red job, not 12. Common per-leg causes: path separators / line endings (CRLF) on Windows, glibc vs musl (alpine) for native deps, arch-specific wheels/binaries on arm64, a stdlib behavior that changed in the new language minor. Fix the portability issue, then restore the full matrix.

7. **Crank up debug logging and `set -x`.** The default log hides what ran. Turn on tracing:

   | CI | Debug switch |
   |---|---|
   | GitHub Actions | secrets/vars `ACTIONS_STEP_DEBUG=true` and `ACTIONS_RUNNER_DEBUG=true` |
   | GitLab CI | `variables: CI_DEBUG_TRACE: "true"` (⚠ leaks env — protected branch only) |
   | shell steps | add `set -euxo pipefail` to see every command + fail-fast on the real line |
   | any | echo `printenv\|sort`, `df -h`, `free -m`, `nproc`, tool `--version` as a debug step |

   `set -x` + `pipefail` alone fixes a whole class of "silent failure" where an early command in a pipe failed but the exit code was masked by the last one.

8. **Drop into an interactive runner when logs aren't enough.** For "I can't reproduce it locally and the log is opaque," open a live shell ON the runner:
   - **GitHub Actions:** `mxschmitt/action-tmate@v3` step (gates on failure) → SSH into the live runner mid-job; or `tmate` in a manual `workflow_dispatch`.
   - **GitLab:** interactive web terminal / `gitlab-runner --debug`; CircleCI: "Rerun job with SSH".
   - Inside: re-run the failing command by hand, inspect `/tmp`, check mounted caches, `cat` the generated config, `ps`/`top` for the OOM, `dmesg | tail` for the kill. Tear it down — don't leave a runner pinned.

9. **Convict resource/OOM with real numbers.** Exit 137 + "Killed" = the kernel OOM-killer. Don't just `continue-on-error` — measure: GitHub-hosted runners are ~7 GB / 2 cores; self-hosted/container jobs have a `--memory` cgroup limit. Add `/usr/bin/time -v <cmd>` (Max RSS), or `while true; do free -m; sleep 5; done &` to watch growth. Fixes: lower test parallelism (`-j2`, `--maxWorkers=2`, `pytest -n2`), raise the container/runner memory limit, split the job, or fix the actual leak. Node OOM specifically → `NODE_OPTIONS=--max-old-space-size=4096`.

10. **Fix the ROOT CAUSE, then re-run to confirm — never ship a blind re-run as the fix.** A green re-run on a flaky/poisoned/under-provisioned job is a false negative that WILL recur. The closing move per class: pin the digest+lockfile+tool version (drift), re-scope or invalidate the cache key (cache), raise the limit or cut parallelism (OOM), randomize-then-pin test order / fix the shared state (ordering/flake → debug-flaky-tests), add a retry-with-backoff ONLY for genuinely external network calls (and nothing else). Then re-run the SAME commit ≥3× to prove it's deterministically green. Quarantining a flaky test (skip + tracking issue) is acceptable as a *stopgap* to unblock the pipeline — but it's a TODO, not the fix.

## Common Errors

- **Hitting "Re-run job" until it's green and calling it fixed.** That's hiding a flaky/OOM/cache bug; it recurs and erodes trust in CI. Fix: classify (step 4) and fix the cause; re-run only to *confirm*.
- **"It passes on my machine" as proof.** Your laptop isn't the runner (arch, tool version, env, cache). Fix: reproduce in the exact image/digest (step 2).
- **Reading only the last red line.** The real error is usually higher; the last line is often a downstream symptom. Fix: read top-down, find the FIRST error + the exit code.
- **Treating exit 137 as a code bug.** It's OOM/kill, not your assertion. Fix: measure RSS, raise mem or cut parallelism (step 9).
- **Floating tags (`node:20`, `ubuntu-latest`, `@v4` minor).** They drift between your pull and CI's → "broke with no diff." Fix: pin by digest + lockfile + exact version (pin-toolchain-versions).
- **`npm install` / non-`ci` installs in CI.** Ignores the lockfile → different deps than local. Fix: `npm ci`, `poetry install --no-update`, `--frozen-lockfile`.
- **Blaming the test when it's the cache.** Stale restored layer fails a clean build. Fix: clean-vs-cached run (step 5) before touching the test.
- **Debugging the whole matrix at once.** 12 red legs hide which is the real bug. Fix: isolate the one failing leg (step 6).
- **`CI_DEBUG_TRACE`/printing secrets to debug.** Leaks credentials into logs. Fix: trace on protected branches only; print `${#SECRET}` length, never the value.
- **No `pipefail`, so a failed mid-pipe command exits 0.** Silent green on a broken step. Fix: `set -euo pipefail` in every shell step.
- **Empty secret on fork PRs read as a code bug.** Secrets aren't exposed to forks/`pull_request` from forks by design. Fix: recognize the class, use `pull_request_target` carefully or a label gate, not a value hunt.
- **Adding broad retries to mask flakiness.** Retrying a deterministic bug just burns minutes. Fix: retry ONLY external network I/O; fix logic/ordering/resource causes.

## Verify

1. **Reproduced in-image:** the failure reproduces with `act`/`gitlab-runner exec`/`docker run @digest` (or you've proven via env-diff exactly what the runner has that you don't) — not just observed in the web UI.
2. **Classified, not guessed:** you can name the class (flaky / env-drift / cache / OOM / secret / timeout / ordering / network) AND state the experiment that confirmed it (clean-vs-cached, isolated test, RSS measurement, env diff).
3. **Exit code accounted for:** you read the real exit code and it's consistent with the diagnosis (137→OOM, 124/143→timeout, 1/2→real error).
4. **Root cause fix, not a re-run:** the diff pins/invalidates/scopes/limits the actual cause; there's no bare "Re-run" or blanket `continue-on-error` standing in for a fix.
5. **Determinism proven:** the SAME commit is re-run ≥3× (and for a flake, ≥10×) and is green every time — not green once after N reds.
6. **No new leak:** debug tracing is off (or gated to protected branches), no secret value was printed, and interactive runners were torn down.
7. **Matrix restored:** if you isolated a leg, the full matrix is back and all legs pass.

Done = the failure was reproduced in the runner's actual image, classified into one named cause confirmed by a targeted experiment (env diff / clean-vs-cached / isolated test / RSS), and fixed at the root (pin, cache-key, limit, order) — proven by the same commit going green ≥3× with no blind re-run, no masking, and no leaked secrets.
