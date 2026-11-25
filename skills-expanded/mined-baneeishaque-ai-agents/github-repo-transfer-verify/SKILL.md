---
name: github-repo-transfer-verify
description: >-
  Verify a completed GitHub repository transfer by comparing the pre-transfer
  fingerprint baseline against both owners — every repo must be missing from
  the old owner and identical (ok) under the destination owner. Composes
  repo-state-fingerprint compare twice.
category: GitHub
---

# GitHub Repo Transfer Verify Skill (v1)

> **Skill ID:** `github-repo-transfer-verify`<br>
> **Version:** 1.0.0<br>
> **Standard:** [Agent Skills (agentskills.io)](https://agentskills.io)<br>
> **Layer:** Composer (per [`skill-factory` §2.0 Layering Decision](../../../skill-factory/SKILL.md))

## Description

Verifies a completed repository transfer with a two-sided fingerprint audit: the
pre-transfer baseline (from
[`github-repo-transfer-baseline-capture`](../github-repo-transfer-baseline-capture/SKILL.md))
is compared against the **old owner** (every repo must be `missing` — gone from
the source account) and against the **destination owner** (every repo must be
`ok` — visibility, default branch, head SHA, archived, fork identical). A `pass`
requires both sides clean; any unexpected verdict fails the verification.

## Composition Rationale

The verification is exactly two cross-owner invocations of
[`github-repo-state-fingerprint`](../../repo/github-repo-state-fingerprint/SKILL.md)
`compare` plus the pass/fail policy — so this skill is a composer that owns the
two-sided criteria and delegates all state capture/comparison to the base. It
re-implements no fingerprint logic.

## Related Skills

- [`github-repo-transfer-baseline-capture`](../github-repo-transfer-baseline-capture/SKILL.md)
  — produces the baseline snapshot consumed here.
- [`github-repo-transfer-completion-poll`](../github-repo-transfer-completion-poll/SKILL.md)
  — establishes that the repos have landed before structural verification.
- [`github-repo-transfer-destination-conflict-check`](../github-repo-transfer-destination-conflict-check/SKILL.md)
  — the pre-transfer gate; verify closes the loop.

## 1. When to Apply

Use this skill after a transfer has landed under the destination owner:

- Prove the old owner no longer serves the repositories (all `missing`).
- Prove the destination owner serves identical state (all `ok`, head SHA
  included).

**Anti-trigger:** Do not use it to check name availability (that is the
destination-conflict-check gate) or to poll for landing (that is the completion
poll).

## 2. Why This Skill (Not Ad-Hoc Checks)

| Option | Verdict | Reason |
| --- | --- | --- |
| Eyeball both accounts in a browser | ❌ | no deterministic record; SHA not compared |
| One fingerprint compare against the destination only | ⚠️ | proves arrival, not departure |
| This skill | ✅ | two-sided criteria + SHA-level equality + machine verdict |

Language tier: **Python 3 (Tier 1)** per
[`scripting-language-selection-rules.md` §2](../../../../../ai-agent-rules/scripting-language-selection-rules.md).

## 3. Required Inputs & Environment

| Requirement | Minimum | Notes |
| --- | --- | --- |
| `gh` CLI | authenticated | `--token-user` selects another account's token |
| Baseline snapshot | `--baseline <path>` | from `github-repo-transfer-baseline-capture` |
| Old owner | `--old-owner <login>` | source account (must be missing) |
| Destination owner | `--destination-owner <login>` | receiving account (must be ok) |
| Python | 3.12+ | pure stdlib; no pip dependencies |

## 4. Operational Logic

### 4.1 Script catalogue

| Script | Role | Exit codes |
| --- | --- | --- |
| `scripts/verify-repo-transfer.py` | two-sided verification driver | `0` pass · `1` fail · `2` config error |

### 4.2 CLI contract

```bash
python3 scripts/verify-repo-transfer.py --baseline <snapshot.json> \
    --old-owner <login> --destination-owner <login> [--token-user <login>]
```

### 4.3 Output contract

One JSON object per stage (old owner, then destination), then the verdict.

```json
{"stage": "old-owner", "summary": {"owner": "<old-owner>", "checked": 6, "counts": {"ok": 0, "drift": 0, "missing": 6, "error": 0}}, "repos": [{"repo": "repo-a", "verdict": "missing", "changes": {}}]}
{"stage": "destination-owner", "summary": {"owner": "<destination-owner>", "checked": 6, "counts": {"ok": 6, "drift": 0, "missing": 0, "error": 0}}, "repos": [{"repo": "repo-a", "verdict": "ok", "changes": {}}]}
{"verdict": "pass", "old_missing": true, "new_ok": true, "checked": 6}
```

### 4.4 End-to-end example

```bash
SCRIPTS=.agents/skills/github/transfer/github-repo-transfer-verify/scripts
python3 "$SCRIPTS"/verify-repo-transfer.py \
    --baseline scratch/<session>/transfer-baseline.json \
    --old-owner <old-owner> --destination-owner <destination-owner>
```

## 5. Composition by Higher-Level Skills

| Composer | Composition Mechanism |
| --- | --- |
| [`github-repo-account-transfer`](../github-repo-account-transfer/SKILL.md) | Stage 6 (final verification) of the orchestrated account-transfer flow. |

## 6. Composition by This Skill

| Base Skill | Composition Mechanism |
| --- | --- |
| [`github-repo-state-fingerprint`](../../repo/github-repo-state-fingerprint/SKILL.md) | `compare` subcommand invoked twice — once with `--owner <old-owner>` (expect all `missing`), once with `--owner <destination-owner>` (expect all `ok`); base summary lines are parsed for the pass/fail policy. |

## 7. Prohibited Behaviors

- Declaring `pass` when either side reports `drift`, `error`, or an unexpected
  count.
- Treating "present under destination" alone as success — departure from the
  old owner is equally mandatory.
- Mutating anything; this skill is strictly read-only.

## 8. Change History

| Timestamp | Summary of Changes | Rationale |
| --- | --- | --- |
| [2026-09-30 16:32] | Initial skill v1 created | The transfer pipeline needed a two-sided structural verification with SHA-level equality |

## 9. Traceability

See [`TRACEABILITY.md`](TRACEABILITY.md) for session logs and provenance.

## 10. Changelog

See [`CHANGELOG.md`](CHANGELOG.md) for release history.
