---
name: pandoc-docx
description: Create clean Word documents (.docx) from Markdown using pandoc, automatically applying the bundled NIH-style reference template (Arial 11pt, 1-inch margins, single-spacing, NIH heading hierarchy) so manuscripts, abstracts, and grant attachments come out grant-ready by default. Use when the user asks to create a new Word document from fresh Markdown content (manuscript draft, NIH grant attachment, abstract, specific aims page, biosketch). Do NOT use this skill to revise an existing .docx with tracked changes — that is `docx-review`'s job.
---

# pandoc-docx

Create clean first-draft Word documents from Markdown with pandoc. The skill ships a bundled **NIH-formatted reference template** at `assets/nih-reference.docx` and applies it automatically unless the user explicitly overrides with `--reference-doc`.

## When to use this skill (vs. docx-review)

| Task | Skill |
|---|---|
| "Create a Word document from this outline / markdown" | **pandoc-docx** |
| "Generate a clean manuscript draft in .docx" | **pandoc-docx** |
| "Convert this NIH specific-aims markdown into the right format" | **pandoc-docx** |
| "Add tracked changes to this .docx" | docx-review |
| "Respond to the reviewer's comments in the .docx" | docx-review |
| "Diff these two .docx files" | docx-review |

**Rule of thumb:** if a `.docx` doesn't exist yet, use this skill. If it does and the user wants edits visible to a reviewer, use docx-review.

## Install (workspace)

`pandoc` is the only required dependency. The Coder workspace's startup script
installs it; if missing:

```bash
brew install pandoc
```

The NIH reference template is bundled at `assets/nih-reference.docx` (this skill's directory). Treat that path as canonical — do not regenerate or modify.

## Default workflow

```bash
# Path to the bundled template — resolve relative to wherever the skill lives.
NIH_REF="$(dirname "$0")/assets/nih-reference.docx"   # if invoked as a script
# Or, when running ad hoc:
NIH_REF=~/.codex/skills/pandoc-docx/assets/nih-reference.docx

# 1. Convert markdown to docx with NIH formatting
pandoc manuscript.md \
  --reference-doc="$NIH_REF" \
  -o manuscript.docx

# 2. Open in Word / LibreOffice to verify
open manuscript.docx                  # macOS
xdg-open manuscript.docx              # Linux
```

Output is clean (no tracked changes) by default.

## NIH formatting baked into the template

The reference template at `assets/nih-reference.docx` enforces NIH grant-application formatting:

| Property | Value | Source |
|---|---|---|
| Font | Arial | NIH grant guide |
| Size | 11 pt | NIH grant guide |
| Line spacing | Single | NIH grant guide |
| Margins | 1 inch on all sides | NIH minimum 0.5" |
| Page size | US Letter (8.5 × 11") | NIH default |
| Heading hierarchy | H1 → H2 → H3 with NIH style IDs | template-defined |

The template defines 49 named styles (Heading1–Heading3, Abstract, AbstractTitle, BodyText, Bibliography, Caption, FirstParagraph, FootnoteReference, etc.) — pandoc uses them automatically based on Markdown structure (`#` → Heading1, `##` → Heading2, blockquotes → BlockText, etc.).

NIH guide reference: <https://grants.nih.gov/grants/how-to-apply-application-guide/format-and-write/format-attachments.htm>

## Common patterns

### Manuscript draft

```bash
# Manuscript with sections, citations as plain text refs
pandoc manuscript.md \
  --reference-doc=$(dirname "$0")/assets/nih-reference.docx \
  --toc \
  -o manuscript.docx
```

### NIH Specific Aims page (single page)

```bash
pandoc specific-aims.md \
  --reference-doc=$(dirname "$0")/assets/nih-reference.docx \
  -o specific-aims.docx
```

### Abstract (250 words, single block)

```bash
pandoc abstract.md \
  --reference-doc=$(dirname "$0")/assets/nih-reference.docx \
  -o abstract.docx
```

### With a bibliography (CSL JSON or BibTeX)

```bash
pandoc manuscript.md \
  --reference-doc=$(dirname "$0")/assets/nih-reference.docx \
  --citeproc \
  --bibliography=refs.bib \
  --csl=american-medical-association.csl \
  -o manuscript.docx
```

### User wants a non-NIH layout

If the user passes their own `--reference-doc`, **respect that override** — do not silently re-apply the NIH template. They may need a journal-specific template (e.g., Cell, JAMA).

## Markdown conventions that round-trip cleanly

| Markdown | Word output |
|---|---|
| `# Title` | Heading 1 (Arial 14pt bold) |
| `## Section` | Heading 2 (Arial 12pt bold) |
| `### Subsection` | Heading 3 (Arial 11pt bold italic) |
| `**bold**` | Bold |
| `*italic*` | Italic |
| `> quote` | BlockText style |
| `1. item` / `- item` | Numbered/bulleted list |
| `[link](url)` | Hyperlink |
| `[@cite2024]` (with `--citeproc`) | Formatted in-text citation |
| `![caption](fig.png)` | CaptionedFigure with auto-caption |

## What this skill does NOT do

- **Tracked changes / comments / revisions**: that is `docx-review`'s job. Do not try to insert `<w:ins>` or `<w:del>` markup with pandoc; the output won't be valid.
- **Specific NIH form attachments** (R&R Cover, PHS Assignment Request, etc.): those are PDF forms downloaded from the NIH website and filled with Adobe Acrobat. Pandoc cannot generate them.
- **Endnote field-code references**: pandoc emits inline citations or a Bibliography section, not Endnote XML field codes. If the user needs `{HYPERLINK...}` Endnote fields, use cliproxy's research-pipeline endnote generator.

## Troubleshooting

| Symptom | Cause | Fix |
|---|---|---|
| "pandoc: not found" | not installed in workspace | `brew install pandoc` (or rerun the workspace startup script) |
| Output looks like Calibri 11pt, not Arial | `--reference-doc` not passed or path wrong | check `ls $(dirname "$0")/assets/nih-reference.docx` resolves; pass an absolute path if invoking from a non-script context |
| Headings render as plain bold text | Markdown source uses `**Section**` instead of `## Section` | rewrite as ATX-style headings |
| `--citeproc` warns "no bibliography" | `--bibliography` flag missing | add `--bibliography=refs.bib` |

## References

- `references/cookbook.md` — copy-paste-ready recipes (manuscript, specific aims, abstract, with bibliography)
- Bundled template: `assets/nih-reference.docx`
- Pandoc DOCX docs: <https://pandoc.org/MANUAL.html#docx>
