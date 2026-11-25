---
name: deployment-infra
description: Packaging, environments, migration rollout, CI/CD, and rollback planning. Use when shipping a feature, running migrations against real environments, or wiring build/deploy. Destructive/prod steps require user approval (Gate G5).
version: 0.2.0
tier: core
stack: [any]
owner: release
gates: [G4, G5]
related: [.ai/modules/git.md, data-migration]
---

# Skill: deployment-infra

## Purpose
Repo-canonical release discipline so shipping is reproducible on any machine/CI, not tied to a host skill.

## When to use
Shipping a feature, wiring build/deploy, or rolling out migrations to real environments.

## Procedure
1. **Readiness (G2/G3)**: tests green (`verification.test_command`), typecheck/build pass, review approved, docs + CHANGELOG updated.
2. **Build**: `verification.build_command`; artifact reproducible from a clean checkout.
3. **Migrations**: any schema/data change already went through `data-migration` (planned, up+down tested). Roll out forward-compatible: expand → migrate → contract.
4. **Environments**: promote staging → prod; config via env, never committed secrets (Gate G4 checks this).
5. **Rollback plan**: written BEFORE deploy — the exact revert (previous artifact + down migration) and the trigger conditions.
6. **Approval (G5)**: production deploy, irreversible migration, or force-push to a shared branch require explicit user approval recorded in the conversation.

## Checklist
- [ ] Tests + typecheck + build green in CI
- [ ] Rollout forward-compatible; migrations reversible
- [ ] No secrets in artifact or config
- [ ] Rollback steps + triggers written before deploy
- [ ] Prod/irreversible steps have explicit user approval (G5)

## Anti-patterns
- Deploying without a written rollback
- Destructive migration in the same release that changes the writer
- Secrets baked into the build or config
- Skipping G5 approval for a production/irreversible action

## Output
Release notes + CHANGELOG entry + `.ai-work/INDEX.md` state update (owner: release).
