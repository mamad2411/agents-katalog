---
name: moe-dev
description: >-
  Use when planning, implementing, or reviewing any feature or change to the
  Moe project itself — enforces integration-completeness and multi-harness
  awareness as non-negotiable development constraints
---

# Developing for Moe

Two tenets govern every piece of work on this project. They are not
guidelines — they are acceptance criteria. Work that violates either is
incomplete.

## Tenet 1 — Integration is part of the feature

A feature is not done if it is not integrated with the project.

**Every plan must include integration steps.** A plan that ends at "the code
works in isolation" is a partial plan. Integration means:

- The feature is reachable from an existing entry point (a hook, a skill
  trigger, a CLI command, a consumer import).
- Registration is updated: the skill registry for skills, `hooks.json` for
  hooks, `package.json` exports for library code, mint yaml for plugin
  surfaces.
- Tests that guard the registration surface pass (`pnpm check`).
- If the feature ships in a plugin, `pnpm mint` produces the correct output
  and `pnpm mint:check` is clean.

A branch that adds a file but does not wire it into the project has not
delivered a feature. It has delivered a file.

## Tenet 2 — Multi-harness by default

No matter which harness you are running under, you are developing a project
that ships to eight harnesses: claude-code, codex, cursor, kimi, opencode,
pi, agent-plugins-1.0, and copilot.

**Planning, exploration, and research must account for this at all times.**

- A design that relies on a harness-specific capability (Claude Code's
  `CLAUDE_PLUGIN_ROOT`, Cursor's `CURSOR_PLUGIN_ROOT`, Codex's agent
  dispatch) must document the equivalent path for the others, or explain why
  the feature is harness-scoped.
- Hook output must use the harness-aware JSON envelope (see existing hooks
  for the pattern: Claude Code's `hookSpecificOutput`, Cursor's
  `additional_context`, the generic fallback).
- Mint yaml is the packaging surface. A feature that works only because you
  are running from a git clone and can see `./packages/` is not portable.
- When evaluating an approach, ask: "does this work for the seven harnesses
  I am not running under right now?" If the answer is no, redesign before
  building.

## Applying the tenets

When you write a plan, include a section called **Integration** that lists
every registration, wiring, and cross-harness consideration the feature
requires. When you review a plan, check for that section first.

When you implement, treat the integration steps as blocking — not follow-up
work. The branch is not ready for review until integration is done and
`pnpm check` and `pnpm mint:check` pass.

When you review code, check that the feature is reachable from outside its
own file, and that harness-specific assumptions are either absent or
explicitly scoped.
