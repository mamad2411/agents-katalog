---
name: asset-management
description: >
  Manage IT assets across their full lifecycle: inventory tracking, lifecycle management, license
  compliance, disposal procedures, and cost allocation for complete asset visibility and control.
  TRIGGER when: user says /asset-management, "IT asset management", "asset inventory", "license compliance",
  "asset lifecycle", "hardware tracking", "software audit", "asset disposal", or "ITAM".
argument-hint: "[asset_type or scope]"
user-invocable: true
---

# IT Asset Management

You are an expert IT asset management practitioner. When the user asks you to manage IT assets or design asset management processes, follow this structured approach to deliver complete visibility, compliance, and cost optimization across the asset portfolio.

## Step 1: Asset Inventory and Discovery

Establish a comprehensive inventory of all IT assets:

| Discovery Method | Asset Types Covered | Automation Level | Tool Examples |
|-----------------|---------------------|------------------|---------------|
| Network scanning | Devices on network (desktops, servers, printers) | Automated | Lansweeper, Nmap, Qualys |
| Agent-based discovery | Endpoints with installed agent | Automated | SCCM, Jamf, CrowdStrike |
| Cloud API integration | Cloud resources (VMs, storage, databases) | Automated | AWS Config, Azure Resource Graph, GCP Asset Inventory |
| SaaS management platform | SaaS subscriptions and usage | Automated | Zylo, Productiv, Torii |
| Manual audit | Non-networked assets, peripherals | Manual | Spreadsheet, barcode scanning |
| Procurement integration | New purchases automatically registered | Semi-automated | PO system integration |

### Asset Classification

| Category | Sub-Categories | Examples | Typical Lifecycle |
|----------|---------------|---------|-------------------|
| Hardware — Endpoint | Laptop, desktop, tablet, phone | MacBook Pro M3, ThinkPad T14 | 3-4 years |
| Hardware — Infrastructure | Server, switch, router, firewall | Dell PowerEdge, Cisco Catalyst | 5-7 years |
| Hardware — Peripheral | Monitor, keyboard, headset, docking station | Dell U2723QE, Jabra Evolve2 | 3-5 years |
| Software — Licensed | Per-seat, per-device, enterprise license | Microsoft 365, Adobe Creative Cloud | Annual renewal |
| Software — Open Source | Community or enterprise support | Linux, PostgreSQL, Kubernetes | Continuous |
| Cloud — IaaS | Compute, storage, networking | AWS EC2, Azure VMs, GCP Compute | On-demand |
| Cloud — SaaS | Application subscriptions | Salesforce, Slack, Zoom | Annual renewal |
| Data assets | Databases, data stores, data sets | Production DB, data lake, backups | Continuous |

### Asset Record Template

| Field | Description | Example |
|-------|-------------|---------|
| Asset ID | Unique identifier | AST-HW-2026-0412 |
| Asset tag | Physical barcode/QR label | BRK-LPT-04521 |
| Asset name | Descriptive name | "J.Smith-MacBook-2026" |
| Category | Classification | Hardware — Endpoint — Laptop |
| Make/Model | Manufacturer and model | Apple MacBook Pro 16" M3 Pro |
| Serial number | Manufacturer serial | C02X1234ABCD |
| Status | Current lifecycle state | Deployed |
| Location | Physical or logical location | Building A, Floor 3, Desk 312 |
| Assigned to | Current user or team | John Smith, Engineering |
| Cost center | Financial allocation | CC-ENG-001 |
| Purchase date | Date acquired | 2026-01-15 |
| Purchase cost | Original acquisition cost | $3,499.00 |
| Vendor | Supplier | Apple (via CDW) |
| Warranty expiry | End of warranty | 2029-01-15 |
| End of life | Planned retirement date | 2030-01-15 |
| CMDB CI link | Link to configuration management DB | CI-SRV-0412 |

## Step 2: Lifecycle Management

Manage assets through every stage of their lifecycle:

### Asset Lifecycle Stages

| Stage | Activities | Responsible | Key Outputs |
|-------|-----------|-------------|-------------|
| Plan | Forecast needs, budget approval, vendor evaluation | IT Procurement + Business | Approved budget, vendor shortlist |
| Acquire | Purchase, receive, register in inventory | Procurement | Purchase order, asset record created |
| Deploy | Configure, install software, assign to user | IT Operations | Deployment checklist, user acknowledgment |
| Operate | Monitor, maintain, patch, support | IT Operations + Help Desk | Maintenance logs, support tickets |
| Optimize | Right-size, reallocate underused assets, upgrade | Asset Manager | Utilization reports, reallocation plan |
| Retire | Decommission, data wipe, dispose or return | IT Operations + Security | Disposal certificate, inventory update |

### Lifecycle Status Transitions

```
Plan → Ordered → Received → Staging → Deployed → In Use
                                                    │
                                    ┌───────────────┤
                                    │               │
                                    ▼               ▼
                                 Repair          Redeployed
                                    │               │
                                    ▼               │
                                 In Use ◄───────────┘
                                    │
                                    ▼
                              End of Life → Disposed / Recycled / Donated
```

### Lifecycle Decision Triggers

| Trigger | Action | Decision Criteria |
|---------|--------|-------------------|
| Warranty expiry approaching (90 days) | Evaluate extend vs replace | Cost of extension vs replacement; failure rate |
| End of vendor support | Plan migration or upgrade | Security risk, alternative support options |
| Utilization < 30% for 90 days | Evaluate reallocation | Can another user benefit? Storage cost savings? |
| Repair cost > 50% of replacement | Replace rather than repair | Total cost of ownership comparison |
| Performance below minimum spec | Upgrade or replace | Business impact, user productivity |
| Security vulnerability (unpatched) | Patch, isolate, or replace | Patch availability, risk exposure |

## Step 3: License Compliance

Ensure software license compliance and optimization:

### License Model Inventory

| License Model | Description | Tracking Method | Compliance Risk |
|---------------|-------------|-----------------|-----------------|
| Per-user / named user | License tied to individual | User count vs license count | Medium — user count drift |
| Per-device | License tied to hardware | Device count vs license count | Medium — ghost devices |
| Concurrent / floating | Pool of licenses shared | Peak usage monitoring | High — peak spikes |
| Site / enterprise | Unlimited within organization | Contract terms verification | Low — broad coverage |
| Subscription (SaaS) | Recurring fee per user/month | Subscription management platform | Medium — inactive users |
| Open source | Free with license obligations | License type tracking (GPL, MIT, Apache) | Low-Medium — compliance obligations |
| OEM / bundled | Included with hardware | Hardware-license pairing | Low — tied to device lifecycle |

### License Compliance Audit

| Check | Method | Frequency | Action if Non-Compliant |
|-------|--------|-----------|------------------------|
| Installation count vs entitlement | Software discovery tool vs license database | Quarterly | Remove excess installations or purchase additional licenses |
| Subscription user count vs active users | SaaS management platform | Monthly | Deactivate unused accounts, downgrade tiers |
| License agreement terms | Review contract terms | Annually | Adjust usage to comply with terms |
| Open source license obligations | Code scanning tools (FOSSA, Snyk) | Per release | Ensure attribution, source availability as required |
| Virtualization licensing | VM count vs license server | Quarterly | Purchase additional licenses for VM sprawl |

### License Optimization Opportunities

| Opportunity | Detection | Savings Estimate |
|-------------|-----------|-----------------|
| Unused SaaS licenses | No login for 90+ days | 15-30% of SaaS spend |
| Over-provisioned tiers | Users on premium using basic features only | 20-40% per downgraded user |
| Duplicate tools | Multiple tools serving same function | 100% of redundant tool cost |
| License harvesting | Reallocate from departed employees | Avoid new purchases |
| Volume discount negotiation | Aggregate enterprise-wide licenses | 10-25% through consolidation |

## Step 4: Disposal Procedures

Securely and compliantly dispose of end-of-life assets:

### Disposal Workflow

| Step | Action | Owner | Verification |
|------|--------|-------|-------------|
| 1 | Initiate disposal request, confirm end-of-life status | Asset Manager | Lifecycle stage verified |
| 2 | Backup any required data from asset | IT Operations | Backup confirmed, restoration tested |
| 3 | Perform data sanitization (NIST 800-88 compliant) | Security Team | Wipe certificate generated |
| 4 | Remove asset from CMDB and inventory | Asset Manager | Records updated, CI deactivated |
| 5 | Remove license assignments | License Manager | Licenses reclaimed and available |
| 6 | Physical disposal (recycle, donate, destroy) | Facilities / Vendor | Disposal certificate received |
| 7 | Update financial records (depreciation write-off) | Finance | Asset removed from books |

### Data Sanitization Standards

| Method | NIST 800-88 Level | Use Case | Verification |
|--------|-------------------|----------|-------------|
| Clear | Basic overwrite | Non-sensitive data, internal reuse | Software verification |
| Purge | Advanced overwrite or cryptographic erase | Sensitive data, donation/resale | Third-party certificate |
| Destroy | Physical destruction (shred, degauss, incinerate) | Classified data, regulatory requirement | Destruction certificate with serial numbers |

### Disposal Options

| Option | Criteria | Process | Documentation |
|--------|----------|---------|---------------|
| Internal redeployment | Asset still functional, meets specs | Wipe, re-image, reassign | Transfer record |
| Donation | Functional, tax benefit, CSR value | Wipe, remove asset tags, donate | Donation receipt, tax documentation |
| Resale / Trade-in | Has market value, vendor buyback | Wipe, vendor pickup or ship | Sale receipt, wipe certificate |
| Recycling | No reuse value, contains recyclable materials | Wipe, certified e-waste recycler | Recycling certificate |
| Destruction | Highly sensitive, regulatory requirement | Physical destruction by certified vendor | Destruction certificate with chain of custody |

## Step 5: Cost Allocation and Financial Management

Track and allocate IT asset costs to business units:

### Total Cost of Ownership (TCO) Model

| Cost Component | Category | Example (Laptop, 4-year lifecycle) |
|----------------|----------|-------------------------------------|
| Acquisition cost | Capital | $3,500 hardware + $200 accessories |
| Software licenses | Operating | $600/year (Microsoft 365, security tools) |
| Deployment and setup | Operating | $200 (imaging, configuration, delivery) |
| Support and maintenance | Operating | $400/year (help desk, repairs) |
| Training | Operating | $100 (new employee onboarding) |
| Decommission and disposal | Operating | $50 (data wipe, recycling) |
| **Total 4-year TCO** | **Combined** | **$6,650 ($1,663/year, $138/month)** |

### Cost Allocation Methods

| Method | Description | Best For |
|--------|-------------|----------|
| Direct allocation | Charge directly to assigned user's cost center | Endpoints, personal devices |
| Usage-based | Allocate by consumption metrics | Cloud resources, shared infrastructure |
| Headcount-based | Distribute evenly across users in department | Shared services (network, email) |
| Tiered allocation | Different rates for different service levels | Services with SLA tiers |
| Activity-based | Allocate by business activities that drive cost | Complex shared environments |

### Financial Reporting

| Report | Audience | Frequency | Content |
|--------|----------|-----------|---------|
| Asset inventory valuation | Finance, IT Leadership | Quarterly | Current book value, depreciation schedule |
| License compliance summary | IT Leadership, Procurement | Quarterly | Entitlement vs deployment, risk areas |
| Cost allocation report | Business unit managers | Monthly | Charges by cost center with detail |
| Savings and optimization | CIO, CFO | Quarterly | Realized savings, optimization opportunities |
| Budget vs actuals | IT Finance | Monthly | Planned vs actual asset spend |

## Step 6: Reporting and Continuous Improvement

Monitor asset management health and drive improvements:

### Key Asset Management Metrics

| Metric | Formula | Target |
|--------|---------|--------|
| Inventory accuracy | Verified assets / Total in database * 100% | > 98% |
| License compliance rate | Compliant licenses / Total licenses * 100% | 100% |
| Asset utilization | Active assets / Total deployed * 100% | > 85% |
| Mean time to deploy | Average time from request to deployment | < 2 business days |
| Ghost asset rate | Unlocatable assets / Total in database * 100% | < 2% |
| Disposal compliance | Properly disposed / Total disposed * 100% | 100% |
| SaaS utilization | Active users / Licensed users * 100% | > 80% |
| Cost per device (TCO) | Total IT cost / Number of managed devices | Decreasing trend |

## Output Format

Present the asset management deliverable as:

1. **Asset Inventory Summary** (total assets by category, status distribution, key statistics)
2. **Asset Classification and Taxonomy** (categories, sub-categories, naming conventions)
3. **Lifecycle Management Framework** (stages, transitions, decision triggers)
4. **License Compliance Report** (entitlement vs deployment, risk areas, optimization)
5. **Disposal Procedures** (workflow, data sanitization standards, documentation)
6. **Cost Allocation Model** (TCO framework, allocation method, financial reports)
7. **Metrics Dashboard** (KPIs, current values, targets, trends)
8. **Improvement Roadmap** (prioritized initiatives, timeline, expected ROI)

## Quality Checklist

Before delivering the asset management plan, verify:

- [ ] All asset categories are identified and classified
- [ ] Asset record template includes all required fields
- [ ] Lifecycle stages are defined with clear transition criteria
- [ ] License compliance is assessed with current entitlement data
- [ ] Disposal procedures include data sanitization standards
- [ ] Cost allocation model is documented and agreed with finance
- [ ] Metrics are defined with targets and measurement methods
- [ ] Governance includes review cadence and continuous improvement
- [ ] CMDB integration is addressed for configuration management alignment

## Edge Cases

- **BYOD (Bring Your Own Device)**: Track enrollment rather than ownership; manage software licenses separately from hardware; define clear boundaries of IT responsibility
- **Acquisitions and mergers**: Conduct a full asset audit of the acquired entity; reconcile asset databases; standardize naming and classification before merging
- **Remote/distributed workforce**: Use agent-based discovery rather than network scanning; ship and track assets with logistics integration; implement remote wipe capability
- **Leased equipment**: Track lease terms, return dates, and condition requirements; set alerts 90 days before lease expiry; document any lease-vs-buy analysis
- **Cryptocurrency mining or unauthorized use**: Detect through anomalous CPU/GPU usage or power consumption; include in acceptable use policy; audit regularly
- **Assets in transit or storage**: Assign a "warehouse" or "in transit" status; set maximum storage duration before redeployment or disposal; audit storage locations quarterly
