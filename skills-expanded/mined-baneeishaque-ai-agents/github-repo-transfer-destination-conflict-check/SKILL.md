---
name: github-repo-transfer-destination-conflict-check
description: >-
  Pre-transfer gate: check the destination owner for name conflicts across the
  transfer repo list using github-repo-name-conflict-check, and emit a
  pass/block gate verdict. Read-only.
category: GitHub
---

# GitHub Repo Transfer Destination Conflict Check Skill (v1)

> **Skill ID:** `github-repo-transfer-destination-conflict-check`<br>
> **Version:** 1.0.0<br>
> **Standard:** [Agent Skills (agentskills.io)](https://agentskills.io)<br>
> **Layer:** Composer (per [`skill-factory` §2.0 Layering Decision](../../../skill-factory/SKILL.md))

## Description

A pre-transfer gate over
[`github-repo-name-conflict-check`](../../repo/github-repo-name-conflict-check/SKILL.md):
checks every repository in the transfer set for name conflicts under the
**destination** owner (the destination receives the same repo names) and emits
a single gate verdict — `pass` only when every name is `AVAILABLE`.

## Composition Rationale

Transfer initiation must be gated on destination-name availability, but the
underlying check is already owned by the name-conflict base. This skill frames
that check in transfer terms (destination owner, transfer repo list) and adds
the gate verdict that initiation workflows consume — without duplicating any
lookup logic.

## Related Skills

- [`github-repo-transfer-baseline-capture`](../github-repo-transfer-baseline-capture/SKILL.md)
  — the next pipeline stage (pre-transfer state snapshot).
- [`github-repo-transfer-completion-poll`](../github-repo-transfer-completion-poll/SKILL.md)
  — the post-initiation landing wait (same pipeline).
- [`github-repo-transfer-verify`](../github-repo-transfer-verify/SKILL.md) —
  the post-transfer verification stage.

## 1. When to Apply

Use this skill before initiating a repository transfer:

- Gate the initiation stage on destination-name availability (no `TAKEN` and no
  `UNKNOWN` names).
- Produce the conflict-check evidence for a transfer run report.

**Anti-trigger:** For non-transfer name checks (e.g., new repo creation), use
[`github-repo-name-conflict-check`](../../repo/github-repo-name-conflict-check/SKILL.md)
directly.

## 2. Why a Dedicated Gate (Not a Bare Check)

| Option | Verdict | Reason |
| --- | --- | --- |
| Manual per-repo web checks | ❌ | not automatable; no gate record |
| Bare name-conflict check per caller | ⚠️ | verdicts exist, but each caller re-derives "is this blocking?" |
| This gate composite | ✅ | one `pass` / `block` verdict + blocking list; initiation consumes it verbatim |

Language tier: **Python 3 (Tier 1)** per
[`scripting-language-selection-rules.md` §2](../../../../../ai-agent-rules/scripting-language-selection-rules.md).

## 3. Required Inputs & Environment

| Requirement | Minimum | Notes |
| --- | --- | --- |
| `gh` CLI | authenticated for the destination account | `--token-user` selects another account's token |
| Destination owner | `--destination-owner <login>` | the account receiving the repos |
| Transfer repo set | `--repos` and/or `--repos-file` | candidate names to verify as free |
| Python | 3.12+ | pure stdlib; no pip dependencies |

## 4. Operational Logic

### 4.1 Script catalogue

| Script | Role | Exit codes |
| --- | --- | --- |
| `scripts/check-destination-conflicts.py` | gate driver — shells the name-conflict base, streams verdicts, emits the gate summary | `0` pass · `1` block · `2` config error |

### 4.2 CLI contract

```bash
python3 scripts/check-destination-conflicts.py --destination-owner <login> \
    --repos a,b [--token-user <login>] [--enumerate]
```

| Option | Default | Purpose |
| --- | --- | --- |
| `--destination-owner <login>` | required | account receiving the transfers |
| `--repos <csv>` / `--repos-file <path>` | — | transfer repo set |
| `--token-user <login>` | ambient auth | destination account's token |
| `--enumerate` | off | passthrough: also report the destination's repo count |

### 4.3 Output contract

The base check's per-name JSONL streams through unchanged, then the gate
summary. Exit `0` = pass, `1` = block.

```json
{"gate": "block", "destination_owner": "<destination-owner>", "blocking": ["repo-b"]}
```

### 4.4 End-to-end example

```bash
SCRIPTS=.agents/skills/github/transfer/github-repo-transfer-destination-conflict-check/scripts
python3 "$SCRIPTS"/check-destination-conflicts.py --destination-owner <destination-owner> \
    --repos repo-a,repo-b --token-user <destination-login> --enumerate
```

## 5. Composition by Higher-Level Skills

| Composer | Composition Mechanism |
| --- | --- |
| [`github-repo-transfer-initiate`](../github-repo-transfer-initiate/SKILL.md) | Consumes the gate verdict as its precondition — initiation must not run when the gate is `block`. |
| [`github-repo-account-transfer`](../github-repo-account-transfer/SKILL.md) | Stage 1 of the orchestrated account-transfer flow; its summary is folded into the run report. |

## 6. Composition by This Skill

| Base | Invoked As | Supplied | Consumed Back |
| --- | --- | --- | --- |
| [`github-repo-name-conflict-check`](../../repo/github-repo-name-conflict-check/SKILL.md) | `check-name-conflicts.py --owner <destination> --repos …` | destination owner + transfer repo list + token user | per-name verdicts (streamed through) + exit code mapped to `pass`/`block` |

## 7. Prohibited Behaviors

- Initiating transfers when the gate is `block` — the gate is a hard
  precondition, not advice.
- Re-implementing lookups — shell out to the name-conflict base (§6).
- Treating `UNKNOWN` names as passable — unknown blocks, like taken.

## 8. Change History

| Timestamp | Summary of Changes | Rationale |
| --- | --- | --- |
| [2026-09-30 16:15] | Initial skill v1 created | The transfer pipeline needed a single destination-availability gate over the name-conflict base |

## 9. Traceability

See [`TRACEABILITY.md`](TRACEABILITY.md) for session logs and provenance.

## 10. Changelog

See [`CHANGELOG.md`](CHANGELOG.md) for release history.
