---
name: latex-debugging
description: Debugging LaTeX documents — PDF text analysis, macro argument pitfalls, spacing diagnostics
category: software-development
---

# LaTeX Debugging

Diagnose and fix LaTeX layout and macro issues using PDF text extraction and targeted checks.

## When to Use

- Resume/paper layout looks wrong and you need exact positions
- A macro argument isn't being parsed as expected
- Bullet text has poorly filled last lines
- Spacing between elements doesn't match what the code suggests

## PDF Text Position Analysis

Use PyMuPDF to extract precise character/line positions from the compiled PDF:

```python
import fitz
doc = fitz.open('main.pdf')
page = doc[0]
blocks = page.get_text('dict')['blocks']
for b in blocks:
    if 'lines' in b:
        for l in b['lines']:
            text = ''.join([s['text'] for s in l['spans']])
            x0, y0, x1, y1 = l['bbox']  # left, top, right, bottom in pt
            font = l['spans'][0]['font']
            size = l['spans'][0]['size']
            print(f'Y={y0:5.1f} X=({x0:4.0f}-{x1:4.0f}) {text[:100]}')
```

### Checking page fit

```python
doc = fitz.open('main.pdf')
print(f'Pages: {len(doc)}')
# First/last text position:
blocks = doc[0].get_text('dict')['blocks']
import math
first_y, last_y = math.inf, 0
for b in blocks:
    if 'lines' in b:
        for l in b['lines']:
            y0, y1 = l['bbox'][1], l['bbox'][3]
            first_y = min(first_y, y0)
            last_y = max(last_y, y1)
print(f'Bottom margin: {doc[0].rect.height - last_y:.1f}pt')
```

### Bullet line fullness analysis

Identify bullets where the last line is poorly filled (<80% of available width):

```python
LINE_FULL = 543  # page width minus margins (adjust for your geometry)
for b in blocks:
    if 'lines' in b:
        for l in b['lines']:
            x0, y0, x1, y1 = l['bbox']
            text = ''.join([s['text'] for s in l['spans']])
            if x0 < 30:  # bullet marker at leftmargin
                continue  # first line of item
            # Continuation line (wrapped) — check fill %
            fill_pct = (x1 - x0) / LINE_FULL * 100
            if fill_pct < 80:
                print(f'  Y={y0:.0f} last line at {fill_pct:.0f}%: {text[:50]}')
```

## Common LaTeX Pitfalls

### 1. `O{}` optional args use `[]` brackets

In `\\NewDocumentCommand`, the `O{}` specifier matches **square brackets `[...]`** exclusively. Curly braces `{...}` are NOT consumed as optional arguments.

```latex
\\NewDocumentCommand{\\ResumeItem}{O{#2} m O{} O{} O{}}

% WRONG — {City} is NOT #5, becomes stray text:
\\ResumeItem{Title}[Sub][Date]{City}

% CORRECT — [City] is parsed as #5:
\\ResumeItem{Title}[Sub][Date][City]
```

Diagnosis: if a parameter that should be rendered with special formatting (italic, right-aligned) appears as plain text on the wrong line, check whether `{}` was used instead of `[]`.

### 2. `\\tl_if_empty:nT` vs `\\tl_if_empty:nF` in expl3

```latex
\\tl_if_empty:nT {#5} {...}  % executes if #5 IS empty     (T = true branch)
\\tl_if_empty:nF {#5} {...}  % executes if #5 is NOT empty (F = false branch)
```

The letter after `n` refers to which branch is provided, not the function name:
- `nT` = `True` branch → runs when EMPTY
- `nF` = `False` branch → runs when NOT EMPTY

A common mistake: using `\\tl_if_empty:nF` when you mean `\\tl_if_empty:nT` (or vice versa) silently inverts the logic.

### 3. `\\vspace` at end of macro gets eaten

When `\\vspace` is the last thing in a macro and the next thing in the .tex is a blank line, the paragraph break can neutralize the vspace. Either:
- Remove the blank line between the macro and `\\begin{itemize}`
- Use `\\vspace*` (starred variant)

## Spacing Diagnostics

Key variables and their effects in enumitem:

| Parameter | Effect |
|-----------|--------|
| `itemsep` | Extra vertical space between consecutive items |
| `parsep` | Paragraph spacing inside list items |
| `topsep` | Space before the list environment |
| `partopsep` | Extra space when list starts a new paragraph (blank line before `\\begin{itemize}`) |
| `\\parskip` | Global paragraph skip — affects everything |

Check the interplay: `\\parskip` persists inside lists unless explicitly overridden by `parsep`/`topsep`. When all list spacing is zero but gaps still appear, check `\\parskip` and blank lines in the source.

## Native TikZ Figures (no PNG, no pgfplots)

User preference for LaTeX deliverables (papers/reports): **all figures drawn natively in TikZ**. Data plots (bar charts, error bars, ablations) are hand-drawn with `\fill` rectangles + `\draw` error bars; values are computed from source JSON first, then hardcoded into coordinates.

### Pitfalls (each hit in real sessions)

1. **`\n` is NOT a line break in TikZ node text** — causes `! LaTeX Error: Not allowed in LR mode`. Use `\\`:
   ```latex
   % WRONG — \n is an undefined control sequence in node text
   \node at (0,0) {joint\nviolation-only};
   % CORRECT
   \node[align=center] at (0,0) {joint\\violation-only};
   ```
2. **`below=... of` positioning with multiline text needs `align=center`**:
   ```latex
   % WRONG — "Not allowed in LR mode"
   \node[below=0.28cm of noisy] {10--30\% omissions,\\box misalignment};
   % CORRECT
   \node[align=center, below=0.28cm of noisy] {10--30\% omissions,\\box misalignment};
   ```
3. **pgfplots "Environment axis undefined"** — symptom: package loads (version prints) but `\begin{axis}` fails. Cause on TeX Live basic: user-dir `pgfplots.sty` (old) mixed with newer `pgfplots.code.tex`, or missing install. **Fix: skip pgfplots entirely and hand-draw with pure TikZ** (bars = `\fill rectangle`, axes = `\draw -{Stealth}`, error bars = vertical `\draw` lines). Pure TikZ has no such dependency and always compiles.
4. **Hardcoded plot coordinates from JSON** — before writing a TikZ data plot, run a small script that reads `experiments/*.json` and prints mean±std per group; transcribe those numbers into the `\fill`/`\draw` calls. This doubles as a honesty check (numbers in the figure trace to real data) and avoids miscalculated scales.
4b. **Poster figures hardcode numbers — VERIFY against repo JSON before porting/trusting them** — poster TikZ often carries hand-transcribed stats that do NOT match the authoritative JSON. Real case: poster missed-fraction histogram claimed 4/12/36/54/94; recomputing from `experiments/vlm_completion/pipeline_per_image.json` (fn/n_gt, center-distance 0.1, half-open bins) gave 4/12/31/59/94 — buckets 3–4 off by ±5, and no script had ever generated the poster numbers. Porting a poster figure into a report: (a) recompute the statistic from the JSON first; (b) if it differs, regenerate the figure data from JSON and update BOTH poster and report; (c) annotate the TikZ comment with the exact source file + definition (e.g. "fn/n_gt with center-distance matching at 0.1, from pipeline_per_image.json") so it is reproducible. A scatter that DID reproduce exactly (32 points, r = 0.9604 vs poster's 0.96) shows the check usually passes — run it anyway.
5. **Bar-chart scaling** — compute bar length explicitly from data range (e.g. `length = (value - base) * scale`), don't use the raw value as cm; a 0.878–0.939 range plotted directly spans only ~0.06cm and is invisible.
5b. **Error bars NEED end-cap ticks or they read as stray vertical lines** — a bare `\draw (x, top) -- (x, top+std*sc)` above a bar looks like an unexplained mark (user asked "柱状图上方的竖线是什么"). Add a short horizontal cap at the top of every error bar: `\draw (x-0.08, top+std*sc) -- (x+0.08, top+std*sc);` (bar width ~0.6cm → cap half-width 0.08). Check the tallest bar (max mean+std) still fits under the axis top before rendering.
6. **Legend must stay INSIDE the plot bounds** — classic bug: legend coordinates (e.g. `(9.6,5.3)`–`(10.05,5.42)`) exceed the x-axis endpoint (`(0,0) -- (8.7,0)`), so the legend floats outside the chart. Check every legend/figure element's x-range against the axis length. Safe pattern: legend at top-center ABOVE the axis (y above axis top), or inside the plot's empty corner. Same bug bit Fig 5 and Fig 6 in separate sessions — always verify legend x-extent vs axis width.
7. **Grouped x-axis labels: one node PER bar, not one stacked node** — a single `\node at (2.5,-0.5) {joint\\violation-only\\proposal-only}` centers all three labels under the middle bar. Each label needs its own node at its bar's center x (`(1.1,-0.5)`, `(2.5,-0.5)`, `(3.9,-0.5)`). Symptom: labels look "stacked at one point" / misaligned.
8. **Multi-panel charts: per-panel scale so bars have comparable height** — two side-by-side panels with different units (accuracy 0.4–0.9 vs MSE 0.05–0.12) need different scale factors (`\def\sc{4}` vs `\def\scm{30}`) so bars visually match; reusing one scale makes one panel look empty. Name them distinctly (`\sc`, `\scm`) and update error bars with the same factor.
9. **Overwide TikZ figure → wrap in `\resizebox{\textwidth}{!}{...}`** — a figure spanning x=0..16cm exceeds textwidth (~16.5cm on letter with 1in margins); the excess shows as a mysterious `Overfull \hbox (48pt too wide)` whose line number points at the caption, not the figure. Wrap the whole `tikzpicture` in `\resizebox{\textwidth}{!}{% ... }` to fit. If Overfull pt value doesn't change when you edit the caption text, the culprit is the figure itself, not the caption.
10. **patch tool double-escapes backslashes in LaTeX — BOTH `mode='patch'` (V4A) AND `mode='replace'`** — editing a .tex line containing commands (`\textbf`, `\par`, `\Delta`, `\emph`) can silently write literal `\\textbf` (double backslash) into the file. Real case: replace-mode edit of `{\normalsize\textbf{Summer Research Project}\par}` produced `{\\normalsize\\textbf{...}\\par}` → `! LaTeX Error: There's no line here to end` at that line (the lone `\\` becomes a linebreak command, `normalsize` renders as stray text). **The tool's diff display shows `\\` regardless of actual bytes — never trust the diff, verify the file.** Checks/fixes:
    - Verify bytes: `sed -n '<line>'p main.tex | od -c` — correct shows single `\` per command, doubled shows `\ \`. (macOS has no `cat -A`; use `od -c`.)
    - After a build, `grep -c "^!" main.log` (non-zero = errors); "There's no line here to end" pointing at your edited line = doubled backslashes. Note xelatex can exit non-zero even when "Output written on main.pdf" appears — trust the log grep, not the exit code.
    - **Reliable fix for backslash-heavy .tex edits: skip the patch tool entirely.** `write_file` a small Python script with raw strings and run it: `bad = r'{\\normalsize\\textbf{Summer Research Intern Project}\\par}'` / `good = r'{\normalsize\textbf{Summer Research Intern Project}\par}'` / `assert bad in t` / `p.write_text(t.replace(bad, good))`. Inline `python3 -c` is escaping hell (SyntaxWarning + assert failures) — always use a script file.
11. **Y-tick labels overlap their tick lines** — `\draw (-0.1,y) -- (0.1,y) node[left] {\v}` anchors the label at the path END (0.1, y), so the label sits ON the tick line. Fix: draw the tick, then place the label separately with `anchor=east` at a point left of the tick's start: `\draw (-0.1,y) -- (0.1,y); \node[anchor=east, font=\tiny] at (-0.15,y) {\v};`. Same class of bug as #6/#7: verify label extent vs the geometry it labels.
12. **Long grouped x-axis labels overlap → rotate 45°** — when labels like `violation-only` (~1.7cm) + `proposal-only` (~1.6cm) sit at bar centers only 1.4cm apart, horizontal half-widths sum (1.66cm) > spacing → collision. Fix: `\node[font=\scriptsize, rotate=45, anchor=east] at (barx, -0.45) {label};` per bar (academic-standard). Also give the axis title enough clearance below tick labels (tick digits ~0.15cm tall; keep axis title ≥0.5cm below, e.g. y=-1.5 not -1.0).
13. **mathptmx needs rsfs10 (missing on TeX Live basic)** — `\usepackage{mathptmx}` dies at `xdvipdfmx:fatal: Unable to find TFM file "rsfs10"` (Ralph Smith Formal Script not in the basic scheme). Fixes: (a) `\usepackage{times}` (Times text, CM math, no rsfs dependency), or (b) under XeLaTeX `\usepackage{fontspec}\setmainfont{Times New Roman}` for true TNR (verify with `pdffonts`). **User preference is FIRM: true Times New Roman via fontspec** — they rejected `times`/`mathptmx` substitutes ("我没让你换字体 改回Times New Roman"). Same install: `IEEEtran.bst` is NOT bundled with the cls in the template zip — download it to the paper dir (CTAN `macros/latex/contrib/IEEEtran/bibtex/IEEEtran.bst`); a local .bst in the working dir beats the system tree.
13b. **`\renewcommand{\ttdefault}{cmtt}` SILENTLY FAILS under fontspec (XeLaTeX)** — the TU encoding override is ignored and `\texttt{}` falls back to LMRoman, so code identifiers (CONTAINMENT, ALIGN_LEFT) render in proportional serif indistinguishable from body text. `pdffonts` shows NO monospace font at all. **Correct fix: `\setmonofont{Courier New}`** after `\setmainfont` (system font, works on macOS), and DELETE the stale `\ttdefault` line. Verify: `pdffonts main.pdf` must show `CourierNewPSMT` embedded, zero "Font shape TU/cmtt/m/n undefined" warnings, and render at ≥200dpi to visually confirm monospace. The old `\ttdefault{cmtt}` advice only works for pdflatex/OT1, not XeLaTeX/fontspec.
14. **Rotated y-axis title vs tick labels** — a rotated 90° axis title placed at `x=-0.55` collides with `anchor=east` tick labels whose right edge is at `x=-0.15` (labels extend LEFT from there ~0.4–0.5cm). Long titles ("Proposal IoU" spans ~1.2cm horizontally when rotated) need generous clearance: `at (-1.45, 2.4)`; short titles ("Score") need less (`-0.95`). Rule: after placing tick labels with `anchor=east at (-0.15,y)`, place the rotated title so title-left-extent < label-right-extent, i.e. `x_title ≤ -0.15 - label_width - gap`. Verify by rendering the page and eyeballing (same check loop as figures).
15. **Tables: caption-to-body spacing + full-width + bold headers** — user requirements for report tables: (a) caption sits too close to the table body by default → add `\usepackage{caption}` + `\captionsetup[table]{skip=14pt}` (10pt was still too tight per user); (b) tables must span the text width → switch `tabular` → `tabularx{\textwidth}` with flex columns: `{lXX}` (3 cols, 2 flex), `{Xc}` (2 cols, left flex), `{Xccc}` (4 cols, first flex). `booktabs` rules (\toprule/\midrule/\bottomrule) stay the same. Don't invent an empty filler column to pad width (`lcccX` with blank trailing cells looks wrong) — make the FIRST data column the flex `X` instead. (c) **header row must be bold**: `\textbf{...}` on every header cell (`\textbf{Type} & \textbf{Predicate} & \textbf{Example}`) — user explicitly asked ("表头加粗"); check ALL tables, the first one may already be bold while others aren't. Verify caption gap visually (should be clearly larger than line spacing), table edges align with body-text margins, and header weight visibly thicker than data rows.
15c. **Table captions must get the SAME margin indent as figure captions** — when the user asks for indented captions ("图注左右各缩进3cm"), apply `margin=3cm` to BOTH figure AND table: `\captionsetup[table]{skip=14pt, margin=3cm}` + `\captionsetup[figure]{margin=3cm}`. Setting only `[figure]{margin=3cm}` leaves table captions full-width — the inconsistency is visible and the user WILL flag it ("Table X 描述为什么没有左右缩进 有没有跟标准走"). caption package applies `margin` symmetrically (both sides); one declaration per float type suffices.
15b. **Error bars under value labels** — when a bar chart shows both value labels AND std error bars, put labels ABOVE the error-bar cap (cap_top + ~0.18), never at `bar_top + 0.15`: a long std bar (e.g. proposal-only std=0.071×scale → top 2.29) crosses a label parked at 2.11, looking like "a stray vertical line through the number". Order per bar: fill bar → draw error line → draw cap → place label above cap.

### 16. natbib superscript citations: link the WHOLE `[n]` including brackets

User requirement: in-text citations rendered as superscript `[1]` where brackets + number are ONE clickable link. Default natbib+hyperref links only the number; `[` sits outside the link (verify: `pdftohtml -xml` shows `<a>1]</a>` with `[` as plain text).

Working preamble (ORDER MATTERS — hack must come AFTER `\usepackage{hyperref}`):
```latex
\usepackage[super]{natbib}
\setcitestyle{super,open={[},close={]}}
...
\usepackage{hyperref}
\makeatletter
% super mode: suppress natbib's per-number inner link
\def\NAT@hyper@#1{%
  \ifNAT@super
    #1%
  \else
    \hyper@natlinkstart{\@citeb\@extra@b@citeb}#1\hyper@natlinkend
  \fi}
\renewcommand\NAT@citesuper[3]{\ifNAT@swa
\if*#2*\else#2\NAT@spacechar\fi
\unskip\kern\p@\textsuperscript{%
  \expandafter\hyper@natlinkstart\expandafter{\NAT@cite@list}%
  \NAT@@open#1\NAT@@close
  \hyper@natlinkend}%
   \if*#3*\else\NAT@spacechar#3\fi\else #1\fi\endgroup}
\makeatother
```

Pitfalls that bit in a real session:
- **hyperref redefines `\NAT@hyper@` on load** — placing the hack after natbib but before hyperref means hyperref silently overwrites it → `! Undefined control sequence`.
- **`\NAT@citesuper`'s #1 (the cite loop body) expands INSIDE `\textsuperscript`** — capturing the key during the `\@for` loop into a `\xdef` var is TOO LATE (loop runs after the link commands are evaluated, `\@citeb` is `\@nil` by then). Don't capture; use `\NAT@cite@list` (sorted key list, already set when citesuper runs). Single-key cites link correctly; multi-key `\cite{a,b}` would target `cite.a,b` (invalid) — fine for reports using only single cites.
- Verify link extent: `pdftohtml -xml -f P -l P main.pdf out.xml`, grep for `<a href=...>[1]</a>`.
- `\setcitestyle{super}` alone renders bare superscript digits (no brackets); `super,open={[},close={]}` adds them.

### 17. Thousands separators in report numbers (user preference)

Every ≥1000 quantity gets a thousands comma; key numbers bold. LaTeX: `4{,}789` (thin-space group separator — same style as the poster); Markdown: plain `4,789`. DO NOT add to: years, reference page ranges (9033–9049), arXiv IDs (2309.16609), decimals, student IDs. Sweep with `grep -noE '[0-9]{4,}' main.tex` and classify each hit. When editing a table row that ends in `\\`, re-verify backslashes with `od -c` (pitfall #10 — a replace-mode patch doubled them once here).

### 18. Cross-references: link label + number together, spelled-out "Figure"

`Fig.~\ref{fig:x}` links only the number; user wants the word inside the link and spelled out: `\hyperref[fig:x]{Figure~\ref{fig:x}}` (same for Table). Bulk-apply with: `s/Fig\.~\\ref\{([^}]+)\}/\\hyperref[$1]{Figure~\\ref{$1}}/g` (also `Table~`). Never write "Fig." in body text.

### 19. PDF metadata: set Title / Author / Creator / Producer from LaTeX (user: all four = their name)

User wants the PDF properties (Creator AND Producer included) to show their name, set inside the .tex so every rebuild is automatic. Engine support DIFFERS:

**XeLaTeX (report-style docs, hyperref):** all four keys work via `\hypersetup`:
```latex
\usepackage{hyperref}
\hypersetup{colorlinks=true, ...,
    pdftitle={...},
    pdfauthor={{Author Name}},
    pdfcreator={{Author Name}},
    pdfproducer={{Author Name}}}
```
Verified: `pdfinfo` shows all four overridden.

**LuaLaTeX (beamer poster, LuaTeX ≥1.10):** hyperref's luatex driver IGNORES pdfcreator/pdfproducer, and beamer writes the RAW `\author{...}` argument into /Author — with a `tabular` in it, /Author becomes garbage like `tbl/hmode/begin@l@ l@ Author: ... tbl/finalizemath/...`. `\hypersetup` in preamble is also too early / overwritten by beamer at `\begin{document}`. Fix: LuaTeX primitive at the very END of the document (after last frame):
```latex
% LuaTeX ≥1.10: \pdfinfo was REMOVED → use \pdfextension info
\pdfextension info {
  /Title (...)
  /Author ({Author Name})
  /Creator ({Author Name})
  /Producer ({Author Name})
}
\end{document}
```
Pitfalls: `\pdfinfo{...}` is undefined on LuaTeX 1.24 (`! Undefined control sequence` at the line) — must be `\pdfextension info {...}`. Placing `\hypersetup{...}` right after `\begin{document}` does NOT work for lualatex. Verify with `pdfinfo file.pdf | grep -E 'Title|Author|Creator|Producer'`.

**Email addresses on cover pages — anti-spam-scan format (user preference):** never print a raw `user@domain` on the cover/page footer (spam crawlers harvest it). Use `user [at] domain` — literal `[at]` WITH spaces on both sides, as plain text (no `\href{mailto:...}`). User asked for the spaces explicitly. Apply consistently: cover author row, supervisor row, poster footer.

### 20. Cover page counts as page 1; no page number on the ToC page (CUHK-style reports)

User requirement for reports with a titlepage + ToC: the cover IS page 1 in the numbering, and the contents page shows NO page number; body text therefore starts at 3.

With `article` class the `titlepage` environment does NOT advance the page counter (ToC would show 1). Fix explicitly:
```latex
\begin{titlepage}
\thispagestyle{empty}
\setcounter{page}{1}   % cover = page 1
...
\end{titlepage}
\setcounter{page}{2}   % force ToC to be page 2 (titlepage doesn't advance the counter)

\tableofcontents
\thispagestyle{empty}  % no page number on the contents page
\newpage
```
Verify page by page: `for i in 1 2 3; do pdftotext -f $i -l $i main.pdf - | grep -vE '^\s*$' | tail -1; done` — page 1 (cover) and page 2 (ToC) show no footer digit, page 3 shows `3`.

### Verifying rendered figures

```bash
# locate which page each figure landed on (caption search):
for p in $(seq 1 $(pdfinfo main.pdf | awk '/Pages/{print $2}')); do
  pdftotext -f $p -l $p main.pdf - | grep -E "^Fig\." | head -3
done
# render that page and eyeball via vision:
pdftoppm -png -r 80 -f 3 -l 3 main.pdf /tmp/fig_p3
```

## PDF Metadata

```bash
# Check fonts used in the PDF:
pdffonts main.pdf

# Or via PyMuPDF:
import fitz
doc = fitz.open('main.pdf')
page = doc[0]
blocks = page.get_text('dict')['blocks']
fonts_seen = set()
for b in blocks:
    if 'lines' in b:
        for l in b['lines']:
            for s in l['spans']:
                fonts_seen.add((s['font'], s['size']))
for f, sz in sorted(fonts_seen):
    print(f'{sz:.1f}pt {f}')
```
