---
name: trans2zh-book-skill
description: >-
  End-to-end workflow for translating an English course or book (lecture notes,
  slides, and reading papers) into a structured Chinese Markdown book published
  via GitHub Pages (Jekyll). Use this whenever the user wants to translate a
  course/textbook/lecture series/paper collection into Chinese as a multi-chapter
  Markdown site or book — phrases like "把这门课翻译成中文教程", "translate this course
  to a Chinese book", "做成中文电子书发到 GitHub Pages", "翻译 lecture notes 输出学习手册".
  ALSO use this skill whenever math/LaTeX formulas render incorrectly on a Jekyll
  / GitHub Pages site (kramdown + MathJax) — broken subscripts, formulas showing
  as raw text, equations turning into tables, italic leaking into math — even if
  no translation is involved, because the math-rendering reference here is the
  authoritative fix. Covers PDF ingestion, parallel per-chapter translation,
  terminology consistency, and the GitHub Pages math-rendering minefield.
---

# Translate an English Course/Book into a Chinese Markdown Book (GitHub Pages)

This skill captures a battle-tested pipeline for turning an English course
(lecture notes + slides + reading papers) into a polished, math-heavy Chinese
Markdown book that renders correctly on GitHub Pages.

The hard-won lessons are in two places, and skipping them is how projects fail:
1. **PDF ingestion fails silently on large files** — see "Phase 1" below.
2. **Math renders fine in your editor but breaks on GitHub Pages** — this is the
   single biggest time sink. Read `references/math-rendering.md` BEFORE writing
   any formula-heavy content, and run the bundled scripts before publishing.

## When to reach for the sub-resources

- Writing/translating chapters with formulas → read `references/math-rendering.md`
  first so you author in the kramdown-safe dialect from the start (cheaper than
  fixing 17 files later).
- Setting up the per-chapter structure → read `references/output-format.md`.
- Fixing an existing site whose math is broken → jump straight to
  `references/math-rendering.md` and the `scripts/`.

## The pipeline

Think of this as four phases. Phases 2's chapters are independent, so parallelize
them; everything else is mostly sequential.

### Phase 1 — Ingest source material (素材采集)

Goal: get every lecture's slides + reading papers into clean **text files** that
translation agents can actually read.

- Fetch the course homepage and per-lecture pages with WebFetch to map the
  structure (lectures → subtopics → assigned papers). Build a table:
  `chapter | lecture | 中文标题 | papers | slides`.
- Download paper PDFs (arXiv etc.) with `curl`/`wget`.
- **PITFALL — large PDFs break the Read tool.** The Read tool renders PDF pages
  as images; papers over ~20MB (or image-heavy slides) blow past limits and the
  agent silently gets nothing. **Always extract to text first:**
  ```bash
  pdftotext -layout paper.pdf paper.txt   # then Read/Grep the .txt
  ```
  Use `scripts/extract_pdfs.sh <dir>` to batch-convert a folder of PDFs.
- **PITFALL — Google Drive / auth-walled slides.** Slides hosted on Drive behind
  login are unreachable by agents. Don't burn time fighting auth. Instead,
  synthesize the chapter from the assigned papers + domain knowledge; note in the
  chapter header which lecture it maps to. Chapters with no public paper (intro,
  pure-background lectures) synthesize fine from general knowledge.

### Phase 2 — Parallel per-chapter translation (批量并行翻译)

- One subagent per chapter, each owning exactly one output file
  `docs/chXX_<中文标题>.md`. Independence keeps each agent's context small and
  lets them run concurrently in batches (~6 per batch).
- Give every agent the SAME output template (`references/output-format.md`) and
  the SAME terminology rules, so the book reads as one voice, not 17.
- **Author math in the kramdown-safe dialect from line one** (see
  `references/math-rendering.md`): use `$$...$$` for BOTH inline and display
  math, never single `$`; never a bare `|` inside math; escape literal `$` and
  prose `|`. Retrofitting this across a finished book is painful — doing it
  up front is free.
- **PITFALL — late agents clobber earlier work.** If two agents target the same
  file, or a re-run overwrites a good chapter, you lose work. Assign disjoint
  filenames explicitly and, if you re-run, accept-or-reject per file rather than
  blanket-overwriting.
- **PITFALL — `---` at file top creates YAML frontmatter that breaks Jekyll.**
  GitHub Pages (Jekyll 3.x) parses `---\n...\n---` at the start of any `.md` file
  as YAML frontmatter. If a chapter starts with `---` wrapping an HTML nav block
  or bare text like `chapter-nav`, the build fails with "Invalid YAML front
  matter." **Never** put `---` as the first line of a chapter unless it's valid
  YAML (e.g., `layout: default`). Put the chapter navigation HTML at the
  **bottom** of each file only, or start the file directly with `# 标题`.
  If you do need frontmatter, make it minimal and valid: `---\nlayout: default\n---`.
- **PITFALL — Liquid template conflicts with `{{` and `{%`.** Jekyll processes
  Liquid templates before Markdown, even inside ```code fences``` and `$$math$$`.
  Any `{{` (e.g., Poisson bracket `{{H, W}, W}` in a Python docstring) triggers
  Liquid variable parsing. Fix by: (a) using `\{` instead of `{` in Python strings
  (Python treats `\{` as literal `{`), (b) replacing f-string `{{` with string
  concatenation, or (c) wrapping affected blocks with `{% raw %}...{% endraw %}`.
  After all chapters are written, run a global grep for `{{` and `{%` across
  `docs/` and eliminate every match outside intentional Liquid includes.

### Phase 3 — Consistency & math QA (质量审核)

- Terminology: maintain `docs/glossary.md` (中英对照) as the single source of
  truth; spot-check that chapters use the same Chinese term for the same concept.
- Math: this is where GitHub Pages bites. Run the verification + fix scripts
  (next section). Do NOT trust "it looks fine in VS Code" — kramdown's parsing is
  different from your editor's.

### Phase 4 — Assemble & publish (汇总输出)

- Generate `docs/index.md` (course homepage), `docs/_sidebar.md` (nav),
  `docs/glossary.md`, and `docs/_config.yml`.
- Configure Jekyll correctly — the config is part of the math fix, see below.
- Add MathJax via the theme's `_includes/head-custom.html`.
- **Pre-push checks** (run from `docs/` dir before committing):
  ```bash
  # 1. Math QA
  python scripts/promote_inline_math.py --apply
  python scripts/fix_math_pipes.py --apply
  GEM_HOME=/tmp/ghp-gems ruby scripts/verify_math_kramdown.rb
  # 2. YAML frontmatter: no chapter should start with --- unless valid YAML
  for f in ch*.md; do
    [ "$(head -1 "$f")" = "---" ] && echo "CHECK: $f starts with ---"
  done
  # 3. Liquid conflicts: must have zero {{ and {% outside intentional includes
  grep -rn '{{|{%' . && echo "FIX Liquid conflicts above" || echo "Liquid: clean"
  ```
- Push; GitHub Pages rebuilds automatically. Spot-check a few subscript-heavy and
  conditional-probability formulas in the browser after the build.

## The GitHub Pages math-rendering fix (the big one)

Formula rendering on GitHub Pages fails for non-obvious reasons. The full
explanation, root causes, and verification method are in
`references/math-rendering.md` — read it. The operational summary:

**Config** (`docs/_config.yml`): GitHub Pages only accepts `kramdown` or
`CommonMark`. `markdown: GFM` is invalid and silently falls back to default
kramdown. Use:
```yaml
markdown: kramdown
kramdown:
  input: GFM
  math_engine: mathjax   # NOT nil — nil wraps math in <pre>, which MathJax skips
```
kramdown's `mathjax` engine converts `$$...$$` → `\(...\)` (inline) / `\[...\]`
(display), which MathJax 3 reads natively.

**Formula spec** — kramdown only recognizes `$$` as math. Make every formula
conform, then verify:

| Bad (kramdown mangles it) | Good | Why |
|---|---|---|
| `$x_i$` (single `$`) | `$$x_i$$` | single `$` isn't math → `_` becomes `<em>`, killing subscripts |
| `$$P(a\|b)$$` (bare pipe) | `$$P(a \mid b)$$` or `\vert` | a `\|` in a non-display line makes kramdown emit a spurious table |
| `$$\|x\|$$` (abs/norm) | `$$\lvert x\rvert$$` / `\lVert x\rVert` | named delimiters contain no pipe char |
| prose `A \| B` | `A \\| B` | a literal `\|` in prose also triggers a phantom table |
| currency `$10` | `\$10` | unescaped `$` can start a phantom math span |

**Scripts** (idempotent, code-block-aware — run from the `docs/` dir):
```bash
python scripts/promote_inline_math.py --apply   # single-$  -> $$   (parity-checked)
python scripts/fix_math_pipes.py     --apply    # bare | in math -> \vert
ruby   scripts/verify_math_kramdown.rb          # render with real kramdown, report leaks
```
The verifier renders every chapter with the SAME kramdown engine GitHub Pages
uses and reports: leaked `$` (unrecognized math), `<em>/<strong>` inside math
(emphasis corruption), and spurious headerless tables. Target: zero of each
(except intentionally-escaped currency).

**PITFALL — you usually can't build full Jekyll locally** (no root → no
`ruby.h` → native gems like `eventmachine`/`commonmarker` won't compile). You
don't need to. Install just the pure-Ruby renderer and verify the only thing
that matters — the math conversion:
```bash
GEM_HOME=/tmp/ghp-gems gem install --no-document 'kramdown:2.4.0' kramdown-parser-gfm rexml
GEM_HOME=/tmp/ghp-gems ruby scripts/verify_math_kramdown.rb
```

## Authoring checklist (paste into each chapter agent's brief)

- Every formula in `$$...$$` (inline and display alike). No single `$`.
- No bare `|` inside math: conditional → `\mid`, abs → `\lvert\rvert`,
  norm → `\lVert\rVert`, cardinality → `\lvert S\rvert`.
- Literal `$` → `\$`; literal `|` in prose/titles → `\\|`.
- Structure per `references/output-format.md`; terms per `glossary.md`.
- Code in fenced ```python blocks (math/pipe rules don't apply inside fences).
- **DO NOT wrap the file in `---` YAML delimiters.** Start directly with `# 标题`
  or with the chapter-nav HTML. If Jekyll frontmatter is truly needed, use minimal
  valid YAML: `---\nlayout: default\n---`.
- **Avoid `{{` and `{%` in all content** (code, docstrings, math prose). Use
  `\{` in Python strings, or string concatenation instead of f-string `{{` escapes.
- Only put chapter navigation at the **bottom** of the file (or top without `---`
  wrapper). Never wrap nav HTML in `---\n...\n---`.
