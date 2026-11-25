# Genex images in AI Game Studio

You are building inside AI Game Studio. Below the upstream marker is Genex's image card,
with the passages of advice Studio does not ship taken out. Where it disagrees with this preface,
this preface wins.

- Run every command through `genex__asset`, never `npx genex`. `npx genex image "<subject>"
  --transparent` is `genex__asset {"operation":"image","prompt":"<subject>","options":
  {"transparent":true}}`. `edit` and `inpaint` name image files inside this game; `clean` and
  `upscale` take a Genex asset URL.
- `open` and `glass` are not available in Studio, and neither are `out-dir`, `no-wait` or
  `no-download`: Studio submits every create without waiting and delivers the file into the
  game. Pick it up with operation `wait` and its generationId.

<!-- upstream @genex-ai/cli-demo/templates/skills/genex-tool-image/SKILL.md v1.40.0 sha256 6c759be788c22aee35b9327a92efe1da5c41f4401e5f2aa7dbf4e71f29fb2995 -->
---
name: genex-tool-image
description: Generate a real image (PNG/JPEG) from a text prompt with `npx genex image` — posters, signs, logos, sprites, icons, card and item art, loading screens, decals, art for in-game screens. Pass `--transparent` for an alpha channel, `--edit` to modify an existing image, `--remove-bg` to cut a background. The file downloads to ./assets and is yours.
---

# Genex Tools · Image

Wherever the project needs a picture, this is the tool. Any style, any subject,
any aspect. It is also the tool for editing an image you already have.

## Run

```bash
npx genex image "wooden sign with iron brackets"
npx genex image "chalk graffiti tag" --transparent    # alpha channel — sprites, icons, logos
```

Blocks until ready, saves the file, and prints where it went:

```
✓ Done — 1 file saved to your project:
  assets/wooden-sign-with-iron-brackets-a1b2c3d4.png  (1.2 MB)
  source of record (provenance, not hosting): https://assets.genex.technology/...
```

Wire the **local path**. The URL is provenance — never fetch it at runtime.

## Options

- `--transparent` — real alpha channel. Use for sprites, icons, logos, decals, anything that sits on top of the game rather than inside a frame. Combines with `--quality` and `--size`: a hero wordmark can ask for `--quality high` on an exact canvas, while a plain sprite is fine on the default mid tier. Not with `--candidates` — this lane cuts the background after generating and that is billed per image, so generate candidates with `--quality`/`--size`, pick one, then cut it with `--clean <url>`.
- `--edit <path|url>` — modify THIS image with the prompt. Takes a local file (≤4 MB) or a previous generation's URL, so a reference screenshot goes straight into the chain.
- `--inpaint <mask>` — with `--edit`, a PNG mask whose TRANSPARENT hole is the region to change. Targets where the edit lands; the whole image still re-renders and alpha is destroyed, so re-run `--remove-bg` afterwards if you need it.
- `--remove-bg` — cut the background after generating or editing.
- `--bg-mode <sprite|glyph|sheet|matte>` — which removal model. `matte` gives soft alpha for hair, glow and smoke edges.
- `--clean <url>` — remove the background of an existing image, no generation.
- `--upscale <url>` — 2× an existing image.
- `--aspect <ratio>` · `--size <WxH>` · `--quality <low|medium|high|xhigh|max>` — framing and fidelity (GPT Image 2.5 tiers; `xhigh` and `max` are for hero art and cost the most).
- `--candidates <2-4>` — several variants in ONE call, so you pick instead of re-rolling. Needs `--quality` or `--size`.
- `--open` — also open it in a browser, for something the user must look at and approve.
- `--out-dir <dir>` — where the file lands (default `./assets`).
- `--no-download` — print the URL only, save nothing.
- `--no-wait` — enqueue and return; pick it up later with `npx genex wait <id>`.

## Cost

From **7 credits** per image at the default high quality (1 credit = $0.01);
`--quality xhigh`, `--quality max` and 4K canvases cost more, `--quality low`,
`--quality medium` and `--transparent` cost less, and `--candidates` bills per
variant - the command prints the exact quote. Live prices and your balance:
`npx genex doctor`.

## Waiting

`--no-wait` returns a generation id immediately. Attach to it with
`npx genex wait <id>` — that never bills. **Re-running the image command creates
(and bills) a NEW image**, so never use it to "check on" one that is running.

## Troubleshooting

- **Out of credits** — Studio keeps the generation's card, which says so and offers Get credits. Never relay the balance, price or refill date, and don't retry.
- **"Email not verified"** — the printed link unlocks the free credits; generation works right after.
- **Anything else** — `npx genex doctor` reports sign-in, credits, and whether the image lane is live on this account.
- A prompt that keeps producing the wrong thing is a prompt problem, not a lane problem — name the subject, the medium and the framing concretely ("a wooden crate, studio photo, three-quarter view"), rather than adding adjectives. Put the subject first and say what you want, never what to leave out: the image model reads the opening words hardest and does not take negative prompts.
