---
name: code-review-agent
description: prompt to dispatch subagent to review code implementation
---

Use the following template to dispatch a subagent to review code implementation.

Ensure information is pasted in the prompt, do not reference files:

```markdown
You are reviewing a set of commits to assess code quality, maintainability and architecture.

# Task description:

[FULL TEXT of task from plan]

# What was implemented:

[FULL TEXT of execution report]

# Worktree

The implementation lives in a dedicated git worktree at: `[WORKTREE_PATH]`

Run git diff and explore files inside this directory.

# Your goal

Use `git diff` to review the code implemented, considering the base and head commits:

**Base:** [commit SHA for latest changes made by the agent — in the worktree]
**Head:** [commit SHA for head commit where the agent started — in the worktree]

If more context is needed, explore related files outside of the commit, but do not consider them as part of your review.

## What to check

**Code quality**

- Clean separation of responsibilities/concerns
- Error handling with proper actions
- DRY
- Premature optimizations/abstractions
- Edge cases
- Type safety (when applicable)
- Breaking type changes: if a shared type was modified, verify callers still compile and no implicit contracts were silently broken

**Testing**

- Tests validate behavior, not mocked implementation
- Edge cases are covered by dedicated tests
- Integration points are tested, using mocks or stubs when needed
- New tests do not overlap with existing tests cases
- All tests pass and no regression issues are found

**Architecture**

- Design decisions can reasonably scale and perform well
- Existing patterns and conventions are followed
- No security concerns

## Additional checks

- **File responsibility**: Does each file have one clear responsibility with a well-defined interface?
- **Unit decomposition**: Are units decomposed so they can be understood and tested independently?
- **Plan alignment**: Is the implementation following the file structure from the plan?
- **Size impact**: Did this implementation create new files that are already large, or significantly grow existing files? (Don't flag pre-existing file sizes — focus on what this change contributed.)

## Hygiene

- **Dead code**: unused types, variables, imports, or functions introduced by this change (run the language's linter or type checker with unused-symbol detection)
- **Ephemeral references**: comments, TODOs, or strings referencing local plan files, session paths, or agent-internal artifacts — these must not be committed

## Report format

Return: Strengths, Issues (Critical/Important/Minor), Assessment
```
