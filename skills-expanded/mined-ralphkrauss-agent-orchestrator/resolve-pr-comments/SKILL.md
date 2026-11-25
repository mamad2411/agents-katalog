---
name: resolve-pr-comments
description: Resolve all pull request comments through a triage-first workflow — including review inline comments, review body comments (summary text on review submissions), and general conversation comments. Checks out the PR branch, loads all comment types, gathers deep context for each, discusses options with the user, and builds a resolution map — all before any code changes. Once aligned, creates an implementation plan via /create-plan, executes it, then replies to all PR comments on GitHub. Use when the user mentions "resolve PR comments", "fix PR feedback", "address review comments", or provides a PR number/URL to resolve.
---
<!-- Generated from .agents/ by scripts/sync-ai-workspace.mjs. Do not edit directly. -->


# Resolve PR Comments

Triage-first workflow for all pull request comments — review inline comments, review body comments, and general conversation comments. Separates **deciding** (interactive, fast) from **doing** (autonomous, batched). Goes through every comment with deep context gathering, discusses options with the user, and builds a complete resolution map. Once fully aligned, hands off to `/create-plan` and `/implement-plan` for autonomous execution, then replies to all PR comments on GitHub.

## Critical Rules

1. **ONE COMMENT AT A TIME**: Triage each comment individually with user approval
2. **DECIDE, DON'T IMPLEMENT**: During triage (Phase 2), only gather context, discuss, and record decisions — make NO code changes, NO GitHub replies, NO issue creation
3. **FULL CONTEXT FIRST**: For code comments, read the referenced file, surrounding code, related files, and docs. For non-code comments (review bodies, conversation), read the PR diff, changed files, and any files referenced in the comment body. This deep context gathering is non-negotiable even though it takes time
4. **FOLLOW PROJECT PATTERNS**: Check existing code and docs before proposing approaches
5. **DRAFT REPLIES DURING TRIAGE**: Write the exact GitHub reply text for each comment during triage while context is fresh — these are stored in the resolution map for Phase 4
6. **COMMENT PREFIX**: All GitHub reply comments MUST start with `**[Claude Code]:**`
7. **USE TODO LIST**: Track all comments as todos for progress visibility
8. **RESOLUTION MAP IS THE BRIDGE**: The file `plans/{branch-name}/resolution-map.md` is the durable artifact that carries decisions from triage into planning and execution — write it carefully, it must be self-contained

---

## Phase 1: Initialize

### Step 1.1: Identify the PR

Determine the PR to work on:

- If user provides a PR number: use it directly
- If user provides a PR URL: extract the number
- If neither: detect from current branch — get the branch name with `git branch --show-current`, then list open pull requests using the available GitHub tools (owner, repo, head branch, state: open) to find the matching PR number

### Step 1.2: Checkout the Branch

Fetch the PR details using the available GitHub tools (owner, repo, pullNumber) to get the PR's head branch name. Then checkout via git:

```bash
git fetch origin <branch-name>
git checkout <branch-name>
```

If the branch is already checked out, just ensure it's up to date with `git pull`.

### Step 1.3: Fetch All Comments

Fetch all three types of PR comments:

**Review comments** (inline code comments with thread context):

Fetch the PR review comments using the available GitHub tools (owner, repo, pullNumber). This returns review threads with metadata including `isResolved`, `isOutdated`, `isCollapsed` and their associated comments — combining both the comment data and thread resolution status in a single call.

Use pagination (`page`, `perPage`) and collect **all pages** before filtering or categorizing comments. Do not rely on the first page only — large PRs can have more than one page of inline review comments. Continue until the API returns no more items, or until the returned item count is less than `perPage`.

Key fields per comment:

| Field | Purpose |
|-------|---------|
| `id` | Unique ID, needed for replying |
| `pull_request_review_id` / `review_id` | Review submission ID; needed to relate inline comments to review-body comments from the same review |
| `path` | File path the comment is on |
| `line` | Line number in the file |
| `start_line` | Start line if comment spans a range (null for single-line) |
| `diff_hunk` | The diff context around the comment |
| `body` | The comment text (markdown) |
| `user.login` | Who wrote it |

The initial response includes thread-level `isResolved` for filtering, but does **not** include the GraphQL node ID needed to resolve threads programmatically. Fetch thread node IDs separately with a paginated GraphQL query:

```
gh api graphql --paginate \
  -f owner="<owner>" \
  -f repo="<repo>" \
  -F number="<number>" \
  -f query='
query($owner: String!, $repo: String!, $number: Int!, $endCursor: String) {
  repository(owner: $owner, name: $repo) {
    pullRequest(number: $number) {
      reviewThreads(first: 100, after: $endCursor) {
        pageInfo {
          hasNextPage
          endCursor
        }
        nodes {
          id
          isResolved
          comments(first: 1) {
            nodes {
              databaseId
            }
          }
        }
      }
    }
  }
}'
```

This returns each thread's `id` (GraphQL node ID, e.g. `PRRT_kwDOQtECwc51toKM`) and the first comment's `databaseId` across every review-thread page. **Correlate thread node IDs to review comments** by matching `databaseId` from GraphQL to the `id` field of the first comment in each thread. Save the thread node ID and review submission ID alongside each comment — they're needed in Phase 2 and Phase 4.

**Review body comments** (summary text on review submissions):

Fetch the PR reviews using the available GitHub tools (owner, repo, pullNumber) via `get_reviews`. Each review represents a submitted review (Approve / Request Changes / Comment) and may include a body — the summary text the reviewer wrote when submitting.

Filter out reviews with empty or whitespace-only bodies — only reviews with substantive body text are actionable comments. Also filter out `DISMISSED` reviews — these represent withdrawn/stale feedback and should not be triaged.

Key fields per review:

| Field | Purpose |
|-------|---------|
| `id` | Unique review ID |
| `body` | The review summary text (may be empty — skip if so) |
| `state` | Review state: `APPROVED`, `CHANGES_REQUESTED`, `COMMENTED`, `DISMISSED` — filter out `DISMISSED` reviews as stale/withdrawn feedback |
| `user.login` | Who submitted the review |
| `submitted_at` | When the review was submitted |

**Note:** Review body comments are distinct from review inline comments. A single review submission can have both a body (summary) and inline comments (on specific code lines). The inline comments are already captured by `get_review_comments` above. This step captures the body text that would otherwise be missed.

When triaging a review body, match the review body's `id` to each inline comment's `pull_request_review_id` / `review_id` to identify inline comments submitted as part of the same review.

Use pagination (`page`, `perPage`) if the PR has many reviews — the same as for review comments.

**Issue comments** (general PR conversation comments):

Fetch the PR issue-level comments using the available GitHub tools (owner, repo, pullNumber) via `get_comments`. These are comments in the main PR conversation thread that are not attached to specific code lines.

Key fields: `id`, `body`, `user.login`, `created_at`.

Use pagination (`page`, `perPage`) if the PR has many conversation comments.

### Step 1.4: Filter, Categorize, and Prioritize

**Filter out already-resolved threads**: Using the thread mapping from Step 1.3, discard any review comment whose thread has `isResolved: true`. These have already been handled in a previous session and don't need re-processing.

**Filter out informational bot comments**: For issue comments and review body comments, apply smart bot filtering based on the comment author:

| Author pattern | Action | Rationale |
|----------------|--------|-----------|
| `github-actions[bot]` | Skip | CI status, workflow notifications |
| `vercel[bot]`, `netlify[bot]` | Skip | Deployment preview notifications |
| `codecov[bot]`, `coveralls[bot]` | Skip | Coverage reports — purely informational |
| `dependabot[bot]`, `renovate[bot]` | Skip | Dependency update notifications |
| `coderabbitai[bot]`, `bugbot` | **Keep** | AI review feedback — contains actionable suggestions |
| `cursor[bot]`, `claude-code[bot]` | **Keep** | AI review feedback — contains actionable suggestions |
| Other `[bot]` accounts | **Keep with flag** | Unknown bot — include but flag for verification during triage |
| Human accounts | **Keep** | Always include human comments |

**Filter out previously-handled comments**: For conversation comments, check if any issue comment exists that references the original comment's ID (e.g., contains `<!-- resolve-pr-comment-id: <comment-id> -->`). For review-body comments, check if any issue comment references the review ID (e.g., contains `<!-- resolve-pr-review-id: <review-id> -->`). These hidden HTML markers are included in Phase 4 replies for exact correlation — but only for **final** decisions (fix, alternative-fix, decline). Deferred and escalated replies intentionally omit the correlation marker so the original comment remains "unhandled" and can be revisited on subsequent runs. Only skip a comment when an exact ID match is found — do not rely on prefix-based heuristics, as multiple `**[Claude Code]:**` replies may exist for unrelated comments. **Important:** run this check against the full raw set of issue comments, before any other filtering — the correlation markers are co-located in reply comments that would be removed by the next step.

**Filter out own previous replies**: Discard any issue comment containing `<!-- resolve-pr-reply -->`. These are replies posted by a previous Phase 4 run and should not be triaged as new comments.

**Categorize all remaining comments** across all three types by:

1. **Comment type** — review-inline, review-body, conversation
2. **Severity** (if indicated in comment body — e.g. "High Severity", "Medium Severity")
3. **File** — for review-inline comments, group by file; review-body and conversation comments have no file
4. **Type** — bug fix, security issue, style, architecture, etc.

Create a todo list with all unresolved/unhandled comments. Order by:
- Review-inline comments first (by severity, then by file)
- Review-body comments next (by review date)
- Conversation comments last (by date)

Comment numbering is unified across all types (Comment 1, 2, 3... regardless of type).

Present a summary to the user:

```
Found X unresolved comments on PR #N:
- A review-inline comments (B already resolved, skipped)
- C review-body comments (F bot reviews skipped)
- D conversation comments (E bot comments skipped)

Severity breakdown:
- G high severity
- H medium severity
- I low severity / other

Files affected (review-inline only):
- path/to/file1.ext (2 comments)
- path/to/file2.ext (1 comment)

Ready to start triage. Begin? (Y/skip to #N/stop)
```

---

## Phase 2: Triage & Decide

This phase is **decision-only**. No code changes, no GitHub replies, no issue creation. The goal is to go through every comment quickly, gather deep context, discuss the right approach, and record the decision in the resolution map.

### Step 2.1: Gather Context

For each comment, invest the time to build a thorough understanding. The context-gathering approach depends on the comment type:

#### For review-inline comments (have file/line references):

1. **Read the comment body** in full
2. **Read the referenced file** — focus on the area around `line` (±30 lines for context)
3. **Read the diff hunk** — understand what changed
4. **Check related files** — if the comment mentions other files, patterns, or interfaces, read those too
5. **Check docs/patterns** — search `docs/` and existing code for relevant patterns
6. **Verify AI comments independently** — if the comment is from an AI reviewer (CodeRabbit, Bugbot, Cursor, Claude Code), do not trust its description of the code's behavior. Read the actual code and confirm whether the described issue exists before proceeding. See the "Bot / Automated Comments" section for the full verification protocol.

#### For review-body and conversation comments (no file/line references):

1. **Read the comment body** in full
2. **Get the PR overview** — fetch the list of changed files using `get_files` to understand what the PR touches
3. **Read the PR diff** — use `get_diff` to understand the overall changes, or read specific changed files if the comment references them by name
4. **Identify referenced files** — scan the comment body for file names, class names, method names, or patterns. If found, read those files for context
5. **Check docs/patterns** — search `docs/` and existing code for relevant patterns mentioned in the comment
6. **Verify AI comments independently** — same protocol as review-inline: do not trust AI descriptions of code behavior. Read the actual code.
7. **For review-body comments specifically** — also check if this review has associated inline comments by matching the review body's `id` to inline comments' `pull_request_review_id` / `review_id`. The body may provide context or summary for the inline comments, which helps understand the reviewer's overall intent.

#### For all comment types — assess depth:

Does this comment point to a localized issue or a deeper pattern? Quick signals:
- The fix requires changes across multiple unrelated files or layers
- The comment challenges an architectural decision, not just the implementation detail
- Similar code exists elsewhere that would need the same treatment (grep for the pattern)
- A proper fix would require understanding and restructuring a broader abstraction

If any of these apply, flag the comment as **deep** — this changes how options are presented in Step 2.3.

### Step 2.2: Present the Comment

Show the user a clear summary. Use the appropriate template based on comment type:

**For review-inline comments:**

```
Comment N of X | review-inline | <severity> | <file-path>:<line>

<comment body — full text>

Referenced code:
<the relevant code section from the file>

Context:
<your analysis of what the comment is asking for and why>
```

**For review-body comments:**

```
Comment N of X | review-body | <severity> | Review by @<user.login> (<state>)

<review body — full text>

PR scope:
<summary of files changed in the PR and what the PR does>

Related inline comments from this review:
<list any inline comments from the same review, or "None">

Context:
<your analysis of what the reviewer is asking for and why>
```

**For conversation comments:**

```
Comment N of X | conversation | <severity> | @<user.login>

<comment body — full text>

PR scope:
<summary of files changed in the PR and what the PR does>

Context:
<your analysis of what the comment is asking for and why>
```

### Step 2.3: Present Options

Based on comment type, present tailored options. These are **decisions about approach**, not immediate actions. **Check depth first** — if the comment was flagged as **deep** in Step 2.1, use the Deep / Systemic category below.

#### For Deep / Systemic Issues

When the comment was flagged as **deep** in Step 2.1, present escalation-first options. Deep refactors cannot be reliably done as a side-effect of PR comment resolution — they need focused attention.

Present your assessment of **why** this is deep: what's the scope, what other areas are affected, what would a proper fix entail. Then offer:

```
This comment touches a deeper pattern. Here's what I see:
<your assessment — scope, affected areas, what a proper solution would look like>

Options:
A) Create GitHub issue — Capture the problem and context as a trackable issue (created in Phase 4)
B) Defer — Acknowledge the problem, handle in a separate session
C) Fix in this PR — You give me specific direction on how to handle this now
D) Actually surface-level — This is a straightforward fix (show me the normal options)
```

#### For Bug Reports / Logic Issues

```
Options:
A) Fix as suggested — <describe the specific code change>
B) Alternative fix — <describe a different approach if applicable>
C) Not a bug — <explain why the current code is correct, will reply explaining>
D) Need more context — I want to investigate further before deciding
```

#### For Security Issues

```
Options:
A) Fix as suggested — <describe the secure implementation>
B) Alternative approach — <different security measure>
C) Accept risk — Document why this is acceptable (will reply with rationale)
D) Need security review — Flag for further discussion
```

#### For Architecture / Design Suggestions

Most architecture comments should be flagged as **deep** in Step 2.1 and handled via the Deep / Systemic options above. Use these options only when the architectural change is genuinely contained to a small scope:

```
Options:
A) Refactor as suggested — <describe the contained refactoring>
B) Defer — Acknowledge but handle in a separate PR or session
C) Discuss — Need to talk through the trade-offs
```

#### For Style / Naming / Cleanup

```
Options:
A) Accept — Apply the suggested change
B) Modify — Apply a variation of the suggestion
C) Decline — Keep current code (will reply with reasoning)
```

### Step 2.4: Wait for User Choice

**CRITICAL**: Do not proceed until the user provides their choice.

Accept:
- Letter choices (A, B, C, D)
- Custom instructions ("Actually, let's do it this way...")
- Requests for more information ("Show me the full file", "What does X do?")
- Deferral ("Skip this one for now")

### Step 2.5: Record Decision in Resolution Map

After the user decides, record the decision in `plans/{branch-name}/resolution-map.md`. Create this file on the first decision.

**Resolution map format:**

```markdown
# PR #<number> — Resolution Map

Branch: `<branch-name>`
Created: <date>
Total comments: X | To fix: Y | To defer: Z | To decline: W | To escalate: V
Comment types: A review-inline | B review-body | C conversation

---

## Comment 1 | <status> | <severity>
- **Comment Type:** <review-inline / review-body / conversation>
- **File:** <path>:<line> _(review-inline only — omit for review-body and conversation)_
- **Comment ID:** <github-comment-id> _(review-inline and conversation only — omit for review-body)_
- **Review ID:** <github-review-id> _(review-body only — omit for other types)_
- **Thread Node ID:** <graphql-thread-node-id> _(review-inline only — omit for other types)_
- **Author:** <user.login>
- **Comment:** <full comment body>
- **Decision:** <fix-as-suggested / alternative-fix / decline / defer / escalate>
- **Approach:** <specific description of what to do — detailed enough for a developer agent to implement without re-reading the comment discussion>
- **Files to change:** <list of files that need modification>
- **GitHub reply (draft):**
  > **[Claude Code]:** <pre-drafted reply text>
  >
  > <explanation of what was changed/why — written as if the fix is already done>

---

## Comment 2 | <status> | <severity>
...
```

**Key requirements for the resolution map:**

- **Approach must be self-contained** — a developer reading only the resolution map entry should have enough detail to implement the fix without needing to re-read the PR comment or re-gather context. Include specific method names, patterns to follow, and the exact change needed.
- **GitHub reply must be pre-drafted** — write the reply as if the fix is already done. This text is posted verbatim in Phase 4. Use the appropriate format based on status (resolved/declined/deferred/escalated) as defined in the reply templates below.
- **Comment Type must be recorded** — determines the reply mechanism and whether thread resolution applies in Phase 4.
- **Thread Node ID must be recorded for review-inline comments** — needed for resolving threads in Phase 4. Not applicable to review-body or conversation comments.
- **Review ID must be recorded for review-body comments** — needed for referencing the review when posting the reply in Phase 4.

**Reply templates for drafting:**

These templates are posted **verbatim** in Phase 4 — include the full prefix in the draft. Phase 4 does not add any additional prefix or wrapping.

**Status-specific resolution text** (used as `<resolution text>` in all templates below):

| Status | Resolution text |
|--------|----------------|
| Resolved (fix/alternative fix) | `<description of what was changed and why>` |
| Escalated (create issue) | `This touches a deeper pattern that needs focused attention. Created <ISSUE_LINK_PLACEHOLDER> to track the proper refactor.\n\n<scope description>` |
| Deferred | `Acknowledged — deferring to a follow-up PR.\n\n<reason for deferral>` |
| Declined | `After review, keeping the current implementation.\n\n<rationale>` |

**For review-inline comments**, combine the prefix with the resolution text:

```
**[Claude Code]:** <resolution text>
```

**For review-body comments**, use the `Re:` attribution format (use the review URL for unambiguous linking), followed by the resolution text (without a second `**[Claude Code]:**` prefix — it's already in the `Re:` line):

```
**[Claude Code]:** Re: @<author>'s [review](https://github.com/<owner>/<repo>/pull/<number>#pullrequestreview-<review-id>) —

<resolution text>
```

**For conversation comments**, use the `Re:` attribution format (use the comment URL for unambiguous linking), followed by the resolution text (without a second `**[Claude Code]:**` prefix):

```
**[Claude Code]:** Re: @<author>'s [comment](https://github.com/<owner>/<repo>/pull/<number>#issuecomment-<comment-id>) —

<resolution text>
```

Update the todo item to completed.

### Step 2.6: Proceed to Next

```
Decision recorded for Comment N. X remaining.

Next: <comment-type> | <severity> | <location> — "<first line of comment>"
Continue? (Y/skip/stop)
```

Where `<location>` is `<file>:<line>` for review-inline, `Review by @<user>` for review-body, or `@<user>` for conversation.

Options:
- **Y / continue**: Process next comment
- **skip**: Skip to the comment after next
- **stop**: Pause processing (can resume later)
- **go to N**: Jump to a specific comment number

---

## Phase 3: Align & Plan

Once all comments have been triaged, present the full resolution map for final alignment and create an implementation plan.

### Step 3.1: Present Resolution Summary

Present the complete resolution map as a summary table:

```
PR #<number> — Resolution Map Complete

| # | Type | Location | Severity | Decision | Approach Summary |
|---|------|----------|----------|----------|-----------------|
| 1 | review-inline | path/file.ext:60 | High | Fix as suggested | Replace X with Y |
| 2 | review-inline | path/file.ui-ext:267 | Medium | Alternative fix | Use pattern Z instead |
| 3 | review-body | @reviewer's review | Medium | Fix as suggested | Address naming concern |
| 4 | conversation | @user comment | Low | Defer | Handle in follow-up |
| 5 | review-inline | path/file.ext:120 | Low | Decline | Current code is correct |
| 6 | review-inline | path/file.ext:200 | High | Escalate (issue) | Needs dedicated refactor |

Fix: X comments | Defer: Y | Decline: Z | Escalate: W

Review the resolution map. Any changes before I create the implementation plan?
```

Wait for user confirmation. If the user wants to revisit any decision, go back to that comment (re-read context if needed) and update the resolution map entry.

### Step 3.2: Create Implementation Plan

Once the user confirms the resolution map, invoke the `/create-plan` skill to create an implementation plan. Feed it the resolution map as input context:

- **Feature slug**: `pr-<number>-review-fixes`
- **Context**: the resolution map — each "fix" and "alternative fix" comment becomes a task, grouped logically by file or concern
- **Scope**: only the comments marked for implementation (fix/alternative fix/escalate). Deferred and declined comments are out of scope for the plan — they only need GitHub replies.

The plan should follow the standard `/create-plan` structure with tasks derived from the resolution map. Each task's acceptance criteria should reference the specific comment number and the agreed approach.

**Skip the /create-plan discussion phase** — the triage in Phase 2 already resolved all decisions. Go straight to writing the plan with the decisions from the resolution map.

For **escalated** comments (create GitHub issue), add a task to the plan for creating the issue with the full context captured in the resolution map.

### Step 3.3: User Confirms Plan

The `/create-plan` skill handles its own review and confirmation. Once the plan is confirmed, proceed to Phase 4.

---

## Phase 4: Execute & Close

This is the autonomous phase — the user can step away. All code changes, GitHub replies, and thread resolutions happen here.

### Step 4.1: Implement the Plan

Use the `/implement-plan` skill to execute the plan created in Phase 3. This handles:
- Delegated agent task execution
- Build and test verification
- Hardening passes

### Step 4.2: Create GitHub Issues (for escalated comments)

For any comments marked as **escalated**, create a GitHub issue with the context from the resolution map. Then update the resolution map's draft reply to replace `<ISSUE_LINK_PLACEHOLDER>` with the actual issue URL.

### Step 4.3: Leave for Review

Do NOT commit or push automatically. Changes from `/implement-plan` remain in the working tree so review skills (`/review`, `/review-codex`) can inspect them.

**Before proceeding to Step 4.4**, require explicit user confirmation that `/commit` has been run and the fixes are pushed to the PR branch. GitHub replies and thread resolution must not happen while fixes exist only locally.

### Step 4.4: Reply to Comments on GitHub

Post the pre-drafted replies from the resolution map to each comment on GitHub. The reply mechanism depends on the comment type:

**For review-inline comments** (`Comment Type: review-inline`):

Reply to the specific PR review comment using the available GitHub tools (owner, repo, pullNumber, commentId from the resolution map, body from the draft reply text).

**For review-body comments** (`Comment Type: review-body`):

Post a new issue comment on the PR using the GitHub tools (owner, repo, issue_number set to the PR number). The reply must include the Review ID for correlation and disambiguation. Post the draft reply text verbatim (it already includes the `**[Claude Code]:**` prefix and `Re:` attribution), then append hidden HTML markers:

- Always include `<!-- resolve-pr-reply -->` (self-identifier so this reply is filtered out on re-runs)
- Only for **final** decisions (fix, alternative-fix, decline): also include `<!-- resolve-pr-review-id: <review-id> -->` (correlation marker that marks the original as handled)
- For **deferred** and **escalated** decisions: omit the correlation marker so the original comment remains "unhandled" on re-runs

```
<pre-drafted reply text from resolution map — posted verbatim>

<!-- resolve-pr-reply -->
<!-- resolve-pr-review-id: <review-id> -->   ← only for final decisions
```

**For conversation comments** (`Comment Type: conversation`):

Post a new issue comment on the PR using the GitHub tools (owner, repo, issue_number set to the PR number). Post the draft reply text verbatim, then append hidden HTML markers:

- Always include `<!-- resolve-pr-reply -->` (self-identifier so this reply is filtered out on re-runs)
- Only for **final** decisions (fix, alternative-fix, decline): also include `<!-- resolve-pr-comment-id: <original-comment-id> -->` (correlation marker that marks the original as handled)
- For **deferred** and **escalated** decisions: omit the correlation marker so the original comment remains "unhandled" on re-runs

```
<pre-drafted reply text from resolution map — posted verbatim>

<!-- resolve-pr-reply -->
<!-- resolve-pr-comment-id: <original-comment-id> -->   ← only for final decisions
```

### Step 4.5: Resolve Review Threads on GitHub

**This step only applies to review-inline comments.** Review-body and conversation comments do not have threads to resolve — skip them.

For each review-inline comment marked as **resolved** or **declined**, resolve the review thread using the GitHub CLI with the GraphQL `resolveReviewThread` mutation. Use the thread node ID from the resolution map:

```bash
gh api graphql -f query='mutation { resolveReviewThread(input: { threadId: "<THREAD_NODE_ID>" }) { thread { isResolved } } }'
```

**Do NOT resolve threads for deferred or escalated comments** — those should remain open for follow-up.

### Step 4.6: Present Summary

```
PR #<number> Review Resolution Summary

| # | Type | Location | Severity | Status | Reply Posted? | Thread Resolved? |
|---|------|----------|----------|--------|---------------|-----------------|
| 1 | review-inline | path/file.ext:60 | High | Resolved | Yes | Yes |
| 2 | review-inline | path/file.ui-ext:267 | Medium | Resolved | Yes | Yes |
| 3 | review-body | @reviewer's review | Medium | Resolved | Yes | n/a |
| 4 | conversation | @user comment | Low | Deferred | Yes | n/a |
| 5 | review-inline | path/file.ext:120 | High | Escalated | Yes (issue link) | No (open) |
| 6 | review-inline | path/file.ext:200 | Low | Declined | Yes | Yes |

Skipped: N already-resolved threads, M bot comments filtered

Files modified:
- path/to/file1.cs — <change summary>
- path/to/file2.ui-ext — <change summary>

Changes: committed and pushed before replies (per Step 4.3)
Replies posted: X of Y comments
Threads resolved: X of Y review-inline (deferred/escalated left open; review-body/conversation have no threads)

Escalated items (need dedicated attention):
- Comment #5: <issue-link> — <brief description>

Deferred items:
- Comment #4: <reason>
```

### Step 4.7: Clean Up

The resolution map at `plans/{branch-name}/resolution-map.md` stays in the working tree alongside code changes — no cleanup needed. It serves as a durable record of the triage decisions and will be committed when the user runs `/commit`.

---

## Phase 5: Knowledge Capture (Self-Learning)

This phase converts PR feedback into durable documentation so the same mistakes are not repeated. It runs after all comments are resolved — the code changes are done, now we improve the knowledge base.

### Step 5.1: Classify Learnings

Review all resolved comments and classify each as `pattern` or `one-off`:

**Ask two questions per comment:**

1. **Is this a general pattern or a one-off?** A general pattern is something that could happen again in a different file, feature, or PR. A one-off is specific to this exact context and unlikely to recur.
2. **Could documentation have prevented this comment?** If a doc or AGENTS.md rule existed that covered this pattern, would the original code have been written correctly the first time?

| Classification | Description | Example |
|---|---|---|
| `pattern` | General convention, architectural rule, or best practice that should be documented | "Always use typed enums instead of magic strings for third-party fields" |
| `one-off` | Specific to this PR — typo, missed requirement, context-dependent choice | "This variable should be named `accountId` not `userId` in this specific handler" |

**Skip this phase entirely if no comments are classified as `pattern`.**

### Step 5.2: Collect and Deduplicate

Merge duplicates — if multiple comments point to the same underlying pattern, combine them into a single learning.

Present the learning candidates to the user:

```
PR #<number> — Learning Candidates

Found N comments that reveal general patterns:

1. [Architecture] "Use typed mappers for third-party contract fields"
   From: comment on src/integrations/{vendor}/auth-builder.ext:45
   Scope: all third-party integrations

2. [Convention] "Request handlers should not access the request context directly"
   From: comment on src/core/handlers/entity-handler.ext:22
   Scope: all request handlers

Review each and approve/reject for documentation? (Y/skip phase)
```

### Step 5.3: Search Existing Lessons

For each approved learning candidate, deduplicate against the centralized review store:

1. **Search `.agents/rules/`** — grep by keywords for overlapping rules
2. **Search `AGENTS.md`** — is this pattern already a universal rule?
3. **Search `docs/`** — does an existing guide already cover this?

If a match exists: refine the existing rule if the new comment adds nuance. Do NOT create a duplicate.

If no match: proceed to create a new rule.

### Step 5.4: Create Rules

For each new rule, delegate to `/create-rule`. Provide:
- The pattern (rule text from the comment)
- The anti-pattern (the bad code that was caught, with example)
- The evidence (PR number, who raised the comment, what happened)
- Suggested context tags (what kind of work this applies to)

**Do NOT write rule files directly** — `/create-rule` handles dedup, ID assignment, index update, and source tracking.

**For patterns that are truly universal** (apply to every PR): propose graduation to AGENTS.md. Present the draft to the user for approval before adding.

### Step 5.5: Present Learning Summary

```
Knowledge Capture Summary

| # | Pattern | Action | Target |
|---|---------|--------|--------|
| 1 | Typed mappers for third-party fields | New lesson | INT-012 |
| 2 | No request-context access in request handlers | Updated lesson | ARCH-009 (added PR evidence) |
| 3 | Metric after commit | Already exists | ARCH-015 |

Index updated: total = N (M active, K graduated)
```

Leave the lesson files in the working tree alongside the code fixes — they will be included when the user runs `/commit`.

---

## Handling Special Cases

### Threaded Comments

If a comment has replies, the thread data is already available from the review comments fetch in Step 1.3 — each thread includes all associated comments. Present the full thread to the user so they have the discussion context.

### Comments Already Addressed

If a comment refers to code that has already been fixed (e.g., in a subsequent commit):

```
This comment appears to be already addressed in the current code.

Current code at <file>:<line>:
<show current code>

Options:
A) Mark as addressed — Reply confirming it's fixed
B) Still applicable — The concern still exists, show me more context
C) Skip — Move to next comment
```

### Comments Spanning Multiple Files

If resolving a comment requires changes across multiple files:

1. List all files that need changes
2. Present the full scope to the user
3. Record the complete list of affected files in the resolution map
4. The implementation plan will handle the cross-file coordination

### Bot / Automated Comments

Do **not** skip Bugbot/Cursor/CodeRabbit comments. Treat them as normal review feedback and process them through the same one-by-one triage flow.

**AI-generated comments are frequently wrong.** CodeRabbit, Bugbot, Claude Code, and similar AI reviewers hallucinate — they report bugs that don't exist, misread control flow, invent race conditions, and confidently describe behavior that the code doesn't have. **Never take an AI comment at face value.** For every AI-generated comment:

1. **Read the actual code yourself** — don't rely on the AI's description of what the code does
2. **Verify the claim independently** — trace the logic, check the call chain, confirm whether the described scenario can actually happen
3. **Present your own assessment** — tell the user whether the comment is valid, partially valid, or wrong, with your reasoning. If the AI is wrong, say so clearly: _"This comment is incorrect because..."_
4. **Do not fix phantom bugs** — if the described issue doesn't exist in the code, recommend declining the comment with an explanation

When presenting an AI-generated comment in Step 2.2, flag it:

```
AI-generated comment (CodeRabbit/Bugbot/etc.) — independently verified: <valid/partially valid/incorrect>
<your assessment of why>
```

For other automated/bot comments that pass the bot filter in Step 1.4 (e.g., unknown bots flagged for triage), apply the same verification protocol — read the code, verify the claim, present your assessment. Note: known informational bots (CI status, coverage, deployment previews) are already filtered out in Step 1.4 and won't reach triage.

---

## Resuming Interrupted Processing

### Interrupted During Triage (Phase 2)

1. Check for an existing resolution map at `plans/{branch-name}/resolution-map.md`
2. If found, read it and present the current triage progress
3. Check the todo list for in-progress/pending items
4. Offer to continue from the next untriaged comment
5. Verify the branch is still checked out and up to date

### Interrupted During Execution (Phase 4)

1. Check the plan at `plans/{branch-name}/` for task completion status
2. Resume `/implement-plan` from where it left off
3. After implementation completes, continue with GitHub replies and thread resolution
