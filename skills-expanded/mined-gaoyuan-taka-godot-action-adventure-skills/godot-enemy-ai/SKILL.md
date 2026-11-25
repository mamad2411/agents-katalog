---
name: godot-enemy-ai
description: Enemy AI system with state-machine-driven behavior such as idle, chase, attack, and related states. Use when the user mentions enemy AI, monster behavior, chasing, or patrol enemies.
---

# Enemy AI System

State-machine-based enemy AI with idle, chase, stun, and related states.

## Dependencies

- `godot-state-machine` - state machine system
- `godot-hitbox-hurtbox` - combat collision system

## Quick Integration

### 1. Copy the files

```
Enemies/Scripts/
├── enemy.gd                    # Base enemy script
├── enemy_state_machine.gd      # Enemy state machine
├── vision_area.gd/.tscn        # Vision detection
├── drop_data.gd                # Drop data
└── States/
    ├── enemy_state.gd          # Base state
    ├── enemy_state_idle.gd     # Idle
    ├── enemy_state_wander.gd   # Wander
    ├── enemy_state_chase.gd    # Chase
    ├── enemy_state_stun.gd     # Stun
    └── enemy_state_destroy.gd  # Death
```

### 2. Scene structure

```
Enemy (CharacterBody2D)
├── Sprite2D
├── AnimationPlayer
├── EnemyStateMachine
│   ├── StateIdle
│   ├── StateWander
│   ├── StateChase
│   └── StateStun
├── HitBox
├── HurtBox
└── VisionArea
```

### 3. Base enemy example

```gdscript
# enemy.gd
class_name Enemy extends CharacterBody2D

signal enemy_damaged(hurt_box: HurtBox)
signal enemy_destroyed(hurt_box: HurtBox)

@export var hp: int = 3

func _ready() -> void:
    state_machine.initialize(self)
    hit_box.damaged.connect(_take_damage)

func _take_damage(hurt_box: HurtBox) -> void:
    hp -= hurt_box.damage
    if hp <= 0:
        enemy_destroyed.emit(hurt_box)
    else:
        enemy_damaged.emit(hurt_box)
```

## Code Files

See `references/code/` for the full implementation.
