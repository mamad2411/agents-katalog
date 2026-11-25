---
name: pr-review-actioner
description: >
  Action GitHub pull request review feedback. Use when the user wants to
  address PR review comments, respond to code review feedback, fix review
  issues, or says things like "action the review", "address feedback",
  "handle review comments", or "go through the PR comments". Fetches all
  unresolved review threads, triages each as actionable or not, implements
  fixes, and replies with rationale where not actioning.
compatibility: Requires gh CLI, git, an authenticated GitHub session, and a clean PR branch.
---

# PR Review Actioner

Go through unresolved PR review comments, fix what should be fixed, and reply to the rest with a rationale.

## Prerequisites

1. `gh` CLI is installed and authenticated
2. Current directory is a git repository with the PR branch checked out
3. Working tree is clean (no uncommitted changes)

## Workflow

### 1. Find the PR

Detect the PR from the current branch:

```bash
gh pr view --json number,url,headRefName,baseRefName
```

If no PR is found, ask the user for a PR number or URL, then use:

```bash
gh pr view <number> --json number,url,headRefName,baseRefName
```

### 2. Fetch unresolved review threads

Use GraphQL pagination to get review threads with their resolution status:

```bash
number=$(gh pr view --json number --jq '.number')
owner=$(gh repo view --json owner --jq '.owner.login')
repo=$(gh repo view --json name --jq '.name')

gh api graphql --paginate -f query='
  query($owner: String!, $repo: String!, $number: Int!, $endCursor: String) {
    repository(owner: $owner, name: $repo) {
      pullRequest(number: $number) {
        reviewDecision
        url
        reviewThreads(first: 100, after: $endCursor) {
          nodes {
            id
            isResolved
            isOutdated
            path
            line
            startLine
            diffSide
            comments(first: 10) {
              nodes {
                id
                databaseId
                body
                author {
                  login
                }
                createdAt
              }
              pageInfo {
                hasNextPage
                endCursor
              }
            }
          }
          pageInfo {
            hasNextPage
            endCursor
          }
        }
      }
    }
  }
' -F owner="$owner" -F repo="$repo" -F number="$number" --jq '.'
```

Filter to threads where `isResolved` is `false`. Do not silently skip outdated unresolved threads. If `isOutdated` is `true`, triage the thread as `Already addressed` when the current code proves the concern was fixed, or as `Needs validation` when the current code still needs review before replying or resolving.

If any thread has `comments.pageInfo.hasNextPage: true`, fetch the remaining comments for that thread before triaging it. Do not silently triage from a partial comment chain.

Use this follow-up query for a specific review thread when the initial thread query returns a partial comment chain:

```bash
thread_id="PRRT_..."

gh api graphql --paginate -f query='
  query($threadId: ID!, $endCursor: String) {
    node(id: $threadId) {
      ... on PullRequestReviewThread {
        comments(first: 100, after: $endCursor) {
          nodes {
            id
            databaseId
            body
            author {
              login
            }
            createdAt
          }
          pageInfo {
            hasNextPage
            endCursor
          }
        }
      }
    }
  }
' -F threadId="$thread_id" --jq '.'
```

If there are no unresolved threads, report that and stop.

### 3. Triage each thread

For each unresolved thread:

1. **Read the comment chain** — understand what the reviewer is asking for
2. **Read the code** — look at the file and line(s) referenced by the thread
3. **Classify** as one of:

| Classification | When to use | Action |
|---------------|-------------|--------|
| **Actionable** | Valid code change: bug fix, style improvement, naming, logic correction, missing edge case, requested refactor | Fix the code |
| **Question** | Reviewer is asking for clarification, not requesting a change | Reply with an explanation |
| **Disagree** | The suggestion would make the code worse, contradicts project conventions, or is out of scope | Reply with rationale |
| **Already addressed** | The issue was fixed in a subsequent commit but the thread wasn't resolved | Reply noting which commit addressed it |
| **Needs validation** | The thread is outdated or ambiguous and the current code must be checked before deciding | Read current code, then reclassify as actionable, already addressed, question, or disagree |

**Important:** Do not blindly agree with every comment. Evaluate each on its merits. A good response to feedback requires technical rigour — if a suggestion is wrong or counterproductive, say so respectfully.

### 4. Present triage for confirmation

Before making any changes or posting any replies, present the full triage to the user:

```
## PR Review Triage — #123

### Will action (3)
1. `src/auth.ts:42` — @reviewer: "Missing null check on user.email"
   → Add null check before accessing email
2. `src/api.ts:15` — @reviewer: "This should return 404 not 500"
   → Change error status code to 404
3. `src/utils.ts:8` — @reviewer: "Rename to parseUserInput"
   → Rename function

### Will reply (1)
1. `src/auth.ts:78` — @reviewer: "Consider using a guard clause here"
   → Reply: "Keeping the if/else structure as it handles the error
   logging path which would be lost with an early return."
```

Wait for the user to confirm or adjust before proceeding.

### 5. Fix actionable comments

For each actionable item:

1. Read the file
2. Make the fix
3. Do not stage yet; keep the working tree available for review

After all fixes are made:

```bash
git status --short
git diff
```

Present the final diff and ask the user for explicit confirmation before staging, committing, or pushing. When confirmed, stage only agent-owned changes. Prefer `git add -p` for mixed files; use explicit file paths only when each whole file belongs to the fix.

```bash
git add path/to/changed-file
git commit -m "fix: address PR review feedback"
```

Ask separately before pushing if the user did not already approve publishing the commit:

```bash
git push
```

### 6. Reply to non-actionable comments

For each thread where you're not making a code change, post a reply:

```bash
top_comment_database_id=123456789
gh api "repos/$owner/$repo/pulls/$number/comments" \
  -X POST \
  -f body="Keeping this as-is — the if/else structure handles the error logging path which would be lost with an early return. Happy to discuss further." \
  -F in_reply_to="$top_comment_database_id"
```

`in_reply_to` must be the `databaseId` of the **first comment** in the thread (the top-level review comment that started the thread). Alternatively, use the dedicated reply endpoint:

```bash
gh api "repos/$owner/$repo/pulls/$number/comments/$top_comment_database_id/replies" \
  -X POST \
  -f body="Keeping this as-is — the if/else structure handles the error logging path which would be lost with an early return. Happy to discuss further."
```

**Reply tone guidelines:**
- Be specific — reference the code, not just "I disagree"
- Be respectful — "Keeping this because X" not "That's wrong"
- Be open — end with "Happy to discuss" or "Let me know if you'd prefer a different approach"
- Be concise — 1-3 sentences is ideal

### 7. Report summary

After all fixes and replies are done, present a summary:

```
## Done — PR #123

- **Actioned:** 3 comments (committed as abc1234)
- **Replied:** 1 comment
- **PR:** https://github.com/org/repo/pull/123
```

## Edge cases

- **Large threads** — if a thread has many back-and-forth replies, read the entire chain to understand the full context before triaging
- **Conflicting feedback** — if two reviewers give contradictory feedback, flag it to the user rather than picking one
- **Suggested code blocks** — GitHub review comments can include code suggestions; apply these directly when actioning
- **Files not in working tree** — if a comment references a file that doesn't exist locally (e.g. deleted or renamed), note this in the triage
