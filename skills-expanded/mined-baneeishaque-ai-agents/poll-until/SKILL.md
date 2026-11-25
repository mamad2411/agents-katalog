---
name: poll-until
description: >-
  Base primitive — bounded polling engine that repeats any check command until
  it succeeds or attempts are exhausted, emitting per-attempt JSONL plus a
  final verdict. Domain-agnostic; composed by GitHub API pollers, email
  waiters, and repo-transfer completion polls.
category: Automation
---

# Poll Until Skill (v1)

> **Skill ID:** `poll-until`<br>
> **Version:** 1.0.0<br>
> **Standard:** [Agent Skills (agentskills.io)](https://agentskills.io)<br>
> **Layer:** Base (per [`skill-factory` §2.0 Layering Decision](../../../skill-factory/SKILL.md))

## Description

A domain-agnostic base primitive for **bounded polling**: run a caller-supplied
check command every `--interval` seconds, up to `--attempts` times, until the
command exits with the success code (default `0`). It emits one JSON object per
attempt plus a final verdict object to stdout, so consumers can pipe the stream
and inspect the full timeline.

## Composition Rationale

This skill is a base primitive: the retry-until-condition loop was previously
re-derived ad hoc in every waiter (API waits, email waits, transfer-completion
polls). Extraction centralizes three contracts in one script — the bounded
attempt budget, the per-attempt JSONL record shape, and the final
`met` / `exhausted` verdict — so callers supply only the check command and its
arguments. Known composers:

- [`github-api-poll-until`](../../../github/github-api-poll-until/SKILL.md) —
  supplies a `gh api` check command over an endpoint template and consumes the
  per-item verdicts.
- [`email-poll-for-message`](../../../email/email-poll-for-message/SKILL.md) —
  supplies an IMAP search check command and consumes the match verdicts.
- [`github-repo-transfer-completion-poll`](../../../github/transfer/github-repo-transfer-completion-poll/SKILL.md)
  — supplies the transfer-landing check command and consumes the
  landed/pending timeline.

## Related Skills

- [`github-actions-workflow-dispatch`](../../../github-actions-workflow-dispatch/SKILL.md)
  — its optional wait-until-completed loop is a candidate future composition of
  this engine (currently self-contained).
- [`github-actions-run-audit`](../../../github-actions-run-audit/SKILL.md) —
  audits workflow runs; polling for run completion is the engine-shaped part of
  that workflow.
- [`repo-scratch-output-capture`](../../../repo-scratch-output-capture/SKILL.md)
  — redirect verbose per-attempt timelines into `scratch/` when needed.

## 1. When to Apply

Use this skill — or a higher-level composer of it — whenever a condition must
be **waited for with a bounded budget** and is checkable by a command whose
exit code encodes the answer. Examples:

- "Wait until `<api endpoint>` starts returning 200."
- "Wait until the confirmation email arrives in the mailbox."
- "Wait until the transferred repo resolves under the new owner."
- "Wait until a build artifact / lock file / marker file exists."

**Anti-trigger:** If the condition is checkable exactly once, just run the
check command directly. If the wait is unbounded or human-in-the-loop, use an
interactive prompt instead — this engine always terminates after
`--attempts`.

## 2. Why a Polling Engine (Not Ad-Hoc Sleep Loops)

| Option | Verdict | Reason |
| --- | --- | --- |
| Ad-hoc `for i in …; sleep …` prose loops | ❌ | re-derived per caller; no machine-readable timeline; typo-prone attempt budgets |
| `watch` / manual re-runs | ❌ | not agent-automatable; no verdict contract |
| Tool-specific waiters (`gh run watch`, …) | ⚠️ | domain-specific semantics; each tool reinvents its own loop |
| This engine + a check command | ✅ | one bounded-loop contract; per-attempt JSONL evidence; works for APIs, mailboxes, files, processes |

Language tier: **Python 3 (Tier 1)** per
[`scripting-language-selection-rules.md` §2](../../../../../ai-agent-rules/scripting-language-selection-rules.md).

## 3. Required Inputs & Environment

| Requirement | Minimum | Notes |
| --- | --- | --- |
| Python | 3.12+ | pure stdlib; no pip dependencies |
| Check command | any executable + args | passed as an **argv list** after `--`; never run through a shell |
| Success contract | exit code | default `0` = condition met (`--success-exit` to change) |

## 4. Operational Logic

### 4.1 CLI contract

```bash
python3 scripts/poll-until.py [options] -- <check-cmd> [args...]
```

| Option | Default | Purpose |
| --- | --- | --- |
| `--interval <seconds>` | `10` | pause between attempts |
| `--attempts <n>` | `12` | maximum attempts (hard bound) |
| `--success-exit <code>` | `0` | exit code that counts as met |
| `--attempt-timeout <seconds>` | `120` | per-attempt wall-clock limit |
| `--label <name>` | empty | label echoed into every record (multi-item callers) |

### 4.2 Output contract

One JSON object per attempt, then a final verdict object — all on stdout;
diagnostics on stderr. Exit `0` = met, `1` = exhausted, `2` = usage error.

```json
{"attempt": 1, "label": "", "exit_code": 1, "elapsed_s": 0.02, "met": false, "stdout_tail": "", "stderr_tail": ""}
{"verdict": "met", "attempts_used": 2, "total_elapsed_s": 10.05, "label": ""}
```

### 4.3 End-to-end example: wait for a marker file

```bash
SCRIPTS=.agents/skills/general/polling/poll-until/scripts
# Attempts 1..N fail until the marker exists; first success exits 0.
python3 "$SCRIPTS"/poll-until.py --interval 2 --attempts 5 -- test -f /tmp/ready.flag
```

## 5. Composition by Higher-Level Skills

| Composer | Composition Mechanism |
| --- | --- |
| [`github-api-poll-until`](../../../github/github-api-poll-until/SKILL.md) | Shells out to `scripts/poll-until.py` with a `gh api` check command per item (`--label` = item); consumes the per-attempt JSONL to report per-item landed/pending status. |
| [`email-poll-for-message`](../../../email/email-poll-for-message/SKILL.md) | Shells out to `scripts/poll-until.py` with a one-shot IMAP search command as the check; consumes the match verdict to report arrival. |
| [`github-repo-transfer-completion-poll`](../../../github/transfer/github-repo-transfer-completion-poll/SKILL.md) | Shells out to `github-api-poll-until` (which in turn invokes this engine) with the transfer-landing endpoint; consumes the timeline to report completion. |

## 6. Prohibited Behaviors

- Running the check command through a shell (`shell=True`) — argv execution only.
- Polling without a bound — `--attempts` always applies; callers must justify
  larger budgets in their own docs.
- Reimplementing the loop in composers — shell out to `poll-until.py` per the
  Composition Rationale.
- Using this engine as a scheduling daemon — it is a bounded waiter, not a cron.

## 7. Change History

| Timestamp | Summary of Changes | Rationale |
| --- | --- | --- |
| [2026-09-30 15:30] | Initial skill v1 created | Extraction of the retry-until-condition primitive from ad-hoc waiters (API / email / transfer-completion polls) |

## 8. Traceability

See [`TRACEABILITY.md`](TRACEABILITY.md) for session logs and provenance.

## 9. Changelog

See [`CHANGELOG.md`](CHANGELOG.md) for release history.
