---
name: quartermaster
description: Checks the game-dev assets the user already owns (Unity Asset Store, Fab, Quixel Megascans, Gumroad, Leartes Cosmos) through the Quartermaster MCP server before anything gets built from scratch or bought. Use when working on a Unity, Unreal or Godot project and the task needs an asset - prototyping a level or scene, needing a mesh, prop, material, texture, shader, VFX, sound, character, animation or tool - when the user asks "what do I have for...", or before recommending a store purchase.
license: MIT
---

# Quartermaster

Quartermaster indexes everything the user owns across five asset stores into one local
library and serves it over MCP. Most game devs own far more than they remember, so the
right mesh or shader is often already on disk. Check the library before writing a
procedural stand-in or sending the user shopping.

## Workflow

1. **Search what's owned first.** Call `search_owned_assets` with a description of what is
   needed, not a product name: "curved concrete wall", "stylized fire spell", "mossy forest
   floor". Search fuses keyword, semantic and screenshot (CLIP) matching, so listings that
   never use the word still come back. For a compound need, search its parts: a dam is
   concrete structures, a water system and rocky terrain.
   Narrow with `engine` (`unity`, `unreal`, `godot`), `pipeline` (`HDRP`, `URP`, `Built-in`),
   `source`, `category` (see `list_asset_categories`) or `local_only=true`.
2. **Map a brief onto the library.** For a feature or level description ("third-person
   village with magic combat"), call `get_stack_recommendations`; it buckets owned packs by
   aspect (terrain, VFX, characters, ...). `list_stack_recipes` shows curated stacks filled
   from the user's own assets.
3. **Inspect before choosing.** `get_asset_details(asset_id)` returns the full listing:
   summary, usage notes, gallery and store URL.
4. **Check fit before importing.** Run `audit_project(project_dir)` to get the target's
   engine, version and render pipeline, so a URP-only shader doesn't land in an HDRP project.
   Run `validate_stack(asset_ids)` on everything planned together: it flags role conflicts
   (two weather systems, two vegetation renderers) and missing prerequisites.
5. **Import.** `import_asset_to_project(asset_id, project_dir)` unpacks a Unity package into
   `Assets/` (demos and docs stripped). It works only for Unity packages with `local=true`;
   `project_dir` is the folder containing `Assets/`.
6. **Report, then fill gaps.** Tell the user what they own, what they can claim free, and
   what is already downloaded. Suggest building or buying only for what the library doesn't
   cover.

## Reading results

- `ownership`: `vault_owned` is in the user's library. `catalog_grant` is a Quixel Megascans
  item claimable free under the Epic Content License but not yet acquired. Say which.
- `local`: `true` means already downloaded (`local_path`); prefer these, they need no download.
- `match`: which signals fired (`keyword`, `semantic`, `vision`). A vision-only hit matched
  the screenshots, not the text; `best_visual_image` shows which one.
- Every result is real: something the user owns or can claim. Never present an asset that
  didn't come back from a tool.

## Not installed?

If the Quartermaster tools aren't available, the MCP server isn't connected:

- Download `Quartermaster-windows-x64.zip` (or `Quartermaster-linux-x64.tar.gz`) from
  [Releases](https://github.com/Tanshaydar/Quartermaster/releases), unpack it and run
  `Quartermaster-mcp.exe --register --all` (`Quartermaster-mcp` on Linux).
- From source (Python 3.10+): clone https://github.com/Tanshaydar/Quartermaster,
  `pip install -r requirements.txt`, then `python -m src.register --all`.

Registration covers Claude Desktop, Cursor, Windsurf and Antigravity; restart the client
afterwards. If the tools respond but find nothing, `get_vault_stats` shows whether the
library has been built yet. Building it is a one-time step the user runs themselves from
the app or the README's Install section; point them there rather than doing it for them.
