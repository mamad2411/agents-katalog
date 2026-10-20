---
alwaysApply: true
description: Linear MCP OAuth, cache-first reads, and validated writes for Core2
---

# Linear (Cursor)

Linear auth is **OAuth via Linear MCP** at `https://mcp.linear.app/mcp`, configured in `.cursor/mcp.json` as server `linear`. There is no `LINEAR_API_KEY` in interactive sessions. `nlt-linear-issues` only validates/caches; it does not call Linear.

## Connect (once per Cursor install / this project)

1. Confirm `.cursor/mcp.json` has `linear.url = https://mcp.linear.app/mcp` (not the deprecated `/sse` path)
2. **Settings → Tools & MCP** — enable **linear** if it shows as disabled
3. On first use, complete browser OAuth (`mcp_auth` on server `linear` if tools are missing)
4. Verify: `list_teams` → expect `TappsCodingAgents`; engineering issues → project `Core2`

## Scope (from `.tapps-mcp.yaml`)

| Field | Value |
|-------|-------|
| Team | `TappsCodingAgents` (key `TAP`) |
| Project | `Core2` |
| Agent assignee | `Claude Agent` |

## Tool names in Cursor

| Task | Tools / skill |
|------|----------------|
| List / triage / backlog | `linear-read` skill → `tapps_linear_snapshot_get` → `list_issues` → `tapps_linear_snapshot_put` |
| Create / update issue | `linear-issue` skill → docs-mcp generate/validate → Linear write → `tapps_linear_snapshot_invalidate` |
| Single issue | `get_issue(id="TAP-###")` — never filtered `list_issues` for one id |

When `nlt-linear-issues` is connected, prefer cache tools before raw `list_issues`. When it is unavailable, use narrow `list_issues` filters (`team`, `project`, `state`, `limit`).

## Assignee policy

Resolve once per session via `list_users`; pick `Claude Agent`. Pass that assignee on every issue write. Never default to the OAuth human.

## Reload after config changes

**Ctrl+Shift+P → Developer: Reload Window** after editing `.cursor/mcp.json` or `.tapps-mcp.yaml`.
