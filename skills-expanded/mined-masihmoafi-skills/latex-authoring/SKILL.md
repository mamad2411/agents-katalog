---
name: latex-authoring
description: Write, structure and compile LaTeX papers and reports (NeurIPS, ICML, ICLR, IEEE, ACM), including Persian and English XeLaTeX. Use for TeX manuscripts, LaTeX/XeLaTeX build errors, BibTeX checks or TikZ diagrams.
---

# LaTeX authoring

Write, compile, debug and check LaTeX manuscripts with a modular layout, a clean build and verified citations.

## Layout and style

- Split the paper: `main.tex` (class, packages, `\input` of sections), `macros.tex` (notation, defined once), `references.bib`, `sections/`, `figures/`, `tables/` (one file per table). Never one big `.tex`.
- Load `hyperref` late, then `cleveref` right after it.
- `align`/`align*` for multi-line equations, never `$$` or `eqnarray`; number only equations the text cites.
- `booktabs` tables with no vertical rules; numbers right-aligned.
- Floats `[t!]`, and `\FloatBarrier` at section ends so figures stay in their section.

## Persian and English with XeLaTeX

For Babel Farsi (RTL) with English (LTR):

- Put a blank line before every LTR environment (`\begin{otherlanguage}{english}`, `\begin{LTR}`) so the RTL paragraph ends first; this prevents the `\endL or \endR` error.
- Define the English typewriter font in the preamble:
  ```latex
  \babelfont{tt}[]{DejaVu Sans Mono}
  \babelfont[english]{tt}[]{DejaVu Sans Mono}
  ```
- When editing `.tex` files from Python, never write `\b` in a normal string: `"\babelfont"` becomes a backspace plus `abelfont`, and XeLaTeX draws empty boxes. Use `r"\babelfont"` or `"\\babelfont"`.
- B Nazanin cannot draw the text bullet (U+2022), so redefine list bullets as math symbols, which use the math fallback font:
  ```latex
  \renewcommand{\labelitemi}{$\bullet$}
  \renewcommand{\labelitemii}{$-$}
  \renewcommand{\labelitemiii}{$\ast$}
  \renewcommand{\labelitemiv}{$\cdot$}
  ```
- Wrap every English word inside Persian text in `\eng{...}` (for example `\newcommand{\eng}[1]{\foreignlanguage{english}{#1}}`), and every Latin name or word in math in `\mathrm{...}` or `\text{\eng{...}}`; otherwise it falls back to the Persian font and renders as empty squares.
- B Nazanin draws the zero-width non-joiner (U+200C) as a square; replace each ZWNJ with a space.

## Compile

```bash
latexmk -pdf -synctex=1 -interaction=nonstopmode -halt-on-error main.tex      # pdfLaTeX
latexmk -xelatex -synctex=1 -interaction=nonstopmode -halt-on-error main.tex  # XeLaTeX, Persian and English
```

A clean build has no undefined references (`??`) and no missing citations. When it fails, filter the log instead of reading it:

```bash
rg -A 3 -B 1 '^!|LaTeX Warning|Package.*Warning' main.log | rg -v 'fontspec' | head -n 40
```

| Log message | Cause | Fix |
| :--- | :--- | :--- |
| `! Undefined control sequence.` | Macro typo or missing package | Check `macros.tex` or load the package |
| `Reference '...' undefined` | Missing `\label` or second pass | Add the label; rerun `latexmk` |
| `Citation '...' undefined` | Key missing from `references.bib` | Fix the key spelling; rerun the build |
| `Overfull \hbox (X pt too wide)` | Equation, table or word wider than the column | Split with `split` or `multline`; narrow the table |
| `\endL or \endR` (XeLaTeX, RTL) | No paragraph break before an LTR block | Add a blank line before the LTR block |

## Citations

1. Give every entry a `doi`, an `eprint` or its exact venue. Never invent authors, titles or entries.
2. Use full fields: `author`, `title`, `booktitle` or `journal`, `volume`, `pages`, `year`, `doi`.
3. Find duplicate keys: `rg -o '^@[a-zA-Z]+\{[^,]+' references.bib | sort | uniq -d`.
4. After a successful build, compare bibliography keys with the keys cited in all `.aux` files (or the `.bcf` file for Biber), counting `\nocite`. Report unused keys; remove them only when cleanup is in scope. A syntax check does not prove usage, and failed checks stay visible in the report.

## Render and open

1. Render pages and inspect them for overfull boxes, float collisions and missing glyphs:
   ```bash
   mkdir -p /tmp/paper_renders && pdftoppm -png -r 150 -f 1 -l 3 main.pdf /tmp/paper_renders/page
   ```
2. Open the PDF for the user with the environment's opener and confirm the viewer started.
