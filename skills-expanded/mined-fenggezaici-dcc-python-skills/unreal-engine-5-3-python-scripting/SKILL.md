---
name: unreal-engine-5-3-python-scripting
description: "Unreal Engine 5.3.2 Python scripting reference. Use automatically for any UE5 Python programming question, including editor scripting, Blutilities, editor tools, asset tools, mesh editing, geometry scripting, material editing, sequencer, animation, rigging, import/export, UI widgets, gameplay, Blueprint, or looking up unreal module classes, methods, and examples."
---

# Unreal Engine 5.3 Python Scripting

This skill covers the Python scripting API exposed by Unreal Engine 5.3.2 (`unreal` module),
focusing on the most commonly used classes for editor scripting, tool development, and content automation.

## Core Frameworks & Mental Models

- **The `unreal` module is the entry point**: Most classes/functions live under `unreal` (e.g., `unreal.EditorUtilityLibrary`, `unreal.StaticMesh`).
- **Editor scripting context matters**: Many helper functions (e.g., `get_selected_assets`) only work inside the Unreal Editor, not in a cooked game.
- **Blutilities / Editor Utility Widgets**: Use `EditorUtilityLibrary` and `EditorUtilityWidget` to create editor tools.
- **Subsystems**: Many editor features are exposed as subsystems (e.g., `EditorActorSubsystem`, `StaticMeshEditorSubsystem`).
- **Geometry Script**: `unreal.GeometryScriptLibrary` provides mesh manipulation in Python.

## Chapter Index

- `ch02-core-engine.md` — Core Engine
- `ch03-editor-utilities.md` — Editor Utilities
- `ch04-asset-content-browser.md` — Asset & Content Browser
- `ch05-import-export.md` — Import & Export
- `ch06-mesh-geometry.md` — Mesh & Geometry
- `ch07-material-texture.md` — Material & Texture
- `ch08-blueprint.md` — Blueprint
- `ch09-animation-sequencer.md` — Animation & Sequencer
- `ch10-ui-widgets.md` — UI & Widgets
- `ch11-gameplay.md` — Gameplay Helpers
- `ch12-subsystems.md` — Subsystems
- `ch13-miscellaneous.md` — Miscellaneous

## How to Use This Skill

- Ask for a specific `unreal` class, method, or function (e.g., "how to get selected assets in UE Python?").
- Load a module chapter (e.g., `/unreal-engine-5-3-python-scripting ch04-asset-content-browser`) to browse asset-related classes.
- Use `cheatsheet.md` for common snippets and `glossary.md` for terms.

## Glossary / Quick Reference

See `glossary.md` for key terms and `cheatsheet.md` for common code snippets.