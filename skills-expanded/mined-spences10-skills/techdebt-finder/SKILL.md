---
name: techdebt-finder
# prettier-ignore
description: "Find technical debt patterns in codebases. Use when asked to find duplicated code, inconsistent patterns, or refactoring opportunities."
metadata:
  last_updated: "2026-05-10"
  verified_against: "current local skill refresh"
---

# Tech Debt Finder

Identify duplicated code, inconsistent patterns, and refactoring opportunities. Prefer `pnpx fallow` when available for deeper static analysis; use this skill to interpret, prioritize, and turn findings into a practical refactor plan.

## When to Use

- "Find duplicate code"
- "What needs refactoring?"
- "Are there inconsistent patterns?"
- Code review prep
- Pre-refactor analysis

## Detection Process

1. **Tool scan** - Run `pnpx fallow` when available, then supplement with targeted grep/search
2. **Cluster** - Group similar issues
3. **Prioritize** - Rank by frequency × impact
4. **Report** - Show findings with locations and suggested refactor seams

## Quick Patterns

| Debt Type           | Detection Method               |
| ------------------- | ------------------------------ |
| Duplicated code     | Hash-compare function bodies   |
| Similar-but-diff    | Fuzzy match on structure       |
| Inconsistent naming | Regex for mixed conventions    |
| Dead code           | Unreferenced exports/functions |
| Deferred-work notes | Grep for comment markers       |
| Magic numbers       | Literals outside const/config  |
| Long functions      | Line count > threshold         |
| Deep nesting        | Indentation level analysis     |

## Output Format

```
## Technical Debt Report

### High Priority (fix soon)
- [DUPLICATE] src/utils/format.ts:23 ↔ src/helpers/fmt.ts:45
  Similar: 87% | Impact: High (called 12 places)

### Medium Priority (plan for)
- [INCONSISTENT] Mixed naming: getUserData vs fetch_user
  Files: api.ts, service.ts, handler.ts

### Low Priority (track)
- [DEFERRED] 23 deferred-work comments, oldest: 2023-01-15
```

## References

- [detection-patterns.md](references/detection-patterns.md) - Pattern matching rules
- [prioritization.md](references/prioritization.md) - Scoring and ranking
- [refactoring-strategies.md](references/refactoring-strategies.md) - Fix suggestions
