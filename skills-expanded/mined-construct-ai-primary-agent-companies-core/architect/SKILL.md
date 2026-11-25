---
name: architect
description: >
  Use when: proposing architecture-aligned refactors before QA runs, assessing technical debt, reviewing code structure against architecture principles, or planning major structural changes.
  Don't use when: mapping features to disciplines (use advisor), fixing bugs (use validator), or handling cross-discipline conflicts (use liaison).
allowed-tools:
  - Read
  - Grep
  - Write
  - Glob
  - Bash
metadata:
  paperclip:
    tags:
      - knowledge-engineering
      - architecture
      - refactoring
---

# Architecture Refactoring Skill

## Purpose

This skill analyzes proposed changes against established architecture documentation and proposes refactoring approaches that improve alignment with architectural patterns while avoiding technical debt.

## When to Use

- Before major QA runs to optimize code structure
- When new features are being designed
- As part of the PR review process for significant changes
- When architecture documentation is updated

## Steps

### 1. Architecture Review

Read the architecture documentation:

```bash
# Find architecture docs
find ../docs-construct-ai/codebase/architecture -name "*.md" -type f

# Read system design principles
cat ../docs-construct-ai/codebase/architecture/system-overview.md
```

### 2. Change Analysis

Analyze the proposed changes:
- Identify which architectural layers are affected
- Check for pattern violations
- Assess coupling and cohesion impact
- Evaluate performance implications

### 3. Pattern Compliance Check

Verify compliance with established patterns:
- **Layer separation**: UI → Business Logic → Data Access
- **Dependency injection**: All dependencies are injected, not hardcoded
- **Error handling**: Consistent error boundaries and recovery
- **State management**: Predictable state updates
- **API contracts**: Stable interfaces between components

### 4. Technical Debt Assessment

Identify potential debt:
- Short-term solutions that may cause long-term problems
- Violations of SOLID principles
- Code duplication or copy-paste patterns
- Missing abstractions or inappropriate coupling

### 5. Refactor Proposal

Create a refactoring proposal that includes:

**Current State**
```typescript
// Show current code with issues
```

**Proposed State**
```typescript
// Show refactored code with improvements
```

**Rationale**
- Why the change improves architecture alignment
- How it reduces technical debt
- What risks are mitigated

**Migration Path**
- Step-by-step refactoring approach
- Backward compatibility considerations
- Testing strategy for refactored code

## Output

```markdown
# Architecture Refactoring Proposal

## Affected Components
- [Component A]: [Issue description]
- [Component B]: [Issue description]

## Pattern Violations Found
- [ ] Layer separation violated in [location]
- [ ] Dependency injection missing in [location]
- [ ] Error handling inconsistent in [location]

## Refactoring Recommendations
1. [High priority refactor]
2. [Medium priority refactor]
3. [Low priority refactor]

## Technical Debt Assessment
- Current debt level: [Low/Medium/High]
- After refactoring: [Low/Medium/High]
```

## Error Handling

- If architecture docs are missing, flag for documentation creation
- If changes are too complex, recommend incremental approach
- If refactoring would break existing functionality, document migration path

## Related Skills

- `qa-strategy` — Ensures refactored code is thoroughly tested
- `app-guardian` — Verifies architectural compliance before approval
- `doc-analysis` — Updates architecture documentation if needed