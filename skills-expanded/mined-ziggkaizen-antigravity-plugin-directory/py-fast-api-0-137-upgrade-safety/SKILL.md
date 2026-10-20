---
name: py-fast-api-0-137-upgrade-safety
description: Audits FastAPI upgrades to 0.137.x and detects router internals that may break because APIRouter and APIRoute preservation changed. Use when upgrading FastAPI, reviewing router composition, or checking direct router.routes usage.
license: MIT
---

# FastAPI 0.137.x Upgrade Safety Skill

Use this skill when a repository upgrades to FastAPI `0.137.x` or when route registration internals are being modified.

## Why This Skill Exists

FastAPI `0.137.0` changed internal router preservation behavior. Code that expected `router.routes` to be a plain list of `APIRoute` objects can break or silently miss routes.

## When to Use

- Upgrading from any earlier FastAPI minor line to `0.137.x`.
- Reviewing code that iterates, mutates, copies, or filters `router.routes`.
- Debugging missing routes, duplicate routes, or route inclusion order.
- Reviewing custom `APIRouter` or `APIRoute` logic.

## How to Work

1. Read `resources/0-137-router-compatibility.md`.
2. Run scripts with `--help` before using them:
   - `scripts/detect-router-routes.py --help`
   - `scripts/guard-dangerous-fastapi-command.py --help`
3. Scan the repository for direct `router.routes` and `app.routes` assumptions.
4. Review each result manually. Some `app.routes` usage in tests or docs generation may be acceptable, but route registration logic should not depend on internals.
5. Prefer public FastAPI routing APIs and behavior-level tests over internal route list manipulation.
6. Run focused tests around router inclusion, OpenAPI generation, auth dependencies, and route availability.

## Workflow

Use `workflows/upgrade-to-0-137-workflow.md` for upgrade or compatibility audit tasks.
