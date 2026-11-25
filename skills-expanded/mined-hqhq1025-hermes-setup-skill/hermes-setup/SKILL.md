---
name: hermes-setup-skill
description: Automated deployment of Hermes Agent — install, configure providers, messaging platforms, and tools on local or remote systems.
version: 1.3.0
author: Haoqing Wang
license: MIT
metadata:
  hermes:
    tags: [hermes, setup, configuration, deployment, install, onboarding]
    related_skills: [hermes-agent]
---

# Hermes Agent Setup

Automated, non-interactive deployment of [Hermes Agent](https://github.com/NousResearch/hermes-agent). Mirrors the official `hermes setup` wizard but driven by a coding agent via shell commands and user prompts.

## When to Use

- User wants to install, configure, or deploy Hermes Agent
- User wants to reconfigure or add platforms to an existing installation
- Keywords: "hermes setup", "deploy hermes", "configure hermes", "install hermes"

## Quick Reference

| Section | Configures | Key Command |
|---------|-----------|-------------|
| Install | Binary + deps | `curl ... \| bash` |
| 1. Model | Provider + model | `hermes config set model.provider <p>` |
| 2. Terminal | Command execution env | `hermes config set terminal.backend <b>` |
| 3. Agent | Iterations, compression | `hermes config set agent.max_turns <n>` |
| 4. Platforms | Messaging integrations | Write tokens to `~/.hermes/.env` |
| 5. Tools | Browser, search, TTS, etc. | Write API keys to `~/.hermes/.env` |
| 6. MCP | External tool servers | `hermes mcp add <name> --url <url>` |

Files: `~/.hermes/config.yaml` (settings), `~/.hermes/.env` (secrets, auto-chmod 0600), `~/.hermes/SOUL.md` (personality).

## Procedure

All commands via `Bash`. For remote servers, prefix with `ssh <host>`. Use `AskUserQuestion` for credentials and choices.

---

### Phase 0: Install

**Ask:** Where to deploy?
- Local machine (macOS / Linux / WSL2)
- Remote server via SSH (provide host)
- Termux (Android)

**OS notes:**
- **Windows native:** NOT supported by bash installer. Use PowerShell: `irm https://raw.githubusercontent.com/NousResearch/hermes-agent/main/scripts/install.ps1 | iex`
- **WSL2:** Works like Linux, but systemd must be enabled for gateway persistence (`systemd=true` in `/etc/wsl.conf`)
- **Termux:** Uses `.[termux]` extra, not `.[all]`. Requires: `pkg install python clang rust make pkg-config libffi openssl git nodejs`

```bash
curl -fsSL https://raw.githubusercontent.com/NousResearch/hermes-agent/main/scripts/install.sh | bash -s -- --skip-setup
```

If `hermes --version` fails, fallback to manual install:
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
export PATH="$HOME/.local/bin:$PATH"
git clone https://github.com/NousResearch/hermes-agent.git ~/.hermes/hermes-agent
cd ~/.hermes/hermes-agent
uv venv venv --python 3.11 -q
VIRTUAL_ENV=venv uv pip install -e ".[all]" -q
echo 'export PATH="$HOME/.hermes/hermes-agent/venv/bin:$HOME/.local/bin:$PATH"' >> ~/.bashrc
# Termux: replace ".[all]" with ".[termux]" and add "-c constraints-termux.txt"
```

**Re-run:** Safe. Existing `~/.hermes/.env` and `config.yaml` are preserved. Code updates via `git pull`.

**OpenClaw migration:** If `~/.openclaw/` exists, `hermes setup` will auto-detect and offer to import. Or run `hermes claw migrate --dry-run` manually.

Verify: `hermes --version`

**Post-install: install recommended system deps:**
```bash
# Linux (apt)
sudo apt install -y ripgrep ffmpeg
# macOS
brew install ripgrep ffmpeg
```

Install agent-browser (for browser tools):
```bash
cd ~/.hermes/hermes-agent && npm install --prefix tools/agent-browser
```

Run health check: `hermes doctor`

---

### Section 1: Model & Provider

**Ask (single-select):** Which inference provider?

| Provider | Config Value | Env Var | Auth |
|----------|-------------|---------|------|
| OpenRouter | `openrouter` | `OPENROUTER_API_KEY` | API key |
| GitHub Copilot | `copilot` | `COPILOT_GITHUB_TOKEN` | OAuth device code |
| Google Gemini | `gemini` | `GOOGLE_API_KEY` | API key |
| Anthropic | `anthropic` | `ANTHROPIC_API_KEY` | API key |
| Nous Portal | `nous` | — | `hermes login` |
| Z.AI / GLM | `zai` | `GLM_API_KEY` | API key |
| Kimi / Moonshot | `kimi-coding` | `KIMI_API_KEY` | API key |
| MiniMax | `minimax` | `MINIMAX_API_KEY` | API key |
| MiniMax China | `minimax-cn` | `MINIMAX_CN_API_KEY` | API key |
| DeepSeek | `deepseek` | `DEEPSEEK_API_KEY` | API key |
| Hugging Face | `huggingface` | `HF_TOKEN` | API key |
| Alibaba / Qwen | `alibaba` | `DASHSCOPE_API_KEY` | API key |
| Ollama (local) | `custom` | — | None |
| Custom endpoint | `custom` | `OPENAI_API_KEY` (optional) | Varies |

For API key providers:
```bash
echo "<ENV_VAR>=<key>" >> ~/.hermes/.env
chmod 600 ~/.hermes/.env
hermes config set model.provider <provider>
hermes config set model.default <model>
```

**Copilot OAuth** — `gh auth login` tokens do NOT work. Must use Copilot-specific flow:
```bash
python3 -c "
from hermes_cli.copilot_auth import copilot_device_code_login
token = copilot_device_code_login()
if token: print(f'COPILOT_GITHUB_TOKEN={token}')
" >> ~/.hermes/.env
```
If import fails, prepend: `import sys; sys.path.insert(0, '$HOME/.hermes/hermes-agent')`
User must open the printed URL and enter the code in browser.

**Ollama / Custom:**
```bash
hermes config set model.provider custom
hermes config set model.base_url http://localhost:11434/v1
```

**Credential pool** (optional, for same-provider fallback): `hermes auth add --provider <p>` to add extra keys. Strategy: `hermes config set credential_pool_strategies.<provider> round_robin`

**Free model tip:** OpenRouter offers free models like `nvidia/nemotron-3-super-120b-a12b:free` — good for zero-cost testing.

**Ask:** Which default model?

---

### Section 1.5: Auxiliary Models

Hermes uses lightweight auxiliary models for session search, context compression, vision analysis, and memory management. If left as `auto`, these require an OpenRouter or Gemini key. Otherwise, explicitly configure them.

**Ask:** Configure auxiliary models with same provider, or skip (use auto)?

If configuring:
```bash
for task in vision web_extract compression session_search approval skills_hub mcp flush_memories; do
  hermes config set auxiliary.${task}.provider <provider>
  hermes config set auxiliary.${task}.model <model>
done
hermes config set compression.summary_model <model>
hermes config set compression.summary_provider <provider>
```

Recommended auxiliary models per provider:

| Main Provider | Auxiliary Model |
|--------------|----------------|
| Copilot | `gemini-3-flash-preview` or `claude-sonnet-4.6` |
| OpenRouter | `google/gemini-3-flash-preview` |
| Gemini | `gemini-3-flash-preview` |
| Anthropic | `claude-haiku-4.5` |
| Ollama | Same local model |

---

### Section 2: Terminal Backend

**Ask (single-select):** Where should commands execute?

| Backend | Value | Extra Config |
|---------|-------|-------------|
| Local (default) | `local` | `cwd: "."` |
| Docker | `docker` | `docker_image`, resource limits |
| SSH | `ssh` | `ssh_host`, `ssh_user`, `ssh_port`, `ssh_key` |
| Modal | `modal` | `pip install modal && modal setup` |
| Daytona | `daytona` | `DAYTONA_API_KEY` |
| Singularity | `singularity` | `singularity_image` (HPC only) |

```bash
hermes config set terminal.backend <value>
```

Docker extra:
```bash
hermes config set terminal.docker_image "nikolaik/python-nodejs:python3.11-nodejs20"
hermes config set terminal.cwd /workspace
hermes config set terminal.container_cpu 1
hermes config set terminal.container_memory 5120
hermes config set terminal.container_persistent true
```

SSH extra: ask for host, user, port, key path, remote cwd.

---

### Section 3: Agent Settings

Apply recommended defaults:
```bash
hermes config set agent.max_turns 90
hermes config set display.tool_progress all
hermes config set compression.enabled true
hermes config set compression.threshold 0.50
hermes config set session_reset.mode both
hermes config set session_reset.idle_minutes 1440
hermes config set session_reset.at_hour 4
```

---

### Section 4: Messaging Platforms

**Ask (multi-select):** Which platforms to connect?

#### Telegram
Guide: "@BotFather → `/newbot` → copy token. User ID from @userinfobot."
**Ask:** Bot token, user ID, use as home channel?
```bash
echo "TELEGRAM_BOT_TOKEN=<token>" >> ~/.hermes/.env
echo "TELEGRAM_ALLOWED_USERS=<id>" >> ~/.hermes/.env
echo "TELEGRAM_HOME_CHANNEL=<id>" >> ~/.hermes/.env
```

#### Discord
Guide: "https://discord.com/developers/applications → New App → Bot."
**Critical:** Enable **Message Content Intent** under Bot → Privileged Gateway Intents.
OAuth2 → URL Generator: enable `bot` + `applications.commands` scopes. Permissions: Send Messages, Read Message History, Attach Files.
**Ask:** Bot token, allowed user IDs (Developer Mode → right-click → Copy ID), home channel ID
```bash
echo "DISCORD_BOT_TOKEN=<token>" >> ~/.hermes/.env
echo "DISCORD_ALLOWED_USERS=<ids>" >> ~/.hermes/.env
echo "DISCORD_HOME_CHANNEL=<channel_id>" >> ~/.hermes/.env
```

#### Slack
Guide: "https://api.slack.com/apps → New App. Enable Socket Mode → create App-Level Token (`connections:write`)."
Required scopes: `chat:write, app_mentions:read, channels:history, channels:read, im:history, im:read, im:write, users:read, files:write`. Optional: `groups:history` (private channels).
Events: `message.im, message.channels, app_mention`. Optional: `message.groups`.
**Warning:** Without `message.channels` event, bot works in DMs only.
Install to workspace, then `/invite @BotName` in channels.
**Ask:** Bot Token (xoxb-), App Token (xapp-), allowed user IDs, home channel ID
```bash
echo "SLACK_BOT_TOKEN=<token>" >> ~/.hermes/.env
echo "SLACK_APP_TOKEN=<token>" >> ~/.hermes/.env
echo "SLACK_ALLOWED_USERS=<ids>" >> ~/.hermes/.env
echo "SLACK_HOME_CHANNEL=<channel_id>" >> ~/.hermes/.env
```

#### Matrix
Guide: "Create bot on homeserver, get access token from Element."
**Ask:** Homeserver URL, access token (or user ID + password), enable E2EE?, allowed users (`@user:server`), home room (`!room:server`)
```bash
echo "MATRIX_HOMESERVER=<url>" >> ~/.hermes/.env
echo "MATRIX_ACCESS_TOKEN=<token>" >> ~/.hermes/.env
echo "MATRIX_ALLOWED_USERS=<ids>" >> ~/.hermes/.env
echo "MATRIX_HOME_ROOM=<room_id>" >> ~/.hermes/.env
# If E2EE: echo "MATRIX_ENCRYPTION=true" >> ~/.hermes/.env
# Install: python3 -m pip install "mautrix[encryption]"
```

#### Mattermost
Guide: "Integrations → Bot Accounts → Add Bot → copy token."
**Ask:** Server URL, bot token, allowed user IDs, home channel ID
```bash
echo "MATTERMOST_URL=<url>" >> ~/.hermes/.env
echo "MATTERMOST_TOKEN=<token>" >> ~/.hermes/.env
echo "MATTERMOST_ALLOWED_USERS=<ids>" >> ~/.hermes/.env
echo "MATTERMOST_HOME_CHANNEL=<id>" >> ~/.hermes/.env
```

#### WhatsApp
Guide: "After config, run `hermes whatsapp` to choose mode (dedicated bot number vs personal self-chat) and pair via QR."
**Ask:** Allowed phone numbers (E.164 format, e.g. `15551234567`)
```bash
echo "WHATSAPP_ENABLED=true" >> ~/.hermes/.env
echo "WHATSAPP_ALLOWED_USERS=<phones>" >> ~/.hermes/.env
```

#### Signal
Guide: "Requires `signal-cli` running as HTTP daemon. Install: `brew install signal-cli` or from GitHub releases. Link account first: `signal-cli link -n HermesAgent`."
**Ask:** HTTP URL (e.g. `http://127.0.0.1:8080`), phone number (E.164), allowed users, home channel
```bash
echo "SIGNAL_HTTP_URL=<url>" >> ~/.hermes/.env
echo "SIGNAL_ACCOUNT=<phone>" >> ~/.hermes/.env
echo "SIGNAL_ALLOWED_USERS=<phones>" >> ~/.hermes/.env
echo "SIGNAL_HOME_CHANNEL=<phone_or_group>" >> ~/.hermes/.env
```

#### Email
Guide: "For Gmail: enable 2FA → create App Password at https://myaccount.google.com/apppasswords"
**Ask:** Email address, app password, IMAP host/port, SMTP host/port, allowed senders, home address
```bash
echo "EMAIL_ADDRESS=<email>" >> ~/.hermes/.env
echo "EMAIL_PASSWORD=<app_password>" >> ~/.hermes/.env
echo "EMAIL_IMAP_HOST=imap.gmail.com" >> ~/.hermes/.env
echo "EMAIL_IMAP_PORT=993" >> ~/.hermes/.env
echo "EMAIL_SMTP_HOST=smtp.gmail.com" >> ~/.hermes/.env
echo "EMAIL_SMTP_PORT=587" >> ~/.hermes/.env
echo "EMAIL_ALLOWED_USERS=<emails>" >> ~/.hermes/.env
echo "EMAIL_HOME_ADDRESS=<email>" >> ~/.hermes/.env
```

#### DingTalk
Guide: "Create robot at https://open-dev.dingtalk.com → Stream Mode."
**Ask:** Client ID, Client Secret, allowed user IDs
```bash
echo "DINGTALK_CLIENT_ID=<id>" >> ~/.hermes/.env
echo "DINGTALK_CLIENT_SECRET=<secret>" >> ~/.hermes/.env
echo "DINGTALK_ALLOWED_USERS=<ids>" >> ~/.hermes/.env
```

#### Feishu / Lark
Guide: "Create app at https://open.feishu.cn/app → get App ID and Secret."
**Ask:** App ID, App Secret, domain (`feishu.cn` or `larksuite.com`), connection mode (`websocket` default or `webhook`), allowed users, home channel
```bash
echo "FEISHU_APP_ID=<id>" >> ~/.hermes/.env
echo "FEISHU_APP_SECRET=<secret>" >> ~/.hermes/.env
echo "FEISHU_DOMAIN=feishu.cn" >> ~/.hermes/.env
echo "FEISHU_CONNECTION_MODE=websocket" >> ~/.hermes/.env
echo "FEISHU_ALLOWED_USERS=<ids>" >> ~/.hermes/.env
echo "FEISHU_HOME_CHANNEL=<chat_id>" >> ~/.hermes/.env
# If webhook mode, also set:
# echo "FEISHU_ENCRYPT_KEY=<key>" >> ~/.hermes/.env
# echo "FEISHU_VERIFICATION_TOKEN=<token>" >> ~/.hermes/.env
```

#### WeCom (企业微信)
**Ask:** Bot ID, Secret, allowed users, home channel
```bash
echo "WECOM_BOT_ID=<id>" >> ~/.hermes/.env
echo "WECOM_SECRET=<secret>" >> ~/.hermes/.env
echo "WECOM_ALLOWED_USERS=<ids>" >> ~/.hermes/.env
echo "WECOM_HOME_CHANNEL=<chat_id>" >> ~/.hermes/.env
```

#### Weixin (WeChat)
Guide: "Run `hermes gateway setup` → select Weixin. Scan QR code with WeChat to authenticate. Credentials stored automatically."
This platform requires interactive QR login — cannot be configured via env vars alone.

#### BlueBubbles (iMessage)
Guide: "Requires BlueBubbles server on a Mac."
**Ask:** Server URL, password, allowed users
```bash
echo "BLUEBUBBLES_SERVER_URL=<url>" >> ~/.hermes/.env
echo "BLUEBUBBLES_PASSWORD=<pass>" >> ~/.hermes/.env
echo "BLUEBUBBLES_ALLOWED_USERS=<ids>" >> ~/.hermes/.env
echo "BLUEBUBBLES_HOME_CHANNEL=<chat_id>" >> ~/.hermes/.env
```

#### Webhooks (GitHub/GitLab)
**Ask:** Port (default: 8644), secret
```bash
echo "WEBHOOK_ENABLED=true" >> ~/.hermes/.env
echo "WEBHOOK_PORT=8644" >> ~/.hermes/.env
echo "WEBHOOK_SECRET=<secret>" >> ~/.hermes/.env
```

#### Install Gateway Service

If any platform configured:
```bash
hermes gateway install
hermes gateway start
```

- **Linux:** Creates systemd user service. Enable linger for SSH persistence: `sudo loginctl enable-linger $USER`. For system service (starts on boot): `sudo hermes gateway install --system --run-as-user <user>`
- **macOS:** Creates launchd agent at `~/Library/LaunchAgents/ai.hermes.gateway.plist`. Starts at login. Logs: `~/.hermes/logs/gateway.log`
- **WSL2:** Requires `systemd=true` in `/etc/wsl.conf`. Without it, falls back to `nohup` (dies when session closes).

---

### Section 5: Tools

**Ask (multi-select):** Which tools to enable?

| Tool | Env Var | Get Key |
|------|---------|---------|
| Web Search (Exa) | `EXA_API_KEY` | https://exa.ai |
| Web Search (Tavily) | `TAVILY_API_KEY` | https://tavily.com |
| Web Search (Parallel) | `PARALLEL_API_KEY` | https://parallel.ai |
| Web Crawl (Firecrawl) | `FIRECRAWL_API_KEY` | https://firecrawl.dev |
| Image Gen (FAL) | `FAL_KEY` | https://fal.ai |
| Browser (Browserbase) | `BROWSERBASE_API_KEY` + `BROWSERBASE_PROJECT_ID` | https://browserbase.com |
| Browser (Camofox) | `CAMOFOX_URL` | Self-hosted (see below) |
| Browser (Browser Use) | `BROWSER_USE_API_KEY` | https://browser-use.com |
| Voice STT (local) | None | Default, uses `faster-whisper` (~150MB model) |
| Voice STT (Groq) | `GROQ_API_KEY` | https://groq.com |
| Voice STT (OpenAI) | `VOICE_TOOLS_OPENAI_KEY` | https://platform.openai.com |
| TTS | See below | Provider-specific |
| X/Twitter | 5 keys | https://developer.x.com |
| Home Assistant | `HASS_TOKEN` + `HASS_URL` | Your HA instance |
| Skills Hub search | `GITHUB_TOKEN` | https://github.com/settings/tokens |
| Honcho (user modeling) | `HONCHO_API_KEY` | https://app.honcho.dev |

**TTS providers** — set with `hermes config set tts.provider <name>`:
- `edge` (default, free, no key)
- `elevenlabs` (requires `ELEVENLABS_API_KEY`)
- `openai` (requires `VOICE_TOOLS_OPENAI_KEY`)
- `minimax` (requires `MINIMAX_API_KEY`)
- `neutts` (local/offline, requires `espeak-ng` system package + ~300MB model)

**STT providers** — set with `hermes config set stt.provider <name>`:
- `local` (default, `faster-whisper`, no key)
- `groq` (requires `GROQ_API_KEY`)
- `openai` (requires `VOICE_TOOLS_OPENAI_KEY`)

For each selected tool: ask for key, write to `~/.hermes/.env`, then `chmod 600 ~/.hermes/.env`.

**Camofox** self-hosted browser:
```bash
git clone https://github.com/jo-inc/camofox-browser.git ~/camofox-browser
cd ~/camofox-browser && npm install
nohup node server.js > /tmp/camofox.log 2>&1 &
echo "CAMOFOX_URL=http://localhost:9377" >> ~/.hermes/.env
hermes config set browser.camofox.managed_persistence true
```

---

### Section 6: MCP Servers (Optional)

MCP (Model Context Protocol) connects external tool servers.

```bash
# HTTP server
hermes mcp add <name> --url <endpoint>

# Stdio server
hermes mcp add <name> --command <cmd> --args '<json_args>'

# List/test
hermes mcp list
hermes mcp test <name>
```

---

## Verification

```bash
hermes --version
hermes doctor                    # Canonical health check
hermes gateway status            # Gateway running?
hermes config show | head -20    # Config summary
```

After verification, secure secrets: `chmod 600 ~/.hermes/.env`

Edit `~/.hermes/SOUL.md` to customize agent personality. Changes take effect immediately.

## Pitfalls

| Problem | Cause | Fix |
|---------|-------|-----|
| Copilot 403 | Used `gh auth login` token | Must use Copilot-specific OAuth (Section 1) |
| Gateway dies on SSH logout | Linger not enabled | `sudo loginctl enable-linger $USER` |
| Gateway dies on WSL close | systemd not enabled | Add `systemd=true` to `/etc/wsl.conf`, restart WSL |
| Discord bot silent | Missing Message Content Intent | Bot settings → Privileged Gateway Intents → enable |
| Slack bot DMs only | Missing `message.channels` event | Add event subscription in Slack app settings |
| `hermes` not found | PATH not updated | `source ~/.bashrc` or add venv/bin to PATH |
| Docker permission denied | Not in docker group | `sudo usermod -aG docker $USER` then re-login |
| Auxiliary "auto" no-op | No OpenRouter/Gemini key | Explicitly set `auxiliary.<task>.provider` |
| Matrix E2EE fails | Missing crypto deps | `python3 -m pip install "mautrix[encryption]"` |
| Termux install fails | Wrong extras | Use `.[termux]` not `.[all]`, add `-c constraints-termux.txt` |
| .env world-readable | Shell `echo >>` default perms | `chmod 600 ~/.hermes/.env` after writing |
| Windows 400 "No models" | Config file encoding (BOM) | Ensure `config.yaml` is saved as UTF-8 without BOM |
| Auxiliary "auto" silent fail | No OpenRouter/Gemini key for aux | Explicitly set `auxiliary.<task>.provider` per Section 1.5 |
