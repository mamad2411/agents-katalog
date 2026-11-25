---
name: address-review
version: 1.0.0
description: Address PR review comments and request re-review
uses:
  - development/git
  - core/memory
requires:
  tools: [git, gh]
  env: []
security:
  risk_level: write
  capabilities:
    - git:read
    - git:write
    - github:pr:read
    - github:pr:comment
  requires_approval: false
---

# Address Review Comments

Respond to PR review feedback by fixing issues, replying to comments, and requesting re-review. This skill handles the developer side of the review cycle.

**Platform note**: This skill currently uses GitHub (`gh` CLI). The methodology is platform-agnostic; only the tool commands are GitHub-specific.

## Execution Model

This is a **bash skill** (`handler: type: bash`). When `pr_comments` is invoked, the executor runs `gh pr view {number} --json reviews,comments` to fetch review data. The agent then applies the methodology below to address each comment. The tool schema in tool.yaml defines the external contract; the executor handles the GitHub CLI call directly.

## When to Use

- When `review_completed` message arrives with comments to address
- When a reviewer requested changes on your PR
- After receiving inline comments on code

## Methodology

### 0. Claim Task

The task is in `changes_requested` status with no owner (the reviewer's handoff released ownership).

1. Extract `task_id` from the `review_completed` bus message payload
2. Claim: `POST /tasks/{task_id}/claim` with body `{"agent_id": "your-name"}`
3. If 409 → another agent already claimed it, skip

### 1. Understand the Feedback

Fetch all review comments and categorize each:

| Category | Criteria | Action |
|----------|----------|--------|
| **Blocking** | Security issues, bugs, broken functionality | Must fix before merge |
| **Suggestions** | Code quality, style, better approaches | Should consider |
| **Questions** | Clarification requests | Must answer |

### 2. Address Each Comment

For each blocking issue:
1. **Understand** what the reviewer is asking
2. **Fix** the code
3. **Reply** to the comment explaining what you changed and why

For suggestions:
- If you agree: implement and reply
- If you disagree: explain your reasoning respectfully

For questions:
- Answer clearly and specifically

### 3. Commit Changes

After addressing all comments:
1. Run tests to verify fixes don't break anything
2. Stage only the files you changed
3. Commit with a message referencing the review feedback
4. Push to the PR branch

### 4. Request Re-Review

Post a summary comment on the PR listing:
- Blocking issues fixed (with brief description of each fix)
- Suggestions implemented
- Questions answered
- Any comments you disagreed with and why

### 5. Move to Review (auto-releases ownership for reviewer)

`POST /tasks/{task_id}/status?new_status=review&agent_id={your-id}`

This transition has `handoff: true` — your `agent_id` is cleared so a reviewer can claim the task.

### 6. Notify via Bus

Publish a `review_request` message so the reviewer knows to re-review.

## Output Format

```
## Review Response

### Comments Addressed
| # | Category | Comment | Resolution |
|---|----------|---------|------------|
| 1 | Blocking | [summary] | Fixed — [what was changed] |
| 2 | Suggestion | [summary] | Implemented / Declined (reason) |
| 3 | Question | [summary] | Answered |

### Changes Made
- [file]: [what changed]

### Commit
- Message: [commit message]
- Files: [count] files changed

### Re-Review
- Status: Requested
```

## Quality Criteria

- All blocking issues are addressed (not ignored)
- All comments have replies (no unanswered comments)
- Changes are tested before committing
- Commit message references the review feedback
- Re-review is requested with a summary of changes
- Disagreements are explained respectfully with reasoning

## Common Mistakes

- **Ignoring comments**: Not replying to a comment, even if you think it's wrong. Every comment deserves a response.
- **Dismissing feedback without explanation**: If you disagree, explain why. "I don't think so" is not sufficient.
- **Not testing after fixes**: Fixing review comments can introduce new bugs. Always run tests before committing.
- **Committing everything at once**: If addressing multiple review comments, consider separate commits per comment for clarity.
- **Not requesting re-review**: The reviewer won't know you've addressed their feedback unless you explicitly request re-review.
- **Getting defensive**: Review comments are about the code, not about you. Accept feedback professionally.

## Completion

Addressing review comments is complete when:
- All blocking issues are fixed
- All comments have replies
- Changes are committed and pushed
- Re-review is requested with a summary
- Bus notification is published
