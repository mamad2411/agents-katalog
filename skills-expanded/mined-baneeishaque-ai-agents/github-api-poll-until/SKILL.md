---
name: github-api-poll-until
description: >-
  Poll one or more GitHub API endpoints (per-item endpoint templates) until an
  expected HTTP status is observed, using the poll-until base engine with a
  gh api check command. Composite; emits per-item met/unmet verdicts.
category: GitHub
---

# GitHub API Poll Until Skill (v1)

> **Skill ID:** `github-api-poll-until`<br>
> **Version:** 1.0.0<br>
> **Standard:** [Agent Skills (agentskills.io)](https://agentskills.io)<br>
> **Layer:** Composer (per [`skill-factory` §2.0 Layering Decision](../../skill-factory/SKILL.md))

## Description

Polls GitHub API endpoints until an expected HTTP status appears. Each item is
substituted into an endpoint template (`{item}` placeholder), checked with
`gh api --include`, and polled by the
[`poll-until`](../../general/polling/poll-until/SKILL.md) base engine with a bounded
attempt budget. Emits the base engine's per-attempt JSONL plus a per-item
`met` / `unmet` summary.

## Composition Rationale

This skill is a thin domain composite: the bounded retry loop, attempt budget,
per-attempt timeout, and JSONL timeline all belong to the base engine; this
skill contributes only the GitHub-specific check — `gh api` status
classification against `--expect`. Composing instead of re-implementing keeps
one polling contract across all waiters.

## Related Skills

- [`email-poll-for-message`](../../email/email-poll-for-message/SKILL.md) — the
  mailbox analogue of this composite (same base engine).
- [`github-repo-commit-fetch`](../../github-repo-commit-fetch/SKILL.md) — read
  primitive for inspecting what a polled endpoint returns.
- [`github-actions-run-audit`](../../github-actions-run-audit/SKILL.md) —
  audits workflow runs; polling for run completion has this composite's shape.

## 1. When to Apply

Use this skill whenever a GitHub API condition must be waited for with a
bounded budget:

- Wait until a transferred repository becomes resolvable under the new owner
  (`repos/<destination>/{item}` reaching 200).
- Wait until a newly created resource becomes readable (repos, releases,
  deployments, workflow runs).
- Wait until a resource disappears (expect 404 after a deletion).

**Anti-trigger:** If the condition is checkable exactly once, run the `gh api`
check directly. If the wait is for a workflow run's completion,
[`github-actions-run-audit`](../../github-actions-run-audit/SKILL.md) owns that
domain.

## 2. Why a Composite (Not Ad-Hoc `sleep` + `gh api` Loops)

| Option | Verdict | Reason |
| --- | --- | --- |
| Ad-hoc `sleep` + `gh api` loops per workflow | ❌ | no shared timeline; attempt budgets drift per caller |
| Tool-specific waiters (`gh run watch`, …) | ⚠️ | not available for arbitrary endpoints (e.g., transfer landing) |
| This composite over `poll-until` | ✅ | bounded budget + per-attempt JSONL + per-item verdicts; `{item}` templating covers many items |

Language tier: **Python 3 (Tier 1)** per
[`scripting-language-selection-rules.md` §2](../../../../ai-agent-rules/scripting-language-selection-rules.md).

## 3. Required Inputs & Environment

| Requirement | Minimum | Notes |
| --- | --- | --- |
| `gh` CLI | authenticated | `--token-user` selects another account's token |
| Endpoint template | must contain `{item}` | e.g. `repos/<owner>/{item}` |
| Items | `--items` and/or `--items-file` | repo names, logins, or any path segment |
| Python | 3.12+ | pure stdlib; no pip dependencies |

## 4. Operational Logic

### 4.1 CLI contract

```bash
python3 scripts/poll-api-until.py --endpoint "repos/<owner>/{item}" --items a,b \
    [--expect 200] [--interval 10] [--attempts 12] [--token-user <login>]
```

| Option | Default | Purpose |
| --- | --- | --- |
| `--endpoint <template>` | required | endpoint path with `{item}` placeholder |
| `--items <csv>` / `--items-file <path>` | — | items substituted into the template |
| `--expect <status>` | `200` | HTTP status that counts as met |
| `--interval <seconds>` | `10` | pause between attempts (base engine) |
| `--attempts <n>` | `12` | maximum attempts (base engine) |
| `--token-user <login>` | ambient auth | run checks with this account's token |

### 4.2 Output contract

Per-attempt JSONL from the base engine (streamed through), then a per-item
summary. Exit `0` = all met, `1` = any unmet, `2` = usage error.

```json
{"met": ["repo-a"], "unmet": ["repo-b"], "expect": 200}
```

### 4.3 End-to-end example

```bash
SCRIPTS=.agents/skills/github/github-api-poll-until/scripts
python3 "$SCRIPTS"/poll-api-until.py --endpoint 'repos/<owner>/{item}' \
    --items repo-a,repo-b --expect 200 --interval 10 --attempts 12 --token-user <login>
```

## 5. Composition by Higher-Level Skills

| Composer | Composition Mechanism |
| --- | --- |
| [`github-repo-transfer-completion-poll`](../transfer/github-repo-transfer-completion-poll/SKILL.md) | Shells out to `poll-api-until.py` with the transfer-landing endpoint under the destination owner (`repos/<destination>/{item}`, expect 200); consumes the per-item met/unmet summary to report landed vs pending repositories. |

## 6. Composition by This Skill

| Base | Invoked As | Supplied | Consumed Back |
| --- | --- | --- | --- |
| [`poll-until`](../../general/polling/poll-until/SKILL.md) | `poll-until.py --interval … --attempts … -- <check>` per item | a `_check` command (`gh api --include` status compare) with the resolved endpoint | per-attempt JSONL (streamed through) + exit code per item |

## 7. Prohibited Behaviors

- Re-implementing the polling loop — shell out to `poll-until.py` (see §6).
- Polling without a bound — `--attempts` always applies.
- Passing tokens as command-line arguments — token resolution uses
  `gh auth token` into the subprocess environment only.
- Treating a mismatched status as met — only `--expect` counts.

## 8. Change History

| Timestamp | Summary of Changes | Rationale |
| --- | --- | --- |
| [2026-09-30 15:45] | Initial skill v1 created | Transfer-landing waits and other endpoint waits needed a bounded, per-item API poller over the poll-until engine |

## 9. Traceability

See [`TRACEABILITY.md`](TRACEABILITY.md) for session logs and provenance.

## 10. Changelog

See [`CHANGELOG.md`](CHANGELOG.md) for release history.
