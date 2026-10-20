---
name: define-core-iam
description: >
  Define the core IAM groups and roles for the platform team itself — the groups that govern
  access to platform-owned sectors (e.g., Platform, Security). Produces a machine-readable
  IAM definition document covering `Role("operator")`, `Role("admin")`, `Role("contributor")`, and `Role("reader")` groups per
  (Sector, Tier) combination, with JIT escalation policies and Workload Identity requirements.
  Use before provisioning cloud IAM resources or configuring a JIT tool.
license: Apache-2.0
metadata:
  version: "0.1.0"
  chapter: "5"
---

# Define Core IAM

## Skill Type

Design

## Your Goal

Produce a **core IAM definition document** — a declarative record of all groups and roles the platform team needs to operate the platform-owned sectors. This document is the input for the cloud-specific IAM provisioning skills (`manage-azure-iam`, `manage-aws-iam`, `manage-gcp-iam`) and the Kubernetes RBAC skill (`manage-k8s-iam`).

The output must be concrete: every group named, its membership policy stated, its access level and scope defined, and its JIT escalation behaviour specified.



## Notation & Types Reference

When writing configurations or documentation, you **MUST** strictly adhere to the structural notation and types defined in the book. Before proceeding, read the following reference files:
- `references/notation.md`
- `references/types.md`

## What to Gather First

Before proceeding, ask the user (or infer from context):

- **Segmentation design**: Which Sectors exist? Which Tiers? (Ideally, import the output of the `design-segmentation` skill.)
- **`Sector("platform")`s in scope**: Typically `Platform` (CI/CD, monitoring, identity tooling) and optionally `Security` (SIEM, log archives, audit systems). Confirm which are present.
- **Cloud provider(s)**: AWS, Azure, GCP, or multi-cloud. Affects naming conventions and JIT tool references.
- **Identity Provider**: Microsoft Entra ID, Okta, Google Workspace, or other. Groups will be created here.
- **CI/CD system**: GitHub Actions, GitLab CI, Azure Pipelines, or other. Determines the Workload Identity Federation trust anchor for `Role("operator")` roles.
- **platform team members**: List of individuals with their intended role (`Role("admin")`, `Role("contributor")`, Reader). At minimum, identify who holds `Role("admin")` access.
- **JIT tooling**: Azure PIM, AWS IAM Identity Center, Teleport, or none yet. Determines how escalation policies are expressed.

If the user cannot answer all questions, proceed with available information and note assumptions explicitly in the output.

## Process

### Step 1 — Enumerate the Group Matrix

For each platform-owned sector and each tier, derive the standard four groups from the role taxonomy:

| Group Name Pattern | Role | Target | Membership Policy |
|--------------------|------|--------|-------------------|
| `{sector}-{tier}-operator` | `Role("operator")` | Non-human | CI/CD runner identity only — no human members |
| `{sector}-{tier}-admins` | `Role("admin")` | Human | JIT-only. Justification required. Approval may be required for `Tier("live")`. |
| `{sector}-{tier}-contributors` | `Role("contributor")` | Human | JIT for `Tier("live")`. Standing in `Tier("sandbox")` for platform engineers. |
| `{sector}-{tier}-readers` | `Role("reader")` | Human | Standing access — granted to all platform team members |

Apply this pattern to each `(Sector, Tier)` combination. Example output for a `Sector("platform")` with `Tier("sandbox")` and `Tier("live")`:

- `platform-sandbox-operator`
- `platform-sandbox-admins`
- `platform-sandbox-contributors`
- `platform-sandbox-readers`
- `platform-live-operator`
- `platform-live-admins`
- `platform-live-contributors`
- `platform-live-readers`

If a `Sector("security")` exists, generate the equivalent set. `Sector("security")` `Tier("live")` groups should have stricter escalation policies — `Role("admin")` access requires two-party approval.

### Step 2 — Define `Role("operator")` Identity Requirements

For each `{sector}-{tier}-operator` group, define the Workload Identity Federation trust policy:

- **Trust anchor**: Which external IdP will issue tokens? (e.g., GitHub Actions OIDC, GitLab, Kubernetes service account token)
- **Subject claim**: The specific repository, pipeline, or service account that is allowed to assume this identity. Be as narrow as possible — do not trust `repo:*`.
- **Permitted operations**: What this operator is allowed to do (full resource management within the sector/tier scope).
- **No human members**: State explicitly that this group must never have human members. If it ever does, treat it as a security incident.

Document the claim conditions that will be used in the cloud trust policy (subject, audience, issuer).

### Step 3 — Define JIT Escalation Policies

For each `Role("admin")` and `Role("contributor")` group, define the escalation policy:

- **Eligible members**: Who can request activation? (List individuals or reference the `Role("reader")` group.)
- **Activation method**: Self-approval, peer approval, or automated (for `Tier("sandbox")` `Role("contributor")`).
- **Maximum session duration**: Typically 4 hours for `Role("contributor")`, 2 hours for `Role("admin")`.
- **Justification requirement**: Always required for `Tier("live")`. Optional for `Tier("sandbox")`.
- **Approval requirement**:
  - `Tier("sandbox")` `Role("contributor")`: self-approve
  - `Tier("live")` `Role("contributor")`: self-approve with justification
  - `Tier("sandbox")` `Role("admin")`: peer approval
  - `Tier("live")` `Role("admin")`: peer approval + mandatory justification
  - `Sector("security")` `Tier("live")` `Role("admin")`: two-party approval

Map these policies to the JIT tooling in use (Azure PIM eligible assignments, AWS Identity Center permission sets, Teleport access requests).

### Step 4 — Define Initial Membership

For each human-facing group (`Role("admin")`, `Role("contributor")`, Reader), record the initial members:

- **Readers**: All platform team members receive standing `Role("reader")` access to all platform sectors and tiers.
- **Contributors**: Platform engineers actively deploying or managing the platform. Eligible for JIT `Role("contributor")` escalation.
- **Admins**: Senior platform engineers and the engineering manager. Eligible for JIT `Role("admin")` escalation.

Always list individuals by email or username — never add a group to another group. This preserves the audit trail and makes least-privilege enforceable.

### Step 5 — Define Cross-Sector Read Access

The platform sector's monitoring and observability tooling often requires read access to business sector resources (e.g., reading metrics from the `Sector("ecommerce")`). Define any cross-sector read grants:

- Which platform groups need `Role("reader")` access outside their own sector?
- In which sectors and tiers?
- Is this standing access or JIT?

Document these as explicit grants — do not assume cross-sector access is implicit.

### Step 6 — Validate Against Principles

Review the draft against the core IAM principles:

- [ ] No human is a member of any `Role("operator")` group
- [ ] No standing write access to any `Tier("live")` (`Role("contributor")` and `Role("admin")` are JIT-only in Live)
- [ ] All groups have a named owner responsible for membership review
- [ ] `Role("operator")` trust conditions are scoped to the minimum necessary CI/CD identity
- [ ] Static API keys or secrets are not referenced anywhere — Workload Identity Federation only
- [ ] Tags and labels are not used as access control mechanisms

Flag any violation and propose a remediation.

### Step 7 — Review and Iterate

Present the complete group matrix to the user. Ask:

- Are there platform team members missing from the initial membership?
- Are the JIT session durations appropriate for this team's operational cadence?
- Does the `Role("operator")` trust condition correctly reflect the CI/CD system in use?
- Are there any cross-sector access requirements not captured?

Iterate until the user is satisfied, then produce the final document.

## Output Format

Produce a YAML document named `core-iam.yaml` with this structure:

``yaml
# core-iam.yaml
# Core IAM definition for platform-owned sectors.
# Input for: manage-azure-iam, manage-aws-iam, manage-gcp-iam, manage-k8s-iam

identity_provider: entra-id  # or: okta, google-workspace, other
jit_tool: azure-pim          # or: aws-identity-center, teleport, none

sectors:
  - name: platform
    tiers:
      - name: sandbox
        groups:
          operator:
            name: platform-sandbox-operator
            type: non-human
            workload_identity:
              issuer: https://token.actions.githubusercontent.com
              subject: repo:mountainlab/platform-infra:ref:refs/heads/main
              audience: api://AzureADTokenExchange
          admins:
            name: platform-sandbox-admins
            type: human
            jit:
              eligible_from: platform-sandbox-readers
              approval: peer
              max_duration_hours: 2
              justification_required: false
            members:
              - marta@mountainlab.io
          contributors:
            name: platform-sandbox-contributors
            type: human
            jit:
              eligible_from: platform-sandbox-readers
              approval: self
              max_duration_hours: 4
              justification_required: false
            members:
              - javi@mountainlab.io
              - ana@mountainlab.io
          readers:
            name: platform-sandbox-readers
            type: human
            standing: true
            members:
              - marta@mountainlab.io
              - javi@mountainlab.io
              - ana@mountainlab.io
              - pedro@mountainlab.io
      - name: live
        groups:
          operator:
            name: platform-live-operator
            type: non-human
            workload_identity:
              issuer: https://token.actions.githubusercontent.com
              subject: repo:mountainlab/platform-infra:environment:live
              audience: api://AzureADTokenExchange
          admins:
            name: platform-live-admins
            type: human
            jit:
              eligible_from: platform-live-readers
              approval: peer
              max_duration_hours: 2
              justification_required: true
            members:
              - marta@mountainlab.io
          contributors:
            name: platform-live-contributors
            type: human
            jit:
              eligible_from: platform-live-readers
              approval: self
              max_duration_hours: 4
              justification_required: true
            members:
              - javi@mountainlab.io
              - ana@mountainlab.io
          readers:
            name: platform-live-readers
            type: human
            standing: true
            members:
              - marta@mountainlab.io
              - javi@mountainlab.io
              - ana@mountainlab.io
              - pedro@mountainlab.io

  # Add additional sectors (e.g., security) following the same structure

cross_sector_reads:
  # Groups from platform sector that need reader access in other sectors
  - group: platform-live-readers
    target_sector: ecommerce
    target_tier: live
    reason: Observability tooling reads metrics and logs from business workloads
``

Accompany the YAML with a brief human-readable summary (a Markdown section) explaining the group matrix, the escalation policy, and any assumptions made.

## Principles to Apply

- **Identity vs. Access**: This skill defines access only — group membership and role scope. It does not manage users in the IdP. That is Corporate IT's responsibility.
- **`Role("reader")` by default**: Every platform team member receives standing `Role("reader")` access. Write access is never standing in the `Tier("live")`.
- **`Role("operator")` groups are non-human**: If a human is listed in an `Role("operator")` group, it is a misconfiguration, not a feature.
- **Workload Identity over static secrets**: `Role("operator")` identities must use federated tokens. Long-lived keys are an anti-pattern.
- **Always individual membership**: Never add a group as a member of another group. List individuals.
- **Tags are not access control**: Do not reference tag-based policies for group membership or access decisions.

## Related Chapter(s)

This skill is grounded in **Chapter 5: Identity and Access Management** of *Crafting Platforms*.

- Read the book: [leanpub.com/crafting-platforms](https://leanpub.com/crafting-platforms)
- Project home: [craftingplatforms.com](https://www.craftingplatforms.com)
