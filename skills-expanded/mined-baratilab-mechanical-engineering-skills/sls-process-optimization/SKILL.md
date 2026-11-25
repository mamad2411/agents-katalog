---
name: sls-process-optimization
description: Optimize polymer selective laser sintering (SLS) process parameters batch by batch — keep a build history, reduce ASTM D638 tensile and D790 flexural test data, compare against the material datasheet, and propose the next batch's fill energy density, hotspot overlap and surface temperature with a bounded Bayesian suggester, the agent explaining each change. Based on the Barati Farimani Lab's agentic SLS work (PA12 GF, PA11, PA12 blends on an SLS4All Inova). Use for SLS parameter development, new powders, or learning from ASTM results.
---

# SLS process optimization (agentic)

Pak, Alvarado & Barati Farimani (arXiv:2608.25928, 2026) let an agent remember every build and its
ASTM results, then propose the next batch on an open-source SLS printer. The agent reached datasheet
values for UTS and flexural strength in 3–4 batches per material. `scripts/sls.py` is that memory,
the test-data reduction, and a bounded suggestion engine. **You** reason, explain, and let the user
approve. Paper data and numbers are in `references/paper-notes.md`.

## Workflow
1. **Set up the history.**
   - `python scripts/sls.py --db builds.sqlite init --seed-paper` loads the paper's 21 batches
     (PA12 GF, PA11 Onyx, PA12 Blend). Omit `--seed-paper` for an empty history.
   - Add the user's powder with its datasheet targets and DSC melt peak:
     `material --name "PA12 White" --tds Et=1950,UTS=47 --tmelt 186`.
2. **First batch of a new powder.** Follow the machine's patch test (the paper prints a 5 × 5 grid of
   energy settings) and start from the lowest energy that sinters visibly. If nothing has been
   recorded, `suggest` returns a conservative starting point.
3. **After each build, reduce the test data.**
   ```bash
   python scripts/sls.py astm --test d638 --type 4 --csv t1.csv t2.csv t3.csv t4.csv t5.csv > tensile.json
   python scripts/sls.py astm --test d790 --csv f1.csv f2.csv f3.csv > flex.json
   python scripts/sls.py --db builds.sqlite result --batch Q --from tensile.json [--Ef .. --sf ..]
   ```
   - Each CSV needs a load (or force) column in N and an extension/deflection column in mm. Pass
     `--strain` if the second column is already strain.
   - The output includes mean ± sd and the best specimen. Record the best (paper convention), but
     **quote the scatter**. If one batch can't be reproduced, mark it `--exclude`.
4. **Propose the next batch.**
   `python scripts/sls.py --db builds.sqlite suggest --material "PA11 Onyx" [--objective UTS|Et|score]`
   - Candidates come ranked by expected improvement, within machine and step bounds, and list which
     levers changed.
   - **Pick one, and change one or two levers.** Explain the physics:
     - more fill energy and overlap → better coalescence, until warping or degradation sets in;
     - higher surface temperature → less curl and better layer bonding, until the powder cakes.
   - Use the notes (warping, brittle corners, early build stop) to override the model when needed.
   - `batch` refuses a surface temperature within 3 °C of the melt peak.
5. **Track progress:** `history --material ... --plot progress.png` shows every batch against the
   datasheet targets.

## Rules
- The datasheet is the target, but machine and atmosphere matter. PA11 Onyx is specified for
  nitrogen, which the paper's machine lacked. Say when a target is unreachable on this setup.
- Every proposal needs a human go-ahead before printing (the paper's GUI step). Never push
  parameters to a printer without approval.

Cite: Pak, Alvarado & Barati Farimani, arXiv:2608.25928 (2026).
