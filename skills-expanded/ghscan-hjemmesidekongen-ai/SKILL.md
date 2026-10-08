---
name: bitbucket-basics
description: >
  Bitbucket PR creation, pipeline status checks, and code review actions via
  the Atlassian MCP server. Use when creating pull requests, checking CI/CD
  pipeline status, adding PR comments, approving PRs, listing open PRs, or
  performing branch operations against a Bitbucket Cloud or Data Center
  workspace.
user_invocable: false
interactive: false
depends_on: []
reads: []
writes: []
model_tier: senior
triggers:
  - "bitbucket"
  - "create pr"
  - "check pipeline"
  - "bitbucket pr"
checkpoint:
  type: data_validation
  required_checks:
    - name: "mcp_available"
      verify: "Atlassian MCP server is reachable before any Bitbucket operation"
      fail_action: "Surface MCP unavailability message and stop — do not fabricate results"
    - name: "workspace_resolved"
      verify: "Bitbucket workspace slug is known before issuing any API call"
      fail_action: "Ask user for workspace slug or read from local git remote"
    - name: "pr_fields_complete"
      verify: "PR creation includes title, source branch, target branch, and description"
      fail_action: "Prompt for missing fields before calling create_pull_request"
    - name: "pipeline_result_surfaced"
      verify: "Pipeline status is reported with step-level detail, not just overall state"
      fail_action: "Fetch step details and include pass/fail breakdown in output"
_source:
  origin: "kronen"
  inspired_by: "D-029 decisions"
  ported_date: "2026-03-10"
  iteration: 1
  changes: "New MCP interaction skill for Bitbucket"
---

# bitbucket-basics

Bitbucket operations via the Atlassian MCP server. Covers PR lifecycle, pipeline
monitoring, and code review actions.

## MCP requirement

This skill requires the Atlassian MCP server. If it is not available:

> "The Atlassian MCP server is not connected. To use Bitbucket operations, add
> the server to your MCP config and restart Claude Code. See references/process.md
> for setup instructions."

Do not attempt to substitute with REST calls or fabricate results.

## Operations

| Operation | MCP tool | Key inputs |
|-----------|----------|------------|
| Create PR | `create_pull_request` | workspace, repo, title, source, target, description |
| List open PRs | `list_pull_requests` | workspace, repo, state=OPEN |
| Check pipeline | `get_pipeline` / `list_pipeline_steps` | workspace, repo, pipeline_uuid |
| Add PR comment | `create_pull_request_comment` | workspace, repo, pr_id, content |
| Approve PR | `approve_pull_request` | workspace, repo, pr_id |
| Branch ops | `create_branch` / `delete_branch` | workspace, repo, branch name |

## Key rules

- Always resolve workspace slug from `git remote -v` before asking the user.
- PR descriptions must follow the structured template in `references/process.md`.
- Report pipeline failures with step-level detail — overall "FAILED" is not enough.
- Never approve a PR in the same session that created it.
- Destructive ops (branch delete, PR decline) require explicit user confirmation.

## Process

Full workflows, error handling, and anti-patterns: `references/process.md`.
