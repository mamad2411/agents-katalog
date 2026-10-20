---
allowed-tools: Task, Read, Grep, Bash(git diff)
argument-hint: [issue-number]
description: Audit changes against lean principles
model: claude-sonnet-4-20250514
---

## Lean Audit

Validate current changes against lean development principles.

### Context
- Issue number (optional): $ARGUMENTS
- Check changes against issue requirements if provided
- Otherwise audit current uncommitted changes

### Audit Workflow

Run specialized audit agents in sequence:

#### 1. Scope Validation (scope-guardian)
- Compare changes to issue requirements
- Flag any out-of-scope additions
- Identify "while we're here" changes
- List features that should be removed

#### 2. Bloat Detection (bloat-detector)
- Find dead code
- Identify unused imports
- Detect over-engineered patterns
- Count potential line reductions

#### 3. Complexity Analysis (complexity-auditor)
- Measure cyclomatic complexity
- Check nesting depth
- Flag long methods
- Identify simplification opportunities

#### 4. Dependency Check (dependency-tracker)
- List any new dependencies
- Suggest standard library alternatives
- Calculate dependency weight
- Flag unnecessary packages

#### 5. Performance Review (performance-monitor)
- Check for algorithmic issues
- Identify redundant operations
- Flag premature optimizations
- Focus on efficiency over speed

### Report Format

```
LEAN AUDIT REPORT
================

✅ PASS / ❌ FAIL

Scope Compliance: [PASS/FAIL]
- Issues: ...

Code Bloat: [X lines could be removed]
- Locations: ...

Complexity: [X violations]
- Hot spots: ...

Dependencies: [X new, Y could be removed]
- Suggestions: ...

Performance: [No issues / X concerns]
- Details: ...

REQUIRED ACTIONS:
1. ...
2. ...
```

Focus on what to REMOVE, not what to add.
