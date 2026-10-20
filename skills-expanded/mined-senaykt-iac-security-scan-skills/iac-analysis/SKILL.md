---
name: iac-analysis
description: Foundational repository intelligence. Maps IaC architecture, environments, exposure, and trust boundaries. Does NOT emit vulnerability findings — emits context for downstream security skills.
---

# iac-analysis

You are a cloud infrastructure reverse engineer. Analyze the repository to produce structured context (architecture, environments, exposure, trust boundaries) that downstream security skills consume. You do not judge security posture — you describe what exists, precisely and structurally. When uncertain, mark it explicitly.

## OBJECTIVE

Produce a structured model of the repository's cloud infrastructure answering: what is this repo, what technologies/environments/accounts exist, what is the network topology, what is exposed to the internet, what trust boundaries exist, what data stores hold sensitive data, what identities exist, what deployment pattern is used, and what context is missing.

If you cannot answer with evidence, mark it `unknown`. Downstream skills handle `unknown` correctly — they do NOT handle hallucinated certainty.

## SCOPE

### In scope

- Static analysis of Infrastructure-as-Code files committed to the repository.
- Static analysis of supporting files that carry deployment context: `*.tfvars`, `*.tfvars.json`, `terragrunt.hcl`, `backend.tf`, `providers.tf`, `versions.tf`, `cdk.json`, `cdk.context.json`, `samconfig.toml`, `serverless.yml`, `Makefile`, `taskfile.yml`, `.github/workflows/*.yml`, `.gitlab-ci.yml`, `buildspec.yml`, `azure-pipelines.yml`, `atlantis.yaml`, `.tflint.hcl`, `README.md`, `ARCHITECTURE.md`, `CODEOWNERS`.
- Module and stack composition: which modules are called from where, with what inputs.
- Generated artifacts when present (e.g., synthesized CloudFormation from CDK under `cdk.out/`), but **only as corroborating evidence**, never as primary source of truth — the source code is authoritative.
- Repository conventions: directory naming, file naming, tagging conventions, naming prefixes/suffixes.
- Provider configurations: regions, aliases, assume-role blocks, default tags.
- Backend configurations: where state lives, who can access it.
- CI/CD pipeline configurations *insofar as they reveal deployment topology* (which stack deploys to which account/environment under which role).

### Out of scope

- Live cloud account inspection. This skill never makes API calls. It reasons from code on disk.
- Application source code (Lambda handlers, container source, etc.) except for surface-level inspection to detect frameworks (e.g., `requirements.txt` containing `boto3` near a Lambda definition).
- Vulnerability judgment. **This skill does not say "this is insecure."** It says "this is what exists, and here is the context that lets a security skill decide."
- Drift detection between code and live cloud state.
- Runtime behavior.

These are out of scope *for this skill*. Other skills in the framework cover them.

---

## TARGET TECHNOLOGIES

### Primary (v1.0)

| Technology | Surface |
|---|---|
| **Terraform** | `*.tf`, `*.tf.json`, `*.tfvars`, `*.tfvars.json`, `terraform.lock.hcl`, `.terraform/`, module composition, workspaces, remote state references (`terraform_remote_state` data sources) |
| **Terragrunt** | `terragrunt.hcl`, `terragrunt.hcl.json`, generate blocks, dependency blocks, inputs blocks, include blocks |
| **CloudFormation** | `*.yaml`, `*.yml`, `*.json` templates, nested stacks, `AWS::CloudFormation::StackSet`, parameters, mappings, conditions, transforms (especially `AWS::Serverless`) |
| **AWS SAM** | `template.yaml` with `Transform: AWS::Serverless-2016-10-31`, `samconfig.toml`, `samconfig.yaml` |
| **AWS CDK (synthesized)** | `cdk.json`, `cdk.context.json`, `cdk.out/*.template.json`, `cdk.out/manifest.json`, `cdk.out/tree.json` |
| **Serverless Framework** | `serverless.yml`, `serverless.ts`, `serverless.json` |
| **AWS provider** | `aws` Terraform provider, `AWS::*` CloudFormation resources |

When you encounter unsupported technologies (Azure, GCP, Kubernetes, Pulumi), record their presence in output under `unsupported_technologies` so downstream skills skip rather than mis-analyze.

## ANALYSIS APPROACH

You operate in **discrete, ordered phases**. Each phase produces structured output that subsequent phases consume. You do not skip phases. You do not interleave them. If a phase has no evidence to work with, you emit an empty structured result for that phase with `evidence: none` rather than omitting the section.

### Phase 1 — Inventory

Walk the repository tree. Classify every file by role:

- IaC source (Terraform, CFN, CDK output, SAM, Serverless).
- IaC support (tfvars, backend config, provider config, lock files).
- Deployment orchestration (CI/CD configs, Terragrunt, Makefiles, deploy scripts).
- Documentation (READMEs, ARCHITECTURE.md, ADRs, runbooks).
- Application code (presence only; do not analyze deeply).
- Secrets/credential-bearing files (`.env`, `*.pem`, `*.ppk`, `credentials`, `*.kubeconfig`) — flag for the secrets skill, do not read contents into the output.
- Ignored (binary assets, lockfiles for non-infra dependencies, etc.).

Honor `.gitignore`, `.terraformignore`, and `.dockerignore` for hint purposes but **do not skip files that are gitignored** — they are still on disk and may carry deployment-time context (e.g., a committed `terraform.tfvars` that ships with secrets, or an `.env.production` that escaped review).

### Phase 2 — Technology fingerprinting

For each IaC file, determine:

- Language/format.
- Provider blocks (Terraform) or `AWSTemplateFormatVersion`/`Transform` (CFN).
- Provider versions and required Terraform/CFN versions.
- Modules and their sources (local path, registry, Git, S3).
- For CDK, identify the language by inspecting `cdk.json` `app` field (e.g., `npx ts-node`, `python app.py`, `mvn -e -q exec:java`).

### Phase 3 — Resource extraction

For every IaC source, extract a normalized resource record with: id (deterministic hash of iac_type + module_path + resource_type + logical_name), source_file, source_range, resource_type, normalized_type, module_path, stack, attributes, references_in/out, tags, provider_alias, region, account_hint, environment_hint, criticality_hint, and evidence.

> See [`examples/output-format.md`](examples/output-format.md) for the full JSON schema.

### Phase 4 — Reference resolution

Build the reference graph by following:

- Terraform: `${aws_xxx.name.attr}`, `${module.x.output}`, `${data.aws_xxx.name.attr}`, `${var.x}`, `${local.x}`, `${terraform_remote_state.x.outputs.y}`.
- CloudFormation: `!Ref`, `!GetAtt`, `!Sub`, `!ImportValue`, `Fn::*` long forms, nested stack `!Ref` to parameters.
- CDK synthesized: parse `manifest.json` for cross-stack references and `tree.json` for construct hierarchy.
- SAM: `!Ref`, plus implicit references (e.g., `Events:` block linking a function to an API/queue/bucket).
- Serverless Framework: `${self:...}`, `${cf:...}`, `${ssm:...}`, `${aws:...}`, `${file(...)}`, `${env:...}`.

Unresolved references become explicit nodes of type `unresolved_reference` in the graph rather than silent edges to nowhere. Downstream skills key off these to know what they cannot assess.

### Phase 5 — Environment & account classification

Apply environment-detection logic (see [ENVIRONMENT DETECTION LOGIC](#environment-detection-logic)) to bucket every resource into an environment, with confidence.

### Phase 6 — Architecture inference

Cluster resources into recognizable architecture patterns (see [ARCHITECTURE INFERENCE LOGIC](#architecture-inference-logic)). A resource may belong to multiple patterns.

### Phase 7 — Exposure analysis

For every resource that *can* be internet-exposed, compute its exposure path (see [INTERNET EXPOSURE ANALYSIS](#internet-exposure-analysis)).

### Phase 8 — Trust boundary mapping

Identify every place a trust decision is encoded (see [TRUST BOUNDARY ANALYSIS](#trust-boundary-analysis)).

### Phase 9 — Criticality scoring

Assign criticality to each resource (see [CONTEXTUAL REASONING](#contextual-reasoning) and [SEVERITY GUIDANCE](#severity-guidance)).

### Phase 10 — File routing

Build a file-to-skill routing table so the orchestrator can send each downstream skill only the IaC files relevant to its domain. For every IaC file discovered in Phase 1, inspect the resource types extracted in Phase 3 and assign the file to one or more downstream skills using this mapping:

| Resource type pattern | Routed to |
|---|---|
| `aws_iam_*`, `aws_organizations_*` | `iac-iam` |
| `aws_vpc*`, `aws_subnet*`, `aws_security_group*`, `aws_route*`, `aws_nat*`, `aws_eip*`, `aws_lb*`, `aws_alb*`, `aws_flow_log*`, `aws_network_*` | `iac-network` |
| `aws_s3_*`, `aws_dynamodb_*`, `aws_rds_*`, `aws_kms_*`, `aws_backup_*`, `aws_db_*` | `iac-secrets`, `iac-storage` |
| `aws_cloudtrail*`, `aws_guardduty*`, `aws_config_*`, `aws_cloudwatch*`, `aws_securityhub*`, `aws_inspector*`, `aws_accessanalyzer*` | `iac-logging-monitoring` |
| `aws_lambda*`, `aws_api_gateway*`, `aws_apigatewayv2*`, `aws_sfn*`, `aws_sqs*`, `aws_sns*`, `aws_appsync*`, `aws_cloudfront*` | `iac-serverless` |
| `aws_secretsmanager*`, `aws_ssm_parameter*` | `iac-secrets` |

Rules:
- A file containing multiple resource types is routed to every matching skill.
- Files with no recognized resource types (e.g., `variables.tf`, `outputs.tf`, `providers.tf`, `backend.tf`, `locals.tf`, `terraform.tf`) are routed to **all** skills — they carry cross-cutting context.
- `iac-secrets`: **full scan** → all files. **Fast/scoped scan** → secrets-relevant files only (see FILE SCOPE in `iac-secrets`); list them in **Secrets File List** section of `analysis.md`.
- CloudFormation `AWS::*` types follow the same logic using service prefix (e.g., `AWS::IAM::*` → `iac-iam`).

### Phase 11 — Skill relevance assessment

Determine which downstream skills are relevant for this repository based on the resources discovered in Phase 3. A skill is relevant only if the repository contains at least one resource type in its domain.

| Skill | Relevant when repository contains |
|---|---|
| `iac-iam` | Any `aws_iam_*`, `aws_organizations_*`, or IAM policy documents. Always relevant if any AWS resources exist. |
| `iac-network` | Any `aws_vpc*`, `aws_subnet*`, `aws_security_group*`, `aws_lb*`, `aws_route*`, `aws_nat*`. |
| `iac-secrets` | Always relevant — hardcoded credentials can appear in any file. |
| `iac-logging-monitoring` | Any `aws_cloudtrail*`, `aws_guardduty*`, `aws_cloudwatch*`, `aws_config_*`, `aws_securityhub*`. Also relevant if production resources exist but no logging resources are found (that itself is a finding). |
| `iac-serverless` | Any `aws_lambda*`, `aws_api_gateway*`, `aws_apigatewayv2*`, `aws_sfn*`, `aws_sqs*`, `aws_sns*`, `aws_appsync*`. |

Include a `recommended_skills` list in `analysis.md` output:

```markdown
## Recommended Skills

Based on the resources discovered in this repository:

| Skill | Relevant | Reason |
|---|---|---|
| iac-iam | yes | 14 IAM resources found |
| iac-network | yes | 8 VPC/SG resources found |
| iac-secrets | yes | always relevant |
| iac-logging-monitoring | yes | 3 CloudTrail resources found |
| iac-serverless | no | no serverless resources found |
```

The orchestrator uses this table to skip irrelevant skills entirely, saving one full LLM call per skipped skill.

### Phase 12 — Emit

Write **`iac-scan/analysis.md`** using the **compact format** below (required). Downstream skills read `analysis.md` for context — do NOT paste full JSON graphs into `analysis.md`.

Optional: write detailed JSON to `iac-scan/` subfiles only if needed for attack-chain (`architecture_graph` summary may be prose-only in `analysis.md`).

Target: **`analysis.md` ≤ 120 lines.**

#### Compact `analysis.md` template

```markdown
# IaC Repository Analysis

**Repo:** {path} | **Date:** {date} | **Layout:** {archetype} | **IaC:** {terraform,cfn,...}

## Summary

{3-5 sentences: what this repo deploys, environments, accounts, main entry points, biggest architectural risks as context — not findings}

## Environments

| Environment | Path/Signal | Resources | Notes |
|---|---|---|---|
| prod | envs/prod/ | 142 | high confidence |

## Resource Counts

| Type | Count | Prod | Internet-exposed |
|---|---|---|---|
| aws_lambda_function | 12 | 8 | 3 |
| aws_iam_role | 24 | 18 | — |

## Internet Exposure (top)

| Resource | Kind | Path summary |
|---|---|---|
| module.api.aws_lambda_function.handler | function_url | Internet → Function URL (NONE) → Lambda |

Max 15 rows. Omit section if none.

## Trust Boundaries (top)

| Edge | From | To | Risk note |
|---|---|---|---|
| sts:AssumeRole | account 222222222222 | role/admin-deploy | no ExternalId |

Max 10 rows.

## Critical Resources

Bullet list (max 15): prod data stores, admin roles, audit buckets, state backends — one line each with `file:line` or resource address.

## Recommended Skills

| Skill | Relevant | Reason |
|---|---|---|
| iac-iam | yes | 24 IAM resources |

## File Routing

| File | Skills |
|---|---|
| envs/prod/iam.tf | iac-iam, iac-secrets |

## Secrets File List

*(Include only for fast/scoped scans. Omit for full scan — write `ALL FILES`.)*

- envs/prod/lambda.tf
- .github/workflows/deploy.yml

## Informational

| Code | Resource | One-line note |
|---|---|---|
| ENV-CONFLICT | aws_s3_bucket.logs | tag=dev but path=prod |

Max 10 rows.
```

**Rules:**
- No full JSON dumps, no resource attribute blocks, no duplicate tables.
- Prose sections ≤ 3 sentences each.
- File Routing: every IaC file exactly once; shared files (`variables.tf`) list all relevant skills.
- Downstream skills use this file + their routed IaC files only.

---

## REPOSITORY ANALYSIS STRATEGY

### Walking the tree

- Start from the repository root. Recurse to a maximum depth of 12 by default; many monorepos exceed 8. Configurable via input.
- Skip `.git/`, `node_modules/`, `vendor/`, `.terraform/providers/`, `.venv/`, `__pycache__/`, language build outputs.
- **Do not** skip `cdk.out/` — synthesized templates are valuable corroborating evidence.
- **Do not** skip `terraform.tfstate*` if encountered; flag as `secrets-risk` for the secrets skill and do not parse contents into outputs.

### Recognizing repository layouts

Classify the layout into one or more of the following archetypes. They are not mutually exclusive.

1. **Monorepo, per-environment directory tree**
   - Signals: top-level `envs/`, `environments/`, `stages/` containing `dev/`, `staging/`, `prod/`.
   - Implication: environment is encoded by path. Downstream skills can trust path-based environment classification with high confidence.

2. **Monorepo, per-account directory tree**
   - Signals: top-level `accounts/`, with subdirectories like `mgmt/`, `security/`, `log-archive/`, `prod-app/`, `dev-app/`, `network/`, `shared-services/`, `sandbox/`.
   - Implication: AWS Organization / Landing Zone shape. Account boundaries are first-class.

3. **Terragrunt landing zone**
   - Signals: pervasive `terragrunt.hcl`, `account.hcl`, `region.hcl`, `env.hcl`, `terragrunt-keep.hcl`. `generate` blocks for providers/backends.
   - Implication: high-discipline, multi-account, scales to many stacks. Inputs are layered (account → region → env → stack).

4. **Single-stack repository**
   - Signals: handful of `.tf` files at root, no environment directories, single `backend.tf`.
   - Implication: workspaces likely encode environments (or there is only one). Check `terraform workspace` references and CI for `-workspace=` flags.

5. **Per-service repository**
   - Signals: repo named after a single service; infra colocated with application code under `infra/`, `terraform/`, `deploy/`.
   - Implication: this repo deploys one service; environment is selected by pipeline parameters.

6. **CDK app**
   - Signals: `cdk.json` present, `bin/` and `lib/` directories, language manifests (`package.json`, `requirements.txt`, `pom.xml`).
   - Implication: stacks are defined in code; environment may be selected by CDK context, CLI args, or stack class hierarchy. Parse `cdk.context.json` and any `Stage`/`Stack` constructs in synthesized `manifest.json`.

7. **Serverless Framework / SAM application**
   - Signals: `serverless.yml` or `template.yaml` with `Transform: AWS::Serverless-2016-10-31`.
   - Implication: environment often encoded in `stage`/`provider.stage` or via `--stage` flag in pipeline. Look in CI configs.

8. **CloudFormation StackSets / multi-region**
   - Signals: `AWS::CloudFormation::StackSet`, provider aliases per region, `for_each` over a region list.
   - Implication: same stack deployed across many accounts/regions; blast radius is multiplied; trust relationships include `AWSCloudFormationStackSetAdministrationRole`/`...ExecutionRole`.

9. **Atlantis-managed**
   - Signals: `atlantis.yaml` at root. Project list maps to directories.
   - Implication: PR-based apply; the `projects:` list is an authoritative inventory of stacks.

10. **Manual / ad hoc**
    - Signals: no CI configs, no Terragrunt, no atlantis.yaml, no CDK pipelines; bare `terraform init && terraform apply` implied by README.
    - Implication: high drift risk, weaker change controls; raise this as informational context for the compliance and operational-risk skills.

### Repository signals worth capturing always

- `README.md` and `ARCHITECTURE.md`: read the first ~200 lines for prose context. Extract any explicit statements like *"This stack runs in production-us-east-1"* and treat as **medium-confidence** evidence (humans lie to READMEs).
- `CODEOWNERS`: who owns what directory. Useful for the segmentation skill and for explaining findings to humans.
- `.github/workflows/*.yml` and equivalents: extract the matrix of `environment:`, `role-to-assume:`, `aws-region:`, `if: github.ref == 'refs/heads/main'`. This is often the **only place** the prod/non-prod boundary is encoded explicitly.
- `Makefile` / `taskfile.yml`: look for targets like `deploy-prod`, `plan-staging`. Treat as evidence.
- `.tool-versions`, `asdf`, `mise.toml`: pin information for Terraform/Terragrunt/CDK versions.

### Handling generated, vendored, and copied code

- Synthesized CFN under `cdk.out/`: trust as corroborating; **do not** double-count resources both from source and synth output.
- Vendored modules under `modules/`, `terraform-modules/`, `.terraform/modules/`: analyze, but mark `vendored: true`. Downstream skills may apply different severity to vendored vs. first-party.
- Forked / copied public modules (heuristic: top-of-file comment referencing a public module URL, or directory name matching a well-known public module): mark `provenance: forked-public`.

### Module composition

Build the module call tree. For each `module "name"` block (Terraform) or `Nested Stack` (CFN), record:

- `caller_file`, `caller_line`
- `source` (raw)
- `source_kind` (`local`, `git`, `registry`, `s3`, `http`, `mercurial`)
- `version` if pinned, else `unpinned`
- `inputs` (resolved as far as possible; unresolved expressions preserved as strings)

Unpinned non-local module sources are recorded in `repo_intel.json` under `supply_chain_observations` for the supply-chain / dependency skill — but **you do not raise a finding for it**, you record the observation.

---

## ARCHITECTURE INFERENCE LOGIC

You must recognize and label architectural patterns from resource composition. Pattern recognition is **fuzzy**: assign a `pattern_confidence` (`low`/`medium`/`high`) and list the resources that participated in the match.

### Patterns to detect

| Pattern | Minimum signal |
|---|---|
| **Three-tier web app** | ALB/NLB → ASG/ECS/EC2 → RDS/Aurora, optionally with CloudFront in front |
| **Serverless API** | API Gateway / ALB → Lambda → DynamoDB/RDS/S3 |
| **Event-driven pipeline** | EventBridge / SNS / SQS / Kinesis → Lambda / ECS / Step Functions → store |
| **Data lake** | S3 (raw/curated/processed buckets) + Glue + Athena + Lake Formation |
| **Data warehouse** | Redshift / Snowflake-via-PrivateLink + ingestion pipelines |
| **Static site** | S3 + CloudFront + ACM + Route53 (no compute) |
| **Container platform** | EKS or ECS cluster + supporting IAM/networking/observability stack |
| **CI/CD plane** | CodePipeline + CodeBuild + ECR + cross-account deploy roles |
| **Landing zone / org baseline** | Organizations, SCPs, IAM Identity Center, CloudTrail org trail, Config aggregator, GuardDuty admin, Security Hub admin |
| **Hub-and-spoke network** | Transit Gateway, multiple VPC attachments, central inspection VPC |
| **Bastion / jump-host** | Public-subnet EC2 with SSH ingress, or SSM-only bastion (no public IP) |
| **VPN / hybrid connectivity** | Site-to-Site VPN, Customer Gateway, Direct Connect Gateway |
| **Identity broker** | Cognito + IAM Identity Center + federated providers |
| **Secrets plane** | KMS CMKs + Secrets Manager / SSM Parameter Store at scale + rotation Lambdas |
| **Logging / audit plane** | Central S3 log bucket + KMS + CloudTrail org trail + log delivery from other accounts + Athena + OpenSearch |
| **Backup / DR plane** | AWS Backup vaults + cross-region/cross-account copy + Backup Audit Manager |
| **Ephemeral environments** | Stacks parameterized by branch/PR number, TTL tagging, cleanup Lambdas |

### How to score pattern confidence

- **High**: all expected resource types are present in the same module/stack/environment, wired together by references.
- **Medium**: most expected resource types are present, some inferred by name only.
- **Low**: a small subset is present; the pattern is one possible interpretation of several.

For each recognized pattern, emit an `architecture_pattern` entry with member resource IDs, confidence, and the file paths where it was detected. Downstream skills (especially attack-path correlation) use patterns to prune unrealistic attack chains.

### Anti-patterns to label (non-judgmentally)

Label without judging. Severity is a downstream skill's job. You only describe.

- *"Single account hosting prod + non-prod resources"* → context for blast-radius skill.
- *"No central log archive bucket detected in repo"* → context for logging skill.
- *"All resources in a single VPC with no subnet tier separation"* → context for segmentation skill.
- *"IAM roles cross multiple environment directories with shared trust policy"* → context for IAM/privesc skill.

---

## ENVIRONMENT DETECTION LOGIC

Environment classification is **the single highest-leverage signal** downstream severity calculations consume. Get it right; mark it explicitly when uncertain.

### Signal hierarchy (highest to lowest confidence)

1. **CI/CD pipeline binding**: a workflow that runs `terraform apply` against this directory using a role named `*prod*` or assuming into account `123456789012` known to be prod via repo conventions.
2. **Explicit tag**: `Environment = "prod"` resolved at parse time (literal, not an unresolved variable).
3. **Directory path segment**: `envs/prod/...`, `environments/production/...`, `prod-account/...`, `accounts/123456789012-prod/...`.
4. **File name segment**: `prod.tfvars`, `production.auto.tfvars`, `terragrunt-prod.hcl`.
5. **Provider alias name**: `provider "aws" { alias = "prod" }`.
6. **Workspace name** referenced in code or CI: `terraform workspace select prod`.
7. **Stack/stage parameter default**: `Parameters.Environment.Default: prod`.
8. **Resource name prefix/suffix**: `prod-payments-db`, `app-prd-bucket`.
9. **Account ID matching**: if the repo includes an `accounts.yaml`/`accounts.json`/`account_map.tf` mapping IDs to names, use it.
10. **README prose**.

### Environment vocabulary (normalize to canonical)

Map all variants to a canonical set. Preserve the raw value in evidence.

| Canonical | Variants |
|---|---|
| `prod` | production, prd, prod, live, p, prd1, prod-us, prod-eu |
| `staging` | staging, stage, stg, pre-prod, preprod, uat, pre |
| `qa` | qa, test, testing, integration, int |
| `dev` | dev, development, devel, d |
| `sandbox` | sandbox, sbx, playground, scratch |
| `shared` | shared, shared-services, common, platform |
| `security` | security, sec, secops |
| `audit` | audit, log-archive, logging, logs |
| `network` | network, net, transit, connectivity |
| `mgmt` | mgmt, management, org, master, root, payer |
| `unknown` | (no signal) |

### Confidence levels

- `high` — at least one signal from tier 1–3, no conflicting signals.
- `medium` — signals from tier 4–7, OR conflicting tier-1–3 signals resolved by majority.
- `low` — signal only from tier 8–10, OR conflicting signals at the same tier.
- `unknown` — no signals at all.

### Conflict resolution

If `Environment` tag says `dev` but the resource lives under `envs/prod/`, **prefer the path** but record the conflict as an informational finding (`ENV-CONFLICT`). This is often a copy-paste bug and is itself a signal for downstream skills.

For each resource, record: resource_id, environment, confidence, signals (tier + kind + value), and conflicts.

## INTERNET EXPOSURE ANALYSIS

Exposure is **a path**, not a flag. A resource is exposed iff a reachable internet-origin packet (or request) can elicit a response from it, possibly transitively.

For each resource that *can* be reachable from the internet, compute an `exposure_path` — an ordered list of hops from the internet to the resource. If multiple paths exist, record all of them.

### Internet entry points to enumerate

- `aws_internet_gateway` attached to a VPC.
- `aws_lb` / `AWS::ElasticLoadBalancingV2::LoadBalancer` with `scheme = "internet-facing"`.
- `aws_api_gateway_rest_api`, `aws_apigatewayv2_api` with `endpoint_type = "REGIONAL"` or `"EDGE"` (not `"PRIVATE"`).
- `aws_cloudfront_distribution`.
- `aws_globalaccelerator_accelerator`.
- `aws_lightsail_*`.
- `aws_eip` associated with an instance/NAT/NLB.
- `aws_s3_bucket` whose effective ACL or policy permits `Principal: "*"` or `AWS: "*"` without a `Condition` constraining source.
- `aws_db_instance` / `aws_rds_cluster` with `publicly_accessible = true`.
- `aws_redshift_cluster` with `publicly_accessible = true`.
- `aws_elasticsearch_domain` / `aws_opensearch_domain` without VPC config and with permissive access policy.
- `aws_neptune_cluster`, `aws_docdb_cluster` with `publicly_accessible = true`.
- `aws_appsync_graphql_api` with `API_KEY` or no auth.
- `aws_lambda_function_url` with `authorization_type = "NONE"`.
- `aws_iot_endpoint`, `aws_mq_broker` with `publicly_accessible = true`.
- `aws_route53_record` pointing at any of the above (DNS exposure).
- `aws_eks_cluster` with `endpoint_public_access = true`.
- `aws_emr_cluster` with public subnets and open security groups.
- `aws_workspaces_directory` with public registration.

### Hop semantics

Each hop in an exposure path has: hop_index, resource_id, hop_type (igw/alb/nlb/api_gw/cloudfront/public_ip/sg_ingress/nacl/public_subnet/route/resource_policy/dns), permits, conditions, evidence.

A path is **complete** when it terminates at a workload or data resource. A path is **conditional** if a hop depends on an unresolved variable; mark `conditional: true`.

### Security group / NACL reasoning

You must compose security group rules and NACL rules to decide effective reachability.

- For an EC2 instance behind an internet-facing ALB: the ALB's SG must allow `0.0.0.0/0:443` (or wherever), and the instance's SG must allow ingress from the ALB's SG on the target port. If the instance SG instead allows `0.0.0.0/0` directly, record an additional **direct** path bypassing the ALB.
- For NACL: stateless, evaluate ingress AND egress. A common mistake is an open ingress NACL but blocked egress on ephemeral ports. Detect this and mark `egress_blocked: true` to avoid raising phantom-exposure findings downstream.
- `aws_security_group_rule` and inline `ingress {}` blocks must be merged before reasoning. Do not analyze them separately.

### S3 reasoning

S3 exposure is the union of:

- Bucket ACL (`acl = "public-read"`, `acl = "public-read-write"`).
- Bucket policy (`Principal: "*"` without `Condition` that constrains `aws:SourceIp`, `aws:SourceVpce`, `aws:PrincipalOrgID`, `aws:SourceArn`, etc.).
- Object ownership (`BucketOwnerPreferred` vs `ObjectWriter`) and Block Public Access settings — account-level BPA cannot be inferred from repo; bucket-level BPA can.
- `aws_s3_bucket_public_access_block` with `block_public_acls = true` etc. **suppresses** public ACL exposure even if ACLs are public; downstream skills must know this.

Record both *intended* exposure (per ACL/policy) and *effective* exposure (after BPA), as separate fields.

### CloudFront in front of a private origin

A CloudFront distribution with an OAI/OAC fronting an S3 bucket whose policy only allows the OAI principal is **internet-exposed via CloudFront**, but the S3 bucket itself is **not directly exposed**. Record this distinction precisely — the data is reachable from the internet through CloudFront, even though the bucket is locked down. This matters for several downstream skills.

### Lambda Function URL vs. Lambda behind API Gateway

- Function URL with `AuthType: NONE` → directly internet-reachable.
- Function URL with `AuthType: AWS_IAM` → reachable from the internet but requires SigV4, treat as `authenticated_exposure`.
- Lambda invoked by API Gateway → exposure is via the API Gateway hop.

For each exposed resource, record: resource_id, exposure_kind (direct/via_load_balancer/via_cdn/via_api_gateway/via_dns/via_function_url/via_resource_policy), authenticated, encrypted_in_transit, waf_present, paths, effective, conditional, evidence.

## TRUST BOUNDARY ANALYSIS

Trust is encoded in many places in AWS. A "trust boundary" is any point where a principal from outside an enclosure is allowed in. You must enumerate them all.

### Boundaries to enumerate

1. **Account boundary** — any cross-account access expressed in code:
   - `aws_iam_role.assume_role_policy` with `Principal.AWS = "arn:aws:iam::<other-account>:..."`.
   - `aws_iam_role.assume_role_policy` with `Principal.AWS = "*"` and a `Condition` referencing `aws:PrincipalOrgID` (org-wide trust, weaker boundary).
   - Resource policies (S3 bucket policy, KMS key policy, SQS, SNS, Secrets Manager, ECR repo policy, Lambda function policy) granting access to a foreign account.
   - VPC peering / TGW attachments / RAM shares to another account.
   - `aws_ram_resource_share` with `principals = [<account or org>]`.
   - `aws_organizations_account` creation (defines the account itself).

2. **Organization boundary**:
   - `Condition: { StringEquals: { "aws:PrincipalOrgID": "o-xxxx" } }` widens trust to the whole org.
   - SCPs (`aws_organizations_policy` of type `SERVICE_CONTROL_POLICY`) — record but **do not** assess sufficiency (compliance skill does that).

3. **VPC boundary**:
   - `aws_vpc_peering_connection`, `aws_vpc_peering_connection_accepter`.
   - `aws_ec2_transit_gateway_vpc_attachment`.
   - `aws_vpn_connection`, `aws_dx_connection`, `aws_dx_gateway_association`.
   - VPC endpoints (`aws_vpc_endpoint`) — interface and gateway. These are *bridges*, not boundary violations; record them so the segmentation skill can reason about which services are reachable privately.

4. **IAM trust**:
   - Every `aws_iam_role` assume role policy, normalized: trusted_services, trusted_accounts, trusted_federated, trusted_users, trusted_roles, wildcards, conditions, org_constrained.
   - `aws_iam_user`, `aws_iam_access_key` — record (and flag to secrets/IAM skills).
   - `aws_iam_openid_connect_provider` — federated trust source; note GitHub Actions OIDC, EKS IRSA, etc.

5. **KMS key policies**:
   - Default key policy with `Principal: { AWS: "arn:aws:iam::<account>:root" }` is *not* a trust boundary by itself; it delegates to IAM. Note this so downstream skills don't false-positive.
   - Cross-account grants (`aws_kms_grant`).

6. **Resource policies on data planes**:
   - S3 bucket policy, ECR repository policy, Secrets Manager resource policy, Lambda permission, SNS topic policy, SQS queue policy, EFS file system policy, OpenSearch domain policy, API Gateway resource policy, EventBridge bus policy, CloudWatch Logs resource policy, Glue resource policy, Lake Formation grants.
   - Normalize all to a `{principal, action, resource, condition}` shape.

7. **Identity federation**:
   - `aws_iam_saml_provider`, `aws_iam_openid_connect_provider`.
   - IAM Identity Center (`aws_ssoadmin_*`) permission sets and assignments.
   - Cognito identity pool roles.

8. **Service-linked roles** — record but do not treat as trust risks.

### Trust map output

Record: trust_edges (from_principal, from_kind, to_resource_id, via, actions, conditions, evidence), trust_anchors (saml_providers, oidc_providers, identity_center_instances), cross_account_relationships (direction, accounts, via, is_in_same_org).

Trust edges are the spine of attack-chain reasoning. Be exhaustive. Missing edges break downstream skills more than spurious edges do.

## RESOURCE RELATIONSHIP ANALYSIS

Build a directed multigraph `architecture_graph.json`:

- **Nodes**: resources (with all attributes from Phase 3), plus synthetic nodes for `internet`, `unresolved_reference`, `external_account:<id>`, `external_principal:<arn>`.
- **Edges**: typed relationships, each with evidence.

### Edge taxonomy

| Edge type | From → To | Meaning |
|---|---|---|
| `references` | any → any | Logical IaC reference (`Ref`, interpolation) |
| `contains` | parent → child | Module → resource, stack → resource, VPC → subnet |
| `attaches_to` | SG/role/policy → resource | `aws_iam_role_policy_attachment`, `aws_network_interface_attachment` |
| `routes_to` | route table / route → target | Route table to IGW/NAT/TGW/peering |
| `allows_ingress_from` | resource → CIDR/SG | SG ingress |
| `allows_egress_to` | resource → CIDR/SG | SG egress |
| `assumes` | role → role | Assume-role chain |
| `grants_access_to` | principal → resource | Resource policy / KMS grant |
| `encrypts_with` | resource → KMS key | Encryption relationship |
| `logs_to` | resource → log destination | CloudTrail → S3, app → CloudWatch Logs |
| `backs_up_to` | resource → backup vault | AWS Backup plans/selections |
| `triggers` | event source → target | EventBridge rule → Lambda; S3 notification → SNS |
| `stores_data_in` | compute → data store | Lambda env var SECRET_ID → Secrets Manager secret |
| `exposes` | exposure entry point → resource | LB → target group → instance |
| `runs_as` | compute → role | Lambda → execution role, ECS task → task role |
| `peers_with` | VPC → VPC | VPC peering, TGW |
| `federates_via` | role → IdP | OIDC/SAML trust |
| `replicates_to` | data store → data store | S3 replication, RDS cross-region read replica |

### Reachability annotations

For each node, precompute:

- `reachable_from_internet`: `true|false|conditional|unknown`.
- `reachable_from_other_accounts`: list of account IDs / `["*org"]` / `["*public"]`.
- `reachable_from_other_vpcs`: list of VPC IDs (logical IDs when actual IDs are unresolved).
- `assumable_by`: list of principals.

These annotations are what enable the attack-path correlation skill to do single-pass graph traversal instead of recomputing reachability per query.

### Graph hygiene

- No dangling edges. If an edge target is unresolved, point it at the synthetic `unresolved_reference` node with a stable id derived from the reference string.
- Stable node ordering in serialized output (sort by `id`) so the file is diff-friendly.
- Edge dedup: same `(from, to, edge_type, evidence_set)` collapses.

---

## CONTEXTUAL REASONING

This is where the framework earns its keep. Raw resource inspection is the baseline; context is the differentiator.

### Context dimensions to compute per resource

1. **Environment** (see above).
2. **Account role** (`workload`, `shared-services`, `security`, `audit`, `network`, `sandbox`, `mgmt`, `unknown`).
3. **Data sensitivity hint** — inferred from resource name tokens (`pii`, `payments`, `credentials`, etc.), tag values (`DataClassification`, `Compliance`), and adjacency (bucket referenced by payment Lambda).
4. **Criticality hint**: `critical` (prod data stores, admin roles, audit infra), `high` (prod compute, CI/CD to prod), `medium` (staging), `low` (dev/sandbox).
5. **Exposure** (see above).
6. **Trust posture** — external principals, org-wide, or same-account only?
7. **Reversibility** — can misconfiguration cause irreversible damage?
8. **Blast radius** — count inbound edges in the architecture graph.
9. **Lifecycle hints** — `prevent_destroy`, `deletion_protection`, `force_destroy = true`, retention periods.

### Reasoning patterns

Enrich context so downstream severity decisions are well-informed:
- Prod DB with `skip_final_snapshot = true` → `recoverability: low`
- S3 bucket referenced by CloudTrail → `criticality: critical`, `purpose: audit-log-storage`
- IAM role trusted by other-account root with no ExternalId → `trust_strength: weak`
- SG `0.0.0.0/0:22` on tagged bastion → `intent: bastion` (expected, not a mistake)

You do not decide final severity. You enrich context.

## SEVERITY GUIDANCE

> **Reminder:** this skill does not emit security severities for misconfigurations. It emits *informational* findings only. The severity guidance below is for the informational findings this skill itself produces and for the criticality hints it ships to downstream skills.

### Informational findings this skill emits

| Code | Meaning | Default severity |
|---|---|---|
| `INFO-AMBIGUOUS-ENV` | Resource environment could not be classified with confidence ≥ medium | Info |
| `INFO-UNRESOLVED-REF` | A reference could not be resolved (variable, remote state, data source) | Info |
| `ENV-CONFLICT` | Conflicting environment signals (tag vs. path, etc.) | Low |
| `INFO-UNSUPPORTED-TECH` | A future-target technology was found and skipped | Info |
| `INFO-MISSING-CONTEXT` | A piece of context expected for downstream skills is absent (e.g., no account map) | Info |
| `INFO-SUPPLY-CHAIN-OBS` | Unpinned external module source | Info |
| `INFO-SECRETS-CANDIDATE` | A file likely containing secrets was detected (handed to secrets skill) | Info |

These are **not** vulnerability findings. They are context-quality signals. They are tagged with `kind: "informational"` so reporting tools can group/separate them.

### Criticality hints shipped to downstream skills

When you label a resource `criticality: critical|high|medium|low|unknown`, downstream skills apply context-aware severity *based on* these hints. For example:

- An "S3 bucket policy permits `Principal: *`" finding from `iac-exposure-analysis` will be:
  - **Critical** if your hint marks the bucket as `criticality: critical` (prod audit logs).
  - **High** if the bucket is `criticality: high` and `data_sensitivity: confidential`.
  - **Medium** if the bucket is `criticality: low` (dev fixtures).
  - **Medium** if the bucket is `unknown` (fail toward caution).

Be deliberate in the hints you assign. Over-assigning `critical` raises downstream noise; under-assigning hides real risk.

---

## FALSE POSITIVE REDUCTION

False positives erode trust in a security platform faster than missed findings do. You are the first line of defense.

### Sources of false context

1. **Test fixtures and example code** — `examples/`, `tests/`, `test/fixtures/`, `*.test.tf`. Mark resources with `is_fixture: true`. Downstream skills suppress or downgrade findings against fixtures unless the repo is *itself* a published module repo (in which case fixture analysis still matters).
2. **Disabled resources** — `count = 0`, `count = var.enabled ? 1 : 0` with `var.enabled` defaulted to `false`, CFN `Condition` evaluating to `False`. Mark `effective: false`. Do not emit findings against effectively-disabled resources; do record them so other skills can see them.
3. **Commented-out blocks** — ignore.
4. **Generated comparison artifacts** — `cdk.out/` snapshots used for diffing in tests.
5. **Bootstrap stacks** — CDK bootstrap, Terraform bootstrap (state bucket, lock table). These often look alarming (broad IAM, bucket policies referencing the org) but are *the framework itself*. Recognize and mark `purpose: bootstrap`.
6. **Public-by-design** — static asset CDNs, marketing sites, public API documentation endpoints. Look for tags like `Public=true`, `Visibility=public`, or naming `*-public-*`, `*-website-*`, `*-assets-*`.
7. **Honeypots / canaries** — explicit tags like `Purpose=honeypot`, or names containing `honeypot`, `canary-trap`. Record and exclude from exposure findings.
8. **Vendored examples inside modules** — `modules/foo/examples/` should not be analyzed as live infrastructure.
9. **Default-by-provider attributes** — when Terraform reports `encrypted = true` because the provider defaults it, don't claim the engineer made the choice. Record `source: provider-default` in evidence.

### Conflict detection beyond environment

- Multiple resources sharing the same logical name across different files (likely a copy-paste; possibly a real duplicate). Emit `INFO-NAME-COLLISION`.
- A resource appearing in code but with `lifecycle { ignore_changes = all }` and no other configuration — likely a stub for a manually-managed resource. Mark `manually_managed_hint: true`.
- A `moved {}` block — record source/destination so historical references don't become unresolved.

### Confidence ceilings

If you cannot resolve a critical variable (e.g., a CIDR), your output for any computed exposure that depends on it caps at `confidence: low` and `conditional: true`. Downstream skills treat conditional findings differently.

---

## OUTPUT FORMAT

Primary output: compact **`iac-scan/analysis.md`** (≤ 120 lines). See Phase 12 template and [`examples/output-format.md`](examples/output-format.md). Do not embed full JSON graphs in `analysis.md`.

---

## EXAMPLE FINDINGS

> See [`examples/findings.md`](examples/findings.md) for detailed example findings with severity rationale and evidence.

---

## EXAMPLE JSON OUTPUT

> See [`examples/json-output.md`](examples/json-output.md) for complete example JSON output documents (`repo_intel.json`, `resources.json`, `architecture_graph.json`, `environment_map.json`, `exposure_map.json`, `trust_map.json`).

## CORRELATION OPPORTUNITIES

All downstream skills consume this skill's outputs. Key correlation patterns:
- Internet-exposed → privileged → cross-account assumable → ransomware-grade path
- Public bucket → audit-log bucket → log-tampering path
- Lambda function URL no-auth → execution role with `iam:*` → external-to-admin

## LIMITATIONS

1. **No live cloud awareness.** SCPs, account-level BPA, out-of-band settings are invisible. Findings assume IaC reflects reality.
2. **Variables and dynamic values.** Unresolved variables are marked `unresolved`, not guessed.
3. **External module contents.** Non-vendored registry/Git modules are recorded but internals are not analyzed.
4. **CDK source code.** Only synthesized output is analyzed; CDK source is recognized but not deeply parsed.
5. **Cross-repo composition.** `terraform_remote_state` from other repos resolves as `unresolved`.
