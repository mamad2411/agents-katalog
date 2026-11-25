---
name: notion-diagram
description: >-
  Build a diagram for a Notion page as an HTML block — an inline-SVG figure, arranged by coordinate and
  interactive if it needs to be — and publish it through the connector. Covers when to reach for this
  rather than Mermaid, the create-attachment to embed pipeline, what the sandbox forbids, and how a
  diagram is revised once it is live. Triggers - "the Mermaid diagram won't line up", "can we get a
  proper diagram into Notion", "make this an HTML block", "interactive diagram for the spec", "the
  boxes are in the wrong order", "put the SVG on the page".
---

# Notion diagrams

A Notion HTML block is an **embed backed by an uploaded `.html` attachment**, rendered in a sandboxed
iframe. It is the only route to a figure whose layout is chosen rather than computed, and the only one
that can respond to a click. Notion's help centre documents none of this; the sources are
`developers.notion.com/reference/block` (embed section) and `notion://docs/enhanced-markdown-spec`.

This file carries when a figure earns a block, the call shapes, the starter file and what has actually
been measured.

## Which kind of diagram

| Reach for | When |
|---|---|
| Mermaid code block | Sequence, flow and state diagrams whose default layout is acceptable. Cheapest to review and to edit, and the right default for timing and handshake sections |
| HTML block, inline SVG | The auto-layout produces a **false reading**, or one the reader cannot follow — crossed edges, a convoluted sequence. Also where interaction is what makes the structure visible |
| Image block, plain `.svg` | The arrangement matters but nothing else does. Static, no scripts, survives contexts an iframe may not |

Two triggers, and neither is complexity. **A false reading**: an eleven-guard diagnosis tree earned a block
because the branch gating a whole subtree was laid out off-screen, so the remaining nodes read as if one
condition led straight to an instruction it never reaches. **Unreadable**: misleading nobody, and still
costing every reader the effort of untangling it. Two shapes produce it reliably — a flowchart whose
branches rejoin on one node, which Mermaid routes as crossed edges, and two transitions carrying
near-identical long labels, which it stacks.

A small classification flowchart on the same page stayed Mermaid, so being a flowchart is not itself a
reason. Interaction passes the same test: four routes converging on one instruction is invisible in any
static rendering. A Mermaid diagram that renders correctly is easier for the next author to change, and
`mmdc` already validates it.

## Publishing

Three steps, no browser and no paste:

1. `create-attachment` with `content` (inline UTF-8, 200 KiB ceiling) and a `.html` `filename`.
2. Take `markdown_source` from the response — `file-upload://<id>`.
3. Place it as the `src` of an `<embed>` in `create-pages` or `update-page` content:

```
<embed src="file-upload://<file_upload_id>">Caption</embed>
```

`<embed>` is the only spelling. A code block or a file block produces something else entirely, and the
markdown spec says so explicitly: "HTML", "HTML block", "HTML artifact" and "HTML embed" all mean an HTML
attachment rendered with `<embed>`.

A file already on disk, or one past the 200 KiB inline ceiling, takes the other route: `create-file-upload`
returns `upload_url` and `upload_headers`, and one multipart POST with the file in the `file` form field
returns the same `markdown_source`. Everything downstream is identical.

**Keep the `file_upload_id` the call returned.** It is the only handle `download-attachment` accepts; the
attachment id stored on the page is a different value and is rejected. An HTML block created in the Notion
UI, or by a Notion agent, cannot be read back at all — the attachment belongs to that integration.

## Writing the file

The block reaches nothing outside itself. What that means while writing:

- Inline every style and script; embed raster assets as `data:` URIs; system font stacks only.
- No library. Hand-written SVG is the medium, not a rendering target.
- **Stricter than a Claude artefact**, which does allow cdnjs and `fonts.googleapis.com`, so an artefact
  diagram needs stripping before it works here.
- `localStorage` works but is per-browser and per-machine, so it holds view preferences and nothing a
  second reader is expected to see.

`reference/template.html` is a starting shell: Notion's own light and dark palettes as tokens, a
responsive `viewBox`, and a keyboard-reachable click handler. Copy it into the scratchpad rather than
writing a page from scratch.

## Revising a live diagram

A block is not editable in place. A change means regenerating the file and swapping the attachment, which
makes the master copy the thing that matters:

- The editable master lives in the repo or the scratchpad. Notion holds a copy.
- Update by calling `create-attachment` again and pointing the same `<embed>` at the new
  `markdown_source`, through `update-page`'s `content_updates`.
- The caption is page content rather than part of the file, so wording fixes never need a re-upload.
- **Replacing a Mermaid block: put the backtick fences in the `old_str`.** Matching the inner source alone
  succeeds and nests the `<embed>` inside the surviving code block — one case of the block rule in
  `notion-editing`.

## Measured behaviour

Notion publishes nothing about how a block behaves away from the desktop app. Keep a probe page in the
space and record each surface here as it is measured.

| Surface | Behaviour |
|---|---|
| Desktop app | Renders, runs scripts, responds to clicks |
| Frame height | Unmeasured |
| Mobile app | Unmeasured |
| PDF export | Unmeasured |
| Dark mode | The iframe carries its own document and inherits nothing, so it sees `prefers-color-scheme` rather than Notion's theme. Define the dark palette off that media query, and paint the page's own background |

Until a row is measured, design so the answer does not matter: a diagram that only works when the frame
auto-sizes is a diagram that breaks on whichever surface turns out to fix the height.

**Do not publish an internal space to a `notion.site` URL to test how a block renders there.** Measure on
a throwaway workspace if the answer is needed.

## Accessibility

The figure is content, not decoration. Give the root `<svg>` a `role="img"` and an `aria-label` that says
what the diagram shows, label interactive elements, and make sure the same information survives without
colour — a reader on the PDF export gets one still frame and no interaction at all.

## Related

`notion-specification` owns what a page says and where a diagram belongs in it. `notion-preview` owns
rendering a whole page for review before it is written. `mmdc` owns the Mermaid path.
