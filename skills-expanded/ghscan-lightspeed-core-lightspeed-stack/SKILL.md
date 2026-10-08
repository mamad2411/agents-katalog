---
name: openshift-troubleshooting
description: Diagnose and fix common OpenShift deployment issues including pod failures, networking problems, and resource constraints. Use when users report deployment failures or application issues on OpenShift.
---

# OpenShift Troubleshooting

## When to use this skill

Use this skill when:
- A user reports pods not starting or crashing
- Deployments are stuck in pending state
- Services are unreachable
- Resource quota issues are suspected

## Diagnostic steps

### 1. Check pod status

First, identify the problematic pods:

```
oc get pods -n <namespace> | grep -v Running
```

For each failing pod, get detailed status:

```
oc describe pod <pod-name> -n <namespace>
```

Look for:
- **Pending**: Usually resource constraints or scheduling issues
- **CrashLoopBackOff**: Application crash, check logs
- **ImagePullBackOff**: Image registry access issues
- **ErrImagePull**: Image not found or auth failure

### 2. Check events

```
oc get events -n <namespace> --sort-by='.lastTimestamp'
```

Events reveal scheduling failures, resource limits, and pull errors.

### 3. Check logs

```
oc logs <pod-name> -n <namespace>
oc logs <pod-name> -n <namespace> --previous  # For crashed pods
```

### 4. Check resource constraints

```
oc describe resourcequota -n <namespace>
oc describe limitrange -n <namespace>
```

## Common issues and solutions

See [references/common-errors.md](references/common-errors.md) for detailed solutions to frequently encountered errors.

## Escalation

If the issue cannot be resolved with the steps above:
1. Collect the output from all diagnostic commands
2. Check if the issue is cluster-wide or namespace-specific
3. Review recent changes to deployments or cluster configuration
