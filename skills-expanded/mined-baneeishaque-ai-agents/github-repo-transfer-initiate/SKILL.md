---
name: github-repo-transfer-initiate
description: >-
  Initiate GitHub repository transfers via POST /repos/<old>/<repo>/transfer
  (HTTP 202) with dry-run-by-default safety; documents the email-based
  acceptance step and the 1-day invitation expiry. Mutating only with
  --execute.
category: GitHub
---

# GitHub Repo Transfer Initiate Skill (v1)

> **Skill ID:** `github-repo-transfer-initiate`<br>
> **Version:** 1.0.0<br>
> **Standard:** [Agent Skills (agentskills.io)](https://agentskills.io)<br>
> **Layer:** Base (per [`skill-factory` §2.0 Layering Decision](../../../skill-factory/SKILL.md))

## Description

Initiates repository transfers with
`POST /repos/<old-owner>/<repo>/transfer` and `new_owner=<destination-owner>`
(HTTP 202 Accepted). The transfer only completes after the destination account
**accepts the confirmation email** — acceptance is email-based (the
collaborator-invitation API path is not applicable to transfers), and an
unaccepted invitation expires after 1 day. The script is **dry-run by default**;
nothing is sent without `--execute`.

## Composition Rationale

Transfer initiation is one atomic API action per repository, so this skill is a
base: it owns the request shape, the 202 contract, the dry-run safety, and the
acceptance-step documentation. Higher-level flows (the account-transfer
composer) consume it as a stage and pair it with the email wait for acceptance.

## Related Skills

- [`email-poll-for-message`](../../../email/email-poll-for-message/SKILL.md) —
  waits for the acceptance/confirmation email that the destination user must
  act on.
- [`github-api-poll-until`](../../github-api-poll-until/SKILL.md) — waits for
  the asynchronous landing under the destination owner after acceptance.

## 1. When to Apply

Use this skill to initiate transfers after the destination-availability gate
([`github-repo-transfer-destination-conflict-check`](../github-repo-transfer-destination-conflict-check/SKILL.md))
has passed:

- Plan the initiation calls (dry-run) for a transfer run.
- Execute the initiation calls (`--execute`) for the transfer set.

**Anti-trigger:** Do not use this skill to create repositories or to move
content between repos; it only initiates ownership transfers.

## 2. Why This Skill (Not Manual Web-UI Transfers)

| Option | Verdict | Reason |
| --- | --- | --- |
| Web-UI transfer per repo | ❌ | not automatable; no machine-readable record |
| Raw `gh api` calls per caller | ⚠️ | works, but each caller re-derives the endpoint, 202 semantics, and dry-run safety |
| This skill | ✅ | one request contract + dry-run default + acceptance-step documentation |

Protocol facts (observed live): the endpoint returns **202** with the repo
object; no invitation object is created for transfers (the
`/user/repository_invitations` endpoint covers collaborator invitations only);
the acceptance email expires after 1 day.

Language tier: **Python 3 (Tier 1)** per
[`scripting-language-selection-rules.md` §2](../../../../../ai-agent-rules/scripting-language-selection-rules.md).

## 3. Required Inputs & Environment

| Requirement | Minimum | Notes |
| --- | --- | --- |
| `gh` CLI | authenticated for the old owner | `--token-user` selects another account's token |
| Old owner | `--old-owner <login>` | current owner of the repos |
| Destination owner | `--destination-owner <login>` | account receiving the repos |
| Transfer repo set | `--repos` and/or `--repos-file` | repositories to transfer |
| Python | 3.12+ | pure stdlib; no pip dependencies |

## 4. Operational Logic

### 4.1 Script catalogue

| Script | Role | Exit codes |
| --- | --- | --- |
| `scripts/initiate-repo-transfers.py` | initiation driver — dry-run plan or live POST per repo | `0` all accepted/planned · `1` any failure · `2` config error |

### 4.2 CLI contract

```bash
python3 scripts/initiate-repo-transfers.py --old-owner <login> \
    --destination-owner <login> --repos a,b [--token-user <login>] [--execute]
```

| Option | Default | Purpose |
| --- | --- | --- |
| `--old-owner <login>` | required | current owner |
| `--destination-owner <login>` | required | receiving account |
| `--repos <csv>` / `--repos-file <path>` | — | transfer repo set |
| `--token-user <login>` | ambient auth | old owner's token |
| `--execute` | off (dry-run) | actually send the POST requests |

### 4.3 Output contract

One JSON object per repo, then (live runs) an acceptance note. Exit `0` = all
accepted (live) or all planned (dry-run).

```json
{"repo": "example-repo", "dry_run": true, "method": "POST", "endpoint": "repos/<old-owner>/example-repo/transfer", "new_owner": "<destination-owner>"}
{"repo": "example-repo", "http_status": 202, "accepted": true}
{"note": "acceptance is email-based — the destination user must accept the confirmation email; unaccepted invitations expire after 1 day"}
```

### 4.4 End-to-end example

```bash
SCRIPTS=.agents/skills/github/transfer/github-repo-transfer-initiate/scripts
# 1) Plan (safe):
python3 "$SCRIPTS"/initiate-repo-transfers.py --old-owner <old-owner> \
    --destination-owner <destination-owner> --repos repo-a,repo-b
# 2) Execute after review:
python3 "$SCRIPTS"/initiate-repo-transfers.py --old-owner <old-owner> \
    --destination-owner <destination-owner> --repos repo-a,repo-b \
    --token-user <old-login> --execute
```

## 5. Composition by Higher-Level Skills

| Composer | Composition Mechanism |
| --- | --- |
| [`github-repo-account-transfer`](../github-repo-account-transfer/SKILL.md) | Stage 3 of the orchestrated account-transfer flow; its per-repo 202 results gate the acceptance wait. |

## 6. Composition by This Skill

None — this is a base skill; it drives `gh api` directly and composes no other
skill scripts.

## 7. Prohibited Behaviors

- Executing without `--execute` — the default must remain dry-run.
- Initiating when the destination gate is `block`.
- Blindly re-initiating a repo that already has a pending transfer — check
  state first (completion poll or `gh api` lookup).
- Treating 202 as completion — completion requires the destination user's
  email acceptance plus asynchronous landing.

## 8. Change History

| Timestamp | Summary of Changes | Rationale |
| --- | --- | --- |
| [2026-09-30 16:30] | Initial skill v1 created | The transfer pipeline needed the atomic initiation action with dry-run safety and the email-acceptance contract documented |

## 9. Traceability

See [`TRACEABILITY.md`](TRACEABILITY.md) for session logs and provenance.

## 10. Changelog

See [`CHANGELOG.md`](CHANGELOG.md) for release history.
