---
name: xkcd-py
description: >
  Generate a Python matplotlib plot script following the user's mandatory xkcd
  style — `with plt.xkcd():` context, `pparam = dict(...)` axis-config, raw-string
  LaTeX labels, wide canvas (`figsize=(10, 6)`), `dpi=300` savefig. Supports
  parquet / CSV / NumPy (`.npy`, `.npz`) and four variants: single line, multi-line
  + legend, scatter / errorbar, multi-panel subplots. Writes the `.py` only — does
  NOT execute it; the user runs it (typically `uv run`).
  Use when asked to write an xkcd-style / hand-drawn / sketch-style matplotlib
  script, plot data in xkcd style from parquet / CSV / `.npy`, scaffold an xkcd
  line / scatter / errorbar / subplot script, or match the lab's xkcd template.
  Triggers on: xkcd plot, xkcd matplotlib, xkcd style, hand-drawn / sketch plot,
  plt.xkcd, comic-style plot; xkcd 플롯, xkcd 그래프, 손그림 그래프, 스케치
  스타일 플롯, xkcd 스크립트, xkcd 코드.
---

# xkcd-py — Matplotlib Script Generator (xkcd / hand-drawn style)

Generate a Python plotting script that **always** follows the user's lab
xkcd template. The skill writes a `.py` file and returns its path; it does
not run the script. The user executes it themselves (preferred:
`uv run <path>` per their global preferences).

The canonical template lives at
`~/Socialst/Templates/PyPlot_Template/xkcd_plot.py`. Every variant in this
skill is a structural extension of that file, normalized to the same
`pparam` + ax-object pattern as `scienceplot-py`.

## Mandatory style invariants

Every generated script MUST keep these load-bearing patterns intact. Do not
"clean up" any of them.

1. **xkcd context block** — all plotting (and `savefig`) lives inside
   `with plt.xkcd():`. Never substitute `plt.rcParams.update(...)` or call
   any plotting outside this block; once the `with` exits, rcParams are
   restored and a later `savefig` will lose the xkcd fonts.
2. **`pparam` dict** — axis configuration is a dict, applied with
   `ax.set(**pparam)`. Do not inline `ax.set_xlabel(...)`, `set_ylabel(...)`,
   `set_title(...)` calls when `pparam` would do.
3. **`ax.autoscale(tight=True)`** — called on every axis, before
   `ax.set(**pparam)`. For subplots, loop over all axes.
4. **Raw-string LaTeX** — every label, title, legend entry uses `r'...'`.
   xkcd uses matplotlib's `mathtext` for `$...$` blocks (not real LaTeX);
   raw strings still matter the moment a backslash appears.
5. **figsize `(10, 6)`** — xkcd-style figures need a wider canvas than the
   matplotlib default for the hand-drawn font and stroke widths to read
   cleanly. Pass `figsize=(10, 6)` to `plt.subplots(...)`. For subplots
   (rows × cols), scale proportionally.
6. **savefig** — `fig.savefig(<path>, dpi=300, bbox_inches='tight')`.
   Default filename is `plot.png`. **DPI is 300 (not 600).** xkcd plots
   are deliberately sketchy; 600 dpi adds no value and bloats the file.

## Font note

xkcd uses Humor Sans / xkcd-Script / Comic Neue. If none are installed,
matplotlib falls back to Bitstream Vera Sans and emits a `findfont:
Font family ['xkcd Script', ...] not found` warning. The plot still
renders — the warning is informational. Do not try to suppress it; do not
install fonts as part of the skill.

## Workflow

1. Gather what the user has not already given:
   - Data source: parquet / CSV / `.npy` / `.npz`, plus the file path
   - x / y column or array names (and y-error if errorbar)
   - Plot variant: single line, multi-line + legend, scatter / errorbar, or
     subplots (rows × cols)
   - Axis labels, title, legend labels (LaTeX OK — strings will be wrapped
     in raw-string form)
   - Output path (default: `plot.png` next to the data file or in cwd)
2. Pick the matching template under `references/`:
   - `single_line.py` — one series, one ax (mirrors `xkcd_plot.py`)
   - `multi_line.py` — multiple series, one ax, with legend
   - `scatter_errorbar.py` — `ax.errorbar(...)` (or `ax.scatter(...)`)
   - `subplots.py` — multi-panel `fig, axes = plt.subplots(rows, cols)`
3. Swap in the requested data-loader block. See
   `references/data_loaders.md` for parquet / CSV / `.npy` / `.npz`
   snippets.
4. Substitute column names, label strings, title, output filename. Preserve
   every invariant from the section above.
5. Write the `.py` file with the Write tool. **Do not execute it.**
6. Print the output path and a one-line "run with `uv run <path>`" hint.
   Do not invoke `uv` / `python` from this skill.

## Data sources

| Source        | Imports                | Read call                                          |
|---------------|------------------------|----------------------------------------------------|
| Parquet       | `import pandas as pd`  | `df = pd.read_parquet('data.parquet')`             |
| CSV           | `import pandas as pd`  | `df = pd.read_csv('data.csv')`                     |
| NumPy `.npy`  | `import numpy as np`   | `data = np.load('data.npy')` (then column-slice)   |
| NumPy `.npz`  | `import numpy as np`   | `data = np.load('data.npz'); x = data['x']`         |

Full snippets in `references/data_loaders.md`.

## Templates

| Variant                | File                                  |
|------------------------|---------------------------------------|
| Single line (base)     | `references/single_line.py`           |
| Multi-line + legend    | `references/multi_line.py`            |
| Scatter / errorbar     | `references/scatter_errorbar.py`      |
| Subplots (multi-panel) | `references/subplots.py`              |
| Data loaders           | `references/data_loaders.md`          |

## What this skill does NOT do

- It does not run the generated script. The user runs it (preferred:
  `uv run <path>`).
- It does not install matplotlib / pandas / numpy or any xkcd font.
- It does not produce publication-quality `science`+`nature` plots — for
  those, use the `scienceplot-py` skill.
- It does not change the style invariants. If the user asks for
  publication-style or different DPI, suggest `scienceplot-py` instead of
  bending xkcd-py's invariants.
