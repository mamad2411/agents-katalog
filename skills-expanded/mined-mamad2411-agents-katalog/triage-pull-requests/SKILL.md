---
name: triage-pull-requests
description: Orchestrates review of one or more GitHub PRs in parallel using subagents. Produces a triage summary table with Critical/Suggestion/NIT findings per PR, then posts reviews (approve/comment/request-changes) based on user decisions. Use when the user asks to review multiple PRs, review PRs in parallel, or batch-review PRs across repos.
allowed-tools: "Bash(gh repo*), Bash(gh search*), Bash(gh api*), Bash(gh pr*), Read"
argument-hint: [owner/repo#n ...]
---

# Triage Pull Requests

Thin orchestrator. All review methodology lives in **review-pull-request**. All `gh` commands live in **github**.

## Input

Accepts any mix of:
- Full URL: `https://github.com/owner/repo/pull/123`
- `owner/repo#n`: `owner/repo#123`
- Bare `#n`: infer repo from current workspace git remote (`gh repo view --json nameWithOwner`)

## No PR list provided (discover PRs)

If the user asks to "review my assigned PRs" without listing them, discover candidates and then filter to **direct** review
requests (you as a User, not just your team) and **exclude drafts**:

- Candidate list (infer owner from current git remote, or prompt user if no git context):

```bash
# Infer owner from current repo
OWNER="$(gh repo view --json owner --jq .owner.login 2>/dev/null)"
# Fall back to prompting user if not in a git repo
gh search prs --owner="${OWNER}" --state=open --review-requested=@me --sort updated --order desc --json number,title,url,repository --limit 50
```

- Filter per PR (keep only when `isDraft == false` AND `reviewRequests` contains your login as a `User`):

```bash
LOGIN="$(gh api user -q .login)"
gh pr view <n> --repo <owner/repo> --json isDraft,reviewRequests

# reviewRequests contains both Teams and Users; filter to Users via __typename
gh pr view <n> --repo <owner/repo> --json reviewRequests --jq \
  --arg login "$LOGIN" \
  'any(.reviewRequests[]?; .__typename=="User" and .login==$login)'
```

Pass the resulting explicit `owner/repo#n` list into Phase 1.

## Phase 1 — Parallel dispatch

Launch **one subagent per PR in a single message batch** using the Task tool. Each subagent prompt must:
- Read and follow the **review-pull-request** skill (review methodology, backport rules, disclaimer rule)
- Read and follow the **github** skill for all `gh` reads
- Return the structured report defined in review-pull-request's **Subagent output mode** section
- NOT post any GitHub comments

**Subagent permission failure**: Subagents inherit permissions from `settings.json` only — not from tools approved interactively in the parent session. Required rules (`Bash(gh:*)`, `Read`) must be in `settings.json`. If subagents still fail, fall back to running each review directly in the main conversation sequentially. The review methodology and output format are the same.

## Phase 2 — Summary

After all subagents return, present a compact table:

```
| PR                                         | Author  | Verdict       | Critical | Suggestions | NITs |
|--------------------------------------------|---------|---------------|----------|-------------|------|
| [repo#123](https://github.com/...)         | @author | Looks OK      | —        | 1           | 2    |
| [repo#456](https://github.com/...)         | @author | Needs changes | 1        | 0           | 1    |
| [repo#789](https://github.com/...)         | @author | Error: 404    | —        | —           | —    |
```

Always include the PR URL as a markdown link in the PR column.

Then list findings per PR (Critical → Suggestions → NITs → Improvements), aligning with the NIT guidelines in **review-pull-request**. Ask the user for a decision per PR.

## Phase 3 — Decisions

Valid responses (blanket or per-PR):
- `approve`, `approve all that look OK`
- `request-changes`
- `comment` — post a comment without a verdict
- `add NITs then approve`
- `discuss <pr>` — defer to follow-up
- `skip` / `skip all` — do nothing

**Post nothing without an explicit decision.**

## Phase 4 — Post reviews

Use the `### Posting reviews` commands from the **github** skill. Apply the disclaimer rule from the **review-pull-request** skill.

### Inline comments (when requested / when obvious)

If the user asks for "request changes with the mentioned comments" (or otherwise wants feedback attached to the code),
prefer **inline review comments** at the relevant lines instead of only a summary body.

- Use the github skill's "Inline comments via REST API" recipe (`POST /pulls/<n>/reviews`) to attach per-line comments.
- If you already submitted a `CHANGES_REQUESTED` review, you can add a follow-up `COMMENT` review with inline comments (keeps the verdict intact).
- Keep the summary review body short and point at the inline comments (avoid duplicating full text in multiple places).
- Only leave inline comments on lines **actually changed by the PR** (avoid commenting on unchanged context shown in hunks).
