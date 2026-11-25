---
name: autofigure
description: Generate clean, EDITABLE vector figures (SVG + exact-size PDF) for research papers — method / architecture / pipeline / system-overview diagrams — with AutoFigure-Edit. Use whenever the user wants to create or vectorize a paper figure from a text description OR from a draft/screenshot/draw.io image: it generates a step-1 raster with OpenAI gpt-image-2 by default (nano-banana optional), then runs local SAM3 segmentation + RMBG-2.0 icon extraction + an LLM SVG re-draw with OpenAI gpt-5.5 into an editable SVG, and exports a margin-free PDF for \includegraphics. Triggers: make a paper figure, method/architecture/pipeline/framework diagram, vectorize a diagram, "editable SVG figure", "用 AutoFigure / AutoFigure-Edit 画图", 论文方法图/流程图/架构图.
---

# autofigure — AutoFigure / AutoFigure-Edit figure generation

Turns a figure idea (or a rough draft image) into a **clean, editable vector figure**.
Two-stage pipeline, all local + subscription CLIs (no raw API keys required):

1. **Step-1 raster** — a journal-style draft PNG, by default from `gpt-image-2` (OpenAI/Codex,
   via the `hermes-gpt-image` skill). nano-banana (Gemini) is a manual alternative. *Skippable*
   if you already have an image (a draw.io export, a screenshot, a hand sketch).
2. **Vectorize (AutoFigure-Edit)** — `SAM3` segments the draft into regions, `RMBG-2.0`
   cuts out transparent icons, and an LLM (`gpt-5.5` via a local Codex shim) re-draws the
   whole thing as a placeholder-aligned **editable SVG** (`final.svg`). Then export an
   exact-size **PDF**.

**Defaults — OpenAI via the Codex subscription (no raw API key):** `gpt-image-2` for the step-1
raster (`gen.sh`) and `gpt-5.5` for the SVG re-draw (`afe.sh`, through the local shim →
`openclaw infer model run --model openai/gpt-5.5`). nano-banana (Gemini) and SiliconFlow are
**optional, non-default** alternatives — used only if you explicitly ask, or set `SF_API_KEY`.

Heavy assets (the `afe_venv`, `sam3.pt`, RMBG weights, the AutoFigure-Edit repo) live under
`AUTOFIG_HOME` (default `~/apps/autofig_work`). The scripts reference them; nothing is duplicated.

## Workflow (follow every time)

1. **Preflight once:** `bash ~/.claude/skills/autofigure/scripts/doctor.sh`.
   If anything is `✗`, see **Setup** below and stop until fixed.
2. **Make / obtain the step-1 raster.**
   - From text: `bash scripts/gen.sh "<detailed figure prompt>" /tmp/fig_input.png`
     Write a concrete, diagram-style prompt: state the layout ("left-to-right pipeline of N
     boxes with arrows"), each box's short label, palette, "flat vector, white background,
     crisp readable sans-serif labels, no clutter". gpt-image-2 spells short English labels
     well; keep dense diagrams to ≲15 labels or text may garble.
   - Or skip this and use an existing image as the input.
   - **`Read` the raster** to confirm it matches before vectorizing.
3. **Vectorize:** `bash scripts/afe.sh <input.png> <out_dir> ["sam,prompts"] [svg_model]`
   - Produces `<out_dir>/final.svg` (+ `template.svg` editable layout, `icons/` assets,
     `samed.png` segmentation overlay, `boxlib.json`).
   - `sam_prompt` (optional) tunes what SAM3 looks for, e.g. `"icon,box,arrow,text label,bottle"`.
   - Default SVG model is `gpt-5.5` via the local shim (auto-started). To use SiliconFlow
     instead: `SF_API_KEY=sk-... SVG_MODEL=Qwen/Qwen3-VL-32B-Instruct bash scripts/afe.sh ...`.
4. **Preview:** `bash scripts/view.sh <out_dir>/final.svg /tmp/fig_preview.png` then `Read` it.
   Check labels are correct/legible and **nothing overlaps**. If off, fix the prompt and redo
   step 2–3, or hand-edit `final.svg`/`template.svg` (it is plain SVG text).
5. **Export PDF for the paper:** `bash scripts/svg2pdf.sh <out_dir>/final.svg figures/fig_x.pdf 10`
   (10 = width in inches; height auto from the SVG aspect; margin-free). Drop it into the
   paper with `\includegraphics[width=\textwidth]{figures/fig_x.pdf}`.

## Commands (scripts/)

- `install.sh` — one-time backend install (venv + repos + SAM3 + RMBG + HF cache seed); see Setup.
- `doctor.sh` — verify the install is ready.
- `gen.sh "<prompt>" <out.png> [landscape|square|portrait]` — step-1 raster via gpt-image-2.
- `afe.sh <input.png> <out_dir> [sam_prompt] [svg_model]` — the AutoFigure-Edit vectorizer.
- `svg2pdf.sh <in.svg> <out.pdf> [width_in]` — exact-size, margin-free PDF.
- `view.sh <in.svg|pdf> <out.png> [width]` — PNG preview to Read.
- `shim.py` — local OpenAI-compatible server that bridges `/v1/chat/completions` (incl. images)
  to `openclaw infer model run --model openai/gpt-5.5`. `afe.sh` starts it on demand (port 8745)
  and leaves it running for reuse; stop it with `pkill -f autofigure/scripts/shim.py`.

## Tips

- **Editing the result:** `final.svg` embeds the extracted icons; `template.svg` is the clean
  layout with labeled placeholders — easiest to tweak text/positions by hand, then re-export PDF.
- **Dense, label-heavy method figures** sometimes vectorize cleaner from a **draw.io export** fed
  straight into `afe.sh` (skip `gen.sh`) than from a text-generated raster.
- **From-scratch SVG (no raster):** `AUTOFIG_HOME/run_af.py` drives the original *AutoFigure*
  agent (text → SVG directly via an OpenAI-compatible LLM). Less reliable here than the
  Edit path; prefer gen.sh → afe.sh.
- Image generation draws on the ChatGPT/Codex (and Google, for nano-banana) subscription quota;
  the SVG re-draw uses Codex (gpt-5.5) or your SiliconFlow balance.

## Setup (if doctor.sh reports ✗)

**One-command install** (builds the venv, clones the repos, installs SAM3, downloads the
SAM3 + RMBG-2.0 weights, seeds the HF cache):

```bash
HF_TOKEN=hf_xxx bash ~/.claude/skills/autofigure/scripts/install.sh   # [AUTOFIG_HOME]
```

`HF_TOKEN` is required (briaai/RMBG-2.0 is gated — request access first, then make a read
token). You still install the driver CLIs yourself: `hermes` (gpt-image-2), `openclaw`
(gpt-5.5), and Google Chrome. `install.sh` is idempotent (skips anything already present).

What it lays down under `AUTOFIG_HOME` (`~/apps/autofig_work`):
- `afe_venv` — Python 3.11 venv with `torch torchvision timm transformers kornia pillow cairosvg`
  plus SAM3 installed editable (`pip install -e` from facebookresearch/sam3).
- `sam3.pt` — the SAM3 checkpoint, **symlinked into the HF cache** so offline mode finds it:
  `ln -sf $AUTOFIG_HOME/sam3.pt ~/.cache/huggingface/hub/models--facebook--sam3/snapshots/<commit>/sam3.pt`
- `rmbg_local/` — a local copy of briaai/RMBG-2.0 (`model.safetensors`, `config.json`, `birefnet.py`).
- `.hf_env` — exports `HF_TOKEN` (+ optional `FAL_KEY`).
- `AutoFigure-Edit/` and `AutoFigure/` — the two repos.
- CLIs on PATH: `hermes` (gpt-image-2 + gpt-5.5 image desc), `openclaw` (gpt-5.5 SVG LLM),
  optional `agy` (nano-banana). Plus Google Chrome for SVG→PDF/PNG.
Network note: keep `HF_HUB_OFFLINE=1` (afe.sh sets it) — the HF Xet downloader hangs on some
networks; seeding `sam3.pt` into the cache + local RMBG path avoids all HF downloads.
