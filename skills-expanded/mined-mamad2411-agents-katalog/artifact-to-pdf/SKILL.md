---
name: artifact-to-pdf
description: Convert a Claude artifact (or any URL / exported .html file) into a SINGLE continuous, pixel-accurate PDF with no page cuts — one long page sized to the whole content. Use when the user wants to export, save, download, or "turn into PDF" an artifact, HTML file, or web page, especially as one long page with no page breaks / no pagination.
---

# artifact-to-pdf

Turn a Claude artifact (or any URL / exported `.html`) into **one continuous, pixel-accurate PDF** — a single long page sized to the whole content, **no page cuts**. It renders the HTML in headless Chromium (the same engine the artifact viewer uses), so the PDF matches what you see on screen.

## When to use
The user asks to export / save / download / "turn into PDF" an artifact, an `.html` file, or a URL — especially when they want **one long page** or a PDF **without page breaks**.

## Inputs
- A path to an exported `.html` file (best fidelity for a Claude artifact), OR an `http(s)` URL.
- Optional output path and render width.

If the user did not give an input, ask for the `.html` file path or URL before running.

## How to run

The converter is a bundled Node script sitting next to this SKILL.md.

1. Set `SKILL_DIR` to the directory that contains this SKILL.md.
2. **First-run setup only** — install dependencies if missing (downloads a bundled Chromium ~120MB the first time; tell the user this is one-time):
   ```bash
   [ -d "$SKILL_DIR/node_modules/playwright" ] || ( cd "$SKILL_DIR" && npm install )
   ```
3. Run the converter (foreground; ~5–20s):
   ```bash
   node "$SKILL_DIR/artifact-to-pdf.mjs" "<input-file-or-url>" -o "<output>.pdf" [--width <px>]
   ```
   - `--width` defaults to 1200; set it to the artifact's design width if the layout is responsive and reflows.
   - Default output name is `<input>.pdf` (or `artifact.pdf` for a URL) in the current directory.
4. Read the tool's stdout — it prints the page size and, if the content exceeded the 200in cap, the scale it applied. Report that to the user.
5. Offer to send the PDF to the user with SendUserFile so they can see it.

## Notes / limits
- Emits exactly **ONE** page sized to the artifact's full height — no page cuts.
- A PDF page caps at **200in (ISO 32000 = 14,400pt ≈ 19,200px)** per side. Artifacts taller than that are **auto-scaled down** to fit one page (nothing is cut); the tool prints the scale used. Absurdly tall content warns it may clip in strict viewers.
- For a Claude artifact, prefer the **exported `.html`** — a `claude.ai` page URL also captures the app chrome around the artifact.
- `npm test` (in `SKILL_DIR`) renders a tall sample and asserts single-page output.

## Source
Full source, README, and issues: https://github.com/yheshamx/artifact-to-pdf
