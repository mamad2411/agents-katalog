---
name: gitopia
description: |
  Gitopia workflow assistant for decentralized git collaboration. Contribute to
  repos, review PRs, hunt bounties, and manage DAO governance using Gitopia MCP
  tools. Use when: "fix issue", "review PR", "find bounties", "create proposal",
  "vote on proposal", "contribute to", "clone from gitopia", "push to gitopia",
  or any Gitopia/decentralized git workflow. Also use when the user references
  gitopia:// URLs, DAO governance, on-chain bounties, or LORE tokens.
---

# Gitopia Workflow Assistant

You have access to 57 Gitopia MCP tools (`mcp__gitopia__*`) for decentralized git
with on-chain governance, bounties, and DAO management. This skill routes you
through opinionated workflows using those tools.

For a full tool reference, read `references/tools.md` in this skill's directory.

## Step 1: Detect Intent

Classify the user's request into one of these modes:

| Mode | Trigger phrases | What happens |
|------|----------------|--------------|
| **contribute** | "fix issue", "send PR", "contribute to", "work on" | Clone, branch, fix, push, PR |
| **review** | "review PR", "check PR", "code review", "look at PR" | Fetch diff, analyze, comment |
| **bounty** | "find bounties", "hunt bounties", "earn rewards", "claim bounty" | Discover, evaluate, pick, fix |
| **govern** | "create proposal", "vote", "DAO members", "governance", "execute proposal" | DAO operations |
| **develop** | "update the skill", "tool changed", "add workflow" | Maintain skill + server code |

If the intent is ambiguous, ask: "Are you looking to contribute code, review a PR,
hunt bounties, or manage DAO governance?"

## Step 2: Setup (all modes)

1. Call `get_user_context` to get identity, wallet address, and DAO memberships.
2. If the user mentions a DAO or org, call `set_active_dao` with the DAO name.
3. Confirm the target repository (owner/name) if not already clear from context.

## Contribute Workflow

Goal: Fix an issue or make a contribution, ending with a merged-ready PR.

### Steps

1. **Understand the problem.** Call `get_issue` with the owner, repo name, and issue IID.
   Read the issue description, labels, and comments to understand what needs fixing.

2. **Get the code.** Call `git_clone` with `repo_url="gitopia://owner/repo"` and
   `local_path="repo-name"`. If the user doesn't have write access, ask whether to
   fork first (`fork_repository`).

3. **Create a feature branch.** Use your built-in git tools to create and checkout a
   branch like `fix/issue-N` or `feat/description`.

4. **Investigate and fix.** Use your built-in file search, read, and edit tools.
   Write tests if the project has a test suite.

5. **Commit and push.** Stage and commit with a message referencing the issue
   (e.g. "fix: resolve issue #N"). Then call `git_push` to publish.

6. **Open a PR.** Call `create_pull_request` with:
   - `owner`, `name`, `title`, `description`
   - `head_branch` (your feature branch)
   - `base_branch` (repo's default branch)
   - `issue_iids` to link the issue

7. **Comment on the issue.** Call `comment_on_issue` to note the PR was submitted.

### Decision Points

At each decision point, use the default unless the user has stated a preference.
After asking, offer: "Want me to use this as your default going forward?"

| Decision | Default | When to ask |
|----------|---------|-------------|
| Fork first or clone directly? | Clone directly | When user may not have write access |
| Base branch? | Repo's default branch | When repo has multiple active branches |
| Link issues to PR? | Yes, link the issue being fixed | Always use default |
| Auto-push after commit? | Yes | Always use default |

## Review Workflow

Goal: Review code changes in a PR and leave actionable feedback.

### Steps

1. **Get PR metadata.** Call `get_pull_request` with owner, name, and pull_iid.
   Note the title, description, author, and linked issues.

2. **Get the diff.** Call `get_pull_request_diff` with the same params.
   This returns unified diffs with per-file addition/deletion stats.

3. **Analyze each file.** For each changed file in the diff:
   - Check for correctness, security issues, and edge cases
   - If you need more context, call `get_file_contents` for the full file
   - Note specific line-level feedback

4. **Post review comments.** Call `comment_on_pull_request` with:
   - General feedback in `body`
   - For inline comments: include `diff_hunk`, `path`, and `position`

5. **Summarize.** Post a final comment with overall assessment: approve or
   request changes, with a summary of findings.

### Decision Points

| Decision | Default | When to ask |
|----------|---------|-------------|
| Post comments on-chain? | Yes | When user might want local-only review |
| Merge after approval? | No, just comment | When user explicitly asks to merge |

## Bounty Workflow

Goal: Find high-value bounties, evaluate them, and execute the fix.

### Steps

1. **Discover bounties.** Call `list_bounties`. Optionally filter by state.

2. **Evaluate top candidates.** For each promising bounty:
   - Call `get_bounty` for full details (amount, expiry, state)
   - Call `get_issue` for the linked issue (complexity, requirements)

3. **Present evaluation.** Show a table with:
   - Bounty ID, amount (in LORE), expiry date
   - Issue title, complexity estimate, skills needed
   - Recommendation: which bounty has the best reward-to-effort ratio

4. **Execute.** When the user picks a bounty, run the Contribute Workflow
   for the linked issue.

### Decision Points

| Decision | Default | When to ask |
|----------|---------|-------------|
| Minimum amount filter? | Show all | When there are many bounties |
| Auto-start contribute after picking? | Yes | Always use default |

## Govern Workflow

Goal: Manage DAO governance — members, proposals, voting, execution.

Detect the sub-intent:

| Sub-intent | Action |
|-----------|--------|
| "list members" | `set_active_dao` then `dao_list_members` with `dao` param |
| "create proposal" | `set_active_dao` then `dao_submit_proposal` with `dao` param, `title`, `summary` |
| "list proposals" | `dao_list_proposals` with `dao` param |
| "vote" | `dao_get_proposal` to show details, then `dao_vote` with `proposal_id` and `option` |
| "execute" | `dao_exec` with `proposal_id` (must have passed) |
| "add/remove member" | `dao_update_members` with `dao` param and `member_updates` |

The `dao` parameter accepts DAO names directly — no need to look up group_id or
group_policy_address first. The server resolves internally.

## Develop Workflow

Goal: Maintain the gitopia-mcp-server and keep this skill in sync.

When working on the MCP server codebase:

### After adding or modifying tools
1. Update `references/tools.md` with the new/changed tool
2. Update `toolTrustRequirements` in `internal/handler/trust.go`
3. Update trust tests in `internal/handler/trust_test.go`
4. If tool belongs to a toolset, update `toolsetMembership` in `internal/handler/toolsets.go`
5. Add unit tests in `internal/handler/*_test.go` (dry-run, validation, no-client)
6. Add E2E test case in appropriate `test/e2e/tier*_test.go`

### After finding bugs during skill usage
1. File issue on Gitopia: `create_issue` on `Gitopia/gitopia-mcp-server`
2. Create fix branch: `htrap/fix/description`
3. Fix, test, push to both remotes (origin + gitopia)
4. Create PR: `create_pull_request` linking the issue

### Test commands
- Unit tests: `go test -race ./...`
- E2E tests: `go test -tags integration -v -timeout 10m ./test/e2e/...`
- Rebuild binary: `go build -o server ./cmd/server`
- Rebuild Docker: `docker build -t gitopia-mcp-server:dev .`

## Error Recovery

When a tool call fails, check for these common errors before retrying:

| Error message | Cause | Fix |
|--------------|-------|-----|
| "pending packfile" | Previous push still processing | Wait 15s, retry |
| "account sequence mismatch" | Stale sequence number | Automatic retry (server handles up to 3x) |
| "couldn't find remote ref" | Repository is empty | Use `bootstrap_repo` to create initial content |
| "owner id must consist minimum 3 chars" | Using numeric DAO ID | Pass DAO name instead (fixed in v0.1.1) |
| "invalid assignee" | Username instead of address | Server resolves automatically (v0.1.1+) |
| "pullRequest already exists" | PR already open for this branch | Check existing PRs with `list_pull_requests` |
| "rate limit exceeded" | Too many chain writes | Wait and retry, or use `batch_execute` |

## User Preferences

At each decision point, check if the user has previously stated a preference in
this conversation. If not, ask with the default shown, then offer:

"Want me to use this as your default for the rest of this session?"

If yes, remember the preference and skip asking for that decision going forward.
This lets power users set defaults once and flow through workflows without interruption.
