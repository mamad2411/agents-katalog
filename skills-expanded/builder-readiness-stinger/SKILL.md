---
name: "builder-readiness-stinger"
description: "Help new coders prepare to build: clarify one goal, learning prerequisites, roles, expectations, unknowns and a first-slice proposal. Read README.md for the guide map."
license: AGPL-3.0-or-later
compatibility: "Claude Code, Cursor, ChatGPT Codex, Claude Cowork; accessible source-reading tools required."
metadata:
  hive-tier: specialist
  hive-drone: builder-readiness-wasp-drone
  pair-drone: builder-readiness-wasp-drone
  domain: developer-learning
  mode: research-only
---

# Builder readiness

## Purpose

Help a new coder turn a product idea into one scoped readiness recommendation, learning prerequisites, responsibilities, unknowns and a first representative slice proposal. Explain what to expect at grade 8 without pretending an interview proves competence or production readiness.

## When to use

- "I want to build an app/site/desktop app/integration/plugin/tool; what should I know and expect?"
- "How should I think and work as a software team while learning?"
- "What should my role be while AI helps me build?"
- "What is a sensible first behavior to learn and qualify?"
- "What security responsibilities do I have when AI helps me build?"
- "Should this be an app, website, integration, plugin or tool?"

## When not to use

- Market validation (`/validate-idea`, Discovery Research), stack/infra choice, actual account preparation, pricing/cost calculation or completion forecasts: route to their actual selected owners.
- App scaffold, implementation, installation or release: separate accepted scope and action authority required.
- Declaring competence/security/production readiness: require actual understanding and review/runtime evidence.
- Initializing a repository/library: Core/App Primer owners retain that work.

## Procedure

1. Read [README.md](README.md) and [interview-goal](guides/interview-goal.md). Ask only material user/job/platform/milestone/experience/data/budget/time questions missing from supplied context; do not force a generic questionnaire.
2. Fill the [readiness worksheet](references/templates/readiness-worksheet.md). Keep reported experience separate from observed exercises and unknowns that change decisions. No credentials/live-user data are needed.
3. Use [expectations](guides/set-expectations.md) and [roles reference](references/readiness-and-roles.md). Explain human product decisions, AI drafting, actual implementation, independent review and operations. Use one bounded analogy; preserve the factual explanation.
4. For product-form questions, use [choose product form](guides/choose-product-form.md) and its worksheet/cases. Recommend one provisional form from supplied job/constraints; selected platform/stack/integration owners retain feasibility and implementation.
5. For beginner security questions, use [security responsibilities](guides/explain-security-responsibilities.md), the [map](references/beginner-security-responsibilities.md) and [worksheet](references/templates/security-responsibility-worksheet.md). Actual controls and reviews remain with selected owners; unknown roles/permissions and learner understanding stay pending.
6. Follow [first slice](guides/choose-first-slice.md). Propose ONE useful behavior with input/output/failure and acceptance owner, scoped to learning or the supplied milestone. Defer irrelevant features/providers.
7. Follow [route readiness](guides/route-readiness.md). Resolve actual selected Discovery Research (`/validate-idea`), Web Stack Selection, Launch Assets, Estimation/Pricing/Operating Cost and App Primer when their decisions are needed. Do not duplicate unavailable specialists or invent rates/durations.
8. Review against [worked cases](references/examples/cases.md). Return one advisory recommendation or the precise blocked question, learning next step, responsibilities, first-slice proposal and owner handoff. Ask one non-shaming teach-back question and mark understanding pending until a reader response supplies evidence.

## References map

- [Digest](references/research/distilled-builder-readiness.md), source ledger: grounding, dated captures and limits.
- [Envelope checker](scripts/check-envelope.py): archive/links/encoded boundary checks, not assessment of a learner.
- [Paired Drone](../../agents/builder-readiness-wasp-drone.md): delegation scope.

Runtime is research-only. Ship Gate removed: intake/readiness advice does not implement application code. Parent source promotion/registration and separately authorized commits follow ordered review gates. Reading the learning manual does not authorize installing or onboarding the user.

## Critical Directive

- You must read all files and context contained within your skill.
- In the event your core knowledge does not provide sufficient guidance you must make every attempt to search the internet, related knowledge base documentation files, and other available resources to supplement your knowledge prior to proceeding with your task.
- Additional related skills can be found here:
  - [Related-owner resolution](README.md#related-owners-and-host-support): use actual selected learning/decision/asset/economic/App Primer owners through trusted Core rather than cached sibling paths or invented roles.
