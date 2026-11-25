---
name: "web-stack-selection-stinger"
description: "Recommend one web framework from product, rendering, team and hosting needs. Separate backend choices and expose implementation-owner gaps. Read README.md for the guide map."
license: AGPL-3.0-or-later
compatibility: "Claude Code, Cursor, ChatGPT Codex, Claude Cowork; accessible official-source reading required."
metadata:
  hive-tier: specialist
  hive-drone: web-stack-selection-wasp-drone
  pair-drone: web-stack-selection-wasp-drone
  domain: web-stack-selection
  mode: research-only
---

# Web stack selection

## Purpose

Recommend ONE web framework track from product, rendering, team and hosting needs. Produce a decision, backend boundary, actual selected-owner graph and acceptance handoff. Keep a supported recommendation distinct from available implementation capability and verified app behavior.

## When to use

- "Should I use React/Vite, SvelteKit, Next.js or Vue/Nuxt?"
- "What web framework fits this quick site or paid app?"
- "Do I need SSR, a SPA, or prerendered pages?"
- "How should my existing backend and native reuse affect this choice?"

## When not to use

- Building/scaffolding/installing/deploying the app: actual implementation owners need separately authorized scope.
- Full infrastructure/rate choice: resolve selected Infrastructure Fit/Operating Cost.
- Component library/design/vendoring/license decisions: actual selected owners retain those domains.
- Security/performance/SEO/runtime certification: identify required evidence and hand it to the proper owner.

## Procedure

1. Read [README.md](README.md) and [interview-product](guides/interview-product.md). Use the [intake](references/templates/intake.md) to confirm public content/freshness, interaction, rendering, backend, team, native reuse and host constraints. Ask only unknowns that change the work.
2. Use [compare-frameworks](guides/compare-frameworks.md) and [discriminators](references/decision-discriminators.md). Compare identical requirements across React19/Vite, SvelteKit, React/Next.js and Vue/Nuxt; use official current capability evidence rather than popularity or universal speed claims.
3. Apply [define-boundaries](guides/define-boundaries.md). Separate UI/app framework/build tool and Go/Python/Rust backend decisions. Retain accepted APIs and actual auth/data/payment/secret boundaries.
4. Resolve actual selected implementation owners. React UI does not stand in for every Next server feature; Next security auditing does not imply implementation. Next.js, Nuxt and Vue have their own implementation owners (`nextjs-stinger`, `nuxt-stinger`, `vue-stinger`); if the pack that ships them is not selected, that remains an explicit delivery gap, even when the technical recommendation fits.
5. Follow [qualify-handoff](guides/qualify-handoff.md). Complete the [decision template](references/templates/decision.md) with ONE supported/provisional recommendation, rendering/deployment model, owner graph, missing evidence and future acceptance checks.
6. Review against [worked cases](references/examples/cases.md). State implementation not started and runtime proof pending. Selection does not authorize dependency installs, scaffolding, credentials, settings, deployment or publication.

## References map

- [Digest](references/research/distilled-web-stack.md), source ledger: factual grounding and source/capability limits.
- [Envelope checker](scripts/check-envelope.py): archive/links/encoded decision checks; no app or recommendation-generation proof.
- [Paired Drone](../../agents/web-stack-selection-wasp-drone.md): delegation contract.

Runtime is research-only. Ship Gate removed: framework selection produces advice and handoff documents, not application-code changes. Separately authorized commits receive ordered Security, Quality and Health review gates. A source checkout is not a registered installation.

## Critical Directive

- You must read all files and context contained within your skill.
- In the event your core knowledge does not provide sufficient guidance you must make every attempt to search the internet, related knowledge base documentation files, and other available resources to supplement your knowledge prior to proceeding with your task.
- Additional related skills can be found here:
  - [Related-owner resolution](README.md#related-owners-and-host-support): use actual selected framework/backend/UI/component/license/infrastructure/security owners through trusted Core rather than cached sibling paths or invented roles.
