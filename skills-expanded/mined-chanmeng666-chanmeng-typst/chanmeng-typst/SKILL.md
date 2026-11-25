---
name: chanmeng-typst
description: >
  Generate professional PDF documents using the Typst typesetting system.
  Use when the user asks to create a PDF, write a document, generate a
  report, typeset a paper, build a presentation, or make a resume / CV /
  cover letter / letter / invoice / thesis / handout / poster — even when
  they do not say "Typst" explicitly. Especially trigger when the user
  mentions one-page CV, two-column resume, academic paper with bibliography,
  an ATS-friendly resume for a job portal, or any CJK (Chinese / Japanese /
  Korean) document, including requests such as 简历, 学术论文, 报告, 发票 or
  幻灯片. Also use when editing an existing .typ file, or when a Typst PDF has
  the wrong page count, spacing, fonts or extracted text.
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
---

# Typst Document Generation Skill

You are an expert Typst typesetter. Generate professional PDF, PNG, SVG, or HTML documents using Typst. This skill is written for Typst 0.14+ and tested on 0.15.1.

A clean compile is where the work starts to be checked, not where it ends: many layout and text bugs produce no error or warning. Step 4 of the Workflow is what catches them.

## Decision Tree — pick a template before writing

Ask, in this order, before writing any `.typ`:

1. **What is the artefact?**
   - Resume / CV → ask where it is going if the user has not said.
     - Uploaded to a job portal or applicant tracking system → `references/ats-resume.md` and `examples/resume-ats.typ`
     - Read directly by a person → `references/typst-templates.md` § 4a Simple or § 4b Typographic Two-Column
   - Cover letter / formal letter → § Letter
   - Academic / research paper → § Academic Paper (two-column, abstract, bibliography)
   - Internal report / whitepaper → § Technical Report
   - Slide deck → § Presentation
   - Bill / receipt → § Invoice
   - Anything else → § General Document

2. **Is the language CJK (Chinese / Japanese / Korean)?**
   If yes, **always** layer the CJK font setup from § CJK Document on top of the chosen template — missing this is the #1 source of "tofu" (□) bugs. Then read `references/typst-pitfalls.md` § CJK text, because system fonts without bold and source line breaks cause problems that no error reports.

3. **Does the user have a JSON / CSV data source?**
   If yes, generate a `.typ` that calls `#let data = json("path.json")` (or `csv(...)`) and loops over it — do **not** hardcode values from the data into the template.

4. **Is it dense, page-limited, or read by a machine?**
   If yes, read `references/typst-pitfalls.md` before tuning layout.

5. **Will it be maintained or reused?**
   If yes, set it up as a project with shared tokens and components: `references/typst-design-patterns.md` § Long-Lived Document Projects.

Use only facts the user gave you in resumes, letters and reports. Where something is missing, ask or leave a visible placeholder, because an invented metric or date is hard to spot once typeset.

## Quick Reference

| Task | Code / Command |
|------|---------------|
| Compile to PDF | `typst compile doc.typ` |
| Compile to PNG | `typst compile doc.typ --format png --ppi 300` |
| Compile & open | `typst compile doc.typ --open` |
| Set page | `#set page(paper: "a4", margin: 2.5cm)` |
| Set font | `#set text(font: "Libertinus Serif", size: 11pt)` |
| CJK font | `#set text(lang: "zh", font: ("Source Han Serif SC", "Noto Serif CJK SC", "SimSun"))` |
| Heading | `= Title` / `== Subtitle` / `=== Sub-subtitle` |
| Math | `$ integral_0^infinity e^(-x^2) dif x = sqrt(pi) / 2 $` |
| Import package | `#import "@preview/cetz:0.5.3": canvas, draw` |
| Load data | `#let data = json("data.json")` or `csv("data.csv")` |
| Evaluate expression | `typst eval "1 + 2"` |
| Conditional format | `#context if target() == "html" { ... } else { ... }` |
| List fonts | `typst fonts` |

## Workflow

### 1. Verify the environment

```bash
typst --version
```

For a deeper check (CJK fonts available, write permissions, version ≥ 0.14), run the bundled script from this skill's directory:

```bash
bash scripts/verify-typst.sh
```

If `typst` is not installed:

- Windows: `winget install --id Typst.Typst`
- macOS: `brew install typst`
- Any platform with Rust: `cargo install --locked typst-cli`

To update an existing install, use `winget upgrade --id Typst.Typst`, `brew upgrade typst`, or `typst update` for a standalone binary.

### 2. Create the `.typ` source file

- Use the Decision Tree above to pick a template from `references/typst-templates.md`
- Consult `references/typst-language-reference.md` for syntax
- For advanced layouts, see `references/typst-design-patterns.md`
- Write the `.typ` file to the user's desired location

### 3. Compile to output

```bash
typst compile document.typ                          # PDF (default)
typst compile document.typ --format png --ppi 300   # High-res PNG
typst compile document.typ output.svg               # SVG
```

See `references/typst-cli-reference.md` for all options.

Check the exit code, because a failed compile leaves any previous PDF in place. Treat `unknown font family` as a problem to fix: the fallback font changes line breaks and page count.

### 4. Verify the output

Do this before telling the user the document is done.

**Look at it.** Render the pages and read each image, since spacing, overflow, orphaned lines and wrong icon colours only show on a render:

```bash
typst compile document.typ "page-{p}.png" --ppi 150
```

**Check it.** Run the bundled checker. It needs poppler, and reports page count, font embedding, text extraction, lost hyphens and bare `~`:

```bash
python scripts/check-pdf.py document.pdf --source document.typ --pages 2
```

Pass `--pages N` when the user gave a page limit, `--ats` for a job-portal resume, and `--require "text" ...` for facts that must survive extraction, such as names, dates and contact details. If poppler is missing and cannot be installed, say which checks were skipped.

### 5. Iterate

Read compilation errors, consult the Recovery Recipes below, fix the `.typ` file, recompile, and repeat Step 4. Re-check the page count after every layout change.

## Gotchas / Common Mistakes

| Mistake | Fix |
|---------|-----|
| CJK glyphs missing or tofu (□) | Set `lang` AND provide a CJK font fallback chain: `#set text(lang: "zh", font: ("Source Han Serif SC", "SimSun"))` |
| Chinese `*bold*` looks like body text | SimSun, SimHei and KaiTi have no bold face. Map `strong` to a font that does |
| Stray space between Chinese characters | A source line break becomes a space. Keep each paragraph on one line |
| First Chinese paragraph is not indented | Use `first-line-indent: (amount: 2em, all: true)` |
| Windows path errors in `#image()` / `#include()` | Use forward slashes: `image("images/photo.jpg")`. Backslashes are an error since 0.15 |
| `~85%` loses its tilde | `~` is a non-breaking space in markup. Write `\~85%` |
| Email address breaks the compile | `@` starts a reference in markup. Write `name\@example.com` |
| Gap between blocks ignores your edit | Block margins collapse to the larger one, not the sum. See `references/typst-pitfalls.md` |
| A title sits closer to the next line after adding `v()` | `v()` replaces the leading between two lines. Give each line its own block |
| SVG icon is black despite `text(fill: ...)` | `image()` does not inherit `currentColor`. Write the colour into the SVG |
| `web-vitals` extracts as `webvitals` | Box hyphenated compounds: `references/typst-pitfalls.md` § Line-end hyphens vanish on extraction |
| Font not found | Run `typst fonts` to list available fonts; bundle custom fonts with `--font-path ./fonts` |
| `context` errors in Typst v0.14+ | Accessing `counter()`, `state()`, or `text.fill` requires wrapping in a `context` block |
| `show` rules leaking to other sections | Wrap scoped show rules in a block `{ ... }` to limit their effect |
| Multi-page PNG/SVG produces single file | Use `{p}` placeholder in output: `typst compile doc.typ "page-{p}.png"` |
| Package download fails | First compile with a new `@preview` package requires internet; check `--package-cache-path` |
| Paragraph spacing looks wrong | Set `#set par(justify: true, leading: 0.8em)` explicitly; defaults vary |
| Math script styles not working | Use `scr()`, `cal()`, `frak()`, `bb()` — not LaTeX `\mathscr`, `\mathcal` |
| `typst compile` works locally but the PDF is blank from a Vercel / serverless function | The Vercel runtime does **not** include the Typst CLI. Either ship a static prebuilt binary in the deploy bundle (`vercel.json` `includeFiles`) or call a separate compile service (Fly.io / Railway). See `references/typst-design-patterns.md` § Serverless. |

## Recovery Recipes

When `typst compile` fails, paste stderr's first line into this lookup before guessing:

| stderr starts with | Most likely cause | First thing to try |
|--------------------|-------------------|--------------------|
| `error: file not found (...) image(...)` | wrong relative path | `cd` to the `.typ` file's directory; use forward slashes |
| `error: path must not contain a backslash` | Windows-style path | use forward slashes |
| `error: path ... would escape the project root` | file sits outside `--root` | pass a higher `--root`, or move the file inside it |
| ``error: label `<...>` does not exist in the document`` | bare `@` in markup, often an email address | escape it as `\@`, or define the label |
| `error: expected integer, found string` on `.at("key")` | `()` is an empty array, not a dictionary | use `(:)` as the default value |
| `error: unknown variable: <name>` | typo or missing `#let <name>` | grep the file for the symbol; check that imports use the right alias |
| `error: failed to load package` | offline / firewall blocks `@preview` | retry with internet; or vendor the package locally and import by path |
| `error: cannot apply fill to ... (context error)` | v0.14 introspection requires `context` | wrap the access in `context { ... }` |
| `error: type mismatch: expected ..., found ...` | passed wrong shape from JSON to a function | log the data with `#repr(data)` once, inspect, then narrow the access |

## When NOT to use

- **Existing LaTeX projects** — use LaTeX directly for `.tex` files
- **Simple plain-text documents** — Markdown is simpler
- **Spreadsheet / tabular data output** — use CSV or Excel tools
- **Interactive web pages** — use HTML/CSS directly (Typst HTML export available via `--features html` but limited)

## Reference Documentation

Read these files on demand (not all at once):

| Reference | Path | Content |
|-----------|------|---------|
| CLI Reference | `references/typst-cli-reference.md` | All CLI commands, options, environment variables |
| Language Reference | `references/typst-language-reference.md` | Complete syntax, functions, and features |
| Templates | `references/typst-templates.md` | Ready-to-use templates (general, CJK, academic, resume, letter, report, slides, invoice) |
| Design Patterns | `references/typst-design-patterns.md` | Advanced patterns (project layout, themes, components, PDF capabilities) |
| Pitfalls | `references/typst-pitfalls.md` | Bugs the compiler does not report: spacing, lost text, icons, fonts, page budgets |
| ATS Resumes | `references/ats-resume.md` | Rules, skeleton and verification for resumes read by machines |

## Output Formats

| Format | Extension | Notes |
|--------|-----------|-------|
| PDF | `.pdf` | Default. Supports PDF/A standards and tagged PDF. |
| PNG | `.png` | One image per page. Use `--ppi` for resolution (default 144). |
| SVG | `.svg` | One file per page. Vector graphics. |
| HTML | `.html` | Experimental. Use `--features html`. |
| Bundle | folder | Experimental. Several files from one source: `--features bundle --format bundle`. |
