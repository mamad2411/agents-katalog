---
name: github-repo-transfer-completion-poll
description: >-
  Wait until the transferred repositories land under the destination owner
  (HTTP 200 on repos/<destination>/{item}) using github-api-poll-until, and
  report landed vs pending repos. Read-only.
category: GitHub
---

# GitHub Repo Transfer Completion Poll Skill (v1)

> **Skill ID:** `github-repo-transfer-completion-poll`<br>
> **Version:** 1.0.0<br>
> **Standard:** [Agent Skills (agentskills.io)](https://agentskills.io)<br>
> **Layer:** Composer (per [`skill-factory` §2.0 Layering Decision](../../../skill-factory/SKILL.md))

## Description

Waits until every repository in the transfer set resolves under the
**destination** owner (HTTP 200 on `repos/<destination>/{item}`), using
[`github-api-poll-until`](../../github-api-poll-until/SKILL.md) (which in turn
composes [`poll-until`](../../../general/polling/poll-until/SKILL.md)). Emits a
`landed` / `pending` summary — completion after acceptance is asynchronous
(a ~70 s outlier was observed for one repo).

## Composition Rationale

Completion detection is an API wait, and the API wait already exists as
[`github-api-poll-until`](../../github-api-poll-until/SKILL.md). This skill
frames it in transfer terms: the destination-owner endpoint template, the
transfer repo set, and the landed/pending summary that the run report consumes.

## Related Skills

- [`github-repo-transfer-destination-conflict-check`](../github-repo-transfer-destination-conflict-check/SKILL.md)
  — the pre-initiation gate (same pipeline).
- [`github-repo-transfer-baseline-capture`](../github-repo-transfer-baseline-capture/SKILL.md)
  — the pre-transfer baseline (same pipeline).
- [`github-repo-transfer-verify`](../github-repo-transfer-verify/SKILL.md) —
  the post-transfer verification stage.

## 1. When to Apply

Use this skill after the transfer has been accepted:

- Wait until the repos appear under the destination owner before verifying.
- Report which repos have landed and which are still pending.

**Anti-trigger:** For generic endpoint waits (not transfer completion), use
[`github-api-poll-until`](../../github-api-poll-until/SKILL.md) directly.

## 2. Why a Dedicated Completion Stage

| Option | Verdict | Reason |
| --- | --- | --- |
| Assume completion once accepted | ❌ | completion is asynchronous; a ~70 s outlier was observed |
| Ad-hoc `sleep` then check | ❌ | unbounded guessing; no landed/pending record |
| This stage over the API poller | ✅ | bounded budget; per-item verdicts; landed/pending summary for the report |

Language tier: **Python 3 (Tier 1)** per
[`scripting-language-selection-rules.md` §2](../../../../../ai-agent-rules/scripting-language-selection-rules.md).

## 3. Required Inputs & Environment

| Requirement | Minimum | Notes |
| --- | --- | --- |
| `gh` CLI | authenticated for the destination account | `--token-user` selects another account's token |
| Destination owner | `--destination-owner <login>` | account receiving the repos |
| Transfer repo set | `--repos` and/or `--repos-file` | repositories to wait for |
| Python | 3.12+ | pure stdlib; no pip dependencies |

## 4. Operational Logic

### 4.1 Script catalogue

| Script | Role | Exit codes |
| --- | --- | --- |
| `scripts/poll-transfer-completion.py` | stage driver — shells the API poller with the transfer-landing endpoint | `0` all landed · `1` any pending · `2` config error |

### 4.2 CLI contract

```bash
python3 scripts/poll-transfer-completion.py --destination-owner <login> \
    --repos a,b [--interval 15] [--attempts 20] [--token-user <login>]
```

| Option | Default | Purpose |
| --- | --- | --- |
| `--destination-owner <login>` | required | account receiving the repos |
| `--repos <csv>` / `--repos-file <path>` | — | transfer repo set |
| `--interval <seconds>` | `15` | pause between attempts |
| `--attempts <n>` | `20` | maximum attempts |
| `--token-user <login>` | ambient auth | destination account's token |

### 4.3 Output contract

The base poller's per-attempt JSONL streams through, then the transfer
summary. Exit `0` = all landed.

```json
{"landed": ["repo-a"], "pending": ["repo-b"]}
```

### 4.4 End-to-end example

```bash
SCRIPTS=.agents/skills/github/transfer/github-repo-transfer-completion-poll/scripts
python3 "$SCRIPTS"/poll-transfer-completion.py --destination-owner <destination-owner> \
    --repos repo-a,repo-b --interval 15 --attempts 20 --token-user <destination-login>
```

## 5. Composition by Higher-Level Skills

| Composer | Composition Mechanism |
| --- | --- |
| [`github-repo-account-transfer`](../github-repo-account-transfer/SKILL.md) | Stage 4 of the orchestrated account-transfer flow; its landed/pending summary gates the verification stage. |

## 6. Composition by This Skill

| Base | Invoked As | Supplied | Consumed Back |
| --- | --- | --- | --- |
| [`github-api-poll-until`](../../github-api-poll-until/SKILL.md) | `poll-api-until.py --endpoint repos/<destination>/{item} --expect 200 …` | destination owner + transfer repo set | per-attempt JSONL (streamed through) + met/unmet summary mapped to landed/pending |

## 7. Prohibited Behaviors

- Polling without a bound — `--attempts` always applies.
- Treating pending repos as landed — the summary distinguishes them.
- Re-implementing the wait — shell out to the API poller (§6).

## 8. Change History

| Timestamp | Summary of Changes | Rationale |
| --- | --- | --- |
| [2026-09-30 16:25] | Initial skill v1 created | Completion after acceptance is asynchronous; the pipeline needed a bounded landing wait with a landed/pending record |

## 9. Traceability

See [`TRACEABILITY.md`](TRACEABILITY.md) for session logs and provenance.

## 10. Changelog

See [`CHANGELOG.md`](CHANGELOG.md) for release history.
