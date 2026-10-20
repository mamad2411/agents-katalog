---
name: ml-package
description: "Package preprocessing, artifacts, dependencies, and interfaces. Use to create a reproducible inference artifact; ml-serving implements the serving boundary."
---

# ml-package

Package preprocessing, artifacts, dependencies, and interfaces.

## Choose this workflow

Use to create a reproducible inference artifact; ml-serving implements the serving boundary.

Read [shared execution](../../references/execution.md) for context/mode/authority handling and [ML deployment methods](../../references/packs/ml-deployment.md) for tool selection and operational details. Resolve these paths from this skill file; all runtime assets ship inside the plugin.

## Input and mode

Use the complete request appended to this invocation, preserving all constraints and references. Default mode: **apply**. Apply; model/preprocessing artifacts, runtime, interface, and output location.

**Pack prerequisites:** Versioned model and preprocessing artifacts, input/output schema, runtime/dependencies, operating targets, and authorized environment. Validate artifact trust before loading formats that can execute code. Packaging or writing monitoring configuration does not deploy a model or enable a hosted service.

- **Infer from evidence:** Read artifact format/trust, preprocessing schema, serving runtime, compatibility and existing rollout controls.
- **Reasonable default:** Prepare packaging/configuration and isolated checks without treating them as a live deployment.
- **Ask only when needed:** Resolve the target, rollback compatibility and operating limits before rollout or load generation; missing production access does not block packaging.

Declared evidence requirements: `ml.artifacts`. Use actual host discovery or adequate supplied artifacts; unavailable evidence remains blocked/unknown.

## Scope

Reproducible inference package and metadata; no registry upload or deployment implicitly.

Apply: only the requested local changes and relevant isolated verification. Inspect/plan requests remain inspection/planning. External actions require their exact action and target in session authorization.

## Execute

1. Verify artifact provenance.
2. Bundle preprocessing, feature order/schema, model identity and pinned compatible dependencies, recording versions and checksums.
3. Validate fresh-load parity with known-input fixtures in an isolated supported environment.

## Technical method

- **Inspect:** Inventory model/preprocessor, ordered feature schema, versions, provenance and artifact format.
- **Method:** Package the complete inference contract with known-input expectations; inspect executable serialization and trusted origin before loading.
- **Avoid misdiagnosis:** Pickle-style loading can execute code; matching a model filename does not establish trusted provenance or preprocessing parity.
- **Check the result:** Fresh-load a trusted fixture in isolation and compare exact feature order, missing/unseen handling and expected output within tolerance.

## Read when relevant

- When a concrete decision or deliverable example would clarify this workflow: [ML deployment worked example](../../references/examples/ml-deployment.md).
- Uploads, filesystem paths, extraction or artifact loading are in scope: [Files and resource limits](../../references/security/files.md).

## Decision branches

- **When serialization may execute code and provenance is untrusted:** Inspect provenance and use a safe supported loading path or stop before loading.

## Deliver and verify

- Package and manifest with checksums, input/output schema, loading instructions and fresh-load expected-output fixture results.

Verify these observable conditions when applicable to the actual task; do not claim they were exercised from merely reading this file:

- A fresh supported environment reproduces fixture outputs within tolerance; incompatible artifact/schema versions fail clearly.

## Stop and recover

- Do not load untrusted executable serialization or bundle training data/secrets unnecessarily. Missing preprocessing prevents a complete package claim.

## Example requests

- **Normal (apply):** Package the model with preprocessing, schema, dependencies, and parity fixtures.
- **Edge (apply):** Package a model whose categorical encoder and feature order were saved separately.
- **Blocked (inspect):** Inspect an artifact manifest without loading untrusted executable serialization.
