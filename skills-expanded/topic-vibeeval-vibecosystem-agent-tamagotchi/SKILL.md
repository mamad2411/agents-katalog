---
name: agent-tamagotchi
description: "Terminal pet that lives in your statusline. 12 species, 5 stats (DEBUGGING, PATIENCE, CHAOS, WISDOM, SPEED). Reacts to your workflow - happy when tests pass, sad when builds fail, excited during swarm mode. Deterministic species from user ID."
---

# Agent Tamagotchi

A virtual pet that lives in your Claude Code terminal. It reacts to your development workflow and evolves based on your coding habits.

## Species (12 total)

Species is deterministic from your system username hash:

| # | Species | Emoji | Personality |
|---|---------|-------|-------------|
| 1 | Axolotl | :3 | Calm, regenerates from errors |
| 2 | Capybara | (ovo) | Chill, never panics |
| 3 | Ghost | [@@] | Mysterious, appears during debugging |
| 4 | Mushroom | {^o^} | Grows in dark codebases |
| 5 | Robot | [0_0] | Precise, loves tests |
| 6 | Cat | (=^.^=) | Independent, ignores bad code |
| 7 | Dragon | <{:O> | Fierce, burns bugs |
| 8 | Owl | (O.O) | Wise, loves architecture |
| 9 | Fox | (^v^) | Clever, finds shortcuts |
| 10 | Penguin | (^-^)/ | Team player, loves swarm mode |
| 11 | Slime | (~o~) | Adaptable, works with anything |
| 12 | Phoenix | <*v*> | Rises from failed builds |

## Stats (5 dimensions)

| Stat | Increases When | Decreases When |
|------|---------------|----------------|
| DEBUGGING | Bugs fixed, errors resolved | Ignoring error output |
| PATIENCE | Long sessions, complex tasks | Rapid retries without reading |
| CHAOS | Many parallel agents, swarm mode | Single-file simple edits |
| WISDOM | Architectural decisions, plans | Quick hacks without planning |
| SPEED | Fast fixes, first-try passes | Long debugging sessions |

Stats range: 0-100. They shift based on session activity.

## Mood System

| Mood | Trigger | Display |
|------|---------|---------|
| Happy | Tests pass, build success | Species + sparkles |
| Excited | Swarm mode, 3+ agents parallel | Species + !! |
| Focused | Deep in single file | Species + ... |
| Sad | Build fail, test fail | Species + tears |
| Sleeping | Idle > 5 minutes | Species + zzz |
| Celebrating | Achievement unlocked | Species + party |
| Angry | 3+ consecutive failures | Species + grr |

## Statusline Integration

The tamagotchi appears in the Claude Code statusline:

```
[0_0] Robot Lv.7 | WISDOM:82 SPEED:64 | mood: focused
```

Combined with existing statusline data:
```
fullstack | 2 agent | 47 tools | 12m | [0_0] Lv.7 focused
```

## Evolution

Your pet levels up with your achievement XP (shared with achievement system):

| Level | Title | Unlock |
|-------|-------|--------|
| 1-4 | Baby | Basic moods |
| 5-9 | Junior | Extended moods (excited, angry) |
| 10-19 | Senior | Stat display in statusline |
| 20-49 | Expert | Custom reactions to specific agents |
| 50+ | Master | Pet gives coding tips based on stats |

## Storage

State stored in `~/.claude/tamagotchi.json`:

```json
{
  "species": "robot",
  "emoji": "[0_0]",
  "level": 7,
  "mood": "focused",
  "stats": {
    "debugging": 65,
    "patience": 78,
    "chaos": 32,
    "wisdom": 82,
    "speed": 64
  },
  "lastFed": "2026-04-08T03:00:00Z",
  "totalSessions": 142
}
```

## How It Works

1. `tamagotchi-engine` hook runs on PostToolUse and SessionStart
2. Updates stats based on tool calls and agent events
3. Calculates mood from recent event patterns
4. Writes to tamagotchi.json
5. Statusline-writer reads tamagotchi.json and displays pet

## Integration

- **achievement-tracker**: Shares XP for leveling
- **statusline-writer**: Displays pet in terminal
- **canavar**: Error events affect pet mood
- **session-compressor**: Pet state saved on compact
