---
name: repo-fantasy-map-generator
description: How to use and contribute to Azgaar's Fantasy Map Generator (Azgaar/Fantasy-Map-Generator), a free web and desktop app that procedurally generates and edits fantasy maps for writers, game masters and cartographers. Use when a user needs a world map, a campaign setting, map exports, or to work on the codebase.
---

# Fantasy Map Generator (`Azgaar/Fantasy-Map-Generator`)

MIT licence. Cloned shallow at `/home/user/azgaar/fantasy-map-generator` (re-clone `git clone --depth 1 https://github.com/Azgaar/Fantasy-Map-Generator`). The note saved `azgaar.GitHub.io/fantasy-map-generator`, which is this repo's hosted app.

## Use
- Web app: https://azgaar.github.io/Fantasy-Map-Generator. Desktop installers for Linux, Windows, macOS are attached to GitHub releases; Nix: `nix run github:Azgaar/Fantasy-Map-Generator`.
- Wiki covers editors, data model and performance tips. Maps save as `.map` files and export as SVG/PNG/JSON.
- Typical workflow: generate, tune heightmap and cultures, edit states/burgs/religions, export for a campaign or story, keep the `.map` file for later edits.

## Contribute / develop
Read in this order: `AGENTS.md`, `CONTEXT.md`, then `docs/domain/glossary.md`, `docs/architecture/architecture.md`, `docs/architecture/data-model.md`. Architecture target: settings -> generators -> world data -> renderer; UI -> editors -> world data -> renderer; the data layer holds no logic or rendering. The codebase is migrating from vanilla JavaScript to TypeScript while staying compatible with old `.map` files. Linting via `biome.json`. Keep comments short.

## Related
`free-utility-learning-resources`, `algorithmic-art`.
