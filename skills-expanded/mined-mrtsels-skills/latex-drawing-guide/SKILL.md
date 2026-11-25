---
name: latex-drawing-guide
description: "Use when drawing figures in LaTeX — TikZ/PGFPlots recipes: neural networks, Bayesian graphs, tensors, time series, camera-ready plots."
metadata:
  openclaw:
    emoji: "🎨"
    category: "writing"
    subcategory: "latex"
    keywords: ["LaTeX typesetting", "LaTeX figure insertion", "LaTeX custom style", "scientific figure creation"]
    source: "https://github.com/xinychen/awesome-latex-drawing"
---

# LaTeX Drawing Guide (TikZ & PGFPlots)

**Trigger:** Use this skill whenever you need publication-quality scientific figures — diagrams, data plots, or model architectures — drawn directly in LaTeX with TikZ and PGFPlots. Drawing natively in LaTeX matches document fonts, produces vector output at any resolution, and keeps figures version-controllable as plain text. This guide blends patterns from awesome-latex-drawing (30+ examples) and the TikZ/PGFPlots manuals into one end-to-end workflow.

## 1. Set Up TikZ and PGFPlots

Load TikZ, the PGFPlots plotting layer, and the libraries you need (see Section 8 for the full library list):

```latex
\usepackage{tikz}
\usetikzlibrary{arrows.meta, positioning, calc, shapes.geometric, fit, backgrounds, matrix, decorations.pathreplacing}

\usepackage{pgfplots}
\pgfplotsset{compat=1.18}          % must be set after loading pgfplots
\usepgfplotslibrary{fillbetween}   % for confidence bands (Section 7)
```

Define shared figure styles once in the preamble with `\tikzset{}` so every figure in the paper uses consistent colors, line widths, and arrow tips.

## 2. Master TikZ Fundamentals

**Coordinates and basic shapes:**

```latex
\begin{tikzpicture}
  \draw[fill=blue!20, rounded corners] (0,0) rectangle (3,2);
  \draw[fill=red!20] (5,1) circle (1cm);
  \draw[fill=gray!20, draw=black] (2,1) ellipse (1 and 0.5);
  \draw[dashed, blue] (0,0) circle (1.5);
  \draw[-{Stealth[length=3mm]}, thick] (3.2,1) -- (3.8,1);   % arrow tip from arrows.meta
  \node at (1.5,1) {Input};
  \node at (5,1) {Output};
\end{tikzpicture}
```

**Nodes and relative positioning** — nodes are the building blocks of scientific diagrams; prefer `positioning` over hardcoded coordinates:

```latex
\begin{tikzpicture}[
  block/.style={rectangle, draw, fill=blue!10, minimum width=2.5cm,
                minimum height=1cm, rounded corners, font=\small},
  arrow/.style={-{Stealth[length=2.5mm]}, thick}
]
  \node[block] (input) {Data Input};
  \node[block, right=2cm of input] (process) {Processing};
  \node[block, right=2cm of process] (output) {Results};
  \draw[arrow] (input) -- (process);
  \draw[arrow] (process) -- (output);
\end{tikzpicture}
```

## 3. Draw Flowcharts and Block Diagrams

Use `block` and `decision` styles with `-Stealth` edges; route bends with `|-` and `-|`:

```latex
\begin{tikzpicture}[
    block/.style={rectangle, draw, fill=blue!10, text width=5em,
                  text centered, rounded corners, minimum height=3em},
    decision/.style={diamond, draw, fill=green!10, text width=4em,
                     text centered, inner sep=0pt, aspect=2},
    line/.style={draw, -Stealth}
]
  \node[block] (data) {Collect Data};
  \node[block, below=1cm of data] (clean) {Clean \& Preprocess};
  \node[decision, below=1cm of clean] (valid) {Valid?};
  \node[block, below=1cm of valid] (analyze) {Analyze};
  \node[block, right=2cm of valid] (fix) {Fix Issues};

  \path[line] (data) -- (clean);
  \path[line] (clean) -- (valid);
  \path[line] (valid) -- node[right] {Yes} (analyze);
  \path[line] (valid) -- node[above] {No} (fix);
  \path[line] (fix) |- (clean);
\end{tikzpicture}
```

## 4. Draw Neural Network Diagrams

**Fully connected network** — iterate layers with `\foreach`, then connect all pairs:

```latex
\begin{tikzpicture}[
  neuron/.style={circle, draw, fill=orange!30, minimum size=8mm},
  conn/.style={->, gray!70}
]
  \foreach \i in {1,...,3}
    \node[neuron] (I\i) at (0, -\i*1.2) {$x_{\i}$};
  \foreach \j in {1,...,4}
    \node[neuron, fill=blue!20] (H\j) at (3, -\j*1.2+0.6) {$h_{\j}$};
  \foreach \k in {1,...,2}
    \node[neuron, fill=green!20] (O\k) at (6, -\k*1.2-0.6) {$y_{\k}$};

  \foreach \i in {1,...,3} \foreach \j in {1,...,4} \draw[conn] (I\i) -- (H\j);
  \foreach \j in {1,...,4} \foreach \k in {1,...,2} \draw[conn] (H\j) -- (O\k);

  \node[above=0.3cm of I1] {\small Input};
  \node[above=0.3cm of H1] {\small Hidden};
  \node[above=0.3cm of O1] {\small Output};
\end{tikzpicture}
```

**Transformer block** — stacked blocks with dashed residual connections via `|-` routing:

```latex
\begin{tikzpicture}[
  block/.style={rectangle, draw, rounded corners, minimum width=3cm,
                minimum height=0.8cm, fill=#1, font=\small},
  block/.default=gray!10,
  arr/.style={-{Stealth}, thick}
]
  \node[block=yellow!20] (attn) at (0,0) {Multi-Head Attention};
  \node[block=blue!10] (norm1) at (0,1.3) {Add \& LayerNorm};
  \node[block=green!20] (ffn) at (0,2.6) {Feed-Forward Network};
  \node[block=blue!10] (norm2) at (0,3.9) {Add \& LayerNorm};

  \draw[arr] (attn) -- (norm1);
  \draw[arr] (norm1) -- (ffn);
  \draw[arr] (ffn) -- (norm2);
  \draw[arr, dashed, gray] (attn.west) -- ++(-0.8,0) |- (norm1.west);
  \draw[arr, dashed, gray] (ffn.west) -- ++(-0.8,0) |- (norm2.west);
\end{tikzpicture}
```

**Architecture patterns** to adapt: encoder-decoder with bottleneck, skip/residual connections, multi-head attention, convolutional layers as stacked feature-map grids, recurrent layers as self-loops or unrolled sequences, attention layers as matrix-operation diagrams.

## 5. Draw Bayesian Networks and Graphical Models

**Construction steps:** (1) define node styles — observed = shaded/thick circles, latent = open circles, hyperparameters = small solid dots; (2) place nodes with relative positioning; (3) draw directed edges with `-{Stealth}` for conditional dependencies; (4) wrap repeated groups in a dashed plate with `fit`; (5) label edges with conditional-probability annotations when needed.

```latex
\begin{tikzpicture}[
  latent/.style={circle, draw, minimum size=1cm, fill=gray!20},
  observed/.style={circle, draw, minimum size=1cm, fill=white, thick},
  plate/.style={rectangle, draw, dashed, rounded corners, inner sep=10pt},
  arr/.style={-{Stealth}, thick}
]
  \node[latent] (theta) at (0,2) {$\theta$};
  \node[latent] (z) at (2,2) {$z_n$};
  \node[observed] (x) at (2,0) {$x_n$};
  \node[latent] (alpha) at (-1.5,2) {$\alpha$};

  \draw[arr] (alpha) -- (theta);
  \draw[arr] (theta) -- (z);
  \draw[arr] (z) -- (x);

  \node[plate, fit=(z)(x), label=below right:$N$] {};
\end{tikzpicture}
```

**Common patterns:** Latent Dirichlet Allocation (LDA) plate diagram, Hidden Markov Model (HMM) chain, variational autoencoder (VAE) graphical model, Gaussian mixture model (GMM) with plates, deep generative model hierarchies.

## 6. Draw Tensor and Matrix Diagrams

**Tensor representations:** matrices as 2D grids with element shading; third-order tensors as 3D cubes with visible faces; tensor networks as connected node diagrams; factor matrices as thin rectangular blocks.

**Decomposition visualizations:** CP decomposition (tensor = sum of rank-one components), Tucker decomposition (core tensor × factor matrices), tensor train (chain of connected 3D cores), matrix factorization (large matrix as product of thin matrices). Build these by placing 3D cubes/filled rectangles as `\node`s with `shading` or `fill=color!N` and connecting them with straight arrows.

## 7. Visualize Data with PGFPlots

**Line plot with error bars** (`error bars/.cd, y dir=both, y explicit` + `+- (0,err)` in coordinates):

```latex
\begin{tikzpicture}
\begin{axis}[width=0.8\textwidth, height=6cm, xlabel={Epoch}, ylabel={Accuracy (\%)},
  legend pos=south east, grid=major, grid style={gray!30}, tick label style={font=\small}]
  \addplot+[mark=o, thick, error bars/.cd, y dir=both, y explicit]
    coordinates {(1,72) +- (0,1.5) (5,85) +- (0,1.2) (10,91) +- (0,0.8) (20,94) +- (0,0.5) (50,96) +- (0,0.3)};
  \addlegendentry{Our Method}
  \addplot+[mark=square, thick, dashed] coordinates {(1,68) (5,79) (10,85) (20,89) (50,91)};
  \addlegendentry{Baseline}
\end{axis}
\end{tikzpicture}
```

**Multiple series from raw data** — pass `table` data instead of `coordinates` and differentiate series by color plus line style (solid vs. dashed) so the plot stays readable in grayscale.

**Bar chart comparing methods** — `ybar` with `symbolic x coords`, `bar width=12pt`, `nodes near coords` for value labels, and a horizontal legend above the plot (`legend style={at={(0.5,1.05)}, anchor=south, legend columns=3}`).

**Time series with confidence bands** — `\usepgfplotslibrary{fillbetween}`:

```latex
\begin{axis}[xlabel={Time}, ylabel={Value}, width=0.8\textwidth, height=5cm]
  \addplot[name path=mean, thick] coordinates {(0,1) (10,2) (20,3) (30,3.5)};
  \addplot[name path=upper, draw=none] coordinates {(0,1.5) (10,2.8) (20,3.8) (30,4.2)};
  \addplot[name path=lower, draw=none] coordinates {(0,0.5) (10,1.2) (20,2.2) (30,2.8)};
  \addplot fill between[of=upper and lower, fill=blue!15];
\end{axis}
```

Mark missing data with dashed segments; stack multivariate series as aligned panels; render spatiotemporal grids as heatmaps using a TikZ `matrix` of color-coded cells (`fill=color!N` per cell) or seasonal decomposition as vertically arranged subplots.

## 8. Use Common TikZ Libraries

| Library | Purpose |
|---------|---------|
| `positioning` | Relative node placement (`right=of`, `below=of`) |
| `arrows.meta` | Modern arrow tip styles (`-{Stealth}`) |
| `shapes.geometric` | Diamond, trapezium, ellipse nodes |
| `calc` | Coordinate arithmetic (`($(a)!0.5!(b)$)`) |
| `fit` | Fit a node (e.g. a plate) around other nodes |
| `decorations.pathreplacing` | Braces, snakes, zigzag decorations |
| `backgrounds` | Draw layers behind other elements |
| `matrix` | Grid-based node layouts |

PGFPlots adds `\usepgfplotslibrary{fillbetween}` (confidence bands) and `groupplots` (aligned multi-panel axes).

## 9. Produce Publication-Quality Figures

**Style guidelines:**
- **Fonts:** TikZ inherits the document font automatically; keep figure labels at 8–10pt and match axis label size to caption text.
- **Colors:** use colorblind-friendly palettes (never red-green only), ensure grayscale readability, and use patterns/line styles as secondary differentiators.
- **Size:** set explicit widths (`width=0.8\textwidth`) matching the target column width; keep sizing consistent across all figures in the paper.
- **Labeling:** label all axes with units, use (a)/(b)/(c) for sub-figures, place legends inside the plot area when possible, and prefer descriptive labels over bare math notation.

**Compile each figure standalone, then include it:**

```latex
% figure.tex -- compile separately, include as PDF
\documentclass[tikz, border=2mm]{standalone}
\usetikzlibrary{arrows.meta, positioning}
\begin{document}
\begin{tikzpicture} % ... your diagram ...
\end{tikzpicture}
\end{document}
% In the main document: \includegraphics{figure.pdf}
```

**Speed up large documents** with `\usetikzlibrary{external}` to cache compiled figures between builds. Keep one node or draw command per line with comments explaining the visual structure — collaborators (and future you) will thank you.

## Pitfalls

- Missing or wrong arrowheads → load `arrows.meta` and use `-{Stealth}` instead of the legacy `->`.
- PGFPlots aborts with a compat-level error → set `\pgfplotsset{compat=1.18}` immediately after `\usepackage{pgfplots}`.
- Figure overflows the text width → set explicit `width` on the axis and test at the target column width before finalizing.
- Nodes overlap after small edits → use relative positioning (`right=2cm of X`) and `calc` instead of hardcoded coordinates.
- Plate doesn't enclose its variables → wrap them with the `fit` library (`\node[plate, fit=(z)(x)]`).
- Figures unreadable in print/grayscale → combine color with line styles or patterns; avoid red-green contrasts.
- Standalone figure has unwanted margins → compile with `\documentclass[tikz, border=2mm]{standalone}`.
- Compilation gets slow in long documents → externalize figures with `\usetikzlibrary{external}`.
- Fonts/labels look off next to the text → keep TikZ inline in the document so it inherits fonts, or set `font=\small` per style explicitly.

## References

- [awesome-latex-drawing](https://github.com/xinychen/awesome-latex-drawing) — 30+ LaTeX drawing examples (2,000+ stars)
- [TikZ and PGF Manual](https://tikz.dev/) — official documentation
- [PGFPlots Manual](https://pgfplots.net/) — data visualization in LaTeX
- [TikZ Examples](https://texample.net/tikz/examples/) — community gallery
- [Overleaf TikZ Tutorial](https://www.overleaf.com/learn/latex/TikZ_package) — beginner walkthrough
