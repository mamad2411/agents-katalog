---
name: gcp-landing-zone-setup
description: >
  Guides designing and implementing a GCP landing zone using the Resource
  Manager folder hierarchy, Organization Policy constraints, VPC Service
  Controls, and project vending aligned to Google's enterprise foundation
  blueprint. Use when a user asks to "design a GCP folder structure", "set
  up a GCP landing zone", "implement Organization Policy guardrails",
  "onboard a new GCP project", "structure our Google Cloud organization",
  or "apply the Google Cloud enterprise foundations blueprint".
license: Apache-2.0
compatibility: "Claude Code, GitHub Copilot, OpenAI Codex, Cursor, Gemini CLI"
metadata:
  domain: cloud
  maturity: stable
---

# GCP Landing Zone Setup

## Purpose

GCP's isolation boundary is the **project** — cheap to create, billed
independently, but with no inherent hierarchy unless one is imposed through
Resource Manager folders. Without a landing zone, organizations accumulate
hundreds of ungoverned projects with inconsistent Organization Policies,
no shared VPC, and IAM bindings granted directly at the project level with
no audit trail of why. This skill defines a landing zone aligned to
Google's **enterprise foundations blueprint**: a folder hierarchy that
encodes environment and business-unit boundaries, Organization Policy
constraints enforced top-down, Shared VPC for centralized networking, and
a repeatable project-vending factory — so new projects are compliant and
network-connected the moment they're created.

## When to use

- Standing up a brand-new Google Cloud Organization or bringing
  ungoverned projects under Resource Manager folder control.
- Designing the folder hierarchy and deciding which Organization Policy
  constraints apply at which folder level.
- Onboarding a new team, product, or environment as a GCP project.
- Migrating from ad hoc project creation to the Terraform-based project
  factory pattern (`terraform-google-modules/project-factory`).
- Auditing an existing organization for projects that sit outside any
  folder governance, or for Organization Policy drift.

## Prerequisites & environment

- Organization Admin (`roles/resourcemanager.organizationAdmin`) or
  equivalent custom role at the Organization node to create folders and
  Organization Policies.
- A Cloud Identity or Google Workspace domain already established (GCP
  Organizations are anchored to one of these) and Google Groups modeled
  for IAM binding (never bind IAM directly to individual user accounts in
  a landing zone).
- `gcloud` CLI ≥ 470.0.0 and Terraform ≥ 1.5 with the `google` /
  `google-beta` providers ≥ 5.x if using IaC — the project-factory and
  folder modules track provider versions closely; pin them.
- A billing account (or multiple, if business units are billed
  separately) and rights to link projects to it
  (`roles/billing.user` at minimum).
- Decide the network model up front: **Shared VPC** (host project owns
  the VPC, service projects attach to it — the default recommendation)
  vs. VPC Network Peering between independent VPCs (only when workloads
  genuinely need separate network admin boundaries).

## Step-by-step guidance

1. **Design the folder hierarchy** before creating any project. The
   enterprise foundations blueprint default:
   ```
   Organization
   ├── fldr-bootstrap        (seed project, Terraform state buckets)
   ├── fldr-common           (shared services: CI/CD, artifact registry)
   ├── fldr-network          (Shared VPC host projects, Cloud NAT/Interconnect)
   ├── fldr-production
   │   ├── prj-checkout-prod
   │   └── prj-payments-prod
   ├── fldr-non-production
   │   ├── prj-checkout-dev
   │   └── prj-payments-staging
   └── fldr-development       (individual/sandbox projects)
   ```
   Keep `fldr-production` and `fldr-non-production` as separate top-level
   folders (not nested under a single "workloads" folder) so Organization
   Policies that must differ between environments (e.g. allowed regions,
   OS Login enforcement) attach cleanly without complex conditions.

2. **Create the folder hierarchy** with Terraform:
   ```hcl
   resource "google_folder" "production" {
     display_name = "fldr-production"
     parent       = "organizations/<ORG_ID>"
   }

   resource "google_folder" "checkout_prod_parent" {
     display_name = "fldr-checkout"
     parent       = google_folder.production.name
   }
   ```

3. **Apply Organization Policy constraints at the folder level.** Example
   — restrict resource locations and disable default service account
   broad roles:
   ```hcl
   resource "google_org_policy_policy" "resource_locations" {
     name   = "folders/${google_folder.production.folder_id}/policies/gcp.resourceLocations"
     parent = google_folder.production.name

     spec {
       rules {
         values {
           allowed_values = ["in:us-locations", "in:eu-locations"]
         }
       }
     }
   }

   resource "google_org_policy_policy" "disable_sa_key_creation" {
     name   = "organizations/<ORG_ID>/policies/iam.disableServiceAccountKeyCreation"
     parent = "organizations/<ORG_ID>"

     spec {
       rules { enforce = "TRUE" }
     }
   }
   ```
   Set `iam.disableServiceAccountKeyCreation` and
   `iam.disableServiceAccountKeyUpload` at the **Organization** node —
   long-lived service account keys are one of the most common GCP
   credential-leak vectors, and Workload Identity Federation (see
   `cloud-iam-hardening`) removes the need for them almost entirely.

4. **Vend projects through a project factory**, not manual `gcloud
   projects create`, so every project lands in the correct folder,
   attaches to the correct billing account, enables the required APIs,
   and attaches to Shared VPC automatically:
   ```hcl
   module "checkout_prod_project" {
     source  = "terraform-google-modules/project-factory/google"
     version = "~> 17.0"

     name              = "prj-checkout-prod"
     org_id            = "<ORG_ID>"
     folder_id         = google_folder.checkout_prod_parent.folder_id
     billing_account   = "<BILLING_ACCOUNT_ID>"
     activate_apis     = ["compute.googleapis.com", "run.googleapis.com"]
     svpc_host_project_id = "prj-net-host-prod"
   }
   ```

5. **Stand up the Shared VPC host project first** in `fldr-network`,
   with Cloud NAT, Cloud Interconnect/VPN, and Private Google Access
   configured, then attach service projects (`prj-checkout-prod`, etc.)
   as they're vended — sequencing host-before-service avoids retrofitting
   subnet/IAM attachment later.

6. **Enable an organization-wide log sink** to a centralized project
   (`fldr-common`) using an aggregated log sink at the Organization node,
   so every project's Admin Activity and Data Access audit logs land in
   one place regardless of which folder the project sits in:
   ```bash
   gcloud logging sinks create org-audit-sink \
     bigquery.googleapis.com/projects/prj-logging/datasets/audit_logs \
     --organization=<ORG_ID> --include-children \
     --log-filter='logName:"logs/cloudaudit.googleapis.com"'
   ```

7. **Layer VPC Service Controls around sensitive data projects** (e.g.
   those holding customer PII in BigQuery/Cloud Storage) as a perimeter
   that blocks data exfiltration even if IAM is misconfigured — this is
   GCP's closest analog to network-layer guardrails for managed services
   and has no direct AWS/Azure equivalent, so budget separate design time
   for it.

8. **Validate with a canary project**: vend one throwaway project through
   the factory, confirm Organization Policy constraints show as enforced
   (`gcloud resource-manager org-policies describe`), Shared VPC
   attachment succeeded, and the aggregated log sink captured its audit
   logs, then delete it.

## Best practices

- Bind IAM at the **folder level using Google Groups**
  (`group:checkout-team@example.com`), not individual users or
  project-level bindings, so access review is one place per team.
- Disable **service account key creation org-wide** and use Workload
  Identity Federation for external workloads and attached service
  accounts for GCE/GKE/Cloud Run — see `cloud-iam-hardening` for the
  detailed pattern.
- Use **Shared VPC** as the default network model; only use VPC Peering
  or standalone VPCs when a team has a genuine regulatory or
  administrative-boundary reason to own its own network.
- Keep **Organization Policies as narrow constraints, not primary
  authorization** — they constrain what's possible (e.g. allowed
  regions, external IPs), while IAM still governs who can do what.
- Version the folder/policy/project-factory Terraform in Git with a
  remote state backend created in the bootstrap project — don't let the
  landing zone itself depend on infrastructure it hasn't provisioned yet.
- Enable **Security Command Center** (Premium tier for production
  organizations) scoped at the Organization node so misconfigurations are
  visible centrally, not per-project.

## Common pitfalls

- **Symptom:** A new project's Terraform apply succeeds, but IAM bindings
  for the team's Google Group never take effect.
  **Fix:** The Google Group wasn't created (or wasn't yet propagated in
  Cloud Identity) before the project-factory module ran. Groups must
  exist before referencing them in `google_project_iam_member` —
  otherwise the API call silently no-ops or errors depending on provider
  version. Create groups in a separate, earlier Terraform apply or via
  Workspace Admin API first.

- **Symptom:** Default compute service account has Editor role on every
  new project, discovered during a security review months later.
  **Fix:** GCP auto-grants the Compute Engine default service account
  `roles/editor` unless the `iam.automaticIamGrantsForDefaultServiceAccounts`
  Organization Policy constraint is enforced. Set that constraint at the
  Organization node before vending any projects, and remediate existing
  projects by explicitly removing the binding and granting narrower
  custom roles.

- **Symptom:** A workload team's project can't reach the internet, and
  Cloud NAT logs show nothing.
  **Fix:** The service project was attached to Shared VPC but no Cloud
  NAT gateway exists in the subnet's region in the host project — Shared
  VPC attachment does not include NAT by default. Provision a Cloud NAT
  gateway per region in the host project, not per service project.

- **Symptom:** Billing spikes in `fldr-development` sandbox projects with
  no clear owner.
  **Fix:** No project-level budget alert or lifecycle policy was attached
  at vend time. Add a Cloud Billing budget with a Pub/Sub notification
  and an automated (human-approved) project-shutdown Cloud Function for
  the development folder specifically — never automate deletion of
  production-folder projects the same way.

## Worked example

**Scenario:** A media company has a handful of ungoverned GCP projects
created ad hoc by individual engineers and wants a real landing zone
before launching a new streaming analytics product.

1. Create the Organization-level folder hierarchy:
   `fldr-bootstrap`, `fldr-common`, `fldr-network`, `fldr-production`,
   `fldr-non-production`, `fldr-development`.
2. Move existing ungoverned projects into `fldr-development` temporarily
   and tag them for review/decommission.
3. Set `iam.disableServiceAccountKeyCreation` and
   `iam.automaticIamGrantsForDefaultServiceAccounts` (disabled) at the
   Organization node.
4. Stand up `prj-net-host-prod` in `fldr-network` with Shared VPC, Cloud
   NAT, and Private Google Access enabled.
5. Use the project factory to vend `prj-streaming-analytics-prod` into
   `fldr-production` and `prj-streaming-analytics-dev` into
   `fldr-non-production`, both attaching to the Shared VPC host and
   inheriting the region-restriction Organization Policy.
6. Bind `group:streaming-team@example.com` as `roles/editor` on the dev
   project and a narrower custom role on the prod project.
7. Result: the new product launches with centralized networking,
   enforced region and key-creation policies, and group-based IAM — while
   legacy ungoverned projects are queued for the same treatment instead
   of blocking the new launch.

## Cross-references

- [cloud-iam-hardening](../cloud-iam-hardening/SKILL.md)
- [multi-cloud-networking-patterns](../multi-cloud-networking-patterns/SKILL.md)
- [cloud-cost-finops-optimization](../cloud-cost-finops-optimization/SKILL.md)
