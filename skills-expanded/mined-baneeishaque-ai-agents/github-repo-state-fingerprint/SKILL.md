---
name: github-repo-state-fingerprint
description: >-
  Capture and compare curated GitHub repository state fingerprints (visibility,
  default branch, head SHA, archived, fork) per repository; volatile metrics are
  recorded but ignored by default. Supports cross-owner comparison for
  verifying repository transfers. Read-only.
category: GitHub
---

# GitHub Repo State Fingerprint Skill (v1)

> **Skill ID:** `github-repo-state-fingerprint`<br>
> **Version:** 1.0.0<br>
> **Standard:** [Agent Skills (agentskills.io)](https://agentskills.io)<br>
> **Layer:** Base (per [`skill-factory` §2.0 Layering Decision](../../../skill-factory/SKILL.md))

## Description

Captures a **curated state fingerprint** per GitHub repository and compares
fingerprints field-by-field. Identity/structure fields (`visibility`,
`default_branch`, `head_sha`, `archived`, `fork`) are compared by default;
volatile metrics (`size`, `stargazers_count`, `forks_count`,
`open_issues_count`, `watchers_count`) are recorded but ignored unless
`--strict`. `full_name` is never compared (it differs trivially across owners),
which enables cross-owner comparison such as verifying a repository transfer.

## Composition Rationale

This skill is a base primitive: before any state-changing repo operation, the
question "is the repo still in the same state?" needs one deterministic
snapshot format and one deterministic comparison verdict. Extraction keeps the
curated compare-key set (volatile counters excluded) and the
`ok` / `drift` / `missing` / `error` verdict contract in one script. Known
composers:

- [`github-repo-transfer-baseline-capture`](../../transfer/github-repo-transfer-baseline-capture/SKILL.md)
  — wraps `capture` with the transfer repo set to snapshot pre-transfer state
  under the old owner.
- [`github-repo-transfer-verify`](../../transfer/github-repo-transfer-verify/SKILL.md)
  — wraps `compare` twice: baseline vs old owner (expect all `missing`) and
  baseline vs new owner (expect all `ok`).

## Related Skills

- [`git-worktree-state-fingerprint`](../../../git/basic/audit/git-worktree-state-fingerprint/SKILL.md)
  — the conceptual sibling for local Git worktrees (pre/post history-rewrite
  fingerprints).
- [`github-repo-name-conflict-check`](../github-repo-name-conflict-check/SKILL.md)
  — sibling Batch-1 engine for pre-change name-availability verdicts.
- [`github-repo-commit-fetch`](../../../github-repo-commit-fetch/SKILL.md) —
  fetch primitive for deeper per-commit inspection when a fingerprint drifts.

## 1. When to Apply

Use this skill whenever repository state must be **snapshotted before** and
**proven unchanged after** an operation:

- Baseline capture before a transfer, rename, or settings change.
- Post-operation verification that `head_sha`, `visibility`, and structure
  fields are preserved (cross-owner capable).
- Drift detection on a set of repositories between two points in time.

**Anti-trigger:** If you need the full commit history or file contents, use a
fetch primitive instead — this skill stores only a compact curated fingerprint.

## 2. Why a Curated Fingerprint (Not a Raw API Dump Diff)

| Option | Verdict | Reason |
| --- | --- | --- |
| Line-diff two raw API JSON dumps | ❌ | volatile counters (stars/forks/size) and timestamps produce constant noise; no verdict contract |
| Manual comparison in the GitHub web UI | ❌ | not automatable; error-prone across many repos |
| Fingerprint with curated compare keys + verdicts | ✅ | deterministic `ok` / `drift` / `missing` / `error` per repo; cross-owner capable |

Language tier: **Python 3 (Tier 1)** per
[`scripting-language-selection-rules.md` §2](../../../../../ai-agent-rules/scripting-language-selection-rules.md).

## 3. Required Inputs & Environment

| Requirement | Minimum | Notes |
| --- | --- | --- |
| `gh` CLI | authenticated for the owner account | `gh auth status` must show the owner login |
| Owner token | `--token-user <login>` when ambient auth is not the owner | resolved via `gh auth token --user <login>` |
| Repo names | `--repos` and/or `--repos-file` (capture) | baseline file keys are the names for `compare` |
| Python | 3.12+ | pure stdlib; no pip dependencies |

## 4. Operational Logic

### 4.1 CLI contract

```bash
python3 scripts/repo-state-fingerprint.py capture --owner <login> --repos a,b --output baseline.json
python3 scripts/repo-state-fingerprint.py compare --baseline baseline.json [--owner <other-owner>] [--current snapshot.json] [--strict]
```

| Option | Mode | Default | Purpose |
| --- | --- | --- | --- |
| `--owner <login>` | both | capture: required; compare: baseline owner | account to capture/compare under |
| `--repos <csv>` / `--repos-file <path>` | capture | — | repositories to fingerprint |
| `--output <path>` | capture | required | snapshot file to write |
| `--baseline <path>` | compare | required | snapshot to compare against |
| `--current <path>` | compare | live re-capture | compare against a stored snapshot instead of live state |
| `--token-user <login>` | both | ambient auth | run API calls with this account's token |
| `--strict` | compare | off | also compare volatile metrics |

### 4.2 Output contract

Capture writes a snapshot file and emits per-repo JSONL + a summary on stdout.
Compare emits one verdict per repo + a summary. Exit `0` = clean, `1` =
missing/error (capture) or drift/missing/error (compare), `2` = usage error.

```json
{"repo": "example-repo", "full_name": "<owner>/example-repo", "visibility": "public", "default_branch": "main", "head_sha": "abc123", "archived": false, "fork": false, "size": 42, "stargazers_count": 1, "forks_count": 0, "open_issues_count": 0, "watchers_count": 1, "captured_at": "2026-09-30T10:00:00+00:00", "status": "captured"}
{"repo": "example-repo", "verdict": "ok", "changes": {}}
```

### 4.3 End-to-end example: baseline then cross-owner verify

```bash
SCRIPTS=.agents/skills/github/repo/github-repo-state-fingerprint/scripts
python3 "$SCRIPTS"/repo-state-fingerprint.py capture --owner <old-owner> \
    --repos repo-a,repo-b --output baseline.json --token-user <old-login>
python3 "$SCRIPTS"/repo-state-fingerprint.py compare --baseline baseline.json \
    --owner <new-owner> --token-user <new-login>
```

## 5. Composition by Higher-Level Skills

| Composer | Composition Mechanism |
| --- | --- |
| [`github-repo-transfer-baseline-capture`](../../transfer/github-repo-transfer-baseline-capture/SKILL.md) | Shells out to `capture` with the transfer repo set and writes the transfer-scoped baseline file; records the snapshot path for later verification stages. |
| [`github-repo-transfer-verify`](../../transfer/github-repo-transfer-verify/SKILL.md) | Shells out to `compare` for the old owner (expect all `missing`) and for the new owner (expect all `ok`); folds both verdict streams into the transfer verification report. |

## 6. Prohibited Behaviors

- Mutating anything — capture/compare are strictly read-only.
- Comparing volatile metrics as drift by default — stars/forks/size legitimately
  move; require `--strict` for that.
- Treating `missing` or `error` as success in verification contexts.
- Reimplementing snapshot or comparison logic in composers — shell out to
  `repo-state-fingerprint.py`.

## 7. Change History

| Timestamp | Summary of Changes | Rationale |
| --- | --- | --- |
| [2026-09-30 15:40] | Initial skill v1 created | Extraction of the curated repo-state fingerprint used to prove SHA/structure preservation across the repo-transfer operation |

## 8. Traceability

See [`TRACEABILITY.md`](TRACEABILITY.md) for session logs and provenance.

## 9. Changelog

See [`CHANGELOG.md`](CHANGELOG.md) for release history.
