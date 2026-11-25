---
name: gh-open-pr
description: Create or update GitHub pull requests with issue links, plan context, and safe closing triggers.
---

# gh-open-pr

## Purpose

Create or update a GitHub pull request after the caller has prepared the complete change or plan set.
Use a draft PR for a plan-set handoff. Use a ready PR only when the caller explicitly requests it
or the implementation workflow has completed its verification gates.

## Preconditions

- Confirm the repository and base branch from Git, not from memory.
- Confirm the head branch is pushed and the PR source is the intended branch.
- For a plan PR, confirm every split plan has been created and linked to the parent Issue.
- For a plan PR, confirm every child Issue has the configured `Planned` status.
- Do not create a PR in `local-markdown` tracker mode.
- If the head branch has no commits beyond the base branch, report that GitHub cannot create the PR yet.

## Core Rules

- Use `gh pr create` for a new PR and `gh pr edit` for an existing PR.
- Never merge or close a PR. The user owns the final merge or close decision.
- Prefer `--draft` for a plan-set PR.
- Use `--body-file` for multi-section bodies; do not place long Markdown in shell quoting.
- When automatic closing is required, state it on one line at the bottom of the PR body.
- Recommended phrases: `Closes #123`, `Fixes #123`, `Resolves #123`
- Use `#123` for issues in the same repository.
- Put one closing trigger on each line when closing multiple issues.
- Never add a closing trigger to a plan PR: planning does not complete implementation Issues.
- Do not add a closing trigger when the issue must remain open.
- Do not rely on the title; include the trigger in the body.
- Never close or change Issue or Project status as a side effect of PR creation.

## Plan PR Body

For a plan-set PR, use this order:

1. State that the PR contains the approved implementation plan set.
2. Link the parent Issue and every child Issue.
3. Summarize dependencies and execution order.
4. Link the Product Spec and Architecture Spec, including class and state diagrams.
5. Record the planning validation performed.
6. State that implementation and completion gates remain pending.

```md
## Plan Set
- Parent: #123
- Child plans: #124, #125

## Execution Order
1. #124 — prerequisite
2. #125 — depends on #124

## Specifications
- Product Spec: `docs/specs/<ticket-id>/product-spec.md`
- Architecture Spec: `docs/specs/<ticket-id>/architecture-spec.md`
- Class diagram: `<link or heading>`
- State diagram: `<link or heading>`

## Planning Validation
- All split plans approved and created.
- Dependencies and tracker statuses verified.

## Remaining Work
- Implementation, verification, and completion remain pending.
```

Do not add `Closes`, `Fixes`, or `Resolves` to this body.

## Implementation PR Body

1. Confirm the linked Issue number and repository scope.
2. Write a title that makes the implementation intent clear.
3. Add the problem, change flow, and test or verification results.
4. Include a Mermaid diagram when it materially clarifies the change flow.
5. Put the closing line at the bottom only when the Issue should close after merge.
6. Confirm that the closing phrase targets the intended Issue.

## Body Example

```md
## Implementation Intent / Problem
- Implement comment creation for authenticated users.
- Fix unauthenticated access to the comment creation API.

## Change Flow
- On login, `loginService` validates the username/password match, then `TokenProvider` issues an access token.


```mermaid
```

## Verification
- Confirmed successful comment creation through `Postman` after login.

Closes #123
```

## Commands

Use the configured repository and current branch:

```bash
gh pr create --draft --base <base-branch> --head <head-branch> \
  --title "<title>" --body-file <body-file>
```

If a PR already exists for the head branch:

```bash
gh pr edit <number> --title "<title>" --body-file <body-file>
```

## User-Owned Finalization

This skill stops after creating or updating the PR. The user decides whether to:

- mark a draft PR ready
- merge the PR
- close the PR without merging

Do not run `gh pr merge`, `gh pr close`, or an equivalent API operation.

## Notes

- Automatic closing usually occurs when the PR merges into the default branch.
- Use the correct repository qualifier for issues in another repository.
- Do not leave a closing trigger on a plan PR or an Issue that should remain open.
