---
name: create-mcp
description: Add a new MCP server to all AI tool configs. Use when user says "add MCP server", "new MCP server", "create MCP", "add tool to MCP", or wants to register a new MCP server across Claude Code, Codex, Cursor, and OpenCode.
---

# Add MCP Server

Add a new MCP server to all AI tool config files, keeping the cross-tool inventory in sync.

If the project documents its own MCP architecture and credential conventions, read that documentation first.

## Instructions

### Step 1: Gather Server Details

Determine the following from the user's request or by asking (one round max):

1. **Name** -- kebab-case server identifier (e.g., `my-tool-local`, `my-tool-stg`)
2. **Tier** -- 1 (third-party image), 2 (custom CLI wrapper, if the project ships one), or custom (Node.js/uv script)
3. **Environment** -- Local or Staging (staging names should include a tenant or environment identifier)
4. **Transport** -- stdio (Docker/Node/uv command) or HTTP (url + headers)
5. **Access mode** -- read-only or read-write
6. **Docker image or command** -- what runs the server
7. **Environment variables** -- which env vars are needed, which are secrets
8. **Guardrails** (Tier 2 only) -- allowed patterns, blocked patterns, strip args, prepend args

### Step 2: Add to `.mcp.json` (Claude Code -- the reference config)

This is the authoritative definition. All other configs are ports of this.

Add the server entry under `mcpServers`. Include a `_comment` field describing tier, environment, access mode, and prerequisites.

Key conventions:
- Use `${VAR:-default}` for env var substitution with defaults
- Use `${VAR:-}` (empty default) for credential-driven activation
- Docker servers use `"type": "stdio"`, `"command": "docker"`, `"args": ["run", "-i", "--rm", ...]`
- Pass env vars to Docker with `-e VAR_NAME` in args + matching `env` block
- Shared repo configs should use `node scripts/run-npx-mcp.mjs ...` instead of raw `npx ...` for stdio servers launched via npm shims
- HTTP servers use `"type": "stdio"` with `node scripts/run-npx-mcp.mjs -y mcp-remote ...` proxy (not direct HTTP)

See `references/config-formats.md` for the exact template.

### Step 3: Add to `.codex/config.toml` (Codex)

Translate the Claude config to TOML format:
- `command` and `args` are TOML key/value pairs
- `env` becomes `[mcp_servers.<name>.env]` table
- JSON arrays in env values need careful TOML string escaping
- HTTP servers use `url` + `http_headers` (no `npx mcp-remote` wrapper)
- Secret-bearing stdio servers should use `scripts/mcp-secret-bridge.mjs` so repo config can map canonical user-level secret names into the child env names expected by the server
- If the child command would be raw `npx`, invoke `node scripts/run-npx-mcp.mjs ...` instead so native Windows works from the shared config
- Add `[mcp_servers.<name>.tools.<tool>]` sections with `approval_mode = "approve"` if tools need gating

Only keep static non-secret values in repo `env` tables. The bridge handles secret remapping and any user-level secrets file the project uses as fallback.

See `references/config-formats.md` for the exact template.

### Step 4: Add to `.cursor/mcp.json` (Cursor)

Translate the Claude config to Cursor format:
- Same JSON structure as Claude but no `type` field, no `_comment`
- Secret-bearing stdio servers should use `scripts/mcp-secret-bridge.mjs`
- If the child command would be raw `npx`, invoke `node scripts/run-npx-mcp.mjs ...` instead
- Only keep static non-secret values in the Cursor `env` block
- Do not reintroduce repo-local `.cursor/mcp.env`

See `references/config-formats.md` for the exact template.

### Step 5: Add to `opencode.json` (OpenCode)

Translate the Claude config to OpenCode format:
- `command` is a single array: `["docker", "run", "-i", "--rm", ...]` (command + args combined)
- `environment` replaces `env`
- `type: "local"` for stdio, `type: "remote"` for HTTP
- HTTP servers use `url` + `headers` directly (no proxy)
- Secret-bearing stdio servers should use `scripts/mcp-secret-bridge.mjs`
- If the child command would be raw `npx`, invoke `node scripts/run-npx-mcp.mjs ...` instead
- Only keep static non-secret values in the OpenCode `environment` block

See `references/config-formats.md` for the exact template.

### Step 6: Update Documentation

If the project maintains an MCP inventory doc, update it:

1. **Server Inventory table** -- add a row with server name, tier, environment, access mode, prerequisites, and description
2. **Cross-Tool Server Mapping table** -- add a row showing which tools have the server (use checkmark or `--`)
3. **Environment Variables Reference table** -- add rows for any new env vars with description and which server uses them

### Step 7: Update Credential Examples

If the server requires credentials:

1. Document required env vars per tool config in whatever the project's MCP docs are
2. **Canonical bootstrap template** -- if the project uses a shared secret-bootstrap script, add the canonical variable there
3. **OpenCode / Cursor / Codex bridge** -- ensure the canonical variable is covered by the bridge profile and any config examples when relevant

### Step 8: Verify

- Confirm server name follows the project's naming conventions (e.g., includes a tenant/environment identifier for staging)
- Confirm all 4 config files are syntactically valid (no trailing commas in JSON, valid TOML)
- Confirm the server entry is consistent across all configs (same Docker args, same env vars)
- For Tier 2 servers, confirm guardrail mode is correct (open, allowlist-only, or blocklist-only -- never both)

## Critical Rules

- `.mcp.json` is the **reference config** -- define the server there first, then port to other formats
- **Never use both allowed and blocked patterns** on the same Tier 2 server -- pick one mode
- **Staging servers include a tenant/environment ID** in the name (e.g., `stg-tenant-region`, not bare `staging`)
- **Canonical secret names live outside the repo** -- preserve user-level canonical names rather than rewriting them per server
- **Cursor secret-bearing stdio servers should use the bridge** -- do not add `.cursor/mcp.env` back or rely on launch-env-only secret wiring
- **OpenCode secret-bearing stdio servers should use the bridge** -- do not add `.opencode/secrets/*` requirements back or rely on launch-env-only secret wiring
- **Codex secret-bearing stdio servers should use the bridge** -- do not reintroduce repo-specific secret tables in `~/.codex/config.toml`
- **Docker Desktop networking**: use `host.docker.internal` (not `localhost`) for host ports accessed from Docker containers on macOS/Windows

## Checklist

- [ ] Server added to `.mcp.json` with `_comment`, correct transport, env vars
- [ ] Server added to `.codex/config.toml` with TOML-translated config
- [ ] Server added to `.cursor/mcp.json` (or documented why skipped)
- [ ] Server added to `opencode.json` with OpenCode-format translation
- [ ] Project's secret-bootstrap script updated (if a new canonical secret is needed)
- [ ] Project's MCP inventory doc updated (if maintained)
- [ ] Cross-Tool Server Mapping updated
- [ ] Environment Variables Reference updated (if new vars)
- [ ] Credential examples updated in all tool sections

## Reference

- `references/config-formats.md` -- per-tool config templates
- `.mcp.json` -- Claude Code reference config (authoritative)
- `.codex/config.toml` -- Codex config
- `.cursor/mcp.json` -- Cursor config
- `opencode.json` -- OpenCode config
