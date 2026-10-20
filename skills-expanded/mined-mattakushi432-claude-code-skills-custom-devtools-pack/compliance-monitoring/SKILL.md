---
name: compliance-monitoring
description: "When to activate: compliance monitoring, continuous compliance, control monitoring, compliance dashboard, policy attestation, compliance calendar, third-party audit, KRI, KCI"
origin: zakr
metadata:
  namespace: zakr/devtools-pack
  version: 1.0.0
  category: business
  domain: compliance
  platforms: [claude-code, codex, gemini-cli, cursor, aider, windsurf]
---

# Compliance Monitoring

## Continuous Control Monitoring Framework

### Monitoring Levels
| Level | What | How | Frequency |
|-------|------|-----|-----------|
| Automated | Technical controls (patch status, MFA enforcement, encryption) | SIEM, CSPM, vulnerability scanners | Real-time / daily |
| Semi-automated | Process controls (access reviews completed, training done) | GRC platform, HRIS integration | Weekly / monthly |
| Manual | Judgment controls (policy adherence, vendor assessments) | Sampling, walkthroughs | Quarterly / annually |

### Control Monitoring Architecture
```
Data Sources → Monitoring Tools → GRC Platform → Dashboard → Alerts
─────────────────────────────────────────────────────────────────────
SIEM logs     →  Splunk/Sentinel →  ServiceNow  → KCI view  → Slack/email
CSPM scans    →  Wiz/Prisma      →  GRC         → Risk heat → PagerDuty
Vuln scanner  →  Tenable/Qualys  →  GRC         → map       → Jira tickets
HRIS data     →  Direct API      →  GRC         →           →
```

## Compliance Dashboard Design

### Dashboard Sections

**1. Overall Compliance Posture**
- Compliance score by framework (0-100%)
- Trend vs prior period (up/down with delta)
- Controls by status: Effective / Needs Attention / Failing / Not Tested

**2. Control Performance**
| Control domain | Total | Effective | At risk | Failing |
|---------------|-------|-----------|---------|---------|
| Access control | 24 | 22 | 1 | 1 |
| Change management | 12 | 11 | 1 | 0 |
| Vulnerability mgmt | 8 | 6 | 2 | 0 |
| Incident response | 10 | 10 | 0 | 0 |

**3. Exception Register Summary**
- Open exceptions by age (< 30 days / 30-90 days / > 90 days)
- Exceptions by severity (Critical / High / Medium / Low)
- Overdue remediation items

**4. Upcoming Compliance Activities**
- Access reviews due
- Policy attestations due
- Audit windows approaching
- Certification renewals

**5. Regulatory Deadlines**
- Breach notification windows (if active incidents)
- Filing deadlines
- Audit submission dates

## Exception Management Process

### Exception Lifecycle
```
Identified → Documented → Risk Accepted → Monitored → Remediated/Expired
```

### Exception Request Template
```
Exception ID: EXC-2024-047
Control: CC6.1 — MFA for all admin access
Exception: Legacy system X cannot support MFA due to vendor limitation
Business justification: Critical operational system; vendor roadmap: MFA in Q3
Risk level: High
Compensating controls:
  - Network-level access restriction (IP whitelist)
  - Session recording enabled
  - Access limited to 2 named administrators
  - Quarterly access review
Requested by: [Name], [Title]
Approved by: CISO
Valid until: [Date — max 12 months]
Review date: [Mid-point review date]
```

### Exception Approval Authority
| Risk level | Approval required |
|-----------|-----------------|
| Low | Control owner |
| Medium | Compliance team |
| High | CISO or equivalent |
| Critical | CISO + Legal + Executive sponsor |

### Exception Reporting
- All open exceptions in monthly compliance report
- Critical exceptions flagged to board/audit committee quarterly
- Exceptions approaching expiry: 30-day advance notification to owner

## Policy Attestation Workflow

### Annual Attestation Process
1. **Q4 prior year**: Review and update all policies
2. **January**: Distribute attestation to all covered employees
3. **Rolling 30 days**: Employees read and acknowledge each policy
4. **Day 30**: Send reminder to non-completers
5. **Day 45**: Escalate non-completers to managers
6. **Day 60**: Final escalation to HR for disciplinary follow-up
7. **End of cycle**: Report completion rates to leadership

### Attestation Coverage
| Policy | Audience | Frequency |
|--------|----------|-----------|
| Information Security Policy | All employees | Annual |
| Acceptable Use Policy | All employees | Annual |
| Data Classification Policy | All employees | Annual |
| Privacy Policy (internal) | All employees | Annual |
| Code of Conduct | All employees | Annual |
| Conflicts of Interest | Leadership + finance | Annual |
| PCI DSS (if applicable) | In-scope employees | Annual |

### Completion Targets
- Overall completion: ≥ 98% by 60-day deadline
- Manager-level and above: 100% required
- Non-completion = unacceptable for audit purposes; HR notified

## Compliance Calendar Template

### By Regulation

**GDPR / Data Protection**
| Month | Activity |
|-------|---------|
| January | Annual privacy notice review |
| March | DPA / controller-processor agreements review |
| June | Data subject request metrics review |
| September | DPIA review for new processing activities |
| November | Data breach register review |

**SOC 2**
| Timing | Activity |
|--------|---------|
| Ongoing | Evidence collection for audit period |
| Quarterly | Access reviews, VA scans |
| 60 days before audit | Gap assessment |
| 30 days before audit | Evidence packaging |
| Audit window | Auditor fieldwork support |

**ISO 27001**
| Timing | Activity |
|--------|---------|
| Annual | Internal audit |
| Annual | Risk assessment |
| Annual | Management review |
| Annual | Policy review and approval |
| Every 3 years | Certification audit (+ annual surveillance audits) |

## Automated vs Manual Control Testing

| Control type | Automated testing approach | Manual testing approach |
|-------------|--------------------------|------------------------|
| MFA enforcement | Query IdP — % accounts with MFA disabled | Sample access logs; verify manual bypass impossible |
| Patch currency | Pull patch scan results; flag > 30-day-old critical patches | Review sample of systems for patch evidence |
| Encryption at rest | CSPM scan for unencrypted storage | Review encryption configuration documentation |
| Access reviews | Track completion % from GRC platform | Verify sample of certifications have correct decisions |
| Incident response | Tabletop exercise results | Review incident log for response time vs SLA |
| Change management | Pull % of changes with approved tickets | Sample emergency changes for retroactive approval |

## Key Risk Indicators vs Key Control Indicators

### Key Risk Indicators (KRIs) — leading indicators of risk
| KRI | Threshold | Action |
|-----|-----------|--------|
| Open critical vulnerabilities > 30 days | > 5 | Escalate to CISO |
| Failed login attempts (anomalous spike) | > 3× baseline | Trigger investigation |
| Privilege escalation events unreviewed | > 0 | Immediate review |
| Employees without security training | > 5% | Escalate to HR |
| Critical vendor without SOC 2 | > 0 | Risk acceptance or remediation |

### Key Control Indicators (KCIs) — lagging indicators of control effectiveness
| KCI | Target | Alert threshold |
|-----|--------|----------------|
| MFA adoption rate | 100% | < 98% |
| Access review completion | 100% by deadline | < 95% at 30 days |
| Patch SLA compliance (critical) | 100% within 30 days | < 90% |
| Policy attestation completion | ≥ 98% | < 90% |
| Incident response time (P1) | < 1 hour | > 4 hours |

## Compliance Reporting

### Monthly Report — Internal
- Control effectiveness summary (% effective)
- Open exceptions and aging
- Incidents with compliance implications
- Upcoming deadlines

### Quarterly Report — Leadership
- Compliance posture vs prior quarter
- Key risks and mitigations
- Audit findings and remediation status
- Regulatory changes on horizon

### Annual Report — Board / Audit Committee
- Year-in-review: assessments completed, certifications maintained
- Material risks and how addressed
- Budget vs actuals for compliance program
- Roadmap for coming year

## Regulatory Change Management

1. **Monitor**: Subscribe to regulatory update feeds (IAPP, regulatory agency newsletters)
2. **Assess**: For each change, assess applicability and impact on current controls
3. **Gap analysis**: Identify control gaps created by new requirements
4. **Remediation plan**: Timeline and owner for each gap
5. **Update**: Revise policies, procedures, training to reflect changes
6. **Communicate**: Brief relevant teams and leadership on changes
7. **Document**: Record assessment and response for audit evidence
