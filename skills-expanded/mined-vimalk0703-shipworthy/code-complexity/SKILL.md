---
name: code-complexity
description: Enforce cyclomatic complexity limits, function/file length limits, nesting depth, parameter counts, and duplication detection. Keeps code readable and maintainable.
invoke_when: Use when writing or reviewing functions that are growing long, deeply nested, or have many parameters, or when refactoring complex code or setting up linting rules.
---

# Code Complexity

## Limits at a Glance

| Metric | Limit | Action When Exceeded |
|--------|-------|---------------------|
| Cyclomatic complexity | < 15 per function | Extract helper functions |
| Function length | ~50 lines max | Split into focused functions |
| File length | ~300 lines max | Extract modules/classes |
| Nesting depth | Max 4 levels | Early returns, extract functions |
| Parameter count | Max 4-5 params | Use an options/config object |
| Duplicate blocks | > 3 lines repeated 2+ times | Extract shared function |

## Cyclomatic Complexity (< 15 per function)

Each `if`, `else`, `case`, `&&`, `||`, `catch`, and ternary adds 1. When a function exceeds 15, extract validation, branching logic, or case handling into separate functions.

## Function Length (~50 Lines Max)

If you need a comment like `// Step 3: ...`, that step is its own function.

```typescript
// BAD -- 120-line function with section comments
function handleRequest(req: Request) { /* validate, fetch, transform, respond */ }

// GOOD -- each concern is a named function
function handleRequest(req: Request) {
  const input = validateInput(req);
  const data = fetchDependencies(input);
  return saveAndRespond(transformData(data));
}
```

## Deep Nesting (Max 4 Levels)

```typescript
// BAD -- 5 levels deep
function process(items) {
  if (items) {
    for (const item of items) {
      if (item.active) {
        if (item.type === 'premium') {
          if (item.balance > 0) { /* buried logic */ }
        }
      }
    }
  }
}

// GOOD -- flat with early returns and filtering
function process(items) {
  if (!items) return;
  const eligible = items.filter(i => i.active && i.type === 'premium' && i.balance > 0);
  for (const item of eligible) { /* top-level logic */ }
}
```

## Parameter Count (Max 4-5)

```typescript
// BAD -- 7 positional params
function createUser(name, email, role, team, avatar, locale, timezone) { ... }

// GOOD -- options object
interface CreateUserOptions {
  name: string; email: string; role: Role;
  team?: string; avatar?: string; locale?: string; timezone?: string;
}
function createUser(options: CreateUserOptions) { ... }
```

## Duplication Detection

If you copy-paste 3+ lines, extract a function. Duplicated code means duplicated bugs. Two functions that are 80% identical should share a parameterized helper.

## Enforcing with Tooling

```json
{
  "rules": {
    "complexity": ["error", 15],
    "max-lines-per-function": ["warn", { "max": 50, "skipBlankLines": true }],
    "max-depth": ["error", 4],
    "max-params": ["warn", 5],
    "max-lines": ["warn", { "max": 300 }]
  }
}
```

## Review Checklist

- [ ] No function exceeds cyclomatic complexity of 15
- [ ] Functions are under ~50 lines
- [ ] Files are under ~300 lines
- [ ] No nesting deeper than 4 levels
- [ ] Functions with 5+ parameters use an options object
- [ ] No copy-pasted blocks longer than 3 lines
