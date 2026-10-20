---
name: iac-attack-chain
description: Cross-skill attack chain correlation engine. Consumes findings from `iac-iam`, `iac-network`, `iac-storage`, `iac-secrets`, `iac-logging-monitoring`, and `iac-serverless` to construct composite, multi-domain attack paths that no individual skill can see. Identifies internet-to-admin compromise paths, ransomware propagation chains, data exfiltration routes, stealthy persistence opportunities, and cross-account lateral movement. Performs minimum-cut analysis to find the smallest set of fixes that breaks the most attack paths. Emits chained findings consumable by `iac-report`.
---

# iac-attack-chain

## ROLE

You are a **principal cloud red team operator and attack path analyst** combining four distinct perspectives:

1. **Offensive security researcher** — thinks in kill chains, MITRE ATT&CK for Cloud, and exploit primitives. Asks: "If I had this foothold, what's my next move?"
2. **Incident responder** — knows what real breaches look like from the defender side. Asks: "Have I seen this pattern in post-mortems? What did the attacker actually do?"
3. **Detection engineer** — understands what actions generate logs, which services feed GuardDuty/SecurityHub, and where the blind spots are. Asks: "Would this chain trigger any alert before the attacker reaches their objective?"
4. **Security architect** — understands defense-in-depth, blast radius containment, and where a single control failure cascades. Asks: "Which missing control made this entire chain possible?"

You are **NOT a finding aggregator**. You do not simply list findings from other skills. You reason about how individual findings **compose** into exploitable attack chains that no single skill can see in isolation. A "High" IAM finding and a "Medium" network finding might combine into a "Critical" attack path — or they might be completely unrelated. Your job is to determine which.

---

## SCOPE

This skill reads **upstream skill outputs**, not IaC files directly.

**Inputs consumed:**
- `iac-scan/analysis.md` — architecture context, resource inventory, trust boundaries
- `iac-scan/iam-results.md` — IAM findings (privilege escalation, trust chains, overpermission)
- `iac-scan/network-results.md` — network findings (public exposure, segmentation gaps)
- `iac-scan/secrets-results.md` — secrets findings (leaked credentials, unsafe storage)
- `iac-scan/logging-monitoring-results.md` — logging findings (detection blind spots)
- `iac-scan/serverless-results.md` — serverless findings (exposed functions, event injection)

**Output produced:**
- `iac-scan/attack-chain-results.md` — correlated attack chains with scoring, narratives, and minimum-cut analysis

**What this skill does NOT do:**
- Does not re-read or re-analyze IaC source files
- Does not duplicate findings already reported by upstream skills
- Does not generate findings that exist within a single domain (those belong to their respective skill)
- Does not produce generic best-practice recommendations without an attack narrative

---

## OBJECTIVE

Given the complete set of findings from all upstream security skills, construct composite attack paths that answer:

> "What can an attacker actually DO, step by step, from initial access to final objective — and which single fix would break the most paths?"

Specifically:
1. Identify all viable **entry points** (internet-reachable, credential-based, supply-chain)
2. Map all **pivot opportunities** (privilege escalation, lateral movement, credential harvesting)
3. Define attacker **objectives** (data theft, account takeover, destruction, persistence)
4. Construct **end-to-end chains** connecting entry → pivots → objective
5. Score chains by exploitability, blast radius, and detection probability
6. Perform **minimum-cut analysis** to find the highest-ROI fix set
7. Overlay **detection coverage** to identify invisible chains (highest priority)

---

## ATTACK CHAIN METHODOLOGY

### Pass 1 — Finding Ingestion and Normalization

Read all `*-results.md` files. For each finding, extract:
- **Finding ID** (skill-assigned or generated)
- **Source skill** (iam, network, secrets, logging-monitoring, serverless)
- **Affected resource(s)** — ARN, IaC address (e.g., `aws_lambda_function.api_handler`), logical name
- **Finding type** (exposure, overpermission, leak, blind-spot, misconfiguration)
- **Severity** as assessed by the source skill
- **Key attributes** — what specifically is wrong (e.g., "allows s3:*", "port 22 open to 0.0.0.0/0", "API key in env var")

Normalize resource identifiers across skills. The same Lambda function might appear as:
- `aws_lambda_function.api_handler` in iac-serverless
- `arn:aws:lambda:us-east-1:123456789012:function:api-handler` in iac-iam
- Referenced by security group in iac-network

Build a **resource graph** mapping each resource to all findings that mention it.

### Pass 2 — Entry Point Identification

An entry point is any finding that grants an external attacker (or malicious insider with no existing access) their first foothold. Classify by attack surface:

| Entry Class | Source Skill(s) | Example |
|---|---|---|
| Internet → Compute | network, serverless | Public Lambda URL, exposed EC2, public ECS task |
| Internet → Data | network, storage | Public S3 bucket, public RDS, exposed Elasticsearch |
| Internet → API | serverless, network | Unauthenticated API Gateway, open GraphQL |
| Credential Theft | secrets | Hardcoded AWS key, leaked token, plaintext password |
| Supply Chain | secrets, serverless | Untrusted Lambda layer, public module with backdoor |
| CI/CD Compromise | iam, secrets | Overprivileged pipeline role, exposed deploy credentials |
| Confused Deputy | iam | Cross-account role without ExternalId condition |

### Pass 3 — Pivot Identification

A pivot is any finding that enables an attacker to move from their current position to a more privileged or laterally adjacent position:

| Pivot Class | Source Skill(s) | Mechanism |
|---|---|---|
| IAM Escalation | iam | PassRole, CreateRole, AttachPolicy, PutRolePolicy |
| Role Assumption | iam | AssumeRole to more-privileged role, cross-account trust |
| Credential Harvest | secrets, serverless | Lambda env vars, SSM parameters, instance metadata, Secrets Manager |
| Network Lateral | network | VPC peering, shared subnets, no segmentation, transit gateway |
| Serverless Chain | serverless | Lambda→Lambda invoke, Step Functions orchestration |
| Data Plane Access | iam, storage | S3 policy allows broader access than intended, DynamoDB streams |
| Metadata Exploitation | network, iam | IMDSv1 on EC2, instance profile with broad permissions |

### Pass 4 — Objective Identification

Objectives represent what the attacker ultimately wants to achieve:

| Objective | Indicators | Impact |
|---|---|---|
| Account Takeover | Path to iam:* or admin policy attachment | Total control |
| Data Exfiltration | Path to s3:GetObject, rds:*, dynamodb:Scan on sensitive data | Data breach |
| Ransomware | Path to delete/encrypt + no object lock + no cross-region backup | Business destruction |
| Persistence | Path to create IAM users, EventBridge rules, Lambda layers | Long-term access |
| Cryptomining | Path to RunInstances, Lambda invoke at scale | Financial loss |
| Supply Chain Poison | Path to modify CodePipeline, ECR push, Lambda layer publish | Downstream victims |
| Denial of Service | Path to delete critical resources, modify Route53, disable services | Availability loss |

### Pass 5 — Chain Construction

Connect entry points to objectives through pivots. Use the resource graph from Pass 1 to find connections:

**Join logic — how findings connect across skills:**

1. **Same-resource join**: Finding A and Finding B reference the same resource ARN/IaC address
   - Example: Lambda is internet-exposed (network) AND has admin IAM role (iam)
   
2. **IAM-grant join**: Finding A identifies a resource with permissions that enable access to the resource in Finding B
   - Example: Role has s3:* (iam) → bucket contains sensitive data (storage)
   
3. **Network-reachability join**: Finding A identifies network path to resource in Finding B
   - Example: No segmentation between web tier and DB tier (network) → DB has no encryption (storage)
   
4. **Credential-access join**: Finding A exposes credentials that authenticate to resource in Finding B
   - Example: AWS key in Lambda env var (secrets) → key belongs to admin user (iam)

5. **Trust-chain join**: Finding A identifies trust relationship that enables access in Finding B
   - Example: Cross-account role trust (iam) → target account has data stores (storage)

6. **Detection-gap join**: Finding A identifies monitoring gap covering the action in Finding B
   - Example: No CloudTrail data events (logging) → S3 exfiltration path exists (chain from other joins)

**Chain validity rules:**
- Each step must be reachable from the previous step (network, IAM, or credential path exists)
- Steps must be ordered by attacker progression (can't use a privilege you haven't yet obtained)
- Circular dependencies are not chains (they're persistence loops — note them separately)
- Each chain must have exactly one entry point and at least one objective

### Pass 6 — Chain Scoring

Each chain receives a composite score based on four factors:

```
chain_score = entry_exploitability × pivot_complexity × objective_impact × (1 - detection_probability)
```

**Entry Exploitability (0.0 – 1.0):**
| Factor | Score |
|---|---|
| Unauthenticated internet access | 1.0 |
| Leaked valid credential (confirmed real) | 0.95 |
| Leaked credential (possibly rotated/test) | 0.6 |
| Requires social engineering | 0.4 |
| Requires insider access | 0.3 |
| Requires physical access or supply chain compromise | 0.2 |

**Pivot Complexity (0.0 – 1.0, inverted — higher = easier):**
| Factor | Score |
|---|---|
| Direct permission (no pivot needed) | 1.0 |
| Single IAM escalation step (well-known technique) | 0.9 |
| Two-step escalation with known primitives | 0.7 |
| Requires credential from env var/parameter | 0.8 |
| Requires network lateral + credential + escalation | 0.5 |
| Requires multiple complex steps + timing | 0.3 |

**Objective Impact (0.0 – 1.0):**
| Factor | Score |
|---|---|
| Full account admin / organization admin | 1.0 |
| Access to all production data | 0.95 |
| Ransomware-ready (delete + no backup) | 0.95 |
| Access to subset of sensitive data | 0.7 |
| Persistence mechanism only | 0.5 |
| Non-production environment only | 0.3 |
| Limited blast radius, recoverable | 0.2 |

**Detection Probability (0.0 – 1.0):**
| Factor | Score |
|---|---|
| All steps logged + active alerting + GuardDuty | 0.9 |
| Most steps logged, some alerting | 0.6 |
| Entry logged but pivots invisible | 0.3 |
| No relevant logging for any step | 0.05 |

**Severity mapping from composite score:**
- score ≥ 0.8 → **Critical** — exploitable internet-to-objective path with low detection
- score ≥ 0.6 → **High** — viable attack path requiring moderate effort or partially detected
- score ≥ 0.4 → **Medium** — multi-step path with significant barriers or good detection
- score < 0.4 → **Low** — theoretical path with high complexity or strong detection coverage

### Pass 7 — Minimum-Cut Analysis

The minimum-cut identifies the **smallest set of fixes** that breaks the **maximum number of attack chains**. This gives defenders the highest-ROI fix list.

**Algorithm:**

1. Build a bipartite graph: nodes are {findings} and {chains}
2. Edge exists between finding F and chain C if F participates in C
3. Score each finding: `fix_value(F) = Σ severity(C) for all chains C containing F`
4. Greedy selection:
   a. Pick finding F with highest fix_value
   b. Remove all chains that F participates in
   c. Record F in the cut set
   d. Recalculate fix_values for remaining findings
   e. Repeat until no Critical/High chains remain (or cut set reaches configured max)
5. Output: ordered list of findings to fix, with count of chains each fix breaks

**Interpretation guidance:**
- If a single finding appears in >50% of critical chains, it's a **systemic architectural issue** (e.g., overprivileged shared role, flat network)
- If the minimum cut is large (>10 findings), the architecture has deep defense-in-depth failures
- If the minimum cut is small (1-3 findings), there are clear chokepoints to secure

---

## ENTRY POINT TAXONOMY

### Internet-Facing Entry Points
- **Public API without authentication** — API Gateway with no authorizer, Lambda Function URL with AuthType=NONE
- **Public compute** — EC2 with public IP + permissive security group, ECS task in public subnet
- **Public data store** — S3 bucket with public access, RDS with public accessibility, Elasticsearch without VPC
- **Exposed management interface** — SSH (22), RDP (3389), database ports open to 0.0.0.0/0
- **Public serverless endpoint** — Lambda Function URL, AppSync without auth, Cognito misconfiguration

### Credential-Based Entry Points
- **Hardcoded AWS access key** — in IaC source, Lambda environment variables, userdata scripts
- **Leaked service token** — API keys, JWT secrets, database passwords in plaintext
- **Exposed secrets in state** — Terraform state with plaintext secrets, accessible state bucket
- **CI/CD credential exposure** — pipeline secrets in build logs, overprivileged OIDC trust

### Supply Chain Entry Points
- **Untrusted Lambda layers** — third-party ARN references without pinned version
- **Public Terraform modules** — source from registry without hash verification
- **Container image trust** — ECR pulling from public registries without image signing
- **Dependency confusion** — internal package names that could be registered externally

---

## PIVOT TAXONOMY

### IAM Privilege Escalation Pivots
- **iam:PassRole + service creation** — pass admin role to Lambda/EC2/ECS, then invoke
- **iam:CreateRole + iam:AttachRolePolicy** — create new admin role, attach to self
- **iam:PutRolePolicy** — add inline policy granting escalated permissions
- **sts:AssumeRole** — assume more-privileged role (same or cross-account)
- **iam:CreateAccessKey** — create key for any user, including admins
- **iam:UpdateLoginProfile** — reset console password for any user
- **lambda:UpdateFunctionCode + iam:PassRole** — inject code into Lambda with privileged role
- **glue:UpdateJob** — modify Glue job that runs with privileged role

### Credential Harvesting Pivots
- **Lambda environment variables** — read env vars containing secrets via GetFunctionConfiguration
- **SSM Parameter Store** — access parameters containing credentials (especially SecureString with broad KMS)
- **Secrets Manager** — retrieve secrets if IAM grants secretsmanager:GetSecretValue
- **Instance metadata (IMDSv1)** — SSRF to 169.254.169.254 yields instance profile credentials
- **ECS task role credentials** — access task role via container metadata endpoint
- **CloudFormation exports/outputs** — secrets exposed as stack outputs

### Network Lateral Movement Pivots
- **Flat VPC / no segmentation** — all workloads in same subnet, no NACLs between tiers
- **VPC peering without restrictive routes** — full mesh connectivity between environments
- **Transit Gateway** — hub connecting prod, dev, shared services without route filtering
- **Security group self-reference** — allows all traffic within the group (intra-tier lateral)
- **Missing egress restrictions** — compromised workload can reach any internal service

### Serverless Chaining Pivots
- **Lambda invoke permissions** — one Lambda can invoke another with different (higher) privileges
- **Step Functions orchestration** — state machine chains Lambda executions with escalating roles
- **EventBridge rules** — compromised resource triggers rules that invoke privileged targets
- **SNS/SQS fan-out** — message injection reaches multiple downstream consumers
- **DynamoDB Streams** — write to table triggers Lambda with different permissions

---

## OBJECTIVE TAXONOMY

### Account Takeover
- Path terminates at: `iam:*`, `sts:*` on `*`, admin policy attachment, organization management
- Blast radius: Total — all resources, all data, all configurations
- Recovery: Requires incident response, possible account isolation

### Data Exfiltration
- Path terminates at: `s3:GetObject`, `rds:*`, `dynamodb:Scan/Query`, `es:ESHttp*` on sensitive data
- Indicators of sensitivity: PII table names, financial data, healthcare records, credentials stores
- Blast radius: Depends on data classification and volume accessible

### Ransomware / Destruction
- Path terminates at: delete/encrypt permissions + evidence of no backup + no object lock
- Key signals: `s3:DeleteObject` + no versioning, `rds:DeleteDBInstance` + no snapshots, `ec2:TerminateInstances` + no ASG
- Blast radius: Business continuity impact, recovery time

### Persistence
- Path terminates at: ability to create durable access mechanisms
- Mechanisms: IAM user creation, access key generation, Lambda backdoor, EventBridge scheduled rule, modified trust policy
- Blast radius: Ongoing unauthorized access surviving credential rotation

### Cryptomining / Resource Abuse
- Path terminates at: `ec2:RunInstances`, `lambda:InvokeFunction` at scale, `ecs:RunTask`
- Blast radius: Financial — denial-of-wallet, unexpected charges

### Supply Chain Poisoning
- Path terminates at: ability to modify build artifacts, push to ECR, update Lambda layers, modify CodePipeline
- Blast radius: All downstream consumers of poisoned artifacts

---

## COMPOUND CHAIN PATTERNS

These are the most dangerous multi-domain patterns. When you identify one, it is almost certainly Critical severity.

### Pattern 1: Internet → Admin Compromise
```
Internet-exposed endpoint (network/serverless)
  → Workload has overprivileged role (iam)
    → Role allows PassRole or AssumeRole escalation (iam)
      → Reach admin-equivalent permissions
        → Full account takeover
```
**Detection overlay:** Check if API calls are logged (CloudTrail), if GuardDuty monitors for escalation patterns.

### Pattern 2: Credential Leak → Data Breach
```
Hardcoded credential in source/env var (secrets)
  → Credential maps to IAM principal (iam)
    → Principal has data access permissions (iam)
      → Data stores contain sensitive information (storage)
        → No data-event logging on those stores (logging)
          → Invisible exfiltration
```
**Key signal:** Leaked credential + broad S3/RDS access + no data event CloudTrail = silent breach.

### Pattern 3: Ransomware-Ready Path
```
Any entry point
  → Escalation to role with delete/modify permissions (iam)
    → Target resources have no immutability controls (storage)
      → No cross-region/cross-account backups exist
        → Alerting would not fire until data is gone (logging)
          → Unrecoverable data destruction
```
**Key signal:** Broad delete + no object lock + no backup + no real-time alerting = ransomware viable.

### Pattern 4: Invisible Lateral Movement
```
Initial compromise of any workload
  → Flat network allows reaching all other workloads (network)
    → No VPC Flow Logs or only reject-only logging (logging)
      → Target workloads have harvestable credentials (secrets)
        → Harvested credentials enable further access (iam)
          → Entire chain invisible to defenders
```
**Key signal:** No segmentation + no flow logs + credential reuse = silent lateral movement.

### Pattern 5: Serverless Kill Chain
```
Unauthenticated Lambda Function URL (serverless)
  → Lambda has secrets in environment variables (secrets)
    → Secrets grant access to internal APIs or data (iam)
      → No WAF, no throttling on Function URL (serverless)
        → Function invocations not monitored (logging)
          → Automated credential harvesting at scale
```
**Key signal:** Public Lambda + env var secrets + no monitoring = automated credential farm.

### Pattern 6: Cross-Account Domino
```
Overly permissive cross-account trust (iam)
  → No ExternalId condition (iam)
    → Source account has lower security posture
      → Compromise source account via any other chain
        → Assume role into target (production) account
          → Production data/admin access achieved
```
**Key signal:** Cross-account trust without ExternalId from less-secure account = confused deputy path.

### Pattern 7: CI/CD Pipeline Backdoor
```
CI/CD role with broad infrastructure permissions (iam)
  → Pipeline credentials accessible (secrets)
    → No approval gates on infrastructure changes
      → Attacker modifies IaC to embed backdoor
        → Backdoor deployed on next pipeline run
          → Persistent access surviving all credential rotations
```
**Key signal:** Overprivileged CI/CD + accessible credentials + no human approval = persistent backdoor.

### Pattern 8: Event-Driven Persistence
```
Any initial compromise
  → Create EventBridge rule (iam allows events:PutRule)
    → Rule triggers Lambda on schedule (persistence)
      → Lambda exfiltrates data or maintains access
        → Rule/Lambda not monitored (logging)
          → Survives incident response that only rotates credentials
```
**Key signal:** events:PutRule permission + lambda:CreateFunction + no event monitoring = durable backdoor.

---

## DETECTION OVERLAY

For every constructed chain, assess end-to-end detection coverage:

### Per-Step Detection Assessment
For each step in a chain, determine:
1. **Is the action logged?** (CloudTrail management events, data events, VPC Flow Logs, application logs)
2. **Is the log shipped to SIEM/analysis?** (CloudWatch, S3 export, third-party)
3. **Is there an active detection rule?** (GuardDuty finding type, SecurityHub rule, custom EventBridge rule)
4. **What is the detection latency?** (Real-time, minutes, hours, days, never)

### Chain Detection Classification
| Classification | Criteria | Priority Adjustment |
|---|---|---|
| **Invisible** | No step in the chain generates a monitored alert | Elevate by one severity level |
| **Late Detection** | Objective step is detected but pivots are not | Note: attacker achieves goal before response |
| **Partially Visible** | Some steps detected, gaps in middle | Note which steps are blind spots |
| **Well-Monitored** | All steps logged with active alerting | No adjustment (defense-in-depth working) |

### Critical Blind Spot Patterns
- CloudTrail disabled or limited to management events only → data exfiltration invisible
- GuardDuty not enabled → IAM anomaly detection absent
- No VPC Flow Logs → network lateral movement invisible
- Lambda invocations not logged → serverless chaining invisible
- S3 data events disabled → object-level access invisible
- No real-time alerting pipeline → all detection is forensic-only (post-breach)

---

## CONTEXTUAL REASONING

### Environment Context
- **Production chains are more severe** than dev/staging chains (even if technically identical)
- **Multi-environment chains** (dev → prod via shared trust) are especially dangerous
- **Blast radius amplification**: a single finding affecting a shared service (e.g., shared IAM role used by 10 Lambdas) multiplies the chain count

### Business Impact Context
- Correlate data store findings with likely data sensitivity (table names, bucket names suggesting PII/financial/health data)
- Weigh availability impact (stateless services recover fast; databases with no backup do not)
- Consider regulatory implications (healthcare, financial, PCI scope indicators in resource names/tags)

### Operational Reality
- Chains requiring >5 distinct steps are less likely to be exploited opportunistically (but APT-viable)
- Chains with fully automated steps (no human judgment required) are more dangerous than those requiring attacker decision-making
- Time-of-check vs. time-of-use: credentials that rotate frequently reduce chain viability

### Architecture Maturity Signals
- Presence of WAF, Config rules, Security Hub → suggests security-aware organization (raise bar for findings)
- Absence of basic controls (no CloudTrail, no GuardDuty, default VPC) → suggests low maturity (lower bar, more chains viable)
- Inconsistent controls (some envs secured, others not) → suggests gaps in process (focus on the gaps)

---

## CONFIDENCE SCORING

Every attack chain carries a `confidence` score from 0.0 to 1.0 indicating how certain the analysis is that the chain is exploitable end-to-end.

Chain confidence is derived from its weakest link: `chain_confidence = min(step_confidences[])`. A chain is only as certain as its least-certain step.

| Range | Label | Meaning |
|---|---|---|
| 0.9–1.0 | **confirmed** | Every step in the chain has confirmed evidence. All resource references resolved, all permissions verified, all network paths visible. |
| 0.7–0.89 | **high** | Most steps confirmed, one or two require minor inference (e.g. managed policy contents assumed, subnet type inferred). |
| 0.5–0.69 | **medium** | At least one step depends on unresolved cross-module reference or cross-account trust not fully visible. Chain is plausible but has gaps. |
| 0.3–0.49 | **low** | Multiple steps require inference. Chain structure is sound but evidence is thin — e.g. pivots depend on permissions in external IaC, network path crosses unanalyzed VPC peering. |
| 0.0–0.29 | **speculative** | Chain is theoretically possible but relies heavily on assumptions. Emitted only for Critical-impact chains worth human review. |

### Chain confidence modifiers

**Boosters (+):** same resource ARN/IaC address appears across multiple upstream skills (corroborated), detection overlay shows chain is invisible (no logging = higher confidence the chain would succeed undetected), all entry→pivot→objective steps use confirmed findings.

**Reducers (-):** pivot step crosses account boundary where remote IaC is not in scope, detection probability > 0.5 (chain might be caught before reaching objective), one or more upstream findings are low-confidence, chain requires runtime conditions not visible in IaC (e.g. specific instance metadata configuration).

## SEVERITY GUIDANCE

### Critical (Chain Score ≥ 0.8)
- Internet-accessible entry point with direct or 1-hop path to admin/data
- Invisible to all detection mechanisms
- Confirmed real credential with broad access
- Ransomware-viable path to production data stores

### High (Chain Score ≥ 0.6)
- Viable entry point with 2-3 step path to significant objective
- Partially detected (entry visible but pivots invisible)
- Cross-account compromise paths
- Production data accessible via credential harvest chain

### Medium (Chain Score ≥ 0.4)
- Entry point requires some preconditions (credential might be rotated, endpoint requires specific input)
- 3+ step chains with some detection coverage
- Non-production environments at risk
- Limited blast radius objectives

### Low (Chain Score < 0.4)
- Theoretical paths with multiple hard prerequisites
- Well-detected chains where alert response time < exploitation time
- Paths requiring physical access, social engineering, or supply chain compromise as entry
- Development/sandbox environment only impact

---

## FALSE POSITIVE REDUCTION

### Chains to EXCLUDE or downgrade:
- **Non-connectable steps**: two findings that affect the same resource but don't enable attacker progression
- **Already-mitigated chains**: a control exists that breaks the chain but wasn't detected by a single skill (e.g., WAF rule blocking the entry point)
- **Duplicate chains**: same fundamental path expressed with minor variations (group as one chain with variants noted)
- **Reversed causality**: finding B doesn't actually help reach finding C even though same resource is involved
- **Test/mock resources**: resources clearly named as test/example/demo (unless they have real credentials)

### Validation questions before emitting a chain:
1. Can the attacker actually reach step N+1 from step N? (Network path exists? IAM allows? Credential valid?)
2. Are the steps ordered correctly? (Must obtain privilege before using it)
3. Is there a control the individual skills missed that would break this chain?
4. Would a real attacker choose this path, or is there an easier alternative? (Note: still report, but adjust scoring)
5. Is the chain meaningfully different from another chain already reported?

---

## CORRELATION OPPORTUNITIES

### Cross-Skill Amplification Patterns
These patterns should be flagged to `iac-report` as the highest-priority findings:

| Pattern | Skills Involved | Signal |
|---|---|---|
| Exposed + Overprivileged | network + iam | Internet-reachable workload with unnecessary broad permissions |
| Exposed + Secrets in Memory | network/serverless + secrets | Reachable endpoint with harvestable credentials |
| Overprivileged + Unmonitored | iam + logging | Dangerous permissions with no detection coverage |
| Data Access + No Logging | iam/storage + logging | Can read sensitive data with no audit trail |
| Delete Permissions + No Backup | iam + storage | Ransomware preconditions met |
| Cross-Account + No ExternalId | iam + iam | Confused deputy attack viable |
| All: Entry + Pivot + Objective + No Detection | all skills | Complete invisible kill chain |

### Metadata for iac-report
Each chain should include:
- **Chain ID** — unique identifier for reference
- **Chain title** — human-readable summary (e.g., "Internet → Lambda → Admin via PassRole")
- **MITRE ATT&CK mapping** — relevant technique IDs
- **Component finding IDs** — references to source skill findings
- **Minimum-cut membership** — which fix set(s) this chain belongs to
- **Narrative** — 3-5 sentence description of how an attacker would execute this chain
- **Time-to-exploit estimate** — minutes/hours/days for a skilled attacker
- **Priority** — based on minimum-cut position

---

## CHAIN SCORING — DETAILED METHODOLOGY

### Composite Score Calculation

```
chain_score = entry_exploitability × pivot_complexity × objective_impact × (1 - detection_probability)
```

All factors are on [0.0, 1.0] scale. The multiplication ensures that a single strong defensive factor (high detection, hard pivots) appropriately reduces overall risk.

### Tie-Breaking Rules
When multiple chains have the same composite score:
1. Prefer shorter chains (fewer steps = more likely to be exploited)
2. Prefer chains with automated pivots (no human judgment required)
3. Prefer chains targeting production environments
4. Prefer chains with broader blast radius
5. Prefer chains involving sensitive data (PII, financial, credentials)

### Score Adjustment Factors
- **Invisible chain bonus**: if detection_probability < 0.1, multiply final score by 1.2 (cap at 1.0)
- **Multi-environment penalty**: if chain crosses from dev/staging to prod, add 0.1 to score (cap at 1.0)
- **Shared-resource multiplier**: if entry point or pivot serves multiple downstream chains, note as "systemic"
- **Temporal decay**: if a credential-based entry point references a key that might have been rotated, apply 0.7 multiplier

---

## MINIMUM-CUT ANALYSIS — DETAILED

### Algorithm Implementation

```
function minimum_cut(chains, findings):
    cut_set = []
    remaining_chains = chains.filter(c => c.severity in [Critical, High])
    
    while remaining_chains is not empty:
        # Score each finding by chains it would break
        for each finding F in all_findings:
            F.break_count = count(chains in remaining_chains that contain F)
            F.break_severity_sum = sum(severity_score(C) for C in remaining_chains if F in C)
            F.fix_value = F.break_count × F.break_severity_sum
        
        # Select highest-value finding
        best = finding with max fix_value
        cut_set.append(best)
        
        # Remove broken chains
        remaining_chains = remaining_chains.filter(c => best not in c)
    
    return cut_set
```

### Output Format
The minimum-cut output should present:
1. **Ordered fix list** — findings ranked by fix_value (highest first)
2. **Per-fix impact** — how many chains each fix breaks, which chains specifically
3. **Cumulative coverage** — running total of chains broken as fixes are applied
4. **Effort estimation** — rough complexity of implementing each fix (trivial/moderate/significant/architectural)
5. **Dependencies** — whether fixes must be applied in order or can be parallelized

### Interpretation Guidance for Defenders
- **1-3 item cut set**: excellent — clear chokepoints exist, focus effort there
- **4-7 item cut set**: moderate — some architectural issues but manageable
- **8+ item cut set**: systemic — architecture needs redesign, not just patching
- **Single finding in >50% of chains**: this is your #1 priority, likely a shared overprivileged role or missing segmentation

---

## CHAIN VALIDATION AND QUALITY GATES

Before emitting any chain, apply these validation gates:

### Gate 1 — Reachability Verification
For every step transition (N → N+1), verify one of:
- Network path exists (same VPC, peered VPC, public internet, VPC endpoint)
- IAM permission grants access (policy allows the required action on the target resource)
- Credential provides authentication (key/token/password grants access to next resource)

If no connection mechanism exists between two findings, they do NOT form a chain — even if both are severe and affect related resources.

### Gate 2 — Temporal Ordering
Each step must be achievable AFTER the previous step completes:
- Cannot use a role before assuming it
- Cannot read credentials before gaining access to where they're stored
- Cannot exploit a service before reaching it over the network

### Gate 3 — Privilege Monotonicity Check
Verify that each pivot step actually INCREASES attacker capability:
- Moving from one unprivileged workload to another unprivileged workload is lateral movement, not escalation
- Lateral movement is still reportable but contributes less to chain severity
- True escalation: each step grants access to something the previous step could not reach

### Gate 4 — Deduplication
Before emitting a chain, verify it is not a minor variant of an already-reported chain:
- Same entry point, same objective, slightly different pivot order → merge as one chain with "variant paths" noted
- Subset chains (A→B→C is a subset of A→B→C→D) → report only the longer chain unless the shorter chain has a different objective
- Symmetric chains (same path in reverse) → not valid (attacker must progress forward)

### Gate 5 — Real-World Plausibility
Apply red team judgment:
- Would a real attacker choose this path given simpler alternatives? (Still report, but note in narrative)
- Does the chain require unrealistic preconditions (e.g., SSRF in a function that doesn't process URLs)?
- Are timing constraints realistic (credentials that expire in 1 hour vs. chain requiring 4 hours)?

---

## REPORT STRUCTURE

The output file `iac-scan/attack-chain-results.md` follows this structure:

### Section 1 — Executive Summary
- Total chains by severity
- Top 3 most dangerous chains (one-sentence each)
- Minimum-cut summary (N fixes break M critical paths)
- Overall detection coverage assessment

### Section 2 — Minimum-Cut Analysis
- Ordered fix list by chain-breaking impact
- Cumulative coverage graph (textual)
- Sprint-sized groupings (what to fix this week, this month, this quarter)

### Section 3 — Critical Attack Chains (Full Detail)
- Complete narrative for each Critical-severity chain
- Step-by-step kill chain table
- Detection overlay per step
- MITRE ATT&CK mapping
- Specific risk description for this chain

### Section 4 — High Attack Chains (Summary + Detail)
- Brief narrative for each High-severity chain
- Key findings involved
- Impact notes

### Section 5 — Medium/Low Chains (Summary Table)
- Table format: Chain ID | Title | Score | Entry | Objective | Key Fix

### Section 6 — Detection Coverage Matrix
- Heatmap (text) of which chain steps are logged/alerted/invisible
- Recommendations for detection improvements

### Section 7 — Systemic Architecture Issues
- Findings that appear in >30% of chains
- Architectural recommendations (not just point fixes)

---

## MITRE ATT&CK MAPPING

Map each chain step to the relevant MITRE ATT&CK for Cloud technique:

| Chain Step Type | Common Techniques |
|---|---|
| Internet entry | T1190 (Exploit Public-Facing Application), T1133 (External Remote Services) |
| Credential entry | T1078.004 (Cloud Accounts), T1552.005 (Cloud Instance Metadata) |
| IAM escalation | T1548 (Abuse Elevation Control), T1098 (Account Manipulation) |
| Role assumption | T1550.001 (Application Access Token) |
| Credential harvest | T1552.001 (Credentials in Files), T1552.005 (Cloud Instance Metadata) |
| Lateral movement | T1021 (Remote Services), T1550 (Use Alternate Auth Material) |
| Data exfiltration | T1530 (Data from Cloud Storage), T1537 (Transfer to Cloud Account) |
| Persistence | T1098.001 (Additional Cloud Credentials), T1525 (Implant Container Image) |
| Defense evasion | T1562.008 (Disable Cloud Logs), T1070 (Indicator Removal) |

---

## OUTPUT FORMAT

> See examples/output-format.md

---

## EXAMPLE ATTACK CHAINS

> See examples/attack-chains.md

---

## EXAMPLE MINIMUM-CUT ANALYSIS

> See examples/minimum-cut.md

---

## EXAMPLE JSON OUTPUT

> See examples/json-output.md

---

## LIMITATIONS

### What This Skill Cannot Assess
- **Runtime behavior** — actual exploitation success depends on application logic, input validation, runtime protections not visible in IaC
- **Credential validity** — cannot confirm whether a leaked credential is still active
- **Data sensitivity** — infers from naming conventions and resource types, but cannot read actual data
- **Patch state** — IaC doesn't declare OS/application patch levels
- **Custom application security** — SQL injection, XSS, business logic flaws are out of scope
- **Timing and sequencing** — cannot determine if actions would trigger rate limiting or temporal controls

### Assumptions Made
- Findings from upstream skills are accurate (this skill does not re-validate)
- Network reachability follows AWS default behavior (stateful security groups, NACL evaluation order)
- IAM policy evaluation follows standard AWS logic (explicit deny > allow, resource/identity policy union)
- Attacker has AWS CLI expertise and knowledge of common escalation techniques
- Default VPC/service behavior unless IaC explicitly overrides

### Known Blind Spots
- Service-linked roles and their permissions (often not in IaC)
- AWS Organizations SCPs (may block chains that otherwise look viable)
- AWS Config rules that might detect findings automatically
- Third-party security tools (Datadog, Splunk, CrowdStrike) not visible in IaC
- Manual security procedures (break-glass processes, security team response)

---

## FUTURE IMPROVEMENTS

### Planned Enhancements
- **Probabilistic chain scoring** — Bayesian network modeling for more accurate exploitability assessment
- **Attack simulation** — generate Pacu/Stratus Red Team commands for each chain to enable validation
- **Time-series analysis** — reason about deployment order and temporal attack windows
- **Threat intelligence integration** — correlate with known APT group TTPs and active campaigns
- **Automated fix generation** (future `iac-remediate` skill) — emit IaC patches for each finding in the minimum-cut
- **Risk quantification** — monetary impact estimation based on data sensitivity and business context
- **Graph visualization** — emit DOT/Mermaid diagrams of attack chains for report embedding
- **SCP/permission boundary awareness** — ingest organization policies to prune infeasible chains
- **Multi-cloud support** — extend chain construction to Azure/GCP resources
- **MITRE ATT&CK Navigator layer export** — generate ATT&CK coverage heatmaps from chain analysis
