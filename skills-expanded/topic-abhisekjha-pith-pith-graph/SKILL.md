---
name: pith-graph
description: >
  Run the Pith wiki graph generator for the current project.
  Scans wiki/ for .md files, extracts [[wikilinks]], and opens an
  interactive force-directed graph in the browser as wiki-graph.html.
---

Run the graph generator against the current project's wiki.

## Steps

1. Run: `python3 <pith_install_dir>/tools/graph_generator.py`
   - Where `<pith_install_dir>` is the directory where pith is installed (the directory containing this skills/ folder).
   - The script resolves `wiki/` and writes `wiki-graph.html` relative to the current working directory (project root).
2. It will open `wiki-graph.html` automatically in the browser.
3. If `wiki/` does not exist or has no `.md` files, tell the user to run `/pith wiki` first to build the wiki.

## When to use

- User runs `/pith-graph`
- User asks to "visualize the wiki" or "show the wiki graph"

## Notes

- Output file: `wiki-graph.html` in the project root (where the user ran the command)
- No dependencies beyond Python 3 stdlib — no install needed
- Ghost nodes (dashed) = pages referenced by wikilinks but not yet written

One-shot. Does not persist.
