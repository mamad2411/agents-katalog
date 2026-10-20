---
description: Project guidance for AI agents working on the Mythos Factorio mod
alwaysApply: true
---

# Mythos Project Guidance

Mythos is a Factorio 2.0 Lua mod for pocket dimensions. Before changing runtime
code, read `ARCHITECTURE.md`; it is the maintainer map for entry points,
packages, persisted names, and manual smoke tests.

## Runtime Map

- `control.lua` should stay thin: lifecycle hooks plus event registration.
- Runtime packages live under `script/bootstrap`, `script/events`,
  `script/mythos`, `script/pocket_dimension`, `script/clone`,
  `script/virtual_chest`, `script/power`, `script/migrations`, and `script/ui`.
- Runtime code should require package paths directly, such as
  `script.mythos.init`, `script.pocket_dimension.init`, and
  `script.ui.remote_view`.

## Save Compatibility

This is a first prototype and targets clean new saves. Do not add migrations or
old-save compatibility for normal changes unless the user explicitly asks for
that work. If a change may break existing saves, tell the user they may need to
start a new save with no placed Mythoses to avoid migration or load errors.
Keep current storage keys, surface names, prototype names, setting names, custom
input names, and blueprint tag names stable during normal feature work.

Virtual chest legacy migration support was intentionally removed. Do not
reintroduce `mythos-inventory`, old virtual chest storage-key migrations, or old
floor-tile migrations unless the user explicitly asks for old-save support.

## Refactor Rules

- Prefer focused modules and facades over re-growing monolithic files.
- Avoid `goto` patterns; use structured conditionals to stay Lua-load safe.
- Keep Factorio API behavior stable unless the user explicitly asks for gameplay
  changes.
- When changing clone, blueprint, power, migrations, or virtual chest code, treat
  it as high-risk and review storage and save/load behavior carefully.

## Verification

This repo has lightweight automated checks for pure Lua helpers and source
regressions. Prefer focused tests for deterministic logic and avoid trying to
simulate the Factorio engine in unit tests. Keep verification to checks that fit
the current prototype, such as `lua tests/run.lua`,
`git diff --check`, focused searches, and IDE diagnostics. Do not require
Factorio load checks for normal work; if Factorio is unavailable, do not treat
that as a verification gap. Use manual Factorio smoke checks only when Factorio
is already available or the user explicitly asks for in-game verification. Use
the smoke-test matrix in `ARCHITECTURE.md` only as a manual checklist for
gameplay-sensitive changes.
