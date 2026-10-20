---
name: "gameplay-code"
description: "Use when editing gameplay code or scenes in my-game: mechanics, player systems, world interactions, state flow, or config-driven behavior."
applyTo: "my-game/scripts/**, my-game/scenes/**"
---

# Gameplay Code Rules

- ALL gameplay values MUST come from external config/data files, NEVER hardcoded
- Use delta time for ALL time-dependent calculations (frame-rate independence)
- NO direct references to UI code — use events/signals for cross-system communication
- Every gameplay system must implement a clear interface
- State machines must have explicit transition tables with documented states
- Write unit tests for all gameplay logic — separate logic from presentation
- Document which design doc each feature implements in code comments
- Avoid ad-hoc global game state — keep shared state explicit and Autoloads narrowly scoped

## Examples

**Correct** (data-driven):

```gdscript
var damage: float = config.get_value("combat", "base_damage", 10.0)
var speed: float = stats_resource.movement_speed * delta
```

**Incorrect** (hardcoded):

```gdscript
var damage: float = 25.0   # VIOLATION: hardcoded gameplay value
var speed: float = 5.0      # VIOLATION: not from config, not using delta
```
