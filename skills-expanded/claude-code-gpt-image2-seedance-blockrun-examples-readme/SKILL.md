# Demo assets

This directory holds the curated demo outputs that the README and
SKILL.md files reference. Files here are the **public face** of the
project — they should be high-quality real outputs, not mockups.

## Shipped

| Path | What | Sourced via |
|---|---|---|
| `cover.jpg` | The 360-tile README hero mosaic | `scripts/` cover build |
| `pizza-collab/01-storyboard-establishing.jpg` | Storyboard 1 — the queue outside Crust & Company | `/poster`-style GPT Image 2 call, 1024×1024 |
| `pizza-collab/02-storyboard-action.jpg` | Storyboard 2 — pizza handed over, USDC into the BR terminal | same run, shot 2 |
| `pizza-collab/03-storyboard-finale.jpg` | Storyboard 3 — CC × BR high-five | same run, shot 3 |
| `pizza-collab/seedance-action.mp4` | Storyboard 2 animated — 5s · 24fps · 1280×720 | Seedance, seeded with frame 2 |
| `pizza-collab/seedance-action.gif` | README-embeddable loop of the same clip | `ffmpeg` palettegen, 420px · 12fps · 2.5 MB |

The `pizza-collab/` set is a single end-to-end run of this bundle — stills first,
then one of them animated — and is the honest answer to "what does this actually
produce?" No retouching beyond PNG→JPEG and the GIF downscale.

## Planned demo assets (not yet shipped)

> The README gallery also renders from remote raw URLs and the `case-library/`,
> so nothing below is required for install — generate these when refreshing the
> public demos.

| Path | What | Sourced via |
|---|---|---|
| `headshot/before-after.gif` | A 4-style before-after grid (one input photo, four polished outputs at corporate/creative/startup/actor) | `/headshot ./examples/_inputs/founder.jpg --all` |
| `dance/dance-hero.gif` | The single most viral 5-second dance clip — Day-1 Twitter hero | `/dance ./examples/_inputs/founder.jpg --style tiktok-trend`, then `ffmpeg` to GIF |
| `dance/dance-3styles.gif` | Three styles side-by-side (hiphop / ballet / terracotta-disco) | three runs of `/dance` + `ffmpeg` hstack |
| `poster/poster-grid.jpg` | 4 genres in one 2x2 grid | four `/poster` runs + image grid compose |
| `gallery/*.{jpg,gif}` | 16+ real outputs picked from `prompts/case-library/` | run the linked cases via the bundle's commands |

## Conventions

- Keep individual GIFs under 5 MB so the README renders fast on GitHub.
- All hero assets are real outputs — no Photoshop touch-ups beyond
  cropping / grid composition.
- Source images for human portraits should be of the founder team or
  consenting collaborators only.
- Caption every gallery thumbnail with the underlying command in
  `prompts/case-library/<slug>.md` so users can run it themselves.

## Generating these

The `_inputs/` subdirectory (gitignored) holds the source photos. Use
the bundle's commands from this repo's root to produce the outputs, then
move/rename them under the paths above. A future `scripts/build_demos.sh`
will wrap this for repeatable launch refreshes.
