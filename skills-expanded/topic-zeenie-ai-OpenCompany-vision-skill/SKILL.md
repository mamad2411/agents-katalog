---
name: vision-skill
description: Understand images (describe content, answer questions about them, extract text/OCR) via a vision model. Use when the user asks what an image, screenshot, chart, scan, or photo contains.
allowed-tools: vision data
metadata:
  author: opencompany
  version: "1.0"
  category: vision
  icon: "👁️"
  color: "#bd93f9"

---

# Vision Skill

See images through the `vision` tool (a vision-capable model looks at the
image and answers in text). Check the tools in your tool list for full
schemas; this skill covers strategy.

## Workflow

1. Locate the image with the `data` tool first (`list` / `search`) — the
   `vision` tool takes a workspace-relative path, and guessing paths wastes
   a paid model call.
2. An image on an external mount (`mnt/...`) must be imported first:
   `data copy_to_workspace`, then pass the returned workspace path.
3. Choose the operation:
   - `describe` — what is in the image; pass `question` for something
     specific ("what is the y-axis peak?") instead of asking for a general
     description and hoping.
   - `extract_text` — OCR-style text extraction (documents, screenshots,
     signs). Returns only the text.

## The budget ladder

`budget` controls resolution and therefore cost: `small` (~256 visual
tokens), `normal` (~1024, default), `large` (~2048, fine detail).

- Skim at `normal`; escalate to `large` only when the answer needs fine
  detail (dense charts, small print, UI screenshots).
- Never open with `large` on an image you haven't seen at `normal` — each
  call bills the vision provider.

## When NOT to use this tool

- The host model may already see images natively: if an image you read via
  the `data` tool is visible in the conversation, answer from it directly —
  a delegate call would be a second opinion at extra cost and latency.
- Extracting text from a PDF: use `data read` (text extraction) first;
  vision OCR is for rasterized/scanned content the parser cannot read.

## Anti-patterns

- Calling `vision` on a path that was never confirmed via `data` list/read.
- Repeating `describe` with rephrased questions — ask one specific
  `question` with the detail you actually need.
- Using `extract_text` on charts to infer numbers — ask `describe` with a
  targeted question instead; OCR on plot labels loses structure.
