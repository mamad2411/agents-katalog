---
name: videogames
slug: videogames
display_name: Video Games
description: A skill to lookup video game information and compare prices across multiple stores.
author: ivanheral
version: 1.0.0
license: MIT
---

# Video Game Skill 🎮

This skill allows OpenClaw to search for games, view Steam details, and find the best prices using CheapShark.

## Tools

### `scripts/game_tool.py`

This Python script interacts with Steam and CheapShark.

**Usage:**

1.  **Search for deals (CheapShark):**
    ```bash
    python3 scripts/game_tool.py deals "Game Name"
    ```
    *Example:* `python3 scripts/game_tool.py deals "Batman"`

2.  **Search on Steam:**
    ```bash
    python3 scripts/game_tool.py search "Game Name"
    ```
    *Example:* `python3 scripts/game_tool.py search "Elden Ring"`

3.  **View details (Steam):**
    ```bash
    python3 scripts/game_tool.py details <APPID>
    ```
    *Example:* `python3 scripts/game_tool.py details 1245620`

## Notes
- The script requires Python 3.
- No external library installation required (uses standard `urllib`).

---
*Created with love by Cachitos for Ivan.*
