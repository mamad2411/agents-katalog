---
name: address-gemini-review
description: Pull recent GitHub PRs and address Gemini code review comments — fix the code, resolve the threads, and re-trigger Gemini. Use this skill when the user wants to check PR reviews, fix Gemini feedback, resolve review comments, or address code review suggestions on their GitHub PRs. Also use when the user says "check PR comments", "fix review feedback", "address reviews", "what did Gemini say", or "resolve gemini comments".
---

# Address Gemini Code Review

This skill fetches recent GitHub PRs from `devanfer02/telnetquiz-cms`, reads Gemini code review
comments, addresses them by making fixes, resolves the review threads, and re-triggers Gemini
to review the new changes.

## Repository

- **GitHub**: `devanfer02/telnetquiz-cms`
- **CLI**: All operations use `gh` CLI

## Workflow

### Step 1: Fetch Recent PRs

List recent open PRs:

```bash
gh pr list --repo devanfer02/telnetquiz-cms --limit 10
```

List recently merged PRs:

```bash
gh pr list --repo devanfer02/telnetquiz-cms --state merged --limit 10
```

Show a specific PR's details:

```bash
gh pr view <PR_NUMBER> --repo devanfer02/telnetquiz-cms
```

### Step 2: Fetch Review Threads via GraphQL

Use GraphQL to get review threads — this gives you the thread IDs needed to resolve them later,
along with the comment content and author info in a single call:

```bash
gh api graphql -f query='
  query($number: Int!) {
    repository(owner: "devanfer02", name: "telnetquiz-cms") {
      pullRequest(number: $number) {
        reviewThreads(first: 100) {
          nodes {
            id
            isResolved
            path
            line
            comments(first: 10) {
              nodes {
                id
                body
                author { login }
                createdAt
              }
            }
          }
        }
      }
    }
  }' -F number=<PR_NUMBER>
```

Also fetch REST review comments if you need diff hunks (GraphQL threads don't include them):

```bash
gh api repos/devanfer02/telnetquiz-cms/pulls/<PR_NUMBER>/comments \
  --jq '[.[] | select(.user.login == "gemini-code-assist")] | .[] | {id, path, line, body, diff_hunk}'
```

### Step 3: Filter Gemini Comments

Gemini code review comments come from the `gemini-code-assist` bot account. Filter by:

- `author.login == "gemini-code-assist"` (GraphQL) or `user.login == "gemini-code-assist"` (REST)
- The comment body includes severity badges like `![high]`, `![medium]`, `![low]`, `![critical]`

When parsing comments, extract:
- **Thread ID** (`id` field from GraphQL `reviewThreads.nodes`) — needed for resolving
- **File path** (`path` field) — which file the comment is on
- **Line number** (`line` field) — which line
- **Body** (`body` field from comments) — the actual review feedback
- **Severity** — parsed from the badge image in the body: `high-priority`, `medium-priority`, `low-priority`, `critical`
- **isResolved** — skip threads that are already resolved

### Step 4: Categorize and Prioritize

Group unresolved Gemini comments by severity and type:

| Priority | Types | Action |
|----------|-------|--------|
| **P0 — Fix now** | Bugs, security issues, crashes | Fix immediately |
| **P1 — Should fix** | Performance, error handling, logic issues | Fix in this PR |
| **P2 — Consider** | Style, naming, minor improvements | Fix if quick, else note for later |
| **P3 — Optional** | Nitpicks, suggestions, alternatives | Acknowledge, skip if not valuable |

### Step 5: Address Each Comment

For each comment that needs action:

1. **Read the file** at the referenced path and line
2. **Understand the suggestion** — what Gemini is asking to change and why
3. **Evaluate validity** — Gemini can be wrong. Check if the suggestion actually applies:
   - Does the suggested pattern match the project's conventions?
   - Is the "bug" actually a bug, or is Gemini misunderstanding context?
   - Does the performance suggestion matter at the project's scale?
4. **Make the fix** if valid, following the project's existing patterns
5. **Skip with reason** if invalid — explain to the user why the suggestion doesn't apply
6. **Track which thread IDs and comment IDs were addressed** — you'll need thread IDs for resolving and comment IDs for replying

### Step 6: Reply to Every Gemini Comment

You MUST reply to every Gemini review comment explaining what you did. This is non-negotiable —
Gemini (and the PR author) needs to see that each comment was acknowledged.

First, get the REST comment IDs (the `id` field from the REST API, not GraphQL):

```bash
gh api repos/devanfer02/telnetquiz-cms/pulls/<PR_NUMBER>/comments \
  --jq '[.[] | select(.user.login == "gemini-code-assist")] | .[] | {id, path, line, body}'
```

Then for each comment, post a reply:

**If you fixed the issue:**
```bash
gh api repos/devanfer02/telnetquiz-cms/pulls/<PR_NUMBER>/comments/<COMMENT_ID>/replies \
  -f body="Fixed — <brief explanation of what was changed and why>"
```

**If you skipped it (with reason):**
```bash
gh api repos/devanfer02/telnetquiz-cms/pulls/<PR_NUMBER>/comments/<COMMENT_ID>/replies \
  -f body="Acknowledged — skipping this because <reason>. <explanation of why the current code is correct/preferred>"
```

Reply to EVERY Gemini comment, no exceptions. Even skipped ones get a reply explaining why.

### Step 7: Resolve Addressed Review Threads

After making fixes and the user confirms they're ready to push, resolve each addressed
Gemini review thread using the GraphQL `resolveReviewThread` mutation. This marks the
conversation as "Resolved" on GitHub so the PR looks clean.

For each addressed thread:

```bash
gh api graphql -f query='
  mutation($threadId: ID!) {
    resolveReviewThread(input: { threadId: $threadId }) {
      thread { isResolved }
    }
  }' -f threadId="<THREAD_ID>"
```

Where `<THREAD_ID>` is the `id` from Step 2's GraphQL response (e.g. `PRRT_kwDOQOCJfc53eyEz`).

Resolve threads in bulk — loop through all addressed thread IDs. Only resolve threads where
a fix was actually made. Do not resolve threads that were skipped or need discussion.

### Step 8: Push Changes and Re-trigger Gemini

After pushing the commit with fixes, post a **top-level PR comment** (not a reply to any
Gemini thread) with `/gemini review` to re-invoke Gemini on the updated code:

```bash
gh pr comment <PR_NUMBER> --repo devanfer02/telnetquiz-cms --body "/gemini review"
```

This is a top-level issue comment on the PR — it goes under the PR conversation, not under
any specific review thread. Gemini picks this up and runs a fresh review on the latest changes.

After posting the comment, **sleep 20 seconds** to give Gemini time to process and post its review:

```bash
sleep 20
```

Then re-fetch the review threads (Step 2) to see if Gemini posted new comments.

### Step 9: Report Summary

After addressing comments, provide a summary:

```markdown
## Gemini Review Summary — PR #<NUMBER>

### Addressed & Resolved
- [file:line] <what was fixed and why> (thread resolved)
- [file:line] <what was fixed and why> (thread resolved)

### Skipped (with reason)
- [file:line] <suggestion> — Skipped: <reason> (thread left open)

### Needs Discussion
- [file:line] <suggestion> — <why this needs human decision> (thread left open)

### Actions Taken
- Resolved N review threads
- Pushed fixes in commit <sha>
- Re-triggered Gemini review via `/gemini review` comment
```

## Useful gh CLI Commands Reference

```bash
# List open PRs
gh pr list --repo devanfer02/telnetquiz-cms

# View specific PR with diff
gh pr view <N> --repo devanfer02/telnetquiz-cms
gh pr diff <N> --repo devanfer02/telnetquiz-cms

# Get review threads with IDs (for resolving)
gh api graphql -f query='query($n:Int!){repository(owner:"devanfer02",name:"telnetquiz-cms"){pullRequest(number:$n){reviewThreads(first:100){nodes{id isResolved path line comments(first:5){nodes{body author{login}}}}}}}}' -F n=<N>

# Get PR review comments via REST (includes diff_hunk)
gh api repos/devanfer02/telnetquiz-cms/pulls/<N>/comments

# Filter to only Gemini comments
gh api repos/devanfer02/telnetquiz-cms/pulls/<N>/comments \
  --jq '[.[] | select(.user.login == "gemini-code-assist")] | .[] | {id, path, line, body}'

# Resolve a review thread
gh api graphql -f query='mutation($id:ID!){resolveReviewThread(input:{threadId:$id}){thread{isResolved}}}' -f id="<THREAD_ID>"

# Reply to a review comment
gh api repos/devanfer02/telnetquiz-cms/pulls/<N>/comments/<COMMENT_ID>/replies \
  -f body="Fixed in <commit_sha>"

# Post top-level PR comment (for /gemini review)
gh pr comment <N> --repo devanfer02/telnetquiz-cms --body "/gemini review"

# Get PR issue comments (conversation-level)
gh api repos/devanfer02/telnetquiz-cms/issues/<N>/comments

# Check PR checks/status
gh pr checks <N> --repo devanfer02/telnetquiz-cms
```

## Behavioral Rules

1. **Always fetch fresh data** — don't rely on cached PR state
2. **Show the user what Gemini said** before making changes — present the categorized list first
3. **Don't blindly apply all suggestions** — evaluate each against project conventions
4. **Preserve existing patterns** — if Gemini suggests a pattern that contradicts the project's established approach, flag it rather than changing
5. **Group related fixes** — if multiple comments touch the same file, batch the edits
6. **Ask before large refactors** — if a suggestion would require changes across many files, get user approval first
7. **Only resolve threads you actually fixed** — skipped or discussion items stay open for visibility
8. **Always re-trigger Gemini after pushing** — post `/gemini review` as a top-level PR comment so Gemini reviews the updated code
9. **Reply to EVERY Gemini comment** — no exceptions. Every comment gets a reply explaining what you did or why you skipped it. Silent fixes are not acceptable
