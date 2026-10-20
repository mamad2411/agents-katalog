Inspect the current implementation of the S-Imply project and update `docs/paper_draft.tex` to accurately reflect any changes. Strictly adhere to academic writing conventions throughout.

Reply to the user in terse caveman lingo to save tokens, e.g.
"why lot word when few word do trick". Keep technical facts correct.
Do not apply caveman lingo to the paper text, code, filenames, commands,
academic prose, generated docs, or quoted text.

## Your task

1. **Read the current paper** at `docs/paper_draft.tex` in full.

2. **Inspect the implementation** — read these files and extract exact parameters, formulas, and algorithmic decisions:
   - `src/ml/core/model.py` — architecture dimensions, layer counts, head counts, embedding sizes
   - `src/ml/core/loss.py` — all loss components, weights, gate formulas
   - `src/ml/train.py` — hyperparameters, optimizer, curriculum schedule, annealing
   - `src/atpg/ai_podem.py` — PODEM integration, fallback logic
   - `src/atpg/recursive_reconv_solver.py` — `HierarchicalReconvSolver` algorithm
   - `src/atpg/reconv_podem.py` — `PathConsistencySolver`, `pick_reconv_pair`
   - `src/ml/core/dataset.py` — dataset structure, anchor injection, curriculum phases
   - `src/ml/data/embedding.py` — DeepGate embedding dimensions

3. **Identify discrepancies** between the paper text and the actual implementation. Look for:
   - Wrong numerical values (dimensions, weights, counts, thresholds)
   - Incorrect algorithmic descriptions (wrong aggregation method, wrong formula structure)
   - Missing loss terms or components
   - Curriculum or training schedule described differently from code
   - Gate logic formulas that don't match the implementation

4. **Update only the sections that are wrong or outdated.** Do not rewrite sections that are accurate. Do not add new sections unless critical information is entirely absent.

5. **Write in precise academic style**: use correct mathematical notation, passive voice where appropriate, and no informal language. All equations must match the implementation exactly.

If $ARGUMENTS is provided, focus your updates on that aspect of the paper (e.g., "loss function", "architecture", "curriculum"). Otherwise perform a full audit.
