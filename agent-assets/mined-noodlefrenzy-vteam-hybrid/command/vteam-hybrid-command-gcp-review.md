<!-- agent-notes: { ctx: "multi-lens GCP deployment readiness review", deps: [docs/research/gcp-landscape.md, .claude/agents/cloud-architect.md, .claude/agents/cloud-costguard.md, .claude/agents/cloud-netdiag.md], state: active, last: "cloud-architect@2026-02-12" } -->
Run a multi-lens review of GCP deployment readiness: $ARGUMENTS

This orchestrates the three cloud specialist agents (Cloud Architect, Cloud CostGuard, Cloud NetDiag) against the current project in GCP mode. Use before deploying to GCP or when reviewing an existing GCP setup.

Reference `docs/methodology/personas.md` for the broader team context. The cloud specialists extend Ines (DevOps) and Archie (architecture) with deep cloud knowledge.

---

## Step 1: Inventory

Before running the lenses, understand what exists:

- Read existing IaC files (Terraform, Deployment Manager) in the repo.
- Check `CLAUDE.md` and `docs/adrs/` for documented GCP decisions.
- Read `docs/research/gcp-landscape.md` for current service landscape.
- If nothing GCP-related exists yet, ask the user what they're planning to deploy.

Summarize: what GCP resources are defined or planned?

---

## Step 2: Architecture Lens (Cloud Architect — GCP mode)

Review the solution design through the Google Cloud Architecture Framework:

- **Service selection.** Are the right GCP services chosen? Cloud Run vs. GKE vs. Cloud Functions — is the choice justified?
- **Networking.** VPC design sound? Custom mode? Private Google Access enabled? Shared VPC where appropriate?
- **Identity.** Service accounts with Workload Identity? No exported keys? Least-privilege IAM?
- **Resilience.** Regional vs. zonal resources? Multi-region for critical data? What happens when a zone goes down?
- **IaC quality.** Well-structured Terraform, parameterized, labeled, APIs explicitly enabled?

---

## Step 3: Cost Lens (Cloud CostGuard — GCP mode)

Review for cost efficiency:

- **Machine type appropriateness.** E2 where sufficient? Right-sized? Dev vs. prod differentiation?
- **Hidden costs.** Cloud NAT data processing, GKE control plane charges, Log ingestion, idle persistent disks, static IPs.
- **Optimization opportunities.** Committed Use Discounts, Spot VMs, Cloud Run scale-to-zero, storage lifecycle policies.
- **GCP-specific savings.** Sustained Use Discounts (automatic on qualifying machine types), free tier coverage.
- **Monitoring.** Billing budgets, BigQuery billing export, Recommender enabled?

Produce a cost estimate table for dev and production environments.

---

## Step 4: Enterprise Readiness Lens (Cloud NetDiag — GCP mode)

If deploying into a customer or enterprise environment, assess deployment readiness:

- **Org/project structure.** Organization hierarchy, folder placement, project ownership.
- **Network constraints.** Shared VPC? Available subnets? Firewall rules? Hierarchical firewall policies?
- **DNS.** Cloud DNS zones, forwarding configuration, Private Google Access.
- **Organization Policies.** Constraints that restrict resource creation (VM external IPs, service usage, SA key creation).
- **VPC Service Controls.** Is the project in a perimeter? Ingress/egress rules needed?
- **IAM.** Deployment identity permissions, Shared VPC subnet access, domain-restricted sharing.

Produce a Deployment Readiness Report with Ready/Blocked/Unknown status per area.

If this is a personal or non-enterprise deployment, this lens can be lighter.

---

## Step 5: Synthesis

Combine findings from all three lenses into a single prioritized report:

### Critical
Must resolve before deploying. Org policy violations, Shared VPC access missing, VPC-SC perimeter blocking, broken IaC.

### Important
Should resolve. Cost overspend risks, missing monitoring, firewall rule gaps, IAM gaps.

### Recommendations
Improvements for the next iteration. CUD opportunities, architecture optimizations, additional resilience.

---

## Step 6: Action Plan

For every finding, provide a concrete next step:
- **Architecture issues** → The Cloud Architect agent can fix the IaC.
- **Cost issues** → The Cloud CostGuard agent can set up monitoring.
- **Network/security issues** → List exactly what to ask the customer's cloud team, or what Cloud NetDiag commands to run.

Confirm the action plan with the user before proceeding with fixes.
