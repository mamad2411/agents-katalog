---
name: mcphub-operator
description: >-
  Operate MCPHub groups, endpoints, compression, and CLI from repo registry.
  Use for hub preflight, group picking, tunnel vs local exposure. NOT harness sync.
license: MIT
metadata:
  author: wyattowalsh
  version: "1.0.0"
user-invocable: true
argument-hint: "[preflight|groups|compression|tunnel|cli|doctor]"
---

# MCPHub Operator

Repo-managed MCPHub control plane: workflow groups, bearer endpoints, optional compression, ChatGPT tunnel policy. Smart Routing stays **off** in tracked config.

**NOT for:** editing the agent-stack sync script, live skills-sync apply installs, or PostgreSQL/pgvector smart-routing setup (use maintainer OpenSpec + explicit user request).

## Dispatch

| `$ARGUMENTS` | Action |
| --- | --- |
| *(empty)* | Show group picker summary, preflight command, and reference index |
| `preflight` / `doctor` | Run `bash scripts/preflight.sh` from skill dir; stop on `fail` |
| `groups` / `picker` | Load [references/group-picker.md](references/group-picker.md) |
| `compression` | Load [references/compression-opt-in.md](references/compression-opt-in.md) |
| `tunnel` | Explain ChatGPT `tunnel` group-only policy + `.env.mcphub` tunnel vars |
| `cli` | Load [references/cli-cheatsheet.md](references/cli-cheatsheet.md) |

## Operator Contract

### `preflight`

1. From repo root (or pass `--cwd` to bundled doctor), run:

```bash
bash skills/mcphub-operator/scripts/preflight.sh
```

2. Stop when JSON `ok` is false or any check with `status: fail` touches settings parity, smart routing, or client profiles.
3. Treat `warn` as advisory (hub not running, bearer unset locally).

### `groups`

1. Default local harnesses attach **`harness`** only, with per-server endpoints available but disabled by default.
2. Treat **`harness`** as the smallest high-signal set for context-bloat control: Brave Search, Context7, DeepWiki, Fetch, and package metadata.
3. Use **`daily`** for routine opt-in expansion; use **`coding`**, **`research`**, **`review`**, or **`release`** for scoped agentic dev flows.
4. Escalate to capability groups (`web-search`, `web-read`, `docs`, `repo`, `browser`, `media`, `design`, `productivity`, `accounts`, `references`) when the task needs that surface.
5. Use **`reasoning`** only for hard problems; keep **`reasoning-lab`** experimental.
6. Attach account-backed, live-browser, heavy, or experimental groups only with explicit user intent.
7. Never attach **`tunnel`** to local harness configs unless testing the remote consumer shape.

### `compression`

1. Tracked `mcp_settings.json` keeps `toolResultCompression.enabled: false`.
2. Opt-in locally via `.env.mcphub` only after user approves; see compression reference.
3. Disable compression when debugging structured tool JSON or investigating truncation.

### `tunnel`

1. ChatGPT remote MCP uses **`tunnel`** group only (`https://mcp.w4w.dev/mcp/tunnel` when tunnel enabled).
2. Do not widen ChatGPT to the global `/mcp` route or per-server endpoints without explicit user request.
3. Tunnel credentials stay in `.env.mcphub` / `~/.cloudflared/` — never commit.

### `cli`

1. Prefer repo recipes: `just mcphub-generate`, `just mcphub-generate-check`, `just mcphub-validate`, `just mcphub-doctor`, `just mcphub-smoke`.
2. Use upstream MCPHub CLI for live hub inspection when the process is running; see CLI reference.

## Maintainer Loop

```bash
just mcphub-generate
just mcphub-generate-check
just mcphub-validate
uv run python skills/mcphub-operator/scripts/check.py
```

Regenerate settings after editing `config/mcp-registry.json` groups or servers.

## References

- [Group picker](references/group-picker.md)
- [CLI cheat sheet](references/cli-cheatsheet.md)
- [Compression opt-in](references/compression-opt-in.md)
- Public maintainer doc: `docs/ai-tools/mcphub.md`
