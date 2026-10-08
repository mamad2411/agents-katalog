---
name: academic-pdf-to-gfm
description: Convert academic PDF papers to GitHub-renderable GFM markdown with math equations. TRIGGERS - PDF, GitHub markdown, math
allowed-tools: Read, Grep, Glob, Bash, Write, Edit
---

# Academic PDF → GitHub GFM Conversion

A battle-tested workflow for converting academic/research PDF papers into GitHub-renderable GFM markdown with inline figures, mathematically correct LaTeX, and validated output.

**Battle-tested on**: López de Prado (2026) "How to Use the Sharpe Ratio" — 51 pages, 82 equations, 8 figures.

> **Self-Evolving Skill**: This skill improves through use. If instructions are wrong, parameters drifted, or a workaround was needed — fix this file immediately, don't defer. Only update for real, reproducible issues.

## Quick Start — Per-Page Routing Workflow

**Do NOT try to apply a single extraction method to the entire PDF.** Modern academic papers mix text, tables, and figures; route each page individually.

### Step 1: Render all pages at 300 DPI

```bash
# Generate PNG for every page at 300 DPI
uv run --python 3.14 --with pymupdf python3 << 'EOF'
import fitz, os
doc = fitz.open('paper.pdf')
os.makedirs("pages", exist_ok=True)
for i in range(len(doc)):
    pix = doc[i].get_pixmap(matrix=fitz.Matrix(300/72, 300/72), alpha=False)
    pix.save(f"pages/page{i:04d}.png")
    print(f"Page {i}: {pix.width}×{pix.height}")
EOF
```

### Step 2: Detect page type for each page

```bash
# Locate the Unlimited-OCR script. If installed via marketplace, it will be in the cc-skills plugin directory.
# If running from the cc-skills repo directly:
S=${S:-~/eon/cc-skills/plugins/unlimited-ocr/scripts/unlimited_ocr.py}

# For each page, run Unlimited-OCR and inspect the <|det|> markers
for img in pages/page*.png; do
    echo "=== $(basename $img) ==="
    uv run --no-project $S parse --input "$img" --collapse-math-spacing --quiet 2>&1 | \
        grep "<|det|>" | cut -d'>' -f2 | cut -d' ' -f1 | sort | uniq -c
done
```

### Step 3: Route each page

Based on the detected `<|det|>` markers:

| Detected                                      | Route to                                     | Command                                                 |
| --------------------------------------------- | -------------------------------------------- | ------------------------------------------------------- |
| `text` only (no `equation`, `image`, `chart`) | pymupdf4llm or pdftotext                     | See Tool Comparison below                               |
| `equation` or `table` present                 | Unlimited-OCR (with `--table-format pipe`)   | `uv run --no-project $S parse --input page.png`         |
| `image` or `chart` present                    | Segment + describe                           | Use `unlimited-ocr-segment-figure` skill + vision model |
| Mixed (`table` + `image`)                     | Unlimited-OCR for table + segment for images | Split the output, route images separately               |

### Step 4: Assemble and validate

```bash
# Concatenate all page outputs
cat pages/page*.md > paper-raw.md

# Extract embedded images (optional)
uv run --python 3.14 --with pymupdf python3 references/extract-images.py paper.pdf

# Validate math before pushing
node references/validate-math.mjs paper-raw.md --fix
```

---

## Tool Comparison (by page type)

**A single academic PDF is routinely born-digital prose on most pages and equation-dense or figure-dense on a few.** Routing the entire document as one type wastes capability and silently loses content.

### The Per-Page Routing Strategy

For every page in the PDF:

1. **Render at 300 DPI** to a PNG (required for Unlimited-OCR accuracy; 150 DPI hallucinates silently)
2. **Detect page type** by running Unlimited-OCR locally (~2.4 s/page on Apple Silicon)
3. **Route based on what the model found**:
   - **Text-only pages** (no math, no charts): extract with `pymupdf4llm` or `pdftotext` (cheaper, preserves structure)
   - **Equation-bearing pages**: use Unlimited-OCR output (returns real LaTeX, e.g. `\left\{ \begin{array} ... \end{array} \right\}`)
   - **Chart-bearing pages**: segment with Unlimited-OCR, hand each panel to a vision model for description (verified 2026-07-31: charts return empty text from Unlimited-OCR)
   - **Fallback**: if a page's text-layer extraction is too thin, re-run through Unlimited-OCR

### Why Per-Page Matters

**The silent failure.** Unlimited-OCR localizes charts with perfect bounding boxes and returns zero characters inside. A user who routes the entire document as "Type C, use Unlimited-OCR" on chart-heavy input loses all chart content AND GETS A WELL-FORMED RESULT, so nothing looks wrong until the output is reviewed.

**Verified (2026-07-31)**: Unlimited-OCR detects charts (via `<|det|>chart` markers) and returns perfect bounding boxes but zero text inside. Pages containing only charts (no text, equations, or tables) would indeed render empty; per-page routing catches this and routes those pages to text-layer extraction or manual inspection instead.

### Page Type Detection (Measured at 300 DPI)

Run Unlimited-OCR on every page and inspect the `<|det|>` markers:

| If the output contains                     | Infer                               | Route to                                                                           |
| ------------------------------------------ | ----------------------------------- | ---------------------------------------------------------------------------------- |
| `text` regions, no `equation` or `chart`   | Text-only page                      | `pymupdf4llm` or `pdftotext` (fallback: Unlimited-OCR)                             |
| `equation` regions                         | Math-bearing page                   | Unlimited-OCR (returns real LaTeX)                                                 |
| `chart` regions                            | Figure-bearing page                 | Segment + describe (use `unlimited-ocr-segment-figure` then a chart-reading model) |
| Empty output (zero characters, no regions) | Page likely unhandled by text layer | Retry with Unlimited-OCR or manual inspection                                      |

### Example: TimeMixer (ICLR 2024, 28 pages)

**Verified 2026-07-31 on `/Users/terryli/eon/quantml/data/papers/a599/b338e44af70d8e9c87be3c5417bde7864b2c92074e1346703f3e2b641e3d.pdf`:**

#### Page 0 — Title page with abstract (route to text extraction)

```bash
# Render at 300 DPI
uv run --python 3.14 --with pymupdf python3 -c "
import fitz
doc = fitz.open('timemixer-iclr-2024.pdf')
pix = doc[0].get_pixmap(matrix=fitz.Matrix(300/72, 300/72), alpha=False)
pix.save('page0.png')
"

# Detect structure
S=~/eon/cc-skills/plugins/unlimited-ocr/scripts/unlimited_ocr.py
uv run --no-project $S parse --input page0.png --collapse-math-spacing --quiet 2>&1 | head -15
```

**Output (actual):**

```
<|det|>header [173, 33, 482, 49]<|/det|>Published as a conference paper at ICLR 2024
<|det|>title [172, 99, 818, 149]<|/det|>TIMEMIXER: DECOMPOSABLE MULTISCALE MIXING FOR TIME SERIES FORECASTING
<|det|>text [181, 170, 777, 200]<|/det|>Shiyu Wang \( ^{1,*} \) , Haixu Wu \( ^{2,*} \) , Xiaoming Shi \( ^{1} \) , Tengge Hu \( ^{2} \) , Huakun Luo \( ^{2} \) , Lintao Ma \( ^{1✉} \) , James Y. Zhang \( ^{1} \) , Jun Zhou \( ^{1✉} \)
<|det|>text [182, 200, 781, 243]<|/det|>\( ^{1} \) Ant Group, Hangzhou, China  \( ^{2} \) Tsinghua University, Beijing, China {weiming.wsy,lintao.mlt,peter.sxm,james.z,jun.zhoujun}@antgroup.com, {wuhx23,htg21,luhk19}@mails.tsinghua.edu.cn
<|det|>title [452, 279, 547, 293]<|/det|>ABSTRACT
<|det|>text [230, 311, 770, 575]<|/det|>Time series forecasting is widely used in extensive applications, such as traffic planning…
```

**Routing decision:** Only `header`, `title`, `text` regions detected. No `equation`, no `chart` → **route to pymupdf4llm or pdftotext** (faster, preserves structure).

#### Page 6 — Benchmark table (route to Unlimited-OCR)

```bash
uv run --no-project $S parse --input page6.png --collapse-math-spacing --quiet 2>&1 | head -20
```

**Output (actual):**

```
<|det|>text [187, 114, 812, 129]<|/det|>Table 1: Summary of benchmarks. Forecastability is one minus the entropy of Fourier domain.
<|det|>table [175, 131, 825, 287]<|/det|>| Tasks | Dataset | Variate | Predict Length | Frequency | Forecastability | Information |
| Long-term forecasting | ETT (4 subsets) | 7 | 96~720 | 15 mins | 0.46 | Temperature |
| Weather | 21 | 96~720 | 10 mins | 0.75 | Weather |
| Solar-Energy | 137 | 96~720 | 10min | 0.33 | Electricity |
…
```

**Routing decision:** `table` detected → **keep Unlimited-OCR output** (already in pipe-markdown format, `--table-format pipe` converts any HTML to markdown).

#### Page 7 — Figure and table mixed (route Unlimited-OCR for table only)

```bash
uv run --no-project $S parse --input page7.png --collapse-math-spacing --quiet 2>&1 | head -30
```

**Output (actual):**

```
<|det|>table [186, 174, 819, 384]<|/det|>| Case | Decompose | Past mixing | Future mixing | M4 | PEMS04 | ETTm1 |
…
```

**Note:** Page 7 contains 6 embedded image objects in the PDF (verified via PyMuPDF), but Unlimited-OCR's 300-DPI screenshot rendering does not detect `image` or `image_caption` regions. Extract images separately via `references/extract-images.py` and route them to a vision model for description.

**Routing decision:** `table` detected → **keep Unlimited-OCR output**; extract embedded images separately and hand to a vision model for description (see `unlimited-ocr-segment-figure` skill).

### Type Classification (Historical, kept for reference)

**Type A — Word-Generated PDF (Type A: most modern academic papers)**

**Signs**: Embedded fonts, copyable text, Unicode math chars when you copy-paste (∑, π, α, β, γ, →)

**Math encoding**: Math is Unicode text in PDF stream — NOT images, NOT glyph maps

**Consequence**: OCR tools like `marker-pdf` **cannot extract LaTeX** — they see text like "γ₄" not `\gamma_4`. They may return empty output or crash silently.

**Type B — LaTeX-Generated PDF**

**Signs**: Computer Modern fonts, precise mathematical spacing, arxiv.org source available

**Math encoding**: Glyph-mapped — structure is partially extractable

**Type C — Scanned/Image PDF**

**Signs**: All pages are raster images, zero copyable text

### Table Format Notice

Tables from Unlimited-OCR come back as HTML `<table>` markup (measured by Baidu at ~88% of real tables). The CLI converts them to pipe-markdown by default (`--table-format pipe`), which is suitable for markdown documents. If you are comparing outputs across readers, pipe-markdown is the canonical form.

---

## Tool Comparison

| Tool              | Page type                    | Install                            | Pros                                                                         | Cons                                                          |
| ----------------- | ---------------------------- | ---------------------------------- | ---------------------------------------------------------------------------- | ------------------------------------------------------------- |
| **pymupdf4llm**   | Text-only, native text layer | `uv run --with pymupdf4llm`        | Best structure preservation, fast                                            | Math comes as Unicode, not LaTeX                              |
| **pdftotext**     | Text-only, plain extraction  | `brew install poppler`             | Very fast, minimal deps                                                      | Loses table structure entirely                                |
| **Unlimited-OCR** | Tables, math, mixed pages    | `uv run --no-project` (no install) | Real LaTeX formulas, tables as pipe-markdown, layout boxes, 300 DPI accurate | Returns empty text for charts; use `segment-figure` for those |
| **markitdown**    | Text-only alternative        | `uv run --with 'markitdown[pdf]'`  | Reasonable structure                                                         | Slight over-spacing; same math limit as pymupdf4llm           |
| **marker-pdf**    | Scanned PDFs (Type C only)   | `pip install marker-pdf`           | Works on scanned images                                                      | **Never use on Type A/B** — fails silently (Unicode text bug) |

**Recommendation**: For per-page routing:

- **Text-only pages** → `pymupdf4llm` (preserves formatting) or `pdftotext` (speed)
- **Tables/math pages** → Unlimited-OCR (returns real LaTeX and pipe-markdown tables)
- **Chart-bearing pages** → Unlimited-OCR (detects charts but returns empty text; route to segment-figure skill + vision model for descriptions)
- **Mixed pages** → Unlimited-OCR (handles tables and layout detection in one pass; segment images separately)

---

## Image Extraction

Save `references/extract-images.py`:

```python
import fitz, os, sys

doc = fitz.open(sys.argv[1])
os.makedirs("references/media", exist_ok=True)
saved = []
for page_num in range(len(doc)):
    for img_idx, img in enumerate(doc[page_num].get_images(full=True)):
        xref = img[0]
        base_image = doc.extract_image(xref)
        img_bytes = base_image["image"]
        if len(img_bytes) < 2048:   # skip icons/logos/watermarks/rules
            continue
        ext = base_image["ext"]
        fname = f"fig-p{page_num+1:02d}-{img_idx+1:02d}.{ext}"
        with open(f"references/media/{fname}", "wb") as f:
            f.write(img_bytes)
        saved.append((page_num+1, fname, base_image.get("width"), base_image.get("height")))
        print(f"Saved: {fname} ({len(img_bytes)//1024}KB, {base_image.get('width')}×{base_image.get('height')})")
doc.close()
print(f"\n{len(saved)} images saved to references/media/")
```

**Naming**: `fig-p{page:02d}-{idx:02d}.{ext}` — page number in name for easy location matching.

**Size filter**: Skip `< 2 KB` (captures icons, watermarks, horizontal rules). Review everything ≥ 2 KB — some are decorative but most are figures.

**Insert in markdown**:

```markdown
![Figure 1: Variance of Sharpe ratio estimates](./media/fig-p12-01.png)
```

Place immediately after the nearest section heading or the paragraph that references the figure.

---

## GitHub GFM Math Rendering Rules

### The `$$` vs ` ```math ``` ` Decision — Root Cause

**GitHub's Markdown pre-processor runs BEFORE the math renderer.** It treats `\\` as an escaped backslash and collapses it to `\`. This breaks LaTeX line breaks in display math.

**The rule is simple**:

| Equation type                                           | Use             | Reason                                     |
| ------------------------------------------------------- | --------------- | ------------------------------------------ |
| Single-line display                                     | `$$...$$`       | No `\\` → pre-processor safe               |
| Multi-line (contains `\\`, `\begin{aligned}`, matrices) | ` ```math ``` ` | Pre-processor does NOT process code fences |
| Inline                                                  | `$...$`         | Standard                                   |

````markdown
# BROKEN on GitHub — \\ stripped by pre-processor:

$$
\begin{aligned}
a &= b + c \\
d &= e + f
\end{aligned}
$$

# CORRECT on GitHub:

```math
\begin{aligned}
a &= b + c \\
d &= e + f
\end{aligned}
```
````

````

### Display Block Formatting Rules

- `$$` must be on its **own line** — not `$$formula$$` on one line
- **Blank line required** before AND after every `$$` block
- **Blank line required between consecutive** `$$` blocks
- These rules do NOT apply to `` ```math ``` `` blocks

### Supported/Unsupported LaTeX

See [references/github-math-support-table.md](./references/github-math-support-table.md) for the full table.

**Key things to avoid**:

| Command | Problem | Fix |
|---------|---------|-----|
| `\begin{align}` | ❌ Not supported by GitHub | Use `\begin{aligned}` |
| `\boxed{}` | ⚠️ Can cause raw LaTeX passthrough | Remove or use bold text |
| `\operatorname{}` | ⚠️ Active GitHub bug, inconsistent | Use `\text{}` or `\mathrm{}` |
| `\newcommand` | ❌ Was briefly available, then pulled | Expand all macros inline |
| `x^_y` | Superscript immediately before subscript | Write `x^{*}_{i}` with braces |

### Common Gotchas

- `\\[8pt]` vertical spacing inside `$$` → eaten by pre-processor → move to `` ```math ``` ``
- `\frac{1}{T}:\left(` → spurious colon after fraction → remove colon
- Pearson vs excess kurtosis: most finance formulas need Pearson (γ₄ = 3 for Gaussian), not excess. **Always document the kurtosis convention in the formula comment.**
- `\begin{pmatrix}` with `\\` → must use `` ```math ``` ``
- `\begin{cases}` with multiple rows → must use `` ```math ``` ``

---

## GitLab: No Workarounds Needed

**Empirically verified 2026-03-15** on GitLab CE 18.9.2. Confirmed by Comrak source code analysis.

GitLab uses the **Comrak** Rust parser with `math_dollars: true`. When Comrak encounters `$$`, it calls `handle_dollars` which slices the raw input buffer directly and stores it as a `NodeMath` AST node — CommonMark's backslash handler is never invoked on math content. The raw LaTeX is passed to KaTeX via `<span data-math-style="display/inline">` unchanged.

**Every GitHub workaround is unnecessary on GitLab:**

| GitHub problem | GitHub fix required | GitLab |
|----------------|---------------------|--------|
| `\\` in `$$` stripped → broken multiline | Use ` ```math ``` ` | `$$` works with `\\` |
| `\left\{` → `\left{` (delimiter error) | Use `\left\lbrace` | `\left\{` works |
| `\{...\}` set notation → invisible braces | Use `\lbrace...\rbrace` | `\{...\}` works |
| `\,` in `$$` → literal comma | Remove `\,` | `\,` works |
| `\,` in inline `$` → literal comma | Remove `\,` | `\,` works |

On GitLab you can write standard LaTeX without any platform-specific workarounds. If you're targeting GitLab (or hosting your own GitLab CE), skip all the `\lbrace`/`\rbrace` substitutions and ` ```math ``` ` conversions — plain `$$` with standard LaTeX is correct.

### GitLab.com Has a Hard 50-Span Per-Page Limit

**GitLab.com (SaaS) enforces a limit of 50 total math spans per page** (display + inline combined). After the 50th span, all subsequent equations silently fall back to raw LaTeX text. This limit exists to prevent DoS attacks and cannot be overridden on GitLab.com.

| Document math density | gitlab.com | Self-hosted CE |
|---|---|---|
| ≤ 50 total spans | ✅ Renders fully | ✅ |
| 51–100 spans | ⚠️ Partial render | ✅ |
| 100+ spans (academic papers) | ❌ Most equations raw text | ✅ Disable with `math_rendering_limits_enabled: false` |

**Validated on**: Sharpe ratio paper (341 spans) — breaks at span 51 on gitlab.com, renders fully on local CE.

**The W6 check in `validate-math.mjs`** warns when a file exceeds the limit.

**Summary: which platform to use**:
- **GitHub.com**: No math span limit. Use `\lbrace`/`\rbrace` workarounds (handled by `--fix`).
- **Self-hosted GitLab CE**: No limit (disable math_rendering_limits_enabled). No workarounds needed.
- **GitLab.com**: Only suitable for documents with ≤ 50 math spans.

### Self-hosting GitLab CE for Math-Heavy Documents

GitLab CE is free and runs on a single machine. On a 61 GB workstation with slim config:
- Memory footprint: ~3 GB (`puma['worker_processes'] = 2`, `sidekiq['concurrency'] = 5`, monitoring disabled)
- Push mirroring to GitHub: free on CE (syncs within 5 min)
- `glab` CLI: first-party, comparable to `gh`

```yaml
# docker-compose.yml — slim GitLab CE
services:
  gitlab:
    image: gitlab/gitlab-ce:latest
    restart: unless-stopped
    environment:
      GITLAB_OMNIBUS_CONFIG: |
        external_url 'http://YOUR_IP:8929'
        puma['worker_processes'] = 2
        sidekiq['concurrency'] = 5
        prometheus_monitoring['enable'] = false
        alertmanager['enable'] = false
        node_exporter['enable'] = false
        redis_exporter['enable'] = false
        postgres_exporter['enable'] = false
        gitlab_exporter['enable'] = false
    ports: ["8929:8929", "8922:22"]
    volumes:
      - /srv/gitlab/config:/etc/gitlab
      - /srv/gitlab/logs:/var/log/gitlab
      - /srv/gitlab/data:/var/opt/gitlab
```

---

## Validation Pipeline

### Step 1: Install KaTeX Validator

```bash
bun add -g katex   # Bun-first per project policy
# or: npm install -g katex
````

### Step 2: Run Before Every Push

```bash
# Validate only (exit 1 on errors)
node references/validate-math.mjs your-file.md

# Validate + auto-fix correctable issues
node references/validate-math.mjs your-file.md --fix
```

The script is at [references/validate-math.mjs](./references/validate-math.mjs). It runs two layers:

**Layer 1 — KaTeX syntax**: parse errors in `$`, `$$`, ` ```math ``` ` blocks
**Layer 2 — GFM structural** (issues KaTeX passes but GitHub breaks):

| Code | Severity | Issue                                                                                         | Auto-fix                               |
| ---- | -------- | --------------------------------------------------------------------------------------------- | -------------------------------------- |
| E0   | Error    | `\!` `\,` `\;` `\{` `\}` in `$$` block — pre-processor strips backslash → parse error cascade | ✅ spacing removed; `\{`→`\lbrace`     |
| E0b  | Warning  | `\{` `\}` `\,` in inline `$...$` — invisible braces or literal commas in prose                | ✅ → `\lbrace`/`\rbrace`; `\,` removed |
| E1   | Error    | `$$` block with `\\` — GitHub pre-processor strips backslashes                                | ✅ → ` ```math ``` `                   |
| E2   | Error    | Consecutive `$$` blocks without blank line — orphaned delimiter cascade                       | ✅ add blank line                      |
| W1   | Warning  | Bare `^*` in `$$` or `$` block — markdown italic pairing eats the `*`                         | ✅ → `^{\ast}`                         |
| W2   | Warning  | `\begin{align}` — not supported on GitHub                                                     | ✗ manual                               |
| W3   | Warning  | `\boxed{}` — can cause raw LaTeX passthrough                                                  | ✗ manual                               |
| W4   | Warning  | `\operatorname{}` — inconsistent GitHub support                                               | ✗ manual                               |

**E0 is the most dangerous**: a single failing `$$` block exposes its `$$` delimiters as literal text, creating an orphaned `$` that shifts ALL subsequent inline `$...$` pairings. One broken equation takes down the entire document.

**`\{`/`\}` trap**: In `$$` blocks, `\left\{` becomes `\left{` (invalid KaTeX delimiter → "Missing or unrecognized delimiter") and `\{...\}` set notation becomes invisible grouping. Fix: use `\lbrace`/`\rbrace` (letter-based, CommonMark-immune). This affects every equation using set notation like `\{\hat{SR}_k\}` or `\min_T\left\{...\right\}`.

Exits code 1 on errors (CI-friendly). Warnings do not block CI but should be reviewed.

### Local Preview Tools

```bash
# GitHub-accurate hot-reload preview
bun add -g @hyrious/gfm
gfm your-file.md --serve

# Offline binary (gh extension)
gh extension install thiagokokada/gh-gfm-preview
gh gfm-preview your-file.md
```

VS Code extensions:

- `shd101wyy.markdown-preview-enhanced` — closest to GitHub rendering
- `bierner.markdown-preview-github-styles` — GitHub CSS styling

---

## Multi-Agent Adversarial Equation Validation

For papers with 10+ equations, use this multi-agent pattern:

### Phase 1 — Parallel Extraction

- **Agent A**: Extract prose with pymupdf4llm, transcribe math from PDF screenshots
- **Agent B**: Extract and categorize all images

### Phase 2 — Parallel Validation

- **Agent C**: Validate equations against reference implementation (if code/repo exists)
- **Agent D**: Numerical spot-checks — compute paper's exhibit values, compare

### Phase 3 — Discrepancy Handling

- For each discrepancy: write `/tmp/paper-discrepancy/eq-{N}.md`
- Spawn resolver agents to search online for authoritative third-party sources
- **Authority rule**: Paper is tentatively more authoritative than code implementation; a third independent source breaks ties

### Phase 4 — Guarded Application

- Apply **only HIGH-confidence fixes** to the markdown
- For MEDIUM-confidence: spawn an independent audit agent before touching the file
- Document all discrepancies even if not fixed — future readers need to know

---

## Anti-Patterns

| Anti-pattern                                         | Why it fails                                                                                                                | Fix                                                                  |
| ---------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------- |
| `\!\left(` or `\,` in `$$` blocks                    | GH pre-processor strips `\!`→`!` before KaTeX — `!\left(` crashes KaTeX, cascades all                                       | Remove `\!` `\,` `\;` (spacing only) — or use ` ```math ``` `        |
| `\left\{` or `\{...\}` in `$$`/`$` blocks            | `\{`→`{` (CommonMark escape), so `\left\{`→`\left{` = "Missing delimiter" error, and `\{x\}` renders without visible braces | Replace with `\left\lbrace`, `\right\rbrace`, `\lbrace`, `\rbrace`   |
| `$$\begin{aligned}...\\...\end{aligned}$$`           | `\\` stripped by GH pre-processor                                                                                           | Use ` ```math ``` `                                                  |
| Trusting `marker-pdf` on Word PDFs                   | Returns no output or zero math (Unicode bug)                                                                                | Read as screenshots, transcribe manually                             |
| `\begin{align}` in display math                      | Not supported by GitHub                                                                                                     | Replace with `\begin{aligned}`                                       |
| `\operatorname{Cov}`                                 | Active GH bug — sometimes renders raw                                                                                       | Use `\text{Cov}` or `\mathrm{Cov}`                                   |
| KaTeX validation only, no ` ```math ``` ` conversion | KaTeX passes but GH pre-processor still breaks `\\`                                                                         | Also convert ALL multi-line blocks                                   |
| `\boxed{}` for highlighting                          | Can cause raw LaTeX passthrough on GitHub                                                                                   | Use bold text or a blockquote callout                                |
| Excess kurtosis in formulas expecting Pearson        | Silent ~50% underestimate in variance formulas                                                                              | Always document convention; use `scipy.stats.kurtosis(fisher=False)` |
| Consecutive `$$` blocks without blank lines          | GitHub collapses them into one broken block                                                                                 | Add blank line between each block                                    |
| Running validation AFTER pushing                     | Bugs visible in public repo                                                                                                 | Validate locally before every push (`--fix` auto-corrects E0/E1/E2)  |

---

## References

| File                                                                      | Purpose                                |
| ------------------------------------------------------------------------- | -------------------------------------- |
| [validate-math.mjs](./references/validate-math.mjs)                       | KaTeX batch validator for GFM files    |
| [pdf-type-detection.md](./references/pdf-type-detection.md)               | Detailed guide to detecting PDF type   |
| [github-math-support-table.md](./references/github-math-support-table.md) | Full supported/unsupported LaTeX table |

---

## Related Skills

| Skill                                                                                                           | Relationship                                                      |
| --------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------- |
| [unlimited-ocr-parse-document](../../../unlimited-ocr/skills/unlimited-ocr-parse-document/SKILL.md)                | Extract text/math from PDFs locally (Type A/C PDFs, ~2.4 s/page)  |
| [unlimited-ocr-segment-figure](../../../unlimited-ocr/skills/unlimited-ocr-segment-figure/SKILL.md)                | Crop multi-panel figures (charts, diagrams) for downstream models |
| [pandoc-pdf-generation](../pandoc-pdf-generation/SKILL.md)                                                      | Opposite direction: markdown → PDF                                |
| [documentation-standards](../documentation-standards/SKILL.md)                                                  | GFM formatting standards                                          |
| [quant-research:opendeviation-eval-metrics](../../../quant-research/skills/opendeviation-eval-metrics/SKILL.md) | Worked example: `references/how-to-use-the-sharpe-ratio-2026.md`  |

## Post-Execution Reflection

After this skill completes, reflect before closing the task:

0. **Locate yourself.** — Find this SKILL.md's canonical path before editing.
1. **What failed?** — Fix the instruction that caused it.
2. **What worked better than expected?** — Promote to recommended practice.
3. **What drifted?** — Fix any script, reference, or dependency that no longer matches reality.
4. **Log it.** — Evolution-log entry with trigger, fix, and evidence.

Do NOT defer. The next invocation inherits whatever you leave behind.
