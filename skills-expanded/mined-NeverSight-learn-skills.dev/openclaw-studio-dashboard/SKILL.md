---
name: openclaw-studio-dashboard
description: Expert in OpenClaw Studio - web dashboard for managing OpenClaw Gateway, agents, chat, approvals, and jobs
triggers:
  - set up openclaw studio dashboard
  - connect studio to openclaw gateway
  - create agent in openclaw studio
  - configure openclaw studio upstream
  - manage openclaw agents with studio
  - deploy openclaw studio to production
  - troubleshoot openclaw studio connection
  - run openclaw studio locally
---

# OpenClaw Studio Dashboard

> Skill by [ara.so](https://ara.so) — Hermes Skills collection.

OpenClaw Studio is a clean web dashboard for OpenClaw Gateway that provides a unified interface to connect gateways, manage agents, chat, handle approvals, and configure jobs. Built with TypeScript/Next.js, it runs a server-owned control plane architecture with SSE streaming for real-time runtime events.

## What OpenClaw Studio Does

- **Gateway Connection**: Connect to local or remote OpenClaw Gateway instances via WebSocket
- **Agent Management**: Create, configure, and monitor AI agents with tool policies and sandbox settings
- **Chat Interface**: Stream conversations with PI agents including tool calls and thinking traces
- **Approval Workflows**: Manage exec approvals and runtime permissions
- **Job Configuration**: Set up and monitor cron jobs
- **Runtime Streaming**: Real-time event streaming over SSE with replay/history

## Installation & Startup

### Quick Start (Recommended)

```bash
# Run latest version with npx
npx -y openclaw-studio@latest

# Opens on http://localhost:3000
# Default gateway URL: ws://localhost:18789
```

### From Source

```bash
git clone https://github.com/grp06/openclaw-studio.git
cd openclaw-studio
npm install
npm run dev
```

### Setup Helper

```bash
# Configure gateway URL/token without opening UI
npm run studio:setup
```

## Connection Architecture

OpenClaw Studio uses a two-path architecture:

1. **Browser → Studio**: HTTP + SSE (`/api/runtime/*`, `/api/intents/*`)
2. **Studio → Gateway**: Server-owned WebSocket to upstream OpenClaw

**Critical concept**: `ws://localhost:18789` means "gateway on the Studio host", not "gateway on your browser's machine".

## Configuration Patterns

### Deployment Scenarios

#### A. Both Local (Same Computer)

```bash
# Start Studio
npx -y openclaw-studio@latest
cd openclaw-studio
npm run dev

# Open http://localhost:3000
# In Studio UI:
# - Upstream URL: ws://localhost:18789
# - Upstream Token: <your-gateway-token>
```

Get gateway token:
```bash
openclaw config get gateway.auth.token
```

#### B. Gateway in Cloud, Studio Local

**Option 1: Tailscale Serve (Recommended)**

On gateway host:
```bash
tailscale serve --yes --bg --https 443 http://127.0.0.1:18789
```

In Studio (local laptop):
- Upstream URL: `wss://<gateway-host>.ts.net`
- Upstream Token: `<gateway-token>`

**Option 2: SSH Tunnel**

From laptop:
```bash
ssh -L 18789:127.0.0.1:18789 user@<gateway-host>
```

In Studio:
- Upstream URL: `ws://localhost:18789`
- Upstream Token: `<gateway-token>`

#### C. Both in Cloud (Always-On)

On Studio VPS:
```bash
# Start Studio
npx -y openclaw-studio@latest
cd openclaw-studio
npm install
npm run dev

# If OpenClaw is on same VPS:
# - Upstream URL: ws://localhost:18789
# - Upstream Token: <gateway-token>

# Expose Studio over Tailscale
tailscale serve --yes --bg --https 443 http://127.0.0.1:3000

# Access from anywhere: https://<studio-host>.ts.net
```

### Environment Variables

```bash
# Gateway connection (optional, can set in UI)
NEXT_PUBLIC_GATEWAY_URL=ws://localhost:18789

# Studio access control (required for public binds)
STUDIO_ACCESS_TOKEN=your-secure-token-here

# OpenClaw state directory
OPENCLAW_STATE_DIR=~/.openclaw

# Bind host (default: 127.0.0.1)
HOST=0.0.0.0  # Public bind - requires STUDIO_ACCESS_TOKEN
```

### Configuration Files

Studio settings are stored in `~/.openclaw/openclaw-studio/`:

```
~/.openclaw/
├── openclaw.json              # OpenClaw Gateway config
└── openclaw-studio/
    ├── settings.json          # Gateway URL/token
    └── runtime.db            # Control-plane runtime DB
```

## API & Key Commands

### Studio Setup

```bash
# Development mode with auto-restart
npm run dev

# Production build
npm run build
npm run start

# Turbo dev mode
npm run dev:turbo

# Verify/repair native dependencies
npm run verify:native-runtime:repair
npm run verify:native-runtime:check
```

### TypeScript API Patterns

#### Connecting to Gateway

```typescript
// In Studio UI components
import { useGatewayConnection } from '@/hooks/useGatewayConnection';

export function DashboardPage() {
  const { connected, connect, disconnect, status } = useGatewayConnection();
  
  const handleConnect = async () => {
    try {
      await connect({
        url: 'ws://localhost:18789',
        token: process.env.GATEWAY_TOKEN
      });
    } catch (error) {
      console.error('Connection failed:', error);
    }
  };
  
  return (
    <div>
      <button onClick={handleConnect} disabled={connected}>
        {connected ? 'Connected' : 'Connect'}
      </button>
      <span>Status: {status}</span>
    </div>
  );
}
```

#### Streaming Runtime Events

```typescript
// Server-side SSE streaming
import { NextRequest } from 'next/server';

export async function GET(request: NextRequest) {
  const encoder = new TextEncoder();
  
  const stream = new ReadableStream({
    async start(controller) {
      // Subscribe to runtime events
      const subscription = runtimeStore.subscribe((event) => {
        const data = `data: ${JSON.stringify(event)}\n\n`;
        controller.enqueue(encoder.encode(data));
      });
      
      // Replay history
      const history = await runtimeStore.getHistory();
      for (const event of history) {
        const data = `data: ${JSON.stringify(event)}\n\n`;
        controller.enqueue(encoder.encode(data));
      }
      
      return () => subscription.unsubscribe();
    }
  });
  
  return new Response(stream, {
    headers: {
      'Content-Type': 'text/event-stream',
      'Cache-Control': 'no-cache',
      'Connection': 'keep-alive'
    }
  });
}
```

#### Creating Agents

```typescript
// Agent creation API
interface AgentConfig {
  name: string;
  systemPrompt: string;
  toolPolicy: 'all' | 'allowlist' | 'denylist';
  allowedTools?: string[];
  sandboxEnabled: boolean;
  execApprovalRequired: boolean;
}

export async function createAgent(config: AgentConfig) {
  const response = await fetch('/api/intents/agent-create', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      agent_name: config.name,
      system_prompt: config.systemPrompt,
      tool_policy: config.toolPolicy,
      allowed_tools: config.allowedTools,
      sandbox_config: {
        enabled: config.sandboxEnabled,
        mounts: config.sandboxEnabled ? [
          { host: '/tmp', container: '/workspace', readonly: false }
        ] : []
      },
      exec_approval_required: config.execApprovalRequired
    })
  });
  
  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.message || 'Failed to create agent');
  }
  
  return response.json();
}
```

#### Chat with Streaming

```typescript
// Client-side chat with SSE
import { useEffect, useState } from 'react';

export function ChatInterface({ agentId }: { agentId: string }) {
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [thinking, setThinking] = useState<string[]>([]);
  
  useEffect(() => {
    // Connect to runtime stream
    const eventSource = new EventSource('/api/runtime/stream');
    
    eventSource.addEventListener('message', (event) => {
      const data = JSON.parse(event.data);
      
      switch (data.type) {
        case 'tool_call':
          setMessages(prev => [...prev, {
            role: 'assistant',
            content: `Using tool: ${data.tool_name}`,
            metadata: { type: 'tool', ...data }
          }]);
          break;
          
        case 'thinking':
          setThinking(prev => [...prev, data.content]);
          break;
          
        case 'transcript':
          setMessages(prev => [...prev, {
            role: data.role,
            content: data.content
          }]);
          setThinking([]);
          break;
      }
    });
    
    return () => eventSource.close();
  }, [agentId]);
  
  const sendMessage = async (content: string) => {
    await fetch('/api/intents/chat', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        agent_id: agentId,
        message: content
      })
    });
  };
  
  return (
    <div>
      {messages.map((msg, i) => (
        <div key={i} className={`message ${msg.role}`}>
          {msg.content}
        </div>
      ))}
      {thinking.length > 0 && (
        <div className="thinking">
          {thinking.map((t, i) => <p key={i}>{t}</p>)}
        </div>
      )}
      <input onKeyPress={(e) => {
        if (e.key === 'Enter') {
          sendMessage(e.currentTarget.value);
          e.currentTarget.value = '';
        }
      }} />
    </div>
  );
}
```

## Real-World Examples

### Example 1: Local Development Setup

```bash
#!/bin/bash
# setup-local-dev.sh

# Start OpenClaw Gateway (in separate terminal)
# openclaw gateway start

# Get gateway token
GATEWAY_TOKEN=$(openclaw config get gateway.auth.token)

# Start Studio
npx -y openclaw-studio@latest
cd openclaw-studio

# Configure via environment
export NEXT_PUBLIC_GATEWAY_URL=ws://localhost:18789

npm run dev

# Open http://localhost:3000
# Enter gateway token in UI
```

### Example 2: Production Cloud Setup

```bash
#!/bin/bash
# deploy-studio-cloud.sh

# On your VPS running OpenClaw Gateway
cd /opt
npx -y openclaw-studio@latest
cd openclaw-studio

# Install dependencies
npm install

# Build for production
npm run build

# Set access token for public access
export STUDIO_ACCESS_TOKEN=$(openssl rand -hex 32)

# Expose over Tailscale
tailscale serve --yes --bg --https 443 http://127.0.0.1:3000

# Run production server
npm run start

echo "Studio available at: https://$(tailscale status --json | jq -r '.Self.DNSName')/"
echo "Access token: $STUDIO_ACCESS_TOKEN"
echo "Use: https://your-host.ts.net/?access_token=$STUDIO_ACCESS_TOKEN"
```

### Example 3: Agent with Sandbox & Approvals

```typescript
// create-secure-agent.ts
import { createAgent } from './lib/agent-api';

async function createSecureCodeAgent() {
  const agent = await createAgent({
    name: 'secure-code-assistant',
    systemPrompt: `You are a secure code assistant. 
Always ask before executing commands. 
Work within the sandboxed environment only.`,
    
    toolPolicy: 'allowlist',
    allowedTools: [
      'bash',
      'read_file',
      'write_file',
      'search_files'
    ],
    
    sandboxEnabled: true,
    execApprovalRequired: true
  });
  
  console.log('Agent created:', agent.id);
  return agent;
}

// Usage
createSecureCodeAgent().catch(console.error);
```

### Example 4: Cron Job Configuration

```typescript
// configure-cron-job.ts
interface CronJobConfig {
  agentId: string;
  schedule: string;
  task: string;
  enabled: boolean;
}

async function createCronJob(config: CronJobConfig) {
  const response = await fetch('/api/intents/job-create', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      agent_id: config.agentId,
      schedule: config.schedule,
      task_prompt: config.task,
      enabled: config.enabled
    })
  });
  
  return response.json();
}

// Schedule daily backup
await createCronJob({
  agentId: 'agent-123',
  schedule: '0 0 * * *', // Daily at midnight
  task: 'Create backup of project files and upload to storage',
  enabled: true
});
```

## Common Patterns

### Pattern 1: Conditional Gateway URL

```typescript
// lib/gateway-config.ts
export function getGatewayUrl(): string {
  // Check environment variable first
  if (process.env.NEXT_PUBLIC_GATEWAY_URL) {
    return process.env.NEXT_PUBLIC_GATEWAY_URL;
  }
  
  // Check saved settings
  const settings = loadStudioSettings();
  if (settings?.gatewayUrl) {
    return settings.gatewayUrl;
  }
  
  // Default to localhost
  return 'ws://localhost:18789';
}

export function isSecureConnection(url: string): boolean {
  return url.startsWith('wss://');
}
```

### Pattern 2: Access Token Management

```typescript
// middleware.ts
import { NextResponse } from 'next/server';
import type { NextRequest } from 'next/server';

export function middleware(request: NextRequest) {
  const requiredToken = process.env.STUDIO_ACCESS_TOKEN;
  
  // No token required for loopback-only binds
  if (!requiredToken) {
    return NextResponse.next();
  }
  
  // Check cookie first
  const cookieToken = request.cookies.get('studio_access_token')?.value;
  if (cookieToken === requiredToken) {
    return NextResponse.next();
  }
  
  // Check query param (for initial setup)
  const queryToken = request.nextUrl.searchParams.get('access_token');
  if (queryToken === requiredToken) {
    const response = NextResponse.next();
    response.cookies.set('studio_access_token', requiredToken, {
      httpOnly: true,
      secure: true,
      sameSite: 'strict',
      maxAge: 60 * 60 * 24 * 30 // 30 days
    });
    return response;
  }
  
  return new NextResponse('Unauthorized', { status: 401 });
}

export const config = {
  matcher: ['/api/:path*', '/dashboard/:path*']
};
```

### Pattern 3: Runtime Event Handling

```typescript
// lib/runtime-store.ts
import Database from 'better-sqlite3';

export class RuntimeStore {
  private db: Database.Database;
  private subscribers: Set<(event: RuntimeEvent) => void>;
  
  constructor(dbPath: string) {
    this.db = new Database(dbPath);
    this.subscribers = new Set();
    this.initDb();
  }
  
  private initDb() {
    this.db.exec(`
      CREATE TABLE IF NOT EXISTS runtime_events (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        event_type TEXT NOT NULL,
        agent_id TEXT,
        payload TEXT NOT NULL,
        timestamp INTEGER NOT NULL
      );
      
      CREATE INDEX IF NOT EXISTS idx_agent_timestamp 
      ON runtime_events(agent_id, timestamp);
    `);
  }
  
  async storeEvent(event: RuntimeEvent) {
    const stmt = this.db.prepare(`
      INSERT INTO runtime_events (event_type, agent_id, payload, timestamp)
      VALUES (?, ?, ?, ?)
    `);
    
    stmt.run(
      event.type,
      event.agentId,
      JSON.stringify(event),
      Date.now()
    );
    
    // Notify subscribers
    this.subscribers.forEach(fn => fn(event));
  }
  
  async getHistory(agentId?: string, limit = 100): Promise<RuntimeEvent[]> {
    const query = agentId
      ? `SELECT payload FROM runtime_events 
         WHERE agent_id = ? 
         ORDER BY timestamp DESC LIMIT ?`
      : `SELECT payload FROM runtime_events 
         ORDER BY timestamp DESC LIMIT ?`;
    
    const stmt = this.db.prepare(query);
    const rows = agentId 
      ? stmt.all(agentId, limit)
      : stmt.all(limit);
    
    return rows.map(row => JSON.parse(row.payload)).reverse();
  }
  
  subscribe(callback: (event: RuntimeEvent) => void) {
    this.subscribers.add(callback);
    return {
      unsubscribe: () => this.subscribers.delete(callback)
    };
  }
}
```

## Troubleshooting

### Connection Issues

**Problem**: UI loads but "Connect" fails

```bash
# Check gateway is running
openclaw gateway status

# Verify gateway URL in Studio settings
cat ~/.openclaw/openclaw-studio/settings.json

# If Studio is remote, remember localhost means Studio host
# Use Tailscale Serve or SSH tunnel if needed
```

**Problem**: `EPROTO` / "wrong version number"

```typescript
// Wrong: using wss:// to non-TLS endpoint
const url = 'wss://localhost:18789'; // ❌

// Right: use ws:// for plain HTTP
const url = 'ws://localhost:18789'; // ✅

// Right: use wss:// for Tailscale HTTPS
const url = 'wss://gateway.ts.net'; // ✅
```

**Problem**: Assets 404 under `/studio`

```bash
# Studio must be served at root path
# If you need /studio path:
# 1. Set basePath in next.config.js
# 2. Rebuild Studio

# next.config.js
module.exports = {
  basePath: '/studio',
  // ...
}
```

### Native Module Issues

**Problem**: `better_sqlite3.node` / `NODE_MODULE_VERSION` mismatch

```bash
# Auto-repair (recommended)
npm run verify:native-runtime:repair

# Manual fix
npm rebuild better-sqlite3
npm install

# Check node/npm versions match
node -v && node -p "process.versions.modules"
which node && which npm

# If using nvm, ensure same node version
nvm use 20
npm install
```

**Problem**: SQLite errors on startup

```bash
# Check permissions on state directory
ls -la ~/.openclaw/openclaw-studio/

# Reset runtime DB if corrupted
rm ~/.openclaw/openclaw-studio/runtime.db
npm run dev
```

### Access Token Issues

**Problem**: 401 "Studio access token required"

```bash
# Set access token for public binds
export STUDIO_ACCESS_TOKEN=your-secure-token

# Access UI with token once to set cookie
curl https://studio.ts.net/?access_token=your-secure-token

# Or set in browser
# https://studio.ts.net/?access_token=your-secure-token
```

### Debugging Connection Path

```typescript
// debug-connection.ts
export function debugConnection() {
  console.log('Studio runtime environment:');
  console.log('- Node version:', process.version);
  console.log('- Platform:', process.platform);
  console.log('- CWD:', process.cwd());
  console.log('- State dir:', process.env.OPENCLAW_STATE_DIR || '~/.openclaw');
  
  const isServer = typeof window === 'undefined';
  console.log('- Running on:', isServer ? 'server' : 'browser');
  
  if (isServer) {
    const os = require('os');
    console.log('- Hostname:', os.hostname());
    console.log('- Network interfaces:', 
      Object.keys(os.networkInterfaces()));
  }
  
  console.log('\nGateway connection:');
  console.log('- URL:', process.env.NEXT_PUBLIC_GATEWAY_URL || 'ws://localhost:18789');
  console.log('- Token set:', !!process.env.GATEWAY_TOKEN);
  console.log('- Access token required:', !!process.env.STUDIO_ACCESS_TOKEN);
}
```

## Key Files Reference

```
openclaw-studio/
├── app/
│   ├── api/
│   │   ├── runtime/
│   │   │   └── stream/route.ts    # SSE streaming endpoint
│   │   └── intents/
│   │       ├── agent-create/route.ts
│   │       ├── chat/route.ts
│   │       └── job-create/route.ts
│   ├── dashboard/
│   │   ├── page.tsx               # Main dashboard
│   │   └── agents/page.tsx
│   └── layout.tsx
├── lib/
│   ├── runtime-store.ts           # SQLite runtime DB
│   ├── gateway-client.ts          # WebSocket client
│   └── settings.ts                # Settings persistence
├── hooks/
│   └── useGatewayConnection.ts
├── docs/
│   ├── ui-guide.md
│   ├── pi-chat-streaming.md
│   ├── permissions-sandboxing.md
│   └── color-system.md
├── next.config.js
├── package.json
└── ARCHITECTURE.md
```

## Additional Resources

- **UI Guide**: `docs/ui-guide.md` - Agent creation, cron jobs, exec approvals
- **PI Chat Streaming**: `docs/pi-chat-streaming.md` - SSE event handling, replay, tool calls
- **Permissions**: `docs/permissions-sandboxing.md` - Tool policies, sandbox config, approval flows
- **Architecture**: `ARCHITECTURE.md` - Modules and data flow
- **Discord**: https://discord.gg/EFkFHbZw
