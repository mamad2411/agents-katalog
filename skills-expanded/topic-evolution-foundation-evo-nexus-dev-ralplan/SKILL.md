---
name: dev-ralplan
description: Multi-perspective consensus planning with Planner/Architect/Critic loop. Use when high-stakes decisions need RALPLAN-DR structured deliberation (auth, migrations, public APIs, irreversible changes). Pairs with @compass-planner + @apex-architect + @raven-critic.
---

# Dev Ralplan

Derived from oh-my-claudecode (MIT, Yeachan Heo). Adapted for the EvoNexus Engineering Layer.

Consensus mode planning: a Planner/Architect/Critic loop that produces a plan with explicit principles, decision drivers, viable options, and an ADR. Used for high-stakes or irreversible work.

## Use When
- Multi-perspective consensus needed on a plan or design
- High-stakes work: auth, security, data migrations, destructive/irreversible changes, production incidents, compliance/PII, public API breakage
- User says "ralplan", "consensus", "let's deliberate"
- When `dev-plan --consensus` would normally apply

## Do Not Use When
- Simple, low-risk task → use `dev-plan` standard mode
- User wants direct execution → use `dev-autopilot`
- Single-perspective is sufficient → use `dev-plan` direct mode

## Workflow

### Stage 1 — Initial plan (`@compass-planner`)
- Run interview if needed
- Emit RALPLAN-DR summary: Principles (3-5), Decision Drivers (top 3), Viable options (≥2)
- If only 1 viable option remains, document explicit invalidation rationale for alternatives

### Stage 2 — Architecture review (`@apex-architect`)
- Read the plan
- Provide consensus addendum: strongest steelman antithesis, real tradeoff tension, synthesis if viable
- In deliberate mode, flag explicit principle violations

### Stage 3 — Critique (`@raven-critic`)
- Multi-perspective adversarial review
- Pre-commitment predictions
- Gap analysis
- Self-audit + realist check
- Verdict: REJECT / REVISE / ACCEPT-WITH-RESERVATIONS / ACCEPT

### Stage 4 — Revised plan (`@compass-planner`)
- Incorporate apex + raven feedback
- Final plan must include ADR: Decision, Drivers, Alternatives considered, Why chosen, Consequences, Follow-ups
- In deliberate mode: pre-mortem (3 scenarios) + expanded test plan (unit/integration/e2e/observability)

## Mode Selection
- **Short mode (default):** principles + drivers + ADR
- **Deliberate mode (`--deliberate`):** + pre-mortem + expanded test plan + principle violation flags

Trigger deliberate mode when: auth/security touched, data migration, destructive/irreversible change, production incident response, compliance/PII implications, public API breakage.

## Output
Final plan saved to `workspace/development/plans/[C]ralplan-{name}-{date}.md` with ADR section.

## Pairs With
- `@compass-planner` (drives the loop)
- `@apex-architect` (architecture review)
- `@raven-critic` (adversarial review)
- `dev-plan` (which can chain into ralplan with `--consensus`)
- `dev-autopilot` (skips its own Phase 0+1 if a ralplan plan already exists)
