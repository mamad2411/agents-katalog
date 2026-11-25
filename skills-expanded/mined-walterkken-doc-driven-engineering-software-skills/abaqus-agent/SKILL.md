---
name: abaqus-agent
description: Build, modify, run, and inspect Abaqus models and jobs using documentation matched to the installed release. Use for CAE scripting, INP generation, parameter studies, ODB extraction, Python-runtime mismatches, and failed Abaqus analyses. Separate script generation, solver completion, and engineering validation.
---

# Abaqus Agent

Turn a modeling request into a replayable job and results that can be traced back to it.

## Establish the model and runtime

Identify the requested response quantity, unit system, analysis procedure, geometry, material law, loads, constraints, contact, and relevant operating conditions. Read an existing model before replacing its setup. Preserve it and use a new job name for trial runs.

Check the installed Abaqus release, launcher, embedded Python version, available solver, and access to the required license. Host Python and Abaqus Python are separate environments. An importable type-hint or wrapper package does not establish that the Abaqus kernel can execute a model.

Use the installed Scripting Reference, Scripting User's Guide, Keywords Guide, and execution documentation. Read the section for the chosen API and release before writing calls. Use [references/automation.md](references/automation.md) for runtime selection. If official web help requires authentication, use accessible local help; do not fill gaps with invented API names.

## Prepare a reproducible job

Choose the smallest suitable entry: CAE script for model construction, an input deck for an existing validated mesh, or an ODB script for postprocessing. Keep solver-side code compatible with its actual interpreter; run modern data analysis separately if needed.

Record assumptions and parameters outside the script's execution logic. Check that referenced sets and surfaces exist and contain the expected mesh entities, sections are assigned, and loads act on the intended regions. A geometric set is not proof of an element set ready for solving. Retain consistency checks unless a documented, task-specific reason requires a change.

Create only the model complexity needed to support the requested result. Use a small sample or a documented data check before an expensive parameter sweep. Do not silently replace contact, nonlinear material, or a transient procedure with an easier model just to obtain a successful run.

## Run and read the evidence

Use documented native launch commands for the detected version and operating system. Log the exact invocation, job name, model revision, and working directory. Set a run budget appropriate to the user request; do not repeatedly submit the same failing expensive job.

Check the job status and its current log/status/message files. The presence of an ODB, a zero launcher exit code, or a completed Python script alone does not establish that the requested analysis finished. Check the expected step and final frame or time against the requested run. Keep partial results labeled as partial.

Use [references/validation.md](references/validation.md) to separate runtime failures from model failures. Fix the first supported cause, then rerun the affected check. Do not suppress warnings to make a report look clean.

## Deliver

Return the model or input deck, replay script, exact run instructions, logs, exported quantities with units, and a short record of what was actually checked. Identify output position and region when reporting stress; integration-point, extrapolated nodal, and averaged values are not interchangeable.

When no native Abaqus runtime is available, complete the script or workflow as far as documentation allows, mark it unexecuted, and state the missing runtime or evidence. Do not claim CAE, ODB, or solver verification from a generic Python syntax check.

For a small first-run task, see [references/example.md](references/example.md).
