---
name: legume-gme-workflow
description: >-
  Guides reproducible Legume 1.0.3 PWE, GME, radiative-loss/Q, field,
  symmetry, mode-tracking, autograd optimization, exciton-Schrodinger,
  Hopfield-polariton, and constrained GDS workflows, including explicit
  resource authorization, convergence evidence, and known implementation
  limits. Use it when a task designs, runs, validates, or diagnoses a Legume
  photonic-crystal calculation.
disable-model-invocation: true
---

# Legume GME Workflow

Legume is a frequency-domain **PWE/GME/ESE/Hopfield** package. It is not an
RCWA solver and not an FDTD solver. Do not describe a Legume result as an
RCWA spectrum, a time-domain response, or a replacement for a full-wave
scattering calculation. GME uses a truncated basis of fully guided modes of
an effective slab; convergence inside that approximation does not prove that
GME is appropriate for every structure.

Use the installed Legume 1.0.3 API and the version-matched local source as the
authority. Keep every repository path in generated documentation, commands,
metadata, and reports in forward-slash form.

## Completion states

Always report exactly one numerical level:

1. **Generated**: input, script, or plan exists, but the intended Legume
   computation was not executed.
2. **Executed**: output is readable, but basic screening is incomplete or
   failed.
3. **Screened**: integrity, shapes, mode identity, and applicable basic physics
   pass.
4. **Corroborated**: screening passes and at least one traceable quantitative
   comparison exists; target accuracy or complete convergence may still fail.
5. **Validated**: the complete convergence plan, requested observable,
   mode-identity, required physics, and task-specific accuracy targets pass.

A successful run is not convergence. Finite output is not validation. Record
expert review separately; base-only may be screened or corroborated, never
validated.

## Non-negotiable resource authorization

Before **any** computation that uses BLAS multithreading, local
multiprocessing, or MPI task distribution—including smoke tests, sweeps,
convergence cases, gradient checks, and optimization—the Agent must ask a
structured question and obtain the user's explicit resource configuration:

- `mode`: exactly `serial`, `local_processes`, or `mpi_tasks`;
- `workers/ranks`;
- `BLAS threads per worker`;
- `nodes` and `ranks-per-node`;
- memory limit or budget;
- launcher and affinity policy.

Record the answer with the run. Hardware detection is information, not
authorization. Never infer permission from detected cores, scheduler
variables, an earlier run, or a request to "run fast." Never automatically
occupy all cores. If any resource value changes, ask again before computing.

For `serial`, require `workers/ranks=1`, one node, and still obtain the BLAS
thread count, memory budget, and launcher/affinity answer (`none` is valid).
Environment inspection that performs no eigensolve is allowed before this
question; a solver smoke test is not.

Legume has no native MPI solver or domain decomposition. A single eigensolve
may benefit from BLAS threads. Independent parameter cases, convergence
cases, or k-point chunks may be dispatched by local processes or by an
external `mpi4py` task layer. Do not imply that MPI ranks cooperate on one
Legume eigensolve. Avoid oversubscription:
`workers_or_ranks × BLAS_threads_per_worker` must stay within the
user-approved allocation.

Read [references/parallel-execution.md](references/parallel-execution.md)
before any nontrivial execution. Use
[`scripts/parallel_sweep.py`](scripts/parallel_sweep.py) and
[`templates/parallel-parameter-sweep.py`](templates/parallel-parameter-sweep.py)
for task-level parallel work.

## Phase 1: Establish the model contract

Read [checklists/requirement-intake.md](checklists/requirement-intake.md),
[references/environment-units.md](references/environment-units.md), and
[references/modeling-api.md](references/modeling-api.md).

When invoked through the platform, validate the method-aware
`../../schemas/v1/contracts.schema.json#/$defs/SimulationContract`. Require
`method` to be `pwe`, `gme`, or `hopfield`, retain its canonical hash in
RunManifest, and use lattice/k-space/layer/basis fields. Never add fake FDTD
source, monitor, PML, mesh, or run-time fields to make an eigenproblem fit.

Confirm:

- whether the physical model is 2D PWE, slab GME, ESE, or coupled Hopfield;
- lattice vectors and the physical lattice constant used for conversion;
- layer order, thicknesses, claddings, real permittivities, and shape geometry;
- k-points, path labels, requested modes, symmetry sector, observables, and
  acceptance thresholds;
- for ESE/Hopfield, SI/eV parameters, active-layer position, exciton mass,
  potential, free energy, non-radiative loss, and three-component oscillator
  strength;
- output files, plots, checkpoints, and reproducibility metadata.

Do not invent a material model, symmetry, target mode, or tolerance. Legume
1.0.3 models scalar, frequency-independent permittivity in these workflows;
it is not a general dispersive or absorptive Maxwell solver.

## Phase 2: Verify the environment

When available, run [`scripts/verify_environment.py`](scripts/verify_environment.py).
Record Python, Legume (`1.0.3` expected), NumPy, SciPy, autograd, plotting,
optional `gdspy`/`scikit-image`, BLAS implementation, and package path.
Confirm that the imported package is the intended installation. Do not alter
physics to work around an import, ABI, or backend error.

The default backend is NumPy. Set `legume.set_backend("autograd")` only for a
differentiated objective and keep objective construction compatible with
autograd. See
[references/autodiff-optimization.md](references/autodiff-optimization.md).

### Optional dependency branches

- Differentiable objectives require `autograd`. Verify it before selecting
  [`templates/inverse-design.py`](templates/inverse-design.py) or
  [`scripts/gradient_check.py`](scripts/gradient_check.py).
- Controlled analytic-shape GDS export requires `gdspy`; use
  [`templates/gds-export.py`](templates/gds-export.py). Raster GDS additionally
  needs `scikit-image` but remains experimental and has no production template.
- MPI task distribution requires both `mpi4py` and a working system MPI
  runtime/launcher. Import `mpi4py.MPI`, record `MPI.get_vendor()`, and verify
  the approved world size; importing the Python package alone is insufficient.
- Optional dependencies extend only their named branch. Their presence does
  not turn Legume into a native MPI/domain-decomposed or GPU solver.

## Phase 3: Build and inspect geometry

Build `Lattice`, `PhotCryst`, layers, and non-overlapping analytic shapes.
Plot the direct geometry and a Fourier-reconstructed permittivity before the
solve. Use `truncate_g="abs"` by default because it preserves lattice
symmetry. Treat `tbt` as an explicit performance choice that must be justified
and cross-checked; it can break rotational symmetry.

Mark these paths **experimental** and report the consequence:

- `FreeformLayer`: core Fourier-transform and sampling methods are not
  implemented in 1.0.3;
- overlapping shapes: Fourier permittivity can be wrong;
- `Ellipse` with nonzero rotation and nonzero center: the implementation's
  coordinate/phase handling requires independent geometry validation;
- GDS raster export: contour transform and boundary boolean handling contain
  source TODOs;
- multiple quantum wells: supported by data structures and Hopfield assembly,
  but require explicit layer-by-layer and independent physical validation.

Read [references/exciton-polariton-gds.md](references/exciton-polariton-gds.md)
before ESE, Hopfield, or GDS work.

## Phase 4: Choose the solver branch

Read [references/pwe-gme-workflows.md](references/pwe-gme-workflows.md).

### PWE

Use `PlaneWaveExp` only for a purely 2D periodic layer. Run TE and TM
separately with `run(kpoints=..., pol="te"|"tm", numeig=...)`. PWE 1.0.3 uses
a TBT-style reciprocal grid internally; increase `gmax` and test convergence.
Store `freqs`, `eigvecs`, `kpoints`, and `gvec`.

### GME

Use `GuidedModeExp` for layered photonic-crystal slabs. Start with
`truncate_g="abs"`, explicit `gmax`, `gmode_inds`, `numeig`, `compute_im`,
and k-points. `eigh` diagonalizes the dense matrix and only limits stored modes
with `numeig`; `eigsh` may help when only a few eigenpairs near `eig_sigma`
are needed, but the matrix construction remains dense and speedup is not
guaranteed.

Even guided-mode indices are TE basis modes and odd indices are TM basis
modes. This basis label is not generally the final photonic-mode
polarization.

### ESE and Hopfield

`ExcitonSchroedEq` solves a 2D effective-mass equation in eV/SI inputs.
`HopfieldPol` runs GME plus every active ESE layer and diagonalizes the
generalized non-Hermitian Hopfield matrix. Report polariton energies, losses,
photonic/excitonic fractions, basis sizes, and all unit conversions. Do not
interpret fractions or splittings before uncoupled photonic and excitonic
branches have been checked.

## Phase 5: Apply symmetry and track identity

Read [references/symmetry-mode-tracking.md](references/symmetry-mode-tracking.md).

- Horizontal `xy` mirror symmetry is selected through appropriate
  `gmode_inds`; it is valid only for a truly symmetric slab.
- Vertical `kz` symmetry is valid only when each k-point lies along a real
  vertical mirror plane. Use `path["angles"]` from `Lattice.bz_path` and pass
  it to `run(..., angles=..., kz_symmetry=...)`.
- `kz_symmetry` is `None`, `"even"`, `"odd"`, or `"both"`. For `"both"`,
  consume `kz_symms` rather than assuming output order.
- Keep `truncate_g="abs"` for symmetry work, especially triangular/hexagonal
  lattices, and investigate any `symm_thr` failure instead of loosening it
  reflexively.

Never identify a band only by its array index near a crossing. Track modes by
normalized eigenvector overlap, constrained by frequency continuity and
symmetry labels. For high-Q modes, BIC candidates, avoided/true crossings,
and optimization objectives, overlap tracking is mandatory. Use
[`scripts/track_modes.py`](scripts/track_modes.py).

## Phase 6: Preflight and execute

Apply [checklists/simulation-review.md](checklists/simulation-review.md).
Confirm the explicit resource authorization immediately before the first
eigensolve. If it is absent or stale, stop and ask.

Run one user-authorized reduced case before a sweep or optimization. Check
array shapes, finite values, ordered frequencies/energies, basis dimensions,
geometry reconstruction, and warnings. A smoke result may be **Executed**,
never **Validated**.

For radiative loss, use `compute_im=True`/`run_im()` for all stored modes or
`compute_im=False` followed by `compute_rad(kind, minds)` or
`compute_rad_sp(kind, minds)` for selected modes. Read
[references/radiation-fields-q.md](references/radiation-fields-q.md).

## Phase 7: Validate convergence

Read [references/convergence-validation.md](references/convergence-validation.md)
and use [`templates/basis-convergence.py`](templates/basis-convergence.py).
Follow the official GME sequence:

1. increase `gmax`;
2. increase `gmode_inds`;
3. retest `gmax` after changing `gmode_inds`;
4. if bands are discontinuous or implausible, reduce `gmode_step`, commonly
   from `1e-2` toward `1e-3` or `1e-4`.

Converge the requested observable—not just runtime or a band plot. Frequency,
loss/Q, field profile, symmetry, overlap identity, and gradient may need
different thresholds. High-Q values are especially sensitive: compare
`freqs_im`, Q, radiative channel decomposition, and overlap-tracked identity.
Run [`scripts/validate_results.py`](scripts/validate_results.py).

PWE, ESE, and Hopfield studies must also increase their reciprocal cutoff and
requested basis sizes as applicable. Hopfield validation must separately
converge the photonic basis, each excitonic basis, and polariton observables.

## Phase 8: Optimize safely

Start from a converged-enough forward model. Use
[`templates/inverse-design.py`](templates/inverse-design.py).
Before optimization, compare autograd directional derivatives with central
finite differences at multiple step sizes using
[`scripts/gradient_check.py`](scripts/gradient_check.py). Do not continue on
an unexplained sign, scale, or mode-switch discrepancy.

Use exact gradients by default. Approximate gradients omit the changing-basis
path; they can be suitable for parameters that do not change average
permittivity, but may be inaccurate for thickness, loss/Q, or fields.
Track the target mode by overlap at every iteration, enforce geometry bounds
and no-overlap constraints, checkpoint parameters/objective/gradient, and
record Adam or L-BFGS-B settings.

After optimization, rebuild from saved parameters and recompute with higher
precision: larger converged `gmax`, sufficient `gmode_inds`, appropriate
`gmode_step`, exact gradients where relevant, and selected radiation loss.
Only this independent high-precision result may support **Validated**.

## Phase 9: Fields, plots, and outputs

Use `get_eps_xy`, `ft_field_xy`, `get_field_xy`, `get_field_xz`, and
`get_field_yz` for GME; PWE supports in-plane equivalents. Fields have an
arbitrary global eigenvector phase that can jump with k. Compare
phase-invariant quantities or apply and record a gauge convention.

Use `legume.viz` for bands, Q coloring, structure, permittivity, reciprocal
basis, fields, exciton potential, and wavefunctions, but retain raw arrays;
plots are not validation. Start from the closest available template:

- [`templates/pwe-bandstructure.py`](templates/pwe-bandstructure.py)
- [`templates/gme-slab-bands-q.py`](templates/gme-slab-bands-q.py)
- [`templates/gme-kz-symmetry.py`](templates/gme-kz-symmetry.py)
- [`templates/exciton-polariton.py`](templates/exciton-polariton.py)
- [`templates/gds-export.py`](templates/gds-export.py)

Save parameters, versions, resource authorization, command, raw complex
arrays, units, k-path and angles, eigenvectors needed for overlap tracking,
radiative channels, derived Q, convergence cases, gradient checks, plots,
warnings, and completion state. Apply
[checklists/result-report.md](checklists/result-report.md) and
[references/output-diagnostics.md](references/output-diagnostics.md).
When running through the platform, package these artifacts in V1 RunManifest
and ValidationReport documents with solver ID `solver-legume-gme`.

## Known-limit review

Before claiming **Validated**, read
[references/known-limitations.md](references/known-limitations.md). At
minimum state that GME is approximate and uses only fully guided basis modes;
dense matrix memory scales steeply (roughly `gmax^4`); autograd retains
intermediates; global eigenvector gauge is arbitrary; Q is perturbative; and
experimental geometry/GDS/multi-QW paths need additional evidence.

## Documentation map

- [README.md](README.md)
- [references/environment-units.md](references/environment-units.md)
- [references/modeling-api.md](references/modeling-api.md)
- [references/pwe-gme-workflows.md](references/pwe-gme-workflows.md)
- [references/symmetry-mode-tracking.md](references/symmetry-mode-tracking.md)
- [references/radiation-fields-q.md](references/radiation-fields-q.md)
- [references/convergence-validation.md](references/convergence-validation.md)
- [references/autodiff-optimization.md](references/autodiff-optimization.md)
- [references/exciton-polariton-gds.md](references/exciton-polariton-gds.md)
- [references/output-diagnostics.md](references/output-diagnostics.md)
- [references/parallel-execution.md](references/parallel-execution.md)
- [references/known-limitations.md](references/known-limitations.md)
