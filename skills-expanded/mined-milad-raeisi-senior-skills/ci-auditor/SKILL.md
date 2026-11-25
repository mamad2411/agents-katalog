---
name: ci-auditor
description: Audit GitHub Actions CI speed with data instead of guesses. Use when the user says CI is slow, asks why builds or checks take so long, wants to cut CI minutes or cost, asks for a pipeline or workflow performance report, or before anyone edits workflows to "speed things up". Pulls the last 150 runs with gh, splits every job's time into queue wait for a runner, setup (checkout, toolchains, dependency install, cache restore), and the actual task, then reports the 5 slowest jobs with seconds for each part. Report first; changes nothing until the user approves specific changes.
license: MIT
metadata:
  category: senior-five
  version: "1.2.0"
---

# CI Auditor

> *Audit this repo's CI: use gh to pull the last 150 CI runs and split each job's time into three parts: waiting in the queue for a machine, setup (checkout, installing dependencies, restoring the cache), and actually running the task. List the 5 slowest jobs and how many seconds each part takes. Give me the report first. Don't change anything.*

"CI is slow" has three different causes with three different cures, and guessing wrong wastes a week. Caching does nothing for a job that waits ten minutes for a runner; bigger runners do nothing for a job that spends most of its time running `npm ci`. Measure first, split the time, then propose fixes for the part that actually dominates.

**This skill is read-only.** Don't edit workflows, re-run or cancel jobs, or change repository settings while auditing. The deliverable is a report; changes come after the user picks them.

## Step 1: Preconditions

```bash
gh auth status                 # must be logged in
gh run list --limit 1          # repository must have GitHub Actions runs
```

If the repo uses a different CI system (GitLab CI, CircleCI, Buildkite, Jenkins), say so and apply the same three-part method with that system's API. The bundled script only covers GitHub Actions.

## Step 2: Collect and split the data

Run the bundled script from this skill's directory. It needs Python 3.9+ (standard library only) and `gh`, and sends GET requests only.

```bash
python3 <this-skill-dir>/scripts/ci_audit.py --runs 150 --top 5 \
  --save-raw "${TMPDIR:-/tmp}/ci-raw.json" --out "${TMPDIR:-/tmp}/ci-audit.md"
```

Useful options:

| Option | Use |
|---|---|
| `--repo OWNER/REPO` | Audit a repo other than the current directory's |
| `--workflow ci.yml` / `--branch main` | Focus on one workflow or branch |
| `--rank-by median\|p90\|sum` | Slowest typical run (default), worst tail, or most total minutes (cost) |
| `--min-runs 3` | Ignore jobs that ran too rarely in the window for a meaningful median |
| `--group-matrix` | Merge matrix variants into one row per job |
| `--setup-pattern REGEX` / `--run-pattern REGEX` | Correct step classification for this repo |
| `--from-raw FILE` | Re-analyze data saved with `--save-raw`, without hitting the API again |
| `--format json` | Machine-readable output |

Write output files to a scratch or temporary location rather than the repo, so the audit leaves the working tree untouched.

**How the split works**

| Part | Definition |
|---|---|
| Queue | `started_at - created_at` of the job: time waiting for a runner. GitHub creates a job only when its `needs:` are satisfied, so waiting on upstream jobs is not counted as queue. |
| Setup | Steps classified as setup by name: `Set up job`, checkout, `setup-*` actions and toolchains, dependency installs (`npm ci`, `pip install`, `uv sync`, `go mod download`, ...), cache restore and save, service containers, registry logins, artifact downloads, `Post ...` cleanup, `Complete job`. |
| Run | The rest of the job's execution time: the actual build, test, lint, or deploy work. |

Skipped and cancelled jobs are excluded. Seconds are medians per job execution, and p90 shows the tail.

## Step 3: Sanity-check the classification

Read the "Biggest steps" line for each of the top jobs. Step names are free text, so a repo-specific step like `Prepare test database` or `Install script smoke test` may land in the wrong bucket. If one does, re-run with `--from-raw` and a `--setup-pattern` or `--run-pattern` override, and mention the correction in the report. Look for a few outliers too: a p90 far above the median usually means flaky retries, cache misses, or runner contention.

Check the **Runs** column as well. If the top rows are one-off jobs (a release build that ran once), they may still deserve a mention, but re-run with `--min-runs 3` to show what slows down everyday CI, and with `--rank-by sum` to show where most of the minutes (and money) go.

## Step 4: Diagnose by dominant part

| Dominant part | Likely causes | Candidate fixes |
|---|---|---|
| **Queue** | Too few runners for the concurrency; self-hosted pool undersized; large or GPU runners scarce; org-wide concurrency limits; jobs serialized by `concurrency:` groups | More or autoscaled runners; fewer redundant jobs per push (path filters; a `concurrency` block with `group: ${{ github.workflow }}-${{ github.ref }}` and `cancel-in-progress: true`); move light jobs to standard runners |
| **Setup** | Cache misses (bad keys, cache evicted, cache saved only on main); installing toolchains every run; full-history checkout; installing all dependencies for a lint job | Lockfile-keyed caches; built-in caching in `setup-*` actions; `fetch-depth: 1`; prebuilt container images; narrower installs per job |
| **Run** | Serial test suite; rebuilding everything on every change; slow individual tests; under-powered runners for compile-heavy work | Sharding and parallelism; affected-only tests and builds; build caching (sccache, Turborepo, Nx, Bazel); profiling the slowest tests; larger runners for CPU-bound jobs |

Every proposed fix should name the job it targets, the part it shrinks, an estimated saving in seconds (derived from the measured numbers, not hope), and your confidence.

## Step 5: Report, then stop

Lead with the table the user asked for, then findings, then proposals. Nothing is applied yet.

```markdown
## CI audit: OWNER/REPO (last 150 runs, DATE to DATE)

**Headline:** Setup is 41% of all job-time; the `test` job spends 95s of its 160s median installing dependencies.

| # | Job | Runs | Queue s | Setup s | Run s | Total s | p90 s |
|---|-----|------|---------|---------|-------|---------|-------|
| 1 | ... |

### Findings
1. ... (evidence: step names and seconds)

### Proposed changes (not applied)
| # | Change | Target job / part | Est. saving per run | Confidence |
|---|--------|-------------------|---------------------|------------|

Reply with the numbers you want applied.
```

After the user approves specific items, implement only those, and verify with a fresh run where possible: compare the same job's median before and after.

## Caveats to mention when relevant

- Step timestamps have one-second resolution, so very short steps round to 0 or 1 second.
- Re-run attempts are reported under the run's latest attempt.
- Jobs waiting on environment protection rules (manual approvals) show inflated queue time.
- A small window or a quiet repo produces noisy medians; say how many executions each row is based on.
