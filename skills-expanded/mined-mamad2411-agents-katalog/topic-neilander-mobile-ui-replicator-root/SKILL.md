# UI Replicator Skill — agent entry point

You (the agent) just got asked to turn a **UI screenshot** + **style reference image** + **a written description of the app's features** into a working **single-file HTML demo** painted in the style of the reference. This file tells you how.

You have three inputs from the user:
1. UI screenshot (file path) — the layout to replicate
2. Style reference image (file path) — the visual language to apply
3. **Feature description** (text in chat, or a `.md`/`.txt` file) — what the app does and what each section means. This is REQUIRED. If the user didn't supply one, ask before doing anything else (see Step 3 below).

Plus a project name. You produce a folder under `output/<name>/` containing `index.html` + `assets/`.

---

## Setup check (run once at the start)

```bash
# python deps installed?
python3 -c "import PIL, scipy, numpy" 2>/dev/null || \
  pip install pillow scipy numpy

# verify .env has real keys (not placeholders)
python3 scripts/load_keys.py
```

The skill ships with a `.env` file that has a placeholder value. If `load_keys.py` complains, stop and tell the user to open `.env` and paste in their real `GEMINI_API_KEY`. Don't try to proceed.

You (the agent) read the user's images directly via your own vision capability and write all JSON / HTML yourself — no Anthropic / OpenAI / etc. key is needed. The only key that goes through Python is `GEMINI_API_KEY`, used by `scripts/gen_image.py` for image generation. Pillow + scipy are only needed by `scripts/flood_fill.py`.

---

## The 5 steps

Always work in this order. Don't parallelize 1–3.

### Step 1 — Read the reference output

```
references/forest-journal.html
```

Open it and look at it. This is the quality bar for what you're about to produce. Pay attention to: paper grain texture, edge vignette, custom fonts, spring animations, colored tiles holding painted icons. You will refer back to this in Step 5.

### Step 2 — Extract the STYLE preamble

Read `prompts/style-extraction.md`. Look at the user's style reference image. Fill in the template's `<...>` slots with terse concrete observations. Save to:

```
output/<name>/style-preamble.txt
```

### Step 3 — Analyze the UI screenshot (using the feature description as ground truth)

Read `prompts/analyze-ui.md`. **First, confirm you have the user's feature description** (chat text, attached `.md`/`.txt`, or pasted block). If you don't, stop and ask the user for it using the template in `analyze-ui.md` — don't proceed by guessing what the screenshot shows.

Once you have both the screenshot and the description, produce:

```
output/<name>/layout.json     ← structure (titles/labels come from description, not your guesses)
output/<name>/assets.json     ← per-asset prompts
```

Cross-check before continuing: every `*_ref` in `layout.json` resolves to an `id` in `assets.json`. If not, fix it. If the description and screenshot disagree on something significant, raise it with the user instead of silently picking one.

### Step 3.5 — Wireframe gate (DEFAULT ON, do NOT skip unless user says so)

Asset generation in Step 4 takes 1–3 minutes and burns ~10 Gemini calls. If the structure from Step 3 is wrong, that time and those calls are wasted. So before you fire any image generation, produce a fast structural preview and let the user confirm.

Read `prompts/wireframe.md`. Render `layout.json` + `assets.json` into:

```
output/<name>/wireframe.html
```

Pure CSS, no Gemini calls, no fonts loaded — just colored bordered boxes per section, dashed placeholders per image slot showing id/aspect/role/prompt, plus a top banner with palette swatches and a bottom asset list.

After writing it:
1. Run `open output/<name>/wireframe.html` (macOS) or print the absolute path so the user can open it.
2. Send the user a short summary and ASK for confirmation. Use the prompt block at the bottom of `wireframe.md`.
3. **Do NOT call `gen_image.py` yet.** Wait for the user's reply.

Possible replies:
- **"ok" / "继续" / "go"** → proceed to Step 4.
- **"改 X: ..." / structural change** → update `layout.json` / `assets.json` based on the feedback, regenerate `wireframe.html`, ask again.
- **"skip" / "直接全跑"** → user is overriding the gate; proceed to Step 4 without further wireframes. Honor this only when stated explicitly.

The wireframe gate is on by default. The user can also opt out from the start by saying "不用 wireframe" / "skip wireframe" in the initial request — in that case, go straight from Step 3 to Step 4.

### Step 4 — Generate the painted assets

For each asset in `assets.json`, call:

```bash
python scripts/gen_image.py \
    --prompt "<asset.prompt>" \
    --style "<user's style image path>" \
    --aspect "<asset.aspect>" \
    --style-preamble output/<name>/style-preamble.txt \
    --out output/<name>/assets/<asset.filename>
```

**`--aspect` is critical, do NOT skip it.** It's the only thing that controls the output dimensions. Without it, Gemini ignores any "Portrait 3:4" / "Square 1:1" hint in the prompt text and just inherits the style reference's shape — which is almost always wrong for the asset slot. Read the value straight from the asset's `aspect` field in `assets.json`.

Run them serially in a loop, OR fire 4 in parallel via `xargs -P 4` / `&`. Each call takes 5–15s. Total wall-clock for ~10 assets: 30–60s if parallel, 1–3min serial.

If a generation fails (the script exits non-zero), retry it once. If still failing, mark it in a brief log message and continue — Step 5 will report missing files.

After all assets are done, for any asset with `post_process: "flood-fill-bg"` (typically mascots, sometimes icons), call:

```bash
python scripts/flood_fill.py \
    --in output/<name>/assets/<filename> \
    --out output/<name>/assets/<filename>
```

This removes the painted background so the mascot sits transparently on the UI.

### Step 5 — Write the HTML

Read `prompts/scaffold-html.md`. Open `references/forest-journal.html` again.

**Strongly recommended: invoke the `frontend-design` skill for this step.** It handles the polish that separates "looks like a wireframe" from "looks shippable" — animation curves, spacing rhythm, typography pairing, micro-interactions. Pass it the layout.json, assets.json, the reference HTML, and `prompts/scaffold-html.md` as context.

```
Skill(skill="frontend-design", args="...")
```

If `frontend-design` isn't installed in your environment, fall back to writing the HTML yourself following `prompts/scaffold-html.md` — the result will work, just less polished. Don't fail the build over a missing skill.

Either way, the output is:

```
output/<name>/index.html
```

Then verify:
1. `ls output/<name>/assets/` matches every `<img src="assets/...">` in the HTML.
2. Open it in a browser. Phone frame is 390×844 with notch. Sections appear top-to-bottom in the right order. Images load. Console clean. Interactions (mascot drag, sheet pull) work.

If anything is broken, fix the HTML directly. Don't ask the user to fix things you can fix.

---

## Output layout (final state)

```
output/<name>/
├── index.html          ← the deliverable
├── assets/
│   ├── hero.png
│   ├── mascot.png      ← already flood-filled
│   ├── tool-*.png
│   └── card-*.png
├── style-preamble.txt  ← intermediate (Step 2), kept for re-runs
├── layout.json         ← intermediate (Step 3), kept for re-runs
└── assets.json         ← intermediate (Step 3), kept for re-runs
```

Keep the intermediates — they let the user (or you, on a follow-up turn) re-run a single asset without redoing the whole pipeline.

---

## Re-running just one asset

If the user says "regenerate the hero" or "the mascot looks wrong", read `assets.json`, find the asset by `id`, and re-run **only** Step 4 for that one asset. Don't redo Steps 1–3.

```bash
python scripts/gen_image.py \
    --prompt "$(jq -r '.assets[] | select(.id=="hero").prompt' output/<name>/assets.json)" \
    --style "<user's style image>" \
    --style-preamble output/<name>/style-preamble.txt \
    --out output/<name>/assets/hero.png
```

---

## What NOT to do

- **Don't invent assets that aren't in `assets.json`.** Every `<img>` must trace back to a generated file.
- **Don't bake text into images.** Text (titles, button labels, POI names, time, search placeholder) lives in HTML/CSS. Image prompts must say `no text, no letters, no numbers`.
- **Don't reach for external image URLs** (Unsplash, placeholder.com). The deliverable must work offline after the build.
- **Don't add features the user didn't ask for** — extra screens, login flows, settings pages. Single-screen replication only.
- **Don't reformat or "improve" `references/forest-journal.html`.** It's a frozen reference.
- **Don't skip the post-processing step for mascots.** A mascot with a square watercolor background looks broken.

---

## Tools available to you

| Path | Purpose |
|---|---|
| `scripts/load_keys.py` | Loads `.env` into `os.environ`. Called automatically by `gen_image.py`. |
| `scripts/gen_image.py` | One-shot Gemini image generation, style-conditioned. CLI. |
| `scripts/flood_fill.py` | PIL+scipy background removal for mascot/icon assets. CLI. |
| `prompts/style-extraction.md` | Template + rules for filling the STYLE TRANSFER preamble. |
| `prompts/analyze-ui.md` | Schema + rules for `layout.json` and `assets.json`. |
| `prompts/scaffold-html.md` | Constraints + structure + reference for `index.html`. |
| `references/forest-journal.html` | Gold-standard finished example. The quality bar. |

That's the whole skill. Go.
