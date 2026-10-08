---
name: documentation-as-code
description: JSDoc/docstrings on exports, README sync, API documentation, architecture decision records, and changelog entries.
invoke_when: Use when creating public APIs, writing modules, completing features, or when documentation is stale, missing, or out of sync with code.
---

# Documentation as Code

## Principle

Documentation that lives outside the codebase rots. Keep documentation as close to the code as possible, ideally generated from it.

## What to Document

### Always Document
- Public API functions (JSDoc/docstrings with params, returns, throws)
- Module purpose (brief comment at top of file explaining what this module does)
- Non-obvious business logic (why, not what)
- Architecture decisions (ADRs in `.shipworthy/decisions/`)
- API endpoints (request/response types serve as documentation)
- Environment variables (what each one does, valid values)

### Don't Document
- Self-explanatory code (`getUser(id)` doesn't need a docstring saying "gets a user")
- Implementation details that change frequently
- Code that should be refactored instead of documented

## JSDoc Pattern (TypeScript/JavaScript)
```typescript
/**
 * Calculate insurance premium based on fleet safety score.
 *
 * @param fleetScore - Safety score from 0-100
 * @param basePremium - Current annual premium in dollars
 * @returns Adjusted premium with discount/surcharge applied
 * @throws {AppError} If fleetScore is outside valid range
 */
export function calculatePremium(fleetScore: number, basePremium: number): number {
```

## README Requirements

Every project README should have:
1. **What** — one sentence explaining what this project does
2. **Quick start** — how to run it locally (3 commands max)
3. **Architecture** — high-level overview (link to architecture.md for details)
4. **Contributing** — how to contribute

## Architecture Decision Records

For significant decisions, create `.shipworthy/decisions/NNN-title.md`:
```markdown
# ADR-NNN: [Decision Title]
## Status: Accepted | Superseded | Deprecated
## Date: YYYY-MM-DD
## Context: [What prompted this decision]
## Decision: [What was decided]
## Consequences: [What this means going forward]
```

## Changelog

Maintain a CHANGELOG.md for user-facing changes:
- **Added** — new features
- **Changed** — changes in existing functionality
- **Fixed** — bug fixes
- **Removed** — removed features
- **Security** — vulnerability fixes
