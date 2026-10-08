---
name: unlimited-ocr-segment-figure
description: Split a composite figure, screenshot, or dashboard into its individual panels by cropping the layout bounding boxes Unlimited-OCR detects, so each panel can be described separately by a vision model that is good at charts. Turns Unlimited-OCR's refusal to transcribe charts into a pre-processing win — one chart per prompt beats a nine-panel collage per prompt. Use when a vision model is misreading a dense multi-panel image, when you need per-figure crops from a paper or report, or when building a two-stage OCR pipeline that localises first and describes second. TRIGGERS - segment figure, split panels, crop charts from image, multi-panel figure, extract subfigures, per-panel description, layout segmentation, chart crops, split a screenshot into regions, dashboard panels, figure extraction.
allowed-tools: Bash, Read, Write, Glob
---

# Unlimited-OCR — segment a composite figure into panels

> **Self-Evolving Skill**: improves through use. The behaviour below was measured, not assumed —
> see [`../../references/EMPIRICAL.md`](../../references/EMPIRICAL.md). Fix this file the moment a
> claim stops holding.

---

## Why this exists

Unlimited-OCR **localises charts and transcribes nothing inside them**. Fed a 1080×1504 image
containing nine matplotlib panels, it returned nine `<|det|>chart [box]<|/det|>` markers with
perfect boundaries and **zero characters of text** — not even the panel titles, which were legible.

That is a dead end if you wanted a transcription. It is excellent if you wanted a _segmenter_: the
boxes were accurate enough to crop nine clean, individually-interpretable panels out of one dense
collage.

The pipeline that follows from it:

```
composite image ──[Unlimited-OCR: localise]──> N panel crops ──[a chart-reading model]──> N descriptions
```

A vision model handed one chart at a time, filling the frame, does markedly better than the same
model handed a nine-panel grid and asked to describe all of it at once. This skill is the first
stage; the describer is whatever you already use.

---

## Use it

```bash
S=~/eon/cc-skills/plugins/unlimited-ocr/scripts/unlimited_ocr.py

# Every detected region, cropped
uv run --no-project $S segment --input figure.png --output ./panels

# Only charts and tables, ignoring text blocks
uv run --no-project $S segment --input figure.png --output ./panels --categories chart,table

# Wider margin — useful when axis labels sit outside the plotted area
uv run --no-project $S segment --input figure.png --output ./panels --pad-pixels 24
```

Output is `<stem>_<index>_<category>.png` per region, plus a `segments.json` manifest carrying the
source size, both coordinate systems, and any text the model did associate with each region.

---

## `--pad-pixels` defaults to 12, and should not be 0

The model's boxes hug the **plotted area**. A pixel-exact crop of a chart therefore cuts off the
x-axis tick labels sitting just below it — verified on the nine-panel figure, where every crop at
padding 0 lost its date axis. Those labels carry the units and the date range, which is most of what
makes a chart interpretable by the next model in the chain.

Twelve pixels is a starting point, not a law. Raise it for figures with outboard captions.

---

## Reading the manifest

```json
{
  "source_size": [1080, 1504],
  "regions_detected": 9,
  "regions_written": 9,
  "segments": [
    {
      "index": 0,
      "category": "chart",
      "normalized_bbox": [0, 0, 999, 152],
      "pixel_bbox": [0, 0, 1080, 241],
      "path": "…_000_chart.png",
      "text": ""
    }
  ]
}
```

`regions_detected` and `regions_written` differ when `--categories` or `--min-pixels` filtered
something out. They are reported separately on purpose: a silent gap between "what the model found"
and "what you got" is how a segmentation job quietly under-delivers.

---

## Limits

- Boxes are normalised to 0–1000 on both axes and converted to pixels using the image's real size.
  A region whose box the model omitted is skipped rather than guessed at.
- Segmentation quality is only as good as the layout detection. Verify a sample visually the first
  time you point this at a new document class — the nine-panel result was checked by eye before it
  was written down here.
- This does not describe anything. It cuts. Pair it with a describer.

---

## Post-Execution Reflection

After this skill completes, check before closing:

1. **Did any crop clip its content?** — raise `--pad-pixels` and record the document class that
   needed it. The default of 12 exists because 0 clipped axis labels off every panel of a real figure.
2. **Were fewer regions emitted than the figure visibly contains?** — the model omitted a box, not
   the CLI. Note the document class in `references/PITFALLS.md`; silent under-delivery is the failure
   mode this skill warns about.
3. **Did you pair it with a describer?** — this skill cuts and never describes. If the describer
   needed a specific crop size or format, write that requirement down here.
