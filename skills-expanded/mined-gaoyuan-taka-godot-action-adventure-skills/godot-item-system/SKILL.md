---
name: godot-item-system
description: Item system for item definitions, effect systems, and pickup logic. Use when the user mentions items, pickups, loot, or drop objects.
---

# Item System

Item definitions, effect systems, and pickup/drop logic.

## Quick Integration

### 1. Copy the files

```
Items/
├── item_data.gd            # Item data resource
├── item_effect.gd          # Base effect class
├── item_effect_heal.gd     # Example heal effect
└── item_pickup/
    └── item_pickup.gd/.tscn  # Pickable item

GeneralNode/
├── ItemDropper/            # Item dropper
└── ItemMagnet/             # Item magnet area
```

### 2. Create an item

Create a `.tres` file of type `ItemData`:

```gdscript
# item_data.gd
class_name ItemData extends Resource

@export var name: String = ""
@export_multiline var description: String = ""
@export var texture: Texture2D
@export var effects: Array[ItemEffect]

func use() -> bool:
    for e in effects:
        e.use()
    return true
```

### 3. Create an item effect

```gdscript
# item_effect_heal.gd
class_name ItemEffectHeal extends ItemEffect

@export var heal_amount: int = 1

func use() -> void:
    GlobalPlayerManager.player.update_hp(heal_amount)
```

### 4. Item pickups

Place an `ItemPickup` node in the scene and assign its `item_data` property.

## Code Files

See `references/code/` for the full implementation.
