---
name: oci-landing-zone-setup
description: >
  Guides designing and implementing an Oracle Cloud Infrastructure (OCI)
  landing zone using the Compartment hierarchy, Identity Domains and IAM
  policies, Cloud Guard/Security Zones, and the CIS OCI Landing Zone
  reference architecture — including tenancy/region structure and hybrid
  connectivity via FastConnect. Use when a user asks to "design an OCI
  landing zone", "set up OCI compartments", "structure our OCI tenancy",
  "implement the CIS OCI Landing Zone", "write OCI IAM policies", "onboard
  a new OCI compartment or workload", or "compare OCI's account model to
  AWS/Azure/GCP".
license: Apache-2.0
compatibility: "Claude Code, GitHub Copilot, OpenAI Codex, Cursor, Gemini CLI"
metadata:
  domain: cloud
  maturity: stable
---

# OCI Landing Zone Setup

## Purpose

OCI has no separate-account model like AWS or GCP-project model — a single
**tenancy** is the entire organization, and everything inside it is
organized by **Compartments**, a hierarchical logical container that is
simultaneously the OU-equivalent grouping construct *and* the place
resources actually live. Get the compartment design wrong and every
workload ends up flat in the root compartment with IAM policies that can't
be scoped cleanly, no separation between security tooling and application
resources, and no way to delegate administration without granting
tenancy-wide access. This skill defines a landing zone aligned to Oracle's
**CIS OCI Landing Zone** reference architecture: a compartment hierarchy
that encodes environment/function boundaries, IAM policies written in
OCI's plain-language policy grammar and scoped per compartment, Identity
Domains for identity isolation, Cloud Guard and Security Zones for
guardrail enforcement, and a hub network built on the Dynamic Routing
Gateway (DRG) — so new workloads land compliant and network-connected from
the first `terraform apply`.

## When to use

- Standing up a brand-new OCI tenancy or bringing an ungoverned "everything
  in the root compartment" tenancy under proper compartment governance.
- Designing the compartment hierarchy and deciding which IAM policies,
  Cloud Guard targets, and Security Zone recipes apply at which
  compartment level.
- Onboarding a new team, product, or environment as an OCI compartment.
- Implementing or migrating to Oracle's CIS OCI Landing Zone Terraform
  reference architecture instead of hand-rolled, console-managed
  compartments and policies.
- Setting up Identity Domains for isolated identity realms (e.g. a
  separate domain for external partner or B2C access) rather than
  overloading the default domain.
- Auditing an existing tenancy for compartment drift, over-broad policies
  attached at the tenancy (root) level, or resources sitting directly in a
  parent compartment instead of a purpose-built leaf compartment.
- Explaining how OCI's tenancy/compartment/Identity Domain model maps to
  (and differs from) AWS Organizations/OUs, Azure Management
  Groups/subscriptions, or GCP folders/projects.

## Prerequisites & environment

- An OCI tenancy already provisioned, with **Administrators** group
  membership (or a narrower delegated-admin policy) for whoever runs the
  initial compartment/policy bootstrap.
- Know that the tenancy's **home region is permanent** — chosen at
  sign-up and never changeable — while additional regions are opt-in via
  `oci iam region-subscription create`. Decide the home region and the
  initial subscribed-region set before building anything region-specific
  (Vault keys, Identity Domains, and some other resources have region
  affinity).
- OCI CLI ≥ 3.40 and Terraform ≥ 1.5 with the `oci` provider ≥ 5.x if
  using infrastructure as code — pin the provider version, since
  Identity Domain resources changed materially between provider 4.x and
  5.x generations.
- Decide up front: Oracle's open-source **CIS OCI Landing Zone**
  Terraform reference architecture (opinionated, aligned to the CIS OCI
  Foundations Benchmark, fastest path to a compliant baseline) vs. a
  fully custom compartment/policy Terraform module for teams with
  unusual compartment topology needs.
- Decide the **Identity Domain strategy**: the tenancy ships with one
  default Identity Domain; only create additional domains when you need a
  genuinely isolated identity realm (e.g. external partners, a sandbox for
  testing IAM changes safely) — each extra domain is a separate user/group
  namespace with its own licensing tier (`free`, `premium`,
  `oracle-apps-premium`, `external-user`).
- A budget for FastConnect (dedicated interconnect) provisioning lead time
  if hybrid connectivity to on-premises or another cloud is in scope —
  unlike a VPN, a physical circuit has a multi-week turnaround.

## Step-by-step guidance

1. **Design the compartment hierarchy before creating any resource.** A
   defensible starting structure, modeled on the CIS OCI Landing Zone:
   ```
   Tenancy (root compartment)
   ├── Security
   │   ├── (Cloud Guard, Vault, centralized Object Storage log archive)
   ├── Network
   │   ├── (DRG hub, hub VCN, FastConnect/Site-to-Site VPN)
   ├── Workloads
   │   ├── Production
   │   │   ├── payments-prod
   │   │   └── checkout-prod
   │   └── NonProduction
   │       ├── payments-dev
   │       └── checkout-staging
   └── Sandbox
       └── individual developer compartments
   ```
   Unlike an AWS OU (which only ever contains accounts) or a GCP folder
   (which only contains projects), an OCI compartment can hold **both**
   sub-compartments **and** resources directly — put actual workload
   resources only in leaf compartments (`checkout-prod`, not `Workloads`
   or `Production`), or IAM policies scoped to the leaf become
   unenforceable because resources leak into the parent.

2. **Create the compartment hierarchy** with Terraform:
   ```hcl
   resource "oci_identity_compartment" "network" {
     compartment_id = var.tenancy_ocid
     name           = "Network"
     description    = "Hub networking resources"
     enable_delete  = false
   }

   resource "oci_identity_compartment" "workloads_prod" {
     compartment_id = oci_identity_compartment.workloads.id
     name           = "Production"
     description    = "Production workload compartments"
   }

   resource "oci_identity_compartment" "checkout_prod" {
     compartment_id = oci_identity_compartment.workloads_prod.id
     name           = "checkout-prod"
     description    = "checkout-prod workload"
   }
   ```
   Or via CLI for a quick bootstrap:
   ```bash
   oci iam compartment create \
     --compartment-id <TENANCY_OCID> \
     --name Network \
     --description "Hub networking resources"
   ```

3. **Write IAM policies scoped to compartments**, using OCI's
   plain-language policy grammar (`Allow <subject> to <verb>
   <resource-type> in compartment <path>`), referencing nested
   compartments with a colon-separated path:
   ```hcl
   resource "oci_identity_policy" "network_admins" {
     compartment_id = var.tenancy_ocid
     name           = "network-admins-policy"
     description    = "Network team manages networking resources"
     statements = [
       "Allow group NetworkAdmins to manage virtual-network-family in compartment Network",
       "Allow group NetworkAdmins to manage virtual-network-family in compartment Workloads:Production:checkout-prod",
     ]
   }

   resource "oci_identity_policy" "checkout_team_delegated_admin" {
     compartment_id = oci_identity_compartment.checkout_prod.id
     name           = "checkout-team-admin-policy"
     description    = "Delegate self-service admin within the leaf compartment only"
     statements = [
       "Allow group CheckoutTeam to manage all-resources in compartment checkout-prod",
     ]
   }
   ```
   The four policy verbs (`inspect` < `read` < `use` < `manage`) are
   additive in privilege — grant the narrowest verb that satisfies the
   need, the same discipline as scoping an AWS IAM action list or a GCP
   custom role.

4. **Use Dynamic Groups for workload identity, not embedded API keys.**
   OCI's analog to an AWS instance profile or a GCP attached service
   account is a **Dynamic Group** — a rule-based group matching compute
   instances or resources, granted permissions via ordinary policy
   statements:
   ```hcl
   resource "oci_identity_dynamic_group" "checkout_compute" {
     compartment_id = var.tenancy_ocid
     name           = "checkout-prod-compute"
     description    = "Compute instances in checkout-prod"
     matching_rule  = "ALL {instance.compartment.id = '${oci_identity_compartment.checkout_prod.id}'}"
   }

   resource "oci_identity_policy" "checkout_compute_policy" {
     compartment_id = var.tenancy_ocid
     name           = "checkout-compute-policy"
     statements = [
       "Allow dynamic-group checkout-prod-compute to read secret-bundles in compartment Security",
     ]
   }
   ```
   This gives compute instances short-lived instance-principal
   authentication instead of long-lived API signing keys — apply the same
   "eliminate long-lived credentials" discipline covered in
   `cloud-iam-hardening`.

5. **Deploy the CIS OCI Landing Zone Terraform reference** (or the
   hand-rolled equivalent above at smaller scale) to get the compartment
   structure, baseline IAM policies, Cloud Guard, and centralized logging
   provisioned consistently rather than assembled ad hoc across multiple
   console sessions.

6. **Stand up the hub network first**, in the `Network` compartment: a
   hub VCN with a Dynamic Routing Gateway (DRG) attached, and spoke VCNs
   (one per workload compartment) attached to the DRG:
   ```hcl
   resource "oci_core_drg" "hub" {
     compartment_id = oci_identity_compartment.network.id
     display_name   = "drg-hub"
   }

   resource "oci_core_drg_attachment" "checkout_prod" {
     drg_id       = oci_core_drg.hub.id
     vcn_id       = oci_core_vcn.checkout_prod.id
     display_name = "checkout-prod-attachment"
   }
   ```
   For hybrid connectivity to on-premises or another cloud, provision
   **FastConnect** (OCI's dedicated-interconnect equivalent to AWS Direct
   Connect / Azure ExpressRoute / GCP Cloud Interconnect) with a
   Site-to-Site VPN as failover — never a VPN-only path for
   production-critical hybrid traffic.

7. **Centralize audit and flow logs** by routing them through a Service
   Connector Hub into an Object Storage bucket in the `Security`
   compartment, with a retention rule so logs can't be shortened or
   deleted even by a compromised workload-compartment credential:
   ```bash
   oci sch service-connector create \
     --compartment-id <SECURITY_COMPARTMENT_OCID> \
     --display-name "audit-log-archive" \
     --source '{"kind":"logging","logSources":[{"compartmentId":"<TENANCY_OCID>","logGroupId":"_Audit_Include_Subcompartment"}]}' \
     --target '{"kind":"objectStorage","namespace":"<OBJECT_STORAGE_NAMESPACE>","bucketName":"security-audit-logs"}'
   ```

8. **Enable Cloud Guard tenancy-wide and layer Security Zones on
   production compartments.** Cloud Guard is OCI's detective posture
   service (the rough analog of AWS GuardDuty + Security Hub, or Azure
   Defender for Cloud / GCP Security Command Center):
   ```bash
   oci cloud-guard configuration update \
     --compartment-id <TENANCY_OCID> \
     --reporting-region us-ashburn-1 \
     --status ENABLED \
     --self-manage-resources false
   ```
   Security Zones go further than Cloud Guard's detect-and-alert model —
   attaching a Security Zone recipe to `Workloads:Production` **blocks**
   the non-compliant API call itself (e.g. creating a public Object
   Storage bucket, or a boot volume without encryption) rather than only
   flagging it after the fact, closer to an SCP/Org Policy hard guardrail
   than a Config rule.

9. **Set compartment-scoped budgets** so a runaway Sandbox workload alerts
   before it becomes a cost surprise:
   ```bash
   oci budgets budget create \
     --compartment-id <TENANCY_OCID> \
     --target-compartment-id <SANDBOX_COMPARTMENT_OCID> \
     --amount 5000 \
     --reset-period MONTHLY \
     --display-name "sandbox-monthly-budget"
   ```

10. **Validate with a canary compartment.** Vend one throwaway leaf
    compartment through the full pipeline, confirm the delegated-admin
    policy, Dynamic Group, Security Zone enforcement, and centralized
    logging all behave as expected, then delete it before opening the
    pipeline to real workload teams.

## Best practices

- Never put workload resources directly in `Workloads`, `Production`, or
  any non-leaf compartment — reserve non-leaf compartments purely for
  grouping and policy inheritance, exactly the discipline the AWS/Azure/
  GCP landing-zone skills apply to OUs/Management Groups/folders.
- Grant the **narrowest policy verb** (`inspect`/`read`/`use` before
  reaching for `manage`) and scope every statement to a specific
  compartment path — avoid `manage all-resources in tenancy`, the OCI
  equivalent of `AdministratorAccess`/`Owner`/`roles/owner`.
- Prefer **Dynamic Groups + instance/resource principal authentication**
  over embedding API signing keys in workload configuration — this is
  OCI's version of eliminating long-lived credentials (see
  `cloud-iam-hardening`).
- Keep the **default Identity Domain for internal workforce identities**
  and create additional Identity Domains only for genuinely isolated
  populations (external partners, a B2C customer-facing app) — extra
  domains are a real isolation boundary, not a free organizational nicety.
- Treat **Security Zones as the primary preventive guardrail** for
  production compartments and **Cloud Guard as the detective layer**
  everywhere else — they're complementary, not substitutes for one
  another.
- Version the compartment/policy/network Terraform in Git and run the
  canary-compartment validation in CI before merging changes that touch
  shared policy statements.
- Budget-alert every compartment, not just Sandbox — production
  compartments benefit from anomaly detection just as much, just tuned to
  a higher threshold.

## Common pitfalls

- **Symptom:** A policy statement referencing `in compartment
  Production` grants access far more broadly than intended, or a policy
  written for a leaf compartment silently does nothing.
  **Fix:** Nested compartments must be referenced by their full
  colon-separated path (`Workloads:Production:checkout-prod`), not just
  the leaf name, once there's ambiguity across the hierarchy — or,
  conversely, granting `manage ... in compartment Production` also
  applies to every sub-compartment beneath it (including `NonProduction`
  siblings if the hierarchy was flattened incorrectly). Confirm the
  actual compartment path with `oci iam compartment list
  --compartment-id-in-subtree true` before trusting a policy's scope.

- **Symptom:** A policy statement referencing a group in a non-default
  Identity Domain (e.g. an isolated `Partners` domain) fails to grant
  access, even though the group clearly exists.
  **Fix:** Groups outside the default Identity Domain must be qualified
  with the domain name in policy statements —
  `Allow group Partners/PartnerViewers to read object-family in
  compartment Shared`, not just `Allow group PartnerViewers to ...`.
  Forgetting the domain prefix is the single most common OCI multi-domain
  policy authoring mistake.

- **Symptom:** Resources keep appearing directly in the `Production` or
  `Workloads` compartment instead of a team's leaf compartment, and the
  team's delegated-admin policy doesn't apply to them.
  **Fix:** Because OCI compartments can hold resources at every level of
  the hierarchy (unlike an AWS OU or GCP folder), nothing stops an
  engineer from creating a resource one level too high. Enforce leaf-only
  resource placement with a Security Zone recipe requiring resources to
  live in a tagged "leaf" compartment, and periodically audit with
  `oci search resource structured-search` for resources sitting in
  non-leaf compartments.

- **Symptom:** A Terraform apply that provisions Vault keys or an
  Identity Domain in a newly subscribed region fails or behaves
  inconsistently with the home region's equivalent resource.
  **Fix:** Some resources (Vault master encryption keys, Identity
  Domains) have region affinity and don't automatically replicate to
  newly subscribed regions the way compartments and policies (which are
  tenancy-wide) do. Explicitly provision the region-scoped resource in
  each subscribed region rather than assuming it inherits from the home
  region.

- **Symptom:** A Dynamic Group's matching rule stops granting access
  after a compute instance is moved to a different compartment as part of
  a reorg.
  **Fix:** Dynamic Group matching rules keyed on `instance.compartment.id`
  are evaluated live — moving the instance changes which dynamic groups
  it matches, silently revoking (or granting) access. Prefer matching on
  a stable freeform/defined tag (`instance.tag.namespace.key = 'value'`)
  over compartment ID when instances are expected to move between
  compartments during their lifecycle.

## Worked example

**Scenario:** A company with one flat OCI tenancy (all resources sitting
in the root compartment, one shared Administrators-group login for
everyone) needs a real landing zone before launching a second product
line and before OCI resources fail their first security audit.

1. Create the compartment hierarchy: `Security`, `Network`, `Workloads`
   (with `Production`/`NonProduction`), and `Sandbox`, all under the
   tenancy root, using the Terraform module shown above.
2. Migrate the existing legacy application's resources into
   `Workloads:Production:legacy-app` via compartment move operations
   (`oci iam compartment ... ` resource moves are per-resource-type; plan
   this as a tracked migration, not a bulk operation).
3. Enable Cloud Guard tenancy-wide and attach a Security Zone recipe to
   `Workloads:Production` blocking public bucket creation and
   unencrypted boot volumes.
4. Stand up the hub VCN and DRG in `Network`, with FastConnect ordered for
   the primary on-premises connection and a Site-to-Site VPN configured
   as immediate failover while the physical circuit provisions.
5. Create `Workloads:Production:checkout-prod` and
   `Workloads:NonProduction:checkout-staging` for the new product line,
   each with a DRG attachment to the hub, a delegated-admin policy scoped
   to `CheckoutTeam`, and a Dynamic Group granting the compartment's
   compute instances read access to Vault secrets in `Security` — no
   embedded API keys anywhere in the deployment.
6. Route Audit and VCN Flow Logs through a Service Connector Hub into an
   Object Storage bucket in `Security` with a retention rule, and set a
   compartment-scoped budget on `Sandbox`.
7. Result: two product lines, a compliant compartment hierarchy, Security
   Zone guardrails enforced (not just monitored) on production, and zero
   long-lived API keys in the new workload's deployment path.

## Cross-references

- [aws-landing-zone-setup](../aws-landing-zone-setup/SKILL.md)
- [azure-landing-zone-setup](../azure-landing-zone-setup/SKILL.md)
- [gcp-landing-zone-setup](../gcp-landing-zone-setup/SKILL.md)
- [cloud-iam-hardening](../cloud-iam-hardening/SKILL.md)
