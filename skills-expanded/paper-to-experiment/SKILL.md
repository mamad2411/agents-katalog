---
name: paper-to-experiment
description: Use when reproducing a physics paper (or part of one) in this MD framework. Walks a paper PDF through the design template + registry, validates against the schema, registers any new force/analyzer/visualizer in the framework's forwarding station, and emits a runnable configs/plan_*.json. Used at the start of any new reproduction campaign.
---

# Paper → Experiment Skill

Turn a physics paper into a validated `configs/plan_<topic>.json` that `python scripts/run_experiment.py` can launch directly. The output of one run of this skill is a campaign that — when run end-to-end — produces a `report.md` and at least one figure per run dir. Anything less is incomplete.

**This skill is a gate, not a free-form writer.** You follow the template, the schema, and the registry. You don't invent fields. You surface ambiguity to the user before writing JSON.

---

## Hard rules (no exceptions)

1. **Registry first.** Open `references/force_types.md` AND `tools/registry.py` (the framework's forwarding station for forces / lattices / analyzers / plotters / aggregators / visualizers) BEFORE proposing any field. The skill works only with **registered** strings — for any extension, you must walk through §"Adding a new force type" 8-step process and register the new class in `tools/registry.py:_REGISTRY` AND in the matching package's local `__init__.py`.

2. **Paper PDF on disk.** Step 2 requires a real PDF under `papers/<slug>.pdf`. If the user only has an abstract / link / mental model, **stop** and ask them to put the PDF in `papers/`. Abstract-only reproduction is unsupported — it has produced bad reproductions in the past.

3. **Citations are mandatory.** Every observable in §1 of the design doc must cite a paper Eq. or Fig. number. If a number isn't in the paper, mark it with `*` and explain in §11. No bare claims like "expected to converge."

4. **Smoke before production.** Every config you emit must have `pipeline.smoke=true` and `smoke_steps ≥ 100` unless the user explicitly asks otherwise (and you note the override in `_comment`).

5. **Validation gate.** Before announcing the config is ready, run `python scripts/validate_config.py <path> --strict`. If it returns non-zero, fix the issues and re-run; do not hand off a failing config.

6. **Cost budget.** If the validator reports `single-run wall > 24 hr` or `VRAM > 8 GB`, propose smaller `N` or `steps` rather than asking the user to approve a 1-day GPU burn.

7. **No silent invention.** If a paper parameter is missing from the source, **ASK** in §10b (decision log) — don't fill in a "reasonable guess." Acceptable: `T0=0.3` because §II of paper says so. Unacceptable: `T0=0.3` because it worked for E1.

8. **Reuse before extending.** If the paper's force resembles `lennardJones`, `HertzianNonreciprocal`, or `ERPotential`, reuse it. Only propose a new force class if §2 of the design doc cites a paper equation that genuinely cannot be expressed by the existing classes. Reuse-with-degenerate-parameter (e.g. `ERPotential` with `MT=0` ≡ isotropic Yukawa) is **forbidden** for thesis-quality reproductions — see Anti-patterns below.

9. **A reproduction is not done until you can see the answer.** Pipeline must produce, per run dir, **at least** `manifest.json` (engine wired up) AND `report.md` (analyzer ran) AND `fig*.png` (visualizer ran). If your config produces only the first one, you **skipped step 7 and/or step 8** of the extension process — analyzer / visualizer were never registered. Go back, register them in `tools/analyzers/<paper>.py`, `tools/plotters/<paper>.py` (or visualizers), then `tools/registry.py:_REGISTRY`, then point your config's `aggregation.class` and `pipeline.visualize.class` at them. Do **not** declare the campaign successful with manifest-only output.

---

## Process flow

```
1. Acknowledge → 2. Read paper + registry → 3. Fill design doc → 4. User approves
                                                                       ↓
                       7. Hand off ← 6. Validate ← 5. Emit JSON ←  (extension step if needed)
```

### Step 1 — Acknowledge

Announce: *"Using paper-to-experiment skill. Will walk through the fixed template, then emit a validated config."*

Confirm with the user where the paper is:
- PDF path under `papers/<slug>.pdf` — required (Hard rule #2).
- If absent, stop and ask user to populate `papers/`. Do not proceed.

### Step 2 — Read paper + registry + framework state

Read in this order:
1. The paper PDF under `papers/`.
2. `references/force_types.md` (registry — what `force_type` strings exist).
3. `tools/registry.py:_REGISTRY` (forwarding station — what classes are wired).
4. The two existing examples under `references/examples/` (worked design docs).
5. Any prior `docs/specs/<TOPIC>-design.md` if this is a continuation.

Identify:
- which `force_type` to use (or whether a new one is needed → §"Adding a new force type" 8-step)
- which physics observables the paper reports as primary results
- which figures of the paper we are claiming to reproduce
- which lattice IC the paper uses (default `square_2d` for ndim=2 / `simple_cubic_3d` for ndim=3; override via design doc §3 only when paper specifies)
- any analytical fingerprints (dimensionless numbers from appendices) that we can compute pre-simulation

### Step 3 — Fill design doc

Copy `templates/physics_design.md` to `docs/specs/YYYY-MM-DD-<topic>-design.md`. Replace EVERY `<...>` placeholder. If a section truly does not apply, write `N/A — <reason>` (do not delete).

§1 (observables) is the spine. Everything else flows from it: §3 setup must be sufficient to measure §1; §4 sweep must vary the dependence claimed in §1; §6 pass criteria must declare numeric thresholds for §1.

For §2 (force field):
- If existing class works: paste the registry entry's required fields verbatim, then list which simulation parameters from §3 you need.
- If new class needed: complete §2a in full and **stop**. Surface to user — new force class triggers the 8-step extension process (force class → tests → adapter → dispatcher → schema → registry → analyzer → visualizer) which is the user's call to greenlight.

For §4 (sweep dimensions):
- Total runs ≤ 12 by default. If more needed, split into Plan A / Plan B and emit two configs.
- Each sweep value must be motivated by a paper passage (cite it).

For §3 simulation setup `initial_state` field:
- Default to `square_2d` (ndim=2) or `simple_cubic_3d` (ndim=3).
- Override only when paper specifies a different lattice (e.g. `triangular_2d` for hexatic-phase studies).
- For long-range repulsive forces (Coulomb / Yukawa / hard-core surrogate), random IC is **forbidden** by `references/force_types.md` "Long-range repulsive IC caveat" subsection — random IC + short Langevin produces wrong steady-state temperature.

### Step 4 — User approval

Save the design doc and ask the user to review it. Cite the path explicitly. List the §10b open questions if any.

§10 has TWO sub-lists:
- **§10a Auto-decisions taken**: defaults from registry/examples, granularity choices justified by paper context. AI may take these in auto-mode without blocking.
- **§10b Open questions for human** (`ASK USER:` prefix required): items only the user can resolve.

§0 metadata also includes an "Open questions early checklist" that the agent should fill **before** filling the rest of the design — surfacing blockers up front.

Approval rules:
- **Interactive**: do not proceed until user signals approval.
- **Auto-mode**: proceed if §10b is empty. Any `ASK USER:` line stops auto-mode.

### Step 5 — Emit JSON

Generate `configs/plan_<topic>.json` from the approved design doc. Required top-level fields:

```json
{
  "_comment": "<one paragraph from §0 + §1 summary>",
  "_paper_ref": "<from §0 citation>",
  "_paper_pdf": "papers/<slug>.pdf",
  "_design_doc": "docs/specs/YYYY-MM-DD-<topic>-design.md",
  "_force_type_doc": "<from references/force_types.md §N>",
  "_units_doc": "<reduced_lj | macro_dust | reduced_yukawa | ...>",
  "campaign": [ /* one entry per run from §4 cross-product */ ],
  "pipeline": {
    "preflight": true,
    "smoke": true,
    "smoke_steps": 100,
    "production": true,
    "analyze": true,
    "analyzer_class": "<paper>Analyzer",
    "halt_on_fail": true,
    "max_parallel": <2 default>,
    "visualize": {"enabled": true, "class": "<paper>Plotter"}
  },
  "aggregation": {
    "enabled": true,
    "class": "<paper>Aggregator",
    "output": "docs/<paper>_campaign_report.md",
    "plots": [...]
  }
}
```

Each campaign entry must contain ONLY fields listed in `references/force_types.md` for the chosen `force_type`. Add `notes` field with one-line rationale linked to the design doc §.

`pipeline.analyzer_class`, `pipeline.visualize.class`, and `aggregation.class` MUST point to classes registered in `tools/registry.py:_REGISTRY`. If the paper requires bespoke analysis, **register** the new analyzer / plotter / aggregator classes via the 8-step extension process before emitting the config — see Hard rule #9.

Pipeline phases run in this order: preflight → smoke → production → **analyze (3.4)** → **visualize (3.5)** → aggregate. Phase 3.4 ANALYZE only fires when both `analyze=true` AND `analyzer_class` are set; existing PRX/ER configs that ran the analyzer inline in their adapters omit `analyzer_class` and skip the phase.

### Step 6 — Validate

Run:
```
python scripts/validate_config.py configs/plan_<topic>.json --strict
```

If exit 0: proceed to Step 7.
If exit 1 or 2: read the errors and warnings, fix the JSON, re-run. Do not hand off until clean.

**Cross-check costs against design doc §7**: validator's `cost estimate` line should be within 2× of your design doc §7 estimate. If they differ by >2×, the validator's step-rate model is stale.

### Step 7 — Hand off

Tell the user:
- design doc path
- config path
- validation summary (exit code + cost estimate)
- exact launch command: `python scripts/run_experiment.py configs/plan_<topic>.json`
- expected wall time and disk
- per-run-dir expected outputs: `manifest.json` + `report.md` + at least one `fig*.png`

DO NOT launch the campaign yourself unless explicitly asked. The user owns the GPU-burn decision.

---

## Adding a new integrator — 9-step extension process

If the paper requires a time-integration scheme the existing integrators cannot faithfully reproduce — most commonly Wiener-noise (FD-balanced) Langevin for diffusion / viscosity / glass-transition observables, or Bussi NVT — walk the 9-step extension flow in `references/force_types.md §5b "Adding a new integrator"`. Briefly: subclass `IntegratorBase`, write tests, register in `integrators/__init__.py:INTEGRATOR_REGISTRY` AND `tools/registry.py:_REGISTRY`, add to the schema's `integrator` enum, and document in the §4 "Integrator selection" table. The default `baoab_drag` is fine for NVE and structural NVT, but plateaus MSD over Langevin runs (no Wiener noise).

If the existing `baoab_drag` is the wrong tool for the paper's central observable, **propose the integrator extension up front in design doc §3** (`integrator: <new_scheme>`) and **stop** for user greenlight before walking step 1 — same gate as the 8-step force extension.

---

## Adding a new force type — 8-step extension process

When the paper requires a force / analyzer / visualizer not in the registry, walk through these 8 steps in order. The skill cannot ship a strict-validating, *visually-meaningful* config until **all 8** are merged.

| Step | Action | Files (write + register) |
|------|--------|--------------------------|
| 1. Force class | Implement `<NewForce>` subclassing `forceField` | Write `forces/<your_force>.py`. Register in `forces/__init__.py:FORCE_REGISTRY` AND `tools/registry.py:_REGISTRY`. |
| 2. Tests | Pair tests for force magnitude / symmetry / cutoff | Write `tests/test_<class>_<N>cases.py`. Run `pytest -x` until green. |
| 3. Adapter | Per-paper run script (one file per registered run_type) | Write `<topic>_run.py` at project root, mirroring `prx_nonreciprocal_run.py` / `er_plasma_run.py`. Use `tools.lattices.LATTICE_REGISTRY[design_doc.initial_state]` for IC. |
| 4. Dispatch | Wire the adapter into the campaign runner AND validator | Edit `scripts/run_experiment.py:_invoke_md` (new branch + `EXP_REQUIRED_<TYPE>`); edit `scripts/run_experiment.py:EXP_DEFAULTS_BY_TYPE`; edit `scripts/validate_config.py:check_force_type_specific` (new elif branch). |
| 5. Schema | Plumb new `force_type` enum value | Edit `templates/plan_config.schema.json` (enum + if/then with `ndim` + `units_regime`; extend top-level `units_regime` enum if a new units yaml is needed). |
| 6. Force registry doc | Document the new force_type for the registry | Add `## N. <new_type>` section to `references/force_types.md` with paper ref, fields, **compat block** (`ndim`, `units_regime`), examples, pre-flight rules. |
| 7. Analyzer | Per-run analysis class producing `report.md` + numeric outputs | Write `tools/analyzers/<paper>.py` with `<Paper>Analyzer.full_analysis(run_dir, **params) -> dict` returning fields written to `report.md`. Register in `tools/registry.py:_REGISTRY`. |
| 8. Visualizer / aggregator | Plot generation per run + cross-run | Write `tools/plotters/<paper>.py` with `<Paper>Plotter.render(run_dir)` writing `figN_*.png`. Optional `tools/aggregators/<paper>.py` for cross-run report. Register both in `tools/registry.py:_REGISTRY`. |

After all 8 steps:
- Config can `pipeline.visualize.class = "<Paper>Plotter"` and `aggregation.class = "<Paper>Aggregator"`.
- Each production run dir gets `manifest.json` + `report.md` + `fig*.png` automatically.
- `python scripts/validate_config.py --strict` passes.

**A reproduction that stops at step 6 has only proved the engine wires up.** It has not produced any visible answer. By Hard rule #9, that is incomplete.

---

## Anti-patterns (red flags — STOP and fix)

| Thought | Reality |
|---------|---------|
| "I'll skip the design doc — it's just one run" | The design doc IS the audit trail. Future-you needs it. |
| "I can guess the paper's φ value from context" | No. Cite or ask. |
| "Smoke wastes 30 seconds, skip it" | Smoke saves 30 minutes when something's broken. Always on. |
| "I'll fix the warnings later" | Validator must be green BEFORE handoff. |
| "Let me launch a quick test of the campaign" | User owns launch. Skill never auto-runs production. |
| "8 sweep dimensions, 64 runs, easy" | Hard cap 12 runs per plan; split if more. |
| "ERPotential with MT=0 is just isotropic Yukawa, reuse it" | The manifest will **lie** about what ran. Dead anisotropy machinery still allocated. Thesis reproductions need clean force classes — flag as §10b decision. |
| "The pipeline ran fine, manifest.json exists, done" | Hard rule #9: no `report.md` + no `fig*.png` = analyzer / visualizer never registered. Step 7 + 8 of the 8-step extension are not optional. |
| "I'll register the analyzer in `tools/registry.py` only — skip the local `__init__.py`" | Forwarding station and local registry kept in sync is the framework contract. Both registers, or neither. |
| "Random IC is fine, the Langevin will sort it out" | For long-range repulsive forces, random IC + short Langevin under-cools by ~10× (see force_types.md "Long-range repulsive IC caveat"). Use `tools/lattices/<lattice>` IC instead. |
| "MSD plateaued in my Langevin run, must be a physics finding" | Probably the integrator: `baoab_drag` has no Wiener noise so caged particles never escape. If the paper's central observable is diffusion / viscosity / glass dynamics, you need a different integrator — walk the 9-step extension in `force_types.md §5b "Adding a new integrator"`. |
| "I'll skip §10b open questions to keep flow" | §10b empty is the auto-mode gate. Lying about it produces wrong physics. |

---

## When to extend (not just use) this skill

If you want to:
- Add a new field to the schema → edit `templates/plan_config.schema.json`, then `references/force_types.md`, then this skill in lockstep.
- Add a new force type → walk the 8-step extension above. Do NOT add to schema until force class + tests + adapter + dispatcher + validator updates are merged.
- Change validator rules → edit `scripts/validate_config.py`, add a regression test (validate against a known-good config and a known-bad one).

---

## Files in this skill

```
.claude/skills/paper-to-experiment/
├── SKILL.md                            # this file
├── templates/
│   ├── physics_design.md               # design doc template (§0–§12)
│   ├── plan_config.schema.json         # JSON Schema for configs/plan_*.json
│   ├── force_class.py.template         # scaffold for new forces/<name>.py
│   └── adapter_run.py.template         # scaffold for new <topic>_run.py
└── references/
    ├── force_types.md                  # registry of valid force_type values
    └── examples/                       # finished design docs as exemplars
        ├── worked_example_PRL2008.md
        └── worked_example_PRX2015.md
```

End of skill.
