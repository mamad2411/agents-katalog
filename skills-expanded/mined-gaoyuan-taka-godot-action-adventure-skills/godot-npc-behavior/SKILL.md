---
name: godot-npc-behavior
description: NPC behavior system for patrols, wandering, and player interaction. Use when the user mentions NPC behavior, patrol NPCs, wandering, or NPC movement.
---

# NPC Behavior System

Manages NPC patrols, wandering, and player interaction.

## Quick Integration

### 1. Copy the files

```
NPC/
├── npc.gd/.tscn                # Base NPC class
├── npc_resource.gd             # NPC resource
├── npc_behavior.gd             # Base behavior class
├── npc_behavior_patrol.gd      # Patrol behavior
├── npc_behavior_wander.gd      # Wander behavior
└── patrol_location.gd/.tscn    # Patrol marker
```

### 2. Create an NPC

1. Create an `NPCResource` (`.tres`) and set the NPC name, sprite, and dialog portrait.
2. Instance the NPC scene.
3. Assign the `npc_resource` property.

### 3. Add behaviors

Add behavior nodes under the NPC:

```
NPC (CharacterBody2D)
├── Sprite2D
├── AnimationPlayer
├── NPCBehaviorPatrol
│   └── patrol_locations: [PatrolLocation, PatrolLocation, ...]
└── DialogInteraction (optional)
```

### 4. Behavior types

| Behavior class | Description |
|--------|------|
| `NPCBehaviorPatrol` | Patrols between specified points |
| `NPCBehaviorWander` | Wanders randomly within a range |

## Code Files

See `references/code/` for the full implementation.
