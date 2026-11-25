# Genex textures in AI Game Studio

You are building inside AI Game Studio. Below the upstream marker is Genex's texture card,
with the passages of advice Studio does not ship taken out. Where it disagrees with this preface,
this preface wins.

- Run every command through `genex__asset`, never `npx genex`. `npx genex texture "<surface>"
  --terrain` is `genex__asset {"operation":"texture","prompt":"<surface>","options":
  {"terrain":true}}`.
- Studio submits every create without waiting and delivers every map into the game: never pass
  `out-dir`, `no-wait` or `no-download`. Pick a set up with operation `wait` and its
  generationId.
- Operation `status` names the lanes that are live.

<!-- upstream @genex-ai/cli-demo/templates/skills/genex-tool-texture/SKILL.md v1.40.0 sha256 d89a284d5b05fe24f69aecee1f860f18e2aeed607be27983168f1a9eaa402829 -->
---
name: genex-tool-texture
description: Generate a tiling PBR texture set with `npx genex texture` — ground, floors, walls, rock, bark, metal, fabric, any repeating surface. Produces several maps (base colour, normal, roughness and friends) as separate files in ./assets, and `--terrain` makes the result seamless for large ground planes.
---

# Genex Tools · Texture

A repeating SURFACE, as a set of PBR maps. Use this for anything a material
covers: ground, floors, walls, cliffs, bark, hull plating, cloth.

For a single flat picture — a poster, a sign, a sprite — use `$genex-tool-image`
instead. That is one image; this is a tiling material.

## Run

```bash
npx genex texture "stone floor tiles"
npx genex texture "dirt ground" --terrain    # seamless, for ground planes
```

Saves EVERY map into `./assets` as its own file, one line each, labelled by role:

```
✓ Done — 3 files saved to your project:
  assets/stone-floor-tiles-a1b2c3d4-basecolor.png  (2.1 MB)
  assets/stone-floor-tiles-a1b2c3d4-normal.png     (1.8 MB)
  assets/stone-floor-tiles-a1b2c3d4-roughness.png  (900 KB)
```

Load each map into the matching material slot and set the wrapping mode to
repeat — the file names carry the role, so the mapping is unambiguous.

## Options

- `--terrain` — a seamless tiling surface, for ground and large planes. Use it whenever the texture repeats across something big.
- `--out-dir <dir>` — where the files land (default `./assets`).
- `--no-download` — print the URLs only.
- `--no-wait` — enqueue and return; pick it up with `npx genex wait <id>`.

## Cost

From **9 credits** for the whole set (1 credit = $0.01). Live prices and
your balance: `npx genex doctor`.

## Waiting

`--no-wait` returns an id; `npx genex wait <id>` picks it up and never bills.
**Re-running the texture command bills a NEW set.**

## Troubleshooting

- **The surface shows a visible repeating grid** — the CLI measures the seam automatically and warns when it is bad. Re-generate with `--terrain`, or scale the repeat down so the tile is smaller on screen.
- **Out of credits** — Studio keeps the generation's card, which says so and offers Get credits. Never relay the balance, price or refill date, and don't retry.
- **Anything else** — `npx genex doctor`.
