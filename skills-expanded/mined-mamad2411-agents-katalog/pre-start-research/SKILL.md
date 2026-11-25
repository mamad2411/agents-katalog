---
name: pre-start-research
description: Background research before implementation — existing solutions, best practices, patterns
triggers: [research, before building, best practices, how to do, patterns, existing solutions]
---

# SKILL: Pre-Start Research

## The 1-Hour Research Protocol

### 15 minutes: Existing Solutions
```bash
# What solves this problem already?
# Python example
pip search "problem keyword"
# Go to: pypi.org, GitHub, pypi.org/pypi

# Node example
npm search "problem keyword"

# Note: top 5 solutions, their:
  - GitHub stars (community validation)
  - Last commit date (actively maintained?)
  - License (compatible?)
  - Use case fit
```

### 15 minutes: Best Practices
```
Search: "best practices for [topic] 2024"
  - Blog posts from reputable sources
  - Official documentation
  - Stack Overflow top answers
  
Look for:
  - What's the standard approach?
  - What are common mistakes?
  - What tools are recommended?
```

### 15 minutes: Technical Patterns
```
Search: "[technology] patterns and practices"
Examples:
  - Authentication patterns
  - Caching strategies
  - Error handling patterns
  - Deployment patterns

Collect: 2-3 patterns per topic
```

### 15 minutes: Test Approach
```
For the chosen approach:
  - How do you test it?
  - What's the testing pattern?
  - What are gotchas?
```

## Research Output

```markdown
# Research: [Topic]

## Existing Solutions
| Solution | Stars | Updated | License | Fit |
|----------|-------|---------|---------|-----|
| A | 5k | 1m | MIT | Good |
| B | 1k | 6m | Apache | OK |

→ Choose: A (most maintained, good fit)

## Best Practices
1. [Practice]: [Why it's important]
2. [Practice]: [Why it's important]

## Technical Pattern
[Pattern name]
- How: [how it works]
- When: [when to use]
- Pitfall: [what goes wrong if done wrong]

## Testing Strategy
- Unit tests: [what to test]
- Integration tests: [what to test]
- Common mistakes: [what NOT to do]
```

## Quality checks
- [ ] Top 5 existing solutions researched
- [ ] Best practices documented
- [ ] Technical pattern selected
- [ ] Testing approach understood
- [ ] Comparison made (why chosen solution over others)
- [ ] Research output documented
- [ ] Ready to implement with confidence
