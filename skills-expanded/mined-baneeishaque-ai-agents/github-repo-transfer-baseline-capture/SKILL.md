---
name: github-repo-transfer-baseline-capture
description: >-
  Capture the pre-transfer state fingerprint of the transfer repo set under the
  old owner via github-repo-state-fingerprint, and emit a transfer-scoped
  summary (snapshot path + per-repo head SHAs) for later verification stages.
  Read-only.
category: GitHub
---

# GitHub Repo Transfer Baseline Capture Skill (v1)

> **Skill ID:** `github-repo-transfer-baseline-capture`<br>
> **Version:** 1.0.0<br>
> **Standard:** [Agent Skills (agentskills.io)](https://agentskills.io)<br>
> **Layer:** Composer (per [`skill-factory` §2.0 Layering Decision](../../../skill-factory/SKILL.md))

## Description

Captures the pre-transfer state fingerprint of every repository in the transfer
set under the **old** owner via
[`github-repo-state-fingerprint`](../../repo/github-repo-state-fingerprint/SKILL.md)
(`capture` subcommand), then emits a transfer-scoped summary: the snapshot path
and a per-repo `head_sha` map that later verification stages assert against.

## Composition Rationale

The snapshot format and comparison semantics belong to the fingerprint base;
this skill frames the capture in transfer terms (old owner, transfer repo set,
named baseline artifact) and surfaces the `head_sha` map that the verification
stage consumes. No capture logic is duplicated.

## Related Skills

- [`github-repo-transfer-destination-conflict-check`](../github-repo-transfer-destination-conflict-check/SKILL.md)
  — the preceding pipeline stage (destination availability gate).
- [`github-repo-transfer-completion-poll`](../github-repo-transfer-completion-poll/SKILL.md)
  — the post-initiation landing wait (same pipeline).

## 1. When to Apply

Use this skill as the pre-transfer baseline stage:

- Before initiating transfers, snapshot the repos under the old owner.
- Produce the `head_sha` map used to prove SHA preservation after the transfer.

**Anti-trigger:** For non-transfer snapshots (settings changes, drift audits),
use [`github-repo-state-fingerprint`](../../repo/github-repo-state-fingerprint/SKILL.md)
directly.

## 2. Why a Transfer-Scoped Baseline

| Option | Verdict | Reason |
| --- | --- | --- |
| No baseline (verify "it looks fine") | ❌ | no evidence; SHA preservation unprovable |
| Ad-hoc `gh api` dumps per repo | ❌ | noisy fields; no comparison contract for later stages |
| This stage over the fingerprint base | ✅ | one snapshot file + SHA map; verification stages consume them verbatim |

Language tier: **Python 3 (Tier 1)** per
[`scripting-language-selection-rules.md` §2](../../../../../ai-agent-rules/scripting-language-selection-rules.md).

## 3. Required Inputs & Environment

| Requirement | Minimum | Notes |
| --- | --- | --- |
| `gh` CLI | authenticated for the old owner | `--token-user` selects another account's token |
| Old owner | `--old-owner <login>` | the account currently holding the repos |
| Transfer repo set | `--repos` and/or `--repos-file` | repositories to snapshot |
| Output path | `--output <path>` | snapshot file for later stages |
| Python | 3.12+ | pure stdlib; no pip dependencies |

## 4. Operational Logic

### 4.1 Script catalogue

| Script | Role | Exit codes |
| --- | --- | --- |
| `scripts/capture-transfer-baseline.py` | stage driver — shells the fingerprint `capture`, then emits the transfer summary | `0` all captured · `1` any missing/error · `2` config error |

### 4.2 CLI contract

```bash
python3 scripts/capture-transfer-baseline.py --old-owner <login> \
    --repos a,b --output baseline.json [--token-user <login>]
```

| Option | Default | Purpose |
| --- | --- | --- |
| `--old-owner <login>` | required | current owner of the repos |
| `--repos <csv>` / `--repos-file <path>` | — | transfer repo set |
| `--output <path>` | required | snapshot file to write |
| `--token-user <login>` | ambient auth | old owner's token |

### 4.3 Output contract

The base capture's JSONL streams through; the snapshot file is written; then
the transfer summary. Exit `0` = all captured.

```json
{"snapshot": "baseline.json", "old_owner": "<old-owner>", "captured": 2, "head_shas": {"repo-a": "abc123", "repo-b": "def456"}}
```

### 4.4 End-to-end example

```bash
SCRIPTS=.agents/skills/github/transfer/github-repo-transfer-baseline-capture/scripts
python3 "$SCRIPTS"/capture-transfer-baseline.py --old-owner <old-owner> \
    --repos repo-a,repo-b --output baseline.json --token-user <old-login>
```

## 5. Composition by Higher-Level Skills

| Composer | Composition Mechanism |
| --- | --- |
| [`github-repo-transfer-verify`](../github-repo-transfer-verify/SKILL.md) | Reads the emitted snapshot file and `head_shas` map to assert SHA/structure preservation in its comparison stages. |
| [`github-repo-account-transfer`](../github-repo-account-transfer/SKILL.md) | Stage 2 of the orchestrated account-transfer flow; its snapshot path is threaded into the verification stage. |

## 6. Composition by This Skill

| Base | Invoked As | Supplied | Consumed Back |
| --- | --- | --- | --- |
| [`github-repo-state-fingerprint`](../../repo/github-repo-state-fingerprint/SKILL.md) | `repo-state-fingerprint.py capture --owner <old-owner> --repos … --output …` | old owner + transfer repo set + snapshot path | per-repo JSONL (streamed through) + written snapshot file (read for the summary) |

## 7. Prohibited Behaviors

- Proceeding to initiation without a successfully captured baseline.
- Editing the snapshot file by hand — verification stages trust its bytes.
- Re-implementing capture logic — shell out to the fingerprint base (§6).

## 8. Change History

| Timestamp | Summary of Changes | Rationale |
| --- | --- | --- |
| [2026-09-30 16:20] | Initial skill v1 created | The transfer pipeline needed a named pre-transfer baseline stage with a SHA map for verification |

## 9. Traceability

See [`TRACEABILITY.md`](TRACEABILITY.md) for session logs and provenance.

## 10. Changelog

See [`CHANGELOG.md`](CHANGELOG.md) for release history.
