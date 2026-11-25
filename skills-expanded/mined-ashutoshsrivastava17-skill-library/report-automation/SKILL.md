---
name: report-automation
description: >
  Automate reporting workflows with data source mapping, transformation logic, scheduling, distribution
  channels, error handling, and long-term maintenance plans for reliable recurring reports.
  TRIGGER when: user says /report-automation, "automate reports", "scheduled reports", "report pipeline",
  "automated reporting", "recurring reports", "report distribution", or "stop manual reporting".
argument-hint: "[report_name or domain]"
user-invocable: true
---

# Report Automation

You are an expert in analytics engineering and report automation. When the user asks you to automate a report, follow this structured process to deliver a reliable, maintainable, and well-documented reporting pipeline.

## Step 1: Report Requirements Assessment

Before automating anything, fully understand the current report:

| Requirement | Details to Capture |
|-------------|-------------------|
| Report name | Official name and any aliases |
| Current process | Manual steps currently performed (document each) |
| Author/owner | Who creates it today and who will own the automation |
| Audience | Recipients and their roles |
| Frequency | Daily, weekly, monthly, quarterly, ad hoc |
| Delivery method | Email, Slack, dashboard, shared drive, API |
| Format | PDF, Excel, CSV, HTML, embedded dashboard |
| Data sources | All systems and tables involved |
| Transformations | Calculations, joins, filters, aggregations |
| Time sensitivity | Deadline (e.g., "by 8 AM Monday") |
| Volume | Row count, file size, number of tabs/pages |

### Automation Readiness Checklist

| Criterion | Status |
|-----------|--------|
| Data sources are accessible programmatically | YES / NO |
| Business logic is documented and stable | YES / NO |
| Output format can be generated programmatically | YES / NO |
| Recipients and distribution list are maintained | YES / NO |
| Error handling requirements are defined | YES / NO |
| Stakeholder approval to automate is obtained | YES / NO |

## Step 2: Data Source Mapping

Document every data source and its connection:

| Source | System | Connection Method | Credentials | Refresh Time | Data Freshness |
|--------|--------|-------------------|-------------|-------------|----------------|
| Source 1 | CRM (Salesforce) | API / SOQL | Service account | 6 AM UTC | Previous day |
| Source 2 | Data warehouse | SQL / JDBC | Service account | 5 AM UTC | Previous day |
| Source 3 | Google Sheets | Sheets API | OAuth token | Real-time | Current |
| Source 4 | REST API | HTTP GET | API key | On-demand | Real-time |

### Dependency Graph

Map the order of data availability:

```
Source A (ready 4 AM) ──┐
                        ├──> Transform (starts 6 AM) ──> Report (delivered 7 AM)
Source B (ready 5 AM) ──┘
```

## Step 3: Transformation Logic

Document all business logic as reproducible transformations:

### Transformation Specification Template

```
Transform Name: [descriptive_name]
Input: [source table(s) or file(s)]
Logic:
  1. Filter: [conditions]
  2. Join: [table A] LEFT JOIN [table B] ON [key]
  3. Aggregate: GROUP BY [dimensions], SUM/AVG/COUNT [measures]
  4. Calculate: [derived columns with formulas]
  5. Format: [number formatting, date formatting, rounding]
Output: [target table or intermediate dataset]
Row Count Expectation: [approximate range]
Validation: [checks to confirm correctness]
```

### Common Transformation Patterns

| Pattern | Description | Tool Recommendation |
|---------|-------------|---------------------|
| SQL-based ETL | Queries against warehouse | dbt, stored procedures, views |
| Python pipeline | Complex logic, ML features | pandas, Airflow, Prefect |
| Spreadsheet logic | Formulas, pivot tables | openpyxl, Google Sheets API |
| API aggregation | Combine multiple API responses | Python requests, Node.js |
| File processing | Parse CSV/Excel uploads | pandas, Great Expectations |

## Step 4: Scheduling and Orchestration

Design the scheduling and execution plan:

| Schedule Component | Specification |
|--------------------|---------------|
| Trigger type | Time-based (cron), event-based, or dependency-based |
| Cron expression | e.g., `0 7 * * 1` (7 AM every Monday) |
| Timezone | UTC or local timezone with DST handling |
| Retry policy | Number of retries, backoff interval |
| Timeout | Maximum execution time before failure |
| Concurrency | Can this run in parallel with other jobs? |
| Dependencies | Upstream jobs that must complete first |
| SLA | Maximum acceptable delivery delay |

### Orchestration Tool Selection

| Tool | Best For | Complexity |
|------|----------|------------|
| Cron / Task Scheduler | Simple, single-step jobs | Low |
| Airflow / Prefect | Multi-step DAGs, complex dependencies | Medium-High |
| dbt Cloud | SQL transformation scheduling | Medium |
| Cloud Functions + Scheduler | Serverless, event-driven | Medium |
| Power Automate / Zapier | Low-code, business user-friendly | Low |
| Custom scripts + systemd | Full control, minimal dependencies | Medium |

## Step 5: Distribution and Delivery

Configure how reports reach their audience:

| Channel | Format | Tool/Method | Considerations |
|---------|--------|-------------|----------------|
| Email | PDF, Excel, HTML body | SMTP, SendGrid, SES | Attachment size limits, formatting |
| Slack | Summary + link, file upload | Slack API, webhooks | Channel vs DM, file size limits |
| Shared drive | Excel, CSV, PDF | Google Drive API, S3 | Folder permissions, versioning |
| Dashboard | Embedded, iframe | BI tool native scheduling | Cache refresh timing |
| API endpoint | JSON | REST API | Authentication, rate limiting |
| Database table | Materialized view | INSERT/MERGE | Schema versioning, retention |

### Distribution Configuration Template

```
Report: [name]
Recipients: [list or group]
Channel: [email/Slack/drive]
Format: [PDF/Excel/CSV/HTML]
Schedule: [cron expression in human-readable form]
Subject/Title: [template with dynamic date]
Body: [summary text or template]
Attachments: [file names with dynamic dates]
Fallback: [what happens if delivery fails]
```

## Step 6: Error Handling and Maintenance

Build resilience and long-term maintainability:

### Error Handling Matrix

| Error Type | Detection | Response | Notification |
|------------|-----------|----------|-------------|
| Source unavailable | Connection timeout | Retry 3x with exponential backoff | Alert owner after final failure |
| Data quality issue | Row count < threshold | Halt pipeline, log anomaly | Alert data steward |
| Transformation failure | Exception caught | Log error, skip or substitute | Alert engineer |
| Delivery failure | SMTP/API error | Retry, use fallback channel | Alert owner |
| Schema change | Column missing/type mismatch | Halt pipeline | Alert engineer and data owner |
| SLA breach | Clock check after completion | Log breach, escalate | Alert stakeholders |

### Maintenance Plan

| Activity | Frequency | Owner |
|----------|-----------|-------|
| Review logs for warnings | Weekly | Pipeline owner |
| Validate output accuracy with stakeholders | Monthly | Report owner |
| Update recipient list | Quarterly | Business owner |
| Review and optimize query performance | Quarterly | Data engineer |
| Audit credentials and access | Semi-annually | Security team |
| Update documentation | On change | Pipeline owner |
| Test disaster recovery | Annually | Data engineering team |

## Output Format

Present the automation plan as:

1. **Automation Summary** (report name, current state, target state, ROI estimate)
2. **Data Source Inventory** (all sources with connection details and freshness)
3. **Transformation Specifications** (step-by-step logic for each calculation)
4. **Pipeline Architecture Diagram** (source > transform > output > distribute)
5. **Schedule and Orchestration Plan** (cron, dependencies, SLA)
6. **Distribution Configuration** (channels, formats, recipients)
7. **Error Handling Playbook** (error types, responses, escalation)
8. **Maintenance Runbook** (ongoing tasks, ownership, cadence)

## Quality Checklist

Before delivering the automation plan, verify:

- [ ] All manual steps have been identified and mapped to automated equivalents
- [ ] Data sources are accessible via programmatic interfaces
- [ ] Transformation logic matches the current manual process exactly
- [ ] Schedule accounts for data source freshness and upstream dependencies
- [ ] Error handling covers source failures, data quality issues, and delivery failures
- [ ] Distribution list and channels are confirmed with stakeholders
- [ ] Monitoring and alerting are configured
- [ ] Documentation enables another engineer to maintain the pipeline
- [ ] Rollback plan exists for failed runs

## Edge Cases

- **Reports with manual data entry**: Create a staging area (Google Form, shared sheet) for manual inputs; automate everything downstream
- **Reports requiring human approval**: Build an approval gate (email confirmation, Slack button) into the pipeline before distribution
- **Multi-timezone audiences**: Stagger delivery or generate timezone-specific versions with localized timestamps
- **Reports with variable structure**: Use templates with conditional sections; handle empty segments gracefully
- **Legacy source systems without APIs**: Use database replication, file drops (SFTP), or screen scraping as last resort; document fragility
- **Compliance-sensitive reports**: Add audit logging, access controls, and data masking; retain report snapshots for regulatory review
