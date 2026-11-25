---
name: render
description: "Render knowledge-base content into shareable artifacts: Marp slide decks, matplotlib charts, printable briefs, Mermaid diagrams, and concept-graph visualizations. Output files land in the vault's outputs/ folder and re-open in Obsidian. Use when the user says 'turn this into slides', 'chart this data', 'build a deck from my notes', 'visualize the concept graph'. Part of the knowledge-base pack."
license: MIT
metadata:
  author: markfive-proto
  version: "0.1.0"
  pack: knowledge-base
---

# Render Pack — "Make my knowledge look like something"

`render` is the **output layer**. Same content, many presentations: a deck for a talk, a chart for a post, a printable brief for a stakeholder, a graph for your own orientation. Everything lands in `outputs/` and is viewable directly in Obsidian (with Marp plugin for slides, standard image embeds for charts).

## Commands

### /slides — Render notes as a Marp deck

When the user invokes `/slides <topic-or-note>`:

1. Gather source material:
   - If `<topic>`, search compiled/ for related notes and load top 5-10.
   - If `<note-path>`, use that single note as the spine.
2. Draft an outline: title slide → problem → 3-5 key points → synthesis → references.
3. Write Marp-flavored markdown to `outputs/slides/<slug>.md`:
   ```markdown
   ---
   marp: true
   theme: default
   paginate: true
   ---

   # <Title>

   ---

   ## Problem
   - ...

   ---

   ## Key idea 1
   - ...

   ---

   ## References
   - [[source-1]]
   - [[source-2]]
   ```
4. Report the path and instructions to preview in Obsidian (Marp plugin) or export with `marp <file> --pdf`.

**Slide density rules:**
- ≤ 6 bullets per slide.
- ≤ 12 words per bullet.
- One idea per slide.
- Always include a "References" slide at end linking back to the vault notes.

### /brief — Render an exec brief (1-2 page PDF-ready)

When the user invokes `/brief <topic>`:

1. Draft a brief in this structure:
   - Title + 1-line summary.
   - "So what" — the single most important takeaway (2-3 sentences).
   - 3 key findings (bullet list).
   - Supporting evidence table.
   - Recommendations / next steps.
   - Sources.
2. Save to `outputs/briefs/<slug>.md`.
3. Suggest: `pandoc <file> -o <file>.pdf` to export.

### /chart — Render a matplotlib chart from structured data

When the user invokes `/chart <data-source>`:

1. Locate structured data (a dataset note under `raw/datasets/`, or an embedded table in a compiled note).
2. Decide chart type from the question shape:
   - Time series → line.
   - Comparison → bar.
   - Distribution → histogram / violin.
   - Part-of-whole → stacked bar (not pie).
   - Correlation → scatter.
3. Write a standalone Python script to `outputs/charts/<slug>.py`:
   ```python
   import matplotlib.pyplot as plt
   import pandas as pd
   df = pd.read_csv("<path>")
   # ... chart code ...
   plt.tight_layout()
   plt.savefig("outputs/charts/<slug>.png", dpi=200)
   ```
4. Run it. Save PNG next to the script.
5. Write a companion `outputs/charts/<slug>.md` that embeds the PNG and explains the chart.

### /graph — Render a concept graph

When the user invokes `/graph [<root-concept>]`:

1. Build a node set from `compiled/concepts/*.md`.
2. Build edges from wikilinks between them.
3. If `<root-concept>` provided, restrict to 2-hop neighborhood.
4. Emit a Mermaid diagram:
   ```markdown
   ```mermaid
   graph TD
     A[Concept A] --> B[Concept B]
     ...
   ```
   ```
5. Save to `outputs/graphs/<slug>.md`. Obsidian's native Mermaid renderer will draw it.
6. For large graphs (>40 nodes), use Graphviz DOT instead and export PNG.

### /timeline-chart — Render a timeline as Gantt or dated bar

When the user invokes `/timeline-chart <topic>`:

1. Pull events from the relevant notes (look for dates in frontmatter and inline).
2. Output a Mermaid `gantt` block in `outputs/charts/timeline-<slug>.md`.

### /flashcards — Render concepts as spaced-repetition cards

When the user invokes `/flashcards <topic>`:

1. Pull 10-30 concepts.
2. Emit Anki-compatible format:
   ```
   Front: What is <concept>?
   Back: <TL;DR> (source: [[<page>]])
   ```
3. Save as `outputs/flashcards/<topic>.tsv` for Anki import.

### /handbook — Compile a printable "handbook" PDF from a tag

When the user invokes `/handbook <tag>`:

1. List all compiled notes with that tag.
2. Order them by frontmatter `order` field if present, else alphabetical.
3. Concat into a single markdown with auto-generated TOC.
4. Save as `outputs/handbooks/<tag>-handbook.md`.
5. Suggest `pandoc <file> -o <file>.pdf --toc` for a bound PDF.

### /talk — Full talk package (slides + speaker notes + handout)

When the user invokes `/talk <topic>`:

1. Run `/slides <topic>` for the deck.
2. Run `/brief <topic>` for a 1-page handout.
3. Add speaker notes to each slide (Marp: HTML comments inside the slide).
4. Output triple: `outputs/slides/<slug>.md`, `outputs/briefs/<slug>.md`, `outputs/handouts/<slug>.md`.

## File-in-back rule

Every rendered artifact is itself a markdown file in the vault. That means:
- It is indexable by `qa` in future runs.
- It can be linked from concept pages (`## Derived outputs`).
- `lint` checks its frontmatter and links like any other note.

## Obsidian plugin recommendations

- **Marp for Obsidian** — preview slides inline.
- **Advanced Tables** — for brief/handbook tables.
- **Excalidraw** — companion hand-drawn diagrams.
- **Mermaid** (core) — graph + timeline rendering.
- **Pandoc plugin** (or shell pandoc) — export to PDF.

## Output frontmatter

Every rendered artifact gets:
```yaml
---
type: rendered
render_kind: slides|brief|chart|graph|timeline|flashcards|handbook|talk
rendered_from: [<source-note-paths>]
rendered_at: <ISO>
tags: [output, render]
---
```

So `lint` and `qa` can filter them out when reading source material.

## Related skills (same pack)

- `[[ingest]]` — source of material
- `[[compile]]` — where the graph structure comes from
- `[[qa]]` — answers that can be rendered as slides/briefs
- `[[lint]]` — can render its report as a dashboard

## Attribution

Pack inspired by Karpathy's preference for visual outputs (Marp slides, matplotlib, markdown reports) filed back into the vault so explorations compound.
