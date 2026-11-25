---
name: scienceplot-py
description: >
  Generate Python matplotlib plotting scripts in the user's scienceplots lab
  style: with plt.style.context(["science", "nature"]), pparam = dict(...),
  raw-string LaTeX labels, and fig.savefig(..., dpi=300,
  bbox_inches='tight'). Support parquet, CSV, NPY/NPZ data and single-line,
  multi-line, scatter/errorbar, or subplot variants. Generate both the
  reproducible plotting script and the requested PNG/PDF/SVG figure by
  default. Use for publication-style plot scripts, science/nature figures,
  plot-from-data scaffolds, and Korean or English requests for matplotlib
  graph scripts.
---

# scienceplot-py — Matplotlib Plot + Figure Generator (scienceplots / science+nature)

Generate a Python plotting script that **always** follows the user's lab
template shape, execute it, and verify the rendered figure artifact. The skill
returns both the `.py` path and the generated figure path(s). The default
workflow is script plus figure generation; use script-only mode only when the
user explicitly requests a script without execution.

The canonical template lives at
`~/Socialst/Templates/PyPlot_Template/pq_plot.py`. Every variant in this
skill is a structural extension of that file.

## Mandatory style invariants

Every generated script MUST keep these load-bearing patterns intact. Do not
"clean up" any of them, even if they look redundant or unused.

1. **`import scienceplots`** — required. It registers the `science` and
   `nature` styles by import side-effect; the symbol is never referenced
   directly. Linters will flag it as unused — keep it anyway.
2. **Style context block** — all plotting code lives inside
   `with plt.style.context(["science", "nature"]):`. Never substitute
   `plt.style.use(...)` or call any plotting outside this block.
3. **`pparam` dict** — axis configuration is a dict, applied with
   `ax.set(**pparam)`. Do not inline `ax.set_xlabel(...)`, `set_ylabel(...)`,
   `set_title(...)` calls when `pparam` would do.
4. **`ax.autoscale(tight=True)`** — called on every axis, before
   `ax.set(**pparam)`. For subplots, loop over all axes.
5. **Raw-string LaTeX** — every label, title, legend entry uses `r'...'`.
   Non-raw `'$x$'` works for the literal `$x$` but breaks the moment a
   backslash appears (`\alpha`, `\sigma`, `\mathrm{...}`). Always `r`-prefix.
6. **savefig** — `fig.savefig(<path>, dpi=300, bbox_inches='tight')`.
   Default filename is `plot.png`. PDF/SVG output is fine if asked, but keep
   `dpi=300` and `bbox_inches='tight'`. (Bump higher only if the user
   explicitly asks for it — the lab default is 300.)

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
   - `single_line.py` — one series, one ax (mirrors `pq_plot.py`)
   - `multi_line.py` — multiple series, one ax, with legend
   - `scatter_errorbar.py` — `ax.errorbar(...)` (or `ax.scatter(...)`)
   - `subplots.py` — multi-panel `fig, axes = plt.subplots(rows, cols)`
3. Swap in the requested data-loader block. See
   `references/data_loaders.md` for parquet / CSV / `.npy` / `.npz`
   snippets.
4. Substitute column names, label strings, title, output filename. Preserve
   every invariant from the section above.
5. Write the `.py` file with the Write tool. Preserve the requested output
   location in the script rather than relying on an accidental current working
   directory.
6. Render the figure by executing the generated script from the project root.
   Prefer `uv run <path>` when the current project is the active uv project;
   when the project environment is in a subdirectory, use
   `uv run --project <project-dir> python <script-path>`. Do not install
   packages automatically: if `scienceplots`, matplotlib, pandas, or numpy is
   missing, report the dependency error and the command needed after the user
   fixes the environment.
7. Verify that every requested output file exists and is non-empty. For report
   figures, generate the requested raster output (normally PNG) and a PDF or
   SVG companion, each with `dpi=300` and `bbox_inches='tight'`. If the figure
   is available to the harness, inspect it for clipped labels, missing glyphs,
   empty axes, and accidental transparent backgrounds.
8. Return the script path, generated figure path(s), the exact render command,
   and a short render-status summary.

If the user explicitly requests **script-only**, stop after step 5 and return
an execution hint instead of running the script.

## Data sources

| Source        | Imports                | Read call                                          |
|---------------|------------------------|----------------------------------------------------|
| Parquet       | `import pandas as pd`  | `df = pd.read_parquet('data.parquet')`             |
| CSV           | `import pandas as pd`  | `df = pd.read_csv('data.csv')`                     |
| NumPy `.npy`  | `import numpy as np`   | `data = np.load('data.npy')` (then column-slice)   |
| NumPy `.npz`  | `import numpy as np`   | `data = np.load('data.npz'); x = data['x']`         |

Full snippets in `references/data_loaders.md`.

## Templates

Each reference is a self-contained, runnable skeleton matching the
mandatory style invariants. Read the file, adapt strings/columns in memory,
then Write the result to the user's chosen path.

| Variant                | File                                  |
|------------------------|---------------------------------------|
| Single line (base)     | `references/single_line.py`           |
| Multi-line + legend    | `references/multi_line.py`            |
| Scatter / errorbar     | `references/scatter_errorbar.py`      |
| Subplots (multi-panel) | `references/subplots.py`              |
| Data loaders           | `references/data_loaders.md`          |

## What this skill does NOT do

- It does not install `scienceplots` / `matplotlib` / `pandas` / `numpy`.
  Assume they are already available in the target environment; dependency
  installation remains the user's or project's responsibility.
- It does not produce methodology / architecture / pipeline diagrams. For
  those, use `wide-slide-illustrator` or `handdrawn-schematic`.
- It does not change the style invariants. If the user asks for a different
  style (e.g., `seaborn`, `ggplot`, plain matplotlib), tell them this skill
  is specifically for the science+nature template and offer to write the
  alternative as a plain script outside the skill.
- It does not silently treat a successful Python exit as proof of a valid
  figure: output existence and basic visual sanity checks are part of the
  rendering workflow.
