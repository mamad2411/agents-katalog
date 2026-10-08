---
name: latex-tips-and-tricks
description: >
  Best-practice LaTeX hygiene for scientific papers, theses, and technical
  reports, distilled from dspinellis/latex-advice. Use this skill whenever
  the user is writing, editing, or reviewing .tex source — including tasks
  like structuring a paper, formatting math or tables, managing references,
  setting up a build system, or asking "how should I do X in LaTeX". Also
  trigger when the user asks about LaTeX packages, cross-referencing, figure
  placement, or typography issues.
---

# LaTeX Tips and Tricks

Source: https://github.com/dspinellis/latex-advice

## Source control

Keep all `.tex`, `.bib`, and figure sources in Git. Never commit generated
files (`.pdf`, `.bbl`, `.aux`). Use `latexmk` for the build — it handles
multi-pass recompilation automatically. Tag each submitted revision with
`git tag -a`. Delete commented-out text; the repo preserves history.

## Source readability

Hard-wrap lines at 60-70 characters. Apply semantic line breaks: one clause
or phrase per line so that `git diff` shows phrase-level changes, not
reflowed paragraphs. Mark work-in-progress with `% TODO` or `% XXX`. For
multi-chapter documents use `\include`/`\includeonly`; keep single papers in
one file to ease global search and section reordering.

## Semantic markup, never manual formatting

Use structural commands (`\section`, `\emph`, `\texttt`) rather than visual
ones (`\large\bfseries`, `\textit` for mere emphasis). Define
document-specific macros for recurring notation — a single edit then
propagates everywhere.

## Cross-references

Label every float and equation: `\label{fig:loss}`, `\label{tab:ablation}`,
`\label{eq:bellman}`. Reference via `\Cref{...}` from `cleveref` — never
hard-code "Figure~\ref{...}". Use namespaced prefixes consistently: `fig:`,
`tab:`, `sec:`, `eq:`, `alg:`.

## Mathematics

Every math symbol — inline or display — goes in math mode. Prefer `\[...\]`
for display math over `$$...$$` (the latter is plain TeX and breaks spacing).
Use `\DeclareMathOperator` for named operators (`\argmax`, `\softmax`).
Prefer `align` over `eqnarray`; the latter has known spacing bugs. Punctuate
display equations as prose: place a period or comma after the final line of a
derivation. Do not abuse math mode for plain-text subscripts; write
`RQ\textsubscript{2}`, not `$RQ_2$`.

## Tables

Never use `\hline` or column `|` rules. Use `\toprule`, `\midrule`,
`\bottomrule` from `booktabs`. Align numbers right (or on the decimal point
via `siunitx`), text left, isolated symbols centered. Use hard tabs before
`&` to keep columns visually aligned in source.

## Figures and floats

Use vector formats (PDF, EPS) for diagrams; raster (PNG ≥300 dpi) only for
photographs. Match font family and size across all figures. Place `\caption`
below figures, above tables. Let LaTeX place floats — avoid `[h!]` overrides
until the paper is finalized. Every figure and table must be cited in the
text before it appears.

## Typography and punctuation

- Use `~` before `\cite`, `\Cref` to suppress a line break: `result~\cite{X}`.
- After an abbreviation period add `\ ` to suppress sentence spacing: `et al.\ found`.
- Use `` ` `` and `'` for quotes, never `"`. Or use `\enquote{}` from `csquotes`.
- Use `\dots` for ellipses, `--` for en-dash (ranges), `---` for em-dash.
- Load `microtype` for protrusion and font expansion; it reduces overfull boxes silently.
- Load `hyperref` last in the preamble.
- Never underline for emphasis; avoid ALL-CAPS passages.
- Treat overfull/underfull `\hbox` warnings as bugs, not noise.

## Bibliography

Maintain a single central `.bib` file shared across projects. Use
`biber`+`biblatex` for new work; fall back to `bibtex` only when venue style
files require it. Cite with `\cite[p.~42]{Key}` when pointing to a specific
page or theorem.
