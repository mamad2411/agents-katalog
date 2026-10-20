---
applyTo: "notebooks/**/*.ipynb"
---

<!-- type: reference -->

# Notebook Surface

You are editing notebooks that explain and demonstrate the public forecastability workflow.
Notebooks are illustrative narration layers over package behavior, not alternate execution surfaces.

## Notebook role

- Use notebooks to explain what the toolkit does, show canonical inputs and outputs, and walk through interpretation.
- Keep notebooks centered on deterministic forecastability triage before any downstream forecasting hand-off.
- Prefer concise, inspectable steps over long hidden setup blocks or opaque helper code.

## Code-placement rules

- Reusable logic belongs in `src/forecastability/` or another package surface, not embedded in notebook cells.
- Notebook imports should prefer the stable `forecastability` facade and stay within the documented public API in `docs/public_api.md` unless the notebook is explicitly contributor-facing.
- Do not add hidden analysis steps that bypass the public package, reproduce internal logic inline, or depend on private one-off notebook helpers when package code can express the same behavior.
- If a notebook needs new behavior more than once, add it to package code first and have the notebook import it.

## Demonstration rules

- Use notebooks to demonstrate public-package entry points, canonical examples, and interpretable outputs.
- Keep the notebook story faithful to the repository identity: triage first, then optional downstream model-family discussion.
- Do not turn notebooks into a second CLI, a hidden benchmark harness, or the only place where an analysis can be run correctly.
- Make key assumptions visible in markdown so readers can see what the notebook is demonstrating and why.

## Review checklist

- Does the notebook demonstrate public package behavior instead of bypassing it?
- Is reusable logic kept out of cells and located in package code?
- Are the analysis steps visible and narratable rather than hidden in opaque helper cells?
- Does the notebook remain illustrative instead of becoming an alternate execution surface?