---
name: opencode-provider-persistence-config
description: Manage OpenCode CLI provider API key storage and startup registration — auth.json persistence model, config-level provider declaration requirement, and root-cause diagnosis of disappearing credentials
category: Tool-Configuration
---

# opencode Provider Persistence Configuration Skill (v1)

## Composition Rationale

This skill is a **base skill**: it owns the generic primitive of how OpenCode persists
provider API keys across restarts and why a provider must be declared in
`opencode.json` to auto-register on startup. Multiple domain-specific composer skills
(such as `opencode-google-gemini-config`) consume this primitive to fix
provider-specific credential-retention bugs without re-documenting the underlying
OpenCode provider-architecture mechanics.

The layering test: *Could a different provider (Anthropic, OpenRouter, a custom
OpenAI-compatible endpoint) ever need the same auth.json + startup-registration
knowledge?* Yes — the OpenCode provider-architecture is shared across all
providers. Inlining this into a single provider-specific skill would split the SSOT
every time a second provider needed the same information.

---

## 1. OpenCode Credential Storage Model

OpenCode stores provider API keys and OAuth tokens in a local file:

- **Path:** `<user-home>/.local/share/opencode/auth.json`
- **Format:** JSON object keyed by provider ID (e.g., `"google"`, `"anthropic"`,
  `"openrouter"`). Each entry contains a `type` field (`"api"` or `"oauth"`)
  and a `key` / token field.
- **Created by:** The `/connect` TUI command, the `opencode auth login` CLI
  command, or environment variables.
- **Persistence:** The file persists across OpenCode restarts. It is not
  deleted or cleared on normal shutdown.

### 1.1 Verification

To inspect stored credentials:

```bash
# List all configured providers and their auth status
opencode auth list

# Read the raw storage file
cat <user-home>/.local/share/opencode/auth.json | python3 -m json.tool
```

The `auth list` output shows each provider ID with a checkmark or
error indicator. If a provider that was connected via `/connect` does
not appear in `auth list`, the credential storage has been lost or
cleared.

---

## 2. Startup Provider Registration

When OpenCode starts, it follows this registration sequence:

1. Reads `<user-home>/.local/share/opencode/auth.json` into memory.
2. Reads `opencode.json` (global or project) to discover the `provider`
   configuration block.
3. For each provider ID declared under `provider` in `opencode.json`,
   OpenCode attempts to match it with:
   - A built-in provider (e.g., `"google"`, `"anthropic"`, `"openai"`), OR
   - A custom provider specification (with `npm` package, `baseURL`, etc.),
     OR
   - A provider registered via a plugin.
4. If the provider ID matches a known provider AND credentials exist in
   `auth.json` for that ID, the provider is registered and available in
   the `/models` picker.

### 2.1 The Silent Registration Gap

**Crucial behavior:** If a provider ID is NOT present in the `provider`
section of `opencode.json`, OpenCode may NOT auto-register it on startup
even though valid credentials exist in `auth.json`. The credentials are
persisted on disk but are not loaded into the runtime provider registry.

This is the root cause of the "API key disappeared after restart" symptom:
the key is still on disk (`auth.json`) but the provider was not declared
in the config, so OpenCode does not pick it up on the next startup.

---

## 3. Config Declaration Requirement

### 3.1 Declaring a Provider in opencode.json

To ensure a provider auto-registers on every startup, add its ID to the
`provider` section of `opencode.json`:

```json
{
  "provider": {
    "<provider-id>": {}
  }
}
```

Where `<provider-id>` matches the key used in `auth.json` (e.g., `"google"`,
`"anthropic"`, `"openrouter"`).

The empty object `{}` tells OpenCode to use the provider's default
configuration. If the provider requires custom options (base URL, API
key override, model whitelist), those go inside the object.

### 3.2 Location Options

| Scope | Path |
|---|---|
| Global | `~/.config/opencode/opencode.json` |
| Project | `<project-root>/opencode.json` or `.opencode/opencode.json` |

Configs are deep-merged — project overrides global.

### 3.3 Restart Requirement

OpenCode loads config once at startup. After editing `opencode.json`,
the user MUST quit and restart OpenCode for changes to take effect.

---

## 4. Troubleshooting

| Symptom | Likely Cause | Fix |
|---|---|---|
| `/connect` succeeds but key missing after restart | Provider not declared in `opencode.json` | Add `"<provider-id>": {}` under `"provider"` in `opencode.json` |
| `opencode auth list` shows the provider | Credentials are stored but not loaded | Add provider declaration to config (see §3.1) |
| `opencode auth list` does NOT show the provider | Credentials were lost | Re-run `/connect` to re-authenticate |
| Provider appears in `/models` but API calls fail | API key invalid or expired | Generate a new key from the provider's console |

---

## 5. Verification Workflow

After configuring a provider in `opencode.json`:

1. Quit and restart OpenCode.
2. Run `/models` in the TUI.
3. Confirm the target provider's models appear in the list.
4. Select a model and send a test prompt.
5. If the prompt succeeds, the config is verified.

---

## Related Skills

- [`opencode-jsonc-util`](../opencode-jsonc-util/SKILL.md) — Base JSONC utility for OpenCode config files
- [`opencode-google-gemini-config`](../opencode-google-gemini-config/SKILL.md) —
  Composer skill: Google AI Studio / Gemini-specific credential setup and
  the explicit config-block fix for the restart-retention bug. Consumes
  this base skill's auth.json + startup-registration knowledge.
- [`opencode-permission-config`](../opencode-permission-config/SKILL.md) —
  OpenCode permission system configuration (complementary OpenCode config
  domain, different subsection of `opencode.json`).

## Source Rules

- [OpenCode Docs — Providers](https://opencode.ai/docs/providers/)
- [OpenCode JSON Schema](https://opencode.ai/config.json)

## Composition by Higher-Level Skills

| Composer | Composition Mechanism |
|---|---|
| [`opencode-google-gemini-config`](../opencode-google-gemini-config/SKILL.md) | Consumes this base skill's §2 (Startup Provider Registration) and §3 (Config Declaration Requirement) to diagnose and fix the Gemini key-disappearance-after-restart bug. The composer adds Google-specific credential setup steps and the concrete `"google": {}` config stanza. |
