---
name: unlimited-ocr-batch-folder
description: Batch parse a folder of PDFs and images to markdown with LaTeX, tables, and layout boxes using baidu/Unlimited-OCR locally — with checkpoint/resume, incremental writes, and per-file repetition detection. Use when processing a large folder of scanned documents or research papers, when you need results written incrementally to survive interruption, or when extracting equations and tables from a document collection. TRIGGERS - batch ocr, ocr a folder, batch parse documents, parse multiple pdfs, folder to markdown, extract formulas from folder, ocr multiple files, batch document extraction, document collection parsing, checkpoint resume.
allowed-tools: Bash, Read, Write, Glob
---

# Unlimited-OCR — batch parse a folder of PDFs and images

Process an **entire folder** of images and PDFs without losing work to interruption, using the same proven `baidu/Unlimited-OCR` model that powers [`unlimited-ocr-parse-document`](../unlimited-ocr-parse-document/SKILL.md). Results are written **incrementally to a manifest**, so a long run that gets interrupted can be resumed without reprocessing.

> **Self-Evolving Skill**: every number and guarantee below was measured on this hardware, not copied from upstream documentation. If a guarantee stops holding, fix this file and references immediately rather than deferring. Re-verify before changing a documented fact.

---

## The guarantees

1. **ONE IMAGE PER FORWARD PASS, ALWAYS** — per-image processing is deliberate and measured. Single-pass multi-image on MLX recovered 1/3, 4/5, and 0/10 pages; per-image recovered 100 % every time. See [`../../references/PITFALLS.md`](../../references/PITFALLS.md) § 3.
2. **CHECKPOINT AND RESUME** — every result is written to disk BEFORE the manifest is updated. If the process dies, the incomplete line is never recorded. Re-run with the same output folder to skip everything already done.
3. **CHARTS COME BACK EMPTY** — this is correct behaviour for a layout parser and a fatal surprise if you expected a vision model. See the next section.
4. **EXIT CODES**: The batch script returns a summary exit code: `0` if all files succeeded without repetition, `1` if some files had repetition suspected (check before trusting), `2` if any files failed with hard errors. Per-file status is always recorded in the manifest.
5. **MEMORY-BOUNDED** — no result accumulation. Each file runs in its own process (load, infer, write, exit), so a 1,000-file folder never threatens machine stability.

---

## What it will NOT do

**Charts come back empty.** Fed a nine-panel matplotlib figure, the model returned nine perfectly-placed `chart` bounding boxes and zero characters. That is correct for a layout parser and catastrophic if you assumed an image captioner.

If you need the _content_ of charts, use [`unlimited-ocr-segment-figure`](../unlimited-ocr-segment-figure/SKILL.md) to crop each detected region independently, then hand the crops to a vision model that does describe images.

---

## Use it

```bash
S=~/eon/cc-skills/plugins/unlimited-ocr/scripts/unlimited_ocr_batch_folder_parser.py

# Process a folder, writing results incrementally to ~/results/
uv run --no-project $S --folder ~/my_documents --output ~/results

# Resume from where it left off (skips everything in the manifest)
uv run --no-project $S --folder ~/my_documents --output ~/results

# Collapse character-spaced math (c u r v e -> curve), keep tables as HTML
uv run --no-project $S --folder ~/my_documents --output ~/results \\
  --collapse-math --table-format html

# Use a specific backend (mlx on Apple Silicon, cuda on NVIDIA)
uv run --no-project $S --folder ~/my_documents --output ~/results --backend mlx

# Suppress per-file progress (quieter stderr)
uv run --no-project $S --folder ~/my_documents --output ~/results --quiet
```

---

## Output structure

```
~/results/
  manifest.jsonl              # One JSON object per file, newline-delimited
  progress_report.txt         # Summary at the end
  <image_stem>.md             # Markdown for each input image
  <pdf_stem>.md               # Markdown for each page of each PDF
  <pdf_stem>.json             # Layout boxes and metadata (optional)
```

Every line in `manifest.jsonl` is:

```json
{
  "source_path": "/path/to/image.png",
  "output_md": "image.md",
  "output_json": null,
  "status": "done",
  "elapsed_seconds": 2.4,
  "backend": "mlx",
  "page_count": 1,
  "error_message": null
}
```

Statuses are:

- `done` — parsed successfully, no repetition detected
- `repetition_suspected` — parsed, but a repetition detector fired; inspect before trusting
- `failed` — error (see `error_message`)

---

## Flags

| Flag                      | Values                | Default    | Meaning                                                                                     |
| ------------------------- | --------------------- | ---------- | ------------------------------------------------------------------------------------------- |
| `--folder`                | PATH                  | (required) | Input folder; searched recursively for images + PDFs                                        |
| `--output`                | PATH                  | (required) | Output folder; created if missing                                                           |
| `--backend`               | `auto`, `mlx`, `cuda` | `auto`     | Which backend: MLX for Apple Silicon, CUDA for NVIDIA GPU                                   |
| `--collapse-math`         | (flag)                | off        | Rejoin `c u r p d f` into `curpdf` inside math (measured fix for the model's output format) |
| `--table-format`          | `html`, `pipe`        | `pipe`     | HTML tables or pipe-markdown; pipe is suitable for concatenating into markdown documents    |
| `--strip-det`             | (flag)                | off        | Remove layout bounding box markers from output                                              |
| `--quiet`                 | (flag)                | off        | Suppress per-file progress to stderr                                                        |
| `--allow-withheld-prompt` | (flag)                | off        | Force a withheld prompt mode (rarely needed; see `../../references/PITFALLS.md` § 1)        |

---

## Interruption safety

The script is safe to interrupt (Ctrl+C) at any time:

1. Each file's result is written to the output folder **before** the manifest is updated.
2. The manifest is append-only; if a line is there, the output files exist.
3. Re-running with the same output folder automatically skips everything already in the manifest.
4. If a process crashes mid-write, the incomplete manifest line is never recorded.

**To re-process a file:** delete its line from `manifest.jsonl` and re-run.

---

## Choosing a backend

`--backend auto` (default) prefers MLX on Apple Silicon, CUDA on NVIDIA.

|              | Apple Silicon (MLX)                           | NVIDIA (transformers)                |
| ------------ | --------------------------------------------- | ------------------------------------ |
| Model        | `mlx-community/Unlimited-OCR-mxfp8` (3.66 GB) | `baidu/Unlimited-OCR` (6.67 GB bf16) |
| Measured on  | M3 Max, 36 GB                                 | RTX 4090, 24 GB, Ada SM 8.9          |
| Single image | **2.4 s**, 5.2 GB peak                        | 3.7 s, 8.3 GB peak VRAM              |
| Determinism  | greedy, T=0                                   | byte-identical on re-run             |

Full benchmarks and platform notes: [`../../references/EMPIRICAL.md`](../../references/EMPIRICAL.md).

---

## Understanding the repetition detector

Exit code 1 means **repetition was suspected, NOT that the run failed**. The detector is structural (short chunks repeating in the tail), not probabilistic, so a NEW repetition is caught, not just the known ones from the reference table.

Measured base rate: **~4 % on tables** (103 real images from the quantml corpus). Budget for it, but do not discard the output automatically — check it first. Most will be valid despite the warning.

All repetition detections are recorded in the manifest, so you can filter afterward:

```bash
jq 'select(.status == "repetition_suspected")' ~/results/manifest.jsonl
```

---

## Common questions

**Q: Can I run this on a CPU?**

No. The model's only published runtimes are MLX (Apple Silicon, GPU-backed) and transformers/CUDA (NVIDIA GPU). A CPU implementation does not exist. On a Mac, you have Apple Silicon MLX available.

**Q: How long does a 1,000-image folder take?**

~2 hours on a single M3 Max at ~7 s/image median. Every image runs in its own process, so if you have spare cores, parallelizing across multiple invocations (folder splits) will help. A separate tool for that is outside scope.

**Q: What if a file is corrupted or unreadable?**

It gets marked `failed` with an error message in the manifest. The batch continues without stopping.

**Q: Can I change the output folder without reprocessing?**

No. The manifest is tied to the output folder. To reprocess everything, use a new output folder.

---

## Limits and guarantees

All documented in [`../../references/PITFALLS.md`](../../references/PITFALLS.md) (every entry was hit while building this plugin) and [`../../references/EMPIRICAL.md`](../../references/EMPIRICAL.md) (every number was measured on the two machines it supports).

Key ones:

- **Single-pass multi-image is deliberately unused.** The model's headline capability does not survive contact with the MLX path — you get incomplete pages and no error. Per-image is slower and complete.
- **The image MIME type is detected from magic bytes, not the file extension.** WeChat serves PNG/WebP under `.jpg` URLs; the CLI reads the first bytes to detect the truth.
- **Bounding box coordinates are normalised to 0–1000 on BOTH axes**, independent of the image's aspect ratio.
- **Mathematics comes back character-spaced** by default (`c u r v e`). Pass `--collapse-math` to rejoin it.
- **The model writes tables as HTML `<table>`, never as pipe-markdown** — measured at 88 of 103 real
  tables. This batch parser converts them to pipe-markdown by default; pass `--table-format html` to
  keep the model's own serialization.
- **`--pad-pixels 0` clips the axis labels off every chart crop.** If you use `segment`, start with the default (12 px) and raise it only if captions are clipped.

---

## Post-Execution Reflection

After this skill completes, check before closing:

1. **Did repetition get detected?** — record which document types triggered it in `../../references/PITFALLS.md` § 3; the base rate is ~4 % on tables.
2. **Did the folder finish?** — check `progress_report.txt` for the final counts.
3. **Are there failures?** — `jq 'select(.status == "failed")' manifest.jsonl` to see which files errored.
4. **Do the markdown outputs look right?** — spot-check a few; tables come back as HTML unless you passed `--table-format pipe`, and charts come back empty.
