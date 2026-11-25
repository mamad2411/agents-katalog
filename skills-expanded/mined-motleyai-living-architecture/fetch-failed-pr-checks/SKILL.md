---
name: fetch-failed-pr-checks
description: Use when the user asks to check / fetch / list / show failed CI checks (GitHub Actions, external CI) on a GitHub PR — including details/logs of the failures. Pulls the statusCheckRollup, filters to non-passing terminal states, and (for GitHub Actions runs) appends a log excerpt, or why there is none.
---

**Preflight:** run `la-doctor --plugin <this skill's base directory>` once per session before using any `la-*` or `dr-*` command; if it fails, stop and show the user its output.

# Fetch failed CI checks (and their log excerpts) for a PR

## How to run

```bash
la-fetch-failed-pr-checks <PR_NUMBER> [--repo OWNER/REPO] [--max-log-lines N]
```

- `<PR_NUMBER>` — required.
- `--repo OWNER/REPO` — optional; defaults to the cwd repo via `gh repo view`.
- `--max-log-lines N` — cap each failed job's log excerpt at N lines (default 200). Pass `0` to skip log fetching entirely.

## Output

Always emits **both**:

- **Markdown to stdout** — one section per failed check: workflow / job name, conclusion, details URL, and either a log excerpt inside a collapsible `<details>` block whose summary names its source, or a line saying why there is none.
- **JSON file** at `${TMPDIR:-/tmp}/failed-pr-checks-<pr>-<utc-ts>.json`. Path printed on the last line, prefixed `JSON: `. Schema:

  ```json
  {
    "pr": 70,
    "repo": "owner/name",
    "failed_checks": [
      {
        "typename": "CheckRun" | "StatusContext" | "WorkflowRun",
        "name": "test",
        "workflow_name": "CI",
        "conclusion": "FAILURE",
        "status": "COMPLETED",
        "details_url": "https://github.com/.../actions/runs/12345/job/67890",
        "completed_at": "2026-05-03T07:42:13Z",
        "run_id": "12345",
        "job_id": "67890",
        "log_excerpt": "...",
        "log_source": "log-failed" | "log" | "api-step" | "api-errors-tail" | null,
        "log_attempts": [{"command": "gh run view --job 67890 --log-failed", "outcome": "empty log"}]
      }
    ]
  }
  ```

## What counts as "failed"

Any check whose `conclusion` (CheckRun/WorkflowRun) or `state` (StatusContext) is one of:

- `FAILURE`
- `TIMED_OUT`
- `CANCELLED`
- `ACTION_REQUIRED`
- `STARTUP_FAILURE`
- `ERROR` (StatusContext only)

In-progress / pending / skipped checks are excluded.

## Steps

1. Run the script with the PR number the user gave (or infer from `gh pr view --json number -q .number`).
2. Read the Markdown output and present a concise summary — count, which workflows / jobs failed, the most likely root cause if visible in the log excerpt.
3. The log excerpt comes from the first source that gives a log: `gh run view --log-failed`, then the tail of the full log (`--log`), then GitHub's job-log API sliced to the failed step (its `##[error]` lines plus the tail when the step can't be isolated). The `<details>` summary and `log_source` name the source; with no excerpt, the check lists each attempt and why it gave nothing. If the default 200-line excerpt isn't enough, re-run with a larger `--max-log-lines` (e.g. `--max-log-lines 1000`). Don't reach for `gh run view --log` directly — keep this workflow inside the command.

## Why use this instead of `gh pr checks` / `gh run view` directly

- One call gives you all failed checks plus a log excerpt of each, in both Markdown and JSON form.
- Handles the three `statusCheckRollup` typenames (CheckRun / StatusContext / WorkflowRun) — `gh pr checks` doesn't expose StatusContext cleanly.
- Truncated logs (default 200 lines per job) keep output bounded; raise with `--max-log-lines` when you need more.

If the command is missing a flag you need, extend it rather than reaching for `gh` directly.
