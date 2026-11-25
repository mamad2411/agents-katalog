---
name: agon-gateway-bonding
description: "Register /level and /bond as gateway slash commands across all platforms (Telegram, Discord, Slack, CLI, WebUI) with AGON bonding system integration."
version: 1.0.0
author: AGON (EREVUS SYSTEMS)
platforms: [windows, linux, macos]
---

# AGON Gateway Bonding Commands

Registers `/level` (compact) and `/bond` (full report) as Hermes gateway slash commands that work on Telegram, Discord, CLI, WebUI, and all other messaging platforms.

## What It Does

1. **Adds CommandDef entries** to `hermes_cli/commands.py` — registers `/level` (aliases: `bond`, `xp`, `bonding`) and `/bond` in `COMMAND_REGISTRY`
2. **Adds dispatch handler** in `gateway/run.py` — intercepts `canonical in ("level", "bond")` and routes to `_handle_agon_bond_command`
3. **Adds handler method** in `gateway/run.py` — `_handle_agon_bond_command()` reads `~/.hermes/agon/bonding.json` and formats output
4. **Creates `~/.hermes/agon/bonding.py`** — utility module with `format_level()`, `format_bond()`, `load_bonding()`
5. **Ensures `~/.hermes/agon/bonding.json`** — bonding data with level, XP, stats, unlocked features

## Files Modified

```
hermes-agent/hermes_cli/commands.py   → +7 lines (2 CommandDef entries)
hermes-agent/gateway/run.py           → +3 lines (dispatch) + ~20 lines (handler)
~/.hermes/agon/bonding.py             → created (utility module)
~/.hermes/agon/bonding.json           → created/updated (bonding data)
```

## Installation

Via `patch_gateway.py` (in repo root) — idempotent, safe to run repeatedly:

```bash
cd ~/Documents/hermes-agon
python patch_gateway.py
hermes gateway restart
```

Or via the full AGON installer which calls `patch_gateway.py` automatically:

```bash
cd ~/Documents/hermes-agon
./install.sh          # macOS/Linux
powershell ./install.ps1   # Windows
```

## Commands

| Command | Description | Output |
|---------|-------------|--------|
| `/level` | Compact bonding report | Level, XP bar, title, stats, next unlock |
| `/bond` | Full bonding report | All stats, unlocked features, next milestone |
| `/xp` | Alias for `/level` | Same as `/level` |
| `/bonding` | Alias for `/level` | Same as `/level` |

## Bonding Data

Stored in `~/.hermes/agon/bonding.json`:

```json
{
  "version": 1,
  "level": 1,
  "cumulative_xp": 0,
  "total_interactions": 0,
  "total_tool_calls": 0,
  "total_tasks_completed": 0,
  "corrections_learned": 0,
  "skills_saved": 0,
  "daily_streak": 0,
  "last_active": "",
  "history": [
    {"ts": "", "event": "Bond initialized. DEUS VULT.", "xp": 0, "source": "init"}
  ]
}
```

Level formula: `floor(10 × N²) + 5` total XP to reach level N.

Title mapping: 1=Stranger, 2=Acquaintance, 3=Friend, 4=Companion, 5=Partner, 6=Champion, 7=Legend, 8=Myth, 9=Apex, 10=Ascendant, 11=Transcendent, 12=Eternal, 13=Daimon, 14=Olympian, 15=Titan.

## After Hermes Update

If Hermes is updated, the `patch_gateway.py` script must be re-run:

```bash
cd ~/Documents/hermes-agon
python patch_gateway.py
hermes gateway restart
```

## Pitfalls

- The `patch_gateway.py` script patches source files — Hermes updates will overwrite them. Always re-run after `pip install --upgrade hermes-agent`.
- `patch` tool can truncate files if the old_string spans too much. Always use explicit markers (`COMMANDS_CHECK`, `DISPATCH_CHECK`, `HANDLER_CHECK`) to detect "already patched" state before attempting insertion.
- On Windows, MSYS path translation (`/c/...`) doesn't work with Python's `py_compile`. Use `C:/Users/...` style paths.
- After restoring from git (`git checkout -- gateway/run.py`), re-apply patches.
