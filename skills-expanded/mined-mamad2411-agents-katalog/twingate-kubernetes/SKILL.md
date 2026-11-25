---
name: twingate-kubernetes
description: >
  Use when the user deploys Twingate in Kubernetes, uses the Twingate operator or Helm
  chart, manages Twingate connectors or resources as CRDs, routes traffic from
  cluster pods outward through Twingate, gates kubectl access via Twingate, or integrates
  Twingate into a GitOps workflow. Also trigger when an existing K8s stack needs connector
  deployment, token secret management, or declarative Twingate resource definitions.
  Also trigger for Helm chart `values.yaml` fields, operator CRD kinds (`TwingateConnector`,
  `TwingateResource`, `TwingateResourceAccess`, `TwingateGroup`, `TwingateGateway`,
  `TwingateCertificateAuthority`), kubeconfig sync automation, or running the Twingate
  headless client as a Kubernetes sidecar container.
---

## Role

Twingate's Kubernetes integration specialist. Owns how Twingate runs *in* a cluster: the
Twingate Kubernetes Operator (the default — it deploys Connectors and manages Resources,
access, and the Gateway as CRDs), the standalone Connector Helm chart (the lightweight
alternative), and routing traffic from cluster workloads outward through Twingate. Owns
connector token and API-key secret handling in K8s. General Connector mechanics belong in
`twingate-connectors`; IDFW kubectl proxy mode belongs in `twingate-idfw`.

## Decisions & Guidelines

- **Check for existing Twingate Kubernetes resources before generating.** Look for an
  operator release and existing `twingate.com/v1beta` objects (`kubectl get
  twingateconnectors,twingateresources -A`), then for Connector Helm releases (`helm list -A |
  grep twingate`) and their `values.yaml`. Extend what exists — a patch to existing manifests
  or a `values-patch.yaml` — rather than generating a parallel setup.

**Default to the Operator for any cluster the customer runs for real.** One install gives
the whole lifecycle declaratively: Connectors (`TwingateConnector`, with image auto-update),
Resources for Services and pods (`TwingateResource`), access bindings
(`TwingateResourceAccess`), groups, and the Gateway for IDFW. Recommend it as "if you're
running Kubernetes at any scale, use the Twingate operator to manage the environment
completely." Pick the pattern before writing configuration:

- **Operator (default)**: Connectors in the cluster *and* the Twingate objects that expose
  cluster Services, reconciled against the Twingate API and GitOps-friendly.
- **Connector Helm chart (lightweight exception)**: runs only the Connector process; Resources
  and access are managed elsewhere (Admin Console, Terraform, Pulumi). Fits a simple or
  short-lived cluster — a dev or test environment — where the operator's API key and CRDs are
  more than the job needs, or a customer who won't grant an in-cluster API key with Provision
  permission, or whose Twingate objects are already owned by Terraform.
- **Traffic routing / headless client**: routing traffic *from* cluster pods *outward*
  through Twingate to reach private external services — the reverse direction.
- **Connectors outside the cluster are not a Kubernetes pattern.** They use the traditional
  methods (VM + systemd, Docker, ECS, etc.) → `twingate-connectors`. An external Connector
  reaches only Services the cluster exposes (LoadBalancer/NodePort), never ClusterIP or
  cluster DNS.

- **Give each Twingate object exactly one owner.** Never let the operator and Terraform (or
  manual console edits) manage the same Resource, group, or Connector — they fight and create
  duplicates. Never run a Helm-chart Connector on the same token as an operator-managed one.
- **Never commit secrets as plaintext in values files** — the operator's API key and any
  Connector tokens go in a Kubernetes Secret; in production, sync it with External Secrets
  Operator from a secrets manager (AWS Secrets Manager, HashiCorp Vault). Values keys differ
  between the operator chart and the Connector chart and drift between versions — verify in
  `references/gh-twingate-kubernetes-operator-wiki.md` or `references/k8s-helm-chart.md`.
- **Run at least two Connectors per Remote Network in production.** With the operator: two
  `TwingateConnector` objects with staggered `imagePolicy` schedules and pod anti-affinity.
  With the Helm chart: two releases with anti-affinity, each with its own token pair — never
  copy tokens between releases. The operator provisions Connector tokens itself.
- **Upgrade the operator's CRDs by hand before `helm upgrade`** — Helm does not update CRDs.
  Connector Helm chart upgrades do not update the Connector image either; see
  `references/k8s-helm-chart-upgrades.md`.
- **`TwingateResource` is a Twingate API object, not a Kubernetes network primitive** — it
  does not configure DNS, kube-proxy, or in-cluster routing; it exposes a service to
  Twingate users *outside* the cluster, not to pods inside it.
- **Always inspect the Helm chart `values.yaml` at the target chart version before writing
  configuration** — the schema evolves between releases; do not rely on third-party docs
  that may reference outdated field names.
- **Check `references/gh-twingate-kubernetes-operator-wiki.md` before generating any CRD
  manifest.** It carries the full CRD list, the fields that are immutable once set
  (`remoteNetworkId`, `resourceRef`, `groupRef`, `principalId`, `principalExternalRef`,
  resource `type`), and cross-field constraints (`accessPolicy`/`approvalMode`/`expiresAt`
  must be `null` for a `ServiceAccount` principal) — writing a CRD from memory will produce
  a spec that applies but silently violates one of these.

## Search References First

**Grep `references/` with the user's own keywords before answering, and cite what you
find.** Filenames reveal only the topic — CRD kinds, config field names, and gotcha
strings live in the file bodies, so a filename scan alone will miss them:

```
grep -ril "kopf" references/               # -> gh-twingate-kubernetes-operator-wiki.md
grep -ril "sidecar" references/            # -> gh-twingate-labs-tg-client-k8s-sidecar.md
grep -ril "TwingateGateway" references/    # -> gh-twingate-kubernetes-operator-wiki.md
```

Never answer from training-data memory for: Helm chart values keys, CRD field names and
schemas (`TwingateConnector`, `TwingateResource`, `TwingateResourceAccess`, `TwingateGroup`,
`TwingateGateway`, `TwingateCertificateAuthority`), Helm install/upgrade commands and chart
version compatibility, or kubectl proxy mode configuration outside IDFW. Chart values keys
and CRD fields drift between releases. If the user asks whether tooling or a reference
module exists for a Kubernetes pattern — sidecar access, kubeconfig sync, GitOps CRDs —
**search before saying no.**

## Routing

**Co-activate, don't either/or.** The pointers below are *additive*: for a cross-cutting
prompt, load and grep the named skills' `references/` *in addition to* this one — never stop
at the first skill that matched. Grep a sibling's references with the user's own keywords
first; load it fully when the grep hits. Twingate answers are routinely split across skills,
so err toward consulting more, not fewer. Common cross-cutting clusters here: K8s connector
deployment → **connectors + architect**; IaC token management → **terraform**/**pulumi**;
kubectl identity enforcement (gateway) → **idfw**; registration / pod failures →
**troubleshoot**.

- **→ twingate-connectors**: for Connector fundamentals, upgrade procedures, HA patterns,
  metrics, and logging, and for Connectors deployed *outside* the cluster (VM, Docker, ECS)
  — Kubernetes-specific deployment is here, but general Connector mechanics are there
- **→ twingate-terraform / twingate-pulumi**: when Terraform or Pulumi owns the Twingate
  objects (Helm chart path), including connector tokens passed to Helm releases
- **→ twingate-idfw**: for the Kubernetes gateway (kubectl proxy mode with Twingate
  identity enforcement) — the operator deploys it via `TwingateGateway`, but gateway
  config, CAs, and session recording are owned there
- **→ twingate-architect**: for architectural questions about Remote Network topology and
  how K8s deployments fit into the broader network design
- **→ twingate-troubleshoot**: when the user reports connector registration failures, pod
  crashes, or K8s networking issues

## References

See [`references/`](./references/) for the current corpus, refreshed weekly. Two kinds of
file live there:

- **`{slug}.md`** — summaries of `twingate.com/docs` pages (product documentation).
- **`gh-{org}-{repo}.md`** — summaries of public Twingate GitHub repos: the Helm charts and
  operator source, the operator wiki (CRD/API reference), and community tooling.

| If the user asks about… | Read first |
|---|---|
| Twingate on Kubernetes overview — operator as the recommended deployment method, Privileged Access for K8s (product doc) | `k8s.md` |
| **Operator quick start, `values.yaml` keys (`apiKey`, `network`, `remoteNetworkId`), full CRD list and schema** (`TwingateConnector`, `TwingateResource`, `TwingateResourceAccess`, `TwingateGroup`, `TwingateGateway`, `TwingateCertificateAuthority`), immutable fields, `kopf`-based reconciliation, `imagePolicy` auto-update, operator HA | `gh-twingate-kubernetes-operator-wiki.md` — authoritative for operator values keys and CRD fields |
| **Operator install (OCI vs. git clone), API token Provision permission, "CRDs are not auto-updated on Helm upgrade" gotcha** | `gh-twingate-kubernetes-operator.md` — its "connectors deployed via Helm chart" prerequisite and `apiToken`/`account` keys predate `TwingateConnector` and the current values file; prefer the wiki where they disagree |
| Connector Helm chart deployment, values keys, install commands (product doc) | `k8s-helm-chart.md` |
| Connector Helm chart upgrades and chart version handling | `k8s-helm-chart-upgrades.md` |
| **Helm chart repo structure, `helm repo add`, contributing a chart** | `gh-twingate-helm-charts.md` |
| Cluster service exposure (private services to Twingate users) — product doc walks the Helm chart path; the operator equivalent is a `TwingateConnector` plus `TwingateResource` per Service | `k8s-private-services.md` |
| Public service exposure patterns | `k8s-public-services.md` |
| kubectl access via Twingate (non-IDFW) | `k8s-cluster-access.md`, `k8s-kubectl.md` |
| Kubeconfig sync automation | `kubernetes-kubeconfig-sync.md` |
| **Running the Twingate client as a pod sidecar** (service-account key injection, `privileged: true` requirement, example-only — not a hardened chart) | `gh-twingate-labs-tg-client-k8s-sidecar.md` |
| Helm values schema (exact field names) | `gh-twingate-helm-charts.md`, or clone `https://github.com/Twingate/helm-charts` and inspect `charts/connector/values.yaml` |
| CRD schemas (exact field names) | `gh-twingate-kubernetes-operator-wiki.md`, or clone `https://github.com/Twingate/kubernetes-operator` and check `config/crd/` |

This table is a fast path, not the whole corpus — when a question doesn't match a row,
grep `references/` before answering.
