---
name: azure-defender-cloud
description: >
  Microsoft Defender for Cloud plans for owned Azure (and connected) estates:
  enabling Defender plans (Servers, Storage, Containers, SQL, Key Vault, App Services,
  Resource Manager, DNS, CSPM), secure score, recommendations, regulatory standards,
  and alert routing to SIEM. Use when onboarding subscriptions or tuning plans/cost —
  not for attacking tenants or ignoring ownership of connected AWS/GCP connectors.
---

# Microsoft Defender for Cloud

## Scope And Authorization

- **In scope:** Subscriptions, management groups, and multi-cloud connectors you are authorized to secure.
- **Out of scope:** Enabling scanning of third-party subscriptions; suppressing critical alerts without process.
- Defender plans are billable — require FinOps/security co-approval for broad enablement.
- Pair remediation of findings with service skills (blob, Key Vault, NSG); `code-quality-standards` for automation.

## When To Use

- First-time Defender for Cloud enablement on a landing zone.
- Choosing which Defender plans to buy vs free CSPM posture only.
- Improving secure score and remediating high-severity recommendations.
- Exporting alerts/recommendations to Log Analytics, Sentinel, or ITSM.
- Reviewing regulatory compliance dashboards (e.g. CIS, ISO mappings).

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| Fixing public blob findings | `azure-blob-misconfig` |
| Key Vault hardening | `azure-keyvault-basics` |
| NSG review | `azure-nsg-review` |
| AWS Security Hub ASFF | `aws-security-hub-asff` |
| Implementation quality baseline | `code-quality-standards` |

## Domain Focus

| Area | Guidance |
| --- | --- |
| Foundational CSPM | Free posture recommendations / secure score components |
| Defender plans | Workload protection (servers, storage, containers, DBs, …) — paid |
| Coverage | Per-subscription or policy-driven at MG scope |
| Alerts | Security alerts with severity; integrate SOC workflow |
| Standards | Assign regulatory compliance initiatives |
| Tooling | Azure Portal, `az security`, Policy, Sentinel, REST/API |

## Workflow

### 1. Confirm scope and success criteria

1. Management group tree, subscriptions, clouds (Azure only vs multi-cloud), budget, SOC owner.
2. Success: required plans On; agents/extensions healthy; alerts flow to SIEM; top critical recommendations owned.
3. Document exceptions process for recommendations.

### 2. Inventory current Defender state

```bash
az account show
az security pricing list -o table
az security auto-provisioning-setting list -o table
az security assessment list --query "[?status.code=='Unhealthy'].{name:displayName,res:resourceDetails}" -o table 2>/dev/null | head
az security alert list -g "$RG" -o table 2>/dev/null | head
```

1. Note which plans are `Standard` vs `Free`.
2. Check Log Analytics workspace and agent onboarding (AMA/MMA legacy).
3. List connected AWS/GCP accounts if multi-cloud CSPM enabled.

### 3. Baseline posture

1. Record secure score and top unhealthy controls.
2. Inventory critical resources unprotected (VMs without Defender servers, storage without malware scanning plan, etc.).
3. Map current SIEM integration gaps.

### 4. Enable plans and integrations

```bash
# Examples — confirm exact plan names with current CLI/API
az security pricing create -n VirtualMachines --tier Standard
az security pricing create -n StorageAccounts --tier Standard
az security pricing create -n KeyVaults --tier Standard
az security pricing create -n Containers --tier Standard
az security pricing create -n SqlServers --tier Standard
az security pricing create -n Arm --tier Standard
az security pricing create -n OpenSourceRelationalDatabases --tier Standard
az security pricing create -n CosmosDbs --tier Standard
az security pricing create -n CloudPosture --tier Standard  # enhanced CSPM if licensed
```

1. Prefer **Azure Policy** assignments at MG for consistent plan enablement and auto-provisioning.
2. Configure continuous export to Log Analytics / Event Hub for recommendations and alerts.
3. Connect Microsoft Sentinel analytics rules for high-severity Defender alerts.
4. Assign regulatory standards relevant to the org; track failing controls as backlog.
5. For servers: ensure agent/extension and correct workspace; for containers: enable Defender on AKS/ACR paths.

### 5. Verify with evidence

```bash
az security pricing list -o table
# Portal: Environment settings → subscription → plans On
# Generate authorized test only in lab; never simulate malware on prod casually
az monitor activity-log list --max-events 20
```

1. Confirm a sample recommendation appears and can be remediated.
2. Confirm alert (lab) reaches Sentinel/ITSM with correct severity.
3. Cost: estimate plan charges vs covered resources.

### 6. Observe and harden

1. Weekly secure score review with owners; SLA for High/Critical.
2. Alert suppression rules with expiry and justification only.
3. Governance: block public storage / open NSG via Policy in addition to Defender detect.

### 7. Hand off

1. Plan matrix (which plans where) + billing owner.
2. Triage runbook: recommendation vs security alert paths.
3. Link service remediation skills per recommendation type.

## Plan Selection Snapshot

| Plan area | Enable when |
| --- | --- |
| Servers | VMs/arc servers need threat detection |
| Storage | Sensitive blobs; malware scanning needs |
| Containers | AKS/Container Apps/ACR in use |
| SQL / OSS DB / Cosmos | Managed DBs hold business data |
| Key Vault | Secrets/keys critical path |
| Resource Manager | Control-plane threat detection |
| CSPM / Cloud Security Posture | Multi-cloud posture, attack path analysis (SKU-dependent) |

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| Enablement | MG policy + tracked cost | Portal click per sub ad hoc forever |
| Alerts | SOC routing + owners | Scoreboard only, no tickets |
| Suppressions | Time-boxed with risk accept | Suppress all High forever |
| Remediation | Fix resource config | Only “disable recommendation” |
| Multi-cloud | Explicit connectors + scope | Scan unknown accounts |

## Output Checklist

- [ ] Subscriptions/MGs and authorization recorded
- [ ] Current pricing/plans inventoried
- [ ] Required Defender plans enabled via code/policy
- [ ] Agents/extensions/workspaces healthy
- [ ] Export/SIEM integration verified
- [ ] Secure score baseline + top findings owned
- [ ] Suppression policy defined
- [ ] Cost owner assigned
- [ ] `code-quality-standards` applied to automation

## Rules

- Authorized tenants/subscriptions only.
- Do not hide risk with permanent suppressions.
- Pair detect (Defender) with prevent (Policy/WAF/NSG).
- Treat plan enablement as a production change with cost impact.
- Redact alert payloads that include secrets or PII in tickets.
