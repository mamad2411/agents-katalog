---
name: relay
description: Use Code Relay from the current project and branch to orchestrate development and remote verification.
---

# Code Relay

Treat the current Git remote and checked-out branch as the project binding. Use the plugin's project-bind action, show the resolved `repository + ref`, and ask for confirmation before writing project files or pushing.

After binding, create a short-lived checkpoint invitation automatically. Never commit a reusable secret or GitHub token.

For each runbook, implement and locally verify the change, record the merged commit SHA, publish a runbook with explicit commands and expected results, then wait for a matching `runbook_id + source_commit` receipt from the `code-relay-checkpoint` GitHub Actions runner. Summarize `passed` as complete, `failed` as a proposed next iteration, and `blocked` as a user decision point.

Prefer natural language such as “绑定当前工程”“生成目标机加入链接”“查看验证状态” and map these to plugin tools. The `code-relay` CLI is an implementation detail.

Treat `/relay` and `/relay bind` as the concise binding entry point. When the
host supplies the active project context, pass its repository and branch to
`bind_project` automatically and show the resolved binding. If no project
context is available in the current session, ask for the repository and branch
once; never ask the user to select or enter a GitHub App installation ID.

Use `$code-relay:relay status` for an explicit status request.
