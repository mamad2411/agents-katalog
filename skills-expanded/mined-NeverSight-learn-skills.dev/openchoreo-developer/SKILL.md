---
name: openchoreo-developer
description: |
  Use whenever the task is about working with an application on OpenChoreo: deploying, updating, debugging, explaining resources, or writing app-facing YAML through the OpenChoreo MCP servers. Also activate `openchoreo-platform-engineer` when the task needs platform resources (DataPlane, ComponentType, Trait, Workflow), cluster-side debugging, any cluster-level access, hard-deletion of any resource, or an operation with no MCP write surface (SecretReference create, Component trait attachment).
metadata:
  version: "1.0.0"
---

# OpenChoreo Developer Guide

Help with application-level work on OpenChoreo through the OpenChoreo MCP servers. Keep this file lean, discover the current platform shape via MCP, and read detailed references only when the task actually needs them.

## Scope and pairing

Use this skill for developer-owned work:

- Deploying a new app or service to OpenChoreo
- Debugging an existing Component, Workload, ReleaseBinding, or WorkflowRun
- Explaining OpenChoreo app concepts and resource relationships
- Writing or fixing app-facing YAML
- Adapting an application so it runs cleanly on OpenChoreo

Activate `openchoreo-platform-engineer` at the same time when the task also includes any of these:

- platform resources such as DataPlane, WorkflowPlane, Environment, DeploymentPipeline, ComponentType, Trait, Workflow, or ClusterWorkflow authoring (write tools exist in MCP but they're PE territory)
- cluster-level access of any kind (controller logs, raw CRD inspection, Helm)
- gateway, secret store, registry, identity, or other platform configuration
- operations with no MCP write surface anywhere — **SecretReference** create/update/delete, **Component `spec.traits[]` attachment**, hard delete of any resource (Component, Workload, ReleaseBinding, Project, Namespace)
- a likely PE-side failure rather than an app-level configuration problem

If both skills are available and the task involves both deployment/debugging and platform behavior, use both immediately. Many OpenChoreo problems cross that boundary.

## Working style

Prefer progressive discovery:

1. Understand the application shape from the repo before authoring resources.
2. Confirm MCP connectivity and the namespace/project scope you'll be working in.
3. Discover only the cluster resources needed for this task via MCP.
4. Read the matching reference file only after you know which area is relevant.
5. Apply the smallest viable change and verify through live status and logs.

The current cluster output is more trustworthy than memory. Do not assume available ComponentTypes, Traits, Workflows, environments, or field names. Discover them via MCP first.

Before inventing YAML, fetch the schema for the target resource (`get_workload_schema`, `get_cluster_component_type_schema`, `get_cluster_trait_schema`) or use a repo sample as a starting point.

## Tool surface

**This skill is MCP-only.** All resource CRUD, schema discovery, and observability queries go through the two OpenChoreo MCP servers:

| Server | Purpose |
|---|---|
| Control plane (`openchoreo-cp`) | Components, Workloads, ReleaseBindings, schemas, workflows |
| Observability (`openchoreo-obs`) | Logs, metrics, traces, alerts, incidents |

> **Tool naming.** Throughout this skill, tools are referenced by their bare name (e.g. `get_component`, `query_component_logs`). The actual callable name in your runtime carries an agent-specific prefix that wraps the server name — for example, in Claude Code the bare `get_component` is invoked as `mcp__openchoreo-cp__get_component`, and `query_component_logs` is `mcp__openchoreo-obs__query_component_logs`. Other coding agents use different prefixes. Apply whatever prefix your agent expects when actually invoking the tool.

Activate `openchoreo-platform-engineer` for anything outside that surface, including:

- Operations with no MCP write surface today: **SecretReference** create/update/delete, **Component `spec.traits[]` attachment** (`patch_component` only covers `auto_deploy` and `parameters`), and **hard delete** of any resource (Component, Workload, ReleaseBinding, Project, Namespace — there are no `delete_*` tools for these in MCP).
- Platform resources (DataPlane, WorkflowPlane, Environment, DeploymentPipeline, ComponentType, Trait, Workflow, ClusterWorkflow). Write tools for these exist in MCP but are PE-owned.
- Cluster-level access (controller logs, raw CRD inspection, Helm).
- Gateway, secret store, registry, identity, or other platform configuration.
- A likely PE-side failure rather than an app-level configuration problem.

The developer skill operates entirely above the cluster boundary, through MCP.

## Reference routing

Foundational material:

- `references/concepts.md` — resource hierarchy, Cell architecture, endpoint visibility, planes, API version
- `references/resource-schemas.md` — full YAML for Project, Component, Workload, Workload Descriptor, Environment, DeploymentPipeline, ReleaseBinding, SecretReference
- `references/mcp.md` — full MCP tool catalog (control plane + observability), workflow patterns, gotchas

Recipes (one task per file, MCP-driven):

Build & Deploy
- `references/recipes/deploy-prebuilt-image.md` — BYOI: deploy an existing image as a Component + Workload, including Project setup and private-registry variant
- `references/recipes/build-from-source.md` — Build a container image from a Git repo via CI workflow, optional `workload.yaml` descriptor, private-Git and auto-build-on-push variants
- `references/recipes/deploy-and-promote.md` — First-environment deploy, promotion across the pipeline, rollback to a previous release, undeploy / redeploy

Configure
- `references/recipes/configure-workload.md` — Endpoints, env vars, config files, ports/replicas, trait attachment
- `references/recipes/connect-components.md` — Endpoint dependencies (same-project + cross-project) with env-var injection
- `references/recipes/manage-secrets.md` — `SecretReference` patterns, secret-referenced env vars and files, registry / Git auth variants
- `references/recipes/override-per-environment.md` — Per-environment replicas / resources / traits / workload overrides via ReleaseBinding

Operate
- `references/recipes/inspect-and-debug.md` — Status conditions, runtime logs, pod-level events, crashloop investigation, common failure matrix, metrics + traces
- `references/recipes/attach-alerts.md` — `observability-alert-rule` trait, log + metric alerts, per-environment channels, incidents and AI RCA

Long-form developer guide:

- `references/deployment-guide.md` — BYOI, source builds, `workload.yaml`, dependencies, overrides, deployment flow, env-var patterns, third-party-app walkthrough (legacy combined doc; recipes supersede sections of this over time)

YAML templates referenced from recipes live in `assets/`. Copy and edit; the values flow into the matching `workload_spec` / Component spec on the relevant MCP `create_*` / `update_*` call.

When the task crosses into PE-managed capabilities — including SecretReference create and Component trait attachment, which have no MCP write surface — activate `openchoreo-platform-engineer`.

## Discovery-first workflow

### 1. Inspect the repo and classify the app

Start by understanding what is being deployed:

- Services and runtimes
- Dockerfiles and build system
- ports, env vars, and inter-service dependencies
- whether the app fits a simple image-based path or a source-build path

Do not create or patch resources until the application shape is clear.

### 2. Confirm MCP connectivity and scope

Before reasoning about app resources, verify the MCP servers respond and you know the working scope:

- `list_namespaces`
- `list_projects` for the target namespace

If the control-plane MCP server is not reachable, that's a setup problem outside this skill — flag it and stop.

### 3. Discover only what this task needs

Use focused discovery via MCP instead of broad inventory:

- existing project, component, or release binding when names are known (`get_component`, `get_release_binding`)
- available ComponentTypes only if you need to create or change the type (`list_cluster_component_types`, `get_cluster_component_type_schema`)
- available Workflows only if this is a source build (`list_cluster_workflows`, `get_cluster_workflow_schema`)
- environments and deployment pipelines only if deployment or promotion depends on them (`list_environments`, `list_deployment_pipelines`)

If the component already exists, inspect it (`get_component`, `get_workload`) before reauthoring.

### 4. Fetch schemas before authoring resource specs

Before writing a `workload_spec`, Component spec, or override payload, fetch the relevant schema:

- `get_workload_schema`
- `get_cluster_component_type_schema`
- `get_cluster_trait_schema`

For existing resources, read the current spec via `get_*` before sending an `update_*`. `update_workload` sends the full spec, not a partial patch — modifying locally then writing back is the canonical loop.

### 5. Verify with live app evidence

Use MCP to verify, in this order of specificity:

- `get_component` — `status.conditions[]`
- `get_release_binding` — per-environment readiness, deployed URLs
- `query_component_logs` — runtime logs
- `query_workflow_logs` — build logs (source-build path)

Trust deployed URLs and endpoint details from `ReleaseBinding.status.endpoints[]` rather than constructing them by hand.

## Stable guardrails

Keep these because they are durable and routinely useful:

- All work goes through the MCP servers. If a task can't be done with MCP, it crosses the PE boundary; activate `openchoreo-platform-engineer`.
- `get_component` / `get_workload` / `get_release_binding` return spec + status (including `status.conditions[]`) and are the primary debugging tools.
- Prefer schema-fetched specs and repo samples over hand-written first drafts. `get_workload_schema`, `get_cluster_component_type_schema`, and `get_cluster_trait_schema` are cheap.
- Source-build Components use `spec.workflow`; `workload.yaml` belongs at the root of the selected `appPath`. **The build auto-generates the Workload as `{component}-workload`** — do NOT call `create_workload` for source-build components. To enrich the workload's endpoints / dependencies / env vars: preferred path is edit `workload.yaml` in the repo and rebuild; fallback is `update_workload` against the existing `{component}-workload` name (only when rebuilding isn't possible).
- Use ReleaseBinding status for the actual deployed URLs.
- When platform capabilities are missing or broken — or when an operation has no MCP write surface (SecretReference create, Component `spec.traits[]` attachment, hard delete of Component/Workload/ReleaseBinding/Project/Namespace) — escalate clearly or activate `openchoreo-platform-engineer`.
- **For third-party/public apps: default to pre-built images (BYO), not source builds.** Source builds commonly fail because third-party Dockerfiles use multi-platform syntax (`ARG BUILDPLATFORM`) that OpenChoreo's buildah builder does not support. If a build exits 125 with a `BUILDPLATFORM` error, switch to BYO immediately.
- **Before deploying any third-party app: fetch the official Kubernetes or Helm manifests** and extract every required env var per service — dependencies inject service addresses but do not provide `PORT`, feature flags, or vendor SDK disable flags.
- **`create_component` without `workflow` for BYO image deployments** — adding a workflow to a BYO component causes unnecessary failed builds. Then call `create_workload` to define the runtime spec.
- **For source-build (Component with `spec.workflow`): never call `create_workload`** — the build auto-generates `{component}-workload`. Use `update_workload` only to patch the auto-generated workload after the build, when the repo has no `workload.yaml`.
- **`dependencies` in workload spec is an object containing an `endpoints` array** — `dependencies.endpoints[]`, not flat `dependencies[]`. Each entry uses `name` (the target endpoint name on the dependency component), not `endpoint`. Field renamed from `connections` in v1.0.0.
- **Cloud-native apps often bundle vendor SDKs** (profilers, tracers, exporters) that crash outside their target cloud. If a service crash-loops before logging "listening on port X", look for a native module load error and apply the relevant disable flag from the official manifests.

## Escalation rule

When you hit a PE-owned issue, state it directly and make the ask concrete:

"To do X, we need Y configured on the platform side. Please ask the platform engineering team to Z."

Activate `openchoreo-platform-engineer` for the full PE escalation surface and resource taxonomy.

## Anti-patterns

- Running every discovery call before checking the resource already implicated
- Writing Components or overrides from memory when `get_*_schema` and `get_*` MCP calls can reveal the current shape
- Reusing old examples without checking the current workflow and schema model
- Guessing deployed URLs or route formats instead of reading `ReleaseBinding.status.endpoints[]`
- Treating a platform-side failure as an app-only problem after MCP evidence (status conditions, resource events, logs) points elsewhere
- Creating source-build components (with `workflow`) for third-party apps that have pre-built images — this produces failed builds and clutters the UI; always check for pre-built images first
- Omitting env vars from official manifests when deploying third-party apps — always fetch and apply the exact env vars the upstream manifests specify (`PORT`, feature flags, vendor SDK disable flags)
- Assuming a deployment is healthy because `status: Ready` without checking application logs — a crash-looping container can briefly appear Ready; always confirm with `query_component_logs`
- Putting connection entries directly under `dependencies:` as a flat list — the canonical shape is `dependencies.endpoints: [...]`, with `name` for the target endpoint (not `endpoint`)
- Assuming dependency-injected service addresses are the only env vars needed — many apps also require `PORT`, telemetry disable flags, and optional service placeholders to start cleanly
- Trying to run shell commands (`occ`, `kubectl`) from this skill — those operations are out of scope. Either an MCP tool exists for it, or it belongs in `openchoreo-platform-engineer`.
