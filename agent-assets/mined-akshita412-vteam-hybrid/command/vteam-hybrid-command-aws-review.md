<!-- agent-notes: { ctx: "multi-lens AWS deployment readiness review", deps: [docs/research/aws-landscape.md, .claude/agents/cloud-architect.md, .claude/agents/cloud-costguard.md, .claude/agents/cloud-netdiag.md], state: active, last: "cloud-architect@2026-02-12" } -->
Run a multi-lens review of AWS deployment readiness: $ARGUMENTS

This orchestrates the three cloud specialist agents (Cloud Architect, Cloud CostGuard, Cloud NetDiag) against the current project in AWS mode. Use before deploying to AWS or when reviewing an existing AWS setup.

Reference `docs/methodology/personas.md` for the broader team context. The cloud specialists extend Ines (DevOps) and Archie (architecture) with deep cloud knowledge.

---

## Step 1: Inventory

Before running the lenses, understand what exists:

- Read existing IaC files (CDK, CloudFormation, Terraform) in the repo.
- Check `CLAUDE.md` and `docs/adrs/` for documented AWS decisions.
- Read `docs/research/aws-landscape.md` for current service landscape.
- If nothing AWS-related exists yet, ask the user what they're planning to deploy.

Summarize: what AWS resources are defined or planned?

---

## Step 2: Architecture Lens (Cloud Architect — AWS mode)

Review the solution design through the Well-Architected Framework:

- **Service selection.** Are the right AWS services chosen? Simpler or more cost-effective alternatives?
- **Networking.** VPC design sound? NAT Gateways where needed? VPC Endpoints to avoid data processing charges?
- **Identity.** IAM roles over access keys? Least-privilege policies? No hardcoded credentials?
- **Resilience.** Multi-AZ? Auto-scaling? Health checks? What happens when a component fails?
- **IaC quality.** Well-structured, parameterized, tagged?

---

## Step 3: Cost Lens (Cloud CostGuard — AWS mode)

Review for cost efficiency:

- **Instance appropriateness.** Graviton where possible? Right-sized? Dev vs. prod differentiation?
- **Hidden costs.** NAT Gateway data processing, cross-AZ transfer, CloudWatch Logs ingestion, idle EIPs, EBS volumes on stopped instances.
- **Optimization opportunities.** Savings Plans, Spot Instances, auto-scaling, storage tiering.
- **Monitoring.** AWS Budgets, Cost Anomaly Detection, billing alarms configured?

Produce a cost estimate table for dev and production environments.

---

## Step 4: Enterprise Readiness Lens (Cloud NetDiag — AWS mode)

If deploying into a customer or enterprise environment, assess deployment readiness:

- **Network constraints.** VPC requirements, subnet capacity, Transit Gateway, centralized egress.
- **DNS.** Route 53 Resolver configuration, Private Hosted Zones, on-premises forwarding.
- **Security controls.** Security Groups, NACLs, Network Firewall, VPC Endpoint policies.
- **SCPs.** Service Control Policies in the AWS Organization that may block actions.
- **IAM.** Permission boundaries, deployment role scope, tag-based policies.
- **AWS Config.** Compliance rules that will flag non-compliant resources.

Produce a Deployment Readiness Report with Ready/Blocked/Unknown status per area.

If this is a personal or non-enterprise deployment, this lens can be lighter.

---

## Step 5: Synthesis

Combine findings from all three lenses into a single prioritized report:

### Critical
Must resolve before deploying. Blocked networking, missing security controls, broken IaC, SCP violations.

### Important
Should resolve. Cost overspend risks, missing monitoring, IAM gaps, Config rule violations.

### Recommendations
Improvements for the next iteration. Architecture optimizations, Graviton migration, Savings Plans.

---

## Step 6: Action Plan

For every finding, provide a concrete next step:
- **Architecture issues** → The Cloud Architect agent can fix the IaC.
- **Cost issues** → The Cloud CostGuard agent can set up monitoring.
- **Network/security issues** → List exactly what to ask the customer's cloud team, or what Cloud NetDiag commands to run.

Confirm the action plan with the user before proceeding with fixes.
