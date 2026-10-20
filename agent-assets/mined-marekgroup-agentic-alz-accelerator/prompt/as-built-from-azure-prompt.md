---
description: "Generate as-built documentation for an existing Azure deployment with no prior artifacts. Discovers resources, collects requirements interactively, synthesizes pseudo-artifacts, then generates documentation."
agent: orchestrator
argument-hint: "Provide subscription name/ID, resource group(s), and workload name"
---

# As-Built Documentation from Existing Azure Deployment

Generate comprehensive as-built documentation for an existing Azure workload where
**no prior APEX artifacts exist** (no IaC, no requirements docs, no architecture
assessments). The agent discovers everything from the live Azure environment and
user-provided context, then generates the full documentation suite.

## Mission

1. Collect Azure environment details and workload requirements interactively (Phases 1-2)
2. Deep-scan the deployed Azure resources to build a full inventory (Phase 3)
3. Synthesize pseudo-artifacts that replicate Steps 1-6 outputs (Phase 4)
4. Generate the documentation suite (Phase 5)

## Scope & Preconditions

- User has Azure CLI authenticated (`az account show` succeeds)
- User has Reader access (minimum) to the target subscription and resource group(s)
- No prior `agent-output/{customer}/` artifacts exist — this prompt creates them from scratch
- All Azure operations go through GitHub Actions or `az` CLI for read-only discovery

## Phase 1: Environment Discovery — Ask Questions FIRST

Your very first action MUST be to ask the user questions. Do NOT read files, search, or
run commands before completing Phases 1-2.

### Round 1: Azure Environment

Ask 4 questions:
1. **Customer name** — used as `{customer}` folder name under `agent-output/`
2. **Subscription** — name or ID
3. **Resource Group(s)** — comma-separated if multiple
4. **Brief workload description** — 1-2 sentences

### Round 2: Deployment Context

Ask 4 questions:
1. **Deployment scenario** — Greenfield, Migrated from on-prem, Migrated from other cloud, Modernized, Unknown
2. **Environments in scope** — Production, Staging, Development, Test, DR (multi-select)
3. **IaC tool for future adoption** — Bicep (recommended) or Terraform
4. **Managing team** — team name

### Round 3: Business & NFR Requirements

Ask 5 questions:
1. **Monthly budget** — range
2. **Compliance frameworks** — GDPR, SOC 2, ISO 27001, HIPAA, PCI-DSS, NIST, None
3. **Data sensitivity** — Public, Internal, Confidential/PII, Highly regulated
4. **RTO** — Recovery Time Objective
5. **Target SLA** — 99.99%, 99.9%, 99.5%, Not defined

## Phase 2: Validate Azure Access

After questions are complete:

```bash
az account set --subscription "{subscription}"
az account show --query "{name:name, id:id, state:state}" -o table
az group show --name "{resource-group}" --query "{name:name, location:location}" -o table
```

If access fails, STOP and ask the user to authenticate.

## Phase 3: Deep Azure Resource Discovery

Run discovery commands sequentially. Capture all output:

1. **Resource inventory** — `az resource list --resource-group "{rg}" -o json`
2. **Networking** — VNets, subnets, NSGs, private endpoints, public IPs
3. **Security** — Role assignments, Key Vaults, managed identities
4. **Diagnostics** — Log Analytics, App Insights, diagnostic settings, alerts
5. **Tags & governance** — Resource group tags, policy assignments
6. **Cost data** — `az costmanagement query` for last 30 days (if available)

## Phase 4: Synthesize Pseudo-Artifacts

Using discovered data + user answers, create in `agent-output/{customer}/`:

1. **`01-requirements.md`** — Synthesized from user answers (business context, NFRs, compliance)
2. **`02-architecture-assessment.md`** — WAF scoring from discovered resources
3. **`04-governance-constraints.md`** — From policy assignments and security scan
4. **`04-implementation-plan.md`** — From resource inventory (what would be in IaC)
5. **`06-deployment-summary.md`** — From live resource state (already deployed)

Initialize session state: `alz-recall init {customer} --json`
Record decisions: `alz-recall decide {customer} --key region --value {discovered-region} --json`

## Phase 5: Generate Documentation

With pseudo-artifacts in place, generate the canonical Step 7 documentation suite
in `agent-output/{customer}/deliverables/`:

- `07-technical-design-document.md` — Architecture overview, resource inventory, design
  decisions; include an inline Mermaid diagram of discovered resource relationships
  (Step 3 was not run in this flow; diagram is synthesized from live-discovered state)
- `07-operational-runbook.md` — Day-2 operations procedures
- `07-resource-inventory.md` — Full discovered resource inventory with names, types,
  regions, SKUs, and tags
- `07-compliance-summary.md` — Compliance mapping from discovered policies and security scan
- `07-cost-baseline.md` — Cost baseline sourced from live Azure cost data and budget
  configuration discovered in Phase 3

## Constraints

- **Read-only Azure access** — never create, modify, or delete Azure resources
- **No local `az` deploys** — discovery only. Deployments go through GitHub Actions
- **Security baseline check** — flag any resources violating the 6 non-negotiable rules
- **Cost governance check** — flag missing budget resources
- **All state via `alz-recall`** — do not write JSON state files directly
