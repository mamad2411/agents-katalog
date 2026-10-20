---
name: azure-policy-initiatives
description: >
  Azure Policy initiatives (policy sets) for owned management groups and
  subscriptions: built-in vs custom policies, assignments, parameters, exemptions,
  compliance evaluation, and remediation tasks. Use when enforcing guardrails
  (locations, public access, TLS, tags) at scale — not for bypassing policy on
  unauthorized tenants.
---

# Azure Policy Initiatives

## Scope And Authorization

- **In scope:** Management groups, subscriptions, and policy objects you are authorized to administer.
- **Out of scope:** Assigning deny policies that sabotage workloads without change control; exemptions without expiry.
- Deny effects can block platform deployments — pilot on sandbox MG first.
- Pair Defender posture with `azure-defender-cloud`; use `code-quality-standards` for custom policy JSON.

## When To Use

- Packaging multiple policies into an initiative (CIS baseline, org security baseline).
- Assigning initiatives at MG for landing zones.
- Creating exemptions with justification and expiration.
- Remediating existing non-compliant resources with deployIfNotExists/modify.

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| Defender for Cloud plans | `azure-defender-cloud` |
| NSG rule design details | `azure-nsg-review` |
| Blob hardening steps | `azure-blob-misconfig` |
| Implementation quality baseline | `code-quality-standards` |

## Domain Focus

| Object | Role |
| --- | --- |
| Policy definition | Single rule (audit/deny/deployIfNotExists/modify/append) |
| Initiative | Group of definitions with shared parameters |
| Assignment | Scope + parameters + identity for remediation |
| Exemption | Time-bounded waiver |
| Compliance | Non-compliant resource inventory |
| Tooling | `az policy`, Portal, Guest Configuration, Epac/ALZ |

## Workflow

### 1. Confirm scope and success criteria

1. MG/sub scopes, required controls, enforcement mode (Default vs DoNotEnforce), authorization.
2. Success: initiative assigned; compliance visible; pilot resources blocked/remediated as designed.
3. Rollback: assignment deletion / DoNotEnforce for emergency.

### 2. Inventory policies and assignments

```bash
az account show
az policy definition list --query "[?policyType=='Custom'].name" -o tsv
az policy set-definition list -o table
az policy assignment list --disable-scope-strict-match -o table
az policy state summarize -o jsonc
```

1. Note inherited assignments from parent MGs.
2. List exemptions nearing expiry.
3. Identify conflicting allow/deny location policies.

### 3. Baseline controls to package

Example initiative contents:

| Control | Effect |
| --- | --- |
| Allowed locations | Deny |
| Storage public access disabled | Deny/Audit |
| Key Vault purge protection | Audit/Deny |
| Require TLS on storage | Deny |
| Require diagnostic settings | DeployIfNotExists |

### 4. Create/assign initiative

```bash
# Custom initiative from file
az policy set-definition create --name "org-security-baseline" \
  --definitions @initiative-rules.json \
  --params @initiative-params.json

az policy assignment create \
  --name "org-security-baseline-root" \
  --scope "/providers/Microsoft.Management/managementGroups/$MG" \
  --policy-set-definition "org-security-baseline" \
  --params @assignment-params.json \
  --mi-system-assigned \
  --location "$LOC"

# Enforcement soft-launch
az policy assignment create ... --enforcement-mode DoNotEnforce
# Later: switch to Default
```

1. Parameters: allowed locations list, required log workspace IDs.
2. Assign **managed identity** with enough rights for deployIfNotExists remediation.
3. Exemptions:

```bash
az policy exemption create --name "legacy-public-site" \
  --scope "$RESOURCE_ID" \
  --exemption-category Waiver \
  --expires-on "2026-12-31T00:00:00Z" \
  --policy-assignment "$ASSIGNMENT_ID"
```

### 5. Verify with evidence

```bash
az policy state list --policy-assignment "$ASSIGNMENT_ID" --filter "complianceState eq 'NonCompliant'" -o table
# Attempt forbidden deployment in pilot sub — expect deny
az storage account create ... # should fail if public access required false etc.
```

1. Compliance dashboard trends after 15–30+ minutes (evaluation latency).
2. Remediation task results for DINE policies.
3. Confirm exemptions show in compliance, not silent.

### 6. Observe and harden

1. Alert on new exemptions and assignment deletions.
2. Quarterly review of NonCompliant top resources.
3. Version initiatives; don’t edit in place without changelog.

### 7. Hand off

1. Initiative catalog with owner and parameter docs.
2. Exemption process (ticket template + max duration).
3. ALZ/EPAC pipeline for policy-as-code.

## Effects Cheatsheet

| Effect | Behavior |
| --- | --- |
| Audit / AuditIfNotExists | Report only |
| Deny | Block noncompliant create/update |
| DeployIfNotExists | Deploy related resource when missing |
| Modify | Mutate request fields |
| Disabled | Off inside initiative |

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| Rollout | DoNotEnforce → Deny on pilot MG | Deny at tenant root untested |
| Exemptions | Expiry + owner | Permanent waiver forever |
| Params | Central allowed locations | Every sub different unmanaged |
| Remediation | MI least privilege | Assignment MI = Owner entire tenant |
| Code | Policy in git with review | Portal-only drift |

## Output Checklist

- [ ] Scope and authorization recorded
- [ ] Existing assignments inventoried
- [ ] Initiative definitions reviewed/created
- [ ] Assignment parameters and MI configured
- [ ] Pilot compliance and deny tests evidenced
- [ ] Exemptions process + expiries
- [ ] Remediation tasks validated where used
- [ ] Monitoring for assignment/exemption changes
- [ ] `code-quality-standards` applied to policy code

## Rules

- Authorized governance only; pilot before broad Deny.
- Every exemption needs owner and expiry.
- Prefer policy-as-code over silent portal edits.
- Remediation identities must be least privilege.
- Pair detect (Defender) with prevent (Policy).
