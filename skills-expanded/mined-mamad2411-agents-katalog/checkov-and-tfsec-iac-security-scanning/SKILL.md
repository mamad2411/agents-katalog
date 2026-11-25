---
name: checkov-and-tfsec-iac-security-scanning
description: >
  Configures Checkov and tfsec to scan Terraform/CloudFormation/Kubernetes
  IaC source for misconfigurations — hardcoded secrets, overly permissive
  IAM policies, unencrypted storage, open security groups — before
  `terraform apply` or `aws cloudformation deploy` ever runs. Use when a
  user asks to "scan my Terraform for security issues," "add Checkov/tfsec
  to CI," "find overly permissive IAM in my IaC," "write a Checkov
  suppression," "compare Checkov and tfsec," or "catch misconfigured cloud
  resources before they're provisioned."
license: Apache-2.0
compatibility: "Claude Code, GitHub Copilot, OpenAI Codex, Cursor, Gemini CLI"
metadata:
  domain: devsecops
  maturity: stable
---

# Checkov and tfsec IaC Security Scanning

## Purpose

Infrastructure-as-code misconfigurations are a distinct risk category from
both application-level vulnerabilities (SAST/DAST) and vulnerable
dependencies (SCA): a syntactically valid, perfectly-passing-`terraform
plan` Terraform module can still define an S3 bucket with public read
access, a security group open to `0.0.0.0/0` on all ports, an IAM policy
granting `*:*`, or an unencrypted RDS instance — none of which Terraform
itself will refuse to apply, and none of which a dependency scanner or a
code-quality linter is positioned to catch. **Checkov** and **tfsec** are
purpose-built, static-analysis scanners for exactly this: they parse
Terraform (and, for Checkov, CloudFormation, Kubernetes manifests, ARM/Bicep,
Serverless Framework, and Dockerfiles) *before* any resource is provisioned,
and check it against a large ruleset of cloud-security best practices. This
is a narrower, IaC-specific scope than Snyk's multi-product platform
(`snyk iac test` covers similar ground as one of three Snyk scan types
alongside dependency and container scanning — see
[snyk-vulnerability-and-license-scanning](../snyk-vulnerability-and-license-scanning/SKILL.md))
and a different concern entirely from generic dependency scanning (see
[software-composition-analysis-sca](../software-composition-analysis-sca/SKILL.md)):
Checkov/tfsec don't care what packages your application depends on, only
whether the infrastructure you're about to create is configured safely.
Both tools are free and open-source, which makes them a common choice when
a team wants dedicated IaC scanning without adopting a commercial platform's
full per-seat licensing for that purpose alone.

## When to use

- Adding a pre-`terraform apply` (or pre-CloudFormation-deploy) security
  gate that catches misconfigurations — hardcoded secrets in `.tf` files,
  overly permissive IAM, open security groups, unencrypted storage/volumes
  — as a PR check, before any cloud resource is actually created.
- Writing or debugging a Checkov `.checkov.yaml` config or a tfsec
  `.tfsec/config.yml`, including custom checks and suppressions.
- Comparing Checkov and tfsec (or either against Snyk IaC) to decide which
  fits a team's existing toolchain, ruleset breadth, and IaC format
  (Terraform-only vs. multi-format).
- Triaging a large initial findings backlog when scanning is first added to
  an existing, previously-unscanned IaC codebase.
- Investigating why a specific resource block is flagged, and confirming
  whether the finding is a real risk or a false positive for a specific
  environment (e.g. a deliberately public static-asset bucket).
- Deciding how IaC scanning fits alongside application SAST/DAST and SCA in
  one coherent pipeline gate.

## Prerequisites & environment

- The IaC source tree itself (Terraform `.tf`/`.tfvars`, CloudFormation
  YAML/JSON templates, Kubernetes manifests, or Helm charts) — neither tool
  needs a live cloud connection or a deployed environment; both scan source
  statically.
- **Checkov** (`pip install checkov` or the container image
  `bridgecrew/checkov`) — Python-based, broadest format coverage
  (Terraform, CloudFormation, Kubernetes, Helm, ARM/Bicep, Serverless
  Framework, Dockerfile, and plain YAML/JSON for some checks).
- **tfsec** (a standalone Go binary, or via `brew install tfsec` /
  container image) — Terraform-only, narrower format scope but often
  faster on large Terraform-only repos; note that tfsec's checks have been
  progressively merged into **Trivy**'s IaC scanning (`trivy config`) by
  its maintainer (Aqua Security) — confirm which binary/command your
  pipeline actually invokes and whether you're intentionally on tfsec
  standalone or Trivy's merged IaC scanner, since both currently exist and
  behavior can differ by version.
- A defined severity threshold and a documented suppression policy (who can
  approve a suppression, with what justification and expiry) agreed before
  wiring a hard PR-blocking gate — the same prerequisite called out in
  [snyk-vulnerability-and-license-scanning](../snyk-vulnerability-and-license-scanning/SKILL.md)
  applies here: an unowned gate either blocks everything or is routed
  around entirely.
- CI runner with no cloud credentials required for the scan step itself
  (a real operational advantage over DAST-style runtime checks) — the scan
  only reads source files.

## Step-by-step guidance

1. **Run a baseline scan** to see current exposure before gating anything,
   on both tools if evaluating them side by side:
   ```bash
   checkov -d infra/terraform --compact
   tfsec infra/terraform
   ```

2. **Add Checkov to CI as a PR-blocking step**, scoping the directory and
   failing on the framework(s) actually in use:
   ```yaml
   name: iac-security-scan
   on: [pull_request]
   jobs:
     checkov:
       runs-on: ubuntu-latest
       steps:
         - uses: actions/checkout@v4
         - name: Run Checkov
           uses: bridgecrewio/checkov-action@v12
           with:
             directory: infra/terraform
             framework: terraform
             output_format: cli,sarif
             output_file_path: console,checkov-results.sarif
             soft_fail: false
         - name: Upload SARIF to code scanning
           if: always()
           uses: github/codeql-action/upload-sarif@v3
           with:
             sarif_file: checkov-results.sarif
   ```
   Uploading SARIF surfaces findings directly in GitHub's code-scanning UI
   as annotations on the PR diff, not just a pass/fail job status.

3. **Add tfsec (or Trivy's merged IaC scanner) as an equivalent, faster
   Terraform-only pass** if the repo is Terraform-only and scan speed on a
   large module tree matters:
   ```yaml
   jobs:
     tfsec:
       runs-on: ubuntu-latest
       steps:
         - uses: actions/checkout@v4
         - uses: aquasecurity/tfsec-sarif-action@v0.1.4
           with:
             working_directory: infra/terraform
             sarif_file: tfsec-results.sarif
   ```
   Running both Checkov and tfsec is reasonable during an evaluation
   period or for defense-in-depth on Terraform specifically (differing
   rule authors sometimes catch different things), but pick one as the
   actual blocking gate long-term — two blocking scanners with no
   severity-reconciliation rule produces the same "which gate do we trust"
   confusion described in
   [snyk-vulnerability-and-license-scanning](../snyk-vulnerability-and-license-scanning/SKILL.md).

4. **Suppress a specific finding with justification and an ID-scoped
   inline comment**, never a directory-wide skip, in Checkov:
   ```hcl
   resource "aws_s3_bucket" "static_assets" {
     bucket = "example-public-static-assets"
     # checkov:skip=CKV_AWS_20:Bucket intentionally public — serves static
     # website assets only, no sensitive data. Reviewed 2026-07-01, JIRA-5102.
   }
   ```
   tfsec equivalent, via an inline `#tfsec:ignore` comment:
   ```hcl
   resource "aws_security_group_rule" "public_health_check" {
     type              = "ingress"
     from_port         = 80
     to_port           = 80
     protocol          = "tcp"
     cidr_blocks       = ["0.0.0.0/0"]
     security_group_id = aws_security_group.lb.id
     #tfsec:ignore:aws-vpc-no-public-ingress-sgr -- ALB health check endpoint, intentionally public on port 80 only
   }
   ```

   > **Warning:** never suppress a hardcoded-secret finding (an API key,
   > password, or access key literal detected in `.tf`/`.tfvars`) with a
   > `checkov:skip`/`#tfsec:ignore` comment. A suppressed secret finding
   > does not make the secret safe — it only silences the scanner while the
   > credential remains exposed in source control history. Rotate the
   > credential and move it to a secrets manager or masked CI variable
   > instead; see the pitfall below for the concrete fix.

5. **Configure a persistent suppression list for findings that apply
   broadly** (e.g. a specific check that's a known false positive for your
   module conventions), rather than repeating inline comments everywhere:
   ```yaml
   # .checkov.yaml
   skip-check:
     - CKV_AWS_8   # example: instance-level detail covered instead at the AMI level
   compact: true
   framework:
     - terraform
   soft-fail-on:
     - LOW
   ```

6. **Fail the build only on real findings for the resources you actually
   control.** Both tools flag data-source blocks or third-party module
   internals sometimes; scope scans to your own module directories rather
   than vendored/third-party module caches (`.terraform/modules/**`) where
   findings aren't actionable by your team.

7. **Run the scan before `terraform plan`/`apply` in the pipeline sequence**
   — this is the entire point of static IaC scanning: catching the
   misconfiguration at PR time, before any resource exists, rather than
   discovering it via a runtime scan or an incident after the resource is
   already live. Place it as an early, fast-failing stage per the general
   staging guidance in
   [ci-cd-pipeline-design](../../../devops/skills/ci-cd-pipeline-design/SKILL.md).

8. **Re-scan on a schedule, not only on `.tf` file changes** — both tools'
   rulesets are updated over time as new best-practice checks are added;
   a module that passed six months ago may fail against a newer ruleset
   version even with no code change, similar in spirit to how a dependency
   scan can newly fail with no code change per
   [software-composition-analysis-sca](../software-composition-analysis-sca/SKILL.md).

## Best practices

- Treat a Checkov/tfsec finding the same as any other security finding for
  triage purposes — feed it into the same backlog/severity process as
  SAST/DAST/SCA findings (see
  [secure-cicd-gates](../secure-cicd-gates/SKILL.md)) rather than running
  IaC scanning as an isolated, disconnected process nobody else on the
  security team sees.
- Require every suppression to carry an explicit reason and a reviewer,
  and prefer an inline, resource-scoped suppression (`checkov:skip=`,
  `#tfsec:ignore`) over a global rule disable in config — a globally
  disabled check silently stops protecting every future resource, not just
  the one it was meant to exempt.
- Pin the scanner version in CI (`bridgecrewio/checkov-action@v12`, a
  specific tfsec/Trivy release) rather than floating on `latest` — both
  tools' rulesets evolve, and an unpinned version can newly fail a
  previously-clean pipeline with no code change, which should be treated as
  expected ruleset drift, not a broken pipeline, but only if you're aware
  it's happening.
- Scope scans to directories you actually author and control; exclude
  vendored third-party module caches from the scan target so the findings
  list stays actionable.
- Run IaC scanning as its own clearly-named CI job (`iac-security-scan`,
  not lumped into a generic `lint` job) so a failure is immediately
  traceable to a security finding, not confused with a formatting or
  syntax error from `terraform validate`.
- Reconcile Checkov and tfsec findings against a single source of truth if
  running both as blocking gates — pick one as primary (or accept that some
  findings only appear in one tool and treat both as complementary,
  non-competing signals) rather than requiring both to independently pass
  with no reconciliation rule.

## Common pitfalls

- **Symptom:** Checkov or tfsec flags a hardcoded value that looks like a
  secret (an API key, a password) directly in a `.tf`/`.tfvars` file.
  **Fix:** Do not suppress this finding — move the value out of source
  entirely into a secrets manager or CI masked variable
  (`TF_VAR_db_password` injected at apply time, `sensitive = true` on the
  corresponding variable) per the secrets guidance in
  [infrastructure-as-code-terraform](../../../devops/skills/infrastructure-as-code-terraform/SKILL.md);
  a hardcoded secret finding is a real, urgent risk, not a false positive
  to work around.

- **Symptom:** A newly-added scan surfaces hundreds of pre-existing
  findings across an established IaC codebase on day one, and the team is
  tempted to disable the check or skip scanning entirely rather than face
  the backlog.
  **Fix:** Set `soft-fail`/non-blocking mode initially to establish a
  baseline without blocking merges, triage the backlog by severity with an
  owner and SLA per finding class, and only flip the gate to hard-blocking
  once the existing backlog is under active remediation — the same phased
  rollout pattern used when any new blocking scanner is introduced to a
  previously-unscanned codebase.

- **Symptom:** A finding is flagged on a data source block or a third-party
  module's internal resource that the team doesn't directly author or
  control.
  **Fix:** Scope the scan's target directory to exclude third-party module
  caches (`.terraform/modules/**`) and vendored code; a finding you can't
  act on directly just adds noise to the actionable backlog.

- **Symptom:** tfsec and Checkov report different severities (or one flags
  something the other doesn't) for what looks like the same underlying
  misconfiguration.
  **Fix:** This is expected — the two tools maintain independently authored
  rulesets. Pick one as the primary blocking gate (or explicitly run both
  as complementary, reconciling differences manually) rather than treating
  disagreement as a bug in either tool; the same reconciliation principle
  applies across any pair of security scanners per
  [snyk-vulnerability-and-license-scanning](../snyk-vulnerability-and-license-scanning/SKILL.md).

- **Symptom:** A previously-passing pipeline starts failing a Checkov/tfsec
  scan after a routine scanner version bump, with no infrastructure change.
  **Fix:** Confirm this is a ruleset update (new checks added in the newer
  scanner version) rather than a regression — review the new failing
  check's rationale, remediate or suppress with justification as
  appropriate, and consider pinning the scanner version deliberately going
  forward if unannounced ruleset changes shouldn't surprise the pipeline.

## Worked example

**Scenario:** A team adds Checkov to CI for a Terraform module tree that
provisions an S3 bucket and a security group, catching an open ingress rule
and an unencrypted bucket before merge.

`infra/terraform/main.tf` (before fix):
```hcl
resource "aws_s3_bucket" "app_data" {
  bucket = "example-app-data"
}

resource "aws_security_group" "app" {
  name = "app-sg"

  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
}
```

Checkov CI run:
```
Check: CKV_AWS_19 "Ensure all data stored in the S3 bucket is securely encrypted at rest"
    FAILED for resource: aws_s3_bucket.app_data
    File: infra/terraform/main.tf:1-3

Check: CKV_AWS_24 "Ensure no security groups allow ingress from 0.0.0.0:0 to port 22"
    FAILED for resource: aws_security_group.app
    File: infra/terraform/main.tf:5-14
```

Fix applied:
```hcl
resource "aws_s3_bucket" "app_data" {
  bucket = "example-app-data"
}

resource "aws_s3_bucket_server_side_encryption_configuration" "app_data" {
  bucket = aws_s3_bucket.app_data.id
  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
  }
}

resource "aws_security_group" "app" {
  name = "app-sg"

  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["10.0.0.0/8"]   # restricted to internal VPN/office CIDR, not the open internet
  }
}
```

Re-running `checkov -d infra/terraform --compact` shows both checks passing,
and the PR merges with the misconfiguration caught before `terraform apply`
ever ran against a real AWS account — no bucket was ever briefly public and
no security group was ever briefly open, because the scan ran on source
before provisioning.

## Cross-references

- [snyk-vulnerability-and-license-scanning](../snyk-vulnerability-and-license-scanning/SKILL.md) — Snyk IaC covers similar misconfiguration ground as one of Snyk's three scan types under one commercial platform/license; compare against Checkov/tfsec's free, dedicated, IaC-only scope when per-seat licensing for a broader platform isn't justified by IaC scanning alone.
- [software-composition-analysis-sca](../software-composition-analysis-sca/SKILL.md) — a different finding class entirely (known-vulnerable third-party dependencies) from IaC misconfiguration; the two are complementary, not overlapping.
- [sast-integration](../sast-integration/SKILL.md) — analyzes your own application source code for vulnerability patterns, a different target than the infrastructure definitions Checkov/tfsec scan.
- [secure-cicd-gates](../secure-cicd-gates/SKILL.md) — combining IaC scanning with SAST/DAST/SCA into one coherent pipeline gate and triage workflow rather than a standalone, disconnected process.
- [infrastructure-as-code-terraform](../../../devops/skills/infrastructure-as-code-terraform/SKILL.md) — the Terraform authoring workflow (modules, state, plan review) that Checkov/tfsec scan; this skill doesn't repeat Terraform structuring guidance.
