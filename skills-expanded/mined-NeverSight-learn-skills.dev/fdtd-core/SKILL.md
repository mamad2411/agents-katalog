---
name: fdtd-core
description: >-
  Defines solver-independent FDTD contracts, canonical result fields,
  preflight gates, convergence checks, completion states, and reports shared by
  Meep and Lumerical. Use when implementing or reviewing a solver adapter or
  comparing FDTD results across solvers.
disable-model-invocation: true
---

# Solver-independent FDTD core

This skill is the common boundary used by `meep-fdtd-workflow` and
`lumerical-fdtd-workflow`. Solver APIs, units, templates, sessions, and license
details remain in their solver-specific skills.

## Required contracts

Validate platform documents against:

```text
../../schemas/v1/contracts.schema.json
```

Every adapter consumes `SimulationContract` and emits `RunManifest` plus
`ValidationReport`.

## Completion states

- `generated`: model-building code exists; no real solver run completed.
- `executed`: solver output is readable; basic screening is incomplete or
  failed.
- `screened`: integrity, units, axes, and applicable basic physics checks pass.
- `corroborated`: screening passes and at least one traceable quantitative
  comparison exists, even if accuracy or full convergence fails.
- `validated`: the complete convergence plan, required physics checks, and
  task-specific accuracy targets pass.

Never promote a base-only run to `validated`. It may reach `screened` or
`corroborated` when the corresponding evidence exists. The platform does not
hard-code a universal tolerance.

Expert review is separate: `screened + limited` derives
`provisionally_reviewed`; `corroborated/validated + confirmed` derives
`reviewed`. Always display the underlying numerical level.

## Canonical fields

Map solver-native names to these fields before common analysis:

```text
frequency
wavelength
reflectance
transmittance
absorption
field_e
field_h
mode_coefficients
q_factor
far_field
```

Record the native-to-canonical mapping in run metadata.

## Common execution contract

1. Validate the SimulationContract and reject unaccepted material assumptions.
2. Verify environment availability without consuming a commercial license by
   default.
3. Generate a deterministic model in an isolated run directory.
4. Complete [checklists/simulation-review.md](checklists/simulation-review.md).
5. Obtain explicit G2 approval for `base_only` or
   `base_plus_convergence`.
6. Run a reduced smoke case before the production case.
7. Export raw arrays before computing derived quantities.
8. If approved, vary mesh, PML/padding, and run-control independently.
9. Run deterministic physics checks.
10. Emit the report described in
    [checklists/result-report.md](checklists/result-report.md).

## Convergence

Always retain proposed convergence cases in `SimulationContract`. Execute them
only after explicit approval.

Compare the requested observable with:

```text
norm(current - previous) / max(norm(current), machine_epsilon)
```

The tolerance belongs to the contract. Do not use a universal threshold.

## Common physics checks

Select only applicable checks:

- passive lossless structures: `R + T` or total outgoing power;
- mode-decomposed power versus total flux;
- symmetry-on versus symmetry-off reduced case;
- resonance frequency/Q stability;
- near-to-far versus direct field sampling;
- reciprocity or a known limiting case;
- cross-solver trend comparison when both mappings are equivalent.

## Utilities

Run common NPZ/JSON/CSV checks:

```text
python scripts/validate_results.py results.npz --rt-tolerance 0.05
```

Compare static Meep and Lumerical benchmark outputs:

```text
python benchmarks/compare_cross_solver.py meep.npz lumerical.npz
```

The comparison checks axes, energy balance, and spectral trend. It does not
require pointwise equality.
