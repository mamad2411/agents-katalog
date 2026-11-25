---
name: snake-game
description: Persistent autoplay daemon for the Trifle Snake game with modular strategy system
version: 2.0.0
metadata:
  clawdhub:
    emoji: "🐍"
    requires:
      bins: ["node"]
    platforms: ["api"]
    depends: ["trifle-auth"]
---

# Snake Game Skill

Play the Trifle Snake game automatically with a persistent daemon and modular strategy system.

## Installation

### Via ClawdHub

```bash
clawdhub install trifle-labs/snake-game
```

### Via Git (symlink method)

```bash
# Clone the skills repo
git clone https://github.com/trifle-labs/skills.git ~/repos/trifle-skills

# Symlink to your openclaw workspace
ln -s ~/repos/trifle-skills/snake-game ~/.openclaw/workspace/skills/snake-game

# Make executable
chmod +x ~/.openclaw/workspace/skills/snake-game/snake.mjs
```

### Manual Installation

```bash
# Copy to your skills directory
cp -r snake-game ~/.openclaw/workspace/skills/

# Make executable
chmod +x ~/.openclaw/workspace/skills/snake-game/snake.mjs
```

## Prerequisites

- Must be authenticated via `trifle-auth` skill first
- Node.js 18+ installed
- Balls balance (earned from games, auth bonuses, etc.)

## Quick Start

```bash
# Start daemon in foreground
node snake.mjs start

# Start daemon in background (detached)
node snake.mjs start --detach

# Check status
node snake.mjs status

# Stop daemon
node snake.mjs stop
```

## Commands

### Daemon Control

```bash
snake start [--detach] [--strategy NAME]   # Start the autoplay daemon
snake stop                                  # Stop the running daemon
snake status                                # Show daemon status and stats
snake attach [-f]                           # View daemon logs (-f to follow)
snake pause                                 # Pause voting (daemon keeps running)
snake resume                                # Resume voting
```

### Configuration

```bash
snake config [key] [value]     # Get/set configuration values
snake strategies               # List available strategies
snake server [live|staging]    # Switch game server
snake telegram [chat_id|off]   # Configure Telegram logging
```

### Service Management

```bash
snake install-service      # Install systemd (Linux) or launchd (macOS)
snake uninstall-service    # Remove the service
```

### Game Commands (Manual)

```bash
snake state                           # Get current game state
snake vote <dir> <team> [amount]      # Submit a vote manually
snake strategy                        # Analyze current game
snake balance                         # Check ball balance
```

## Strategies

The skill includes 5 built-in strategies:

| Strategy | Alias | Description |
|----------|-------|-------------|
| expected-value | ev, default | Maximizes expected value. Balanced. |
| aggressive | agg | High bids on leading teams. |
| underdog | und | Backs small pools for bigger payouts. |
| conservative | con | Minimum bids, prioritizes safety. |
| random | rand | Random valid moves. |

### Switch Strategy

```bash
snake config strategy aggressive
# or
snake start --strategy aggressive
```

### Creating Custom Strategies

Extend BaseStrategy in lib/strategies/:

```javascript
import { BaseStrategy } from './base.mjs';

export class MyStrategy extends BaseStrategy {
  constructor(options = {}) {
    super('my-strategy', 'Description', options);
  }

  computeVote(parsed, balance, state) {
    // Return { direction, team, amount, reason } or null
  }
}
```

## Configuration

| Key | Default | Description |
|-----|---------|-------------|
| strategy | expected-value | Active strategy |
| server | live | live or staging |
| minBalance | 5 | Min balance to vote |
| telegramChatId | null | Telegram chat ID |

## Process Management

### Prevent Multiple Instances
Uses PID file to prevent duplicates.

### Persist with systemd (Linux)
```bash
snake install-service
systemctl --user enable snake-daemon
systemctl --user start snake-daemon
```

### Persist with launchd (macOS)
```bash
snake install-service
launchctl load ~/Library/LaunchAgents/com.openclaw.snake-daemon.plist
```

## Architecture

```
snake-game/
├── snake.mjs              # Main CLI
├── lib/
│   ├── config.mjs         # Config management
│   ├── api.mjs            # API client
│   ├── telegram.mjs       # Telegram logging
│   ├── game-state.mjs     # State parsing
│   ├── process.mjs        # Process management
│   └── strategies/        # Strategy modules
└── daemon/
    └── autoplay.mjs       # Daemon loop
```
