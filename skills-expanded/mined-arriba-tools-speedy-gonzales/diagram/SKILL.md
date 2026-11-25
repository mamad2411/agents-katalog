---
name: diagram
description: House style and grid-layout primitives for SVG diagrams of layouts and relationships, such as architecture, data flow, module dependencies, or what connects to what, with a matching ASCII rendering. Use before drawing one, when a reply pairs an ASCII diagram with an SVG, or when a repo has a vendored diagrams.py.
---

# Diagrams

Diagrams are self-contained SVGs written by standard-library-only Python scripts with
`diagrams.py`. It draws with `data_graphs.py` from the graph-data skill, so diagrams share its
palette, font, and light and dark mode. The same grid also renders as box-drawing ASCII, so the
two versions always agree.

## Building one

```python
from diagrams import Diagram

d = Diagram()
d.group("plugin", "speedy-gonzales plugin")
d.node("skill", "diagram/SKILL.md", col=0, row=0, group="plugin")
d.node("py", "diagrams.py", col=0, row=1, group="plugin", note="grid layout and routing")
d.edge("skill", "py", "documents")
d.save("diagram.svg")
print(d.ascii())
```

The canonical `diagrams.py` finds `data_graphs.py` in the sibling graph-data skill, and a vendored
copy finds it beside itself. Run scripts with `python3 -B` so no `__pycache__` lands in the skill.

## Placing nodes

- Give every node a cell. Each column takes the width of its widest node, and each gap grows to
  fit the labels and group padding inside it.
- Lay the main flow left to right along one row, and put what hangs off it in the rows below.
- Place connected nodes in the same row or column wherever you can, so their edge draws straight.
  Other edges bend once or twice through the gaps between cells, which reads worse.
- A group's members fill a rectangle of cells that holds no other node and overlaps no other
  group. Groups don't nest.
- Leave a cell or a whole column empty rather than crowd nodes.
- Keep to about 15 nodes. Split anything bigger into two diagrams.

## Edges

- Label edges with a short lowercase verb phrase of three words or fewer ("reads", "copied
  unchanged").
- Use `both=True` for a two-way link. Two opposite edges would draw side by side.
- Use `dashed=True` for optional, async, or runtime-only links.

## Color

- Groups take `SERIES` slots in the order they're declared. Nodes outside any group take the
  neutral last slot. Never pick colors by hand.
- More than nine groups means the diagram needs splitting.
- Only use colors from the `data_graphs` constants, or the dark-mode swap can't reach them.

## Output

- In a chat reply, put the output of `d.ascii()` in the reply as a code block. Write the script
  and its SVG to a scratch directory and open the SVG in a browser.
- Keep the ASCII within 100 columns so a terminal doesn't wrap it. Fewer columns of nodes and
  shorter labels both narrow it.
- In a repo, vendor `diagrams.py` and `data_graphs.py` side by side, unchanged. A change goes into
  the canonical copies first, then gets copied out to every repo that vendors them.

## Checking a diagram

Both renderers print a warning to stderr when two edges line up and read as one, when a label
collides with something, and when the ASCII runs wider than 100 columns. Fix every warning by
moving nodes or shortening labels, then render again.

Then open the SVG in a browser in both light and dark mode and look it over. Fix what you find by
moving nodes, never by editing the SVG.
