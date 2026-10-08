---
name: cloud-lateral
description: |
  Activate this skill whenever the user mentions cloud lateral movement, cloud privilege escalation,
  cloud post-exploitation, cloud red team, multi-cloud attack, cloud pentesting,
  AWS, Amazon Web Services, EC2, S3, Lambda, IAM, STS, SSM, Systems Manager,
  CloudTrail, GuardDuty, CloudShell, Secrets Manager, Parameter Store, RDS,
  ECS, EKS, Fargate, ECR, CodeBuild, CodePipeline, Glue, SageMaker,
  instance profile, instance metadata, EC2 role, cross-account, assume role,
  Azure, Entra ID, Azure AD, managed identity, service principal, Azure Functions,
  Key Vault, Azure Storage, Cosmos DB, Azure Sentinel, Azure DevOps, AKS, ACR,
  Azure Automation, Logic Apps, Azure Resource Manager, ARM,
  GCP, Google Cloud, GKE, Cloud Functions, Cloud Run, Cloud Build,
  service account, Workload Identity, Secret Manager, Cloud SQL, BigQuery, Pub/Sub,
  IMDS, metadata service, 169.254.169.254, metadata.google.internal,
  cloud enumeration, cloud credential theft, cloud persistence,
  container escape, Kubernetes escape, pod-to-node, container breakout,
  serverless exploitation, Lambda injection, function event injection,
  S3 bucket enumeration, blob storage, GCS bucket, storage exfiltration,
  cloud persistence, backdoor IAM, cross-account trust, cloud backdoor,
  pacu, ScoutSuite, prowler, enumerate-iam, cloudfox, Stratus Red Team,
  SSRF to cloud, cloud SSRF, metadata SSRF, credential harvesting cloud,
  CloudTrail evasion, GuardDuty bypass, cloud stealth, cloud OPSEC,
  terraform state, cloud credentials file, .aws/credentials, gcloud auth,
  cloud-init, user-data secrets, startup script credentials.
version: 2.0.0
---

# Cloud Lateral Movement

Cloud environments expose a fundamentally different attack surface from traditional networks. Identity IS the network -- IAM policies, service accounts, and managed identities replace firewalls and VLANs. A single misconfigured permission can grant access to every resource in an organization. This skill covers the full cloud attack lifecycle across AWS, Azure, and GCP for authorized penetration testing.

## Attack Lifecycle

Follow this sequence. Each phase feeds the next -- credential harvesting enables escalation, escalation enables lateral movement, lateral movement discovers new targets.

```
Initial Access --> Credential Harvesting --> Permission Enumeration --> Privilege Escalation
     |                                                                        |
     v                                                                        v
Data Exfiltration <-- Persistence <-- Lateral Movement <-- Service Abuse
```

### Phase 1 -- Initial Access and Cloud Fingerprinting

Before attacking, determine the cloud provider, account structure, and available attack surface.

**Cloud provider indicators**:
- **AWS**: `amazonaws.com` domains, `X-Amz-*` headers, `arn:aws:` patterns, `.aws/credentials`, `169.254.169.254` IMDS
- **Azure**: `azure.com`/`windows.net`/`core.windows.net` domains, `X-Ms-*` headers, Entra ID endpoints, `169.254.169.254` with `Metadata: true`
- **GCP**: `googleapis.com` domains, `metadata.google.internal`, service account JSON files, `X-Goog-*` headers

Log detected cloud info immediately:
```bash
node "${CLAUDE_PLUGIN_ROOT}/scripts/target-intel.js" add "<target>" "tech-stack" "cloud-provider" "<aws|azure|gcp>" --source scan
node "${CLAUDE_PLUGIN_ROOT}/scripts/target-intel.js" add "<target>" "tech-stack" "cloud-account-id" "<account/subscription/project>" --source scan
```

Common initial access vectors:
1. SSRF to metadata service (most common cloud-specific vector)
2. Exposed credentials in repos, environment variables, CI/CD pipelines
3. Misconfigured storage buckets (public S3/Blob/GCS)
4. Compromised web application running on cloud compute
5. Leaked AWS keys in GitHub, terraform state, Docker images
6. Cloud-init / user-data containing plaintext secrets

### Phase 2 -- Credential Harvesting

The metadata service is the primary credential source from a compromised cloud instance.

**See**: `references/imds-exploitation.md` for full IMDS attack techniques, SSRF payloads, IMDSv2 bypass, and container credential endpoints.

Quick credential checks:
```bash
# AWS -- IMDSv1
curl -s http://169.254.169.254/latest/meta-data/iam/security-credentials/

# AWS -- IMDSv2
TOKEN=$(curl -s -X PUT "http://169.254.169.254/latest/api/token" -H "X-aws-ec2-metadata-token-ttl-seconds: 21600")
curl -s -H "X-aws-ec2-metadata-token: $TOKEN" http://169.254.169.254/latest/meta-data/iam/security-credentials/

# Azure -- Managed Identity token
curl -s -H "Metadata: true" "http://169.254.169.254/metadata/identity/oauth2/token?api-version=2018-02-01&resource=https://management.azure.com/"

# GCP -- Service account token
curl -s -H "Metadata-Flavor: Google" "http://metadata.google.internal/computeMetadata/v1/instance/service-accounts/default/token"
```

SSRF to IMDS is a critical finding -- log immediately:
```bash
node "${CLAUDE_PLUGIN_ROOT}/scripts/findings-tracker.js" add "<endpoint>" "ssrf" "<param>" "CRITICAL" "SSRF to cloud metadata service -- credential theft confirmed"
node "${CLAUDE_PLUGIN_ROOT}/scripts/techniques-tracker.js" add "curl" "<target>" "imds-credential-harvest" "success" --notes "Extracted <aws|azure|gcp> credentials via IMDS"
```

Other credential sources:
- Environment variables (`AWS_ACCESS_KEY_ID`, `AZURE_CLIENT_SECRET`, `GOOGLE_APPLICATION_CREDENTIALS`)
- Config files (`.aws/credentials`, `~/.azure/`, `~/.config/gcloud/`)
- Terraform state files (`terraform.tfstate` -- contains plaintext secrets)
- CI/CD pipelines (GitHub Actions secrets, GitLab CI variables)
- Container orchestrator secrets (Kubernetes secrets, ECS task definitions)
- Cloud-init / user-data scripts

### Phase 3 -- Permission Enumeration

With credentials in hand, map what you can do before attempting escalation.

**Automated enumeration tools**:
```bash
# AWS -- enumerate-iam (brute-force permission discovery)
python3 enumerate-iam.py --access-key <key> --secret-key <secret> --session-token <token>

# AWS -- pacu (comprehensive AWS exploitation framework)
pacu
# > import_keys <profile>
# > run iam__enum_permissions
# > run iam__enum_users_roles_policies_groups

# Multi-cloud -- ScoutSuite (audit and enumeration)
scout aws --profile <profile>
scout azure --cli
scout gcp --service-account <key.json>

# AWS -- cloudfox (cloud pentesting)
cloudfox aws --profile <profile> all-checks

# AWS -- prowler (security assessment)
prowler aws -p <profile> -M csv
```

Manual identity checks:
```bash
# AWS
aws sts get-caller-identity
aws iam list-attached-user-policies --user-name <user>
aws iam list-attached-role-policies --role-name <role>

# Azure
az account show
az role assignment list --assignee <object-id> --all
az ad signed-in-user show

# GCP
gcloud auth list
gcloud projects get-iam-policy <project-id> --flatten="bindings[].members" --filter="bindings.members:<identity>"
```

Log enumeration results:
```bash
node "${CLAUDE_PLUGIN_ROOT}/scripts/techniques-tracker.js" add "enumerate-iam" "<target>" "iam-enumeration" "<result>" --notes "Discovered <N> permissions on <identity>"
node "${CLAUDE_PLUGIN_ROOT}/scripts/target-intel.js" add "<target>" "credential" "<role/user>" "<permission-summary>" --source scan
```

### Phase 4 -- Privilege Escalation

Cloud IAM privilege escalation is the most impactful phase. A single over-permissioned policy can escalate to full account takeover.

**See**: `references/iam-escalation.md` for 21+ AWS paths, Azure Entra ID techniques, GCP IAM abuse, and cross-account escalation.

Priority escalation checks (AWS):
1. `iam:CreatePolicyVersion` -- write yourself admin
2. `iam:AttachUserPolicy` / `iam:AttachRolePolicy` -- attach AdministratorAccess
3. `iam:PassRole` + `lambda:CreateFunction` -- create admin Lambda
4. `sts:AssumeRole` -- pivot to more powerful roles
5. `ec2:RunInstances` + instance profile -- launch instance with target role

Priority escalation checks (Azure):
1. User Access Administrator -- assign Owner to yourself
2. Application Admin -- add credentials to service principals
3. Automation Account Contributor -- create runbooks with managed identity
4. Key Vault access policy modification

Priority escalation checks (GCP):
1. `iam.serviceAccounts.getAccessToken` -- impersonate service accounts
2. `iam.serviceAccountKeys.create` -- create persistent SA keys
3. `cloudfunctions.functions.create` + `iam.serviceAccounts.actAs` -- serverless escalation
4. `resourcemanager.projects.setIamPolicy` -- grant yourself Owner

Log all escalation paths:
```bash
node "${CLAUDE_PLUGIN_ROOT}/scripts/findings-tracker.js" add "<service>" "iam-escalation" "<permission>" "CRITICAL" "Cloud privilege escalation via <technique>"
node "${CLAUDE_PLUGIN_ROOT}/scripts/techniques-tracker.js" add "<tool>" "<target>" "iam-privesc" "success" --notes "Escalated from <role> to <role> via <method>"
```

### Phase 5 -- Service Abuse and Lateral Movement

With escalated permissions, abuse cloud services to move laterally across the environment.

**See**: `references/cloud-service-abuse.md` for SSM, Lambda, S3, Key Vault, Secrets Manager, and cross-service pivoting.

Key lateral movement vectors:
- **AWS**: SSM command execution on instances, Lambda function backdooring, cross-account role assumption, VPC peering pivots, Transit Gateway access, ECS/EKS cluster access
- **Azure**: Azure Automation runbooks, Logic Apps with managed identity, Azure DevOps pipeline injection, AKS cluster access, Cosmos DB cross-region access
- **GCP**: Cloud Build with elevated SA, Compute Engine SSH via IAP, GKE cluster access, Cloud Functions chaining, Shared VPC pivots

### Phase 6 -- Container and Serverless Attacks

Modern cloud environments heavily use containers and serverless. These introduce unique attack paths.

**See**: `references/container-escape.md` for Docker/K8s breakout, pod-to-node escalation, and registry abuse.
**See**: `references/serverless-attacks.md` for Lambda/Functions exploitation, event injection, and runtime manipulation.

### Phase 7 -- Persistence

Establish durable access that survives credential rotation and incident response.

**See**: `references/cloud-persistence.md` for backdoor IAM roles, Lambda triggers, cross-account trust abuse, and stealth persistence mechanisms.

### Phase 8 -- Data Exfiltration

Extract target data while minimizing detection.

**See**: `references/storage-exfil.md` for S3/Blob/GCS bucket enumeration, permission misconfiguration discovery, and data exfiltration techniques.

### Phase 9 -- Log and Report

Record all findings, techniques, and intelligence gathered during cloud testing.

```bash
# Log cloud-specific findings
node "${CLAUDE_PLUGIN_ROOT}/scripts/findings-tracker.js" add "<service>" "<vuln-type>" "<detail>" "<severity>" "<description>"

# Log techniques used
node "${CLAUDE_PLUGIN_ROOT}/scripts/techniques-tracker.js" add "<tool>" "<target>" "<technique>" "<result>" --notes "<details>"

# Log target intelligence
node "${CLAUDE_PLUGIN_ROOT}/scripts/target-intel.js" add "<target>" "<category>" "<key>" "<value>" --source scan

# Check for exploit chains
node "${CLAUDE_PLUGIN_ROOT}/scripts/chain-detector.js"
```

## Cloud OPSEC

Cloud environments have extensive logging. Adjust behavior based on scan profile.

```bash
# Check current profile
node "${CLAUDE_PLUGIN_ROOT}/scripts/scan-profile.js" get
```

### Detection Sources by Provider

| Provider | Logging | Threat Detection | SIEM |
|----------|---------|-----------------|------|
| AWS | CloudTrail, VPC Flow Logs, S3 Access Logs | GuardDuty, Security Hub, Detective | CloudWatch, Athena |
| Azure | Activity Log, Diagnostic Logs, NSG Flow Logs | Microsoft Defender, Sentinel | Log Analytics, Sentinel |
| GCP | Cloud Audit Logs, VPC Flow Logs, Access Transparency | Security Command Center, Chronicle | Cloud Logging, BigQuery |

### Profile-Specific Guidance

**loud** -- Lab/CTF only. No OPSEC constraints. Run all enumeration tools freely.

**normal** -- Authorized external testing. Avoid:
- Mass IAM enumeration (triggers GuardDuty `Recon:IAMUser`)
- Rapid API calls across many services (anomaly detection)
- Using known-bad user agents (`pacu`, `ScoutSuite` default UAs)

**stealth** -- Add delays between API calls. Avoid:
- CloudTrail-logged IAM write operations without prior approval
- Cross-region enumeration (triggers geographic anomaly alerts)
- Service enumeration from IP ranges not associated with the target
- Modify tool user agents to blend with legitimate SDK traffic

**paranoid** -- Red team. Minimize all cloud API calls. Prefer:
- Read-only operations where possible
- Use stolen session tokens (not long-term keys) to blend with legitimate traffic
- Route through target's expected IP ranges if possible
- Avoid `sts:GetCallerIdentity` from new IPs (triggers anomaly)
- Stagger operations across sessions to avoid temporal correlation

### High-Risk API Calls (Detection Triggers)

**AWS** -- These generate GuardDuty/CloudTrail alerts in mature environments:
- `CreatePolicyVersion`, `AttachUserPolicy`, `PutUserPolicy` (IAM modification)
- `CreateAccessKey`, `CreateLoginProfile` (credential creation)
- `GetSecretValue`, `GetParametersByPath` (secrets access)
- `RunInstances` with high-privilege instance profile
- Any call from Tor exit nodes or known cloud pentesting IPs

**Azure** -- Microsoft Defender / Sentinel detections:
- Role assignment changes, service principal credential resets
- Key Vault access from new IPs
- Bulk Azure AD enumeration (user/group listing)
- Cross-tenant access attempts

**GCP** -- Security Command Center / Chronicle detections:
- Service account key creation
- IAM policy modifications at organization level
- Data export operations (BigQuery export, Cloud SQL export)
- Anomalous API usage patterns

## Tool Integration

Use Hexstrike MCP tools where available:
- `http_repeater` -- SSRF to metadata endpoints, token requests
- `http_intruder` -- bucket enumeration, API endpoint discovery
- Bash for CLI tools (aws, az, gcloud, pacu, ScoutSuite, cloudfox, prowler)

Always check scan profile before aggressive enumeration:
```bash
node "${CLAUDE_PLUGIN_ROOT}/scripts/scan-profile.js" get
```

## Tool Reference

| Tool | Install | Best For |
|------|---------|----------|
| `pacu` | `pip3 install pacu` | AWS exploitation framework -- 100+ modules for enumeration, escalation, exfiltration |
| `ScoutSuite` | `pip3 install scoutsuite` | Multi-cloud security auditing -- AWS, Azure, GCP, Alibaba, Oracle |
| `prowler` | `pip3 install prowler` | AWS/Azure/GCP security assessment -- CIS benchmarks, compliance checks |
| `cloudfox` | Go binary | AWS/Azure/GCP attack surface enumeration -- find exploitable misconfigs |
| `enumerate-iam` | Python script | AWS permission brute-force -- discover allowed API calls without IAM read access |
| `Stratus Red Team` | Go binary | Cloud attack simulation -- MITRE ATT&CK mapped techniques for AWS/Azure/GCP |
| `aws cli` | `apt install awscli` | AWS API interaction -- all service operations |
| `az cli` | Microsoft install script | Azure API interaction -- all service operations |
| `gcloud` | Google Cloud SDK | GCP API interaction -- all service operations |
| `kubectl` | `apt install kubectl` | Kubernetes cluster interaction -- pod/node/secret enumeration |
| `trivy` | Aqua Security | Container/IaC vulnerability scanning |

## Chaining Paths

Common multi-step attack chains in cloud environments:

1. **SSRF -> IMDS -> IAM creds -> S3 exfil**: Web app SSRF reads metadata credentials, enumerate S3, download sensitive data
2. **Exposed keys -> IAM enum -> privesc -> cross-account**: Leaked credentials, enumerate permissions, escalate, pivot accounts
3. **Container escape -> node creds -> cluster admin -> secrets**: Break out of container, access node IMDS, escalate to cluster admin, dump all secrets
4. **Lambda env vars -> DB creds -> RDS access -> data exfil**: Read Lambda configuration, extract database credentials, connect and exfiltrate
5. **CI/CD secrets -> cloud creds -> terraform state -> full access**: Pipeline secrets contain cloud keys, terraform state has all resource details
6. **Storage misconfig -> config files -> more creds -> deeper access**: Public bucket has config files with additional credentials

## References

| Reference | Coverage |
|-----------|----------|
| `references/imds-exploitation.md` | IMDSv1/v2 techniques, SSRF payloads, Azure/GCP metadata, container credential endpoints, EKS/ECS/Lambda creds, DNS rebinding |
| `references/iam-escalation.md` | 21+ AWS privesc paths, Azure Entra ID escalation, GCP IAM abuse, cross-account pivoting, automated escalation with pacu |
| `references/cloud-service-abuse.md` | S3/Blob/GCS abuse, SSM command execution, Lambda backdooring, Secrets Manager, Key Vault, Cloud SQL, cross-service pivoting |
| `references/container-escape.md` | Docker breakout, K8s pod-to-node escalation, privileged containers, container registry abuse, EKS/AKS/GKE specific attacks |
| `references/serverless-attacks.md` | Lambda/Functions/Cloud Functions exploitation, event injection, environment manipulation, cold start abuse, runtime layer attacks |
| `references/storage-exfil.md` | S3/Blob/GCS enumeration, permission misconfig discovery, data staging, exfiltration channels, detection-aware transfer |
| `references/cloud-persistence.md` | Backdoor IAM roles/users, Lambda triggers, cross-account trust, stealth persistence, surviving credential rotation |
