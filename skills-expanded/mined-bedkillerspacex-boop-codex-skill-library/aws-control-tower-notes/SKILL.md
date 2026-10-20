---
name: aws-control-tower-notes
description: >
  AWS Control Tower notes for owned landing zones: OU structure, baseline guardrails
  (preventive/detective/proactive), Account Factory, logging/audit accounts, and
  common drift issues. Use when operating or reviewing a Control Tower landing zone —
  not for unauthorized multi-account takeover or bypassing customer guardrails.
---

# AWS Control Tower Notes

## Scope And Authorization

- **In scope:** AWS Organizations + Control Tower environments you own or are contracted to operate.
- **Out of scope:** Disabling guardrails or creating accounts in someone else’s organization without authority.
- Changes to SCPs/controls can break app accounts — use non-prod OUs for experiments.
- Protect management account credentials; prefer delegated admins.
- Pair account vending automation with `code-quality-standards`.

## When To Use

- Designing OUs (Security, Sandbox, Workloads/Prod/NonProd, Suspended).
- Understanding mandatory vs strongly recommended controls / control catalog.
- Account Factory / Account Factory for Terraform (AFT) vending.
- Investigating drift (moved accounts, modified baselines, CloudTrail changes).
- Mapping detective Config rules vs preventive SCPs.

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| Config conformance packs detail | `aws-config-conformance-packs` |
| Org tag policies | `aws-organizations-tag-policies` |
| IAM least privilege in one account | `aws-iam-least-privilege` |
| SCP deep authoring only | SCPs skill if present |
| Implementation quality baseline | `code-quality-standards` |

## Domain Focus

| Piece | Role |
| --- | --- |
| Management account | Org root operations; minimize workloads |
| Log Archive | Central CloudTrail/Config evidence |
| Audit | Security tooling delegated admin patterns |
| OUs | Inheritance of controls/SCPs |
| Controls | Preventive (SCP), detective (Config), proactive (CFN hooks / Control API — version dependent) |
| Account Factory | Standardized account provisioning |

## Suggested OU Sketch

```text
Root
├── Security (Log Archive, Audit)
├── Infrastructure (shared net, dual-homed tools)
├── Sandboxes
├── Workloads
│   ├── Prod
│   └── NonProd
└── Suspended (deny-all SCP)
```

## Workflow

### 1. Confirm scope and success criteria

1. Record org ID, home Region, CT version/landing zone version, OUs, mandatory controls.
2. Success: new account vended with baselines; CloudTrail org trail immutable in log archive; drift remediated; least management account use.
3. Identify who can approve SCP exceptions.

### 2. Inventory landing zone

```bash
aws organizations describe-organization
aws organizations list-roots
aws organizations list-organizational-units-for-parent --parent-id "$ROOT_ID"
aws controltower list-landing-zones 2>/dev/null || true
aws organizations list-policies --filter SERVICE_CONTROL_POLICY
# Control Tower console still primary for many control states
```

1. Confirm Log Archive / Audit account IDs.
2. List enabled controls per OU (console/API as available in your region/version).
3. Note Regions governed (deny ungoverned Regions if policy requires).

### 3. Baseline

1. Export SCP JSON and control enablement inventory.
2. Capture Account Factory product versions.
3. Document known exceptions (accounts outside CT governance).

### 4. Operate safely

**Account vending**

1. Use Account Factory/AFT with SSO permission sets baseline.
2. Tag accounts (owner, cost center, data class) — pair with tag policies skill.
3. Place new accounts in correct OU **before** workloads deploy.

**Controls**

1. Preventive SCPs: deny leaving org, deny disabling CloudTrail/Config/GuardDuty where mandated, deny root user actions broadly.
2. Detective: Config + Security Hub aggregation in Audit.
3. Test SCP in NonProd OU first (`aws:RequestedRegion`, resource exceptions carefully).

**Drift common causes**

| Drift | Response |
| --- | --- |
| Account moved OUs | Re-align; reapply controls |
| Modified CT roles/stacks | Repair via CT lifecycle / support docs |
| CloudTrail altered | Investigate as security incident |
| Member disables Config | SCP/preventive control + detect |

**Exceptions**

1. Prefer OU-level exception accounts over weakening root SCPs.
2. Time-box SCP exemptions with tickets.
3. Never remove Log Archive protections casually.

### 5. Verify with evidence

```bash
# Org trail present
aws cloudtrail describe-trails --include-shadow-trails
# Member account: attempt denied action in lab (e.g., leave organization) → AccessDenied
aws organizations describe-account --account-id "$MEMBER"
```

1. Vend a sandbox account end-to-end; confirm baselines (IAM, trail, config).
2. Security Hub/Control findings for CT-related standards green or owned.
3. SSO users assume intended permission sets only.

### 6. Observe and harden

1. Alerts on Organizations API (attach policy, create account, leave organization).
2. Regular access review on management account and CT admin roles.
3. Landing zone upgrade planning — read release notes for breaking control changes.

### 7. Hand off

1. OU diagram, account vending runbook, exception process.
2. RACI: platform vs security vs app teams.
3. Link Config packs and tag policies for layered governance.

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| Management account | billing/org only | prod apps in management |
| SCPs | deny dangerous services at root carefully | empty SCPs on prod OUs |
| Exceptions | OU + ticket + expiry | root SCP full allow for convenience |
| Logging | central immutable logs | each account DIY trail only |
| Vending | Account Factory standardized | ad-hoc accounts no baseline |
| Drift | detect + repair | ignore console warnings |

## Output Checklist

- [ ] Org, home Region, LZ version, OUs recorded
- [ ] Log Archive/Audit identified
- [ ] Controls/SCPs inventoried and baselined
- [ ] Account vending path documented/tested
- [ ] Drift issues remediated or ticketed
- [ ] Exception process with expiry
- [ ] Monitoring on org-level changes
- [ ] Management account hardened/minimized
- [ ] Links to Config packs / tag policies
- [ ] `code-quality-standards` for automation

## Rules

- Authorized org administration only.
- Protect log archive integrity as a top priority.
- Pilot controls on NonProd OUs before Prod.
- Prefer delegated admin over standing management account sessions.
- Notes-level landing zone skill — deep SCP/Config packs in specialized skills.
