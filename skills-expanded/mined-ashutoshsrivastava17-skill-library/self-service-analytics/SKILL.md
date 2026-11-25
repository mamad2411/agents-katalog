---
name: self-service-analytics
description: >
  Enable self-service analytics for business users with data catalog design, governed datasets,
  user training programs, semantic layer architecture, and role-based access controls.
  TRIGGER when: user says /self-service-analytics, "self-service analytics", "data democratization",
  "data catalog", "semantic layer", "governed datasets", "enable analysts", or "business user analytics".
argument-hint: "[organization or domain]"
user-invocable: true
---

# Self-Service Analytics

You are an expert in analytics platform strategy and data democratization. When the user asks you to enable self-service analytics, follow this structured process to deliver a comprehensive, governed, and user-friendly analytics ecosystem.

## Step 1: Current State Assessment

Before designing the self-service platform, assess the organizational maturity:

| Assessment Area | Questions to Answer |
|-----------------|---------------------|
| Current tools | What BI/analytics tools are in use today? |
| User segments | Who are the data consumers (analysts, managers, executives)? |
| Data literacy | What is the average comfort level with data tools? |
| Pain points | What slows down data access today (requests, queues, tickets)? |
| Data infrastructure | Warehouse, lake, or legacy databases? |
| Governance posture | Strict (regulated industry) or flexible (startup)? |
| Request volume | How many ad hoc data requests per week? |
| Existing documentation | Is there a data dictionary or glossary? |

### Maturity Model

| Level | Description | Characteristics | Target State |
|-------|-------------|-----------------|--------------|
| 1 - Ad Hoc | No standard tools or processes | Spreadsheet-driven, tribal knowledge | Stabilize |
| 2 - Reactive | Central team handles all requests | Ticket queues, long turnaround | Enable |
| 3 - Managed | Some self-service with guardrails | Governed datasets, basic training | Scale |
| 4 - Self-Service | Business users independently explore | Semantic layer, data catalog, literacy | Optimize |
| 5 - Data-Driven | Data embedded in all decisions | Automated insights, ML-assisted | Innovate |

## Step 2: Data Catalog Design

Build a discoverable inventory of data assets:

### Catalog Structure

| Catalog Component | Description | Example |
|-------------------|-------------|---------|
| Data assets | Tables, views, dashboards, reports | `fact_orders`, `Marketing Dashboard` |
| Business glossary | Plain-language definitions of terms | "MRR = sum of all active subscription revenue" |
| Data lineage | Source-to-consumption flow | Salesforce > Staging > Warehouse > Dashboard |
| Ownership | Data owner and steward per asset | Marketing team owns `dim_campaign` |
| Quality scores | Freshness, completeness, accuracy | 98% complete, refreshed daily at 6 AM |
| Usage metrics | Popularity, query frequency | Queried 340 times last month |
| Tags and domains | Categorical organization | Domain: Finance; Tag: PII, Revenue |

### Catalog Tool Selection

| Tool | Type | Best For | Key Feature |
|------|------|----------|-------------|
| DataHub | Open-source | Engineering-led orgs | Lineage, metadata API |
| Atlan | Commercial | Collaborative teams | Active metadata, Slack integration |
| Alation | Commercial | Enterprise, governance-heavy | Behavioral analysis, curation |
| dbt Docs | Open-source | dbt-centric teams | Auto-generated from models |
| Google Data Catalog | Cloud-native | GCP shops | Integrated with BigQuery |
| AWS Glue Catalog | Cloud-native | AWS shops | Integrated with Athena, Redshift |

## Step 3: Governed Datasets

Create curated, trustworthy datasets for self-service consumption:

### Dataset Governance Framework

| Governance Layer | Purpose | Implementation |
|------------------|---------|----------------|
| Certified datasets | Mark trusted, production-quality data | Certification badge in BI tool/catalog |
| Access tiers | Control who sees what | Role-based access (public, internal, restricted, confidential) |
| Data contracts | Define schema and quality guarantees | Schema tests, freshness SLAs |
| Version control | Track changes to definitions | dbt version control, migration scripts |
| Change management | Review process for metric changes | PR review for metric definition changes |

### Dataset Tier System

| Tier | Name | Access | Quality | Use Case |
|------|------|--------|---------|----------|
| Gold | Certified | All business users | High — tested, documented, SLA-backed | Self-service reporting and dashboards |
| Silver | Validated | Analysts and power users | Medium — tested, documented | Exploratory analysis, ad hoc queries |
| Bronze | Raw | Data team only | Low — as-is from source | Data engineering, debugging |
| Sandbox | Experimental | Individual user | None — user-created | Personal exploration, prototyping |

## Step 4: Semantic Layer Design

Build a consistent business logic layer between raw data and users:

### Semantic Layer Components

| Component | Purpose | Example |
|-----------|---------|---------|
| Metrics | Standardized measure definitions | `revenue = SUM(order_amount) WHERE status = 'completed'` |
| Dimensions | Standardized grouping attributes | `region`, `product_category`, `customer_segment` |
| Entities | Business objects with relationships | Customer, Order, Product, Campaign |
| Hierarchies | Drill-down paths | Country > Region > City |
| Time intelligence | Standard date calculations | YTD, QTD, MoM, YoY, rolling 30 days |
| Filters | Predefined filter sets | Active customers, current fiscal year |

### Semantic Layer Tool Options

| Tool | Approach | Integration |
|------|----------|-------------|
| dbt Metrics / MetricFlow | Code-defined, version-controlled | dbt ecosystem, BI tools via Semantic Layer API |
| Looker / LookML | Modeling language in BI tool | Native Looker, API access |
| Cube.js | Headless BI, API-first | Any BI tool, custom apps |
| AtScale | Virtual OLAP | Excel, Tableau, Power BI |
| Power BI Composite Models | In-tool semantic layer | Power BI ecosystem |

## Step 5: User Training and Enablement

Design a training program to build data literacy:

### Training Curriculum

| Module | Audience | Duration | Content |
|--------|----------|----------|---------|
| Data Foundations | All users | 1 hour | What is a database, table, metric; how data flows |
| Tool Training (Basic) | All users | 2 hours | Navigate dashboards, apply filters, export |
| Tool Training (Advanced) | Power users | 4 hours | Create charts, calculated fields, custom queries |
| SQL Fundamentals | Analysts | 8 hours | SELECT, JOIN, GROUP BY, window functions |
| Data Governance | All users | 1 hour | Access policies, PII handling, data classification |
| Metric Definitions | All users | 30 min | Where to find definitions, how to request new metrics |

### Enablement Resources

| Resource | Format | Update Cadence |
|----------|--------|----------------|
| Data dictionary | Wiki / catalog | On change |
| FAQ and troubleshooting | Knowledge base | Monthly |
| Office hours | Live session | Weekly |
| Slack channel | Async support | Always available |
| Video tutorials | Recorded walkthroughs | Quarterly |
| Template gallery | Pre-built reports/queries | Monthly |
| Champions network | Peer support program | Ongoing |

## Step 6: Access Controls and Security

Implement role-based access to protect data while enabling access:

### Access Control Matrix

| Role | Bronze (Raw) | Silver (Validated) | Gold (Certified) | Sandbox | Admin |
|------|-------------|-------------------|-------------------|---------|-------|
| Executive | No | View | View | No | No |
| Manager | No | View | View + Export | Create | No |
| Analyst | View | View + Query | View + Query + Export | Create | No |
| Power User | View | View + Query + Create | View + Query + Export | Create | No |
| Data Engineer | Full | Full | Full | Full | Yes |
| Data Steward | View | Full | Full | View | Partial |

### Security Implementation

| Security Layer | Mechanism | Tool |
|----------------|-----------|------|
| Authentication | SSO / SAML / OAuth | Okta, Azure AD, Google Workspace |
| Authorization | RBAC with group-based policies | Warehouse grants, BI tool permissions |
| Row-level security | Dynamic filters by user attribute | Row policies, user attributes in BI tool |
| Column masking | Redact or hash sensitive columns | Dynamic data masking, policy tags |
| Audit logging | Track who accessed what and when | Query logs, catalog usage analytics |
| Data classification | Tag PII, PHI, financial data | Catalog tags, automated classifiers |

## Output Format

Present the self-service analytics plan as:

1. **Current State Assessment** (maturity level, pain points, opportunity)
2. **Target Architecture** (tools, layers, data flow diagram)
3. **Data Catalog Specification** (structure, tool choice, population plan)
4. **Governed Dataset Design** (tier system, certification criteria, access model)
5. **Semantic Layer Design** (metrics, dimensions, hierarchies, tool choice)
6. **Training and Enablement Plan** (curriculum, resources, timeline)
7. **Access Control Matrix** (roles, permissions, security layers)
8. **Rollout Roadmap** (phases, milestones, success metrics)

## Quality Checklist

Before delivering the self-service analytics plan, verify:

- [ ] Current state maturity is assessed with evidence
- [ ] User segments and their needs are identified
- [ ] Data catalog covers all key data assets
- [ ] Governed datasets have clear tier definitions and certification criteria
- [ ] Semantic layer provides consistent metric definitions
- [ ] Training program addresses all user segments
- [ ] Access controls balance openness with security
- [ ] Success metrics for adoption are defined
- [ ] Rollout is phased with quick wins in the first phase

## Edge Cases

- **Highly regulated industries (healthcare, finance)**: Add data classification as a prerequisite; implement column-level masking before any self-service access
- **Very small data team**: Start with certified dashboards rather than full query access; use a lightweight catalog (dbt docs) over a full platform
- **Resistance to change**: Identify 3-5 champions in business units; start with their most painful report and automate it as a proof of concept
- **Multiple conflicting metric definitions**: Run a metric reconciliation workshop; establish a single source of truth before building the semantic layer
- **Legacy BI tools with limited governance**: Run the new and old tools in parallel during transition; provide side-by-side comparisons to build trust
- **No data warehouse**: This is a prerequisite; recommend a modern warehouse (Snowflake, BigQuery, Redshift) and a basic ELT pipeline before self-service
