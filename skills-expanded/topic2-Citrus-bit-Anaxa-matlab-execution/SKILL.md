---
name: matlab-execution
description: Use when the user explicitly needs MATLAB or .m scripts for local scientific computing, simulation, signal processing, image processing, statistics, or experiment reproduction. Prefer command-line MATLAB batch execution and do not imply GUI control.
---

# MATLAB Execution

Use this skill only when MATLAB itself is needed. Prefer Python/R tooling for
normal data analysis unless the user requires MATLAB code, `.mat` files, or a
MATLAB-specific toolbox.

## Capability Boundary

- Supported: command-line MATLAB through `matlab -batch` using the `matlab_execution` tool.
- Supported: reading and writing files in the thread workspace and output folders.
- Not supported by this skill: controlling MATLAB's GUI, clicking menus, or operating desktop windows.
- Host MATLAB execution requires trusted local configuration with host bash explicitly enabled.

## Workflow

1. Generate a complete `.m` script with deterministic inputs and output paths.
2. Save all figures, `.mat`, `.csv`, and logs under the output directory provided by the tool.
3. Call `matlab_execution(script_content=..., script_name=...)`.
4. Inspect the manifest and logs before using results in a report or manuscript.
5. Link any manuscript claim to generated numeric or figure artifacts.

## Safety

- Do not run indefinite GUI sessions.
- Do not assume MATLAB is installed; report the executable error if missing.
- Do not bypass license, filesystem, or sandbox restrictions.
- If MATLAB cannot run, provide a Python or pseudocode fallback only when scientifically appropriate.
