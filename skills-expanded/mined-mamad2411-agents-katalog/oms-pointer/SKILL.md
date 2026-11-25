---
name: oms-pointer
description: Use after `oms commit` or `oms pull` moves a submodule's working commit, to record the moved root gitlink pointer with `oms record`. Covers the cross-command commit-or-pull-then-record loop so a submodule source change is not left without a recorded root pointer, and the root pointer is not committed by mistake.
metadata:
  author: oh-my-space
  version: "1.1.0"
---

# Record the root pointer after a submodule commit moves

When a submodule's working commit moves — because you ran `oms commit` to commit source changes, or `oms pull` fast-forwarded its branch — the root repository's gitlink still points at the old commit until you record the new one. Recording is a separate, explicit step.

## Scope guardrail (applies before any Git work)

- Run `oms status --json` before Git work involving `oms/` to read root versus submodule state.
- Treat each `oms/<alias>/` directory as a separate Git repository.
- Use `oms` commands for scoped submodule workflows; do not guess root repository versus submodule Git scope.
- Do not create root commits for existing submodule pointer updates unless the user explicitly runs `oms record <alias>`.

## Commit source, then record the pointer

1. Commit the submodule's source changes with `oms commit <alias> -m "<message>"`. The `-m` flag is required to create the commit. This commits inside `oms/<alias>/` only, never the root gitlink.
2. Record the moved root pointer afterward with `oms record <alias>`. This is the only step that writes a root commit for the pointer move.

## A pull that fast-forwards also moves the pointer

`oms pull <alias>` fast-forwards the submodule branch and moves its working commit, so it moves the root pointer the same way a commit does. Record it with `oms record <alias>` afterward, exactly as after `oms commit`.

## Several moved pointers at once

A wide pull or push (`oms pull --all`, `oms push --all`) can move several root pointers in one run, and the command then hints `oms record --all` instead of one hint per alias. Record them together with `oms record --all` (or name them: `oms record <alias> <alias>`); they land in one root commit. With `--all`, an alias that cannot be recorded is reported and skipped while the rest are still recorded, and the command exits non-zero — read the skipped reasons rather than assuming everything was recorded.

## Do not commit the root pointer by mistake

Do not stage and commit the root gitlink yourself to capture a pointer move — that is what `oms record <alias>` is for, and doing it by hand is the mistake this workflow exists to prevent. Run `oms status --json` to confirm whether a pointer is unrecorded before and after.

These instructions were written against `oms status --json` schemaVersion 1. If `oms status --json` reports a different schemaVersion, defer to `oms status --help` for exact field semantics. Defer remaining flag detail to `oms commit --help`, `oms pull --help`, and `oms record --help`.
