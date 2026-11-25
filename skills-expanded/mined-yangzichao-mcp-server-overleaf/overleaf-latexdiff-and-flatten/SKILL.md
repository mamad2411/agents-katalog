---
name: overleaf-latexdiff-and-flatten
description: Build a latexdiff PDF that marks what changed in an Overleaf paper between two revisions, or flatten a multi-file paper into a single .tex with latexpand. Use when the user wants a changes-marked PDF for co-authors, reviewers or a response letter, or a one-file version for a journal, and you can run shell commands where the Overleaf MCP server runs.
---

# latexdiff and flattening for an Overleaf paper

Work in a temporary directory, never in the clone: `push_changes` publishes every file in
the clone, so a stray `diff.tex` or PDF there would reach Overleaf.

## 1. Pick the revisions

- `read_project` (view `overview`) gives the clone path, `$CLONE`, and the main document.
- `read_history` (view `commits`) lists revisions with short hashes, dates and authors. Ask
  the user which one is the baseline, for example the submitted version.

## 2. Export both versions

```sh
tmp=$(mktemp -d) && mkdir -p "$tmp/old" "$tmp/new" "$tmp/diff"
git -C "$CLONE" archive <old-hash> | tar -x -C "$tmp/old"    # read-only: reads Git's objects
git -C "$CLONE" archive HEAD | tar -x -C "$tmp/new"           # the version last pulled or pushed
```

To include local edits that are not pushed yet, copy the working tree instead of using
`archive HEAD`: `rsync -a --exclude .git "$CLONE"/ "$tmp/new"/`.

## 3. Flatten

latexpand inlines `\input` and `\include` and strips comments (`--keep-comments` keeps
them):

```sh
(cd "$tmp/old" && latexpand main.tex > "$tmp/diff/old.tex")
(cd "$tmp/new" && latexpand main.tex > "$tmp/diff/new.tex")
```

The flattened `new.tex` alone is the single-file version a journal asks for; give the user
its path. Without a shell, `read_file` with `followIncludes` returns the paper in one call,
each included file inlined between `% ---- begin` and `% ---- end` comments. That reply is
cut off like any long read, so use it to read the paper and latexpand to make the file a
journal gets. If the paper uses BibTeX, `latexpand --expand-bbl main.bbl` also inlines the
bibliography from a compiled `.bbl`.

## 4. Diff and compile

```sh
latexdiff "$tmp/diff/old.tex" "$tmp/diff/new.tex" > "$tmp/diff/diff.tex"
rsync -a --exclude '*.tex' "$tmp/new"/ "$tmp/diff"/           # figures, .bib, .cls, .sty
(cd "$tmp/diff" && latexmk -pdf -interaction=nonstopmode -halt-on-error diff.tex)
```

Give the user `$tmp/diff/diff.pdf`. If latexdiff's markup breaks compilation inside a
table, figure or math, rerun with `--math-markup=0` or `--exclude-textcmd=section`, or
report which environment fails.

Without a shell, `read_history` (view `diff`) still shows the source-level changes between
two revisions as a unified diff.
