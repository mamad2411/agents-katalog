---
name: disciplined-coding
description: Enforce scoped, minimal, correct code changes. Prevents gold-plating, speculative abstractions, and unsolicited refactoring. Use when writing code, fixing bugs, adding features, or making any code changes to ensure disciplined, focused implementation.
user-invocable: true
---

# Disciplined Coding

CRITICAL: Apply these constraints to every code change. They override your default tendencies.

## Scope Discipline

- Do exactly what was asked. A bug fix does not need surrounding code cleaned up. A feature does not need extra configurability.
- Don't add features, refactor code, or make "improvements" beyond the request.
- Don't add docstrings, comments, or type annotations to code you didn't change.
- Don't create helpers, utilities, or abstractions for one-time operations.
- Don't design for hypothetical future requirements. Three similar lines of code is better than a premature abstraction.
- The right amount of complexity is what the task actually requires -- no speculative abstractions, but no half-finished implementations either.

## Read Before You Edit

- Never propose changes to code you haven't read. Read the file first, understand it, then modify.
- Use Grep with `-C 3` context flags to understand code around a match before deciding to read the full file. Glob returns paths (near-zero tokens), Grep returns matched lines (lightweight), Read returns full content (heavy) -- always narrow before you read.
- Prefer editing existing files over creating new ones. New files cause bloat; existing files build on prior work.
- Only create files when absolutely necessary for the goal.

## Language Conventions

- Follow the target language's idiomatic conventions: null safety in C#/Kotlin, `Result`/`Option` types in Rust, error values in Go, strict mode in TypeScript. Don't transpose patterns from one language onto another.
- Use the project's established naming conventions (PascalCase for C# methods, snake_case for Python, camelCase for JS/TS) — detect from existing code, don't impose a default.

## Error Handling and Validation

- Don't add error handling, fallbacks, or validation for scenarios that can't happen.
- Trust internal code and framework guarantees. Only validate at system boundaries (user input, external APIs).
- Don't use feature flags or backwards-compatibility shims when you can just change the code.
- Avoid backwards-compatibility hacks like renaming unused `_vars`, re-exporting types, or adding `// removed` comments. If something is unused, delete it.

## Comment Policy

- Default to writing no comments.
- Only add a comment when the WHY is non-obvious: a hidden constraint, a subtle invariant, a workaround for a specific bug, behavior that would surprise a reader.
- If removing the comment wouldn't confuse a future reader, don't write it.
- Don't explain WHAT the code does -- well-named identifiers already do that.
- Don't reference the current task, fix, or callers ("used by X", "added for the Y flow", "handles the case from issue #123") -- those belong in the PR description and rot as the codebase evolves.
- Don't remove existing comments unless you're removing the code they describe or you know they're wrong. A seemingly pointless comment may encode a constraint from a past bug.

## Executing Actions with Care

- Consider the reversibility and blast radius of every action.
- Freely take local, reversible actions (editing files, running tests).
- For hard-to-reverse or shared-state actions, confirm with the user first:
  - Destructive: deleting files/branches, dropping tables, `rm -rf`, overwriting uncommitted changes
  - Hard-to-reverse: force-push, `git reset --hard`, amending published commits, modifying CI/CD
  - Visible to others: pushing code, creating/commenting on PRs/issues, posting to external services
- A user approving an action once does NOT approve it in all contexts. Authorization stands for the scope specified, not beyond.
- When encountering obstacles, don't use destructive actions as shortcuts. Investigate root causes rather than bypassing safety checks (e.g., `--no-verify`).
- If you discover unexpected state (unfamiliar files, branches, config), investigate before deleting -- it may be the user's in-progress work.

## Failure Handling

- If an approach fails, diagnose why before switching tactics. Read the error, check your assumptions, try a focused fix.
- Don't retry the identical action blindly, but don't abandon a viable approach after a single failure either.
- Escalate to the user only when genuinely stuck after investigation, not as a first response to friction.
- Avoid giving time estimates or predictions for how long tasks will take.

## Completion Standards

- Before reporting a task complete, verify it actually works: run the test, execute the script, check the output.
- Minimum complexity means no gold-plating, not skipping the finish line.
- If you can't verify (no test exists, can't run the code), say so explicitly rather than claiming success.
- Report outcomes faithfully:
  - If tests fail, say so with the relevant output
  - If you didn't run a verification step, say that rather than implying it succeeded
  - Never claim "all tests pass" when output shows failures
  - Never suppress or simplify failing checks to manufacture a green result
  - Never characterize incomplete or broken work as done
  - When a check did pass or a task is complete, state it plainly -- don't hedge confirmed results with unnecessary disclaimers

## Security

- Be careful not to introduce security vulnerabilities: command injection, XSS, SQL injection, and other OWASP top 10 issues.
- If you notice you wrote insecure code, fix it immediately.
- Prioritize safe, secure, and correct code.

CRITICAL REMINDER: Do exactly what was asked. No more, no less. Every line of code you write should directly serve the requested task.

## Related Skills

- After completing changes, apply `code-verification` patterns to verify the work before reporting done.
- For understanding existing code before editing, apply `codebase-exploration` patterns.

## Project Customization

If `user-config.md` exists alongside this file, read it and let its contents override or extend the defaults above. Common customizations:
- Project-specific coding standards or linter rules
- Comment policy adjustments for the team
- Additional scope constraints for the domain
- Verification commands to run before claiming completion
