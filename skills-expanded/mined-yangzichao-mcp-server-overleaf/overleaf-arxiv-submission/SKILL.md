---
name: overleaf-arxiv-submission
description: Prepare an Overleaf paper for arXiv by checking references and citations, compiling, stripping comments and unused files, and building the upload folder or ZIP. Use when the user wants to submit or update a paper on arXiv from a project opened through the Overleaf MCP server.
---

# Preparing an arXiv submission from Overleaf

arXiv publishes the source files, comments included, so the upload should hold only what
the paper needs.

## 1. Check the paper first

1. `check_references` on the main document. Fix undefined references and missing files
   before going further.
2. `look_up_citations` (action `verify`) to catch entries that name the wrong work or none.
3. `compile_project` and read the errors and warnings. Use `where: "overleaf"` to compile
   exactly what co-authors see, or the local build when edits are not pushed yet.

## 2. Build the upload (with a shell)

Copy the project out of the clone; never clean files inside it, since `push_changes` would
publish the deletions.

```sh
tmp=$(mktemp -d) && rsync -a --exclude .git "$CLONE"/ "$tmp/paper"/
```

`$CLONE` comes from `read_project` (view `overview`). If that overview says the checkout
is text-only, figures are not on disk; use `manage_project` (action `download_zip`) and
unzip it into `$tmp/paper` instead.

Then either:

- `arxiv_latex_cleaner "$tmp/paper" --keep_bib` (Google's tool, `pip install
  arxiv-latex-cleaner`), which removes comments and unused files into a cleaned copy beside
  the input folder. It deletes `.bib` files unless `--keep_bib` is given, and
  `--resize_images --im_size 1600` shrinks large figures; or
- in `$tmp/paper`, `latexpand main.tex > ../flat.tex && mv ../flat.tex main.tex` (latexpand
  strips comments as it inlines), then delete the inlined section files and anything else
  the paper does not use, keeping figures, `.bib`/`.bbl` and any `.cls`/`.sty`/`.bst`.

## 3. Bibliography rules arXiv applies

- Since November 2025 arXiv runs BibTeX or Biber itself, so uploading the `.bib` files is
  enough. It uses a `.bbl` when one is present.
- A `.bbl` must have the same base name as the main `.tex` file (`main.tex` with
  `main.bbl`). Upload one only when you use a processor arXiv does not run, such as
  `bibtex8` or `upbibtex`.
- With biblatex, a `.bbl` must match arXiv's Biber version: for TeX Live 2025, bbl format
  3.3 only. A `.bbl` from an older TeX Live fails.
- arXiv removes auxiliary files (`.aux`, `.log`, the PDF) itself; do not include backup
  files, unused figures, or hidden files.

## 4. Test and hand over

Compile the cleaned folder once (`latexmk -pdf -interaction=nonstopmode main.tex` there),
then zip that folder from inside it (`zip -r ../arxiv.zip .`) and give the user the
path. The user uploads it; do not submit on their behalf.
