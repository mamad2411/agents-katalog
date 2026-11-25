---
name: yesmem-config
description: Use when managing pins, scratchpad, runtime config, session settings, persona traits, or opencode configuration. Trigger on "pin this"/"merk dir als Regel", persistent instructions, shared agent state, persona overrides, configuration changes like token_threshold, or opencode.json questions ("change opencode model", "add GLM provider", "opencode baseURL", "switch default model").
---

# Configuration & State

Manage pins, scratchpad, persona, runtime settings, and opencode configuration.

## Pins (Persistent Instructions)
Instructions visible in EVERY turn — survive collapse and stubbing.

| Action | Tool |
|--------|------|
| Pin instruction | `pin(content, scope="session\|permanent")` |
| Remove pin | `unpin(id, scope)` |
| List pins | `get_pins(project)` |

- `session` pins last until /clear
- `permanent` pins survive across sessions

## Scratchpad (Shared State)
Key-value sections for inter-agent or cross-session data.

| Action | Tool |
|--------|------|
| Write section | `scratchpad_write(project, section, content)` |
| Read section(s) | `scratchpad_read(project, section)` |
| List sections | `scratchpad_list(project)` |
| Delete | `scratchpad_delete(project, section)` |

## Runtime Config

| Action | Tool |
|--------|------|
| Read setting | `get_config(key)` |
| Change setting | `set_config(key, value)` |

Currently supported: `token_threshold` (per-session or global).

## Persona

| Action | Tool |
|--------|------|
| Set trait | `set_persona(trait_key, value)` — user override, highest priority |

Dimensions: communication, workflow, expertise, context, boundaries, learning_style.

## Session Control

| Action | Tool |
|--------|------|
| Skip indexing | `skip_indexing(session_id)` — session won't be extracted |
| Quarantine session | `quarantine_session(session_id)` — exclude all learnings |
| Who am I? | `whoami()` — get session ID and agent metadata |

## Opencode Configuration Helper

`opencode.json` lives at `~/.config/opencode/opencode.json` and controls opencode's default model, provider routing, and MCP wiring. The YesMem setup wizard writes defaults there on install but does NOT overwrite existing scalar values — so users who want to change `model`, `small_model`, or specific `baseURL` entries must edit the file manually or ask an agent to do it.

### Top-level keys you can change

| Key | Type | Example | What it controls |
|---|---|---|---|
| `model` | string (scalar) | `"deepseek/deepseek-reasoner"` or `"zai-coding-plan/glm-5.2"` | Default model for opencode prompts |
| `small_model` | string (scalar) | `"deepseek/deepseek-chat"` | Lighter model for summaries, tool-choice, etc. |
| `provider` | map | see below | Per-provider baseURL + models |
| `mcp.yesmem` | map | see below | YesMem MCP integration |
| `compaction.auto` | bool | `false` | opencode's own compaction (disabled by YesMem, proxy pipeline handles it) |

### Common change requests

**Switch default model** (e.g. user asks "use GLM-5.2 instead of DeepSeek"):
```json
{
  "model": "zai-coding-plan/glm-5.2",
  "small_model": "zai-coding-plan/glm-5.2"
}
```

**Add a provider** (e.g. add zai-coding-plan for GLM-5.2):
```json
"provider": {
  "zai-coding-plan": {
    "npm": "@ai-sdk/openai-compatible",
    "options": {
      "baseURL": "http://localhost:9099/v1"
    },
    "models": {
      "glm-5.2": {
        "name": "GLM-5.2 Coding Plan",
        "limit": {"context": 1000000, "output": 131072}
      }
    }
  }
}
```

All providers route through the YesMem proxy at `http://localhost:9099/v1`. The proxy forwards to the upstream API using keys from `~/.local/share/opencode/auth.json` (per-provider `key` field).

**Change DeepSeek to direct (bypass proxy)** — only for debugging:
```json
"provider": {
  "deepseek": {
    "options": {
      "baseURL": "https://api.deepseek.com/v1"
    }
  }
}
```

Without proxy routing, YesMem loses briefing/telemetry/compaction for that provider.

### Validating changes

After editing, ask the user to restart opencode (or run `/mcp reconnect` in opencode TUI). If MCP fails, check:

1. `mcp.yesmem.command` points to a valid yesmem binary path
2. `mcp.yesmem.timeout` is 60000 or higher (default opencode 10s is too short for deep_search/embedding calls)
3. `mcp.yesmem.enabled` is `true`

### Default vs user state

The setup wizard's `defaultOpencodeSettings()` in `internal/setup/opencode_settings.go` writes these defaults:

- `model`: derived from user's chosen provider (via `derivePrimaryAndSmallModel`)
- `small_model`: derived likewise
- `provider.deepseek`: baseURL localhost:9099 + 2 models (deepseek-chat as Flash, deepseek-reasoner as Pro)
- `provider.openai`: baseURL localhost:9099 + gpt-5.5
- `provider.anthropic`: baseURL localhost:9099 only (first-party, no models block)
- `mcp.yesmem`: local type, command [yesmem-binary, "mcp"], 60000 timeout
- `compaction`: `{auto: false, prune: false}`

These are merged via `deepMergeJSON` which does NOT overwrite existing scalars. So if the user already has `model: deepseek/deepseek-reasoner` and re-runs setup choosing GLM-5.2, the old DeepSeek value stays — they must edit the file.

### When to recommend re-running setup

- User wants all provider baseURLs reset to proxy defaults
- User wants MCP timeout upgraded to 60000 (only applied via setup, not runtime)
- User wants compaction.auto set to false (only applied via setup)
- Fresh installation on a new machine

For pure model or single-provider changes, edit opencode.json directly.
