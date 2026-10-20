---
name: azure-container-apps-current-app-design
description: Designs Azure Container Apps applications and environments. Use when planning app boundaries, ingress, health probes, configuration, managed identity, registry access, YAML shape, or service-to-service communication.
license: MIT
compatibility: Azure Container Apps managed service, current Microsoft Learn guidance.
---

# Azure Container Apps App Design

This skill helps agents design app and environment configuration for Azure Container Apps without assuming a specific runtime, CI/CD system, or IaC provider.

## When to Use

Use this skill when the task involves:

- creating a new container app design;
- deciding public vs internal ingress;
- defining health probes, target ports, and environment variables;
- planning managed environment boundaries;
- assigning managed identity;
- designing service-to-service communication;
- reviewing exported Container Apps YAML;
- choosing whether a workload should be a container app or a job.

## Design Principles

1. Start with workload type: long-running app, HTTP API, worker, event-driven consumer, or finite job.
2. Decide exposure: public internet, VNet/internal, environment-only, or no ingress.
3. Define target port, protocol, transport, CORS, auth, IP restrictions, and mTLS before enabling external ingress.
4. Define secrets as references, not inline values.
5. Prefer managed identity for Azure resource access and private ACR pulls.
6. Set health probes according to actual startup, readiness, and liveness behavior.
7. Set CPU/memory and min/max replicas from evidence, not defaults alone.
8. Keep Container Apps service design separate from IaC-provider-specific syntax unless the repository requires a provider-specific plugin.

## Workflows

Use `workflows/design-container-app-workflow.md` when designing or reviewing a new Container App configuration.

## Resources

Use `resources/app-design-checklist.md` for design review.

## Examples

Use `examples/containerapp-yaml-example.md` for a conservative YAML shape.

## Script Guidance

This skill has no scripts.
