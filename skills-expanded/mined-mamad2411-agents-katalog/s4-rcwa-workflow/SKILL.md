---
name: s4-rcwa-workflow
description: Build, run, validate, and diagnose S4 1.1.1 RCWA/Fourier-modal simulations for stratified structures with zero, one, or two in-plane periodic directions. Use for layered-stack or grating reflection/transmission, diffraction orders, complex mode amplitudes, E/H/epsilon fields, S-matrix poles, optical force or energy integrals, adaptive spectra, and approved independent-case threading or MPI execution through S4/S4mpi.
---

# S4 RCWA Workflow

Use the stable S4 1.1.1 Lua interface for solving and Python only for
orchestration, contract rendering, result conversion, and validation. Do not
substitute the incomplete native Python extension or the experimental S4v2 API.

## Completion states

Report exactly one numerical level:

1. **Generated**: the contract and self-contained Lua run exist, but S4 did not
   execute.
2. **Executed**: S4 output is readable, but basic screening is incomplete or
   failed.
3. **Screened**: integrity, units, axes, order accounting, and applicable basic
   physics pass.
4. **Corroborated**: screening passes and at least one traceable quantitative
   comparison exists; target accuracy or complete convergence may still fail.
5. **Validated**: the complete convergence plan, requested observable,
   applicable physics, and task-specific accuracy targets pass.

A successful process exit is not convergence. Record expert review separately;
base-only may be screened or corroborated, never validated.

## Phase 1: establish the RCWA contract

Read [references/modeling-api.md](references/modeling-api.md) and
[references/environment-units.md](references/environment-units.md).

Require:

- `method: rcwa`, Cartesian coordinates, and dimensionality `1d`, `2d`, or
  `2.5d`;
- an ordered layer stack with zero-thickness first and last half spaces;
- lattice vectors, analytic layer regions, material tensors or scalars,
  excitation, frequencies, requested outputs, and validation tolerances;
- periodic or invariant transverse boundaries and open half spaces along z;
- explicit `NumG`, Fourier formulation, truncation, and convergence cases.

When invoked through the platform, validate
`../../schemas/v1/contracts.schema.json#/$defs/SimulationContract` and preserve
its canonical hash in RunManifest.

Do not invent material dispersion, tensor entries, polarization, incidence
angles, pattern precedence, or acceptance thresholds. Reject PML, time-domain
sources, nonlinear media, and `SetExcitationInterior`.

## Phase 2: authorize and probe resources

Read [references/platform-parallel.md](references/platform-parallel.md).
Before any S4 computation, including a smoke test, obtain and record
`resources.tool_config` with:

- runtime: `linux`, `wsl`, or `windows_msys2`;
- exact S4/S4mpi executable and WSL distribution when applicable;
- mode: `serial`, `threaded_cases`, or `mpi_tasks`;
- workers or ranks, BLAS threads, approved CPUs, nodes/ranks-per-node;
- memory budget/per task, launcher, affinity, and approval ID.

Run `scripts/verify_environment.py` without `--run-smoke` for a read-only
probe. Hardware detection is information, not authorization. S4mpi and
`SolveInParallel` distribute independent cases; they do not domain-decompose
one RCWA solve.

## Phase 3: build and inspect the model

Read [references/formulations-convergence.md](references/formulations-convergence.md).

1. Define the length unit and use `frequency = 1 / wavelength_in_unit`.
2. Add every material before its layers and regions.
3. Add layers in increasing z; keep the first and last thickness zero.
4. Add circle, ellipse, rectangle, or polygon regions in declared order.
5. Use circular G-vector truncation unless a recorded reason requires
   parallelogramic truncation.
6. Select the Fourier formulation from material type and convergence evidence.
7. Inspect `GetEpsilon` or a layer-pattern realization before solving.

Use `scripts/render_model.py` to render contract data as a safe Lua table.
Keep the generated contract, model table, driver, and helper together.

## Phase 4: select an output profile

Read [references/outputs-validation.md](references/outputs-validation.md).

- `layered_periodic_scattering.lua`: total R/T/A, per-order efficiencies, and
  optional complex amplitudes;
- `field_map.lua`: epsilon and complex E/H samples;
- `s_matrix_poles.lua`: scaled S-matrix determinant in the complex-frequency
  plane;
- `force_energy_integrals.lua`: stress and layer/line energy integrals;
- `adaptive_spectrum.lua`: adaptive scalar spectrum sampling;
- `mpi_frequency_sweep.lua`: rank-sharded independent frequency cases.

Use a stable profile for registered Adapter execution. Treat dipole excitation,
experimental FMM, POV-Ray, S4v2, and direct C/Python bindings as manual or
experimental branches.

## Phase 5: preflight and execute

Read [checklists/simulation-review.md](checklists/simulation-review.md).

- Verify material names, layer order, region dimensions, lattice convention,
  polarization, frequency sign, output sample bounds, and expected file sizes.
- Confirm tensor materials are not combined with an unsupported polarization
  decomposition formulation.
- Avoid exact diffraction-threshold frequencies where the layer eigensystem
  can become singular.
- Ask for G2 choice `base_only` or `base_plus_convergence` immediately before
  execution.
- Execute only with the approved resource configuration and preserve stdout,
  stderr, command, executable paths, runtime, and S4 version.

## Phase 6: normalize and validate

Use `scripts/collect_results.py` to convert S4 TSV files to NPZ plus JSON
metadata. Use `scripts/validate_results.py` for finite-value, shape, R/T/A,
per-order sum, and convergence checks.

Vary independently:

1. `NumG`;
2. Fourier formulation resolution when discretization, subpixel smoothing, or
   polarization decomposition is active;
3. lattice truncation or a justified formulation cross-check.

Compare the requested observable, not only a field image. For passive lossless
scattering, check `R + T = 1` within the contract tolerance. For lossy media,
check `R + T + A = 1` and the declared loss sign. Verify per-order sums against
total flux. Require pole position, force, energy, or field samples to converge
when they are the target.

## Phase 7: report and diagnose

Read [checklists/result-report.md](checklists/result-report.md) and
[references/known-limitations.md](references/known-limitations.md).

Save the SimulationContract, Lua files, resource configuration, RunManifest,
raw TSV, normalized NPZ/JSON, plots, convergence cases, ValidationReport,
warnings, and final state.

Diagnose in this order:

1. executable, Lua/BLAS/LAPACK, MPI, or path translation;
2. units, frequency sign, incidence angles, and polarization;
3. missing material/layer names and half-space order;
4. region periodization and non-orthogonal lattice sampling;
5. diffraction threshold or insufficient `NumG`;
6. Fourier formulation/tensor incompatibility;
7. flux sign, normalization, and per-order mapping;
8. thread-unsafe LAPACK or resource oversubscription.
