---
name: meep-fdtd-workflow
description: >-
  Guides end-to-end Meep FDTD simulations with PyMeep on Linux or WSL using
  Conda. Covers requirements, units, geometry, materials, sources, PML,
  periodicity, monitors, run control, normalization, convergence, HDF5/NumPy
  output, MPI, and diagnosis. Use when asked to design, generate, run, validate,
  or troubleshoot a Meep or PyMeep electromagnetic simulation.
disable-model-invocation: true
---

# Meep FDTD Workflow

Use this workflow to turn a physical question into a reproducible and validated
PyMeep simulation. Do not report a result as physically trustworthy merely
because the script ran.

## Operating contract

- Default to the Python API in a Conda environment on Linux or WSL2.
- Treat the installed Meep version and its matching official documentation as
  the source of truth. Use a local source checkout only when its revision is
  explicitly recorded and matches the runtime being diagnosed.
- Ask only for missing inputs that materially change the model. Never invent a
  material model, polarization, boundary condition, or accuracy target.
- Keep physical input parameters separate from simulation mechanics.
- Generate deterministic scripts and record the Meep version and command used.
- Place no source or monitor inside a PML unless the method explicitly requires
  it and the consequence is documented.
- Prefer decay/convergence stopping criteria to unexplained fixed run times.
- Always include a convergence protocol in the simulation plan, but execute it
  only after the user opts in.
- Require convergence evidence before using the **Validated** completion state.

## Completion states

Always state exactly one numerical level:

1. **Generated**: files are syntactically valid, but Meep was not run.
2. **Executed**: Meep output is readable, but basic screening is incomplete or
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
first, then apply the Meep-specific details below.
Read [checklists/requirement-intake.md](checklists/requirement-intake.md).
When invoked through the platform, accept
`../../schemas/v1/contracts.schema.json#/$defs/SimulationContract`, validate it
before selecting a template, and preserve its `contract_id` and canonical hash
in `RunManifest`.
Before writing the PyMeep script, ask the user in this Meep workflow to select
`single_mpi_process` or `multi_mpi_process`, the exact `mpi_processes`, and the
launcher. Record them in `resources`; do not silently default to serial
execution. This is a Meep-specific intake requirement, not a global G1 field
required from unrelated tools.
Establish:

- physical objective and requested observables;
- dimensionality, coordinate system, geometry, and material dispersion;
- wavelength/frequency range and source polarization/profile;
- open, periodic/Bloch, metallic, or symmetry boundaries;
- target accuracy, spectral resolution, available memory/cores, and outputs.

If the request is exploratory, propose explicit defaults and label them as
assumptions for user confirmation.

## Phase 2: Verify the runtime

Read [references/environment-units.md](references/environment-units.md).

1. Confirm execution is inside Linux/WSL, not native Windows.
2. Run `scripts/verify_environment.py` in the intended Conda environment.
3. Record Python, Meep, MPI, HDF5, NumPy, and platform information.
4. Stop on import/ABI errors; diagnose the environment before writing around
   them.

## Phase 3: Normalize units and design the model

Read [references/modeling-api.md](references/modeling-api.md) and
[references/sources-boundaries.md](references/sources-boundaries.md).

1. Declare the length unit `a` in physical units.
2. Convert vacuum wavelength with `f = 1 / wavelength_in_a`.
3. Compute the shortest wavelength inside every material over the full band.
4. Choose resolution from that shortest wavelength and geometric feature size.
5. Size the cell to include geometry, propagation padding, and PML.
6. Add symmetry only after checking geometry, source, monitor, and desired
   field parity.
7. Use `k_point` only for a physically periodic/Bloch problem.
8. Estimate grid points, memory, time steps, and expected runtime before a 3D
   production run.

Write all tunable values in one parameter section at the top of the generated
script.

## Phase 4: Select source, monitor, and workflow

Read [references/monitors-run-control.md](references/monitors-run-control.md).
Choose one primary workflow:

- field visualization: CW or narrow-band source plus `get_array`;
- broadband R/T: Gaussian source, flux monitors, and two-run normalization;
- resonances/Q: short pulse plus `Harminv`;
- modal S parameters: `EigenModeSource` and eigenmode coefficients;
- frequency-domain fields: DFT fields or `solve_cw`;
- radiation: closed near2far surface plus far-field sampling;
- periodic bands: Bloch `k_point`/`run_k_points`;
- inverse design: `MaterialGrid` and adjoint workflow.

Start from the closest file in `templates/`. Preserve its phase ordering:
parameters → model → preview → monitors → run → validate → save.

Every execution plan must include Phase 7 and list the proposed resolution,
PML/absorber, and run-control cases even though running those cases is optional.

## Phase 5: Preflight before the expensive run

Apply
[`../fdtd-core/checklists/simulation-review.md`](../fdtd-core/checklists/simulation-review.md)
before the Meep-specific review.
Read [checklists/simulation-review.md](checklists/simulation-review.md).

- Render the geometry, PML, source, and monitor layout.
- Confirm all objects are in the intended dimensions and units.
- Check the source spectrum covers every monitor frequency.
- Check PML only occupies open directions and periodic directions remain free
  of PML.
- Confirm the field component is compatible with the requested polarization.

Immediately before the first Meep execution, including a coarse smoke test, ask
the user whether to:

1. run the base simulation plus the planned convergence validation; or
2. run only the base simulation and skip convergence validation.

Use a structured user question when available. Do not infer consent from an
earlier request to generate code or run Meep. Record the choice in metadata and
the result report.

After this decision, run a coarse smoke test and verify finite, nonzero
fields/flux. Do not begin a large parameter sweep until one case passes
preflight.

## Phase 6: Run correctly

- Register DFT/flux/near2far monitors before `run`.
- Launch with the user-approved MPI process count. Use the recorded MPI launcher
  for both the smoke and production cases; do not change process count between
  convergence cases without creating a new approved Run.
- Broadband transient: prefer `until_after_sources=stop_when_*_decayed(...)`.
- Harminv: run after the source and provide enough ring-down time.
- CW: allow transients to decay or use `solve_cw` when appropriate.
- Reflection: first run the reference structure, retain incident flux data,
  then use `load_minus_flux_data` in the device run.
- Under MPI, call Meep collectives on every rank; guard only ordinary plotting
  and non-Meep file operations with `mp.am_master()`.

## Phase 7: Optionally validate convergence

Read [references/convergence-validation.md](references/convergence-validation.md).
Keep the following protocol in the plan regardless of the user's execution
choice. If the user opted in, vary independently:

1. resolution;
2. PML thickness or absorber thickness;
3. decay threshold/run duration.

Evaluate the requested observable, not merely a field image. Apply relevant
checks:

- passive lossless structures: `R + T` or total outgoing power is near one;
- mode decomposition power agrees with flux;
- near2far agrees with a direct DFT field where feasible;
- resonance frequency/Q is stable against resolution and ring-down duration;
- adjoint directional derivative agrees with finite differences;
- symmetry-on and symmetry-off results agree for one reduced case.

Thresholds belong to the simulation contract. Never hard-code a universal
accuracy claim.

If the user opted out, do not run the convergence cases. Mark this phase
`not performed by user choice`, preserve the proposed cases in the report, and
prohibit **Validated**. Completed screening or a traceable quantitative
comparison may still support **Screened** or **Corroborated**.

## Phase 8: Save reproducible outputs

Read [references/output-mpi-diagnostics.md](references/output-mpi-diagnostics.md)
and [checklists/result-report.md](checklists/result-report.md).

Save:

- source script and command;
- V1 `RunManifest` and `ValidationReport` documents;
- parameter/configuration snapshot;
- environment/version metadata;
- frequency/wavelength axes and raw complex data;
- derived quantities and plots;
- convergence cases and relative differences;
- warnings, assumptions, and final completion state.

Prefer NPZ/JSON for compact numerical products and HDF5 for volumetric fields.
Keep raw and derived data separate.

## Phase 9: Diagnose failures

Use this order:

1. environment/import/ABI;
2. units and frequency band;
3. source/monitor placement and field component;
4. numerical stability, material poles, and Courant factor;
5. PML geometry and evanescent overlap;
6. normalization and sign convention;
7. convergence and insufficient decay;
8. MPI collective/I/O ordering.

Read [references/output-mpi-diagnostics.md](references/output-mpi-diagnostics.md)
before modifying physics to hide a numerical problem.

## Advanced branches

Read [references/advanced-workflows.md](references/advanced-workflows.md) before
using dispersive materials, cylindrical coordinates, modal S parameters,
near2far transforms, MPB coupling, MPI subgroup sweeps, or adjoint optimization.

## Documentation anchors

- Installed PyMeep API and version-matched official documentation.
- Official Meep Python examples and regression tests for the installed release.
- A local Meep source checkout may be used for implementation diagnosis when
  its revision is recorded in the run report; it is not a repository
  prerequisite.
