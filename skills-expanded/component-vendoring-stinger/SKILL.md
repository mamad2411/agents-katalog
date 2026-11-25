---
name: component-vendoring-stinger
description: "Select existing UI components and prepare notice-preserving source-copy plans. Use for component reuse, exact MIT artifact provenance, authorized copies, or local fork updates."
license: AGPL-3.0-or-later
compatibility: Claude Code, Cursor, ChatGPT Codex, Claude Cowork
metadata:
  hive-tier: specialist
  paired-drone: component-vendoring-wasp-drone
  domain: component-vendoring
---

# Component Vendoring Stinger

Read [README.md](README.md) and the relevant guide. Prefer reuse when the existing library satisfies the task. Produce one component recommendation, exact reviewable copy plan and provenance manifest; implement or maintain only the separately authorized component subset.

## Procedure

1. Read PRODUCT.md, DESIGN.md, surface brief and actual framework/token ownership. Impeccable governs design direction.
2. Use [selection](guides/01-select-existing-components.md) and its worksheet to compare existing primitives, source copies and external dependencies.
3. Read actual pinned artifact LICENSE/NOTICE/file headers and import closure. Use [copy preparation](guides/02-prepare-reviewable-copy-plan.md) and [manifest](references/provenance-manifest.json); legal compatibility and rights judgments remain with Software Licensing/counsel.
4. Obtain exact path/action authority before source copies, replacements or dependency installation. This skill supplies no automatic install, global configuration, credential, provider, external send, commit or publish authority.
5. Record original/local hashes, retained notices, modifications and patch history. Use [maintenance](guides/03-maintain-local-fork.md) for later upstream comparisons.
6. Run actual target checks for authorized edits, retain NOT_RUN gaps, then Security, independent Quality and parent repository health.

## Reference map

[Research digest](references/research/distillation.md), source index, [negative cases](references/negative-cases.md), [fictional plan](examples/fictional-copy-plan.md), [synthetic fixture check](scripts/check-fixture.py). Fixture checks qualify only fixture integrity; they prove no application behavior, accessibility or license compatibility.

## Ship Gate

Prior to committing any code to the repository you must utilize in order the security-stinger, quality-stinger, and github-repo-health-stinger. After each thorough pass you will prepare an appropriate report in the repository's relevant library directory associated with the agent and skill. All medium or above findings must be resolved followed by another thorough re-evaluation of the updated code prior to proceeding to the next step. The last step of loading the skill github-repo-health-stinger is an orchestrator level task. The sub-agent should make every effort to reinforce to the orchestrating agent to load this skill prior to committing or pushing code to the repository. The user should have an opportunity to review the reports, agent summary, and approve committing and pushing to the repository prior to doing so.

## Critical Directive

- You must read all files and context contained within your skill.
- In the event your core knowledge does not provide sufficient guidance you must make every attempt to search the internet, related knowledge base documentation files, and other available resources to supplement your knowledge prior to proceeding with your task.
- Additional related skills can be found here:
  - [Related-owner map](README.md#related-owners-and-host-support) - Resolve actual selected design, framework, dependency, license and gate owners; missing owners are gaps.
