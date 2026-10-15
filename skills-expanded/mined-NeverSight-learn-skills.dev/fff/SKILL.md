---

name: fff
description: Set up, register, or troubleshoot the fff MCP file-search server — install the binary and wire it into Claude Code, Codex, opencode, Cursor, or Cline. Load when the user mentions fff setup/install/registration or the fff tools are missing. Daily searching is driven by the agent-memory rule ("use fff tools"), which the kit-setup skill installs.
license: MIT
---

# fff-mcp setup

fff (dmtrKovalenko/fff) is a fast, frecency-ranked file-search toolkit. Its MCP
server exposes three tools — `ffgrep` (content), `fffind` (paths), `fff-multi-grep`
(multi-pattern OR) — that beat grep/ripgrep for agents running many searches per
session. This skill covers the one-time setup; everyday usage comes from the
always-on memory rule installed by `kit-setup`.

## Install the binary
macOS / Linux (Homebrew — formula auto-bumped from upstream releases):
```bash
brew install dmtrKovalenko/fff/fff-mcp
```
Any platform: grab a prebuilt `fff-mcp` binary from the upstream
[GitHub Releases](https://github.com/dmtrKovalenko/fff/releases) page.

The installer prints the exact wiring instructions for your client. If you would
rather use the upstream one-line remote installers (`curl … | bash` /
`irm … | iex`), see [INSTALLATION.md](INSTALLATION.md) for the commands and how
to review the scripts first.

## Register with your client
Point the client at the installed `fff-mcp` binary (use an absolute path, since desktop
sessions may not inherit your shell `PATH`):

- **Codex:** `codex mcp add fff -- "/abs/path/to/fff-mcp"` (writes `~/.codex/config.toml`).
- **Claude Code:** `claude mcp add fff -- /abs/path/to/fff-mcp` (or add to `.mcp.json`).
- **OpenCode:** add to `~/.config/opencode/opencode.json` under `mcpServers`:
  ```json
  { "mcpServers": { "fff": { "type": "stdio", "command": "/abs/path/to/fff-mcp", "args": [] } } }
  ```
Restart the client (or start a new task) so it loads the server.

## Verify
Restart the client (or start a new task), run one search through `ffgrep`, and
confirm results come back. If tools are missing, check the registered path is
absolute and points at the installed binary.

For a single one-off grep from a shell, `rg` is still fine — fff pays off when
an agent runs many searches per session against a warm index.
