---
name: lumerical-fdtd-workflow
description: >-
  Guides end-to-end Ansys Lumerical FDTD simulations using the Python API and
  Lumerical Script Language. Covers requirements, units, geometry, materials,
  sources, boundaries, monitors, run control, sweeps, convergence, output, and
  diagnosis. Use when asked to design, generate, run, validate, or troubleshoot
  a Lumerical FDTD electromagnetic simulation.
disable-model-invocation: true
---

# Lumerical FDTD Workflow

Turn a physical question into a reproducible, reviewable, and validated
Lumerical FDTD simulation. A completed solver run is not, by itself, evidence
that the result is physically trustworthy.

## Operating contract

- Prefer the Python API. Try `ansys.lumerical.core` first and support the
  traditional `lumapi` module when that is what the installed release provides.
- Use Lumerical Script Language (LSF) when an existing workflow or command is
  clearer in LSF; record which interface was used.
- Ask only for missing inputs that materially change the model. Never invent a
  material model, polarization, boundary condition, mode, or accuracy target.
- Keep physical parameters separate from solver, mesh, and output mechanics.
- Use SI values in Python. Label every displayed or exported converted unit.
- Generate deterministic scripts and record the Lumerical version, API import,
  project file, script, command, and relevant license configuration.
- Manage sessions explicitly. Prefer a context manager and save the `.fsp`
  project before an expensive run.
- Place sources and monitors outside PML. Put mode-expansion monitors in
  uniform waveguide sections.
- Always include a convergence protocol in the plan. Execute it only after the
  user explicitly opts in.
- Require convergence evidence before using the **Validated** completion state.

## Completion states

Always state exactly one numerical level:

1. **Generated**: scripts and project-building logic were created, but FDTD was
   not run.
2. **Executed**: FDTD output is readable, but basic screening is incomplete or
   failed.
3. **Screened**: integrity, units, axes, and applicable basic physics pass.
4. **Corroborated**: screening passes and at least one traceable quantitative
   comparison exists; target accuracy or full convergence may still fail.
5. **Validated**: the complete convergence plan, required physics, and
   task-specific accuracy targets pass.

Record expert review separately. A base-only run may be screened or
corroborated, but never validated.

## Phase 1: Collect the simulation contract

Read the solver-independent
[`../fdtd-core/checklists/requirement-intake.md`](../fdtd-core/checklists/requirement-intake.md)
first, then apply the Lumerical-specific details below.
Read [checklists/requirement-intake.md](checklists/requirement-intake.md).
When invoked through the platform, accept
`../../schemas/v1/contracts.schema.json#/$defs/SimulationContract`, validate it
before building the model, and preserve its `contract_id` and canonical hash in
`RunManifest`.
Before writing Python/LSF model code, ask the user in this Lumerical workflow
to select `single_mpi_process` or `multi_mpi_process`, the exact
`mpi_processes`, and the FDTD resource configuration. Record them in
`resources`; do not rely on an unrecorded GUI default. This is a
Lumerical-specific intake requirement, not a global G1 field required from
unrelated tools.
Establish:

- physical objective and requested observables;
- dimensionality, geometry, materials, and valid dispersion ranges;
- wavelength/frequency range, source profile, polarization, and guided mode;
- open, periodic/Bloch, symmetric/antisymmetric, or metallic boundaries;
- target accuracy, spectral resolution, available memory/cores/licenses, and
  required outputs.

For exploratory work, propose explicit defaults and ask the user to confirm
assumptions whose consequences materially affect the result.

## Phase 2: Verify the runtime

Read [references/environment-units.md](references/environment-units.md).

1. Run `python scripts/verify_environment.py`.
2. If the API cannot be imported, locate the installed API without copying
   package files into the project.
3. Before a real run, use `--launch-session` to test an FDTD session and
   license only after the user permits consuming a license seat.
4. Record platform, Python, API flavor, package path, and solver version.
5. Stop on import, license, or interop errors; diagnose them before altering
   simulation physics.

## Phase 3: Design the model

Read [references/modeling-api.md](references/modeling-api.md) and
[references/sources-boundaries.md](references/sources-boundaries.md).

1. Express Python geometry and wavelength values in metres.
2. Verify every material model covers the full simulation band.
3. Size the FDTD region for geometry, propagation padding, and PML.
4. Choose mesh accuracy and local mesh overrides from the shortest material
   wavelength and smallest relevant feature.
5. Add symmetry only after checking geometry, source, monitor, and field
   parity.
6. Use periodic or Bloch boundaries only for a physically periodic problem.
7. Estimate cells, memory, simulation time, and license/resource needs before
   a 3D production run.

Keep tunable values in one parameter/configuration section.

## Phase 4: Select source, monitor, and workflow

Read [references/monitors-run-control.md](references/monitors-run-control.md).
Choose one primary workflow:

- field distribution: narrow-band source plus field/profile monitor;
- broadband reflection/transmission: plane-wave or mode source plus power
  monitors and a documented normalization convention;
- modal S parameters: mode source/port plus mode-expansion monitors;
- resonance/Q: pulsed excitation plus time signal or frequency-domain analysis;
- radiation: near-field monitor plus far-field projection;
- periodic diffraction: one unit cell, periodic/Bloch boundaries, and
  diffraction-order analysis;
- inverse design: a validated forward model followed by LumOpt or another
  documented optimization workflow.

No concrete templates are supplied. Derive code from these references and
official documentation. Preserve this phase order:

`parameters → session → model → preview → monitors → save → run → validate → export`

Add a script to `templates/` only after it is mature, parameterized, documented,
and independently reviewed.

Every execution plan must include Phase 7 and list proposed mesh, PML/padding,
and run-control cases even when the user may skip them.

## Phase 5: Preflight before execution

Apply
[`../fdtd-core/checklists/simulation-review.md`](../fdtd-core/checklists/simulation-review.md)
before the Lumerical-specific review.
Read [checklists/simulation-review.md](checklists/simulation-review.md).

- Save and inspect the `.fsp` layout before the expensive run.
- Confirm geometry, source, monitors, boundaries, and mesh use intended units.
- Check the source spectrum covers all requested monitor frequencies.
- Check PML is present only on open boundaries.
- Confirm monitor orientation, power sign, mode basis, and propagation
  direction.
- Verify estimated memory and storage are acceptable.

Immediately before the first solver execution, including a coarse smoke test,
ask whether to:

1. run the base simulation plus the planned convergence validation; or
2. run only the base simulation and skip convergence validation.

Use a structured question when available. Record the choice in metadata and
the result report. Do not infer consent from an earlier request to generate
code or run FDTD.

Run one reduced smoke case before any large sweep. Require finite, nonzero,
physically plausible monitor data.

## Phase 6: Run correctly

- Use an explicit session lifecycle, preferably `with lumapi.FDTD(...) as fdtd`.
- Apply the user-approved FDTD resource/MPI process count before `run`, record it
  in metadata, and do not silently substitute a different resource profile.
- Set order-dependent object properties with an ordered mapping or in a safe
  sequence.
- Save the project before `run`; save again after configuration changes whose
  state must be preserved.
- Use auto shutoff with a justified simulation-time ceiling. Do not treat auto
  shutoff as a convergence study.
- Retrieve named datasets and inspect axes, shapes, units, and complex-valued
  conventions before computing derived quantities.
- For sweeps, validate one case first, keep parameter/result names stable, and
  distinguish solver parallelism from independent-job parallelism.
- Close sessions after success or failure so licenses are released.

## Phase 7: Optionally validate convergence

Read [references/convergence-validation.md](references/convergence-validation.md).
Keep the protocol in the plan regardless of the user's execution choice. If
the user opted in, vary independently:

1. global mesh accuracy and/or local mesh spacing;
2. PML layers/type and distance from the structure;
3. simulation-time ceiling and auto-shutoff threshold.

Evaluate the requested observable, not only a field image. Apply relevant
energy balance, reciprocity, modal power, symmetry, far-field, resonance, and
reference-geometry checks. Accuracy thresholds belong to the simulation
contract; never claim a universal tolerance.

If the user opted out, mark this phase `not performed by user choice`, retain
the proposed cases, and prohibit **Validated**. Completed screening or a
traceable quantitative comparison may still support **Screened** or
**Corroborated**.

## Phase 8: Save reproducible outputs

Read [references/output-diagnostics.md](references/output-diagnostics.md) and
[checklists/result-report.md](checklists/result-report.md).

Save:

- Python/LSF source, `.fsp` project, and launch command;
- V1 `RunManifest` and `ValidationReport` documents;
- input parameter snapshot and object-name map;
- solver, API, platform, and license-mode metadata;
- frequency/wavelength axes and raw complex monitor data;
- derived quantities, plots, sweep definitions, and sweep results;
- convergence cases, relative differences, assumptions, and warnings;
- the final completion state.

Prefer NPZ/JSON for portable numerical products, CSV for simple real-valued
tables, and MAT only when downstream tooling requires it. Keep raw and derived
data separate.

## Phase 9: Diagnose failures

Use this order:

1. API import, installation path, license, and session launch;
2. units, wavelength/frequency band, and material validity;
3. geometry/object selection and property-setting order;
4. source, monitor, mode, orientation, and dataset names;
5. mesh, memory, conformal-mesh behavior, and simulation duration;
6. PML placement, periodicity, symmetry, and evanescent overlap;
7. normalization, power sign, and mode convention;
8. convergence, sweep configuration, job scheduling, and output paths.

Read [references/output-diagnostics.md](references/output-diagnostics.md)
before changing physics to hide a numerical or environment problem.

## Advanced branches

Read [references/advanced-workflows.md](references/advanced-workflows.md) before
using mode-expansion S parameters, periodic diffraction, far-field projection,
resonance/Q extraction, parameter optimization, LumOpt, or cluster execution.

## Documentation anchors

- Ansys Lumerical Python API reference and session-management documentation.
- Lumerical scripting command reference for the installed release.
- FDTD Solver, source, boundary-condition, mesh, and monitor documentation.
- Installed examples matching the current solver version.

Confirm command and property names against the installed version. Do not assume
an online example targets the user's release or API flavor.
