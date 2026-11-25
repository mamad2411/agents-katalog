---
name: renovate-dependent-branch-auto-rebase
description: Composer — orchestrates Renovate auto-rebase workflow using config patterns + detector + git-dependent-branch-restack-cascade fallback
category: Composer
---

# Renovate Dependent Branch Auto-Rebase Skill (v1)

> **Skill ID:** `renovate-dependent-branch-auto-rebase`<br>
> **Version:** 1.0.0<br>
> **Standard:** [Agent Skills (agentskills.io)](https://agentskills.io)

## Description

A composer skill that orchestrates the "Renovate auto-rebases dependent branches on base branch rewrite" workflow. It uses two base skills (`renovate-config-patterns` for config generation, `renovate-auto-rebase-detector` for detection) and integrates with the existing `git-dependent-branch-restack-cascade` skill for manual restack fallback when Renovate won't auto-rebase.

**The core problem**: Renovate's default `rebaseWhen: "auto"` does NOT auto-rebase on every base branch rewrite — only if automerge is enabled OR branch protection requires up-to-date PRs. This skill ensures Renovate branches always follow the base branch, either via Renovate's native auto-rebase (when properly configured) or via manual restack cascade fallback.

## Composition Rationale

This skill is a **composer**. It orchestrates the following primitives without reimplementing them:

| Composed Skill | Used for |
|---|---|
| [`renovate-config-patterns`](../renovate-config-patterns/SKILL.md) | Generating Renovate config with `rebaseWhen: "behind-base-branch"` for true auto-rebase |
| [`renovate-auto-rebase-detector`](../renovate-auto-rebase-detector/SKILL.md) | Detecting if current Renovate config will auto-rebase on base rewrite |
| [`git-dependent-branch-restack-cascade`](../../git/branch/dependent-branch-restack-cascade/SKILL.md) | Manual restack fallback when Renovate won't auto-rebase |

The composer **MUST NOT** reimplement config generation, detection logic, or restack mechanics — those are the base skills' jobs.

## Related Skills

- [`renovate-config-patterns`](../renovate-config-patterns/SKILL.md) — base skill for config generation
- [`renovate-auto-rebase-detector`](../renovate-auto-rebase-detector/SKILL.md) — base skill for detection
- [`git-dependent-branch-restack-cascade`](../../git/branch/dependent-branch-restack-cascade/SKILL.md) — manual restack fallback

## Source Rules

| Rule File | Scope Incorporated |
|---|---|
| [`ai-rule-standardization-rules.md`](../../../../ai-agent-rules/ai-rule-standardization-rules.md) | Skill-First Architecture, Layered Composition Mandate |
| [`scripting-language-selection-rules.md`](../../../../ai-agent-rules/scripting-language-selection-rules.md) | Tier-1 (Python) default for new scripts |
| [`skill-factory/SKILL.md`](../../../skill-factory/SKILL.md) | Industrial protocol for skill creation |

***

## 1. When to Apply

Apply this skill when you want to ensure Renovate branches always follow the base branch after a rewrite/push, regardless of Renovate's current configuration. Use cases:

- After a base branch rewrite (amend, rebase, force-push), ensure all Renovate branches follow
- Pre-flight check: will Renovate handle the restack, or do we need manual cascade?
- Automated workflow: configure Renovate for auto-rebase, then verify; fallback to manual if not

Do NOT apply when:
- You only need config generation (use `renovate-config-patterns` directly)
- You only need detection (use `renovate-auto-rebase-detector` directly)
- You only need manual restack (use `git-dependent-branch-restack-cascade` directly)

***

## 2. Prerequisites

| Requirement | Minimum |
|---|---|
| Python | 3.12+ |
| Dependencies | `ruff` (lint), `pytest` (test) |
| Git | CLI available |
| `gh` CLI | For branch protection / merge queue detection |
| Base skills | `renovate-config-patterns`, `renovate-auto-rebase-detector` |
| Composed skill | `git-dependent-branch-restack-cascade` |

***

## 3. Step-by-Step Procedure

### 3.1 Workflow Script

**Script:** `scripts/run-renovate-auto-rebase-workflow.py`

**CLI Contract:**

```bash
python3 scripts/run-renovate-auto-rebase-workflow.py \
    --base-branch <name> \
    --renovate-branches <glob-pattern> \
    --mode auto|manual \
    --dry-run \
    [--config-path <path>] \
    [--git-dir <path>]
```

**Parameters:**

| Argument | Required | Description |
|---|---|---|
| `--base-branch` | Yes | Base branch name (e.g., `main`, `develop`) |
| `--renovate-branches` | Yes | Glob pattern for Renovate branches (e.g., `renovate/*`) |
| `--mode` | Yes | `auto` (use Renovate if possible, fallback to manual) or `manual` (always use cascade) |
| `--dry-run` | No | If set, print actions without executing |
| `--config-path` | No | Path to Renovate config (default: `renovate.json`) |
| `--git-dir` | No | Git repo path (default: current dir) |

**Workflow Logic:**

```python
def run_workflow(args):
    # 1. Detect if Renovate will auto-rebase
    detector_result = run_detector(args.config_path, args.git_dir)
    
    if detector_result["will_auto_rebase"] and args.mode == "auto":
        # Renovate will handle it - verify config has rebaseWhen=behind-base-branch
        if not detector_result["rebaseWhen"] == "behind-base-branch":
            # Config needs update - generate new config with rebaseWhen=behind-base-branch
            generate_config_with_auto_rebase()
            print("Updated Renovate config with rebaseWhen=behind-base-branch")
        print("Renovate will auto-rebase on base rewrite - no manual action needed")
        return
    
    # Renovate won't auto-rebase - use manual cascade
    if args.mode == "auto":
        print("Renovate won't auto-rebase (default config). Falling back to manual cascade.")
    else:
        print("Manual mode selected. Using git-dependent-branch-restack-cascade.")
    
    # Discover Renovate branches
    renovate_branches = discover_renovate_branches(args.renovate_branches_glob)
    
    # Run git-dependent-branch-restack-cascade
    run_cascade(base_branch=args.base_branch, 
                old_tip=detector_result.get("old_tip"),
                new_tip=detector_result.get("new_tip"),
                dependents=renovate_branches)
```

### 3.2 Base Skill Integration

The composer shells out to the base skills via their CLI contracts:

```python
# Generate config with auto-rebase
subprocess.run([
    "python3", 
    "renovate-config-patterns/scripts/generate-renovate-config.py",
    "--template", "automerge",
    "--output", "renovate.json",
    "--params", json.dumps({
        "rebaseWhen": "behind-base-branch",
        "automerge": True,
        "automergeStrategy": "rebase",
    })
], check=True)

# Detect auto-rebase behavior
result = subprocess.run([
    "python3",
    "renovate-auto-rebase-detector/scripts/detect-renovate-auto-rebase.py",
    "--config", "renovate.json",
    "--git-dir", ".",
    "--output", "json"
], capture_output=True, text=True, check=True)
detector_result = json.loads(result.stdout)
```

### 3.3 Manual Cascade Integration

The composer invokes `git-dependent-branch-restack-cascade` via its PowerShell script or by shelling out to its entry point. The composer prepares the dependent inventory (Renovate branches matching the glob pattern) and passes the old/new tip SHAs.

```powershell
# Discover Renovate branches
$renovateBranches = git for-each-ref --format='%(refname:short)' refs/heads/renovate/* refs/remotes/origin/renovate/*

# For each, check if merge-base with base branch equals old tip
$dependents = foreach ($b in $renovateBranches) {
    $mb = git merge-base $b $newTip
    if ($mb -eq $oldTip) { $b }
}

# Invoke cascade skill
& "$SCRIPT_DIR/../../git/branch/dependent-branch-restack-cascade/scripts/cascade.ps1" `
    -OldTip $oldTip `
    -NewTip $newTip `
    -Dependents $dependents `
    -MovedBranch $baseBranch
```

***

## 4. Composition Rationale

This skill is a **composer**: it does NOT re-implement config generation, detection logic, or restack mechanics. It orchestrates three atomic primitives:

1. **`renovate-config-patterns`** — invoked FIRST when config update needed. Generates Renovate config with `rebaseWhen: "behind-base-branch"` for true auto-rebase. Called via `scripts/generate-renovate-config.py --template automerge --params '{"rebaseWhen": "behind-base-branch", "automerge": true}'`.

2. **`renovate-auto-rebase-detector`** — invoked SECOND to determine current state. Detects if current Renovate config will auto-rebase on base rewrite. Called via `scripts/detect-renovate-auto-rebase.py --config renovate.json --git-dir . --output json`. Output determines workflow path.

3. **`git-dependent-branch-restack-cascade`** — invoked LAST as fallback. When Renovate won't auto-rebase (detector returns false), this skill cascades the restack across all Renovate branches. Called via its PowerShell entry point with the discovered Renovate branches as dependents.

**The composer's domain-specific value-add**: A single unified workflow that guarantees Renovate branches follow the base branch, regardless of Renovate's current configuration. It bridges the gap between Renovate's conditional auto-rebase and the guarantee that dependent branches must always follow the base.

**Bidirectional discoverability**: Both base skills list this composer in their `## Composition by Higher-Level Skills` tables.

***

## 5. Acceptance Criteria

The skill is complete when:

1. `scripts/run-renovate-auto-rebase-workflow.py` correctly orchestrates all three primitives
2. Auto mode: detects auto-rebase capability, updates config if needed, falls back to cascade
3. Manual mode: skips detection, directly runs cascade on Renovate branches
4. Dry-run mode prints actions without executing
5. Integration with `git-dependent-branch-restack-cascade` works (per-dependent parity audit, force-with-lease)
4. `CHANGELOG.md`, `TRACEABILITY.md`, `AGENTS.md` present and compliant
5. `skill-cross-reference-audit` passes

***

## 6. Related Conversations & Traceability

- Session 2026-09-19: Initial creation per implementation plan `2026-09-19-renovate-auto-rebase-documentation.md`
- Depends on: `renovate-config-patterns`, `renovate-auto-rebase-detector`, `git-dependent-branch-restack-cascade`

***

## 7. Change History

| Timestamp | Summary of Changes | Rationale |
| :--- | :--- | :--- |
| [2026-09-19 17:00] | Initial skill v1 created | Composer for Renovate auto-rebase workflow with manual fallback |

---

## 8. Traceability

See [`TRACEABILITY.md`](TRACEABILITY.md) for session logs and provenance.

---

## 9. Changelog

See [`CHANGELOG.md`](CHANGELOG.md) for release history.