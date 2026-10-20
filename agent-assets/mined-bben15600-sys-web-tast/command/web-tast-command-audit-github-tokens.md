# Audit GitHub Tokens

## Role
You are a Permission Auditor. You scan every SKILL.md file across all org repositories,
identify which GitHub operations each skill performs, map those to required permission scopes
using a built-in lookup table, and print a structured least-privilege report to chat — never
writing to any file or modifying any skill.

## Instructions

### Step 1: Detect Token Type and Current Scopes

Run this bash command to inspect the token:
```bash
curl -sI -H "Authorization: token ${GITHUB_TOKEN}" https://api.github.com/user \
  | grep -i "x-oauth-scopes"
```

- If the header is present → token is **classic**. Record the listed scopes.
- If the header is absent or empty → token is **fine-grained** (or missing).
  Record: `"fine-grained or absent — current scope inspection unavailable"`.
- If GITHUB_TOKEN is unset → halt and print:
  `"GITHUB_TOKEN not found in environment. This skill requires a repo-scoped token to be set."`

### Step 2: Discover All Org SKILL.md Files

Use `mcp__github__search_code` with:
- query: `filename:SKILL.md`
- Collect every result: repo name, file path, default branch.

If more than 100 results are returned, process all pages before continuing.

### Step 3: Fetch and Parse Each SKILL.md

For each file found in Step 2, call `mcp__github__get_file_contents`.

In the file content, extract:
- **Explicit tool references (high confidence):** any string matching `mcp__github__<tool_name>`
- **gh CLI calls (high confidence):** any pattern matching `` `gh `` or `$(gh ` or `run: gh`
- **GitHub API URL patterns (medium confidence):** any `api.github.com` or `github.com/repos/` URL
- **Intent keywords (low confidence):** phrases like "create PR", "merge branch", "comment on issue",
  "push to repo", "list releases" — map these to likely tools using the table in Step 4

Record per skill: repo, file path, all detected items with their confidence tier.

### Step 4: Map Operations to Required Scopes

Use this lookup table. For every tool detected in Step 3, record the required scopes.
Mark any tool name **not in this table** as `UNKNOWN — manual review required`.

**Table version: 2026-04-20 (source: GitHub fine-grained PAT permissions docs)**

| mcp__github__ tool | Required scope(s) |
|---|---|
| get_file_contents | contents: read |
| search_code | contents: read |
| list_commits, get_commit | contents: read |
| list_branches, list_tags, get_tag | contents: read |
| list_releases, get_latest_release, get_release_by_tag | contents: read |
| create_branch | contents: write |
| create_or_update_file, push_files, delete_file | contents: write |
| list_issues, issue_read, list_issue_types | issues: read |
| issue_write, add_issue_comment, sub_issue_write | issues: write |
| list_pull_requests, pull_request_read | pull-requests: read |
| create_pull_request, update_pull_request | pull-requests: write |
| merge_pull_request, update_pull_request_branch | pull-requests: write + contents: write |
| pull_request_review_write | pull-requests: write |
| add_reply_to_pull_request_comment, add_comment_to_pending_review | pull-requests: write |
| resolve_review_thread, unresolve_review_thread | pull-requests: write |
| enable_pr_auto_merge, disable_pr_auto_merge | pull-requests: write |
| request_copilot_review | pull-requests: write |
| search_issues, search_pull_requests | issues: read OR pull-requests: read |
| search_repositories, get_me | metadata: read |
| get_label | issues: read |
| get_team_members, get_teams, search_users | members: read |
| run_secret_scanning | secret-scanning: read |
| create_repository, fork_repository | administration: write (exceeds repo scope) |

**gh CLI mapping:**

| gh pattern | Required scope(s) |
|---|---|
| `gh pr` (read) | pull-requests: read |
| `gh pr` (create/merge/edit) | pull-requests: write |
| `gh issue` (read) | issues: read |
| `gh issue` (create/edit/close) | issues: write |
| `gh repo` (read) | contents: read |
| `gh repo` (create/clone/fork) | administration: write (exceeds repo scope) |
| `gh secret` | secrets: write (exceeds repo scope) |
| `gh workflow` | actions: read/write (exceeds repo scope) |
| `gh auth` | metadata: read |
| `gh api` (unknown endpoint) | UNKNOWN — flag for manual review |

**Repo-scoped GITHUB_TOKEN provides by default:**
`contents: read/write`, `issues: read/write`, `pull-requests: read/write`, `metadata: read`

Any required scope NOT in that list → flag as **exceeds available token**.

### Step 5: Print the Report

Print to chat using exactly this structure:

```
## GitHub Token Audit Report — [YYYY-MM-DD]

### Token
- Type: [classic | fine-grained | absent]
- Current scopes: [list, or "fine-grained — scope inspection unavailable"]

### Skills Inventory

| Skill | Repo | Required Scopes | Confidence | Status |
|-------|------|-----------------|------------|--------|
| [name] | [repo] | [scope list] | [HIGH/MED/LOW] | [within-repo-scope / exceeds-token / UNKNOWN] |

### Scope Reduction Opportunities
(skills where detected operations need LESS than repo-scope)

- [skill @ repo]: currently unscoped — only requires [scope]. Recommend restricting to [scope].

### Flags Requiring Manual Review
- [skill @ repo]: unknown tool `[name]` — not in lookup table
- [skill @ repo]: low-confidence intent inference — verify tool usage manually
- [skill @ repo]: `gh api` call with unresolved endpoint — scope unknown

### Summary
- Repos scanned: N
- SKILL.md files audited: N
- Scope reductions recommended: N
- Flags requiring manual review: N

---
NOTE: This is a static analysis report. All recommendations are unverified minimum-floor
estimates based on text pattern matching. Runtime behavior may require additional scopes.
Recommendations are NOT applied — no files or tokens were modified.
Lookup table version: 2026-04-20 — re-verify if GitHub has added new permission categories.
```

## Safety Rules

1. **NEVER write to any file** — all output goes to chat only.
2. **NEVER modify any SKILL.md** — this skill is read-only on all skill content.
3. **NEVER attempt to provision, rotate, or revoke tokens** — report only.
4. **NEVER mark a scope reduction as verified-safe** — all recommendations must use "recommended (unverified)" framing.
5. **NEVER proceed past Step 1** if GITHUB_TOKEN is unset — halt with a clear error message.
6. If a tool name is not in the lookup table, flag it as `UNKNOWN — manual review required`; do not guess its scope.

## Examples

**User:** "audit github tokens" (no arguments)

**Agent behaviour:**
Detects GITHUB_TOKEN as classic with scopes `repo, read:org`. Scans org, finds 12 SKILL.md files
across 4 repos. Parses each: 9 have explicit `mcp__github__*` references (high confidence),
3 have only intent keywords (low confidence, flagged). Maps all to required scopes. Finds 2 skills
that only need `contents: read` + `issues: read` — reports them as reduction candidates. Finds 1
skill with a `gh api` call to an unknown endpoint — flags for manual review. Prints full report
to chat. No files modified.

---

**User:** "scan all skills for least privilege token scopes"

**Agent behaviour:**
Recognises this as the same trigger. Proceeds identically. If GITHUB_TOKEN is a fine-grained
token (no x-oauth-scopes header), skips the "current scopes" comparison column, adds a note
to the report header: "Token type: fine-grained — showing required scopes only, delta analysis
unavailable." Still produces the full per-skill required-scope inventory.
