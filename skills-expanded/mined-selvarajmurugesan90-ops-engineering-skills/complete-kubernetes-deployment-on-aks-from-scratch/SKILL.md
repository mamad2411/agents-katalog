---
name: complete-kubernetes-deployment-on-aks-from-scratch
description: >
  Sequences a complete, end-to-end AKS deployment from a bare Azure
  subscription to a production-ready cluster serving a first workload —
  Azure landing zone prerequisites, AKS cluster and node pool provisioning,
  Azure CNI (with the Calico/Cilium alternative noted), ingress (Application
  Gateway Ingress Controller vs. ingress-nginx), cert-manager with Azure
  DNS, conformance validation, a Helm-deployed workload, and a node/cluster
  health baseline. This is an integration/orchestration skill that sequences
  several existing tool-specific skills in the correct order and flags the
  handoff points between them — it does not restate their internals. Use
  when a user asks to "deploy a Kubernetes cluster on AKS from scratch,"
  "set up a new AKS environment end to end," "build a production AKS
  cluster from a fresh Azure subscription," or "give me the full sequence
  to go from nothing to a working AKS cluster."
license: Apache-2.0
compatibility: "Claude Code, GitHub Copilot, OpenAI Codex, Cursor, Gemini CLI"
metadata:
  domain: kubernetes-platform
  maturity: stable
---

# Complete Kubernetes Deployment on AKS From Scratch

## Purpose

An AKS cluster that reports every node `Ready` is not the same claim as
"this environment is ready for a production workload" — the Azure AD
Workload Identity federation, the Management Group/subscription hierarchy
it lands in, the CNI mode chosen at cluster creation (which cannot be
changed later without rebuilding), and cert-manager's Azure DNS-01
credentials each have their own setup order, and getting that order wrong
produces a cluster that looks finished right up until someone depends on
the piece that was skipped or sequenced too late. This skill is the
Azure-specific end-to-end runbook: it sequences Azure landing zone
prerequisites, AKS provisioning, CNI mode selection, ingress, cert-manager
with Azure DNS, conformance validation, a first workload, and a health
baseline into one ordered path, cross-referencing the tool-specific skill
that covers each phase's actual detail.

## When to use

- Deploying a brand-new AKS cluster into an Azure subscription for the
  first time, where the subscription already exists inside the org's
  Management Group hierarchy but has no Kubernetes workload yet.
- Auditing an existing AKS rollout for a skipped or out-of-order phase
  (e.g. cert-manager configured before its federated credential existed,
  or a cluster handed off with no conformance validation).
- Rebuilding a reference AKS environment (a second region, a DR cluster)
  that should follow the same sequence as a known-good first cluster.
- Onboarding a team unfamiliar with how the individual AKS/CNI/ingress/
  cert-manager skills in this repository fit together into one coherent
  deployment.

## Prerequisites & environment

- An Azure subscription already vended through the org's subscription
  vending process and landed in the correct Management Group with Azure
  Policy guardrails applied — this skill does **not** cover Management
  Group design or subscription vending; see
  [azure-landing-zone-setup](../../../cloud/skills/azure-landing-zone-setup/SKILL.md).
- RBAC rights to create the AKS cluster, its node resource group, Entra ID
  app registrations/managed identities, and federated credentials — see
  [cloud-iam-hardening](../../../cloud/skills/cloud-iam-hardening/SKILL.md)
  for the least-privilege design that should govern every identity
  created in Phase 1.
- An Azure DNS public zone already delegated for the domain cert-manager
  will issue certificates for (Phase 4 depends on this existing before
  DNS-01 can succeed).
- `az` CLI ≥ 2.60 with the `aks-preview` extension current, `kubectl`, and
  `helm` ≥ 3.14.
- A non-production subscription to rehearse this exact sequence in at
  least once — the CNI mode decision in Phase 3 in particular cannot be
  changed on a live cluster without a rebuild, so getting it wrong the
  first time is expensive to undo.

## Step-by-step guidance

This is the phase sequence. Each phase links to the skill that covers its
full depth; the text here covers only AKS-specific sequencing and
integration decisions.

1. **Phase 1 — Azure landing zone & identity prerequisites.** Confirm the
   subscription sits in the correct Management Group with Azure Policy
   guardrails applied (see
   [azure-landing-zone-setup](../../../cloud/skills/azure-landing-zone-setup/SKILL.md)).
   AKS-specific sequencing point: **create the Entra ID managed identities
   this cluster will need up front**, even though their federated
   credentials (which require the AKS OIDC issuer URL from Phase 2) can't
   be finished until after the cluster exists:
   ```bash
   az identity create --name payments-api-identity --resource-group payments-rg
   az identity create --name cert-manager-dns01-identity --resource-group payments-rg
   ```
   Planning both identities together in Phase 1 avoids a second identity-
   creation pass once Phase 5 needs one.

2. **Phase 2 — Provision the AKS cluster and node pools.** Use
   [managed-kubernetes-eks-aks-gke](../managed-kubernetes-eks-aks-gke/SKILL.md)
   for the full `az aks create`/node pool/workload identity setup detail.
   AKS-specific sequencing point: enable Azure AD Workload Identity and
   OIDC issuer **at cluster creation** — retrofitting these onto a live
   cluster is possible but disruptive, unlike EKS's IRSA (which layers
   cleanly onto an already-running cluster via the OIDC association
   step alone):
   ```bash
   az aks create --name payments-prod --resource-group payments-rg \
     --kubernetes-version 1.30 --enable-managed-identity \
     --enable-oidc-issuer --enable-workload-identity \
     --network-plugin azure --enable-private-cluster
   az aks get-credentials --name payments-prod --resource-group payments-rg
   AKS_OIDC_ISSUER=$(az aks show --name payments-prod --resource-group payments-rg \
     --query "oidcIssuerProfile.issuerUrl" -o tsv)
   ```

3. **Phase 3 — CNI: Azure CNI mode, decided before nodes exist.** Unlike
   EKS (where VPC CNI is simply already running) or a self-managed
   cluster (where no CNI exists until applied), AKS requires choosing a
   CNI **mode** at cluster creation that cannot be changed afterward
   without rebuilding the cluster:
   - **Azure CNI Overlay** (the current recommended default) — pods get
     IPs from a private overlay CIDR independent of the VNet's address
     space, avoiding VNet IP exhaustion at scale.
   - **Azure CNI (VNet-integrated, "Azure CNI Node Subnet")** — pods get
     real VNet IPs, needed only when pods must be directly addressable
     from other VNet-resident resources without translation.
   - **Kubenet** (legacy, being phased out) — avoid for new clusters.
   `--network-plugin azure` was set in Phase 2's `az aks create` for
   exactly this reason — confirm the mode matches the VNet's actual IP
   budget before Phase 2 runs, since this is one of the few decisions in
   this sequence that isn't cheaply reversible later.
   **Alternative:** for `NetworkPolicy` enforcement or a non-Azure-
   specific CNI for portability, Azure CNI Powered by Cilium (an
   AKS-native option) or a self-managed Calico installation are valid
   swaps — see
   [cni-networking-calico-flannel](../cni-networking-calico-flannel/SKILL.md)
   for the underlying tradeoffs; decide this alongside the CNI mode
   above, not as an afterthought once nodes are already running.

4. **Phase 4 — Ingress: Application Gateway Ingress Controller (AGIC) vs.
   ingress-nginx, and DNS wiring.** Decide deliberately:
   - **AGIC** — provisions/manages an Azure Application Gateway (L7 LB
     with WAF integration) driven by Ingress resources; preferred when
     Azure WAF or Application Gateway-specific features are required.
   - **ingress-nginx** behind a `Service` of `type: LoadBalancer`
     (provisions an Azure Load Balancer) — see
     [ingress-nginx-configuration](../ingress-nginx-configuration/SKILL.md)
     for full install/annotation detail; preferred for parity with
     non-Azure clusters running the same ingress-nginx configuration.
   Once the controller has an external address, create the Azure DNS
   record pointing at it **before** Phase 5's DNS-01 challenge needs to
   resolve — DNS-01 itself validates via the Azure DNS API's `TXT`
   records, not this application record, but a missing record here still
   leaves Phase 7's workload unreachable after TLS succeeds.

5. **Phase 5 — cert-manager with Azure DNS.** Install cert-manager and
   configure a `ClusterIssuer` per
   [cert-manager-tls-automation](../cert-manager-tls-automation/SKILL.md),
   substituting Azure DNS for the Route 53 example shown there. The
   AKS-specific integration point: complete the federated credential for
   the `cert-manager-dns01-identity` planned in Phase 1, using the OIDC
   issuer URL captured in Phase 2:
   ```bash
   az identity federated-credential create \
     --name cert-manager-fic --identity-name cert-manager-dns01-identity \
     --resource-group payments-rg --issuer "$AKS_OIDC_ISSUER" \
     --subject system:serviceaccount:cert-manager:cert-manager
   az role assignment create --assignee <CERT_MANAGER_IDENTITY_CLIENT_ID> \
     --role "DNS Zone Contributor" \
     --scope /subscriptions/<SUB_ID>/resourceGroups/dns-rg/providers/Microsoft.Network/dnszones/example.com
   ```
   ```yaml
   apiVersion: cert-manager.io/v1
   kind: ClusterIssuer
   metadata: { name: letsencrypt-dns }
   spec:
     acme:
       server: https://acme-v02.api.letsencrypt.org/directory
       email: platform-team@example.com
       privateKeySecretRef: { name: letsencrypt-dns-account-key }
       solvers:
         - dns01:
             azureDNS:
               subscriptionID: "<SUB_ID>"
               resourceGroupName: dns-rg
               hostedZoneName: example.com
               environment: AzurePublicCloud
           selector: { dnsZones: ["example.com"] }
   ```
   Validate against Let's Encrypt staging first, exactly as
   [cert-manager-tls-automation](../cert-manager-tls-automation/SKILL.md)
   describes.

6. **Phase 6 — Conformance and smoke validation.** Run Sonobuoy quick
   mode, then full `certified-conformance`, then targeted smoke tests —
   see
   [kubernetes-cluster-post-provision-conformance-validation](../kubernetes-cluster-post-provision-conformance-validation/SKILL.md).
   For AKS specifically, also confirm the default `managed-csi`
   `StorageClass` (Azure Disk CSI driver) provisions a PVC, and — if Azure
   CNI Overlay was chosen in Phase 3 — that cross-node pod connectivity
   works correctly across the overlay, since overlay mode's data path
   differs materially from VNet-integrated mode's.

7. **Phase 7 — Deploy the first workload via Helm.** Package and install
   per
   [helm-chart-authoring](../helm-chart-authoring/SKILL.md), completing
   the `payments-api-identity` federated credential from Phase 1 the same
   way Phase 5 completed cert-manager's, using the workload's own
   namespace/ServiceAccount subject:
   ```bash
   az identity federated-credential create \
     --name payments-api-fic --identity-name payments-api-identity \
     --resource-group payments-rg --issuer "$AKS_OIDC_ISSUER" \
     --subject system:serviceaccount:payments:payments-api
   helm upgrade --install payments-api oci://ghcr.io/example/charts/payments-api \
     --version 2.3.0 --namespace payments --create-namespace --atomic --timeout 5m
   ```

8. **Phase 8 — Node/cluster health baseline.** Establish the ongoing
   operational baseline: node drain/cordon discipline and `NotReady`
   diagnosis via
   [kubernetes-node-maintenance-and-troubleshooting](../kubernetes-node-maintenance-and-troubleshooting/SKILL.md).
   **Note what does *not* apply here:** AKS's control plane and etcd are
   fully Azure-managed — the procedures in
   [etcd-backup-restore-and-cluster-health](../etcd-backup-restore-and-cluster-health/SKILL.md)
   do not apply; rely on AKS diagnostic settings routed to the landing
   zone's central Log Analytics workspace instead.

## Best practices

- Decide the CNI mode (Phase 3) and create every Entra ID managed
  identity the cluster will need (Phase 1) before Phase 2's `az aks
  create` runs — both are far more disruptive to change after the fact
  than any later phase's decisions.
- Treat Phase 6 as a hard gate before Phase 7 — an unvalidated overlay
  CNI or ingress path surfaces as a confusing application bug instead of
  a clean pre-handoff finding if skipped.
- Rehearse this sequence in a non-production subscription first,
  specifically to validate the CNI mode choice against the real VNet's
  IP budget before committing a production cluster to it.
- Keep the whole sequence as versioned IaC (Terraform/Bicep, Helm values,
  cert-manager manifests) in one repository per cluster.
- Route AKS diagnostic settings to the landing zone's shared Log
  Analytics workspace from cluster creation, not retrofitted after
  production traffic already flows.

## Common pitfalls

- **Symptom:** cert-manager's `Certificate` in Phase 5 never leaves
  `Pending`, with the `Challenge` object reporting an authorization
  failure against Azure DNS.
  **Fix:** This traces back to Phase 1/2: either the federated
  credential's `issuer` doesn't match the AKS OIDC issuer URL exactly
  (captured once, right after cluster creation — a stale or mistyped
  value here is common if it wasn't saved), or the `subject` doesn't
  match `system:serviceaccount:cert-manager:cert-manager` precisely, or
  the `DNS Zone Contributor` role was never assigned at the correct zone
  scope. Confirm all three before assuming the DNS-01 solver
  configuration itself is wrong.

- **Symptom:** After Phase 2 completes, someone realizes `NetworkPolicy`
  enforcement is actually required and tries to switch CNI modes on the
  running cluster.
  **Fix:** Azure CNI mode (Overlay vs. VNet-integrated vs. Kubenet) is
  set at cluster creation and is not a live-cluster setting to flip. This
  requires provisioning a new cluster with the corrected mode (or, for
  policy enforcement specifically, layering Azure CNI Powered by Cilium
  or Calico on top of the existing mode rather than changing the mode
  itself) — decide this in Phase 3 before Phase 2 runs, not after.

- **Symptom:** A workload team requests Workload Identity access for
  `payments-api` in Phase 7, and it silently doesn't work even though the
  managed identity clearly exists.
  **Fix:** The managed identity created in Phase 1 has no federated
  credential yet — that step only happens once the OIDC issuer URL from
  Phase 2 exists, and it's easy to create the identity early (as
  recommended) and then forget to complete the federation once the
  cluster is up. Confirm `az identity federated-credential list
  --identity-name payments-api-identity` shows the expected entry before
  troubleshooting the workload itself.

- **Symptom:** The cluster is declared "production ready" and handed off
  the same day Phase 2 completes, skipping Phase 6 — and a storage
  provisioning gap or overlay-CNI cross-node issue surfaces days later
  under real traffic.
  **Fix:** Treat Phase 6 as a required gate, not optional — see
  [kubernetes-cluster-post-provision-conformance-validation](../kubernetes-cluster-post-provision-conformance-validation/SKILL.md)
  for exactly the checklist this catches before handoff.

## Worked example

**Scenario:** Deploy `payments-api` end-to-end on a new AKS cluster in a
freshly vended subscription, with Azure CNI Overlay, ingress-nginx (for
parity with an existing EKS cluster), Azure DNS-01, and a full validation
gate before handoff.

```bash
# Phase 1 — identities planned up front
az identity create --name payments-api-identity --resource-group payments-rg
az identity create --name cert-manager-dns01-identity --resource-group payments-rg

# Phase 2 — cluster with workload identity + OIDC issuer enabled at creation
az aks create --name payments-prod --resource-group payments-rg \
  --kubernetes-version 1.30 --enable-managed-identity \
  --enable-oidc-issuer --enable-workload-identity \
  --network-plugin azure --network-plugin-mode overlay --enable-private-cluster
az aks get-credentials --name payments-prod --resource-group payments-rg
AKS_OIDC_ISSUER=$(az aks show --name payments-prod --resource-group payments-rg \
  --query "oidcIssuerProfile.issuerUrl" -o tsv)

# Phase 3 — overlay CNI already active; confirm
kubectl get pods -n kube-system -l k8s-app=azure-cni

# Phase 4 — ingress-nginx via Helm
helm install ingress-nginx ingress-nginx/ingress-nginx \
  --namespace ingress-nginx --create-namespace \
  --set controller.service.type=LoadBalancer
kubectl get svc -n ingress-nginx ingress-nginx-controller   # note EXTERNAL-IP
az network dns record-set a add-record --zone-name example.com \
  --resource-group dns-rg --record-set-name payments --ipv4-address <EXTERNAL_IP>

# Phase 5 — cert-manager federated credential + Azure DNS-01
az identity federated-credential create \
  --name cert-manager-fic --identity-name cert-manager-dns01-identity \
  --resource-group payments-rg --issuer "$AKS_OIDC_ISSUER" \
  --subject system:serviceaccount:cert-manager:cert-manager
helm install cert-manager jetstack/cert-manager \
  --namespace cert-manager --create-namespace --version v1.15.1 --set crds.enabled=true
kubectl apply -f azure-dns-staging-issuer.yaml   # validate, then swap to prod

# Phase 6 — validation gate
sonobuoy run --mode quick --wait && sonobuoy results "$(sonobuoy retrieve)"
sonobuoy run --mode certified-conformance --wait && sonobuoy results "$(sonobuoy retrieve)" --mode=report

# Phase 7 — workload identity + first workload
az identity federated-credential create \
  --name payments-api-fic --identity-name payments-api-identity \
  --resource-group payments-rg --issuer "$AKS_OIDC_ISSUER" \
  --subject system:serviceaccount:payments:payments-api
helm upgrade --install payments-api oci://ghcr.io/example/charts/payments-api \
  --version 2.3.0 --namespace payments --create-namespace --atomic --timeout 5m

# Phase 8 — health baseline
kubectl get nodes
kubectl get pdb -A
```

`curl -I https://payments.example.com` returns `HTTP/2 200` with a
Let's Encrypt production certificate, confirming the full sequence wired
together correctly, and the node maintenance runbook (Phase 8) is
documented before the first planned patch window.

## Cross-references

- [azure-landing-zone-setup](../../../cloud/skills/azure-landing-zone-setup/SKILL.md) — the Management Group/subscription/guardrail layer this sequence assumes already exists.
- [cloud-iam-hardening](../../../cloud/skills/cloud-iam-hardening/SKILL.md) — least-privilege design for every identity created across Phases 1, 5, and 7.
- [managed-kubernetes-eks-aks-gke](../managed-kubernetes-eks-aks-gke/SKILL.md) — full detail for Phase 2's cluster/node pool/workload identity provisioning.
- [cni-networking-calico-flannel](../cni-networking-calico-flannel/SKILL.md) — the Calico alternative/complement to Azure CNI referenced in Phase 3.
- [ingress-nginx-configuration](../ingress-nginx-configuration/SKILL.md) — full detail for the ingress-nginx path in Phase 4.
- [cert-manager-tls-automation](../cert-manager-tls-automation/SKILL.md) — full detail for Phase 5's Issuer/Certificate setup.
- [kubernetes-cluster-post-provision-conformance-validation](../kubernetes-cluster-post-provision-conformance-validation/SKILL.md) — full detail for Phase 6's validation gate.
- [helm-chart-authoring](../helm-chart-authoring/SKILL.md) — full detail for Phase 7's chart packaging and release discipline.
- [kubernetes-node-maintenance-and-troubleshooting](../kubernetes-node-maintenance-and-troubleshooting/SKILL.md) — the ongoing operational baseline established in Phase 8.
- [etcd-backup-restore-and-cluster-health](../etcd-backup-restore-and-cluster-health/SKILL.md) — explains why its procedures do not apply to this managed control plane.
