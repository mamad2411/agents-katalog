---
name: git-submodule-misconfiguration-audit-and-revert
description: Orchestrates end-to-end remediation of an incorrectly configured submodule URL in .gitmodules.
category: Git-Operations
---

# Git Submodule Misconfiguration Audit & Revert Skill (v1)

> **Skill ID:** `git-submodule-misconfiguration-audit-and-revert`<br>
> **Version:** 1.0.0<br>
> **Standard:** [Agent Skills (agentskills.io)](https://agentskills.io)

## Description

A composer that orchestrates the end-to-end remediation of an incorrectly-configured submodule URL in `.gitmodules`:

1. Detect that the submodule is in a suspicious state (detached HEAD, behind `origin/<default>`).
2. Audit the URL — `.gitmodules` declaration vs the live submodule's `origin` (they should match, but may diverge after a `submodule sync` was skipped).
3. Attribute the change: which superproject commit edited `.gitmodules` for this submodule? Read both the diff direction (`-`/`+`) AND the commit message verbs to catch reversed-direction messages.
4. If the change is single-purpose, drop the commit (rebase `--onto <C^> <C>`); else extract the offending hunk into its own revert commit (out of scope for v1).
5. `git submodule sync <path>` to push the corrected URL into the submodule's local `.git/config`.
6. Hand off to `git-dependent-branch-restack-cascade` for branches rooted on the now-rewritten history — with explicit §4.7 callout when any dependent's parent was a mid-history commit (not just the old tip).

## Composition Rationale

Composer per `skill-factory/SKILL.md` §2.0. Reuses, never reimplements:

| Composed Skill | Used for |
|---|---|
| [`git-submodule-selective-init-no-lfs`](../git-submodule-selective-init-no-lfs/SKILL.md) | Prerequisite — materialize the submodule for auditing without paying the LFS bandwidth cost (audit reads `.gitmodules` + `git log`; LFS bytes are irrelevant) |
| [`git-divergence-audit`](../git-divergence-audit/SKILL.md) | Phase 1 — detached HEAD + behind-origin detection |
| [`git-commit-details-audit`](../git-commit-details-audit/SKILL.md) | Phase 3 — find URL-changing commit; reversed-direction message trap |
| [`git-commit-edit`](../git-commit-edit/SKILL.md) | Phase 4 — drop / split the offending commit |
| [`git-submodule-fork-reconfigure`](../git-submodule-fork-reconfigure/SKILL.md) §3 | Phase 5 — `git submodule sync` mechanics |
| [`git-dependent-branch-restack-cascade`](../git-dependent-branch-restack-cascade/SKILL.md) (esp. §4.7) | Phase 6 — propagate the corrected superproject history |

## Related Skills

- [`git-submodule-dead-upstream-audit`](../git-submodule-dead-upstream-audit/SKILL.md) — diagnoses a different failure (dead URL or force-rewritten upstream); this skill assumes the configured URL is *wrong*, not *dead*.

## Source Rules

| Rule File | Scope Incorporated |
| --- | --- |
| [`ai-rule-standardization-rules.md`](../../../ai-agent-rules/ai-rule-standardization-rules.md) | Skill-First, Layered Composition, SSOT |
| [`scripting-language-selection-rules.md`](../../../ai-agent-rules/scripting-language-selection-rules.md) §2 | Tier-1 Python for the audit script |

***

## 1. When to Apply

ALL must hold:

- A specific submodule is suspected of having the wrong remote URL.
- The wrong URL was introduced by a discoverable superproject commit (typically a `.gitmodules` edit).
- The user wants the change reverted in-place, not formalized as a fork swap.

Do NOT apply when:

- The URL change was intentional and you want to *keep* the new URL → use `git-submodule-fork-reconfigure`.
- The upstream URL is dead / 404 / repo deleted → use `git-submodule-dead-upstream-audit`.
- The submodule's upstream was force-rewritten (URL valid, pinned SHA orphaned) → use `git-submodule-dead-upstream-audit` "force-rewrite detection" section.

***

## 2. Prerequisites

| Requirement | Minimum |
|---|---|
| Git | 2.23+ |
| Python | 3.12+ |
| Submodule | Already initialized (use `git-submodule-selective-init-no-lfs` if not; audit needs the submodule's `.git/config` populated but never reads LFS-backed files) |
| Working tree | Clean (`git status --short` empty) |
| Auth | Push permission on the superproject's branches |


***

## 3. Step-by-Step Procedure

### Phase 0 — State Capture

```bash
git -C <repo> status --short          # MUST be empty
git -C <repo> rev-parse HEAD          # superproject tip
git -C <repo> -C <submodule> rev-parse HEAD  # pinned SHA
```

### Phase 1 — Submodule divergence audit (delegates to `git-divergence-audit`)

The composer script (Phase 2 below) reports:

- Whether the submodule is in **detached HEAD**.
- Ahead / behind counts of HEAD vs `origin/<default>`.

If `behind > 0` and detached, that is the fingerprint of "pinned SHA refers to a fork the upstream never had". Continue.

### Phase 2 — URL audit (composer script)

```bash
python3 <skills-root>/git-submodule-misconfiguration-audit-and-revert/scripts/audit-submodule-url-history.py \
    --repo <repo> \
    --submodule <submodule-path>
```

The script prints a structured report:

```
== STATE ==
detached_head: true
ahead:  26
behind: 0      # vs the WRONG origin
== URLS ==
.gitmodules: https://github.com/<wrong-owner>/<repo>.git
live origin: https://github.com/<wrong-owner>/<repo>.git
mismatch:    false
== HISTORY ==
URL-changing commits on .gitmodules for this submodule (newest-first):
  abc1234  2026-05-01  Author  chore(submodules): align <name> with personal fork
  ...
```

When `.gitmodules` and the live `origin` agree but neither matches the expected upstream, the wrong URL was committed AND a `submodule sync` was performed at that time. Both must be reverted (Phase 4 + Phase 5).

### Phase 3 — Direction audit (delegates to `git-commit-details-audit` "Message-vs-Diff Direction Audit")

For the candidate commit:

```bash
git -C <repo> show <SHA> -- .gitmodules
git -C <repo> log -1 --format='%B' <SHA>
```

Map every English noun in the message to a concrete URL/SHA. A message like "update from X to Y" with a diff showing `-Y / +X` is the **reversed-direction trap**. The commit may still be the right one to drop — but the author's stated intent is the inverse of what the diff did. Surface this to the user before proceeding.

### Phase 4 — Drop the commit (delegates to `git-commit-edit`)

If the commit is **single-purpose** (touches only `.gitmodules`'s URL line for this submodule):

```bash
git -C <repo> rebase --onto <SHA>^ <SHA> <branch>
```

If **mixed**, escalate to `git-commit-edit` for hunk-level extraction. (v1 of this skill does not automate the mixed case.)

### Phase 5 — Realign the live submodule (delegates to `git-submodule-fork-reconfigure` §3)

```bash
git -C <repo> submodule sync -- <submodule-path>
```

Re-run the Phase 2 script — `mismatch` must now be `false` AND both URLs must match the expected upstream.

### Phase 6 — Cascade restack (hand-off to `git-dependent-branch-restack-cascade`)

Discover dependents per cascade Phase 1. For each dependent classify the **pre-rewrite parent**:

- If the dependent's old parent **was** the old tip → restack onto the new tip (cascade §3).
- If the dependent's old parent was a **mid-history** commit that was itself rewritten by the drop → restack onto the rewritten equivalent per cascade **§4.7**. This is the central pitfall of this workflow.

***

## 4. Pitfalls

### 4.1 Reversed-direction commit message

Already covered by Phase 3 / `git-commit-details-audit`. The risk is dropping the WRONG commit because you trusted the message verbs. Always read the diff first.

### 4.2 Forgetting `git submodule sync` after the rebase

`git rebase --onto` updates `.gitmodules` in the superproject working tree, but the submodule's own `.git/config` still carries the wrong URL until you run `submodule sync`. Skipping Phase 5 leaves the submodule broken even though the superproject looks correct.

### 4.3 Dependent rooted on a rewritten mid-history commit

Cascade §4.7. Do NOT silently rebase `--onto <new-tip> <old-tip>` for ALL dependents; classify per-dependent first.

***

## 5. Acceptance Criteria

- Superproject `.gitmodules` URL for the named submodule matches the expected upstream.
- Live submodule's `git -C <submodule> remote get-url origin` matches.
- Phase 2 script reports `mismatch: false` with both URLs at the expected value.
- Dependent branches restacked per cascade skill; force-pushes gated by the author.

***

## 6. Source Recipe Reference

Session 2026-05-30 on `<ORG-USER>/<REPO>`: discovered `<SUBMODULE>` submodule URL had been silently swapped to a personal fork by commit `<SHA-URL-SWAP>` with a *reversed-direction* message; dropped via `git rebase --onto <SHA-URL-SWAP>^ <SHA-URL-SWAP> <DEFAULT-BRANCH>`; ran `git submodule sync <SUBMODULE>`; cascaded two stash branches — one (`<STASH-A>`) was rooted on the old tip (correct on naive `--onto <new-tip>`), the other (`<STASH-B>`) was rooted on a mid-history commit `<SHA-OLD-PARENT>` whose rewritten equivalent is `<SHA-NEW-EQUIV>` (required cascade §4.7 fix). Sanitized via [`redaction-portability`](../redaction-portability/SKILL.md).
