---
name: minecraft-build-design
description: >-
  Design Minecraft Java Edition builds that paste straight into the player's own world. Reads the real terrain
  (singleplayer saves, servers cached with Voxy or Bobby, an area saved with Litematica, or no site at all), finds the
  spot from coordinates, F3 info, screenshots or "next to my house", matches a style (the player's builds, photos, a
  named style), designs in Python with a tested toolkit and delivers a verified Litematica .litematic (+ .schem), an
  offline 3D preview page, a survival materials list and a placement guide in the player's language; optional
  real-client paste test and making-of video. Use it whenever someone wants anything designed or built in Minecraft -
  house, base, tower, bridge, castle, garden, farm, statue, terraforming, schematic, 投影, 原理图, 建筑设计, 帮我盖,
  设计一个, 房子, 小屋, 塔, 桥, 亭子, 城堡, 花园, 地形改造, 预览, 材料清单 - even from one screenshot and one sentence.
  Not for mods, datapacks, redstone engineering or Bedrock Edition.
license: MIT (LICENSE.txt; third-party notices in THIRD_PARTY_NOTICES.md)
compatibility: >-
  Needs a shell and Python 3.10+ with numpy and Pillow (pip install -r scripts/requirements.txt). Optional: Java 17+
  for Voxy caches, JDK 21 + Litematica for the real-client test, Playwright for preview screenshots, ffmpeg + edge-tts
  for video. Works offline on Windows, macOS and Linux; block data for Minecraft Java 1.21.11 is bundled.
metadata:
  version: "2.0.0"
  author: "yimeng-YM"
  repository: "https://github.com/yimeng-YM/minecraft-build-design"
  toolkit: "mcbuild"
  minecraft: "Java Edition 1.21.11 data; schematics also load in newer versions"
---

# Minecraft build design

Deliver a build the player can paste into their real world and that looks and works right there:
**cheap intake → real site data → decisions written down → design in code → automatic checks → deliverables**.
Everything mechanical lives in the bundled toolkit (`scripts/mcbuild`); your job is the questions, the decisions and
the design.

## Running the toolkit

`<skill>` below means the folder that contains this file. Commands run from any folder:

```bash
python <skill>/scripts/mcb.py <command> -p <project folder>     # "python3" on macOS/Linux if "python" is missing
```

- First time in an environment: `mcb doctor` (≈ 5 s, read-only). It prints the saved player profile, what works here
  (textures, screenshots, Voxy, in-game test, video) and the exact fix for anything missing. If numpy/Pillow are
  missing: `python -m pip install -r <skill>/scripts/requirements.txt`. Optional extras are listed in
  `scripts/requirements-optional.txt`; install them only when a step needs them and the user agrees.
- `mcb selftest` proves the install end to end in ~5 s (no game needed).
- Commands: `doctor · config · fetch · selftest · init · find-data · site · map · analyze · style · camera · design ·
  draw · export · verify · materials · preview · shots · ingame · release · all · video · blocks · facts` - see
  [references/api.md](references/api.md). Negative numbers after an option need `=`: `--box=-420,-330,-200,-150`.
- Write multi-line files (design.py, notes) with your file-editing tool, not shell heredocs; use absolute paths.
- Reply to the player in their language. Set the project language once (`mcb init --lang zh|en`); the guide,
  preview page, materials list and image labels follow it.

## 0 · Profile check, then one round of questions

Questions are cheap; wrong guesses, disk searches and screenshot camera fitting are expensive. So, before any heavy
step:

1. Run `mcb doctor --brief`. The **profile** (`~/.mcbuild/config.json`) may already hold the game folder, language,
   launcher, version and notes from earlier jobs - don't ask for those again.
2. Read the request and attachments, then ask **one** short message covering only what is missing and matters (use
   the templates in [references/intake.md](references/intake.md), in the player's language, with defaults the player
   can accept with one word). Typical first-time items:
   - **What**: type, purpose, rough size (small/medium/large or W×D), style or "you choose", survival or creative.
   - **Where**: the cheapest exact answer is to stand on the spot, look at it and press **F3+C**, then paste the copied
     text (`/execute in minecraft:overworld run tp @s x y z yaw pitch`); or a screenshot taken **with F3 open**; or
     coordinates; or "no fixed place" (portable build).
   - **Which world**: singleplayer → its folder (Singleplayer → select world → Edit → Open World Folder); server → do
     they have **Voxy** or **Bobby** installed, or can they save the area with **Litematica** (Area selection → Save
     schematic, plus the selection origin's coordinates)?
   - **Game folder & version** (only if needed and unknown): in game Options → Resource Packs → Open Pack Folder, then
     one folder up; the version is on the top-left line of F3. Do they have Litematica (to paste)?
3. Save stable answers so the next job asks nothing: `mcb config add game_dirs <folder>`,
   `mcb config set lang zh`, `mcb config set launcher HMCL`, `mcb config add notes "base at -360 64 -270 on server X"`.

If the request already answers enough, skip the questions: pick sensible defaults, state them in the brief and in your
reply, and go. Ask again later only when a wrong guess would waste the whole job (two far-apart candidate sites, a
style you cannot infer at all). Never search whole drives unprompted - `mcb find-data` checks the profile and known
launcher folders; `mcb find-data --scan auto` (bounded, ~10 s) is for when the player cannot tell you.

Then create the project and keep everything inside it: `mcb init <folder> --name … --id AsciiId --source
voxy|anvil|schematic|flat|none --lang … --images <attachments>` (copies attachments into `input/` right away -
uploaded files can be temporary), and write `artifacts/brief.md`: one line each for where, data, what, size, style,
deliverables, constraints, with the defaults you chose.

## 1 · Site data  ([references/site-and-location.md](references/site-and-location.md))

- `[site]` in `project.toml`: `voxy` (server/world cache), `anvil` (save folder, or a Bobby/backup region folder),
  `schematic` (an area the player saved), `flat`/`none` (no site → portable build). Then `mcb site` →
  `site.npz` + `site-map.png`.
- Read a generous box: the build + 40–80 blocks of context; y from below the deepest foundation to above the tallest
  neighbour. Missing Voxy sections mean the player never visited there - ask them to fly over it.
- Everything is read-only: never write to the player's saves, caches, mods or server.

## 2 · Locate

- **F3+C text / F3 screenshot** → `mcb camera set --f3 "<text>" [--image input/image1.png --fov 70]`: exact camera,
  no fitting; the screenshot's centre (crosshair) is `mcb camera ray`. "Targeted Block" from F3 is the spot itself.
- **Coordinates** → use them; check with `mcb map --mark=x,z,label`.
- **Screenshot without F3** → `mcb camera fit` on 6+ recognisable features, then `outline` / `ray` (slow; prefer
  asking for F3 first).
- **Map screenshot** (Xaero, JourneyMap, web map) → `mcb map` the same area and match shapes.
- **"Next to my house" / landmarks** → `mcb analyze` lists player-built clusters with their blocks; Xaero waypoints
  (`find-data`) often name the base.
- **Nothing** → `flat`/`none`, portable schematic the player places.
Record the origin, facing and reasoning in the brief.

## 3 · Analyse the site and decide the concept

`mcb analyze --footprint WxD` (ground, slope, water, existing builds, flat candidates) and `mcb map` close-ups.
Decide footprint and orientation (entrance toward the approach, views toward water/valley), how it meets the ground
(pad, plinth, stilts, terraces, pier - [references/design-guide.md](references/design-guide.md)) and what must not be
touched (`mcb verify` warns when the design overwrites player blocks). Style
([references/style.md](references/style.md)): reference build → `mcb style --box=…`; photos → materials and
signature elements; named style → palette table; nothing → derive from biome and neighbours, keep a small palette,
and say it is your choice.

## 4 · Design in code  ([references/api.md](references/api.md))

`design.py` builds `B = Build(P.site())` with frames `F = B.frame(origin, turns)`; design in a canonical orientation
and rotate with `turns` (block states rotate too). Use `shapes` and `nature`; keep all materials in one `PAL` dict.
Loop: `mcb design` (rules pass + drawings) → `mcb export` → `mcb verify` → `mcb preview --shots` → look at the
images (drawings first, then 3–5 shots: overview, front, eye level, a cut-away, the player's own viewpoint) → fix →
repeat. Check silhouette from afar, depth (no flat walls), night lighting, how people walk in.

## 5 · Verify  ([references/delivery.md](references/delivery.md))

`mcb verify` must PASS: file decoded independently, every state valid, design == file, vanilla neighbour rules,
support (torches, lanterns, plants, doors …), water containment, every spawnable surface lit, walk test from
`walk_start` to every `walk_targets` entry, floating parts, overwritten player blocks. Errors are real design flaws
(dark attic, doorway into a railing) - fix the design, don't silence the check.
Optional real-client test for site builds: `mcb ingame` opens a Minecraft window for a few minutes (needs JDK 21 and
Litematica + MaLiLib jars; `mcb doctor` says if it is possible). Ask before running it.

## 6 · Deliver

`mcb materials && mcb preview --shots && mcb release` → `release/`: the `.litematic` (+ `.schem`), the preview page,
the materials CSV, screenshots and the guide (使用说明.md / README.md). In the reply (player's language, concise):
what was built and why (location, orientation, style, deviations), the placement origin or how to place it, the
paste setting (**Litematica `pasteReplaceBehavior` = With non-air** for site builds, **All** when the design clears
trees/terrain), verification results with numbers, what was *not* checked, and file links. Offer to copy the
schematic into their `schematics` folder (new file name, never overwrite). Video on request:
[references/video.md](references/video.md).

## When the environment is limited

- **No game files here** (cloud sandbox, game on another computer): the kit still designs, exports and verifies;
  previews use block shapes in map colours (`mcb fetch client` gets real textures if the user agrees to a ~30 MB
  download from Mojang). For real terrain, ask the player to upload a zipped save, a Bobby region folder or a
  Litematica area schematic - or build portable.
- **No screenshots** (no Playwright): look at the drawings (`artifacts/drawings/*.png`) instead and say so.
- **Other game versions**: bundled data is 1.21.11; schematics load in newer versions. For older versions avoid
  blocks newer than theirs and tell them - see [references/setup.md](references/setup.md).
- Downloads (`mcb fetch …`), installs and opening a game window always need the user's OK first; `mcb fetch` refuses
  without `--yes`.

## Scale tiers

| Tier | Blocks | Adjust |
|---|---|---|
| small | < 2k | one design file; in-game test is quick |
| medium | 2k–30k | parts per wing/floor (`B.cur`), sub-regions follow parts |
| large | 30k–300k | modules/functions; `max_region = 64`; smaller preview `context`; staged schematics for survival |
| huge | > 300k | sector schematics, build-order guide, showcase world instead of only previews; several sessions |

## Rules of thumb

- Real data over guesses: heights, water, neighbours and the player's materials come from the world, not from pictures.
- Never overwrite player-built blocks unless asked; never modify their saves, caches or mods; only add new files.
- Light everything (attics, roofs, gardens), make every room reachable, keep doors and stairs clear.
- Write decisions down (brief, `B.notes`, `[release] notes`); explain deviations and how to change them.
- When something fails, read the log, fix the cause, re-run; report honestly what was and wasn't verified.

Further reading: [references/intake.md](references/intake.md) (questions, where things are per launcher),
[references/setup.md](references/setup.md) (install, profile, downloads, versions, sandboxes),
[references/workflow.md](references/workflow.md) (step-by-step commands), [references/pitfalls.md](references/pitfalls.md),
[references/examples.md](references/examples.md).
