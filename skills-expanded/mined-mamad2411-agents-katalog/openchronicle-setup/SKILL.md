---
name: openchronicle-setup
description: Install, configure, connect, and troubleshoot Einsia/OpenChronicle local-first agent memory on macOS. Triggers when a user asks to install OpenChronicle, configure its models, wire its MCP server into Codex/opencode/Claude/Cursor/ChatGPT, or debug capture, daemon, memory, or MCP behavior. Do NOT trigger for unrelated Chronicle products or generic MCP setup without OpenChronicle.
---

# OpenChronicle setup

Use this skill to get [Einsia/OpenChronicle](https://github.com/Einsia/OpenChronicle) installed, configured, running, and connected to local agent clients. OpenChronicle is an early-alpha macOS memory daemon, so treat upstream documentation as the source of truth and verify current commands before making changes.

## When to use

- The user asks to install, upgrade, uninstall, or configure OpenChronicle.
- The user asks to set up local agent memory backed by OpenChronicle.
- The user asks to connect OpenChronicle to Codex, opencode, Claude Code, Claude Desktop, Cursor, or ChatGPT Desktop.
- The user asks why OpenChronicle is not capturing screen context, not writing memory, not answering via MCP, or not using a configured model.
- The user asks where OpenChronicle stores config, memory, captures, logs, or indexes.

## When NOT to use

- The user asks about OpenAI Chronicle, Posit Chronicle, or another unrelated product named Chronicle.
- The user only asks general MCP questions and does not mention OpenChronicle or local memory.
- The user wants a reusable packaged binary, Nix derivation, launchd service, or cross-project CLI wrapper. That belongs in a tooling repo such as `darkmatter/tools`; this skill should still explain the desired behavior and constraints.
- The user wants to expose private memory over the public internet without understanding the trade-off. Stop and explain the data path before configuring a tunnel.

## Placement guidance

Keep this skill in the shared `darkmatter/skills` catalog because the reusable part is agent behavior: inspect the user's machine, install or configure OpenChronicle, connect whichever agent client they use, and troubleshoot from live logs. Put deterministic packaging, Nix modules, launchd units, or company-wide wrapper commands in `darkmatter/tools` if those become necessary.

## Upstream check

Before running install or config commands, check the current upstream docs because the project is alpha and command surfaces may change:

```bash
open https://github.com/Einsia/OpenChronicle
```

Prefer the current upstream files:

- `README.md` for install, run, and project status.
- `docs/config.md` for `~/.openchronicle/config.toml`, model stages, capture tuning, and MCP daemon settings.
- `docs/mcp.md` for client-specific MCP installation.
- `docs/troubleshooting.md` for daemon, capture, writer, classifier, and MCP failures.
- `install.sh` before executing it, because it mutates local client config when requested.

Use `curl` or `gh repo view` when browser access is not convenient. If upstream differs from this skill, follow upstream and note the delta to the user.

## Install workflow

1. Confirm the machine is macOS 13 or newer:

   ```bash
   sw_vers -productVersion
   ```

2. Confirm Xcode Command Line Tools and Swift are available:

   ```bash
   xcode-select -p
   command -v swiftc
   ```

   If either is missing, run `xcode-select --install` and wait for the user to finish the GUI install.

3. Choose an install location. The default upstream installer uses `~/.openchronicle` for the install root and `~/.local/bin/openchronicle` for the shim. If the user wants an isolated install, set `OPENCHRONICLE_INSTALL_HOME` or pass `--bin-dir`.

4. Clone from upstream and inspect the installer:

   ```bash
   git clone https://github.com/Einsia/OpenChronicle.git ~/git/Einsia/OpenChronicle
   cd ~/git/Einsia/OpenChronicle
   sed -n '1,260p' install.sh
   ```

5. Run the installer. Use `--no-client-config` when you want to configure MCP clients manually, or `--yes` only when the user has explicitly asked for automatic client injection.

   ```bash
   bash install.sh --no-client-config
   ```

   The installer creates a virtualenv, installs Python dependencies with `uv`, compiles the macOS AX helper binaries, writes the `openchronicle` shim, and verifies `openchronicle status`.

6. Ensure the shim directory is on `PATH` in the user's shell:

   ```bash
   command -v openchronicle
   openchronicle status
   ```

## Permissions and daemon

OpenChronicle captures macOS accessibility context. After install, grant Accessibility permission to the terminal or app that launches it:

System Settings -> Privacy & Security -> Accessibility

Enable the launching terminal, and enable `openchronicle` too if it appears. Restart the daemon after changing permissions.

Run and inspect the daemon:

```bash
openchronicle start
openchronicle status
openchronicle capture-once
openchronicle timeline tick
openchronicle writer run
openchronicle stop
```

Use `openchronicle start --foreground` when the daemon exits or logs are needed immediately. Tail logs from `~/.openchronicle/logs/*.log` when debugging.

## Configure models

Runtime config lives at `~/.openchronicle/config.toml`, or under `$OPENCHRONICLE_ROOT/config.toml` when that env var is set. It is created with defaults after the first `openchronicle status`.

Inspect the resolved config:

```bash
openchronicle config
```

The model stages are `default`, `timeline`, `reducer`, `classifier`, and `compact`. Stage configs inherit from `[models.default]`.

For cloud models, set an API-key env var or an explicit key in the TOML. Prefer env vars over inline secrets:

```toml
[models.default]
model = "gpt-5.4-nano"
api_key_env = <REDACTED>

[models.reducer]
model = "claude-haiku-4-5"
api_key_env = <REDACTED>
```

For local Ollama, clear `api_key_env` and set a local base URL:

```toml
[models.default]
model = "ollama/llama3.1:8b"
base_url = "http://localhost:11434"
api_key_env = <REDACTED>
```

Use stronger models for `classifier` and `compact` than for `timeline` when quality matters. The classifier needs reliable tool calling; timeline and reducer need JSON-mode compliance.

After edits, restart and probe:

```bash
openchronicle stop
openchronicle start
openchronicle status
```

Use `OPENCHRONICLE_LLM_MOCK=1 openchronicle status` only when you need to inspect config without probing providers.

## Connect agent clients

The daemon hosts a local MCP endpoint at:

```text
http://127.0.0.1:8742/mcp
```

Prefer the built-in idempotent installers when supported:

```bash
openchronicle install codex
openchronicle install opencode
openchronicle install claude-code
openchronicle install claude-desktop
```

Remove entries with the matching `uninstall` command:

```bash
openchronicle uninstall codex
```

Client notes:

- Codex: upstream uses `codex mcp add openchronicle --url http://127.0.0.1:8742/mcp`; config lands in `~/.codex/config.toml`.
- opencode: upstream writes a top-level `mcp.openchronicle` remote entry in `~/.config/opencode/opencode.json`. If the user uses `opencode.jsonc`, install currently refuses to strip comments; add the entry manually.
- Claude Code: upstream shells out to `claude mcp add --transport http -s user openchronicle http://127.0.0.1:8742/mcp`.
- Claude Desktop: upstream registers a stdio server command, because Claude Desktop's JSON config expects local subprocess servers. Quit and reopen Claude Desktop after changing config.
- Cursor: add the local HTTP MCP URL to `~/.cursor/mcp.json` if the upstream installer does not support the current version.
- ChatGPT Desktop: localhost is not reachable because the MCP client runs from OpenAI's cloud. A tunnel such as ngrok or Cloudflare Tunnel is required, and every memory tool request and response leaves the machine. Explain this clearly before setting it up.

Verify MCP reachability from the local machine:

```bash
openchronicle status
curl -s http://127.0.0.1:8742/mcp -XPOST -H 'Content-Type: application/json' -d '{}' | head -5
```

Restart the agent client after changing MCP config so it re-reads tool schemas and server instructions.

## Troubleshooting workflow

Start with observed symptoms and inspect live state before editing config.

Daemon:

```bash
openchronicle status
openchronicle start --foreground
tail -50 ~/.openchronicle/logs/*.log
```

Stale PID:

```bash
ps -p "$(cat ~/.openchronicle/.pid)" || rm ~/.openchronicle/.pid
openchronicle start
```

Port conflict:

```bash
lsof -i :8742
```

Empty captures:

```bash
openchronicle capture-once
ls ~/.openchronicle/capture-buffer | tail
```

The usual causes are missing Accessibility permission or too-shallow `capture.ax_depth` for Electron apps. Keep `ax_depth = 100` unless the user is deliberately reducing CPU cost.

No event entries:

```bash
tail -30 ~/.openchronicle/logs/session.log
tail -30 ~/.openchronicle/logs/timeline.log
tail -50 ~/.openchronicle/logs/writer.log
openchronicle writer run
```

Classifier writes nothing:

- This may be correct. It should only write durable facts.
- If logs show tool-call or commit failures, use a stronger `[models.classifier]` and check provider auth.

MCP client cannot connect:

```bash
openchronicle config | grep -A4 '\[mcp\]'
openchronicle status
```

Confirm `mcp.auto_start = true`, the transport is `streamable-http` or another client-supported value, and the daemon is running.

Indexes drifted:

```bash
openchronicle rebuild-index
openchronicle rebuild-captures-index
```

Reset while keeping config:

```bash
openchronicle stop
openchronicle clean all -y
openchronicle start
```

Full reset:

```bash
openchronicle stop
rm -rf ~/.openchronicle
openchronicle start
```

Use the full reset only when the user understands it removes local captures, memory, database state, and config.

## Privacy and security

OpenChronicle records screen and app context into local Markdown, JSON capture buffers, logs, and SQLite indexes under `~/.openchronicle` by default. Treat these files as sensitive. Do not paste raw captures, logs, memory entries, API keys, tunnel URLs, or config files into public issues without redaction.

Keep the MCP server bound to `127.0.0.1` unless the user explicitly accepts the data-egress risk. Public tunnels currently have no OpenChronicle-specific auth by default; treat the tunnel URL as a secret.

## Reference

- Upstream repo: `https://github.com/Einsia/OpenChronicle`
- Config docs: `https://github.com/Einsia/OpenChronicle/blob/main/docs/config.md`
- MCP docs: `https://github.com/Einsia/OpenChronicle/blob/main/docs/mcp.md`
- Troubleshooting docs: `https://github.com/Einsia/OpenChronicle/blob/main/docs/troubleshooting.md`
