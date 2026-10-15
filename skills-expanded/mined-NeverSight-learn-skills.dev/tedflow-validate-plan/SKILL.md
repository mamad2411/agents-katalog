---
name: tedflow-validate-plan
description: Validate that a coding plan was correctly implemented by comparing plan phases, git evidence, code changes, tests, and success criteria. Use when the user asks to validate a plan, verify implementation, check completed work against a plan, audit plan execution, review whether success criteria are met, or confirm work is ready to finalize.
---

# Workflow Validate Plan

Use this skill to validate implementation against an approved plan.

## Inputs

Treat the user's current request as the input. If it does not include a plan path, locate the likely plan from recent context or ask for it.

## Preparation

1. Determine whether you have implementation context in the current conversation.
2. Read the plan completely.
3. Read project guidance when present: `AGENTS.md`, `CLAUDE.md`, `.claude/CLAUDE.md`, `.cursor/rules`, or equivalent docs.
4. Gather implementation evidence from conversation context, git status, git diff, recent commits, and changed files.
5. Use native subagents only when available and allowed. Otherwise inspect directly with `rg`, `fd`, `ast-grep`, file reads, and git commands.

## Validation Workflow

For each phase:

1. Check the phase completion status in the plan.
2. Identify planned files, behaviors, and success criteria.
3. Verify actual code matches the planned behavior.
4. Run every automated verification command listed in the plan.
5. If commands are missing or stale, infer the narrowest useful checks from project guidance and explain the substitution.
6. Assess manual verification criteria and list any items requiring human confirmation.
7. Look for edge cases, regressions, missing tests, and maintainability issues.

Be skeptical but practical. Focus on correctness, regressions, missing coverage, and mismatches between plan and implementation.

## Validation Report

Return a report shaped like:

```markdown
## Validation Report: [Plan Name]

### Implementation Status

- [status] Phase 1: [Name] - [summary]
- [status] Phase 2: [Name] - [summary]

### Automated Verification Results

- [status] `[command]` - [result]

### Code Review Findings

#### Matches Plan

- [Evidence with file:line reference]

#### Deviations From Plan

- [Deviation, impact, and whether it is acceptable]

#### Potential Issues

- [Issue, risk, and suggested fix]

### Manual Testing Required

- [ ] [Manual step]

### Recommendation

[Finalize, fix issues first, or request human testing.]
```

## Finalization Behavior

If automated validation passes and required manual verification is either confirmed by the user or explicitly accepted as pending:

1. If `tedflow-finalize-plan` is available, use it with the same plan path.
2. If skill-to-skill invocation is unavailable, follow the finalization workflow inline or ask whether to finalize now.

If manual verification is still required and the user has not confirmed or accepted it as pending, do not finalize yet. Report the manual testing steps and ask for confirmation.

If validation reveals issues:

- Do not finalize.
- Document failures clearly.
- Suggest specific fixes.
- Tell the user validation can be rerun after fixes.

## Checklist

Always verify:

- [ ] Completed phases are actually implemented.
- [ ] Automated checks pass or failures are explained.
- [ ] Code follows existing patterns.
- [ ] No obvious regressions were introduced.
- [ ] Error handling is robust enough for the scope.
- [ ] Documentation was updated when needed.
- [ ] Manual testing needs are clear.
