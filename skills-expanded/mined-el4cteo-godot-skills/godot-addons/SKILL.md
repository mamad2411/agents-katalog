---
name: godot-addons
description: Finding, vetting, installing and maintaining Godot 4.7 addons - the in-editor Asset Store, editor plugins vs GDExtensions vs C# addons, compatibility and platform-binary checks, enabling plugins, versioning addons in git, optional dependencies, and a curated 4.7 list (LimboAI, Beehave, Dialogue Manager, Phantom Camera, Terrain3D, GodotSteam, billing, Mod Loader). Use when adding or fixing plugins.
license: MIT
compatibility: Godot 4.7+ (GDScript and C#). Python 3.9+ for scripts/addon_inspect.py.
metadata:
  author: godot-agent-skills
  version: "1.1.0"
---

# Addons and Plugins (4.7)

**Run it:** `python scripts/addon_inspect.py [DIR]` lists every `addons/<name>/` folder: kind, version, enabled state, GDExtension compatibility versus 4.7, missing native binaries for your export platforms, C# addons in non-.NET projects, Godot 3 code, and stale enabled entries. `--enable NAME`/`--disable NAME` edit `[editor_plugins]` in `project.godot` (close the editor first).

## Kinds of addons
| Kind | Looks like | Notes |
|---|---|---|
| Editor plugin | `addons/x/plugin.cfg` + `@tool` script | must be **enabled** (Project Settings → Plugins). Often adds autoloads and custom nodes on enable |
| GDExtension | `*.gdextension` + native libraries per platform | loads by itself (restart the editor after install). Needs a binary for **every** export target (Windows, Linux, macOS, Android, iOS, Web). `compatibility_minimum` must be ≤ 4.7 |
| GDScript library | `.gd` files with `class_name`, no plugin.cfg | nothing to enable. Run `gd_check.py --addons` |
| C# addon | `.cs` files | needs the .NET build. Rebuild with `cs_build.py`; may need NuGet references in your `.csproj` |
| Asset pack | textures, models, sounds | check the license and the import settings |
Writing your own plugin or GDExtension: `godot-editor-tooling`.

## Install
1. **Asset Store** (in the 4.7 editor, it replaces the Asset Library; the old library is read-only for older engines), or GitHub releases / itch.io. Prefer a release asset over the default branch.
2. Copy **only** the `addons/<name>/` folder into your project. Leave out the demo project, its `project.godot` and its `.godot/`.
3. `python ../godot-core/scripts/run_godot.py import` (registers classes and imports assets), then `addon_inspect.py`, then enable the editor plugins (`--enable NAME` or the Plugins tab).
4. Verify: `gd_check.py --addons`, `cs_build.py` for C#, `run_godot.py smoke`. Then export once to every target platform before you depend on the addon (`godot-export-ci`).

## Vet before you depend on it
- **Version match**: the release says 4.7 (or 4.6+ with no breaking notes), and the GDExtension `compatibility_minimum` is ≤ 4.7. A GDExtension built for a *newer* engine won't load. Older builds usually load forward within 4.x, but test them.
- **Maintenance**: recent commits, issues answered, a 4.6/4.7 release in the last year.
- **Platforms**: binaries for every target, including Web and mobile if you ship there. Web needs `variant/extensions_support` for GDExtensions.
- **License**: MIT, Apache, CC0 and zlib are fine for commercial games. GPL/LGPL have obligations. Assets need their own license check (CC-BY needs credits).
- **Footprint**: does enabling it add autoloads, project settings or input actions? `git diff project.godot` after enabling.
- **Godot 3 code** (`tool`, `export var`, `yield`): the wrong version. `addon_inspect.py` flags it.

## Maintain
- **Commit `addons/`** (lock the exact version), and record name, version and source URL in the README or an `ADDONS.md`. CI then builds without network.
- Don't edit addon code in place. Wrap it, or fork it and note the patch, so upgrades stay possible.
- Upgrade one addon at a time on a branch: delete the old folder, copy the new one, import, run `addon_inspect.py` + the tests, and read the addon's changelog for breaking changes.
- GDExtension upgrade crashes in the editor: close the editor, delete `.godot/`, reopen.
- Keep optional integrations optional: check `Engine.has_singleton("Steam")` or `ClassDB.class_exists(&"LimboHSM")` before you use them, so a build without the plugin still runs (reference).

## Curated list for 4.7 (checked November 2026; confirm the newest release before installing)
| Need | Addon | Status |
|---|---|---|
| Unit tests | GdUnit4 (GDScript), gdUnit4Net (C#) | 6.2.x on 4.7; see `godot-testing-debug` |
| Behavior trees + state machines | LimboAI | 1.8.x for 4.6+, built against 4.7.2 (GDExtension or module) |
| Behavior trees (pure GDScript) | Beehave | 2.9.3 supports 4.7 |
| Dialogue | Dialogue Manager | v4 for 4.6+ (v3 for older). See `godot-narrative` for Dialogic 2 (alpha) and Yarn Spinner |
| Camera behaviors (follow, framing, blends) | Phantom Camera | 2D/3D. Check the latest release notes for 4.7 |
| Terrain (sculpting, texturing, LOD) | Terrain3D | 1.1 (GDExtension, Godot 4.5+) |
| Steam | GodotSteam | GDExtension "4.4+" builds (Steamworks 1.64). Use the GDExtension, not a custom engine, unless you need multiplayer peer features |
| Google Play purchases | GodotGooglePlayBilling (official, 3.x) / AndroidIAPP | Android plugin v2, needs a Gradle build |
| Mods | Godot Mod Loader | script extensions and hooks; see `godot-modding-dlc` |
| Procedural tiles | Wave Function Collapse (AlexeyBond) | TileMapLayer and GridMap |
**Built in, don't install**: Godot Jolt (Jolt is built in since 4.4 and the default for new 4.6+ projects), tween/easing libraries (`Tween`), autotile addons (TileSet terrains), IK addons for simple cases (the 4.6 IK modifiers), virtual joystick addons (`VirtualJoystick` in 4.7).

Optional-dependency wrappers in GDScript and C# (compiled by the tests): [references/patterns.md](references/patterns.md)
