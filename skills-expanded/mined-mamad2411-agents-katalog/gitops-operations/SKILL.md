---
name: gitops-operations
description: "Operate Argo CD without fighting the controller: establish which repository and generator own desired state, explain OutOfSync and drift, review rendered changes before sync, order dependencies, choose prune and self-heal policy, recover by changing Git, and verify convergence from commit to workload. Use this skill when someone asks why Argo CD keeps reverting a kubectl edit, whether to sync or prune, how to structure sync waves, how to recover or roll back a GitOps deployment, why an ApplicationSet child changed, or how multiple sources produced an unexpected manifest. Also use its ownership workflow for Flux drift, while verifying Flux-specific controls in the installed controller documentation. Not for designing canary cohorts and promotion metrics (`release-strategy`), authoring workload probes and resources (`k8s-workloads`), or diagnosing a live broken cluster (`k8s-triage`)."
allowed-tools: "Read, Write, Edit, Grep, Glob, Bash(git:*), Bash(kubectl:*), Bash(argocd:*), Bash(flux:*)"
---

# GitOps Operations

Operate the desired state, then let the controller converge the cluster to it. A recovery is complete only when Git, rendered desired state, live state, application health, and the user-facing signal agree.

GitOps incidents become confusing when an operator treats the live object as the authority while a controller treats a commit as the authority. A manual patch may appear to fix the service and then vanish; a UI rollback may be immediately undone; a harmless-looking generator edit may fan out across clusters. Resolve ownership before changing anything.

## Scope

Use for: Argo CD or Flux reconciliation, drift, sync and prune decisions, self-heal, dependency ordering, controller-safe recovery, ApplicationSet fan-out, and multi-source composition.

Do not use for: rollout percentages, bake times, feature flags, or promotion guardrails, which belong to `release-strategy`; workload manifest design, probes, requests, limits, and disruption budgets, which belong to `k8s-workloads`; or active outage diagnosis and mitigation, which belongs to `k8s-triage`.

## Workflow

### 1. Establish the authority chain

Record these before proposing a mutation:

| Question | Evidence to capture | Why it matters |
| --- | --- | --- |
| Which controller owns the object? | Application label/annotation, owner reference, inventory, controller status | Two reconcilers claiming one object create a write loop |
| Which declaration owns it? | Application or Kustomization, repository URL, path/chart, revision | The live object is an output, not the edit target |
| Is it generated? | ApplicationSet name, generator inputs, rendered child Application | A child edit is overwritten by its parent |
| Is desired state composite? | Every source and its resolved revision | The last source may override an earlier resource |
| What commit is observed? | Controller-reported revision, not merely repository HEAD | HEAD may not be fetched or reconciled yet |

Read `references/ownership-and-drift.md` when ownership is ambiguous or more than one controller can write the same object.

Stop if the source is mutable or unresolved: a floating chart version, branch whose commit was not recorded, generated values that cannot be reproduced, or a source the operator cannot inspect. First make the desired input identifiable.

### 2. Classify the difference

Do not equate `OutOfSync` with broken. Compare three things: rendered desired manifests at the observed revision, live objects, and controller diff rules.

| Signal | Likely class | Action |
| --- | --- | --- |
| Git changed; live has not | Pending or failed reconciliation | Inspect sync status, conditions, events, and dependency health |
| Live changed; Git did not | Manual drift or another controller's mutation | Identify the writer; encode the legitimate change in Git or remove it |
| Diff repeats on defaulted/status fields | Normal API/controller mutation | Narrowly ignore fields only after naming their writer and semantics |
| Desired output changes with no obvious app commit | Generator, dependency, or second source moved | Pin and inspect every input |
| Resource exists live but not desired | Prune candidate, orphan, or shared resource | Prove ownership and retention requirements before deletion |

An ignore rule is an ownership decision. Scope it to the exact group, kind, and field; document who owns that field; confirm the field cannot conceal security, routing, replica, or image drift. Broad exclusions convert useful drift detection into false health.

### 3. Review the rendered change and blast radius

Review the controller's rendered desired state rather than only the source diff. Include generated names, resolved values, CRDs, hooks, and resources that would be pruned.

Before sync, record:

1. The exact desired revision for every source.
2. The Applications, clusters, namespaces, and resources affected.
3. Creates, updates, replacements, and prune candidates separately.
4. Whether an ApplicationSet generator expands or contracts its output.
5. Whether any resource is shared, retained, stateful, or externally adopted.
6. The health and customer signal that will prove success.

A label-only change across 200 generated Applications is still a 200-application operation. Treat generator cardinality as blast radius.

### 4. Make ordering explicit

Use phases or waves only for real dependencies. Within a wave, assume resources may proceed together; do not rely on file order or incidental lexical order.

Typical dependency shape:

| Order | Content | Gate before next order |
| --- | --- | --- |
| Earlier | Namespace, CRD, controller, shared configuration | API established and controller healthy |
| Middle | Stateful dependencies and migrations designed for this release | Explicit completion and compatibility check |
| Later | Application workloads and routes | Ready plus service-level verification |
| Final | Cleanup or removal | New path proven and rollback window closed |

Hooks are jobs with side effects. Make them idempotent, give them observable success and failure, and define cleanup. Selective sync can skip hooks, so do not hide an indispensable invariant only inside a hook. Read `references/argo-safety-controls.md` before designing waves, hooks, prune, or automated sync.

### 5. Choose Argo CD automation policy deliberately

The controls and defaults in this section are Argo CD-specific. Treat them separately:

- **Automated sync** applies a new desired revision without a human sync action.
- **Self-heal** permits reconciliation of live drift when desired revision has not changed.
- **Prune** deletes tracked resources removed from desired state.
- **Allow empty** permits pruning when an application renders no target resources.

Enable each only with a stated owner and recovery path. Prune deserves an ownership and retention review; self-heal deserves proof that emergency changes can be committed quickly; allow-empty deserves a generator-empty test because an input or selector mistake can otherwise look like intentional removal.

For an ApplicationSet-generated Application, change automation in the ApplicationSet template or its governing policy. Editing the child is temporary because the ApplicationSet controller owns it.

For Flux, retain the same ownership, rendered-diff, recovery, and verification gates, but verify the installed controller's suspension, pruning, dependency, and remediation semantics in its version-specific documentation. Do not translate Argo CD field names or defaults into Flux policy.

### 6. Sync through the controller

Prefer merging a reviewed desired-state change and allowing reconciliation. A manual sync is acceptable when policy requires promotion, but pin it to the reviewed revision and record who initiated it.

During convergence, distinguish:

- **Sync status**: whether live state matches rendered desired state.
- **Health status**: whether resources report a healthy operating state.
- **Service verification**: whether the customer-facing SLI or intended behavior is correct.

None substitutes for the others. `Synced` can serve broken traffic, and `Healthy` can describe the wrong revision.

Pause when the observed revision differs from the reviewed revision, a prune set grows, a shared resource appears, a hook is not idempotent, or an ApplicationSet produces an unexpected child set. Re-review rather than forcing convergence.

### 7. Recover by restoring desired state

Choose recovery based on the controller mode:

| Situation | Recovery |
| --- | --- |
| Bad commit, automated sync active | Revert or forward-fix in Git; let the controller reconcile the new commit |
| Manual sync policy | Select the known-good desired revision, review its rendered diff, then sync it |
| Emergency live mitigation | Record the patch and expiry; immediately encode it in Git or suspend the relevant reconciliation under an incident owner |
| Bad ApplicationSet expansion | Correct or revert generator/template input; verify the generated Application set before resuming |
| Bad multi-source output | Pin or revert the responsible source; render the combined result before syncing |

Do not issue an Argo CD rollback while automated sync remains enabled: Argo CD documents that rollback is unavailable in that mode, and the reconciliation model would otherwise restore the current Git state. If automation must be suspended for an emergency, name the owner, scope, reason, and resumption condition. Leaving reconciliation suspended turns future Git changes into silent non-deployments.

### 8. Verify closure

Verify in this order:

1. The repository contains the intended recovery or forward state.
2. The controller observes the intended immutable revision for every source.
3. The rendered diff contains only the approved changes and prune set.
4. Sync completes and all hooks or waves reach their defined gates.
5. Resource health stabilizes without a repeated reconcile loop.
6. The service-level signal and intended behavior recover.
7. Automation, prune, and self-heal match policy again; temporary suspensions and live patches are gone.

Record the old revision, bad revision, recovery revision, affected Applications, sync result, prune result, verification signal, and any follow-up ownership correction.

## Output format

```markdown
## Authority
Controller / parent generator / repository / path / resolved revision(s).

## Difference
Desired versus live, writer of each differing field, and ignored fields.

## Blast radius
Applications / clusters / namespaces / creates / updates / prunes.

## Reconciliation plan
Ordering, gates, automation policy, and stop conditions.

## Recovery
Git revert or forward fix, any bounded suspension, and resumption condition.

## Verification
Observed revision / rendered diff / sync / health / service signal.
```

## Anti-patterns

**Patching the live object as the fix.** Self-heal or the next source change removes it. Commit the change to the owning source, or explicitly suspend reconciliation for a bounded emergency.

**Forcing sync before identifying the observed revision.** The operator may deploy an unreviewed commit or a newly resolved dependency. Match the controller's immutable revision to the reviewed input first.

**Turning on prune to clear `OutOfSync`.** Prune is deletion, not status cleanup. Prove that each candidate is owned, disposable, and recoverable.

**Editing an ApplicationSet child.** The generator owns the child and recreates its declared fields. Change the template or generator input and inspect the fan-out.

**Using multiple sources as an application grouping mechanism.** Resource precedence becomes part of deployment behavior, and a change in any source may trigger the combined application. Use it only when the sources form one coherent desired state.

**Ignoring a noisy diff broadly.** A global exclusion can hide a real image, route, privilege, or replica change. Identify the writer and ignore only its exact field.

## Reference files

- `references/ownership-and-drift.md` — read when locating desired-state ownership, classifying persistent drift, or untangling ApplicationSet and multi-source precedence.
- `references/argo-safety-controls.md` — read before changing automated sync, self-heal, prune, allow-empty, waves, hooks, or recovery behavior.
