# AGENTS.md — Agentic ALZ Accelerator

> Multi-agent workflow that turns Azure Landing Zone requirements into deployed,
> governed, and continuously monitored infrastructure — aligned with CAF design areas.

## Philosophy

**AI Orchestrates · Humans Decide · Azure Executes**

This accelerator follows the [APEX](https://github.com/jonathan-vella/azure-agentic-infraops)
patterns for agentic infrastructure operations, extended with continuous monitoring
and auto-remediation for full landing zone lifecycle management.

The accelerator supports both **greenfield** (new environment) and **brownfield**
(existing environment) scenarios. For brownfield, an optional Step 0 runs a
WAF-aligned assessment of the current estate before the standard workflow begins.

---

## CAF Design Area Alignment

Every agent and IaC module maps to official Azure Landing Zone design areas:

| CAF Design Area | IaC Module | Agent(s) Responsible |
|-----------------|------------|---------------------|
| Billing & Tenant | `billing-and-tenant/` | Scribe, Oracle |
| Identity & Access | `identity/` | Warden, Forge |
| Resource Organization | `governance/`, `policies/` | Oracle, Strategist |
| Network Topology & Connectivity | `connectivity/`, `networking/` | Oracle, Forge |
| Security | `security/`, `platform-security/` | Warden, Sentinel |
| Management | `management/`, `logging/` | Chronicler, Sentinel |
| Governance | `governance/`, `policies/` | Warden, Sentinel |
| Platform Automation & DevOps | — (CI/CD pipelines) | Envoy, Forge |

---

## Agent Roster

### Primary Orchestrator

| Agent | Codename | Role |
|-------|----------|------|
| `orchestrator` | 🧠 **Conductor** | Master orchestrator — routes workflow steps, enforces approval gates, maintains session state |

### Brownfield Assessment Agent

Step 0 runs **only for brownfield scenarios** — skipped entirely for greenfield deployments.

| Agent | Codename | Role |
|-------|----------|------|
| `assessment` | 🔍 **Assessor** | Brownfield discovery, WAF-aligned assessment, gap analysis, and migration roadmap |

### Core Agents (by Workflow Step)

Steps 1–3.5 and 7 are shared across IaC tracks. Steps 4–6 have Bicep and Terraform variants.
Step 0 runs only for brownfield scenarios.

| Step | Agent | Codename | Role | Artifact |
|------|-------|----------|------|----------|
| 0 | `assessment` | 🔍 **Assessor** | Brownfield discovery + WAF assessment (brownfield only) | `00-assessment-*` |
| 1 | `requirements` | 📜 **Scribe** | Captures landing zone requirements through conversation | `01-requirements.md` |
| 2 | `architect` | 🏛️ **Oracle** | WAF assessment, CAF design area mapping, cost estimation | `02-architecture-assessment.md` |
| 3 | `design` | 🎨 **Artisan** | Architecture diagrams and ADRs (required for Standard and Complex; optional for Simple) | `03-*.{drawio,png,md}` |
| 3.5 | `governance` | 🛡️ **Warden** | Policy discovery, compliance constraints, security baseline | `04-governance-constraints.md/.json` |
| 4b/4t | `iac-planner` | 📐 **Strategist** | Implementation planning with AVM module selection | `04-implementation-plan.md` |
| 5b | `bicep-code` | ⚒️ **Forge** | Bicep template generation (AVM-first) | `infra/bicep/{customer}/` |
| 5t | `terraform-code` | ⚒️ **Forge** | Terraform configuration generation (AVM-TF) | `infra/terraform/{customer}/` |
| 6b/6t | `deploy` | 🚀 **Envoy** | Deployment with what-if/plan preview | `06-deployment-summary.md` |
| 7 | `documentation` | 📚 **Chronicler** | Post-deployment documentation suite | `07-*.md` |

### Day-2 Operations Agents

| Agent | Codename | Role |
|-------|----------|------|
| `monitor` | 🔭 **Sentinel** | Continuous compliance monitoring, drift detection, security posture |
| `remediate` | 🔧 **Mender** | Auto-remediation with snapshot/rollback, policy violation repair |

### Adversarial Review Agent

| Agent | Codename | Role |
|-------|----------|------|
| `challenger` | ⚔️ **Challenger** | Adversarial reviewer — challenges architecture, plans, code, and security |

---

## Workflow Steps

```
 ┌────────────┐
 │  Step 0     │  ◄── Brownfield only
 │ Assessment │
 │ (Assessor) │
 └─────┬──────┘
       ▼
┌─────────┐    ┌────────────┐    ┌────────┐    ┌────────────┐
│ Step 1   │───▶│  Step 2     │───▶│ Step 3 │───▶│ Step 3.5   │
│ Require- │    │ Architect  │    │ Design │    │ Governance │
│ ments    │    │ (WAF+CAF)  │    │        │    │ (Policy)   │
└─────────┘    └────────────┘    └────────┘    └────────────┘
     🛑              🛑                              🛑
  GATE 1          GATE 2                          GATE 3
                                                      │
                    ┌─────────────────────────────────┘
                    ▼
             ┌────────────┐    ┌────────────┐    ┌────────────┐
             │  Step 4     │───▶│  Step 5     │───▶│  Step 6     │
             │ IaC Plan   │    │ Code Gen   │    │ Deploy     │
             │ (Bicep/TF) │    │ (AVM-first)│    │ (what-if)  │
             └────────────┘    └────────────┘    └────────────┘
                  🛑                 🛑                 🛑
               GATE 4            GATE 5             GATE 6
                                                      │
             ┌────────────────────────────────────────┘
             ▼
      ┌────────────┐    ┌────────────┐    ┌────────────┐
      │  Step 7     │    │  Step 8     │    │  Step 9     │
      │ As-Built   │    │ Monitor    │◀──▶│ Remediate  │
      │ Docs       │    │ (Sentinel) │    │ (Mender)   │
      └────────────┘    └────────────┘    └────────────┘
                         Continuous Loop
```

---

## Approval Gates

| Gate | After Step | User Action |
|------|-----------|-------------|
| Gate 1 | Requirements (Step 1) | Confirm requirements complete |
| Gate 2 | Architecture (Step 2) | Approve WAF/CAF assessment |
| Gate 3 | Governance (Step 3.5) | Approve governance constraints |
| Gate 4 | Planning (Step 4) | Approve implementation plan |
| Gate 5 | Code Gen (Step 5) | Approve lint/review/what-if results |
| Gate 6 | Deployment (Step 6) | Verify deployed resources |

> ⚠️ **Never skip gates.** Gates are non-negotiable. The Challenger agent reviews
> outputs at gates 1, 2, 4, and 5 with adversarial depth proportional to complexity.

---

## Complexity Classification

| Tier | Criteria | Challenger Passes |
|------|----------|-------------------|
| **Simple** | ≤3 resource types, single region, no custom policy, single env | 1× at each gate |
| **Standard** | 4–8 types, multi-region OR multi-env, ≤3 custom policies | 2× at arch + code |
| **Complex** | >8 types, multi-region + multi-env, >3 custom policies, hub-spoke | 3× at arch + code |

---

## Shared Workflow Contract

### Step 3: Design optionality and validation

- **Simple** workloads may skip Step 3 when Step 2 provides enough architecture context for downstream steps.
- **Standard** and **Complex** workloads must complete Step 3 before Step 3.5 begins.
- The orchestrator records explicit Step 3 state as `skipped`, `completed`, or `failed`. Downstream steps must not infer Step 3 disposition from missing files.
- Before Step 3.5 and Gate 3, validate that the expected `03-*` design artifacts for the chosen path exist and are complete. If validation fails, mark Step 3 as `failed` and stop advancement.

### Step 7: Documentation validation

- Before Step 8 begins, validate that the required `07-*.md` documentation artifacts for the selected scope exist, reflect the current deployment, and reference the recorded Step 3 disposition.
- Incomplete or inconsistent Step 7 artifacts block Step 8 until corrected.

### Artifact naming note

- In this shared contract, Step 3 outputs use the `03-` prefix and Step 7 outputs use the `07-` prefix. Example filenames are illustrative, not exclusive basenames.

---

## Security Baseline

Non-negotiable rules enforced at code generation, deployment preflight, and continuous monitoring:

| # | Rule | Bicep Property | Terraform Argument |
|---|------|----------------|-------------------|
| 1 | TLS 1.2 minimum | `minimumTlsVersion: 'TLS1_2'` | `min_tls_version = "1.2"` |
| 2 | HTTPS-only traffic | `supportsHttpsTrafficOnly: true` | `https_traffic_only_enabled = true` |
| 3 | No public blob access | `allowBlobPublicAccess: false` | `allow_nested_items_to_be_public = false` |
| 4 | Managed Identity preferred | `identity: { type: 'SystemAssigned' }` | `identity { type = "SystemAssigned" }` |
| 5 | Azure AD-only SQL auth | `azureADOnlyAuthentication: true` | `azuread_authentication_only = true` |
| 6 | Public network disabled (prod) | `publicNetworkAccess: 'Disabled'` | `public_network_access_enabled = false` |

---

## Cost Governance

Every deployment **must** include budget alerts:

| Threshold | Type | Action |
|-----------|------|--------|
| 80% | Forecast | Email notification |
| 100% | Forecast | Email + action group |
| 120% | Forecast | Email + action group |

Budget amounts are parameterized per environment. No hardcoded values.

---

## Documentation Citation (Non-Negotiable)

Every agent recommendation **must** be validated against Microsoft Learn documentation:

| Rule | Enforcement |
|------|-------------|
| Use `microsoft-learn` MCP (`microsoft_docs_fetch`) for lookups | All agents — code gen, architecture, governance, monitoring |
| Include `📖 References` section with Learn URLs | All output artifacts (assessments, plans, docs) |
| Never contradict official Azure documentation | Code review + Challenger gates |
| Flag unverifiable recommendations as `⚠️ Unverified` | Self-attestation by producing agent |
| Cite Microsoft-recommended approach first when alternatives exist | Architecture and planning artifacts |

### Sub-Agent Documentation Access

MCP tools are session-scoped — spawned sub-agents do NOT inherit MCP tool access. Two patterns ensure live documentation lookup:

1. **Parent pre-fetch**: The orchestrating agent (Conductor, Oracle, etc.) calls `microsoft_docs_search`/`microsoft_docs_fetch` via MCP, then passes results into the sub-agent's prompt as context.
2. **Bash helper**: Any agent can query Learn docs directly via HTTP:
   ```bash
   scripts/fetch-learn-docs.sh search "Azure Firewall best practices"
   scripts/fetch-learn-docs.sh fetch "https://learn.microsoft.com/azure/firewall/overview"
   scripts/fetch-learn-docs.sh code "deploy Azure Firewall" bicep
   ```

Agents **must** use one of these patterns rather than citing URLs from training data alone.

---

## Artifact Naming Convention

| Step | Prefix | Example |
|------|--------|---------|
| Assessment (brownfield) | `00-` | `00-assessment-report.md` |
| Requirements | `01-` | `01-requirements.md` |
| Architecture | `02-` | `02-architecture-assessment.md` |
| Design | `03-` | `03-design-diagram.drawio` |
| Governance | `04-gov-` | `04-governance-constraints.md` |
| Planning | `04-` | `04-implementation-plan.md` |
| Implementation | `05-` | `05-implementation-reference.md` |
| Deployment | `06-` | `06-deployment-summary.md` |
| As-Built | `07-` | `07-technical-design-document.md` |
| Monitoring | `08-` | `08-compliance-report.md` |
| Remediation | `09-` | `09-remediation-log.md` |

---

## Skills

The full skill catalog and agent→skill mappings are maintained in `.github/copilot-instructions.md`. Waves 1–5 introduced service-specific skill categories covering Identity, Compute, Tenant Architecture, Data Platform, and Hybrid.

### Identity

The W1 Identity skills cover the 4 Entra ID surface areas most commonly encountered in Azure Landing Zone deployments: app registration and workload federation, Conditional Access policy governance, hybrid identity synchronization, and identity lifecycle governance (PIM, access reviews, entitlement management).

| Skill | Location | Used By |
|-------|----------|---------|
| `entra-app-registration` | `.github/skills/entra-app-registration/` | Warden, Envoy |
| `entra-conditional-access` | `.github/skills/entra-conditional-access/` | Warden, Oracle, Sentinel, Challenger |
| `entra-connect-hybrid-identity` | `.github/skills/entra-connect-hybrid-identity/` | Warden, Oracle, Forge, Assessor |
| `entra-identity-governance` | `.github/skills/entra-identity-governance/` | Warden, Oracle, Sentinel, Challenger |

### Compute

The W2 Compute skills cover the 3 primary Azure compute tiers used in enterprise Landing Zones: AKS for container-native workloads, Virtual Machines for lift-and-shift and regulated estates, and Container Apps for serverless container workloads.

| Skill | Location | Used By |
|-------|----------|---------|
| `azure-kubernetes-service` | `.github/skills/azure-kubernetes-service/` | Oracle, Forge, Strategist, Assessor |
| `azure-virtual-machines` | `.github/skills/azure-virtual-machines/` | Oracle, Forge, Strategist, Assessor |
| `azure-container-apps` | `.github/skills/azure-container-apps/` | Oracle, Forge, Strategist |

### Tenant Architecture

The W3 Tenant Architecture skills cover the foundational resource organization layer for Landing Zones. Use these together with `docs/decisions/billing-tenant-hierarchy.md` (ADR), which locks the management group hierarchy pattern and subscription vending threshold decisions.

| Skill | Location | Used By |
|-------|----------|---------|
| `management-group-architecture` | `.github/skills/management-group-architecture/` | Warden, Oracle, Strategist, Assessor |
| `subscription-vending` | `.github/skills/subscription-vending/` | Warden, Strategist, Envoy, Forge |

### Data Platform

The W4 Data Platform skills cover the Azure persistence layer for the data platform tier. Use these together with `docs/decisions/data-tier-selection.md` (ADR), which locks the "Choose SQL when / Cosmos when / Storage when" decision boundary.

| Skill | Location | Used By |
|-------|----------|---------|
| `azure-sql-database` | `.github/skills/azure-sql-database/` | Oracle, Forge |
| `azure-cosmos-db` | `.github/skills/azure-cosmos-db/` | Oracle, Forge |
| `azure-storage-accounts` | `.github/skills/azure-storage-accounts/` | Oracle, Forge |

### Hybrid

The W5 Hybrid skills use `docs/decisions/hybrid-onboarding-strategy.md` (ADR) as the canonical Arc-vs-migrate decision boundary and MI-first credential default. Both skills extend the Step 0 Assessor discovery and Step 3.5 Warden policy reach to non-Azure resources using the same governance infrastructure established for native Azure.

| Skill | Location | Used By |
|-------|----------|---------|
| `azure-arc-servers` | `.github/skills/azure-arc-servers/` | Oracle, Assessor, Warden, Forge |
| `azure-arc-kubernetes` | `.github/skills/azure-arc-kubernetes/` | Oracle, Assessor, Warden, Forge |

---

## Day-2 Operations (Unique to ALZ Accelerator)

Beyond the APEX workflow (Steps 1–7), this accelerator adds continuous operations:

### Step 8: Monitor (🔭 Sentinel)
- Full scan (compliance + drift + audit) once daily at 06:00 UTC
- Security posture from Defender for Cloud secure score
- Full audit daily at 6 AM
- Alert thresholds: Critical → immediate, High → 15 min, Medium → daily report

### Step 9: Remediate (🔧 Mender)
- 8 built-in remediation strategies mapped to common policy violations
- Auto-remediate critical and high severity
- Snapshot before remediation for rollback
- Full audit trail with action history
- Escalation to human approval for medium/low severity
