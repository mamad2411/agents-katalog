---
name: maya-2024-python-commands
description: "Maya 2024.2 Python / maya.cmds command reference. Use automatically for any Maya Python scripting question, including writing plugins, tools, rigging, modeling, animation, rendering, effects, nCloth, nHair, fluids, paint effects, UI, MEL-to-Python conversion, or looking up maya.cmds commands, flags, return values, and examples."
---

# Maya 2024 Python Commands

This skill covers the Autodesk Maya 2024.2 Python command documentation (`maya.cmds`).

## Core Frameworks & Mental Models

- **Maya commands are procedural wrappers**: Most `maya.cmds` functions mirror MEL commands and operate on the current scene graph.
- **create / query / edit modes**: Many commands support `query=True` (`q=True`) and `edit=True` (`e=True`) in addition to object creation.
- **construction history**: Modeling commands often insert a DG node; use `constructionHistory=True/False` to control it.
- **selection-sensitive**: Most commands operate on explicit object names or the current selection if none are provided.
- **undoable by default**: Commands are generally undoable unless documented otherwise.
- **Python-specific notes**: String arguments, list return values, and Maya's linear/unit types are all Python-friendly.

## Chapter Index

- `ch01-animation-animation` — Animation - Animation
- `ch02-animation-deformation` — Animation - Deformation
- `ch03-animation-skinning` — Animation - Skinning
- `ch04-animation-constraints` — Animation - Constraints
- `ch05-animation-ik` — Animation - IK
- `ch06-animation-mocap` — Animation - MoCap
- `ch07-animation-blue-pencil` — Animation - Blue Pencil
- `ch08-effects-dynamics` — Effects - Dynamics
- `ch09-effects-ndynamics` — Effects - nDynamics
- `ch10-effects-painteffects` — Effects - PaintEffects
- `ch11-effects-fluids` — Effects - Fluids
- `ch12-effects-hair` — Effects - Hair
- `ch13-general-general` — General - General
- `ch14-general-attributes` — General - Attributes
- `ch15-general-display` — General - Display
- `ch16-general-selection` — General - Selection
- `ch17-general-contexts` — General - Contexts
- `ch18-language-math` — Language - Math
- `ch19-language-strings` — Language - Strings
- `ch20-language-array` — Language - Array
- `ch21-language-scripting` — Language - Scripting
- `ch22-modeling-polygons` — Modeling - Polygons
- `ch23-modeling-nurbs` — Modeling - NURBS
- `ch24-modeling-curves` — Modeling - Curves
- `ch25-modeling-subds` — Modeling - SubDs
- `ch26-rendering-rendering` — Rendering - Rendering
- `ch27-rendering-camera` — Rendering - Camera
- `ch28-rendering-layers` — Rendering - Layers
- `ch29-rendering-lights` — Rendering - Lights
- `ch30-system-files` — System - Files
- `ch31-system-devices` — System - Devices
- `ch32-system-plug-ins` — System - Plug-ins
- `ch33-system-localization` — System - Localization
- `ch34-system-utilities` — System - Utilities
- `ch35-windows-windows` — Windows - Windows
- `ch36-windows-panels` — Windows - Panels
- `ch37-windows-controls` — Windows - Controls
- `ch38-windows-layouts` — Windows - Layouts
- `ch39-windows-menus` — Windows - Menus
- `ch40-windows-misc.-ui` — Windows - Misc. UI

## How to Use This Skill

- Ask for a command by name to get its synopsis, flags, return value, and examples.
- Ask for commands in a category (e.g., "poly modeling commands" or "animation keyframe commands").
- Use the chapter names above to load a specific category on demand.

## Glossary / Quick Reference

See `glossary.md` for an alphabetical list of all commands and `cheatsheet.md` for common patterns.
