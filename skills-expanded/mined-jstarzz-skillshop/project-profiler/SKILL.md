---
name: project-profiler
description: "Fingerprint an unfamiliar repository's stack, boundaries, risks, tests and delivery shape before other skills act. Use when new repository, route skills by stack, plan substantial work."
license: MIT
compatibility: "Agent Skills compatible hosts; optimized for coding agents with repository and test/tool access."
metadata:
  category: "meta"
  version: "0.1.0"
  maintainer: "SkillShop maintainers"
  maturity: "draft"
---

# Project Profiler

Fingerprint an unfamiliar repository's stack, boundaries, risks, tests and delivery shape before other skills act.

## Activate when

- new repository
- route skills by stack
- plan substantial work

## Focus

- Primary mission: Fingerprint an unfamiliar repository's stack, boundaries, risks, tests and delivery shape before other skills act.
- Use project/runtime evidence; this skill is a workflow, not a role-play persona.
- If another skill owns a deeper specialist concern, hand off instead of duplicating its entire workflow.

## Workflow

1. Read repository instructions, README, top-level tree, package/module manifests, CI and deployment files.
2. Identify languages, frameworks, package managers, runtimes, databases, queues, caches, object stores and external services.
3. Map process boundaries, entry points, request/data flow, generated code, migrations and test frameworks.
4. Tag sensitive surfaces such as authentication, authorization, payments, multi-tenancy, file uploads, migrations and background jobs.
5. Record maturity signals: test coverage shape, observability, release automation, health checks, backups and environment configuration.
6. Separate hard facts from inferences and unknowns.
7. Emit a compact fingerprint and likely relevant skills rather than a giant architecture essay.

## Deliverables

- Evidence-based output for the skill's mission
- Explicit assumptions and unknowns
- Clear downstream actions
- A result that directly satisfies: Fingerprint an unfamiliar repository's stack, boundaries, risks, tests and delivery shape before other skills act.

## Common failure modes

- Loading every available skill 'just in case'
- Replacing evidence with conversational confidence
- Producing a giant narrative when a compact reusable artifact would do
- Hiding uncertainty instead of stating what was not inspected, reproduced, measured, or verified.

## Composition

Use `skill-router` when this task needs multiple specialties. Prefer composition over copying another skill's workflow into this one.

## Exit criteria

- The requested decision, change, test, or review is supported by concrete evidence.
- Important residual risks, limitations, and unknowns are explicit.
- The output is specific enough for another engineer or agent to act on without reconstructing hidden reasoning.
