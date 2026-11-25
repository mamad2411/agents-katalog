---
name: leeway-capability-resilience
description: Governed capability resilience and sovereignty layer for LeeWay Agent Skills. Tracks required capabilities, providers, external dependencies, fallback routes, capability debt, observed failures, and promotion candidates so loss of an MCP/tool/provider does not automatically terminate the parent mission.
license: MIT
metadata:
  authority: Creator/Human Authority > LeeWay Standards
  mode: capability-resilience
  stage: post-operating-loop-pre-capability-dispatch
  capability-kernel: skills/leeway-universal-capability-kernel/SKILL.md
  factory: skills/leeway-skill-factory/SKILL.md
  lifecycle: skills/leeway-skill-lifecycle-governance/SKILL.md
  gateway: skills/leeway-tool-gateway/SKILL.md
---

# LeeWay Capability Resilience

## Purpose

Make capability availability resilient without creating duplicate LeeWay authorities.

A repeatedly required external MCP, tool, runtime, model, API, adapter or service is a dependency. LeeWay must know what capability it provides, what depends on it, what alternatives exist, what fails when it disappears, and when a LeeWay-owned fallback or replacement is justified.

## Capability graph

Track relationships using at least:

- NEEDS
- PROVIDES
- DEPENDS_ON
- FALLBACK_FOR
- REPLACES
- EXTENDS
- COMPOSES_WITH
- GOVERNS
- EXECUTES
- VERIFIES
- LEARNS_FROM

A provider is not the capability itself.

Example:

`filesystem.read ← provided by Desktop Commander / Host Commander / native PowerShell`

Loss of one provider must not be promoted into loss of the abstract capability until alternatives are evaluated.

## Required provider state

For a material capability/provider relationship track:

- capability id;
- provider id and type;
- authority source;
- current availability;
- authorization;
- health;
- last verified execution;
- recurrence/demand;
- criticality;
- failure impact;
- fallback providers;
- coverage gaps;
- portability;
- security boundary;
- ownership state: EXTERNAL | ADAPTED | LEEWAY_NATIVE;
- evidence references.

## Capability debt

Create capability debt when an external dependency is repeatedly necessary and its absence materially threatens LeeWay completion.

A debt record should identify:

`capability → external dependency → recurrence → criticality → failure impact → native coverage → fallback quality → proposed action → evidence state`

Capability debt is evidence for evaluation, not automatic permission to clone an external system.

## Resilience decision

When a provider is unavailable:

`required capability → enumerate providers → verify authority/health → select authorized fallback → execute/qualify → record evidence`

If no sufficient provider exists:

`gap → compose existing primitives? → extend canonical owner? → create adapter? → create skill/MCP/native capability? → qualify → register → resume parent mission`

Use `leeway-skill-factory` and `leeway-skill-lifecycle-governance` for new or sourced skills. After qualification, re-enumerate through `leeway-universal-capability-kernel` and return control to `leeway-agent-operating-loop` so the original acceptance gate resumes. Use the Universal Capability Kernel for cross-capability composition and routing.

## Capability sovereignty law

When recurrence, criticality, failure impact, security, economics, portability or availability justify ownership, evaluate a governed LeeWay-native capability.

Possible decisions:

- USE_EXISTING
- COMPOSE_EXISTING
- EXTEND_CANONICAL
- ADAPT_EXTERNAL
- CREATE_ADAPTER
- CREATE_SKILL
- CREATE_MCP
- CREATE_NATIVE_CAPABILITY
- PROMOTE_NATIVE
- RETAIN_EXTERNAL
- DEPRECATE
- BLOCKED_BY_AUTHORITY

These are governance decision classes, not fabricated outputs from the canonical Formula evaluator. If Formula is actually executed, preserve its real decision/version/hash separately.

## Desktop Commander pattern

Desktop Commander is a provider, not sovereign capability identity.

If unavailable, determine which abstract capabilities are actually needed (filesystem, terminal, process, diagnostics, service management, hashing, etc.), then evaluate authorized alternatives.

A temporary fallback may restore execution. Repeated dependency/failure should raise capability debt and may justify LeeWay Host Commander or another governed native provider.

## Digital Brain / Cognitive Fabric handoff

Publish capability/provider relationships and evidence states so the Cognitive Fabric can show:

- what Agent Lee needs;
- what currently provides it;
- provider health;
- dependencies;
- fallback providers;
- coverage gaps;
- capability debt;
- promotion state.

Do not invent numeric coverage scores without measured evidence.

## Mandatory probes

At provider failure, promotion review, or capability-gap discovery ask:

1. What capability did we actually lose?
2. What are we not discovering about alternate providers or native primitives?
3. What needs to be enhanced so this dependency is not a single point of failure?
4. What authorized route resumes the parent acceptance gate?

## Final law

External dependency failure is a routing event before it is a mission failure.

Preserve the parent objective. Select an authorized fallback when one exists. Build the missing bridge only when governance justifies it. Qualify it. Register it. Resume the mission.
