---
name: refactor-scan
description: Read-only refactoring analysis. Shows what needs fixing without making changes.
---

# /refactor-scan [target]

Analyze code for refactoring opportunities. **Read-only — no changes made.**

> **No arguments?** Describe this skill and stop. Do not execute.

## On Invoke

1. **Read target** files (argument or recently discussed code)
2. **Analyze** against refactoring criteria
3. **Report** issues found with locations and severity
4. **Show plan** of what `/refactoring` would do

## Criteria to Check

| Issue | Threshold | Severity |
|-------|-----------|----------|
| Function too long | >30 lines | HIGH |
| File too long | >300 lines | HIGH |
| High complexity | cyclomatic >10 | HIGH |
| Deep nesting | >3 levels | MEDIUM |
| Vague names | data/result/temp/item/info | MEDIUM |
| Duplicate code | repeated blocks | MEDIUM |
| Magic numbers | unlabeled literals | LOW |
| Missing error handling | unhandled paths | MEDIUM |
| God file | multiple concerns | HIGH |

## AI Antipatterns to Flag

- Over-abstraction (factories/wrappers used once)
- Defensive paranoia (impossible null checks)
- Comment spam (obvious comments)
- Speculative features (unused config options)
- Wrapper classes adding no value

## Output Format

```
═══════════════════════════════════════════
 REFACTOR SCAN: [target]
═══════════════════════════════════════════

 Summary: X issues found (Y high, Z medium)

 HIGH SEVERITY
   [file:line] Function too long (45 lines)
     → Split into: parseInput(), validateData(), formatOutput()

   [file:line] File too long (387 lines)
     → Extract: utils.ts, validators.ts

 MEDIUM SEVERITY
   [file:line] Vague name: "data"
     → Rename to: userPreferences

   [file:line] Deep nesting (4 levels)
     → Flatten with early returns

 LOW SEVERITY
   [file:line] Magic number: 86400
     → Extract: SECONDS_PER_DAY = 86400

 AI ANTIPATTERNS
   [file:line] Over-abstraction: ConfigFactory used once
     → Inline the factory

═══════════════════════════════════════════
 REFACTOR PLAN
═══════════════════════════════════════════

 1. Split [file] into focused modules
 2. Extract [function] from [large-function]
 3. Rename [vague-names] to [clear-names]
 4. Flatten nested conditionals in [locations]

 Run `/refactoring [target]` to apply these changes.

═══════════════════════════════════════════
```

## Rules

- **DO NOT** edit any files
- **DO NOT** use Edit, Write, or Bash tools that modify files
- Only use Read, Glob, Grep for analysis
- Report findings, suggest fixes, but make no changes
- End with clear next step: `/refactoring`
