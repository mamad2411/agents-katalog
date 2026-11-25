---
name: godot-player-hud
description: Player HUD system for health bars and heart-based HP display. Use when the user mentions health bars, HUD, HP display, or heart-based health.
---

# Player HUD System

Displays player HUD elements such as health bars and heart-based HP.

## Quick Integration

### 1. Configure Autoload

| Name | Path |
|------|------|
| PlayerHud | res://GUI/PlayeHUD/player_hud.tscn |

### 2. Copy the files

```
GUI/PlayeHUD/
├── player_hud.gd/.tscn    # Main HUD scene
└── heart_gui.gd/.tscn     # Heart health component
```

### 3. Update the HP display

```gdscript
# In the player script
func update_hp(delta: int) -> void:
    hp = clamp(hp + delta, 0, max_hp)
    PlayerHud.update_hp(hp, max_hp)
```

### 4. Customize the heart sprite

The heart sprite sheet should contain 5 horizontal frames:
1. Full heart
2. Three-quarter heart
3. Half heart
4. Quarter heart
5. Empty heart

## Code Files

See `references/code/` for the full implementation.
