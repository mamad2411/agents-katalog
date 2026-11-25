---
name: dev-guide
description: Writes a textbook-style developer guide for any code repository, then typesets it as a real book. The source is linked Markdown in docs/guide/ (it reads on GitHub or in Obsidian, with Mermaid diagrams, callouts and "check yourself" quizzes). From it the skill builds designed PDF and Word editions with a publisher-grade cover (a public-domain engraving printed in one ink, a colour per volume, classic book type) and a cover thumbnail. Every fact is checked against the code. Use when asked to document a repository for developers, onboard engineers, write a developer guide, handbook or book for a codebase, or produce printable technical documentation; sibling repositories become volumes of one series. Not for API references, READMEs, changelogs or single-page docs.
license: MIT
metadata:
  version: 2.0.0
  author: vvhybe
---

# Developer guide

Produces, for one repository:

- `docs/guide/`: a home page (`README.md`), chapters `NN-slug.md` in four parts, `glossary.md`, `assets/` (SVG charts, the cover plate and its credit) and `.print.json` (the book's settings)
- `docs/<name>-developer-guide.pdf`: an A4 book with a cover, contents, part dividers, edge tabs, chapter openers and a back cover with the colophon
- `docs/<name>-developer-guide.docx`: the same book in Word, fonts embedded, the same cover
- `docs/<name>-developer-guide-cover.png`: the cover as an image, for the README and link previews

The Markdown is the only source; the books are builds. The look is deterministic: the same pages always build the same PDF and Word file.

It was built on three related repositories (a rendering service, its PDF engine plugins and its template kit), which became three volumes of one series. Nothing in the method depends on their language or framework.

## Ground rules

1. **Every fact has a source.** Each claim in the guide traces to a `path:line`, and each number to a command you ran. Re-verify numbers right before they go on a page; code moves. See [references/research.md](references/research.md).
2. **Teach, don't list.** Write for a capable developer who is new to this codebase. Every chapter says what it covers, explains why things are the way they are, and ends with questions that check understanding. See [references/writing.md](references/writing.md).
3. **Document once, in the repo that owns it.** Before writing about a sibling repository's feature, check how this repo already links to it. Cross-reference; don't duplicate.
4. **The Markdown is the book.** Never edit the PDF or Word file by hand. Fix the page and rebuild.
5. **A cover like a real publisher's.** One real public-domain plate tied to the subject, printed in one ink, with type and colour from a series system. No stock illustration and no fake UI. Always credit the plate. Never copy a publisher's trade dress. See [references/cover.md](references/cover.md).
6. **Respect licences.** Fonts are open-licensed and their licence texts ship with the skill. Plates are public domain or CC0 unless the owner accepts an attribution licence. The default PDF engine is WeasyPrint (free software). Never work around a commercial tool's licence restrictions, such as a PDF engine's evaluation stamp. Use WeasyPrint or a genuine licence.
7. **Follow the target repo.** Read its `AGENTS.md`, `CLAUDE.md` and `CONTRIBUTING.md` first, and follow its branch, commit and package-manager rules. Keep secrets and internal infrastructure out of guides that may be shared.

## Workflow

| Step | Do | Read |
| --- | --- | --- |
| 1. Rules | Read the repo's own agent and contribution rules | the repo |
| 2. Research | Build a fact sheet: what it is, how it works, every number with its command, what's unfinished. Use background agents for repos over ~50 files | [references/research.md](references/research.md) |
| 3. Plan | Choose the four parts and the chapters; copy `assets/templates/print.json` to `docs/guide/.print.json` and fill it | [references/writing.md](references/writing.md) § Structure |
| 4. Write | The home page from `assets/templates/home.md`, each chapter from `chapter.md`, the glossary from `glossary.md` | [references/writing.md](references/writing.md) |
| 5. Figures | Mermaid diagrams in the pages; charts only from verified numbers (`scripts/charts.py`); check printed sizes with `scripts/diagram_sizes.py` | [references/writing.md](references/writing.md) § Diagrams |
| 6. Cover | Find a plate with `scripts/find_plate.py`, look at the candidates, download one into `docs/guide/assets/plate/`, set `cover` in the config, preview it | [references/cover.md](references/cover.md) |
| 7. Build | `bash <skill>/scripts/build.sh docs/guide/.print.json` | [references/build.md](references/build.md) |
| 8. Verify | Contact sheets of every page, the cover at thumbnail size, links, a final fact re-check | [references/build.md](references/build.md) § Verify |
| 9. Ship | Link the printable editions and the cover thumbnail from the guide's home page and the repo README; open a PR | [references/build.md](references/build.md) § Ship |

For sibling repositories, write each guide in its own repo and make them volumes of one series: the same `cover.series`, `Volume I`, `II`, `III`, one plate and one colour each (references/cover.md § Series).

## Scripts

`<skill>` is this skill's folder. Python scripts run in the skill's own venv, which `build.sh` creates.

- `scripts/build.sh <config>`: builds the PDF, the cover image and the Word file. Env: `ENGINE=weasyprint|prince`, `PRINCE_LICENSE`, `KEEP_DIAGRAMS=1`, `SKIP_WORD=1`, `DEV_GUIDE_WORK=<dir>`, `DEV_GUIDE_OUT=<dir>` (write outputs somewhere other than the repo, for previews).
- `scripts/find_plate.py "<query>" [--sheet out.png]`: searches open collections for public-domain plates. `--get <ref> --out <dir>` downloads one with a `.json` credit next to it.
- `scripts/make_cover.py <config> <work> <repo> --preview out.pdf`: renders the cover alone, in seconds, while you iterate.
- `scripts/contact_sheet.py <file.pdf> <prefix>`: tiles every page into PNG sheets for a visual review.
- `scripts/diagram_sizes.py <work>`: lists diagrams whose printed text would be too small.
- `scripts/charts.py`: honest, print-friendly SVG bar charts, imported from a small per-repo script.
- The rest are internal to the build: `build_book.py` (Markdown to the book's HTML), `make_art.py` (part tabs), `rasterize.py` and `build_docx.cjs` (the Word edition), `docx_model.py`, `patch_docx.py`, `toc_pages.py` (Word contents page numbers).

## Assets

- `assets/book.css`: the printed book's design. Its placeholders are filled by `build_book.py`.
- `assets/fonts/`: Inter (text), Montserrat (headings), Anton (figures), EB Garamond (cover), each with its OFL licence.
- `assets/mermaid-print.json`: the Mermaid theme the diagrams print with.
- `assets/templates/`: `print.json`, `home.md`, `chapter.md`, `glossary.md`.

## Owner checkpoints

Ask once, with options, and keep working while you wait:

- who the guide is for (new hires, contributors, integrators) and whether it may be shared outside the team
- the series name, if several repos get guides, and each volume's colour (the brand's own colour first)
- the cover plate: show two or three candidates as a contact sheet and recommend one
- the legal line (licence, copyright holder) for the back cover
