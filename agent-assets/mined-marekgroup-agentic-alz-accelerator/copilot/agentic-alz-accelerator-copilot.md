# Copilot Instructions — Agentic ALZ Accelerator

> Project-level instructions auto-loaded by GitHub Copilot for every session.
> For the full AGENTS.md spec, see the repo root.

## Quick Start

This repo implements a multi-agent APEX workflow that turns Azure Landing Zone
requirements into deployed, governed, and continuously monitored infrastructure —
aligned with all 8 CAF design areas.

The accelerator supports both **greenfield** (new environment) and **brownfield**
(existing environment) scenarios. For brownfield, an optional Step 0 runs a
WAF-aligned assessment before the standard workflow begins.

Enable subagents: In VS Code Copilot Chat, prefix with `@workspace` and use
the agent names below (e.g., `@requirements`, `@governance`, `@orchestrator`).

## Multi-Step Workflow

| Step | Agent | Codename | Artifact |
|------|-------|----------|----------|
| 0 | `assessment` | 🔍 Assessor | `00-assessment-*.{md,json,mmd}` (brownfield only) |
| 1 | `requirements` | 📜 Scribe | `01-requirements.md` |
| 2 | `architect` | 🏛️ Oracle | `02-architecture-assessment.md` |
| 3 | `design` | 🎨 Artisan | `03-design-*.{drawio,png,md}` |
| 3.5 | `governance` | 🛡️ Warden | `04-governance-constraints.md/.json` |
| 4 | `iac-planner` | 📐 Strategist | `04-implementation-plan.md` |
| 5 | `bicep-code` / `terraform-code` | ⚒️ Forge | `infra/{bicep,terraform}/{project}/` |
| 6 | `deploy` | 🚀 Envoy | `06-deployment-summary.md` |
| 7 | `documentation` | 📚 Chronicler | `07-*.md` |
| 8 | `monitor` | 🔭 Sentinel | `08-compliance-report.md` |
| 9 | `remediate` | 🔧 Mender | `09-remediation-log.md` |
| Gates | `challenger` | ⚔️ Challenger | Gate reviews at 1, 2, 4, 5 |

## Skills (Auto-Invoked by Agents)

### Core Skills

| Skill | Location | Used By |
|-------|----------|---------|
| `caf-design-areas` | `.github/skills/caf-design-areas/` | Scribe, Oracle, Warden |
| `security-baseline` | `.github/skills/security-baseline/` | Warden, Forge, Challenger |
| `cost-governance` | `.github/skills/cost-governance/` | Oracle, Forge, Sentinel |
| `profile-management` | `.github/skills/profile-management/` | Envoy, Strategist |
| `workflow-engine` | `.github/skills/workflow-engine/` | Conductor (Orchestrator) |

### Azure & IaC Skills

| Skill | Location | Used By |
|-------|----------|---------|
| `azure-defaults` | `.github/skills/azure-defaults/` | All agents (naming, tags, AVM, WAF) |
| `azure-bicep-patterns` | `.github/skills/azure-bicep-patterns/` | Forge (Bicep), Strategist |
| `terraform-patterns` | `.github/skills/terraform-patterns/` | Forge (Terraform), Strategist |
| `azure-diagnostics` | `.github/skills/azure-diagnostics/` | Sentinel, Chronicler |
| `azure-rbac` | `.github/skills/azure-rbac/` | Warden, Forge |
| `azure-compliance` | `.github/skills/azure-compliance/` | Warden, Sentinel, Challenger |
| `azure-cost-optimization` | `.github/skills/azure-cost-optimization/` | Oracle, Sentinel |
| `azure-quotas` | `.github/skills/azure-quotas/` | Strategist, Envoy |
| `iac-common` | `.github/skills/iac-common/` | Strategist, Forge |
| `terraform-test` | `.github/skills/terraform-test/` | Forge (Terraform) |
| `terraform-search-import` | `.github/skills/terraform-search-import/` | Forge (Terraform), Assessor |

### Tooling & Operations Skills

| Skill | Location | Used By |
|-------|----------|---------|
| `session-resume` | `.github/skills/session-resume/` | Conductor (Orchestrator) |
| `python-diagrams` | `.github/skills/python-diagrams/` | Artisan |
| `drawio` | `.github/skills/drawio/` | Artisan |
| `mermaid` | `.github/skills/mermaid/` | Artisan, Chronicler |
| `azure-diagrams` | `.github/skills/azure-diagrams/` | Artisan (routing) |
| `azure-resource-visualizer` | `.github/skills/azure-resource-visualizer/` | Artisan, Assessor |
| `azure-adr` | `.github/skills/azure-adr/` | Oracle, Chronicler |
| `github-operations` | `.github/skills/github-operations/` | Envoy, Conductor |
| `docs-writer` | `.github/skills/docs-writer/` | Chronicler |

### Agent Governance & Context Skills

| Skill | Location | Used By |
|-------|----------|---------|
| `golden-principles` | `.github/skills/golden-principles/` | All agents (operating invariants) |
| `context-shredding` | `.github/skills/context-shredding/` | All agents (context compression) |
| `azure-validate` | `.github/skills/azure-validate/` | Envoy, Challenger |
| `azure-governance-discovery` | `.github/skills/azure-governance-discovery/` | Warden |
| `context-optimizer` | `.github/skills/context-optimizer/` | Conductor (audits) |
| `count-registry` | `.github/skills/count-registry/` | All agents (entity counts) |
| `workload-identity-federation` | `.github/skills/workload-identity-federation/` | Warden, Forge, Strategist, Envoy |

### Assessment Skills (Brownfield)

| Skill | Location | Used By |
|-------|----------|---------|
| `brownfield-discovery` | `.github/skills/brownfield-discovery/` | Assessor |
| `wara-assessment` | `.github/skills/wara-assessment/` | Assessor, Oracle |
| `assessment-report` | `.github/skills/assessment-report/` | Assessor, Chronicler |

### Microsoft Learn Skills (Azure Services)

> Source: [MicrosoftDocs/Agent-Skills](https://github.com/MicrosoftDocs/Agent-Skills). Provide Learn doc links fetched via `mcp_microsoftdocs:microsoft_docs_fetch`.

#### Governance & Architecture

| Skill | Location | Used By |
|-------|----------|---------|
| `azure-policy` | `.github/skills/azure-policy/` | Warden, Sentinel, Challenger |
| `azure-cloud-adoption-framework` | `.github/skills/azure-cloud-adoption-framework/` | Scribe, Oracle, Conductor |
| `azure-well-architected` | `.github/skills/azure-well-architected/` | Oracle, Challenger, Assessor |
| `azure-architecture` | `.github/skills/azure-architecture/` | Oracle, Artisan |
| `azure-resource-manager` | `.github/skills/azure-resource-manager/` | Forge, Strategist, Envoy |
| `azure-resource-graph` | `.github/skills/azure-resource-graph/` | Assessor, Sentinel, Warden |

#### Security

| Skill | Location | Used By |
|-------|----------|---------|
| `azure-security` | `.github/skills/azure-security/` | Warden, Challenger, Sentinel |
| `azure-defender-for-cloud` | `.github/skills/azure-defender-for-cloud/` | Warden, Sentinel, Mender |
| `azure-sentinel` | `.github/skills/azure-sentinel/` | Sentinel, Chronicler |
| `azure-key-vault` | `.github/skills/azure-key-vault/` | Warden, Forge |

#### Identity

The W1 Identity skills cover the 4 Entra ID surface areas most commonly encountered in Azure Landing Zone deployments: app registration and workload federation, Conditional Access policy governance, hybrid identity synchronization, and identity lifecycle governance (PIM, access reviews, entitlement management). Mirrors `AGENTS.md` `### Identity`.

| Skill | Location | Used By |
|-------|----------|---------|
| `entra-app-registration` | `.github/skills/entra-app-registration/` | Warden, Envoy |
| `entra-conditional-access` | `.github/skills/entra-conditional-access/` | Warden, Oracle, Sentinel, Challenger |
| `entra-connect-hybrid-identity` | `.github/skills/entra-connect-hybrid-identity/` | Warden, Oracle, Forge, Assessor |
| `entra-identity-governance` | `.github/skills/entra-identity-governance/` | Warden, Oracle, Sentinel, Challenger |

#### Networking

| Skill | Location | Used By |
|-------|----------|---------|
| `azure-virtual-network` | `.github/skills/azure-virtual-network/` | Oracle, Forge |
| `azure-networking` | `.github/skills/azure-networking/` | Oracle, Forge, Strategist |
| `azure-firewall` | `.github/skills/azure-firewall/` | Forge, Warden |
| `azure-firewall-manager` | `.github/skills/azure-firewall-manager/` | Warden, Forge |
| `azure-bastion` | `.github/skills/azure-bastion/` | Forge, Strategist |
| `azure-dns` | `.github/skills/azure-dns/` | Forge, Oracle |
| `azure-expressroute` | `.github/skills/azure-expressroute/` | Oracle, Forge |
| `azure-vpn-gateway` | `.github/skills/azure-vpn-gateway/` | Oracle, Forge |
| `azure-virtual-wan` | `.github/skills/azure-virtual-wan/` | Oracle, Forge |
| `azure-virtual-network-manager` | `.github/skills/azure-virtual-network-manager/` | Warden, Forge |
| `azure-private-link` | `.github/skills/azure-private-link/` | Forge, Warden |
| `azure-application-gateway` | `.github/skills/azure-application-gateway/` | Forge, Oracle |
| `azure-web-application-firewall` | `.github/skills/azure-web-application-firewall/` | Warden, Forge |
| `azure-ddos-protection` | `.github/skills/azure-ddos-protection/` | Warden, Forge |
| `azure-nat-gateway` | `.github/skills/azure-nat-gateway/` | Forge |
| `azure-network-watcher` | `.github/skills/azure-network-watcher/` | Sentinel, Chronicler |
| `azure-front-door` | `.github/skills/azure-front-door/` | Oracle, Forge |
| `azure-load-balancer` | `.github/skills/azure-load-balancer/` | Forge, Oracle |
| `azure-route-server` | `.github/skills/azure-route-server/` | Forge |

#### Compute & Containers

| Skill | Location | Used By |
|-------|----------|---------|
| `azure-kubernetes-service` | `.github/skills/azure-kubernetes-service/` | Oracle, Forge, Strategist, Assessor |
| `azure-virtual-machines` | `.github/skills/azure-virtual-machines/` | Oracle, Forge, Strategist, Assessor |
| `azure-container-apps` | `.github/skills/azure-container-apps/` | Oracle, Forge, Strategist |

#### Tenant Architecture

| Skill | Location | Used By |
|-------|----------|---------|
| `management-group-architecture` | `.github/skills/management-group-architecture/` | Warden, Oracle, Strategist, Assessor |
| `subscription-vending` | `.github/skills/subscription-vending/` | Warden, Strategist, Envoy, Forge |

#### Data Platform

The W4 data platform skills cover the Azure persistence layer for the data platform tier. Use these together with `docs/decisions/data-tier-selection.md` (ADR), which locks the "Choose SQL when / Cosmos when / Storage when" decision boundary.

- **`azure-sql-database`** — Relational persistence for regulated estates (S3). Covers SQL Database and Managed Instance topologies: failover groups, Hyperscale, Entra-only auth, TDE with CMK, MI lift-and-shift. Brownfield playbook includes a ⛔ HARD GATE on Entra-only auth migration (irrevocable).
- **`azure-cosmos-db`** — Globally distributed document tier for multi-region AI platforms (S2). Covers multi-region writes, consistency levels, partition key design, RU provisioning (manual/autoscale/serverless plus database-shared vs container-dedicated), and continuous backup. Brownfield playbook includes ⛔ HARD GATEs on consistency-level change (time-windowed) and key-based auth disable (irrevocable).
- **`azure-storage-accounts`** — Blob/Queue/Table/Files platform for ISV multi-tenant SaaS estates (S5). Covers multi-tenant blob isolation, lifecycle tiering, immutability, private endpoints, disable shared key, and SFTP/NFS/HNS feature-gating assessment. Brownfield playbook includes ⛔ HARD GATEs on account-level public-access disable (time-windowed) and shared-key disable (invalidates existing SAS tokens). HNS/ADLS Gen2, Azure NetApp Files, Azure Managed Disks, and Azure Files Premium are explicitly out of W4 scope.

When the Oracle assesses an existing data estate, sequence: `data-tier-selection.md` (ADR — decide which service tier is appropriate) → per-skill brownfield playbook (assess + harden the chosen tier).

#### Hybrid

The W5 Hybrid skills extend the accelerator's governance, policy, and observability reach beyond the Azure subscription boundary to on-premises servers and off-Azure Kubernetes clusters. Use these together with `docs/decisions/hybrid-onboarding-strategy.md` (ADR), which locks the Arc-vs-migrate decision boundary and the MI-first credential default (Azure Automation Hybrid Runbook Worker) for all Arc onboarding operations.

- **`azure-arc-servers`** — Hybrid estate governance for on-premises and multi-cloud VMs (S6). Covers Arc-enabled server onboarding at scale (MI-first via Azure Automation HRW), guest configuration / machine configuration policy, Arc extension management (AMA, MDE, Dependency Agent), Defender for Servers Plan 2, Update Manager, and Resource Graph inventory for hybrid estates. Brownfield playbook includes ⛔ HARD GATEs on credential scope (irrevocable SP scope) and MDE extension removal (irrevocable coverage gap).
- **`azure-arc-kubernetes`** — Hybrid K8s fleet governance for off-Azure clusters (S8). Covers Arc K8s cluster connection, Flux v2 GitOps (cluster bootstrap and multi-cluster fleet delivery), Azure Policy constraint templates via OPA Gatekeeper, cluster extensions (Container Insights, Defender for Containers), and OIDC issuer for workload identity federation. Brownfield playbook includes ⛔ HARD GATEs on Arc agent helm install and OIDC issuer enablement (irrevocable).

When the Assessor (Step 0) discovers a hybrid estate or the Oracle assesses a workload with off-Azure resources, sequence: `hybrid-onboarding-strategy.md` (ADR — Arc or migrate decision) → per-skill brownfield playbook (onboard and harden the chosen resource type).

#### Management & Operations

| Skill | Location | Used By |
|-------|----------|---------|
| `azure-monitor` | `.github/skills/azure-monitor/` | Sentinel, Chronicler |
| `azure-automation` | `.github/skills/azure-automation/` | Forge, Mender |
| `azure-backup` | `.github/skills/azure-backup/` | Forge, Oracle |
| `azure-update-manager` | `.github/skills/azure-update-manager/` | Sentinel, Mender |
| `azure-service-health` | `.github/skills/azure-service-health/` | Sentinel |
| `azure-advisor` | `.github/skills/azure-advisor/` | Oracle, Sentinel |
| `azure-site-recovery` | `.github/skills/azure-site-recovery/` | Forge, Oracle |

#### Cost & Reliability

| Skill | Location | Used By |
|-------|----------|---------|
| `azure-cost-management` | `.github/skills/azure-cost-management/` | Oracle, Sentinel |
| `azure-reliability` | `.github/skills/azure-reliability/` | Oracle, Challenger |
| `azure-resiliency` | `.github/skills/azure-resiliency/` | Oracle, Challenger |

## Hooks (Runtime Guards)

The Copilot runtime auto-discovers hooks from `.github/hooks/*/hooks.json` and
wraps every session with guard + telemetry. See
[`.github/hooks/README.md`](hooks/README.md) for the full inventory, lifecycle
events, and environment variables.

| Hook | Event(s) | Purpose | Blocking? |
|------|----------|---------|-----------|
| `tool-guardian` | `PreToolUse` | Deny destructive tool calls + protect `.github/hooks/` | `GUARD_MODE=block` only |
| `post-edit-format` | `PostToolUse` | `az bicep lint`, `terraform fmt`, `py_compile`, `markdownlint-cli2` | advisory |
| `secrets-scanner` | `Stop` | Regex-scan changed files for credentials | `SCAN_MODE=block` only |
| `governance-audit` | `SessionStart` / `Stop` / `UserPromptSubmit` | Append audit metadata (no prompt content) | non-blocking |
| `session-logger` | `SessionStart` / `Stop` / `UserPromptSubmit` | Session telemetry | non-blocking |
| `subagent-validation` | `SubagentStop` | Validate Challenger output shape | advisory |

> **Important**: `tool-guardian` blocks any tool call that edits files under
> `.github/hooks/`. To change a hook, route the work through a human-reviewed PR.

Local developers also get git-level hooks via `lefthook.yml` (security baseline,
cost governance, ruff, terraform fmt, yamllint, conventional commits, pytest).
The devcontainer runs `npx lefthook install` automatically; CI re-runs the same
checks in `.github/workflows/5-pr-validate.yml`.

## Approval Gates

6 non-negotiable gates (1, 2, 3, 4, 5, 6). Challenger reviews at gates 1, 2, 4, 5.
Passes scale with complexity: Simple = 1×, Standard = 2×, Complex = 3×.
**Never skip gates.**

## Key Conventions

### AVM-First
Always use Azure Verified Modules (AVM) when available for both Bicep and Terraform.
Fall back to native `resource` / `module` blocks only when no AVM module exists.

### Security Baseline (Non-Negotiable)
6 mandatory rules enforced at code gen, deploy preflight, and continuous monitoring:
1. TLS 1.2 minimum
2. HTTPS-only traffic
3. No public blob access
4. Managed Identity preferred
5. Azure AD-only SQL authentication
6. Public network disabled (prod)

### Cost Governance
Every deployment **must** include a budget resource with alerts at 80%, 100%, 120%
forecast thresholds. Budget amounts are parameterized per environment — never hardcoded.

### Naming & Tagging
Follow CAF naming conventions. Required tags on all resource groups:
`Environment`, `Owner`, `CostCenter`, `Project`, `ManagedBy`.

### IaC Defaults
- Default region: `southcentralus` (configurable via `AZURE_DEPLOYMENT_REGION`)
- IaC framework: Bicep or Terraform (configurable via `IAC_FRAMEWORK`)
- Management group prefix: `mrg` (configurable via `AZURE_MANAGEMENT_GROUP_PREFIX`)

### Documentation-Backed Recommendations (Non-Negotiable)
Every architecture recommendation, service configuration, or best-practice assertion **must**
be validated against Microsoft Learn documentation. Agents must:
1. Use the `microsoft-learn` MCP server (`microsoft_docs_fetch` tool) to look up relevant docs
2. Include a `📖 References` section in output artifacts with Learn URLs (e.g., `https://learn.microsoft.com/azure/...`)
3. Never recommend configurations that contradict official Azure documentation
4. When multiple approaches exist, cite the Microsoft-recommended approach first
5. Flag any recommendation that cannot be validated against current docs as `⚠️ Unverified`

**Sub-agent documentation access** (MCP tools are session-scoped, not inherited by spawned agents):
- **Parent pre-fetch pattern**: The orchestrating agent calls `microsoft_docs_search` before delegating,
  then includes the results in the sub-agent's prompt context
- **Bash fallback**: Any agent can query docs via `scripts/fetch-learn-docs.sh`:
  ```bash
  scripts/fetch-learn-docs.sh search "Azure Firewall premium features"
  scripts/fetch-learn-docs.sh fetch "https://learn.microsoft.com/azure/firewall/overview"
  scripts/fetch-learn-docs.sh code "deploy Azure Firewall" bicep
  ```
- Both approaches ensure citations are from **live documentation**, not training data

## Key Files

| File/Dir | Purpose |
|----------|---------|
| `AGENTS.md` | Full agent spec, workflow diagram, security rules |
| `.github/agents/` | Agent definition files (8 agents) |
| `.github/skills/` | Skill SKILL.md entry points (20 skills) |
| `.github/workflows/` | CI/CD pipelines (8 workflows) |
| `src/agents/` | Agent Python implementations |
| `src/tools/` | Tool implementations (11 tools) |
| `src/config/` | Settings, profiles, agent config |
| `infra/bicep/{customer}/` | Bicep modules and parameters |
| `infra/terraform/{customer}/` | Terraform modules and environments |
| `mcp/` | MCP servers (3: azure-pricing, azure-platform, drawio) |
| `docs/` | Architecture docs, diagrams, runbooks |
| `scripts/validators/` | Security baseline and cost governance validators |

## Validation Commands

```bash
# Security baseline validation
python scripts/validators/validate_security_baseline.py infra/bicep/{customer}/

# Cost governance validation
python scripts/validators/validate_cost_governance.py infra/bicep/{customer}/

# Bicep lint
az bicep build --file infra/bicep/{customer}/main.bicep

# Terraform validate
cd infra/terraform/{customer} && terraform init && terraform validate

# Python tests
python -m pytest tests/ -v

# Brownfield assessment (via GitHub Actions)
gh workflow run assess.yml -f scope=/subscriptions/<sub-id> -f scope_type=subscription -f mode=full
```

## MCP Servers

4 MCP servers configured in `mcp/mcp-config.json`:
1. **azure-pricing** — Cost estimation and pricing lookups
2. **azure-platform** — Consolidated 27-tool Azure platform server
3. **drawio** — Architecture diagram generation
4. **microsoft-learn** — Azure documentation lookup (all agents must use for citation validation)

## CAF Design Areas → IaC Module Mapping

| Design Area | IaC Module | Agent(s) |
|-------------|-----------|----------|
| Billing & Tenant | `billing-and-tenant/` | Scribe, Oracle |
| Identity & Access | `identity/` | Warden, Forge |
| Resource Organization | `governance/`, `policies/` | Oracle, Strategist |
| Network Topology | `connectivity/`, `networking/` | Oracle, Forge |
| Security | `security/`, `platform-security/` | Warden, Sentinel |
| Management | `management/`, `logging/` | Chronicler, Sentinel |
| Governance | `governance/`, `policies/` | Warden, Sentinel |
| Platform Automation | — (CI/CD pipelines) | Envoy, Forge |

## Day-2 Operations

Beyond deployment (Steps 1–7), continuous operations run in Steps 8–9:
- **Sentinel** runs a full scan (compliance + drift + audit) once daily at 06:00 UTC
- **Mender** auto-remediates critical/high violations with snapshot/rollback
- Alert thresholds: Critical → immediate, High → 15 min, Medium/Low → daily report
