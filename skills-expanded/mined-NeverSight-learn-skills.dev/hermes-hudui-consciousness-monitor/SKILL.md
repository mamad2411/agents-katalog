---
name: hermes-hudui-consciousness-monitor
description: Expert in deploying and using Hermes HUD Web UI for monitoring AI agent memory, sessions, costs, and health
triggers:
  - how do i set up hermes hud web ui
  - monitor my hermes agent with the web dashboard
  - view hermes agent memory and sessions in browser
  - export hermes replay artifacts
  - configure hermes hudui themes and shortcuts
  - check hermes agent health and costs
  - manage hermes gateway tools and plugins
  - troubleshoot hermes hudui installation
---

# Hermes HUD Web UI Skill

> Skill by [ara.so](https://ara.so) — Hermes Skills collection.

## Overview

Hermes HUD Web UI is a browser-based consciousness monitor for [Hermes](https://github.com/nousresearch/hermes-agent), the AI agent with persistent memory. It provides 18 tabs covering executive dashboard, identity, memory, skills, sessions, health diagnostics, costs, model analytics, gateway control, plugin management, and live chat. The UI updates in real-time via WebSocket and reads from the same `~/.hermes/` data directory as the Hermes agent.

**Key Features:**
- Real-time monitoring of agent memory, sessions, and health
- Cost and token analytics per model
- Gateway managed-tool visibility (web search, image generation, TTS, browser automation)
- Hermes Replay: export shareable, redacted session artifacts
- 5 themes, keyboard shortcuts, command palette
- Bilingual: English and Chinese
- Companion to the TUI version; both can run simultaneously

## Installation

### Requirements
- Python 3.11+
- Node.js 18+
- A running Hermes agent with data in `~/.hermes/`

### Quick Start

```bash
git clone https://github.com/joeynyc/hermes-hudui.git
cd hermes-hudui
./install.sh
hermes-hudui
```

The installer creates a Python virtual environment, installs dependencies, and builds the frontend. Open http://localhost:3001 after launch.

### Manual Installation

```bash
# Clone repository
git clone https://github.com/joeynyc/hermes-hudui.git
cd hermes-hudui

# Create virtual environment
python3.11 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install Python dependencies
pip install -e .

# Install Node dependencies and build frontend
cd frontend
npm install
npm run build
cd ..

# Launch
hermes-hudui
```

### Future Runs

```bash
cd hermes-hudui
source venv/bin/activate && hermes-hudui
```

### Optional TUI Integration

If you also want the TUI version available:

```bash
# In zsh (quotes required)
pip install 'hermes-hudui[tui]'

# In bash/fish (quotes optional but safe)
pip install 'hermes-hudui[tui]'
```

## Configuration

### Environment Variables

```bash
# Custom port (default: 3001)
export HERMES_HUD_PORT=8080

# Custom Hermes data directory (default: ~/.hermes/)
export HERMES_DATA_DIR=/path/to/custom/hermes/data

# WebSocket host (default: localhost)
export HERMES_WS_HOST=0.0.0.0
```

### Data Directory Structure

Hermes HUD reads from `~/.hermes/`:

```
~/.hermes/
├── identity.json          # Agent identity and configuration
├── memory/                # Persistent memory store
├── sessions/              # Session logs and history
├── skills/                # Installed skills
├── cron/                  # Scheduled jobs
├── projects/              # Project tracking
├── health/                # Health metrics
└── costs/                 # Usage and cost tracking
```

### Replay Export Directory

Exported replay artifacts are written to:

```
~/.hermes-hud/replays/
├── session_abc123/
│   ├── replay.redacted.json
│   ├── replay.md
│   ├── replay.html
│   ├── share-card.png
│   └── fork.json
```

## Key Commands

### CLI

```bash
# Start the web UI
hermes-hudui

# Start on custom port
HERMES_HUD_PORT=8080 hermes-hudui

# Point to custom Hermes data directory
HERMES_DATA_DIR=/custom/path hermes-hudui
```

### Keyboard Shortcuts (In Browser)

| Key | Action |
|-----|--------|
| `1`–`9`, `0` | Switch between tabs 1-10 |
| `t` | Open theme picker |
| `Ctrl+K` | Open command palette |

### Themes

Five built-in themes (toggle with `t`):
1. **Neural Awakening** (cyan) — default
2. **Hermes Teal** (official Nous palette)
3. **Blade Runner** (amber)
4. **fsociety** (green)
5. **Anime** (purple)

Optional CRT scanlines available in theme settings.

### Language Toggle

Click the language icon in the top-right header to switch between English and Chinese. Persists to localStorage. When Chinese is selected, chat responses from your agent also come back in Chinese.

## Core Functionality

### Accessing the Dashboard

After starting `hermes-hudui`, navigate to http://localhost:3001 in your browser. The executive dashboard loads first, showing:

- Agent health status
- Spend pulse (recent costs)
- Top model by usage
- Provider/gateway risk
- Highest-cost session
- Action items

### Real-Time Updates

The UI uses WebSocket for live updates. Health reacts to filesystem changes in `~/.hermes/` and WebSocket messages. Expensive refresh paths (e.g., full memory scans) are throttled.

### Gateway Managed Tools

The **Gateway** tab shows routing for:
- Web search
- Image generation
- Text-to-speech
- Browser automation

Each tool displays one of three states:
- **Gateway**: routed through Nous Tool Gateway
- **Direct Key**: using your own API key
- **Unavailable**: not configured

### Plugin Hub

The **Plugins** tab shows:
- Installed dashboard and agent plugins
- Extension entry points
- Runtime status
- Required auth commands
- Enable/disable/update actions (two-click safety)

### Hermes Replay

**Purpose:** Turn agent runs into redacted, shareable proof artifacts.

**Workflow:**
1. Open the **Replay** tab
2. Select a Hermes session from the list
3. Inspect the normalized timeline
4. Review the run receipt
5. Export artifacts (local files, no upload by default)

**Export Formats:**
- Redacted JSON (`replay.redacted.json`)
- GitHub-ready Markdown (`replay.md`)
- Standalone HTML (`replay.html`)
- PNG share card 1200×630 (`share-card.png`)
- Fork-safe metadata (`fork.json`)

**Safe Share Mode (default):**
- Redacts raw tool arguments
- Strips terminal output
- Removes assistant reasoning
- Masks tokens, emails, local paths
- Includes local hashes and Ed25519 signatures for integrity

Example redacted payload: `assets/example-replay.redacted.json`

## Code Examples

### Python: Extending the Backend

Add a custom WebSocket event handler:

```python
# server/handlers/custom_handler.py
from server.websocket import send_message

async def handle_custom_event(websocket, data):
    """
    Custom event handler for new dashboard features.
    """
    event_type = data.get("type")
    
    if event_type == "request_custom_metric":
        metric_data = compute_custom_metric()
        await send_message(websocket, {
            "type": "custom_metric",
            "payload": metric_data
        })

def compute_custom_metric():
    # Read from ~/.hermes/ or compute live data
    return {
        "metric_name": "agent_velocity",
        "value": 42,
        "timestamp": "2026-05-16T18:00:00Z"
    }
```

Register the handler in `server/websocket.py`:

```python
from server.handlers.custom_handler import handle_custom_event

async def handle_message(websocket, message):
    data = json.loads(message)
    
    if data["type"] == "request_custom_metric":
        await handle_custom_event(websocket, data)
    # ... existing handlers
```

### Python: Reading Hermes Data

Access agent identity and memory:

```python
import json
from pathlib import Path

def load_hermes_identity():
    """Load agent identity from ~/.hermes/identity.json"""
    hermes_dir = Path.home() / ".hermes"
    identity_path = hermes_dir / "identity.json"
    
    if identity_path.exists():
        with open(identity_path, "r") as f:
            return json.load(f)
    return None

def get_recent_sessions(limit=10):
    """Get most recent session logs"""
    sessions_dir = Path.home() / ".hermes" / "sessions"
    
    if not sessions_dir.exists():
        return []
    
    session_files = sorted(
        sessions_dir.glob("*.json"),
        key=lambda p: p.stat().st_mtime,
        reverse=True
    )
    
    sessions = []
    for session_file in session_files[:limit]:
        with open(session_file, "r") as f:
            sessions.append(json.load(f))
    
    return sessions
```

### JavaScript: Custom Dashboard Widget

Add a new chart to the frontend:

```javascript
// frontend/src/components/CustomMetricWidget.jsx
import React, { useEffect, useState } from 'react';
import { useWebSocket } from '../hooks/useWebSocket';

export function CustomMetricWidget() {
  const [metricData, setMetricData] = useState(null);
  const { sendMessage, onMessage } = useWebSocket();

  useEffect(() => {
    // Request custom metric from backend
    sendMessage({ type: 'request_custom_metric' });

    // Listen for response
    const unsubscribe = onMessage((data) => {
      if (data.type === 'custom_metric') {
        setMetricData(data.payload);
      }
    });

    return unsubscribe;
  }, []);

  if (!metricData) return <div>Loading...</div>;

  return (
    <div className="metric-widget">
      <h3>{metricData.metric_name}</h3>
      <div className="metric-value">{metricData.value}</div>
      <div className="metric-timestamp">{metricData.timestamp}</div>
    </div>
  );
}
```

### Python: Replay Export Customization

Create a custom replay exporter:

```python
# server/replay/custom_exporter.py
import json
from pathlib import Path
from datetime import datetime

class CustomReplayExporter:
    def __init__(self, session_id, replay_data):
        self.session_id = session_id
        self.replay_data = replay_data
        self.output_dir = Path.home() / ".hermes-hud" / "replays" / session_id
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def export_json(self):
        """Export custom JSON format"""
        output_path = self.output_dir / "custom-export.json"
        
        custom_format = {
            "version": "1.0",
            "session_id": self.session_id,
            "exported_at": datetime.utcnow().isoformat(),
            "timeline": self.replay_data.get("timeline", []),
            "metadata": self.replay_data.get("metadata", {})
        }
        
        with open(output_path, "w") as f:
            json.dump(custom_format, f, indent=2)
        
        return output_path
    
    def export_csv(self):
        """Export timeline as CSV"""
        import csv
        
        output_path = self.output_dir / "timeline.csv"
        timeline = self.replay_data.get("timeline", [])
        
        if not timeline:
            return None
        
        with open(output_path, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=timeline[0].keys())
            writer.writeheader()
            writer.writerows(timeline)
        
        return output_path
```

## Common Patterns

### Monitoring Agent Health

```python
from pathlib import Path
import json

def check_agent_health():
    """Check Hermes agent health status"""
    health_file = Path.home() / ".hermes" / "health" / "status.json"
    
    if not health_file.exists():
        return {"status": "unknown", "message": "Health file not found"}
    
    with open(health_file, "r") as f:
        health_data = json.load(f)
    
    return {
        "status": health_data.get("status"),
        "last_check": health_data.get("timestamp"),
        "issues": health_data.get("issues", [])
    }
```

### Accessing Cost Analytics

```python
def get_cost_summary(model_name=None):
    """Get cost analytics, optionally filtered by model"""
    costs_dir = Path.home() / ".hermes" / "costs"
    
    if not costs_dir.exists():
        return {"total": 0, "by_model": {}}
    
    total_cost = 0
    by_model = {}
    
    for cost_file in costs_dir.glob("*.json"):
        with open(cost_file, "r") as f:
            data = json.load(f)
            model = data.get("model")
            cost = data.get("cost", 0)
            
            if model_name and model != model_name:
                continue
            
            total_cost += cost
            by_model[model] = by_model.get(model, 0) + cost
    
    return {
        "total": total_cost,
        "by_model": by_model
    }
```

### WebSocket Real-Time Updates

```javascript
// frontend/src/hooks/useAgentHealth.js
import { useEffect, useState } from 'react';
import { useWebSocket } from './useWebSocket';

export function useAgentHealth() {
  const [health, setHealth] = useState(null);
  const { sendMessage, onMessage } = useWebSocket();

  useEffect(() => {
    // Request initial health status
    sendMessage({ type: 'request_health' });

    // Subscribe to health updates
    const unsubscribe = onMessage((data) => {
      if (data.type === 'health_update') {
        setHealth(data.payload);
      }
    });

    // Refresh every 30 seconds
    const interval = setInterval(() => {
      sendMessage({ type: 'request_health' });
    }, 30000);

    return () => {
      unsubscribe();
      clearInterval(interval);
    };
  }, []);

  return health;
}
```

## Troubleshooting

### Port Already in Use

```bash
# Error: Address already in use
# Solution: Use a different port
HERMES_HUD_PORT=8080 hermes-hudui
```

### WebSocket Connection Failed

**Symptom:** Dashboard loads but shows "disconnected" status, no real-time updates.

**Causes:**
- Backend not running
- Firewall blocking WebSocket
- Port mismatch between frontend and backend

**Solution:**
```bash
# Verify backend is running
ps aux | grep hermes-hudui

# Check logs for WebSocket errors
tail -f ~/.hermes-hud/logs/server.log

# Ensure frontend points to correct WebSocket URL
# Check frontend/.env or frontend/src/config.js
```

### Missing Hermes Data Directory

**Symptom:** Dashboard shows "No data found" or empty tabs.

**Cause:** Hermes agent hasn't run yet or data is in non-standard location.

**Solution:**
```bash
# Verify Hermes data exists
ls -la ~/.hermes/

# If data is elsewhere, set environment variable
HERMES_DATA_DIR=/path/to/hermes/data hermes-hudui
```

### Replay Export Fails

**Symptom:** Export button doesn't create files or throws permission error.

**Cause:** Insufficient permissions on `~/.hermes-hud/replays/` directory.

**Solution:**
```bash
# Create directory with correct permissions
mkdir -p ~/.hermes-hud/replays
chmod 755 ~/.hermes-hud/replays

# Check disk space
df -h ~
```

### Frontend Build Errors

**Symptom:** `./install.sh` fails during `npm run build`.

**Cause:** Node.js version < 18 or missing dependencies.

**Solution:**
```bash
# Check Node.js version
node --version  # Should be 18+

# Update Node.js (via nvm)
nvm install 18
nvm use 18

# Clean install
cd frontend
rm -rf node_modules package-lock.json
npm install
npm run build
```

### Theme Not Persisting

**Symptom:** Theme resets to default on page reload.

**Cause:** localStorage disabled or browser privacy mode.

**Solution:**
- Disable private/incognito mode
- Check browser console for localStorage errors
- Verify site isn't blocked in browser settings

### Gateway Tools Show "Unavailable"

**Symptom:** All gateway-managed tools show unavailable status.

**Cause:** Hermes agent not configured with gateway credentials or direct API keys.

**Solution:**
```bash
# Configure Nous Tool Gateway (if using gateway)
# In Hermes agent config (~/.hermes/config.json):
{
  "gateway": {
    "enabled": true,
    "api_key": "${NOUS_GATEWAY_API_KEY}"
  }
}

# Or configure direct API keys
{
  "providers": {
    "openai": {
      "api_key": "${OPENAI_API_KEY}"
    },
    "anthropic": {
      "api_key": "${ANTHROPIC_API_KEY}"
    }
  }
}

# Restart Hermes agent and HUD
```

## Platform Support

- **macOS**: Full support
- **Linux**: Full support
- **Windows**: Use WSL (Windows Subsystem for Linux)

## Related Resources

- [Hermes Agent](https://github.com/nousresearch/hermes-agent) — The AI agent Hermes HUD monitors
- [Hermes HUD TUI](https://github.com/joeynyc/hermes-hud) — Terminal UI companion
- [Example Redacted Replay](assets/example-replay.redacted.json) — Sample export artifact
