---
name: kos-run-log-mining
description: Extract knowledge from zai workflow run logs efficiently (status/conclusion rollup first, then surgical --log-failed grep) using gh + scan-claude-logs, without burning context on full logs.
user-invocable: true
when_to_use: "When investigating why a workflow or set of runs failed, or mining runs for repeated patterns across the 5 knowledge categories."
category: utilities
argument-hint: "[workflow-name or run-id]"
keywords: [gh-run, logs, mining, diagnosis, scan-claude-logs, conclusion, failures]
related: [kos-zai-run-failure-prevention, kos-gh-automation-tooling]
metadata:
  author: kos-workflow-improvement
  attribution: distilled from analyze-claude-runs.sh + scan-claude-logs.cjs usage patterns
  license: repo
  version: "1.0"
---

# Idea

Run logs are huge; reading them top-to-bottom wastes the context budget and hides the signal. The efficient pattern is layered: (1) roll up conclusions across runs, (2) read the failure reason the scanner already computed, (3) only then `--log-failed` + grep the one failing step. This skill codifies that order so diagnosis is fast and grounded.

## When to invoke this skill directly

- You are diagnosing one failed run.
- You are mining the latest N runs of a workflow for repeated patterns.
- You need to extract knowledge across the categories (repeated issues, re-derived knowledge, incorrect behavior, lacked knowledge, failed tool calls).

## References

- `gh run list --workflow <name>.yml --limit 30 --json conclusion,status,event` — rollup.
- `gh run view <id>` — job/step that failed.
- `gh run view <id> --log-failed` — only failed-step logs.
- `scan-claude-logs.cjs` outputs already attached to runs: `claude_failure_reason`, `claude_has_findings`, `claude_num_turns`, `claude_denial_rate`.
- `.github/workflows/scripts/analyze-claude-runs.sh` — batch analyzer.

## Communication Style

Lead with the conclusion rollup (counts), then the single dominant failure mode + evidence line. Keep raw log out of the main answer.

## Core Principles

YAGNI / KISS / DRY. Conclusions before logs. Scanner output before raw grep. One mode per run, cited with a metric/line.

## The 5 knowledge categories (map findings into these)

| Category | What it looks like in runs |
|---|---|
| (a) Repeated issues | Same `claude_failure_reason` across many runs |
| (b) Re-derived knowledge | Agent re-reads the same docs/scripts every run (could be a skill) |
| (c) Incorrect behavior | Agent takes a wrong/unsupported action repeatedly |
| (d) Lacked knowledge | Run blocked because a fact wasn't available (→ encode it) |
| (e) Failed tool calls / misuse | `num_failed_tool_calls>0`, denials, bad flags |

## Your Approach

1. **Rollup:** conclusion counts for the workflow's last 30 runs.
2. **Triage:** list the failed/cancelled run ids + their event.
3. **Reason first:** read each failure's `claude_failure_reason` (scanner) before raw logs.
4. **Surgical log:** `--log-failed` piped through a tight grep for error markers; cap with `head`.
5. **Categorize:** drop each finding into one of the 5 categories.

## Process Flow (Authoritative)

1. `gh run list … --json conclusion,status,event` → rollup.
2. Filter to non-success; collect ids.
3. For each: `gh run view <id>` → failing step; read scanner `failure_reason`.
4. If still unclear: `gh run view <id> --log-failed | grep -iE '<markers>' | head`.
5. Aggregate into the 5 categories; cite run id + line for each.

## Output Format

```text
ROLLOP: success=X fail=Y cancel=Z skip=W
DOMINANT MODE: <category> (n=<count>) — <evidence run-id:line>
OTHER: <mode> (n) ; <mode> (n)
CATEGORIES: (a).. (b).. (c).. (d).. (e)..
```

## Critical Constraints

- Never dump a full `--log` into context; use `--log-failed` + grep.
- `cancelled` usually means a newer run superseded it (concurrency) — confirm before treating as failure.
- `skipped` for gated workflows is the trust gate, not a failure (see [[kos-trigger-policy-trust-gate]]).
- Cite a run id + the matching line for every claimed pattern; no unsourced assertions.
