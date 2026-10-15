---
name: buildgit
description: Jenkins CI/CD build pipeline monitor. Check build status, push and monitor builds, follow builds in real-time, and analyze build timing, executor capacity, pipeline structure, and queue contention. Use when the user asks about CI/CD status, build results, wants to push code and monitor the Jenkins build, asks if CI is passing, or needs help optimizing Jenkins throughput. Triggers include "check build", "build status", "is CI passing", "is the build green", "push and watch", "push and monitor", "what failed in CI", "why did the build fail", "follow the build", "watch the build", "trigger a build", "run the build", "why is Jenkins slow", "which agents are busy", "what is in the queue", "show pipeline structure", and "find the bottleneck".
license: MIT
---

# buildgit

A CLI for git operations and monitoring Jenkins CI/CD build pipelines.

## What this skill does

- replacement for `git push` command.  Instead of `git push` use `buildgit push`
- uses git to push changes then expects a Jenkins build to automatically start, then monitors it
- shows Jenkins build status in many different ways
- analyzes build timing, executor capacity, pipeline structure, and queue contention to enable build optimization
- uses Jenkins REST api to monitor and track a Jenkins pipeline build job
- any command unknown to `buildgit` is delegated to `git`, e.g. `buildgit log` would run `git log`

All paths in this document are relative to this SKILL.md file's directory, not the project root.

## How to use

```
what is the build status
```

```
push the staged changes and monitor the build.  fix any errors you find.
```


## Agent Workflow: Common Patterns

**IMPORTANT: `build` and `push` already follow the build to completion by default.**
Do NOT run `status -f` after `build` or `push` — that is redundant. The `-f` flag is only valid on the `status` subcommand.

Invoke commands from the skill directory, or use the full path to `scripts/buildgit` relative to this SKILL.md

| Goal | Command |
|------|---------|
| Commit is pushed, trigger a new build and watch it | `scripts/buildgit build` |
| Push unpushed commits and watch the resulting build | `scripts/buildgit push` |
| Watch a build that is already running or about to start | `scripts/buildgit status -f --once=60` |
| Check what the last build did (already finished) | `scripts/buildgit status` |
| Trigger a build without monitoring | `scripts/buildgit build --no-follow` |

**When to use `build` vs `push`:**
- Use `push` when you have commits to push — it pushes first, then monitors the Jenkins build triggered by that push.
- Use `build` when commits are already pushed (e.g. triggering a retry, or someone else pushed) — it triggers Jenkins directly without a git push.
- Do NOT use `push` if there is nothing to push; it will say "Everything up-to-date" and may not trigger a build.

**`-f` flag only works with `status`**, not with `build` or `push`. These are wrong:
- ~~`buildgit build -f`~~ — invalid, will error
- ~~`buildgit push -f`~~ — invalid, will error

## Commands

| Command | Purpose |
|---------|---------|
| `scripts/buildgit status` | Jenkins build status snapshot |
| `scripts/buildgit status <build#>` | Status of one build (`31`, `0`, `-1`, `-2`) |
| `scripts/buildgit status --line` | One-line status for latest build |
| `scripts/buildgit status -n <N> --line` | One-line status for latest N builds (oldest first) |
| `scripts/buildgit status --prior-jobs <N>` | Snapshot with N prior one-line builds before target build |
| `scripts/buildgit status -n <N>` | Full snapshot output for latest N builds (oldest first) |
| `scripts/buildgit status -n <N> --json` | JSONL snapshot output for latest N builds |
| `scripts/buildgit status -n <N> --no-tests` | One-line status while skipping test-report API calls |
| `scripts/buildgit status --format '<fmt>'` | One-line status with custom format string (implies --line) |
| `scripts/buildgit status --all` | Force full snapshot output |
| `scripts/buildgit -v status --all` | Full snapshot with untruncated failed-test details and stdout |
| `scripts/buildgit status --console-text [stage]` | Raw build console or one stage's console text; empty parent stages recurse into descendant substages |
| `scripts/buildgit status --list-stages [--json]` | List stage names or emit the raw stage array |
| `scripts/buildgit status -f --once` | Follow current/next build to completion, then exit (10s timeout) |
| `scripts/buildgit status -f --once=N` | Same, but wait up to N seconds for a build to start |
| `scripts/buildgit status -f --probe-all` | Follow the next build that starts on any multibranch branch |
| `scripts/buildgit status -f --probe-all --once` | Follow one multibranch branch build, then exit |
| `scripts/buildgit status -n <N> -f --once` | Show N prior builds then follow once with timeout |
| `scripts/buildgit status -f --line --once` | Follow builds with compact one-line output (TTY shows progress bar) |
| `scripts/buildgit status -f --prior-jobs <N>` | Follow with N prior one-line builds + estimate preamble |
| `scripts/buildgit status -n <N> -f --line --once` | Show N prior one-line rows then follow in one-line mode |
| `scripts/buildgit --threads '[%a] %S %p' status -f --line` | Follow with custom live per-stage row formatting on TTY |
| `scripts/buildgit status --json` | Machine-readable Jenkins build status |
| `scripts/buildgit push` | git push + monitor Jenkins build until complete |
| `scripts/buildgit push --prior-jobs <N>` | git push + preamble with N prior builds + estimate |
| `scripts/buildgit push --no-follow` | git push only, no build monitoring |
| `scripts/buildgit push --line` | git push + compact one-line monitoring (TTY shows progress bar) |
| `scripts/buildgit push --format '<fmt>'` | git push + compact one-line monitoring with custom format |
| `scripts/buildgit build` | Trigger a new build + monitor until complete |
| `scripts/buildgit build --prior-jobs <N>` | Trigger + preamble with N prior builds + estimate |
| `scripts/buildgit build --no-follow` | Trigger only, no monitoring |
| `scripts/buildgit build --line` | Trigger + compact one-line monitoring (TTY shows progress bar) |
| `scripts/buildgit build --format '<fmt>'` | Trigger + compact one-line monitoring with custom format |
| `scripts/buildgit agents` | Show Jenkins executor capacity by label |
| `scripts/buildgit agents --json` | Emit executor capacity and node details as JSON |
| `scripts/buildgit agents --label <name>` | Show executor capacity for one Jenkins label |
| `scripts/buildgit agents --nodes` | Pivot to one row per Jenkins node with all labels and busy/idle counts |
| `scripts/buildgit timing` | Show per-stage timing for the latest successful build |
| `scripts/buildgit timing --tests` | Include slowest test suites and test counts in timing output |
| `scripts/buildgit timing --tests --by-stage` | Group test suites under the pipeline stages that published them |
| `scripts/buildgit timing --compare <a> <b>` | Compare two builds side by side with signed per-stage deltas |
| `scripts/buildgit timing -n <N>` | Show a compact stage timing table across the latest N builds |
| `scripts/buildgit timing --tests --json` | Emit timing, parallel bottlenecks, and test suite timing as JSON |
| `scripts/buildgit timing -n <N> --json` | Emit timing JSON for the latest N builds |
| `scripts/buildgit pipeline` | Show pipeline structure, stage hierarchy, and parallel branches |
| `scripts/buildgit pipeline --json` | Emit pipeline graph, stage types, agent labels, and per-stage `testSuites` as JSON |
| `scripts/buildgit queue` | Show the current Jenkins queue and wait reasons |
| `scripts/buildgit queue --json` | Emit queued items, wait reasons, and queue duration as JSON |
| `scripts/buildgit --console auto status` | Show default console log on failure |
| `scripts/buildgit --console <N> status` | Show last N raw console lines on failure |
| `scripts/buildgit --job <name|name/branch> <cmd>` | Override auto-detected job name (supports multibranch) |
| `scripts/buildgit --version` | Show version number and exit |

Default one-line format (`status --line`, `push --line`, `build --line`) is:
`%s #%n id=%c Tests=%t Took %d on %I (%r)`

Default threads format (`--threads` on TTY monitoring) is:
`  [%-14a] %S %g %p %e / %E`

Threads placeholders are separate from `--format` placeholders:
`%a`=agent `%S`=stage `%g`=progress-bar `%p`=percent `%e`=elapsed `%E`=estimate `%%`=literal%
Use width/alignment like `%14a` or `%-14a`. `BUILDGIT_THREADS_FORMAT` sets the default when `--threads` has no explicit format argument.

## Interpreting Output

**Exit codes:**

| Code | Meaning |
|------|---------|
| 0 | Success (build passed, or git command succeeded) |
| 1 | Build failed, or an error occurred |
| 2 | Build is currently in progress |

**Build states:**  as reported by Jenkins
- `SUCCESS` — build passed, all tests green
- `FAILURE` — build failed; output includes failed stage and error details
- `BUILDING` — build is still running
- `ABORTED` — build was manually cancelled
- `UNSTABLE` — build completed with test failures or marked warnings (common for flaky tests)
- `NOT_BUILT` — build was skipped or not executed (e.g., due to upstream failure or explicit skip)
- `UNKNOWN` — the state could not be determined (e.g., API error, incomplete data)
- `QUEUED` — build is waiting in the Jenkins queue and hasn't started running yet
- `Tests=!err!` in line output means Jenkins test-report data could not be retrieved due to a communication failure (network/sandbox/API connectivity), not a test result.

For failures, summarize the failed stage name, error logs, and test failure details for the user.
When a failure needs more detail, prefer `scripts/buildgit -v status --json` for structured failed-test stdout and `scripts/buildgit status --console-text <stage>` after `scripts/buildgit status --list-stages`.
`--console-text <stage>` accepts exact, case-insensitive, and unique partial stage matches. If the requested parent stage has no direct log text, it walks descendant substages and emits their logs in pipeline order.
Normal build/status output goes to stdout, including queue updates, stage progress, completion summaries, and verbose diagnostics. stderr is reserved for invalid input, Jenkins communication failures, and transient TTY redraw sequences.
Full header output is condensed: `Trigger:` merges cause plus user (`Manual by …`, `SCM change`, `Timer`, `Upstream`), `Commit:` includes the subject line when available, and `Agent:` is a top-level field instead of a boxed Build Info section.
For jobs that trigger downstream builds, full output now shows a hierarchical `=== Test Results ===` tree with parent and child rows, while one-line output aggregates the `Tests=` counts across the whole tree. In `--json`, the top-level `test_results` totals match the line output and multi-job builds add a `breakdown` array with one entry per parent/downstream build; missing reports are represented as `null` counts.

For snapshot mode defaults, `scripts/buildgit status` prints one-line output by default on both TTY and non-TTY stdout (TTY adds color).
- Monitoring commands (`push`, `build`, `status -f`) print prior-jobs + estimated build time before monitoring starts
- `scripts/buildgit status -f --probe-all` only applies to multibranch jobs, waits on the top-level job, then switches to the detected `job/branch` build once Jenkins starts it
- Parallel branches with local `stages {}` blocks print as `Branch->Substage` rows under the branch, reuse the branch `║` marker and agent, expose `parallel_path` plus `parent_branch_stage` in `--json`, and `--threads` now shows the active `Branch->Substage` row live while follow-mode monitoring is running.

Build reference rules:
- `0` and `-0` mean latest/current build
- Negative values (`-1`, `-2`) are relative offsets from latest build
- Build reference and `-n` are mutually exclusive

**Console log (`--console`):**
On failed builds, buildgit shows a curated error summary by default.
- `--console auto` — force the default error log display even when test failures are present
- `--console N` — show last N raw console lines instead of curated summary (useful for troubleshooting)

For agent-safe follow mode, prefer:
- `scripts/buildgit status -f --once` to follow exactly one build and exit
- `scripts/buildgit status -f --probe-all --once` when the next multibranch build may start on a different branch than the current checkout

## Build Optimization

Use this workflow when the user wants to reduce build time or understand Jenkins contention:

1. Run `scripts/buildgit queue` to see whether builds are waiting on capacity or blocked by quiet periods.
2. Run `scripts/buildgit agents` to identify which executor labels are saturated or offline, then `scripts/buildgit agents --nodes` to see which physical nodes overlap those labels.
3. Run `scripts/buildgit timing --tests` on a recent successful build to find slow stages, parallel bottlenecks, and expensive test suites.
4. Run `scripts/buildgit timing --tests --by-stage` to map those suites back to the stages that published them, or `scripts/buildgit timing --compare <a> <b>` / `scripts/buildgit timing -n <N>` to measure whether a rebalance actually helped.
5. Run `scripts/buildgit pipeline` to understand stage ordering, parallel branches, agent-label placement, and per-stage test suite summaries, then use [references/build-optimization.md](references/build-optimization.md) for the full workflow and constraints.

## Dynamic Context

To inject live build state into context before reasoning about build issues:

```
`scripts/buildgit status --json 2>/dev/null`
```

## References

See [references/buildgit-setup.md](references/buildgit-setup.md) for setup instructions (required tools, fixing permission errors,project setup, needed network access, docker sandbox instructions)
See [references/reference.md](references/reference.md) for real-world output examples
(push failures, parallel pipelines, progress bars, live follow mode).
