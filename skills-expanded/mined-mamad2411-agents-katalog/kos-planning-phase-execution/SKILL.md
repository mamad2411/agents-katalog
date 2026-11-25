---
name: kos-planning-phase-execution
description: Keep .planning artifacts in sync (gsd-planning) and execute one planned wave (gsd-planning-execute --wave N --no-transition) — validate intake, verify with npm test, include a Proposals-deferred section; do not push/PR.
user-invocable: true
when_to_use: "When refreshing planning artifacts for a phase (gsd-planning) or executing a phase by waves (gsd-planning-execute), or when intake is missing/broken."
category: utilities
argument-hint: "[phase or wave]"
keywords: [planning, phase, wave, execute, intake, no-transition, proposals-deferred, npm-test]
related: [kos-zai-agent-runtime-contract, kos-gh-automation-tooling, kos-zai-run-failure-prevention, kos-claude-turn-budget]
metadata:
  author: kos-workflow-improvement
  attribution: distilled from gsd-planning.yml + gsd-planning-execute.yml prompts + intake scripts
  license: repo
  version: "1.1"
---

# Idea

Two workflows serve `.planning/`:
- **gsd-planning** (`/gsd:plan-phase`) — refresh a phase's planning artifacts; edit only `.planning/**`; preserve intake markers; don't push.
- **gsd-planning-execute** (`/gsd:execute-phase 999 --wave N --no-transition`) — execute exactly the imported wave; `npm test` gate; include a `### Proposals deferred` section; don't push/PR.

Both depend on correct **intake**. Neither pushes/PRs (the workflow handles branch push + PR).

## When to invoke this skill directly
- Refreshing a phase's planning artifacts.
- Executing a phase wave.
- Intake is empty/broken.

## References
- `gsd-planning.yml` (`/gsd:plan-phase`; edit only `.planning/**`; preserve intake markers; keep planning PRs limited to planning artifacts for auto-merge; don't modify app source/manifests/workflow logic; don't push).
- `gsd-planning-execute.yml` (`--wave N --no-transition`; execute only that wave; don't process other waves; don't open/approve/merge/comment PRs; don't push; `npm test` gate; `### Proposals deferred` section).
- `.github/workflows/scripts/collect-gsd-planning-intake.cjs`, `repair-planning-intake.cjs` (workflow steps).
- [[kos-zai-agent-runtime-contract]].

## Communication Style
State phase + wave + intake status, then artifacts refreshed / tasks executed + verification. Explicit no-transition.

## Core Principles
YAGNI / KISS / DRY. Validate intake before acting. Refresh only stale artifacts. Execute one wave, report, stop (`--no-transition` = do not auto-advance).

## gsd-planning contract (enforce)
- Edit only `.planning/**`; preserve existing phase intake markers.
- Update phase tracking status, acceptance criteria, and verification checklist when missing.
- Keep planning PRs limited to planning artifacts (so PR flow can auto-merge after CI + core/security review).
- Do NOT modify app source, package manifests, or workflow logic. Do NOT push.

## gsd-planning-execute contract (enforce)
- Execute only Wave `<wave>` from Phase 999; keep implementation scoped to the imported source artifact; do not process other waves.
- Do NOT open/approve/merge/comment on PRs. **Do NOT push** — the workflow handles branch push + PR.
- Run `npm test` after implementation; **typecheck, unit, lint, and Prettier failures are unfinished work — fix them before reporting completion.**
- If a source-artifact proposal is intentionally left out of scope, include a final `### Proposals deferred` section with one bullet per deferred proposal (number, title, rationale), e.g. `- **Proposal 2 (Decompose vpn-services.ts):** rationale`.

## Failure modes to avoid
- **Auto-transitioning** — `--no-transition` is intentional; don't advance.
- **Executing without valid intake** — repair first.
- **Skipping the npm test gate** — fix typecheck/lint/prettier before reporting done.
- **Pushing/PR-ing** — forbidden; the workflow does.
- **Over-refreshing** (gsd-planning) — patch only stale artifacts.

## Process Flow (Authoritative)
- gsd-planning: read phase → diff artifacts vs code/requirements → patch stale `.planning/**` only → no push.
- gsd-planning-execute: read intake (repair if needed) → execute the one wave → `npm test` (+ fix typecheck/lint/prettier) → `### Proposals deferred` if any → no push/PR.

## Output Format
- gsd-planning: `PHASE=<id> REFRESHED: <files> — <what changed>` (no push).
- gsd-planning-execute: `PHASE=<id> WAVE=<n> EXECUTED: <tasks> VERIFY: npm test=ok (tsc/lint/prettier fixed) DEFERRED: <proposals|none> TRANSITION: none`.

## Critical Constraints
- Never auto-advance phases under `--no-transition`; never push/open PR.
- Never execute a wave without valid intake — repair first.
- gsd-planning-execute: `npm test` must pass and typecheck/lint/prettier failures must be fixed before reporting completion; list deferred proposals.
