---
name: azure-container-apps-current-deploy-operations
description: Reviews and performs safe Azure Container Apps deployments, revisions, traffic splits, rollbacks, and az containerapp commands. Use when changing images, revisions, rollout strategy, or production ACA resources.
license: MIT
compatibility: Azure Container Apps managed service and Azure CLI containerapp commands.
---

# Azure Container Apps Deploy Operations

This skill helps agents deploy and operate Container Apps safely with revision awareness and explicit rollback planning.

## When to Use

Use this skill when the task involves:

- `az containerapp create`, `update`, `up`, `deploy`, `revision`, `ingress`, `job`, or `env` commands;
- deploying a new image;
- traffic splitting;
- rollback;
- deactivating revisions;
- changing probes, scale, env vars, secrets, identity, or ingress;
- reviewing deployment YAML.

## Deployment Rules

1. Verify subscription, tenant, resource group, app name, environment, and target image.
2. Avoid mutable production tags such as `latest`.
3. Record current revision and traffic split before changing anything.
4. Use multiple revisions and traffic splits when gradual rollout is needed.
5. Keep old known-good revisions active until rollback risk has passed.
6. Confirm health probes and target port before rollout.
7. Validate secret references without printing secret values.
8. Require explicit approval for destructive, production, public-ingress, or secret-changing commands.

## Workflows

Use `workflows/deploy-and-rollback-workflow.md` for a safe deployment or rollback.

## Resources

Use `resources/deployment-safety-checklist.md` before executing deployment commands.

## Examples

Use `examples/traffic-split-rollback-example.md` for traffic split and rollback patterns.

## Scripts

Run `scripts/guard-az-containerapp-command.py --help` before manual use. Antigravity hooks call this script automatically through `hooks.json`.
