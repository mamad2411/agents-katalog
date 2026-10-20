<!-- agent-notes: { ctx: "multi-lens Azure deployment readiness review", deps: [docs/research/azure-landscape.md, .claude/agents/cloud-architect.md, .claude/agents/cloud-costguard.md, .claude/agents/cloud-netdiag.md], state: active, last: "cloud-architect@2026-02-12" } -->
Run a multi-lens review of Azure deployment readiness: $ARGUMENTS

This orchestrates the three cloud specialist agents (Cloud Architect, Cloud CostGuard, Cloud NetDiag) against the current project in Azure mode. Use before deploying to Azure or when reviewing an existing Azure setup.

Reference `docs/methodology/personas.md` for the broader team context. The cloud specialists extend Ines (DevOps) and Archie (architecture) with deep cloud knowledge.

---

## Step 1: Inventory

Before running the lenses, understand what exists:

- Read existing IaC files (Bicep, Terraform, ARM templates) in the repo.
- Check `CLAUDE.md` and `docs/adrs/` for documented Azure decisions.
- Read `docs/research/azure-landscape.md` for current service landscape.
- If nothing Azure-related exists yet, ask the user what they're planning to deploy.

Summarize: what Azure resources are defined or planned?

---

## Step 2: Architecture Lens (Cloud Architect — Azure mode)

Review the solution design through the Well-Architected Framework:

- **Service selection.** Are the right Azure services chosen for the workload? Simpler or more appropriate alternatives?
- **Networking.** Is the topology sound? Private endpoints where needed? DNS configured correctly?
- **Identity.** Managed identities over keys? RBAC over shared access?
- **Resilience.** What happens when a component fails? Is there redundancy where needed?
- **IaC quality.** Is the Bicep/Terraform well-structured, parameterized, and tagged?

---

## Step 3: Cost Lens (Cloud CostGuard — Azure mode)

Review for cost efficiency:

- **SKU appropriateness.** Are dev resources using dev-appropriate SKUs? Are production resources right-sized?
- **Hidden costs.** Egress, premium features, idle resources, logging volume.
- **Optimization opportunities.** Reservations, consumption-based pricing, auto-scaling, lifecycle policies.
- **Monitoring.** Are budget alerts and cost views configured?

Produce a cost estimate table for dev and production environments.

---

## Step 4: Enterprise Readiness Lens (Cloud NetDiag — Azure mode)

If deploying into a customer or enterprise environment, assess deployment readiness:

- **Network constraints.** VNet requirements, subnet capacity, hub-spoke topology, forced tunneling.
- **DNS.** Custom DNS servers, Private DNS zone configuration, forwarding rules.
- **Security controls.** NSG rules, Azure Firewall, Network Virtual Appliances.
- **Azure Policy.** Blocking policies on the target subscription.
- **RBAC.** Does the deployment identity have sufficient permissions?

Produce a Deployment Readiness Report with Ready/Blocked/Unknown status per area.

If this is a personal or non-enterprise deployment, this lens can be lighter.

---

## Step 5: Synthesis

Combine findings from all three lenses into a single prioritized report:

### Critical
Must resolve before deploying. Blocked networking, missing security controls, broken IaC.

### Important
Should resolve. Cost overspend risks, missing monitoring, RBAC gaps.

### Recommendations
Improvements for the next iteration. Architecture optimizations, additional resilience, cost savings.

---

## Step 6: Action Plan

For every finding, provide a concrete next step:
- **Architecture issues** → The Cloud Architect agent can fix the IaC.
- **Cost issues** → The Cloud CostGuard agent can set up monitoring.
- **Network/security issues** → List exactly what to ask the customer's network team, or what Cloud NetDiag commands to run.

Confirm the action plan with the user before proceeding with fixes.
