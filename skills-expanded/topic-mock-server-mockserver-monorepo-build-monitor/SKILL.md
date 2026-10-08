---
name: build-monitor
description: Continuously monitors Buildkite pipeline builds, detects failures, investigates root causes, fixes issues, and pushes fixes. Runs a polling loop that checks build status at configurable intervals for a configurable duration. Use when the user says "monitor builds", "watch pipeline", "watch CI", "continuous monitoring", "keep checking builds", or wants automated build-fix cycles.

---

# Buildkite Build Monitor

Continuously monitor the Buildkite pipeline, detect failures, investigate root causes, fix code issues, perform adversarial review, and push fixes — all in an automated loop.

## Tooling — use `scripts/ci/bk-pipeline-status.sh`

Do NOT re-derive the build polling/parsing each time. Use the reusable
`scripts/ci/bk-pipeline-status.sh`, which wraps the **reliable** `bk build list`
/ `bk job log` commands. (Prefer these over `bk auth token` + `curl` to the REST
API and over the AWS Secrets Manager tokens: only the local `bk` CLI dependably
has both build-state and `read_build_logs` scope here, and it does not need an
AWS SSO session — see [docs/infrastructure/ci-cd.md](../../../docs/infrastructure/ci-cd.md).)

```bash
# one-shot status of a build (by commit prefix, build number, or newest)
scripts/ci/bk-pipeline-status.sh -p mockserver-java -c <commitSha>
scripts/ci/bk-pipeline-status.sh -p mockserver-java -b <buildNumber>

# tail the failing job's log for investigation
scripts/ci/bk-pipeline-status.sh -p mockserver-java -b <buildNumber> --logs -n 80

# find the failure in the WHOLE log (the failure is usually NOT in the tail)
scripts/ci/bk-pipeline-status.sh -p mockserver-java -b <buildNumber> \
  --grep 'Tests run: [0-9]+, Failures: [1-9]|<<< (FAILURE|ERROR)|BUILD FAILURE|There was a timeout|npm error'

# raw JSON of the matched build (for classifying exit_status / agent state)
scripts/ci/bk-pipeline-status.sh -p mockserver-java -b <buildNumber> --json
```

It prints `build#<n> <commit> build=<state> <job>=<state> exit=<code>` and exits
`0` when the watched job passed, `2` when failed/broken/canceled, `3` on timeout.

**For continuous watching, drive it with the agent Monitor tool in `--watch`
mode** instead of an in-context polling loop — it emits one line per state change
and exits when terminal, so you are only re-invoked on a real change:

```
Monitor(command="scripts/ci/bk-pipeline-status.sh -p mockserver-java -c <commitSha> --watch")
```

The prose check-loop below is the fallback when a script run is not appropriate.

## Prerequisites — Authentication Check

Before starting the monitoring loop, verify ALL required authentication is in place. **Stop and report any failures** before proceeding.

### Step 1: Buildkite CLI

```bash
which bk || echo "FAIL: bk CLI not installed — run: brew tap buildkite/buildkite && brew install buildkite/buildkite/bk"
bk auth status 2>&1 | head -5
```

If not authenticated, ask the user to run `bk auth login` in a separate terminal — it requires interactive browser OAuth.

If org is not selected:

```bash
bk auth switch mockserver
```

### Step 2: GitHub CLI

```bash
gh auth status 2>&1 | head -3
```

Needed for pushing fixes and creating PRs if required.

### Step 3: Git Status

```bash
git status --porcelain
git branch --show-current
```

Verify:
- Working tree is clean (no uncommitted changes that would conflict with fixes)
- On `master` branch (or confirm which branch to monitor)

### Step 4: Report Authentication Status

Print a summary table:

```
Authentication Status:
  Buildkite CLI: OK (org: mockserver)
  GitHub CLI:    OK
  Git:           clean, on master
```

If any check fails, **stop and report** — do not start monitoring.

## Monitoring Loop

### Parameters

| Parameter | Default | Description |
|-----------|---------|-------------|
| `interval` | 10 minutes | Time between checks |
| `duration` | 90 minutes | Total monitoring duration |
| `branch` | `master` | Branch to monitor (ignore other branches) |
| `auto_fix` | `false` (report only) | When `false`, investigate and report fixes only — do not change files. When `true`, the loop fixes, runs the full commit-workflow gate chain, then commits and pushes autonomously per the DVRR operating model (gate failure ⇒ no commit). Default off so an unattended monitor does not change master unless explicitly enabled. |

Calculate total checks: `duration / interval` (e.g., 90/10 = 9 checks).

### Check Procedure

For each check iteration:

#### 1. Fetch Recent Builds

Use the reusable script (newest build of the pipeline, or a specific commit):

```bash
scripts/ci/bk-pipeline-status.sh -p mockserver           # newest build
scripts/ci/bk-pipeline-status.sh -p mockserver -c <sha>  # the build for a commit
```

Run it once per pipeline you track (`mockserver` for the top-level fan-out,
`mockserver-java` for the core test fork). It prints
`build#<n> <commit> build=<state> :maven: build=<state> exit=<code>`.

#### 2. Classify Builds

For each build on the monitored branch:

| State | Action |
|-------|--------|
| `passed` | Log as healthy. No action needed. |
| `running` | Log progress. Check again next interval. |
| `failed` | **Investigate** if not already investigated in this session. |
| `skipped` | Normal (superseded by newer commit). Ignore. |
| `canceled` | Log. No action. |

Track investigated build numbers to avoid re-investigating the same failure.

#### 3. Investigate Failures

For each new failed build:

**a. Classify the failure type:**

```bash
# job state + exit_status for the failed build
scripts/ci/bk-pipeline-status.sh -p mockserver-java -b {number}
# full build JSON (inspect each failed job's exit_status + agent connection_state)
scripts/ci/bk-pipeline-status.sh -p mockserver-java -b {number} --json
```

| exit_status | agent_state | Diagnosis |
|-------------|-------------|-----------|
| `1` | `connected`/`disconnected` | Build/test failure — investigate logs |
| `-1` | `lost` | Agent died (spot termination, OOM) — infrastructure issue, no code fix needed |
| `0` with failed state | any | Unusual — check pipeline config |
| `1`, passes on re-run / intermittent | `connected` | `FLAKY` — timing/ordering/port/resource related, not a deterministic code failure |

**Confirm flaky-vs-real before fixing:** if the failure looks
timing/ordering/port/resource-related, re-run the single failing test (or check
recent builds of the same commit) to confirm intermittency BEFORE classifying it
real-vs-flaky. If it passes on re-run, classify it `FLAKY` and do not push a
speculative code fix — log it as flaky and surface it.

**b. For build/test failures (exit_status=1):**

Launch the `pipeline-investigator` subagent:

```
Task(subagent_type="pipeline-investigator", prompt="Investigate Buildkite build #{number}...")
```

The investigator will return:
- Exact error messages
- Root cause analysis
- Affected files/modules
- Suggested fix

**c. For infrastructure failures (exit_status=-1, agent lost):**

Log the failure as infrastructure-related. Optionally trigger a rebuild:

```bash
bk build rebuild {number} -p mockserver -y
```

Do NOT attempt code fixes for infrastructure failures.

#### 4. Fix Code Issues

If the investigator identifies a code issue:

**a. Understand the fix:**
- Read the affected source files
- Understand the surrounding code context and conventions
- Plan the minimal fix

**b. Implement the fix:**
- Edit only the necessary files
- Follow existing code style and conventions
- Do NOT add comments unless the code is genuinely confusing

**c. Validate locally (if possible):**

For Java changes, run the specific failing test:

```bash
cd mockserver && ./mvnw test -pl {module} -Dtest={TestClassName}#{testMethodName} -Djava.security.egd=file:/dev/./urandom
```

Note: Full integration tests require the Docker CI image and may not run locally. Unit tests should run.

#### 5. Adversarial Review

Before committing, run the adversarial review defined in
`.opencode/rules/commit-workflow.md` Step 4 (a `review-cheap` subagent on a
different model with fresh context, applying the 8-lens review constitution):

```
Task(subagent_type="review-cheap", prompt="Adversarially review the following changes using .opencode/rules/review-constitution.md. Verdict PASS or BLOCK: {diff}")
```

If the verdict is BLOCK, address the feedback, re-verify, and re-run the review before committing.

#### 6. Commit and Push

Run only when `auto_fix` is enabled (it is off by default — see Parameters). When
enabled, the **gate chain is the authority to ship**, per the DVRR operating
model (`.opencode/rules/operating-model.md`): follow the full pre-commit workflow
in `.opencode/rules/commit-workflow.md` (classify → validate → changelog →
adversarial review with a PASS verdict → re-verify after any fix), then commit
and push to master autonomously — no separate human approval step.

**Fail-closed:** if any gate fails (tests red, review BLOCK, review subagent
unavailable), do NOT commit — report the failure and continue monitoring. A user
can interject at any time to halt or amend. Report the fix you applied:
```
Applied fix for build #{number}:
{git diff --stat output}
```

**Commit workflow:**

**a. Classify changed files:**

```bash
git diff --name-only
```

**b. Stage by explicit path (NEVER `git add .`):**

```bash
git add path/to/file1.java path/to/file2.java
```

**c. Commit with descriptive message:**

```bash
git commit -m "Fix {description of what was fixed}

{Brief explanation of root cause and fix}"
```

**d. Pull and push:**

```bash
git pull --rebase
git push
```

**e. Verify new build triggered:**

```bash
scripts/ci/bk-pipeline-status.sh -p mockserver                 # newest build of the orchestrator
scripts/ci/bk-pipeline-status.sh -p mockserver -c <newCommit>  # the build for the pushed fix
```

#### 7. Wait for Next Check

```bash
sleep {interval_seconds}
```

### Status Report

After each check, print a concise status report:

```
=== Build Monitor Check {N}/{total} — {timestamp} ===
Build #{number}: {state} ({branch})
  {jobs summary}
Action: {none|investigating|fixing|pushed fix|waiting for result}
Next check: {timestamp}
```

### End of Monitoring

After all checks complete, print a final summary:

```
=== Build Monitor Summary ===
Duration: {start} to {end}
Checks performed: {N}
Builds observed: {list of build numbers and states}
Failures investigated: {count}
Fixes pushed: {count}
Current pipeline status: {passing|failing|running}
```

## Failure Patterns Reference

| Error Pattern | Category | Typical Fix |
|---|---|---|
| `COMPILATION ERROR` | Build error | Fix Java source code |
| `Tests run:.*Failures:` | Test failure | Fix test or production code |
| `invalid target release` | JDK mismatch | Update Docker image or compiler config |
| `class file has wrong version` | JDK mismatch | Update Docker image |
| `OutOfMemoryError` | Resource | Increase JVM heap in build script |
| `exit_status: -1` + agent `lost` | Infrastructure | Rebuild (spot termination) |
| `Timeout` | Hanging test | Add test timeouts or fix deadlock |
| `Connection refused` | Port conflict | Fix parallel test isolation |
| Passes on re-run / intermittent across builds of same commit | `FLAKY` | Confirm by re-run; do not push a speculative code fix — log and surface |

## Important Rules

1. **Only fix failures on the monitored branch** (default: `master`). Ignore dependabot PR branches unless explicitly asked.
2. **Never amend commits that have been pushed.**
3. **Stage files by explicit path** — never `git add .` or `git add -A`.
4. **Pull before push** — `git pull --rebase` to handle concurrent changes.
5. **Check `git status` before committing** — if unexpected changes appear, stop and ask the user.
6. **Track investigated builds** — don't re-investigate the same failure.
7. **Infrastructure failures don't need code fixes** — just rebuild or wait.
8. **Rate limit rebuilds** — don't trigger more than one rebuild per check interval.
