---
name: k8s-review
description: MUST USE before kubectl apply — manifest/Helm review, probes, resources, securityContext, RBAC, ingress TLS, CrashLoop/OOM diagnosis. Triggers on K8s deploys, Helm upgrades, pod restarts, or production cluster changes.
---

# Kubernetes Review

Treat manifests as **production contracts**: every Deployment is a promise about availability, security, and blast radius. Review in phases — workload safety, cluster security, operability — with severity and runnable checks.

## When This Skill Applies

- New manifests, Helm charts, Kustomize overlays
- Pods CrashLoopBackOff, OOMKilled, ImagePullBackOff
- Pre-prod cluster upgrade or ingress change
- Multi-tenant cluster sharing namespaces
- GitOps PR (Argo CD / Flux) changing live paths

## Severity Model

| Level | Signal | Gate |
|-------|--------|------|
| **K0** | `privileged`, hostPath secrets, cluster-admin bindings, `latest` prod tag, plaintext secrets in manifest | Block apply |
| **K1** | Missing probes/limits, runAsRoot, wide NetworkPolicy allow-all, no PDB | Fix before traffic |
| **K2** | Suboptimal requests/limits, missing topology spread, verbose RBAC | Same release train |
| **K3** | Labels/annotations hygiene | Backlog |

Cross-ref: `docker-audit` for image source; `terraform-review` for cluster/IAM; `observability` for traces/metrics; `backup-restore` for etcd/Velero.

## Phase 0 — Context & Blast Radius

```bash
kubectl config current-context
kubectl get ns
kubectl get deploy,sts,ds -A --no-headers | wc -l
```

Identify: namespace, env (prod/stage), change type (new vs patch), rollback owner.

## Phase 1 — Workload Correctness

### 1.1 Pod spec essentials

- [ ] `resources.requests` and `limits` set (CPU/mem); limits ≥ requests
- [ ] **Liveness** vs **readiness** distinct — liveness not hitting DB
- [ ] `startupProbe` for slow-start apps (JVM, heavy migrations)
- [ ] `terminationGracePeriodSeconds` matches drain time; `preStop` hook if needed
- [ ] `replicas` ≥2 for HA; `PodDisruptionBudget` for voluntary disruptions
- [ ] `imagePullPolicy: IfNotPresent` dev; digest or immutable tag in prod

### 1.2 Configuration

- [ ] ConfigMaps for non-secret config; Secrets from ESO/SealedSecrets/Vault — not git plaintext
- [ ] Env from secret keys referenced, not duplicated in ConfigMap
- [ ] Versioned migrations run as Job/CronJob with backoff — not only initContainer without guard

```bash
kubectl apply --dry-run=server -f deploy/
helm template release ./chart | kubectl apply --dry-run=server -f -
kubeconform -summary deploy/*.yaml  # or kubeval
```

## Phase 2 — Security Hardening (2025–2026)

### 2.1 Pod security

- [ ] `securityContext`: `runAsNonRoot: true`, `readOnlyRootFilesystem: true` where feasible
- [ ] `allowPrivilegeEscalation: false`; drop ALL caps
- [ ] No `hostNetwork` / `hostPID` unless CNI/monitoring exception documented
- [ ] **Pod Security Standards** enforced at namespace: baseline/restricted

### 2.2 RBAC & identity

- [ ] ServiceAccount per app; no default SA for prod workloads
- [ ] Role bindings least privilege — not `cluster-admin` for apps
- [ ] IRSA/GKE workload identity for cloud API access — no long-lived cloud keys in Secrets

### 2.3 Network

- [ ] NetworkPolicy default-deny + explicit egress to DNS and dependencies
- [ ] Ingress TLS (cert-manager or managed cert); HSTS at edge
- [ ] mTLS service mesh only where justified — document ops cost

```bash
kubectl auth can-i --list --as=system:serviceaccount:ns:sa-name -n ns
```

## Phase 3 — Reliability & Scale

- [ ] HPA/VPA or KEDA scalers with sane min/max
- [ ] Anti-affinity / topology spread for zone failure
- [ ] Rolling update: `maxUnavailable`/`maxSurge` safe for state
- [ ] StatefulSet: stable network ID, ordered rollout, backup for PVCs

## Phase 4 — Live Diagnosis Commands

```bash
kubectl get pods -n NAMESPACE -o wide
kubectl describe pod POD -n NAMESPACE | tail -40
kubectl logs POD -n NAMESPACE --previous --tail=100
kubectl top pod -n NAMESPACE
kubectl get events -n NAMESPACE --sort-by='.lastTimestamp' | tail -20
```

| Symptom | First checks |
|---------|----------------|
| CrashLoop | `logs --previous`, exit code, missing env, migration failure |
| OOMKilled | Raise mem limit or fix leak; check JVM `-Xmx` |
| ImagePullBackOff | tag exists, pull secret, registry IAM |
| Pending | quotas, taints, PVC binding, insufficient CPU |

## Phase 5 — GitOps & Policy Gates

- OPA/Gatekeeper or Kyverno: block `:latest`, require limits, require probes
- CI: `helm lint`, `kube-score`, `polaris`, dry-run server-side apply
- Record chart/app version in change ticket

Cross-ref: `ci-fix` to wire policy checks in Actions.

## Output Template

```markdown
## K8s Review: [app/chart]

**Cluster/context:** ... | **Namespace:** ... | **Verdict:** ✅ / 🔶 / ❌

### Change summary
- Resources touched: Deployments, Ingress, ...

### Findings
| ID | Sev | Resource | Issue | Fix (YAML snippet) |

### Pre-apply checklist
- [ ] dry-run server passed
- [ ] rollback: `kubectl rollout undo deploy/...`
- [ ] PDB/HPA reviewed

### Live diagnosis (if incident)
- Symptom:
- Evidence:
- Mitigation:

### Follow-ups
- [ ] `observability` — RED metrics + traces
- [ ] `cost-optimize` — requests vs actual usage
```

## Anti-Patterns

- **Copy-paste YAML from tutorials** — no limits, `latest`, default SA
- **Liveness hits `/health` that includes DB** — restart storms during DB blip
- **Giant ConfigMap** — use external config or split
- **Manual kubectl edit in prod** — drift from git; fix GitOps source
- **Shared namespace** prod+dev — RBAC and quota nightmares

## Cross-References

| Skill | Use when |
|-------|----------|
| `docker-audit` | Image build issues |
| `terraform-review` | EKS/GKE module changes |
| `monitoring-check` | Prometheus rules for pods |
| `backup-restore` | Velero, PVC snapshots |
| `incident-response` | Sev1 outage (engineering plugin) |

## Cursor Kit Templates

- `kubernetes` — baseline Deployments, ingress, cert-manager
- `monitoring` — ServiceMonitor patterns
- `ci-cd` — deploy workflow with rollout wait

## Extended Reference — Operational Drill

Run this drill when the skill triggers in production (not only doc review):

1. **Capture evidence first** — commands, screenshots, log lines with timestamps; do not change prod before snapshot.
2. **Classify severity** using this skill's table; if between two levels, choose the higher until disproved.
3. **Apply the smallest fix** that addresses root cause; avoid drive-by refactors in the same change.
4. **Verify with the same command** that failed before; add automated guard (CI rule, test, alert).
5. **Record in output template** and link follow-up skills from Cross-References.

## Extended Reference — Runnable Sanity Pack

```bash
# Repository context (adapt paths)
git status -sb
git log -3 --oneline
# Replace SVC with your service name
test -f docker-compose.yml && docker compose ps
test -f package.json && npm run -s test 2>&1 | tail -5
```

## Extended Reference — Stakeholder Comms

| Severity | Who to inform | Channel | SLA |
|----------|---------------|---------|-----|
| Blocker | On-call / founder | incident chat | <15m |
| High | Team lead | ticket comment | same day |
| Medium | PR reviewer | PR description | this sprint |
| Low | backlog | deferred list | next review |

## Extended Reference — Definition of Done

- [ ] Output template filled completely
- [ ] Severity assigned per finding with fix snippet
- [ ] Cross-skill follow-ups checked or N/A with reason
- [ ] No secrets pasted into notes or tickets
- [ ] Re-run key verification command after fix

## Extended Reference — 2025–2026 Practice Notes

- Prefer **automation in CI** over manual checklist repetition for this domain.
- Pair **metrics/alerts** with any production change recommended here (`observability` where applicable).
- Document **rollback** in the same PR/issue as the forward fix.
- Keep playbooks **versioned in git** — when process changes, update this SKILL in the same PR.

## Extended Reference — Common Questions

**Q: How long should this review take?**  
A: Time-box discovery (15–30m), then fix loop. If stuck without new evidence, switch to `diagnose-bugs` or `research`.

**Q: Can we waive a blocker?**  
A: Only with written accept + expiry date + compensating control; never silent waive.

**Q: What if tools are missing locally?**  
A: Run what you can; document gaps in "Commands run" with install note — do not skip severity classification.

## Extended Reference — Finding ID Convention

Use stable IDs in reports: `[SKILL]-001`, increment per session. Refer to IDs in PR comments for traceability.

## Extended Reference — Pair Review

For S0/A0/T0 class issues, second person validates reproduction steps before merge when team size allows.

