---
name: github-repo-account-transfer
description: >-
  Orchestrate a full GitHub repository account transfer: gate -> baseline ->
  initiate -> (email acceptance) -> wait -> verify -> cleanup -> repoint.
  Top-level composer dispatching to the seven transfer composite scripts.
category: GitHub
---

# GitHub Repo Account Transfer Skill (v1)

> **Skill ID:** `github-repo-account-transfer`<br>
> **Version:** 1.0.0<br>
> **Standard:** [Agent Skills (agentskills.io)](https://agentskills.io)<br>
> **Layer:** Composer (per [`skill-factory` §2.0 Layering Decision](../../../skill-factory/SKILL.md))

## Description

Orchestrates a complete account-to-account repository transfer as one
dispatcher with one subcommand per stage:

```text
gate -> baseline -> initiate -> (email acceptance, human) -> wait -> verify -> cleanup -> repoint
```

The dispatcher (`run-account-transfer.py`) is a thin passthrough: every
subcommand invokes the corresponding transfer composite script with the flags
it owns, inheriting stdio and returning the child's exit code. The only
non-mechanical stage is the destination account's **email acceptance** between
`initiate` and `wait` (acceptance is email-based; unaccepted invitations expire
after 1 day).

## Composition Rationale

The end-to-end transfer is a fixed sequence of independently-verified stages, so
this skill is a top-level composer: it owns the stage order, the shared
identifier flags, and the human-gate documentation, and delegates every action
to the composites (which in turn compose the bases). It re-implements nothing.

## Related Skills

- [`email-poll-for-message`](../../../email/email-poll-for-message/SKILL.md) —
  optional proactive wait for the acceptance/confirmation email.
- [`gmail-poll-for-message`](../../../email/gmail-poll-for-message/SKILL.md) —
  Gmail preset for the same acceptance wait.

## 1. When to Apply

Use this skill for the whole operation, or to run any single stage with a
consistent interface:

- Plan and execute a batch transfer of repositories between accounts.
- Resume a partially completed transfer at any stage (`wait`, `verify`, …).

**Anti-trigger:** For a single atomic action use the stage's composite directly;
for non-transfer GitHub operations use the relevant base skill.

## 2. Why This Skill (Not Manual Sequencing)

| Option | Verdict | Reason |
| --- | --- | --- |
| Manual stage-by-stage commands | ⚠️ | works, but flag names drift between stages |
| Remembering the pipeline order | ❌ | skipping `gate` or `verify` silently weakens safety |
| This skill | ✅ | one dispatcher, fixed order, uniform flags, passthrough exit codes |

Language tier: **Python 3 (Tier 1)** per
[`scripting-language-selection-rules.md` §2](../../../../../ai-agent-rules/scripting-language-selection-rules.md).

## 3. Required Inputs & Environment

| Requirement | Minimum | Notes |
| --- | --- | --- |
| `gh` CLI | authenticated | both accounts' tokens resolvable |
| Old owner | `--old-owner <login>` | required by baseline/initiate/verify |
| Destination owner | `--destination-owner <login>` | required by gate/initiate/wait/verify |
| Repo set | `--repos` and/or `--repos-file` | forwarded to every stage |
| Python | 3.12+ | pure stdlib; no pip dependencies |

## 4. Operational Logic

### 4.1 Script catalogue

| Script | Role | Exit codes |
| --- | --- | --- |
| `scripts/run-account-transfer.py` | stage dispatcher — passthrough to the seven composite scripts | child's exit code (`0`/`1`/`2`) |

### 4.2 CLI contract

```bash
python3 scripts/run-account-transfer.py <stage> [stage flags]
```

| Stage | Delegates to | Stage-specific flags |
| --- | --- | --- |
| `gate` | destination-conflict-check | `--destination-owner`, `--enumerate` |
| `baseline` | baseline-capture | `--old-owner`, `--output` |
| `initiate` | transfer-initiate | `--old-owner`, `--destination-owner`, `--execute` |
| `wait` | completion-poll | `--destination-owner`, `--interval`, `--attempts` |
| `verify` | transfer-verify | `--baseline`, `--old-owner`, `--destination-owner` |
| `cleanup` | collaborator-remove | `--owner`, `--collaborator`, `--execute` |
| `repoint` | origin-repoint | `--clones-root`, `--new-owner`, `--remote`, `--url-template`, `--execute` |

All stages also accept `--repos` / `--repos-file` / `--token-user`.

### 4.3 Output contract

Stage banners go to stderr; stdout is exactly the delegated script's output
(JSONL), and the exit code is the delegated script's.

### 4.4 End-to-end example

```bash
SCRIPTS=.agents/skills/github/transfer/github-repo-account-transfer/scripts
R="repo-a,repo-b"
python3 "$SCRIPTS"/run-account-transfer.py gate     --destination-owner <dest> --repos "$R"
python3 "$SCRIPTS"/run-account-transfer.py baseline --old-owner <old> --repos "$R" --output baseline.json
python3 "$SCRIPTS"/run-account-transfer.py initiate --old-owner <old> --destination-owner <dest> --repos "$R"
python3 "$SCRIPTS"/run-account-transfer.py initiate --old-owner <old> --destination-owner <dest> --repos "$R" --execute
# (destination account accepts the confirmation email)
python3 "$SCRIPTS"/run-account-transfer.py wait     --destination-owner <dest> --repos "$R"
python3 "$SCRIPTS"/run-account-transfer.py verify   --baseline baseline.json --old-owner <old> --destination-owner <dest>
python3 "$SCRIPTS"/run-account-transfer.py cleanup  --owner <dest> --collaborator <old-login> --repos "$R" --execute
python3 "$SCRIPTS"/run-account-transfer.py repoint  --clones-root ~/clones --new-owner <dest> --repos "$R" --execute
```

## 5. Composition by Higher-Level Skills

None — this is the top-level orchestrator for the transfer pipeline.

## 6. Composition by This Skill

| Composed Skill | Composition Mechanism |
| --- | --- |
| [`github-repo-transfer-destination-conflict-check`](../github-repo-transfer-destination-conflict-check/SKILL.md) | `gate` stage — passthrough to its gate script. |
| [`github-repo-transfer-baseline-capture`](../github-repo-transfer-baseline-capture/SKILL.md) | `baseline` stage — passthrough to its capture script. |
| [`github-repo-transfer-initiate`](../github-repo-transfer-initiate/SKILL.md) | `initiate` stage — passthrough to its initiation script. |
| [`github-repo-transfer-completion-poll`](../github-repo-transfer-completion-poll/SKILL.md) | `wait` stage — passthrough to its completion poller. |
| [`github-repo-transfer-verify`](../github-repo-transfer-verify/SKILL.md) | `verify` stage — passthrough to its verification script. |
| [`github-repo-collaborator-remove`](../../repo/github-repo-collaborator-remove/SKILL.md) | `cleanup` stage — passthrough to its removal script. |
| [`git-remote-origin-repoint`](../../../git/repo/git-remote-origin-repoint/SKILL.md) | `repoint` stage — passthrough to its repoint script. |

## 7. Prohibited Behaviors

- Reordering the pipeline (e.g. `initiate` before `gate`, `cleanup` before
  `verify`).
- Forwarding `--execute` to a stage that was not reviewed in dry-run first.
- Automating or bypassing the email-acceptance human gate.

## 8. Change History

| Timestamp | Summary of Changes | Rationale |
| --- | --- | --- |
| [2026-09-30 16:42] | Initial skill v1 created | The suite needed one dispatcher owning the fixed 8-stage transfer order |

## 9. Traceability

See [`TRACEABILITY.md`](TRACEABILITY.md) for session logs and provenance.

## 10. Changelog

See [`CHANGELOG.md`](CHANGELOG.md) for release history.
