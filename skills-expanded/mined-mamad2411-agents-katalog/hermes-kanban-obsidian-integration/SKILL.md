---
name: hermes-kanban-obsidian-integration
description: Turn Hermes into an autonomous project executor using Kanban boards inside Obsidian vault with visual rendering and REST API control
triggers:
  - "create a kanban board in obsidian"
  - "set up hermes kanban bridge"
  - "break down project into kanban board"
  - "run daily standup on kanban"
  - "move kanban card to in progress"
  - "query kanban board state"
  - "setup obsidian project tracking"
  - "integrate hermes with obsidian kanban"
---

# Hermes Kanban Obsidian Integration

> Skill by [ara.so](https://ara.so) — Hermes Skills collection.

## Overview

Hermes Kanban Bridge is an Obsidian plugin that exposes a REST API (default port 27124) allowing Hermes agents to manage Kanban boards inside your Obsidian vault. Boards are stored as Markdown files with YAML frontmatter, rendered visually by the obsidian-kanban community plugin.

**Architecture:**
- Hermes Agent → HTTP REST API → hermes-kanban-bridge plugin → Obsidian Vault API → Markdown files → obsidian-kanban visual renderer

**Key Features:**
- Break goals into structured Kanban boards via API
- Move cards, update metadata, query state in real-time
- Daily standups and weekly review rituals
- Fully local, no cloud dependencies
- Visual board rendering in Obsidian

## Installation

### Automated Install (Recommended)

```bash
# Clone the repository
git clone https://github.com/GumbyEnder/hermes-kanban.git
cd hermes-kanban

# Edit install script to set your vault path
export VAULT_PATH="/path/to/your/ObsidianVault"

# Run automated installer
bash hermes-kanban-install.sh
```

The script installs:
1. hermes-kanban-bridge plugin (REST API server)
2. obsidian-kanban plugin (visual renderer)
3. Registers both in vault's community-plugins.json

### Manual Installation

**Build the plugin:**
```bash
cd plugin
npm install
npm run build
```

**Copy to vault:**
```bash
VAULT="/path/to/your/vault"
mkdir -p "$VAULT/.obsidian/plugins/hermes-kanban-bridge"
cp main.js manifest.json "$VAULT/.obsidian/plugins/hermes-kanban-bridge/"
```

**Install obsidian-kanban renderer:**
```bash
KANBAN_DIR="$VAULT/.obsidian/plugins/obsidian-kanban"
mkdir -p "$KANBAN_DIR"
TAG="2.0.51"
for f in main.js manifest.json styles.css; do
  curl -sL "https://github.com/obsidian-community/obsidian-kanban/releases/download/$TAG/$f" -o "$KANBAN_DIR/$f"
done
```

**Enable plugins in Obsidian:**
1. Reload Obsidian
2. Settings → Community Plugins → disable Safe Mode
3. Enable "Hermes Kanban Bridge" and "Kanban"
4. Verify notice: "Hermes Kanban Bridge started on port 27124"

**Install Hermes skills:**
```bash
mkdir -p ~/.hermes/profiles/$HERMES_PROFILE/skills/productivity
cp skills/*.md ~/.hermes/profiles/$HERMES_PROFILE/skills/productivity/
```

## Configuration

**Plugin Settings** (Obsidian → Settings → Hermes Kanban Bridge):

| Setting | Default | Description |
|---------|---------|-------------|
| Port | 27124 | Local REST API port |
| Board folder | Kanban | Vault folder for boards |
| Trust mode | confirm | `confirm` = approval modal, `auto` = silent |
| Enable server | on | Toggle REST API |

**Network Configuration for Remote Access:**

If Hermes runs on a different machine, use Tailscale/LAN IP instead of localhost.

Windows firewall rule:
```powershell
netsh advfirewall firewall add rule name="Hermes Kanban Bridge" dir=in action=allow protocol=TCP localport=27124
```

Verify listening on all interfaces:
```powershell
netstat -ano | findstr 27124
# Should show: TCP  0.0.0.0:27124  LISTENING
```

## REST API Reference

**Base URL:** `http://localhost:27124` (or remote IP)

### Health Check

```bash
curl http://localhost:27124/health
# {"ok":true,"status":"running","port":27124,"version":"1.0.0"}
```

### Create Board

```bash
curl -X POST http://localhost:27124/boards \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Q3 Launch",
    "columns": ["Backlog", "In Progress", "Review", "Done"]
  }'
# {"success":true,"board_id":"Q3-Launch","path":"Kanban/Q3-Launch.md"}
```

### Add Card

```bash
curl -X POST http://localhost:27124/boards/Q3-Launch/cards \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Design landing page",
    "column": "Backlog",
    "metadata": {
      "priority": "high",
      "assignee": "alice"
    }
  }'
# {"success":true,"card_id":"card-001"}
```

### Move Card

```bash
curl -X PATCH http://localhost:27124/boards/Q3-Launch/cards/card-001 \
  -H "Content-Type: application/json" \
  -d '{
    "column": "In Progress"
  }'
# {"success":true}
```

### Query Board State

```bash
# Get all cards
curl http://localhost:27124/boards/Q3-Launch/cards
# {"cards":[{"id":"card-001","title":"Design landing page","column":"In Progress",...}]}

# Filter by column
curl http://localhost:27124/boards/Q3-Launch/cards?column=Backlog

# Filter by metadata
curl http://localhost:27124/boards/Q3-Launch/cards?assignee=alice
```

### Daily Standup

```bash
curl -X POST http://localhost:27124/rituals/standup \
  -H "Content-Type: application/json" \
  -d '{
    "board_id": "Q3-Launch"
  }'
# {"summary":"3 cards in progress, 2 blocked, 5 completed yesterday"}
```

### Weekly Review

```bash
curl -X POST http://localhost:27124/rituals/weekly-review \
  -H "Content-Type: application/json" \
  -d '{
    "board_id": "Q3-Launch"
  }'
# {"summary":"12 cards completed this week, velocity: 2.4 cards/day"}
```

## Python Client Usage

```python
import requests
import os

BASE_URL = os.getenv("HERMES_KANBAN_URL", "http://localhost:27124")

class KanbanClient:
    def __init__(self, base_url=BASE_URL):
        self.base = base_url
    
    def health_check(self):
        """Verify server is running"""
        r = requests.get(f"{self.base}/health")
        return r.json()
    
    def create_board(self, name, columns):
        """Create new Kanban board"""
        r = requests.post(
            f"{self.base}/boards",
            json={"name": name, "columns": columns}
        )
        return r.json()
    
    def add_card(self, board_id, title, column, metadata=None):
        """Add card to board"""
        payload = {"title": title, "column": column}
        if metadata:
            payload["metadata"] = metadata
        r = requests.post(
            f"{self.base}/boards/{board_id}/cards",
            json=payload
        )
        return r.json()
    
    def move_card(self, board_id, card_id, new_column):
        """Move card between columns"""
        r = requests.patch(
            f"{self.base}/boards/{board_id}/cards/{card_id}",
            json={"column": new_column}
        )
        return r.json()
    
    def query_cards(self, board_id, filters=None):
        """Query cards with optional filters"""
        params = filters or {}
        r = requests.get(
            f"{self.base}/boards/{board_id}/cards",
            params=params
        )
        return r.json()
    
    def daily_standup(self, board_id):
        """Run daily standup ritual"""
        r = requests.post(
            f"{self.base}/rituals/standup",
            json={"board_id": board_id}
        )
        return r.json()

# Example usage
client = KanbanClient()

# Verify connection
print(client.health_check())

# Create board
board = client.create_board(
    name="Product Roadmap",
    columns=["Ideas", "Planned", "In Development", "Shipped"]
)
board_id = board["board_id"]

# Add cards
client.add_card(
    board_id,
    "Implement dark mode",
    "Planned",
    metadata={"priority": "medium", "estimate": "3d"}
)

# Query blocked items
blocked = client.query_cards(board_id, {"status": "blocked"})
print(f"Blocked cards: {len(blocked['cards'])}")

# Run standup
standup = client.daily_standup(board_id)
print(standup["summary"])
```

## Board Markdown Format

Boards are stored as Markdown with YAML frontmatter:

```markdown
---
kanban-plugin: board
---

## Backlog

- [ ] Design landing page #high @alice
- [ ] Set up CI/CD pipeline #medium @bob

## In Progress

- [ ] Implement authentication #high @alice
  - Started: 2026-05-15
  - Blocked: waiting on API keys

## Review

- [ ] Write user documentation #low @carol

## Done

- [x] Initialize project repository
  - Completed: 2026-05-14
```

**Important:** The `kanban-plugin: board` frontmatter triggers visual rendering. Without it, boards display as plain Markdown.

## Common Patterns

### Breaking Down a Project

```python
def break_down_project(client, project_name, tasks):
    """Create board and populate with tasks"""
    board = client.create_board(
        name=project_name,
        columns=["Backlog", "In Progress", "Review", "Done"]
    )
    board_id = board["board_id"]
    
    for task in tasks:
        client.add_card(
            board_id,
            task["title"],
            "Backlog",
            metadata=task.get("metadata", {})
        )
    
    return board_id

# Usage
tasks = [
    {"title": "Research competitors", "metadata": {"priority": "high"}},
    {"title": "Draft wireframes", "metadata": {"priority": "medium"}},
    {"title": "Set up analytics", "metadata": {"priority": "low"}}
]

board_id = break_down_project(client, "Market Analysis", tasks)
```

### Automated Workflow Progression

```python
def progress_workflow(client, board_id):
    """Move cards through workflow automatically"""
    # Get all cards in Review
    cards = client.query_cards(board_id, {"column": "Review"})
    
    for card in cards["cards"]:
        # Check if ready to move (example: all subtasks done)
        if card_is_complete(card):
            client.move_card(board_id, card["id"], "Done")
            print(f"Completed: {card['title']}")

def card_is_complete(card):
    """Example validation logic"""
    metadata = card.get("metadata", {})
    return metadata.get("reviewed", False) and metadata.get("tests_passing", False)
```

### Daily Ritual Integration

```python
import schedule
import time

def daily_standup_job():
    """Run standup for all active boards"""
    client = KanbanClient()
    
    # Get all boards
    boards = requests.get(f"{client.base}/boards").json()
    
    for board in boards["boards"]:
        if board.get("active", True):
            result = client.daily_standup(board["id"])
            send_notification(result["summary"])

# Schedule daily at 9 AM
schedule.every().day.at("09:00").do(daily_standup_job)

while True:
    schedule.run_pending()
    time.sleep(60)
```

## Testing

The project includes 105 tests (59 unit, 46 E2E):

```bash
# All tests
pytest tests/

# E2E only
pytest tests/e2e/

# Skip slow TUI tests
pytest tests/e2e/ -k "not tui"

# Mock API server (no Obsidian required)
python tests/e2e/mock_api_server.py
```

**Mock API for development:**
```python
# tests/e2e/mock_api_server.py implements all REST endpoints
# Use for testing without running Obsidian

import requests
# Start mock server on port 27125
response = requests.get("http://localhost:27125/health")
assert response.json()["ok"] == True
```

## Troubleshooting

### Connection Refused

**Symptoms:** `curl: Failed to connect to localhost port 27124`

**Solutions:**
1. Verify plugin is enabled: Settings → Community Plugins → Hermes Kanban Bridge = ON
2. Look for notice "Hermes Kanban Bridge started on port 27124"
3. Toggle plugin off/on to restart server
4. Check port not in use: `lsof -i :27124` (Unix) or `netstat -ano | findstr 27124` (Windows)

### Board Shows as Markdown List

**Symptoms:** Board opens as plain text instead of visual kanban

**Solution:** Add YAML frontmatter to top of file:
```markdown
---
kanban-plugin: board
---
```

All API-created boards include this automatically. Manually created boards need it added.

### Remote Access Not Working

**Symptoms:** Can't connect from Hermes on different machine

**Solutions:**
1. Use Obsidian machine's Tailscale/LAN IP instead of `localhost`
2. Verify server binds to `0.0.0.0` not `127.0.0.1`:
   ```bash
   netstat -ano | findstr 27124
   # Should show: TCP  0.0.0.0:27124  LISTENING
   ```
3. Add firewall rule (Windows):
   ```powershell
   netsh advfirewall firewall add rule name="Hermes Kanban Bridge" dir=in action=allow protocol=TCP localport=27124
   ```
4. macOS: System Settings → Network → Firewall → allow Obsidian

### Plugin Not Appearing

**Symptoms:** Plugin not in Community Plugins list

**Solution:** Quit Obsidian completely (not just reload), then reopen. Obsidian requires full restart to detect new plugin folders.

### Port Conflict

**Symptoms:** Server fails to start, port already in use

**Solution:**
1. Change port: Settings → Hermes Kanban Bridge → Port → set to 27125 (or other)
2. Toggle plugin off/on to apply
3. Update Hermes skill configs and `HERMES_KANBAN_URL` to new port

## Environment Variables

```bash
# REST API base URL (default: http://localhost:27124)
export HERMES_KANBAN_URL="http://192.168.1.100:27124"

# Hermes profile for skills installation
export HERMES_PROFILE="frodo"

# Obsidian vault path for scripts
export VAULT_PATH="/Users/alice/Documents/ObsidianVault"
```

## Integration with Hermes Agent

Once skills are installed (`~/.hermes/profiles/*/skills/productivity/`), interact naturally:

**Voice Commands:**
- "Break down the Q3 launch into a Kanban board"
- "Run my daily standup"
- "What cards are blocked?"
- "Move the authentication task to In Progress"
- "Give me a weekly review"

Hermes uses the installed skills to translate commands into REST API calls automatically.

## Resources

- **API Documentation:** `docs/API.md` in repository
- **Demo Board:** `docs/demo/Q3-Launch.md` - sample board for testing
- **Test Suite:** `tests/` - 105 tests, 55% coverage
- **obsidian-kanban plugin:** https://github.com/obsidian-community/obsidian-kanban
