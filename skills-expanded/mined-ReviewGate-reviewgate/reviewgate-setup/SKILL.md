---
name: reviewgate-setup
description: Use when the ReviewGate MCP tools are unavailable, the reviewgate binary is missing from PATH, or the user asks to install or configure ReviewGate. Installs the single-file binary, connects the model key, and prepares the project rules.
---

# Set ReviewGate up on this machine

The whole setup is driven by the binary itself — it prints an
agent-facing instruction that is always in sync with the installed version:

```bash
reviewgate help agent-setup
```

If the binary is not installed yet, install it first (a single file, no Node
and no Docker; **git** must be on PATH):

1. Download the archive for this platform — either from
   `https://reviewgate.dev/dl/` or from
   `https://github.com/ReviewGate/reviewgate/releases/latest`
   (`reviewgate-latest-<platform>.xz`; platforms: `darwin-arm64`, `darwin-x64`,
   `linux-x64`, `linux-arm64`, `linux-x64-musl`, `win-x64.exe`).
2. Verify the checksum against `SHA256SUMS` published next to the artifacts —
   you are about to run an executable downloaded from the network.
3. Unpack (`xz -d`), `chmod +x`, move onto PATH as `reviewgate`.
4. Run `reviewgate doctor` — it live-probes the environment and the model
   endpoint and names exactly what is missing.

Then follow `reviewgate help agent-setup` for the rest: the user config with
the model key (`~/.config/reviewgate/config.yml` — the key is the USER'S
decision and the user's secret; never invent or move keys yourself), and the
project rules (`reviewgate init` scaffolds `.reviewgate/config.yml`).

Full reference for humans: https://reviewgate.dev/docs/agents
