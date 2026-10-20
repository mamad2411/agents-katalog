---
name: aws-security-hub-asff
description: >
  AWS Security Hub findings in AWS Security Finding Format (ASFF): schema fields,
  BatchImportFindings, custom product integrations, severity/normalization, workflow
  status, and automation rules. Use when publishing or consuming Security Hub findings,
  building custom security products, or routing ASFF to SIEM/ticketing — not for
  generic SIEM design alone or unauthorized account access.
---

# AWS Security Hub ASFF

## Scope And Authorization

- **In scope:** Security Hub and custom finding providers in AWS accounts/orgs you own or administer.
- **Out of scope:** Injecting findings into accounts without authorization; using ASFF to spam or obscure real incidents.
- Findings may contain resource ARNs and account structure — protect exports.
- Pair integration code with `code-quality-standards`.

## When To Use

- Enabling Security Hub standards and understanding finding shape.
- Building a custom product that calls `BatchImportFindings` / `BatchUpdateFindings`.
- Mapping GuardDuty/Inspector/Macie/partner findings via ASFF.
- Automating triage (suppress, note, severity update) with EventBridge + Lambda.
- Normalizing third-party scanner output into ASFF for a single pane of glass.

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| Fixing the underlying S3/SG/IAM issue | Domain skill (e.g. `aws-s3-bucket-hardening`, `aws-security-groups-review`) |
| Org SCPs | `aws-scps-organization` |
| WAF bot mitigation | `aws-waf-bot-control` |
| Implementation quality baseline | `code-quality-standards` |

## Domain Focus

| ASFF area | Notes |
| --- | --- |
| Identity | `SchemaVersion`, `Id`, `ProductArn`, `GeneratorId`, `AwsAccountId` |
| What | `Types`, `Title`, `Description`, `Severity` (`Product`/`Normalized`/`Label`) |
| Where | `Resources[]` with `Type`, `Id`, `Region`, `Details` |
| State | `RecordState`, `Workflow.Status` (NEW/NOTIFIED/RESOLVED/SUPPRESSED) |
| Compliance | `Compliance.Status` for standard controls |
| Tooling | Security Hub API, EventBridge `Security Hub Findings - Imported`, custom actions |

## Workflow

### 1. Confirm scope and success criteria

1. Hub account (admin) vs member accounts; regions; products to integrate.
2. Success: findings import without validation errors; appear in console/filters; updates change workflow status.
3. Define ownership of suppression vs remediation.

### 2. Inventory Security Hub and products

```bash
aws sts get-caller-identity
aws securityhub describe-hub
aws securityhub get-enabled-standards
aws securityhub list-enabled-products-for-import
aws securityhub get-findings --max-results 5
```

1. Note administrator account and member linkage for Organizations.
2. Identify existing custom product ARNs.

### 3. Baseline sample findings

1. Export a few native findings to learn required fields.
2. Document filters used by SOC (severity ≥ HIGH, `RecordState=ACTIVE`, not SUPPRESSED).
3. Align finding `Types` namespace with org taxonomy (e.g. `Software and Configuration Checks/...`).

### 4. Produce or update ASFF

**Minimal custom finding sketch (validate against current AWS docs for required fields):**

```json
{
  "SchemaVersion": "2018-10-08",
  "Id": "custom/my-scanner/account/region/finding-001",
  "ProductArn": "arn:aws:securityhub:region:account:product/account/default",
  "GeneratorId": "my-scanner/policy-x",
  "AwsAccountId": "123456789012",
  "Types": ["Software and Configuration Checks/Industry and Regulatory Standards"],
  "CreatedAt": "2026-07-01T12:00:00.000Z",
  "UpdatedAt": "2026-07-01T12:00:00.000Z",
  "Severity": { "Label": "HIGH", "Product": 80 },
  "Title": "S3 bucket missing default encryption",
  "Description": "Bucket example-app-prod has no ServerSideEncryptionConfiguration.",
  "Resources": [{
    "Type": "AwsS3Bucket",
    "Id": "arn:aws:s3:::example-app-prod",
    "Region": "us-east-1"
  }],
  "RecordState": "ACTIVE",
  "Workflow": { "Status": "NEW" }
}
```

```bash
aws securityhub batch-import-findings --findings file://finding.json
aws securityhub batch-update-findings \
  --finding-identifiers Id=custom/my-scanner/...,ProductArn=arn:aws:securityhub:... \
  --workflow Status=NOTIFIED \
  --note Text="Ticket INC-123 assigned",UpdatedBy="soc-bot"
```

1. Use stable `Id` values so re-import updates rather than duplicates.
2. Set `UpdatedAt` on every change; respect throttle limits on batch APIs.
3. For automation rules: match on product/title/severity → suppress known false positives with expiry notes.

### 5. Verify with evidence

```bash
aws securityhub get-findings --filters '{
  "Id":[{"Value":"custom/my-scanner/account/region/finding-001","Comparison":"EQUALS"}]
}'
aws securityhub get-findings --filters '{
  "SeverityLabel":[{"Value":"CRITICAL","Comparison":"EQUALS"}],
  "WorkflowStatus":[{"Value":"NEW","Comparison":"EQUALS"}]
}'
```

1. Confirm EventBridge rule fires on import for ticketing pipeline.
2. Resolve underlying issue and show finding moves to RESOLVED or `RecordState=ARCHIVED` as appropriate.
3. Rejected batch items: read `FailedCount` / error codes and fix schema.

### 6. Observe and harden

1. Metrics: import failures, open HIGH/CRITICAL age, mean time to NOTIFIED.
2. Guard product IAM: only the scanner role may `BatchImportFindings` for its product.
3. Redact secrets from `Description` / `Resources.Details` — ASFF is widely readable by security roles.

### 7. Hand off

1. Product onboarding doc: ProductArn, GeneratorId conventions, severity mapping.
2. SOC playbooks keyed by `GeneratorId` / ASFF `Types`.
3. Link remediation to resource-specific skills.

## Severity And Workflow

| Field | Guidance |
| --- | --- |
| `Severity.Label` | INFORMATIONAL / LOW / MEDIUM / HIGH / CRITICAL |
| Normalization | Prefer Labels; Product score for custom ranking |
| NEW | Untriaged |
| NOTIFIED | Ticket/IR engaged |
| SUPPRESSED | Accepted risk / false positive — require note + review date |
| RESOLVED | Fixed or no longer applicable |

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| IDs | Deterministic per resource+check | Random UUID every scan (duplicate flood) |
| Content | Actionable title + resource ARN | “Vulnerability detected” with no resource |
| Secrets | ARNs only | Passwords in Description |
| Suppressions | Ticketed expiry | Mass suppress CRITICAL forever |
| Integration | BatchUpdate for triage | Manual console-only at scale |

## Output Checklist

- [ ] Hub enabled; standards/products inventoried
- [ ] ASFF schema validated via successful import
- [ ] Stable finding IDs and GeneratorId convention documented
- [ ] Workflow update path tested
- [ ] EventBridge/SIEM routing verified if required
- [ ] IAM least privilege for import role
- [ ] Suppression policy defined
- [ ] Remediation owners mapped for top finding types
- [ ] `code-quality-standards` applied to integration code

## Rules

- Authorized Security Hub admins/products only.
- Do not hide real risk with untracked suppressions.
- Keep ASFF free of raw secrets and excessive PII.
- Prefer fixing the resource over perpetual NOTIFIED without owner.
- Route actual hardening work to the service-specific skill.
