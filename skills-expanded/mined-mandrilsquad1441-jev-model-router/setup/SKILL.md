---
name: setup
description: Set up or troubleshoot Jev Model Router API keys and defaults. Use when the user asks how to configure the model router, add an OpenRouter or TypeSafe key, change the default priority, or when a routing result says Jev was unavailable or no API key is configured.
metadata:
  short-description: Configure API keys and defaults
---

# Set up Jev Model Router

The router needs one API key to use Jev, TypeSafe's decision model. Without a key it still works, using offline keyword analysis, which is less accurate.

- **OpenRouter key (recommended):** https://openrouter.ai/keys. Jev runs through OpenRouter's Decisions API and is billed to the user's OpenRouter account, a fraction of a cent per analysis.
- **TypeSafe key (official Jev API):** https://console.typesafe.ai/keys. If both keys exist, TypeSafe is used unless `JEV_PROVIDER=openrouter` is set.

## Steps

1. Call `router_status` to see which key is active, whether a live Jev call works, and the exact local setup command.
2. Help the user add a key. The user must type the key themselves; never ask them to paste it into the chat and never put it in a tool call.
   - **Claude Code or the Claude desktop app:** run `/plugin`, open jev-model-router, and enter the key in its configuration. The key is kept in the system keychain. Setting `OPENROUTER_API_KEY` in the environment also works.
   - **Codex:** set `OPENROUTER_API_KEY` (or `TYPESAFE_API_KEY`) in the shell before starting Codex; the plugin passes it through. Alternatively, run the setup command that `router_status` prints, in a terminal outside the agent: it asks for the key with a hidden prompt and stores it in the user's private config file.
   - **Any host:** the same setup command also sets defaults, for example `setup --priority cost`.
3. Restart the session if the host caches MCP servers, then call `router_status` again to confirm "live".

## Defaults

- `JEV_ROUTER_PRIORITY`: `balanced` (default), `intelligence`, `speed` or `cost`.
- `JEV_ROUTER_ALLOW_FREE=1`: also consider free and data-sharing model tiers.
- `JEV_ROUTER_EXCLUDE`: comma-separated providers or model globs to never recommend.
- `JEV_ROUTER_OFFLINE=1`: never touch the network (bundled catalog and offline analysis).
