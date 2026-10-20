---
name: aws-organizations-tag-policies
description: >
  AWS Organizations tag policies for owned orgs: defining required tags, allowed
  values, enforcement vs report-only, OU attachment, and remediation of noncompliant
  resources. Use when standardizing cost allocation and ownership tags — not for
  modifying organizations you do not administer.
---

# AWS Organizations Tag Policies

## Scope And Authorization

- **In scope:** AWS Organizations tag policies in orgs you administer under authorization.
- **Out of scope:** Attaching policies to foreign organizations.
- Effective enforcement can block resource creation if tags invalid — pilot carefully.
- Tag values may contain sensitive owner names; treat policy exports as internal.
- Pair with Control Tower account tags and `code-quality-standards` for automation.

## When To Use

- Defining required tags: `Owner`, `CostCenter`, `Environment`, `DataClass`.
- Enforcing allowed values (e.g., Environment ∈ {dev,stage,prod}).
- Attaching tag policies to OUs (Workloads/Prod).
- Moving from report-only to enforceable.
- Integrating with SCPs that deny untagged resources (complementary).

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| Control Tower landing zone | `aws-control-tower-notes` |
| Config conformance packs | `aws-config-conformance-packs` |
| IAM least privilege | `aws-iam-least-privilege` |
| Resource sharing | `aws-ram-resource-share` |
| Implementation quality baseline | `code-quality-standards` |

## Domain Focus

| Concept | Detail |
| --- | --- |
| Tag policy | JSON document of tag keys and allowed operators/values |
| Inheritance | Policies merge down OU tree |
| Enforcement | `enforced_for` services list when supported |
| Compliance | Resource groups / console tag policies compliance |
| Limits | Not all services enforce equally — know gaps |

## Example Tag Policy Sketch

```json
{
  "tags": {
    "Environment": {
      "tag_key": { "@@assign": "Environment" },
      "tag_value": { "@@assign": ["dev", "stage", "prod"] },
      "enforced_for": { "@@assign": ["ec2:instance", "ec2:volume"] }
    },
    "Owner": {
      "tag_key": { "@@assign": "Owner" },
      "tag_value": { "@@assign": ["*@example.com"] }
    },
    "CostCenter": {
      "tag_key": { "@@assign": "CostCenter" },
      "tag_value": { "@@assign": ["CC-*"] }
    }
  }
}
```

Syntax operators (`@@assign`, etc.) follow Organizations tag policy language — validate against current docs.

## Workflow

### 1. Confirm scope and success criteria

1. Record org ID, OUs, required tag taxonomy, enforcement readiness.
2. Success: policy attached; compliance visible; new EC2 without tags blocked if enforced; owners fix existing drift.
3. Agree exception process for tools that cannot tag.

### 2. Inventory

```bash
aws organizations list-policies --filter TAG_POLICY
aws organizations list-targets-for-policy --policy-id "$PID"
aws organizations describe-policy --policy-id "$PID"
```

1. Existing SCPs related to tags.
2. Current tag usage sample via Resource Groups Tagging API.

```bash
aws resourcegroupstaggingapi get-tag-keys
aws resourcegroupstaggingapi get-resources --tag-filters Key=Environment
```

### 3. Baseline

1. Export all tag policies.
2. Measure % resources missing required keys in prod OU.
3. Communication plan to account owners.

### 4. Author and attach

1. Start **report-only** (no/limited `enforced_for`) in Sandbox OU.
2. Expand allowed values carefully (case sensitivity!).
3. Attach to NonProd → Prod OUs after cleanup.
4. Add enforcement service by service (`ec2:instance`, etc.).
5. Optionally complement with SCP: deny `ec2:RunInstances` without `aws:RequestTag/Environment`.

```bash
aws organizations create-policy \
  --content file://tag-policy.json \
  --description "Core ownership tags" \
  --name CoreTags \
  --type TAG_POLICY

aws organizations attach-policy --policy-id "$PID" --target-id "$OU_ID"
```

### 5. Verify with evidence

1. Create resource with invalid Environment → fail if enforced.
2. Create with valid tags → success.
3. Compliance report shows noncompliant legacy resources with owners.

### 6. Observe and harden

1. Monthly noncompliance report to account owners.
2. Automations: auto-tag from Account Factory defaults.
3. Review policy changes via CloudTrail Organizations APIs.

### 7. Hand off

1. Tag taxonomy wiki + examples.
2. IaC modules with required tags variables.
3. Exception register with expiry.

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| Rollout | report then enforce | enforce all services org-wide day one |
| Values | controlled enums | free text without validation |
| Ownership | Owner tag required | only CostCenter |
| IaC | modules enforce tags | console wild west |
| Exceptions | ticketed | permanent silent untagged prod |
| Case | documented casing | Env vs env drift |

## Output Checklist

- [ ] Taxonomy agreed and documented
- [ ] Policies created/versioned in Git
- [ ] Attached to correct OUs
- [ ] Pilot evidence for allow/deny
- [ ] Compliance report process running
- [ ] SCP complements considered
- [ ] IaC defaults updated
- [ ] Exceptions with expiry
- [ ] Org change monitoring

## Rules

- Administer only your organization.
- Pilot enforcement; tag policy blocks can halt delivery.
- Keep taxonomy small and meaningful.
- Combine with Account Factory defaults for new accounts.
- Focus on tag policies; broader CT/Config in neighbor skills.
