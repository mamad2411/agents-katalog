---
name: ccx-proxy-setup
description: Install, configure, and troubleshoot CCX (BenedictKing/ccx) — a Go-based AI API proxy/gateway. Covers binary installation, .env setup, upstream channel configuration via config.json or web UI, protocol translation between Claude Messages, Codex Responses, and OpenAI Chat for providers like DeepSeek, plus Claude Desktop 3p mode integration.
tags: [ccx, proxy, api-gateway, deepseek, claude-code, claude-desktop, codex, openai, anthropic]
---

# CCX Proxy Setup & Configuration

Use this when the user wants to install or configure [CCX](https://github.com/BenedictKing/ccx) — an AI API proxy that provides a unified entrypoint for Claude Messages, Codex Responses, OpenAI Chat/Images, and Gemini APIs with channel orchestration, failover, and protocol translation.

## Trigger

- User wants to install CCX from GitHub (BenedictKing/ccx)
- User wants to set up CCX as a proxy for DeepSeek or other AI APIs
- User reports connectivity failures when testing Claude Code or Codex through CCX
- User asks about configuring upstream channels in CCX

## Steps

### 1. Install Binary (macOS ARM64 example)

CCX publishes pre-built binaries. Use `install-binary-from-github-releases` skill, or:

```bash
# Get latest version
LATEST=$(curl -s https://api.github.com/repos/BenedictKing/ccx/releases/latest | python3 -c "import sys,json;print(json.load(sys.stdin)['tag_name'])")
PLATFORM="darwin-arm64"  # or darwin-amd64, linux-amd64, etc.

# Download
cd /tmp
curl -sLO "https://github.com/BenedictKing/ccx/releases/latest/download/ccx-${PLATFORM}"
curl -sLO "https://github.com/BenedictKing/ccx/releases/latest/download/ccx-${PLATFORM}.sha256"

# Verify
EXPECTED=$(cat ccx-${PLATFORM}.sha256 | awk '{print $1}')
ACTUAL=$(shasum -a 256 "ccx-${PLATFORM}" | awk '{print $1}')
if [ "$EXPECTED" = "$ACTUAL" ]; then echo "OK"; else echo "FAIL"; fi

# Install
chmod +x "ccx-${PLATFORM}"
sudo mv "ccx-${PLATFORM}" /usr/local/bin/ccx
```

### 2. Create .env Configuration

Always create a dedicated directory (e.g. `~/.ccx/`):

```ini
PROXY_ACCESS_KEY=<your-proxy-key>
ADMIN_ACCESS_KEY=<your-admin-key>
PORT=3000
ENABLE_WEB_UI=true
APP_UI_LANGUAGE=zh
LOG_LEVEL=info
REQUEST_TIMEOUT=300000
```

### 3. Start CCX

```bash
cd ~/.ccx && ccx
```

Or in background:
```bash
terminal(command="cd ~/.ccx && ccx", background=true)
```

### 4. Add Upstream Channels via config.json

CCX auto-detects config file changes. The config lives at `~/.ccx/.config/config.json`.

#### Claude Messages Upstream (for Claude Code)

Point to DeepSeek's Anthropic-compatible endpoint:

```json
{
  "upstream": [
    {
      "baseUrl": "https://api.deepseek.com/anthropic",
      "apiKeys": ["sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"],
      "serviceType": "claude",
      "name": "DeepSeek Claude",
      "priority": 1,
      "status": "active"
    }
  ],
  ...
}
```

**IMPORTANT**: `serviceType` must be `"claude"` (not `"anthropic"`). Using `"anthropic"` causes "Unsupported service type" error because CCX's converter factory only recognizes: `"claude"`, `"openai"`, `"gemini"`, `"responses"`.

#### Codex Responses Upstream

Point to DeepSeek's standard API base (CCX translates Responses → OpenAI Chat):

```json
{
  "responsesUpstream": [
    {
      "baseUrl": "https://api.deepseek.com",
      "apiKeys": ["sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"],
      "serviceType": "openai",
      "name": "DeepSeek",
      "priority": 1,
      "status": "active"
    }
  ],
  ...
}
```

#### Full config.json structure

```json
{
  "upstream": [ /* Claude Messages channels */ ],
  "responsesUpstream": [ /* Codex Responses channels */ ],
  "chatUpstream": [ /* OpenAI Chat channels */ ],
  "imagesUpstream": [ /* OpenAI Images channels */ ],
  "geminiUpstream": [ /* Gemini channels */ ],
  "fuzzyModeEnabled": true,
  "stripBillingHeader": true
}
```

### 5. Verify Connectivity

Check health:
```bash
curl -s http://localhost:3000/health
```

Test Claude Messages:
```bash
curl -s -X POST http://localhost:3000/v1/messages \
  -H "x-api-key: <PROXY_ACCESS_KEY>" \
  -H "anthropic-version: 2023-06-01" \
  -H "Content-Type: application/json" \
  -d '{"model": "deepseek-v4-flash", "max_tokens": 10, "messages": [{"role": "user", "content": "hi"}]}'
```

Test Codex Responses:
```bash
curl -s -X POST http://localhost:3000/v1/responses \
  -H "x-api-key: <PROXY_ACCESS_KEY>" \
  -H "Content-Type: application/json" \
  -d '{"model": "deepseek-v4-flash", "max_output_tokens": 10, "input": "hi"}'
```

### 6. Using with Claude Code

Set these env vars in `~/.claude/settings.json`:

```json
{
  "env": {
    "ANTHROPIC_BASE_URL": "http://localhost:3000",
    "ANTHROPIC_AUTH_TOKEN": "<PROXY_ACCESS_KEY>",
    "ANTHROPIC_DEFAULT_HAIKU_MODEL": "claude-haiku-4-5",
    "ANTHROPIC_DEFAULT_HAIKU_MODEL_NAME": "deepseek-v4-flash",
    "ANTHROPIC_DEFAULT_SONNET_MODEL": "claude-sonnet-4-6",
    "ANTHROPIC_DEFAULT_SONNET_MODEL_NAME": "deepseek-v4-flash",
    "ANTHROPIC_DEFAULT_OPUS_MODEL": "claude-opus-4-7",
    "ANTHROPIC_DEFAULT_OPUS_MODEL_NAME": "deepseek-v4-pro"
  }
}
```

**Model name validation caveat**: Claude Code v2.1+ validates model names against a local model pricing table. Direct use of non-Anthropic model names (like `deepseek-v4-flash`) triggers _"There's an issue with the selected model"_ errors. The `_NAME` env var suffix (e.g., `ANTHROPIC_DEFAULT_SONNET_MODEL_NAME`) overrides the actual model name sent in the API request while keeping the primary name valid for Claude's own validation. Always pair each `ANTHROPIC_DEFAULT_*_MODEL` with its `_NAME` variant when using non-Anthropic providers.

**Pipe mode (`-p`)**: Add `--bare` flag for non-interactive pipe mode with custom providers to skip plugin/hook loading that may interfere:
```bash
claude --bare -p "prompt" --output-format text
```
Without `--bare`, plugins, LSP, auto-memory, and background prefetches may cause empty or delayed responses through the proxy.

### System Role Proxy Fix (Claude Code ≥2.1.154)

Claude Code 2.1.154+ changed how system prompts are sent: instead of the top-level `system` field, it now places `{"role": "system", "content": "..."}` as the first message in the `messages[]` array. Many third-party APIs (CCX/DeepSeek, MiMo, 智谱 GLM-5) do not accept `role: "system"` in messages and return HTTP 400 with `messages[1].role must be either 'user' or 'assistant', but got 'system'`.

**Fix:** A local Node.js proxy that converts `messages[].role=system` back to the top-level `system` field before forwarding to CCX.

**Architecture:** `Claude Code (154+) → proxy:4567 → CCX:3000 → upstream`

The proxy script lives at `~/.claude/claude-mimo-proxy.js`. It:
1. Extracts all `messages[].role=system` entries
2. Merges them with any existing top-level `data.system` field
3. Removes system messages from `messages[]`
4. Sets `data.system` to merged content
5. Forwards to CCX

**Setup (`.zshrc`):**
```bash
if ! lsof -i :4567 > /dev/null 2>&1; then
  nohup node ~/.claude/claude-mimo-proxy.js > /dev/null 2>&1 &
fi
export ANTHROPIC_BASE_URL="http://127.0.0.1:4567"
export ANTHROPIC_AUTH_TOKEN="<CCX...port ANTHROPIC_MODEL="deepseek-v4-flash"
export ANTHROPIC_DEFAULT_OPUS_MODEL="deepseek-v4-pro"
export ANTHROPIC_DEFAULT_SONNET_MODEL="deepseek-v4-flash"
export ANTHROPIC_DEFAULT_HAIKU_MODEL="deepseek-v4-flash"
export CLAUDE_CODE_SUBAGENT_MODEL="deepseek-v4-flash"
```

**Upgrading Claude Code past brew:**
```bash
rm /opt/homebrew/bin/claude
ln -s ~/.npm-global/bin/claude /opt/homebrew/bin/claude
npm install -g @anthropic-ai/claude-code
```

**Verification:** `curl` to `:4567/v1/messages` with a `role: system` message in the payload — expect valid response (not 502).

**Pitfalls:** CCX must be running before proxy starts (ECONNREFUSED otherwise). `--model` flag bypasses `_NAME` mapping (passes model name straight through). Proxy script is in `references/claude-system-role-proxy.js`.

### 7. Web Admin UI

Admin UI at `http://localhost:3000`. Login with `ADMIN_ACCESS_KEY`. Supports:
- Visual channel management (add/edit/reorder)
- Connectivity ping tests
- Traffic monitoring
- Model mapping / redirects

### 8. Using with Claude Desktop (3rd-party mode)

Claude Desktop in 3p mode uses a **separate** data directory from Claude Code CLI:

**Config location**: `~/Library/Application Support/Claude-3p/claude_desktop_config.json`

Key fields in the `enterpriseConfig` object:

```json
{
  "deploymentMode": "3p",
  "enterpriseConfig": {
    "inferenceProvider": "gateway",
    "inferenceGatewayBaseUrl": "http://localhost:3000",
    "inferenceGatewayApiKey": "<PROXY_ACCESS_KEY>",
    "inferenceGatewayAuthScheme": "bearer"
  }
}
```

CCX's PROXY_ACCESS_KEY acts as the API key here. After editing the config, **restart Claude Desktop** (Cmd+Q, reopen) for changes to take effect.

The request flow becomes:
```
Claude Desktop → CCX (localhost:3000/v1/messages) → DeepSeek/upstream API
```

Note: This is independent from Claude Code CLI configuration (`~/.claude/settings.json` with `ANTHROPIC_BASE_URL`). Both can coexist — Claude Desktop uses the 3p data dir, while `claude` CLI uses its own env config.

### Extension Model: What Works Where

When using a 3rd-party API (no Anthropic login), there are sharp capability differences between Claude Desktop and Claude Code CLI:

| Extension Type | Claude Desktop (3p mode) | Claude Code CLI | Notes |
|---|---|---|---|
| **MCP servers** | Yes — via `mcpServers` in `claude_desktop_config.json` | Yes — via env or `--mcp` | Works with any provider, no login needed |
| **Plugins** (`--plugin-dir`, `.claude-plugin/`) | No — only available in Cowork mode (requires login) | Yes — native `--plugin-dir` support | Plugins add custom slash commands, agents, hooks |
| **Skills** (SKILL.md files) | No — only in Cowork mode | Yes — loaded from `~/.claude/skills/` or `/skill` command | Shared format with Hermes Agent |
| **Claude Code CLI** via Desktop | No — Desktop doesn't forward CLI features | N/A | CLI has full plugin/skill/agent ecosystem |

**Practical implications for non-logged-in users:**

- Claude Desktop 3p mode is **chat-only** with MCP server extensions. No plugins, no skills, no agents.
- All plugin and skill features require using `claude` CLI (Claude Code) directly.
- Both can point to the same CCX proxy — configure each independently.

**Claude Code CLI (`~/.claude/`) directory structure:**

```
~/.claude/
├── settings.json              # ANTHROPIC_BASE_URL, enabledPlugins, env overrides
├── config.json                # primaryApiKey
├── skills/                    # SKILL.md files (symlinks or copies)
│   ├── code-review/ -> ../../.agents/skills/code-review
│   └── ...
├── plugins/
│   ├── installed_plugins.json # Tracks all installed plugins
│   ├── known_marketplaces.json # Plugin sources (GitHub repos)
│   ├── blocklist.json
│   ├── cache/                 # Downloaded plugin copies
│   └── marketplaces/          # Cloned marketplace repos
└── projects/                  # Per-project config and worktrees
```

**Key discovery — Desktop app has an internal plugin system (Cowork):**

The Claude Desktop app source code contains a full plugin management system (`LocalPluginsWriter`) that reads `~/.claude/plugins/installed_plugins.json` and supports `.claude-plugin/plugin.json` format with skills, commands, agents, and hooks. However, this system is wired into the **Cowork (agent) mode** session pipeline, which requires an Anthropic account login. The basic 3p chat mode does NOT instantiate plugins or skills.

**Recommendation for 3p users who want extensions:** Use `claude` CLI (Claude Code) instead of the Desktop app. It supports everything — plugins, skills, MCP servers — and works with any provider through CCX proxy.

### MCP Servers for Claude Desktop (3p mode)

MCP servers are the only extension mechanism available in 3p mode. Add them under `mcpServers` in `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": {
        "GITHUB_PERSONAL_ACCESS_TOKEN": "ghp_..."
      }
    },
    "filesystem": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "/Users/me"]
    },
    "sequential-thinking": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-sequential-thinking"]
    },
    "brave-search": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-brave-search"],
      "env": {
        "BRAVE_API_KEY": "..."
      }
    },
    "memory": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-memory"]
    },
    "puppeteer": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-puppeteer"]
    },
    "mcp-time": {
      "command": "uvx",
      "args": ["mcp-server-time"]
    },
    "mcp-sqlite": {
      "command": "uvx",
      "args": ["mcp-server-sqlite", "--db-path", "/Users/me/.mcp-sqlite.db"]
    },
    "mcp-fetch": {
      "command": "uvx",
      "args": ["mcp-server-fetch"]
    }
  }
}
```

These MCP servers correspond to functionality from Claude Code plugins:
- **github** → code-review, pr-review, commit, create-pr, changelog-generator
- **sequential-thinking** → debugger, bug-fix (step-by-step reasoning)
- **puppeteer** → frontend-design, canvas-design (browser preview)
- **memory** → persistent knowledge graph
- **mcp-fetch** → web scraping
- **mcp-sqlite** → database operations

Requires `npx` (Node.js) and/or `uvx` (Python/uv). Restart Claude Desktop (Cmd+Q) to load new servers.

**Computer Use via MCP**: For desktop automation (screenshot, click, type) without an Anthropic subscription, see the `open-computer-use-mcp` skill — installs the `open-computer-use` npm package as an MCP server providing macOS computer use to any MCP client, including Claude Desktop 3p mode.

### 9. Using with VS Code Claude Code Extension

VS Code's Claude Code extension (v2.1+) uses `claudeCode.environmentVariables` in VS Code's `settings.json` to pass environment variables to the Claude Code process it spawns. This is independent from `~/.claude/settings.json`.

**Config location**: `~/Library/Application Support/Code/User/settings.json`

**⚠️ ANTHROPIC_BASE_URL must go through proxy when using Claude Code ≥2.1.154:**
VS Code's extension spawns the same `claude` CLI binary under the hood. If you have the system role proxy (port 4567) to fix the `role: system` issue, VS Code's `ANTHROPIC_BASE_URL` must also point to the proxy, not directly to CCX:
- ❌ `"value": "http://localhost:3000"` — direct to CCX, will get 400 errors from system role messages
- ✅ `"value": "http://127.0.0.1:4567"` — through the proxy, format conversion works

```json
{
  "claudeCode.disableLoginPrompt": true,
  "claudeCode.environmentVariables": [
    { "name": "ANTHROPIC_BASE_URL",                    "value": "http://127.0.0.1:4567" },
    { "name": "ANTHROPIC_API_KEY",                     "value": "<PROXY_ACCESS_KEY>" },
    { "name": "ANTHROPIC_MODEL",                       "value": "claude-sonnet-4-6" },
    { "name": "ANTHROPIC_SMALL_FAST_MODEL",            "value": "claude-haiku-4-5" },
    { "name": "ANTHROPIC_DEFAULT_SONNET_MODEL",        "value": "claude-sonnet-4-6" },
    { "name": "ANTHROPIC_DEFAULT_SONNET_MODEL_NAME",   "value": "deepseek-v4-flash" },
    { "name": "ANTHROPIC_DEFAULT_HAIKU_MODEL",         "value": "claude-haiku-4-5" },
    { "name": "ANTHROPIC_DEFAULT_HAIKU_MODEL_NAME",    "value": "deepseek-v4-flash" },
    { "name": "ANTHROPIC_DEFAULT_OPUS_MODEL",          "value": "claude-opus-4-7" },
    { "name": "ANTHROPIC_DEFAULT_OPUS_MODEL_NAME",     "value": "deepseek-v4-pro" }
  ],
  "claudeCode.selectedModel": "claude-sonnet-4-6"
}
```

**Key points:**
- The `_NAME` suffix env vars (`ANTHROPIC_DEFAULT_SONNET_MODEL_NAME`) are required for non-Anthropic providers — the primary model name must be an Anthropic-recognized name for validation, and `_NAME` overrides what's actually sent in the API request
- `ANTHROPIC_MODEL` sets the default model for the extension's session
- `claudeCode.selectedModel` is the display name shown in the VS Code UI
- After editing VS Code settings, run **Cmd+Shift+P → Developer: Reload Window** for changes to take effect
- The VS Code extension spawns `claude` CLI under the hood, so the same model validation and `_NAME` mapping rules apply

### 10. Using Awesome Claude Plugins with Claude Code CLI

The [awesome-claude-plugins](https://github.com/ComposioHQ/awesome-claude-plugins) repo provides production-ready Claude Code plugins (not Claude Desktop plugins — they only work with `claude` CLI).

```bash
git clone --depth 1 https://github.com/ComposioHQ/awesome-claude-plugins.git /path/to/plugins
```

Load plugins via `--plugin-dir` (repeatable for multiple plugins):

```bash
claude --plugin-dir /path/to/plugins/code-review --plugin-dir /path/to/plugins/commit
```

Or with print mode and all plugins:

```bash
claude --bare --dangerously-skip-permissions \
  --plugin-dir /path/to/plugins/code-review \
  --plugin-dir /path/to/plugins/commit \
  -p "Review my code and suggest a commit message"
```

**MCP equivalents for plugin functionality** (use these if you're on Claude Desktop 3p mode instead):

| Plugin | MCP Equivalent | Setup |
|--------|---------------|-------|
| `code-review`, `pr-review`, `commit`, `create-pr`, `changelog-generator` | GitHub MCP | `npx @modelcontextprotocol/server-github` |
| `debugger`, `bug-fix` | Sequential Thinking | `npx @modelcontextprotocol/server-sequential-thinking` |
| `frontend-design`, `canvas-design` | Puppeteer | `npx @modelcontextprotocol/server-puppeteer` |
| `connect-apps` (500+ integrations) | Composio MCP | Requires Composio API key |
| `documentation-generator` | Filesystem MCP | `npx @modelcontextprotocol/server-filesystem` |

**Available plugins** (each has its own `--plugin-dir`):
- **code-review** — comprehensive code review of recent changes
- **commit** — smart git commits with conventional commit format
- **pr-review** — detailed PR reviews with code quality and security feedback
- **create-pr** — automated PR creation with templates and labels
- **changelog-generator** — auto-generate release notes from git history
- **debugger** — advanced debugging assistant
- **bug-fix** — analyze stack traces and fix bugs
- **backend-architect** — backend patterns, API design, system design
- **frontend-design** — distinctive, production-grade interfaces
- **connect-apps** — connect to 500+ apps (Gmail, Slack, GitHub, Notion, etc.)
- **security-guidance** — OWASP security best practices
- **documentation-generator** — READMEs, API docs, guides
- **perf** — performance analysis and optimization
- **audit-project** — full project audit for code quality and dependencies
- **mcp-builder** — guides creation of MCP servers
- **frontend-developer** — frontend development specialist agent

### CC Switch Integration

[CC Switch](https://github.com/farion1231/cc-switch) is a desktop tray app that manages provider configs across Claude, Codex, Gemini, Hermes, and OpenCode. It stores configurations in a SQLite database and runs a local proxy server on `127.0.0.1:15721` for traffic interception.

CC Switch supports two routing modes:

**1. Direct to DeepSeek (no CCX needed):**
```
Claude Code → CC Switch Proxy (:15721) → DeepSeek API (anthropic/v1/messages)
```
The provider's `ANTHROPIC_BASE_URL` must include the full path `https://api.deepseek.com/anthropic/v1/messages` with `isFullUrl: true` in the DB meta column — otherwise DeepSeek returns 404.

**2. Via CCX (protocol translation / multi-upstream):**
```
App → CC Switch Proxy (:15721) → CCX (:3000) → DeepSeek/upstream
```
Provider configs point back at CCX: `base_url = "http://localhost:3000"`.

Takeover-active CC Switch rewrites `~/.claude/settings.json` to use `ANTHROPIC_AUTH_TOKEN: "PROXY_MANAGED"` and `ANTHROPIC_BASE_URL: "http://127.0.0.1:15721"` — manual edits to settings.json may be overwritten. Make provider changes in the CC Switch DB instead.

Detailed DB schema, proxy config, activation commands, provider config format, model visibility control (hiding sonnet/opus from `claude model list`), and troubleshooting in `references/cc-switch-integration.md`.

### codex-plusplus (Codex Desktop Tweak System)

[codex-plusplus](https://github.com/b-nnett/codex-plusplus) is a tweak system for the Codex desktop app. Install via Homebrew:

```bash
brew install b-nnett/codex-plusplus/codexplusplus
codexplusplus install
```

The installer backs up Codex.app, patches `app.asar`, updates Electron asar integrity, re-signs ad-hoc, installs a LaunchAgent watcher, and installs default tweaks. Tweaks go in `~/Library/Application Support/codex-plusplus/tweaks/`. To update Codex safely, use `codexplusplus update-codex` instead of the in-app updater.

### Codex CLI Limitations with CCX

Codex CLI v0.125+ uses **WebSocket** transport (`wss://api.openai.com/v1/responses`) for the OpenAI Responses API. CCX only supports HTTP POST at `/v1/responses`. This means:

- CCX translates Responses HTTP to Chat Completions, but Codex never sends HTTP — it only uses WebSocket.
- The `wire_api = "chat"` config option was removed from Codex in favor of Responses API only.
- **Codex + non-OpenAI providers through CCX is NOT viable.**
- Use Claude Code CLI or other tools (Aider, Continue.dev) instead.

## Known DeepSeek Upstream Issues

DeepSeek-V4-Pro has a known bug (upstream issue #1244, still open, no fix) where tool calls are intermittently emitted as plain text in `content` instead of structured `tool_calls` objects — ~11% rate in multi-turn sessions. Caused by mode locking during prefill. Schema compression (removing description fields) pushes the failure window from turn ~15 to ~40+.

When thinking/reasoning content doesn't appear in Claude Code through CC Switch, check:
- `streaming_idle_timeout` in proxy_config (default 180s) — too short for long reasoning
- `?beta=true` must be in the upstream URL (CC Switch appends it automatically)
- CC Switch handles thinking blocks internally but Claude Code's TUI may not render them from third-party providers

Full details in `references/deepseek-tool-call-bug.md`.

## Troubleshooting

### CCX Upstream Key Rotated or Expired (Disabled/Suspended)

When an upstream API key is rotated or invalidated (e.g. DeepSeek key rotated after a leak, key revoked at provider), CCX auto-detects `authentication_error` responses, moves the key to `disabledApiKeys`, and sets the upstream `status` to `"suspended"`. Claude Code then fails with `"Authentication Fails, Your api key: ****... is invalid"` through the entire chain.

**Symptoms:**
- `curl http://localhost:3000/v1/messages` returns `authentication_error`
- CCX admin UI shows upstream as "suspended" (红色)
- `cat ~/.ccx/.config/config.json` shows `"disabledApiKeys": [{...}]` and `"status": "suspended"`

**Recovery (no CCX restart needed — auto-reloads within ~2s):**

1. Read the config to confirm the state:
   ```bash
   cat ~/.ccx/.config/config.json | python3 -c "import sys,json;d=json.load(sys.stdin);[print(json.dumps(u,indent=2)) for u in d.get('upstream',[])]"
   ```

2. Update the config — replace the upstream block:
   ```json
   {
     "baseUrl": "https://api.deepseek.com/anthropic",
     "apiKeys": ["<NEW_API_KEY>"],
     "historicalApiKeys": [],
     "disabledApiKeys": [],
     "serviceType": "claude",
     "name": "DeepSeek Claude",
     "priority": 1,
     "status": "active"
   }
   ```

   Key fields to fix:
   - `apiKeys`: replace with the new valid key
   - `disabledApiKeys`: clear to empty array `[]`
   - `historicalApiKeys`: clear to empty array `[]`
   - `status`: change from `"suspended"` to `"active"`

3. Wait ~2s for CCX auto-reload, then verify:
   ```bash
   # Health check
   curl -s http://localhost:3000/health

   # Auth test
   curl -s -X POST http://localhost:3000/v1/messages \
     -H "x-api-key: <PROXY_ACCESS_KEY>" \
     -H "anthropic-version: 2023-06-01" \
     -H "Content-Type: application/json" \
     -d '{"model": "deepseek-v4-flash", "max_tokens": 10, "messages": [{"role": "user", "content": "hi"}]}'
   ```

4. If the proxy layer (port 4567) was also failing, verify the full chain:
   ```bash
   curl -s -X POST http://127.0.0.1:4567/v1/messages \
     -H "x-api-key: <PROXY_ACCESS_KEY>" \
     -H "anthropic-version: 2023-06-01" \
     -H "Content-Type: application/json" \
     -d '{"model":"deepseek-v4-flash","max_tokens":20,"messages":[{"role":"user","content":"hi"}]}'
   ```

5. Test with a `role: system` message to confirm the proxy format conversion still works:
   ```bash
   curl -s -X POST http://127.0.0.1:4567/v1/messages \
     -H "x-api-key: <PROXY_ACCESS_KEY>" \
     -H "anthropic-version: 2023-06-01" \
     -H "Content-Type: application/json" \
     -d '{"model":"deepseek-v4-flash","max_tokens":20,"messages":[{"role":"system","content":"You are helpful"},{"role":"user","content":"hi"}]}'
   ```

**Prevention:** When rotating API keys, always update CCX's config.json in the same operation. The `.ds-key` file and CCX config are two separate storage locations — updating one but not the other leaves the proxy chain broken.

### "Errors in both terminal and VS Code" — Triple Config Diagnostic

When Claude Code fails in both terminal and VS Code plugin, the root cause is rarely a single config issue. Follow this diagnostic order:

1. **Check CCX is running:** `lsof -i :3000` — if not, start it
2. **Check proxy is running:** `lsof -i :4567` — auto-launched via .zshrc
3. **Test proxy directly:** `curl :4567/v1/messages` — isolates proxy/CCX/upstream issues
4. **Inspect `~/.claude/settings.json`:** check BASE_URL, [1M] suffix, AUTH_TOKEN
5. **Inspect VS Code settings:** `claudeCode.environmentVariables` — must match CLI settings
6. **Inspect CCX config:** `~/.ccx/.config/config.json` — check disabledApiKeys and status
7. **Verify `.ds-key` content:** `xxd ~/.hermes/.ds-key` — `cat` may truncate the key

Common root cause clusters:
- **Upstream key disabled** → fix CCX config only (all frontends share CCX)
- **BASE_URL wrong** → fix per-frontend (terminal vs VS Code vs Desktop are independent)
- **[1M] suffix on model names** → fix per-frontend (Claude Code validates locally)
- **CCX not running** → fix once, all frontends come back

## Pitfalls

- **serviceType must be "claude" not "anthropic"**: CCX's `NewConverter()` factory only recognizes "claude", "openai", "gemini", "responses". The web UI displays "anthropic" as label text but the config expects "claude".
- **Config file changes auto-reload**: CCX's `Config-Watcher` detects changes within ~1-2s. No restart needed after editing config.json.
- **API key masking in log**: The raw hex dump of config.json may show the real key while `cat` masks it. Verify with `xxd` if needed.
- **Messages vs Responses upstream**: They are separate arrays (`upstream` vs `responsesUpstream`). Both need to be configured independently.
- **DeepSeek's Anthropic endpoint**: DeepSeek's Anthropic-compatible API lives at `https://api.deepseek.com/anthropic`, not `https://api.deepseek.com`.
- **For Codex**: CCX translates the Responses API → OpenAI Chat Completions via the `openai` serviceType converter. Just point to the base DeepSeek URL.
- **CC Switch DeepSeek base URL must be full path**: When routing directly through CC Switch (without CCX), set `ANTHROPIC_BASE_URL` to `https://api.deepseek.com/anthropic/v1/messages` (not just `/anthropic`). Without `/v1/messages`, DeepSeek returns 404. Also set `isFullUrl: true` in the provider's `meta` column.
- **CC Switch overwrites settings.json**: When takeover is active, CC Switch rewrites `~/.claude/settings.json` with `PROXY_MANAGED` auth and its proxy URL. Manual edits to settings.json may be reverted. Make config changes in the CC Switch DB provider settings instead.

### Trace a real API call through the proxy

Use the techniques in `references/proxy-connection-verification.md` to trace the full network path — DNS resolution chain, proxy tunnel negotiation, TLS handshake, HTTP/2 negotiation, and response headers — when you need to verify the proxy is routing correctly to real upstream APIs.

Key commands:
```bash
# Full DNS chain from root to authoritative
dig +trace dashscope.aliyuncs.com

# Bypass proxy DNS
dig @8.8.8.8 dashscope.aliyuncs.com A +short

# Full API call trace with every connection detail
curl -v --trace-ascii /tmp/trace.txt \
  -H "Authorization: Bearer *** \
  ...  \
  'https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions'
```

What to expect:
- Through CCX proxy → curl shows `Trying 127.0.0.1:1082...`, DNS resolves to `198.18.0.x`
- Without proxy → curl shows `Trying 8.152.159.24:443...` (real Alibaba IP)
- No redirects (direct 200), no port changes

## Verification

After setup, confirm:
- `curl http://localhost:3000/health` returns `{"status":"healthy","config":{"upstreamCount":N}}`
- `POST /v1/messages` returns a valid message response (not 400 error)
- Admin UI at `http://localhost:3000` shows channel as "正常" (healthy)
