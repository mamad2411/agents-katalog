---
name: godot-inventory-system
description: Inventory system for item slots, inventory UI, and item add/remove operations. Use when the user mentions inventory, inventory UI, or item management.
---

# Inventory System

Manages item slots, inventory UI, and item add/remove operations, with save-data integration.

## Quick Integration

### 1. Copy the files

```
GUI/pause_menu/Inventory/
├── inventory_data.gd       # Inventory data (Resource)
├── slot_data.gd            # Slot data (Resource)
├── inventory_ui.gd/.tscn   # Inventory UI
└── inventory_slot_ui.gd    # Inventory slot UI component
```

### 2. Create an inventory data resource

Create `player_inventory.tres` with type `InventoryData`:

```gdscript
# inventory_data.gd
class_name InventoryData extends Resource

@export var slots: Array[SlotData]  # Slot array

func add_item(item: ItemData, count: int = 1) -> bool:
    # Try stacking first, then look for an empty slot
    ...
```

### 3. Usage example

```gdscript
# Add items
var inventory: InventoryData = preload("res://Inventory/player_inventory.tres")
inventory.add_item(apple_item, 5)

# Use an item
inventory.use_item(potion_item, 1)
```

## Core Classes

| Class | Purpose |
|---|------|
| `InventoryData` | Inventory data management |
| `SlotData` | Single slot data |
| `InventoryUI` | Inventory screen |
| `InventorySlotUI` | Slot button UI |

## Code Files

See `references/code/` for the full implementation.
