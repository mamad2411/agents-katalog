---
name: deploy-strategy
description: Choose and configure the deployment strategy for a service (rolling update, blue-green or canary), size its parameters from measurements, and write the rollback procedure as a Foundry runbook. Use before the first production deploy, after a bad rollout, when adopting progressive delivery, or when nobody can state how a rollback happens.
user-invocable: true
argument-hint: "[service] [--strategy rolling|blue-green|canary] [--dry-run]"
model: opus
effort: high
metadata:
  foundry.vertical: operations
  foundry.io: "service + measurements -> manifests + .foundry/runbooks/rollback-<service>.md + adr.v1"
license: Apache-2.0
---

# Deploy strategy

Picks the rollout mechanism, sizes it from real numbers, and — the part that is usually missing —
produces a **rollback runbook that has been rehearsed and timed**.

**A deployment design without a tested rollback is not finished.** That is the hard rule this
skill enforces; it will refuse to report success without the runbook and its measured duration.

**Do not use it** to decide whether Kubernetes is the right target (`cloud-architect`), to size
requests and limits (`kubernetes-engineer`), or for platforms whose rollout mechanism you do not
control — on Vercel, Netlify, Render or Railway, use the platform's immutable-deployment rollback
and write the runbook around **that**, at step 5.

## Step 1 — Gather the inputs that decide the answer

None of these are optional. Missing any one of them means you are guessing.

```bash
# current shape
kubectl -n <NS> get deploy/<NAME> -o yaml | \
  yq '.spec.replicas, .spec.strategy, .spec.template.spec.containers[].readinessProbe'

# traffic volume - decides whether canary can ever reach significance
#   sum(rate(http_requests_total{service="<NAME>"}[5m]))
# error baseline for the comparison window
#   sum(rate(http_requests_total{service="<NAME>",status=~"5.."}[5m]))
#     / sum(rate(http_requests_total{service="<NAME>"}[5m]))
# is the version label on the metrics at all? without it a canary is unmeasurable
#   count by (version) (up{service="<NAME>"})

# traffic-splitting capability
kubectl get crd 2>/dev/null | grep -Ei 'rollout|canary|httproute|virtualservice|trafficsplit'
kubectl -n <NS> get ingress,gateway 2>/dev/null
```

Record: requests per minute at trough, error-rate baseline and its variance, whether metrics
carry a version label, whether a traffic splitter exists, whether sessions are sticky, whether
the release contains a schema change, and the availability target.

## Step 2 — Choose, using the decision table

Full reasoning and failure modes in `references/strategy-matrix.md`.

| Condition | Strategy |
|---|---|
| Default; both versions can coexist safely | **Rolling update** |
| Needs an instant single-operation reversal, and you can pay double capacity for the overlap | **Blue-green** |
| High traffic **and** per-version metrics **and** a traffic splitter **and** automated analysis | **Canary** |
| Any of those four canary preconditions missing | **Not canary.** Say which one is missing |
| Release contains an irreversible migration or an irreversible external side effect | Strategy is secondary: the release is **forward-only** and needs a kill switch |

The precondition that fails most often is the third and fourth together: teams have a mesh but
aggregate metrics across versions, so the canary's error rate is diluted by the stable pods and
a bad build gets promoted. Check the version label before anything else.

**Sample-size reality check.** Before choosing canary, compute how long the analysis window must
be to distinguish the canary's error rate from the baseline at your traffic level and your
baseline variance. If the answer is "hours", canary is theatre — use blue-green with synthetic
checks instead, and say so in the ADR.

## Step 3 — Size the parameters from measurements

| Parameter | Derived from | Never |
|---|---|---|
| `maxSurge` / `maxUnavailable` | spare cluster capacity and the availability target | copied from another service |
| `minReadySeconds` | how long after Ready a bad pod actually starts failing | 0, when startup is lazy |
| `progressDeadlineSeconds` | worst observed successful rollout × 2 | left at the default and then ignored |
| canary step weights and pauses | traffic volume and the analysis window from step 2 | 10/25/50/100 by habit |
| analysis thresholds | the measured baseline plus its variance, not a round number | "error rate < 1 %" with no baseline |
| `terminationGracePeriodSeconds` | measured endpoint-propagation delay + longest request + margin | guessed |

Measure the propagation delay directly — it is the number behind most redeploy 502s:

```bash
kubectl -n <NS> get endpointslices -l kubernetes.io/service-name=<SVC> -w &
kubectl -n <NS> delete pod <POD>
# time from deletion to the endpoint disappearing = your preStop sleep floor
```

## Step 4 — Write the manifests

- Rolling update: `references/rolling-update.yaml`
- Blue-green: `references/blue-green-k8s.yaml`
- Canary: `references/argo-rollouts-canary.yaml`

Apply in a non-production environment first, always.

Cross-cutting requirements, regardless of strategy:
- ConfigMap/Secret content hashed into the pod template annotation, or `rollout undo` will ship
  the old image against the new config — a combination nobody tested.
- No `replicas:` field when an HPA owns the count and GitOps is in play; the controller will
  fight the autoscaler.
- `progressDeadlineSeconds` set, so a stalled rollout fails loudly instead of hanging.
- Schema changes follow expand/contract. Both versions run simultaneously in every strategy here
  — including blue-green, where the *database* is shared even though the pods are not.

## Step 5 — Write the rollback runbook (mandatory)

Copy `references/rollback-runbook-template.md` to `.foundry/runbooks/rollback-<service>.md`,
fill in **every** placeholder, and keep the frontmatter fields `title` and `trigger` — the
Foundry `UserPromptSubmit` hook matches on `trigger`, and `runbook_list` reads `title`.

It must answer, in order: what signal fires and at what threshold; who decides; the exact
commands; the expected duration; how you verify the rollback worked; what the rollback does
**not** undo (config, migrations, consumed events, sent emails); and who to tell.

Include the honest negative case: "for release N this rollback is not possible because …".

## Step 6 — Rehearse it and time it

An untimed rollback procedure is a hope, not a plan.

```bash
# in a non-production environment: deploy a deliberately broken build
kubectl -n <NS> set image deploy/<NAME> <CONTAINER>=<IMAGE>@sha256:<BAD-DIGEST>
# start the clock, follow the runbook exactly as written, stop the clock
time kubectl -n <NS> rollout undo deploy/<NAME> --to-revision=<N>
kubectl -n <NS> rollout status deploy/<NAME> --timeout=<SECONDS>s
```

Write the measured duration into the runbook. Target **< 5 minutes** to stable.

**Under GitOps the measured number is different and larger**: `kubectl rollout undo` is reverted
by the controller on the next sync, so the real rollback is `git revert` plus the sync interval
plus reconcile time. Measure *that*. If it is 5 minutes, your MTTR floor is 5 minutes — and that
is a fact worth knowing before an incident, not during one.

## Step 7 — Record the decision

Emit `adr.v1` to `.foundry/blackboard/<wave>/kubernetes-engineer.json` via `blackboard_write`:
at least two options with honest `cons` and a `cost` line, the chosen strategy, and
`consequences.risks` naming the **specific failure mode you are accepting**. Reference the
runbook path from `context`.

If `superpowers` is installed, invoke `superpowers:verification-before-completion` before
reporting done; otherwise paste the rehearsal output and the measured duration.

## Rollback of this change itself

Changing a deployment strategy is itself a production change.

1. The manifests are in git: `git revert <SHA>`, then let the normal rollout apply it.
2. If a progressive-delivery controller was introduced and is misbehaving, convert back to a
   plain Deployment **before** removing the controller — deleting a `Rollout` CR while it owns
   the ReplicaSets can leave the workload with no owner and no pods.
3. If traffic is currently split, drive the weight to 100 % stable first, then revert the config.
   Reverting the split configuration while a canary is live can leave routing in an
   indeterminate state.
4. Keep the previous strategy's manifests reachable for one release cycle.

## References

- `references/strategy-matrix.md` — the three strategies, preconditions, cost and failure modes.
- `references/rolling-update.yaml` — annotated Deployment with probes, preStop and PDB.
- `references/blue-green-k8s.yaml` — two Deployments, one Service, the switch and the switch back.
- `references/argo-rollouts-canary.yaml` — weighted steps with automated analysis and abort.
- `references/rollback-runbook-template.md` — the Foundry runbook to fill in.

## Deliberately not covered

- Cluster and mesh installation, and the choice of ingress controller.
- Database migration authoring; this skill enforces expand/contract and refuses to approve a
  release that violates it.
- Feature-flag platform selection — `release-engineer` covers flags as a release-decoupling tool.
- Multi-cluster or multi-region traffic management and failover.
- Serverless platform rollout semantics beyond pointing at the platform's own immutable rollback.

## Exit criteria

- [ ] The strategy is justified by the decision table, citing the **measured** inputs from step 1.
- [ ] If canary was rejected, the missing precondition is named explicitly.
- [ ] Every parameter in step 3 derived from a measurement, with the query or command recorded.
- [ ] `terminationGracePeriodSeconds` and `preStop` set from the measured propagation delay; a
      rolling restart under synthetic load produces **zero** 5xx.
- [ ] `progressDeadlineSeconds` set; a stalled rollout fails within a stated budget.
- [ ] PDB present for `replicas ≥ 2` with `disruptionsAllowed ≥ 1`.
- [ ] ConfigMap/Secret hash annotation present in the pod template.
- [ ] `.foundry/runbooks/rollback-<service>.md` exists with **no unfilled placeholders**.
- [ ] Rollback rehearsed in a non-production environment and the **measured** duration written
      into the runbook; target **< 5 min** to stable.
- [ ] The runbook states what the rollback does not undo.
- [ ] `adr.v1` on the blackboard, naming the accepted failure mode.
