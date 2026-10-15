---
name: doc-n-fix
description:
  Processes PR review feedback into a prioritized checklist, documents it to a
  user-chosen destination, then fixes issues one by one with progress tracking.
  Use when user says "doc-n-fix", "fix review comments", "address feedback",
  "work through PR review", or "fix PR comments".
allowed-tools:
  - Bash
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - Task
  - AskUserQuestion
---

# Doc-n-Fix

Gather PR review feedback, document it as a prioritized checklist, then fix issues one by one -- checking them off as you go.

## Workflow

Follow all 7 steps sequentially.

### Step 1: Identify the PR

1. Parse the invocation from everything after `/doc-n-fix`:
   - `/doc-n-fix` (bare) -- auto-detect from current branch
   - `/doc-n-fix 42` or `/doc-n-fix #42` -- specific PR number
   - `/doc-n-fix https://github.com/owner/repo/pull/42` -- PR URL
   - `/doc-n-fix --manual` -- user will paste feedback directly (skip GitHub gathering)

2. **Auto-detect** (bare invocation or PR number):

   ```bash
   gh pr view --json number,title,url,body,headRefName,state
   ```

   For a specific PR number, append the number: `gh pr view {number} --json ...`

3. **PR state gate** -- if `state` is `MERGED` or `CLOSED`, report "PR #{number} is {state} -- nothing to fix." and **STOP**.

4. **Edge cases:**
   - **Not a git repo** -- report "Not a git repository." and stop.
   - **`gh` not installed or not authenticated** -- suggest `gh auth login` and stop.
   - **No open PR for current branch** -- use `AskUserQuestion` to ask for a PR number, URL, or `--manual`.

5. Store PR metadata: `number`, `title`, `url`, `headRefName`, `state`.

### Step 2: Gather Review Feedback

#### GitHub path

Run a single Bash call to get repo info:

```bash
gh repo view --json owner,name
```

Then run 3 parallel Bash calls to collect all review types:

```bash
gh pr view {number} --json reviews
```

```bash
gh api --paginate repos/{owner}/{repo}/pulls/{number}/comments
```

```bash
gh pr view {number} --json comments
```

**Error handling** -- if any `gh` command fails, route by error:

| Error                      | Action                                                   |
| -------------------------- | -------------------------------------------------------- |
| 404 Not Found              | PR number is wrong or repo mismatch -- report and STOP    |
| Authentication / 401 / 403 | Suggest `gh auth login` and STOP                         |
| Rate limit / 429           | Report "GitHub rate limit hit -- wait and retry" and STOP |
| Other errors               | Print the raw error message and STOP                     |

Combine all feedback into a single list. Deduplicate using these explicit criteria:

1. **Same `id`** -- exact duplicate, keep one copy
2. **Same `path` + `line` + `author`** -- merge into one item, keep the newest body
3. **Thread grouping** -- comments linked via `in_reply_to_id` collapse to a single item

**DO NOT** deduplicate based on similar body text alone -- reviewers may intentionally leave similar comments on different locations.

**Empty feedback gate** -- if all 3 sources return zero comments/reviews, use `AskUserQuestion`: "No review feedback found. Options: (1) Switch to --manual mode and paste feedback, (2) Stop."

#### Manual path (`--manual`)

Use `AskUserQuestion` to ask the user to paste their review feedback. Parse using these rules:

- Split on numbered lists (`1.`, `2.`), bullet points (`-`, `*`), or blank-line-separated paragraphs
- Extract file/line references via patterns: `file.ts:42`, `line 42`, `in foo.ts`, `at line N`
- If the text is completely unstructured with no clear item boundaries, present as a single item and let the user split it during Step 3 validation

### Step 3: Build the Deliverables List

Parse all feedback into fix items. For each item, extract:

| Field       | Description                         |
| ----------- | ----------------------------------- |
| `#`         | Sequential number                   |
| Description | What needs to change                |
| Source      | `@author` who left the comment      |
| Location    | `file:line` when available          |
| Priority    | P1, P2, or P3                       |
| Effort      | S (small), M (medium), or L (large) |

#### Priority rules

- **P1 -- Must Fix** -- Correctness, bugs, security, blockers. Signal words: "must", "bug", "broken", "wrong", "blocker", "security", "critical", "fix this"
- **P2 -- Should Fix** -- Substantive improvements, refactoring, error handling, test gaps. This is the default for most comments.
- **P3 -- Nice to Have** -- Style, naming, optional suggestions. Signal words: "nit", "consider", "might want to", "optional", "minor", "style", "suggestion"

#### Grouping

Group related comments into single items:

- Thread replies to the same comment
- Multiple comments about the same logical issue
- Comments on the same code block

#### User validation

Present the list as a markdown table with columns: `#`, `Description`, `Source`, `Location`, `Priority`, `Effort`. Then use `AskUserQuestion` with these options:

- **Looks good** -- proceed as-is
- **Adjust priorities** -- user specifies which items to re-prioritize
- **Add items** -- user adds items not captured from review
- **Remove items** -- user removes items they don't want to fix
- **Merge items** -- user identifies items that should be combined

After each user edit, re-number items sequentially (no gaps). Repeat until the user confirms "Looks good."

### Step 4: Choose Destination & Fix Order

#### Destination

Use `AskUserQuestion` to ask where to write the checklist:

1. **GitHub PR description** -- append a `## Review Checklist` section (Recommended)
2. **GitHub PR comment** -- post as a new comment
3. **Local file** -- save to `REVIEW-{PR#}.md`
4. **Other** -- use `AskUserQuestion` to get the path, use `Write` to create the file, treat subsequent updates like a local file via `Edit`

#### Fix order

Use `AskUserQuestion` to ask what order to fix items:

1. **Priority-first** -- P1 > P2 > P3 (Recommended)
2. **Quick wins first** -- S > M > L within each priority tier
3. **File-grouped** -- group by file to minimize context switching

#### Write the initial checklist

Format the checklist using `- [ ]` items (renders as interactive checkboxes on GitHub):

```markdown
## Review Checklist

**PR:** #{number} -- {title} | **Progress:** 0/{total}

### P1 -- Must Fix

- [ ] **#1** `src/auth.ts:42` -- Fix null check in auth middleware (@reviewer1, S)

### P2 -- Should Fix

- [ ] **#2** `src/api/users.ts:88` -- Extract validation to shared util (@reviewer2, M)

### P3 -- Nice to Have

- [ ] **#3** `src/api/users.ts:12` -- Rename variable for clarity (@reviewer1, S)
```

Write to the chosen destination:

- **PR description**: Read the current body with `gh pr view {number} --json body --jq '.body'`. If `## Review Checklist` already exists, find it and replace everything from `## Review Checklist` to the next `## ` heading or EOF. Otherwise append. Use `Write` to create `/tmp/pr-body-{number}.md`, then run `gh pr edit {number} --body-file /tmp/pr-body-{number}.md`.
- **PR comment**: Use `Write` to create `/tmp/pr-comment-{number}.md`, then run `gh pr comment {number} --body-file /tmp/pr-comment-{number}.md`. Parse the comment URL from the command output, extract the numeric comment ID (last segment of the URL), and store it for Step 6 updates.
- **Local file**: Use `Write` to create the file.

**Important:** Use `Write` tool for all temp files -- **DO NOT** use `echo`, `cat <<EOF`, or shell redirects. Always use `--body-file` or `-F body=@file` (capital F) for `gh` write commands.

### Step 5: Fix Issues

Work through items in the chosen order, one at a time. For each item:

1. **Read context** -- Read the file(s) referenced in the comment. Use `Grep` to find related usages. Understand the surrounding code.

2. **Apply fix:**
   - **Simple fix** (1-2 files, clear intent) -- use `Read` and `Edit` directly.
   - **Complex fix** (touches 3+ files, requires understanding a call chain across 2+ modules, or reviewer references architectural concerns like refactor/redesign/extract) -- spawn a `Task` agent (`subagent_type: general-purpose`) with the fix description, relevant file paths, and reviewer comment as context.

3. **Ambiguity gate** -- if the reviewer's intent is unclear, use `AskUserQuestion` with options:
   - Interpretation A -- {your best guess}
   - Interpretation B -- {alternative reading}
   - **Skip** -- skip this item for now (record `{ item_number, description, reason }` -- used in Step 7)
   - **Ask reviewer** -- post a clarifying question on the original comment

4. **Ask reviewer** option: Use `Write` to create `/tmp/reply-{number}.md` with the clarifying question, then post a reply:

   ```bash
   gh api repos/{owner}/{repo}/pulls/{number}/comments/{comment_id}/replies -F body=@/tmp/reply-{number}.md
   ```

   If this returns 404 (the `comment_id` may be a top-level PR comment, not a review comment), fall back to:

   ```bash
   gh pr comment {number} --body-file /tmp/reply-{number}.md
   ```

5. **Error recovery** -- if a fix fails (edit produces errors, tests break, etc.): revert the affected files with `git checkout -- {files}`, record the item as skipped with reason "fix failed", and proceed to the next item.

### Step 6: Update the Checklist

After each fix, immediately update the checklist:

1. **Toggle the item**: Find the line containing `**#{item_number}**` and change `- [ ]` to `- [x]`.
2. **Update the counter**: Find the `**Progress:**` line and increment the first number.

Destination-specific update method:

- **PR description**: Re-read the full body with `gh pr view {number} --json body --jq '.body'`, find and toggle the item, update the progress counter, use `Write` to create `/tmp/pr-body-{number}.md`, write back via `gh pr edit {number} --body-file /tmp/pr-body-{number}.md`.
- **PR comment**: Re-read the comment via `gh api repos/{owner}/{repo}/issues/comments/{comment_id} --jq '.body'`, update, use `Write` to create `/tmp/pr-comment-{number}.md`, write back via `gh api repos/{owner}/{repo}/issues/comments/{comment_id} -X PATCH -F body=@/tmp/pr-comment-{number}.md`.
- **Local file**: Use `Edit` to toggle the checkbox and update the counter directly.

**Update-failure recovery** -- if the write fails (conflict, stale content), re-read the latest content and retry once. If it still fails, log the error and continue fixing remaining items -- bulk-update the checklist at the end.

Print brief progress after each update:

```
Fix #1 complete: Fix null check in auth middleware -- Progress: 1/5
```

Proceed to the next item automatically -- do NOT ask "continue?" between items.

### Step 7: Completion Summary

After all items are processed, output:

```markdown
## Doc-n-Fix Complete: PR #{number}

**Fixed:** {completed}/{total} | **Skipped:** {skipped}

### Completed

- [x] #1 {description} (P1, S)
- [x] #2 {description} (P2, M)

### Skipped (if any)

- [ ] #3 {description} -- {reason}

## What's Next?

1. **Push changes** -- commit and push all fixes
2. **Re-request review** -- notify reviewer that feedback is addressed
3. **Fix skipped items** -- revisit items that were skipped
4. **Run /check** -- verify the fixes are complete
5. **View diff** -- see all changes made
```

## Guidelines

- **Sequential fixing** -- fix items one at a time. Fixes can affect subsequent fixes; parallel fixing risks merge conflicts with yourself.
- **No auto-commit** -- never commit on behalf of the user. They can use `/commit` after.
- **`Write` tool for all temp files** -- use the `Write` tool to create temp files, include the PR number in the filename (e.g., `/tmp/pr-body-{number}.md`). **DO NOT** use `echo`, `cat <<EOF`, or shell redirects. Pass temp files via `--body-file` or `-F body=@file` (capital F).
- **Replace-in-place for re-runs** -- if `## Review Checklist` already exists in the PR description, replace it. Don't append a second copy.
- **`Task` agents only for complex individual fixes** (3+ files or ambiguous scope) -- keep most fixes fast and direct with `Read`/`Edit`.
- **Respect skips** -- if the user skips an item, mark it as skipped with the reason. Don't revisit it unless asked.
- **Group related comments** -- thread replies and comments about the same issue should be a single checklist item, not separate entries.
- **Temp file cleanup** -- clean up `/tmp/pr-body-{number}.md`, `/tmp/pr-comment-{number}.md`, `/tmp/reply-{number}.md`, and similar temp files after use.
- **Comment ID tracking** -- parse the comment ID from `gh pr comment` output and store it for Step 6 updates. If the stored comment ID becomes invalid, re-fetch via `gh api repos/{owner}/{repo}/issues/{number}/comments --jq '.[] | select(.body | contains("## Review Checklist")) | .id'`.
- **Fail loud on errors** -- DO NOT silently continue with missing data when a `gh` command fails. Always report the error and either STOP or route to a recovery action.
