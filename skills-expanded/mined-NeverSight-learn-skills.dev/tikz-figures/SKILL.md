---
name: tikz-figures
description: Generate detailed, well-spaced TikZ figures (physics, geometry, math) from textbook page images, written descriptions of a setup, or conversation threads where another AI explains the situation. Compiles in /tmp (no clutter in the user's home) and opens the resulting PDF directly in macOS Preview, then iterates on layout and orientation with the user. Use this skill whenever the user asks for a TikZ diagram, wants to recreate or annotate a textbook figure (especially physics, electromagnetism, mechanics, geometry, optics), wants to visualize a situation that's just been explained to them by another AI or teacher, or uses words like "graficá", "diagrama", "ilustrá", "TikZ", "gráfico", "figura", "render this in LaTeX" — even when they don't explicitly say TikZ or LaTeX. Trigger broadly; under-triggering wastes a real strength.
---

# TikZ figures from textbook pages, descriptions, and conversation threads

This skill makes TikZ figures that are **legible** — readable labels, no overlapping text, vectors clearly distinct from field lines, angle arcs that point at the right pair of things — and renders them where the user can see them immediately (macOS Preview).

It's tuned for a specific common situation: the user is studying something, has a textbook image and/or a back-and-forth with another AI explaining the setup, and wants a clean diagram to anchor their understanding. Iteration on orientation and layout is expected; first compiles are rarely final.

## Output discipline

- **Always work under `/tmp`**. Never write `.tex`, `.pdf`, `.aux`, `.log`, or any auxiliary files to the user's home directory or current working directory unless they explicitly say so. The user has stated this preference.
- The deliverable is a PDF opened in Preview, not source code pasted into the chat. Show the source only if the user asks.
- Use a meaningful filename derived from the topic (`espira_torque.tex`, `lanzamiento_proyectil.tex`) — not `figure.tex`.

## Workflow

The four phases below are not optional ceremony — each one prevents a specific failure mode that shows up in real use.

### 1. Understand the situation before drawing

The single biggest source of wrong figures is misreading the source. Before writing TikZ, make sure you can answer:

- What objects are present? (vectors, axes, surfaces, current loops, particles, rays, planes)
- Which way does each vector point, **in the chosen view**?
- What angles appear, and **between which pairs of things**? (e.g. "θ between μ and B" vs "θ between the loop plane and the vertical" — these are different!)
- What sign conventions apply? Which way is +k̂? What direction counts as "positive rotation"?
- For currents in physics figures: which sides have current going into the page, which out? Right-hand rule outcomes flip if you get this wrong.
- For tilts and rotations: which way does the object lean, **viewed from where**? "Tilted to the right" depends on the observer's orientation.

When the source is a **textbook image**, describe back to yourself, in plain words, what's in the figure: the position of each labeled element, where the angle arcs sit, which dot/cross goes on which side. Don't skip this — compressing visual reasoning into TikZ without an intermediate verbal description is where orientation errors are born.

When the source is a **conversation thread with another AI**, the user has usually clarified subtleties in there ("φ is between μ and B", "the loop tilts to the right not the left", "the torque comes out at -k̂"). Read those clarifications carefully before drawing — they're the user's understanding and the diagram needs to reflect it.

When the source is just a **textual description**, ask one clarifying question if anything is genuinely ambiguous (the orientation of an axis, the side of a tilt, the direction of a current). One clarifying question is much cheaper than three iterations of "no, the other way".

### 2. Plan the layout for spacing

The default TikZ instinct is to cram everything into a 5×5 cm canvas. That produces overlapping labels and unreadable angle arcs. Counter that explicitly:

- **Generous canvas**: set `x=1.4cm, y=1.4cm` (or larger) on the `tikzpicture` so coordinates spread out. The user does not mind a large image; they mind illegibility.
- **Border**: `\documentclass[tikz,border=12pt]{standalone}` for breathing room around the bounding box.
- **Legends and explanatory boxes go OUTSIDE the central diagram region**, typically below-left or below-right. Use a styled node and place it at coordinates well clear of any drawn element. See `references/layout-patterns.md` for the exact pattern.
- **Field arrows / background patterns belong in side bands**, not running through the main diagram. For a vertical field, draw arrows in two columns far left and far right.
- **Auxiliary indicators** (torque rotation glyphs, ⊗/⊙ symbols, "this means giro horario" notes) get their own corner. Don't pile them next to the central vectors.
- **Vector labels offset by `(±0.4, ±0.4)`** from the arrow tip — never write the label directly on the line.
- **Font sizing**: `font=\large` for primary vector and axis labels, `font=\small` for legend body text. If a label is hard to read at the first compile, **scale up the canvas before shrinking the font** — illegible text in a tight canvas is worse than a bigger PDF.

`references/layout-patterns.md` has concrete coordinates that have worked in practice. Read it before laying out a multi-element figure.

### 3. Write TikZ that compiles on the first try

Most "fatal error, no PDF produced" surprises come from a small known set of issues. `references/pitfalls.md` documents them. Read it before writing constructs you haven't used in this session.

The non-obvious ones, summarized here:

- **`\pic{angle=A--O--B}` requires named coordinates.** Inline coordinates like `(0,2.2)` will fail with `Unknown key '/tikz/pics/2.2)'`. Always declare `\coordinate (X) at (...);` first, then reference by name.
- **`pic angle` sweeps counterclockwise** from the ray to the first point to the ray to the third point. If you get a 330° arc instead of 30°, swap the first and third arguments.
- **Don't use `above left=2pt of foo`** unless `\usetikzlibrary{positioning}` is loaded. Default to offset calc syntax: `at ($(foo)+(-0.4,0.4)$)`. (`calc` library is in the standard preamble below.)
- **Don't use `\text{...}`** outside math without `amsmath`. Just write the word: `$\vec{\mu}\perp$ plano $\Rightarrow \phi=90^{\circ}-\theta$`.
- **Standard preamble for physics figures:**
  ```latex
  \documentclass[tikz,border=12pt]{standalone}
  \usepackage{amsmath}
  \usetikzlibrary{arrows.meta,decorations.markings,angles,quotes,calc}
  ```
  This combination handles vectors with nice arrowheads, mid-line current arrows on loops, named angle arcs, quoted angle labels, calc-style coordinate offsets, and gives access to `\dfrac`, `\text{...}`, `\boxed{...}`, and the `align*` environment for legend formulas. `amsmath` is cheap to include and prevents a class of "Undefined control sequence" errors that otherwise come up the moment a legend has a pretty fraction.

- **Don't pick a custom style name that collides with a TikZ key.** `tension`, `opacity`, `dashed`, `loop`, `solid`, `bend left`, `every node` are reserved. Defining `tension/.style={...}` and then `\draw[tension]` produces `! Package pgfkeys Error: The key '/tikz/tension' requires a value`. Prefer Spanish-language semantic names when working in Spanish (`peso`, `cuerda`, `campo`, `rayo`, `vel`, `fuerza`) — they're unambiguous and self-documenting.

A starter `assets/template.tex` ships with this skill. Read it once at the start of a new figure — it's calibrated to the conventions above.

### 4. Compile in /tmp and open in Preview

```bash
cd /tmp && pdflatex -interaction=nonstopmode -halt-on-error <name>.tex >/tmp/<name>_build.log 2>&1 \
  && open -a Preview /tmp/<name>.pdf && echo OK \
  || tail -30 /tmp/<name>_build.log
```

Notes:

- The `|| tail -30` falls back to showing the last 30 lines of the log on failure, which is enough to find the offending line in almost every case.
- On the **first** compile, Preview opens the PDF in a new window. On **subsequent** compiles to the same path, Preview auto-reloads the existing window — you don't need to re-`open` it. Don't close and reopen Preview between iterations.
- If a compile fails, **read the actual error message** before changing things. Most errors point at a specific line; fix that line and recompile. Don't blindly delete code or rewrite from scratch.

## Verify, then iterate

After the first compile, **briefly state what you drew, in plain words**, and invite the user to verify orientation and conventions:

> "Espira inclinada hacia la derecha (lado ④ arriba-derecha, corriente entrando), $\vec{\mu}$ apuntando arriba-izquierda, $\phi$ entre $\vec{\mu}$ y $\vec{B}$. ¿Coincide con la figura del libro?"

This costs one short paragraph and saves at least one full compile cycle. The user is studying a specific source — they'll spot orientation errors instantly when prompted, and silently miss them when not.

When the user reports a correction, **also re-check dependent elements**:

- Flipping a tilt direction → check angle pic argument order (first/third may need to swap), label rotation transforms, side-of-segment label placement.
- Flipping a current → re-derive $\vec{\mu}$ direction by right-hand rule, then re-check torque sign.
- Moving the legend → make sure no vector or arrow now passes through it.

A correction that fixes the named issue but leaves a downstream element wrong is a frustrating second iteration; preempt them by walking through what depends on what.

## Choosing what goes where

For a typical physics figure with central vectors, an ambient field, and an explanatory legend, this layout is reliable:

- **Center**: main diagram (axes, primary objects, primary vectors, angle arcs).
- **Far left and far right side bands**: ambient field arrows (uniform $\vec{B}$, $\vec{E}$, gravity field, etc.).
- **Below-left**: explanatory legend node — definitions of every angle and vector, sign conventions, and the headline formula. Yellow tinted background (`fill=yellow!10`) makes it clearly meta-information.
- **Below-right**: auxiliary indicators — torque rotation glyph with $\otimes$/$\odot$ symbol, into-page/out-of-page reminders, the resulting sign of the cross product.
- **Above each vector tip**: the vector's symbol, offset diagonally so the arrow is unobstructed.

For non-physics figures (pure geometry, function plots, graph-theoretic diagrams), the side-band trick is unnecessary — but the canvas-spacing and legend-placement instincts still apply.

## When NOT to use this skill

- The user wants a quick ASCII sketch in chat — just draw it inline.
- The user explicitly wants matplotlib, plotly, or another tool — respect that.
- The user wants an interactive page — use the `interactive-educational-site` skill instead.

## Reference files

- `references/pitfalls.md` — every TikZ compile error pattern observed in practice and the exact fix.
- `references/layout-patterns.md` — concrete coordinates and node styles for legends, side bands, indicators.
- `assets/template.tex` — known-good starter with the standard preamble, common styles, and named-coordinate stubs.
