---
name: plugin-overview
description: >-
  Architecture reference for the opencode-litellm plugin. Use when working on
  the plugin hooks (auth, tool, config), the litellm-setup command flow, API key
  handling, /connect provider registration, opencode.json writes, config file
  format, graceful degradation, or understanding how the plugin fits into the
  OpenCode plugin system.
allowed-tools: Read, Glob, Grep
---
# opencode-litellm Plugin Architecture

## Overview

An OpenCode plugin that auto-discovers models from a LiteLLM proxy and injects
them as a `litellm` provider at startup. No manual model listing required.

## Three Hooks

### `chat.params` hook
Runs on every outbound LLM request; injects `metadata.session_id` into the request body so LiteLLM groups all turns in one OpenCode chat session into a single session in the Admin UI.

- Only fires for requests routed to the `litellm` provider (`input.provider.info.id === "litellm"`); no-op for all others.
- `input.sessionID` is OpenCode's stable ULID for the current chat session — same value across every turn, different per session.
- Written to `output.options.metadata.session_id`; the `@ai-sdk/openai-compatible` provider forwards `options` fields as extra body args on `/chat/completions`, so LiteLLM receives `metadata.session_id` directly.
- Pre-existing keys on `output.options` and `output.options.metadata` are preserved (spread, not replaced).

### `auth` hook
Registers the `litellm` provider with OpenCode so `/connect litellm` prompts for credentials.

- `provider: "litellm"` — the key used when calling `ctx.client.auth.get("litellm")`
- Single `type: "api"` method with TWO prompts:
  1. `baseURL` — LiteLLM proxy base URL (e.g., `http://localhost:4000`)
  2. `apiKey` — API key (optional; leave blank if proxy has no auth)
- `authorize()` strips `/v1` suffix and trailing slash, writes `provider.litellm.options.baseURL` 
  directly to `~/.config/opencode/opencode.json`, and returns `{ type: "success", key: apiKey || "no-key" }` 
  (the `no-key` sentinel stands in for an empty string because OpenCode can't store blank keys)
- `loader()` builds the credential object used by the AI SDK when routing calls;
  reads both `baseURL` from `opencode.json` and the API key from the auth store, then wraps 
  `await auth()` in try/catch because it throws when no credential is stored yet

### `config` hook
Runs at every OpenCode startup; mutates the config object in place (returns void).

1. On first run (no `provider.litellm` in `opencode.json`), writes a static placeholder with the "setup" model:
   ```
   config.provider.litellm = {
     npm: "@ai-sdk/openai-compatible",
     name: "LiteLLM",
     options: { baseURL: "http://localhost:4000/v1" },
     models: { setup: { id: "setup", name: "Run /connect litellm to configure" } }
   }
   ```
   This makes LiteLLM appear in `/connect` before the user configures it.
2. Reads `baseURL` from `~/.config/opencode/opencode.json` (written by `authorize()`)
3. Reads stored API key from `~/.local/share/opencode/auth.json`
4. Calls `GET {baseURL}/v1/models` with 5 s timeout + optional Bearer token
5. On any fetch failure → returns early (graceful degradation, no crash)
6. Injects `config.provider.litellm` with `@ai-sdk/openai-compatible`, discovered models,
   and `baseURL: "{rootURL}/v1"` (dynamic, overrides the static placeholder)

## Config Files

**OpenCode config:** `~/.config/opencode/opencode.json`
```json
{
  "provider": {
    "litellm": {
      "npm": "@ai-sdk/openai-compatible",
      "name": "LiteLLM",
      "options": { "baseURL": "http://your-host:4000/v1" },
      "models": { ... }
    }
  }
}
```
- `provider.litellm.options.baseURL` is written by `authorize()` when user runs `/connect litellm`
- On first run, the `config` hook writes a static placeholder entry so LiteLLM appears in `/connect` 
  before the user configures it
- The `config` hook dynamically updates the model list at startup based on what the proxy returns

**Auth Store:** `~/.local/share/opencode/auth.json`
```json
{
  "litellm": {
    "key": "sk-..." 
  }
}
```
- Stores the API key returned by `authorize()` after the user runs `/connect litellm`
- Absence of `litellm.key` means the user has not yet run `/connect litellm`, or ran it with a blank key
  (in which case the value is the `"no-key"` sentinel)

## API Key Handling

| Stored value | Meaning | Config hook behavior |
|---|---|---|
| absent / `null` | No key entered | `apiKey` omitted from provider options |
| `"no-key"` | User left key blank | treated as absent — `apiKey` omitted |
| `"sk-..."` | Real key | passed as `Authorization: Bearer sk-...` |

## User Setup Flow

```
First OpenCode startup:
  → config hook writes placeholder provider.litellm to opencode.json
  → LiteLLM appears in /connect with "Run /connect litellm to configure" model

User runs /connect litellm:
  → Prompt 1: LiteLLM proxy base URL
  → Prompt 2: API key (or blank)
  → authorize() writes provider.litellm.options.baseURL to opencode.json
  → authorize() returns key; OpenCode stores it in auth.json
  → On next OpenCode startup, config hook fetches models dynamically
```

## Key Invariants

- `fetchModels` is called with the **root URL** (no `/v1`); it appends `/v1/models` itself
- `config.provider.litellm.options.baseURL` is always `{rootURL}/v1`
- `authorize()` strips `/v1` and trailing slash; stores as root URL in opencode.json
- `baseURL` in opencode.json is `{rootURL}/v1` (full path, not just root)
- `apiKey` in auth.json is either a real key, the `"no-key"` sentinel, or absent entirely
- Model IDs come directly from `/v1/models` — no prefix added
- Any network failure in `config` hook is swallowed so OpenCode still starts

## Logs & Debugging

The plugin writes timestamped debug lines directly to a dedicated file using
`appendFile` — OpenCode discards plugin process stderr so `console.error` is
ineffective:

- **Windows:** `%USERPROFILE%\.local\share\opencode\log\litellm-plugin.log`
- **macOS/Linux:** `~/.local/share/opencode/log/litellm-plugin.log`

To read it from inside an agent session, use `/read-plugin-logs`.

### Key log lines and what they mean

| Log message | Meaning |
|---|---|
| `config hook: start` | Plugin loaded; config hook is running |
| `config hook: writing static placeholder entry to opencode.json` | First run or no provider.litellm entry yet; writing default |
| `config hook: baseURL=<url>` | LiteLLM URL read from opencode.json; continuing |
| `config hook: auth key <set\|none>` | Credential read result from auth store |
| `GET <url>/v1/models (with API key\|no auth)` | Model fetch attempt — check this URL is reachable |
| `fetched N model(s): [...]` | Models discovered successfully |
| `config hook: fetchModels failed — <err>` | Proxy unreachable or returned error; err message included |
| `config hook: injected provider with N model(s)` | Provider registered in config — N > 0 means success |
| `auth loader called` | Auth loader invoked by OpenCode for a request |
| `authorize: saving baseURL=<url>` | `/connect litellm` writing URL to opencode.json |

### Launching with inline logs

To see log lines directly in the terminal (instead of a file) during active debugging:

```sh
opencode --print-logs --log-level DEBUG
```

## Starting Fresh

To wipe all plugin state — the `provider.litellm` entry in `opencode.json` and 
the stored credential in OpenCode's auth store — run `/reset-plugin-config` 
inside a Claude Code session, or `uv run reset` from the repo root. Use `--dry-run` 
to preview. After reset, run `/connect litellm` to reconfigure from scratch.

## Dependencies

- `@opencode-ai/plugin` — `Plugin`, `tool`, `tool.schema` (zod)
- `@ai-sdk/openai-compatible` — loaded by OpenCode at runtime (not bundled here)
- No env vars — all config via OpenCode auth UI + plugin config file
