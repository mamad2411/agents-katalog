---
name: hermes-web-ui-dashboard
description: Web dashboard for managing Hermes Agent multi-platform AI chat sessions, analytics, scheduled jobs, and platform channels
triggers:
  - set up hermes web ui dashboard
  - manage hermes agent sessions
  - configure hermes platform channels
  - view hermes usage analytics
  - create hermes scheduled jobs
  - deploy hermes web interface
  - configure telegram discord slack for hermes
  - monitor hermes ai chat costs
---

# Hermes Web UI Dashboard

> Skill by [ara.so](https://ara.so) — Hermes Skills collection.

Hermes Web UI is a full-featured web dashboard for [Hermes Agent](https://github.com/NousResearch/hermes-agent). It provides AI chat session management, usage analytics, platform channel configuration (Telegram, Discord, Slack, WhatsApp, Matrix, Feishu, WeChat, WeCom), scheduled cron jobs, model management, file browsing, multi-profile support, and gateway control through a responsive Vue 3 interface.

## Installation

### Global npm Installation (Recommended)

```bash
npm install -g hermes-web-ui
hermes-web-ui start
```

Access at **http://localhost:8648**

### Docker Compose

```bash
# Using pre-built image
WEBUI_IMAGE=ekkoye8888/hermes-web-ui docker compose up -d

# Or build from source
docker compose up -d --build

# View logs
docker compose logs -f hermes-webui
```

Access at **http://localhost:6060**

### Auto-Setup Script (Linux/macOS)

```bash
bash <(curl -fsSL https://raw.githubusercontent.com/EKKOLearnAI/hermes-web-ui/main/scripts/setup.sh)
```

### Development Setup

```bash
git clone https://github.com/EKKOLearnAI/hermes-web-ui.git
cd hermes-web-ui
npm install
npm run dev
```

- Frontend dev server: http://localhost:5173
- BFF server: http://localhost:8648

## CLI Commands

```bash
# Start in background (daemon mode)
hermes-web-ui start

# Start on custom port
hermes-web-ui start --port 9000

# Stop background process
hermes-web-ui stop

# Restart
hermes-web-ui restart

# Check running status
hermes-web-ui status

# Update to latest version and restart
hermes-web-ui update
# or
hermes-web-ui upgrade

# Show version
hermes-web-ui -v

# Show help
hermes-web-ui -h
```

## Environment Variables

Configure the Web UI server (not Hermes Agent itself):

```bash
# Web UI listen port
export PORT=8648

# Bind host (use :: for IPv6)
export BIND_HOST=0.0.0.0

# Web UI data directory (auth token, logs, DB)
export HERMES_WEB_UI_HOME=~/.hermes-web-ui

# Upload directory override
export UPLOAD_DIR=$HERMES_WEB_UI_HOME/upload

# CORS origins
export CORS_ORIGINS=*

# Disable authentication
export AUTH_DISABLED=1

# Explicit bearer token (auto-generated if unset)
export AUTH_TOKEN=your-secret-token

# Initial Hermes profile
export PROFILE=default

# Server log level
export LOG_LEVEL=info

# Bridge log level
export BRIDGE_LOG_LEVEL=info

# File size limits
export MAX_DOWNLOAD_SIZE=200MB
export MAX_EDIT_SIZE=10MB

# Workspace base directory
export WORKSPACE_BASE=/opt/data/workspace

# Gateway host for profile config
export GATEWAY_HOST=127.0.0.1

# Stop gateways on shutdown
export HERMES_WEB_UI_STOP_GATEWAYS_ON_SHUTDOWN=true
```

## Docker Environment Configuration

In `docker-compose.yml`:

```yaml
services:
  hermes-webui:
    image: ekkoye8888/hermes-web-ui:latest
    container_name: hermes-webui
    ports:
      - "6060:8648"
    environment:
      - PORT=8648
      - BIND_HOST=0.0.0.0
      - HERMES_WEB_UI_HOME=/app/data/hermes-web-ui
      - AUTH_DISABLED=0
      - PROFILE=default
      - LOG_LEVEL=info
      - MAX_DOWNLOAD_SIZE=200MB
      - WORKSPACE_BASE=/app/data/workspace
    volumes:
      - ./hermes_data:/app/data
    restart: unless-stopped
```

## Architecture

```
Browser → BFF Server (Koa :8648) → Hermes Gateway (:8642)
              ↓
         Hermes CLI (sessions, logs)
              ↓
         ~/.hermes/config.yaml   (channel behavior)
         ~/.hermes/auth.json     (credentials)
         ~/.hermes-web-ui/       (Web UI data)
```

**BFF Layer Responsibilities:**
- API proxy with path rewriting
- SSE streaming from Hermes Gateway
- File upload/download (local, Docker, SSH, Singularity backends)
- Session CRUD via Hermes CLI
- Config and credential management
- WeChat QR login via Tencent iLink API
- Model discovery from credential pool
- Skills and memory management
- Log reading and parsing

**Frontend:** Vue 3 + TypeScript + Vite + Naive UI + Pinia + Vue Router

## Key Features & Usage

### AI Chat Sessions

The Web UI maintains its own SQLite session database separate from Hermes' `state.db`:

```typescript
// Create new chat session via Socket.IO
import { io } from 'socket.io-client';

const socket = io('http://localhost:8648');

socket.emit('chat-run', {
  sessionId: 'session-123',
  message: 'Hello, Hermes!',
  model: 'gpt-4',
  profile: 'default'
});

socket.on('chat-delta', (data) => {
  console.log('Streaming chunk:', data.content);
});

socket.on('chat-done', (data) => {
  console.log('Response complete:', data);
});
```

**Session Management:**
- Sessions grouped by source (Telegram, Discord, Slack, etc.)
- Active sessions pinned to top with spinner
- Sessions sorted by latest message time
- Markdown rendering with syntax highlighting
- Tool call expansion (arguments/result)
- File upload and download support
- Ctrl+K global search across sessions
- Per-session model badge and token usage display

### Platform Channel Configuration

Configure 8 platforms from a unified interface. Settings write to:
- Credentials → `~/.hermes/.env`
- Behavior → `~/.hermes/config.yaml`

**Example Telegram Configuration:**

```yaml
# ~/.hermes/config.yaml
telegram:
  mention_control: true
  reactions_enabled: true
  free_response_chats:
    - -1001234567890
```

```bash
# ~/.hermes/.env
TELEGRAM_BOT_TOKEN=your_bot_token_here
```

**Supported Platforms:**
- **Telegram:** Bot token, mention control, reactions, free-response chats
- **Discord:** Bot token, mention, auto-thread, reactions, channel allow/ignore
- **Slack:** Bot token, mention control, bot message handling
- **WhatsApp:** Enable/disable, mention control, mention patterns
- **Matrix:** Access token, homeserver, auto-thread, DM mention threads
- **Feishu (Lark):** App ID/Secret, mention control
- **WeChat:** QR code login (scan in browser)
- **WeCom:** Bot ID/Secret

The Web UI auto-restarts the gateway on config changes.

### Model Management

Models are auto-discovered from `~/.hermes/auth.json` credential pool:

```json
{
  "providers": [
    {
      "name": "openai",
      "type": "openai",
      "base_url": "https://api.openai.com/v1",
      "api_key": "${OPENAI_API_KEY}",
      "models": ["gpt-4", "gpt-3.5-turbo"]
    },
    {
      "name": "anthropic",
      "type": "anthropic",
      "base_url": "https://api.anthropic.com/v1",
      "api_key": "${ANTHROPIC_API_KEY}",
      "models": ["claude-3-opus-20240229"]
    }
  ]
}
```

**Model Discovery API:**

```bash
# Fetch available models from provider
GET http://localhost:8648/api/models/providers/openai/models
```

**Add Custom Provider:**

```typescript
// POST /api/models/providers
const response = await fetch('http://localhost:8648/api/models/providers', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer your-auth-token'
  },
  body: JSON.stringify({
    name: 'custom-llm',
    type: 'openai-compatible',
    base_url: 'https://api.custom-llm.com/v1',
    api_key: process.env.CUSTOM_LLM_KEY,
    models: ['custom-model-7b']
  })
});
```

### Usage Analytics

View token usage, session counts, estimated costs, and 30-day trends:

```bash
# Get usage analytics
GET http://localhost:8648/api/analytics/usage
```

**Response:**

```json
{
  "totalTokens": 1500000,
  "inputTokens": 800000,
  "outputTokens": 700000,
  "sessionCount": 245,
  "dailyAverage": 8.2,
  "estimatedCost": 12.45,
  "cacheHitRate": 0.35,
  "modelDistribution": {
    "gpt-4": 60,
    "claude-3-opus": 30,
    "gpt-3.5-turbo": 10
  },
  "dailyTrend": [
    { "date": "2026-05-01", "tokens": 50000, "cost": 0.42 },
    { "date": "2026-05-02", "tokens": 48000, "cost": 0.38 }
  ]
}
```

### Scheduled Jobs (Cron)

Create and manage cron jobs for recurring tasks:

```typescript
// POST /api/cron/jobs
const job = await fetch('http://localhost:8648/api/cron/jobs', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'Authorization': `Bearer ${process.env.AUTH_TOKEN}`
  },
  body: JSON.stringify({
    name: 'Daily Report',
    schedule: '0 9 * * *', // 9 AM daily
    command: 'hermes agent run --prompt "Generate daily summary"',
    enabled: true
  })
});
```

**Cron Presets:**
- Every hour: `0 * * * *`
- Daily at 9 AM: `0 9 * * *`
- Weekly Monday 9 AM: `0 9 * * 1`
- Monthly 1st 9 AM: `0 9 1 * *`

**Job Operations:**

```bash
# List all jobs
GET /api/cron/jobs

# Pause job
PATCH /api/cron/jobs/:id/pause

# Resume job
PATCH /api/cron/jobs/:id/resume

# Trigger immediate execution
POST /api/cron/jobs/:id/trigger

# Delete job
DELETE /api/cron/jobs/:id
```

### Multi-Profile Management

Create isolated Hermes profiles with separate configs and caches:

```typescript
// POST /api/profiles
const profile = await fetch('http://localhost:8648/api/profiles', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'Authorization': `Bearer ${process.env.AUTH_TOKEN}`
  },
  body: JSON.stringify({
    name: 'production',
    cloneFrom: 'default' // Optional: clone existing profile
  })
});

// Switch active profile
// POST /api/profiles/production/activate

// Export profile for backup
// GET /api/profiles/production/export
// Returns .tar.gz archive

// Import profile
// POST /api/profiles/import
// FormData with .tar.gz file
```

**Gateway Management per Profile:**

```bash
# Start gateway for profile
POST /api/profiles/:name/gateway/start

# Stop gateway
POST /api/profiles/:name/gateway/stop

# Get gateway status
GET /api/profiles/:name/gateway/status
```

### File Browser

Browse and manage files on remote backends:

```typescript
// List directory contents
const files = await fetch('http://localhost:8648/api/files/list?path=/workspace', {
  headers: { 'Authorization': `Bearer ${process.env.AUTH_TOKEN}` }
});

// Upload file
const formData = new FormData();
formData.append('file', fileBlob);
formData.append('path', '/workspace/data');

await fetch('http://localhost:8648/api/files/upload', {
  method: 'POST',
  headers: { 'Authorization': `Bearer ${process.env.AUTH_TOKEN}` },
  body: formData
});

// Download file
GET /api/files/download?path=/workspace/output.txt

// Create directory
POST /api/files/mkdir
Content-Type: application/json
{ "path": "/workspace/new-dir" }

// Delete file
DELETE /api/files/delete?path=/workspace/old-file.txt

// Rename/move
POST /api/files/rename
{ "oldPath": "/workspace/old.txt", "newPath": "/workspace/new.txt" }
```

**Supported Backends:**
- Local filesystem
- Docker containers
- SSH remote hosts
- Singularity containers

### Group Chat (Multi-Agent)

Create chat rooms with multiple agents and context compression:

```typescript
import { io } from 'socket.io-client';

const socket = io('http://localhost:8648');

// Create room
socket.emit('room-create', {
  name: 'Engineering Team',
  agents: [
    { name: 'CodeReviewer', profile: 'default' },
    { name: 'Architect', profile: 'production' }
  ]
});

// Send message with @mention
socket.emit('room-message', {
  roomId: 'room-123',
  content: '@CodeReviewer can you review this function?',
  userId: 'user-456'
});

// Receive agent reply
socket.on('room-agent-reply', (data) => {
  console.log(`${data.agentName}: ${data.message}`);
});
```

**Features:**
- @mention routing to specific agents
- Auto context compression when history exceeds token threshold
- Typing status and reply progress
- SQLite message persistence
- Invite code management

### Authentication

```bash
# First run generates token in ~/.hermes-web-ui/.token
cat ~/.hermes-web-ui/.token

# Use token in API requests
curl -H "Authorization: Bearer your-token-here" \
  http://localhost:8648/api/sessions

# Disable auth (not recommended for production)
export AUTH_DISABLED=1
hermes-web-ui start
```

**Username/Password Auth:**

After initial token auth, set up username/password via Settings page. Credentials stored in Web UI database.

### Web Terminal

Integrated terminal with multi-session support:

```typescript
// WebSocket connection for PTY
const ws = new WebSocket('ws://localhost:8648/terminal');

ws.onopen = () => {
  ws.send(JSON.stringify({
    type: 'create',
    cols: 80,
    rows: 24
  }));
};

ws.onmessage = (event) => {
  const data = JSON.parse(event.data);
  if (data.type === 'output') {
    console.log(data.data); // PTY output
  }
};

// Send keyboard input
ws.send(JSON.stringify({
  type: 'input',
  data: 'ls -la\n'
}));

// Resize terminal
ws.send(JSON.stringify({
  type: 'resize',
  cols: 120,
  rows: 30
}));
```

## Configuration Files

### Hermes Config (`~/.hermes/config.yaml`)

```yaml
api_server:
  host: 127.0.0.1
  port: 8642
  cors_origins: ["*"]

telegram:
  mention_control: true
  reactions_enabled: true
  free_response_chats: []

discord:
  mention_required: true
  auto_thread: true
  reactions_enabled: true
  allowed_channels: []
  ignored_channels: []

memory:
  enabled: true
  max_chars: 10000

agent:
  max_turns: 10
  timeout: 300
  enforce_tools: false

privacy:
  redact_pii: false
```

### Credentials (`~/.hermes/auth.json`)

```json
{
  "providers": [
    {
      "name": "openai",
      "type": "openai",
      "base_url": "https://api.openai.com/v1",
      "api_key": "${OPENAI_API_KEY}",
      "models": ["gpt-4", "gpt-3.5-turbo"]
    }
  ]
}
```

Use environment variable references (`${VAR_NAME}`) instead of hardcoded keys.

## Common Patterns

### Starting Web UI with Custom Config

```bash
export PORT=9000
export LOG_LEVEL=debug
export AUTH_DISABLED=1
export HERMES_WEB_UI_HOME=/custom/path
hermes-web-ui start
```

### Programmatic Chat Session

```typescript
import { io, Socket } from 'socket.io-client';

class HermesChatClient {
  private socket: Socket;

  constructor(serverUrl = 'http://localhost:8648') {
    this.socket = io(serverUrl);
  }

  sendMessage(sessionId: string, message: string, model = 'gpt-4'): Promise<string> {
    return new Promise((resolve) => {
      let fullResponse = '';

      this.socket.emit('chat-run', {
        sessionId,
        message,
        model,
        profile: 'default'
      });

      this.socket.on('chat-delta', (data) => {
        fullResponse += data.content;
      });

      this.socket.on('chat-done', () => {
        resolve(fullResponse);
      });
    });
  }

  disconnect() {
    this.socket.disconnect();
  }
}

// Usage
const client = new HermesChatClient();
const response = await client.sendMessage('session-123', 'What is TypeScript?');
console.log(response);
client.disconnect();
```

### Batch Session Export

```bash
# Export all sessions from Web UI database
GET http://localhost:8648/api/sessions/export

# Returns JSON array of all sessions with messages
```

### Auto-Configure Platform on Startup

```typescript
// Auto-configure Telegram on container startup
const configureTelegram = async () => {
  const token = process.env.TELEGRAM_BOT_TOKEN;
  if (!token) return;

  await fetch('http://localhost:8648/api/platforms/telegram', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${process.env.AUTH_TOKEN}`
    },
    body: JSON.stringify({
      bot_token: token,
      mention_control: true,
      reactions_enabled: true
    })
  });
};
```

## Troubleshooting

### Port Already in Use

```bash
# Web UI auto-kills stale processes on startup
# Manual check:
lsof -ti:8648 | xargs kill -9

# Or start on different port
hermes-web-ui start --port 9000
```

### Gateway Not Starting

```bash
# Check gateway status
GET http://localhost:8648/api/gateway/status

# View gateway logs
GET http://localhost:8648/api/logs?file=gateway.log

# Manually start gateway
hermes-web-ui restart
```

### Authentication Token Not Found

```bash
# Token stored in ~/.hermes-web-ui/.token
cat ~/.hermes-web-ui/.token

# Set explicit token
export AUTH_TOKEN=my-secret-token
hermes-web-ui restart

# Or disable auth
export AUTH_DISABLED=1
hermes-web-ui restart
```

### Docker Volume Permissions

```bash
# Fix permissions on host
sudo chown -R $(id -u):$(id -g) ./hermes_data

# Or run container with host UID/GID
docker compose run --user $(id -u):$(id -g) hermes-webui
```

### Model Discovery Fails

```bash
# Check auth.json syntax
cat ~/.hermes/auth.json | jq .

# Verify API keys are set as env vars
echo $OPENAI_API_KEY

# Test provider endpoint manually
curl -H "Authorization: Bearer $OPENAI_API_KEY" \
  https://api.openai.com/v1/models
```

### WebSocket Connection Errors

```javascript
// Check CORS configuration
export CORS_ORIGINS=http://localhost:5173,http://localhost:8648
hermes-web-ui restart

// Verify WebSocket path
const socket = io('http://localhost:8648', {
  path: '/socket.io/',
  transports: ['websocket', 'polling']
});
```

### Session Database Locked

```bash
# SQLite lock issue - restart Web UI
hermes-web-ui restart

# Or clear lock file
rm ~/.hermes-web-ui/sessions.db-wal
rm ~/.hermes-web-ui/sessions.db-shm
```

### Update Fails

```bash
# Clear npm cache and retry
npm cache clean --force
npm install -g hermes-web-ui@latest

# Or reinstall from scratch
npm uninstall -g hermes-web-ui
npm install -g hermes-web-ui
```

## Production Deployment

```bash
# Use systemd service (Linux)
cat > /etc/systemd/system/hermes-web-ui.service <<EOF
[Unit]
Description=Hermes Web UI
After=network.target

[Service]
Type=simple
User=hermes
Environment="PORT=8648"
Environment="AUTH_DISABLED=0"
Environment="LOG_LEVEL=info"
ExecStart=/usr/bin/hermes-web-ui start
Restart=on-failure

[Install]
WantedBy=multi-user.target
EOF

sudo systemctl daemon-reload
sudo systemctl enable hermes-web-ui
sudo systemctl start hermes-web-ui
```

```bash
# Behind nginx reverse proxy
server {
  listen 80;
  server_name hermes.example.com;

  location / {
    proxy_pass http://127.0.0.1:8648;
    proxy_http_version 1.1;
    proxy_set_header Upgrade $http_upgrade;
    proxy_set_header Connection "upgrade";
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
  }

  location /socket.io/ {
    proxy_pass http://127.0.0.1:8648;
    proxy_http_version 1.1;
    proxy_set_header Upgrade $http_upgrade;
    proxy_set_header Connection "upgrade";
  }
}
```

---

**Resources:**
- GitHub: https://github.com/EKKOLearnAI/hermes-web-ui
- npm: https://www.npmjs.com/package/hermes-web-ui
- Homepage: https://ekkolearnai.com
- Docker: https://github.com/EKKOLearnAI/hermes-web-ui/blob/main/docs/docker.md
- Development Guide: https://github.com/EKKOLearnAI/hermes-web-ui/blob/main/DEVELOPMENT.md
