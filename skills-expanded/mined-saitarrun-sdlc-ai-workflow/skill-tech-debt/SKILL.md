---
name: skill-tech-debt
description: Tech debt inventory, paydown strategy, prioritization (Critical/High/Medium/Low), deprecation planning, communicating to stakeholders, refactoring initiatives. Use when managing technical debt, planning paydown, or assessing refactoring ROI.
version: 1.0.0
---

# Skill: Tech Debt Management

Track, prioritize, and pay down tech debt systematically. Don't let it spiral.

## Tech Debt Scoring

**Impact × Effort Matrix**:

```
         LOW EFFORT → HIGH EFFORT
HIGH   |  Quick wins  | Strategic |
IMPACT |              |           |
LOW    | Skip (low ROI)| Avoid    |
```

**Quick wins**: High impact, low effort → Do first  
**Strategic**: High impact, high effort → Plan next quarter  
**Skip**: Low impact, any effort → Only if free time

## Inventory Template

```
## Tech Debt Inventory: [Service]

### CRITICAL (Ship next sprint)
- [ ] Remove Python 2 support (ends 2025, blockers future deps)
  - Effort: 2 weeks
  - Impact: Unblocks 5 dependencies
  - Owner: Backend lead

### HIGH (Backlog, 10% capacity/sprint)
- [ ] Refactor auth middleware (5 places copy-pasted)
  - Effort: 1 week
  - Impact: Reduces bugs, improves maintainability
  - Owner: TBD

### MEDIUM (Nice to have)
- [ ] Extract common utils from 3 services
  - Effort: 3 weeks (spans services)
  - Impact: Code reuse

### LOW (Skip unless free time)
- [ ] Rename internal variable
  - Effort: 1 hour
  - Impact: Readability (minimal)
```

## Paydown Strategy

**Allocate 10% of sprint to tech debt**:
- 80% features (business value)
- 10% tech debt (internal quality)
- 10% bugs (production stability)

**Communicate ROI**:
```
Tech debt paydown: Remove Python 2 support
- Effort: 2 weeks (1 engineer)
- Unblocks: 5 dependencies (new features)
- Prevents: 3+ security issues (old Python 2 libs)
- ROI: High (enables future work)
```

## Deprecation Planning

```
v1.0: Old API endpoint alive
v1.5: Announce deprecation (email, docs)
v2.0: Mark endpoints as "deprecated" (header warning)
v2.5: Remove endpoint (6 months later)
```

---

**Status**: Ready for tech debt management  
**Best for**: Debt prioritization, paydown planning, refactoring
