---
name: reproduce-instructor
description: Generate a simulation-grounded instruction.md for reproducing scientific-paper figures from a PDF or a converted Markdown paper with an images folder. Use when preparing paper-reproduction tasks that must build and solve the reported structure through an open-source or commercial simulator API.
---

# Reproduce Instructor

Generate `instruction.md` in the paper task root. Accept either a local PDF or an
already converted Markdown paper with a sibling `images/` directory.

The instruction must be solver-agnostic but simulation-mandatory: choose a
suitable open-source or commercial solver for the paper, require its library or
automation API, and require the structure to be built and solved inside that
simulator. Never permit analytical or synthetic fields to replace the simulation
data used for final results.

## References

Read these before drafting:

1. [`examples/instruction-template.md`](examples/instruction-template.md) for the
   solver-agnostic baseline structure and requirements shared by existing
   instructions.
2. [`preferred-simulators.md`](preferred-simulators.md) for preferred simulation
   software/libraries, method-to-task guidance, and admission criteria for
   another tool.
3. [`../../schemas/README.md`](../../schemas/README.md) and
   [`../../schemas/v1/contracts.schema.json`](../../schemas/v1/contracts.schema.json)
   for the machine-readable `PaperManifest`, `Evidence`, `Targets`, and
   `SimulationContract` boundaries.
4. Query the external Example Library when it is configured. Treat retrieved
   examples as versioned suggestions, never as paper evidence or mandatory
   wording.
5. For PDF conversion, read
   [`../UniParser-Paper-Markdown/SKILL.md`](../UniParser-Paper-Markdown/SKILL.md)
   and use its bundled scripts rather than writing an ad hoc parser.

## Output Contract

- Write the final file as `<task-root>/instruction.md`.
- Write all headings, prose, tables, and directives in `instruction.md` in
  English, following the section structure and directive style of
  `examples/instruction-template.md`. Preserve source titles, author names,
  identifiers, equations, symbols, citations, and paths verbatim where needed.
- Also write the following V1 documents and validate each against
  `../../schemas/v1/contracts.schema.json`:
  - `<task-root>/evidence.json` as `Evidence`;
  - `<task-root>/targets.json` as `Targets`;
  - `<task-root>/simulation-contract.json` as `SimulationContract`.
- Keep `instruction.md` as the human-readable view. The JSON documents are the
  machine interface used by the Planner and solver adapters; do not maintain
  conflicting values in both places.
- Keep the source PDF (when supplied), primary paper Markdown, and `images/` in
  `<task-root>`. PDF conversion performed by this skill must produce all three
  in that directory.
- Do not create `brief_analysis.md` unless the user requests it.
- Do not overwrite an existing `instruction.md`, paper Markdown, image, or
  directory without inspecting it and obtaining confirmation for destructive
  replacement.
- Keep edits within `<task-root>` except when reading this skill and its
  references or using a temporary conversion directory.
- Never write directly to the published Example Library. A completed run may
  only create an `ExampleCandidate`; publication requires result review.

## Workflow

### 1. Resolve the input and task root

Identify which input mode applies.

**Already converted**

- Locate one primary paper Markdown file and its sibling `images/`.
- Exclude generated files such as `instruction.md`, `brief_analysis.md`,
  `ANALYSIS.md`, and plans when identifying the paper.
- If several plausible paper Markdown files exist, ask the user which is
  primary.

**Local PDF**

1. Read the UniParser skill named above.
2. Use `skills/UniParser-Paper-Markdown/scripts/parse_paper.py` with
   `--file-path`.
3. Never use `--overwrite` on a directory containing the source PDF.
4. If the desired task root does not exist:
   - parse into that new directory with `--output-dir`;
   - after successful parsing, copy the PDF into the task root.
5. If the PDF is already inside an existing task root:
   - parse into a new sibling staging directory;
   - verify the generated Markdown and image links;
   - merge the generated Markdown, `images/`, and parser metadata into the task
     root without replacing collisions silently;
   - remove the staging directory only after a successful merge.
6. On `Token is duplicated` or an interrupted job, use the UniParser
   `fetch_by_token.py` recovery flow instead of resubmitting.

For a public PDF URL, use the UniParser `--pdf-url` flow, then save the
downloaded/source PDF in the task root when it is available.

### 2. Validate the paper package

- Confirm the primary Markdown and `images/` are siblings. If a source PDF is
  supplied, confirm it is their sibling as well.
- Check every Markdown image link resolves to a real file under the task root.
- Inspect unlinked supplied images using captions, figure numbers, filenames,
  and image content. Insert missing links at the matching caption without
  rewriting the paper body.
- Preserve UniParser filenames unless renaming is necessary and all links can be
  updated safely.
- Read the paper together with its figures, captions, equations, methods, and
  supplementary details.

### 3. Select reproduction targets

- Follow figure or panel targets explicitly named by the user.
- Otherwise rank panels by numerical-simulation reproducibility:
  1. direct field, spectrum, mode, force, transport, or derived-quantity output;
  2. adequate geometry, materials, source, boundary, and solver information;
  3. a clear visual or numerical reference for validation.
- Distinguish direct simulation targets from experimental statistics,
  fabrication images, instrument artifacts, or panels requiring unavailable
  measurement data.
- If several materially different target sets remain, present the recommended
  set and ask the user to choose before writing `instruction.md`.
- Do not claim an experimental panel is directly reproducible unless the
  instruction also specifies the required measurement or instrument model.
- After the reproduction targets are fixed, inspect other figures, panels, and
  supplementary schematics for information that can clarify those targets.
  Pay particular attention to experimental setup diagrams, optical paths,
  sample orientation, illumination/collection geometry, polarization, ports,
  detector placement, calibration, and normalization. Treat these figures as
  supporting evidence rather than additional reproduction targets.

### 4. Extract reproducibility facts

For each selected target, inspect related non-target figures and experimental
setup schematics before completing the evidence table. Extract any information
that constrains the source, polarization, incidence angle, collection geometry,
sample orientation, ports, monitors, detector response, reference measurement,
or normalization. Record the exact source figure/panel and do not infer details
that are not shown.

Build a working evidence table before drafting. For each value, record the
paper location (page, section, equation, caption, table, or supplement):

- article title, authors, DOI, and source filename;
- target figure and panel identifiers;
- geometry, dimensions, coordinate system, and parameter sweeps;
- material models, dispersion, loss, and temperature where relevant;
- sources, wavelengths/frequencies, polarization, phase, amplitude, and ports;
- dimensionality, domain, boundaries, mesh/basis settings, convergence criteria,
  monitors/probes, and exported quantities;
- equations used for post-processing and expected limiting cases;
- explicit target values, axis ranges, symmetries, signs, peaks, and tolerances.

Never invent a missing value. Mark it as unspecified, define a justified
assumption separately, cite the basis for that assumption, and require a
sensitivity or convergence check when it can affect the target.

### 5. Choose the simulation engine

Choose a solver from the paper's method and target physics, not from the sample
instruction's software:

- prefer the paper's reported solver when it is known and automatable;
- otherwise consult [`preferred-simulators.md`](preferred-simulators.md) and
  prefer a listed tool that satisfies the current task;
- otherwise choose a technically suitable method such as FDTD, FEM, RCWA, BEM,
  PWE, GME, eigenmode, circuit, particle, or multiphysics simulation;
- consider `legume-gme-workflow` when the target is a periodic 2D/slab
  eigenproblem, perturbative radiative Q, symmetry-resolved mode, or supported
  exciton-polariton calculation. Reject it for driven broadband scattering,
  time dynamics, RCWA, or general dispersive/lossy materials;
- consider `s4-rcwa-workflow` and `solver-s4-rcwa` when the target is a
  Cartesian stratified stack, grating, or metasurface with zero, one, or two
  in-plane periodic directions and steady-state scattering, diffraction-order,
  field, S-matrix, stress, or energy-integral outputs. Prefer S4 over a general
  FDTD workflow only within the capability boundary documented in
  [`../s4-rcwa-workflow/SKILL.md`](../s4-rcwa-workflow/SKILL.md); reject it for
  PML, transient dynamics, nonlinear media, interior/dipole excitation, finite
  non-periodic 3D devices, or coupled multiphysics;
- permit open-source and commercial tools;
- require a maintained library, official API, scripting interface, or batch
  automation interface. A GUI-only manual workflow is insufficient;
- when two or more tools satisfy the technical requirements, run non-destructive
  availability checks for each before selecting one. Check package import and
  version, executable/API discovery, and license or service access when these
  can be queried safely; do not install software, activate a license, or submit
  a paid/cloud simulation merely to probe availability;
- record the availability evidence and choose from the usable candidates. If no
  candidate is usable, or access requires user action, report it and ask the
  user before fixing the instruction to a tool;
- state the selected software, numerical method, API/library, required version
  or compatibility range, and selection rationale;
- if license or local availability materially changes the implementation, ask
  the user before committing the instruction to one tool.

Do not retain a software name, API, native file extension, or numerical method
merely because it appears in a sample. Keep it only when selected for the
current paper. A tool outside the preferred list is allowed when the instruction
documents why it is a better technical fit and meets the list's admission
criteria.

### 6. Emit the machine-readable contracts

Write `evidence.json`, `targets.json`, and `simulation-contract.json` before the
human-readable instruction:

- Give every extracted parameter a stable `parameter_id`.
- Use exactly one evidence status: `specified`, `literature`,
  `example_suggestion`, `assumption`, or `unknown`.
- Preserve paper locations and retrieved example IDs/versions as provenance.
- Include proposed mesh/PML/run-control convergence cases even if the user may
  later opt out of executing them.
- Keep requested observables in both `objective.observables` and
  `outputs.raw`/`outputs.derived`.
- Record the numerical `method`. For PWE/GME/Hopfield, describe lattice,
  k-space, basis, layers/claddings, and quantum wells as applicable; never
  invent FDTD sources, monitors, or PML merely to satisfy a contract.
- For the registered S4 path, set `method: rcwa` and
  `physics.model_family: rcwa`; describe the Cartesian lattice, ordered layer
  stack, zero-thickness exterior half spaces, analytic regions, supported
  excitation, periodic/invariant transverse boundaries, frequencies, `NumG`,
  Fourier formulation, convergence cases, and approved
  `resources.tool_config`. Never invent PML or time controls for an RCWA
  contract.
- Do not proceed with an unaccepted assumption that changes physical
  interpretation.

Validate all three documents with the V1 schema catalog. Correct the documents
rather than weakening the schema.

### 7. Draft `instruction.md`

Start from [`examples/instruction-template.md`](examples/instruction-template.md),
then adapt the closest paper-specific reference instead of copying it blindly.
Use this structure:

1. `# Physics Paper Figure Reproduction`
2. `## 1. Article Information`
3. `## 2. Core Directives`
4. `## 3. Interactive Workflow`
   - Input and source verification
   - Extraction and hard-logic verification
   - Solver selection and implementation plan
   - API-driven model construction and computation
   - Plotting from exported data
   - Data generation
   - Anti-cheat and consistency audit
   - Documentation
5. `## 4. Coding Guidelines`
6. `## 5. Data Files to Reproduce`
7. `## 6. Banned Practices`
8. `## 7. Validation Requirements`
9. `## 8. Deliverables`

Tailor every section to the current paper. Remove placeholders and stale terms.

#### Mandatory simulation language

The generated instruction must require all of the following:

- Programmatically create the paper's method-appropriate geometry, materials,
  excitation or eigenproblem, boundaries/periodicity, mesh or basis, outputs,
  and parameter sweeps inside the chosen simulator through its API.
- Run the simulator's actual numerical solver through that API.
- Export raw or minimally processed solver results before plotting.
- Derive final CSV data and PNG figures from those exported simulation results.
- Save a native simulator project/model for every target panel using the
  simulator's real extension. If a library-only solver has no project format,
  save its complete executable model/configuration plus native raw result files.
- Make every final artifact traceable to the model, solver run, and post-process
  that produced it.

Analytical formulas may define geometry or excitation, implement paper-specified
post-processing, predict limiting cases, and validate results. They must not
directly construct the final field, spectrum, image, CSV, or target answer in
place of running the simulator.

#### Required implementation separation

- Put automation and post-processing code under `reproduction/`.
- Require `reproduction/plan.md` to document evidence, solver choice,
  pseudocode, assumptions, and convergence strategy before coding.
- Separate simulation/compute code from plotting code.
- Simulation/compute code builds and runs the model through the simulator API
  and exports tabular plotting data. It must not render final figures.
- Plot code reads only exported simulation-derived data and renders figures. It
  must not recreate target data analytically.

#### Required per-panel artifacts

Use a stable basename such as `fig2_b` for each requested panel and require:

- `data/<basename>.<native-model-extension>` or the documented library-only
  model/configuration equivalent;
- `data/<basename>.csv`;
- `data/<basename>.png`.

Additional native raw data such as HDF5, VTK, MAT, or solver result databases may
also be required. Keep final artifacts directly under `data/` unless the user
requests another layout.

### 8. Define validation honestly

- Use a numerical error threshold only when the paper or supplied target data
  supports it.
- Otherwise require non-triviality, physical plausibility, convergence, and
  panel-specific visual/numerical checks.
- Require mesh/basis/time-step/domain convergence appropriate to the solver.
- Define checks for conservation laws, reciprocity, symmetry, limiting cases,
  units, normalization, sign conventions, peaks, and axis ranges where relevant.
- Document acceptable transformations such as normalization or physically
  equivalent rotations; do not silently excuse mismatches.
- On mismatch, require checking evidence, units, material models, geometry,
  boundaries, discretization, source definitions, and post-processing, then
  rerunning the simulation.

## Anti-Cheat Rules

The final instruction must explicitly ban:

- hardcoded target arrays, traced images, digitized values presented as computed
  results, or precomputed answers embedded in code;
- analytical, synthetic, or surrogate fields used as final simulation output;
- plotting directly from formulas when the requested result is a simulation
  observable;
- manually constructing the answer outside the simulator while claiming it came
  from the simulator;
- opening a supplied project and exporting its results instead of
  programmatically constructing the paper's model through the simulator API;
- using a nominal API call that does not build and solve the required structure.

Digitized paper data may be used only as validation ground truth and must be
labeled separately from simulated output.

## Final Quality Gate

Before finishing:

- confirm `instruction.md` is in the task root and names the real paper file;
- confirm `evidence.json`, `targets.json`, and `simulation-contract.json` exist
  and pass their V1 schemas;
- confirm the instruction and JSON documents contain no conflicting parameter,
  target, assumption, or validation values;
- verify every target panel appears consistently in workflow, filenames,
  validation, and deliverables;
- search for stale titles, figures, physics, software, API names, and extensions
  inherited from examples;
- confirm the solver and API match the current paper and are not hard-wired to
  any tool without a technical reason;
- confirm software-internal model construction, actual solver execution, and
  simulation-result traceability are explicit;
- confirm native model/configuration, CSV, and PNG deliverables exist in the
  specification for every target;
- confirm assumptions and missing parameters are visible and not presented as
  paper facts;
- confirm relevant non-target figures and experimental setup schematics were
  checked for supporting information;
- verify useful setup-derived parameters cite their source figure/panel in
  Evidence or SimulationContract, and no schematic detail was silently treated
  as a paper-specified numerical value;
- confirm the analytical-bypass and hardcoding bans remain explicit;
- confirm all Markdown image and reference links resolve.
