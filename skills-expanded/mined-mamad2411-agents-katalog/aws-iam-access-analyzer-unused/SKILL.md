---
name: aws-iam-access-analyzer-unused
description: >
  IAM Access Analyzer unused access findings for owned AWS accounts: external
  access analyzers vs unused access analysis, last-used data, remediation of
  unused roles/permissions/access keys, and exception handling. Use when reducing
  standing IAM privilege based on analyzer evidence — not for enumerating third-party
  accounts without authorization.
---

# AWS IAM Access Analyzer Unused

## Scope And Authorization

- **In scope:** IAM Access Analyzer and IAM entities in accounts/orgs you own or assess with authorization.
- **Out of scope:** Using analyzer APIs against accounts without permission.
- Removing “unused” permissions can break quarterly jobs — validate last-used windows and business calendars.
- Prefer ticketed removals with rollback (policy version).
- Pair with `aws-iam-least-privilege` for redesign; `code-quality-standards` for automation.

## When To Use

- Enabling unused access analysis (account or organization).
- Removing unused IAM roles, users, access keys, and unused services/actions from policies.
- Differentiating external access findings from unused access findings.
- Building quarterly access reviews with analyzer exports.
- CI/automation that opens tickets for new unused findings.

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| Writing least-privilege policies from scratch | `aws-iam-least-privilege` |
| Policy simulator dry-runs | `aws-iam-policy-simulator` |
| External public/cross-account resource shares | Access Analyzer external access + `aws-ram-resource-share` |
| Secrets/key rotation hygiene | `secrets-management-hygiene` |
| Implementation quality baseline | `code-quality-standards` |

## Domain Focus

| Analyzer type | Purpose |
| --- | --- |
| External access | Who outside zone can access resources |
| Unused access | Roles/users/perms/keys not used in tracking period |
| Internal access (if available) | Zone of trust analysis variants per current features |

| Finding class (examples) | Remediation idea |
| --- | --- |
| Unused role | Delete or detach after owner confirm |
| Unused permission | Shrink policy statements |
| Unused access key | Disable → delete; prefer SSO/roles |
| Unused password | Disable console user |

## Workflow

### 1. Confirm scope and success criteria

1. Record account/OU scope, tracking period (e.g., 90/180 days), owners.
2. Success: analyzer active; critical unused keys disabled; policies reduced with no breakages; exceptions documented.
3. Agree freeze windows (year-end jobs may look “unused”).

### 2. Inventory analyzers and findings

```bash
aws accessanalyzer list-analyzers
aws accessanalyzer list-findings --analyzer-arn "$ANALYZER_ARN" --filter '{"status":{"eq":["ACTIVE"]}}'
# Unused access analyzers may use specific APIs:
aws accessanalyzer list-findings-v2 --analyzer-arn "$ANALYZER_ARN" 2>/dev/null || true
aws iam generate-service-last-accessed-details --arn "$ROLE_ARN"
aws iam get-service-last-accessed-details --job-id "$JOB"
```

1. Separate external vs unused analyzers.
2. Prioritize: access keys and admin-level unused roles first.
3. Export findings to CSV/Security Hub if integrated.

### 3. Baseline

1. Snapshot IAM policy versions and role trust policies before change.
2. Map each high-priority finding to an owner tag/email.
3. Note break-glass roles (may be intentionally rare-use — exception).

### 4. Remediate systematically

**Priority order**

1. Active unused **access keys** on users (disable 7 days → delete).
2. Unused **console users** with passwords.
3. Unused **roles** with admin policies.
4. **Permission trimming** using last-accessed services/actions.
5. External access findings (separate track).

**Trim policy process**

```bash
aws iam get-policy-version --policy-arn "$POLICY" --version-id vN
# Create new version without unused actions/resources
aws iam create-policy-version --policy-arn "$POLICY" --set-as-default \
  --policy-document file://policy-vnext.json
```

1. Prefer managed policy versions for rollback.
2. For inline policies, export then replace carefully.
3. Never delete break-glass without alternate path.

**Automation sketch**

- EventBridge on new findings → ticket with role ARN, last used, suggested diff.
- Human approval for production account role deletion.

### 5. Verify with evidence

```bash
aws iam get-role --role-name "$ROLE"
aws iam list-access-keys --user-name "$USER"
# Application canaries / integration tests after policy shrink
aws accessanalyzer get-finding --analyzer-arn "$ARN" --id "$FID"
```

1. Confirm finding resolves or moves to archived after remediation.
2. Watch CloudTrail AccessDenied spikes for 1–2 weeks.
3. Keep rollback policy version ID in ticket.

### 6. Observe and harden

1. Monthly review of new unused findings.
2. SSO permission sets over long-lived users/keys.
3. SCPs denying create access key for most OUs if org-ready.

### 7. Hand off

1. Access review calendar and RACI.
2. Exception register (role, reason, expiry).
3. Link least-privilege skill for rebuilds that need redesign not just trim.

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| Keys | disable then delete | leave AKIA unused forever |
| Roles | owner confirm + canary | mass delete on day 90 |
| Break-glass | documented exception | deleted as “unused” |
| Policies | versioned shrink | no rollback |
| Scope | org analyzer + owners | ignore member accounts |
| Evidence | last-accessed report | gut feel removals |

## Output Checklist

- [ ] Analyzer type/scope/period recorded
- [ ] Findings exported and prioritized
- [ ] Keys/users/roles remediated with owners
- [ ] Policy versions retained for rollback
- [ ] Canaries/AccessDenied monitoring after change
- [ ] Exceptions with expiry documented
- [ ] Recurring review scheduled
- [ ] `aws-iam-least-privilege` used when redesign needed
- [ ] `code-quality-standards` for automation

## Rules

- Authorized accounts only.
- Validate business calendars before deleting “unused” access.
- Prefer SSO roles over long-lived keys.
- Archive findings with rationale — do not silently ignore.
- Focus on unused access analysis; policy authoring and simulation in neighbor skills.
