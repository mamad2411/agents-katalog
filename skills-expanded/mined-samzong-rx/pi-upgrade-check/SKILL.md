---
name: pi-upgrade-check
description: Review whether rx-agent should move its pinned pi packages and return a stay-or-upgrade decision with the affected surfaces. Use for the periodic dependency check of agent/ (the @earendil-works/pi-* set and the ACP SDK pin).
---

# pi-upgrade-check

Judge whether rx-agent should move its pinned pi packages. This review is
read-only: it reports a decision and the surfaces an upgrade would touch. It
does not edit package.json or the lockfile, and it does not perform the
upgrade.

## Gather the signals

Run these in `agent/`:

1. `pnpm outdated` for current vs latest versions of `@earendil-works/*` and
   `@agentclientprotocol/sdk`.
2. `pnpm audit` for the dependency chain.
3. Changelog coverage is uneven. `pi-coding-agent` and `pi-mcp` ship a
   `CHANGELOG.md` in the npm package; `pi-ai` and `pi-agent-core` do not. For
   those two, read the release notes in the pi monorepo at
   https://github.com/earendil-works/pi.

## Decide

pi releases weekly, and most changes (TUI, codemode, summaries, terminal
fixes) never reach rx-agent's runtime path. Recommend an upgrade only when at
least one of these is true:

- An audit finding affects the pi dependency chain.
- A changelog entry changes the slice rx-agent consumes: the pi-agent-core
  `Agent` loop, pi-ai `Models`/streaming/fetch hook/thinking levels/model
  catalog, or pi-coding-agent `loadSkills`/`formatSkillsForPrompt`.
- The pi-ai model catalog changed for a provider rx-agent actually ships.
- Rx wants a new pi capability, for example pi-mcp for MCP support or
  pi-telemetry for evals.

Otherwise recommend staying on the current pins.

## Constraints

- All `@earendil-works/pi-*` packages are cross-pinned to one version and move
  together. Never propose upgrading a single pi package.
- Replacing pi-agent-core or pi-ai (a behavior change to the agent loop or
  model layer) requires eval evidence and an owner decision per
  `agent/DESIGN.md` RX-CORE-001. A routine minor bump does not.
- When an upgrade looks warranted, read
  [references/upgrade-surfaces.md](references/upgrade-surfaces.md) for the
  blast-radius checklist and verification loop before finalizing the report.

## Report

Return: stay or upgrade; the target version when upgrading; the trigger that
justifies it; and the affected surfaces from the reference. Name the checks an
approved upgrade must pass, not the commands to run them.
