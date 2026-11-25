---
name: query2cad-freecad
description: Generates FreeCAD CAD models from natural-language queries with the Query2CAD self-refinement loop — plan steps, write a FreeCAD Python macro, repair execution errors (≤3), capture an isometric view, score image-text agreement (VQAScore ≥ 0.9 to stop), and refine from a caption of what was actually built (≤3), with optional human feedback. Use when the user wants a FreeCAD macro or FreeCAD model from a description, works in FreeCAD, or asks for conversational/iterative CAD from plain language.
---

# Query2CAD: natural language → FreeCAD macro with self-refinement

Paper: A. Badagabettu, S. S. Yarlagadda, A. Barati Farimani, *Query2CAD: Generating CAD models using natural language queries*, arXiv:2406.00144 (code: github.com/akshay140601/Query2CAD). With GPT-4 Turbo, success went from 53.6% on the first try to 73.2% after one refinement and 76.7% after three (easy 95%, medium 70%, hard 42%). Most of the gain comes from the **first** refinement, and most failures (69%) were macros that never executed.

When to prefer the alternatives: CADSmith (`cadsmith-text-to-cad`) gives kernel-checked dimensional accuracy in CadQuery. Use Query2CAD when the user lives in FreeCAD, wants a `.FCMacro`, or the query is conceptual ("a basketball hoop", "a bookshelf") rather than dimension-exact.

Requires FreeCAD with `freecadcmd` on PATH, or `FREECAD_CMD` set. Tested headless with FreeCAD 26.3 from conda-forge: `micromamba create -p ./fc -c conda-forge freecad python=3.11`, then `export FREECAD_CMD=./fc/bin/freecadcmd`. The AppImage and Homebrew builds also work. Rendering uses `pyvista`. VQAScore optionally uses `pip install t2v-metrics`. Q = `scripts/q2c.py`.

## Workflow
1. **Steps first.** Write the construction steps in plain language: components, dimensions (assume sensible mm values and list them), placement relationships. Then write `macro.py` using `references/freecad_macros.md` (headless: no `FreeCADGui`).
2. **Execute (error refinement, at most 3).**
   ```bash
   python $Q run runs/q/macro.py --out runs/q/v0
   ```
   On failure, give yourself the code and traceback, fix only the error, then run `python $Q log --run runs/q --kind error --note "<error>"`. If the budget runs out, report a non-executable macro.
3. **Capture and score.**
   ```bash
   python $Q render runs/q/v0.stl --out runs/q/v0_iso.png
   python $Q score  --image runs/q/v0_iso.png --query "<user query>"
   ```
   VQAScore = P("Yes" | image, "Does this figure show {query}? Please answer yes or no."). If `t2v_metrics` isn't installed, answer that question yourself from the image as a calibrated probability and log it as `--judged-by agent`. Be strict: a pentagon isn't a star.
4. **Stop or refine (model refinement, at most 3).** If score ≥ 0.9, accept. Otherwise:
   - **Caption** the isometric image: describe only what is **actually there** (shapes, counts, arrangement), not what was intended. The paper used BLIP-2 for this. Its captions were often accurate but too thin to guide the fix, so add specifics. Ask the user for a correction when they're present; the paper's human-in-the-loop captions worked best.
   - Diff the caption against the query, revise the macro, run `python $Q log --run runs/q --kind model --note "<caption + diff>" --score <s>`, and go back to step 2.
5. **Deliver** the `.FCMacro` (rename `macro.py`), STEP/STL, the isometric image, the score history from the ledger, and the assumed dimensions.

## Example of the refinement signal (from the paper)
Query: "a plate in the shape of a star". v0 drew an open pentagon outline. Caption feedback, "an open pentagon outline", led to v1, a closed pentagon plate. Caption "a pentagonal plate" plus the diff "needs 5 pointed tips" led to v2, a star-shaped plate. The fix comes from the gap between what was built and what was asked for.
