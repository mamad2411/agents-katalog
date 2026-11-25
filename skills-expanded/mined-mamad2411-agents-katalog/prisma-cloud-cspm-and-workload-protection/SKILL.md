---
name: prisma-cloud-cspm-and-workload-protection
description: >
  Guides deep, tool-specific use of Palo Alto Networks Prisma Cloud for
  Cloud Security Posture Management (CSPM) across AWS/Azure/GCP accounts,
  IaC scanning (Terraform/CloudFormation) via Prisma's checkov-based
  engine, and agent-based workload protection (Defender agents) for
  hosts, containers, and serverless functions. Use when the user asks to
  "set up Prisma Cloud CSPM", "write a Prisma Cloud custom policy",
  "scan Terraform with Prisma/checkov", "deploy Prisma Cloud Defender
  agents", "triage a Prisma Cloud alert", "connect an AWS/Azure/GCP
  account to Prisma Cloud", or "compare CSPM posture findings against
  runtime protection". Prisma-Cloud-specific depth on RQL policies,
  IaC scan API, and Defender deployment; cross-references cloud IAM
  hardening for the underlying identity concepts CSPM findings surface.
license: Apache-2.0
compatibility: "Claude Code, GitHub Copilot, OpenAI Codex, Cursor, Gemini CLI"
metadata:
  domain: security-scanning-tooling
  maturity: stable
---

# Prisma Cloud CSPM and Workload Protection

## Purpose

Prisma Cloud (Palo Alto Networks) is a combined Cloud Native Application
Protection Platform (CNAPP) spanning three distinct capabilities that
are easy to conflate but solve different problems: **CSPM** (Cloud
Security Posture Management) continuously evaluates the *configuration*
of connected cloud accounts against policies (public S3 buckets,
overly-permissive security groups, IAM users without MFA) using
read-only API access — it never touches running workloads. **IaC
scanning** evaluates the same class of misconfiguration *before* it's
ever deployed, against Terraform/CloudFormation/ARM source, using an
engine built on the open-source Checkov project. **Workload Protection**
requires installing a Defender agent onto hosts, container runtimes, or
serverless functions to observe and enforce behavior at runtime — a
fundamentally different data source (agent telemetry) from CSPM's
API-polling model. A team that stops at CSPM alone has visibility into
*configuration* drift but zero visibility into what's actually happening
inside a running container or host; this skill covers all three
capabilities and where each one's blind spots require the others.

## When to use

- The user asks to "connect an AWS/Azure/GCP account to Prisma Cloud"
  or wants a first CSPM posture assessment.
- The user needs to write or debug a custom Prisma Cloud policy in RQL
  (Resource Query Language) for an organization-specific compliance
  requirement not covered by a built-in policy.
- The user wants Terraform/CloudFormation scanned for misconfiguration
  before merge/apply, using Prisma Cloud's IaC scanning (`checkov` CLI
  or the Prisma Cloud IaC scan API/GitHub App).
- The user wants to deploy Prisma Cloud **Defender agents** to hosts,
  a Kubernetes cluster, or serverless functions for runtime workload
  protection, and needs to understand what that adds beyond CSPM alone.
- The user is triaging a Prisma Cloud alert and needs to know whether
  it's a posture (CSPM) finding, an IaC finding, or a runtime
  (Defender) detection, since the remediation path differs for each.
- The user is comparing Prisma Cloud against a narrower point tool
  (e.g. Trivy for IaC/image scanning, native cloud-provider security
  services) for overlapping ground, and needs to know what's genuinely
  additive at enterprise/multi-cloud scale.

## Prerequisites & environment

- A Prisma Cloud tenant (Compute Edition, CSPM-only, or the combined
  CNAPP license — capabilities referenced here assume the combined
  license, since Defender/workload protection is a separate add-on from
  CSPM-only).
- Cloud account onboarding requires a **read-only** IAM role/service
  principal per connected account for CSPM (AWS cross-account IAM role
  via CloudFormation/Terraform onboarding template, Azure service
  principal with Reader role, GCP service account with `roles/viewer`
  plus specific additional read permissions Prisma documents per
  feature) — this is intentionally least-privilege and read-only; it
  cannot make changes to the cloud account by design.
- For IaC scanning: the `checkov` CLI (Prisma Cloud's IaC scan engine is
  built on it) or the Prisma Cloud IaC scan API/CI plugin, plus a
  Prisma Cloud access key (API key ID + secret) for API-based scans —
  store as CI secrets, never inline. See
  [secrets-management](../../../devsecops/skills/secrets-management/SKILL.md).
- For Workload Protection: outbound network connectivity from each
  host/cluster to the Prisma Cloud Compute console (self-hosted
  Compute console or the SaaS one), and sufficient privilege to deploy
  a DaemonSet (Kubernetes), a host agent package, or a Lambda
  layer/extension (serverless) — Defender agents typically need
  elevated (often privileged, for container-runtime visibility) access
  on the host, which is a materially different trust boundary than
  CSPM's read-only cloud API access and should be reviewed accordingly.
- A defined alert-triage workflow and severity taxonomy before
  onboarding accounts at scale — a first CSPM scan against an
  established, non-trivial cloud estate routinely surfaces hundreds to
  thousands of findings, and an unprioritized dump becomes noise
  nobody acts on.

## Step-by-step guidance

1. **Onboard cloud accounts read-only first**, using Prisma's
   provided onboarding template rather than a hand-rolled role, so the
   granted permissions match exactly what Prisma's policy set expects
   to evaluate (over- or under-scoping a hand-written role produces
   either unnecessary exposure or silent gaps in what CSPM can see):
   ```bash
   # AWS onboarding (illustrative — use Prisma's current CFT/Terraform module)
   aws cloudformation create-stack \
     --stack-name prisma-cloud-cspm-readonly \
     --template-url https://<prisma-provided-template-url> \
     --capabilities CAPABILITY_NAMED_IAM \
     --parameters ParameterKey=ExternalId,ParameterValue=<PRISMA_EXTERNAL_ID>
   ```

2. **Let the built-in policy set run first** before writing custom
   policies — Prisma ships hundreds of policies mapped to CIS
   Benchmarks, PCI-DSS, SOC 2, and cloud-provider-specific best
   practices; triage what's already covered before duplicating it.

3. **Write custom RQL policies** for organization-specific rules the
   built-in set doesn't cover:
   ```
   config from cloud.resource where
     cloud.type = 'aws'
     AND api.name = 'aws-s3api-get-bucket-acl'
     AND json.rule = 'publicAccessBlockConfiguration does not exist or
       (publicAccessBlockConfiguration.blockPublicAcls is false or
        publicAccessBlockConfiguration.blockPublicPolicy is false)'
   ```
   Attach the policy to an alert rule scoped to specific accounts/tags
   and a severity, and route it to the team's actual notification
   channel (webhook, ticketing integration) rather than leaving it in
   the console-only alert feed where it won't be seen promptly.

4. **Add IaC scanning to the pipeline**, so misconfiguration is caught
   before `terraform apply`, not only after the fact by CSPM polling a
   deployed resource:
   ```yaml
   # GitHub Actions, using checkov (Prisma Cloud's IaC scan engine)
   name: iac-scan
   on: [pull_request]
   jobs:
     checkov:
       runs-on: ubuntu-latest
       steps:
         - uses: actions/checkout@v4
         - name: Prisma Cloud IaC scan
           uses: bridgecrewio/checkov-action@v12
           with:
             directory: infra/terraform
             framework: terraform
             api-key: ${{ secrets.PRISMA_CLOUD_API_KEY }}
             soft_fail: false
   ```
   Sample finding:
   ```
   Check: CKV_AWS_20 "S3 Bucket has an ACL defined which allows public READ access"
   FAILED for resource: aws_s3_bucket.data
   File: /infra/terraform/s3.tf:5-14
   ```

5. **Reconcile IaC findings with CSPM findings on the same resource**
   — the goal is that a CSPM alert on a live resource has a matching
   IaC guardrail preventing recurrence; if CSPM keeps re-flagging the
   same class of misconfiguration after a fix, the IaC scan isn't
   gating the pipeline that actually provisions that resource type
   (see Common pitfalls).

6. **Deploy Defender agents deliberately, scoped by environment risk**
   — start with production/internet-facing workloads, not a blanket
   fleet-wide rollout on day one, given the elevated host/runtime
   access Defender requires:
   ```bash
   # Kubernetes Defender DaemonSet (illustrative install pattern)
   twistcli defender export kubernetes \
     --address https://<prisma-compute-console> \
     --cluster-address <cluster-endpoint> \
     > defender.yaml
   kubectl apply -f defender.yaml
   ```

7. **Use Defender for runtime + image scanning together**, not CSPM
   alone, to close the gap between "the Terraform/config looks fine"
   and "nothing malicious is actually running": Defender scans images
   at deploy time and observes running container/host behavior
   (unexpected process execution, network connections, file-system
   writes) against a behavioral model, distinct from CSPM's
   config-only view.

8. **Triage by resource criticality and exposure, not raw alert
   count** — tag cloud resources (environment, data classification,
   internet-facing) so Prisma's alert rules and dashboards can prioritize
   a public-facing production resource's misconfiguration over an
   identical finding on an isolated internal dev resource.

## Best practices

- Treat CSPM, IaC scanning, and Workload Protection as three different
  data sources answering three different questions (declared config
  before deploy, actual config after deploy, actual runtime behavior)
  — a mature program runs all three, not just the CSPM dashboard that
  happens to be easiest to turn on first.
- Onboard cloud accounts read-only via the vendor-provided template,
  not a hand-written role — see
  [cloud-iam-hardening](../../../cloud/skills/cloud-iam-hardening/SKILL.md)
  for the underlying least-privilege principle this onboarding role
  should itself follow.
- Gate the pipeline on IaC scanning for new/changed infrastructure and
  use CSPM primarily for drift detection (manual console changes,
  misconfiguration introduced outside the IaC pipeline) — relying on
  CSPM alone to catch everything means every fix is reactive, applied
  only after a resource is already live and possibly already exposed.
- Scope Defender agent rollout by risk (internet-facing and production
  first) and review the elevated host/runtime privilege it requires as
  its own access-control decision, not an automatic extension of CSPM's
  read-only trust.
- Map custom RQL policies and Defender runtime rules to a compliance
  framework (CIS, PCI-DSS, SOC 2) explicitly where relevant, so audit
  evidence is a byproduct of normal alerting rather than a separate
  manual exercise.
- Don't treat a clean CSPM dashboard as "no runtime risk" — CSPM cannot
  see a compromised process inside a correctly-configured container;
  pair it with
  [sysdig-secure-runtime-security](../sysdig-secure-runtime-security/SKILL.md)
  or Prisma's own Defender runtime detection for that layer.

## Common pitfalls

- **Symptom:** The same misconfiguration (e.g. a public S3 bucket) keeps
  getting flagged by CSPM, fixed manually in the console, and
  re-flagged weeks later on a newly-provisioned resource of the same
  type.
  **Fix:** The fix is being applied to the live resource but not to the
  Terraform/CloudFormation module that provisions new instances of it —
  add the equivalent IaC scan check (step 4-5) to the pipeline that
  actually creates these resources so the class of misconfiguration
  can't recur, not just the one instance CSPM happened to catch.

- **Symptom:** A first-time CSPM scan against an established AWS
  organization returns several thousand findings, and the team gives up
  triaging within the first week.
  **Fix:** Filter and prioritize by resource criticality/exposure tags
  and severity before attempting to work the full list — start with
  Critical/High severity on internet-facing or production-tagged
  resources only, and schedule the rest as a longer-term paydown rather
  than an all-at-once effort.

- **Symptom:** Defender agent deployment to a Kubernetes cluster is
  blocked or delayed pending a lengthy security review, because it
  requests privileged/host-level access that the platform team wasn't
  expecting from what they assumed was "just another monitoring agent."
  **Fix:** Review and document the Defender agent's actual required
  privileges up front as part of onboarding (it needs container-runtime
  and host-level visibility to do behavioral detection, which is a
  materially different trust boundary than CSPM's read-only cloud API
  role) rather than bundling it into a CSPM rollout conversation where
  the privilege difference goes unnoticed until deployment time.

- **Symptom:** A custom RQL policy compiles and saves but never fires
  even against a resource that should clearly match.
  **Fix:** RQL's `json.rule` clause matches against the *exact* API
  response shape Prisma's connector captured for that resource type —
  test the rule against the "Investigate" tab's live resource JSON
  first to confirm field names/nesting, rather than guessing from cloud
  provider API documentation, which can differ from what Prisma's
  connector actually normalizes.

- **Symptom:** IaC scanning in CI passes cleanly, but the same resource
  is later flagged as misconfigured by CSPM once deployed.
  **Fix:** Something changed the resource outside the IaC pipeline
  (manual console edit, a separate script, another team's Terraform
  state) after apply — this is exactly the drift detection CSPM exists
  to catch; investigate the change history/CloudTrail for that
  resource rather than assuming the IaC scan missed something.

## Worked example

A platform team onboards their AWS organization to Prisma Cloud CSPM,
adds an IaC scanning gate for Terraform, and rolls out Defender to their
production EKS cluster.

1. Onboard the AWS org with the Prisma-provided read-only
   cross-account role (step 1), scoped to all member accounts via AWS
   Organizations integration.

2. Initial CSPM scan surfaces 2,400 findings; the team filters to
   `severity IN (critical, high) AND resource.tags.environment =
   'production'`, reducing the actionable list to 62 findings for the
   first remediation sprint.

3. Add the `checkov-action` IaC gate (step 4) to the Terraform repo
   that provisions the flagged resource types, blocking new
   misconfigurations of the same class going forward.

4. A recurring finding — `CKV_AWS_20` (public-read S3 ACL) — is traced
   to a shared Terraform module (`modules/data-bucket`) used by six
   services; fixing the module once resolves the CSPM finding across
   all six, rather than patching each bucket individually in the
   console.

5. Deploy the Defender DaemonSet to the production EKS cluster (step
   6), scoped first to production before extending to staging/dev.

6. Within two weeks, a Defender runtime alert fires: a pod matching a
   payments service unexpectedly spawns a shell process and initiates
   an outbound connection to an IP not in any documented dependency —
   a detection CSPM's config-only view could never have produced, since
   the pod's declared configuration (image, resource limits,
   `securityContext`) was fully compliant.

## Cross-references

- [cloud-iam-hardening](../../../cloud/skills/cloud-iam-hardening/SKILL.md) —
  the least-privilege principle behind Prisma's read-only CSPM
  onboarding role, and the broader IAM hardening practice CSPM findings
  frequently point back to.
- [trivy-vulnerability-scanning](../trivy-vulnerability-scanning/SKILL.md) —
  a lighter-weight, self-hosted alternative/complement for IaC and
  image scanning at a smaller scale than Prisma's full CNAPP.
- [sysdig-secure-runtime-security](../sysdig-secure-runtime-security/SKILL.md) —
  a comparable runtime-protection approach (Falco-rule-based) worth
  understanding alongside Prisma's Defender agent model.
- [container-image-hardening](../../../devsecops/skills/container-image-hardening/SKILL.md) —
  reducing what both Defender's image scanning and CSPM have to find in
  workload images in the first place.
