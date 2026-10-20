---
name: selemene-orchestrator
description: "Route Selemene Engine tasks to the right surface: deterministic reports (birth/compatibility/transit) via selemene-core and the @selemene/bridge CLI, or narrative witness readings via selemene-report. USE WHEN the user wants anything under the Selemene/Noesis umbrella but has not named the exact surface."
origin: project
cluster: selemene
version: 1.0.0
---

# Selemene Orchestrator

Hub for the Selemene cluster. Use this when the user mentions Selemene, Noesis, birth chart, compatibility, transit, or witness reading without specifying a tool or surface.

## Routing matrix

| User intent | Route to |
|-------------|----------|
| Generate any Selemene report or reading | `selemene-report` |
| Understand which surface to use | `selemene-core` |
| Build/modify a Rust engine or report generator | `rust-orchestrator` |
| Build/modify the bridge CLI or its generators | `createcli` or direct repo work |
| Build/modify the web intake app | `frontend-web-orchestrator` or `astro-orchestrator` |
| Render PDF/DOCX from a generated report | `documents-orchestrator` |

## Rules

- Prefer `selemene-report` for end-user report requests.
- Read `selemene-core` before making cross-surface decisions.
- Never route to a deferred cluster without first running `node ~/.agents/skill-clusters/scripts/tier.mjs --activate <cluster> --apply`.
