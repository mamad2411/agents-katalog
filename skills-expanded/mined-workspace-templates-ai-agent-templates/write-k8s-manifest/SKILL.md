---
name: write-k8s-manifest
description: Writes Deployment, Service and config manifests for a service with probes, resource limits and a rollout that can be undone.
disable-model-invocation: true
---

Write Kubernetes manifests for: $ARGUMENTS (service name; infer it from the repository if empty).

1. Look for existing manifests, Helm charts or kustomize folders and match their layout, labels and naming. Read the app for its port, health route, config variables and startup time.
2. Create a Deployment with the image set to a specific tag (never latest), app.kubernetes.io labels, and a RollingUpdate strategy with maxUnavailable 0 and maxSurge 1.
3. Add readinessProbe, livenessProbe and a startupProbe if boot is slow. Point them at the health route, not at /.
4. Set resource requests and limits with a short note on how you chose the numbers. Add securityContext: runAsNonRoot, readOnlyRootFilesystem where the app allows it.
5. Add a Service, a ConfigMap for non-secret settings, and reference secrets by name only. Never write secret values.
6. Run `kubectl apply --dry-run=client -f <dir>` and, if a cluster is reachable, `--dry-run=server`.

Show the files and the dry-run result. Ask before writing them, and never run `kubectl apply` for real.
