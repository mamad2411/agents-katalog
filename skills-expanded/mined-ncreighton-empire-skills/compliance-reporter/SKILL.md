---
name: compliance-reporter
description: "Generate automated compliance reports with customizable templates and regulatory system integration. Use when the user needs SOX, GDPR, HIPAA, or industry-specific compliance documentation, audit trails, or regulatory submissions."
version: 1.0.0
homepage: https://github.com/ncreighton/empire-skills
metadata:
  {
    "openclaw": {
      "requires": {
        "env": ["COMPLIANCE_API_KEY", "REGULATORY_DB_URL"],
        "bins": []
      },
      "os": ["macos", "linux", "win32"],
      "files": ["SKILL.md"],
      "emoji": "📋"
    }
  }
---

## Overview

**Compliance Reporter** automates the generation of regulatory compliance reports with enterprise-grade accuracy and customization. This skill eliminates manual report compilation, reduces audit preparation time by 70%, and ensures consistent adherence to SOX, GDPR, HIPAA, PCI-DSS, and industry-specific frameworks.

### Why This Matters

Compliance reporting is time-intensive, error-prone, and increasingly scrutinized by regulators. Organizations waste 200+ hours annually on manual report generation. This skill:

- **Automates data aggregation** from multiple regulatory systems (Workiva, Domo, Tableau, custom APIs)
- **Generates audit-ready documentation** with timestamps, signatures, and evidence chains
- **Integrates with compliance platforms** (AuditBoard, Compliance.ai, Workiva Wdesk)
- **Produces templated outputs** for SOX 404, GDPR Article 32, HIPAA Risk Assessments, and custom frameworks
- **Exports to multiple formats** (PDF, Excel, JSON, XML) for regulatory submission

### Supported Integrations

- **Compliance Management:** AuditBoard, Workiva Wdesk, Compliance.ai, LogicGate
- **Data Sources:** Salesforce, ServiceNow, Jira, GitHub (for code audit trails)
- **Export Destinations:** Slack (notifications), Email (scheduled distribution), SharePoint (document storage)
- **Regulatory Systems:** SEC EDGAR, FDA eCopy, HIPAA OCR portal, GDPR DPA systems

---

## Quick Start

### Example 1: Generate SOX 404 Compliance Report

```
Generate a SOX 404 compliance report for Q4 2024 covering:
- Internal control assessment results from AuditBoard
- IT general controls from our ServiceNow CMDB
- Material weakness updates from the audit committee
- Evidence attachment index for all 47 control tests
Format as PDF with executive summary, detailed findings, and remediation timelines.
```

**What happens:** The skill queries your AuditBoard instance, compiles control test results, retrieves ServiceNow CMDB data, and generates a 50-80 page PDF with cross-referenced evidence links, ready for external auditor review.

---

### Example 2: GDPR Data Processing Agreement Report

```
Create a GDPR Article 32 compliance report for our cloud infrastructure:
- Data processing inventory from our data catalog (include: storage location, retention period, encryption method)
- Sub-processor list from our vendor management system
- Incident response procedures and 2024 breach log
- Data subject rights fulfillment metrics (access requests, deletion requests, portability requests)
Include risk assessment for cross-border transfers to US cloud services.
```

**What happens:** The skill aggregates your data catalog, vendor contracts, incident logs, and generates a comprehensive GDPR report with risk ratings, remediation recommendations, and sub-processor compliance matrix.

---

### Example 3: Automated Monthly Compliance Dashboard

```
Schedule a monthly compliance report that:
- Extracts control test results from Jira (filter: label="compliance-control")
- Pulls policy update audit trail from GitHub
- Retrieves user access reviews from Okta
- Compiles into a Slack summary every 1st of the month
- Generates detailed Excel workbook for compliance team
Include trend analysis vs. previous 3 months and flagged items requiring escalation.
```

**What happens:** The skill sets up a recurring automation that pulls data from multiple sources, analyzes trends, and delivers a compliance dashboard to your team on schedule.

---

## Capabilities

### 1. Multi-Framework Report Generation

Generate compliance reports for any regulatory framework:

- **Financial Services:** SOX 404, SOX 906, GLBA, NIST CSF
- **Healthcare:** HIPAA Risk Assessment, BAA compliance, OCR audit readiness
- **Data Privacy:** GDPR Article 32, CCPA, LGPD, UK DPA
- **Security:** ISO 27001, SOC 2 Type II, PCI-DSS, CIS Controls
- **Industry-Specific:** FDA 21 CFR Part 11, FINRA compliance, FCA rules

**Usage:** Specify the framework, reporting period, and scope; the skill auto-populates required sections and evidence requirements.

### 2. Automated Data Aggregation

Pull compliance data from disparate systems:

```
Aggregate compliance data from:
- AuditBoard (control test results, audit findings)
- Workiva Wdesk (SOX documentation, process narratives)
- ServiceNow (IT controls, change management log)
- Okta (user access reviews, MFA compliance)
- GitHub (code review audit trail, deployment logs)
- Slack (incident response communications)
Create a unified compliance database for cross-system analysis.
```

Supported connectors: REST APIs, SQL databases, CSV/Excel imports, PDF extraction (OCR), Salesforce, Workday, Tableau, Domo.

### 3. Customizable Report Templates

Build and reuse templated reports:

- **Pre-built templates:** 20+ industry-standard templates included
- **Custom templates:** Define your own sections, formatting, and auto-fill rules
- **Dynamic content:** Conditionally include sections based on scope, risk level, or regulatory requirement
- **Branding:** Add logos, headers, footers, and custom styling

**Example:** Create a "Monthly Risk Report" template that auto-pulls high-risk findings, calculates risk scores, and includes remediation timelines.

### 4. Evidence Management & Audit Trails

Link compliance findings to supporting evidence:

- Attach documents, screenshots, logs, and approval records
- Auto-generate evidence index with cross-references
- Track who accessed, modified, and approved each report
- Generate immutable audit trail for regulatory inspection
- Support digital signatures and timestamp verification

### 5. Regulatory Submission Integration

Export reports directly to regulatory portals:

- **SEC EDGAR:** Auto-format SOX 404 for SEC filing
- **FDA eCopy:** Generate 21 CFR Part 11 compliant documentation
- **HIPAA OCR:** Create risk assessment reports for OCR submission
- **GDPR DPA:** Submit Data Processing Agreements to data protection authorities
- **Email delivery:** Auto-send reports to regulators, auditors, and stakeholders

### 6. Compliance Trend Analysis

Track compliance metrics over time:

- Control effectiveness trends (% passing tests month-over-month)
- Remediation velocity (time to close findings)
- Risk scoring evolution
- Regulatory change impact analysis
- Benchmarking against industry standards

---

## Configuration

### Environment Variables (Required)

```bash
# Primary compliance API
COMPLIANCE_API_KEY=your-api-key-here
REGULATORY_DB_URL=https://your-compliance-db.com/api

# Optional: Third-party integrations
AUDITBOARD_API_KEY=auditboard-key
WORKIVA_TENANT_ID=workiva-tenant
OKTA_API_TOKEN=okta-token
GITHUB_API_TOKEN=github-token
SLACK_WEBHOOK_URL=https://hooks.slack.com/services/...
SALESFORCE_CLIENT_ID=sf-client-id
SALESFORCE_CLIENT_SECRET=sf-client-secret
```

### Setup Instructions

1. **Obtain API credentials** from your compliance platform (AuditBoard, Workiva, etc.)
2. **Set environment variables** in your ClawHub environment or `.env` file
3. **Test connectivity** with: `compliance-reporter --test-connection`
4. **Validate data sources** by running a sample report
5. **Configure templates** in the compliance dashboard

### Report Options

```yaml
Report Configuration:
  framework: "SOX 404"              # Framework type
  period: "Q4 2024"                 # Reporting period
  scope: ["IT", "Finance"]          # Functional areas
  include_evidence: true            # Attach supporting docs
  format: "PDF"                     # Output format: PDF, Excel, JSON, XML
  recipients: ["audit@company.com"] # Auto-send to stakeholders
  signature_required: true          # Digital signature
  retention_days: 2555              # Archive for 7 years
```

---

## Example Outputs

### Sample 1: SOX 404 Report Header

```
INTERNAL CONTROL ASSESSMENT REPORT
Fiscal Year Ended December 31, 2024

Management's Assessment of Internal Control Over Financial Reporting
Company: Acme Corporation
Reporting Date: March 15, 2025
Prepared by: Compliance Team
Reviewed by: Chief Compliance Officer

EXECUTIVE SUMMARY
- Total Controls Tested: 127
- Passing Controls: 124 (97.6%)
- Control Deficiencies: 2 (1.6%)
- Material Weaknesses: 0
- Overall Assessment: EFFECTIVE

CONTROL TESTING RESULTS BY FUNCTION
Finance:        25/25 passing (100%)
IT General:     48/50 passing (96%)
Sales:          31/32 passing (96.9%)
Operations:     20/20 passing (100%)
```

### Sample 2: GDPR Compliance Scorecard

```
GDPR COMPLIANCE SCORECARD - Q4 2024

Article 32 (Security): 94/100
  ✓ Encryption in transit: Implemented (AES-256)
  ✓ Encryption at rest: Implemented (AES-256)
  ✓ Access controls: Implemented (RBAC + MFA)
  ⚠ Incident response time: 2.5 hours (target: 1 hour)

Data Subject Rights: 98/100
  ✓ Access requests: 12 processed in avg. 8 days (30-day requirement)
  ✓ Deletion requests: 8 processed in avg. 5 days
  ✓ Portability requests: 3 processed in avg. 12 days
  ⚠ One request exceeded deadline by 2 days (remediated)

Sub-processor Compliance: 100/100
  ✓ All 23 sub-processors have current DPAs
  ✓ All DPAs include Article 28 clauses
  ✓ All sub-processors EU/US Privacy Shield certified
```

### Sample 3: Risk Assessment Matrix

```
RISK ASSESSMENT SUMMARY

HIGH RISK (Immediate Action Required):
  1. Legacy system without encryption (Finance DB)
     - Impact: High | Likelihood: Medium | Score: 8/10
     - Remediation: Upgrade to encrypted database (In progress, 60% complete)

MEDIUM RISK (Monitor & Plan):
  2. Backup retention policy not documented
     - Impact: Medium | Likelihood: Medium | Score: 5/10
     - Remediation: Document policy by Q1 2025

  3. Third-party vendor security assessment overdue
     - Impact: Medium | Likelihood: High | Score: 6/10
     - Remediation: Complete assessment by end of month

LOW RISK (Monitor):
  4. Policy review cycle needs optimization
     - Impact: Low | Likelihood: Low | Score: 2/10
     - Remediation: Schedule for annual review
```

---

## Tips & Best Practices

### 1. Automate Recurring Reports

Set up monthly/quarterly reports to run automatically:

```
Schedule compliance report:
- Frequency: Monthly on the 1st
- Framework: SOX 404
- Auto-send to: audit@company.com, cfo@company.com
- Archive location: SharePoint /Compliance/Reports
```

This eliminates manual report generation and ensures timely delivery to stakeholders.

### 2. Create a Compliance Data Hub

Centralize all compliance data in one place:

- Link all data sources (AuditBoard, ServiceNow, GitHub, etc.)
- Standardize data formats and naming conventions
- Create a single source of truth for audit evidence
- Reduce time spent hunting for documentation

### 3. Use Risk Scoring for Prioritization

Leverage the skill's risk scoring to prioritize remediation:

```
Generate risk prioritization report:
- Sort findings by risk score (descending)
- Filter by remediation difficulty
- Estimate remediation timeline
- Assign owners and due dates
```

Focus effort on high-impact, lower-effort fixes first.

### 4. Build Custom Templates for Your Industry

Don't use generic templates—customize for your business:

```
Create custom template "Quarterly Risk Report":
- Include your company's risk categories
- Auto-populate with your control framework
- Add branded headers and executive summary format
- Define required approvers and sign-off process
```

### 5. Integrate with Incident Management

Link compliance reports to incident tracking:

```
When generating compliance report:
- Pull open incidents from Jira
- Flag incidents related to control failures
- Include incident response timeline
- Show trend of incident closure rates
```

This connects compliance findings to operational reality.

### 6. Validate Data Quality Before Reporting

Always verify source data accuracy:

```
Run pre-report validation:
- Check for missing or stale data
- Validate data format consistency
- Flag outliers or anomalies
- Confirm data source connectivity
- Generate data quality score
```

A report is only as good as its underlying data.

---

## Safety & Guardrails

### What This Skill WILL NOT Do

⛔ **Does NOT guarantee regulatory compliance** — Reports are tools to support compliance efforts, not substitutes for legal/regulatory expertise. Always consult with compliance officers and legal counsel.

⛔ **Does NOT modify source systems** — The skill reads data only; it cannot alter control configurations, user access, or system settings. All changes must be made through proper change management.

⛔ **Does NOT provide legal advice** — Interpretations of regulatory requirements are informational only. Engage legal counsel for authoritative guidance.

⛔ **Does NOT replace auditor judgment** — External auditors make final determinations on control effectiveness. Reports support audit work but don't substitute for auditor testing.

⛔ **Does NOT guarantee data security** — While reports can be encrypted and signed, transmission security depends on your infrastructure. Use secure delivery methods (VPN, encrypted email, secure file sharing).

⛔ **Does NOT support real-time compliance monitoring** — Reports are point-in-time snapshots. For continuous monitoring, integrate with dedicated compliance monitoring tools.

### Data Privacy & Security Boundaries

- **Sensitive data handling:** Reports may contain PII, financial data, or trade secrets. Ensure proper access controls and encryption.
- **Data retention:** Configure retention policies per regulatory requirements (SOX = 7 years, GDPR = specific periods, etc.)
- **Audit logging:** All report access is logged; review audit trails regularly.
- **Export restrictions:** Some jurisdictions restrict cross-border data transfers; verify compliance before exporting.

### Limitations

- **Data source availability:** Reports require access to configured data sources; if sources are down, report generation fails
- **API rate limits:** Large reports may take 15-30 minutes if pulling from multiple APIs
- **Template complexity:** Highly customized templates may require technical support to configure
- **Regulatory changes:** Templates may need updates when regulations change; monitor regulatory updates regularly

---

## Troubleshooting

### Common Issues & Solutions

**Issue: "API Key Invalid" Error**

```
Error: COMPLIANCE_API_KEY not found or invalid
Solution:
1. Verify API key in environment variables: echo $COMPLIANCE_API_KEY
2. Confirm API key has not expired in your compliance platform
3. Check API key permissions (may need "reports:generate" scope)
4. Regenerate API key if necessary and update environment
5. Test connection: compliance-reporter --test-connection
```

**Issue: Data Source Connection Timeout**

```
Error: Failed to connect to AuditBoard (timeout after 30s)
Solution:
1. Verify network connectivity: ping auditboard-api.com
2. Check firewall rules (may need to whitelist IP range)
3. Confirm API endpoint URL is correct
4. Reduce report scope (fewer controls/time periods)
5. Contact AuditBoard support if endpoint is down
```

**Issue: Report Generation Takes Too Long**

```
Error: Report generation exceeded 30-minute timeout
Solution:
1. Reduce reporting scope (fewer functional areas or shorter period)
2. Exclude evidence attachments (include_evidence: false)
3. Split into multiple smaller reports
4. Run during off-peak hours (fewer API calls competing)
5. Upgrade to batch processing mode for large reports
```

**Issue: Missing Data in Report**

```
Error