---
name: ai-smell-scan
description: Detect AI-generated code smells. Read-only - does not fix.
---

# /ai-smell-scan [path]

**Read-only** scan for AI-generated code patterns. Reports findings without making changes.

> **No arguments?** Describe this skill and stop. Do not execute.

## The AI Smell Index

Each smell type has a severity weight. The **AI Smell Index** is the weighted sum.

| Smell Type | Weight | Why |
|------------|--------|-----|
| Over-abstraction | 3 | Adds complexity, hides logic |
| Defensive paranoia | 3 | Implies distrust in own code |
| Comment spam | 1 | Noise, but harmless |
| Speculative features | 3 | Dead code, maintenance burden |
| Enterprise patterns | 3 | Massive overkill |
| Generic wrappers | 2 | Indirection without value |
| Verbose naming | 1 | Annoying but functional |
| Excessive structure | 2 | Navigation overhead |

**Index interpretation:**
- 0-5: Clean — human-like code
- 6-15: Minor — a few AI fingerprints
- 16-30: Moderate — noticeable AI patterns
- 31-50: Heavy — needs cleanup
- 51+: Severe — AI slop, run /ai-smell-fix

## The AI Smell Checklist

### Over-Abstraction (weight: 3)
- Factories/wrappers used exactly once
- Abstract base class with one implementation
- Unnecessary indirection layers
- Single-use helper functions

### Defensive Paranoia (weight: 3)
- Null checks where null is impossible (typed params)
- Try/catch around infallible code
- Validating internal function arguments
- Empty catch blocks

### Comment Spam (weight: 1)
- Comments that repeat the code
- `// increment counter` above `counter++`
- JSDoc restating the function name
- Obvious comments on obvious code

### Speculative Features (weight: 3)
- Config options nobody uses
- Parameters with only one value ever passed
- Dead feature flags
- Options objects with single caller

### Enterprise Patterns in Simple Code (weight: 3)
- Repository pattern for one entity
- Strategy pattern with one strategy
- Builder pattern for simple objects
- Factory for single product

### Generic Wrapper Abuse (weight: 2)
- `Result<T, E>` when you just throw
- Custom types that add no value over primitives
- Wrapper class with one method

### Verbose Naming (weight: 1)
- Names longer than 25 characters
- Redundant prefixes/suffixes (`userUserData`)

### Excessive Structure (weight: 2)
- Single-method classes
- Deep folder nesting (4+ levels)
- Index file re-export chains
- Files with 5+ functions under 5 lines each

## Output Format

```markdown
## AI Smell Scan: [target]

SMELLS_FOUND:
- [file:line] [smell type]: [description]
- [file:line] [smell type]: [description]

SUMMARY:
| Smell Type | Count | Weight | Score |
|------------|-------|--------|-------|
| Over-abstraction | N | 3 | N×3 |
| Defensive paranoia | N | 3 | N×3 |
| Comment spam | N | 1 | N×1 |
| Speculative features | N | 3 | N×3 |
| Enterprise patterns | N | 3 | N×3 |
| Generic wrappers | N | 2 | N×2 |
| Verbose naming | N | 1 | N×1 |
| Excessive structure | N | 2 | N×2 |

TOTAL_SMELLS: N
AI_SMELL_INDEX: N (interpretation)

RECOMMENDATION: Run /ai-smell-fix to clean up
```

## Tracking Over Time

Use the AI_SMELL_INDEX to compare before/after:

```bash
# Before changes
/ai-smell-scan src/  → AI_SMELL_INDEX: 12

# After implementing with full base brain
/ai-smell-scan src/  → AI_SMELL_INDEX: 18

# Delta: +6 (got worse)
```

Track index after each `/build` or `/improve` run to detect skill configuration impact.

## No Changes Made

This is a **read-only** scan. Use `/ai-smell-fix` to fix issues.
