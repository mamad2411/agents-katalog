---
name: iac-security
description: IaC misconfig scanning and cloud-aware review for Terraform, CloudFormation, Ansible and Pulumi. Covers tool orchestration (checkov/tfsec/kics/cfn-nag), policy-as-code (OPA/Conftest), CIS benchmark mapping, IAM over-permission detection, drift monitoring.
---

# IaC Security

## When to use

This skill reviews Infrastructure-as-Code for misconfig: over-broad IAM, public storage, missing encryption, open security groups, logging off. It leans on the cloud-provider best practices plus CIS benchmarks and orchestrates the common scanners.

Activates on:

- A request like "scan this Terraform for misconfigs", "checkov on our CloudFormation template", "is this S3 bucket policy OK", "review our Pulumi stack", "write a Conftest policy".
- New or modified IaC files: `*.tf`, `*.tfvars`, `*.hcl`, CloudFormation `*.yaml`/`*.json` templates, Ansible `playbook.yml`, `roles/`, Pulumi `Pulumi.yaml` plus `__main__.py`/`index.ts`.
- A compliance audit (ISO/SOC2/NIS2) that asks for cloud-control evidence.
- A handoff from `security-review` phase 3 where IaC sits in the diff.
- A drift suspicion: "is prod drifting from the Terraform state?".

### When NOT to use (handoff)

- Kubernetes manifests and Helm charts → `k8s-security`. Even though it's IaC, K8s is its own world with its own tools.
- Dockerfile hardening → `container-hardening`. Image content belongs there; image-registry IAM here.
- CI pipeline hardening (the workflow that runs `terraform apply`) → `cicd-hardening`. Overlap: which creds via OIDC is mentioned here.
- Secrets in IaC files → `secrets-scanner`. Scan IaC with that skill before continuing here.
- Per-CVE triage on Terraform providers or modules → `cve-triage`.
- Cloud-runtime misconfig that doesn't come from IaC (manual console change, drift) → drift detection here, but remediation routes to `ir-runbook` if it's an incident.

## Approach

Six phases. Phases 2 and 3 are the heart (scanning + cloud-aware review).

### 1. Inventory per IaC type

What do you have, in which tool, for which cloud, and what's the coverage?

- **Terraform / OpenTofu**: `*.tf` files, `terraform.lock.hcl`, state location (S3 + DynamoDB lock, GCS, Azure Blob, Terraform Cloud). Modules: in-house or public? Providers: which versions are pinned?
- **CloudFormation**: `*.yaml`/`*.json` templates, CDK output (transpiled to CFN), StackSets in multi-account setups.
- **Ansible**: `playbooks`, `roles`, `inventory`. Note: Ansible often runs against existing hosts, so IaC + runtime config are mixed.
- **Pulumi**: `Pulumi.yaml` plus language-specific code (Python/TS/Go/C#). State in Pulumi Cloud or self-hosted backend.
- **Cloud-provider matrix**: which providers are you touching? AWS, GCP, Azure, multi-cloud? Provider-specific tools (e.g. cfn-nag) only make sense with the matching provider.

Outcome: an overview of which IaC tech touches which cloud resources. Without that you're picking tools blind and missing the drift between tools and stacks.

### 2. Tool orchestration

One tool per IaC type is rarely enough; the overlap is useful because rule sets differ. Minimize to what genuinely adds value.

**Terraform**:

- **Checkov** (Prisma Cloud OSS, Apache-2). Python, broad rule set including CIS benchmarks per cloud, IaC plus container plus K8s plus secrets. Default breadth tool.
- **tfsec** (Aqua, MIT). Tight Terraform focus, fast. Fewer rules than Checkov but less noise. Since 2023 in maintenance mode; Trivy absorbs the rules.
- **Trivy** (Aqua, Apache-2). Scanner for containers, IaC, and filesystems. Useful if you already use Trivy for images.
- **KICS** (Checkmarx OSS). Broad IaC coverage (Terraform, CFN, K8s, Dockerfile, Ansible). Comparable to Checkov; pick one of the two.
- **terrascan** (Accurics, owned by Tenable). OPA-rego-based.

**CloudFormation**:

- **cfn-lint** (AWS official). Syntax and schema validation, no security rules but a required starting point.
- **cfn-nag** (Stelligent, MIT). Ruby, security-focused rules. Warns on IAM wildcards, open security groups, unencrypted storage.
- **cfn-guard** (AWS, Apache-2). Policy-as-code with its own DSL. Heavier than cfn-nag but policy-driven.
- **Checkov** also covers CFN; practical to combine with cfn-lint for syntax.

**Ansible**:

- **ansible-lint** (Ansible community, MIT). Best-practice plus security rules.
- **KICS** has Ansible rules.
- Ansible playbooks are often imperative; static analysis misses runtime state. Complement with smoke tests.

**Pulumi**:

- **Checkov** (version ≥ 2.3) supports Pulumi via state inspection.
- **Policy as Code** (Pulumi-native, free tier). Policy packs in the same language as the stack.
- Alternative: convert Pulumi state to a Terraform plan and scan that. Less direct.

Run tools in CI with a baseline file (see also `sast-orchestrator` phase 5 for noise-reduction discipline). Findings on new code are blockers; existing ones are plannable.

### 3. Cloud-aware review

The difference between IaC scanning and cloud review: tools catch the rules, humans catch the context. Walk these categories for every resource type that's in play.

- **IAM / identity.** Wildcards in `Action` (`s3:*`), wildcards in `Resource` (`arn:aws:s3:::*`), service accounts with Owner/Admin roles, cross-account trust without ExternalId, MFA not required on root or admin users. Make principle of least privilege verifiable by generating policies from CloudTrail/Audit Logs (`aws iam generate-service-last-accessed-details`).
- **Storage.** Public S3 buckets or GCS objects, default encryption off, no lifecycle policy on aging data, no versioning + MFA-delete on sensitive buckets. EBS/EFS/Azure disks unencrypted.
- **Networking.** Security groups with `0.0.0.0/0` on non-web ports (22 SSH, 3389 RDP, 3306 MySQL, 5432 Postgres), NACLs too permissive, route tables steering traffic via unintended paths, VPC peering without proper segmentation.
- **Logging and audit.** CloudTrail / Cloud Audit Logs on across all regions, logs in a separate log-archive account inaccessible to the compromise target, retention ≥ 1 year (compliance-dependent).
- **Encryption.** In-transit (TLS forced, `RequireTLS: true` on buckets, RDS forced SSL), at-rest (KMS-CMK or equivalent), key rotation on.
- **Secrets.** No hardcoded values in templates; reference Secrets Manager / Parameter Store / Key Vault. See `secrets-scanner`.
- **Public exposure.** Load balancers, API Gateways, App Runners, App Services: which are public? Is there a WAF in front? Geo-restrictions?

CIS benchmarks as the baseline: AWS Foundations Benchmark v3, GCP Foundation Benchmark v2, Azure Foundations Benchmark v2. All three exist as Checkov rule sets (`cis_aws`, `cis_gcp`, `cis_azure`).

### 4. Policy-as-code guardrails

Scanning is detect-after-the-fact. Policy-as-code enforces before apply.

- **OPA + Conftest** — Rego policies against IaC plans. `terraform plan -out=tfplan && terraform show -json tfplan | conftest test -`. Policies in git, reusable across stacks.
- **Checkov custom policies** — Python or Rego, run in the same Checkov pass.
- **Terraform Sentinel** (commercial, HashiCorp) — policy-as-code native in Terraform Cloud / Enterprise.
- **AWS Service Control Policies (SCPs)** — organization-level guardrails that IaC cannot bypass. E.g. "no region outside the EU", "no S3 ACL public-read".
- **Azure Policy / GCP Organization Policy** — equivalents on those platforms.

Write policies for org-specific rules tools don't know: "all databases in their own VPC", "no EC2 with public IP unless tagged `public-allowed`", "all S3 buckets must have object-lock on in finance accounts".

### 5. Drift detection

IaC state and actual cloud state can diverge through manual console changes, other tools, or compromised credentials. Without drift detection your model goes stale.

- **Terraform**: `terraform plan` in CI on a schedule, alert on non-zero diff.
- **CloudFormation**: Drift Detection API (`aws cloudformation detect-stack-drift`), wireable to CloudWatch alerts.
- **Pulumi**: `pulumi refresh --expect-no-changes`, fails on diff.
- **Driftctl** (OSS) — cross-provider drift detection.
- **Cloudquery** — declarative cloud-state extractor, match against IaC.

Drift is not by definition a security incident, but unintended drift must be triaged. On suspicious drift (a new IAM role not in code): escalate to `ir-runbook`.

### 6. Verification-loop

Layer 1: scope (every IaC type in the repo covered? all regions/accounts? drift check active?), assumptions ("CIS-benchmark compliant" backed by tool output, not eyeballed), gaps (secrets and k8s-manifests explicitly handed off?), consistency (policy-as-code rules not in conflict with SCPs).

Layer 2: CIS benchmark version numbers correct, cloud-provider feature names current (AWS changes feature names), no fabricated rule IDs from a scanner, CVE references (when used for a specific IaC misconfig) verified against NVD.

## Output

```
IaC Security review — <scope>
IaC types: <terraform | cfn | ansible | pulumi>
Clouds in scope: <aws | gcp | azure | multi>

Scan output (summary, no raw dumps):
  Checkov:    <N blockers, M medium, K low>
  tfsec/Trivy:<...>
  cfn-nag:    <...>

Cloud-aware findings:
  IAM:         <list of overly permissive roles/policies>
  Storage:     <public buckets, unencrypted volumes>
  Networking:  <open security groups, NACL gaps>
  Logging:     <CloudTrail/audit gaps>
  Encryption:  <in-transit + at-rest gaps>

Policy-as-code status:
  Active:      <OPA/Conftest | Sentinel | SCPs | Org Policy>
  Coverage:    <which rules active, which not>

Drift:
  Last checked: <date>
  Divergence:   <none | see appendix>

Findings (severity-sorted, blockers first, follow security-review format)

Verification-loop: ...
```

## References

- OWASP IaC Security — [https://owasp.org/www-project-iac-security/](https://owasp.org/www-project-iac-security/). OWASP IaC Top 10 and guidance.
- CIS Benchmarks — [https://www.cisecurity.org/cis-benchmarks](https://www.cisecurity.org/cis-benchmarks). AWS Foundations, GCP Foundation, Azure Foundations — the baseline.
- Checkov — [https://www.checkov.io/](https://www.checkov.io/). Tool docs plus rule-set reference.
- tfsec / Trivy IaC — [https://aquasecurity.github.io/trivy/latest/docs/coverage/iac/](https://aquasecurity.github.io/trivy/latest/docs/coverage/iac/). Trivy-integrated IaC scanning.
- cfn-nag — [https://github.com/stelligent/cfn_nag](https://github.com/stelligent/cfn_nag). CloudFormation rules.
- AWS cfn-guard — [https://docs.aws.amazon.com/cfn-guard/latest/ug/what-is-guard.html](https://docs.aws.amazon.com/cfn-guard/latest/ug/what-is-guard.html).
- ansible-lint — [https://ansible.readthedocs.io/projects/lint/](https://ansible.readthedocs.io/projects/lint/). Lint rules including security.
- Pulumi Policy as Code — [https://www.pulumi.com/docs/using-pulumi/crossguard/](https://www.pulumi.com/docs/using-pulumi/crossguard/).
- OPA / Conftest — [https://www.openpolicyagent.org/](https://www.openpolicyagent.org/) and [https://www.conftest.dev/](https://www.conftest.dev/).
- NIST SP 800-204D — [https://csrc.nist.gov/pubs/sp/800/204/d/final](https://csrc.nist.gov/pubs/sp/800/204/d/final). Strategies for secure DevSecOps.
- AWS Well-Architected Security Pillar — [https://docs.aws.amazon.com/wellarchitected/latest/security-pillar/welcome.html](https://docs.aws.amazon.com/wellarchitected/latest/security-pillar/welcome.html). Primary AWS guidance.
- Google Cloud Security Best Practices — [https://cloud.google.com/security/best-practices](https://cloud.google.com/security/best-practices).
- Azure Security Baseline — [https://learn.microsoft.com/en-us/security/benchmark/azure/](https://learn.microsoft.com/en-us/security/benchmark/azure/).

## Categories

- appsec
