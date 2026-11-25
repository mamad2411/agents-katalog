---
name: argo-workflows-pipeline-design
description: >
  Designs Argo Workflows pipelines using the `Workflow`/`WorkflowTemplate`/
  `CronWorkflow` CRDs — choosing DAG vs. steps templates, passing artifacts
  and parameters between steps, and structuring Kubernetes-native batch/ML
  pipelines distinct from a CI system. Use when the user asks to "write an
  Argo Workflow," "build a DAG pipeline on Kubernetes," "pass an artifact
  between workflow steps," "reuse a WorkflowTemplate across pipelines,"
  "schedule a recurring Argo CronWorkflow," or "decide whether a batch job
  belongs in Argo Workflows vs. a CI pipeline."
license: Apache-2.0
compatibility: "Claude Code, GitHub Copilot, OpenAI Codex, Cursor, Gemini CLI"
metadata:
  domain: gitops-argo-ecosystem
  maturity: stable
---

# Argo Workflows Pipeline Design

## Purpose

Argo Workflows is a Kubernetes-native workflow engine where each step of a
pipeline runs as its own Pod, orchestrated by a `Workflow` CRD rather than
by an external CI server's job runner. It exists for workloads that are
naturally graphs of containerized steps with data dependencies between
them — data/ML pipelines, batch ETL, multi-stage image builds, infra
provisioning fan-out — rather than the "checkout, build, test, deploy"
linear shape a CI system optimizes for. Getting the template type (DAG vs.
steps), artifact passing, and reuse pattern (`WorkflowTemplate`) right
determines whether a pipeline is maintainable and debuggable at scale, or
a tangle of shell scripts strung together in one giant Pod. This matters
operationally because Argo Workflows pipelines commonly run unattended,
at high fan-out (hundreds of parallel Pods), and outside a human's
real-time attention — failures need to be attributable to a specific
step and step output, not a single opaque job log.

## When to use

- Building a pipeline that is a genuine dependency graph (step C needs
  outputs from both A and B) rather than a strictly linear sequence.
- The pipeline needs to run inside the cluster, close to data or GPU
  resources, rather than on a CI runner (e.g., a data pipeline reading
  from an in-cluster data lake, an ML training/eval fan-out).
- Deciding whether a batch/data workload belongs in Argo Workflows versus
  the org's existing CI system (Jenkins, GitHub Actions, GitLab CI).
- Passing structured outputs (files, model artifacts, JSON results)
  between steps rather than just exit codes/logs.
- Standardizing a repeated pipeline shape (e.g., "build → scan → push")
  across many teams via a shared `WorkflowTemplate` or `ClusterWorkflowTemplate`.
- Scheduling a recurring in-cluster job (nightly ETL, periodic report)
  with `CronWorkflow` instead of a bespoke `CronJob` + shell script.

## Prerequisites & environment

- Argo Workflows ≥ 3.5 installed in-cluster (`argo` namespace by
  convention), with the `argo` CLI matching the server's major version.
- A configured artifact repository for cross-step data (S3-compatible
  object storage — AWS S3, MinIO, GCS — is the common backend) if any step
  needs to pass files rather than only small parameters; configured either
  cluster-wide in the `workflow-controller-configmap` or per-`Workflow`.
- RBAC: the `ServiceAccount` a `Workflow` runs as needs only the
  permissions its steps require (e.g., permission to read a specific
  Secret, not cluster-admin) — Argo Workflows executes each step as a real
  Pod under a real ServiceAccount, so ordinary Kubernetes RBAC applies.
- Clarity on where Argo Workflows sits relative to the org's CI system:
  it is not a replacement for source-triggered build/test pipelines (see
  [ci-cd-pipeline-design](../../../devops/skills/ci-cd-pipeline-design/SKILL.md)
  if one exists in this repo, or the org's existing CI tooling) — it's
  for graph-shaped, in-cluster, often data-heavy workloads.

## Step-by-step guidance

1. **Choose `Steps` for sequential-with-simple-parallelism pipelines**,
   where each list entry is a stage and items within a stage run in
   parallel:
   ```yaml
   apiVersion: argoproj.io/v1alpha1
   kind: Workflow
   metadata:
     generateName: etl-report-
   spec:
     entrypoint: main
     templates:
       - name: main
         steps:
           - - name: extract
               template: extract
           - - name: transform-a
               template: transform
               arguments: { parameters: [{ name: shard, value: "a" }] }
             - name: transform-b
               template: transform
               arguments: { parameters: [{ name: shard, value: "b" }] }
           - - name: load
               template: load
   ```
   Double-dashed (`- -`) entries in the same outer list item run in
   parallel; a new outer list item waits for all of the previous one to
   finish. This reads naturally for pipelines that are genuinely a
   sequence of stages, each possibly fanned out.

2. **Choose `DAG` for anything with real dependency structure** — steps
   that don't form a clean stage sequence, or where you want to express
   "C depends on A and B, but D only depends on A":
   ```yaml
   templates:
     - name: main
       dag:
         tasks:
           - name: extract
             template: extract
           - name: validate
             template: validate
             dependencies: [extract]
           - name: transform
             template: transform
             dependencies: [validate]
           - name: enrich
             template: enrich
             dependencies: [extract]        # runs in parallel with validate/transform
           - name: load
             template: load
             dependencies: [transform, enrich]   # waits on both branches
   ```
   Prefer `DAG` over `Steps` whenever the dependency graph isn't a
   straight line — it's more verbose per-task but far more legible than
   simulating a DAG's shape by nesting `Steps` awkwardly.

3. **Pass small values with parameters, larger data with artifacts.**
   Parameters are strings passed via templated `{{steps.X.outputs.
   parameters.Y}}` / `{{tasks.X.outputs.parameters.Y}}`; artifacts are
   files staged to the configured artifact repository between steps:
   ```yaml
   templates:
     - name: extract
       container:
         image: ghcr.io/example/etl-extract:1.2.0
         command: ["./extract.sh", "/tmp/out/raw.parquet"]
       outputs:
         artifacts:
           - name: raw-data
             path: /tmp/out/raw.parquet
     - name: transform
       inputs:
         artifacts:
           - name: raw-data
             path: /tmp/in/raw.parquet
             from: "{{tasks.extract.outputs.artifacts.raw-data}}"
       container:
         image: ghcr.io/example/etl-transform:1.2.0
         command: ["./transform.sh", "/tmp/in/raw.parquet", "/tmp/out/clean.parquet"]
       outputs:
         artifacts:
           - name: clean-data
             path: /tmp/out/clean.parquet
   ```
   Never pass large files as `outputs.parameters` (they're stored as
   plain strings in the `Workflow` status object, with a hard size limit)
   — that's what `outputs.artifacts` and the artifact repository exist
   for.

4. **Extract reusable pipeline shape into a `WorkflowTemplate`** (or
   `ClusterWorkflowTemplate` for cross-namespace reuse) once more than one
   `Workflow` shares structure:
   ```yaml
   apiVersion: argoproj.io/v1alpha1
   kind: WorkflowTemplate
   metadata:
     name: build-scan-push
     namespace: ci
   spec:
     entrypoint: main
     arguments:
       parameters:
         - name: image-name
         - name: image-tag
     templates:
       - name: main
         dag:
           tasks:
             - { name: build, template: build }
             - { name: scan, template: scan, dependencies: [build] }
             - { name: push, template: push, dependencies: [scan] }
       - name: build
         container: { image: gcr.io/kaniko-project/executor:latest, args: ["--destination={{workflow.parameters.image-name}}:{{workflow.parameters.image-tag}}"] }
       - name: scan
         container: { image: aquasec/trivy:latest, args: ["image", "{{workflow.parameters.image-name}}:{{workflow.parameters.image-tag}}"] }
       - name: push
         container: { image: ghcr.io/example/registry-push:1.0.0 }
   ```
   Individual teams then submit a thin `Workflow` referencing it:
   ```yaml
   apiVersion: argoproj.io/v1alpha1
   kind: Workflow
   metadata:
     generateName: payments-api-build-
   spec:
     workflowTemplateRef:
       name: build-scan-push
     arguments:
       parameters:
         - { name: image-name, value: ghcr.io/example/payments-api }
         - { name: image-tag, value: "1.4.2" }
   ```

5. **Schedule recurring runs with `CronWorkflow`** rather than a plain
   Kubernetes `CronJob` running a script, when the job is itself a
   multi-step graph:
   ```yaml
   apiVersion: argoproj.io/v1alpha1
   kind: CronWorkflow
   metadata:
     name: nightly-etl
   spec:
     schedule: "0 2 * * *"
     timezone: "UTC"
     concurrencyPolicy: Replace   # or Forbid / Allow
     startingDeadlineSeconds: 300
     workflowSpec:
       workflowTemplateRef: { name: build-scan-push }
   ```
   `concurrencyPolicy: Replace` terminates a still-running previous
   instance before starting the new one — appropriate for idempotent ETL;
   `Forbid` skips the new run if the previous is still in-flight —
   appropriate when overlapping runs would corrupt shared state.

6. **Set resource requests/limits and retry/backoff per template**, not
   just at the workflow level, since each step is a distinct Pod with
   potentially very different resource needs:
   ```yaml
   templates:
     - name: transform
       retryStrategy:
         limit: 3
         retryPolicy: OnFailure
         backoff: { duration: "10s", factor: 2, maxDuration: "2m" }
       container:
         image: ghcr.io/example/etl-transform:1.2.0
         resources:
           requests: { cpu: "2", memory: 4Gi }
           limits: { cpu: "4", memory: 8Gi }
   ```

7. **Submit, monitor, and debug:**
   ```bash
   argo submit workflow.yaml
   argo list -n argo
   argo get <workflow-name> -n argo
   argo logs <workflow-name> -n argo --follow
   argo logs <workflow-name> -n argo -c transform   # logs for one step's container
   ```
   For a failed multi-step run, `argo get` renders the DAG/steps tree with
   per-node status, which is the fastest way to identify exactly which
   node failed before diving into that node's logs specifically.

## Best practices

- Default to `DAG` for anything beyond a strictly linear pipeline — it
  costs a little verbosity but avoids the common failure mode of forcing
  a real dependency graph into `Steps`' stage-shaped model and getting
  the parallelism/ordering subtly wrong.
- Keep each template doing one thing with one container image — a
  template that shells out to five different tools in one script loses
  Argo Workflows' main debugging benefit (per-step status, logs,
  retries scoped to the failing unit).
- Pass data through the artifact repository, not through a shared
  `PersistentVolumeClaim` mounted by every step, unless steps genuinely
  need concurrent read/write access to the same files — a shared PVC
  reintroduces implicit coupling and race conditions the DAG structure
  was supposed to make explicit.
- Push shared, cross-team pipeline shapes into a `WorkflowTemplate`/
  `ClusterWorkflowTemplate` early, parameterized by inputs — don't let
  five teams maintain five near-identical `Workflow` YAMLs that drift.
- Set `activeDeadlineSeconds` at the workflow level and per-template
  `retryStrategy` with bounded `backoff.maxDuration` — an unattended,
  scheduled `CronWorkflow` with no deadline can run (and retry) forever
  against a persistently failing dependency, burning cluster resources.
- Scope each step's `ServiceAccount`/RBAC to exactly what that step's
  container needs; don't run every step under one workflow-wide
  cluster-admin-ish account for convenience.

## Common pitfalls

- **Symptom:** A `Steps`-based pipeline meant to run two independent
  branches in parallel actually runs them sequentially, doubling total
  runtime.
  **Fix:** Parallel steps must be additional list entries within the
  *same* outer `- -` group; a common mistake is putting each step as its
  own top-level list item (which forces sequential ordering). Restructure
  as a `DAG` if the sequential-vs-parallel intent is getting hard to read
  in `Steps` form.

- **Symptom:** A workflow step fails intermittently with an artifact
  "not found" error even though the producing step completed
  successfully.
  **Fix:** Usually a misconfigured or missing artifact repository (no
  `artifactRepositoryRef` / no default configured in
  `workflow-controller-configmap`, or wrong bucket credentials) — the
  producing step silently failed to upload the artifact, or the consuming
  step's `from:` reference doesn't match the exact artifact name declared
  in the producer's `outputs.artifacts`. Check
  `argo get <workflow> -o yaml` for the actual artifact repository
  location recorded in status, not just the template YAML.

- **Symptom:** A `CronWorkflow` scheduled hourly has multiple overlapping
  runs stacking up, each partially mutating shared external state (e.g.,
  the same downstream table), causing inconsistent results.
  **Fix:** Set `concurrencyPolicy: Forbid` (skip a new run if one is
  still active) or `Replace` (kill the old one first) instead of the
  default `Allow`, matched to whether overlapping runs are safe for that
  specific pipeline's side effects.

- **Symptom:** A workflow with dozens of fanned-out parallel pods
  (e.g., a `withItems`/`withParam` loop over 500 elements) overwhelms
  the cluster's scheduler/API server or hits pod quota, and most nodes
  fail with generic scheduling errors rather than the pipeline's own
  logic.
  **Fix:** Set `parallelism` at the workflow or template level to cap
  concurrent Pods (`spec.parallelism: 20`), and confirm the target
  namespace's `ResourceQuota` accommodates the intended fan-out before
  scaling it up.

- **Symptom:** A `WorkflowTemplate` shared across teams changes (a step's
  image is bumped) and every team's already-running or newly submitted
  `Workflow`s referencing it via `workflowTemplateRef` pick up the change
  immediately and unexpectedly, with no version pin.
  **Fix:** `workflowTemplateRef` resolves the template at submission
  time from the *current* `WorkflowTemplate` object, not a pinned
  version — for teams needing stability guarantees, version the template
  name itself (`build-scan-push-v2`) on breaking changes, or embed the
  full template inline in critical workflows instead of referencing a
  shared mutable object.

## Worked example

**Scenario:** A nightly ETL pipeline: extract raw data, validate it,
transform it in two parallel shards, then load — reusable as a
`WorkflowTemplate`, scheduled nightly, with bounded retries and fan-out.

```yaml
apiVersion: argoproj.io/v1alpha1
kind: WorkflowTemplate
metadata:
  name: nightly-etl
  namespace: data-pipelines
spec:
  entrypoint: main
  activeDeadlineSeconds: 3600
  templates:
    - name: main
      dag:
        tasks:
          - { name: extract, template: extract }
          - { name: validate, template: validate, dependencies: [extract] }
          - name: transform-a
            template: transform
            dependencies: [validate]
            arguments: { parameters: [{ name: shard, value: "a" }] }
          - name: transform-b
            template: transform
            dependencies: [validate]
            arguments: { parameters: [{ name: shard, value: "b" }] }
          - name: load
            template: load
            dependencies: [transform-a, transform-b]

    - name: extract
      retryStrategy: { limit: 3, retryPolicy: OnFailure }
      container: { image: ghcr.io/example/etl-extract:1.2.0 }
      outputs:
        artifacts:
          - { name: raw-data, path: /tmp/out/raw.parquet }

    - name: validate
      inputs:
        artifacts:
          - { name: raw-data, path: /tmp/in/raw.parquet, from: "{{tasks.extract.outputs.artifacts.raw-data}}" }
      container: { image: ghcr.io/example/etl-validate:1.0.0 }

    - name: transform
      inputs:
        parameters: [{ name: shard }]
        artifacts:
          - { name: raw-data, path: /tmp/in/raw.parquet, from: "{{tasks.extract.outputs.artifacts.raw-data}}" }
      container:
        image: ghcr.io/example/etl-transform:1.2.0
        args: ["--shard", "{{inputs.parameters.shard}}"]
      outputs:
        artifacts:
          - { name: "clean-{{inputs.parameters.shard}}", path: /tmp/out/clean.parquet }

    - name: load
      inputs:
        artifacts:
          - { name: clean-a, path: /tmp/in/clean-a.parquet, from: "{{tasks.transform-a.outputs.artifacts.clean-a}}" }
          - { name: clean-b, path: /tmp/in/clean-b.parquet, from: "{{tasks.transform-b.outputs.artifacts.clean-b}}" }
      container: { image: ghcr.io/example/etl-load:1.0.0 }
---
apiVersion: argoproj.io/v1alpha1
kind: CronWorkflow
metadata:
  name: nightly-etl-schedule
  namespace: data-pipelines
spec:
  schedule: "0 2 * * *"
  timezone: "UTC"
  concurrencyPolicy: Forbid
  workflowSpec:
    workflowTemplateRef: { name: nightly-etl }
```

`argo get nightly-etl-schedule-<run-id> -n data-pipelines` renders the DAG
tree, immediately showing whether `transform-a` or `transform-b` (rather
than the whole run) is the one that failed, and `argo logs ... -c
transform` scoped to the failing node avoids trawling combined logs from
five steps.

## Cross-references

- [argo-events-and-event-driven-automation](../argo-events-and-event-driven-automation/SKILL.md)
- [argocd-application-configuration](../argocd-application-configuration/SKILL.md)
- [container-build-and-release](../../../devops/skills/container-build-and-release/SKILL.md)
