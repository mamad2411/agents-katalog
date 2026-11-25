# Genex models in AI Game Studio

You are building inside AI Game Studio. Below the upstream marker is Genex's model card,
with the passages of advice Studio does not ship taken out. Where it disagrees with this preface,
this preface wins.

- Run every command through `genex__asset`, never `npx genex`. `npx genex model "<prompt>"
  --auto-size --low-poly` is `genex__asset {"operation":"model","prompt":"<prompt>","options":
  {"auto-size":true,"low-poly":true}}`. A flag's value is the option's value
  (`"face-limit":20000`); `image` names an image file inside this game.
- `model import <file>` is operation `model.import` with the game file as `prompt`. `model
  segment`, `model rig` and `model animate` are `model.segment`, `model.rig` and `model.animate`,
  with the generation id as `id`.
- Studio submits every create without waiting and delivers the files into the game: never pass
  `out-dir`, `no-wait`, `no-download` or `json`. Pick a result up with operation `wait` and its
  generationId; operation `status` lists your jobs in place of `wait --all`.
- This lane is Tripo, and Studio has no provider option. A rigged character or creature is the
  character card's lane (Meshy).
- Pass `auto-size` whenever the model's real size matters: without it the model is not to scale.
  Its meshes are dense (150000 faces by default); `low-poly` and `face-limit` lower the count.

<!-- upstream @genex-ai/cli-demo/templates/skills/genex-tool-model/SKILL.md v1.40.0 sha256 849485e095d91b019e09dda27123c33297889cf732b219772eb075b5373f4771 -->
---
name: genex-tool-model
description: Generate a 3D model (GLB) from a text prompt or a reference image with `npx genex model` — props, vehicles, weapons, furniture, environment pieces, anything the scene needs as geometry. Also splits a model into named parts, rigs any mesh across 7 body plans, and retargets ready-made animation clips onto that rig. Files download to ./assets.
---

# Genex Tools · Model

Props, vehicles, weapons, buildings, set dressing — anything the scene needs as
real geometry. Output is a standard GLB that loads in any engine.

For a character or creature with a skeleton and animations, use
`$genex-tool-character` instead; this lane is for objects.

## Run

```bash
npx genex model "wooden barrel with iron bands"
npx genex model --image ./reference-photo.jpg       # build it FROM an image; prompt optional
```

Blocks until ready, saves the GLB into `./assets`, and prints the path. Wire the
local path; the URL printed beside it is provenance, not hosting.

## Bring your own mesh

```bash
npx genex model import ./hero-cart.glb           # free — a file you already have becomes a model of yours
```

`.glb` only, ≤ 64 MB (export a `.gltf`/FBX as one binary `.glb` first). The
import is free and checked before it completes; after it, `segment`, `rig`,
`animate` and `character import` all take its id. **Never rebuild a mesh the
user hands you** — import it.

## Mesh lanes

Each takes the **generation id** of a previous model — never a URL.

```bash
npx genex model segment <model-id> --granularity balanced
npx genex model rig <model-id> --type quadruped
npx genex model animate <rig-id> --preset walk,run
```

- **`segment`** — one GLB split into addressable parts: doors, turrets, magazines, destructibles. `--granularity simple|balanced|detailed`. The parts are named by index (`tripo_part_0`, `tripo_part_1`, …), not by what they are — find the one you want by its bounds (the sails are the part with the widest extent, the door the lowest thin one), then keep that index.
- **`rig`** — a skeleton for any mesh, across 7 body plans: `biped`, `quadruped`, `hexapod`, `octopod`, `avian`, `serpentine`, `aquatic`. The plan is auto-detected; `--type` picks it. A mesh that cannot be rigged is refused and refunded before the paid step.
- **`animate`** — retarget ready-made clips onto a rig, billed per clip. biped: `idle|walk|run|dive|climb|jump|slash|shoot|hurt|fall|turn`; quadruped/hexapod/octopod: `walk`; serpentine/aquatic: `march`.

## Options

- `--image <path|url>` — build the model from a reference image (local file ≤ 4 MB, or a previous generation's URL). The prompt becomes optional.
- **Quality knobs** (Tripo H3.1, each priced in the quote): `--texture standard|detailed|none` (detailed default, +10 over standard; none = geometry only), `--geometry detailed` (+20), `--quad` (+5, for meshes you will edit; face limit ≤150000), `--low-poly` (+10, game-ready topology for props in numbers — it holds `--face-limit` to 1000-20000, 500-10000 with `--quad`; omit the flag to take 20000; it runs a post-process after the mesh, so allow up to 30 minutes), `--parts` (+20, named parts at generation), `--face-limit <n>` (1000-2000000, default 150000; see `--low-poly` for its band), `--auto-size` (real-world metres).
- `--out-dir <dir>` — where the file lands (default `./assets`).
- `--no-download` — print the URL only.
- `--no-wait` — enqueue and return; pick it up with `npx genex wait <id>`.

## Cost

From **35 credits** a model (**46** from a reference image; `--texture standard`
**23**, `--geometry detailed` **58**, `--low-poly` **46**, `--parts` **58**) ·
**46** segment · **29** rig · **12 per clip** for animate (1 credit = $0.01).
Live prices and your balance: `npx genex doctor`.

## Waiting

Models take the longest of any lane. `--no-wait` is the normal way to run
several at once: enqueue them all, keep building, then `npx genex wait --all`
for one status line each — in a tools workspace it also downloads every
finished model that is not in `./assets` yet, so one call after a break (or a
restarted session) delivers the whole batch. `npx genex wait <id>` picks one
up. **Re-running the model command bills a NEW model** — never use it as a
status check. Five or so in flight at a time is the provider's comfortable
concurrency; a burst beyond that waits on the server side rather than failing.

## Moving parts

For models that need moving parts, use `--parts` during generation or
`genex model segment <id>` to split an existing model. Inspect the resulting
pieces, set their pivots, and animate them. Simple moving parts can also be
built in code.

## Placing a model

A generated GLB has no shared "front": one building's door faces −x, the next
one's +z. Do not guess and do not spend a render per side — read the mesh once
on load (bounding box, and where the detail is: the door, the counter, the
opening) or check it in a viewer, then record a per-model `front` (a yaw)
beside its path and apply it when you place it. Ask for a facing
in the prompt too (`"…front toward +Z"`) — it helps, it does not guarantee.

## Troubleshooting

- **Out of credits** — Studio keeps the generation's card, which says so and offers Get credits. Never relay the balance, price or refill date, and don't retry.
- **The rig was refused** — that mesh has no usable skeleton for any body plan. It is refunded.
- **Repeated failures in this folder** — the CLI says so after the second one. That pattern is the lane, not your prompt.
- **Anything else** — `npx genex doctor`.
