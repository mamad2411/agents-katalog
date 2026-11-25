---
name: hermes-studio-dashboard
description: Web dashboard for Hermes Agent with multi-platform AI chat, session management, scheduled jobs, and usage analytics
triggers:
  - set up hermes studio web interface
  - install hermes web ui dashboard
  - configure hermes studio channels
  - manage hermes agent profiles
  - create hermes scheduled jobs
  - integrate telegram discord with hermes
  - deploy hermes studio docker
  - connect models to hermes dashboard
---

# Hermes Studio Dashboard

> Skill by [ara.so](https://ara.so) — Hermes Skills collection.

Hermes Studio is a comprehensive web dashboard and desktop application for [Hermes Agent](https://github.com/NousResearch/hermes-agent). It provides a unified control plane for managing AI agent conversations, platform integrations (Telegram, Discord, Slack, WhatsApp, Matrix, Feishu, WeChat, WeCom), session management, scheduled automation, model configuration, and usage analytics. Built with TypeScript and Vue3, it runs as a self-hosted local runtime, npm CLI package, or Docker container.

## Installation

### Desktop App (Recommended)

Download the native installer for Windows, macOS, or Linux from [GitHub Releases](https://github.com/EKKOLearnAI/hermes-web-ui/releases/latest).

Hermes data location:
- **Windows**: `%LOCALAPPDATA%\hermes` (fallback: `%APPDATA%\hermes`)
- **macOS/Linux**: `~/.hermes`

### NPM CLI

```bash
npm install -g hermes-web-ui

# Start the server
hermes-web-ui start

# Start with custom port
hermes-web-ui start --port 3001

# Start with custom Hermes home
HERMES_HOME=/custom/path hermes-web-ui start
```

### Docker

```bash
docker pull ekkolearnai/hermes-studio:latest

docker run -d \
  --name hermes-studio \
  -p 3000:3000 \
  -v ~/.hermes:/root/.hermes \
  -v ~/.hermes-web-ui:/root/.hermes-web-ui \
  -e AUTH_TOKEN=your-secure-token \
  ekkolearnai/hermes-studio:latest
```

Access at `http://localhost:3000`

## Core Architecture

Hermes Studio runs a Node.js backend (`packages/server`) that:
- Bridges to Hermes Agent Python runtime via HTTP and Socket.IO
- Manages its own SQLite database for Web UI sessions, users, jobs, Kanban tasks
- Reads Hermes `state.db` for historical agent sessions (read-only)
- Writes platform credentials to `~/.hermes/.env`
- Writes channel behavior config to `~/.hermes/config.yaml`

The Vue3 frontend (`packages/client`) connects via REST API and Socket.IO for real-time chat streaming.

## Authentication

### Default Credentials

First login after fresh install:
- **Username**: `admin`
- **Password**: `123456`

**Important**: Change default credentials immediately after first login via Settings → Account Management.

### Token-Based Auth

Set a custom auth token:

```bash
export AUTH_TOKEN=my-secure-token-123
hermes-web-ui start
```

Or in Docker:

```bash
docker run -d \
  -e AUTH_TOKEN=my-secure-token-123 \
  -p 3000:3000 \
  ekkolearnai/hermes-studio:latest
```

### CLI Maintenance

```bash
# Clear login IP locks
hermes-web-ui clear-login-locks

# Clear locks and restart server
hermes-web-ui clear-login-locks --restart

# Reset admin account to admin/123456
hermes-web-ui reset-default-login
```

## Profile Management

Hermes Studio supports multiple isolated profiles, each with its own:
- Configuration and credentials
- Session history and cache
- Models, providers, skills, plugins
- Scheduled jobs and usage metrics
- Uploaded files

### Creating Profiles

```typescript
// Via API: POST /api/hermes/profiles
const response = await fetch('http://localhost:3000/api/hermes/profiles', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'Authorization': `Bearer ${token}`
  },
  body: JSON.stringify({
    name: 'production-bot',
    description: 'Production customer support agent'
  })
});
```

### Switching Profiles

```typescript
// Via API: POST /api/hermes/profiles/switch
await fetch('http://localhost:3000/api/hermes/profiles/switch', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'Authorization': `Bearer ${token}`
  },
  body: JSON.stringify({
    profileName: 'production-bot'
  })
});
```

### Exporting/Importing Profiles

```bash
# Export creates ~/.hermes/profiles/{profile-name}.tar.gz
# Import via Web UI: Profiles → Import Profile → select .tar.gz file
```

## Chat Integration

### Real-Time Chat via Socket.IO

```typescript
import { io } from 'socket.io-client';

const socket = io('http://localhost:3000', {
  auth: { token: process.env.AUTH_TOKEN }
});

// Start chat run
socket.emit('chat-run', {
  sessionId: 'session-uuid',
  message: 'What is the weather in San Francisco?',
  profile: 'default',
  model: 'gpt-4'
});

// Listen for streaming chunks
socket.on('chat-chunk', (data) => {
  console.log('Chunk:', data.chunk);
  console.log('Tool calls:', data.toolCalls);
});

// Listen for completion
socket.on('chat-complete', (data) => {
  console.log('Final response:', data.response);
  console.log('Usage:', data.usage);
});

// Listen for errors
socket.on('chat-error', (error) => {
  console.error('Error:', error.message);
});
```

### REST API Chat

```typescript
// Create session
const sessionResponse = await fetch('http://localhost:3000/api/hermes/sessions', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'Authorization': `Bearer ${process.env.AUTH_TOKEN}`
  },
  body: JSON.stringify({
    name: 'Customer Support Chat',
    profile: 'default'
  })
});

const { sessionId } = await sessionResponse.json();

// Send message (non-streaming)
const chatResponse = await fetch('http://localhost:3000/api/hermes/chat', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'Authorization': `Bearer ${process.env.AUTH_TOKEN}`
  },
  body: JSON.stringify({
    sessionId,
    message: 'Help me debug this Python error',
    profile: 'default',
    model: 'claude-3-5-sonnet-20241022'
  })
});

const result = await chatResponse.json();
console.log(result.response);
```

## Platform Channel Configuration

### Telegram Bot

```typescript
// Configure via API: POST /api/hermes/channels/telegram
await fetch('http://localhost:3000/api/hermes/channels/telegram', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'Authorization': `Bearer ${process.env.AUTH_TOKEN}`
  },
  body: JSON.stringify({
    enabled: true,
    botToken: process.env.TELEGRAM_BOT_TOKEN,
    mentionControl: 'required', // 'required' | 'optional' | 'none'
    reactions: true,
    freeResponseChats: ['123456789'] // Chat IDs for always-respond
  })
});
```

Writes to `~/.hermes/.env`:
```bash
TELEGRAM_BOT_TOKEN=your-token-here
```

And `~/.hermes/config.yaml`:
```yaml
telegram:
  enabled: true
  mention_control: required
  reactions: true
  free_response_chats:
    - 123456789
```

### Discord Bot

```typescript
await fetch('http://localhost:3000/api/hermes/channels/discord', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'Authorization': `Bearer ${process.env.AUTH_TOKEN}`
  },
  body: JSON.stringify({
    enabled: true,
    botToken: process.env.DISCORD_BOT_TOKEN,
    mentionControl: 'required',
    autoThread: true,
    reactions: true,
    allowedChannels: ['1234567890123456789'],
    ignoredChannels: []
  })
});
```

### Slack Bot

```typescript
await fetch('http://localhost:3000/api/hermes/channels/slack', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'Authorization': `Bearer ${process.env.AUTH_TOKEN}`
  },
  body: JSON.stringify({
    enabled: true,
    botToken: process.env.SLACK_BOT_TOKEN,
    appToken: process.env.SLACK_APP_TOKEN,
    mentionControl: 'optional',
    handleBotMessages: false
  })
});
```

### WhatsApp

```typescript
await fetch('http://localhost:3000/api/hermes/channels/whatsapp', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'Authorization': `Bearer ${process.env.AUTH_TOKEN}`
  },
  body: JSON.stringify({
    enabled: true,
    mentionControl: 'none',
    mentionPattern: '@bot'
  })
});
```

### Matrix

```typescript
await fetch('http://localhost:3000/api/hermes/channels/matrix', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'Authorization': `Bearer ${process.env.AUTH_TOKEN}`
  },
  body: JSON.stringify({
    enabled: true,
    accessToken: process.env.MATRIX_ACCESS_TOKEN,
    homeserver: 'https://matrix.org',
    autoThread: true,
    dmMentionThreads: true
  })
});
```

## Model Management

### Add Custom Provider

```typescript
// POST /api/hermes/providers
await fetch('http://localhost:3000/api/hermes/providers', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'Authorization': `Bearer ${process.env.AUTH_TOKEN}`
  },
  body: JSON.stringify({
    name: 'local-ollama',
    baseUrl: 'http://localhost:11434/v1',
    apiKey: 'ollama', // Ollama doesn't require real key
    type: 'custom'
  })
});
```

### Fetch Available Models

```typescript
// GET /api/hermes/providers/{providerId}/models
const response = await fetch(
  `http://localhost:3000/api/hermes/providers/${providerId}/models`,
  {
    headers: { 'Authorization': `Bearer ${process.env.AUTH_TOKEN}` }
  }
);

const models = await response.json();
// [{ id: 'llama3.2', name: 'Llama 3.2', ... }, ...]
```

### Set Default Model

```typescript
// PATCH /api/hermes/settings
await fetch('http://localhost:3000/api/hermes/settings', {
  method: 'PATCH',
  headers: {
    'Content-Type': 'application/json',
    'Authorization': `Bearer ${process.env.AUTH_TOKEN}`
  },
  body: JSON.stringify({
    defaultModel: 'gpt-4o',
    defaultProvider: 'openai'
  })
});
```

## Scheduled Jobs (Cron)

### Create Cron Job

```typescript
// POST /api/hermes/jobs
await fetch('http://localhost:3000/api/hermes/jobs', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'Authorization': `Bearer ${process.env.AUTH_TOKEN}`
  },
  body: JSON.stringify({
    name: 'Daily Report',
    cronExpression: '0 9 * * *', // 9 AM daily
    profile: 'default',
    task: 'Generate and email daily analytics report',
    enabled: true
  })
});
```

### Cron Expression Presets

- `0 * * * *` - Every hour
- `0 9 * * *` - Daily at 9 AM
- `0 9 * * 1` - Every Monday at 9 AM
- `*/15 * * * *` - Every 15 minutes
- `0 0 1 * *` - First day of month at midnight

### Trigger Job Manually

```typescript
// POST /api/hermes/jobs/{jobId}/trigger
await fetch(`http://localhost:3000/api/hermes/jobs/${jobId}/trigger`, {
  method: 'POST',
  headers: { 'Authorization': `Bearer ${process.env.AUTH_TOKEN}` }
});
```

## File Management

### Upload File to Profile

```typescript
const formData = new FormData();
formData.append('file', fileBlob, 'document.pdf');
formData.append('profile', 'default');

const response = await fetch('http://localhost:3000/api/hermes/files/upload', {
  method: 'POST',
  headers: { 'Authorization': `Bearer ${process.env.AUTH_TOKEN}` },
  body: formData
});

const { path, url } = await response.json();
```

Files are stored under `~/.hermes/profiles/{profile}/uploads/`

### Download Agent-Generated File

```typescript
// GET /api/hermes/files/download?path={filePath}&backend={local|docker|ssh|singularity}
const downloadUrl = `http://localhost:3000/api/hermes/files/download?path=${encodeURIComponent(filePath)}&backend=local`;

const response = await fetch(downloadUrl, {
  headers: { 'Authorization': `Bearer ${process.env.AUTH_TOKEN}` }
});

const blob = await response.blob();
```

### Browse Files (File Browser API)

```typescript
// GET /api/hermes/files/browse?path={dirPath}&backend=local
const response = await fetch(
  `http://localhost:3000/api/hermes/files/browse?path=/home/user&backend=local`,
  { headers: { 'Authorization': `Bearer ${process.env.AUTH_TOKEN}` } }
);

const { files, directories } = await response.json();
```

## Usage Analytics

### Get Usage Stats

```typescript
// GET /api/hermes/usage?profile={profile}&days=30
const response = await fetch(
  'http://localhost:3000/api/hermes/usage?profile=default&days=30',
  { headers: { 'Authorization': `Bearer ${process.env.AUTH_TOKEN}` } }
);

const stats = await response.json();
/*
{
  totalTokens: { input: 125000, output: 87000 },
  sessionCount: 342,
  dailyAverage: 11.4,
  estimatedCost: 12.45,
  cacheHitRate: 0.23,
  modelDistribution: [
    { model: 'gpt-4o', percentage: 65 },
    { model: 'claude-3-5-sonnet-20241022', percentage: 35 }
  ],
  dailyTrend: [
    { date: '2024-01-01', tokens: 4500, sessions: 12 },
    ...
  ]
}
*/
```

## Group Chat (Multi-Agent Rooms)

### Create Room

```typescript
// POST /api/hermes/group-chat/rooms
const response = await fetch('http://localhost:3000/api/hermes/group-chat/rooms', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'Authorization': `Bearer ${process.env.AUTH_TOKEN}`
  },
  body: JSON.stringify({
    name: 'Engineering Team',
    description: 'Multi-agent code review room',
    agents: [
      { name: 'code-reviewer', profile: 'reviewer-profile' },
      { name: 'security-bot', profile: 'security-profile' }
    ],
    contextCompressionThreshold: 8000 // tokens
  })
});

const { roomId, inviteCode } = await response.json();
```

### Send Message in Room

```typescript
// Connect via Socket.IO
socket.emit('group-chat-message', {
  roomId: 'room-uuid',
  message: '@code-reviewer Please review this PR',
  sender: 'user'
});

// Agent will respond when @mentioned
socket.on('group-chat-reply', (data) => {
  console.log(`${data.agent}: ${data.message}`);
});
```

## Voice & TTS/STT

### Configure TTS Provider

```typescript
// POST /api/hermes/tts/settings
await fetch('http://localhost:3000/api/hermes/tts/settings', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'Authorization': `Bearer ${process.env.AUTH_TOKEN}`
  },
  body: JSON.stringify({
    provider: 'openai', // 'browser' | 'edge' | 'openai' | 'custom' | 'mimo'
    apiKey: process.env.OPENAI_API_KEY,
    voice: 'alloy', // For OpenAI: alloy, echo, fable, onyx, nova, shimmer
    model: 'tts-1' // tts-1 or tts-1-hd
  })
});
```

### Synthesize Speech

```typescript
// POST /api/hermes/tts/synthesize
const response = await fetch('http://localhost:3000/api/hermes/tts/synthesize', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'Authorization': `Bearer ${process.env.AUTH_TOKEN}`
  },
  body: JSON.stringify({
    text: 'Hello, this is a test message.',
    provider: 'openai',
    voice: 'nova'
  })
});

const audioBlob = await response.blob();
const audioUrl = URL.createObjectURL(audioBlob);
```

### Configure STT (Speech-to-Text)

```typescript
// POST /api/hermes/stt/settings
await fetch('http://localhost:3000/api/hermes/stt/settings', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'Authorization': `Bearer ${process.env.AUTH_TOKEN}`
  },
  body: JSON.stringify({
    provider: 'openai', // 'browser' | 'openai'
    apiKey: process.env.OPENAI_API_KEY,
    model: 'whisper-1'
  })
});
```

## Web Terminal

### Create Terminal Session

```typescript
// Socket.IO: terminal-create
socket.emit('terminal-create', { 
  cols: 80, 
  rows: 24 
});

socket.on('terminal-created', (data) => {
  const terminalId = data.id;
  
  // Send input
  socket.emit('terminal-input', {
    id: terminalId,
    data: 'ls -la\n'
  });
  
  // Receive output
  socket.on('terminal-output', (output) => {
    console.log(output.data);
  });
});
```

### Resize Terminal

```typescript
socket.emit('terminal-resize', {
  id: terminalId,
  cols: 120,
  rows: 30
});
```

## Kanban Task Management

### Create Task

```typescript
// POST /api/hermes/kanban/tasks
await fetch('http://localhost:3000/api/hermes/kanban/tasks', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'Authorization': `Bearer ${process.env.AUTH_TOKEN}`
  },
  body: JSON.stringify({
    title: 'Implement OAuth flow',
    description: 'Add OAuth2 authentication for GitHub',
    status: 'todo', // 'todo' | 'in-progress' | 'review' | 'done'
    priority: 'high', // 'low' | 'medium' | 'high'
    assignedProfile: 'default',
    tags: ['auth', 'backend']
  })
});
```

### Move Task Status

```typescript
// PATCH /api/hermes/kanban/tasks/{taskId}
await fetch(`http://localhost:3000/api/hermes/kanban/tasks/${taskId}`, {
  method: 'PATCH',
  headers: {
    'Content-Type': 'application/json',
    'Authorization': `Bearer ${process.env.AUTH_TOKEN}`
  },
  body: JSON.stringify({
    status: 'in-progress'
  })
});
```

## Environment Variables

### Core Configuration

```bash
# Authentication
AUTH_TOKEN=your-secure-token-here

# Server
PORT=3000
HOST=0.0.0.0

# Hermes paths
HERMES_HOME=~/.hermes
HERMES_WEB_UI_HOME=~/.hermes-web-ui

# Database
DATABASE_PATH=${HERMES_WEB_UI_HOME}/hermes-studio.db

# Backend type
HERMES_BACKEND=local  # local | docker | ssh | singularity

# Logging
LOG_LEVEL=info  # debug | info | warn | error
```

### Platform Credentials

```bash
# Telegram
TELEGRAM_BOT_TOKEN=your-telegram-token

# Discord
DISCORD_BOT_TOKEN=your-discord-token

# Slack
SLACK_BOT_TOKEN=xoxb-your-slack-bot-token
SLACK_APP_TOKEN=xapp-your-slack-app-token

# Matrix
MATRIX_ACCESS_TOKEN=your-matrix-token
MATRIX_HOMESERVER=https://matrix.org

# Feishu/Lark
FEISHU_APP_ID=your-app-id
FEISHU_APP_SECRET=your-app-secret

# WeCom
WECOM_BOT_ID=your-bot-id
WECOM_BOT_SECRET=your-bot-secret
```

### Model Providers

```bash
# OpenAI
OPENAI_API_KEY=sk-your-key

# Anthropic
ANTHROPIC_API_KEY=sk-ant-your-key

# Custom providers
CUSTOM_PROVIDER_URL=https://your-api.example.com/v1
CUSTOM_PROVIDER_KEY=your-api-key
```

## Docker Compose Example

```yaml
version: '3.8'

services:
  hermes-studio:
    image: ekkolearnai/hermes-studio:latest
    container_name: hermes-studio
    ports:
      - "3000:3000"
    volumes:
      - ./hermes-data:/root/.hermes
      - ./hermes-ui-data:/root/.hermes-web-ui
    environment:
      - AUTH_TOKEN=${AUTH_TOKEN}
      - TELEGRAM_BOT_TOKEN=${TELEGRAM_BOT_TOKEN}
      - DISCORD_BOT_TOKEN=${DISCORD_BOT_TOKEN}
      - OPENAI_API_KEY=${OPENAI_API_KEY}
      - ANTHROPIC_API_KEY=${ANTHROPIC_API_KEY}
      - LOG_LEVEL=info
    restart: unless-stopped
```

Run with:
```bash
docker-compose up -d
```

## Common Patterns

### Multi-Profile Bot Setup

```typescript
// 1. Create profiles for different contexts
const profiles = ['customer-support', 'internal-tools', 'dev-assistant'];

for (const profileName of profiles) {
  await fetch('http://localhost:3000/api/hermes/profiles', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${process.env.AUTH_TOKEN}`
    },
    body: JSON.stringify({
      name: profileName,
      description: `Profile for ${profileName}`
    })
  });
}

// 2. Configure different models for each profile
const modelConfigs = {
  'customer-support': 'gpt-4o',
  'internal-tools': 'claude-3-5-sonnet-20241022',
  'dev-assistant': 'gpt-4o-mini'
};

for (const [profile, model] of Object.entries(modelConfigs)) {
  // Switch to profile
  await fetch('http://localhost:3000/api/hermes/profiles/switch', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${process.env.AUTH_TOKEN}`
    },
    body: JSON.stringify({ profileName: profile })
  });
  
  // Set default model
  await fetch('http://localhost:3000/api/hermes/settings', {
    method: 'PATCH',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${process.env.AUTH_TOKEN}`
    },
    body: JSON.stringify({ defaultModel: model })
  });
}

// 3. Bind profiles to platform channels
await fetch('http://localhost:3000/api/hermes/channels/telegram', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'Authorization': `Bearer ${process.env.AUTH_TOKEN}`
  },
  body: JSON.stringify({
    enabled: true,
    botToken: process.env.TELEGRAM_BOT_TOKEN,
    profile: 'customer-support'
  })
});
```

### Scheduled Backup Job

```typescript
// Daily profile export at midnight
await fetch('http://localhost:3000/api/hermes/jobs', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'Authorization': `Bearer ${process.env.AUTH_TOKEN}`
  },
  body: JSON.stringify({
    name: 'Daily Backup',
    cronExpression: '0 0 * * *',
    profile: 'default',
    task: 'export-profile',
    enabled: true,
    config: {
      destination: '/backups',
      retention: 7 // days
    }
  })
});
```

### Context-Aware Group Chat

```typescript
// Create room with context compression
const roomResponse = await fetch('http://localhost:3000/api/hermes/group-chat/rooms', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'Authorization': `Bearer ${process.env.AUTH_TOKEN}`
  },
  body: JSON.stringify({
    name: 'Code Review',
    agents: [
      { name: 'reviewer', profile: 'code-review' },
      { name: 'security', profile: 'security-scan' },
      { name: 'docs', profile: 'documentation' }
    ],
    contextCompressionThreshold: 8000,
    systemPrompt: 'You are part of a code review team. Focus on your specialty.'
  })
});

const { roomId } = await roomResponse.json();

// Send code for review
socket.emit('group-chat-message', {
  roomId,
  message: '@reviewer @security Check this authentication function:\n```python\n...\n```',
  sender: 'developer'
});
```

## Troubleshooting

### Server Won't Start

**Issue**: `Error: EADDRINUSE: address already in use`

```bash
# Find process using port 3000
lsof -i :3000

# Kill process
kill -9 <PID>

# Or start on different port
hermes-web-ui start --port 3001
```

### Authentication Failures

**Issue**: Login locked after multiple attempts

```bash
# Clear login locks
hermes-web-ui clear-login-locks --restart

# Reset admin credentials
hermes-web-ui reset-default-login
```

### Profile Not Found

**Issue**: `Profile 'xyz' does not exist`

```bash
# List available profiles
ls ~/.hermes/profiles/

# Ensure profile exists in Hermes home
hermes profile list
```

### Platform Channel Not Responding

**Issue**: Bot doesn't respond to Telegram/Discord messages

1. **Check credentials** in `~/.hermes/.env`:
   ```bash
   cat ~/.hermes/.env | grep TELEGRAM
   ```

2. **Verify channel config** in `~/.hermes/config.yaml`:
   ```bash
   cat ~/.hermes/config.yaml
   ```

3. **Check mention control** - If `mention_control: required`, you must @mention the bot

4. **Review logs**:
   ```bash
   # Via CLI
   hermes-web-ui logs --filter telegram
   
   # Or in Web UI: Settings → Logs → Filter by "telegram"
   ```

### Models Not Appearing

**Issue**: Models don't show up in chat selector

1. **Fetch models** for provider:
   ```typescript
   // GET /api/hermes/providers/{providerId}/models
   const response = await fetch(
     `http://localhost:3000/api/hermes/providers/${providerId}/models`,
     { headers: { 'Authorization': `Bearer ${process.env.AUTH_TOKEN}` } }
   );
   ```

2. **Verify provider credentials**:
   ```bash
   cat ~/.hermes/auth.json
   ```

3. **Check provider base URL** - Ensure `/v1` suffix for OpenAI-compatible APIs

### Socket.IO Connection Errors

**Issue**: `WebSocket connection failed`

```typescript
// Enable debug logging
const socket = io('http://localhost:3000', {
  auth: { token: process.env.AUTH_TOKEN },
  transports: ['websocket', 'polling'], // Fallback to polling
  reconnection: true,
  reconnectionAttempts: 5,
  reconnectionDelay: 1000
});

socket.on('connect_error', (error) => {
  console.error('Connection error:', error.message);
});
```

### File Upload Fails

**Issue**: `413 Payload Too Large`

Increase file size limit in server config:

```typescript
// In packages/server/src/index.ts or environment
export MAX_FILE_SIZE=52428800  // 50 MB in bytes
```

For voice clone reference audio (MiMo TTS), max size is 10 MB per `.mp3` or `.wav` file.

### Docker Container Permission Issues

**Issue**: Permission denied when accessing `/root/.hermes`

```bash
# Run with user permissions
docker run -d \
  --user $(id -u):$(id -g) \
  -v ~/.hermes:/home/user/.hermes \
  -v ~/.hermes-web-ui:/home/user/.hermes-web-ui \
  -e HERMES_HOME=/home/user/.hermes \
  -e HERMES_WEB_UI_HOME=/home/user/.hermes-web-ui \
  ekkolearnai/hermes-studio:latest
```

### Cron Jobs Not Running

**Issue**: Scheduled job doesn't execute at expected time

1
