---
name: simplification
description: Complexity reduction and architectural streamlining for Frontend, Backend, and Quality agents.
---

# Simplification Skill (Occam's Razor)

## Purpose

"Simplicity is the ultimate sophistication." This skill provides a rigorous protocol for identifying and eliminating over-engineering, code bloat, and technical debt across the entire stack.

## Overview

The Simplification Skill is a cross-functional protocol used to flatten logic, reduce state, and ensure every line of code justifies its existence. It leverages specialized agents and MCP tools to validate architectural simplicity and performance.

## Prerequisites

- **Agents**: [Backend](file:///.opencode/agents/backend.md), [Frontend](file:///.opencode/agents/frontend.md), [Quality](file:///.opencode/agents/quality.md).
- **MCP Tools**:
  - `context7`: To research lightweight alternatives and library standards.
  - `sequential-thinking`: To audit complex logic flows for potential flattening.
  - `sqlite`: To verify if database schemas or queries can be compressed.
  - `playwright`/`chrome-devtools`: To identify UI "jank" or DOM complexity.

## Agent-Specific Simplification Protocols

### [Senior Backend Engineer](file:///.opencode/agents/backend.md)

- **State Reduction**: Derive values instead of storing them. If `is_active` can be derived from `status === 'active'`, delete the redundant field.
- **Query Optimization**: Use `sqlite` to check for N+1 issues. Replace nested loops with single optimized queries or batching.
- **Error Flattening**: Centralize error handling middleware. Remove repetitive `try/catch` blocks from business logic to expose the "Happy Path".

### [Senior Frontend Engineer](file:///.opencode/agents/frontend.md)

- **DOM Streamlining**: Replace "Div Soup" with semantic HTML elements.
- **Hook Optimization**: Audit `useEffect` usage. If it's used to sync state, replace it with derived constants or `useMemo`.
- **Styling Discipline**: Replace custom inline styles with standard Tailwind utility classes or `cva` variants.

### [QA Automation Engineer](file:///.opencode/agents/quality.md)

- **Test Pruning**: Remove redundant unit tests if the logic is covered by a high-confidence integration test.
- **Selector Simplification**: Replace fragile XPaths or class-based selectors with accessible `getByRole` or `getByLabel` locators.

## The Procedural Workflow

### 1. The Deletion Test

- **Action**: Use `grep_search` to find references to the target code. If references < 1, **DELETE**.
- **Rule**: Dead code is the best code.

### 2. The Library Leverage (via `context7`)

- **Action**: Use `context7` to check if a complex custom utility (e.g., date formatting, deep cloning) can be replaced by a native function or a lightweight standard library (Lodash/Zustand).

### 3. Flat Logic Audit (via `sequential-thinking`)

- **Action**: Step through the logic. If nesting > 3 levels or cyclomatic complexity is high, apply guard clauses.
- **Target Pattern**:

  ```diff
  - if (user) {
  -   if (user.active) {
  -     return doThing();
  -   }
  - }
  + if (!user?.active) return;
  + return doThing();
  ```

## Complexity Metrics to Watch

- **Nesting Level**: Maximum 3 levels of indentation.
- **Function Size**: Maximum 30 lines.
- **Cognitive Weight**: If a function requires `sequential-thinking` just to "read" it, it's too complex.

## Output Format

```markdown
## Simplification Review: [Target File/Function]

### 1. Opportunities Identified
| Area | Description | Tool Used | Impact |
|------|-------------|-----------|--------|
| Logic | Flatten nested `if` statements | `sequential-thinking` | High |
| State | Remove redundant `isLoading` boolean | - | Medium |
| Lib | Replace custom deep clone with `structuredClone` | `context7` | Low |

### 2. Implementation: Before vs After
**Before**:
```javascript
// Complex, nested, or redundant code
```

**After**:

```javascript
// Streamlined, readable, and efficient code
```

### 3. Impact Assessment

- Lines Removed: [Count]
- Performance Gain: [e.g., Reduced O(N²) to O(N)]
- Maintenance Status: Optimized

```
