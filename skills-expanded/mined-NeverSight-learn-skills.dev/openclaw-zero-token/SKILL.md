---
name: openclaw-zero-token
description: Use major AI models (Claude, ChatGPT, Gemini, DeepSeek, Qwen, etc.) without API tokens by leveraging browser authentication instead of paid API keys
triggers:
  - "set up openclaw zero token"
  - "use AI models without API keys"
  - "configure browser auth for LLMs"
  - "run DeepSeek/Claude/Qwen without tokens"
  - "onboard web model authentication"
  - "start openclaw gateway"
  - "use tool calling with web models"
  - "query multiple AI models at once"
---

# OpenClaw Zero Token

> Skill by [ara.so](https://ara.so) — Hermes Skills collection.

OpenClaw Zero Token is a TypeScript-based gateway that lets you use major AI models (Claude, ChatGPT, Gemini, DeepSeek, Qwen, Kimi, Doubao, Grok, GLM, Xiaomi MiMo, Manus) **completely free** by automating browser-based authentication instead of requiring paid API tokens. It drives official web UIs using Chrome DevTools Protocol (CDP) and Playwright to capture credentials, then proxies requests through a unified OpenAI-compatible API gateway.

## What It Does

- **Zero-cost LLM access**: Log in via browser once, reuse credentials for API calls
- **Unified gateway**: OpenAI-compatible API endpoint on port 3001
- **11 web models with tool calling**: `web_search`, `web_fetch`, `exec`, `read`, `write`, `message`
- **AskOnce multi-model queries**: Broadcast one question to all configured providers
- **Web UI + CLI + Gateway**: Multiple interaction modes (Lit 3.x UI, TUI, REST API)

### Supported Providers

| Provider       | Status | Auth Method      |
|----------------|--------|------------------|
| DeepSeek       | ✅     | Browser login    |
| Qwen (intl/cn) | ✅     | Browser login    |
| Kimi           | ✅     | Browser login    |
| Claude Web     | ✅     | Browser login    |
| ChatGPT Web    | ✅     | Browser login    |
| Gemini Web     | ✅     | Browser login    |
| Grok Web       | ✅     | Browser login    |
| Doubao         | ✅     | Browser login    |
| GLM/GLM Intl   | ✅     | Browser login    |
| Xiaomi MiMo    | ✅     | Browser login    |
| Manus API      | ✅     | API key (free)   |

## Installation

### Prerequisites

```bash
# Check versions
node --version  # >= 22.12.0
pnpm --version  # >= 9.0.0

# Install Node.js 22+ if needed
curl -fsSL https://deb.nodesource.com/setup_22.x | sudo -E bash -
sudo apt-get install -y nodejs

# Install pnpm
npm install -g pnpm
```

### Clone and Build

```bash
git clone https://github.com/linuxhsj/openclaw-zero-token.git
cd openclaw-zero-token

# Install dependencies
pnpm install

# Build backend + frontend
pnpm build
pnpm ui:build
```

## Configuration

### Environment Setup

Create `.env` file:

```bash
# Gateway settings
PORT=3001
NODE_ENV=production

# Browser debugging (DO NOT expose publicly)
CHROME_DEBUG_PORT=9222

# Optional: workspace for agent file access
AGENT_WORKSPACE=/home/user/agent-workspace

# Optional: logging
LOG_LEVEL=info
```

### First-Time Authentication Flow

OpenClaw uses a three-step process:

1. **Start debug Chrome** → Opens browser on port 9222
2. **Login to web models** → Manual browser login (scan QR / password)
3. **Run onboard wizard** → Captures credentials automatically

```bash
# Terminal 1: Start Chrome in debug mode (keep running)
./start-chrome-debug.sh

# This opens Chrome with tabs for:
# - DeepSeek: https://chat.deepseek.com
# - Qwen intl: https://hf.co/chat
# - Qwen cn: https://tongyi.aliyun.com
# - Kimi: https://kimi.moonshot.cn
# - Claude: https://claude.ai
# etc.

# LOG IN to each site manually in the browser
```

```bash
# Terminal 2: Run authentication wizard
./onboard.sh webauth

# Interactive menu:
# [1] deepseek-web
# [2] qwen-web
# [3] qwen-cn
# [4] kimi
# [5] claude-web
# ... etc

# Select provider → wizard captures auth automatically
# Saved to: data/auth/<provider>.json
```

The `onboard.sh` script uses Playwright CDP to intercept network requests and extract:
- Cookies
- Bearer tokens
- User-Agent headers

### Starting the Gateway

```bash
# Start server (daemon mode)
./server.sh start

# Other commands
./server.sh stop
./server.sh restart
./server.sh status

# Manual start (foreground, for debugging)
pnpm start
```

Gateway runs on **http://localhost:3001** with OpenAI-compatible endpoints.

## Key Commands and Scripts

### Core Scripts

| Script                     | Purpose                                    |
|----------------------------|-------------------------------------------|
| `./start-chrome-debug.sh`  | Launch Chrome on port 9222 for logins     |
| `./onboard.sh webauth`     | Run auth wizard to capture credentials    |
| `./server.sh [start|stop]` | Manage gateway daemon                     |
| `pnpm build`               | Build TypeScript backend                  |
| `pnpm ui:build`            | Build Lit 3.x frontend                    |
| `pnpm test`                | Run test suite                            |

### pnpm Scripts (package.json)

```bash
# Build
pnpm build          # Compile TypeScript
pnpm ui:build       # Build frontend
pnpm build:all      # Both backend + UI

# Development
pnpm dev            # Watch mode with hot reload
pnpm start          # Production server

# Testing
pnpm test           # Run tests
pnpm lint           # ESLint check
pnpm format         # Prettier format
```

## API Usage

### OpenAI-Compatible Endpoints

OpenClaw exposes a standard OpenAI API format on port 3001:

```bash
# List available models
curl http://localhost:3001/v1/models

# Chat completion (non-streaming)
curl http://localhost:3001/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "deepseek-web/deepseek-chat",
    "messages": [{"role": "user", "content": "Hello!"}]
  }'

# Streaming
curl http://localhost:3001/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "qwen-web/qwen-turbo",
    "messages": [{"role": "user", "content": "Count to 5"}],
    "stream": true
  }'
```

### TypeScript Client Example

```typescript
import OpenAI from 'openai';

const client = new OpenAI({
  baseURL: 'http://localhost:3001/v1',
  apiKey: 'not-needed', // Zero Token doesn't require keys
});

async function chat() {
  const response = await client.chat.completions.create({
    model: 'deepseek-web/deepseek-chat',
    messages: [
      { role: 'user', content: 'Explain TypeScript generics' }
    ],
  });

  console.log(response.choices[0].message.content);
}

chat();
```

### Streaming Response

```typescript
async function streamChat() {
  const stream = await client.chat.completions.create({
    model: 'kimi/moonshot-v1-8k',
    messages: [{ role: 'user', content: 'Write a haiku' }],
    stream: true,
  });

  for await (const chunk of stream) {
    process.stdout.write(chunk.choices[0]?.delta?.content || '');
  }
}
```

## Tool Calling (Web Models)

OpenClaw injects tool definitions into prompts for 11/13 web models. Tools are only injected when user message contains keywords like "search", "read", "execute".

### Available Tools

| Tool         | Function                          | Provider Support |
|--------------|-----------------------------------|------------------|
| `web_search` | DuckDuckGo search                 | 11/13 models     |
| `web_fetch`  | Fetch webpage content             | 11/13 models     |
| `exec`       | Execute shell command             | 11/13 models     |
| `read`       | Read file (workspace restricted)  | 11/13 models     |
| `write`      | Write file (workspace restricted) | 11/13 models     |
| `message`    | Structured output                 | 11/13 models     |

### Tool Calling Example

```typescript
const response = await client.chat.completions.create({
  model: 'deepseek-web/deepseek-chat',
  messages: [{
    role: 'user',
    content: 'Search for TypeScript 5.4 release notes and summarize'
  }],
});

// Model automatically:
// 1. Detects "search" keyword
// 2. Calls web_search tool
// 3. Fetches results
// 4. Summarizes content
```

### Agent File Access Configuration

Tools like `read`/`write` are restricted to the configured workspace:

```bash
# In .env
AGENT_WORKSPACE=/home/user/projects/safe-zone
```

```typescript
// Attempting to read outside workspace fails
const badRead = await client.chat.completions.create({
  model: 'kimi/moonshot-v1-32k',
  messages: [{
    role: 'user',
    content: 'Read /etc/passwd'  // ❌ Blocked
  }],
});

// Within workspace succeeds
const goodRead = await client.chat.completions.create({
  model: 'kimi/moonshot-v1-32k',
  messages: [{
    role: 'user',
    content: 'Read project-notes.md'  // ✅ Allowed if in workspace
  }],
});
```

## AskOnce: Multi-Model Queries

Query all configured providers simultaneously:

```bash
# CLI usage (if implemented)
pnpm ask-once "What is the capital of France?"

# Returns responses from:
# - DeepSeek: "Paris..."
# - Qwen: "The capital is Paris..."
# - Kimi: "Paris, established in..."
# etc.
```

```typescript
// Programmatic AskOnce
import { askOnce } from './src/zero-token/ask-once';

const results = await askOnce({
  query: 'Explain quantum entanglement in one sentence',
  providers: ['deepseek-web', 'qwen-web', 'kimi', 'claude-web'],
});

results.forEach(({ provider, response, duration }) => {
  console.log(`[${provider}] (${duration}ms): ${response}`);
});
```

## Common Patterns

### 1. Multi-Provider Failover

```typescript
const providers = [
  'deepseek-web/deepseek-chat',
  'qwen-web/qwen-turbo',
  'kimi/moonshot-v1-8k',
];

async function chatWithFailover(message: string) {
  for (const model of providers) {
    try {
      const response = await client.chat.completions.create({
        model,
        messages: [{ role: 'user', content: message }],
      });
      return response.choices[0].message.content;
    } catch (error) {
      console.warn(`${model} failed, trying next...`);
    }
  }
  throw new Error('All providers failed');
}
```

### 2. Model Routing by Task

```typescript
function selectModel(task: string): string {
  if (task.includes('reasoning') || task.includes('logic')) {
    return 'deepseek-web/deepseek-reasoner';
  }
  if (task.includes('code')) {
    return 'qwen-web/qwen-plus';
  }
  return 'kimi/moonshot-v1-8k'; // default
}

const model = selectModel('Write a sorting algorithm');
const response = await client.chat.completions.create({
  model,
  messages: [{ role: 'user', content: 'Implement quicksort in Python' }],
});
```

### 3. Workspace-Safe Agent

```typescript
import * as path from 'path';

const WORKSPACE = process.env.AGENT_WORKSPACE || '/tmp/agent-workspace';

async function safeAgentTask(instruction: string) {
  // Ensure workspace exists
  await fs.promises.mkdir(WORKSPACE, { recursive: true });

  const response = await client.chat.completions.create({
    model: 'kimi/moonshot-v1-32k',
    messages: [{
      role: 'system',
      content: `You are a helpful agent. All file operations must be within ${WORKSPACE}.`
    }, {
      role: 'user',
      content: instruction
    }],
  });

  return response.choices[0].message.content;
}

// Example: "Create a file notes.txt with today's date"
await safeAgentTask('Write the current timestamp to notes.txt');
```

### 4. Re-authentication Helper

```typescript
import { execSync } from 'child_process';

async function ensureAuth(provider: string) {
  const authPath = `data/auth/${provider}.json`;
  
  try {
    const authData = await fs.promises.readFile(authPath, 'utf-8');
    const parsed = JSON.parse(authData);
    
    // Check if token is expired (example logic)
    if (Date.now() > parsed.expiresAt) {
      console.log(`Auth expired for ${provider}, re-running onboard...`);
      execSync(`./onboard.sh webauth ${provider}`, { stdio: 'inherit' });
    }
  } catch (error) {
    console.log(`No auth found for ${provider}, running onboard...`);
    execSync(`./onboard.sh webauth ${provider}`, { stdio: 'inherit' });
  }
}

// Before making API calls
await ensureAuth('deepseek-web');
```

## Troubleshooting

### Chrome Debug Port Issues

**Symptom**: `onboard.sh` fails with "Cannot connect to CDP"

```bash
# Kill existing Chrome processes
pkill -f "chrome.*remote-debugging-port=9222"

# Restart debug Chrome
./start-chrome-debug.sh

# Verify port is open
lsof -i :9222  # Should show Chrome process
```

### Authentication Expired

**Symptom**: API calls return 401/403 after initial setup

```bash
# Re-run onboarding for specific provider
./onboard.sh webauth

# Select the provider that's failing
# Example: [1] deepseek-web

# Manually verify in browser:
# 1. Open http://localhost:9222 in another browser
# 2. Navigate to chat site
# 3. Check if logged in
```

### Stream Parsing Errors

**Symptom**: "Cannot parse SSE stream" for Doubao or Gemini

```typescript
// Use non-streaming for unstable providers
const response = await client.chat.completions.create({
  model: 'doubao/doubao-pro',
  messages: [{ role: 'user', content: 'Hello' }],
  stream: false,  // ← Disable streaming
});
```

### Tool Calling Not Triggering

**Symptom**: Model doesn't use tools despite keyword in message

```typescript
// Ensure keywords are explicit
const response = await client.chat.completions.create({
  model: 'kimi/moonshot-v1-32k',
  messages: [{
    role: 'user',
    content: 'SEARCH for TypeScript 5.4 release notes'  // ← Explicit keyword
  }],
});

// Check middleware logs
// Tool injection only happens when keywords detected:
// "search", "fetch", "execute", "read file", "write file"
```

### Gateway Won't Start

```bash
# Check if port 3001 is already in use
lsof -i :3001

# Kill existing process
kill -9 $(lsof -t -i :3001)

# Check logs
tail -f logs/gateway.log

# Verify build succeeded
pnpm build
pnpm ui:build
```

### Model Rate Limits

**Symptom**: Web model returns "Too many requests"

```typescript
// Implement exponential backoff
async function chatWithRetry(model: string, message: string, retries = 3) {
  for (let i = 0; i < retries; i++) {
    try {
      return await client.chat.completions.create({
        model,
        messages: [{ role: 'user', content: message }],
      });
    } catch (error: any) {
      if (error.status === 429 && i < retries - 1) {
        const delay = Math.pow(2, i) * 1000;
        console.log(`Rate limited, waiting ${delay}ms...`);
        await new Promise(resolve => setTimeout(resolve, delay));
      } else {
        throw error;
      }
    }
  }
}
```

## Advanced Configuration

### Custom Provider Setup

```typescript
// src/zero-token/providers/custom-provider.ts
import { BaseWebProvider } from './base-web-provider';

export class CustomProvider extends BaseWebProvider {
  constructor() {
    super({
      name: 'custom-web',
      chatUrl: 'https://custom-ai.example.com/chat',
      apiEndpoint: 'https://custom-ai.example.com/api/v1/chat',
    });
  }

  async authenticate(page: Page): Promise<AuthData> {
    // Custom auth logic
    const token = await page.evaluate(() => {
      return localStorage.getItem('auth_token');
    });
    
    return {
      token,
      cookies: await page.context().cookies(),
      userAgent: await page.evaluate(() => navigator.userAgent),
    };
  }
}
```

### Environment Variables Reference

```bash
# Core settings
PORT=3001                          # Gateway port
NODE_ENV=production                # production | development
LOG_LEVEL=info                     # error | warn | info | debug

# Browser automation
CHROME_DEBUG_PORT=9222             # CDP port
HEADLESS=false                     # true for headless mode

# Agent configuration
AGENT_WORKSPACE=/path/to/workspace # Tool file access restriction
TOOL_TIMEOUT=30000                 # Tool execution timeout (ms)

# Provider-specific (optional)
DEEPSEEK_CUSTOM_ENDPOINT=https://... # Override default endpoints
QWEN_API_VERSION=v1                  # API version
```

## File Structure

```
openclaw-zero-token/
├── src/
│   ├── zero-token/
│   │   ├── providers/          # Web model implementations
│   │   │   ├── deepseek-web.ts
│   │   │   ├── qwen-web.ts
│   │   │   ├── kimi.ts
│   │   │   └── ...
│   │   ├── tool-calling/       # Tool injection middleware
│   │   │   ├── tools.ts        # Tool definitions
│   │   │   └── middleware.ts   # Prompt injection logic
│   │   ├── ask-once/           # Multi-model query system
│   │   └── auth/               # Authentication capture
│   ├── gateway/                # OpenAI-compatible API gateway
│   └── ui/                     # Lit 3.x web interface
├── data/
│   └── auth/                   # Stored credentials (gitignored)
│       ├── deepseek-web.json
│       ├── qwen-web.json
│       └── ...
├── scripts/
│   ├── start-chrome-debug.sh   # Chrome launcher
│   ├── onboard.sh              # Auth wizard
│   └── server.sh               # Gateway daemon manager
├── .env                        # Environment config
└── package.json
```

## Security Notes

1. **Auth Data**: `data/auth/*.json` contains sensitive credentials — never commit
2. **Chrome Debug Port**: Port 9222 allows full browser control — DO NOT expose externally
3. **Workspace Restriction**: Agent file tools are sandboxed to `AGENT_WORKSPACE`
4. **HTTPS Required**: Use reverse proxy (nginx/Caddy) for production deployment

Example nginx config:

```nginx
server {
  listen 443 ssl;
  server_name openclaw.example.com;
  
  ssl_certificate /path/to/cert.pem;
  ssl_certificate_key /path/to/key.pem;
  
  location / {
    proxy_pass http://localhost:3001;
    proxy_http_version 1.1;
    proxy_set_header Upgrade $http_upgrade;
    proxy_set_header Connection 'upgrade';
    proxy_set_header Host $host;
  }
}
```

## References

- [OpenClaw Upstream](https://github.com/openclaw/openclaw)
- [Zero Token Documentation](docs/zero-token/index.md)
- [Tool Calling Paper (arXiv:2407.04997)](https://arxiv.org/html/2407.04997v1)
- [ComfyUI LLM Party](https://github.com/heshengtao/comfyui_LLM_party)
