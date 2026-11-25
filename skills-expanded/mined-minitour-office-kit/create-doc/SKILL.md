---
name: create-doc
description: Create or revise a branded, self-contained HTML document with OfficeKit. Use for reports, proposals, memos, briefs, articles, letters, whitepapers, one-pagers, or requests to write up source material.
compatibility: Requires an OfficeKit workspace created by setup-office-kit and Python 3.10+ with uv.
metadata:
  author: OfficeKit
  version: "0.2.0"
---

# Create an OfficeKit document

Work in `.office-kit/`. If that workspace is absent, use `setup-office-kit`
first. Write the document in the main agent; research directly with whatever
read/search tools the client provides when claims need verification.

## Output and boundary

The deliverable is one file:
`.office-kit/projects/<slug>/<slug>.html`. It opens directly from disk and
contains its styles, behavior, brand tokens, logo, and embedded images.

Edit only that HTML file and its short `NOTES.md`. Do not create a preview
server, JavaScript project, per-document dependencies, plan, stage reports, or
packaging step. Never edit the generated brand region by hand.

## Pass

From `.office-kit/`:

```bash
uv run python scripts/document/doc.py new <slug> --title "…" \
  [--subtitle "…"] [--footer "…"] [--brand <id>]
```

Replace the `<!-- officekit:content -->` marker in `<main>` with the complete
document in one edit. Use semantic sections:

```html
<section id="overview" aria-labelledby="overview-heading">
  <h2 id="overview-heading">Overview</h2>
  <p>…</p>
</section>
```

The scaffold provides `.lede`, `.callout`, `.code-figure`, and
`.table-scroll`. Put project-only CSS in the `officekit:styles` region and use
the existing `--doc-*` variables. Generic fixes belong in
`.templates/document-html/document.html`.

Finish with:

```bash
uv run python scripts/document/doc.py toc projects/<slug>/<slug>.html
uv run python scripts/document/doc.py check projects/<slug>/<slug>.html
open projects/<slug>/<slug>.html
```

`check` must pass. If supplied images are needed, preserve the originals and
run `doc.py embed` to create data URIs. Write `NOTES.md` in at most 20 lines:
request, audience, decisions, sources, brand ID, and deliberate omissions.

For revisions, inspect the existing HTML and `NOTES.md`, change only what the
user requested, rebuild the contents list when headings changed, and rerun
`check`.
