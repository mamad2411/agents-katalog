---
name: kubecost-cost-visibility
description: >
  Guides deploying Kubecost inside Kubernetes clusters to allocate cloud
  spend down to namespace, workload, and label, build showback/chargeback
  reports for platform stakeholders, and feed cost signals into cluster
  autoscaling and rightsizing decisions. Use when a user asks to "show
  cost per namespace/team/label in Kubernetes", "set up Kubecost", "build
  a Kubernetes showback or chargeback report", "find which workload is
  driving the cloud bill", "size resource requests based on cost", or
  "connect Kubernetes cost data to autoscaler decisions."
license: Apache-2.0
compatibility: "Claude Code, GitHub Copilot, OpenAI Codex, Cursor, Gemini CLI"
metadata:
  domain: observability-and-platform-extras
  maturity: stable
---

# Kubecost Cost Visibility

## Purpose

Cloud billing is emitted per node, per disk, per load balancer — never
per pod, per namespace, or per team. On a shared Kubernetes cluster
running dozens of workloads on the same node pool, that means the
provider's cost dashboard tells you the cluster costs $40k/month but
cannot tell you which of twenty teams' namespaces is responsible for how
much of it. Kubecost closes that gap: it correlates node/PV/load-balancer
pricing (from cloud provider billing APIs or custom pricing sheets) with
actual Kubernetes resource **requests and usage** at the pod/container
level, then rolls that up by namespace, label, deployment, or any other
Kubernetes concept — turning an opaque node-level bill into per-team
showback and chargeback numbers, and giving rightsizing and autoscaling
decisions a cost dimension instead of just a utilization one. This skill
is Kubernetes-specific allocation; for the broader cross-cloud FinOps
practices (tagging discipline, commitment discounts, anomaly response)
that Kubecost data feeds into, see the general FinOps skill referenced
below.

## When to use

- Standing up per-namespace/per-team cost visibility on a shared
  Kubernetes cluster for the first time.
- Building a showback (visibility) or chargeback (internal billing)
  report broken down by namespace, label, deployment, or annotation.
- Investigating which workload, team, or environment is driving an
  unexpected increase in Kubernetes-hosted cloud spend.
- Deciding whether to rightsize a workload's CPU/memory requests based
  on the gap between requested and actually-used resources (idle cost).
- Feeding cost-per-node-shape data into cluster autoscaler/Karpenter
  provisioning decisions (e.g. choosing between On-Demand, Spot, and
  Reserved/Savings-Plan-covered node pools based on workload
  cost-sensitivity).
- Auditing shared-cost allocation (control-plane overhead, cluster
  add-ons, idle capacity) so it's distributed fairly rather than landing
  entirely on whichever team's namespace happens to be biggest.

## Prerequisites & environment

- A running Kubernetes cluster (EKS, AKS, GKE, or self-managed) with
  metrics-server and, ideally, the kube-prometheus-stack already
  installed — Kubecost ships its own bundled Prometheus but can instead
  federate from an existing one to avoid running two metrics stacks.
  See [prometheus-and-grafana-monitoring-stack](../prometheus-and-grafana-monitoring-stack/SKILL.md)
  if that stack isn't in place yet.
- Cloud billing API access so Kubecost can price nodes/storage/network
  accurately: an AWS IAM role with Cost and Usage Report / Cost Explorer
  read access (or the simpler node-price-from-instance-type mode without
  CUR for a rough estimate), an Azure Cost Management reader role, or a
  GCP Billing Export to BigQuery with a service account granted
  `bigquery.dataViewer`.
- Cluster-admin (or namespace-scoped, if federated per-team) access to
  install the `cost-analyzer` Helm chart into a `kubecost` namespace.
- A tagging/labeling convention already applied to namespaces/workloads
  (e.g. `team`, `cost-center`, `environment` labels) — Kubecost allocates
  by whatever Kubernetes labels/annotations exist, so allocation quality
  is only as good as label coverage. Reuse the same taxonomy as the
  cross-cloud FinOps tagging convention rather than inventing a
  Kubernetes-only one.
- Kubecost Free tier covers single-cluster allocation and is sufficient
  for the guidance in this skill; multi-cluster aggregation and
  SSO/RBAC require Kubecost Enterprise — confirm licensing needs before
  assuming multi-cluster rollup is free.

## Step-by-step guidance

1. **Install Kubecost via Helm**, pointing it at cloud billing for
   accurate node pricing:
   ```bash
   helm repo add kubecost https://kubecost.github.io/cost-analyzer/
   helm upgrade --install kubecost kubecost/cost-analyzer \
     --namespace kubecost --create-namespace \
     --set kubecostToken="<KUBECOST_TOKEN>" \
     -f values-kubecost.yaml
   ```
   `values-kubecost.yaml` (AWS example, using CUR for accurate pricing):
   ```yaml
   kubecostProductConfigs:
     athenaProjectID: "<AWS_ACCOUNT_ID>"
     athenaBucketName: "s3://<CUR_ATHENA_RESULTS_BUCKET>"
     athenaRegion: "us-east-1"
     athenaDatabase: "athenacurcfn_cur_report"
     athenaTable: "cur_report"
     masterPayerARN: "arn:aws:iam::<PAYER_ACCOUNT_ID>:role/<KUBECOST_ROLE>"
   prometheus:
     fqdn: "http://kube-prom-stack-prometheus.monitoring:9090"  # federate existing Prometheus
     enabled: false  # don't install a second Prometheus if one already exists
   ```
   Without a CUR/Cost Management/Billing-export connection, Kubecost
   falls back to public on-demand list pricing per instance type — usable
   for relative allocation between namespaces, but inaccurate for
   commitment-discounted or Spot-priced nodes.

2. **Confirm allocation data is flowing** before building reports:
   ```bash
   kubectl port-forward -n kubecost svc/kubecost-cost-analyzer 9090:9090
   curl "http://localhost:9090/model/allocation?window=1d&aggregate=namespace"
   ```
   A response with non-zero `cpuCost`/`ramCost`/`totalCost` per namespace
   confirms allocation is working; all-zero costs usually mean the
   billing connection (step 1) isn't authenticated correctly yet.

3. **Query allocation by namespace, label, or controller** via the
   Allocation API for showback reporting:
   ```bash
   # cost per namespace for the trailing 7 days
   curl "http://localhost:9090/model/allocation?window=7d&aggregate=namespace"

   # cost per team label, split out by cost type (cpu/ram/pv/network)
   curl "http://localhost:9090/model/allocation?window=7d&aggregate=label:team&accumulate=true"

   # cost per deployment within a namespace, for chargeback granularity
   curl "http://localhost:9090/model/allocation?window=30d&aggregate=namespace,deployment&filter=namespace:payments"
   ```

4. **Break out idle and shared cost explicitly** rather than letting it
   silently inflate whichever namespace happens to be measured first:
   ```bash
   curl "http://localhost:9090/model/allocation?window=7d&aggregate=namespace&idle=true&shareIdle=true&shareTenancyCosts=true"
   ```
   `shareIdle=true` distributes unallocated (idle) node capacity
   proportionally across active namespaces instead of leaving it as an
   unattributed lump — decide with stakeholders whether idle cost should
   be shared proportionally (fair to teams who scaled down) or charged
   to a platform/shared-services cost center (clearer accountability for
   who owns rightsizing the cluster's headroom).

5. **Build a showback dashboard** (Kubecost's built-in UI, or export to
   Grafana via Kubecost's Prometheus metrics `kubecost_cluster_management_cost`,
   `container_cpu_allocation`, etc.) broken down by the same `team`/
   `cost-center` labels used in the cross-cloud FinOps showback view, so
   Kubernetes cost isn't a separate silo from the rest of cloud spend.

6. **Set up chargeback only once label coverage is reliably high**
   (>95% of pods carry the `team`/`cost-center` label) — enable
   Kubecost's chargeback/invoicing report and reconcile it monthly
   against the team's own understanding of their footprint before
   treating the numbers as authoritative for internal billing.

7. **Use request-vs-usage data to drive rightsizing**, not just cost
   totals:
   ```bash
   curl "http://localhost:9090/model/allocation?window=7d&aggregate=namespace&filter=namespace:payments" \
     | jq '.data[0].payments | {cpuCost, cpuEfficiency, ramCost, ramEfficiency}'
   ```
   A namespace with `cpuEfficiency`/`ramEfficiency` well below 50%
   (requests far exceeding actual usage) is paying for idle headroom —
   feed that back to the owning team as a rightsizing recommendation
   with the dollar amount attached, which lands better than a raw
   utilization percentage.

8. **Feed cost signals into autoscaling/node-shape decisions.** Query
   Kubecost's cluster-level `savings` recommendations
   (`/model/savings/requestSizingV2`) and cross-reference with node-pool
   composition: workloads that are cost-sensitive and interruption-
   tolerant are candidates for Spot-backed Karpenter `NodePool`s; steady,
   latency-sensitive workloads justify On-Demand or Reserved/Savings-
   Plan-covered capacity. See
   [karpenter-cluster-autoscaling](../karpenter-cluster-autoscaling/SKILL.md)
   for how consolidation and node-shape selection actually happen.

## Best practices

- **Federate an existing Prometheus instead of installing a second
  one** if kube-prometheus-stack is already running — two Prometheus
  instances scraping the same cluster doubles cardinality cost and
  creates two sources of truth for the same metrics.
- **Connect real cloud billing (CUR/Cost Management/BigQuery export)
  rather than relying on list-price estimates** — list pricing ignores
  Reserved Instance/Savings Plan/CUD discounts already purchased,
  systematically overstating true per-namespace cost.
- **Decide and document the idle/shared-cost allocation policy
  explicitly** (proportional share vs. platform cost center) — an
  undocumented default confuses teams when their showback number moves
  for reasons unrelated to anything they changed.
- **Tie chargeback to the same tagging/labeling taxonomy used for
  cross-cloud FinOps**, not a Kubernetes-only one, so a team's total
  cost story (VMs + Kubernetes + managed services) is coherent in one
  place.
- **Report cost alongside efficiency (requested vs. used), not cost
  alone** — a namespace's bill going up because it's serving more
  traffic is a different conversation than its bill going up because
  requests were doubled "just in case."
- **Re-run label-coverage audits before enabling chargeback** — Kubecost
  allocation quality is bounded by label coverage; low coverage produces
  numbers that look precise but are quietly wrong.
- **Treat multi-cluster aggregation as an Enterprise-tier decision
  point** — don't assume free-tier Kubecost aggregates cost across
  clusters; plan licensing before promising a fleet-wide dashboard.

## Common pitfalls

- **Symptom:** Every namespace shows the same near-zero cost, or costs
  don't change even after obviously scaling a workload up.
  **Fix:** Kubecost isn't authenticated against real cloud billing and
  is silently falling back to (or failing to reach) pricing data.
  Verify the CUR/Cost Management/BigQuery billing connection
  credentials and IAM role/permissions (step 1), and check the
  `kubecost-cost-model` pod logs for pricing-API auth errors.

- **Symptom:** A namespace's showback cost is far higher than the team
  believes it should be, and they dispute the number.
  **Fix:** Idle/shared cluster capacity is being allocated to that
  namespace in a way the team wasn't told about (e.g.
  `shareIdle=true` spreading unused node capacity across all active
  namespaces including theirs). Make the idle-allocation policy explicit
  and visible in the report itself, not just in the API parameters.

- **Symptom:** Chargeback invoices generated from Kubecost data are
  rejected by a team as inaccurate.
  **Fix:** Label coverage was below the threshold needed for reliable
  chargeback (pods without a `team`/`cost-center` label get bucketed
  into an `__unallocated__` catch-all that then gets redistributed
  incorrectly). Run a label-coverage report first and fix coverage
  before enabling chargeback, keeping it as showback in the meantime.

- **Symptom:** Kubecost's own pods (`cost-analyzer`, bundled Prometheus)
  consume a surprisingly large amount of the cluster's CPU/memory,
  showing up as a new top-line cost themselves.
  **Fix:** A second Prometheus was installed instead of federating the
  existing one, doubling scrape/storage load. Set
  `prometheus.enabled: false` and point `prometheus.fqdn` at the
  existing kube-prometheus-stack instance.

- **Symptom:** A rightsizing recommendation based on Kubecost's
  efficiency numbers is applied and the workload starts getting OOMKilled
  under peak load.
  **Fix:** Efficiency was computed from average usage over the query
  window, hiding periodic peaks (batch jobs, traffic spikes). Cross-check
  peak (not just average) usage — the same caution that applies to
  cloud-level rightsizing applies here; see
  [cloud-cost-finops-optimization](../../../cloud/skills/cloud-cost-finops-optimization/SKILL.md)
  for the general principle.

## Worked example

**Scenario:** A platform team runs one shared EKS cluster for six
product teams. The AWS bill for the cluster's node group is $28k/month,
but there's no way to tell which team is responsible for how much of it,
and finance wants a monthly chargeback report.

1. Install Kubecost via Helm, federating the cluster's existing
   kube-prometheus-stack Prometheus and connecting it to the AWS CUR
   Athena table for accurate, discount-aware node pricing (step 1).
2. Confirm allocation data via the Allocation API and spot-check that
   `cpuCost + ramCost + pvCost` roughly reconciles with the actual AWS
   invoice for the node group over the same window.
3. Run a label-coverage audit: 92% of pods carry a `team` label; the
   remaining 8% (mostly cluster add-ons and a couple of unlabeled jobs)
   are backfilled with labels before proceeding.
4. Query `aggregate=label:team&shareIdle=true&shareTenancyCosts=true`
   for the trailing 30 days, and present the breakdown as **showback**
   first, giving each team two weeks to review and dispute their number
   before switching to chargeback.
5. One team, `checkout`, disputes their number as high relative to their
   traffic; the efficiency query shows `cpuEfficiency: 18%` — their
   deployments request 4 CPU per pod but use under 1 CPU even at peak.
   The team rightsizes requests down to 1.5 CPU, cutting their showback
   cost by roughly 60% the following month.
6. Once label coverage stays above 95% for a full month and the
   showback numbers have been validated without further disputes,
   finance enables monthly chargeback invoicing from the same
   Allocation API data.
7. The platform team separately reviews Kubecost's savings
   recommendations and moves `checkout`'s now-rightsized, traffic-
   tolerant background workers onto a Spot-backed Karpenter `NodePool`,
   further reducing their allocated node cost.

## Cross-references

- [prometheus-and-grafana-monitoring-stack](../prometheus-and-grafana-monitoring-stack/SKILL.md)
- [karpenter-cluster-autoscaling](../karpenter-cluster-autoscaling/SKILL.md)
- [cloud-cost-finops-optimization](../../../cloud/skills/cloud-cost-finops-optimization/SKILL.md)
