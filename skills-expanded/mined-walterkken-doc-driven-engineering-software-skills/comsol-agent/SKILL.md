---
name: comsol-agent
description: "Automate COMSOL Multiphysics modeling and simulation tasks through doc-driven workflows: discover installed COMSOL access, retrieve official/local API documentation, generate Java/MATLAB/COMSOL batch scripts, run or guide simulations, diagnose blockers, and search trusted COMSOL forums when needed. Use when Codex is asked to create, modify, run, debug, or explain COMSOL models, MPH files, LiveLink workflows, parametric sweeps, geometry/material/physics setup, meshing, solving, or result export."
---

# COMSOL Agent

## Overview

Use this skill to turn a COMSOL modeling request into reproducible scripts, model files, exports, and validation notes. Prefer documented COMSOL APIs and batch execution over manual UI instructions.

## Workflow

1. Frame the model: identify physics interface, geometry, materials, boundary conditions, mesh, study type, parameters, outputs, and validation criteria.
2. Discover access: check whether COMSOL Desktop, `comsolbatch`, COMSOL Server, or LiveLink for MATLAB is available.
3. Retrieve docs first: use COMSOL API/help/manuals available to the user before generating Java, MATLAB LiveLink, or batch commands.
4. Generate reproducible automation: create scripts that build or modify the model, run studies, and export plots/tables.
5. Run or guide execution: execute command-line workflows when available; otherwise give exact COMSOL Desktop steps only for UI-only gaps.
6. Diagnose and unblock: use `references/blocker-remediation.md` for licenses, missing modules, API access, and solver failures.
7. Search forums when needed: use `references/community-troubleshooting.md` after official docs and local errors are insufficient.
8. Report artifacts: list scripts, `.mph` files, result tables, figures, solver logs, and assumptions.

## Resources

- `references/software-notes.md`: COMSOL-specific automation surfaces and artifacts.
- `references/blocker-remediation.md`: legitimate ways to resolve access, module, solver, and export blockers.
- `references/community-troubleshooting.md`: trusted forum search process.

Never bypass COMSOL licensing or module restrictions. If a required physics interface or solver is unavailable, report the module/license blocker and the smallest user action needed.
