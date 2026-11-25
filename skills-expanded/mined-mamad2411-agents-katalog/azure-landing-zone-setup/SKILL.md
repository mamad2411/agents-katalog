---
name: azure-landing-zone-setup
description: >
  Guides designing and implementing an Azure landing zone using Management
  Groups, subscription democratization, Azure Policy, and the Cloud
  Adoption Framework (CAF) Landing Zone Accelerator pattern. Use when a
  user asks to "design an Azure landing zone", "set up Management Groups
  and subscriptions", "implement Azure Policy guardrails", "onboard a new
  Azure subscription", "structure our Azure tenant", or "migrate to the
  CAF enterprise-scale landing zone".
license: Apache-2.0
compatibility: "Claude Code, GitHub Copilot, OpenAI Codex, Cursor, Gemini CLI"
metadata:
  domain: cloud
  maturity: stable
---

# Azure Landing Zone Setup

## Purpose

Azure's isolation boundary is the **subscription**, not the account — and
subscriptions default to being cheap and numerous, which is a feature if
the tenant has a real Management Group hierarchy and a liability if it
doesn't. Without a landing zone, organizations end up with dozens of
subscriptions with inconsistent Azure Policy assignments, no shared
connectivity hub, and RBAC assigned ad hoc at the resource group level.
This skill defines a landing zone aligned to Microsoft's Cloud Adoption
Framework (CAF) "enterprise-scale" pattern: a Management Group hierarchy
that mirrors organizational/environment boundaries, policy-as-guardrail
enforced at scale, and a repeatable subscription vending process — so new
teams get compliant subscriptions in hours, not weeks of manual RBAC and
policy setup.

## When to use

- Standing up a new Azure tenant or restructuring subscriptions under
  Management Groups for the first time.
- Deciding the Management Group hierarchy and which Azure Policy
  initiatives apply at which level.
- Onboarding a new subscription for a business unit, product team, or
  environment (dev/test/prod).
- Migrating from the classic CAF "foundation" template to
  "enterprise-scale," or from a flat single-subscription tenant.
- Auditing an existing tenant for Azure Policy compliance drift or
  subscriptions that sit outside any Management Group governance.

## Prerequisites & environment

- Global Administrator or at least `Owner`/`User Access Administrator` at
  the tenant root Management Group to create the Management Group
  hierarchy.
- Azure CLI ≥ 2.60 or Azure PowerShell `Az` module, and Terraform ≥ 1.5
  with the `azurerm` provider ≥ 3.x if using IaC (the `azurerm`
  provider's Management Group and Policy resources changed materially
  between 2.x and 3.x — do not mix generations of examples).
- An Enterprise Agreement (EA), Microsoft Customer Agreement (MCA), or
  Cloud Solution Provider (CSP) billing relationship — subscription
  creation mechanics (and who can automate it) differ by agreement type.
- Decide the accelerator: the Azure Landing Zone (ALZ) Bicep/Terraform
  modules (`Azure/alz-terraform-accelerator`) for enterprise-scale, or a
  lighter hand-rolled Management Group + Policy setup for smaller
  estates. Enterprise-scale is the right default above roughly a handful
  of subscriptions or multiple business units.
- Microsoft Entra ID (formerly Azure AD) tenant with groups already
  modeled for RBAC assignment (don't assign roles to individual users in
  a landing zone).

## Step-by-step guidance

1. **Design the Management Group hierarchy** before creating any
   subscription. The CAF enterprise-scale default:
   ```
   Tenant Root Group
   └── Contoso (intermediate root)
       ├── Platform
       │   ├── Management (Log Analytics, Automation)
       │   ├── Connectivity (Hub VNet, Azure Firewall, ExpressRoute)
       │   └── Identity (domain controllers, if any)
       ├── Landing Zones
       │   ├── Corp (no direct internet egress)
       │   └── Online (internet-facing workloads)
       ├── Sandbox
       └── Decommissioned
   ```
   Map `Landing Zones/Corp` and `Landing Zones/Online` further into
   per-environment Management Groups (`Prod`, `NonProd`) or rely on
   subscription-level tagging plus policy `Condition`s — either is valid;
   pick one and keep it consistent.

2. **Create the Management Group hierarchy** with Terraform:
   ```hcl
   resource "azurerm_management_group" "platform" {
     display_name               = "Platform"
     parent_management_group_id = azurerm_management_group.contoso.id
   }

   resource "azurerm_management_group" "landing_zones_online" {
     display_name               = "Online"
     parent_management_group_id = azurerm_management_group.landing_zones.id
   }
   ```

3. **Assign Azure Policy initiatives at the Management Group level**, not
   per-subscription. Example — deny public IP creation in the `Corp`
   landing zone, and require diagnostic settings on all resources
   tenant-wide:
   ```json
   {
     "properties": {
       "displayName": "Deny public IP in Corp landing zone",
       "policyType": "Custom",
       "mode": "All",
       "policyRule": {
         "if": {
           "field": "type",
           "equals": "Microsoft.Network/publicIPAddresses"
         },
         "then": { "effect": "deny" }
       }
     }
   }
   ```
   Assign built-in initiatives where they exist — e.g. the
   "Azure Security Benchmark" initiative — instead of hand-authoring
   equivalents; Microsoft updates them as new services ship.

4. **Vend subscriptions through a repeatable process**, either the Azure
   subscription vending Terraform module
   (`Azure/subscription-vending/azurerm`) or a ServiceNow/self-service
   portal backed by the same Terraform. Every vended subscription should
   land directly in the correct Management Group at creation time — never
   in the tenant root — and inherit RBAC group assignments and budget
   alerts automatically:
   ```hcl
   module "subscription_vending" {
     source  = "Azure/subscription-vending/azurerm"
     version = "~> 1.0"

     subscription_alias_name        = "sub-checkout-prod"
     subscription_display_name      = "checkout-prod"
     subscription_management_group_id = azurerm_management_group.landing_zones_online.id
     subscription_billing_scope      = "<BILLING_SCOPE_ID>"
   }
   ```

5. **Stand up the Connectivity subscription first** (hub VNet, Azure
   Firewall or NVA, ExpressRoute/VPN gateway, private DNS zones) since
   every landing-zone subscription will peer to it — sequencing this
   after workload subscriptions exist means retrofitting peering and
   routes everywhere.

6. **Centralize logging**: route Activity Logs and resource diagnostic
   settings from every subscription to a shared Log Analytics workspace
   in the `Management` subscription via an Azure Policy
   `DeployIfNotExists` assignment, so new resources are captured
   automatically without per-team opt-in.

7. **Define RBAC at the Management Group and subscription level using
   Entra ID groups**, e.g. `checkout-team-contributors` mapped to
   `Contributor` on the `checkout-prod` subscription — never assign roles
   to individual user principals in a landing zone.

8. **Validate with a canary subscription**: vend one throwaway
   subscription through the pipeline, confirm policy assignments show as
   "Compliant," RBAC groups resolved correctly, and diagnostic settings
   auto-deployed, then decommission it.

## Best practices

- Keep the **Connectivity, Management, and Identity subscriptions** free
  of application workloads — they exist purely for shared platform
  services.
- Use **Azure Policy `deployIfNotExists` and `modify` effects** to
  auto-remediate common gaps (tags, diagnostic settings) instead of
  relying on `audit` effects that only report non-compliance.
- Model environment separation (`Prod`/`NonProd`) as **Management Groups
  or a consistent tag + policy condition**, decided once, not mixed
  across subscriptions.
- Prefer the **Azure Verified Modules (AVM)** or the official ALZ
  Terraform/Bicep accelerator over hand-rolled Management Group/Policy
  code — the accelerator is versioned and tested against Microsoft's
  reference architecture.
- Set **Azure Cost Management budgets and action groups** on every
  subscription at vend time, not retroactively.
- Keep policy assignments **idempotent and Git-versioned**; policy drift
  detection (`az policy state list`) should run in CI, not be discovered
  during an audit.

## Common pitfalls

- **Symptom:** A newly created subscription shows as "Not Compliant" or,
  worse, has none of the expected policies at all.
  **Fix:** Subscriptions created outside the vending pipeline (e.g.
  directly in the EA portal) land in the tenant root Management Group by
  default, which usually has no policy assignments. Move the subscription
  into the correct Management Group explicitly — policy inheritance is
  not retroactive for resources already deployed, so also trigger a
  policy remediation task.

- **Symptom:** Azure Policy assignment with `deployIfNotExists` shows
  "Compliant" but the remediation never actually ran.
  **Fix:** `deployIfNotExists` and `modify` policies require a
  system-assigned managed identity with an RBAC role (e.g.
  `Log Analytics Contributor`) granted at the assignment scope. If the
  identity's role assignment is missing, remediation silently fails while
  the policy still evaluates as compliant-pending. Check
  `az policy remediation list` for failed tasks explicitly.

- **Symptom:** Two teams both try to peer their spoke VNet to the hub and
  get overlapping address space errors.
  **Fix:** No central IP address management (IPAM) plan existed before
  subscriptions were vended. Reserve CIDR blocks per landing zone /
  environment in the vending module itself (e.g. via Azure Virtual
  Network Manager or a simple IPAM spreadsheet-as-code) before the first
  spoke is created.

- **Symptom:** Billing shows unexpectedly high spend in Sandbox
  subscriptions.
  **Fix:** Sandbox Management Group had lighter policy than intended
  (e.g. no SKU restriction policy), so a developer spun up expensive VM
  SKUs. Apply a SKU-allowlist policy and a hard subscription spending
  limit/budget action group to the Sandbox Management Group specifically.

## Worked example

**Scenario:** A retailer with a single legacy Azure subscription needs a
proper landing zone before launching an online ordering platform.

1. Create the enterprise-scale Management Group hierarchy under the
   tenant root: `Platform` (with `Connectivity`/`Management`/`Identity`),
   `Landing Zones` (with `Corp`/`Online`), `Sandbox`, `Decommissioned`.
2. Move the legacy subscription into `Landing Zones/Corp` and assign the
   Azure Security Benchmark initiative plus a tag-enforcement policy.
3. Stand up the `Connectivity` subscription with a hub VNet, Azure
   Firewall, and a shared private DNS zone for `privatelink` endpoints.
4. Use the subscription vending module to create `sub-ordering-prod` and
   `sub-ordering-dev`, landing in `Landing Zones/Online` and `Sandbox`
   respectively, each auto-peered to the hub and pre-assigned the
   "deny public IP" and "require diagnostic settings" policies.
5. Assign `ordering-team-contributors` (an Entra ID group) `Contributor`
   on `sub-ordering-dev` and a narrower custom role on
   `sub-ordering-prod`.
6. Result: the online platform launches with network isolation from the
   legacy corp subscription, centralized logging, and policy guardrails
   already enforced — no manual RBAC or policy authoring by the ordering
   team.

## Cross-references

- [cloud-iam-hardening](../cloud-iam-hardening/SKILL.md)
- [multi-cloud-networking-patterns](../multi-cloud-networking-patterns/SKILL.md)
- [cloud-cost-finops-optimization](../cloud-cost-finops-optimization/SKILL.md)
