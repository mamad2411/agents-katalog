---
name: mcp-infra-scanner
description: "MCP Infrastructure Scanner — cloud resources, IaC configs, CIS benchmarks, compliance rules. Use when scanning infrastructure for misconfigurations or compliance gaps."
---

# MCP Infrastructure Scanner (MCP Infra Scanner)

## Overview

MCP Infra Scanner is a skill designed to scan cloud infrastructures (AWS, GCP, Azure), Infrastructure as Code (IaC) configurations, and system properties over the MCP protocol. It provides resource enumeration, configuration audits, CIS benchmark compliance verification, and vulnerability scanning. It ensures that infrastructure is continuously monitored for security, compliance, and architectural best practices.

**Core principle:** UNSCANNED INFRASTRUCTURE IS INSECURE — INFRASTRUCTURE CHANGES MUST ALWAYS BE AUDITED.

## The Iron Law

```
NO INFRASTRUCTURE CHANGE CAN BE DEPLOYED TO PRODUCTION WITHOUT UNDERGOING SCANNING AND VERIFICATION. EVERY IaC CHANGE MUST PASS AT LEAST ONE SECURITY AND COMPLIANCE AUDIT.
```

## When to Use

**Use this when:**
- You need to list all active resources and compile an inventory of a cloud provider (AWS/GCP/Azure).
- You need to audit IaC files (Terraform, CloudFormation, Pulumi) against best practices.
- You need to verify system configurations against CIS benchmarks.
- You need to evaluate the security impact of an infrastructure update.

**Use this ESPECIALLY when:**
- You assume "I just made a minor change, it should be fine" — this is exactly when scanning is most critical.
- You say "we are already secure, no need to scan again" — infrastructures change dynamically, requiring continuous validation.
- Preparing for a compliance audit and needing to verify overall infrastructure status.

**Don't skip when:**
- The infrastructure is still in the planning phase and has not been initialized.
- You lack access credentials to log into the cloud provider.
- The target environment (development/staging/production) is not specified.

## Phase 1: Cloud Provider Authentication and Authorization

**BEFORE proceeding:**

1. **Identify the authentication method** — AWS CLI profile, GCP service account, Azure Service Principal (SP).
2. **Define credential scope** — is ReadOnly access sufficient for the scan?
3. **Configure target accounts** — list the AWS accounts, GCP projects, or Azure subscriptions to audit.
4. **Test access credentials** — verify that the keys are valid and have the permissions required to pull configurations.

```
mcp-infra-scanner auth aws --profile security-audit --regions us-east-1,us-west-2,eu-west-1
mcp-infra-scanner auth gcp --service-account sa@project.iam.gserviceaccount.com --project production-project
mcp-infra-scanner auth azure --subscription prod-sub --tenant example.onmicrosoft.com
mcp-infra-scanner auth test --provider aws
```

## Phase 2: Cloud Resource Inventory Enumeration

**BEFORE proceeding:**

1. **Define target resource types** — EC2, S3, RDS, Lambda, IAM, VPC, Security Groups, etc.
2. **Execute service-by-service scans** — query and catalog resources for each API.
3. **Categorize the inventory** — group by compute, storage, networking, security, databases, or serverless.
4. **Export results** — output the inventory in JSON or CSV format.

```
mcp-infra-scanner inventory list --provider aws --service ec2,s3,iam,rds
mcp-infra-scanner inventory list --provider gcp --service compute,storage,iam
mcp-infra-scanner inventory export --format json --output /tmp/inventory.json
```

## Phase 3: IaC Configuration Scanning

**BEFORE proceeding:**

1. **Locate IaC configuration files** — find Terraform (.tf), CloudFormation (.yaml/.json), or Pulumi project directories.
2. **Run static analysis** on the files to check for security vulnerabilities.
3. **Audit results** — scan for open S3 buckets, unencrypted databases, or public security groups.
4. **Evaluate findings** — categorize issues by severity (Critical, High, Medium, Low).

```
mcp-infra-scanner iac scan --path /path/to/terraform --format terraform
mcp-infra-scanner iac scan --path /path/to/cloudformation --format cloudformation
mcp-infra-scanner iac findings --scan-id scan-456 --severity critical,high
```

## Phase 4: CIS Benchmark Compliance Audits

**BEFORE proceeding:**

1. **Select the target CIS benchmark version** (e.g., CIS AWS Foundations, CIS GCP Foundations, CIS Azure Foundations).
2. **Review the controls** — differentiate between automated rules and manual audit steps.
3. **Trigger automated checks** — execute the CIS check suite via the MCP provider.
4. **Calculate compliance scores** — generate a report detailing passed, failed, and out-of-scope controls.

```
mcp-infra-scanner compliance cis --benchmark "CIS AWS Foundations Benchmark v3.0.0"
mcp-infra-scanner compliance run --benchmark-id cis-aws-v3
mcp-infra-scanner compliance report --benchmark-id cis-aws-v3
```

## Phase 5: Security and Configuration Scans

**BEFORE proceeding:**

1. **Configure the security scan scope** — select target resource groups or tags.
2. **Run network security checks** — scan for exposed ports, public egress interfaces, and VPC peering issues.
3. **Verify encryption settings** — ensure encryption at rest and encryption in transit are configured with active KMS keys.
4. **Verify logging and monitoring setups** — ensure services like CloudTrail, VPC Flow Logs, and GuardDuty are enabled.

```
mcp-infra-scanner security scan --provider aws --services ec2,s3,iam
mcp-infra-scanner security network --check-public-instances
mcp-infra-scanner security encryption --check-at-rest --check-in-transit
mcp-infra-scanner security logging --check-cloudtrail --check-guardduty
```

## Phase 6: Final Verification

Before marking complete:

- [ ] Have all cloud accounts been successfully accessed and audited?
- [ ] Is the resource inventory complete?
- [ ] Has the IaC configuration static scan completed, with findings exported?
- [ ] Are CIS benchmark checks complete, yielding a compliance score?
- [ ] Are all security configuration findings categorized by severity?
- [ ] Are the final scan reports formatted and saved?
- [ ] Have plain-text credentials and API tokens been completely scrubbed from outputs?

## Red Flags — STOP and Follow Process

If you catch yourself thinking:
- "I only modified a single parameter; running a full configuration scan is unnecessary."
- "I can write the API keys directly in the command argument, nobody will audit it."
- "The CIS benchmark warnings are too strict; I will ignore them."
- "IaC static analysis takes too long; I'll perform a manual review instead."
- "Scanning all regions takes too much time; I'll scan only one region."

**ALL OF THESE MEAN: STOP. Return to the relevant phase.**

## Your Human Partner's Signals You're Doing It Wrong

**Watch for these redirections:**
- "Why didn't you scan this resource group?" — You omitted services or regions from your scan configurations.
- "Where did these credentials leak from?" — You exposed secrets in log files or reports.
- "Why is our CIS compliance score so low?" — You skipped checks or applied incorrect benchmark versions.
- "Is this finding actually critical?" — You misclassified vulnerability severities.
- "Why wasn't this IaC misconfiguration caught?" — You skipped the static scanning phase.

**When you see these:** STOP. Return to the relevant phase.

## Common Rationalizations

| Excuse | Reality |
|--------|---------|
| "It's just a minor change, a full scan is overkill." | A single line-change in a security group can expose the entire infrastructure. Scans are mandatory. |
| "I'll write the password in the CLI statement just this once." | CLI history logs are stored persistently, leading to credential leaks. Use environment variables. |
| "CIS rules are too theoretical to apply to our startup." | Compliance frameworks provide basic baselines that protect against common infrastructure attacks. |
| "Manual checks are faster than running static scanners." | Humans miss subtle misconfigurations that automated linters catch instantly. |
| "We don't use other regions, so scanning them is a waste of time." | Attackers spin up resources in unused regions to evade detection. Scan all regions. |

## Related Skills

- **mcp-server-hub** — Integrate scanning tools (e.g., Nmap, Nuclei) to verify infrastructure findings.
- **mcp-db-connector** — Check database configurations during infrastructure audits.
- **mitre-attack-mapper** — Map infrastructure findings to MITRE ATT&CK techniques.

## Self-Review

After completing this process:

1. **Scope Verification:** Have all cloud providers, accounts, regions, and services been scanned?
2. **IaC Coverage:** Are all Terraform, CloudFormation, or Pulumi files processed?
3. **CIS Accuracy:** Is the correct CIS Foundations benchmark version applied?
4. **Finding Quality:** Are severities classified accurately, excluding false positives?
5. **Log Cleanness:** Are plain-text tokens or keys removed from all output logs?
