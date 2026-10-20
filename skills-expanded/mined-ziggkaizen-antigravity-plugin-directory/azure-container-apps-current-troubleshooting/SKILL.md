---
name: azure-container-apps-current-troubleshooting
description: Troubleshoots Azure Container Apps incidents, failed revisions, image pull errors, startup failures, ingress issues, health probes, logs, scale-to-zero, and degraded replicas. Use during ACA debugging or incident response.
license: MIT
compatibility: Azure Container Apps managed service, current Microsoft Learn guidance.
---

# Azure Container Apps Troubleshooting

This skill guides debugging and incident triage for Container Apps.

## When to Use

Use this skill when the task involves:

- failed or degraded revisions;
- app not responding;
- HTTP 403 or ingress problems;
- image pull failures;
- container crashes;
- health probe failures;
- missing logs;
- scale-to-zero confusion;
- job execution failures;
- scaler metric errors.

## Triage Principles

1. Capture state before changing it.
2. Check revision state first.
3. Review system logs and console logs.
4. Verify image pull access and image tag.
5. Verify startup command, target port, and probes.
6. Verify ingress mode, IP restrictions, auth, and traffic split.
7. Verify scale rules and minimum replicas.
8. Make reversible changes during incidents.

## Workflows

Use `workflows/incident-triage-workflow.md` for incident response.

## Resources

Use `resources/troubleshooting-runbook.md`.

## Examples

Use `examples/log-query-examples.md` for CLI and Log Analytics examples.
