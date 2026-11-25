---
name: overleaf-pdf-and-figures
description: Look at a compiled Overleaf paper page by page, map a source line to its PDF page and back with SyncTeX, and convert figures to formats LaTeX accepts. Use when the user asks how a page, figure or table looks, where a passage lands in the PDF, why a float moved, or needs a figure converted before adding it to a project opened through the Overleaf MCP server.
---

# Pages, SyncTeX and figures

## 1. Get a PDF

Call `compile_project`. Its reply names the files it saved in this server's build directory,
outside the clone: the PDF and its SyncTeX map (`.synctex.gz`), and with `where: "overleaf"`
also the log, `.bbl` and `.blg`. The local build needs latexmk.

## 2. See a page

```sh
pdfinfo paper.pdf | grep Pages                         # page count
pdftoppm -png -r 110 -f 3 -l 3 paper.pdf /tmp/page     # page 3 as PNG
```

pdftoppm adds the page number to the name (`/tmp/page-3.png` for a short document; it pads
the number for longer ones, so list the folder to get the exact name). Open the PNG to look
at it: overfull lines, a figure on the wrong page, a table running into the margin. Use
`-r 150` or more to read small text, `-r 72` to skim many pages.

## 3. Source line to page and back (SyncTeX)

`compile_project` saves `<name>.synctex.gz` beside the PDF. Prefer the map from a local
build: it records the paths on this computer, while one from `where: "overleaf"` records the
paths on Overleaf's compile server.

```sh
synctex view -i "42:1:/abs/path/sections/method.tex" -o /abs/path/paper.pdf   # line 42 -> Page:, x:, y:
synctex edit -o "3:150:200:/abs/path/paper.pdf"                               # page 3 at (150,200) -> Input:, Line:
```

Use absolute paths. If there is no `.synctex.gz`, compile again with `compile_project`.

Without a shell, `read_file` on a PNG, JPEG, GIF or WebP file in the project returns the
image itself, so you can still look at a figure.

## 4. Convert a figure

pdfLaTeX takes PDF, PNG and JPEG. Keep vector figures vector:

```sh
epstopdf figure.eps                              # EPS -> figure.pdf (ships with TeX Live)
rsvg-convert -f pdf -o figure.pdf figure.svg     # SVG -> PDF, if librsvg is installed
pdftocairo -png -r 300 -singlefile chart.pdf chart # PDF page -> PNG at 300 dpi
```

Add the result with `manage_files` (action `upload`, with `sourcePath`), not by copying it
into the clone: in a text-only checkout a copied binary file is not pushed. Then reference
it with `\includegraphics` through `edit_file`, and check it with `check_references`.
