---
name: game-assets
description: Organizes, previews and exports 2D game assets (sprites, UI, tiles) for Unity, Electron and Roblox - folder structure, snake_case naming (categoria_objeto_estado_01.png), a per-game ASSETS.md style guide, and the AssetForge scaffold (local Vite+React viewer plus an export CLI with one exporter per engine). Use whenever the user creates, renames, imports or exports game art, asks how assets should be named or laid out, wants an asset browser/inspector, needs pixel-art import settings (Point filter, no compression, Pixels Per Unit), or needs to upload images to Roblox. EXPERIMENTAL - only load in game projects; for design decisions (loop, economy, scope) use game-design-doc instead.
---

# Game assets

> Provenance: own skill (2026-10-22), **experimental**. Not yet used in two real projects (see Validation). Roblox exporter is tested only against a mocked API.

Oficina does not run the app. It holds this skill, the template and the commands; `/oficina:asset-forge` copies the scaffold into the game project (`tools/asset-forge/`), where it runs.

## Folder structure (in the game project)

```
assets/<project>/<categoria>/<categoria_objeto_estado_01>.png
tools/asset-forge/        (copied from templates/asset-forge)
ASSETS.md                 (style guide, from templates/ASSETS.md)
```
`<project>` is the art set (usually the game's name); `<categoria>` groups files (enemies, ui, tiles, items, fx).

## Naming
`categoria_objeto_estado_NN.png`, lowercase snake_case, at least three words then a two-digit index: `enemy_alien_idle_01.png`, `ui_button_hover_01.png`. Rules enforced by `scripts/lib/naming.ts`: the name is the identifier in generated code, so it must be unique across the project and start with a letter. Export aborts, writing nothing, if any selected name is invalid or duplicated.

## Process for a new or changed asset
1. Read the project's `ASSETS.md` (style, palette, base sizes). If missing, create it from the template first.
2. Create or adjust the image to the documented size and palette; name it by the rule; place it in `assets/<project>/<categoria>/`.
3. Add it to the asset list in `ASSETS.md`.
4. Check in the viewer (`npm run dev` in `tools/asset-forge`), then export: `npm run export -- <game> <path>` or `--all`.

## What each target does
| Target | Export does | Generated file |
|---|---|---|
| `electron` | Copies to `<destination>/<categoria>/<file>` | `assets.ts`: `ASSETS` (name to relative path, `as const`) and `AssetName` type |
| `unity` | Copies to `Assets/Sprites/<categoria>/` and installs `Assets/Editor/PixelArtImporter.cs` | `PixelArtImporter.json` (spritesRoot, pixelsPerUnit from `ppu`; written once, edits survive) |
| `roblox` | Uploads as `Decal` via Open Cloud, caches sha256 to assetId | `Assets.lua` ModuleScript (name to `rbxassetid://ID`), Rojo-ready |

All targets also write `asset-manifest.json` (name, source path, sha256, bytes, dest or assetId) into the destination.

- **Electron/Vite:** the paths in `assets.ts` are relative to that file. Build the URL with a bundler-aware import, not a runtime string, if you need hashed production URLs.
- **Unity:** the importer sets Sprite, Filter Mode Point, Compression None, no mipmaps, Pixels Per Unit from the JSON. Unity creates the `.meta` files itself; commit them.
- **Roblox:** needs `ROBLOX_API_KEY`, `ROBLOX_CREATOR_ID`, `ROBLOX_CREATOR_TYPE` (User|Group) in `tools/asset-forge/.env`. Key permissions: asset read and write, restricted by IP. Images only (PNG/JPEG), one asset per call, under 8000x8000 px and 20 MB. The returned ID is a Decal asset ID; Roblox's docs show `rbxassetid://<id>` for it but do not confirm it for `ImageLabel.Image`, so **check one asset in Studio on first real use** and record the result under Validation. On every pixel-art `ImageLabel`/`ImageButton` set `ResampleMode = Enum.ResamplerMode.Pixelated`. Commit `.asset-forge-cache.json` (no secrets) so teammates do not re-upload.

## Security (Oficina baseline)
- `.env` is gitignored; only `.env.example` is committed. `/oficina:asset-forge` also adds `tools/asset-forge/.env` to the game repo's root `.gitignore`.
- Run the `secrets-gitleaks` skill in the game repo (pre-commit hook) before the first Roblox upload. A leaked key means rotate it, not delete it.
- Errors never print the key. The viewer only reads `assets/` and binds to 127.0.0.1.

## Viewer
`npm run dev`: tree by project, category, file; checkerboard preview; zoom 25-400%; crisp (`image-rendering: pixelated`) or smooth; size in px and format; search by name or path with a total counter; footer shows the export command for the selected asset and chosen game. Read-only: it never writes files.

## Validation (experimental)
Record each real project where this was used and what broke. Promote to stable after two.

| Project | Date | Targets used | Result / what was missing |
|---|---|---|---|
| Galaslime (`idle-game`) | 2026-10-23 | none (ASSETS.md only) | Jogo sem PNG (arte em código): só o guia de estilo foi preenchido, AssetForge não instalado. Template serviu, mas falta campo para arte gerada em código e conflito guia x código. Exporters não exercitados. |
