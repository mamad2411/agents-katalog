---
name: test-gap-cartographer
description: "Semantic test gap mapper: inventories the public code surface (exports, routes) and all existing tests, then has the LLM map which BEHAVIORS of each public symbol are covered by which test and which are not - reporting untested behaviors (edge cases, error paths, boundaries) ranked by risk, with proposed test case names. Static, never runs tests. Read-only. Trigger: /testgap"
trigger: /testgap
---

## What this is for

100% coverage, 0% confidence? Coverage measures lines, not behavior. A function can have 100% line coverage and still be untested for exactly the cases that hurt in production: empty lists, boundaries, error paths, concurrency. The question "which BEHAVIOR is untested?" requires understanding code semantically AND mapping existing tests - infeasible for humans at real scale, systematically feasible for an LLM.

**Audience:** Senior
- QA uses it to prioritize what to test next.
- Reviewers use it to catch "is there a test for this?" gaps.
- Teams use it before refactoring to know what's guarded.

### Trigger: `/testgap`


## PROTECTION RULE - never ~/.claude/

Read-only skill. Guard required if write mode added later.

## What You Must Do When Invoked
During analysis, assign a confidence level to each finding: proven (confirmed by evidence), likely (strong signal, needs review), or suspected (weak signal).

### Step 1 - `-help`/`-h` check
Print usage block and stop.

### Step 2 - Determine project path
Ask for `-ProjectDir` + optional focus subpath. Confirm with user.

### Step 3 - Run both collectors
```powershell
& .\scripts\surface-inventory.ps1 -ProjectDir "<path>" [-Focus "<subdir>"]
& .\scripts\test-inventory.ps1 -ProjectDir "<path>"
```

### Step 4 - LLM analysis
1. **Behavior model per symbol** (prioritize: branchCount x blockLines, routes always): read source code and enumerate distinguishable behaviors - normal case(s), edge cases (empty/null/0/negative/maximum), error paths (throws, error returns), state dependencies.
2. **Test mapping**: via imports + test names + (if unclear) test file content → which test case covers which behavior. Confidence: `confirmed` (test calls symbol with matching scenario), `probable` (name matches, content not checked).
3. **Gap determination**: behaviors without a mapped test. Risk: `high` (error path/money/data loss proximity), `medium` (edge case in used path), `low` (exotic).
4. **Report**: summary (n symbols, m behaviors, k untested, high: x) → gap list by risk → coverage table (symbol x behavior x test) → unmapped tests → open questions.

### Step 5 - Produce report
Write `testgap-report.md`:

```
# Test Gap Report - <project>

## Summary
- <N> public symbols, <M> behaviors identified, <U> untested
- <H> high, <M2> medium, <L> low risk gaps

## Gaps (by Risk)
### High
Symbol | File:Line | Untested Behavior | Why Risky | Suggested Test Name | Scenario
...

### Medium
...

### Low
...

## Coverage Table
Symbol | File:Line | Behavior | Covered By | Confidence
... | ... | ... | ... | ...

## Unmapped Tests
Test | File:Line | Target Symbol Unknown
... | ... | ...

## Open Questions
```

## Usage

```powershell
# Interactive
/testgap

# Full project
/testgap C:\Projects\my-app

# Focus on subdirectory
/testgap C:\Projects\my-app src/core

# Help
/testgap --help
```
