---
name: propose-pod-security-standards
description: Propose Kubernetes Pod Security Standards (privileged/baseline/restricted) per namespace; identify violating workloads and remediations.
---

# propose-pod-security-standards

> Roll out PSS at the namespace level. Output is the labels to apply + the workloads that need fixes first.

## When to use

- A cluster has no Pod Security configured.
- A team wants to graduate a namespace from `baseline` to `restricted`.
- A workflow needs a security gate before workloads land in shared namespaces.

## The three levels

- **Privileged** — no restrictions. Reserved for system workloads (kube-system).
- **Baseline** — minimum prevention of known privilege escalations. Blocks `hostNetwork`, `hostPID`, privileged containers, `hostPath` (mostly), and similar.
- **Restricted** — security-best-practices. Requires `runAsNonRoot`, drops all capabilities, `readOnlyRootFilesystem`, `seccompProfile: RuntimeDefault`, and more.

## Procedure

1. **Per namespace, decide target level**:
   - Application namespaces → `restricted`.
   - Shared-service namespaces with operators that need privileged pods → `baseline` *if and only if* the operator workloads are isolated; otherwise lift them to their own privileged namespace.
   - `kube-system` and node-agent namespaces → `privileged` (no choice).
2. **Apply labels** on the Namespace:

   ```yaml
   metadata:
     labels:
       pod-security.kubernetes.io/enforce: restricted
       pod-security.kubernetes.io/enforce-version: latest
       pod-security.kubernetes.io/audit: restricted
       pod-security.kubernetes.io/warn: restricted
   ```

   Use `audit` + `warn` first to get a report before flipping `enforce`.
3. **Find violators** — list pods in the namespace and check each container's spec against the target level. The common gaps moving from `baseline → restricted`:
   - `runAsNonRoot: true` not set.
   - `readOnlyRootFilesystem: true` not set.
   - `capabilities.drop: [ALL]` not set.
   - `seccompProfile.type: RuntimeDefault` not set.
   - `allowPrivilegeEscalation: false` not set.
4. **Remediate** — patch each workload's `securityContext`. For workloads that genuinely need a capability (e.g. `NET_BIND_SERVICE` to bind <1024), document the exception in an ADR and grant only that capability.
5. **Verify** — re-list pods; `kubectl get pods -A | grep -i warn` should be empty for the target namespace after the `enforce` flip.

## Output

```text
PSS rollout: payments namespace

Target: restricted

Audit pass — violators:
  - refund (Deployment)
      missing: runAsNonRoot, readOnlyRootFilesystem, capabilities.drop:[ALL]
      Fix: add securityContext block (see write-manifest skill).
  - billing-job (CronJob)
      missing: seccompProfile RuntimeDefault, allowPrivilegeEscalation: false
      Fix: add the two fields to the job template's container.
  - legacy-cron (CronJob)
      requires CAP_NET_RAW (ping-based health checks).
      Remediation: convert to a different health-check mechanism; or
                   ADR + move to a baseline namespace.

Step 1 — label namespace audit+warn=restricted. 1 week observation.
Step 2 — fix refund + billing-job; ADR for legacy-cron.
Step 3 — flip enforce=restricted.
```

## Anti-patterns to avoid

- Going straight to `enforce` without an `audit/warn` shakedown.
- Granting `privileged: true` "temporarily" to unblock a deploy.
- Mixing `restricted` and `privileged` workloads in the same namespace.
