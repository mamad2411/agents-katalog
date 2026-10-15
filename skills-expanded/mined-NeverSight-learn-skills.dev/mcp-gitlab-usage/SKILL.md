---
name: mcp-gitlab-usage
description: (NS) Guides correct usage of GitLab MCP tools for planning, milestones, issues, merge requests, delivery reports, and board sync. Use whenever the user mentions GitLab, MCP GitLab, create issues, start planning in GitLab, delivery report, issue comments, set_issue_labels, merge requests, or execution sync — even if they do not name this skill. Do NOT hand-craft issue payloads or skip confirmation gates. Do NOT use for non-GitLab project management.
depends:
  - nextstage-harness
---

# MCP GitLab Usage

Binding rules for GitLab MCP tool invocation. Tool schemas and detailed flows live in references — read them before calling tools.

## Harness discovery

See `../nextstage-harness/references/harness-discovery.md`. For GitLab product config (status labels, project ids), read `{product_root}/docs/context/gitlab-sync-config.md` when it exists.

## FIRST ACTION (critical)

When the human asks for requirements, planning, or issues in GitLab:

1. **Your first action** must be `start_execution_planning` with inferred arguments. Do not output planning text, RF suggestions, or issue descriptions before a tool response.
2. **If MCP tools are unavailable:** Say exactly that GitLab MCP is not available in this context. Do not output payloads that cannot be executed.

## First access and version check

When connecting to a GitLab MCP server that exposes `get_mcp_gitlab_skill`:

1. Call with `check_version: true` only.
2. Compare server version to any local MCP skill copy if present.
3. Call with `for_update: true` only when missing or versions differ.
4. Do not pass `check_version` and `for_update` together.

## Mandatory practices

- **Always pass `arguments`** — never call tools with empty required fields.
- **Read tool schema** before each unfamiliar call.
- **Never shortcut planning** — run the full MCP flow; do not return "payloads for you to apply."
- **Project discovery:** `git remote get-url origin` → send path to MCP → use numeric `project_id` after human confirms full trio (`id`, `name`, `path_with_namespace`).

## Confirmation gates (non-negotiable)

Cannot be inferred from context:

| Flag                        | Set `true` only after                                      |
| --------------------------- | ---------------------------------------------------------- |
| `requirements_confirmed`    | Human says yes to validating requirements                  |
| `projects_confirmed`        | Human confirms all project trios (main, backend, frontend) |
| `issues_creation_confirmed` | Human says yes to "Should I create the issues in GitLab?"  |

A broad request ("do everything") is **not** confirmation.

## Execution sync (status labels)

Three-step cycle per issue — never skip the middle step:

```
status_backlog → status_in_progress → status_done
```

Read label names from `gitlab-sync-config.md` or discover via `list_project_labels`. Full flow: `references/flows.md`.

## Delivery report

1. Confirm issue target (`project_id` + `issue_iid` or URL).
2. Summarize diff vs agreed base branch.
3. `add_issue_comment` with `internal: true`.

## Related skills

- **Board sync during implementation:** `gitlab-board-sync` (do not duplicate status sync rules here).
- **Issue execution workflow:** `execute-gitlab-issue`.

## References

| File                                                 | When to read                                              |
| ---------------------------------------------------- | --------------------------------------------------------- |
| `references/tool-catalog.md`                         | Before any tool call — required args and examples         |
| `references/flows.md`                                | Planning, issue creation, execution sync, delivery report |
| `../nextstage-harness/references/gates.md`           | SDD planning gates                                        |
| `../nextstage-harness/references/artifact-layout.md` | `requirements.md` and version paths                       |

## Error handling — STOP

On `Plan limit exceeded` or similar hard MCP errors: stop all GitLab operations, inform the human, wait for guidance. No workarounds.
