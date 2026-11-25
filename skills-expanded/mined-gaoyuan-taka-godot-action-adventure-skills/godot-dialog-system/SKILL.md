---
name: godot-dialog-system
description: Dialog system for NPC conversations, branching choices, portrait animation, and typewriter text. Use when the user mentions dialog systems, NPC dialog, branching dialog, or dialog choices.
---

# Dialog System

A complete NPC dialog system with typewriter text, portrait animation, and branching choices.

## Features

- **Portrait animation**: supports blinking and mouth movement
- **Typewriter effect**: reveals text letter by letter with automatic punctuation delays
- **Branching choices**: supports dialog trees and multiple choice options
- **Automatic pause**: pauses the game while dialog is active
- **Voice audio**: supports dialog audio with random pitch variation

## Quick Integration

### 1. Copy the files

```
GUI/dialog_system/
├── dialog_system.gd/.tscn  # Dialog UI (Autoload)
├── dialog_portrait.gd      # Portrait animation
└── ...

Interactables/Dialog/Scripts/
├── dialog_item.gd          # Base dialog item
├── dialog_text.gd          # Text dialog
├── dialog_choice.gd        # Choice dialog
├── dialog_branch.gd        # Branch data
└── dialog_interaction.gd   # Interaction trigger

NPC/Scripts/
└── npc_resource.gd         # NPC info resource
```

### 2. Configure Autoload

Add this in `Project > Project Settings > Autoload`:

| Name | Path |
|------|------|
| DialogSystem | res://GUI/dialog_system/dialog_system.tscn |

### 3. Create an NPC resource

```gdscript
# Create a .tres file for NPC info
# Type: NPCResource

# npc_resource.gd
class_name NPCResource extends Resource

@export var npc_name: String = ""
@export var sprite: Texture       # NPC sprite
@export var portrait: Texture     # Dialog portrait (4 frames: normal, blink, open mouth, blink + open mouth)
@export_range(0.5, 1.8, 0.02) var dialog_audio_pitch: float = 1
```

### 4. Set up dialog content

Create a dialog node structure like this in the scene:

```
DialogInteraction (Area2D)
├── CollisionShape2D
├── DialogText
│   └── text: "Hello! Welcome to the village."
└── DialogChoice
    ├── DialogBranch
    │   ├── text: "I want to buy something"
    │   └── DialogText
    │       └── text: "Sure, take a look at our goods."
    └── DialogBranch
        ├── text: "Goodbye"
        └── DialogText
            └── text: "Farewell, traveler!"
```

### 5. Usage example

```gdscript
# Trigger dialog manually (without DialogInteraction)
var dialog_items: Array[DialogItem] = [my_dialog_text, my_dialog_choice]
DialogSystem.show_dialog(dialog_items)

# Listen for dialog completion
DialogSystem.finished.connect(_on_dialog_finished)
```

## Node Types

| Class | Purpose | Description |
|---|------|------|
| `DialogInteraction` | Interaction trigger | Starts dialog when the player enters the area and presses the interact key |
| `DialogText` | Text dialog | Displays a line of NPC dialog |
| `DialogChoice` | Choice dialog | Displays multiple options for the player |
| `DialogBranch` | Branch container | Holds one option button and the dialog that follows it |

## Portrait Sprite Requirements

The portrait image should contain 4 horizontal frames:
1. Normal
2. Blink
3. Open mouth
4. Blink + open mouth

## FAQ

**Q: The mouth animation only works during the first conversation. Why?**
- Make sure you call `portrait_sprite.reset_state()` when starting a new dialog.

**Q: How do I customize the dialog speed?**
- Change the `text_speed` variable in `dialog_system.gd` (default: `0.1` seconds).

## Code Files

See the full implementation in `references/code/`.
