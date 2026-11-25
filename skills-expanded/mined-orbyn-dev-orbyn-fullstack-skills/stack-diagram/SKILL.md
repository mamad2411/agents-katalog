---
name: stack-diagram
description: "Turn a described stack into an architecture diagram as self-contained HTML, PNG or TSX, with grouped nodes and three edge kinds. Use architect for system design and state or lifecycle diagrams, technical-illustration for model-driven figures and motion, product-illustration for faux product UI."
---

# Stack diagram

Use this when someone describes a stack, a service topology or an infrastructure layout and wants a picture of how the parts connect. The result is an engineering-style drawing: icons on tiles, labelled group boxes, orthogonal arrows.

One built HTML file is the source of truth. PNG and TSX derive from it. Keep job files in a git-ignored working folder, for example `output/<job>/`.

This draws what exists and how it connects. A diagram of how one thing changes over time, with states, transitions and guards, is a statechart: use [architect](../architect/references/statecharts.md), which checks it against the real behaviour. A deployment shown here and a lifecycle shown there are often both useful. A diagram inside a film is redrawn in film code under the [code-only rule](../technical-illustration/references/code-only.md), using only logos the user supplied.

## Method

### 1. Settle the content

From the user's list, decide:

- **Nodes.** One per technology: a name and a short lowercase role such as `http server`.
- **Groups.** Draw a box around things that share a runtime, vendor or repository. Nest one level at most. Write labels in the brand's own casing.
- **Edges**, in three kinds:
  - accent solid (`e`): the primary request or data flow, ideally one continuous path
  - neutral solid (`n`): secondary internal connections
  - neutral dashed (`n dash`): dev-time and deploy-time relationships such as CI, hooks and IaC

From a flat list, infer groups and flows. Ask only when a tool is ambiguous enough that the diagram would be wrong either way.

### 2. Get the icons

Fetch logos only when the user asked for them and the network is available. Otherwise take pictograms and say so. Spec forms and commands: [icons](references/icons.md).

Logos are fetched per job, sanitised, stored in the ignored folder and embedded in that job's output. `build.py` and `render_png.py` refuse a folder Git would commit unless the user asked for `--allow-tracked`. Nothing branded goes into a repository or into this skill.

- **Never recolour a logo.** A white logo goes on a dark tile (`tile dark`).
- **Official marks only.** simple-icons is not a source, because its glyphs are monochrome redraws.
- **On a miss or offline,** the node gets a neutral pictogram from `assets/generic`, the run prints `FALLBACK`, and the footer counts it. Tell the user which nodes lack logos.

### 3. Plan the coordinates

Read [geometry](references/geometry.md#edge-anchoring--the-rule-that-prevents-text-collisions) before placing anything. The rule behind the rest: a node is its tile plus the text below it, so vertical arrows run from box bottom to tile top, never through the label. Crossing an edge is fine; crossing a node box is not.

### 4. Build the HTML

Copy `assets/template.html` into the job folder, replace the sample content and keep colours and fonts behind the CSS tokens. Run `scripts/build.py`; it fails on an unresolved token or anything that would load at view time. Steps: [build and render](references/build-and-render.md#build-the-html).

### 5. Render and look

Render with `scripts/render_png.py` ([build and render](references/build-and-render.md#render-and-look)), then open both the light and dark images and read them. A successful exit proves nothing about layout. Check:

- No arrow crosses label text, and no arrowhead lands in text.
- Edge labels are readable and clear of group borders.
- Every icon is visible, including group-label icons in the dark render.
- Group labels sit top-left, clear of nodes and edges, with matching left and right padding.
- Nothing sticks out of its group or clips at the canvas edge.

Fix and render again until clean.

### Worked failure

An API node's tile top is 120 and a database sits below it at 350. The first draft draws the vertical edge from the tile bottom, and the render shows the line running through the name and role. Start it at the box bottom (120+100+6) instead, then list every vertical segment and ask which node boxes it passes between its two ends; the answer must be none. Full coordinates: [build and render](references/build-and-render.md#worked-failure).

### 6. Deliver

- **HTML** is the default: the built file, self-contained and offline.
- **PNG** always comes from `render_png.py`. Never draw a separate image with another library, because the HTML is the single source of truth. Deliver both themes unless the user asked for one.
- **TSX:** convert the built HTML per [TSX output](references/tsx.md).

Build the HTML once and derive the rest. Keep the footer credit. It names the sources this diagram uses (`aws`, `gcp`, `azure` and `k8s` read as the vendor's icons) and states that logos remain the trademarks of their owners. Report any fallbacks.

## Boundaries

- This skill draws a system someone has described. To decide what the system should be, use [architect](../architect/SKILL.md) first.
- Output that embeds logos stays out of the repository unless the user decides otherwise.
- System fonts vary by host, so the HTML can reflow on another machine. The PNG is the fixed record.

## Read when needed

- Build and render steps, the worked failure: [build and render](references/build-and-render.md).
- Coordinates, spacing, edge classes and a worked layout: [geometry](references/geometry.md).
- Spec forms, missed logos, fetch limits and placing marks: [icons](references/icons.md).
- A stack on AWS: [AWS diagrams](references/aws.md); on Google Cloud or Azure: [Google Cloud and Azure](references/gcp-azure.md) (spec forms, network hosts, group rules); on Kubernetes: [Kubernetes diagrams](references/kubernetes.md) (`k8s/` specs, pinned source, normal tile style).
- A React component: [TSX output](references/tsx.md).
