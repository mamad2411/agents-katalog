---
name: pr-comments-plan
description: Use when triaging unresolved PR review threads — builds a comprehensive implementation plan saved to ./temp for execution in a fresh session.
---

## Address PR Comments

Interactively triage and address unresolved review threads on a GitHub pull request.

### Step 1 — Verify prerequisites

Run this exact command and stop with a clear error if it fails:

```bash
gh --version
```

If `gh` is not installed or the command fails, output:

> **Error:** GitHub CLI (`gh`) is not installed or not on PATH. Install it from https://cli.github.com and run `gh auth login` before using this command.

Then stop. Do not proceed.

### Step 2 — Resolve the PR number

The argument passed to this command is: `$ARGUMENTS`

- If `$ARGUMENTS` contains a number (e.g. `#42` or `42`), use that as the PR number.
- Otherwise, detect the current branch with:

  ```bash
  git rev-parse --abbrev-ref HEAD
  ```

  Then find the open PR for that branch:

  ```bash
  gh pr list --head <current-branch> --state open --json number,title,url --limit 1
  ```

  If no PR is found, output:

  > **Error:** No open PR found for branch `<branch-name>`. Pass the PR number explicitly: `/pr-comments-plan 123`

  Then stop.

### Step 3 — Fetch unresolved review threads

First show the PR title and URL:

```bash
gh pr view <PR> --json number,title,url,headRefName
```

Then run the helper script to fetch and nest all comments:

```bash
node ~/.claude/skills/pr-comments-plan/get_pr_comments.ts <PR>
```

The script outputs a JSON array of root comments. Each object has this shape:

```jsonc
{
  "id": 123,
  "author": "alice",
  "path": "src/foo.ts", // "(general)" for issue-level comments
  "line": 42, // null for issue-level comments
  "body": "...",
  "created_at": "2026-01-01T00:00:00Z",
  "replies": [
    { "id": 456, "author": "bob", "body": "...", "created_at": "..." },
  ],
}
```

Parse the JSON. If the array is empty, output:

> No review comments or unresolved threads found on PR #`<PR>`. Nothing to address.

Then stop.

### Step 4 — Prompt for comment selection

Print a numbered list of all unresolved comments, up to 10 per page:

```
Unresolved comments (page 1 of 2):

  [1]  @alice  src/modules/patient/patient.service.ts:42
       The error here should use ServerError instead of throwing a raw Error.

  [2]  @bob  (general)
       Please add a migration for the new column before this merges.

  ...

  [10] @alice  src/modules/auth/auth.controller.ts:18
       This violates the logger-usage rule — remove the duplicate logger call.
```

Then use `AskUserQuestion` to ask which to address:

```javascript
AskUserQuestion({
  questions: [
    {
      question: 'Which comments would you like to address? (page N of M)',
      header: 'Selection',
      multiSelect: false,
      options: [
        { label: 'All on this page', description: 'Select all comments listed above.' },
        { label: 'None on this page', description: 'Skip all comments on this page.' },
        { label: 'Other', description: 'Type the numbers you want, e.g. 1,3,5' },
        // If more pages remain, add:
        // { label: 'None on this page (more pages follow)', description: '...' }
      ],
    },
  ],
});
```

- **All on this page** — add all comments on this page to the selection; if more pages remain, print the next page and ask again.
- **None on this page** — skip this page; if more pages remain, print the next page and ask again.
- **Other** — the user types comma-separated numbers (e.g. `1,3,5`); parse them, add to selection, then continue to next page if any remain.

After all pages are shown, if nothing was selected across all pages output:

> No comments selected. Exiting.

Then stop.

### Step 5 — Enter planning mode and build the implementation plan

**Switch to planning mode now.** Do not make any code changes in this step — only analyze and plan.

#### 5.1 — Gather structural context with the knowledge graph

For each selected comment, use code-review-graph MCP tools to collect context _before_ reading files directly. **Always use these tools for codebase navigation — never grep or find.** Run these in parallel where independent:

- `mcp__code-review-graph__get_review_context_tool` — full architectural context for the affected file
- `mcp__code-review-graph__semantic_search_nodes_tool` — find the relevant function/class by name or keyword from the comment body
- `mcp__code-review-graph__get_impact_radius_tool` — understand what else is affected if this code changes
- `mcp__code-review-graph__query_graph_tool` with `pattern: "callers_of"` — find all callers of the function being changed
- `mcp__code-review-graph__query_graph_tool` with `pattern: "tests_for"` — check whether the affected code has tests

Fall back to `Read` with a specific line range only for exact line content the graph cannot provide (e.g. SQL queries, schema literals). Never use `Grep` or `Bash(grep/find)` for codebase exploration.

#### 5.2 — Read the affected files and evaluate each comment

Read each file referenced by a selected comment once. Use the graph-resolved locations from 5.1; do not rely solely on the line numbers from the comment (they may have drifted). Note the current surrounding context for each change site.

For each comment, apply the `receiving-code-review` evaluation before writing the proposed change:
- Verify the suggestion is technically correct for this codebase
- YAGNI-check: grep for actual usage if the suggestion adds or removes a feature
- Check whether the suggestion conflicts with the developer's prior architectural decisions
- If the suggestion seems wrong or unclear, note it in **Convention notes** and flag it for the developer rather than planning a blind implementation
- Push back is valid — if the reviewer is wrong, the plan should say so with technical reasoning

Also assess whether the review thread itself is a signal that an inline comment is warranted (per `comment-keeper` Rule 3). Flag it if:
- The discussion explains a non-obvious WHY (a business rule, a constraint, a workaround) that isn't visible in the code
- There was back-and-forth or pushback that resolved into a decision — the resolution reasoning belongs near the code
- The reviewer had to ask for clarification because the code's intent was unclear

If flagged, draft the inline comment text in the **Inline comment to add** field of the plan section.

#### 5.3 — Cross-reference project conventions

Check whether each comment touches a known convention:

- `CLAUDE.md` — architecture rules, naming, config patterns
- `.claude/rules/` — all rule files
- TypeBox schema patterns, `BaseController`/`BaseService`/`BaseRepository` contracts, `ServerError` usage

Flag any comment where the reviewer's suggestion would itself violate a project convention — note the conflict in the plan.

#### 5.4 — Check whether the PR description needs updating

Fetch the current PR description:

```bash
gh pr view <PR> --json title,body
```

Compare the description against the changes being planned for each selected comment. Ask: does the existing description accurately reflect what the PR does after these changes land?

- **If yes** — note "PR description is current" in the plan and move on.
- **If no** — add a note in the plan (see § 5.5) recommending `/update-pr-description` be run before merging, with a one-sentence reason.

#### 5.5 — Compile the plan document

First, detect the worktree root:

```bash
git rev-parse --show-toplevel
```

Store the result as `<REPO_ROOT>`. Ensure the `temp/` directory exists:

```bash
mkdir -p <REPO_ROOT>/temp
```

Then write the full plan to `<REPO_ROOT>/temp/pr-<PR-number>-plan.md` using the **Write** tool (not a bash redirect). Use the following structure — one section per comment, followed by a parallelism note and a pre-commit checklist.

**File header:**

- `# PR #<number> — Implementation Plan`
- `**Branch:** <headRefName>`
- `**Generated:** <ISO date>`
- `**Comments selected:** <N>`

**Per-comment section (repeat for each comment):**

Each field must be separated by a blank line so markdown renders it as a block (not a tight list). Use this exact layout:

```markdown
## Comment [N/total]

**Comment ID:** <id>

**Reviewer:** @<author>

**File:** [<path>](../<path>)

**Location:** <function or class name> — line <line>

**Comment:**

> <full comment body>

**Current code (relevant excerpt):**

```<lang>
<relevant lines>
```

**Callers affected:** <list from graph, or "none / not applicable">

**Tests covering this code:** <list from graph, or "none found">

**Convention notes:** <any rule from CLAUDE.md or .claude/rules/ that applies; flag conflicts>

**Proposed change:**

- <bullet 1>
- <bullet 2>
- …

**Inline comment to add:** <drafted comment text, or "none">

**Suggested reply draft:**

<1–2 sentences>

Written with Claude Code
```

- `**Location:**` — use the function name, not just the line number, so it survives rebases
- `**Inline comment to add:**` — draft only if the thread surfaced a non-obvious WHY (business rule, constraint, workaround) per `comment-keeper` Rule 3; otherwise write "none"
- `**Suggested reply draft:**` — must end with a blank line then `Written with Claude Code` on its own line

**Closing sections:**

- `## PR description` — either "PR description is current — no update needed" or "Run `/update-pr-description` before merging — <reason>"
- `## Parallelism recommendation` — if N >= 2, note which comments can be addressed concurrently (no overlapping files) vs. which must be sequential (same file — edits shift line numbers)
- `## Pre-commit checklist` — `pnpm lint:fix` passes, plus any convention checks identified above

#### 5.6 — Present the plan for review

Tell the developer:

> Plan written to `<REPO_ROOT>/temp/pr-<number>-plan.md`. Please review it — open the file, edit any section you disagree with, then let me know when it's ready.

Use `AskUserQuestion` to ask:

```
Question: "Is the plan ready to execute?"
Options:

- "Yes, run /pr-comments-address <REPO_ROOT>/temp/pr-<number>-plan.md in a new session"
- "I'll edit it first — check back when I say ready"
```

- If **"Yes"**: proceed to Step 7.
- If **"I'll edit it first"**: stop here. The developer will start the address session manually.

### Step 7 — Hand off to execution session

Output the following block verbatim so the developer can copy it:

```
Context is now spent on planning. Start a fresh session to keep the full context budget for implementation:

/pr-comments-address <REPO_ROOT>/temp/pr-<number>-plan.md

The plan file contains everything the address command needs: file locations, proposed changes, reply drafts, and the pre-commit checklist.
```

Then stop. Do not make any code changes.
