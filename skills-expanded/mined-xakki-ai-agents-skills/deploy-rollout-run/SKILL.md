---
name: deploy-rollout-run
description: 'Plan, perform or verify authorized rollouts, cutovers and releases with scoped evidence and rollback. Use when deploying or releasing a service. RU: деплой, выкатка, релиз.'
disable-model-invocation: true
---

# Deployment operations

Identify the actual task phase: investigation, preflight, source preparation, approved live action or acceptance. Resolve the service, environment, immutable candidate or configuration identity, owner, access, existing work and supported operator interface. A prior successful build, healthy container or research approval does not establish that the requested runtime is running the intended version or authorize an additional external effect.

Before any admitted live change, establish the exact authorized target, operation, limits, effect on users and related services, readiness predicates and rollback or recovery route. Inspect the project's actual deployment and test contracts; do not assume a host, agent-specific path, container engine, shell target or secret location. Distinguish direct observations from a dry run or an unexecuted plan. A user-approved sequence remains authorized within its scope; do not ask again for unchanged routine steps.

Execute only the approved operations, keeping identities, actual outcomes, failures and still-running work visible. Preserve unrelated work, resources, configuration and sensitive data. A timeout or ambiguous side effect is not proof of failure: reconcile the actual state through permitted readback before a repeat, and honor any one-shot limit or stop boundary. Verify actual readiness, effective configuration and relevant functional behavior at the boundary the task requires; report local tests, production readback and unverified claims separately.

For a live preflight or constrained external actions, use [preflight and bounded actions](references/preflight-and-actions.md). For stateful and generated-state cutovers, use [cutover and recovery](references/cutover-and-recovery.md). For versioned release artifacts, use [artifact packaging acceptance](../quality-artifact-verify/SKILL.md). Report what changed, measured results, gaps, active work and rollback state.

When a rollout includes persistent schema changes, use [schema evolution](references/schema-evolution.md). When runtime identity or mount ownership prevents access, use [runtime ownership](references/runtime-ownership.md).
