---
name: dashboard
description: MILO Dashboard - Real-time monitoring for Ralph Loop sessions. Shows memory usage, costs, conversation history, and session status.
allowed-tools: Read, Bash, WebFetch
---

# MILO Dashboard

Real-time monitoring dashboard for Ralph Loop autonomous AI sessions.

## Command Syntax

```bash
/dashboard              # Start the dashboard (if not running)
/dashboard start        # Start the dashboard server
/dashboard stop         # Stop the dashboard server
/dashboard status       # Check if dashboard is running
/dashboard restart      # Restart the dashboard server
/dashboard logs         # View recent server logs
/dashboard open         # Open dashboard in browser
```

## Dashboard Location

```
Directory: /Users/eddiebelaval/clawd/skills/ralph-loops/dashboard
URL: http://localhost:3939
```

## Starting the Dashboard

### Development Mode (hot reload)
```bash
cd /Users/eddiebelaval/clawd/skills/ralph-loops/dashboard
npm run dev
```

### Production Mode
```bash
cd /Users/eddiebelaval/clawd/skills/ralph-loops/dashboard
npm start
```

### With PM2 (recommended for production)
```bash
cd /Users/eddiebelaval/clawd/skills/ralph-loops/dashboard
pm2 start ecosystem.config.cjs
pm2 status milo-dashboard
pm2 logs milo-dashboard
```

## API Endpoints

| Endpoint | Description |
|----------|-------------|
| `GET /health` | Health check with memory stats |
| `GET /api/health` | Same as /health |
| `GET /api/system/memory` | Current memory usage |
| `GET /api/system/predictions` | Memory predictions |
| `GET /api/loops` | List all active loops |
| `GET /api/loops/:id` | Single loop details |
| `GET /api/loops/:id/history` | Loop iteration history |
| `POST /api/loops/:id/kill` | Kill a session |
| `GET /api/analytics/costs` | Cost breakdown |
| `GET /api/memories` | List memories |
| `GET /api/memories/search` | Search memories |
| `GET /api/episodes` | List episodes |
| `GET /api/activity` | Activity timeline |
| `GET /api/conversations` | Conversation history |
| `GET /api/schedule` | Scheduled tasks |
| `WS /ws/updates` | Real-time WebSocket |

## Quick Actions

### Check if Running
```bash
lsof -i :3939
```

### Kill Process on Port
```bash
kill $(lsof -t -i:3939)
```

### View Logs
```bash
tail -f /Users/eddiebelaval/clawd/skills/ralph-loops/dashboard/logs/out.log
```

## Features

- **3-column layout**: Conversation | Visualization | Sidebar
- **Tab navigation**: Files, Graph, Costs, Cascade
- **Real-time updates**: WebSocket connection
- **Memory visualization**: Particle canvas with clustering
- **Session monitoring**: Active loops, costs, activity timeline

## Design System

Uses id8labs color palette with Factory.ai aesthetic:
- Coral accent (#FF6B5B)
- Dark backgrounds (#0A0A0A)
- Clean, minimal design with pipe separators
- Status dots for session state

## Hardening

- Error Boundary prevents white screen crashes
- Graceful shutdown handler (SIGTERM/SIGINT)
- Health check endpoints for monitoring
- PM2 auto-restart on crashes
- Memory limit: 500MB

---

*MILO Dashboard v3.0 - id8Labs*
