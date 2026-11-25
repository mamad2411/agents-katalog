---
name: imagine-agy
description: >-
  Generate images with the Antigravity CLI (`agy`) in headless mode — art, illustrations, icons, textures, hero/banner art, photoreal shots, storyboards, asset sets. Generation happens in a separate process, so image bytes and generation tokens never enter your context; you only see a one-line summary and the file paths. Covers the permission layers agy needs, the working-directory trap that silently misplaces every file, aspect-ratio control, batching a whole asset set in one run, and QA. Use when the user asks for an image / picture / illustration / icon / logo art / texture / banner / concept art, or says imagine/"generate an image"/"make me a picture"/"use antigravity for images". Trigger: /imagine-agy
user-invocable: true
---

`agy` (Antigravity CLI, usually `~/.local/bin/agy`) ships a first-class **`generate_image`** tool. Driving it headlessly is the token-cheap way to produce images: the model that paints runs in a separate process, and you get back only a short text summary plus files on disk. You never pay context for image bytes.

This skill is the reliable way to drive it. There are three traps that make it silently produce nothing, or put every file somewhere you'll never look.

## ⚠️ Three traps — get these right or you get nothing

**1. Claude Code's Bash classifier blocks `agy`.** Add an allow-rule once:
```json
// .claude/settings.local.json  (or ~/.claude/settings.json for all projects)
{ "permissions": { "allow": ["Bash(agy:*)"] } }
```
Without it the Bash tool refuses the command outright.

**2. agy auto-denies its own tools in headless mode.** In print mode it can't prompt for approval, so it denies `generate_image` and `write_to_file` and returns an empty result. Always pass `--dangerously-skip-permissions`. (Trap 1 is what lets that flag through the classifier.)

**3. 🔴 agy ignores your shell's working directory.** This is the big one. `cd`-ing into a folder and asking for `./out/fox.png` writes to **`~/.gemini/antigravity-cli/scratch/out/fox.png`** — the run reports success, the paths in its summary look plausible, and your target directory stays empty.

The fix is both halves together:
- pass **`--add-dir "<absolute output dir>"`** so the directory is in agy's workspace, and
- put **absolute paths** in the prompt itself. Never `./foo.png`, never `out/foo.png`.

If images "generated fine" but aren't where you expect, look in `~/.gemini/antigravity-cli/scratch/`.

## Invocation

```bash
OUT=/absolute/path/to/output; mkdir -p "$OUT"
agy -p "Generate 1 image with generate_image and save it to exactly $OUT/hero.png: <rich visual description>. Then run: ls -la $OUT" \
  --model gemini-3.1-pro-low \
  --dangerously-skip-permissions \
  --add-dir "$OUT" \
  --print-timeout 8m 2>&1 | tail -20
```

Then **verify on disk yourself** — never trust the summary:
```bash
ls -la "$OUT"; file "$OUT"/*
```

Run with **`run_in_background: true`** for anything past a single image. Roughly ~30–60s per image; a 5-image set can take several minutes and you get a task-notification when it lands.

### Model choice — do not reach for the expensive one

Image quality comes from the image model behind `generate_image`, **not** from the model driving the CLI. The driver only reads your prompt and calls a tool, so paying for a thinking model buys you nothing.

- **`gemini-3.1-pro-low`** — the default. Reliable at following exact paths and multi-image batches.
- **`gemini-3.6-flash-low`** — fastest/cheapest; fine for simple one-off images.
- Reserve `claude-opus-4-6-thinking` for when image generation is a *step inside* a real coding task (generate assets *and* wire them into a component). Never for images alone.

## Controlling the output

**Aspect ratio — say it in the prompt in words.** There's no flag; the phrasing drives it. Confirmed results:

| Ask for | You get |
|---|---|
| (nothing) | 1024×1024 square |
| "16:9 widescreen aspect ratio" | 1376×768 |
| "vertical 9:16 portrait aspect ratio" | 768×1376 |

State the ratio **both** as digits and as a word ("wide banner", "tall portrait") — that combination lands most consistently.

**⚠️ The bytes are always JPEG, whatever you name the file.** Ask for `hero.png` and you get a file named `hero.png` containing JPEG data (baseline, 300 DPI). Usually harmless — browsers sniff content — but it **will** break strict loaders, `sharp`/PIL format assertions, and anything checking the PNG magic number. Two consequences:

- Name outputs `.jpg` unless something downstream demands otherwise; it's honest about what's in them.
- **You cannot get transparency this way.** JPEG has no alpha channel. If the user needs a transparent-background logo or icon, say so and convert/matte afterwards — don't just ask agy harder.

Verify with `file "$OUT"/*` and convert if needed (`sips -s format png in.png --out real.png` on macOS).

## Batching an asset set — the real win

One run can produce a whole set, and images in the same run stay stylistically coherent. Number the deliverables and give each an absolute path:

```
Generate exactly 3 images with generate_image, saving to these EXACT absolute paths:
1. /abs/out/hero.jpg — <description>, 16:9 widescreen aspect ratio
2. /abs/out/icon.jpg — the same subject as a flat 2-color vector icon, minimal
3. /abs/out/bg.jpg  — <description>, vertical 9:16 portrait

All three must share one visual language: <palette, line weight, mood>.
Then run: ls -la /abs/out
Do nothing else.
```

Style coherence across a set comes from one explicit shared-language sentence, not from repeating adjectives in each item.

## Writing the image prompt

`generate_image` rewards concrete visual direction over adjectives. Cover:

- **Subject** — what, doing what, in what setting.
- **Medium/style** — "flat vector illustration", "cinematic photograph, 35mm", "isometric 3D render", "watercolor", "pixel art". This is the highest-leverage token in the whole prompt.
- **Palette** — name colors ("muted earth tones", "teal and gold") rather than "nice colors".
- **Light & mood** — "warm studio lighting", "overcast", "moody".
- **Composition** — "centered", "wide establishing shot", "generous negative space at the top for a headline".
- **Negatives** — "no text, no watermark, no people". Worth adding by default: baked-in gibberish text is the most common way a generated image becomes unusable.

Text rendering inside images is unreliable across all image models. For anything with real words — a poster, a UI mock, a titled banner — generate the art with **space left for text** and compose the type in HTML/SVG/CSS on top.

## Close the loop

- **Actually look at the image.** Read the file back — you can see it, and a prompt that reads perfectly can still produce something wrong. This is the only real QA.
- **Verify paths on disk** (`ls -la`, `file`). agy's summary sometimes reports a path it did not write to (see trap 3).
- **Report honestly** — give the user real paths, and mention the JPEG-bytes detail if it matters downstream.
- **Iterating beats explaining.** If it's close but off, re-run one item with a sharper prompt rather than describing the gap. Change one axis at a time (style, or palette, or composition) so you know what moved.

## When it fails

| Symptom | Cause |
|---|---|
| "Blocked by classifier" | Missing `Bash(agy:*)` allow-rule (trap 1). |
| Ran, empty output, no files | Missing `--dangerously-skip-permissions` (trap 2). |
| Claims success, target dir empty | Trap 3 — check `~/.gemini/antigravity-cli/scratch/`, then re-run with `--add-dir` + absolute paths. |
| Timed out mid-set | Raise `--print-timeout`, or split the set across runs. Files already written survive. |
| Wrong aspect ratio | Ratio wasn't in the prompt, or only as digits — add the word form too. |
| Transparency missing | Inherent: output is JPEG. Convert and matte, or use a different tool. |

## Minimal recipe

1. Ensure `Bash(agy:*)` is allowed in settings.
2. `OUT=<absolute dir>; mkdir -p "$OUT"`.
3. Write the prompt: numbered deliverables, **absolute** paths, style + palette + composition, aspect ratio in words and digits, "no text/watermark", shared-style sentence for sets.
4. Run with `--dangerously-skip-permissions --add-dir "$OUT" --print-timeout 8m`, backgrounded for multi-image.
5. `ls -la "$OUT"` and `file "$OUT"/*` to verify, then **read an image back and look at it**.
6. Report real paths; re-run individual items to refine.
