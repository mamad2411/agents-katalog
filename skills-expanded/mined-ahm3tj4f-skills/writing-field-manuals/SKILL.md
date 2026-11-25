---
name: writing-field-manuals
description: Writes explanatory technical documents as single HTML pages in the style of a 1980s or 1990s field manual, with Simplified Technical English text, numbered figures and tables, Mermaid diagrams rendered by Pele, Caution and Note boxes, and light or dark vintage themes. A build script checks structure, wording and diagrams and reports each error with a fix. Use when the user asks for an explainer, a lesson, a decision record, a comparison, a procedure or an incident report as an HTML document, a visual explanation in "the manual style", or a document from source material (RFCs, docs, code).
compatibility: Requires Node.js 20 or later. The render check (scripts/check.sh) uses the agent-browser CLI; without it, examine the page by eye.
metadata:
  version: "1.0"
---

# Writing field manuals

The agent writes the content. The skill controls the layout and the style. Write a source file with front matter, plain HTML components and Mermaid text. The build adds the anatomy, the numbers, the diagrams and the theme, and it does not accept a source with errors.

## Workflow

Copy this checklist and track your progress:

```
- [ ] 0. Ask the user for the theme. Wait for the answer.
- [ ] 1. Read the sources. Write down the facts and numbers that the document needs.
- [ ] 2. Plan: type, section titles, one figure for each section (from the reader question).
- [ ] 3. Write the source file (doc.src.html).
- [ ] 3b. Rewrite all text with the asd-ste100 skill.
- [ ] 4. Build. Fix every error. Build again until it prints BUILT.
- [ ] 5. Check the render. Examine the screenshots. Fix overlaps.
- [ ] 6. Open the page for the user.
```

**Step 0. Theme.** Before you write the source file, ask the user which theme to use. Show the themes from the Themes table below (light and dark). Use the question tool if it is available. Wait for the answer. Do not ask if the user already named a theme in the request, or named an earlier document whose theme you know. Write the answer in the front matter (`theme: ...`).

**Step 1. Sources.** Use only facts from the sources or the project. Mark invented values as examples ("example values" in the caption).

**Step 2. Plan.** Select the type from the question of the reader:

| Question | Type |
|---|---|
| How does X work? Why does X happen? | `explainer` |
| Teach me X. | `lesson` |
| What must we do? | `decision` |
| A or B? | `comparison` |
| How do I do X? | `procedure` |
| What happened? | `incident` |

The section order for each type is in [references/doc-types.md](references/doc-types.md). Select each figure from the question that it answers, with the table in [references/diagrams.md](references/diagrams.md). Prefer a short document: 3 to 6 sections.

**Step 3. Write.** Start from [assets/example.src.html](assets/example.src.html). Copy components from [references/components.md](references/components.md). Rules:
- Front matter gives the title, running head, question and footer. Do not write `<h1>`.
- `<h2>` holds only the title. The build adds "Section N." or "Lesson N.".
- Figures: `<figure id="x" data-mermaid caption="...">` with Mermaid text. Refer to them in the text with `{{fig:x}}`, tables with `{{tab:x}}`.
- No `style` attributes, no new CSS, no inline SVG coordinates for 2D figures.
- Box heads and subheads use normal case, not capitals: "Bottom line", "Caution", "Note".
- All text is full width. One paragraph is one row. Do not use two columns.

**Step 3b. Language.** Write all text in ASD-STE100 Simplified Technical English. Load the `asd-ste100` skill (`/skill:asd-ste100`) and apply its Rewrite branch to the text of each section: paragraphs, captions, table cells, notes and cautions. Do not change code, Mermaid labels that are technical names, or quoted text. [references/writing.md](references/writing.md) has the short rules and shows which rules the build checks. If the `asd-ste100` skill is not available, use writing.md only.

**Step 4. Build.** Run:

```bash
node scripts/build.mjs /tmp/<topic>/doc.src.html --theme microfilm
```

Output: `doc.html` next to the source (or `--out <file>`). Each problem prints as `file:line CODE message` and `Fix: ...`. Errors (`E...`) stop the build. Warnings (`W...`) do not, but fix them unless you have a reason. Use `--strict` to stop on warnings too. Repeat until it prints `BUILT`. If the same error stays after 3 rounds, change the figure type or simplify the source.

**Step 5. Check the render.**

```bash
bash scripts/check.sh /tmp/<topic>/doc.html /tmp/<topic>/shots
```

It reports JS errors, text outside a figure, wide figures and wide code lines. It also saves one screenshot for each figure. Look at each screenshot: the check cannot find two boxes on top of each other. Fix, build and check again.

**Step 6. Deliver.** Put files in `/tmp/<topic>/` unless the user gives a path. Open the page (`open doc.html` on macOS). Tell the user the path, the sections, and any limit you could not fix.

## Themes

Ask the user (Step 0), then set `theme:` in the front matter. `--theme` on the build command overrides it. The build stops with E004 if no theme is set. The built page also has a native theme select above the page, so the reader can switch themes. The selected theme is only the first one that the reader sees.

| Light | Dark |
|---|---|
| `paper` (cream) | `microfilm` (near black, bone ink, grain) |
| `microfilm-print` (gray, grain) | `night-blueprint` (navy, grid) |
| `whiteprint` (off-white, blue ink, grid) | `blue-microfiche` (blue black, scan lines) |
| `blue-photocopy` (pale blue gray) | `graphite-drafting` (charcoal, blue grid) |
| `drafting-vellum` (cream, blue grid) | |

If the user names one of the documents or themes from earlier work, use the same theme.

## Error codes

| Code | Meaning |
|---|---|
| E001 to E004 | Front matter missing, wrong type, wrong theme, no theme |
| E101 to E104 | Required part missing (Bottom line, steps, sections), manual title, two-column text |
| E201, E204, E205 | Figure without caption, wrong reference, double id |
| E300 to E303 | Mermaid syntax, forbidden style, forbidden class, undeclared lane |
| E401 | Em dash or en dash |
| W102 to W104 | Lesson parts missing, Bottom line too long, too few figures |
| W310 to W312 | Figure too wide, label too long, too many lanes |
| W401 to W402 | Sentence too long, non-STE word |
| W501 | Custom 2D drawing code |

## Files

- `scripts/build.mjs`: build and lint (run it). `scripts/lib/`: Mermaid and prose checks.
- `scripts/check.sh`: render check and screenshots (run it).
- `scripts/vendor/pele.js`: Pele 1.12.0, Mermaid to SVG (MIT, see PELE-LICENSE). Do not edit.
- `assets/`: page shell, CSS, themes, icons, `svg2d.js`, and the example source.
