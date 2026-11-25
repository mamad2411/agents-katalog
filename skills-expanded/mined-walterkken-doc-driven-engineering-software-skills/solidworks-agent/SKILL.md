---
name: solidworks-agent
description: "Automate SOLIDWORKS modeling, assembly, drawing, and export workflows through doc-driven execution: discover installed SOLIDWORKS/API access, retrieve official/local API documentation, generate VBA/API macro or COM automation guidance, diagnose blockers, and search trusted SOLIDWORKS forums when needed. Use when Codex is asked to create, modify, batch process, debug, or explain SOLIDWORKS parts, assemblies, drawings, features, configurations, equations, mates, BOMs, exports, or CAD automation."
---

# SOLIDWORKS Agent

## Overview

Use this skill to convert SOLIDWORKS CAD requests into reproducible macro/API workflows, generated files, exports, and validation notes. Prefer documented SOLIDWORKS API and macro workflows over manual clicking.

## Workflow

1. Frame the CAD task: identify part/assembly/drawing target, dimensions, units, features, configurations, mates, materials, exports, and validation criteria.
2. Discover access: check operating system, SOLIDWORKS installation, API help, macro recorder, COM access, and Document Manager availability.
3. Retrieve docs first: use official/local SOLIDWORKS API help, object model docs, macro examples, and error messages before generating code.
4. Generate reproducible automation: create VBA macros, API pseudocode, or COM automation guidance that can be rerun.
5. Run or guide execution: execute only when SOLIDWORKS/API access is available; otherwise provide exact macro import/run steps.
6. Diagnose and unblock: use `references/blocker-remediation.md` for Windows-only access, missing APIs, macro security, file locks, add-ins, and license issues.
7. Search forums when needed: use `references/community-troubleshooting.md` after official docs and local diagnostics are insufficient.
8. Report artifacts: list macros, generated parts/assemblies/drawings, exports, screenshots, logs, and assumptions.

## Resources

- `references/software-notes.md`: SOLIDWORKS-specific automation surfaces and artifacts.
- `references/blocker-remediation.md`: legitimate ways to resolve installation, platform, macro security, add-in, API, and license blockers.
- `references/community-troubleshooting.md`: trusted forum search process.

Never overwrite original CAD files without making a copy. Treat SOLIDWORKS automation as Windows/API dependent unless the user's environment proves otherwise.
