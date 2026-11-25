---
name: aws-config-conformance-packs
description: >
  AWS Config conformance packs for owned accounts/organizations: packing managed and
  custom Config rules, remediations, deployment via console/CLI/CloudFormation, and
  compliance reporting. Use when enforcing CIS/FSBP-style controls as code — not for
  scanning AWS accounts outside authorization.
---

# AWS Config Conformance Packs

## Scope And Authorization

- **In scope:** AWS accounts/OUs where you may enable Config and deploy conformance packs under authorization.
- **Out of scope:** Enabling Config or packs in third-party accounts without agreement.
- Config and packs incur cost (Config recorder, rules evaluations, S3 delivery) — budget intentionally.
- Remediations can mutate resources — prefer non-auto-remediate until reviewed.
- Pair custom Lambda rules with `code-quality-standards` and `aws-lambda-least-privilege`.

## When To Use

- Deploying CIS AWS Foundations / AWS Foundational Security Best Practices style packs.
- Creating organization conformance packs from the management or delegated admin account.
- Adding custom rules (Guard/Lambda) into a pack template.
- Measuring compliance % and excluding resources with justification.
- Wiring results to Security Hub / dashboards.

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| Control Tower landing zone design | `aws-control-tower-notes` |
| IAM Access Analyzer unused access | `aws-iam-access-analyzer-unused` |
| Manual one-off Config rule only | still Config; pack optional |
| Incident response malware | `aws-guardduty-malware` |
| Implementation quality baseline | `code-quality-standards` |

## Domain Focus

| Concept | Detail |
| --- | --- |
| Conformance pack | Bundle of Config rules + optional remediation in a template |
| Sample packs | AWS-provided YAML templates (CIS, operational best practices) |
| Org packs | Deploy across accounts/OUs via Organizations |
| Compliance | Compliant / noncompliant / not applicable per resource |
| Exclusions | Documented exceptions with owner/expiry — not silent ignore forever |

## Workflow

### 1. Confirm scope and success criteria

1. Record accounts/OUs, Regions, recorder status, pack selection, remediation policy.
2. Success: pack deployed; rules evaluating; dashboard shows baseline; critical noncompliant owned.
3. Confirm Config is enabled with proper IAM service-linked role and delivery channel.

### 2. Inventory Config state

```bash
aws configservice describe-configuration-recorders
aws configservice describe-delivery-channels
aws configservice describe-conformance-pack-status
aws configservice describe-compliance-by-config-rule --query "ComplianceByConfigRules[?Compliance.ComplianceType=='NON_COMPLIANT']"
```

1. List existing rules that may duplicate pack rules.
2. Check organization delegated admin for Config if multi-account.
3. S3 bucket for Config history: encrypt, block public, restrict access.

### 3. Baseline

1. Snapshot current noncompliant counts before pack (cost/noise expectation).
2. Map critical rules to owners (S3, IAM, CloudTrail, VPC).
3. Decide Regions: recorder in all active Regions or org policy.

### 4. Deploy conformance packs

**Account-level (template from file):**

```bash
aws configservice put-conformance-pack \
  --conformance-pack-name OrgBaseline \
  --template-body file://conformance-pack.yaml \
  --delivery-s3-bucket "$CONFIG_BUCKET" \
  --delivery-s3-key-prefix packs/OrgBaseline/
```

**Organization-level (from management/delegated admin):**

```bash
aws configservice put-organization-conformance-pack \
  --organization-conformance-pack-name OrgBaseline \
  --template-body file://conformance-pack.yaml \
  --delivery-s3-bucket "$CONFIG_BUCKET"
```

**Template sketch (rules only):**

```yaml
Resources:
  S3BucketPublicReadProhibited:
    Type: AWS::Config::ConfigRule
    Properties:
      ConfigRuleName: s3-bucket-public-read-prohibited
      Source:
        Owner: AWS
        SourceIdentifier: S3_BUCKET_PUBLIC_READ_PROHIBITED
  IamPasswordPolicy:
    Type: AWS::Config::ConfigRule
    Properties:
      ConfigRuleName: iam-password-policy
      Source:
        Owner: AWS
        SourceIdentifier: IAM_PASSWORD_POLICY
```

1. Start **without** automatic remediation SSM docs until change board approves.
2. Customize parameters (required tags, desired AMI, SSL-only) per org standards.
3. Avoid deploying conflicting custom rules with same name.

### 5. Verify with evidence

```bash
aws configservice describe-conformance-pack-compliance --conformance-pack-name OrgBaseline
aws configservice get-compliance-details-by-config-rule --config-rule-name s3-bucket-public-read-prohibited --compliance-types NON_COMPLIANT
```

1. Sample a known-bad resource → noncompliant within evaluation window.
2. Sample a fixed resource → returns to compliant after re-evaluation.
3. Confirm org pack status across member accounts.

### 6. Observe and harden

1. Export compliance to S3/Athena or Security Hub for trends.
2. Ticket automation for new NON_COMPLIANT on critical rules.
3. Review exceptions quarterly; expire suppressions.
4. Cost monitor: Config item changes volume.

### 7. Hand off

1. Pack catalog, owners, remediation stance documented.
2. Runbook for adding a custom rule to the pack via PR.
3. Link Control Tower controls mapping if both used (avoid double noise).

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| Deploy | staged OU pilot | all accounts + auto-remediate day one |
| Remediation | manual/SSM with approval | silent delete/mutate |
| Exceptions | owner + expiry | infinite ignore |
| Recorder | all needed Regions | only us-east-1 while resources elsewhere |
| Templates | versioned in Git | one-off console clicks |
| Duplicates | consolidated rules | triple-evaluate same control |

## Output Checklist

- [ ] Accounts/OUs/Regions authorization recorded
- [ ] Config recorder + delivery channel healthy
- [ ] Pack template versioned and deployed
- [ ] Compliance status reviewed; owners assigned
- [ ] Remediation policy explicit (off/on)
- [ ] Exceptions ticketed with expiry
- [ ] Security Hub/reporting path considered
- [ ] Cost monitoring noted
- [ ] `code-quality-standards` applied for custom rules

## Rules

- Authorized accounts only; packs change compliance posture and potentially resources.
- Prefer detect-first; remediate with change control.
- Document exceptions; do not hide noncompliance permanently.
- Align with Control Tower/Security Hub to reduce alert fatigue.
- Focus on conformance packs; landing zone architecture in Control Tower skill.
