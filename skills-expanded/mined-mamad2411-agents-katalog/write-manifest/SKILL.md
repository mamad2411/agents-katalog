---
name: write-manifest
description: Write a Kubernetes Deployment + Service + PDB manifest with safe defaults — resource requests/limits, probes, security context, topology spread.
---

# write-manifest

> Author a Kubernetes manifest set that runs safely from day one.

## When to use

- A new workload needs k8s manifests.
- An existing manifest is missing probes, resources, or security context.

## Inputs

- Workload name + image + replica count.
- Port the container listens on.
- HTTP health endpoint (if any).
- Namespace.

## Procedure

1. **Minimum useful set**: `Deployment` + `Service` + `PodDisruptionBudget`. Add `HorizontalPodAutoscaler` only when you have a metric to scale on; otherwise it's noise.
2. **Resource requests/limits** — required:
   - `requests.cpu` controls scheduling.
   - `requests.memory` controls scheduling.
   - `limits.memory` — set equal to or slightly above requests (CPU limits are usually counterproductive for latency-sensitive workloads).
3. **Probes**:
   - `readinessProbe` — gate traffic. Fail-fast so unhealthy pods are removed from endpoints.
   - `livenessProbe` — restart on hang. Use a separate, very cheap endpoint or omit; restarting under load can amplify outages.
   - `startupProbe` — for slow boots; lets liveness/readiness use shorter intervals.
4. **Security context** at pod and container:
   - `runAsNonRoot: true`, `runAsUser: 65532` (or workload-specific).
   - `readOnlyRootFilesystem: true` + `emptyDir` for any writable need.
   - `allowPrivilegeEscalation: false`, `capabilities.drop: [ALL]`.
   - `seccompProfile.type: RuntimeDefault`.
5. **PodDisruptionBudget** — `minAvailable: 1` or `maxUnavailable: 25%`, sized to allow node upgrades.
6. **Topology spread** — across zones (or hosts) so a single AZ failure doesn't take you down. `topologySpreadConstraints` with `whenUnsatisfiable: ScheduleAnyway`.
7. **Labels & annotations** — `app.kubernetes.io/name`, `app.kubernetes.io/instance`, owner team, source repo annotation.

## Output

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: refund
  namespace: payments
  labels:
    app.kubernetes.io/name: refund
    app.kubernetes.io/instance: refund
spec:
  replicas: 3
  selector:
    matchLabels:
      app.kubernetes.io/name: refund
  template:
    metadata:
      labels:
        app.kubernetes.io/name: refund
    spec:
      securityContext:
        runAsNonRoot: true
        runAsUser: 65532
        seccompProfile:
          type: RuntimeDefault
      topologySpreadConstraints:
        - maxSkew: 1
          topologyKey: topology.kubernetes.io/zone
          whenUnsatisfiable: ScheduleAnyway
          labelSelector:
            matchLabels:
              app.kubernetes.io/name: refund
      containers:
        - name: refund
          image: example/refund:0.1.0
          ports:
            - containerPort: 8080
              name: http
          readinessProbe:
            httpGet: { path: /healthz, port: http }
            periodSeconds: 5
            timeoutSeconds: 1
          startupProbe:
            httpGet: { path: /healthz, port: http }
            failureThreshold: 30
            periodSeconds: 2
          resources:
            requests: { cpu: 100m, memory: 128Mi }
            limits:   { memory: 256Mi }
          securityContext:
            allowPrivilegeEscalation: false
            readOnlyRootFilesystem: true
            capabilities: { drop: [ALL] }
---
apiVersion: v1
kind: Service
metadata:
  name: refund
  namespace: payments
spec:
  selector:
    app.kubernetes.io/name: refund
  ports:
    - name: http
      port: 80
      targetPort: http
---
apiVersion: policy/v1
kind: PodDisruptionBudget
metadata:
  name: refund
  namespace: payments
spec:
  minAvailable: 1
  selector:
    matchLabels:
      app.kubernetes.io/name: refund
```

## Quality bar

- `requests.cpu` and `requests.memory` set.
- `runAsNonRoot: true` + `readOnlyRootFilesystem: true`.
- `readinessProbe` defined.
- `PodDisruptionBudget` exists.
- Labels follow the recommended `app.kubernetes.io/*` set.

## Anti-patterns to avoid

- CPU limit equal to request on a latency-sensitive workload (throttling kills tail latency).
- `livenessProbe` that hits the same heavy endpoint as `readinessProbe`.
- Missing PDB on a workload that gets evicted during node upgrades.
- Manifest with no `securityContext` defaults to root + writable rootfs.
