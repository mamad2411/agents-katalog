---
name: action-server
description: Use when authoring or debugging ACTIONS packages, package.yaml, actions-core, actions-runtime, MCP, secrets, tests, or Docker/Compose builds and deployments.
---

# Action Server

Use this skill for ACTIONS package authoring, debugging, and container deployment. The owning source is `joshyorko/actions`; the runtime and action library are `actions-runtime` and `actions-core` on PyPI.

## Scope

- Build or repair action packages using `package.yaml` spec-version v2.
- Work with `actions-core`, `actions-runtime`, `actions.mcp`, typed responses, `Secret`, `OAuth2Secret`, tests, lint dev tasks, OpenAPI, and local MCP endpoint validation.
- Build and run existing Action Server packages in Docker/Compose. Read `references/container-deployment.md` for the pinned community runtime, reusable starter, datadir lifecycle, browser dependencies, and runtime smoke checks. Match the runtime's action library before selecting an image.
- Use `actions-work-items` only when the action package itself needs producer/consumer work item behavior; switch to `$rcc-workitems` for adapter-heavy queue design.
- If an action package uses `actions-work-items` with Redis, DocumentDB, retry/outbox, or cross-job queues, read the RCC work-items adapter references before changing action code.

## Non-Goals

- Do not prototype an plugins marketplace server.
- Do not implement a new MCP server, Action Server runtime, daemon, web service, or marketplace product in this repo. Containerizing an existing Action Server for action packages is in scope.
- Do not make plugin distribution sound hosted; this skill is for ordinary Action Server action packages.

## First Inspection

1. Locate `package.yaml`, action modules such as `my_actions.py`, `src/**`, `tests/**`, and `.action-server/` or datadir settings if present.
2. Inspect dependencies, `pythonpath`, `dev-dependencies`, and `dev-tasks` before changing action code.
3. Check secrets and typed inputs/outputs before writing sample payloads.
4. Validate local endpoints only when Action Server is installed and intended for the project.
5. For container work, inspect the existing Dockerfile, Compose config, runtime release, action-library imports, datadir mounts, and browser/system dependencies before adapting the bundled starter.
6. Import the action API from `actions` and MCP decorators from `actions.mcp`. Name action files `my_actions.py` or another nonconflicting name. A top-level `actions.py` or `actions/` directory shadows the installed `actions-core` package.

## References

- `references/action-server-recipes.md`: package v2 patterns, actions, MCP decorators, secrets, dev tasks, endpoint validation, and work-item-in-actions examples.
- `references/container-deployment.md`: complete Linux container build/run guide, source evidence, compatibility choices, updates, and troubleshooting.
- `assets/container/`: runnable Docker/Compose starter with a harmless action, non-root runtime, runtime secret, and persistent datadir.
- `scripts/smoke-container.py`: opt-in Docker build, authenticated action/MCP checks, recreation persistence, and image-update regression. Run with `python3`; uses only the host standard library.
- `../rcc/references/python-library-audit.md`: cross-source Python library map, action/MCP example gaps, and source refresh workflow.
- `../rcc-workitems/references/workitems-adapters.md`: queue/adapters details when action packages use `actions-work-items`.
- `../rcc-workitems/references/docdb-rpa-patterns.md`: DocDB queue/outbox/retry patterns to reuse only when an action package has real durable work-item semantics.
- `../rcc-robots/references/troubleshooting-validation.md`: shared failure triage and validation commands.
- `assets/container/package.yaml`: pinned ACTIONS package v2 starter.
- `../rcc/references/source-map.md`: repository source evidence; use the container reference for current PyPI runtime pins.
