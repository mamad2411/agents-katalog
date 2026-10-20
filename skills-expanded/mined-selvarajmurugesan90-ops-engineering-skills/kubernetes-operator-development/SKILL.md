---
name: kubernetes-operator-development
description: >
  Guides building Kubernetes Operators with Kubebuilder or the Operator
  SDK — CustomResourceDefinition (CRD) API design, controller
  scaffolding, the reconciliation loop pattern, status/conditions
  reporting, finalizers for cleanup, and testing with envtest. Use when
  a user asks to "build a Kubernetes Operator," "design a CRD," "write a
  reconcile loop," "add a finalizer to my controller," "test a
  controller with envtest," or "package an Operator for OLM."
license: Apache-2.0
compatibility: "Claude Code, GitHub Copilot, OpenAI Codex, Cursor, Gemini CLI"
metadata:
  domain: kubernetes-platform
  maturity: stable
---

# Kubernetes Operator Development

## Purpose

An Operator encodes operational knowledge — how to provision, upgrade,
back up, and heal an application — as a Kubernetes controller watching a
custom resource, so operating that application becomes "apply a YAML
spec" instead of a runbook. Building one wrong (a reconcile loop that
isn't idempotent, a CRD with no versioning strategy, a controller that
never terminates finalizers) produces a system that appears to work in
demos and then deadlocks, leaks resources, or corrupts state under real
concurrent load. This skill covers designing the CRD API and writing a
reconciliation loop that is safe to run continuously against a live
cluster.

## When to use

- Deciding whether a problem genuinely needs an Operator (ongoing
  day-2 lifecycle management) versus a Helm chart or Job being
  sufficient.
- Designing a new CRD's `spec`/`status` schema, including which fields
  are user-desired-state vs. controller-observed-state.
- Scaffolding a new controller with Kubebuilder or Operator SDK.
- Writing or reviewing a `Reconcile()` function for correctness
  (idempotency, requeue behavior, error handling).
- Adding a finalizer so external resources are cleaned up before the
  custom resource is deleted.
- Testing a controller against `envtest`/`kind` instead of only manual
  cluster testing.
- Packaging an Operator for distribution via OLM (Operator Lifecycle
  Manager) on OpenShift or other OLM-enabled clusters.

## Prerequisites & environment

- Go ≥ 1.22 (Kubebuilder and Operator SDK's Go-based scaffolding track
  current Go releases; check the scaffolding tool's compatibility matrix
  before pinning an older Go version).
- Kubebuilder ≥ 3.14 or Operator SDK ≥ 1.34, both built on
  `controller-runtime` (the version of `controller-runtime` pulled in
  determines available features like server-side apply support and
  workqueue rate limiting defaults — check `go.mod` after scaffolding).
- `kubectl` and a disposable cluster (`kind` or `minikube`) for manual
  verification; `envtest` (bundled via `setup-envtest`) for running
  reconcile tests against a real API server + etcd without a full
  kubelet/scheduler, in CI.
- RBAC to install CRDs and the controller's own ServiceAccount
  permissions (cluster-admin is *not* required to develop against a
  personal dev cluster, but is commonly needed to install CRDs
  cluster-wide the first time).
- If targeting OpenShift/ROSA distribution, familiarity with OLM
  bundle format — see
  [openshift-and-rosa-platform](../openshift-and-rosa-platform/SKILL.md).

## Step-by-step guidance

1. **Confirm an Operator is the right tool.** If the task is "run this
   once" (a migration, a one-time provisioning step), a Job or a CI
   pipeline step is simpler and has no ongoing failure mode to maintain.
   Build an Operator when there's genuine *ongoing* reconciliation work:
   the desired state can drift from actual state over time and needs
   continuous correction (e.g. managing a clustered database's topology,
   rotating credentials, scaling based on custom metrics).

2. **Scaffold the project and API**:
   ```bash
   kubebuilder init --domain example.com --repo github.com/example/cache-operator
   kubebuilder create api --group cache --version v1alpha1 --kind RedisCluster --resource --controller
   ```

3. **Design the CRD spec/status split explicitly** — `spec` is
   user-declared desired state; `status` is controller-observed actual
   state, and only the controller should ever write to `status`:
   ```go
   type RedisClusterSpec struct {
       // +kubebuilder:validation:Minimum=1
       // +kubebuilder:validation:Maximum=15
       Replicas int32 `json:"replicas"`

       // +kubebuilder:validation:Enum=Standard;HighMemory
       // +kubebuilder:default=Standard
       Tier string `json:"tier,omitempty"`
   }

   type RedisClusterStatus struct {
       ObservedGeneration int64              `json:"observedGeneration,omitempty"`
       Phase              string             `json:"phase,omitempty"`
       Conditions         []metav1.Condition `json:"conditions,omitempty"`
   }
   ```
   Start the API at `v1alpha1` — it signals "no compatibility guarantee
   yet" and gives room to fix schema mistakes before committing to
   `v1beta1`/`v1` conversion webhooks.

4. **Write the reconcile loop as idempotent and level-triggered**, never
   assuming it runs exactly once per change:
   ```go
   func (r *RedisClusterReconciler) Reconcile(ctx context.Context, req ctrl.Request) (ctrl.Result, error) {
       var rc cachev1alpha1.RedisCluster
       if err := r.Get(ctx, req.NamespacedName, &rc); err != nil {
           return ctrl.Result{}, client.IgnoreNotFound(err)
       }

       if !rc.DeletionTimestamp.IsZero() {
           return r.reconcileDelete(ctx, &rc)
       }
       if !controllerutil.ContainsFinalizer(&rc, redisFinalizer) {
           controllerutil.AddFinalizer(&rc, redisFinalizer)
           if err := r.Update(ctx, &rc); err != nil {
               return ctrl.Result{}, err
           }
       }

       desired := buildStatefulSet(&rc)
       var current appsv1.StatefulSet
       err := r.Get(ctx, client.ObjectKeyFromObject(desired), &current)
       switch {
       case apierrors.IsNotFound(err):
           if err := ctrl.SetControllerReference(&rc, desired, r.Scheme); err != nil {
               return ctrl.Result{}, err
           }
           if err := r.Create(ctx, desired); err != nil {
               return ctrl.Result{}, err
           }
       case err != nil:
           return ctrl.Result{}, err
       default:
           if !equalSpec(current.Spec, desired.Spec) {
               current.Spec = desired.Spec
               if err := r.Update(ctx, &current); err != nil {
                   return ctrl.Result{}, err
               }
           }
       }

       rc.Status.ObservedGeneration = rc.Generation
       rc.Status.Phase = derivePhase(current)
       if err := r.Status().Update(ctx, &rc); err != nil {
           return ctrl.Result{}, err
       }
       return ctrl.Result{RequeueAfter: 30 * time.Second}, nil
   }
   ```
   Every branch either returns an error (triggering exponential-backoff
   requeue from the workqueue) or a deterministic result — never a
   silent no-op that leaves drift uncorrected.

5. **Use finalizers for any resource with external side effects** that
   must be cleaned up before Kubernetes garbage-collects the object
   (external cloud resources, DNS records, other clusters' state):
   ```go
   const redisFinalizer = "cache.example.com/cleanup"

   func (r *RedisClusterReconciler) reconcileDelete(ctx context.Context, rc *cachev1alpha1.RedisCluster) (ctrl.Result, error) {
       if err := deprovisionExternalBackupBucket(ctx, rc); err != nil {
           return ctrl.Result{}, err  // finalizer stays, delete is retried
       }
       controllerutil.RemoveFinalizer(rc, redisFinalizer)
       return ctrl.Result{}, r.Update(ctx, rc)
   }
   ```
   > **Warning:** if a finalizer's cleanup logic can never succeed (a
   > bug, a permanently unreachable external system, or the finalizer
   > string itself was mistyped/orphaned), the custom resource — and
   > anything Kubernetes-garbage-collection-blocked behind it — becomes
   > stuck in `Terminating` forever. Recovering requires manually
   > patching out the finalizer (`kubectl patch ... -p '{"metadata":{"finalizers":[]}}' --type=merge`),
   > which skips the cleanup the finalizer existed to guarantee — treat
   > this as an incident, not a routine unstick command, and confirm the
   > external resource really doesn't need manual cleanup first.

6. **Report status via `status.conditions`**, not just a free-text phase
   string, so other tooling (dashboards, `kubectl wait --for=condition=`)
   can consume it reliably:
   ```go
   meta.SetStatusCondition(&rc.Status.Conditions, metav1.Condition{
       Type:               "Ready",
       Status:             metav1.ConditionTrue,
       Reason:             "AllReplicasAvailable",
       Message:            "3/3 replicas ready",
       ObservedGeneration: rc.Generation,
   })
   ```

7. **Test with `envtest`** before relying on manual `kind` testing for
   every change:
   ```go
   var _ = Describe("RedisCluster controller", func() {
       It("creates a StatefulSet matching spec.replicas", func() {
           rc := &cachev1alpha1.RedisCluster{ /* ... */ Spec: cachev1alpha1.RedisClusterSpec{Replicas: 3} }
           Expect(k8sClient.Create(ctx, rc)).To(Succeed())
           Eventually(func() int32 {
               var sts appsv1.StatefulSet
               _ = k8sClient.Get(ctx, client.ObjectKeyFromObject(rc), &sts)
               return *sts.Spec.Replicas
           }).Should(Equal(int32(3)))
       })
   })
   ```
   ```bash
   make test   # runs envtest-backed suite via ginkgo
   ```

8. **Install the CRD and run the controller against a `kind` cluster**
   before shipping:
   ```bash
   make install   # kubectl apply -f config/crd
   make run       # runs the controller locally against the cluster's API server
   ```

9. **Package for distribution.** For a plain chart-based install, wrap
   `config/crd` + `config/rbac` + `config/manager` into a Helm chart
   (see [helm-chart-authoring](../helm-chart-authoring/SKILL.md),
   putting CRDs under the chart's `crds/` directory since Helm never
   upgrades or deletes files there automatically). For OLM-based
   distribution (OpenShift), use `operator-sdk generate bundle` to
   produce a `ClusterServiceVersion` and bundle image.

## Best practices

- Make `Reconcile` fully re-entrant and safe to call with stale or
  duplicate events — controller-runtime's workqueue coalesces and
  retries events, so "reconcile ran twice for one change" is normal, not
  a bug to work around with external locking.
- Always check `ObservedGeneration` vs. `.metadata.generation` before
  reporting a condition as current, so a status update from a stale
  reconcile of an already-superseded spec doesn't overwrite a newer
  status.
- Use `SetControllerReference`/owner references on every child resource
  the controller creates, so Kubernetes garbage-collects children
  automatically when the parent custom resource is deleted (except
  where a finalizer intentionally intercepts deletion first for external
  cleanup).
- Rate-limit and cap requeues on persistent errors (`controller-runtime`
  does this by default with exponential backoff) rather than hot-looping
  reconciliation against a failing dependency.
- Keep CRD versions and conversion webhooks in mind from `v1alpha1`
  onward even if you don't need a webhook yet — plan which fields could
  need renaming, and prefer additive changes to avoid a conversion
  webhook becoming mandatory later.
- Scope RBAC in `config/rbac` to exactly the resources/verbs the
  controller touches (`kubebuilder:rbac` markers) instead of granting
  the controller's ServiceAccount cluster-admin "to be safe" — an
  over-privileged controller is a top attack-surface risk in clusters
  running third-party Operators.

## Common pitfalls

- **Symptom:** The controller works in testing but under real load
  starts making conflicting writes / `409 Conflict` errors on `Update`.
  **Fix:** Missing optimistic-concurrency handling. Re-`Get` the object
  and retry on conflict (`client.IgnoreNotFound` + a retry helper like
  `retry.RetryOnConflict`) rather than treating every `Update` as
  guaranteed to succeed against the resource version last read.

- **Symptom:** Deleting the custom resource hangs indefinitely; `kubectl
  get` shows it stuck with a `deletionTimestamp` set but the object
  never disappears.
  **Fix:** A finalizer's cleanup path is erroring out (check controller
  logs) or was left on the object by a previous controller version that
  no longer exists to remove it. Fix the underlying cleanup failure
  first; only manually patch the finalizer list as a last resort, and
  only after confirming external resources don't need the cleanup that
  finalizer guaranteed.

- **Symptom:** Deleting the CRD itself (`kubectl delete crd
  redisclusters.cache.example.com`) cascades to delete every
  `RedisCluster` custom resource across every namespace, and their owned
  StatefulSets/PVCs along with them.
  **Fix:** This is expected Kubernetes behavior — deleting a CRD deletes
  all its instances. > **Warning:** never delete a CRD as a
  troubleshooting step on a production cluster; it is equivalent to
  deleting every resource of that kind cluster-wide. Confirm no
  instances exist (`kubectl get <kind> -A`) or explicitly accept the
  data-loss blast radius before proceeding.

- **Symptom:** Two reconciler replicas (run for HA) both act on the same
  resource simultaneously, causing duplicate child-resource creation.
  **Fix:** Controller-runtime managers use leader election
  (`--leader-elect=true`) to ensure only one replica reconciles at a
  time; confirm it's enabled in the manager setup and that the
  Lease-based leader election RBAC/permissions are actually granted —
  a manager silently failing to acquire the lease due to missing RBAC
  can otherwise leave *no* active reconciler rather than duplicating
  work, which looks like the controller "randomly stopped working."

- **Symptom:** A schema change to the CRD (renaming a spec field) breaks
  every existing custom resource instance in the cluster after upgrade.
  **Fix:** CRD schema changes are not automatically migrated. Add a new
  field alongside the old one, dual-read in the controller for one
  release, and only remove the old field after all instances have been
  migrated (a conversion webhook is the safe path for a true rename
  across API versions instead of an in-place field rename).

## Worked example

**Scenario:** A `RedisCluster` CRD that reconciles a StatefulSet and
reports readiness via conditions, packaged for `kind` testing.

```yaml
# config/samples/cache_v1alpha1_rediscluster.yaml
apiVersion: cache.example.com/v1alpha1
kind: RedisCluster
metadata:
  name: sessions-cache
spec:
  replicas: 3
  tier: Standard
```

```bash
make manifests generate    # regenerate CRD YAML + deepcopy funcs from markers
kind create cluster --name operator-dev
make install               # apply CRDs
make run &                 # run the controller against kind, out-of-cluster
kubectl apply -f config/samples/cache_v1alpha1_rediscluster.yaml
kubectl get rediscluster sessions-cache -o jsonpath='{.status.conditions}'
```

Expected status after reconciliation stabilizes:

```json
[{"type":"Ready","status":"True","reason":"AllReplicasAvailable","message":"3/3 replicas ready","observedGeneration":1}]
```

`kubectl get statefulset sessions-cache` shows 3/3 ready replicas, and
`kubectl get statefulset sessions-cache -o jsonpath='{.metadata.ownerReferences}'`
confirms the StatefulSet is owned by the `RedisCluster`, so deleting the
custom resource (once its finalizer's external-cleanup step succeeds)
garbage-collects the StatefulSet and its Pods automatically — though not
its PVCs by default, which is worth calling out explicitly to whoever
deletes a `RedisCluster` expecting full cleanup.

## Cross-references

- [helm-chart-authoring](../helm-chart-authoring/SKILL.md) — packaging the Operator's CRDs/RBAC/Deployment as an installable chart.
- [cert-manager-tls-automation](../cert-manager-tls-automation/SKILL.md) — a widely-deployed real-world example of the CRD + controller + finalizer pattern (Certificate/Issuer resources) to study.
- [managed-kubernetes-eks-aks-gke](../managed-kubernetes-eks-aks-gke/SKILL.md) — cloud-specific RBAC/IAM considerations when the controller needs to call out to a cloud provider API (e.g. IRSA/workload identity for the controller's ServiceAccount).
