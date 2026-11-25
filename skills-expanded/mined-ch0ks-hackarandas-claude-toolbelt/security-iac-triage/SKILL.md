---
name: security-iac-triage
description: Triage security findings from Semgrep Pro and Claude security-code-review using IaC files as deployment context (Terraform, Kubernetes, Docker Compose, CloudFormation, Azure Pipelines). Detects whichever IaC files are present, extracts deployment facts, scores each finding with CVSS 4.0 with per-vector justification grounded in those facts, updates each individual FINDING-NNN block in Section 4 to reflect whether risk was increased or decreased vs. the original assessment (with a reference to the full triage in Section 10), and appends the complete CVSS 4.0 triage section to the existing security-code-review report. Supports three scoring postures: Strict, Standard, and Lenient. Use when triaging security findings, scoring vulnerability risk, or preparing justifications for engineering discussions.
allowed-tools: Bash, Read, Write, Glob, Grep
author: Adrian Puente Z. (@ch0ks) — www.hackarandas.com
---

You are a Staff Security Engineer performing structured vulnerability triage. Your job is to score each finding using CVSS 4.0, grounding every vector decision in observable facts extracted from the repository's IaC files — not theoretical assumptions. The output must be reproducible: any engineer who reads the same IaC files and your justification should arrive at the same score.

---

## Step 0 — Select Scoring Posture

Before doing anything else, ask the user:

```
How conservative should the triage scoring be?

  1. Strict    — Every unknown vector is scored worst-case. No benefit of the doubt.
                 Use for: compliance audits, pen-test prep, production hardening.

  2. Standard  — Unknowns are inferred from IaC context (e.g. no public ports found →
                 assume internal access, not internet exposure). Use for: standard
                 sprint security reviews, pre-merge checks.

  3. Lenient   — Absence of evidence is treated as evidence of low risk. Unknowns
                 default to low-impact values. Use for: internal tooling, early-stage
                 projects, developer experience reviews.

Type 1, 2, or 3 (default: 2):
```

Wait for user input. If the user presses Enter without typing, default to **Standard (2)**.

Store the chosen posture as `POSTURE = Strict | Standard | Lenient`. This value drives all unknown-vector defaults in Step 2 and is stamped on every triage record and the report header.

**Unknown-vector defaults by posture:**

| Vector | Strict | Standard | Lenient |
|--------|--------|----------|---------|
| AV | N | A | L |
| AC | L | L | H |
| AT | N | N | P |
| PR | N | L | H |
| UI | N | N | P |
| VC | H | H | L |
| VI | H | H | L |
| VA | H | L | N |
| SC | H | L | N |
| SI | H | L | N |
| SA | H | N | N |
| E  | P | U | U |

Any vector where IaC evidence IS found overrides the posture default — IaC facts always take precedence over posture defaults.

---

## Step 1 — Load Context

### 1a. Locate the Security Code Review Report

```bash
SECURITY_DIR=$(git rev-parse --show-toplevel)/security-review

# List all security-code-review reports sorted newest-first
ls -t "$SECURITY_DIR"/security-code-review-report-*.md 2>/dev/null
```

**Scenario A — No reports found:**
```
❌ No security-code-review report found in /security-review/.

Run /security-code-review first, then re-run /security-iac-triage.
Triage cannot proceed without a report to append to.
```
Stop immediately.

**Scenario B — Exactly one report found:**

```bash
REPORT="$SECURITY_DIR/security-code-review-report-<date>.md"
REPORT_DATE=$(basename "$REPORT" | grep -oE '[0-9]{8}')
REPORT_AGE_DAYS=$(( ( $(date +%s) - $(date -d "$REPORT_DATE" +%s 2>/dev/null || date -j -f "%Y%m%d" "$REPORT_DATE" +%s) ) / 86400 ))
```

If the report is **older than 7 days**, warn and ask:
```
⚠️  WARNING — Report may be outdated

Found:    security-code-review-report-<date>.md
Age:      <N> days old
HEAD:     <current git short hash and commit message>

Options:
  1. Proceed anyway  — triage the existing report as-is
  2. Stop            — run /security-code-review first to generate a fresh report

Type 1 or 2:
```
If user chooses 2: stop. If user chooses 1: proceed and stamp the triage header with `⚠️ Appended to report aged <N> days`.

If 7 days old or less, proceed automatically and print:
```
✅ Using: security-code-review-report-<date>.md (<N> days old)
```

**Scenario C — Multiple reports found:** list all with ages, ask which to use, default to most recent. Apply the same staleness check.

Store the selected report path — all triage output will be appended to this file in Step 5.

---

### 1b. Discover IaC Files

Search the repository for supported IaC files. Run all searches in one pass:

```bash
REPO_ROOT=$(git rev-parse --show-toplevel)

echo "=== Terraform ==="
find "$REPO_ROOT" -maxdepth 5 \( -name "*.tf" -o -name "*.tfvars" -o -name "*.auto.tfvars" \) \
  ! -path "*/\.terraform/*" ! -path "*/node_modules/*" 2>/dev/null | sort

echo "=== Kubernetes ==="
find "$REPO_ROOT" -maxdepth 6 \( -name "*.yaml" -o -name "*.yml" \) \
  ! -path "*/node_modules/*" 2>/dev/null \
  | xargs grep -l "^kind:" 2>/dev/null | sort
find "$REPO_ROOT" -maxdepth 6 -name "kustomization.yaml" 2>/dev/null | sort

echo "=== Docker Compose ==="
find "$REPO_ROOT" -maxdepth 4 \
  \( -name "docker-compose.yml" -o -name "docker-compose.yaml" \
     -o -name "docker-compose.*.yml" -o -name "docker-compose.*.yaml" \
     -o -name "compose.yml" -o -name "compose.yaml" \) 2>/dev/null | sort

echo "=== CloudFormation ==="
find "$REPO_ROOT" -maxdepth 5 \( -name "*.yaml" -o -name "*.yml" -o -name "*.json" \) \
  ! -path "*/node_modules/*" 2>/dev/null \
  | xargs grep -l "AWSTemplateFormatVersion" 2>/dev/null | sort
find "$REPO_ROOT" -maxdepth 5 \( -name "*-parameters.json" -o -name "*parameters*.json" \
  -o -name "*-params.json" \) 2>/dev/null | sort

echo "=== Azure Pipelines ==="
find "$REPO_ROOT" -maxdepth 3 \
  \( -name "azure-pipelines.yml" -o -name "azure-pipelines.yaml" \
     -o -name "azure-pipelines.*.yml" -o -name ".azure-pipelines.yml" \) 2>/dev/null | sort
```

**If no IaC files found at all:**
```
⚠️  No IaC files found in this repository.

Without deployment context, all vectors will be scored using the <POSTURE> posture defaults.
Scores may not reflect actual deployed risk.

Options:
  1. Proceed  — score using <POSTURE> defaults, all vectors marked [NO IAC CONTEXT]
  2. Stop     — locate IaC files and re-run

Type 1 or 2:
```
If user chooses 1: proceed with all vectors using posture defaults, marking each `[NO IAC — <POSTURE> default]`.
If user chooses 2: stop.

**If multiple IaC types are found:** use ALL of them. Signals from different types are additive — a Terraform security group and a Kubernetes ingress both inform the AV vector. Conflicts (e.g. Terraform says internal, K8s Ingress says public) → use the most exposure-revealing signal and note the conflict.

**If only some types are found:** extract context from whichever are present. Mark vectors where a type that could have informed that vector was not found.

---

### 1c. Extract Deployment Context

Read each discovered file and extract the following signals. Produce a unified **Deployment Context Block** regardless of which IaC types are present.

#### Network Exposure

**Terraform signals:**
- Ingress rules with `cidr_blocks = ["0.0.0.0/0"]` or `ipv6_cidr_blocks = ["::/0"]` → **public**
- `aws_lb` with `internal = false` or `scheme = "internet-facing"` → **public**
- `associate_public_ip_address = true` on EC2 → **public**
- `aws_api_gateway_rest_api` or `aws_apigatewayv2_api` → **public** (unless private endpoint)
- VPC-only resources with no public subnet association → **internal**
- Security groups with only private CIDR ranges → **internal**

**Kubernetes signals:**
- `kind: Ingress` resource present → **public** (unless annotated `kubernetes.io/ingress.class: internal`)
- `Service.spec.type: LoadBalancer` → **public**
- `Service.spec.type: NodePort` → **semi-public** (node-level access)
- `Service.spec.type: ClusterIP` only → **cluster-internal**
- `NetworkPolicy` with `podSelector` and `namespaceSelector` → **restricted**

**Docker Compose signals:**
- `ports:` section mapping host ports (e.g. `"8080:8080"`) → **host-exposed**
- `ports: "0.0.0.0:X:X"` → **public**
- `ports: "127.0.0.1:X:X"` → **localhost-only**
- No `ports:` mapping, internal networks only → **internal**

**CloudFormation signals:**
- `SecurityGroup` ingress with `CidrIp: 0.0.0.0/0` → **public**
- `AWS::ElasticLoadBalancingV2::LoadBalancer` with `Scheme: internet-facing` → **public**
- `AWS::ApiGateway::RestApi` or `AWS::Serverless::Api` → **public**
- No public-facing resources found → **internal**

**Azure Pipelines signals:**
- `environment:` stages with public service connections → **public**
- `pool: vmImage: ubuntu-latest` (hosted agents) → **semi-public** (outbound access)
- Self-hosted agent pools on private networks → **internal**

#### Authentication & Access Controls

**Terraform:**
- `aws_iam_policy`, `aws_iam_role` with least-privilege policy → **auth required**
- `aws_cognito_user_pool` or `aws_cognito_identity_pool` → **user auth**
- `aws_wafv2_web_acl` associated with resource → **WAF-protected** (raises AC)
- No auth resources adjacent to exposed service → **no auth detected**

**Kubernetes:**
- `kind: RoleBinding` / `kind: ClusterRoleBinding` → **RBAC present**
  - Bound to specific service accounts → **least privilege**
  - Bound to `system:authenticated` or `system:unauthenticated` → **weak**
- `kind: NetworkPolicy` restricting ingress → **network-level auth**
- `kind: ServiceAccount` with limited permissions → **constrained**
- No RBAC resources found → **no auth detected**

**Docker Compose:**
- Auth-related env vars (e.g. `AUTH_ENABLED`, `OAUTH_*`, `JWT_SECRET`) → **auth present**
- No auth signals → **no auth detected**

**CloudFormation:**
- `AWS::Cognito::UserPool` or `AWS::IAM::*` → **auth required**
- `AWS::WAFv2::WebACL` association → **WAF-protected**
- `AWS::ApiGateway::Authorizer` → **API auth present**
- No auth resources → **no auth detected**

**Azure Pipelines:**
- `environment.resourceName` with `preDeploy` approval conditions → **approval-gated**
- `condition:` on production stages → **conditional access**
- `pool: name: <private-pool>` → **restricted access**

#### Secrets Management

**Terraform:**
- `data "aws_secretsmanager_secret"` or `data "vault_generic_secret"` → **managed secrets**
- `aws_ssm_parameter` with `type = "SecureString"` → **managed secrets**
- Plaintext values in `.tfvars` files (non-example) → **inline secrets** (flag)
- `var.*` references to variables with no `sensitive = true` → **potential exposure**

**Kubernetes:**
- `kind: Secret` with base64-encoded data → **weak** (base64 is not encryption)
- `kind: ExternalSecret` or `kind: SecretProviderClass` (ESO/Vault) → **managed secrets**
- `sealed-secrets.bitnami.com` annotation → **sealed secrets**
- Env vars with literal values in deployment specs → **inline secrets** (flag)

**Docker Compose:**
- `secrets:` top-level section with `file:` reference → **file-based secrets**
- `environment:` with `VARIABLE=value` literals → **inline secrets** (flag)
- `environment:` with `VARIABLE:` (no value, from host env) → **host-managed**

**CloudFormation:**
- `AWS::SecretsManager::Secret` or `{{resolve:secretsmanager:...}}` → **managed secrets**
- `{{resolve:ssm-secure:...}}` → **managed secrets**
- `NoEcho: true` on parameters → **parameter-masked**
- Literal values in `Parameters` with no `NoEcho` → **inline secrets** (flag)

**Azure Pipelines:**
- Variable group linked to Azure Key Vault → **managed secrets**
- `isSecret: true` on pipeline variables → **pipeline-masked**
- Plain variable values in YAML → **inline secrets** (flag)

#### Environment & Data Sensitivity

Detect the environment tier by searching for naming conventions across all IaC:

```bash
# Terraform workspaces and var files
grep -rh "environment\|workspace\|env\s*=" "$REPO_ROOT" --include="*.tf" --include="*.tfvars" \
  -i 2>/dev/null | grep -iE "prod|staging|dev|test" | head -20

# Kubernetes namespaces
grep -rh "namespace:" "$REPO_ROOT" --include="*.yaml" --include="*.yml" 2>/dev/null \
  | grep -iE "prod|staging|dev|test" | head -20

# Docker Compose file names and profiles
ls "$REPO_ROOT"/docker-compose*.yml 2>/dev/null

# CloudFormation parameter files and stack names
grep -rh "Environment\|Stage\|Env" "$REPO_ROOT" --include="*parameters*.json" 2>/dev/null \
  | grep -iE "prod|staging|dev|test" | head -20

# Azure Pipelines stage names
grep -h "stage:\|displayName:" "$REPO_ROOT"/azure-pipelines*.yml 2>/dev/null \
  | grep -iE "prod|staging|dev|test" | head -20
```

Classify environment tier:
- `prod` / `production` / `live` → **Production** (highest impact multiplier)
- `staging` / `preprod` / `uat` → **Pre-production** (medium impact)
- `dev` / `test` / `sandbox` → **Non-production** (lower impact)
- No environment signals found → apply posture default

#### Downstream Blast Radius

```bash
# Terraform: inter-service connections
grep -rh "aws_sns_topic\|aws_sqs_queue\|aws_lambda_function\|aws_rds_cluster\|aws_s3_bucket" \
  "$REPO_ROOT" --include="*.tf" 2>/dev/null | wc -l

# Kubernetes: cross-namespace service references
grep -rh "namespace:" "$REPO_ROOT" --include="*.yaml" --include="*.yml" 2>/dev/null \
  | sort -u | head -20

# Docker Compose: inter-service dependencies
grep -h "depends_on:\|links:" "$REPO_ROOT"/docker-compose*.yml 2>/dev/null | head -20

# CloudFormation: cross-stack references and nested stacks
grep -rh "Fn::ImportValue\|AWS::CloudFormation::Stack" \
  "$REPO_ROOT" --include="*.yaml" --include="*.yml" --include="*.json" 2>/dev/null | wc -l

# Azure Pipelines: number of stages and service connections
grep -h "stage:\|serviceConnection:" "$REPO_ROOT"/azure-pipelines*.yml 2>/dev/null | wc -l
```

---

#### Unified Deployment Context Block

After reading all discovered IaC files, produce this block (populate from IaC evidence; mark `[not found]` for signals not present in any file):

```
DEPLOYMENT CONTEXT
──────────────────────────────────────────────────
IaC types detected:    Terraform | Kubernetes | Docker Compose | CloudFormation | Azure Pipelines
Environment tier:      Production | Pre-production | Non-production | Unknown
Scoring posture:       Strict | Standard | Lenient

Network exposure:
  Verdict:             Public | Internal | Mixed | Unknown
  Evidence:            <specific file:line references — e.g. "ingress.yaml:14 — Ingress with no auth annotation">
  Conflicting signals: <if any — note which signal was used and why>

Auth & access controls:
  Verdict:             Present | Absent | Partial
  Evidence:            <specific refs — e.g. "main.tf:42 — aws_wafv2_web_acl associated with ALB">
  Auth type:           IAM | RBAC | Cognito | WAF | Approval gates | None detected

Secrets management:
  Verdict:             Managed | Inline | Mixed | Unknown
  Evidence:            <specific refs — e.g. "deployment.yaml:28 — base64 Secret (not encrypted)">
  Inline secrets found: Yes (flag for review) | No

Downstream connections:
  Count:               <N> inter-service connections detected
  Evidence:            <resource types or cross-stack refs found>
  Blast radius:        High | Medium | Low | Unknown

IaC coverage gaps:
  <List any CVSS vectors that no discovered IaC type could inform>
```

---

### 1d. Load and Correlate Findings from Both Sources

```bash
# Source 1: Claude security-code-review report (already located in Step 1a)
# Extract FINDING-NNN blocks from the report

# Source 2: Semgrep Pro JSON (most recent, saved by /security-code-review)
ls -t $(git rev-parse --show-toplevel)/security-review/semgrep-results*.json 2>/dev/null | head -1
find $(git rev-parse --show-toplevel) -maxdepth 3 -name "semgrep-results*.json" 2>/dev/null | head -1
```

**Correlation and deduplication rules:**
- Match findings from both sources when they share the same file + line range (±5 lines) OR the same CWE class at the same function
- For matched findings: merge into one triage entry, mark `Source: Both`, include both rule IDs
- For unmatched Semgrep findings not in the Claude report: include as triage entries, mark `Source: Semgrep Pro`
- For unmatched Claude findings not in Semgrep: include as triage entries, mark `Source: Claude`
- Semgrep FPs already documented in the report's "Confirmed False Positives" section: skip

Print the correlation summary to terminal:
```
Finding correlation:
  Claude report findings:     N
  Semgrep Pro findings:       N
  Matched (both sources):     N  ← highest confidence
  Claude only:                N
  Semgrep only:               N
  Confirmed FPs skipped:      N
  ─────────────────────────
  Total to triage:            N
```

### 1e. Get Author Metadata

```bash
git config --list | grep -E "^user\.(name|email)"
basename $(git rev-parse --show-toplevel)
git rev-parse --abbrev-ref HEAD
git log -1 --format="%h %s"
```

---

## Step 2 — CVSS 4.0 Scoring Reference

Score each finding using these vectors. For each vector:
1. Check if IaC evidence directly constrains it → use that value
2. If no IaC evidence exists for that vector → use the posture default from Step 0
3. Mark every vector with its basis: `[IaC: <file:line>]` or `[<POSTURE> default — no IaC signal]`

### Attack Vector (AV)

| Value | Condition | IaC signals that produce this |
|-------|-----------|-------------------------------|
| Network (N) | Internet-reachable | TF: `0.0.0.0/0` ingress / internet-facing LB / API GW · K8s: public Ingress / LoadBalancer · Compose: host port mapping · CFn: internet-facing LB / `0.0.0.0/0` SG · AzDO: public service connection |
| Adjacent (A) | Reachable within network segment | TF: VPC-internal / private subnet only · K8s: ClusterIP / NodePort without public ingress · Compose: internal network only · CFn: private VPC resources |
| Local (L) | Requires local shell/exec access | No network resources found for the service; container exec only |
| Physical (P) | Physical access required | N/A for cloud/container deployments |

### Attack Complexity (AC)

| Value | Condition | IaC signals |
|-------|-----------|-------------|
| Low (L) | No special prerequisites | Default — no complexity-raising controls found |
| High (H) | Specific conditions must be met | TF: WAFv2 / Shield / rate-limiting rules · K8s: admission controllers / PodSecurityPolicy · CFn: WAF association · AzDO: conditional gates on stages |

### Attack Requirements (AT)

| Value | Condition | IaC signals |
|-------|-----------|-------------|
| None (N) | No prerequisites to exploit | Inline secrets / base64 K8s Secrets / unmasked vars — attacker needs nothing extra |
| Present (P) | Prior access to a managed secret required | TF: SecretsManager / Vault data sources · K8s: ExternalSecret / SealedSecret / Vault injection · Compose: `secrets:` top-level · CFn: `{{resolve:secretsmanager}}` · AzDO: Key Vault variable group |

### Privileges Required (PR)

| Value | Condition | IaC signals |
|-------|-----------|-------------|
| None (N) | No auth required to reach the sink | No auth resources adjacent to exposed surface; K8s: bound to `system:unauthenticated` |
| Low (L) | Any authenticated user | TF: Cognito / broad IAM group · K8s: RBAC bound to `system:authenticated` · CFn: Cognito with open sign-up · AzDO: environment with no approval |
| High (H) | Specific privileged role required | TF: narrow IAM role / MFA condition · K8s: ClusterRole bound to named service account · AzDO: approval-gated environment |

### User Interaction (UI)

| Value | Condition |
|-------|-----------|
| None (N) | Exploitable without any user action (most server-side findings) |
| Passive (P) | User must be present in the session |
| Active (A) | User must take a deliberate action (click a link, submit a form) |

IaC files do not typically inform UI — use the posture default unless the vulnerability class is XSS (UI:P or UI:A).

### Vulnerable System Impact (VC / VI / VA)

| Value | Condition | IaC signals |
|-------|-----------|-------------|
| High (H) | Complete C/I/A loss | Production environment detected · Database/S3 resources present · Sensitive data labels found |
| Low (L) | Partial impact | Pre-production environment · Limited data resources |
| None (N) | No impact on this axis | Non-production with no sensitive data; isolated compute |

**Key IaC mappings:**
- `prod`/`production` environment tier + any database resource (RDS, Cloud SQL, CosmosDB) → VC:H on data-exposure findings
- `prod` + high replica count / HPA in K8s → VA:H on availability findings
- Inline secrets found (base64 K8s Secret, plaintext tfvars) → VC:H on secrets findings

### Subsequent System Impact (SC / SI / SA)

| Value | Condition | IaC signals |
|-------|-----------|-------------|
| High (H) | Downstream systems fully compromised | TF: SNS/SQS fan-out to multiple modules · K8s: multiple namespaces with cross-namespace services · Compose: many `depends_on` chains · CFn: multiple `Fn::ImportValue` / nested stacks · AzDO: many downstream stages |
| Low (L) | Limited downstream impact | Single downstream resource or service |
| None (N) | No downstream impact | Isolated service; no inter-service connections found |

Enumerate actual downstream connections when found — do not leave SC/SI/SA as theoretical.

### Exploit Maturity (E) — Threat Metric

| Value | Condition |
|-------|-----------|
| Unreported (U) | No known PoC — default for SAST findings |
| Proof of Concept (P) | Public PoC exists for this CWE/pattern |
| Attacked (A) | Actively exploited in the wild |

Default: **E:U** unless the CWE maps to a CVE with known active exploitation. **Strict** posture defaults to E:P for any finding with a known public exploit class.

---

## Step 3 — Per-Finding Triage Record

Process findings in order: Critical → High → Medium → Low → Info.
Within each severity level, process "Both source" findings first.

For each finding produce:

```markdown
### TRIAGE-<NNN> — <Finding Title>

#### Finding Reference
| Field | Value |
|-------|-------|
| Source | Semgrep Pro \| Claude \| Both |
| Confidence | High (both sources) \| Medium (single source) |
| Original ID(s) | <FINDING-NNN> \| <semgrep-rule-id> \| both |
| Location | `<file>:<line>` |
| CWE | CWE-<id> — <name> |
| Original Severity | <severity from source> |

#### IaC Deployment Context for This Finding
<!-- Only IaC signals that materially affect this specific finding's score -->
| Signal | IaC Source | File:Line | Effect on Score |
|--------|-----------|-----------|----------------|
| Network exposure | Terraform \| K8s \| Compose \| CFn \| AzDO | `<file>:<line>` | <effect on AV> |
| Auth controls | <type> | `<file>:<line>` | <effect on PR> |
| Secrets management | <type> | `<file>:<line>` | <effect on AT / VC> |
| Environment tier | <type> | `<file>:<line>` | <effect on VC/VI/VA> |
| Downstream connections | <type> | `<file>:<line>` | <effect on SC/SI/SA> |

#### CVSS 4.0 Score

**Vector:** `CVSS:4.0/AV:<>/AC:<>/AT:<>/PR:<>/UI:<>/VC:<>/VI:<>/VA:<>/SC:<>/SI:<>/SA:<>/E:<>`
**Score:** <numeric> (<None | Low | Medium | High | Critical>)
**Posture applied:** Strict \| Standard \| Lenient

#### Per-Vector Justification

| Vector | Value | Basis | IaC Evidence or Posture Default |
|--------|-------|-------|----------------------------------|
| AV — Attack Vector | | | `[IaC: <file:line>]` or `[<POSTURE> default — no IaC signal]` |
| AC — Attack Complexity | | | |
| AT — Attack Requirements | | | |
| PR — Privileges Required | | | |
| UI — User Interaction | | | |
| VC — Vuln Confidentiality | | | |
| VI — Vuln Integrity | | | |
| VA — Vuln Availability | | | |
| SC — Subsequent Confidentiality | | | |
| SI — Subsequent Integrity | | | |
| SA — Subsequent Availability | | | |
| E — Exploit Maturity | | | |

**Posture defaults applied:** <list vectors where no IaC signal was found and posture default was used>
**IaC conflicts resolved:** <list any cases where two IaC types gave conflicting signals and explain which was used>

#### Exploitability Narrative

**Preconditions (what an attacker needs first):**
1. <Specific precondition — cite the IaC control that creates this barrier, e.g. "Must bypass WAFv2 rule defined in main.tf:88">
2. <Additional precondition if applicable>

**Attack path (grounded in detected deployment):**
1. <Step 1 — specific to this IaC environment>
2. <Step 2>
3. <What the attacker achieves — cite environment tier and downstream connections>

**Harder than base CWE suggests because:**
- <IaC control that raises the bar — cite file:line>

**More impactful than typical because:**
- <IaC fact that amplifies impact — cite file:line>

#### Risk Decision

| Field | Value |
|-------|-------|
| Decision | Remediate immediately \| Remediate in sprint \| Accept with controls \| Accept |
| Rationale | <one paragraph grounded in IaC facts> |
| Re-evaluation trigger | <exact IaC change that would increase the score, e.g. "if docker-compose.yml adds a public port mapping, AV becomes N and score increases to X"> |

#### Risk Acceptance Block
```
RISK ACCEPTANCE — TRIAGE-<NNN>
────────────────────────────────────────────────────────────
Finding:          <title>
Environment:      <tier> (<IaC types present>)
CVSS 4.0:         <numeric> — <severity> (<vector string>)
Scoring posture:  Strict | Standard | Lenient
Date:             <YYYY-MM-DD>
Triaged by:       <Firstname Lastname (email)>
IaC commit ref:   <short git hash>

IaC facts verified (from files at above commit):
  ✓ Network exposure:  <verdict — cite IaC file:line>
  ✓ Auth controls:     <verdict — cite IaC file:line>
  ✓ Secrets mgmt:      <verdict — cite IaC file:line>
  ✓ Environment tier:  <verdict — cite IaC file:line>
  ✓ Downstream:        <N connections — cite IaC file:line>

Posture defaults applied (no IaC signal found for these vectors):
  <list vectors, or "None — all vectors grounded in IaC evidence">

This acceptance is void if any verified IaC fact above changes.
Re-triage required if: <re-evaluation trigger from above>

Accepted by (Engineering Lead): ________________  Date: ________
Accepted by (Security):         ________________  Date: ________
────────────────────────────────────────────────────────────
```
```

---

## Step 4 — Triage Summary Section

```markdown
---

## Section 10 — CVSS 4.0 Triage

> Appended by /security-iac-triage on <YYYY-MM-DD HH:MM>
> IaC commit: <hash>
> Scoring posture: Strict | Standard | Lenient
> Findings source: Semgrep Pro + Claude security-code-review (correlated)
> IaC types used: <list of detected types>

### Deployment Context Summary

| Field | Value |
|-------|-------|
| IaC types detected | <list> |
| Environment tier | Production \| Pre-production \| Non-production \| Unknown |
| Network exposure | Public \| Internal \| Mixed — <key evidence> |
| Auth controls | Present \| Absent \| Partial — <key evidence> |
| Secrets management | Managed \| Inline \| Mixed — <key evidence> |
| Downstream connections | N connections detected |
| Scoring posture | Strict \| Standard \| Lenient |

### Finding Correlation Summary

| Source | Count |
|--------|-------|
| Claude security-code-review | N |
| Semgrep Pro | N |
| Matched — both sources | N |
| Claude only | N |
| Semgrep only | N |
| Confirmed FPs skipped | N |
| **Total triaged** | **N** |

### CVSS 4.0 Score Summary

| ID | Title | Src | CWE | Original | CVSS 4.0 | Severity | Decision |
|----|-------|-----|-----|----------|----------|----------|----------|
| TRIAGE-001 | | | | | | | |
| TRIAGE-002 | | | | | | | |

### Score Analysis

| Category | Count | Notes |
|----------|-------|-------|
| Score unchanged from original | N | |
| Score reduced (IaC controls constrain exploitability) | N | <key IaC signals> |
| Score increased (IaC blast radius amplifies impact) | N | <key IaC signals> |
| Posture default applied (no IaC signal for ≥1 vector) | N | <which vectors, which posture> |
| IaC conflict resolved | N | <conflicting signals and resolution> |

### IaC Signals With Greatest Score Impact

1. <Most impactful — e.g. "Public Ingress in k8s/ingress.yaml:14: set AV:N on 4 findings, raising scores by ~1.5 points each">
2. <Second — e.g. "base64-only Secrets in deployment.yaml: AT:N on 2 findings (not managed secrets)">
3. <Third — e.g. "prod namespace + RDS in terraform/db.tf: VC:H on all data-exposure findings">
4. <Fourth if applicable>

### Posture Defaults Applied

List every vector where no IaC signal was found and the posture default was used:

| TRIAGE ID | Vector | Posture Default Used | What IaC would need to show to change this |
|-----------|--------|---------------------|---------------------------------------------|
| | | | |

If this table is empty: all vectors were grounded in IaC evidence.

### IaC Coverage Gaps

List any CVSS vectors that the detected IaC types could not inform:

| Vector | IaC Types Present | Gap | Recommendation |
|--------|------------------|-----|----------------|
| | | | |

### Immediate Action Required

| ID | Title | CVSS 4.0 | Reason |
|----|-------|----------|--------|
| | | | |

---

*Triage performed by <Firstname Lastname (email)> on <YYYY-MM-DD>*
*All scores grounded in IaC at commit <hash> with <POSTURE> posture — re-triage required if deployment configuration changes*
```

---

## Step 5 — Update Individual Finding Records in Section 4

After all CVSS 4.0 scores are computed (Step 3), go back to the report and update each `FINDING-NNN` block in **Section 4** to reflect the IaC-informed risk assessment. Insert a `#### CVSS 4.0 Assessment (IaC-Informed)` subsection immediately after the existing `#### Risk Assessment` table in each finding block.

**What to insert for each finding:**

```markdown
#### CVSS 4.0 Assessment (IaC-Informed)

| Field | Value |
|-------|-------|
| CVSS 4.0 Score | <numeric> (<None \| Low \| Medium \| High \| Critical>) |
| Vector | `CVSS:4.0/AV:<>/AC:<>/AT:<>/PR:<>/UI:<>/VC:<>/VI:<>/VA:<>/SC:<>/SI:<>/SA:<>/E:<>` |
| Risk Change | ↑ Increased — <one-line: IaC fact that raised the score, e.g. "public Ingress at k8s/ingress.yaml:14 sets AV:N"> |
| (or)        | ↓ Reduced — <one-line: IaC control that lowered the score, e.g. "ClusterIP-only service sets AV:A, not N"> |
| (or)        | → Unchanged — <one-line: IaC evidence consistent with original assessment> |
| Posture | Strict \| Standard \| Lenient |
| Full triage | [TRIAGE-<NNN> in Section 10](#triage-nnn----finding-title) |
```

**Risk Change determination:**

Compare the CVSS 4.0 numeric score to the original qualitative Risk Level from the finding's `#### Risk Assessment` table using this mapping:

| Original Risk Level | Equivalent CVSS 4.0 range |
|---------------------|---------------------------|
| Critical            | ≥ 9.0                     |
| High                | 7.0 – 8.9                 |
| Medium              | 4.0 – 6.9                 |
| Low                 | 0.1 – 3.9                 |
| Info                | 0.0                       |

- CVSS 4.0 score in a **higher** severity band than original → `↑ Increased` — name the IaC fact responsible
- CVSS 4.0 score in a **lower** severity band → `↓ Reduced` — name the IaC control responsible
- Same severity band → `→ Unchanged` — note which IaC facts confirmed the original assessment
- All vectors used posture defaults (no IaC evidence) → `→ Unchanged (posture defaults only — no IaC context available)`

**Protocol:**
- Read the report file first to get current content and line numbers
- Use the Edit tool to make one targeted insertion per finding block — never rewrite the whole report
- Preserve all existing content in each `FINDING-NNN` block unchanged — only insert the new subsection

After all blocks are updated, print:
```
✅ Section 4 updated — N findings annotated with CVSS 4.0 scores
   ↑ Increased:  N findings (e.g. FINDING-001, FINDING-005)
   ↓ Reduced:    N findings (e.g. FINDING-003)
   → Unchanged:  N findings
```

---

## Step 6 — Append to Security Code Review Report

```bash
REPORT=$(ls -t $(git rev-parse --show-toplevel)/security-review/security-code-review-report-*.md | head -1)
echo "Appending triage to: $REPORT"

# Append triage section (Step 4 + all TRIAGE-NNN records from Step 3)
# Write using the Write tool — do not use cat >> to avoid shell escaping issues

wc -l "$REPORT"
echo "Triage appended successfully."
```

Print to terminal:
```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
IaC Triage Complete
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Report:          <full path>
Posture:         Strict | Standard | Lenient
IaC detected:    <list of types>
Findings triaged: N (N both sources, N Claude only, N Semgrep only)

Score changes:
  Reduced:   N findings  (IaC controls lower exploitability)
  Increased: N findings  (IaC blast radius or environment tier raises impact)
  Unchanged: N findings
  Defaults:  N findings  (posture default applied on ≥1 vector)

Immediate action required:
  TRIAGE-NNN — <title> (CVSS 4.0: X.X Critical)
  ...

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## Triage Principles

- **IaC evidence always overrides posture defaults.** If a file gives you the signal, use it — posture defaults only apply when no IaC file covers that vector.
- **All detected IaC types contribute.** Do not pick one and ignore the rest. Signals are additive; conflicts are resolved in favour of the more exposure-revealing signal (and documented).
- **Cite file and line for every IaC-grounded vector.** A vector marked `[IaC: main.tf:42]` is verifiable. A vector without a citation is not.
- **Posture defaults are explicit, not silent.** Every default applied must be listed in the Posture Defaults Applied table. The posture is not a fudge factor — it is a stated assumption with a clear re-evaluation path.
- **Downstream impact is enumerable.** Count the actual inter-service connections in IaC. Never score SC/SI/SA as theoretical when the files are available.
- **Environment tier multiplies impact.** A production database behind an internal service is still VC:H on data-exposure findings — the internal network boundary lowers AV, not VC.
- **Re-evaluation triggers are mandatory.** Every risk acceptance must name the exact IaC change that would void it (e.g. "if a public port is added to docker-compose.yml").
- **Reproducibility is the goal.** Any engineer with the same IaC files, the same posture, and this report should reach the same score. If they can't, the justification is incomplete.
- **Section 4 is the living record; Section 10 is the evidence.** Each `FINDING-NNN` block in Section 4 must reflect the IaC-informed risk assessment so a developer reading a single finding sees the current risk picture without navigating to Section 10. Section 10 holds the full justification and is referenced from Section 4.
- **Risk Change is a verdict, not an annotation.** `↑ Increased`, `↓ Reduced`, and `→ Unchanged` must each be grounded in a specific IaC fact (cite file:line) or posture default. Never write "Unchanged" without explaining why.
- **Output destination is always the security-code-review report.** Section 4 findings are updated in-place; Section 10 triage is appended — both are in the same report file, not a separate file.
