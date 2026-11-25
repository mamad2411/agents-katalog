---
name: agentscad-fdm-dfam
description: Automates design-for-additive-manufacturing on an existing STEP part for FDM printing with the AgentsCAD method — B-Rep → LLM-readable face/adjacency JSON, rule-based 45° overhang detection, tool-grounded reorientation, programmatic teardrops/chamfers/fillets, and kernel + visual verification with a modified STEP and report. Use when the user has a CAD part to 3D print and asks about overhangs, supports, print orientation, teardrop holes, or making a part printable.
---

# AgentsCAD: DFAM for FDM parts

Paper: E. George, C. Keefe, P. Pak, A. Barati Farimani, *AgentsCAD: Automated Design for Manufacturing of FDM Parts via Multi-Agent LLM Reasoning and Geometric Feature Recognition*, arXiv:2607.02448.

This is a blackboard pipeline. Deterministic phases (parse, overhang detection, adjacency, modification, re-check) are code. You are the **Design Reasoner**, and you must ground every rotation in tool output. The paper's ablation found that without the orientation tools the agent hallucinated rotation angles every time, and with them those errors disappeared.

Setup: `pip install cadquery pyvista numpy`. D = `scripts/dfam.py`.

## Workflow
1. **Parse to the blackboard.**
   ```bash
   python $D analyze part.step --out bb.json
   ```
   `bb.json` holds per-face type, area, centroid, normal or axis, tilt angles, radius of gyration, elongation index, the `links` adjacency list, rule-based `feature_hints` (a light stand-in for the paper's GraphSAGE labels), `overhangs`, and a summary. Overhangs are flagged by rule (more than 45° from vertical facing down, not on the bed; horizontal bores by the downward-facing fraction of their sampled normals). If the summary shows 0 actionable overhangs, say so and stop. The paper skips the modifier and verifier in that case.
2. **Recall similar parts** (RAG memory, optional): `python $D memory query --bb bb.json --store dfam_memory.jsonl`.
3. **Reason in the mandatory order** in `references/reasoner_rules.md`: reorient → local modifications → supports → split.
   ```bash
   python $D candidates part.step          # scripted orientation sub-phase, ≤4 candidates, ranked
   python $D lay part.step --face 3        # exact rx/ry to put face 3 on the bed + overhangs after
   python $D orient part.step --rx 90      # check any rotation you consider
   ```
4. **Write `mods.json`** (typed operations by original face ID, reorient last) and apply it:
   ```bash
   python $D modify part.step --plan mods.json --out part_dfam.step
   ```
5. **Verify.**
   ```bash
   python $D verify part.step part_dfam.step --plan mods.json --out verify
   ```
   This checks kernel validity, a single solid, volume Δ%, and re-checks overhangs. `pass_deterministic` must be true. Then answer the generated yes/no `vlm_questions` from `verify_4view.png`, one per modification plus the integrity questions. Use an independent subagent for this when possible; the paper used a separate VLM. Treat "unclear" honestly: low render resolution isn't a defect, but say so.
6. **Report**: a human-readable table of each overhang (face, kind, angle), the action taken and why, the before/after summary, volume Δ, the final orientation (bed face, rx/ry), the render, and any function caveats (for example, a teardropped bore that locates a shaft). Store the outcome with `python $D memory add --bb bb.json --decision mods.json --note "<lesson>"`.

## Worked reference (the paper's birdhouse)
A nine-face birdhouse with two horizontal bores (−90°). Laying end face 3 on the bed makes the entrance bore vertical; the Ø8 perch hole stays horizontal → teardrop. Result: actionable overhangs 2 → 0, a valid single solid, volume −0.17%, faces 9 → 11. See `docs/tutorials/agentscad-fdm-dfam.md` in the repo.

## Limits
Single parts, no assemblies. The GraphSAGE feature classifier isn't bundled (the weights weren't released), so rule hints stand in for it. Very large parts strain the context window: summarize faces by type, keeping only flagged faces and their neighbours.
