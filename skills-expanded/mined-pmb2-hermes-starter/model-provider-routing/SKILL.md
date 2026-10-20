---
name: model-provider-routing
version: 1.0.0
category: devops
author: Hermes Agent
description: "Centralized LLM provider/model routing for Hermes scripts via model_config.json — configure, switch, and fallback providers."
metadata:
  hermes:
    tags: [model-routing, provider-config, llm-provider, centralized-config]
    triggers:
      - configure model routing
      - switch provider
      - centralized provider config
      - model fallback setup
      - AI provider swap
    related_skills: [ai-model-router-gateway, gateway-troubleshooting]
---

# Model Provider Routing — Centralized Config

## Overview

All Hermes scripts that call an LLM API read their provider configuration from
a single source of truth: `~/AppData/Local/hermes/model_config.json`.
Scripts import `hermes_model.py` to get the active profile's base URL, model
name, and API key. To swap providers, edit ONE file.

## Architecture

```
model_config.json           ← single source of truth
       │
       ▼
hermes_model.py             ← Python module imported by all scripts
       │
       ├── get_config()        → dict of active profile
       ├── get_api_key()       → API key from env var
       ├── active_profile()    → name of active profile
       ├── list_profiles()     → all available profiles
       └── switch_to(name)     → change active profile programmatically
       │
       ▼
cron-guardian.py         pim-pipeline.py         pim_enhancement_mcp.py
workflow_runner.py       jippity_bridge_v2.py    jippity_bridge_v3.py
pim_enhancement_scanner.py
```

## model_config.json — Canonical Copy

Path: `~/AppData/Local/hermes/model_config.json`

The canonical copy (tracked in git) is in the `hermes-config` repo at
`config/model_config.json`. After updating the live config, sync it to the
repo and commit. Also update `~/.hermes/config.yaml` and `config/config.yaml`
in the repo so Hermes Agent stays in sync with the scripts.

**Git repo:** `~/Documents/github/hermes-config` (`pmb2/hermes-config` on GitHub)

```json
{
  "active_profile": "deepseek",
  "profiles": {
    "deepseek": {
      "provider": "deepseek",
      "base_url": "https://api.deepseek.com/v1",
      "api_key_env": "DEEPSEEK_API_KEY",
      "model": "deepseek-v4-flash",
      "chat_model": "deepseek-chat",
      "reasoning_model": "deepseek-reasoner",
      "description": "DeepSeek API direct"
    },
    "opencode-go": {
      "provider": "opencode-go",
      "base_url": "https://opencode.ai/zen/go/v1",
      "api_key_env": "OPENCODE_GO_API_KEY",
      "model": "deepseek-v4-flash",
      ...
    }
  }
}
```

## hermes_model.py — Module Interface

Path: `~/AppData/Local/hermes/scripts/hermes_model.py`

Every script imports it as:
```python
sys.path.insert(0, str(Path(__file__).parent))
from hermes_model import get_config, get_api_key
```

### Key Functions

| Function | Returns | Description |
|----------|---------|-------------|
| `get_config(profile=None)` | dict | Active profile's config (base_url, provider, model, api_key_env, chat_model, reasoning_model) |
| `get_api_key(profile=None)` | str | API key from the profile's env var (`os.environ.get`) |
| `active_profile()` | str | Name of the active profile |
| `list_profiles()` | list of (name, desc) tuples | All available profiles |
| `switch_to(name)` | bool | Change active_profile in the JSON file |

### Config Dict Shape

```python
{
    'provider': 'deepseek',
    'base_url': 'https://api.deepseek.com/v1',
    'api_key_env': 'DEEPSEEK_API_KEY',
    'model': 'deepseek-v4-flash',        # primary model
    'chat_model': 'deepseek-chat',        # visible-content model for health checks
    'reasoning_model': 'deepseek-reasoner',
    'description': 'DeepSeek API direct',
}
```

## How to Swap Providers

1. Open `model_config.json`
2. Change `"active_profile"` to a different key in `"profiles"`
3. Ensure the corresponding env var (`api_key_env`) is set in `.env`
4. Done — all scripts pick up the change on next run

### Profile Naming

Each profile has a:
- `provider` name used in Hermes config.yaml (e.g. 'deepseek', 'opencode-go', 'openrouter')
- `base_url` — the API endpoint
- `api_key_env` — the env var name holding the API key
- Up to 3 model slots for different use cases

## Provider-Specific Quirks

### DeepSeek API
- **Auth required on ALL endpoints** including `/models`. Health checks must include `Authorization: Bearer <key>` on every request.
- `deepseek-chat` is the safe health-check model (always returns visible content)
- `deepseek-reasoner` may return empty `content` with just `reasoning_content`
- Key from `DEEPSEEK_API_KEY` env var, set in `~/AppData/Local/hermes/.env`
- **Rate limit**: Returns HTTP 429 `GoUsageLimitError` when weekly limits hit

### OpenCode Go API (fallback)
- `/models` endpoint was PUBLIC (no auth needed) — unlike DeepSeek
- Python's default urllib UA gets HTTP 403. Always set `User-Agent: curl/7.68.0`
- Key from `OPENCODE_GO_API_KEY` env var or `~/.local/share/opencode/auth.json`
- `kimi-k2.5` preferred for health checks (visible content, unlike reasoning models)

## Scripts That Use Centralized Config

| Script | Config Source | Key Enum |
|--------|-------------|----------|
| `cron-guardian.py` | `hermes_model.py` import | DEEPSEEK_API_KEY |
| `pim-pipeline.py` | `hermes_model.py` import | DEEPSEEK_API_KEY |
| `pim_enhancement_mcp.py` | `hermes_model.py` import | DEEPSEEK_API_KEY |
| `pim_enhancement_scanner.py` | `hermes_model.py` import | DEEPSEEK_API_KEY (primary), OPENCODE_GO_API_KEY (fallback) |
| `workflow_runner.py` | `hermes_model.py` import | DEEPSEEK_API_KEY |
| `jippity_bridge_v2.py` | `hermes_model.py` import | DEEPSEEK_API_KEY |
| `jippity_bridge_v3.py` | `hermes_model.py` import | DEEPSEEK_API_KEY |
| `ingest-chatgpt-grok.sh` | inline Python → `hermes_model.py` | DEEPSEEK_API_KEY |

## Provider Stack Priority (OmniRoute + CLIProxyAPI + Free Tiers)

When OmniRoute is running as the local AI gateway, the configured model routing
priority cascade (configurable via OmniRoute's dashboard or combo settings) is:

| Priority | Tier | Source | Model ID | Cost | Quality |
|----------|------|--------|----------|------|---------|
| 1st 🥇 | Free unlimited | OpenCode Zen | `oc/deepseek-v4-flash-free` | $0 | DeepSeek V4 Flash |
| 2nd 🥈 | Free unlimited | Together/SiliconFlow | `tllm/together_deepseek_v3` | $0 | DeepSeek V3 |
| 3rd 🥉 | Free auto | OmniRoute auto | `auto/coding:free` | $0 | Best free coding |
| 4th | Paid API | DeepSeek direct | deepseek-v4-flash | Pay | DeepSeek V4 Flash |
| ⛔ NEVER | Premium | Kimi K3 / Claude / GPT | manual switch only | Expensive | Never auto-routed |

**Hard rules:**
- Never compromise below DeepSeek V4 Flash intelligence
- Kimi K3, Claude Fable, GPT 5.6+ are NEVER auto-routed — manual switch only
- OpenCode Zen free tier (`oc/deepseek-v4-flash-free`) is the first choice for every request
- Paid DeepSeek key is the LAST resort, not the default
- OmniRoute's `OMNIROUTE_AUTO_FREE_FALLBACK_TO_FULL_POOL=true` enables falling back to the full free pool when specific auto combos are exhausted

### Startup Script

OmniRoute runs as a local dev server on port 20128. The unified startup script starts all services:

```bash
# Start the full stack (OmniRoute + Hermes-router + Model Switch Monitor)
# + optionally Firefox CDP for browser automation
bash ~/AppData/Local/hermes/scripts/hermes-stack.sh
```

The startup script (at `hermes-stack.sh`, not the older `start-model-stack.sh`):
1. Kills any zombie processes on the target ports
2. Starts OmniRoute with `node scripts/dev/run-next.mjs dev` on port 20128
3. Starts Hermes-router with `python router.py` on port 8319
4. Starts the model switch monitor daemon
5. Optionally starts Firefox CDP on port 9239 with the user's default profile

### Router Ecosystem (Tier Cascade for All Agents)

All 47+1 Hermes profiles route through OmniRoute with this cascade:

| Tier | Source | Model ID | Cost | Quality |
|------|--------|----------|------|---------|
| 1st | OpenCode Zen | `oc/deepseek-v4-flash-free` | $0 | DeepSeek V4 Flash |
| 2nd | Together/SiliconFlow | `tllm/together_deepseek_v3` | $0 | DeepSeek V3 |
| 3rd | OmniRoute auto-free | `auto/coding:free` | $0 | Best free coding |
| 4th | Hermes-router (port 8319) | USER's custom router | $0 | Falls back to Gemini/OpenRouter/Groq |
| 5th | CLIProxyAPI (port 8317) | Antigravity/Codex/Claude | $0 | Free Claude/Codex via OAuth |
| 6th | FreeLLMAPI | 28 free providers | $0 | ~4B tokens/mo free |
| Last | DeepSeek paid API | deepseek-v4-flash | Pay | Only if all free exhausted |
| ⛔ NEVER | Kimi K3, Claude, GPT | manual switch only | Expensive | Never auto-routed |

**Additional router projects for free API key generation:**
- **9Router-v2** (`${MY_REPOS}/Documents/github/9router-v2`) — has built-in Playwright + 2Captcha automation for Cloudflare Workers AI account signup, auto-extracts free API keys
- **FreeLLMAPI** (`${USER_HOME}/freellmapi`) — 28 free providers behind one endpoint

### Batch Profile Migration

To switch ALL Hermes profiles from one provider to another at once:

```python
from pathlib import Path
profiles_base = Path("~/AppData/Local/hermes/profiles").expanduser()
for profile_dir in sorted(profiles_base.iterdir()):
    if not profile_dir.is_dir(): continue
    config = profile_dir / "config.yaml"
    if not config.exists(): continue
    content = config.read_text()
    # Make replacements
    content = content.replace("old_base_url", "new_base_url")
    content = content.replace("old_model", "new_model")
    content = content.replace("old_provider", "new_provider")
    config.write_text(content)
```

This batch-updates all profiles in one pass. Also update `~/.hermes/config.yaml` (the default profile) separately.

### Model Switch Notifications

When OmniRoute fallbacks between tiers, a short Discord notification is sent.

**Preferred format (short & low-key):**
```
↑ DeepSeek V4 Flash        (upgraded to a better tier)
↓ DeepSeek V3              (downgraded to a lower tier)
→ DeepSeek V4 Flash exhausted   (current provider exhausted, falling back)
```

Arrow indicates direction: `↑` better tier, `↓` lower tier, `→` exhausted/falling back.
No emoji, no full sentences, no "Model Switch:" prefix. Just the quality label.

The `model_switch_monitor.py` daemon tails OmniRoute's dev log and detects:
- Model routing events (`[COMBO] Routed to <model>`)
- Provider exhaustion (`[AUTO] <model> matched no connected models`)
- Any model/provider change

**Script:** `~/AppData/Local/hermes/scripts/model_switch_monitor.py`
**Log file:** `~/OmniRoute/.build/next/dev/logs/next-development.log`
**State file:** `~/AppData/Local/hermes/.model_switch_state.json`

Run as daemon:
```bash
python ~/AppData/Local/hermes/scripts/model_switch_monitor.py --daemon
```

The unified startup script (`hermes-stack.sh`) starts the monitor automatically.

## Migration: Adding a New Provider Profile

1. Add a new entry to `model_config.json` `"profiles"`:
   ```json
   "my-provider": {
     "provider": "my-provider",
     "base_url": "https://api.my-provider.com/v1",
     "api_key_env": "MY_PROVIDER_API_KEY",
     "model": "my-model",
     "chat_model": "my-chat-model",
     "reasoning_model": "my-reasoning-model",
     "description": "My custom provider"
   }
   ```
2. Set the API key env var: `export MY_PROVIDER_API_KEY=sk-...`
3. Set `"active_profile": "my-provider"`
4. Optionally update `~/.hermes/config.yaml` and `~/AppData/Local/hermes/config.yaml`
   to match the new provider for Hermes Agent itself.

### Gateway Router Profiles (OmniRoute, CLIProxyAPI, FreeLLMAPI)

Local AI gateways can also be added as provider profiles. They expose OpenAI-compatible endpoints and handle provider routing themselves. Example:

```json
"omniroute": {
  "provider": "omniroute",
  "base_url": "http://localhost:20128/v1",
  "api_key_env": "OMNIROUTE_API_KEY",
  "model": "auto",
  "chat_model": "auto",
  "reasoning_model": "auto",
  "description": "OmniRoute local AI gateway — 271 providers, auto-fallback"
}
```

Key: OmniRoute's `model: auto` lets it choose the best provider in real-time. CLIProxyAPI wraps free CLI tools (Codex, Grok Build, Antigravity) as API endpoints. See `references/gateway-router-options.md` for full installation, configuration, and provider-stack priority recommendations.

## How to Migrate From One Provider to Another

When switching all scripts from Provider A to Provider B (e.g., OpenCode Go → DeepSeek):

1. **Add the new profile** to `model_config.json` `"profiles"`
2. **Set `active_profile`** to the new provider name
3. **Update Hermes Agent configs** — Two configs need the provider change:
   - `~/.hermes/config.yaml` — `provider:` and `base_url:` under `model:`
   - `~/AppData/Local/hermes/config.yaml` — the `openai:` provider block (lines ~397) with `provider:`, `base_url:`, `api_key:`
4. **Update cron job pinned providers** — `~/AppData/Local/hermes/cron/jobs.json` may have per-job `provider` overrides. Use `grep -c '"provider": "opencode-go"' jobs.json` to check. Change every `opencode-go` to the new provider name using Python mass-replace.
5. **Set the API key env var** in `~/AppData/Local/hermes/.env`
6. **Update MCP server env vars** — Check `~/AppData/Local/hermes/config.yaml` for MCP server blocks that reference the old API key env var (e.g., `OPENCODE_GO_API_KEY`). Change to the new one.
7. **Clean up old references** — Comment out or remove old `export OPENCODE_GO_API_KEY` lines in `.bashrc`
8. **Commit to hermes-config repo** — The canonical config lives at `~/Documents/github/hermes-config/`

### Migration Verification Script

After migrating, verify with this check:
```python
import importlib.util, sys, pathlib, json

# 1) Central model config loads correctly
H = pathlib.Path.home()
sys.path.insert(0, str(H / 'AppData/Local/hermes/scripts'))
from hermes_model import get_config, get_api_key, active_profile
m = get_config()
assert m['base_url'] == 'https://api.deepseek.com/v1'  # or new URL
assert m['provider'] == 'deepseek'  # or new provider

# 2) Cron jobs have no old pinned providers
cj = json.loads((H / 'AppData/Local/hermes/cron/jobs.json').read_text())
jobs = cj.get('jobs', cj) if isinstance(cj, dict) else cj
assert sum(1 for j in jobs if isinstance(j, dict) and j.get('provider') == 'opencode-go') == 0

# 3) Live config points to new provider
assert 'provider: deepseek' in (H / '.hermes/config.yaml').read_text()
assert 'provider: deepseek' in (H / 'AppData/Local/hermes/config.yaml').read_text()

# 4) Health check passes
spec = importlib.util.spec_from_file_location('cg', str(H / 'AppData/Local/hermes/scripts/cron-guardian.py'))
mod = importlib.util.module_from_spec(spec)
sys.modules['cg'] = mod
spec.loader.exec_module(mod)
healthy, detail, credits = mod.check_model_health()
assert healthy, f'Health FAILED: {detail}'
```

## Pitfalls

- **Key not found in env** — `get_api_key()` only checks `os.environ`. If the key is in `.env` but not exported, scripts with a fallback path (reading `.env` directly) will find it. Pure `get_api_key()` will return empty. Either export the var or use the script's own key-loading fallback.
- **Hermes Agent config is separate** — `~/.hermes/config.yaml` uses its own provider/model settings. The centralized config covers script-level model usage. Both should be updated together when swapping providers, or Hermes Agent will use a different model than the scripts.
- **Two configs, one outdated** — `~/AppData/Local/hermes/config.yaml` has its own `openai:` provider block (around line 397) that can be out of sync with the user-level config. Always check BOTH when migrating.
- **Cron jobs have cascading provider resolution** — Each cron job in `jobs.json` can have `"provider": null` (inherits from Hermes Agent config) or a pinned provider string. Pinned overrides DON'T change when you update the central config — you must update them individually. Use Python mass-replace.
- **Error history is NOT the same as active config** — After migration, cron jobs' `last_error` fields still contain the old provider's error URLs in their message strings. These are harmless historical logs. The active `provider` and `base_url` fields are what matter.
- **OpenCode Go fallback in auth.json** — Some scripts fall back to reading `~/.local/share/opencode/auth.json` for backward compatibility. This key only works with OpenCode Go's endpoint. If the active profile points to DeepSeek but the fallback finds the old opencode key, DeepSeek auth will fail (401).
- **PIM .env is regenerated** — `pim-pipeline.py` writes a `.env` file from the central config on every run. If you customize the PIM `.env` manually, it gets overwritten.
- **health check model ≠ primary model** — Always use `chat_model` (not `model`) for health probes. `model` may be a reasoning model that returns empty `content`.
- **Health check NameError on health subcommand** — `pim_enhancement_mcp.py health` imports `hermes_model` but its own `active_profile()` may not be in scope. The health endpoint should use `get_config()['provider']` instead of calling `active_profile()`.
- **DeepSeek requires auth on /models** — Unlike OpenCode Go, DeepSeek's `/models` endpoint returns HTTP 401 without an `Authorization` header. The Tier 1 health check in `cron-guardian.py` must include the API key on the `/models` request.
- **Environment variable not propagated to subprocess** — Scripts that call a subprocess (like `pim-pipeline.py`) need the API key explicitly passed because `os.environ` isn't inherited in cron sandboxes. Fall through: env vars → `.env` file → auth.json.
