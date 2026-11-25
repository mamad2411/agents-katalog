---
name: karpenter-cluster-autoscaling
description: >
  Guides configuring Karpenter for Kubernetes node autoscaling —
  NodePool and EC2NodeClass (or equivalent) provisioning, consolidation
  and bin-packing behavior, Spot/On-Demand mixing, and how Karpenter
  compares to and can replace the Kubernetes Cluster Autoscaler. Use when
  a user asks to "set up Karpenter", "write a NodePool spec", "reduce
  node cost via consolidation/bin-packing", "mix Spot and On-Demand
  nodes", "choose between Karpenter and Cluster Autoscaler", or "debug
  why pods are stuck Pending / a node won't scale down."
license: Apache-2.0
compatibility: "Claude Code, GitHub Copilot, OpenAI Codex, Cursor, Gemini CLI"
metadata:
  domain: observability-and-platform-extras
  maturity: stable
---

# Karpenter Cluster Autoscaling

## Purpose

The Kubernetes Cluster Autoscaler scales fixed-shape node groups
(Auto Scaling Groups / VM Scale Sets / node pools) up and down based on
pending pods and node utilization — it's reliable but coarse: node
shape is decided ahead of time per node group, and scale-down is
group-aware rather than genuinely bin-packing across instance types.
Karpenter instead provisions individual nodes directly (no node group
indirection), choosing the cheapest instance type and Availability Zone
that satisfies a pending pod's actual requirements at scale-up time, and
continuously **consolidates** running nodes — replacing several
underutilized nodes with fewer, better-packed ones, or swapping an
On-Demand node for a cheaper Spot equivalent — without waiting for a
fixed node-group scaling policy to catch up. That flexibility is also
where most Karpenter misconfiguration bites: an unbounded `NodePool` can
provision instance types or sizes nobody intended, and aggressive
consolidation can evict pods more often than a stateful or
latency-sensitive workload can tolerate if not scoped with disruption
budgets and pod-level guardrails.

## When to use

- Replacing or supplementing the Kubernetes Cluster Autoscaler with
  faster, more cost-efficient node provisioning on AWS (EKS), or the
  equivalent on other clouds where Karpenter providers exist.
- Writing or tuning a `NodePool`/`EC2NodeClass` (AWS) to constrain
  which instance types, architectures, capacity types (On-Demand vs.
  Spot), and zones Karpenter is allowed to provision.
- Reducing node cost through consolidation/bin-packing, or mixing Spot
  and On-Demand capacity for interruption-tolerant vs. latency-sensitive
  workloads.
- Debugging pods stuck `Pending` that should have triggered a scale-up,
  or nodes that never scale down despite being underutilized.
- Deciding between Karpenter and Cluster Autoscaler for a given
  cluster, or planning a migration from one to the other.
- Setting disruption budgets so consolidation/expiration doesn't evict
  pods from stateful or availability-sensitive workloads too
  aggressively.

## Prerequisites & environment

- An EKS cluster (Karpenter's most mature provider) with the
  Karpenter controller installed via Helm — Karpenter 1.0+ (the
  `karpenter.sh/v1` API) consolidated the earlier `v1beta1` CRDs;
  confirm which API version a given cluster is running before applying
  examples, since `Provisioner`/`AWSNodeTemplate` (pre-1.0) were renamed
  to `NodePool`/`EC2NodeClass`.
- IAM: a node IAM role Karpenter-provisioned nodes will assume (with the
  standard EKS worker node policies), and an IAM role for the Karpenter
  controller itself (via IRSA/Pod Identity) with permissions to create/
  terminate EC2 instances, describe subnets/security groups, and
  fleet/spot APIs — scoped to the specific cluster via
  `aws:ResourceTag/karpenter.sh/discovery` conditions, not
  account-wide EC2 permissions.
- Subnets and security groups tagged for discovery
  (`karpenter.sh/discovery: <cluster-name>`) so `EC2NodeClass` can find
  them without hardcoding IDs.
- An existing (even minimal) node group or Fargate profile to run the
  Karpenter controller itself — Karpenter cannot provision the node it
  runs on.
- If migrating from Cluster Autoscaler: Cluster Autoscaler must be
  fully removed (or explicitly scoped away from the node groups
  Karpenter now owns) before cutover — running both against the same
  node groups causes scaling conflicts.

## Step-by-step guidance

1. **Install the Karpenter controller** via Helm, scoped to the
   cluster's IRSA/Pod Identity role:
   ```bash
   helm upgrade --install karpenter oci://public.ecr.aws/karpenter/karpenter \
     --version 1.1.1 \
     --namespace kube-system \
     --set settings.clusterName=<CLUSTER_NAME> \
     --set settings.interruptionQueue=<CLUSTER_NAME>-karpenter-interruption \
     --set serviceAccount.annotations."eks\.amazonaws\.com/role-arn"="arn:aws:iam::<AWS_ACCOUNT_ID>:role/KarpenterControllerRole-<CLUSTER_NAME>"
   ```

2. **Define an `EC2NodeClass`** describing the AMI, subnets, security
   groups, and instance profile Karpenter-provisioned nodes should use:
   ```yaml
   apiVersion: karpenter.k8s.aws/v1
   kind: EC2NodeClass
   metadata:
     name: default
   spec:
     amiFamily: AL2023
     role: "KarpenterNodeRole-<CLUSTER_NAME>"
     subnetSelectorTerms:
       - tags:
           karpenter.sh/discovery: <CLUSTER_NAME>
     securityGroupSelectorTerms:
       - tags:
           karpenter.sh/discovery: <CLUSTER_NAME>
     blockDeviceMappings:
       - deviceName: /dev/xvda
         ebs:
           volumeSize: 50Gi
           volumeType: gp3
           encrypted: true
   ```

3. **Define a `NodePool`** constraining instance types, capacity type,
   and consolidation behavior — this is the primary lever for cost and
   blast-radius control:
   ```yaml
   apiVersion: karpenter.sh/v1
   kind: NodePool
   metadata:
     name: general-purpose
   spec:
     template:
       spec:
         nodeClassRef:
           group: karpenter.k8s.aws
           kind: EC2NodeClass
           name: default
         requirements:
           - key: karpenter.k8s.aws/instance-category
             operator: In
             values: ["c", "m", "r"]
           - key: karpenter.k8s.aws/instance-generation
             operator: Gt
             values: ["4"]
           - key: karpenter.sh/capacity-type
             operator: In
             values: ["spot", "on-demand"]
           - key: kubernetes.io/arch
             operator: In
             values: ["amd64"]
         expireAfter: 720h     # force node replacement at least every 30 days (patching hygiene)
     limits:
       cpu: "1000"             # hard ceiling on total CPU this NodePool can provision
       memory: 4000Gi
     disruption:
       consolidationPolicy: WhenEmptyOrUnderutilized
       consolidateAfter: 5m
   ```
   `limits` is not optional in production — an unbounded `NodePool` will
   happily scale to whatever a runaway Deployment/HPA requests.

4. **Create a separate, more restrictive `NodePool` for
   latency-sensitive or stateful workloads** that shouldn't be
   consolidated as aggressively, using `nodeAffinity`/taints to steer
   scheduling:
   ```yaml
   apiVersion: karpenter.sh/v1
   kind: NodePool
   metadata:
     name: stateful-on-demand
   spec:
     template:
       spec:
         nodeClassRef:
           group: karpenter.k8s.aws
           kind: EC2NodeClass
           name: default
         requirements:
           - key: karpenter.sh/capacity-type
             operator: In
             values: ["on-demand"]
         taints:
           - key: workload-type
             value: stateful
             effect: NoSchedule
     disruption:
       consolidationPolicy: WhenEmpty   # only consolidate fully-empty nodes, not underutilized ones
       consolidateAfter: 30m
   ```
   Pair with a matching `tolerations` + `nodeAffinity` on the stateful
   workload's pod spec so it lands only on this `NodePool`.

5. **Set a `PodDisruptionBudget` on anything consolidation/expiration
   could evict**, so Karpenter's disruption controller respects
   availability requirements rather than draining a node all at once:
   ```yaml
   apiVersion: policy/v1
   kind: PodDisruptionBudget
   metadata:
     name: payments-api-pdb
     namespace: payments
   spec:
     minAvailable: 2
     selector:
       matchLabels:
         app: payments-api
   ```

6. **Verify consolidation and bin-packing behavior** with
   `kubectl get nodeclaims` and node utilization dashboards — Karpenter
   should be replacing multiple underutilized nodes with fewer,
   better-packed ones over time, not just scaling up on demand and never
   scaling down.

7. **Debug pods stuck `Pending`** by checking Karpenter controller logs
   and events on the pod itself:
   ```bash
   kubectl describe pod <pod-name> -n <namespace>
   kubectl logs -n kube-system deployment/karpenter -f
   ```
   Common causes: no `NodePool` satisfies the pod's requested
   resources/`nodeSelector`/`affinity` combination, the `NodePool`'s
   `limits` are already exhausted, or the pod requests a resource
   (e.g. a specific GPU type) not represented in any `requirements`
   list.

8. **If migrating from Cluster Autoscaler**, remove the
   `cluster-autoscaler` Deployment (or scale it to zero and confirm no
   scaling activity) and taint/cordon its managed node groups before
   introducing Karpenter `NodePool`s, so both autoscalers never compete
   for the same pending pods simultaneously.

## Best practices

- **Always set `limits.cpu`/`limits.memory` on every `NodePool`** —
  without it, a misbehaving HPA or a bad deploy can scale a NodePool
  far beyond intended capacity/cost before anyone notices.
- **Use `consolidationPolicy: WhenEmptyOrUnderutilized` for stateless,
  interruption-tolerant workloads and `WhenEmpty` (or disable
  consolidation) for stateful/latency-sensitive ones** — aggressive
  consolidation is a cost win for the former and an availability risk
  for the latter without a `PodDisruptionBudget` in place.
- **Set `PodDisruptionBudget`s on anything Karpenter might consolidate
  or expire**, especially workloads with fewer than 3 replicas — without
  one, Karpenter's disruption controller has no signal to slow down or
  stagger evictions.
- **Prefer several instance families/sizes in `requirements` over
  pinning one exact type** — flexibility across instance types is what
  lets Karpenter find Spot capacity and bin-pack efficiently; an overly
  narrow `NodePool` behaves like a fixed node group again.
- **Use `expireAfter` to force periodic node replacement** (e.g. 30
  days) so nodes pick up the latest AMI/patches automatically rather
  than accumulating drift on long-lived nodes.
- **Separate `NodePool`s by workload class (general-purpose vs.
  stateful/GPU/latency-sensitive)** rather than one NodePool for the
  whole cluster — it lets consolidation aggressiveness, capacity type,
  and instance requirements differ per workload's actual tolerance.
- **Run Karpenter alongside Kubecost or the cost dashboard, not
  blind** — Karpenter's Spot/On-Demand mix and consolidation decisions
  are cost levers; measure the actual savings rather than assuming
  defaults are optimal. See
  [kubecost-cost-visibility](../kubecost-cost-visibility/SKILL.md).
- **Never run Karpenter and Cluster Autoscaler against the same node
  groups simultaneously** — pick one per node group/pool, since both
  reacting to the same pending pods causes duplicate or conflicting
  scale-up decisions.

## Common pitfalls

- **Symptom:** Pods remain `Pending` indefinitely even though Karpenter
  is installed and running.
  **Fix:** No `NodePool` in the cluster satisfies the pod's
  requirements (resource requests, `nodeSelector`, architecture,
  toleration for a taint), or every eligible `NodePool` has already hit
  its `limits`. Check `kubectl describe pod` for scheduling events and
  the Karpenter controller logs for the specific reason no `NodeClaim`
  was created; widen `requirements` or raise `limits` deliberately.

- **Symptom:** Node cost is much higher than expected, and Karpenter
  keeps provisioning large, expensive instance types.
  **Fix:** The `NodePool`'s `requirements` are too narrow (e.g. pinned
  to one large instance family) or a workload's resource requests are
  oversized relative to actual usage, forcing Karpenter to provision
  bigger nodes to fit them. Broaden instance-type flexibility and
  cross-check actual usage via Kubecost/Prometheus before treating
  requested resources as accurate sizing.

- **Symptom:** A stateful workload (e.g. a Kafka broker or database
  StatefulSet) gets evicted and rescheduled more often than expected,
  causing intermittent availability blips.
  **Fix:** The workload was scheduled onto a `NodePool` with
  `consolidationPolicy: WhenEmptyOrUnderutilized` and no
  `PodDisruptionBudget`, so Karpenter's consolidation treated it like
  any other movable pod. Move it to a dedicated `NodePool` with
  `consolidationPolicy: WhenEmpty` (or disruption disabled) and add a
  `PodDisruptionBudget`.

- **Symptom:** After enabling Karpenter alongside an existing Cluster
  Autoscaler setup, nodes scale up and down erratically, sometimes
  within the same minute.
  **Fix:** Both autoscalers are managing (or reacting to) the same node
  groups/pending pods and fighting each other's decisions. Fully
  decommission Cluster Autoscaler for any node group Karpenter now
  owns, or partition workloads so only one autoscaler is ever
  responsible for a given set of pods.

- **Symptom:** Karpenter-provisioned Spot nodes get interrupted
  frequently, and interruption handling doesn't drain pods gracefully
  before termination.
  **Fix:** The SQS interruption queue (`settings.interruptionQueue`)
  wasn't configured, so Karpenter never received the two-minute Spot
  interruption notice from AWS to cordon/drain proactively. Configure
  the interruption queue at install time (step 1) and confirm events
  are flowing (`aws sqs receive-message` against the queue during a
  test interruption, or check controller logs for interruption events).

## Worked example

**Scenario:** A cluster runs the Kubernetes Cluster Autoscaler against
three fixed EKS managed node groups (small/medium/large instance
types), and the platform team wants to cut node cost by moving
interruption-tolerant workloads to Spot and letting Karpenter bin-pack
more efficiently, without risking the cluster's one stateful Kafka
StatefulSet.

1. Install Karpenter (step 1) alongside the existing managed node
   groups, keeping Cluster Autoscaler running for now but scoped only
   to the (soon to be removed) managed node groups.
2. Create the `default` `EC2NodeClass` (step 2) using subnet/security-
   group discovery tags already present on the cluster's VPC.
3. Create a `general-purpose` `NodePool` (step 3) allowing `c`/`m`/`r`
   instance categories, both `spot` and `on-demand` capacity types, with
   `consolidationPolicy: WhenEmptyOrUnderutilized` and a `limits.cpu`
   ceiling set to roughly 20% above current peak cluster CPU usage.
4. Create a `stateful-on-demand` `NodePool` (step 4) for the Kafka
   StatefulSet: `on-demand` only, tainted `workload-type=stateful`, with
   `consolidationPolicy: WhenEmpty`, and add a matching toleration plus
   a `PodDisruptionBudget` (`minAvailable: 2` out of 3 Kafka brokers) so
   consolidation never drops below quorum.
5. Migrate stateless services first: relabel their Deployments'
   `nodeSelector` to prefer the `general-purpose` `NodePool`, verify
   pods land on Karpenter-provisioned nodes, and monitor for a day.
6. Once stable, cordon and drain the old Cluster Autoscaler-managed
   node groups' nodes and scale Cluster Autoscaler's managed ASGs to
   zero, then remove the Cluster Autoscaler Deployment entirely.
7. Migrate the Kafka StatefulSet onto the `stateful-on-demand` `NodePool`
   last, verifying the `PodDisruptionBudget` holds during the node
   swap and no broker quorum is lost.
8. After a week, compare node cost before/after via Kubecost — expect a
   material reduction from Spot adoption on stateless workloads and
   tighter bin-packing, while Kafka's availability profile is unchanged
   because it stayed on-demand with disruption limited to empty-node
   consolidation only.

## Cross-references

- [kubecost-cost-visibility](../kubecost-cost-visibility/SKILL.md)
- [prometheus-and-grafana-monitoring-stack](../prometheus-and-grafana-monitoring-stack/SKILL.md)
- [managed-kubernetes-eks-aks-gke](../../../kubernetes-platform/skills/managed-kubernetes-eks-aks-gke/SKILL.md)
