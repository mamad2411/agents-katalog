---
name: hermesclaw-wechat-multi-agent
description: Run Hermes Agent, OpenClaw, and OpenCode simultaneously on a single WeChat account with intelligent message routing
triggers:
  - set up multiple AI agents on WeChat
  - run Hermes and OpenClaw on same WeChat account
  - install HermesClaw for WeChat multi-agent
  - switch between different AI agents in WeChat
  - configure dual agent WeChat bot
  - troubleshoot HermesClaw iLink connection
  - route messages between Hermes and OpenClaw
  - add OpenCode to WeChat bot
---

# HermesClaw WeChat Multi-Agent Skill

> Skill by [ara.so](https://ara.so) — Hermes Skills collection.

HermesClaw enables running multiple AI agents (Hermes Agent, OpenClaw, OpenCode) on a single WeChat account by acting as a proxy router. It solves the token conflict problem where each gateway tries to exclusively lock the iLink connection, causing 403 errors when running simultaneously.

## What HermesClaw Does

HermesClaw is a Python proxy service (~870 lines) that:

- Becomes the **sole iLink API poller** using a shared WeChat token
- Runs two local proxy servers (ports 19999 for OpenClaw, 19998 for Hermes)
- Bridges OpenCode via its native ACP subprocess protocol
- Routes messages based on commands (`/hermes`, `/openclaw`, `/opencode`, `/both`, `/three`)
- Forwards raw iLink protocol messages (text, voice transcriptions, media CDN URLs)
- Does **not** process media, decrypt AES, or touch agent memory — each gateway handles its own

## Prerequisites

Before installing HermesClaw, you need **at least one** of these installed:

1. **OpenClaw** with `openclaw-weixin` gateway (logged into WeChat)
2. **Hermes Agent** with WeChat gateway configured (`hermes gateway`)
3. **OpenCode** CLI (optional, enables `/opencode` and `/three` modes)

## Installation

### Quick Install (Interactive)

```bash
curl -fsSL https://raw.githubusercontent.com/AaronWong1999/hermesclaw/main/install.sh | bash
```

### Non-Interactive Install (CI/CD)

```bash
curl -fsSL https://raw.githubusercontent.com/AaronWong1999/hermesclaw/main/install.sh | HERMESCLAW_YES=1 bash
# Or with the script directly:
# bash install.sh -y
```

### What the Installer Does

1. Detects installed gateways (Hermes, OpenClaw)
2. Extracts iLink token from gateway account files
3. Patches OpenClaw `baseUrl` → `http://127.0.0.1:19999`
4. Patches Hermes `WEIXIN_BASE_URL` → `http://127.0.0.1:19998`
5. Detects OpenCode CLI at `~/.npm-global/bin/opencode` or via `command -v opencode`
6. Installs Python deps: `requests`, `python-dotenv`
7. Creates OpenClaw media symlink (handles path mismatch)
8. Sets up systemd service `hermesclaw`

### Manual Installation Steps

If you need to install manually:

```bash
# 1. Clone the repo
cd ~
git clone https://github.com/AaronWong1999/hermesclaw.git
cd hermesclaw

# 2. Install dependencies
pip3 install requests python-dotenv

# 3. Configure .env
cat > .env << 'EOF'
ILINK_TOKEN=your_ilink_token_here
HERMES_PROXY_PORT=19998
OPENCLAW_PROXY_PORT=19999
OPENCODE_CMD=/path/to/opencode
OPENCODE_MODEL=opencode/minimax-m2.5-free
EOF

# 4. Create systemd service
sudo tee /etc/systemd/system/hermesclaw.service > /dev/null << 'EOF'
[Unit]
Description=HermesClaw WeChat Multi-Agent Router
After=network.target

[Service]
Type=simple
User=$USER
WorkingDirectory=$HOME/hermesclaw
ExecStart=/usr/bin/python3 $HOME/hermesclaw/hermesclaw.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

# 5. Enable and start
sudo systemctl daemon-reload
sudo systemctl enable hermesclaw
sudo systemctl start hermesclaw
```

## Configuration

### Environment Variables (.env)

```bash
# Required: iLink API token (extracted from gateway account files)
ILINK_TOKEN=your_token_here

# Proxy ports (defaults shown)
HERMES_PROXY_PORT=19998
OPENCLAW_PROXY_PORT=19999

# OpenCode integration (optional)
OPENCODE_CMD=/home/user/.npm-global/bin/opencode
OPENCODE_MODEL=opencode/minimax-m2.5-free  # Free, no API key needed
# Other free models: opencode/deepseek-free, opencode/qwen-free, opencode/glm-free

# Logging
LOG_LEVEL=INFO  # DEBUG for verbose output
```

### Gateway Configuration

**OpenClaw** (`~/.openclaw/openclaw-weixin/accounts/*.json`):
```json
{
  "baseUrl": "http://127.0.0.1:19999",
  "token": "your_token"
}
```

**Hermes** (`~/.hermes/.env`):
```bash
WEIXIN_BASE_URL=http://127.0.0.1:19998
WEIXIN_TOKEN=your_token
```

### Optional: Fix Hermes Message Splitting

Hermes by default splits long messages by newlines. To send as single messages:

```bash
cd ~/hermesclaw
bash fix_hermes_splitting.sh
```

This patches `~/.hermes/hermesagent/gateways/weixin.py` to disable paragraph splitting.

## Commands

### In-WeChat Commands

Send these in any WeChat conversation with the bot:

```text
/hermes       # Route to Hermes Agent only
/openclaw     # Route to OpenClaw only
/opencode     # Route to OpenCode only (voice coding)
/both         # Route to Hermes + OpenClaw (both reply)
/three        # Route to all three agents
/whoami       # Show current routing mode and status
```

Default mode is **Hermes**. In `/both` or `/three` modes, replies are prefixed:
- `[Hermes Agent]`
- `[OpenClaw]`
- `[OpenCode]`

### Service Management

```bash
# Check status
sudo systemctl status hermesclaw

# View logs
journalctl -u hermesclaw -f

# Restart
sudo systemctl restart hermesclaw

# Stop
sudo systemctl stop hermesclaw
```

## Code Examples

### Routing Logic (Python)

```python
# hermesclaw.py core routing
class HermesClawRouter:
    def __init__(self, token):
        self.token = token
        self.route_mode = "hermes"  # default
        self.hermes_proxy = ProxyServer(19998, token)
        self.openclaw_proxy = ProxyServer(19999, token)
        self.opencode_bridge = ACPBridge()
    
    def handle_message(self, msg):
        text = msg.get("content", "").strip()
        
        # Route switching commands
        if text == "/hermes":
            self.route_mode = "hermes"
            return self.send_reply(msg, "Switched to Hermes Agent")
        elif text == "/openclaw":
            self.route_mode = "openclaw"
            return self.send_reply(msg, "Switched to OpenClaw")
        elif text == "/opencode":
            self.route_mode = "opencode"
            return self.send_reply(msg, "Switched to OpenCode")
        elif text == "/both":
            self.route_mode = "both"
            return self.send_reply(msg, "Switched to dual-agent mode")
        elif text == "/three":
            self.route_mode = "three"
            return self.send_reply(msg, "Switched to triple-agent mode")
        
        # Forward to active agent(s)
        if self.route_mode == "hermes":
            self.hermes_proxy.queue_message(msg)
        elif self.route_mode == "openclaw":
            self.openclaw_proxy.queue_message(msg)
        elif self.route_mode == "opencode":
            self.opencode_bridge.send_message(msg)
        elif self.route_mode == "both":
            self.hermes_proxy.queue_message(msg)
            self.openclaw_proxy.queue_message(msg)
        elif self.route_mode == "three":
            self.hermes_proxy.queue_message(msg)
            self.openclaw_proxy.queue_message(msg)
            self.opencode_bridge.send_message(msg)
```

### Proxy Server Implementation

```python
class ProxyServer:
    def __init__(self, port, token):
        self.port = port
        self.token = token
        self.message_queue = queue.Queue()
        
    def run(self):
        app = Flask(__name__)
        
        @app.route("/v1/weixinbot/getupdate", methods=["POST"])
        def get_update():
            # Pop from queue and return to gateway
            try:
                msg = self.message_queue.get(timeout=25)
                return jsonify(msg)
            except queue.Empty:
                return jsonify({"type": "heartbeat"})
        
        @app.route("/v1/weixinbot/sendmessage", methods=["POST"])
        def send_message():
            # Forward to real iLink API
            data = request.json
            response = requests.post(
                "https://ilinkai.weixin.qq.com/v1/weixinbot/sendmessage",
                json=data,
                headers={"Authorization": f"Bearer {self.token}"}
            )
            return response.json()
        
        app.run(host="127.0.0.1", port=self.port)
```

### OpenCode ACP Bridge

```python
class ACPBridge:
    def __init__(self, cmd, model):
        self.cmd = cmd  # Path to opencode CLI
        self.model = model
        self.process = None
        
    def start(self):
        self.process = subprocess.Popen(
            [self.cmd, "acp", "--model", self.model],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=1
        )
        
    def send_message(self, msg):
        # Format as ACP protocol
        acp_msg = {
            "type": "user_message",
            "content": msg.get("content", ""),
            "context": {
                "from": msg.get("from_wxid"),
                "chat_id": msg.get("room_wxid", msg.get("from_wxid"))
            }
        }
        self.process.stdin.write(json.dumps(acp_msg) + "\n")
        self.process.stdin.flush()
        
    def read_response(self):
        while True:
            line = self.process.stdout.readline()
            if not line:
                break
            response = json.loads(line)
            if response.get("type") == "assistant_message":
                return response.get("content")
```

## Common Patterns

### Pattern 1: Voice to OpenCode

OpenCode excels at voice-based coding. Route voice messages:

```text
User: /opencode
User: [voice message: "Create a Python script that reads CSV and generates a bar chart"]
OpenCode: [creates chart.py with pandas and matplotlib]
```

### Pattern 2: Dual-Agent Comparison

Get different perspectives on the same question:

```text
User: /both
User: What's the best way to handle rate limiting in a REST API?
[Hermes Agent]: Use exponential backoff with jitter...
[OpenClaw]: Implement a token bucket algorithm...
```

### Pattern 3: Seamless Switching

Switch contexts without losing conversation history:

```text
User: /hermes
User: Explain async/await in Python
[Hermes responds]
User: /openclaw
User: Now write an example with aiohttp
[OpenClaw responds with code]
```

### Pattern 4: Media Forwarding

HermesClaw forwards raw iLink messages, so each gateway handles media natively:

```python
# Voice message flow:
# 1. iLink sends voice with transcription
# 2. HermesClaw forwards raw message to active gateway(s)
# 3. Gateway extracts transcription or downloads/decrypts audio
# 4. Gateway processes and replies

# Image flow:
# 1. iLink sends CDN URL + AES key
# 2. HermesClaw forwards raw message
# 3. Gateway downloads and decrypts using its native logic
# 4. Gateway processes image (OCR, vision model, etc.)
```

## Troubleshooting

### Problem: 403 Token Conflict

**Symptom**: One gateway works, the other gets 403 errors or no messages.

**Solution**:
```bash
# 1. Verify HermesClaw is running
sudo systemctl status hermesclaw

# 2. Check both gateways point to proxies
grep baseUrl ~/.openclaw/openclaw-weixin/accounts/*.json
# Should show: http://127.0.0.1:19999

grep WEIXIN_BASE_URL ~/.hermes/.env
# Should show: http://127.0.0.1:19998

# 3. Restart all services
sudo systemctl restart hermesclaw
# Restart Hermes gateway
# Restart OpenClaw gateway
```

### Problem: Messages Not Routed

**Symptom**: `/hermes` or `/openclaw` commands don't switch mode.

**Solution**:
```bash
# Check HermesClaw logs
journalctl -u hermesclaw -n 100

# Verify message reception
curl -X POST http://127.0.0.1:19998/v1/weixinbot/getupdate \
  -H "Content-Type: application/json" \
  -d '{}'

# Should return queued message or heartbeat
```

### Problem: OpenCode Not Found

**Symptom**: `/opencode` or `/three` commands don't work.

**Solution**:
```bash
# Install OpenCode
npm install -g opencode-ai

# Verify installation
command -v opencode
# Should print: /home/user/.npm-global/bin/opencode

# Update .env
cd ~/hermesclaw
echo "OPENCODE_CMD=$(command -v opencode)" >> .env

# Restart HermesClaw
sudo systemctl restart hermesclaw
```

### Problem: Media Path Errors

**Symptom**: OpenClaw can't find media files.

**Solution**:
```bash
# HermesClaw installer creates this symlink automatically
ln -sf ~/.openclaw/openclaw-weixin/files ~/hermesclaw/openclaw-weixin-files

# If missing, create manually and restart
sudo systemctl restart hermesclaw
```

### Problem: Long Messages Split

**Symptom**: Hermes sends replies as multiple short messages.

**Solution**:
```bash
cd ~/hermesclaw
bash fix_hermes_splitting.sh

# This patches ~/.hermes/hermesagent/gateways/weixin.py
# to send long replies as single messages
```

### Problem: Token Extraction Failed

**Symptom**: Installer can't find iLink token.

**Manual extraction**:
```bash
# For OpenClaw:
grep -r "token" ~/.openclaw/openclaw-weixin/accounts/*.json

# For Hermes:
grep WEIXIN_TOKEN ~/.hermes/.env

# Add to ~/hermesclaw/.env:
echo "ILINK_TOKEN=your_extracted_token" >> ~/hermesclaw/.env
```

## Architecture Overview

```
┌─────────────────────────────────────┐
│      iLink API (WeChat)             │
│   ilinkai.weixin.qq.com             │
└──────────────┬──────────────────────┘
               │
        (sole poller)
               │
┌──────────────▼──────────────────────┐
│        HermesClaw Router            │
│  - Routes by /hermes /openclaw      │
│  - Queues raw iLink messages        │
│  - Prefix replies in multi-mode     │
├─────────┬─────────┬─────────────────┤
│ Proxy A │ Proxy B │   ACP Bridge    │
│ :19999  │ :19998  │  (subprocess)   │
└────┬────┴────┬────┴────┬────────────┘
     │         │         │
     ▼         ▼         ▼
┌─────────┐ ┌─────────┐ ┌─────────┐
│OpenClaw │ │ Hermes  │ │OpenCode │
│ gateway │ │ gateway │ │   CLI   │
└─────────┘ └─────────┘ └─────────┘
```

## Uninstallation

### Quick Uninstall

```bash
sudo systemctl stop hermesclaw
sudo systemctl disable hermesclaw
sudo rm -f /etc/systemd/system/hermesclaw.service
sudo systemctl daemon-reload

# Restore OpenClaw configs
find "$HOME" -maxdepth 5 -name "*.json.bak" -path "*/openclaw-weixin/accounts/*" \
  -exec sh -c 'for f; do cp "$f" "${f%.bak}"; done' sh {} +

# Restore Hermes .env
[ -f "$HOME/.hermes/.env.bak" ] && cp "$HOME/.hermes/.env.bak" "$HOME/.hermes/.env"

# Remove HermesClaw directory (optional)
rm -rf "$HOME/hermesclaw"
```

## Testing

HermesClaw includes 82 pytest tests covering core routing, proxy servers, ACP bridge, and recovery scenarios:

```bash
cd ~/hermesclaw
pip3 install pytest pytest-mock
python3 -m pytest tests/ -v
```

Key test files:
- `tests/test_core.py` — Routing logic, mode switching
- `tests/test_proxy.py` — Proxy server message queuing
- `tests/test_acp.py` — OpenCode bridge protocol
- `tests/test_recovery.py` — Connection failures, retries

## Advanced Usage

### Custom OpenCode Models

Edit `.env` to use different free models:

```bash
# MiniMax M2.5 (default, recommended)
OPENCODE_MODEL=opencode/minimax-m2.5-free

# DeepSeek (coding-focused)
OPENCODE_MODEL=opencode/deepseek-free

# Qwen (multilingual)
OPENCODE_MODEL=opencode/qwen-free

# GLM (ChatGLM)
OPENCODE_MODEL=opencode/glm-free
```

All models are **free** and require **no API keys**.

### Programmatic Control

Control HermesClaw from other scripts:

```python
import requests

# Switch to dual-agent mode
requests.post("http://127.0.0.1:19998/control", json={
    "action": "set_mode",
    "mode": "both"
})

# Get current status
status = requests.get("http://127.0.0.1:19998/status").json()
print(f"Current mode: {status['mode']}")
print(f"Queued messages: {status['queue_size']}")
```

### Debug Logging

Enable verbose logging:

```bash
# Edit .env
echo "LOG_LEVEL=DEBUG" >> ~/hermesclaw/.env

# Restart and tail logs
sudo systemctl restart hermesclaw
journalctl -u hermesclaw -f
```

## References

- **GitHub**: https://github.com/AaronWong1999/hermesclaw
- **Hermes Agent**: https://github.com/NousResearch/hermes-agent
- **OpenClaw**: https://github.com/openclaw/openclaw
- **OpenCode**: https://github.com/sst/opencode
- **iLink API**: WeChat gateway protocol (proprietary)
