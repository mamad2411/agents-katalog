---
name: kos-zai-run-failure-prevention
description: Prevent the known failure modes of zai/Claude agent runs (the GitHub Actions workflows that drive Claude Code via the run-zai action). Canonical taxonomy + per-mode prevention.
user-invocable: true
when_to_use: "Before or during any task executed inside a run-zai / claude-code-action workflow run, or when diagnosing why one failed."
category: utilities
argument-hint: "[failed-run-id or workflow name]"
keywords: [zai, claude-code-action, run-zai, failure, ci, workflow, denial, rate-limit, turn-limit]
related: [kos-run-log-mining, kos-claude-turn-budget, kos-trigger-policy-trust-gate, kos-runner-disk-hygiene, kos-commit-and-push-branch]
metadata:
  author: kos-workflow-improvement
  attribution: distilled from .github/workflows/scripts/scan-claude-logs.cjs + mined run logs
  license: repo
  version: "1.0"
---

# Idea

These repos run Claude Code inside GitHub Actions through the `run-zai` action (`.github/actions/run-zai/action.yml`), which calls the Z.AI Anthropic-compatible API. Runs fail in a small, **already-classified** set of ways. `scan-claude-logs.cjs` is the source of truth for that taxonomy. This skill is the operator-facing mirror: what each mode looks like and how to **prevent** it next run.

## When to invoke this skill directly

- You are operating inside a workflow run (the prompt told you a `/gsd:*` command + a task) — apply prevention up front.
- You are diagnosing a red run before re-dispatching it.
- You are editing a workflow YAML / prompt / `allowed-tools` list and want to avoid reintroducing a known mode.

## References

- `.github/actions/run-zai/action.yml` — runtime wrapper; exposes `claude_failed`, `claude_failure_reason`, `claude_has_findings`, denial/turn metrics.
- `.github/workflows/scripts/scan-claude-logs.cjs` — canonical finding categories (do not re-derive; this is the authority).
- `.github/workflows/scripts/classify-claude-retry.cjs` — decides retry vs. give-up for rate/overload errors.
- `.github/actions/report-failure/` — opens the failure issue when a run goes red.

## Communication Style

Lead with the single most likely mode, cite the metric/line that proves it, then the one-line prevention. Do not enumerate all 12 modes unless asked.

## Core Principles

YAGNI / KISS / DRY. Reuse `scan-claude-logs.cjs` categories verbatim — do not invent new names for the same failure. One prevention per mode; prefer fixing the workflow (allowlist, prompt scope, disk) over adding runtime checks.

## The canonical failure taxonomy (operator view)

| Mode (scan category) | Signal in run | Root cause | Prevention |
|---|---|---|---|
| `non_human_actor` | "Workflow initiated by non-human actor … allowed_bots" / Claude refused | Bot actor not in `allowed-bots` | Add the bot login to `run-zai: allowed-bots`, or dispatch from a trusted actor |
| `permission_denials` | `num_rejected_tool_calls > 0`, "DISALLOWED_TOOLS" | Agent called a tool not in `allowed-tools` | Add the exact tool spec to `allowed-tools` (e.g. `Bash(npm:*)`); >5 denials = hard fail |
| `failed_tool_calls` | `num_failed_tool_calls > 0` + samples | Tool ran but errored (bad path, bad flag, missing file) | Fix the call; the sample's `tool/category: command` names it |
| `git_push_403` | "fatal: unable to access … returned error: 403" | Push token lacks write / wrong remote | Use `GH_PAT` with `contents: write`; push via setup-bot-git identity |
| `graphql_pr_fail` | "pull request create failed: GraphQL:" | PR creation hit a GraphQL error | Retry; check for duplicate-PR guard (`find-duplicate-automation-pr.cjs`) |
| `turn_limit_hit` | `num_turns >= max_turns` + `is_error` | Task too big for turn budget | Apply [[kos-claude-turn-budget]]; narrow the prompt; raise `MAX_TURNS` deliberately |
| `zero_turns` | `num_turns == 0` | Agent did nothing (gate/prompt/parse) | Verify trigger fired and prompt is non-empty; check `action_not_found` |
| `rate_limited` | `is_rate_limited=true` x3, or "529 / temporarily overloaded" | Z.AI API overloaded | Already retried 3x by runtime; re-dispatch later; not a code bug |
| `action_not_found` | "Can't find 'action.yml'" | Wrong action path / missing checkout | Fix `uses:` path; ensure checkout ran first |
| `internal_error` | "Internal error: directory mismatch" | Stray worktree / checkout artifact | Clean worktree dirs; benign if isolated |
| `graphql_user_err` | "Failed to fetch user display name … GraphqlResponseError" | Transient GitHub user fetch | Benign/warning; ignore unless blocking |
| `uncategorized` | "N unrecognized error(s)" | New pattern not yet classified | Capture the message; consider adding a `scan-claude-logs.cjs` detector |

Soft failures: a run may exit 1 with `claude_soft_success=true` ("Claude soft failure: claude-code-action step failed"). Treat as "agent produced output but the wrapper flagged a recoverable issue" — read `claude_soft_success_reason` before assuming total failure.

## Your Approach

1. **Classify, don't guess.** Pull `claude_failure_reason` / `claude_has_findings` outputs first (they already ran the scanner). Only read raw logs for the one flagged mode.
2. **Fix the workflow, not the symptom.** A denial → allowlist; a turn limit → scope; disk-full → ensure-disk-space. The fix lives in YAML/prompt, not in agent cleverness.
3. **Distinguish retryable from structural.** `rate_limited` / `graphql_user_err` = re-dispatch. `non_human_actor` / `permission_denials` / `git_push_403` = edit the workflow.

## Process Flow (Authoritative)

1. Identify the run's conclusion + `claude_failure_reason` (workflow summary, not raw log).
2. Map to one taxonomy row above.
3. Apply that row's Prevention.
4. If `uncategorized`: extract the message, propose a new `scan-claude-logs.cjs` detector, and add it — do not leave it uncategorized.

## Output Format

```text
MODE: <category>  |  EVIDENCE: <metric or log line>  |  FIX: <one-line workflow change>
```

## Output Requirements

- Always name the exact `allowed-tools` / `allowed-bots` / action / script to touch.
- Never recommend "retry blindly" for a structural mode.
- If a mode recurs across ≥3 runs of a workflow, escalate to editing the workflow prompt to prevent it at the source.

## Critical Constraints

- Do not rename scan categories — downstream reports key on them.
- Do not silence `permission_denials` by widening `allowed-tools` beyond what the task needs (least privilege).
- `rate_limited` is never "fixed" by code; it is re-dispatched.
