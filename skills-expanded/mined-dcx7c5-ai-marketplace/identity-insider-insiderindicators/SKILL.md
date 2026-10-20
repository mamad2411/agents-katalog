---
name: identity-insider-insiderindicators
description: "Identity Insider Insiderindicators."
domain: cybersecurity
---

--|
| **Insider Threat** | Risk posed by individuals with legitimate access who misuse it for unauthorized purposes |
| **Data Exfiltration** | Unauthorized transfer of data outside the organization via email, USB, cloud, or other channels |
| **DLP** | Data Loss Prevention — technology monitoring and blocking unauthorized data transfers based on content policies |
| **Notice Period Monitoring** | Enhanced surveillance of departing employees during their resignation-to-departure window |
| **Chain of Custody** | Documented evidence handling procedures ensuring forensic integrity for potential legal proceedings |
| **Need-to-Know Violation** | Accessing information or systems beyond what is required for an employee's role or current tasks |

## Tools & Systems

- **Microsoft Purview (formerly DLP)**: Data classification and loss prevention platform monitoring endpoints, email, and cloud storage
- **Splunk UBA**: User behavior analytics detecting insider threat patterns through ML-based anomaly detection
- **Forcepoint Insider Threat**: Dedicated insider threat detection platform with behavioral indicators and risk scoring
- **DTEX InTERCEPT**: Endpoint-based insider threat detection focusing on user activity metadata collection
- **Code42 Incydr**: Data risk detection platform specializing in file exfiltration monitoring across endpoints and cloud

## Common Scenarios

- **Departing Employee**: Bulk download of customer lists and product roadmaps during two-week notice period
- **Disgruntled Employee**: After negative performance review, employee accesses executive salary data outside their role
- **Contractor Overreach**: External consultant accessing systems beyond contracted scope, downloading source code
- **Account Misuse**: Employee sharing credentials with unauthorized third party for competitive intelligence
- **Sabotage Indicator**: IT admin creating backdoor accounts and modifying system configurations before departure

## Output Format

```
INSIDER THREAT INVESTIGATION REPORT — IT-2024-0089
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Subject:      jsmith (Financial Analyst, Finance Dept)
Period:       2024-03-01 to 2024-03-15
Status:       Employee resigned 2024-03-15, last day 2024-03-29

Key Findings:
  [HIGH]  3,847 files downloaded from SharePoint (12.4 GB) — 10x peer average
  [HIGH]  USB device connected 14 times during notice period (0 times prior month)
  [HIGH]  187 emails with attachments sent to personal Gmail
  [MEDIUM] After-hours activity increased 340% during notice period
  [MEDIUM] Accessed HR salary database 3 times (not authorized for role)

Timeline:
  Mar 01-14:  Normal activity baseline (avg 150 events/day)
  Mar 15:     Resignation submitted (activity spike to 890 events)
  Mar 16-17:  Weekend access — 2,100 SharePoint downloads
  Mar 18:     USB device first connected, DLP alert triggered

Evidence Collected:   4 items (SHA-256 verified, chain of custody documented)
Recommendation:       Immediate access revocation recommended
                      Evidence package prepared for Legal review
```
