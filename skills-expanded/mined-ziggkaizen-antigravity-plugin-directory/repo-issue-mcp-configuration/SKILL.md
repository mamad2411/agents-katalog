---
name: repo-issue-mcp-configuration
description: Reviews optional issue-tracker MCP configuration for Linear and Atlassian/Jira-style workflows. Use when enabling, disabling, validating, or troubleshooting issue tracker MCP servers and their security boundaries.
---

# Repo Issue MCP Configuration

Use this skill when enabling or reviewing issue-tracker MCP connections.

## Included MCP Servers

The plugin includes disabled-by-default MCP entries for:

- `linear`
- `atlassian-rovo`

## Safety Requirements

- Enable only the tracker this repository uses.
- Do not hard-code tokens.
- Prefer OAuth flows where supported.
- Confirm tracker visibility and permissions.
- Confirm whether tools can create, update, close, or comment on issues.
- Do not enable GitHub MCP here; use a dedicated source-control collaboration plugin.

## Workflow

Use `workflows/issue-tracker-mcp-setup-review-workflow.md`.

## Resources

- `resources/mcp-tracker-setup-matrix.md`

## Scripts

This skill owns:

```text
scripts/validate-issue-mcp-config.py
```

Run scripts with `--help` before manual use.
