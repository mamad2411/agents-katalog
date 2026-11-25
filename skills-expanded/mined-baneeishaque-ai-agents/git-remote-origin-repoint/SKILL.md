---
name: git-remote-origin-repoint
description: >-
  Repoint local clone origin remotes to new URLs (e.g. after a GitHub
  transfer) via git remote set-url plus git ls-remote verification, with
  dry-run-by-default safety and per-repo records.
category: Git
---

# Git Remote Origin Repoint Skill (v1)

> **Skill ID:** `git-remote-origin-repoint`<br>
> **Version:** 1.0.0<br>
> **Standard:** [Agent Skills (agentskills.io)](https://agentskills.io)<br>
> **Layer:** Base (per [`skill-factory` §2.0 Layering Decision](../../../skill-factory/SKILL.md))

## Description

Repoints each local clone's remote (default `origin`) to the post-transfer URL
and proves it works with `git ls-remote`. Typical use: after repositories move
to a new owner, local clones still point at the old URLs — GitHub serves
301 redirects for a while, but local remotes should be repointed promptly.
**Dry-run by default**; nothing is changed without `--execute`.

## Composition Rationale

Repointing is a per-clone `git remote set-url` plus an `ls-remote` verification,
so this skill is a base: it owns the batch loop, the URL template, the dry-run
safety, and the machine record. The account-transfer composer consumes it as the
local-clone repoint stage.

## Related Skills

- [`github-repo-transfer-verify`](../../../github/transfer/github-repo-transfer-verify/SKILL.md)
  — confirm the server-side transfer before repointing local clones.
- [`git-worktree-state-fingerprint`](../../../git/basic/audit/git-worktree-state-fingerprint/SKILL.md)
  — fingerprint working-tree state around history-adjacent git operations.

## 1. When to Apply

Use this skill when local clones must follow a repository to its new owner:

- After a completed transfer, repoint each local clone's `origin`.
- Any batch remote-URL migration across a clone root.

**Anti-trigger:** Do not use it to rewrite history or to add/remove remotes —
it only changes the URL of one existing remote per clone.

## 2. Why This Skill (Not Manual `set-url`)

| Option | Verdict | Reason |
| --- | --- | --- |
| Manual `git remote set-url` per clone | ❌ | not batchable; no verification record |
| `set-url` without verification | ⚠️ | a typo silently breaks the clone |
| This skill | ✅ | template-driven batch + `ls-remote` proof + dry-run default |

Language tier: **Python 3 (Tier 1)** per
[`scripting-language-selection-rules.md` §2](../../../../../ai-agent-rules/scripting-language-selection-rules.md).

## 3. Required Inputs & Environment

| Requirement | Minimum | Notes |
| --- | --- | --- |
| `git` CLI | any modern version | network or local-path remote for `ls-remote` |
| Clone root | `--clones-root <dir>` | directory containing `<repo>` clones |
| New owner | `--new-owner <login>` | feeds the default URL template |
| Repo set | `--repos` and/or `--repos-file` | clone directory names |
| Python | 3.12+ | pure stdlib; no pip dependencies |

Credentials are not handled by this skill — `ls-remote` uses the ambient git
credential helper (or a local-path remote in tests).

## 4. Operational Logic

### 4.1 Script catalogue

| Script | Role | Exit codes |
| --- | --- | --- |
| `scripts/repoint-origin-remotes.py` | batch repoint driver — dry-run plan or live set-url + ls-remote per clone | `0` all verified/planned · `1` any failure · `2` config error |

### 4.2 CLI contract

```bash
python3 scripts/repoint-origin-remotes.py --clones-root <dir> \
    --new-owner <login> --repos a,b [--remote origin] \
    [--url-template 'https://github.com/{owner}/{repo}.git'] [--execute]
```

| Option | Default | Purpose |
| --- | --- | --- |
| `--clones-root <dir>` | required | directory containing the clones |
| `--new-owner <login>` | required | fills `{owner}` in the template |
| `--repos <csv>` / `--repos-file <path>` | — | clone directory names |
| `--remote <name>` | `origin` | remote to repoint |
| `--url-template <str>` | `https://github.com/{owner}/{repo}.git` | `{owner}`/`{repo}` placeholders |
| `--execute` | off (dry-run) | actually run `set-url` |

### 4.3 Output contract

```json
{"repo": "example-repo", "path": "<clones-root>/example-repo", "remote": "origin", "old_url": "https://github.com/<old-owner>/example-repo.git", "new_url": "https://github.com/<new-owner>/example-repo.git", "dry_run": true}
{"repo": "example-repo", "path": "<clones-root>/example-repo", "remote": "origin", "old_url": "…", "new_url": "…", "head_sha": "7fd1a60…", "verified": true}
```

### 4.4 End-to-end example

```bash
SCRIPTS=.agents/skills/git/repo/git-remote-origin-repoint/scripts
python3 "$SCRIPTS"/repoint-origin-remotes.py --clones-root ~/clones \
    --new-owner <new-owner> --repos repo-a,repo-b
python3 "$SCRIPTS"/repoint-origin-remotes.py --clones-root ~/clones \
    --new-owner <new-owner> --repos repo-a,repo-b --execute
```

## 5. Composition by Higher-Level Skills

| Composer | Composition Mechanism |
| --- | --- |
| [`github-repo-account-transfer`](../../../github/transfer/github-repo-account-transfer/SKILL.md) | Stage 8 (local clone repoint) of the orchestrated account-transfer flow. |

## 6. Composition by This Skill

None — this is a base skill; it drives `git` directly and composes no other
skill scripts.

## 7. Prohibited Behaviors

- Executing without `--execute` — the default must remain dry-run.
- Repointing clones before the server-side transfer is verified.
- Repointing when `ls-remote` cannot be verified without flagging the clone as
  failed.

## 8. Change History

| Timestamp | Summary of Changes | Rationale |
| --- | --- | --- |
| [2026-09-30 16:38] | Initial skill v1 created | The transfer pipeline needed the local-clone repoint action with verification |

## 9. Traceability

See [`TRACEABILITY.md`](TRACEABILITY.md) for session logs and provenance.

## 10. Changelog

See [`CHANGELOG.md`](CHANGELOG.md) for release history.
