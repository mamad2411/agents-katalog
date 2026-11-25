---
name: blueprint-audit
description: Deep audit of exported Blueprint data — full pattern scan, graph health checks, and cross-function analysis. Use after blueprint-export has generated T3D or snapshot files.
allowed-tools: [Read, Write, Glob, Grep, Bash]
---

# Blueprint Audit

Perform a comprehensive audit of previously exported Blueprint data. This is the deep analysis — it reads exported files and runs every pattern and heuristic check.

## Before Starting

Read the knowledge base:
1. `${CLAUDE_SKILL_DIR}/../../data/patterns/ue5-universal-patterns.md`
2. `${CLAUDE_SKILL_DIR}/../../data/language-rules.md`

## Steps

### 1. Find Export Data

Look for exported files in `${CLAUDE_PLUGIN_DATA}/`:
- `.t3d` files (T3D exports)
- `*_snapshot.json` files (graph snapshots)

If no exports found, tell the user to run `/ue5-blueprints:blueprint-export` first.

### 2. Parse and Map

For each Blueprint function/graph:
- List all nodes with friendly names
- Trace execution flow (entry → ... → return)
- Map data wiring (which pins connect to which)
- Identify all variables (Get and Set)
- Note all default/literal values

### 3. Pattern Scan

Run every pattern P-001 through P-025 against each function. For each match:

**Tag with confidence:**
- **CERTAIN** — You traced the wires and confirmed the bug
- **PROBABLE** — Strong signal but needs context
- **POSSIBLE** — Heuristic flag, might be intentional

### 4. Graph Health Checks

For each function:
- [ ] Dead-end execution paths?
- [ ] Orphaned nodes (no connections)?
- [ ] Cast without failure wiring?
- [ ] ForEachLoop with unwired Completed?
- [ ] Array Get without bounds check?
- [ ] Write-only variables (Set but never Get)?
- [ ] Read-before-write variables?
- [ ] Select/Switch with missing cases?

### 5. Cross-Function Analysis

If multiple functions were exported:
- Do any functions share variables? Check for write conflicts.
- Are there Save/Restore pairs? Check for field index mismatches.
- Does the call chain propagate required parameters (like actor references)?

### 6. Report

```
=== AUDIT: [BlueprintName] ===

FUNCTIONS SCANNED: [count]
ISSUES FOUND: [count by severity]

--- [FunctionName] ---

EXEC FLOW:
  Entry → Node1 → Node2 → ... → Return

BUGS:
  [Bug1] P-001 CRITICAL (CERTAIN) — BreakStruct copy on Array_Set_1
    Plain English: [explanation]
    Fix: [steps using language rules]

HEURISTIC FINDINGS:
  [H1] ForEachLoop_1.Completed disconnected (POSSIBLE)
  [OK] No orphaned nodes
  [OK] No write-only variables

CROSS-FUNCTION:
  [Any dependency issues]

VERDICT: [Clean / Needs Fixes / Critical Issues]
```

Present CERTAIN findings first, then PROBABLE, then POSSIBLE.
