---
name: unlimited-ocr-parse-document
description: Parse an image, PDF, or directory into markdown with LaTeX formulas, HTML/markdown tables, and per-block layout bounding boxes, using baidu/Unlimited-OCR locally — free, offline, no API key, no upload quota. Runs on Apple Silicon via MLX (~2.4 s/image, ~5 GB) or an NVIDIA GPU via transformers. Use when transcribing scanned or image-based documents, extracting equations from a paper, converting a PDF to markdown, OCR-ing screenshots, or replacing a paid vision-API OCR call with a local one. TRIGGERS - unlimited-ocr, ocr this, ocr a pdf, extract text from image, transcribe document, pdf to markdown, document parsing, extract formulas, extract equations, latex from image, local ocr, offline ocr, scanned pdf, image to text, layout parsing, bounding boxes from document.
allowed-tools: Bash, Read, Write, Glob
---

# Unlimited-OCR — parse a document locally

`baidu/Unlimited-OCR` (MIT, [arXiv 2606.23050](https://arxiv.org/abs/2606.23050)) is a 3B-total /
500M-activated MoE document parser. It reads a page image and returns markdown with LaTeX
mathematics, tables, and a `<|det|>` bounding box for every block it found.

> **Self-Evolving Skill**: improves through use. Every number below was MEASURED on this hardware,
> not copied from a README — provenance in [`../../references/EMPIRICAL.md`](../../references/EMPIRICAL.md).
> If a measurement drifts, a flag stops working, or a new failure mode appears, fix this file and
> the references immediately rather than deferring. Re-verify before changing a documented fact.

---

## The one rule: `Free OCR.` is the only prompt mode that works

Of the three prompt modes the upstream project documents, **two are broken on MLX** and both are
refused by this CLI with exit 2 and a printed reason:

| Mode               | Measured behaviour                                                                                       |
| ------------------ | -------------------------------------------------------------------------------------------------------- |
| `free-ocr`         | **works** — correct output with layout boxes in 2.4 s. The default.                                      |
| `document-parsing` | decodes `parsing.parsing.parsing…` until `max_tokens`. This is the prompt the upstream README documents. |
| `multi-page`       | deterministically hallucinates the word `industrydocuments` onto a single image.                         |

`--allow-withheld-prompt-mode` forces one anyway. They are kept nameable rather than deleted so the
failures stay reproducible.

**This CLI sends one image per forward pass, always.** The model's headline multi-page capability is
deliberately unused — a five-page single-pass run dropped a page with no error, which is the worst
failure mode there is for an archive. Per-page is slower and verifiable.

---

## Use it

```bash
S=~/eon/cc-skills/plugins/unlimited-ocr/scripts/unlimited_ocr.py

# Which backends does this machine actually have?
uv run --no-project $S doctor

# One image -> markdown on stdout
uv run --no-project $S parse --input page.png

# A PDF -> one .md per page, plus a JSON report, rendered at 300 DPI
uv run --no-project $S parse --input paper.pdf --output ./out

# A directory of images, machine-readable, with math repaired for cross-model comparison
uv run --no-project $S parse --input ./images --format json --collapse-math-spacing --quiet

# Just the prose: strip the layout markers
uv run --no-project $S parse --input page.png --strip-det

# The CLI contract itself, as JSON (the SSoT an agent should introspect)
uv run --no-project $S spec
```

`uv run` reads the script's PEP 723 header and materialises its own dependencies. There is nothing
to install and no virtualenv to manage.

---

## What it returns

```
<|det|>equation [249, 82, 699, 202]<|/det|>\[
c u r p d f = t r i a n g (l o w, h i g h, v o l)
\]
```

- **Bounding boxes are `[x0, y0, x1, y1]` normalised to 0–1000 on BOTH axes**, independent of the
  real aspect ratio. Verified: a box of `y1=909` on a 211-pixel-tall image. The CLI also emits
  pixel coordinates in `--format json`.
- **Categories observed so far:** `equation`, `title`, `text`, `chart`, `header`, `page_footnote`,
  `page_number`, `image`. The taxonomy is not documented upstream; treat any new value as valid.
- **Mathematics comes back character-spaced** — `c u r p d f`, not `curpdf`. In LaTeX math mode
  those render identically, so it is not wrong, but it is not byte-identical to any other model's
  output either. Pass `--collapse-math-spacing` to rejoin it. This matters enormously if you are
  comparing transcriptions across models: without it, every formula scores as a disagreement.

---

## Choosing a backend

`--backend auto` (default) prefers MLX, then CUDA.

|              | Apple Silicon (MLX)                           | NVIDIA (transformers)                          |
| ------------ | --------------------------------------------- | ---------------------------------------------- |
| Model        | `mlx-community/Unlimited-OCR-mxfp8` (3.66 GB) | `baidu/Unlimited-OCR` (6.67 GB bf16)           |
| Measured on  | M3 Max, 36 GB                                 | RTX 4090, 24 GB, Ada SM 8.9                    |
| Single image | **2.4 s**, 5.2 GB peak                        | 3.7 s, 8.3 GB peak VRAM                        |
| Multi-page   | per page, one call each                       | 1.5 s/page synthetic, 11 s/page dense academic |
| Determinism  | greedy, T=0                                   | byte-identical on re-run                       |

**Do not follow the upstream SGLang instructions on an Ada GPU.** They specify
`--attention-backend fa3`; FlashAttention-3 requires Hopper (SM 9.0). The transformers path needs
no backend flag and is what these numbers come from. `doctor` reports compute capability and says
so explicitly.

---

## What it will NOT do

**It does not describe charts.** It localises them and transcribes nothing inside. On a nine-panel
matplotlib figure it emitted nine perfectly-placed `chart` boxes and zero characters — not even the
panel titles, which were plainly legible. That is correct behaviour for a layout parser and a nasty
surprise if you expected an image captioner.

If you need the _content_ of a chart, use
[`unlimited-ocr-segment-figure`](../unlimited-ocr-segment-figure/SKILL.md) to crop each panel and
hand the crops to a model that does describe images.

**The model writes tables as HTML `<table>`, never as pipe-markdown.** Measured over 103 real
tables: 88 came back as `<table>` markup and 15 as prose; none as pipe-markdown. The CLI converts
them for you — `--table-format` defaults to `pipe`; pass `--table-format html` to keep the model's
own serialization. Pipe-markdown is suitable for concatenating into markdown
documents and for comparing against other readers (M3, GLM-4.6v) which emit pipe-markdown natively.

Other limits, all with evidence, in [`../../references/PITFALLS.md`](../../references/PITFALLS.md):
degenerate repetition, multi-page page-dropping, and why "Unlimited" is not unlimited.

---

## Exit codes

| Code | Meaning                                                                                  |
| ---- | ---------------------------------------------------------------------------------------- |
| `0`  | parsed; no degenerate repetition detected                                                |
| `1`  | parsed, but repetition suspected in at least one output — **inspect before trusting it** |
| `2`  | usage or input error, including the refused prompt mode                                  |

Exit 1 is not a crash and not a success. The CLI detects loops structurally (a short chunk repeating
in the tail), so a NEW loop is caught, not just the known one.

---

## Post-Execution Reflection

After this skill completes, check before closing:

1. **Did it exit 1?** — repetition was detected. Record which prompt mode and image type triggered it
   in `references/PITFALLS.md` § 3; the measured base rate is ~4 % on tables.
2. **Did a prompt mode behave differently than documented?** — the two withheld modes are withheld on
   measured evidence. If one now works, update the withholding reason and its test, not just the doc.
3. **Did the output need reformatting downstream?** — tables come back as HTML. If you wrote a
   converter, it belongs in this plugin rather than in the calling project.
