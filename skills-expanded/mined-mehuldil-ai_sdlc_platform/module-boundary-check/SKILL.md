---
name: module-boundary-check
description: Enforce module boundaries, detect circular dependencies, validate layer separation and import rules
model: sonnet-4-6
token_budget: {input: 6000, output: 3000}
---

# Module Boundary Check Skill

Validates architectural module boundaries, prevents circular dependencies, and enforces proper layer separation.

## Architectural Rules

### 1. Layer Separation
- Valid: UI → Business Logic → Data (inward only)
- Violation: Reverse imports forbidden

### 2. No Circular Dependencies
- Rule: A → B → A not allowed (any cycle length)
- Detection: Build complete dependency graph
- Action: Reject and recommend refactor

### 3. Platform Isolation
- Separate: iOS, Android, RN code
- Shared: Common utilities only
- Violation: Platform-specific in shared forbidden

### 4. Shared Code Constraints
- Only: Common utilities, types, constants
- Never: Platform-specific code
- Forbidden: External imports in shared

### 5. Type Safety
- Require: Strict TypeScript
- Forbid: `any` types

## Import Rule Validation

### Valid Patterns
- Feature → Shared utilities
- Feature → Core services
- Screens → Components (same feature)
- Feature A → Core → Feature B (via core)

### Invalid Patterns
- Component → Screen (reverse)
- Feature A → Feature B (direct cross-feature)
- Shared → Platform-specific
- Data → UI (reverse layer)

## Validation Process

1. **Dependency Graph Analysis**: Parse imports, build graph
2. **Circular Detection**: Detect all cycle types
3. **Layer Validation**: Verify inward-only imports
4. **Import Rule Check**: Enforce valid patterns
5. **Public API Check**: Verify only public imports

## Common Violations & Fixes

| Violation | Fix |
|-----------|-----|
| Circular: A ↔ B | Extract common component |
| Reverse layer | Move UI code to separate module |
| Cross-feature | Route through Core module |
| Shared imports external | Keep external in feature |
| Platform in shared | Move to platform directory |

## Guardrails

- Reject boundary violations (FAIL)
- Enforce layer separation (FAIL if reversed)
- No external imports in shared (FAIL)
- Proper dependency direction (FAIL if reversed)
- No circular dependencies (FAIL)
- Type safety (WARN on any)

## Triggers

Use when:
- PR changes module imports
- New dependencies added
- Module structure refactored
- Cross-module refactor needed
- Architecture review required

---
