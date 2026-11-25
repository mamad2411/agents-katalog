---
name: resolve-issue-comments
description: Resolve GitHub issue comments through a triage-first workflow. Loads the issue, fetches all comments, gathers context for each, discusses options with the user, and builds a resolution map. Once aligned, executes actions (replies, plans, PRs, closes). Use when the user mentions "resolve issue comments", "address issue feedback", "process issue comments", "respond to issue", or provides an issue number/URL to resolve.
---

# Resolve Issue Comments

Triage-first workflow for GitHub issue comments. Separates **deciding** (interactive) from **doing** (autonomous, batched). Goes through every comment with context gathering, discusses the right response, and records decisions. Once aligned, posts replies, creates plans/PRs, and closes the issue if appropriate.

## Critical Rules

1. **ONE COMMENT AT A TIME**: Triage each comment individually with user approval
2. **DECIDE, DON'T ACT**: During triage (Phase 2), only gather context, discuss, and record decisions — make NO GitHub replies, NO code changes, NO issue state changes
3. **FULL CONTEXT FIRST**: If a comment references code, files, or features — read them before analyzing
4. **COMMENT PREFIX**: All GitHub reply comments MUST start with `**[Claude Code]:**`
5. **USE TODO LIST**: Track all comments as todos for progress visibility
6. **RESOLUTION MAP IS THE BRIDGE**: `plans/{branch-name}/issue-{number}-resolution-map.md` carries decisions from triage into execution

---

## Phase 1: Initialize

### Step 1.1: Identify the Issue

Determine the issue to work on:

- If user provides an issue number: use it directly
- If user provides an issue URL: extract the number
- If neither: ask the user for an issue number

### Step 1.2: Fetch the Issue and Comments

**Fetch the issue body:**

Fetch the issue details using the available GitHub tools (owner, repo, issue_number). Extract: title, body, state, labels, assignees, milestone.

**Fetch all comments:**

Fetch the issue comments using the available GitHub tools (owner, repo, issue_number).

Key fields per comment:

| Field | Purpose |
|-------|---------|
| `id` | Unique ID, needed for replying |
| `body` | The comment text (markdown) |
| `user.login` | Who wrote it |
| `created_at` | When it was posted |

### Step 1.3: Check for Existing Branch/PR

Check if there's already a branch or PR linked to this issue:

```bash
git branch -r --list "origin/{issue-number}-*"
git branch --list "{issue-number}-*"
```

Also check for open PRs referencing the issue:

Search for open pull requests using the available GitHub tools (query: `repo:{owner}/{repo} is:open {issue-number} in:title`).

If a branch exists, note it — it provides implementation context.

### Step 1.4: Categorize and Summarize

Classify each comment as one of:

| Type | Description | Examples |
|------|-------------|---------|
| `action-item` | Requires code changes, configuration, or deliverables | "We also need to handle the edge case where..." |
| `question` | Requires an answer or investigation | "Does this work with multi-currency?" |
| `feedback` | Opinion or suggestion on approach | "I'd prefer if we used X pattern instead" |
| `status-update` | Progress report, no action needed | "Deployed to staging, testing now" |
| `clarification` | Adds context to the original issue | "To be clear, this only applies to..." |
| `resolved` | Already handled by a subsequent comment or commit | (self-evident from thread) |

Create a todo list with all actionable comments (skip `status-update` and `resolved`), ordered by type priority: action-items first, then questions, then feedback, then clarifications.

Present a summary:

```
Issue #{number}: {title}
State: {open/closed} | Labels: {labels} | Assignee: {assignee}
Branch: {branch-name or "none"}

Found X comments (Y actionable, Z status/resolved — skipped):
- A action items
- B questions
- C feedback/suggestions
- D clarifications

Ready to start triage. Begin? (Y/skip to #N/stop)
```

---

## Phase 2: Triage & Decide

### Step 2.1: Gather Context

For each comment:

1. **Read the comment body** in full, including any replies in the thread
2. **If it references code** — read the referenced files/functions
3. **If it references other issues/PRs** — fetch their titles and status
4. **Check related docs** — search `docs/` for relevant patterns
5. **Check git history** — if a branch exists, check recent commits for relevant changes
6. **Verify AI/bot comments independently** — same protocol as `/resolve-pr-comments`: read actual code, don't trust the description

### Step 2.2: Present the Comment

```
Comment N of X | {type} | @{author} | {date}

{comment body — full text}

Context:
{your analysis of what the comment asks for and what's involved}
```

### Step 2.3: Present Options

Options depend on comment type:

#### For Action Items

```
Options:
A) Accept — Add to implementation scope: {describe the work}
B) Already done — This is handled by {commit/PR/code}: {evidence}
C) Out of scope — Defer to a separate issue
D) Needs discussion — I have questions about the approach
```

#### For Questions

```
Options:
A) Answer now — {draft answer based on code/docs investigation}
B) Investigate further — Need to check {what} before answering
C) Redirect — This should be asked in {other issue/channel}
D) User answers — I don't have enough context, you should reply
```

#### For Feedback/Suggestions

```
Options:
A) Accept — Incorporate into the approach: {how}
B) Partially accept — Take {part} but not {other part}: {reasoning}
C) Acknowledge — Valid point but no change needed: {reasoning}
D) Discuss — Need to talk through trade-offs
```

#### For Clarifications

```
Options:
A) Note taken — Update understanding, no reply needed
B) Confirm — Reply confirming we've incorporated this context
C) Follow-up question — Need more detail on {what}
```

### Step 2.4: Wait for User Choice

**CRITICAL**: Do not proceed until the user provides their choice.

### Step 2.5: Record Decision in Resolution Map

After the user decides, record in `plans/{branch-name}/issue-{number}-resolution-map.md`. If no branch exists yet, use `plans/issue-{number}/issue-{number}-resolution-map.md`.

**Resolution map format:**

```markdown
# Issue #{number} — Resolution Map

Title: {issue title}
Branch: {branch-name or "none — to be created"}
Created: {date}
Total comments: X | Action: Y | Answer: Z | Acknowledge: W | Defer: V

---

## Comment 1 | {status} | {type}
- **Comment ID:** {github-comment-id}
- **Author:** {user.login}
- **Date:** {created_at}
- **Comment:** {full comment body}
- **Decision:** {accept / already-done / out-of-scope / answer / acknowledge / defer}
- **Action:** {specific description of what to do}
- **GitHub reply (draft):**
  > **[Claude Code]:** {pre-drafted reply text}

---
```

**Reply templates:**

For **accepted action items**:
```
**[Claude Code]:** Accepted — {description of what will be implemented}.
```

For **already done**:
```
**[Claude Code]:** This is already handled — {evidence: commit hash, file:line, or PR link}.
```

For **answers**:
```
**[Claude Code]:** {answer text with references to code/docs}
```

For **acknowledged feedback**:
```
**[Claude Code]:** Good point — {how it's been incorporated, or why no change is needed}.
```

For **deferred/out-of-scope**:
```
**[Claude Code]:** Noted — deferring to a follow-up. {ISSUE_LINK_PLACEHOLDER if creating a new issue}
```

### Step 2.6: Proceed to Next

```
Decision recorded for Comment N. X remaining.

Next: {type} | @{author} — "{first line of comment}"
Continue? (Y/skip/stop)
```

---

## Phase 3: Align & Execute

### Step 3.1: Present Resolution Summary

```
Issue #{number} — Resolution Map Complete

| # | Type | Author | Decision | Action Summary |
|---|------|--------|----------|---------------|
| 1 | action-item | @user | Accept | Implement X |
| 2 | question | @user | Answer | Explain Y |
| 3 | feedback | @user | Acknowledge | No change needed |

Accept: X | Answer: Y | Acknowledge: Z | Defer: W

Review the resolution map. Any changes before I execute?
```

Wait for confirmation.

### Step 3.1b: Knowledge Capture — Rule Check

Before executing, review the triage decisions for patterns worth capturing:

1. **Check for recurring patterns** — did the issue triage reveal handler patterns, EF constraints, architectural conventions, or domain rules not covered by existing `.agents/rules/` files?
2. **Search existing rules** — grep `.agents/rules/` and `AGENTS.md` by keywords to confirm the pattern is not already documented.
3. **If a new rule is warranted**, suggest `/create-rule` with:
   - The pattern (rule text)
   - The anti-pattern (the bad code or behavior that the issue exposed, with example)
   - The evidence (source: issue number, who reported it, what happened)
   - Suggested context tags (what kind of work this applies to)

**Do NOT write rule files directly** — `/create-rule` handles dedup, ID assignment, index update, and source tracking.

Skip this step if the issue was purely operational (e.g., configuration change, data fix) with no generalizable lesson.

### Step 3.2: Execute Actions

Process decisions in order:

**For accepted action items with code changes:**
- If a branch exists: check it out, create/update a plan via `/create-plan`
- If no branch exists: create one from the issue number + title slug, then plan
- Execute via `/implement-plan`

**For answers and acknowledgments (no code changes):**
- Post the pre-drafted replies by adding a comment to the issue using GitHub tools (owner, repo, issue_number, body)

**For deferred items:**
- Create new GitHub issues if agreed during triage (replace `ISSUE_LINK_PLACEHOLDER` in the draft reply)
- Post the reply with the new issue link

### Step 3.3: Post All Replies

Post pre-drafted replies from the resolution map to each comment.

Add a comment to the issue using GitHub tools (owner, repo, issue_number, body). Post one consolidated reply per decision rather than replying to individual comments (issues don't support threaded replies to specific comments).

Format as a single reply grouping related decisions:

```markdown
**[Claude Code]:** Addressing comments on #{number}:

**Re: @{author}'s {type} ({date}):**
{reply text}

**Re: @{author}'s {type} ({date}):**
{reply text}

---
{code changes summary if applicable, with commit hash}
```

### Step 3.4: Close Issue (if appropriate)

If ALL action items are resolved and no items are deferred, ask the user:

```
All items resolved. Close issue #{number}? (Y/N/close with comment)
```

If yes, close the issue using the available GitHub tools (owner, repo, issue_number, state: "closed", state_reason: "completed").

### Step 3.5: Present Summary

```
Issue #{number} Resolution Summary

| # | Type | Decision | Reply Posted? |
|---|------|----------|---------------|
| 1 | action-item | Accepted | Yes |
| 2 | question | Answered | Yes |
| 3 | feedback | Acknowledged | Yes |

Replies posted: X
Code changes: {commit hash or "none"}
New issues created: {links or "none"}
Issue state: {open/closed}

Deferred items:
- {description} — {new issue link}
```

---

## Resuming Interrupted Processing

### Interrupted During Triage (Phase 2)

1. Check for existing resolution map at `plans/{branch-name}/issue-{number}-resolution-map.md`
2. If found, read it and present current progress
3. Check the todo list for pending items
4. Offer to continue from the next untriaged comment

### Interrupted During Execution (Phase 3)

1. Read the resolution map to see which replies have been posted
2. Check GitHub issue comments for `**[Claude Code]:**` replies already posted
3. Resume from the next unposted reply
