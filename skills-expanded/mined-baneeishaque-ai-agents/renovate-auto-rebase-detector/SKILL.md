---
name: renovate-auto-rebase-detector
description: Detects if Renovate will auto-rebase given current config (domain-agnostic detection primitive)
category: Base Primitive
---

# Renovate Auto-Rebase Detector Skill (v1)

> **Skill ID:** `renovate-auto-rebase-detector`<br>
> **Version:** 1.0.0<br>
> **Standard:** [Agent Skills (agentskills.io)](https://agentskills.io)

## Description

A domain-agnostic base primitive for detecting whether a given Renovate configuration will auto-rebase on base branch rewrite. Given a Renovate config file and optional git state, outputs a deterministic boolean + reason explaining whether Renovate will auto-rebase on base branch push/rewrite.

## Composition Rationale

This skill is a **base primitive**. It owns ONLY the detection logic for Renovate's auto-rebase behavior based on config + git state. The primitive is domain-agnostic — it knows only the Renovate `rebaseWhen` semantics and git branch relationships.

Composer skills (e.g., `renovate-dependent-branch-auto-rebase`) consume this primitive by shelling out to `scripts/detect-renovate-auto-rebase.py` and interpreting the boolean + reason output.

## Related Skills

- [`renovate-config-patterns`](../renovate-config-patterns/SKILL.md) — generates configs this detector analyzes
- [`renovate-dependent-branch-auto-rebase`](../renovate-dependent-branch-auto-rebase/SKILL.md) — composer that uses this detector to decide workflow path
- [`git-dependent-branch-restack-cascade`](../../git/branch/dependent-branch-restack-cascade/SKILL.md) — manual restack fallback when detector returns false

## Source Rules

| Rule File | Scope Incorporated |
|---|---|
| [`ai-rule-standardization-rules.md`](../../../../ai-agent-rules/ai-rule-standardization-rules.md) | Skill-First Architecture, Layered Composition Mandate |
| [`scripting-language-selection-rules.md`](../../../../ai-agent-rules/scripting-language-selection-rules.md) | Tier-1 (Python) default for new scripts |
| [`skill-factory/SKILL.md`](../../../skill-factory/SKILL.md) | Industrial protocol for skill creation |

***

## 1. When to Apply

Apply this skill when you need to determine whether Renovate will auto-rebase a branch when its base branch is rewritten/pushed. Use cases:

- Pre-flight check before relying on Renovate to auto-rebase
- CI/CD pipeline gate: only skip manual restack if detector returns true
- Audit: report which Renovate branches will/won't auto-rebase

Do NOT apply when:
- You need to generate a Renovate config (use `renovate-config-patterns` instead)
- You need to orchestrate a full workflow (use `renovate-dependent-branch-auto-rebase` instead)

***

## 2. Prerequisites

| Requirement | Minimum |
|---|---|
| Python | 3.12+ |
| Dependencies | `ruff` (lint), `pytest` (test) |
| Git | CLI available for repo state queries |

***

## 3. Step-by-Step Procedure

### 3.1 Detection Logic (from Renovate docs)

The detector implements the exact `rebaseWhen` semantics from Renovate docs:

| `rebaseWhen` Value | Auto-rebase on base rewrite? | Condition |
|---|---|---|
| `behind-base-branch` | **YES** | Always rebases when 1+ commits behind base |
| `auto` | **CONDITIONAL** | Only if `automerge: true` OR branch protection requires up-to-date PRs; else `conflicted` (no auto-rebase on base rewrite) |
| `automerging` | **CONDITIONAL** | Only if `automerge: true`; else `never` |
| `conflicted` | **NO** | Only rebases when conflicted |
| `never` | **NO** | Never auto-rebase |

Additional factors:
- `platformAutomerge: true` (default) + GitHub branch protection requiring up-to-date PRs → `auto` behaves as `behind-base-branch`
- GitHub merge queue / GitLab merge trains → `auto` behaves as `conflicted`

### 3.2 Detection Script

**Script:** `scripts/detect-renovate-auto-rebase.py`

**CLI Contract:**

```bash
python3 scripts/detect-renovate-auto-rebase.py \
    --config <path-to-renovate.json> \
    --git-dir <path-to-git-repo> \
    --output json|bool \
    [--base-branch <name>]
```

**Parameters:**

| Argument | Required | Description |
|---|---|---|
| `--config` | Yes | Path to `renovate.json` / `renovate.jsonc` |
| `--git-dir` | Yes | Path to git repository (for branch protection check) |
| `--output` | No | `json` (default) or `bool` |
| `--base-branch` | No | Base branch name (default: repo's default branch) |

**Output (JSON):**

```json
{
  "will_auto_rebase": true,
  "reason": "rebaseWhen=behind-base-branch (explicit)",
  "rebaseWhen": "behind-base-branch",
  "automerge": true,
  "branch_protection_up_to_date": false,
  "platform_automerge": true,
  "merge_queue_enabled": false
}
```

**Output (bool):** Prints `true` or `false` only.

**Exit Codes:**
- `0` = detection successful (output valid)
- `1` = config not found / parse error / git error
- `2` = invalid arguments

### 3.3 Detection Algorithm

```python
def will_auto_rebase(config: dict, git_info: dict) -> tuple[bool, str]:
    rebase_when = config.get("rebaseWhen", "auto")
    automerge = config.get("automerge", False)
    platform_automerge = config.get("platformAutomerge", True)
    
    branch_protection = git_info.get("branch_protection_up_to_date", False)
    merge_queue = git_info.get("merge_queue_enabled", False)
    
    if rebase_when == "behind-base-branch":
        return True, "rebaseWhen=behind-base-branch (explicit)"
    
    if rebase_when == "automerging":
        if automerge:
            return True, "rebaseWhen=automerging with automerge=true"
        return False, "rebaseWhen=automerging but automerge=false"
    
    if rebase_when == "conflicted":
        return False, "rebaseWhen=conflicted (only rebases on conflicts)"
    
    if rebase_when == "never":
        return False, "rebaseWhen=never"
    
    # rebase_when == "auto" (default)
    if automerge:
        return True, "rebaseWhen=auto with automerge=true"
    if platform_automerge and git_info.get("branch_protection_up_to_date"):
        return True, "rebaseWhen=auto with platformAutomerge + branch protection"
    if merge_queue:
        return False, "rebaseWhen=auto with merge queue (uses conflicted)"
    
    return False, "rebaseWhen=auto (default) → conflicted (no automerge, no branch protection)"
```

***

## 4. Composition by Higher-Level Skills

| Composer | Composition Mechanism |
|---|---|
| [`renovate-dependent-branch-auto-rebase`](../renovate-dependent-branch-auto-rebase/SKILL.md) | Calls `scripts/detect-renovate-auto-rebase.py --config <path> --git-dir <path> --output json`; if `will_auto_rebase` is false, delegates to `git-dependent-branch-restack-cascade` for manual restack |

***

## 5. Acceptance Criteria

The skill is complete when:

1. `scripts/detect-renovate-auto-rebase.py` correctly implements the detection algorithm per Renovate docs
2. All `rebaseWhen` variants handled correctly (behind-base-branch, auto, automerging, conflicted, never)
3. Git branch protection / merge queue detection works on GitHub
4. Unit tests pass for all `rebaseWhen` variants + automerge/branch protection combinations
5. `CHANGELOG.md`, `TRACEABILITY.md`, `AGENTS.md` present and compliant
6. `skill-cross-reference-audit` passes

***

## 6. Related Conversations & Traceability

- Session 2026-09-19: Initial creation per implementation plan `2026-09-19-renovate-auto-rebase-documentation.md`
- Renovate rebaseWhen docs: https://docs.renovatebot.com/configuration-options/#rebasewhen

***

## 7. Change History

| Timestamp | Summary of Changes | Rationale |
| :--- | :--- | :--- |
| [2026-09-19 16:30] | Initial skill v1 created | Base primitive for Renovate auto-rebase detection |

---

## 8. Traceability

See [`TRACEABILITY.md`](TRACEABILITY.md) for session logs and provenance.

---

## 9. Changelog

See [`CHANGELOG.md`](CHANGELOG.md) for release history.