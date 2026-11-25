---
name: godot-save-system
description: Save system with JSON-based game saves, player data, item data, and persistence. Use when the user mentions save, load, save system, or saving the game.
---

# Save System

A JSON-based save system for player data, items, and persistent world state.

## Quick Integration

### 1. Configure Autoload

Add this in `Project > Project Settings > Autoload`:

| Name | Path |
|------|------|
| GlobalSaveManager | res://Globals/GlobalSaveManager.gd |

### 2. Save structure

```gdscript
var current_save: Dictionary = {
    scene_path = "",           # Current scene path
    player = {
        hp = 1,
        max_hp = 1,
        pos_x = 0,
        pos_y = 0,
    },
    items = [],                # Inventory items
    persistent = [],           # Persistent flags, for example opened chests
    quests = [],               # Quest data
}
```

### 3. Usage example

```gdscript
# Save the game
GlobalSaveManager.save_game()

# Load the game
GlobalSaveManager.load_game()

# Check persistent data, for example whether a chest has been opened
if GlobalSaveManager.check_persistent_value("chest_001"):
    queue_free()

# Add persistent data
GlobalSaveManager.add_persistent_value("chest_001")
```

## Persistent Data Handler

Use the `PersistentDataHandler` node to automatically handle persistent scene objects:

```gdscript
# persistent_data_handler.gd - attach to objects that need persistence
class_name PersistentDataHandler extends Node

@export var data_id: String  # Unique identifier

func _ready() -> void:
    if GlobalSaveManager.check_persistent_value(data_id):
        get_parent().queue_free()

func set_value() -> void:
    GlobalSaveManager.add_persistent_value(data_id)
```

## Code Files

See `references/code/` for the full implementation.
