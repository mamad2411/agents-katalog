---
name: godot-modding-dlc
description: Mod support, DLC and patches in Godot 4.7 - resource packs (PCK/ZIP) with load_resource_pack, load timing and file overrides, mod folders, manifests and load order, registries and a mod API, runtime loading of images, audio, glTF and fonts, PCKPacker mod tools, Godot Mod Loader, Steam Workshop, DLC packs, delta patches, security limits. Use for mods, user content, DLC or patching.
license: MIT
compatibility: Godot 4.7+ (GDScript and C#).
metadata:
  author: godot-agent-skills
  version: "1.1.0"
---

# Modding, DLC and Patches (4.7)

## Choose the kind of mod support
| Level | What mods can do | How |
|---|---|---|
| Data mods | new items, levels as JSON, textures, sounds, models | read files from a mods folder at runtime (no Godot needed by modders) |
| Pack mods | new scenes, scripts, resources; replace any game file | `.pck`/`.zip` loaded with `ProjectSettings.load_resource_pack()`; modders use the Godot editor |
| Script-extension mods | change existing game logic without replacing files | the **Godot Mod Loader** addon (script extensions and hooks, used by shipped games) |
| Workshop | discovery and install | Steam UGC through GodotSteam; it downloads into a folder you then load like any other mod |
Start with data mods plus a registry API. Add packs when modders need scenes and scripts.

## Resource packs
- `ProjectSettings.load_resource_pack(path, replace_files := true, offset := 0)` mounts a PCK or ZIP into `res://`. It returns `false` on failure. With `replace_files = true`, pack files **override** game files at the same path (texture packs, balance patches). Set `false` to protect the base game.
- **Timing**: resources already loaded or preloaded stay cached. Load packs as early as possible, in an autoload's `_init()` (the first autoload), before the main scene loads. To swap later, reload with `ResourceLoader.load(path, "", ResourceLoader.CACHE_MODE_REPLACE)` and rebuild the scenes that use it.
- Where to look: `user://mods/` (always writable) and the folder next to the executable (`OS.get_executable_path().get_base_dir() + "/mods"`, for Steam/manual installs; not writable on every platform). In the editor, `OS.has_feature("editor")` points to a dev folder instead.
- Ask mods to put their files under `res://mods/<mod_id>/` so two mods don't overwrite each other by accident. Overrides then become deliberate (same path as a game file).
- A pack must be exported by the **same Godot version** (4.7.x) as the game, from a project with the same import settings. Give modders a "mod SDK" project: the game's public assets and scripts, a sample mod and an export preset (`godot --headless --export-pack "Mod" mymod.pck`, see `godot-export-ci`).
- **`class_name` in mod scripts isn't reliable** (the global class cache comes from the game). Mods should reference scripts and scenes by path or through your registry.
- C# games: GDScript mods still work in .NET builds. Mod C# assemblies aren't loaded from packs; supporting them needs your own `AssemblyLoadContext` code. Most games keep mods GDScript or data only.

## Manifest, order, conflicts
- Each mod has `mod.cfg` (a `ConfigFile`): `id`, `name`, `version`, `game_version` (min compatible), `depends`, `priority`. Read it **before** loading the pack (the reference reads it from inside a ZIP with `ZIPReader`, or from a folder).
- Sort by dependencies, then priority. Packs loaded later win on file conflicts, so show a load-order UI and save the enabled list in `user://mods.cfg`.
- Skip mods with a newer `game_version` or missing dependencies and **say why** in the mod menu. Never crash because of a bad mod: `push_warning` and continue.
- After loading, call each mod's entry script (`res://mods/<id>/main.gd` with `func _mod_init(api)`), passing a narrow API object.

## A mod API instead of free access
- **Registries**: `ItemRegistry.register(id, item_resource)`, `EnemyRegistry`, `LevelRegistry`. The game reads from registries, never from hard-coded lists, so mods add content without patching files.
- **Events**: expose an event bus (`enemy_killed`, `level_loaded`, `player_spawned`) for mods to react to.
- **Version the API** (`api_version` in the manifest), and deprecate before you remove anything.
- Data validation: parse JSON with `JSON.parse_string`, check types and ranges, clamp numbers, and fall back to defaults.

## Runtime loading for data mods (no import step)
| Asset | API |
|---|---|
| Image → texture | `Image.load_from_file(path)` → `ImageTexture.create_from_image(img)` |
| Audio | `AudioStreamOggVorbis.load_from_file`, `AudioStreamWAV.load_from_file`, `AudioStreamMP3.load_from_file` |
| 3D model | `GLTFDocument.new().append_from_file(path, state)` → `generate_scene(state)` |
| Font | `FontFile.new().load_dynamic_font(path)` |
| Text, data | `FileAccess.get_file_as_string`, `JSON.parse_string`, `ConfigFile.load` |
| Zipped content | `ZIPReader.open` → `read_file` (then `Image.load_png_from_buffer`, …) |
Runtime-loaded textures aren't VRAM-compressed, so cap their size for mobile. Load big sets with `WorkerThreadPool` (`godot-performance`).

## Security (tell your players)
Pack mods and Mod Loader mods run **unrestricted GDScript**: file access, network and OS calls. Godot has no sandbox. Show a warning on first enable, and keep data-only mods as the default for user-generated content you download automatically. Evaluate expressions from mod data with `Expression.execute(..., const_calls_only = true)`.

## DLC and patches
- **DLC**: export the DLC content as a PCK (`--export-pack` with a preset that includes only `res://dlc/<name>/`). Ship it as a separate depot or download, verify ownership (Steam: GodotSteam `isDLCInstalled(app_id)`; consoles and mobile stores have their own APIs), then `load_resource_pack`. PCKs aren't DRM: anyone can copy the file.
- **Patches**: `godot --export-patch out.pck --patches base.pck` (4.6+) writes only changed files, delta-encoded. Load patches in order after the base. Each patch adds load-time overhead, so fold patches into a new base PCK at major updates. Steam and most stores already diff builds, so patch PCKs matter mainly for custom launchers and mobile hot-content.
- Code signing and console certification rules may forbid loading code at runtime. iOS forbids downloaded executable code, so ship content-only packs there.

## Tools for modders
- `PCKPacker` builds packs from inside the game (`pck_start`, `add_file(res_path, source)`, `flush`), e.g. a level editor that exports shareable levels.
- Document the folder layout, the registry API and the event list in the SDK README.

Mod loader (discovery, manifests, order, packs), registry, runtime asset loading, PCK export from game, DLC gate (compiled by the tests): [references/patterns.md](references/patterns.md)
