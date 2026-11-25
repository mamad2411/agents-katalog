---
name: prompt-injection-review
description: "Review LLM-integrated systems for untrusted instruction/data boundaries, tool authorization, secret exposure and unsafe action chaining. Use when prompt injection, LLM security, agent tool safety."
license: MIT
compatibility: "Agent Skills compatible hosts; optimized for coding agents with repository and test/tool access."
metadata:
  category: "security"
  version: "0.1.0"
  maintainer: "SkillShop maintainers"
  maturity: "draft"
---

# Prompt Injection Review

Review LLM-integrated systems for untrusted instruction/data boundaries, tool authorization, secret exposure and unsafe action chaining.

## Activate when

- prompt injection
- LLM security
- agent tool safety

## Focus

- Primary mission: Review LLM-integrated systems for untrusted instruction/data boundaries, tool authorization, secret exposure and unsafe action chaining.
- Use project/runtime evidence; this skill is a workflow, not a role-play persona.
- If another skill owns a deeper specialist concern, hand off instead of duplicating its entire workflow.

## Workflow

1. Map actors, assets, entry points, trust boundaries, and the sensitive operations touched by the change.
2. Trace authentication, authorization, untrusted input, secrets, and sensitive data through real code paths before looking for generic categories.
3. Test negative cases across identities, resources, malformed inputs, duplicates, replay, and abuse limits where applicable.
4. Validate suspicious findings against actual reachable behavior; do not report speculative vulnerabilities as confirmed.
5. Prefer server-side enforcement, explicit limits, least privilege, parameterized APIs, and auditable state transitions.
6. Consider logging, error messages, caches, background jobs, exports, and integrations as part of the attack/data surface.
7. Prioritize findings by realistic impact and prerequisites, then pair each with a concrete remediation and regression check.

## Deliverables

- Verified security findings
- Attack/data-flow reasoning
- Concrete remediation and regression checks
- A result that directly satisfies: Review LLM-integrated systems for untrusted instruction/data boundaries, tool authorization, secret exposure and unsafe action chaining.

## Common failure modes

- Checklist dumping without reachable evidence
- Relying on UI hiding for authorization
- Logging or persisting secrets while testing security
- Hiding uncertainty instead of stating what was not inspected, reproduced, measured, or verified.

## Composition

Use `skill-router` when this task needs multiple specialties. Prefer composition over copying another skill's workflow into this one.

## Exit criteria

- The requested decision, change, test, or review is supported by concrete evidence.
- Important residual risks, limitations, and unknowns are explicit.
- The output is specific enough for another engineer or agent to act on without reconstructing hidden reasoning.
