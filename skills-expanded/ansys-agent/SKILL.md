---
name: ansys-agent
description: "Automate ANSYS simulation workflows through doc-driven execution: discover installed ANSYS products and licenses, retrieve official/local API documentation, generate Workbench scripts, Mechanical APDL, PyMAPDL/PyAnsys code, or solver command files, run or guide simulations, diagnose blockers, and search trusted ANSYS forums when needed. Use when Codex is asked to create, modify, run, debug, or explain ANSYS Mechanical, MAPDL, Fluent, Electronics, Workbench, meshing, solving, post-processing, or result export tasks."
---

# ANSYS Agent

## Overview

Use this skill to convert ANSYS simulation requests into reproducible scripts, solver inputs, output files, and validation notes. Prefer documented ANSYS command-line, scripting, and PyAnsys APIs over manual UI workflows.

## Workflow

1. Frame the simulation: identify product family, physics, geometry, materials, mesh, loads, boundary conditions, solver, outputs, and validation criteria.
2. Discover access: check Workbench, MAPDL, Fluent, Electronics, PyAnsys packages, licenses, and command-line executables.
3. Retrieve docs first: use local/official command references, API docs, and examples before generating APDL, Python, journal, or Workbench scripts.
4. Generate reproducible automation: create scripts or solver input files that can rebuild and rerun the analysis.
5. Run or guide execution: run command-line/Python workflows when available; otherwise provide exact UI steps for unavoidable UI-only tasks.
6. Diagnose and unblock: use `references/blocker-remediation.md` for license checkout, missing products, solver errors, mesh failures, and environment issues.
7. Search forums when needed: use `references/community-troubleshooting.md` after official docs and local diagnostics are insufficient.
8. Report artifacts: list scripts, project files, solver logs, result exports, plots, and assumptions.

## Resources

- `references/software-notes.md`: ANSYS-specific automation surfaces and artifacts.
- `references/blocker-remediation.md`: legitimate ways to resolve license, solver, module, and environment blockers.
- `references/community-troubleshooting.md`: trusted forum search process.

Never bypass license checks or suppress solver warnings. Treat engineering simulation outputs as unvalidated until the solver log, mesh quality, units, and expected behavior are reviewed.
