---
name: refactoring
description: Use when improving code structure, reducing duplication, or improving code quality without changing behavior.
tags: refactoring, code-quality, cleanup, improvement
---

# Refactoring Skill

Use this skill when refactoring code to improve structure, readability, or performance.

## Workflow

1. Understand current code: read and analyze the code to refactor
2. Identify refactoring opportunities: duplication, complexity, naming issues
3. Plan changes: determine safe refactoring steps
4. Execute incrementally: make small, safe changes
5. Verify behavior: run tests to ensure nothing breaks

## Common Refactorings

- **Extract Function**: Break large functions into smaller pieces
- **Rename**: Improve variable/function/class names for clarity
- **Remove Dead Code**: Delete unused code and imports
- **Simplify Conditionals**: Reduce complex boolean expressions
- **Move Method**: Relocate methods to more appropriate classes
- **Introduce Parameter Object**: Group related parameters

## Key Tools

- `workspace_read_file` - Read code to refactor
- `workspace_edit_at_hash` - Edit specific sections (safe)
- `workspace_apply_patch` - Apply larger changes
- `shell` - Run tests/linters

## Rules

- Keep changes focused and incremental
- Run tests after each significant change
- Use `workspace_edit_at_hash` for precise, reversible edits
- Verify no behavior change occurs
- Document significant refactorings in commit messages
- Follow project's code style (run formatter after changes)

## Safety Checklist

- [ ] All existing tests pass
- [ ] Linting passes
- [ ] Type checking passes
- [ ] Code compiles/builds successfully

## References

- See the common refactorings and safety checklist sections above for specific refactoring patterns.