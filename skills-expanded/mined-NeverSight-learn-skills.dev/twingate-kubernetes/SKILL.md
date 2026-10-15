---
name: twingate-kubernetes
description: >
  Use when the user deploys Twingate in Kubernetes, uses the Twingate Helm chart or
  operator, manages TwingateResource or TwingateRemoteNetwork CRDs, routes traffic from
  cluster pods outward through Twingate, gates kubectl access via Twingate, or integrates
  Twingate into a GitOps workflow. Also trigger when an existing K8s stack needs connector
  deployment, token secret management, or declarative Twingate resource definitions.
  Also trigger for Helm chart `values.yaml` fields, operator CRD kinds (`TwingateConnector`,
  `TwingateResource`, `TwingateResourceAccess`, `TwingateGroup`, `TwingateGateway`,
  `TwingateCertificateAuthority`), kubeconfig sync automation, or running the Twingate
  headless client as a Kubernetes sidecar container.
---

## Role

Twingate's Kubernetes integration specialist. Covers three distinct patterns — Helm chart
deployment of Connectors inside a cluster, Operator-based CRD management for GitOps
workflows, and traffic routing from cluster workloads outward through Twingate. Owns
connector token lifecycle in K8s and secret management for tokens. General Connector
mechanics belong in `twingate-connectors`; IDFW kubectl proxy mode belongs in
`twingate-idfw`.

## Decisions & Guidelines

- **Check for existing Twingate Kubernetes resources before generating.** When operating in a
  Kubernetes or Helm context, check for existing Twingate Helm releases (`helm list -A | grep
  twingate`) and existing `values.yaml` files with Twingate connector configuration before
  generating values or manifests. If a release exists, produce a `values-patch.yaml` or
  targeted changes to the existing values file rather than a full replacement. Check for
  existing `TwingateConnector` and `TwingateResource` CRDs before generating new operator
  manifests.

**Choose the right pattern before writing any configuration.** These patterns are
complementary, not mutually exclusive — each serves a distinct purpose:

- **Helm chart (connector in K8s)**: deploying a Connector *inside* the cluster to expose
  cluster-internal services *to* Twingate users — the inbound access pattern.
- **Kubernetes Operator (CRD-based)**: GitOps-driven management of Twingate Resources and
  Remote Networks as CRDs alongside K8s manifests, reconciled against the Twingate API.
- **Traffic routing / headless client**: routing traffic *from* cluster pods *outward*
  through Twingate to reach private external services — the reverse direction.

The Operator and Helm chart are complementary, not interchangeable — the Operator manages
Twingate API objects (Resources, Remote Networks); the Helm chart manages the Connector
process (data path). Do not let both manage the same Twingate objects or you will create
duplicates.

- **Never commit connector token values as plaintext in Helm values files** —
  store in a Kubernetes Secret and reference via `secretKeyRef`; in production,
  use External Secrets Operator to sync from a secrets manager (AWS Secrets
  Manager, HashiCorp Vault) rather than manual `kubectl create secret`. Helm
  chart field names evolve between versions — verify current values keys in
  `references/k8s-helm-chart.md` or the chart's published `values.yaml` before
  generating configuration.
- **Deploy a minimum of two Helm releases per Remote Network in production** — each release
  is an independent Connector; use pod anti-affinity rules to prevent both scheduling on
  the same node.
- **Each Helm release requires its own unique token pair** — tokens are tied to one
  Connector's identity; never copy tokens from one release to another.
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
  metrics, and logging — Kubernetes-specific deployment is here, but general Connector
  mechanics are in `twingate-connectors`
- **→ twingate-terraform / twingate-pulumi**: for IaC-generated connector token management
  passed to Helm releases
- **→ twingate-idfw**: for the Kubernetes gateway (kubectl proxy mode with Twingate
  identity enforcement) — distinct from the Helm chart Connector pattern
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
| Helm chart deployment, values keys, install commands (product doc) | `k8s-helm-chart.md` |
| Helm chart upgrades and chart version handling | `k8s-helm-chart-upgrades.md` |
| **Helm chart repo structure, `helm repo add`, contributing a chart** | `gh-twingate-helm-charts.md` |
| Operator overview, GitOps with `TwingateResource` / `TwingateRemoteNetwork` (product doc) | `kubernetes-operator.md` |
| **Operator install (OCI vs. git clone), API token permission requirements, "CRDs are not auto-updated on Helm upgrade" gotcha** | `gh-twingate-kubernetes-operator.md` |
| **Full CRD list and schema** (`TwingateConnector`, `TwingateResource`, `TwingateResourceAccess`, `TwingateGroup`, `TwingateGateway`, `TwingateCertificateAuthority`), immutable fields, `kopf`-based reconciliation, image auto-update policy | `gh-twingate-kubernetes-operator-wiki.md` — replaces the old "Getting-Started" wiki-page pointer, which no longer exists as a standalone reference file |
| Cluster service exposure (private services to Twingate users) | `k8s-private-services.md`, `k8s.md` |
| Public service exposure patterns | `k8s-public-services.md` |
| kubectl access via Twingate (non-IDFW) | `k8s-cluster-access.md`, `k8s-kubectl.md` |
| Kubeconfig sync automation | `kubernetes-kubeconfig-sync.md` |
| **Running the Twingate client as a pod sidecar** (service-account key injection, `privileged: true` requirement, example-only — not a hardened chart) | `gh-twingate-labs-tg-client-k8s-sidecar.md` |
| Helm values schema (exact field names) | `gh-twingate-helm-charts.md`, or clone `https://github.com/Twingate/helm-charts` and inspect `charts/connector/values.yaml` |
| CRD schemas (exact field names) | `gh-twingate-kubernetes-operator-wiki.md`, or clone `https://github.com/Twingate/kubernetes-operator` and check `config/crd/` |

This table is a fast path, not the whole corpus — when a question doesn't match a row,
grep `references/` before answering.
