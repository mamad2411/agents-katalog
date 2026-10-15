---
name: arc-parallel-implement
description: "Implements multiple planned user stories in parallel using subagents. Each story gets its own branch, commit, and PR. Use when asked to implement multiple issues, execute a batch of stories, or build several features at once."
---

# Parallel Story Implementation

Spawns concurrent subagents via the Task tool to implement multiple user stories simultaneously, each on its own feature branch with isolated commits and PRs.

## When to Use

- User says "implement all plans", "build these stories", "execute issues #X, #Y, #Z"
- Multiple independent stories/issues are ready for implementation (plans exist)
- Stories touch different files or different layers with minimal overlap

## When NOT to Use

- Stories have sequential dependencies (one must merge before the next can start)
- Stories modify the same files heavily (merge conflicts are likely)
- Only one story — just implement it directly, no subagent needed

## Prerequisites

Before spawning subagents, verify:

1. **Plans exist** — Each story must have an implementation plan (issue comment, plan file, or inline spec). If not, use `arc-planning-work` first.
2. **Stories are independent** — Review file overlap. If two stories edit the same file, implement them sequentially or plan non-overlapping edits.
3. **Main is clean** — `git status` shows no uncommitted changes that would conflict.
4. **Tests pass** — Run the project's test suite on main before starting.

## Workflow

### Step 1: Gather Context

For each story, collect:
- Issue number and title
- Implementation plan (from issue comments or plan files)
- Target branch name (e.g., `feat/W-XXXXXX-short-description`)
- Files to modify/create
- Test commands to verify

```bash
gh issue view <number> --json title,body,labels
gh issue view <number> --comments --json comments
```

### Step 2: Check for File Conflicts

Build a file map across all stories. Flag overlaps:

| Story | Files Modified |
|-------|---------------|
| #5    | useWeather.ts, weatherCache.ts (new), App.tsx, Dashboard.tsx |
| #30   | MapView.tsx, MapView.test.tsx |
| #17   | WeatherPanel.css, Dashboard.css, index.html |

If overlap exists:
- **Minor overlap** (e.g., adding a prop to a shared component): Include the shared change in only ONE task, note the dependency
- **Heavy overlap**: Implement sequentially, not in parallel

### Step 3: Spawn Subagents

Use the `Task` tool to launch one subagent per story. Each task prompt must include:

1. **Full context** — Don't assume the subagent has prior conversation history
2. **The implementation plan** — Copy the complete task list from the plan
3. **Branch name** — The exact branch to create
4. **File contents or locations** — Tell the subagent which files to read
5. **Test commands** — How to verify the implementation
6. **Commit message** — The exact semantic commit message to use
7. **Constraints** — Do NOT commit/push, do NOT modify files outside scope

#### Task Prompt Template

```
## Task: Implement Issue #<N> — <Title>
**Branch:** `feat/W-XXXXXX-short-description`

### Context
- [Project tech stack, test framework, conventions]
- [Relevant architectural context the subagent needs]

### Implementation Plan
[Paste the full plan task list here]

### Files to Read First
- [List key files the subagent should read before editing]

### Verification
- Run `<test command>` — all tests must pass
- Run `<lint command>` — no new errors
- Run `<typecheck command>` — clean
- Run `<build command>` — builds successfully

### Commit
Do NOT commit or push. Just make changes and verify tests pass.

### Report
When done, report: files changed, tests added, test results.
```

Launch all tasks in a **single assistant message** so they run concurrently:

```
<Task prompt="...story A...">
<Task prompt="...story B...">
<Task prompt="...story C...">
```

### Step 4: Verify Combined State

After all subagents complete:

1. Run the full test suite: `npm run test:run` (or project equivalent)
2. Run typecheck: `npx tsc --noEmit`
3. Run build: `npm run build`
4. Review `git status` to see all changed files

### Step 5: Create Branches and Commits

For each story, isolate its files onto a dedicated branch:

```bash
# Stash everything
git stash --include-untracked

# For each story:
git checkout main
git checkout -b feat/W-XXXXXX-short-description
git stash pop
git add <story-specific-files>
git commit -m "feat: <description>

<body>

Closes #<N>"
git stash  # re-stash remaining files
```

**Important:** If subagent changes overlap (e.g., both modified App.tsx), handle the shared file carefully — include it in the story that owns the primary change.

### Step 6: Push and Create PRs

For each branch:

```bash
git push -u origin feat/W-XXXXXX-short-description

gh pr create \
  --base main \
  --head feat/W-XXXXXX-short-description \
  --title "feat: <short title>" \
  --body "## Summary
<what changed>

## Related Issue
Closes #<N>

## Changes
- <file1>: <what changed>
- <file2>: <what changed>

## Testing
- <N> new tests added
- All <total> tests passing"
```

### Step 7: Verify PRs

```bash
gh pr list --state open --json number,title,headRefName
```

## Branch Naming Convention

Follow the project's convention. Default: `feat/W-XXXXXX-short-description`

## Commit Convention

Use semantic commits per `arc-conventional-commits`:
- `feat:` for new features
- `fix:` for bug fixes
- `test:` for test-only changes

Include `Closes #N` in the commit body to auto-close the issue on merge.

## Rules

- **Never modify files outside a story's scope** in a subagent
- **Never commit on main** — always use feature branches
- **Never use `git add .`** — only stage story-specific files
- **Always verify tests pass** before and after subagent work
- **Always include full context** in task prompts — subagents have no memory of the parent conversation
- **Report back to the user** with a summary table of branches, test counts, and PR links after all work is complete

## Error Handling

- If a subagent fails tests: fix the failing story manually, don't re-run all subagents
- If file conflicts exist after subagents: resolve manually, commit the resolution on the affected branch
- If a story is more complex than expected: implement it directly instead of via subagent

## Output Format

After completion, report to the user:

| Branch | Issue | Tests | Files | PR |
|--------|-------|-------|-------|----|
| `feat/W-000005-...` | #5 | 149 (12 new) | 7 files | #61 |
| `feat/W-000027-...` | #30 | 141 (4 new) | 2 files | #62 |
| `feat/W-000017-...` | #17 | 137 | 3 files | #63 |
