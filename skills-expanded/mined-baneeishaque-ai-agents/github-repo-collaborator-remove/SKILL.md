---
name: github-repo-collaborator-remove
description: >-
  Remove a collaborator from one or more GitHub repositories via
  DELETE /repos/<owner>/<repo>/collaborators/<user> (HTTP 204), with
  dry-run-by-default safety and per-repo records. Mutating only with --execute.
category: GitHub
---

# GitHub Repo Collaborator Remove Skill (v1)

> **Skill ID:** `github-repo-collaborator-remove`<br>
> **Version:** 1.0.0<br>
> **Standard:** [Agent Skills (agentskills.io)](https://agentskills.io)<br>
> **Layer:** Base (per [`skill-factory` §2.0 Layering Decision](../../../skill-factory/SKILL.md))

## Description

Removes a collaborator from one or more repositories with
`DELETE /repos/<owner>/<repo>/collaborators/<user>` (HTTP 204). Typical use:
revoking a personal account's access after a repository set has been transferred
to it and the interim collaborator grant is no longer needed. **Dry-run by
default**; nothing is deleted without `--execute`.

## Composition Rationale

Collaborator removal is one atomic API action per repository, so this skill is a
base: it owns the endpoint shape, the 204 contract, the dry-run safety, and the
per-repo machine record. The account-transfer composer consumes it as the
post-transfer cleanup stage.

## Related Skills

- [`github-repo-transfer-verify`](../../transfer/github-repo-transfer-verify/SKILL.md)
  — confirm the transferred repos are intact before revoking interim access.
- [`github-repo-state-fingerprint`](../github-repo-state-fingerprint/SKILL.md)
  — snapshot repo state around access-changing operations.

## 1. When to Apply

Use this skill when an interim collaborator grant must be revoked:

- After a transfer run, remove the previous owner's user from the destination
  repos if a collaborator grant was added during cutover.
- Any batch revoke of one user across a repo set.

**Anti-trigger:** Do not use it for org/team membership changes or for removing
the repository owner.

## 2. Why This Skill (Not the Web UI)

| Option | Verdict | Reason |
| --- | --- | --- |
| Web-UI removal per repo | ❌ | not automatable; no record |
| Raw `gh api` DELETE per caller | ⚠️ | works, but each caller re-derives the endpoint and 204 semantics |
| This skill | ✅ | one contract + dry-run default + per-repo records |

Protocol facts (observed live): `DELETE …/collaborators/<user>` returns **204 No
Content** on success; re-deleting an absent collaborator returns 404.

Language tier: **Python 3 (Tier 1)** per
[`scripting-language-selection-rules.md` §2](../../../../../ai-agent-rules/scripting-language-selection-rules.md).

## 3. Required Inputs & Environment

| Requirement | Minimum | Notes |
| --- | --- | --- |
| `gh` CLI | authenticated for the repo owner | `--token-user` selects another account's token |
| Owner | `--owner <login>` | repos' owner |
| Repo set | `--repos` and/or `--repos-file` | repositories to clean |
| Collaborator | `--collaborator <login>` | user to remove |
| Python | 3.12+ | pure stdlib; no pip dependencies |

## 4. Operational Logic

### 4.1 Script catalogue

| Script | Role | Exit codes |
| --- | --- | --- |
| `scripts/remove-repo-collaborators.py` | removal driver — dry-run plan or live DELETE per repo | `0` all removed/planned · `1` any failure · `2` config error |

### 4.2 CLI contract

```bash
python3 scripts/remove-repo-collaborators.py --owner <login> \
    --collaborator <login> --repos a,b [--token-user <login>] [--execute]
```

| Option | Default | Purpose |
| --- | --- | --- |
| `--owner <login>` | required | repos' owner |
| `--collaborator <login>` | required | user to remove |
| `--repos <csv>` / `--repos-file <path>` | — | repo set |
| `--token-user <login>` | ambient auth | owner's token |
| `--execute` | off (dry-run) | actually send the DELETE requests |

### 4.3 Output contract

```json
{"repo": "example-repo", "dry_run": true, "method": "DELETE", "endpoint": "repos/<owner>/example-repo/collaborators/<login>"}
{"repo": "example-repo", "http_status": 204, "removed": true}
```

### 4.4 End-to-end example

```bash
SCRIPTS=.agents/skills/github/repo/github-repo-collaborator-remove/scripts
python3 "$SCRIPTS"/remove-repo-collaborators.py --owner <owner> \
    --collaborator <login> --repos repo-a,repo-b
python3 "$SCRIPTS"/remove-repo-collaborators.py --owner <owner> \
    --collaborator <login> --repos repo-a,repo-b --token-user <owner> --execute
```

## 5. Composition by Higher-Level Skills

| Composer | Composition Mechanism |
| --- | --- |
| [`github-repo-account-transfer`](../../transfer/github-repo-account-transfer/SKILL.md) | Stage 7 (post-transfer cleanup) of the orchestrated account-transfer flow. |

## 6. Composition by This Skill

None — this is a base skill; it drives `gh api` directly and composes no other
skill scripts.

## 7. Prohibited Behaviors

- Executing without `--execute` — the default must remain dry-run.
- Removing the repository owner or org-managed access via this path.
- Assuming 404 means success on re-run — treat unexpected statuses as failures.

## 8. Change History

| Timestamp | Summary of Changes | Rationale |
| --- | --- | --- |
| [2026-09-30 16:35] | Initial skill v1 created | The transfer pipeline needed the post-transfer access-revocation action with dry-run safety |

## 9. Traceability

See [`TRACEABILITY.md`](TRACEABILITY.md) for session logs and provenance.

## 10. Changelog

See [`CHANGELOG.md`](CHANGELOG.md) for release history.
