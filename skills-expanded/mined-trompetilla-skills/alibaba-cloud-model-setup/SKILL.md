---
name: alibaba-cloud-model-setup
description: Configure OpenClaw (including historical Moltbot/Clawdbot paths) to use Alibaba Cloud Model Studio through a strict interactive flow. The first required step is asking whether the user can run terminal commands now; use that answer to choose env-var mode (preferred) or inline mode before collecting site/key details. Use this skill when a user asks to add, switch, or repair Alibaba Cloud/Qwen provider configuration in OpenClaw.
---

# Alibaba Cloud Model Setup

## Overview

Use this skill to configure Alibaba Cloud as an OpenClaw model provider with minimal manual editing. Prefer the bundled script for deterministic updates and safe backups.

## Workflow

1. Confirm OpenClaw config location.
2. Run the interactive script to collect:
- First and mandatory: whether user can run terminal commands now (decides env mode vs inline mode)
- In env mode, show 2 commands for user to run (`export` + append to `~/.bashrc`), then wait for confirmation and verify
- Retry env detection up to 2 times; if still not detected, ask whether to fallback to inline key
- Site choice (`Beijing/中国站/CN`, `Singapore/国际站/INTL`, or `Virginia/美国站/US`)
- Access Key (only required if inline mode, or if user chooses inline fallback)
- Validate API key against selected site before any config write
- In systemd deployments, ensure service environment is ready before write
- Default preset models (`qwen-max`, `qwen-flash`, `qwen3-coder-plus`)
- Whether to add extra models from live API list
- Whether to change primary model from default
- Whether to set this model as default
3. Validate the resulting JSON and report the final provider/model path.
4. If user is unsure which model IDs are available, fetch live models from API first.

## Safety Rules (Mandatory)

1. Always run `python3 scripts/alibaba_cloud_model_setup.py` for configuration changes.
2. Never edit `~/.openclaw/openclaw.json` manually when this skill is used.
3. In environment-variable mode, never proceed to config write unless env detection succeeds in the script flow; if detection fails and user rejects inline fallback, stop with `Config not changed.`
4. In systemd deployments, never proceed to config write unless `systemctl --user show-environment` contains the configured env var.

## Run Script

Execute:

```bash
python3 scripts/alibaba_cloud_model_setup.py
```

Optional flags for non-interactive use:

```bash
python3 scripts/alibaba_cloud_model_setup.py \
  --site intl \
  --api-key-source env \
  --env-var DASHSCOPE_API_KEY \
  --api-key "$DASHSCOPE_API_KEY" \
  --models qwen-max,qwen-flash,qwen3-coder-plus \
  --model qwen3-coder-plus \
  --set-default
```

List live model IDs via API (no config write):

```bash
python3 scripts/alibaba_cloud_model_setup.py \
  --site intl \
  --api-key "$DASHSCOPE_API_KEY" \
  --list-models \
  --non-interactive
```

## Default Behavior

- Detect config path in this order:
- `~/.openclaw/openclaw.json`
- `~/.moltbot/moltbot.json`
- `~/.clawdbot/clawdbot.json`
- If none exists, create `~/.openclaw/openclaw.json`
- Write provider `balian` with OpenAI-compatible API mode
- Create a timestamped backup before overwriting an existing file
- Preserve unrelated config sections

## Validation Checklist

After configuration:

1. Confirm JSON is valid by running `python3 -m json.tool <config-path>`.
2. Ensure `models.providers.balian.baseUrl` matches site selection.
3. Ensure `models.providers.balian.models` contains expected model IDs.
4. Ensure `agents.defaults.model.primary` is `balian/<model-id>` when default is enabled.
5. Start dashboard (`openclaw dashboard`) or TUI (`openclaw tui`) and verify model call succeeds.

## References

- Endpoint and field conventions: `references/openclaw_alibaba_cloud.md`
