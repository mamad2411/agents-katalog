---
name: python-dead-code
description: >-
  Run vulture to detect dead code in Python projects, then carefully evaluate
  each finding before acting. Use this skill whenever the user asks to find
  unused code, dead code, or unreachable code in Python. Also trigger when the
  user mentions vulture, cleanup, or removing unused functions, classes, or
  variables. This skill enforces extreme caution — only remove code the agent
  is 100% confident is unused.
compatibility:
  - uv
  - vulture
---

# Python Dead Code Detection

Use this skill to run `vulture` on Python projects, critically evaluate each finding, and either remove confirmed dead code or report uncertain findings for user review.

## Prerequisites

- Project uses `uv` for dependency management
- `vulture` is installed in the environment
- If missing, stop and inform the user — do not attempt to install it

## Commands

### Whole project

```bash
uv run vulture .
```

### Specific directory or file

```bash
uv run vulture <path>
```

## How to evaluate findings

Vulture is heuristic and produces false positives. Before acting on any finding, verify it is truly unused:

1. **Search for dynamic references** — grep for the symbol name as a string (e.g., dynamically invoked methods, framework entry points, plugin hooks).
2. **Check for framework-managed code** — functions or classes referenced by decorators, configuration files, or external tools may not appear in static analysis.
3. **Look for import-side effects** — a module may be imported solely for side effects, making its contents appear unused.
4. **Review conditional or runtime paths** — code guarded by environment variables, feature flags, or runtime conditions may not be detected.

## Rules

- **100% confidence required.** Only remove code you are absolutely sure is unused. When in doubt, leave it and report the finding.
- **Never remove code based solely on vulture output.** Always cross-reference with the codebase using grep and file reads.
- **Report uncertain findings.** Mark any vulture result you cannot confirm as dead code in a summary report for the user to review.
- **Preserve public APIs.** Do not remove functions, classes, or modules that could be part of a public interface, even if unused internally.
- **One finding at a time.** Evaluate each result individually to avoid cascading false positives.

## Example workflow

```bash
# 1. Run vulture
uv run vulture .

# 2. For each finding, verify it is truly unused
#    - grep for the symbol name across the codebase
#    - check for dynamic references, framework hooks, etc.

# 3. Remove confirmed dead code
#    (use edit tool to remove verified unused code)

# 4. Report uncertain findings for user review
```

## Report format

After evaluation, provide a summary:

```
## Dead Code Report

### Removed (confirmed unused)
- `module.function` — no references found, not a framework entry point

### Uncertain (requires user review)
- `module.handler` — vulture flags as unused, but may be invoked dynamically via config
```
