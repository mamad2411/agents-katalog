---
name: precommit-pipeline
version: 1.0.0
description: Pre-commit verification pipeline. Run before git commit: self-audit, syntax check, reference integrity, optional cross-model review.
---

# Pre-Commit Verification Pipeline

> **"改完代码 → 自动检查 → 安全提交"** — 提交前拦截 bug，不是提交后修 bug。

## Pipeline

```
Code done → Self-audit (4Q) → Syntax check → Reference integrity → Cross-model review (optional) → Commit
```

## 1. Self-Audit (4 Questions)
- Read first? Verified? All references checked? Can it be simpler?

## 2. Syntax Check
- PowerShell: `[Parser]::ParseFile($path, [ref]$null, [ref]$errors)`
- Python: `python -m py_compile`
- JSON: `ConvertFrom-Json`
- Fail → fix → back to step 1

## 3. Reference Integrity
- Changed symbols → Grep entire repo
- Changed paths → Grep all `.ps1/.py/.md`
- Changed config keys → check all usage points
- Broken refs → fix → back to step 1

## 4. Cross-Model Review (required for)
- Security-related code → security-auditor agent
- Architecture changes → adversarial-reviewer agent
- Complex logic (>20 new lines) → code-review agent

## 5. Commit
- Message: what + why. End with `Co-Authored-By: Claude <noreply@anthropic.com>`

## Fast Track (skip step 4)
- Single-line typo / formatting / comments / config value (no logic change)

## Success Story
Without: changed function signature → forgot 3 call sites → broke production → 2h debugging.
With: changed signature → reference check caught all 3 → fixed before commit → 0 downtime.

## Trigger

Run manually before `git commit`, or wire into a git pre-commit hook. Fast-track skips step 4 for: single-line typo, formatting only, config value change (no logic).

## Integration
- **second-brain**: Step 4 cross-model review delegates to Brain 2 adversarial-reviewer
- **memory-lora**: 🔜 Bugs caught → stored in memory.db for pattern detection
- **delegation-lora**: Step 4 = delegation trigger #5 (cross-model review)
