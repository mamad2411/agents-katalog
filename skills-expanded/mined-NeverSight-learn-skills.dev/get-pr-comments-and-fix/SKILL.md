---
name: get-pr-comments-and-fix
description: Triage and address unresolved PR review comments. Fixes clear issues (commit + reply), dismisses false findings (reply with reasoning), and surfaces uncertain items for human review. Use when the user wants to fix PR comments, address review feedback, resolve PR threads, or handle Copilot reviewer suggestions. This extends the get-pr-comments skill by also acting on comments rather than just summarizing them.
---

# Get PR Comments and Fix

Extends `get-pr-comments` — instead of just fetching and summarising, this skill also acts on the comments: fixing code, dismissing false positives, and surfacing ambiguous items for human judgment.

## Prerequisites

Read `project-context/SKILL.md` first if you haven't already — it has branch naming conventions, commit message format, and architecture context that helps you make better triage decisions.

## Trigger

User wants to act on unresolved review comments from a pull request. Typical invocations:

- `/get-pr-comments-and-fix` (uses current branch's PR)
- `/get-pr-comments-and-fix https://github.com/org/repo/pull/123`

## Workflow

### 1. Resolve the PR

- If a URL is provided, extract owner/repo/number.
- Otherwise, detect the PR from the current branch:
  ```
  gh pr view --json number,url,headRefName,baseRefName
  ```

### 2. Fetch unresolved comments only

Use the GraphQL API to get review threads with resolution status:

```
gh api graphql -f query='{
  repository(owner: "<owner>", name: "<repo>") {
    pullRequest(number: <number>) {
      reviewThreads(first: 50) {
        nodes {
          isResolved
          id
          comments(first: 10) {
            nodes {
              id databaseId body author { login }
              path line originalLine diffHunk
              url
            }
          }
        }
      }
    }
  }
}'
```

Filter to `isResolved: false` threads only. Capture the thread `id` and each comment's `url` — you'll need these for commit messages and replies.

### 3. Read affected files

For every unresolved comment, read the current version of the affected file to understand the actual state of the code. Also check `git log` / `git show` for the old version when needed to verify whether a reviewer's claim about behavioural regression is accurate.

Also read `project-context/SKILL.md` → "Intentional patterns" section. This helps you distinguish between patterns that are architectural decisions vs. actual issues the reviewer is flagging.

### 4. Triage each comment

Categorise every unresolved comment into exactly one bucket:

| Category | Criteria | Action |
|----------|----------|--------|
| **Fixable** | Clear bug, valid defensive fix, or confirmed regression | Fix, commit, push, reply on PR |
| **False finding** | Reviewer is factually wrong or the concern doesn't apply | **Present to user for approval**, then reply on PR |
| **Uncertain** | Reasonable concern but debatable, needs human judgement | Present to user — do NOT comment on PR |

**Deciding between buckets:**

- *Fixable*: You can verify the issue by reading the code and you are confident the fix is correct and low-risk. "No-brainer" fixes.
- *False finding*: You can prove the reviewer is wrong (e.g. the code already handles the case, the concern is about dead code, or the suggested change would break something).
- *Uncertain*: The reviewer might be right but the fix has trade-offs, touches architecture, or you're unsure whether the reviewer or the current code is correct.

### 5. Execute fixes (Fixable bucket)

For each fixable comment, in a sensible implementation order:

1. **Fix** the code.
2. **Commit** with a message that references the PR comment thread so reviewers can trace which commit addresses which comment:
   ```
   fix: <concise what>

   <why this change is needed — reference the concern>

   Addresses: <comment URL>
   ```
3. **Push** after all fixable commits are done (single push).
4. **Reply** on the PR thread. The reply must describe the change and why it was made. Keep it concise — one or two sentences. Example:
   > Fixed — `useBranches` now accepts an `enabled` option so callers can gate the query, preventing unnecessary fetches when the modal is closed.

### 6. Present false findings for approval

Telling a reviewer they're wrong is high-stakes — a poorly worded dismissal can damage team dynamics. Instead of posting directly, present each false finding to the user first:

```
## False findings — awaiting your approval to reply

### <file>:<line> — <short summary>
**Reviewer says:** <paraphrase>
**Why this is a false finding:** <your analysis with evidence>
**Proposed reply:**
> Not an issue — [explanation]

Approve this reply? (yes / edit / skip)
```

Only post the reply after the user approves or edits it.

### 7. Present uncertain items (Uncertain bucket)

Do NOT comment on the PR. Instead, present these to the user in a structured format:

```
## Needs your input

### <file>:<line> — <short summary>
**Reviewer says:** <paraphrase>
**My analysis:** <your assessment, including why you're unsure>
**Options:**
1. <option A — with trade-offs>
2. <option B — with trade-offs>
```

### 8. Final summary

End with a table summarising everything:

| # | File | Comment | Category | Action taken |
|---|------|---------|----------|--------------|
| 1 | `file.ts` L42 | description | Fixable | Committed: `abc1234` |
| 2 | `file.ts` L78 | description | False finding | Awaiting your approval |
| 3 | `other.ts` L15 | description | Uncertain | Awaiting your input |

## Commit message rules

Every commit message must:
- Start with a conventional prefix (`fix:`, `refactor:`, `chore:`, etc.)
- Describe WHAT changed in the subject line
- Explain WHY in the body (reference the reviewer concern)
- Include the comment URL in an `Addresses:` footer line so the reviewer can trace the fix back to their comment
- Be concise — one subject line + one short paragraph body

## PR reply rules

Every reply on a PR comment must:
- Start with "Fixed —" (for fixes) or a clear stance (for dismissals)
- Describe the change and WHY, not just "done"
- Be concise — one to two sentences max

## End of response

Always finish with two suggested commit messages (short + long) for the overall batch, per the user's workspace rule. Do not auto-push to remote unless explicitly asked.
