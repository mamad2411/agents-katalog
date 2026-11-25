---
name: minecraft-builder-skill
description: Programmatically generate Minecraft builds as vanilla structure NBT files and open Lodestone-powered previews. Use when an agent needs to create, export, inspect, or iterate on Minecraft structures, schematics, block palettes, or build recipes using JavaScript and .nbt output.
---

# Minecraft Builder Skill

## Overview

Create Minecraft builds by writing small JavaScript recipes that use Lodestone-backed helper functions. Export vanilla `.nbt` structure files, then open the included viewer so the user can inspect and iterate on the build.

## Workflow

1. Work from the installed skill directory. Do not rerun the Skills CLI after installation; use this skill's local `scripts/` and `assets/`.
2. Before running any build or preview scripts, ensure dependencies are installed. If `node_modules/@mattzh72/lodestone` is missing, run this from the installed skill directory:

```bash
npm install --omit=dev
```

3. Write an ESM recipe file. Use `assets/examples/celestial-forge.mjs` as the canonical example for ambitious floating megastructures.
4. Generate NBT:

```bash
node scripts/run-build.mjs path/to/recipe.mjs --out-dir minecraft-builds/my-build
```

5. Open the preview:

```bash
node scripts/preview.mjs --nbt minecraft-builds/my-build/my-build.nbt
```

6. Iterate by editing the recipe, regenerating the `.nbt`, and reopening or refreshing the preview.

## Dependencies

Skills CLI installs copy the skill files but may not install Node packages. This skill intentionally keeps dependencies in `package.json` and `npm-shrinkwrap.json` instead of vendoring `node_modules`.

Before using `scripts/run-build.mjs` or `scripts/preview.mjs`, check for `node_modules/@mattzh72/lodestone`. If it is absent, run `npm install --omit=dev` from the installed skill directory. Do not install dependencies globally, and do not guess alternate Lodestone versions.

## Recipe Contract

Export a default function that receives `api` and returns either a Lodestone `Structure` or an object with `{ structure, metadata }`.

```js
export default function build(api) {
  const structure = api.createStructure([16, 12, 16])
  api.fill(structure, [0, 0, 0], [15, 0, 15], 'minecraft:stone_bricks')
  api.hollowBox(structure, [4, 1, 4], [11, 7, 11], 'minecraft:spruce_planks')
  return { structure, metadata: { name: 'example-build' } }
}
```

Available helpers include `createStructure`, `setBlock`, `fill`, `hollowBox`, `line`, `sphere`, `cylinder`, `normalizeBlock`, `createBlockNbt`, and Lodestone classes under `api.lodestone`.

## References

- For exact recipe helper signatures, supported option fields, defaults, and unsupported behavior, search `references/recipe-api.md`.
- For Lodestone classes, structure NBT, block states, renderer APIs, resource pack APIs, supported fields, and unsupported behavior, search `references/lodestone/`.
- For exact default-pack block ids, rendered block-state value enums, special renderer state values, and generic renderer properties like `waterlogged`, search `references/lodestone/default-pack-block-states.md`.
- Prefer these local references over guessing. Use `rg` for class names, method names, block-state properties, NBT tag names, and option fields before using advanced APIs.

## Reference Lookup

- Before choosing nontrivial block-state values, search `references/lodestone/default-pack-block-states.md`.
- For one block, print its exact section, for example ``rg -n -A 80 '### `minecraft:oak_stairs`' references/lodestone/default-pack-block-states.md``.
- For global property enums, search property-index lines, for example ``rg -n '^- `shape`|^- `waterlogged`' references/lodestone/default-pack-block-states.md``.
- Before relying on automatic connection behavior, search `references/lodestone/structure.md` for `updateBlockStates()` and check the supported and unsupported coverage.
- When writing block entities or custom NBT, search `references/lodestone/nbt.md` and `references/recipe-api.md` before constructing tags.

## Build Guidance

- Keep all coordinates inside the structure size. The runner validates bounds and fails fast.
- Use vanilla block IDs with the `minecraft:` namespace. Block-state strings like `minecraft:oak_stairs[facing=east,half=bottom,shape=straight]` are supported.
- The runner enables Lodestone's Minecraft-like block state updates by default. Panes, iron bars, and fences get `north/east/south/west` states from neighboring compatible or solid blocks. Use `--no-block-state-updates` only when a recipe intentionally sets those states by hand.
- Prefer clear block palettes and readable geometry. The viewer uses Lodestone's bundled default resource pack, so highly unusual or custom blocks may not preview well.
- Include `metadata.name` to control the output filename. Names are slugified.
- Default output is gzip-compressed vanilla structure NBT with `DataVersion` set by the runner unless overridden.
- For block entities, pass a Lodestone `NbtCompound` as the last argument to `setBlock` or use `api.createBlockNbt({ id: 'minecraft:chest' })`.

## Preview

The preview script starts a minimal Vite server and opens the build automatically. It serves the target `.nbt` and Lodestone's default resource pack through local middleware, so recipes do not need to copy assets.

Use `--no-open` when running in a non-interactive environment:

```bash
node scripts/preview.mjs --nbt path/to/build.nbt --no-open
```

Open directly in night lighting when helpful for review:

```bash
node scripts/preview.mjs --nbt path/to/build.nbt --lighting night
```
