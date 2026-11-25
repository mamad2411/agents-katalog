---
name: provider-migration-centralization
description: >-
  Centralize LLM provider configuration into a single source of truth and
  perform clean provider migrations across all scripts, cron jobs, and config
  files. Covers the OpenCode Go → DeepSeek migration pattern and the
  hermes_model.py + model_config.json architecture.
version: 1.0.0
author: Hermes Agent
metadata:
  hermes:
    tags: [provider-migration, model-config, centralized-config, api-key-migration, llm-config]
    triggers:
      - migrate provider
      - switch model provider
      - centralized model config
      - swap API endpoint
      - provider migration
      - model_config.json
      - hermes_model.py
      - opencode to deepseek
      - API key migration
      - cron job provider override
    related_skills:
      - cron-watchdog
      - model-health-watchdog
---

# Provider Migration & Centralized Model Config

When migrating all scripts from one LLM provider to another (e.g., OpenCode Go → DeepSeek), this skill captures the exact pattern, pitfalls, and verification steps.

## Architecture: Centralized Model Config

```
model_config.json          ← single source of truth (JSON)
       │
       ▼
hermes_model.py            ← Python module imported by all scripts
       │
       ├── get_config()    → dict of active profile
       ├── get_api_key()   → API key from env var
       ├── active_profile() → name of active profile
       └── switch_to(name) → change active profile
       │
       ▼
All scripts import from hermes_model.py
```

## Files That Need Migration

A provider migration touches **6 categories** of files. Miss one and something breaks silently:

### 1. Central Config (1 file)
- `~/AppData/Local/hermes/model_config.json` — change `active_profile`

### 2. Hermes Agent Configs (2 files)
- `~/.hermes/config.yaml` — `provider:` and `base_url:` under `model:`
- `~/AppData/Local/hermes/config.yaml` — `openai:` provider block (around line 397) with `provider:`, `base_url:`, `api_key:`
- MCP server env vars in this file (e.g., `OPENAI_API_KEY: ${OPENCODE_GO_API_KEY}`)

### 3. All Scripts That Call LLM APIs
Each script needs:
- Import `hermes_model` and use `get_config()` / `get_api_key()` instead of hardcoded values
- Remove hardcoded URLs, model names, and API key env var references

Scripts: cron-guardian.py, pim-pipeline.py, pim_enhancement_mcp.py, pim_enhancement_scanner.py, workflow_runner.py, jippity_bridge_v2.py, jippity_bridge_v3.py, ingest-chatgpt-grok.sh

### 4. Cron Jobs (48+ jobs)
- `~/AppData/Local/hermes/cron/jobs.json` — each job can have pinned `"provider": "opencode-go"`
- Mass-replace: change all `"provider": "opencode-go"` to `"provider": "deepseek"`
- Also fix pinned `"base_url"` values

### 5. Env Files
- `~/AppData/Local/hermes/.env` — set new API key env var
- `~/.hermes/.env` — check for old key references
- `~/.bashrc` — comment out old `export OPENCODE_GO_API_KEY`

### 6. Auth/Credential Files
- `~/.local/share/opencode/auth.json` — fallback auth, harmless if left
- `~/.hermes/auth.json` — cached credentials, harmless if left
- `~/.oci/config` — unrelated to LLM migration but relevant for VPS provisioning

## Step-by-Step Migration Process

### Step 1: Build Central Config
Create `model_config.json` and `hermes_model.py`. Test that `get_config()` and `get_api_key()` work.

### Step 2: Update All Scripts
For each script:
1. Add `sys.path.insert(0, str(Path(__file__).parent))` and `from hermes_model import get_config, get_api_key`
2. Replace hardcoded `API_URL`, `API_MODEL`, and key loading with centralized values
3. Remove old fallback chains (opencode auth.json → env → hardcoded)

### Step 3: Update Hermes Agent Configs
Edit both config.yaml files to change provider, base_url, and API key env var.

### Step 4: Mass-Replace Cron Job Providers
```python
import json, pathlib
cj = json.loads(pathlib.Path.home().joinpath('AppData/Local/hermes/cron/jobs.json').read_text())
jobs = cj.get('jobs', cj) if isinstance(cj, dict) else cj
for j in jobs:
    if j.get('provider') == 'old-provider': j['provider'] = 'new-provider'
    if j.get('base_url') == 'https://old-api.com/v1': j['base_url'] = 'https://new-api.com/v1'
```

### Step 5: Set API Key
Add `NEW_API_KEY=sk-...` to `~/AppData/Local/hermes/.env`.

### Step 6: Test Health Check
```python
from hermes_model import get_config, get_api_key
import urllib.request, json
key = get_api_key()
req = urllib.request.Request(
    get_config()['base_url'] + '/models',
    headers={'Authorization': f'Bearer {key}'}
)
resp = urllib.request.urlopen(req, timeout=15)
print(f'Health OK: {resp.status}')
```

### Step 7: Verify & Commit
Run verification script, commit to hermes-config repo, push.

## Provider-Specific Quirks

### DeepSeek API
- **Auth required on ALL endpoints** including `/models` (unlike OpenCode Go)
- `deepseek-chat` is safe for health checks (always returns visible content)
- `deepseek-v4-flash` is the default model for all cron jobs
- Rate limit: HTTP 429 with `GoUsageLimitError` message
- Key from `DEEPSEEK_API_KEY` env var

### OpenCode Go API (deprecated)
- `/models` was PUBLIC (no auth needed)
- Python default urllib UA gets HTTP 403 — set `User-Agent: curl/7.68.0`
- Key from `OPENCODE_GO_API_KEY` env var or `auth.json`

## Pitfalls

- **Two config files, one forgotten** — `~/.hermes/config.yaml` and `~/AppData/Local/hermes/config.yaml` both need updating. The live config (AppData) is what Hermes actually reads.
- **Cron jobs have pinned providers** — jobs.json stores `"provider": "opencode-go"` per-job. These don't inherit from the central config. Must mass-replace.
- **`get_api_key()` reads env ONLY** — `hermes_model.get_api_key()` checks `os.environ`; when scripts run from cron or a fresh subprocess, the key env var is often NOT exported (it lives in `.env` files, not the shell). Keep a `.env`-file fallback (like cron-guardian's `load_env_key()` which reads `HERMES_HOME/.env` line-by-line, then auth.json, then env). Test key loading in a bare `python -c` — if `get_api_key()` returns empty but the key exists in `.env`, that's this pitfall.
- **Error history strings** — after migration, `last_error` fields still contain old API URLs in their messages. These are harmless logs, not active config.
- **MCP server env vars** — config.yaml has MCP blocks with `OPENAI_API_KEY: ${OPENCODE_GO_API_KEY}`. Change the env var reference too.
- **Health check model ≠ primary model** — always use `chat_model` for health probes, not the reasoning model.
- **DeepSeek /models requires auth** — unlike OpenCode Go which was public. Tier 1 health check must include Authorization header.
- **Secondary provider defs look like stragglers but aren't** — `opencode-zen:` under `providers:` in config.yaml is a secondary/fallback provider definition, not the active one. Don't delete it; verify the ACTIVE block (`model.provider` / `openai:` block) instead.

## Final Sweep Checklist (post-migration)

After migrating, do a full grep sweep — active refs hide in more places than scripts. Command:

```bash
grep -rn 'opencode\.ai\|OPENCODE_GO\|opencode-go\|OPENCODE_API' \
  ~/AppData/Local/hermes/ ~/.hermes/ ~/.bashrc \
  --include='*.py' --include='*.sh' --include='*.yaml' --include='*.json' \
  --include='*.md' --include='.env' 2>/dev/null | grep -v __pycache__
```

Sweep targets and expected classification:

| Location | What's usually left | Action |
|----------|--------------------|--------|
| `cron/jobs.json` `"provider"` fields | old provider if not mass-replaced | **FIX** (active override) |
| `cron/jobs.json` `last_error` strings | old URLs in error text | Leave (history) |
| Live `config.yaml` `model:`/`openai:` block | old provider if missed | **FIX** (active) |
| `config.yaml` secondary `providers:` defs | old provider as fallback profile | Leave (intentional) |
| `model_config.json` profiles | old provider as switchable profile | Leave (intentional — this is the router's job) |
| Script fallback chains (`auth.json` reads) | old-key fallback code | Leave (graceful degradation) or clean |
| `~/.hermes/auth.json`, guardian-backups/ | cached old credentials, stale snapshots | Leave |
| `.bashrc` | commented-out `export` | Leave |
| `cache/terminal/hermes-snap-*.sh` | exported env snapshots | Leave (logs) |

Rule: count **active provider settings**, not raw string matches. A clean migration has zero active refs and any number of historical/intentional ones.

## Verification Checklist

After migration, verify ALL of these:
1. `hermes_model.get_config()` returns correct provider/URL/model
2. `hermes_model.get_api_key()` returns a non-empty key
3. `cron-guardian.py check_model_health()` returns True
4. No `"provider": "old-provider"` in cron jobs.json
5. Both config.yaml files reference new provider
6. `.env` has new API key
7. All scripts import from hermes_model.py (grep for old hardcoded URLs)

## Discord Noise Filtering (Cron Jobs)

When auditing cron job delivery settings, classify every LLM-driven job:

| Category | `deliver` | Examples |
|----------|-----------|---------|
| Revenue/actionable | `origin` | C2C Hunter, Land Sales, picks, alerts |
| Pulse/heartbeat/monitor | `local` | Morning Brief, Flash Intel, Weekly Strategy |
| Errored jobs | `local` | Any with `last_status: error` |
| no_agent script jobs | Auto-silent | Empty stdout = no delivery |

Rule: only jobs with actionable output should appear in Discord.
