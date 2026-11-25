---
name: openfoam-agent
description: Prepare, run, debug, and postprocess OpenFOAM CFD cases using the installed distribution's documentation and tutorials. Use for case dictionaries, solver selection, meshing, boundary conditions, parameter studies, residual interpretation, and field exports. Check distribution compatibility and native execution before claiming a CFD result.
---

# OpenFOAM Agent

Build the case for the OpenFOAM installation that will actually run it.

## Identify the installation and physics

Read the existing case and requested result. Identify geometry scale, fluid properties, incompressible or compressible treatment, steady or transient behavior, turbulence model, boundary conditions, reference quantities and required outputs. Preserve the original case and run trials in a separate directory.

Identify the distribution, release, active environment and available applications. Foundation releases and the openfoam.com distribution do not have interchangeable solver names or dictionaries. A sourced environment or a source-code directory does not prove that a selected solver binary or module is available.

Use [references/automation.md](references/automation.md). Start from a relevant tutorial shipped with the installed distribution, inspect its run script before executing it, and use matching help/source for all changed entries. Do not mix tutorials from different releases to make missing keywords disappear.

## Prepare the case

Choose the physical model before choosing an application. Check the actual application or module selection used by the installed tutorial and its executable path. If the requested transient solver is missing, report that blocker; do not silently run a steady solver and label it transient.

Record case provenance and parameter changes. Check dimensional units, patch names, field dimensions, initial conditions, numerical schemes, solution controls and any referenced libraries. Treat initial or restart time directories according to the selected workflow rather than requiring `0/` in every case.

Generate or import the mesh using documented utilities. Run the applicable mesh checks and inspect their findings before solving. A generated mesh file is not proof of suitable mesh quality. Explain exceptions that matter to the requested model.

## Run within a useful budget

Run a short representative case before a costly sweep when runtime behavior is uncertain. Keep preprocessing, solving and postprocessing logs separate and preserve each process exit status. Confirm parallel prerequisites before decomposing or launching MPI; do not default to running as root or changing cluster policies.

Track the requested final time or stopping criterion, written fields and termination state. Solver-log residuals are useful evidence but are not sufficient on their own to establish the requested physical result. Follow [references/validation.md](references/validation.md).

Make targeted changes based on the first supported error. Preserve before/after dictionaries and the change reason. Stop repeated failures at a task-appropriate budget and report the remaining blocker rather than replacing solver outputs with heuristic numbers.

## Export actual results

Extract the requested quantities from the solved fields at identified times and locations using documented function objects or postprocessing tools. Include units, reference values, averaging windows and normalization conventions. Distinguish input-derived estimates from field-derived results.

Deliver the replayable case, commands, logs, source tutorial/release, parameter record and exported quantities. If the runtime or selected solver is missing, deliver an unexecuted case/workflow and the missing dependency. Do not claim CFD validation from file generation or a generic script check.

See [references/example.md](references/example.md) for a small case and its acceptance evidence.
