---
name: openclaw-bot-review-dashboard
description: A lightweight web dashboard for monitoring OpenClaw agents, models, sessions, and health status in real-time without a database
triggers:
  - how do I monitor my OpenClaw bots
  - set up OpenClaw dashboard
  - view OpenClaw agent status
  - monitor OpenClaw model usage and tokens
  - check OpenClaw session health
  - deploy OpenClaw monitoring dashboard
  - configure OpenClaw bot review interface
  - track OpenClaw agent performance
---

# OpenClaw Bot Review Dashboard

> Skill by [ara.so](https://ara.so) — Hermes Skills collection.

## What It Does

OpenClaw Bot Review Dashboard is a Next.js-based web interface that provides real-time monitoring for OpenClaw agents across multiple platforms (Feishu, Discord, etc.). It reads directly from `~/.openclaw/openclaw.json` and local session files to display:

- Bot/agent status with model bindings and platform health
- Model configurations with context windows and capabilities
- Session management with token usage tracking
- Statistics and trends (token consumption, response times)
- Skill inventory (built-in, extension, custom)
- Alert rules with notification support
- Gateway health monitoring with auto-polling
- Pixel-art office visualization of agents

No database required — all data is derived from OpenClaw's local configuration.

## Installation

### Standard Setup

```bash
# Clone the repository
git clone https://github.com/xmanrui/OpenClaw-bot-review.git
cd OpenClaw-bot-review

# Install dependencies
npm install

# Start development server
npm run start
```

The dashboard will be available at `http://localhost:3000`.

### Production Build

```bash
# Build for production
npm run build

# Start production server
npm run start
```

### Docker Deployment

```bash
# Build Docker image
docker build -t openclaw-dashboard .

# Run container with default OpenClaw path (~/.openclaw)
docker run -d --name openclaw-dashboard \
  -p 3000:3000 \
  -v $HOME/.openclaw:/root/.openclaw:ro \
  openclaw-dashboard

# Run with custom OpenClaw config path
docker run -d --name openclaw-dashboard \
  -p 3000:3000 \
  -e OPENCLAW_HOME=/opt/openclaw \
  -v /path/to/openclaw:/opt/openclaw:ro \
  openclaw-dashboard
```

## Requirements

- **Node.js**: 18+ required
- **OpenClaw**: Must be installed with config at `~/.openclaw/openclaw.json`
- **Platforms**: Works with Feishu, Discord, and other OpenClaw-supported platforms

## Configuration

### Environment Variables

```bash
# Custom OpenClaw config path
export OPENCLAW_HOME=/opt/openclaw

# Port configuration (default: 3000)
export PORT=3000

# Start with custom config
OPENCLAW_HOME=/opt/openclaw npm run start
```

### Directory Structure

The dashboard expects the following OpenClaw directory structure:

```
~/.openclaw/
├── openclaw.json          # Main configuration file
├── sessions/              # Session data per agent
│   ├── agent1/
│   │   ├── session1.json
│   │   └── session2.json
│   └── agent2/
└── skills/                # Installed skills
```

### OpenClaw Configuration

The dashboard reads from `openclaw.json`:

```json
{
  "agents": [
    {
      "name": "my-agent",
      "emoji": "🤖",
      "model": "gpt-4",
      "platforms": {
        "feishu": {
          "app_id": "${FEISHU_APP_ID}",
          "app_secret": "${FEISHU_APP_SECRET}"
        }
      }
    }
  ],
  "models": {
    "gpt-4": {
      "provider": "openai",
      "api_key": "${OPENAI_API_KEY}",
      "context_window": 8192,
      "max_output": 4096
    }
  },
  "gateway": {
    "enabled": true,
    "port": 8080
  }
}
```

## Key Features and Usage

### Bot Dashboard

View all agents at a glance:

```typescript
// The dashboard automatically reads from ~/.openclaw/openclaw.json
// Each bot card shows:
// - Name and emoji
// - Bound model
// - Platform status (Feishu, Discord, etc.)
// - Session count
// - Gateway health indicator
```

### Model Management

Monitor all configured models:

```typescript
// Models page displays:
// - Provider (OpenAI, Anthropic, etc.)
// - Model name and version
// - Context window size
// - Max output tokens
// - Reasoning support
// - Per-model connectivity test
```

### Session Monitoring

Track active sessions per agent:

```typescript
// Sessions are automatically detected from:
// ~/.openclaw/sessions/{agent-name}/*.json

// Each session shows:
// - Type (DM, group, cron)
// - Platform
// - Token usage
// - Last activity
// - Connectivity test button
```

### Auto-Refresh Configuration

```typescript
// Available refresh intervals:
// - Manual (no auto-refresh)
// - 10 seconds
// - 30 seconds
// - 1 minute
// - 5 minutes
// - 10 minutes

// Select from dropdown in top-right corner
```

### Theme and Language

```typescript
// Theme toggle: Light / Dark mode
// Available in sidebar

// Language toggle: English / 中文
// Available in top navigation
```

## API Routes

The dashboard includes Next.js API routes for reading OpenClaw data:

### Get All Bots

```typescript
// pages/api/bots.ts
import type { NextApiRequest, NextApiResponse } from 'next';
import { readOpenClawConfig } from '@/lib/openclaw';

export default async function handler(
  req: NextApiRequest,
  res: NextApiResponse
) {
  if (req.method !== 'GET') {
    return res.status(405).json({ error: 'Method not allowed' });
  }

  try {
    const config = await readOpenClawConfig();
    const bots = config.agents.map(agent => ({
      name: agent.name,
      emoji: agent.emoji,
      model: agent.model,
      platforms: Object.keys(agent.platforms || {}),
      sessionCount: getSessionCount(agent.name),
    }));
    
    res.status(200).json({ bots });
  } catch (error) {
    res.status(500).json({ error: 'Failed to read config' });
  }
}
```

### Get Models

```typescript
// pages/api/models.ts
export default async function handler(
  req: NextApiRequest,
  res: NextApiResponse
) {
  const config = await readOpenClawConfig();
  const models = Object.entries(config.models).map(([name, model]) => ({
    name,
    provider: model.provider,
    contextWindow: model.context_window,
    maxOutput: model.max_output,
    reasoning: model.reasoning_support || false,
  }));
  
  res.status(200).json({ models });
}
```

### Test Platform Connection

```typescript
// pages/api/test/platform.ts
export default async function handler(
  req: NextApiRequest,
  res: NextApiResponse
) {
  const { platform, agentName } = req.query;
  
  try {
    const result = await testPlatformConnection(
      platform as string,
      agentName as string
    );
    res.status(200).json({ success: result.success, message: result.message });
  } catch (error) {
    res.status(500).json({ success: false, error: error.message });
  }
}
```

### Gateway Health Check

```typescript
// pages/api/gateway/health.ts
export default async function handler(
  req: NextApiRequest,
  res: NextApiResponse
) {
  const config = await readOpenClawConfig();
  
  if (!config.gateway?.enabled) {
    return res.status(200).json({ healthy: false, reason: 'disabled' });
  }
  
  try {
    const port = config.gateway.port || 8080;
    const response = await fetch(`http://localhost:${port}/health`);
    const healthy = response.ok;
    
    res.status(200).json({ healthy, port });
  } catch (error) {
    res.status(200).json({ healthy: false, reason: 'unreachable' });
  }
}
```

## Common Patterns

### Reading OpenClaw Config

```typescript
// lib/openclaw.ts
import fs from 'fs/promises';
import path from 'path';
import os from 'os';

export interface OpenClawConfig {
  agents: Agent[];
  models: Record<string, Model>;
  gateway?: Gateway;
}

export async function readOpenClawConfig(): Promise<OpenClawConfig> {
  const openclawHome = process.env.OPENCLAW_HOME || 
    path.join(os.homedir(), '.openclaw');
  
  const configPath = path.join(openclawHome, 'openclaw.json');
  
  try {
    const content = await fs.readFile(configPath, 'utf-8');
    return JSON.parse(content);
  } catch (error) {
    throw new Error(`Failed to read OpenClaw config: ${error.message}`);
  }
}
```

### Reading Session Data

```typescript
// lib/sessions.ts
export async function getAgentSessions(agentName: string) {
  const openclawHome = process.env.OPENCLAW_HOME || 
    path.join(os.homedir(), '.openclaw');
  
  const sessionsDir = path.join(openclawHome, 'sessions', agentName);
  
  try {
    const files = await fs.readdir(sessionsDir);
    const sessions = await Promise.all(
      files
        .filter(f => f.endsWith('.json'))
        .map(async file => {
          const content = await fs.readFile(
            path.join(sessionsDir, file),
            'utf-8'
          );
          return JSON.parse(content);
        })
    );
    
    return sessions;
  } catch (error) {
    return [];
  }
}
```

### Testing Platform Connection

```typescript
// lib/test.ts
export async function testPlatformConnection(
  platform: string,
  agentName: string
): Promise<{ success: boolean; message: string }> {
  const config = await readOpenClawConfig();
  const agent = config.agents.find(a => a.name === agentName);
  
  if (!agent) {
    return { success: false, message: 'Agent not found' };
  }
  
  const platformConfig = agent.platforms?.[platform];
  if (!platformConfig) {
    return { success: false, message: `${platform} not configured` };
  }
  
  if (platform === 'feishu') {
    // Test Feishu API
    try {
      const response = await fetch('https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          app_id: process.env[platformConfig.app_id] || platformConfig.app_id,
          app_secret: process.env[platformConfig.app_secret] || platformConfig.app_secret,
        }),
      });
      
      const data = await response.json();
      return {
        success: data.code === 0,
        message: data.code === 0 ? 'Connected' : data.msg,
      };
    } catch (error) {
      return { success: false, message: error.message };
    }
  }
  
  return { success: false, message: 'Platform test not implemented' };
}
```

### Component Example: Bot Card

```typescript
// components/BotCard.tsx
import { useState } from 'react';

interface BotCardProps {
  bot: {
    name: string;
    emoji: string;
    model: string;
    platforms: string[];
    sessionCount: number;
  };
}

export default function BotCard({ bot }: BotCardProps) {
  const [isTestingPlatform, setIsTestingPlatform] = useState(false);
  
  const testPlatform = async (platform: string) => {
    setIsTestingPlatform(true);
    try {
      const res = await fetch(
        `/api/test/platform?platform=${platform}&agentName=${bot.name}`
      );
      const data = await res.json();
      alert(data.message);
    } finally {
      setIsTestingPlatform(false);
    }
  };
  
  return (
    <div className="border rounded-lg p-4 shadow-sm hover:shadow-md transition">
      <div className="flex items-center gap-2 mb-2">
        <span className="text-3xl">{bot.emoji}</span>
        <h3 className="text-lg font-semibold">{bot.name}</h3>
      </div>
      
      <div className="text-sm text-gray-600 dark:text-gray-400">
        <p>Model: {bot.model}</p>
        <p>Sessions: {bot.sessionCount}</p>
      </div>
      
      <div className="mt-3 flex gap-2">
        {bot.platforms.map(platform => (
          <button
            key={platform}
            onClick={() => testPlatform(platform)}
            disabled={isTestingPlatform}
            className="px-2 py-1 text-xs bg-blue-500 text-white rounded hover:bg-blue-600 disabled:opacity-50"
          >
            Test {platform}
          </button>
        ))}
      </div>
    </div>
  );
}
```

## Troubleshooting

### Dashboard Not Loading Bots

**Problem**: Dashboard shows no bots or "Config not found" error.

**Solution**:

```bash
# Verify OpenClaw config exists
ls -la ~/.openclaw/openclaw.json

# Check permissions
chmod 644 ~/.openclaw/openclaw.json

# If using custom path, set env var
export OPENCLAW_HOME=/path/to/openclaw
npm run start
```

### Gateway Health Shows Unhealthy

**Problem**: Gateway indicator shows red or unreachable.

**Solution**:

```bash
# Check if gateway is enabled in config
cat ~/.openclaw/openclaw.json | grep -A 3 gateway

# Verify gateway is running
netstat -an | grep 8080

# Check OpenClaw gateway logs
tail -f ~/.openclaw/logs/gateway.log
```

### Platform Test Fails

**Problem**: Clicking "Test Feishu" or "Test Discord" returns error.

**Solution**:

```bash
# Verify environment variables are set
echo $FEISHU_APP_ID
echo $FEISHU_APP_SECRET

# Check if credentials are in openclaw.json
cat ~/.openclaw/openclaw.json | grep -A 5 feishu

# Ensure proper format (${VAR_NAME} or direct value)
# Dashboard resolves process.env for ${} references
```

### Sessions Not Showing

**Problem**: Session count shows 0 or sessions page is empty.

**Solution**:

```bash
# Check sessions directory exists
ls -la ~/.openclaw/sessions/

# Verify agent has session files
ls ~/.openclaw/sessions/my-agent/

# Check JSON file format
cat ~/.openclaw/sessions/my-agent/session1.json | jq .
```

### Docker Container Can't Read Config

**Problem**: Docker container shows "Config not found" error.

**Solution**:

```bash
# Mount OpenClaw directory correctly
docker run -d --name openclaw-dashboard \
  -p 3000:3000 \
  -v $HOME/.openclaw:/root/.openclaw:ro \
  openclaw-dashboard

# For custom path, use OPENCLAW_HOME
docker run -d --name openclaw-dashboard \
  -p 3000:3000 \
  -e OPENCLAW_HOME=/data/openclaw \
  -v /opt/openclaw:/data/openclaw:ro \
  openclaw-dashboard

# Check logs
docker logs openclaw-dashboard
```

### Auto-Refresh Not Working

**Problem**: Dashboard doesn't update automatically.

**Solution**:

```typescript
// Check if refresh interval is set
// In browser dev tools:
localStorage.getItem('dashboardRefreshInterval')

// Should return: '10s', '30s', '1m', '5m', or '10m'

// Clear and reset
localStorage.removeItem('dashboardRefreshInterval')
// Then select interval from dropdown again
```

### Build Fails

**Problem**: `npm run build` errors.

**Solution**:

```bash
# Clear cache and reinstall
rm -rf node_modules package-lock.json
npm install

# Use Node 18+
node --version  # Should be v18.0.0 or higher

# Check for TypeScript errors
npm run type-check

# Build with verbose output
npm run build -- --debug
```

## Additional Resources

- [OpenClaw Documentation](https://github.com/openclaw/openclaw)
- [Quick Start Guide](https://github.com/xmanrui/OpenClaw-bot-review/blob/main/quick_start.md)
- [GitHub Issues](https://github.com/xmanrui/OpenClaw-bot-review/issues)
- [Next.js Documentation](https://nextjs.org/docs)
