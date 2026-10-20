---
name: branch-completion
description: Use when implementation is complete, all tests pass, and you need to decide how to integrate the work - guides completion of development work by presenting structured options for merge, PR, or cleanup
---

# Finishing a Development Branch

## Core Principle

## Trigger Conditions

Invoke this skill when any of the following is true:

- Implementation work is complete and all tests pass.
- A decision is needed on how to integrate a development branch (merge, PR, or discard).
- A prompt to the user for integration path selection is required.

## Core Principle

Verify tests, present structured options, execute exactly one path, then apply cleanup rules.

## Required Prompt to User

Present exactly these options:

```text
Implementation complete. What would you like to do?

1. Merge back to <base-branch> locally
2. Push and create a Pull Request
3. Keep the branch as-is (I'll handle it later)
4. Discard this work

Which option?
```

## Preconditions

- Run project test command before offering options.
- If tests fail, stop and report failures.
- Determine base branch using merge-base or explicit user confirmation.

## Decision Matrix

| Option | Primary Action | Command Sequence | Must Re-Test | Branch Cleanup | Worktree Cleanup |
|---|---|---|---|---|---|
| 1 | Merge into base locally | `git checkout <base>; git pull; git merge <feature>; <test-command>; git branch -d <feature>` | Yes | Delete feature branch after pass | Yes |
| 2 | Push branch and open PR | `git push -u origin <feature>; gh pr create --title "<title>" --body "<summary-and-test-plan>"` | No | Keep branch | Yes |
| 3 | Keep branch unchanged | No git mutation commands; report branch/worktree retained | No | Keep branch | No |
| 4 | Discard branch | Confirm token; `git checkout <base>; git branch -D <feature>` | No | Force-delete after explicit confirmation | Yes |

## Confirmation Rule for Option 4

Before deletion, require an explicit typed confirmation token:

```text
Type 'discard' to confirm permanent deletion.
```

## Safety Rules

- Do not proceed with failing tests.
- Do not force-push unless explicitly requested.
- Do not delete worktree for Option 3.
- Do not delete branch for Option 4 without typed confirmation.

## Required Inputs

- Current branch and expected base branch.
- Test command and current pass/fail status.

## Required Outputs

- Selected completion path and execution result.
- Explicit statement of branch/worktree post-state.

## Workflow

1. Verify tests.
2. Confirm base branch.
3. Present four options.
4. Execute chosen option using matrices.
5. Apply cleanup rules and report final state.
