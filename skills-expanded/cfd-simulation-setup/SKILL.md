---
name: cfd-simulation-setup
description: Sets up, runs, diagnoses, and reports OpenFOAM CFD simulations from a plain-language request, using the CFD Forge method — registered flow families with acceptance contracts, a closed action vocabulary, and deterministic validators that alone decide ACCEPT / CORRECT_AND_RERUN / REJECT / INCONCLUSIVE. Use when the user asks to set up, run, check, or trust a CFD simulation (OpenFOAM, nozzle, shock, step, bluff body, pipe/duct, airfoil), asks whether a CFD result is converged, mesh-independent or acceptable, or wants a CFD case built from a description.
---

# CFD Simulation Setup (CFD Forge method)

Based on *CFD Forge: A Physics-Constrained Agentic Framework for Autonomous CFD* (Oza, Johnson, Barati Farimani, arXiv:2610.14104; code at github.com/aakashoza31/physics-constrained-cfd-agent).

**The central rule: you propose, the code decides.** You interpret the request, build the case, read the evidence, diagnose, and propose one action from a closed list. `scripts/validate.py` alone returns the verdict. In the paper, a model judging from the evidence alone accepted 12 of 13 detectable planted faults, and with the deterministic gates in place it accepted none. Never write ACCEPT yourself, never relax a threshold to make a run pass, and never present a number in the report that didn't come from an evidence file.

Requires OpenFOAM Foundation v14 (v11 or later works for `foamRun`), plus `numpy`. Everything except the solve itself runs without OpenFOAM.

## Workflow

### 0. Pick or register a flow family
```bash
python scripts/contracts.py                      # list registered families
python scripts/contracts.py forward-step-2d      # show a contract
```
Registered families: `cd-nozzle` (steady, quasi-1-D reference), `forward-step-2d` (transient shock, storage-aware mass closure), `cube-stationarity` (development gate for force histories), and `generic-steady-incompressible` (a template).

If the request fits no family, **register one before running anything**. Follow `references/new_family.md` and agree the thresholds with the user. A threshold chosen after seeing the result isn't an acceptance criterion. If the user won't fix tolerances up front, the best possible outcome is INCONCLUSIVE, and you should say so.

### 1. Interpret → stated values only
Write `stated.json` with **only** the values the request states, plus `request_criteria` (what the user wants to know: e.g. `transient_health`, `grid_sensitivity`, `q1d_consistency`) and `requests_unsupported_physics: true` if the request asks for physics the family excludes (viscosity in an Euler family, combustion, and so on). Leave everything else out. Don't guess.
```bash
python scripts/build_case.py spec --family forward-step-2d --stated stated.json --out spec.json
```
`spec.json` labels every field `stated_by_user` or `inferred_from_family_defaults`. Show the user this table.

### 2. Scope gate
```bash
python scripts/validate.py scope --family forward-step-2d --spec spec.json
```
If it's out of scope, stop and report which parameter is outside the envelope. Offer the nearest admissible case or a new family. Don't stretch the family.

### 3. Build the case (values change, formulations don't)
```bash
python scripts/build_case.py forward-step --spec spec.json --case cases/m2   # copies $FOAM_TUTORIALS recipe, hashes it
python scripts/build_case.py nozzle       --spec spec.json --case cases/noz
```
If `patches_missing_in_template_fields` in the builder output is non-empty, the template's `0/` files don't match the mesh patches. Fix that before solving. Boundary-condition types, numerics, and the physical model come from the family recipe. Don't hand-edit fvSchemes, fvSolution, or BC types. For a new family, write its builder first (see `references/new_family.md`).

### 4. Mesh gate, then solve
```bash
cd cases/m2 && ./Allrun.agent          # blockMesh, checkMesh, foamRun with logs
```
Before solving, run `python scripts/evidence.py mesh log.checkMesh`. If `mesh_ok` is false, or a 2-D family has fewer than 2 solution directions, stop.

### 5. Extract evidence (deterministic; never typed by hand)
```bash
E=scripts/evidence.py
python $E log  cases/m2/log.foamRun > ev_log.json
python $E mesh cases/m2/log.checkMesh > ev_mesh.json
python $E minmax  cases/m2/postProcessing/fieldMinMax/0/fieldMinMax.dat > ev_mm.json
python $E closure mass_records.csv > ev_mass.json          # transient families
python $E front   line_y0p1.csv --step-x 0.6 > ev_front.json
python $E drift   monitor.dat --col 1 --window 2e-3 > ev_drift.json   # steady families
python $E growth  forces.dat --col 3 --window 20 > ev_growth.json     # bluff-body development
python $E merge --family forward-step-2d --criteria transient_health \
   --state t=4,end_time=4,iteration=1,refinements=0,max_co=0.2 --out evidence.json ev_*.json
```
`references/function_objects.md` has the controlDict function objects that write these records, including the per-step mass and boundary-flux records. Reference or theory comparisons are computed with `scripts/theory.py` and added to evidence **after** diagnosis.

### 6. Diagnose from the blind packet, and propose ONE action
```bash
python scripts/validate.py blind --evidence evidence.json --out packet.json
```
Read only `packet.json`. Theory and reference values are stripped out, so you diagnose from the simulation's own evidence. Write `proposal.json`:
```json
{"diagnosis": "INSUFFICIENT_RUN_TIME", "action": "CONTINUE_RUN",
 "evidence_cited": ["monitor_drift 2.0% > 0.2%", "mass mismatch decreasing"],
 "competing_hypotheses": [{"h": "local_underresolution", "for": "...", "against": "checkMesh clean"}],
 "confidence": "high"}
```
Diagnosis rules (from the paper's system instruction):
- Solver completion is **not** evidence of stationarity. A settled mean is **not** evidence of a developed flow; check growth of fluctuating components too.
- Keep these apart: insufficient run time vs. local under-resolution vs. numerical failure vs. boundary anomaly.
- If the evidence can't separate competing hypotheses, propose `REQUEST_DIAGNOSTIC`.
- Don't invent measurements. Cite packet keys.
- Choose the action from `permitted_actions` only.

### 7. Gates decide
```bash
python scripts/validate.py action  --evidence evidence.json --proposal proposal.json
python scripts/validate.py verdict --evidence evidence.json
```
- Action **REFUSED** → don't execute it. You may propose once more, citing the refusal reason. A refused ACCEPT ends as `STOPPED_ACTION_REFUSED`, which is INCONCLUSIVE.
- Action **APPROVED** → execute exactly that action (continue, bounded extension, refine ×2 as a fresh solve), increment `iteration`, and go back to step 5. The budget is 4 iterations.
- The terminal verdict is whatever `verdict` returns. Record it unchanged.

### 8. Report
Use `references/report_template.md`: the request, the provenance table, case/mesh, the evidence table straight from `evidence.json`, each proposal with its ruling, the verdict with reasons, the reference comparison, and limitations. Use normalized units where the family is normalized; the paper's model wrongly attached SI units to normalized quantities. Keep every case file, log, proposal, and ruling so the run can be audited.

## Things the gates catch that look fine
- Mesh-sensitivity requests with no registered cross-grid tolerance → INCONCLUSIVE, even when both grids pass.
- `CONTINUE_RUN` after the horizon is reached is refused; an `EXTEND_END_TIME` beyond the registered horizon is refused.
- Refinement is refused unless the current solution is healthy (mesh or topology faults aren't resolution problems).
- Unequal inlet and outlet mass flux in a transient run isn't a conservation failure if the change in stored mass balances it.
- The OpenFOAM start-up line `sigFpe : Enabling floating point exception trapping` isn't a fatal error. The extractor ignores it; the paper's validator once didn't.

The contracts protect against the model's errors, not against errors in their own diagnostics. If a verdict looks wrong, inspect the extractor, fix it, and re-analyse **without** re-solving. Report that you did.
