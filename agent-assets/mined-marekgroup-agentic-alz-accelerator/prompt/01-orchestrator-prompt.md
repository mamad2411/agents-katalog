---
agent: orchestrator
description: "Run the full APEX workflow for an Azure Landing Zone deployment"
---

# Full APEX Workflow — Enterprise Landing Zone

You are the Conductor (Orchestrator). Run the full APEX workflow for an Azure
Enterprise Landing Zone deployment.

## Enterprise Landing Zone Context

This accelerator deploys **CAF enterprise-scale architecture**:
- **Platform Landing Zones** — 4 sequential: Management → Connectivity → Identity → Security
- **Application Landing Zones** — Workloads stamped on the platform (corp, online, sandbox profiles)
- **Management Group Hierarchy** — `{prefix}` naming convention with platform and app LZ separation (prefix from `AZURE_MANAGEMENT_GROUP_PREFIX`, e.g., `mrg`)
- **Deployments via GitHub Actions** — `2-platform-deploy.yml`, `3-app-deploy.yml` (never local `az` CLI)
- **OIDC authentication** — Workload identity federation, no stored secrets
- **State management** — Use `alz-recall` CLI for all session state (never write JSON directly)

## Steps

Execute steps in order, enforcing approval gates at each checkpoint:

0. **Assessment** (🔍 Assessor) → Brownfield discovery + WAF assessment (brownfield only) → `00-assessment-*`
1. **Requirements** (📜 Scribe) → Gather requirements, map to 8 CAF design areas → `01-requirements.md`
2. **Architecture** (🏛️ Oracle) → WAF assessment, CAF mapping, cost estimation → `02-architecture-assessment.md`
3. **Design** (🎨 Artisan) → Architecture diagrams and ADRs (required for Standard/Complex; optional for Simple) → `03-design-*.{drawio,png,md}`
3.5. **Governance** (🛡️ Warden) → Policy discovery, compliance constraints → `04-governance-constraints.md`
4. **IaC Planning** (📐 Strategist) → AVM module selection, implementation plan → `04-implementation-plan.md`
5. **Code Generation** (⚒️ Forge) → Bicep/Terraform templates → `infra/{bicep,terraform}/`
6. **Deployment** (🚀 Envoy) → What-if/plan preview then deploy → `06-deployment-summary.md`
7. **As-Built Docs** (📚 Chronicler) → Post-deployment documentation suite → `07-*.md`
8. **Monitor** (🔭 Sentinel) → Continuous compliance + drift detection → `08-compliance-report.md`
9. **Remediate** (🔧 Mender) → Auto-remediation with rollback → `09-remediation-log.md`

## Platform LZ Deployment Order

Deploy platform LZs sequentially via `2-platform-deploy.yml`:
```
Management (LAW, Automation) → Connectivity (Hub VNet, Bastion) → Identity (Spoke, RBAC) → Security (Sentinel, Defender)
```

## Gates

- Gate 1 after Step 1 — Confirm requirements
- Gate 2 after Step 2 — Approve architecture
- Gate 3 after Step 3.5 — Approve governance constraints
- Gate 4 after Step 4 — Approve implementation plan
- Gate 5 after Step 5 — Approve code review
- Gate 6 after Step 6 — Verify deployment

The Challenger (⚔️) reviews at Gates 1, 2, 4, and 5.

Before advancing to Step 8, validate that all required `07-*.md` artifacts exist, reflect the current deployment, and reference the recorded Step 3 disposition.

## Ask the user: greenfield or brownfield? Then start with Step 0 (brownfield) or Step 1 (greenfield).
