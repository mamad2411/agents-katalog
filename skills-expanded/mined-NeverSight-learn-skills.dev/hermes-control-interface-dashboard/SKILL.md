---
name: hermes-control-interface-dashboard
description: Self-hosted web dashboard for managing Hermes AI agent stacks with terminals, file explorer, multi-agent gateway, and RBAC
triggers:
  - "set up hermes control interface dashboard"
  - "manage hermes agents through web ui"
  - "configure hermes control interface"
  - "deploy hermes dashboard with rbac"
  - "use hermes control interface api"
  - "troubleshoot hermes control interface"
  - "create users in hermes control"
  - "manage hermes gateway profiles"
---

# Hermes Control Interface Dashboard

> Skill by [ara.so](https://ara.so) — Hermes Skills collection.

A self-hosted web dashboard for managing the Hermes AI agent stack. Provides browser-based terminal, file explorer, session management, cron jobs, multi-agent gateway control, token analytics, and RBAC — all behind password authentication.

**Stack:** Vanilla JS + Vite, Node.js, Express, WebSocket, xterm.js  
**Port:** 10272 (default)  
**Version:** 3.5.0

## Installation

### Prerequisites

```bash
# Required: Node.js 18+, build tools for node-pty
sudo apt-get install -y python3 make g++  # Ubuntu/Debian
# OR
brew install python3  # macOS
```

### Manual Installation (Recommended)

```bash
# Clone repository
git clone https://github.com/xaspx/hermes-control-interface.git
cd hermes-control-interface

# Install dependencies
npm install

# Configure environment
cp .env.example .env

# Generate secure secret
openssl rand -hex 32  # Copy output for HERMES_CONTROL_SECRET

# Edit .env with your settings
nano .env
```

### Environment Configuration

**Minimal `.env`:**

```bash
# Required
HERMES_CONTROL_PASSWORD=your-secure-password-here
HERMES_CONTROL_SECRET=<output-from-openssl-rand-hex-32>

# Optional
PORT=10272
NODE_ENV=production
HERMES_CONTROL_ROOTS=~/.hermes,~/Documents  # File explorer roots
```

### Build and Run

```bash
# Build frontend
npm run build

# Start server
npm start

# Development mode (auto-reload)
npm run dev
```

### Production Deployment (Systemd)

```bash
# Create systemd service
sudo tee /etc/systemd/system/hermes-control.service > /dev/null <<EOF
[Unit]
Description=Hermes Control Interface
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=$(pwd)
ExecStart=/usr/bin/node server.js
Restart=always
Environment=NODE_ENV=production

[Install]
WantedBy=multi-user.target
EOF

# Enable and start
sudo systemctl enable hermes-control
sudo systemctl start hermes-control
sudo systemctl status hermes-control
```

## Core Features

### Authentication & RBAC

HCI supports multi-user authentication with role-based access control:

**Roles:**
- `admin` — Full access (all 20 permissions)
- `viewer` — Read-only access
- `custom` — Granular permission selection

**Key Permissions:**
- `agents:read`, `agents:write`, `agents:delete`
- `chat:read`, `chat:write`
- `sessions:read`, `sessions:write`, `sessions:delete`
- `config:read`, `config:write`
- `gateway:control`, `gateway:logs`
- `files:read`, `files:write`
- `terminal:exec`
- `users:manage`
- `system:maintain`
- `cron:manage`

**Creating Users (via Maintenance → Users):**

```javascript
// API endpoint: POST /api/users
{
  "username": "alice",
  "password": "secure-password",
  "role": "viewer"
}
```

### Multi-Agent Gateway Management

**Profile Structure:**
```
~/.hermes/
  ├── profiles/
  │   ├── default/
  │   │   └── config.yaml
  │   ├── production/
  │   │   └── config.yaml
  │   └── testing/
  │       └── config.yaml
```

**API: List Profiles**

```javascript
// GET /api/agents/profiles
fetch('/api/agents/profiles', {
  headers: { 
    'Authorization': `Bearer ${sessionToken}`,
    'X-CSRF-Token': csrfToken 
  }
})
.then(res => res.json())
.then(data => {
  // data.profiles = [{ name: 'default', isDefault: true, status: 'running', model: 'hermes-3' }]
});
```

**API: Start/Stop Gateway**

```javascript
// POST /api/agents/gateway/start
fetch('/api/agents/gateway/start', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'Authorization': `Bearer ${sessionToken}`,
    'X-CSRF-Token': csrfToken
  },
  body: JSON.stringify({ profile: 'production' })
})
.then(res => res.json())
.then(data => console.log(data.message)); // "Gateway started for production"
```

**API: Create Profile**

```javascript
// POST /api/agents/profiles
fetch('/api/agents/profiles', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'Authorization': `Bearer ${sessionToken}`,
    'X-CSRF-Token': csrfToken
  },
  body: JSON.stringify({
    name: 'staging',
    cloneFrom: 'default'  // Optional: clone existing config
  })
});
```

### Chat Interface

**Session Management:**

```javascript
// POST /api/chat/send
const sendMessage = async (message, sessionId = null) => {
  const args = sessionId 
    ? ['--continue', sessionId, message]
    : ['--continue', '', message];  // Empty string creates new session

  const response = await fetch('/api/chat/send', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${sessionToken}`,
      'X-CSRF-Token': csrfToken
    },
    body: JSON.stringify({
      profile: 'default',
      args: args,
      suppressBanner: true  // Use -Q flag for clean output
    })
  });

  const reader = response.body.getReader();
  const decoder = new TextDecoder();
  
  while (true) {
    const { done, value } = await reader.read();
    if (done) break;
    
    const chunk = decoder.decode(value);
    const lines = chunk.split('\n');
    
    for (const line of lines) {
      if (line.startsWith('data: ')) {
        const data = JSON.parse(line.slice(6));
        
        if (data.type === 'session_id') {
          console.log('Session ID:', data.sessionId);
        } else if (data.type === 'tool_call') {
          console.log('Tool:', data.tool, 'Status:', data.status);
        } else if (data.type === 'output') {
          console.log('Output:', data.text);
        }
      }
    }
  }
};

// Usage
await sendMessage('What is the weather?');  // New session
await sendMessage('And tomorrow?', 'abc123');  // Continue session
```

**List Sessions:**

```javascript
// GET /api/chat/sessions?profile=default
fetch('/api/chat/sessions?profile=default', {
  headers: { 'Authorization': `Bearer ${sessionToken}` }
})
.then(res => res.json())
.then(data => {
  // data.sessions = [{ id: 'abc123', title: 'Weather discussion', timestamp: '2026-05-17...' }]
});
```

**Rename Session:**

```javascript
// PUT /api/chat/sessions/:sessionId
fetch('/api/chat/sessions/abc123', {
  method: 'PUT',
  headers: {
    'Content-Type': 'application/json',
    'Authorization': `Bearer ${sessionToken}`,
    'X-CSRF-Token': csrfToken
  },
  body: JSON.stringify({ title: 'Weather Research' })
});
```

### Token Analytics

**Get Usage Stats:**

```javascript
// GET /api/usage/stats?range=7d&profile=default
fetch('/api/usage/stats?range=7d&profile=default', {
  headers: { 'Authorization': `Bearer ${sessionToken}` }
})
.then(res => res.json())
.then(data => {
  console.log('Sessions:', data.totalSessions);
  console.log('Tokens:', data.totalTokens);
  console.log('Cost:', data.estimatedCost);
  console.log('Models:', data.modelBreakdown);
  // modelBreakdown: [{ model: 'hermes-3', sessions: 42, tokens: 150000, avgTokens: 3571 }]
  console.log('Platforms:', data.platformBreakdown);
  // platformBreakdown: [{ platform: 'CLI', count: 30 }, { platform: 'Telegram', count: 12 }]
  console.log('Top Tools:', data.topTools);
  // topTools: [{ tool: 'web_search', calls: 15, success_rate: 0.93 }]
});
```

**Query Ranges:** `today`, `7d`, `30d`, `90d`

### Configuration Management

**Get Config:**

```javascript
// GET /api/agents/config?profile=default
fetch('/api/agents/config?profile=default', {
  headers: { 'Authorization': `Bearer ${sessionToken}` }
})
.then(res => res.json())
.then(data => {
  console.log('Config YAML:', data.config);
  console.log('Categories:', data.categories);
  // categories: ['llm', 'platforms', 'memory', 'tools', 'prompts', ...]
});
```

**Update Config:**

```javascript
// PUT /api/agents/config
fetch('/api/agents/config', {
  method: 'PUT',
  headers: {
    'Content-Type': 'application/json',
    'Authorization': `Bearer ${sessionToken}`,
    'X-CSRF-Token': csrfToken
  },
  body: JSON.stringify({
    profile: 'default',
    config: `
llm:
  model: hermes-3
  provider: openrouter
  temperature: 0.7
platforms:
  telegram:
    enabled: true
    token: \${TELEGRAM_BOT_TOKEN}
memory:
  provider: honcho
  honcho_url: http://localhost:8000
`
  })
});
```

**Reset Category to Defaults:**

```javascript
// POST /api/agents/config/reset
fetch('/api/agents/config/reset', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'Authorization': `Bearer ${sessionToken}`,
    'X-CSRF-Token': csrfToken
  },
  body: JSON.stringify({
    profile: 'default',
    category: 'llm'
  })
});
```

### Cron Job Management

**List Cron Jobs:**

```javascript
// GET /api/cron?profile=default
fetch('/api/cron?profile=default', {
  headers: { 'Authorization': `Bearer ${sessionToken}` }
})
.then(res => res.json())
.then(data => {
  // data.jobs = [{ id: 'job1', schedule: '0 9 * * *', command: 'hermes chat "Daily summary"', enabled: true, nextRun: '...' }]
});
```

**Create Cron Job:**

```javascript
// POST /api/cron
fetch('/api/cron', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'Authorization': `Bearer ${sessionToken}`,
    'X-CSRF-Token': csrfToken
  },
  body: JSON.stringify({
    profile: 'default',
    schedule: '0 */6 * * *',  // Every 6 hours
    command: 'hermes chat "Check system health"',
    enabled: true
  })
});
```

**Run Job Immediately:**

```javascript
// POST /api/cron/:jobId/run
fetch('/api/cron/job1/run', {
  method: 'POST',
  headers: {
    'Authorization': `Bearer ${sessionToken}`,
    'X-CSRF-Token': csrfToken
  },
  body: JSON.stringify({ profile: 'default' })
});
```

### File Explorer

**List Directory:**

```javascript
// GET /api/files?path=~/.hermes
fetch('/api/files?path=~/.hermes', {
  headers: { 'Authorization': `Bearer ${sessionToken}` }
})
.then(res => res.json())
.then(data => {
  console.log('Files:', data.files);
  // files: [{ name: 'config.yaml', type: 'file', size: 1024 }, { name: 'sessions', type: 'directory' }]
});
```

**Read File:**

```javascript
// GET /api/files/read?path=~/.hermes/config.yaml
fetch('/api/files/read?path=~/.hermes/config.yaml', {
  headers: { 'Authorization': `Bearer ${sessionToken}` }
})
.then(res => res.json())
.then(data => {
  console.log('Content:', data.content);
});
```

**Write File:**

```javascript
// POST /api/files/write
fetch('/api/files/write', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'Authorization': `Bearer ${sessionToken}`,
    'X-CSRF-Token': csrfToken
  },
  body: JSON.stringify({
    path: '~/.hermes/custom-prompt.txt',
    content: 'You are a helpful assistant specializing in DevOps.'
  })
});
```

**Security Note:** All paths are validated and scoped to `HERMES_CONTROL_ROOTS` (default: `~/.hermes`). Path traversal attacks are prevented.

### Terminal (WebSocket)

**Connect to Terminal:**

```javascript
const ws = new WebSocket(`ws://${location.host}/terminal`);

ws.onopen = () => {
  console.log('Terminal connected');
  ws.send(JSON.stringify({ 
    type: 'auth', 
    token: sessionToken 
  }));
};

ws.onmessage = (event) => {
  const data = JSON.parse(event.data);
  
  if (data.type === 'output') {
    console.log('Output:', data.data);
  } else if (data.type === 'error') {
    console.error('Error:', data.message);
  }
};

// Send command
ws.send(JSON.stringify({
  type: 'input',
  data: 'hermes doctor\n'
}));

// Resize PTY
ws.send(JSON.stringify({
  type: 'resize',
  cols: 80,
  rows: 24
}));
```

**Rate Limiting:** 30 commands per minute per IP.

### System Maintenance

**Run Doctor (Diagnostics):**

```javascript
// POST /api/maintenance/doctor
fetch('/api/maintenance/doctor', {
  method: 'POST',
  headers: {
    'Authorization': `Bearer ${sessionToken}`,
    'X-CSRF-Token': csrfToken
  }
})
.then(res => res.json())
.then(data => {
  console.log('Issues found:', data.issues);
  console.log('Fixes applied:', data.fixes);
});
```

**Generate Debug Dump:**

```javascript
// GET /api/maintenance/dump
fetch('/api/maintenance/dump', {
  headers: { 'Authorization': `Bearer ${sessionToken}` }
})
.then(res => res.json())
.then(data => {
  console.log('System info:', data.system);
  console.log('Config:', data.config);
  console.log('Logs:', data.logs);
});
```

**Backup System:**

```javascript
// GET /api/maintenance/backup
// Returns a zip file download
window.location.href = '/api/maintenance/backup?token=' + sessionToken;
```

**Restart HCI Server:**

```javascript
// POST /api/maintenance/restart-hci
fetch('/api/maintenance/restart-hci', {
  method: 'POST',
  headers: {
    'Authorization': `Bearer ${sessionToken}`,
    'X-CSRF-Token': csrfToken
  }
});
// Server will restart in 2 seconds
```

## Common Patterns

### Programmatic Profile Switching

```javascript
class HermesProfileManager {
  constructor(baseUrl, token, csrfToken) {
    this.baseUrl = baseUrl;
    this.token = token;
    this.csrfToken = csrfToken;
  }

  async switchProfile(from, to) {
    // Stop current profile gateway
    await fetch(`${this.baseUrl}/api/agents/gateway/stop`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${this.token}`,
        'X-CSRF-Token': this.csrfToken
      },
      body: JSON.stringify({ profile: from })
    });

    // Start new profile gateway
    await fetch(`${this.baseUrl}/api/agents/gateway/start`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${this.token}`,
        'X-CSRF-Token': this.csrfToken
      },
      body: JSON.stringify({ profile: to })
    });

    console.log(`Switched from ${from} to ${to}`);
  }

  async createTestProfile(name, baseProfile = 'default') {
    // Clone base profile
    await fetch(`${this.baseUrl}/api/agents/profiles`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${this.token}`,
        'X-CSRF-Token': this.csrfToken
      },
      body: JSON.stringify({ name, cloneFrom: baseProfile })
    });

    // Update config for testing (lower temperature, etc.)
    const config = await fetch(`${this.baseUrl}/api/agents/config?profile=${name}`, {
      headers: { 'Authorization': `Bearer ${this.token}` }
    }).then(res => res.json());

    const modifiedConfig = config.config.replace(/temperature: \d\.\d+/, 'temperature: 0.3');

    await fetch(`${this.baseUrl}/api/agents/config`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${this.token}`,
        'X-CSRF-Token': this.csrfToken
      },
      body: JSON.stringify({ profile: name, config: modifiedConfig })
    });

    console.log(`Test profile ${name} created`);
  }
}

// Usage
const manager = new HermesProfileManager('http://localhost:10272', sessionToken, csrfToken);
await manager.createTestProfile('experiment-1');
await manager.switchProfile('default', 'experiment-1');
```

### Bulk Session Export

```javascript
async function exportAllSessions(profile) {
  const sessions = await fetch(`/api/chat/sessions?profile=${profile}`, {
    headers: { 'Authorization': `Bearer ${sessionToken}` }
  }).then(res => res.json());

  const exports = [];
  
  for (const session of sessions.sessions) {
    const data = await fetch(`/api/chat/sessions/${session.id}/export?profile=${profile}`, {
      headers: { 'Authorization': `Bearer ${sessionToken}` }
    }).then(res => res.json());
    
    exports.push({
      id: session.id,
      title: session.title,
      messages: data.messages
    });
  }

  // Save to file
  const blob = new Blob([JSON.stringify(exports, null, 2)], { type: 'application/json' });
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = `hermes-sessions-${profile}-${Date.now()}.json`;
  a.click();
}

// Usage
await exportAllSessions('production');
```

### Custom Token Usage Reporter

```javascript
class TokenUsageReporter {
  constructor(baseUrl, token) {
    this.baseUrl = baseUrl;
    this.token = token;
  }

  async generateReport(profile, range = '30d') {
    const stats = await fetch(
      `${this.baseUrl}/api/usage/stats?range=${range}&profile=${profile}`,
      { headers: { 'Authorization': `Bearer ${this.token}` } }
    ).then(res => res.json());

    const report = {
      period: range,
      profile: profile,
      summary: {
        totalSessions: stats.totalSessions,
        totalMessages: stats.totalMessages,
        totalTokens: stats.totalTokens,
        estimatedCost: stats.estimatedCost,
        avgTokensPerSession: Math.round(stats.totalTokens / stats.totalSessions)
      },
      topModels: stats.modelBreakdown.slice(0, 5),
      topTools: stats.topTools.slice(0, 10),
      platformDistribution: stats.platformBreakdown
    };

    console.table(report.topModels);
    console.table(report.topTools);
    
    return report;
  }

  async compareProfiles(profileA, profileB, range = '7d') {
    const [statsA, statsB] = await Promise.all([
      fetch(`${this.baseUrl}/api/usage/stats?range=${range}&profile=${profileA}`,
        { headers: { 'Authorization': `Bearer ${this.token}` } }).then(res => res.json()),
      fetch(`${this.baseUrl}/api/usage/stats?range=${range}&profile=${profileB}`,
        { headers: { 'Authorization': `Bearer ${this.token}` } }).then(res => res.json())
    ]);

    return {
      profileA: { name: profileA, cost: statsA.estimatedCost, tokens: statsA.totalTokens },
      profileB: { name: profileB, cost: statsB.estimatedCost, tokens: statsB.totalTokens },
      costDiff: statsA.estimatedCost - statsB.estimatedCost,
      tokenDiff: statsA.totalTokens - statsB.totalTokens
    };
  }
}

// Usage
const reporter = new TokenUsageReporter('http://localhost:10272', sessionToken);
const report = await reporter.generateReport('production', '30d');
console.log('Monthly cost:', report.summary.estimatedCost);

const comparison = await reporter.compareProfiles('production', 'staging', '7d');
console.log('Cost difference:', comparison.costDiff);
```

## Configuration Examples

### Multi-Platform Setup

**~/.hermes/profiles/production/config.yaml:**

```yaml
llm:
  model: hermes-3
  provider: openrouter
  api_key: ${OPENROUTER_API_KEY}
  temperature: 0.7
  max_tokens: 4000

platforms:
  telegram:
    enabled: true
    token: ${TELEGRAM_BOT_TOKEN}
  
  whatsapp:
    enabled: true
    account_sid: ${TWILIO_ACCOUNT_SID}
    auth_token: ${TWILIO_AUTH_TOKEN}
    from_number: ${TWILIO_PHONE_NUMBER}
  
  slack:
    enabled: true
    bot_token: ${SLACK_BOT_TOKEN}
    app_token: ${SLACK_APP_TOKEN}

memory:
  provider: honcho
  honcho_url: http://localhost:8000
  honcho_app_name: hermes-prod

tools:
  web_search:
    enabled: true
    provider: tavily
    api_key: ${TAVILY_API_KEY}
  
  code_execution:
    enabled: true
    sandbox: docker
    timeout: 30

prompts:
  system: |
    You are Hermes, a production AI assistant for the DevOps team.
    Focus on accuracy and provide detailed technical responses.
```

### Custom RBAC Setup

**Create a "Analyst" role (read-only + chat):**

```javascript
// Via Maintenance → Users UI or API
const analystPermissions = [
  'agents:read',
  'chat:read',
  'chat:write',
  'sessions:read',
  'config:read',
  'gateway:logs'
];

await fetch('/api/users', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'Authorization': `Bearer ${adminToken}`,
    'X-CSRF-Token': csrfToken
  },
  body: JSON.stringify({
    username: 'analyst1',
    password: 'secure-password',
    role: 'custom',
    permissions: analystPermissions
  })
});
```

### Scheduled Maintenance Cron

```javascript
// Daily health check at 3 AM
await fetch('/api/cron', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'Authorization': `Bearer ${sessionToken}`,
    'X-CSRF-Token': csrfToken
  },
  body: JSON.stringify({
    profile: 'default',
    schedule: '0 3 * * *',
    command: 'hermes doctor --auto-fix && hermes chat "Daily system report"',
    enabled: true
  })
});

// Weekly backup every Sunday at 2 AM
await fetch('/api/cron', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'Authorization': `Bearer ${sessionToken}`,
    'X-CSRF-Token': csrfToken
  },
  body: JSON.stringify({
    profile: 'default',
    schedule: '0 2 * * 0',
    command: 'cd ~/.hermes && tar -czf backup-$(date +%Y%m%d).tar.gz .',
    enabled: true
  })
});
```

## Troubleshooting

### Gateway Won't Start

**Symptom:** "Failed to start gateway" error

**Solutions:**

```bash
# 1. Check if port is already in use
sudo lsof -i :8000  # Default gateway port

# 2. View gateway logs
journalctl -u hermes-gateway-default -n 50

# 3. Check systemd service status
systemctl status hermes-gateway-default

# 4. Manually test gateway
hermes gateway start --profile default --debug

# 5. Check config.yaml syntax
hermes config validate --profile default
```

### WebSocket Connection Fails

**Symptom:** Terminal or chat streaming doesn't work

**Solutions:**

```javascript
// 1. Check WebSocket origin in server.js
// Ensure your domain is allowed in WebSocket verification

// 2. If behind reverse proxy, configure headers:
// Nginx example:
/*
location /terminal {
    proxy_pass http://localhost:10272;
    proxy_http_version 1.1;
    proxy_set_header Upgrade $http_upgrade;
    proxy_set_header Connection "upgrade";
    proxy_set_header Host $host;
}
*/

// 3. Check browser console for CORS errors
// Update .env if needed:
// HERMES_CONTROL_CORS_ORIGIN=https://yourdomain.com
```

### Session Not Resuming

**Symptom:** `--continue <session-id>` creates new session instead

**Solutions:**

```bash
# 1. Verify session exists
ls -la ~/.hermes/sessions/

# 2. Check session ID format
# New format: abc123
# Legacy format: Session_abc123

# 3. Test CLI directly
hermes chat --continue abc123 "test message"

# 4. Check session file permissions
chmod 644 ~/.hermes/sessions/abc123.json

# 5. Review chat logs in HCI
# Navigate to Agents → [Profile] → Sessions tab
```

### Token Analytics Not Showing

**Symptom:** Usage page shows zero data

**Solutions:**

```bash
# 1. Verify session log files exist
ls -la ~/.hermes/sessions/*.json

# 2. Check token tracking is enabled in config
cat ~/.hermes/profiles/default/config.yaml | grep -A5 analytics

# 3. Manually trigger analytics rebuild
hermes analytics rebuild

# 4. Check for parsing errors in logs
tail -f ~/.hermes/hci.log | grep analytics
```

### Permission Denied Errors

**Symptom:** "Permission denied" when accessing files/terminals

**Solutions:**

```bash
# 1. Check user permissions on ~/.hermes
ls -ld ~/.hermes
chmod 755 ~/.hermes

# 2. If running as non-root, ensure RBAC role allows action
# Check Maintenance → Users → [Your User] → Permissions

# 3. For terminal: verify user has shell access
echo $SHELL

# 4. For files: check HERMES_CONTROL_ROOTS in .env
# Default: ~/.hermes (user must have read/write access)
```

### High Memory Usage

**Symptom:** HCI process consuming excessive RAM

**Solutions:**

```bash
# 1. Check active WebSocket connections
# Navigate to browser DevTools → Network → WS tab

# 2. Restart HCI to clear stale connections
systemctl restart hermes-control
# OR via UI: Maintenance → HCI Restart

# 3. Limit concurrent sessions
# Edit server.js to add connection limits if needed

# 4. Check for memory leaks in logs
node --expose-gc server.js
```

### CSRF Token Mismatch

**Symptom:** "Invalid CSRF token" on form submissions

**Solutions:**

```javascript
// 1. Ensure CSRF token is included in request headers
const csrfToken = document.querySelector('meta[name="csrf-token"]').content;

fetch('/api/agents/profiles', {
  method: 'POST',
  headers: {
    'X-CSRF-Token': csrfToken,
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({ name: 'test' })
});

// 2. Check session hasn't expired
// Default: 24 hour session timeout

// 3. Clear cookies and re-login
document.cookie.split(";").forEach(c => {
  document.cookie = c.replace(/^ +/, "").replace(/=.*/, "=;expires=" + new Date().toUTCString() + ";path=/");
});
```

### Gateway Logs Not Streaming

**Symptom:** Gateway log viewer shows "Connecting..." indefinitely

**Solutions:**

```bash
# 1. Verify gateway is actually running
systemctl status hermes-gateway-default

# 2. Check systemd journal accessibility
sudo journalctl -u hermes-gateway-default --no-pager -n 10

# 3. Grant user access to systemd journal (if non-root)
sudo user
