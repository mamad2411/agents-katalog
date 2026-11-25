---
name: validate
description: "Validate Agent Teams configuration in the current project. Use for debugging or verifying setup."
user-invocable: true
allowed-tools: Bash(npx:*), Read, Glob, Grep
---

# /validate

Validate Claude Code Agent Teams configuration in the current project.

## Usage

```bash
npx create-agent-system validate [target] [options]
```

Options:
- `--quiet, -q` — Show errors only (suppress warnings)

## Examples

```bash
# Validate current directory
npx create-agent-system validate

# Validate a specific directory
npx create-agent-system validate ./my-project

# Quiet mode (for CI)
npx create-agent-system validate --quiet
```

## Validation checks

### Errors (failure conditions)
- YAML frontmatter parsing failure
- Missing `name` field
- Missing `description` field
- Unsupported frontmatter fields used
- Invalid `model` value (must be opus, sonnet, haiku, or inherit)
- `skills` references pointing to non-existent directories
- CLAUDE.md `@import` paths pointing to non-existent files

### Warnings (non-blocking, improvement recommended)
- `description` too short (< 20 chars) or too long (> 1024 chars)
- Missing `tools` field (inherits all tools)
- Disabled agent files still present

## Interpreting results

- Errors present → exit code 1, configuration needs fixing
- Warnings only → exit code 0, works but improvements recommended
- All passing → summary of agent/skill counts displayed
