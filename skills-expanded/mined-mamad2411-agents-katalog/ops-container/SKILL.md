---
name: ops-container
description: "Diagnose container builds, runtime failures, and configuration differences. Use for image/build/runtime diagnosis; ops-restore handles recovery of persisted state."
---

# ops-container

Diagnose container builds, runtime failures, and configuration differences.

## Choose this workflow

Use for image/build/runtime diagnosis; ops-restore handles recovery of persisted state.

Read [shared execution](../../references/execution.md) for context/mode/authority handling and [Operations methods](../../references/packs/operations.md) for tool selection and operational details. Resolve these paths from this skill file; all runtime assets ship inside the plugin.

## Input and mode

Use the complete request appended to this invocation, preserving all constraints and references. Default mode: **inspect**. Inspect; Dockerfile/image/runtime configuration, logs, and failing build/start behavior. Apply for a requested focused fix.

**Pack prerequisites:** Exact service/environment, time window, revision/configuration identity, authorized logs/metrics, and operational constraints. Prefer observation before intervention; live restarts, traffic changes, restores, and notifications require the requested target/action. Redact sensitive telemetry.

- **Infer from evidence:** Read service/environment, time window, revision, available telemetry and existing incident or recovery procedure.
- **Reasonable default:** Start from supplied logs and read-only observation; rank hypotheses without presenting an unexecuted intervention as recovery.
- **Ask only when needed:** Resolve the precise target and missing authority before restart, restore, notification or traffic changes; continue evidence analysis while waiting.

Declared evidence requirements: `container.context`. Use actual host discovery or adequate supplied artifacts; unavailable evidence remains blocked/unknown.

## Scope

Container build context, dependencies, permissions, entrypoint, networking, resources, and health checks.

Inspect/plan: inspect or propose; save requested artifacts only. Apply: edit the requested local implementation and perform relevant bounded checks while preserving unrelated work. Live data changes, remote actions and paid jobs require their resolved target and existing session authorization.

## Execute

1. Compare build context, multi-stage copy paths, runtime user, working directory, ports and volume permissions with host assumptions.
2. Inspect image metadata and logs from the intended image digest, and reproduce in an isolated build after evaluating its execution effects.
3. Propose a focused fix, applying it in apply mode.

## Technical method

- **Inspect:** Inspect build stages, image digest, architecture, user, filesystem permissions, entrypoint and signal handling.
- **Method:** Separate build-time assets from runtime requirements; use least-needed privileges and remove secrets from build layers.
- **Avoid misdiagnosis:** Deleting a secret in a later layer leaves it in earlier layers; a running process does not prove readiness or graceful shutdown.
- **Check the result:** Build/run an isolated image, exercise readiness, SIGTERM and read-only/non-root requirements, and inspect final-image contents.

## Read when relevant

- When a concrete decision or deliverable example would clarify this workflow: [Operations worked example](../../references/examples/operations.md).
- The container runs on Kubernetes: probes, readiness or rollout recovery: [Kubernetes release and readiness](../../references/methods/kubernetes-release.md).
- Pinning base images, toolchains or build environments: [Reproducible environments](../../references/methods/reproducible-environments.md).
- Secrets or unpinned dependencies may be baked into image layers: [Supply chain and image secrets](../../references/security/supply-chain.md).

## Decision branches

- **When local build and deployed digest differ:** Establish artifact identity before patching source or diagnosing runtime configuration.

## Deliver and verify

- Diagnosis or patch with the build/runtime boundary, artifact identity, build/start evidence and remaining isolated-reproduction or environment gaps.

Verify these observable conditions when applicable to the actual task; do not claim they were exercised from merely reading this file:

- Required runtime files survive multi-stage builds; a non-root process can access only intended paths.

## Stop and recover

- No privileged host mounts or deployment changes by default. Building/running untrusted images requires evaluating their execution effects first.

## Example requests

- **Normal (inspect):** Diagnose why this multi-stage image lacks its runtime files.
- **Edge (inspect):** Diagnose a multi-stage image missing a required runtime file under a non-root user.
- **Blocked (inspect):** Inspect a Dockerfile without building untrusted images or granting privileged mounts.
