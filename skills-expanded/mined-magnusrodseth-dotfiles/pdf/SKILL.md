---
name: pdf
description: "Export markdown as professional PDF using pandoc + typst (no LaTeX needed). Use when the user asks to: create a PDF, export markdown to PDF, generate a report/handout/document as PDF, or when they mention PDF, pandoc, print-ready, or document export."
---

# Markdown to PDF

Export markdown files as professional PDFs using **pandoc + typst**. Typst is the
default engine: it needs no LaTeX toolchain, is fast, and handles full Unicode
(including æ/ø/å) out of the box. An optional eisvogel + xelatex path is available
for a branded colored title page when a LaTeX install is present.

## Prerequisites

- `pandoc` (3.0+): `brew install pandoc`
- `typst` (0.11+): `brew install typst`

That's it for the default path. Everything below works with just pandoc + typst.

**Optional** (only for the branded `--engine xelatex` title-page path):

- LaTeX with xelatex: `brew install --cask basictex`
- Eisvogel template: download `eisvogel.latex` from
  https://github.com/Wandmalfarbe/pandoc-latex-template/releases into
  `~/.local/share/pandoc/templates/`
- LaTeX packages: `tlmgr --usermode install adjustbox babel-german background bidi collectbox csquotes everypage filehook footmisc footnotebackref framed fvextra letltxmacro ly1 mdframed mweights needspace pagecolor sourcecodepro sourcesanspro titling ucharcat ulem unicode-math upquote xecjk xurl zref`

Mermaid diagrams (optional): `npm install -g @mermaid-js/mermaid-cli`

## Quick Export

```bash
bash ~/.claude/skills/pdf/scripts/md-to-pdf.sh \
  -o report.pdf \
  -t "Report Title" \
  -s "Subtitle" \
  -a "Author Name" \
  --lang nb \
  --toc \
  input.md
```

Defaults to the typst engine and to the house style below. For the branded
colored title page instead, add `--engine xelatex` (requires the optional LaTeX
install above).

## House Style (typst default)

`md-to-pdf.sh` ships an opinionated default look. It is tuned for dense,
table-heavy documents that get read on screen and sent to other people. You get
it by doing nothing; every part is overridable.

| Setting | Default | Why |
|---|---|---|
| Body font | Helvetica Neue, 10pt | Sans reads better on screen than the typst serif default. Falls back to the engine font when Helvetica Neue is not installed, so this stays portable. |
| Margins | 0.8in | 1in wastes width that wide tables need. |
| Headings | `#123a5c` dark slate blue | Sections findable when skimming, without looking like a rainbow. |
| Links | `#0b57d0` blue | Readable when printed in greyscale, unlike pure `blue`. |
| Tables | 8.8pt, ragged right, no hyphenation | The important one, see below. |
| Table header row | Bold | Header stays distinct once the body text is small. |

**The table rule is what matters most.** Pandoc's typst template justifies every
paragraph, including inside table cells. In a narrow cell that produces stretched
word spacing and hyphenation like `Torremoli-nos` or `Web Sum-mit`. Turning
justification and hyphenation off *inside tables only* fixes it while leaving
body prose justified.

Three more fixes come from `table-typography.lua`, applied by default:

1. **Columns written `|---|` are left-aligned, not centered.** Pandoc marks them
   `AlignDefault` and the typst writer centers them; centered prose in a table
   reads badly. Columns that explicitly ask with `|:---|` or `|---:|` are left
   alone, so right-aligned number columns still work.
2. **Numbers do not break across lines.** `10 400` is three tokens to pandoc, so a
   narrow cell splits it into `10 400-11` / `500`. Thousands groups are joined
   with a non-breaking space.
3. **A cell starting `16.` is not turned into a list.** That is enumeration syntax
   in typst's *own* markup, so such a cell silently renders with `16.` on one line
   and the rest indented below. Pandoc emits it as ordinary text, so this only
   ever shows up in the PDF. A non-breaking space after the marker defuses it.

Disable all three with `--no-typography`.

### Script Flags

| Flag | Default | Description |
|------|---------|-------------|
| `-o, --output` | (required) | Output PDF path |
| `-t, --title` | "Untitled" | Document title |
| `-s, --subtitle` | "" | Subtitle |
| `-a, --author` | "" | Author name |
| `-d, --date` | today | Date (DD.MM.YYYY) |
| `--engine` | typst | `typst` (default) or `xelatex` (branded title page) |
| `--lang` | en | Document language code (e.g. `nb` for Norwegian Bokmål) |
| `--toc` | off | Include table of contents |
| `--highlight-style` | tango | Code syntax theme |
| `--mainfont` | Helvetica Neue if installed | Body font, e.g. "Iowan Old Style" |
| `--monofont` | engine default | Code font (e.g. "Menlo") |
| `--fontsize` | 10pt | Body font size |
| `--margin` | 0.8in | Page margins |
| `--heading-color` | 123a5c | Heading hex, with or without `#` (**typst only**) |
| `--link-color` | 0b57d0 | Link hex, with or without `#` (**typst only**) |
| `--table-fontsize` | 8.8pt | Table text size (**typst only**) |
| `--no-typography` | off | Turn off table alignment / non-breaking number fixes |
| `--mermaid` | off | Pre-render mermaid diagrams (requires mmdc) |
| `--title-color` | 1e293b | Title-page background hex (**xelatex only**) |
| `--text-color` | ffffff | Title-page text hex (**xelatex only**) |
| `--no-titlepage` | off | Skip title page (**xelatex only**; typst has no separate title page) |

Multiple input files are concatenated with page breaks between them.

## Custom Export Workflow (typst)

When assembling a document by hand or needing fine control, call pandoc directly.

### Step 1: Write or Assemble Markdown

Standard markdown features:

- `#` for major sections, `##` for subsections
- Standard markdown tables
- Fenced code blocks with a language ID for syntax highlighting
- `[colored text]{color="red"}` for colored text (via `color-spans.lua`; works in typst)
- Markdown links render blue automatically

### Step 2: Run Pandoc with the typst engine

```bash
pandoc input.md -o output.pdf \
  --from=markdown+bracketed_spans \
  --pdf-engine=typst \
  --syntax-highlighting=tango \
  --toc --toc-depth=3 \
  --lua-filter=~/.claude/skills/pdf/scripts/color-spans.lua \
  --lua-filter=~/.claude/skills/pdf/scripts/table-typography.lua \
  -V margin-x=0.8in \
  -V margin-y=0.8in \
  -V fontsize=10pt \
  -V mainfont="Helvetica Neue" \
  -V 'header-includes=#show link: set text(fill: rgb("#0b57d0"))
#show heading: set text(fill: rgb("#123a5c"))
#show heading.where(level: 1): set block(above: 1.7em, below: 0.9em)
#show table: it => {
  set par(justify: false, leading: 0.55em)
  set text(hyphenate: false, size: 8.8pt)
  it
}
#show table.cell.where(y: 0): set text(weight: "bold")' \
  --metadata title="Title" \
  --metadata subtitle="Subtitle" \
  --metadata author="Author" \
  --metadata date="19.06.2026" \
  --metadata lang=nb
```

`header-includes` is raw typst injected into the preamble, and it is where the
whole house style lives. It is multi-line: keep it in single quotes so the `#`
show rules survive the shell.

**Do not detect fonts with `typst fonts | grep -q`.** Under `set -o pipefail`,
`grep -q` closes the pipe on its first match and `typst` dies with SIGPIPE, so
the pipeline reports failure exactly when the font *is* installed. Read the list
into a variable and use a here-string, as `md-to-pdf.sh` does.

### typst variables (via `-V`)

| Variable | Example | Notes |
|----------|---------|-------|
| `margin-x` / `margin-y` | `2cm` | Horizontal / vertical page margins |
| `papersize` | `a4` | Defaults to a4 |
| `fontsize` | `11pt` | Body font size |
| `mainfont` | `Helvetica Neue` | System font name (macOS resolves these) |
| `monofont` | `Menlo` | Code font |
| `section-numbering` | `1.1.1` | Numbered headings |
| `header-includes` | `#show link: set text(fill: blue)` | Raw typst injected into the preamble |

Title, subtitle, author, and date come from `--metadata`; the typst template
renders them as a centered heading block at the top of page one.

## Optional: Branded Title Page (eisvogel + xelatex)

Only when you specifically want the colored full-page title and a LaTeX toolchain
is installed (see optional Prerequisites). Add `--engine xelatex` to the script, or
run pandoc directly:

```bash
pandoc input.md -o output.pdf \
  --from=markdown+bracketed_spans \
  --template=eisvogel \
  --pdf-engine=xelatex \
  --syntax-highlighting=tango \
  --toc --toc-depth=3 \
  --lua-filter=~/.claude/skills/pdf/scripts/color-spans.lua \
  -V titlepage=true \
  -V titlepage-color="1e293b" \
  -V titlepage-text-color="ffffff" \
  -V titlepage-rule-color="ffffff" \
  -V titlepage-rule-height=2 \
  -V toc-own-page=true \
  -V colorlinks=true -V linkcolor=blue -V urlcolor=blue \
  -V mainfont="Helvetica Neue" -V monofont="Menlo" \
  -V fontsize=11pt -V geometry:margin=1in \
  --metadata title="Title" --metadata author="Author"
```

If xelatex is not installed this path fails with `xelatex not found` — use the
default typst engine instead.

## Mermaid Diagrams

If the markdown contains mermaid code blocks, use the `--mermaid` flag with
`md-to-pdf.sh`. It pre-processes mermaid blocks into SVG before PDF generation.
Requires `mmdc` (mermaid-cli): `npm install -g @mermaid-js/mermaid-cli`.

## Highlight Styles

Available syntax themes: `pygments`, `tango`, `espresso`, `zenburn`, `kate`,
`monochrome`, `breezedark`, `haddock`.

## Bundled Scripts

| File | Purpose |
|------|---------|
| `scripts/md-to-pdf.sh` | One-command markdown to PDF export (typst default, `--engine xelatex` optional) |
| `scripts/color-spans.lua` | Enables `[text]{color="red"}` syntax (typst + LaTeX + HTML) |
| `scripts/table-typography.lua` | Left-aligns default columns, keeps numbers unbroken, stops `16.` cells becoming lists |
| `scripts/render-mermaid.sh` | Pre-renders mermaid blocks to SVG |
