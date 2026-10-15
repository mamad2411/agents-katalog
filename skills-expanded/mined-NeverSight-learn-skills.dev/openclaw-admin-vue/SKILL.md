---
name: openclaw-admin-vue
description: AI agent management platform built with Vue 3 for OpenClaw Gateway and Hermes Agent
triggers:
  - "set up openclaw admin dashboard"
  - "how do i configure the claw admin interface"
  - "install openclaw admin frontend"
  - "manage ai agents with openclaw"
  - "connect hermes agent to openclaw admin"
  - "deploy openclaw admin ui"
  - "configure openclaw gateway dashboard"
  - "troubleshoot openclaw admin connection"
---

# OpenClaw Admin Vue Skill

> Skill by [ara.so](https://ara.so) — Hermes Skills collection.

OpenClaw Admin is a modern AI agent management platform built with Vue 3 that provides a comprehensive web interface for both OpenClaw Gateway and Hermes Agent. It enables visual management of AI agents, sessions, models, channels, skills, and includes a full-featured Web CLI terminal with session persistence.

## What OpenClaw Admin Does

- **Dual Gateway Support**: Manages both OpenClaw Gateway and Hermes Agent from a single interface
- **Web CLI Terminal**: Real terminal emulation using xterm.js with session persistence and reconnection
- **Multi-Agent Orchestration**: Create and coordinate multiple AI agents for complex workflows
- **Real-time Monitoring**: System resources, session states, token usage, and event streams
- **Channel Management**: Configure QQ, Feishu, DingTalk, WeChat integrations
- **Skill Management**: Install, update, and configure agent skills/plugins
- **Memory Management**: Edit agent identity, personality (SOUL.md), and instructions

## Installation

### Prerequisites

```bash
# Required
node >= 18.0.0
npm >= 9.0.0

# For Hermes CLI terminal feature
python >= 3.10

# Must be deployed on the same node as the gateway
# .env only supports 127.0.0.1 or localhost
```

### Setup Steps

```bash
# Clone repository
git clone https://github.com/itq5/OpenClaw-Admin.git
cd OpenClaw-Admin

# Install dependencies
npm install

# Initialize environment configuration
cp .env.example .env

# Edit .env file
vim .env
```

### Environment Configuration

```bash
# .env
# Server Port
VITE_PORT=3001

# OpenClaw Gateway Configuration
VITE_OPENCLAW_WS_URL=ws://localhost:8081
VITE_OPENCLAW_HTTP_URL=http://localhost:8081

# Hermes Agent Configuration
VITE_HERMES_API_URL=http://localhost:8642
VITE_HERMES_WEB_URL=http://localhost:9119
VITE_HERMES_API_KEY=

# CLI Terminal Configuration (for Hermes CLI)
VITE_CLI_SESSION_DB=./cli-sessions.db
```

### Development Mode

```bash
# Start frontend only
npm run dev

# Start backend only (for CLI terminal)
npm run dev:server

# Start both frontend and backend
npm run dev:all

# Access at http://localhost:3001
```

### Production Build

```bash
# Build for production
npm run build

# Start production server
npm run start

# Access at configured port (default 3001)
```

## Hermes Agent Integration

### Install Hermes Agent

```bash
# Official installation script
curl -fsSL https://raw.githubusercontent.com/NousResearch/hermes-agent/main/scripts/install.sh | bash

# Run configuration wizard
hermes setup
```

### Configure Hermes Agent

```bash
# Configure AI model provider
hermes setup model

# Or edit ~/.hermes/.env directly
# Example for OpenRouter:
OPENROUTER_API_KEY=${OPENROUTER_API_KEY}

# Example for Anthropic:
ANTHROPIC_API_KEY=${ANTHROPIC_API_KEY}

# Enable API Server
vim ~/.hermes/.env
# Add:
API_SERVER_ENABLED=true
GATEWAY_ALLOW_ALL_USERS=true
API_SERVER_KEY=${API_SERVER_KEY}
```

### Start Hermes Gateway

```bash
# Install gateway
hermes gateway install

# Start gateway (background)
hermes gateway start

# Start Web UI dashboard
hermes dashboard

# Verify services
curl http://localhost:8642/v1/health
curl http://localhost:9119/api/status
```

## Key Features and API Usage

### OpenClaw Gateway Module

#### Session Management API

```typescript
// Create new session
import { sessionApi } from '@/api/openclaw/session'

const createSession = async () => {
  const response = await sessionApi.createSession({
    session_id: 'my-session',
    agent_id: 'default',
    metadata: {
      user_id: 'user123',
      channel: 'web'
    }
  })
  return response.data
}

// List sessions with filters
const listSessions = async () => {
  const sessions = await sessionApi.listSessions({
    agent_id: 'default',
    active: true,
    limit: 20
  })
  return sessions.data
}

// Reset session
await sessionApi.resetSession('session-id')

// Delete session
await sessionApi.deleteSession('session-id')
```

#### Model Management API

```typescript
import { modelApi } from '@/api/openclaw/model'

// Add model provider
const addModel = async () => {
  await modelApi.addModel({
    provider: 'openrouter',
    api_key: process.env.OPENROUTER_API_KEY,
    base_url: 'https://openrouter.ai/api/v1',
    models: ['anthropic/claude-3.5-sonnet']
  })
}

// Set default model
await modelApi.setDefaultModel('anthropic/claude-3.5-sonnet')

// Probe model availability
const probeResult = await modelApi.probeModel({
  provider: 'openrouter',
  model: 'anthropic/claude-3.5-sonnet',
  api_key: process.env.OPENROUTER_API_KEY
})
```

#### Skill Management API

```typescript
import { skillApi } from '@/api/openclaw/skill'

// List available skills
const skills = await skillApi.listSkills()

// Install skill
await skillApi.installSkill({
  name: 'web-search',
  version: 'latest'
})

// Update skill
await skillApi.updateSkill('web-search')

// Toggle skill visibility in chat
await skillApi.toggleSkillVisibility('web-search', true)
```

#### Cron Task API

```typescript
import { cronApi } from '@/api/openclaw/cron'

// Create scheduled task
const createTask = async () => {
  await cronApi.createTask({
    name: 'morning-report',
    schedule_type: 'cron',
    cron_expression: '0 9 * * *', // Every day at 9 AM
    prompt: 'Generate daily summary report',
    agent_id: 'default',
    enabled: true
  })
}

// List tasks
const tasks = await cronApi.listTasks()

// Trigger task manually
await cronApi.triggerTask('task-id')
```

### Hermes Agent Module

#### Chat API Integration

```typescript
import { hermesApi } from '@/api/hermes'

// Send chat message (SSE streaming)
const sendMessage = async (message: string) => {
  const eventSource = hermesApi.chat.sendMessageStream({
    message,
    session_id: 'session-123',
    model: 'anthropic/claude-sonnet-4',
    stream: true
  })

  eventSource.onmessage = (event) => {
    const data = JSON.parse(event.data)
    if (data.type === 'content') {
      console.log('Chunk:', data.content)
    } else if (data.type === 'tool_call') {
      console.log('Tool invoked:', data.tool_name)
    }
  }

  return eventSource
}

// Execute slash command
await hermesApi.chat.executeCommand('/skills enable web-search')
```

#### Session Management

```typescript
import { hermesApi } from '@/api/hermes/session'

// List sessions
const sessions = await hermesApi.listSessions({
  page: 1,
  page_size: 20,
  search: 'keyword'
})

// Get session messages
const messages = await hermesApi.getSessionMessages('session-id')

// Delete session
await hermesApi.deleteSession('session-id')
```

#### Configuration Management

```typescript
import { hermesApi } from '@/api/hermes/config'

// Get configuration
const config = await hermesApi.getConfig()

// Update configuration
await hermesApi.updateConfig({
  model: 'anthropic/claude-sonnet-4',
  provider: 'anthropic',
  max_turns: 10,
  temperature: 0.7
})

// Get environment variables
const envVars = await hermesApi.getEnvVars()

// Set environment variable
await hermesApi.setEnvVar('MY_API_KEY', process.env.MY_API_KEY)
```

### Web CLI Terminal

#### Using the CLI Terminal UI

The CLI terminal provides a real terminal experience with full Hermes CLI support:

```typescript
// Component usage
import CliTerminal from '@/components/hermes/cli/CliTerminal.vue'

// In your Vue component
<template>
  <CliTerminal
    :session-id="currentSessionId"
    :auto-connect="true"
    @session-created="handleSessionCreated"
  />
</template>
```

#### CLI Session API

```typescript
import axios from 'axios'

// Create CLI session with startup parameters
const createCliSession = async () => {
  const response = await axios.post('/api/cli/sessions', {
    name: 'My CLI Session',
    startup_params: {
      model: 'anthropic/claude-sonnet-4',
      provider: 'anthropic',
      skills: ['web-search', 'code-execution'],
      yolo: false,
      verbose: true
    }
  })
  return response.data.session_id
}

// List CLI sessions
const sessions = await axios.get('/api/cli/sessions')

// Reconnect to existing session
const reconnect = async (sessionId: string) => {
  const response = await axios.post(`/api/cli/sessions/${sessionId}/connect`)
  return response.data
}

// Send input to CLI
await axios.post(`/api/cli/sessions/${sessionId}/input`, {
  data: 'what skills are enabled?\n'
})

// Resize terminal
await axios.post(`/api/cli/sessions/${sessionId}/resize`, {
  cols: 120,
  rows: 30
})

// Destroy session
await axios.delete(`/api/cli/sessions/${sessionId}`)
```

#### CLI Commands Available in Terminal

```bash
# Hermes CLI-specific commands (work in Web Terminal)
/skills                  # List all skills
/skills enable web-search # Enable a skill
/tools                   # List available tools
/cron list              # List scheduled tasks
/config                 # Show configuration
/browser                # Open browser tool
/help                   # Show all commands

# Regular slash commands
/new                    # Start new session
/model claude-sonnet-4  # Switch model
/status                 # Show system status
```

### WebSocket Event Handling

```typescript
import { useOpenClawStore } from '@/stores/openclaw'

const store = useOpenClawStore()

// Connect to OpenClaw Gateway
await store.connect()

// Listen to events
store.on('session.message', (data) => {
  console.log('New message:', data)
})

store.on('system.stats', (stats) => {
  console.log('System stats:', stats)
})

// Send command
store.sendCommand({
  type: 'chat.send',
  data: {
    session_id: 'my-session',
    message: 'Hello AI'
  }
})
```

## Configuration Patterns

### Connecting to Multiple Gateways

```typescript
// stores/settings.ts
export const useSettingsStore = defineStore('settings', {
  state: () => ({
    connections: {
      openclaw: {
        wsUrl: 'ws://localhost:8081',
        httpUrl: 'http://localhost:8081',
        enabled: true
      },
      hermes: {
        apiUrl: 'http://localhost:8642',
        webUrl: 'http://localhost:9119',
        apiKey: '',
        enabled: true
      }
    }
  }),
  actions: {
    async testConnection(type: 'openclaw' | 'hermes') {
      if (type === 'openclaw') {
        const ws = new WebSocket(this.connections.openclaw.wsUrl)
        return new Promise((resolve, reject) => {
          ws.onopen = () => { ws.close(); resolve(true) }
          ws.onerror = reject
        })
      } else {
        const response = await fetch(`${this.connections.hermes.webUrl}/api/status`)
        return response.ok
      }
    }
  }
})
```

### Slash Command Implementation

```typescript
// components/chat/CommandProcessor.ts
export class CommandProcessor {
  private commands = {
    '/new': () => this.newSession(),
    '/model': (args: string) => this.switchModel(args),
    '/skills': () => this.listSkills(),
    '/status': () => this.showStatus(),
    '/help': () => this.showHelp()
  }

  async process(input: string) {
    const [command, ...args] = input.split(' ')
    const handler = this.commands[command]
    
    if (handler) {
      return await handler(args.join(' '))
    }
    return null
  }

  private async switchModel(modelName: string) {
    await modelApi.setDefaultModel(modelName)
    return `Switched to model: ${modelName}`
  }
}
```

### Real-time Dashboard Updates

```typescript
// components/Dashboard.vue
<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue'
import { useDashboardStore } from '@/stores/dashboard'

const store = useDashboardStore()
const stats = ref({})
let updateInterval: number

onMounted(() => {
  // Initial load
  store.loadStats()
  
  // Poll every 5 seconds
  updateInterval = setInterval(() => {
    store.loadStats()
  }, 5000)
  
  // Listen to WebSocket events
  store.on('stats.update', (data) => {
    stats.value = data
  })
})

onUnmounted(() => {
  clearInterval(updateInterval)
})
</script>
```

## Common Patterns

### Agent Office Workflow

```typescript
import { agentOfficeApi } from '@/api/openclaw/agent-office'

// Create multi-agent scenario
const createScenario = async () => {
  const scenario = await agentOfficeApi.createScenario({
    name: 'Code Review Team',
    description: 'Collaborative code review workflow',
    agents: [
      { id: 'reviewer-1', role: 'senior-reviewer' },
      { id: 'reviewer-2', role: 'security-expert' },
      { id: 'coordinator', role: 'team-lead' }
    ]
  })

  // Assign task
  await agentOfficeApi.delegateTask(scenario.id, {
    agent_id: 'coordinator',
    task: 'Review pull request #123',
    context: { pr_url: 'https://github.com/...' }
  })

  return scenario
}
```

### Custom Skill Installation

```typescript
// Install skill from custom source
const installCustomSkill = async () => {
  await skillApi.installSkill({
    name: 'my-custom-skill',
    source: 'github',
    repository: 'username/skill-repo',
    branch: 'main',
    path: 'skills/my-skill'
  })
}
```

### Memory/Identity Management

```typescript
import { memoryApi } from '@/api/openclaw/memory'

// Update agent SOUL (personality)
const updateSoul = async () => {
  await memoryApi.updateDocument('SOUL', `
# Agent Personality

You are a helpful coding assistant specialized in Vue.js and TypeScript.

## Guidelines
- Always provide type-safe examples
- Explain Vue 3 Composition API patterns
- Reference official documentation
  `)
}

// Update agent instructions
await memoryApi.updateDocument('AGENTS', `
# Agent Instructions

## Available Tools
- code_executor: Run code snippets
- web_search: Search the web
- file_manager: Manage files
  `)
```

## Troubleshooting

### Connection Issues

```typescript
// Test OpenClaw Gateway connection
const testOpenClaw = async () => {
  try {
    const ws = new WebSocket('ws://localhost:8081')
    ws.onopen = () => console.log('✓ OpenClaw connected')
    ws.onerror = (err) => console.error('✗ OpenClaw error:', err)
  } catch (error) {
    console.error('Cannot connect to OpenClaw:', error)
    // Check: Is gateway running? Correct port? Firewall?
  }
}

// Test Hermes API connection
const testHermes = async () => {
  try {
    const health = await fetch('http://localhost:8642/v1/health')
    const webUI = await fetch('http://localhost:9119/api/status')
    console.log('API Server:', health.ok ? '✓' : '✗')
    console.log('Web UI:', webUI.ok ? '✓' : '✗')
  } catch (error) {
    console.error('Cannot connect to Hermes:', error)
    // Check: hermes gateway start, hermes dashboard running
  }
}
```

### CLI Terminal Not Starting

```bash
# Check Python availability
which python3
python3 --version  # Must be >= 3.10

# Check Hermes CLI installation
hermes --version

# Check backend server logs
npm run dev:server
# Look for "CLI session manager initialized"

# Verify database
ls -la cli-sessions.db

# Check process limits
ulimit -n  # Should be >= 1024
```

### Session Persistence Issues

```typescript
// Verify CLI session database
import Database from 'better-sqlite3'

const db = new Database('./cli-sessions.db')
const sessions = db.prepare('SELECT * FROM cli_sessions').all()
console.log('Active sessions:', sessions)

// Clear stuck sessions
db.prepare('DELETE FROM cli_sessions WHERE last_activity < ?')
  .run(Date.now() - 24 * 60 * 60 * 1000) // Older than 24h
```

### WebSocket Reconnection

```typescript
// Implement exponential backoff
class ResilientWebSocket {
  private reconnectDelay = 1000
  private maxDelay = 30000

  connect() {
    this.ws = new WebSocket(this.url)
    
    this.ws.onerror = () => {
      setTimeout(() => {
        this.reconnectDelay = Math.min(this.reconnectDelay * 2, this.maxDelay)
        this.connect()
      }, this.reconnectDelay)
    }

    this.ws.onopen = () => {
      this.reconnectDelay = 1000 // Reset on success
    }
  }
}
```

### CORS Issues

```javascript
// server/index.js - Backend server configuration
app.use(cors({
  origin: process.env.VITE_FRONTEND_URL || 'http://localhost:3001',
  credentials: true
}))
```

### Build Errors

```bash
# Clear cache and reinstall
rm -rf node_modules package-lock.json
npm install

# Check Node version
node --version  # Must be >= 18

# Build with verbose output
npm run build -- --mode production --debug

# Check TypeScript errors
npx tsc --noEmit
```

### Model API Key Issues

```bash
# Verify Hermes configuration
hermes config show

# Test model directly
hermes chat --model anthropic/claude-sonnet-4 "Hello"

# Check API key in environment
echo $ANTHROPIC_API_KEY

# Update .env file (must be in ~/.hermes/.env)
vim ~/.hermes/.env
```

## Production Deployment

```bash
# Build optimized bundle
npm run build

# Use PM2 for process management
npm install -g pm2

# Start with PM2
pm2 start npm --name "openclaw-admin" -- start

# Monitor
pm2 logs openclaw-admin
pm2 monit

# Auto-restart on system reboot
pm2 startup
pm2 save
```

### Nginx Reverse Proxy

```nginx
server {
    listen 80;
    server_name admin.yourdomain.com;

    location / {
        proxy_pass http://127.0.0.1:3001;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
    }

    # WebSocket support
    location /ws {
        proxy_pass http://127.0.0.1:8081;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "Upgrade";
    }
}
```

## Additional Resources

- Official Documentation: https://claw.227727.xyz
- GitHub Repository: https://github.com/itq5/OpenClaw-Admin
- Hermes Agent Docs: https://docs.nousresearch.com/hermes-agent
- OpenClaw Gateway: Contact project maintainers for documentation
