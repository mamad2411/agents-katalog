---
name: hook-lifecycle-execution
description: Load and execute YAML-defined lifecycle hooks with optional conditions and controlled timeouts.
---

# Hook Lifecycle Execution

Load and execute YAML-defined lifecycle hooks with optional conditions and controlled timeouts.

## When to Use

Use this skill when:

- Working with code in `src/hooks/index.ts/`
- User mentions "hooks"
- User mentions "pre-commit"
- User mentions "post-generate"
- User mentions "condition"
- User mentions "timeout"

## Patterns

- event-scoped hook discovery under .github/hooks
- execSync command execution with timeout
- file/command condition evaluation
- verbose output and early failure stop
- per-hook success/error aggregation

## Examples

```
const runner = new HookRunner(rootPath, verbose); await runner.execute('post-generate');
```

## Category

**reliability** - Error handling, recovery, and fault tolerance
