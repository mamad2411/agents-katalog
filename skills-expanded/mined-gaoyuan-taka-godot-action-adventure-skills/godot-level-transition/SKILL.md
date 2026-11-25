---
name: godot-level-transition
description: Level transition system for scene changes, transition animation, and player placement management. Use when the user mentions scene transitions, level transitions, portals, or transition animation.
---

# Level Transition System

Manages scene transitions, fade animation, and player placement.

## Quick Integration

### 1. Configure Autoload

| Name | Path |
|------|------|
| GlobalLevelManager | res://Globals/GlobalLevelManager.gd |
| SceneTransitionAnime | res://GUI/scene_transition_anime/scene_transition_anime.tscn |

### 2. Core components

```
Levels/
├── level.gd                  # Base level class
├── level_transition.gd/.tscn # Portal / exit
└── player_spawn.gd/.tscn     # Player spawn point
```

### 3. Usage example

```gdscript
# Load a new level
GlobalLevelManager.load_new_level(
    "res://Levels/Area01/scene02.tscn",  # Target scene
    "door_from_scene01",                 # Target door name
    Vector2.ZERO                         # Position offset
)

# Listen for level loading events
GlobalLevelManager.Level_load_started.connect(_on_load_started)
GlobalLevelManager.Level_load_completed.connect(_on_load_completed)
```

### 4. Portal setup

Add a `LevelTransition` node to the scene:
- Set `Level`: the target scene path
- Set `target_door`: the target door name in the destination scene
- Configure the transition area size and side as needed

## Code Files

See `references/code/` for the full implementation.
