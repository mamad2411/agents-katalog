# office/pptx-toolkit — skill payload

> Machine-readable contract: [`../pptx-toolkit.manifest.json`](../pptx-toolkit.manifest.json).

## What this skill does

Builds PowerPoint decks from a structured slide spec via `python-pptx`.
Each slide entry names a layout (`title`, `title_and_content`,
`two_content`, `comparison`, `blank`) and supplies the relevant content
(titles, bullets, tables, images, charts). Output is a `.pptx`.

## When to use it

- The user wants a deck (executive summary, status update, training).
- You have structured data (e.g. last quarter's numbers) and need slides
  *from* it, not slides *about* it.

## When **not** to use it

- The deliverable is a one-page graphic — use `design/canvas`.
- The deliverable is a written report — use `office/docx-toolkit`.
- The deck must follow strict brand templating beyond what `python-pptx`
  exposes — start from a brand template and pass it in.

## Determinism and risk

Determinism: **high** — same input spec, same deck. Risk: **low**.

## How it composes

Common downstream of `office/xlsx-toolkit` (chart-from-data) and
`content/research-writer` (bullet outline → deck). Upstream of
`comms/meeting-insights` only in the loop where the deck *generated* the
meeting; the more common direction is meeting → deck via the analyser.
