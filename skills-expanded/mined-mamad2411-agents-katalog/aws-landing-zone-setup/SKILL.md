---
name: aws-landing-zone-setup
description: >
  Guides designing and implementing a multi-account AWS landing zone using
  AWS Organizations, Control Tower, and Account Factory — including the
  account/OU hierarchy, Service Control Policies, centralized logging, and
  baseline guardrails. Use when a user asks to "set up a new AWS account
  structure", "design an AWS landing zone", "implement AWS Control Tower",
  "create OUs and SCPs", "bootstrap a multi-account AWS environment", or
  "onboard a new AWS account into our organization".
license: Apache-2.0
compatibility: "Claude Code, GitHub Copilot, OpenAI Codex, Cursor, Gemini CLI"
metadata:
  domain: cloud
  maturity: stable
---

# AWS Landing Zone Setup

## Purpose

A landing zone is the multi-account foundation an organization builds once
and every application team builds on top of afterward: account structure,
identity, network, logging, and guardrails. Getting it wrong is expensive to
unwind — teams end up with flat single-account sprawl, inconsistent
tagging, no centralized audit trail, and no policy enforcement boundary
between "sandbox" and "production." This skill defines a repeatable,
Control-Tower-based AWS landing zone so new accounts are vended consistently,
guardrails are enforced at the Organizational Unit (OU) level instead of
per-account, and security/audit teams get a single pane of glass without
blocking developer velocity.

## When to use

- Standing up AWS for a new organization or migrating off a single flat
  AWS account.
- Designing the OU hierarchy and deciding which Service Control Policies
  (SCPs) apply where.
- Onboarding a new business unit, environment, or acquired company into an
  existing AWS Organization.
- Reviewing/auditing an existing landing zone for drift (e.g. accounts
  created outside Control Tower, missing guardrails, orphaned root-level
  IAM users).
- Migrating from a hand-rolled multi-account setup to AWS Control Tower or
  Landing Zone Accelerator (LZA).

## Prerequisites & environment

- An AWS Organization already exists or you have rights to create one
  (`organizations:CreateOrganization`) from a dedicated **Management
  Account** that runs no workloads.
- AWS CLI v2 and, if using infrastructure-as-code, Terraform ≥ 1.5 (for the
  `aws` provider ≥ 5.x) or the AWS Landing Zone Accelerator (LZA) CDK
  toolchain.
- Decide up front: Control Tower (AWS-managed, opinionated, fastest to
  start) vs. Landing Zone Accelerator (more customizable, config-as-code,
  used when you need FedRAMP/regulated-industry guardrails Control Tower
  doesn't ship out of the box) vs. fully custom Terraform (only for teams
  with deep multi-account IaC maturity already).
- Enable AWS IAM Identity Center (successor to AWS SSO) in the management
  account — Control Tower assumes it for federated human access.
- A registered root/parent domain or subdomain delegation if you plan
  per-account Route 53 zones.
- Budget for the mandatory Control Tower resources: a Log Archive account
  and an Audit account are created automatically and incur S3/CloudTrail/
  Config costs even when idle.

## Step-by-step guidance

1. **Design the OU hierarchy before creating any account.** A defensible
   starting structure:
   ```
   Root
   ├── Security OU
   │   ├── Log Archive (AWS-managed by Control Tower)
   │   └── Audit (AWS-managed by Control Tower)
   ├── Infrastructure OU
   │   ├── Network (Transit Gateway hub, Route 53 Resolver)
   │   └── Shared Services (CI/CD runners, artifact registries)
   ├── Workloads OU
   │   ├── Prod OU
   │   │   ├── payments-prod
   │   │   └── checkout-prod
   │   └── NonProd OU
   │       ├── payments-dev
   │       └── checkout-staging
   └── Sandbox OU
       └── individual developer sandboxes
   ```
   Keep environment separation (Prod vs. NonProd) at the OU level, not the
   account-name level, so SCPs and Config rules can target the OU.

2. **Enable AWS Organizations with all features** (not consolidated
   billing only) so SCPs, tag policies, and delegated administration work:
   ```bash
   aws organizations create-organization --feature-set ALL
   ```

3. **Bootstrap Control Tower** in the management account via the console
   or the `aws-ia/aws-ia-landing-zone-accelerator` reference architecture.
   Control Tower will provision the Log Archive and Audit accounts and
   enable AWS Config, CloudTrail (org trail), and mandatory guardrails
   automatically.

4. **Enroll or vend new accounts through Account Factory**, never through
   the standalone `organizations:CreateAccount` API directly, so every
   account inherits the baseline (CloudTrail, Config, guardrail SCPs, IAM
   Identity Center permission sets) from day one. For IaC-driven vending,
   use Account Factory for Terraform (AFT):
   ```hcl
   module "aft_account_request" {
     source  = "aws-ia/aft-account-request/aws"
     version = "~> 1.0"

     control_tower_parameters = {
       AccountEmail             = "aws-payments-prod@example.com"
       AccountName               = "payments-prod"
       ManagedOrganizationalUnit = "Workloads/Prod"
       SSOUserEmail              = "payments-team@example.com"
       SSOUserFirstName          = "Payments"
       SSOUserLastName           = "Team"
     }
   }
   ```

5. **Attach Service Control Policies at the OU level.** Example — deny
   leaving the org's approved regions (defense in depth, not a substitute
   for IAM):
   ```json
   {
     "Version": "2012-10-17",
     "Statement": [
       {
         "Sid": "DenyOutsideApprovedRegions",
         "Effect": "Deny",
         "NotAction": [
           "iam:*", "organizations:*", "route53:*",
           "cloudfront:*", "waf:*", "support:*", "sts:*"
         ],
         "Resource": "*",
         "Condition": {
           "StringNotEquals": {
             "aws:RequestedRegion": ["us-east-1", "eu-west-1"]
           }
         }
       },
       {
         "Sid": "DenyRootUserActions",
         "Effect": "Deny",
         "Action": "*",
         "Resource": "*",
         "Condition": {
           "StringLike": { "aws:PrincipalArn": "arn:aws:iam::*:root" }
         }
       }
     ]
   }
   ```
   Attach the region-restriction SCP to the `Workloads` OU (not `Security`
   or `Infrastructure`, which may need `us-gov` or global services), and
   attach `DenyRootUserActions` at the Root so it applies everywhere.

6. **Centralize logging and security tooling.** Ensure the org-wide
   CloudTrail trail and AWS Config aggregator write to the Log Archive
   account, and delegate GuardDuty, Security Hub, and IAM Access Analyzer
   administration to the Audit account via
   `organizations:RegisterDelegatedAdministrator` so account teams cannot
   disable them.

7. **Define tag policies and a mandatory tagging SCP** (e.g. require
   `cost-center`, `environment`, `owner` on all taggable resources) before
   the first workload account goes live — retrofitting tags across
   thousands of resources later is far more expensive than enforcing at
   creation.

8. **Validate with a dry-run account.** Vend one throwaway account through
   the full pipeline, confirm guardrails, Config rules, and IAM Identity
   Center permission sets appear as expected, then decommission it before
   opening the pipeline to real workload teams.

## Best practices

- Never run workloads in the Management account — its only job is
  Organizations, billing, and IAM Identity Center.
- Prefer **OU-scoped SCPs over per-account SCPs**; per-account exceptions
  create drift that nobody remembers the reason for six months later.
- Use **permission sets in IAM Identity Center**, not per-account IAM
  users, for human access — this makes cross-account access auditable
  from one place and de-risks account compromise (no long-lived access
  keys for humans).
- Keep a **Sandbox OU** with a tight SCP (no internet gateway changes, no
  IAM changes, hard spend guardrails via budgets) so experimentation
  doesn't threaten production account guardrails.
- Version the OU/SCP/account-vending configuration in Git (Terraform or
  AFT) — a landing zone that lives only in the console cannot be
  reviewed, diffed, or rolled back.
- Treat SCPs as a **deny-only backstop**, not your primary authorization
  mechanism — least-privilege IAM policies inside the account are still
  required (see `cloud-iam-hardening`).
- Budget alerts and Cost Anomaly Detection should be wired into every
  vended account by default, not opted into later.

## Common pitfalls

- **Symptom:** New accounts appear in Organizations but never get
  CloudTrail, Config, or guardrails applied.
  **Fix:** Accounts were created via `organizations:CreateAccount` or the
  console directly instead of through Account Factory/AFT. Re-enroll them
  into Control Tower ("Enroll account") so the baseline is applied
  retroactively.

- **Symptom:** An SCP attached to block a risky action (e.g. disabling
  CloudTrail) also silently breaks a legitimate CI/CD role in a different
  OU.
  **Fix:** SCPs are inherited down the OU tree and apply to every
  principal in every account under that node, including service roles.
  Scope the SCP's `Condition` block tightly (e.g. by `aws:PrincipalTag`)
  and test in a non-prod OU first, not directly in the OU that contains
  production.

- **Symptom:** Cost Explorer shows steadily increasing spend in accounts
  nobody is actively using.
  **Fix:** Idle sandbox/dev accounts still accrue Config, CloudTrail,
  GuardDuty, and NAT Gateway costs from the baseline. Apply a Sandbox OU
  budget guardrail and an automated cleanup Lambda (or AWS Nuke in
  non-prod only, with explicit human approval — **never run an
  account-wide teardown tool against a production OU**).

- **Symptom:** Terraform/AFT account vending pipeline fails intermittently
  with "OU not found" errors.
  **Fix:** OU IDs, not names, are the stable reference; if an OU was
  renamed or recreated, hardcoded OU IDs in `terraform.tfvars` go stale.
  Look up OUs by name at apply time via a data source instead of
  hardcoding IDs.

## Worked example

**Scenario:** A company with one flat AWS account ("legacy-prod") wants a
proper landing zone before launching a second product line.

1. Create a new Management account (billing only, no workloads).
2. Invite `legacy-prod` into the new Organization as a member account
   under `Workloads/Prod`.
3. Enable Control Tower in the Management account; it provisions
   `log-archive` and `audit` accounts automatically.
4. Attach the region-restriction and root-lockout SCPs (shown above) to
   `Root` and the `Workloads` OU.
5. Use AFT to vend `checkout-prod` and `checkout-staging` for the new
   product line, landing in `Workloads/Prod` and `Workloads/NonProd`
   respectively — each arrives with CloudTrail, Config, GuardDuty
   delegation, and an IAM Identity Center permission set for the
   `checkout-team` group already wired up.
6. Register the Audit account as delegated administrator for GuardDuty and
   Security Hub so `checkout-team` engineers (who only have
   `PowerUserAccess` in their own account) cannot disable org-wide
   security tooling.
7. Result: two product lines, four workload accounts, one enforced set of
   guardrails, and zero manual "please remember to enable CloudTrail"
   onboarding steps.

## Cross-references

- [cloud-iam-hardening](../cloud-iam-hardening/SKILL.md)
- [multi-cloud-networking-patterns](../multi-cloud-networking-patterns/SKILL.md)
- [cloud-cost-finops-optimization](../cloud-cost-finops-optimization/SKILL.md)
