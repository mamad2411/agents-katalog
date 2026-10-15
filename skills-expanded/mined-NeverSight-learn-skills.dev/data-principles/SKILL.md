---
name: data-principles
description: |
  Apply and review adherence to our Data engineering principles when designing data models,
  reviewing data access patterns, working with data pipelines, building schemas, or handling
  privacy and access control. Use this skill when creating domain models, reviewing cross-context
  data access, checking data quality, managing data lifecycle, evaluating technology choices for
  data storage, or ensuring data integrity and auditability. Covers: bounded context data
  ownership, data integrity and trust, domain modelling, data minimisation, access control,
  provable data quality, lifecycle management, performance at load, and tool selection.
metadata:
  category: Data
  version: "1.0.0"
  source: principles
---

# Data Principles

Our engineering principles for designing, accessing, modelling, and managing data across systems.

## When to Apply

Apply this skill when:
- Designing data models, schemas, or domain entities
- Reviewing data access patterns across service or context boundaries
- Building or reviewing data pipelines, ETL processes, or data transformation logic
- Evaluating data storage technology choices
- Reviewing privacy controls, data minimisation, or access restrictions
- Checking data quality practices in CI/CD pipelines or runtime
- Reviewing audit trails, lineage tracking, or integrity guarantees
- Assessing data retention, archival, or deletion policies

## Principles Overview

| Principle | Coverage | Reference |
|-----------|----------|-----------|
| Bounded Contexts Own Their Data | Full guidance | `principles/bounded-contexts-own-their-data.md` |
| Data You Can Trust | Full guidance | `principles/data-you-can-trust.md` |
| Model the Domain, Not the Database | Full guidance | `principles/model-the-domain-not-the-database.md` |
| Minimum Access, Minimum Data | Full guidance | `principles/minimum-access-minimum-data.md` |
| Provable Data Quality | Full guidance | `principles/provable-data-quality.md` |
| Data Lifecycle Management | Full guidance | `principles/data-lifecycle-management.md` |
| Performance at Realistic Load | Full guidance | `principles/performance-at-realistic-load.md` |
| Right Tool for the Data Job | Full guidance | `principles/right-tool-for-the-data-job.md` |
| Data Ownership Accountability | Process reminder | See below |

## Quick Review Checklist

Use this for a fast adherence scan. Load individual principle files for detailed guidance.

### Bounded Contexts Own Their Data
- [ ] No cross-context data access occurs through shared database tables
- [ ] Data shared across contexts flows through explicit, documented interfaces

### Data You Can Trust
- [ ] Audit trails exist for all data access and modification events
- [ ] Automated integrity and consistency checks run as part of the delivery pipeline

### Model the Domain, Not the Database
- [ ] Data model entities and fields use terminology recognised by business stakeholders
- [ ] Business rules are enforced in the domain layer, not solely through database constraints

### Minimum Access, Minimum Data
- [ ] Access control is implemented with least-privilege permissions for all users and systems
- [ ] APIs and data interfaces return only the data required by the consumer

### Provable Data Quality
- [ ] Data quality criteria are documented with measurable thresholds
- [ ] Automated tests validate data against those criteria as part of the delivery pipeline

### Data Lifecycle Management
- [ ] Retention policies are documented for every data set with clear timelines
- [ ] Automated processes exist for archival and deletion in line with those policies

### Performance at Realistic Load
- [ ] Performance targets are documented with measurable thresholds
- [ ] Load and performance test results are reviewed before production release

### Right Tool for the Data Job
- [ ] Storage technology selection is documented with rationale linked to data shape and usage patterns
- [ ] Architecture decision records capture the trade-offs considered during tool selection

## Process Reminders

> **Data Ownership Accountability**: Every data set must have a named owner who is accountable for how it is collected, stored, processed, and shared — including approval of new access or downstream usage. Unowned data is treated as technical debt and must be remediated. Ownership should be documented, reviewed periodically, and included as a mandatory consideration in all solution design and architecture reviews.

## How to Use

Load the relevant principle file when you need detailed guidance:

```
principles/bounded-contexts-own-their-data.md   — when reviewing cross-context data access or schema sharing
principles/data-you-can-trust.md               — when reviewing data integrity, audit trails, or lineage
principles/model-the-domain-not-the-database.md — when reviewing domain models and schema design
principles/minimum-access-minimum-data.md       — when reviewing privacy, data minimisation, or access controls
principles/provable-data-quality.md            — when reviewing data validation and quality checks
principles/data-lifecycle-management.md        — when reviewing data retention, deletion, or archival policies
principles/performance-at-realistic-load.md    — when reviewing data performance at scale
principles/right-tool-for-the-data-job.md      — when evaluating data storage or processing technology choices
```
