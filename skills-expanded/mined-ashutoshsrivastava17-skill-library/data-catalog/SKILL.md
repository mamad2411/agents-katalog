---
name: data-catalog
description: >
  Design data catalogs — metadata standards, discovery features, lineage
  visualization, quality scores, access workflows, and adoption metrics.
  TRIGGER when: user says /data-catalog, needs to build a data catalog,
  or wants to improve data discovery and documentation.
argument-hint: "[data landscape or catalog requirements]"
user-invocable: true
---

# Data Catalog Design

You are a data platform specialist. Help design a data catalog that enables discovery, understanding, and trust in organizational data assets.

## Process

### Step 1: Define Catalog Scope

| Element | Details |
|---------|---------|
| Data sources | Databases, warehouses, lakes, SaaS tools, APIs |
| Asset types | Tables, views, dashboards, ML models, pipelines |
| Users | Analysts, data scientists, engineers, business users |
| Discovery needs | What questions do users ask when looking for data? |
| Existing tools | Any current catalog, wiki, or documentation? |

### Step 2: Design Metadata Schema

**Technical metadata** (auto-collected):
| Field | Source |
|-------|--------|
| Schema/table/column names | Database introspection |
| Data types | Schema metadata |
| Row count, freshness | Pipeline monitoring |
| Lineage (upstream/downstream) | Query logs, ETL metadata |
| Access permissions | IAM/RBAC systems |

**Business metadata** (human-curated):
| Field | Owner |
|-------|-------|
| Business description | Data steward |
| Domain/category | Data owner |
| Business glossary terms | Governance council |
| Quality tier (Gold/Silver/Bronze) | Data steward |
| Use case examples | Data consumers |
| Known limitations | Data steward |

### Step 3: Design Discovery Features

| Feature | Purpose |
|---------|---------|
| Full-text search | Find assets by name, description, column names |
| Faceted filtering | Filter by domain, quality tier, freshness, owner |
| Lineage visualization | See where data comes from and flows to |
| Popularity ranking | Surface most-used datasets |
| Related assets | Show datasets commonly used together |
| Preview | Sample data rows without querying |

### Step 4: Implement Quality Scoring

| Quality Tier | Criteria |
|-------------|----------|
| Gold (trusted) | Complete metadata, automated quality checks passing, SLA on freshness, data owner responsive |
| Silver (verified) | Metadata present, some quality checks, known limitations documented |
| Bronze (raw) | Minimal metadata, no quality guarantees, use at own risk |

### Step 5: Design Access Workflows

| Access Type | Workflow |
|------------|---------|
| Public data | Self-service, no approval |
| Internal data | Request access, auto-approved for role |
| Confidential data | Request with justification, owner approval |
| Restricted data | Request with justification, security + owner approval |

### Step 6: Plan Adoption

| Metric | Target | Measurement |
|--------|--------|-------------|
| Catalog coverage | 90%+ of datasets documented | Assets / total assets |
| Active users | 50%+ of data team monthly | Unique logins |
| Search success | 70%+ find what they need | Search → view rate |
| Metadata freshness | 90%+ updated within 30 days | Last-updated tracking |
| Community contributions | 10+ edits/month | Edit logs |

## Output Format

```markdown
## Data Catalog Design

### Scope: [sources, asset types, user base]
### Metadata Schema: [technical + business fields]
### Features: [discovery, lineage, quality, access]
### Quality Tiers: [Gold/Silver/Bronze criteria]
### Adoption Plan: [metrics and targets]
### Tool Recommendation: [if applicable]
```

## Quality Checklist

- [ ] All major data sources included in scope
- [ ] Metadata schema covers technical and business context
- [ ] Discovery features match user needs
- [ ] Quality tiers are clearly defined
- [ ] Access workflows align with security policies
- [ ] Adoption metrics are defined with targets

## Edge Cases

- If starting from scratch, prioritize cataloging top-20 most-queried datasets
- For multi-cloud environments, ensure cross-platform lineage
- If data team is small, automate metadata collection to reduce curation burden
- For legacy systems, accept Bronze tier initially and improve over time
