---
name: f5-shared-patterns
description: Shared reference patterns used across F5 skills
category: shared
allowed-tools: Read, Write, Glob, Grep, Bash
user-invocable: false
context: inject
---

# F5 Shared Patterns

Common patterns referenced by multiple skills and commands.

## Contents

- [Test Patterns](./test-patterns.md) - Common testing patterns
- [Security Patterns](./security-patterns.md) - Security best practices
- [API Patterns](./api-patterns.md) - API design patterns

## Usage

These patterns are referenced by specialized skills.
Load specific patterns when needed:

```
See: .claude/skills/_shared/test-patterns.md
See: .claude/skills/_shared/security-patterns.md
See: .claude/skills/_shared/api-patterns.md
```

## When to Use

- **Test Patterns**: When writing unit/integration/e2e tests
- **Security Patterns**: When implementing authentication, authorization
- **API Patterns**: When designing REST/GraphQL APIs

## Related Skills

- `.claude/skills/testing/` - Detailed testing strategies
- `.claude/skills/security/` - Security implementations
- `.claude/skills/api-design/` - API design patterns
