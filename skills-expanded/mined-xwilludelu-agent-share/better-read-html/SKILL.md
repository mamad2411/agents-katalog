---
name: better-read-html
description: Create or audit source-first static HTML artifacts from papers, reports, notes, plans, or specifications. Use only for local, offline, single-file, or printable HTML; document-to-HTML conversion; source-preserving relayout; evidence-linked reports or close-reading pages; or auditing existing HTML. Do not use for general reading, summarization, Markdown/math editing, design exploration, or non-HTML reports.
---

# Better Read HTML

Produce local, offline HTML reading pages from the bundled template, with a
source boundary a reader can inspect. This skill is for HTML creation or audit,
not general document analysis.

## Mode first

Choose one mode before rendering.

| Mode | Use when | Boundary |
|---|---|---|
| `preserve` | Exact conversion, source-preserving relayout, or “do not summarize/rewrite/add” requests. | Canonical text and source order are copied from validated source extraction/IR; no rewriting. |
| `annotate-synthesize` | The requested HTML includes explanation, close reading, report structure, reading guide, or synthesis. | Generated material is labeled noncanonical and source-linked for material claims. |
| `audit` | Inspect an existing/generated HTML artifact. | Report fidelity, links, assets, duplicate ids, remote dependencies, accessibility basics, and uncertainty; fix only if asked. |

Source type changes risk, not the basic mode. DOCX, PDF/OCR, Markdown, Obsidian,
text, papers, and math all still use one of the modes above.

## Default workflow

1. Inventory supplied sources, assets, extraction quality, privacy/network
   constraints, high-risk material, and content shape: long prose,
   figures/assets, tables, equations, citations, code, comments, and footnotes.
2. Select mode and fidelity tier before rendering; ask if exact preservation and
   generated analysis conflict.
3. Build or verify a small source IR before rendering:
   - separate document body from site chrome, menus, search widgets, duplicate
     tables of contents, and decorative/navigation assets before anything
     becomes canonical;
   - for converter output (DOCX/PDF/Office/LibreOffice/Pandoc HTML), map the
     converter DOM to source blocks, assets, tables, equations, citations,
     comments, headings, lists, inline links, emphasis, and code spans instead
     of reusing it as reader DOM;
   - give every section and source block a stable id derived from the source.
4. Render: copy the whole `template/` directory to the output location and
   replace the title, brand, `annotation-report` id, and the contents of
   `<main>`, following [`references/template.md`](references/template.md). Read
   that file before writing markup. Output is `index.html` plus `assets/`;
   produce a single file only when asked. Preserve the full selected source
   scope in `preserve`; an intentional excerpt is labeled as an excerpt in the
   title or colophon.
5. Keep canonical source regions separate from noncanonical material:
   evidence notes and added blocks carry `data-canonical="false"`, layout
   copies carry `data-layout-duplicate="true"`. Omit empty apparatus.
6. Validate with `python3 <skill-dir>/scripts/audit_html.py <dir>/index.html
   --strict [--profile preserve|scholarly] [--source-text <extracted.txt>]`
   (all flags: `--help`). Include the command in your report for substantial
   artifacts.

## Load references only when needed

- [`references/template.md`](references/template.md): every render — page
  skeleton, ids, components, evidence notes, IR-to-markup mapping.
- [`references/mode-contracts.md`](references/mode-contracts.md): ambiguous
  preserve vs generated-content boundaries, PDFs/OCR preservation claims,
  fidelity tiers, or implied exactness.
- [`references/scholarly-rigor.md`](references/scholarly-rigor.md):
  academic/formal technical sources with citations, figures, tables, equations,
  derivations, or claim-level annotation.
- [`references/content-contract.md`](references/content-contract.md): structured
  IR, stable source ids, generated-block ids, asset ids, or evidence links.
- [`references/optional-components.md`](references/optional-components.md):
  requested question/evidence ledgers, translations, math renderer policy,
  figure records, or citation status.
- [`references/integrity-validation.md`](references/integrity-validation.md):
  strict conversion gates or HTML audit failures.

## Fidelity invariants

- Canonical source content is never rewritten to sound better.
- Source facts, labels, metadata, citations, identities, quantities, and claims
  are copied from the source or marked unavailable/uncertain; inferred or
  generated claims belong only in noncanonical blocks.
- Evidence excerpts are verbatim, and every evidence note names its source
  location (`data-target` or `data-locator`).
- Strict conversion requires verifiable source-order text. If it cannot be
  verified, mark the artifact unverified or ask; do not claim 100% preservation.
- For PDFs/OCR, preservation can only be claimed against validated extracted
  text/IR unless trusted structure or equivalent audit evidence exists.
  Reading-order uncertainty must be visible.

## Design

The template is the design: its typography, panes, components, print, and
narrow-screen behavior are the house style. Do not restyle it per artifact or
add parallel CSS; add CSS only for a source structure the template lacks.

Shape content within it:

- Material claims that need source support get evidence notes; the evidence
  pane exists only when notes do.
- One `key-point` block per substantive conclusion; qualifications stay in body
  text or an `aside-note`.
- Each figure appears once: at its first relevant mention when the user permits
  relayout, otherwise in source order.
- Wide tables go in `table-responsive`; long code and display math scroll
  inside their blocks.
- Link semantics stay distinct: author affiliations, footnotes, bibliography
  citations, and figure/table/equation references are different links.
- The source's own frontmatter is the page opening; no generated hero repeats
  it.
- Visible UI stays quiet: no assistant commentary, debug notes, process
  explanations, or provenance prose unless the user asks or the artifact would
  otherwise mislead.

## Reporting contract

For substantial artifacts, report the output folder, mode, fidelity tier,
source list, layout notes when they affect reading, validation summary, and
unresolved uncertainty. For trivial artifacts, report only path, mode/fidelity,
and validation warnings.

## Stop rules

Stop and ask, downgrade the fidelity tier, or mark the artifact unverified when:

- Exact conversion is requested but only lossy extraction/OCR is available.
- Source text or assets are unavailable and would require guessing.
- A source block, attachment, table, figure, equation, citation, or evidence
  target is uncertain in strict mode.
- Remote services, remote fonts, or CDN assets are needed for private/local
  sources without approval.
- A requested change would reduce readability, accessibility, or source
  auditability.
