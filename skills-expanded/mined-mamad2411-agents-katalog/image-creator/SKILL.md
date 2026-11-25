---
name: image-creator
description: >
  Generates images (and videos) for a project's missing/fallback assets using the best of
  three APIs, with automatic fallback. Routes TRANSPARENT-background images (logos, mascots,
  icons, sprites, UI frames) to OpenAI gpt-image-1.5, NORMAL/photographic images (backgrounds,
  hero art, banners, scenes) to Google Gemini "Nano Banana", and VIDEO (animate a still,
  text-to-video) to Kling AI. Reads a project's prompts.md, generates each asset, writes it
  to the expected path in the correct format, and tracks estimated spend. Use when a user asks
  to create/fill image or video assets for a project.
---

# image-creator agent

You create the images (and videos) a project is waiting on. Typical job: the user opens a
session, points you at THIS skill **and** at a target project's `prompts.md` (or a single
prompt), and says "create these and drop them at the right paths." You decide the provider per
asset, run `imagegen.py`, and place each file with the correct extension. Every run logs an
estimated cost so you (and the user) can watch spending.

## The three engines (and why the split)

| | OpenAI `gpt-image-1.5` | Gemini `gemini-2.5-flash-image` ("Nano Banana") | Kling AI |
|---|---|---|---|
| **Transparency (alpha PNG)** | ✅ native (`background="transparent"`) | ❌ none | ❌ none |
| Best at | clean isolated subjects, logos, icons, sprites, cut-outs; strong text rendering | photorealism, scenes, lighting, **iterative editing**, character consistency, fusion | **VIDEO**: image→video, text→video, motion/physics, lip-sync, virtual try-on |
| Image cost (≈1024², high) | ~$0.13/img | ~$0.039/img (cheapest) | ~$0.01/img |
| Video | ❌ | ❌ | ✅ ~$0.07–0.14 / second |
| Watermark | none | invisible SynthID | — |

> ⚠️ `gpt-image-2` (OpenAI's flagship) does **NOT** support transparency — that's why the
> transparent route pins `gpt-image-1.5`. **Gemini and Kling have no alpha at all** — anything
> needing a transparent background MUST go to OpenAI.
> Kling's real strength is **video**, not still images — reach for it when the project wants
> motion (animated hero, looping background, product spin), not just a static picture.

## Fallback chain (automatic)

With `--provider auto` (the default), `imagegen.py` picks a capability-ordered chain and
falls through if a provider has no API key or its call fails (no credit, rate limit, error):

- **Transparent image** → `[openai]` only. No fallback exists — Gemini/Kling can't do alpha.
  If `OPENAI_API_KEY` is missing it errors and says so.
- **Opaque image** → `[gemini → openai → kling]` (cheap & photoreal first, then capable, then Kling).
- **Video** → Kling only.

Force a single provider (no fallback) with `--provider openai|gemini|kling`.

## Decision matrix — pick the provider with these rules

1. **Does the asset need a transparent background?** → **OpenAI** (`--transparent`).
   Tells: prompt says "transparent", "isolated", "cut-out", "for app icon", "sprite",
   "PNG with alpha"; or the asset is a logo / mascot / icon / UI frame / character cutout;
   or the target extension is `.png` AND it overlays other content.
2. **Otherwise it's a normal raster image** → **Gemini** (`--opaque`, the default).
   Tells: backgrounds, hero/landscape art, news banners, textures, photographic scenes,
   anything with a full-bleed background. Cheaper and stronger at photorealism/scenes.
3. **Editing an existing image** (add/change something on a given image)? Pass `--ref`.
   - Need the edit to stay transparent → OpenAI.
   - Photographic edit / relight / add element on opaque art → Gemini (its strength).
4. **`.svg` requested?** Neither API outputs vector. Generate a clean raster (transparent
   PNG via OpenAI at the largest sensible size) and tell the user it must be traced/vectorized
   separately. Never silently save a `.png` as `.svg`.
5. **Format from the project's filename**: `.png` (keep alpha), `.jpg/.jpeg` (opaque, Gemini),
   `.webp` (either). Match exactly what the project expects.

When unsure between the two for a borderline case, prefer the rule above on transparency;
if still ambiguous, ask the user briefly.

## How to run

Use `uv` (auto-installs deps from the script's inline metadata — no venv setup needed):

```bash
# transparent logo -> OpenAI
uv run agents/image-creator/imagegen.py generate \
  --prompt "<full prompt>" --out client/assets/logo.png --transparent --aspect 1:1

# opaque hero background -> Gemini (default)
uv run agents/image-creator/imagegen.py generate \
  --prompt "<full prompt>" --out client/assets/hero.jpg --opaque --aspect 16:9

# edit an existing image (add element), keep it photographic -> Gemini
uv run agents/image-creator/imagegen.py generate \
  --prompt "raise the right arm in a wave" --ref mascote.png --out mascote-aceno.png --opaque

# force a provider / pick a different model
uv run .../imagegen.py generate --prompt "..." --out x.png --provider openai --model gpt-image-1.5

# VIDEO via Kling — animate a still (image2video)
uv run .../imagegen.py video --prompt "camera slowly pushes in, gentle wind" \
  --ref hero.png --out hero.mp4 --duration 5 --kmode pro

# VIDEO via Kling — text2video (no --ref)
uv run .../imagegen.py video --prompt "drone shot over a canyon at sunset" \
  --out clip.mp4 --aspect 16:9 --duration 5

# spending so far (today / last 7 days / all-time, by provider)
uv run .../imagegen.py usage

# BATCH — generate a whole project from a JSON manifest (deterministic, low-token)
uv run .../imagegen.py batch --manifest assets.json --base-dir client/
```

### Batch mode (prefer this for multi-asset jobs)

Don't hand-write a shell loop of 20 `generate` calls — that burns tokens and drifts.
Instead write ONE small JSON manifest and let the script do the routing, generation,
cost logging, **auto-backup**, retries-by-rerun, and a summary table. The model only
authors the manifest; everything mechanical stays in code.

Manifest = a JSON list (or `{"assets": [...]}`). Per item only `out` + `prompt` are
required; the rest default (`transparent:false`, `aspect:"1:1"`, `provider:"auto"`,
`quality:"high"`). Relative `out` paths join `--base-dir`.

```json
[
  {"label":"icon","out":"assets/icon.png","prompt":"...","provider":"gemini","aspect":"1:1"},
  {"label":"logo","out":"assets/logo.png","prompt":"...","transparent":true,"aspect":"3:2","ref":"brand/logo.png"},
  {"label":"home-hero","out":"assets/images/home-hero.png","prompt":"...","transparent":true,"ref":"brand/mascot.png"}
]
```

Generation continues past per-asset failures; the run ends with a
`BATCH SUMMARY (N/M ok)` table and the usage breakdown. Re-run the same manifest to
retry only what you trim it down to.

`generate` flags: `--transparent|--opaque` (default opaque) · `--provider auto|openai|gemini|kling`
(auto = capability chain + fallback) · `--aspect 1:1|16:9|9:16|3:4|4:3|...` · `--quality
low|medium|high` (OpenAI) · `--image-size 1K|2K|4K` (Gemini-3 only) · `--ref <img>` (edit) ·
`--model <id>` · `--json` · `--ref` is **repeatable** for multi-image fusion
(`--ref pose.png --ref face.jpg`) — pass it twice to do a **face-swap**: first ref = the
original image (pose/clothes/lighting to keep), second ref = the real person's face. Works on
OpenAI (keeps alpha) and Gemini (photoreal). The `remodeling` agent uses this.

`video` flags: `--prompt` · `--out *.mp4` · `--ref <img>` (omit → text2video) · `--aspect` ·
`--duration 5|10` · `--kmode std|pro` · `--model`.

## Cost tracking

Every `generate`/`video` run appends an estimated cost to a local ledger
(`agents/image-creator/.usage/ledger.jsonl`, gitignored) and prints a running line:
`~$0.039 (est) via gemini | today ~$0.04 | 7d ~$0.04 | all-time ~$0.04`. Run
`imagegen.py usage` any time for the today / 7-day / all-time breakdown by provider.
Costs are **estimates** — providers bill by tokens/seconds/credits and prices drift;
treat the numbers as a spend gauge, not an invoice. When batch-generating, report the
running total to the user so they can stop if it climbs.

## Automatic backups (every asset, outside the repo)

After each successful `generate`/`video`, `imagegen.py` copies the written file to a
backup folder that lives **outside the target project's main repo**, so a stray
`git clean`, checkout, or sandboxed write can't lose the art. It prints a second line:
`backup -> <path>`.

- **Default layout:** `<repo_parent>/_asset-backups/<repo_name>/<path-relative-to-repo>`.
  Example: `hey-ania/assets/images/home-hero.png` →
  `…/Repositórios/_asset-backups/hey-ania/assets/images/home-hero.png`.
- The repo root is found by walking up to the nearest `.git`. If the output isn't inside
  a git repo, backups go to a sibling `_asset-backups/` next to the file.
- **Override the root:** set `IMAGEGEN_BACKUP_ROOT=/some/dir` (assets land under
  `<root>/<repo_name>/…`). **Disable:** `IMAGEGEN_BACKUP=0`.
- Backups never block a generation — a copy failure only prints a `WARN`.

## Workflow when given a project's prompts.md

1. Read the project's `prompts.md` and any `DESIGN.md` for palette/style. Note the
   "master style suffix" and negative prompt — **append the master style** to each prompt.
2. Build the full asset list: for each, apply the **decision matrix** and record
   `{label, out, prompt (with style appended), aspect, transparent?, provider?, ref?}`.
   Infer the target path from the project layout (e.g. its assets dir) — confirm with the
   user if the destination isn't obvious.
3. Write these as ONE JSON manifest and run `imagegen.py batch --manifest … --base-dir <repo>`
   — it generates, costs, **backs up**, and prints a summary in a single low-token call.
   (Only drop to per-asset `generate` for a one-off or a targeted re-roll.)
4. Read the `BATCH SUMMARY` table. Re-run a trimmed manifest for any failures (safety blocks
   or rate limits) with a tweaked prompt or backoff.
5. Don't burn budget: generate at `--quality high` for finals, but if iterating on a look,
   draft at `low` first.

## Gotchas

- **Aspect ratios**: OpenAI snaps to 1024²/1536×1024/1024×1536; Gemini & Kling honor the exact ratio.
- OpenAI image endpoints need **org verification** (403 otherwise). Gemini free tier ≈ 500 req/day.
- Failed/blocked OpenAI prompts still consume quota — fix prompts before retry-storming.
- **Kling**: needs a prepaid resource pack — a `429` means no active credit/quota (not an auth
  problem). JWT auth is minted per call (30-min expiry). Video is async (~30–120s) and billed by
  the second — keep clips short while iterating. Result URLs are temporary; the script downloads
  immediately. No alpha output.
- Model names drift; if a call 404s, override `--model` or update `.env`. Defaults are pinned
  in `imagegen.py` and documented in `.env.example`.
