---
name: cloud-gcp-forseti
description: "Cloud Gcp Forseti."
domain: cybersecurity
---

|
| Security Command Center | GCP-native security and risk management platform that provides asset inventory, vulnerability detection, and threat monitoring |
| Forseti Security | Open-source GCP security toolkit (now deprecated in favor of SCC) that provided inventory, scanning, enforcement, and notification capabilities |
| Cloud Asset Inventory | GCP service that provides a complete inventory of cloud resources with metadata, IAM policies, and org policy configurations |
| CIS GCP Foundations Benchmark | Security best practice guidelines from Center for Internet Security specific to Google Cloud Platform configuration |
| Uniform Bucket-Level Access | GCP storage setting that disables legacy ACLs and enforces access exclusively through IAM policies for consistent access control |
| Organization Policy | GCP constraint-based governance mechanism that restricts resource configurations across the organization hierarchy |

## Tools & Systems

- **Security Command Center**: GCP-native CSPM providing asset inventory, vulnerability findings, and compliance scoring
- **ScoutSuite**: Multi-cloud security auditing tool with comprehensive GCP checks for IAM, compute, storage, and networking
- **gcloud CLI**: Primary command-line interface for querying GCP resource configurations and security settings
- **Cloud Asset Inventory**: API for searching and exporting resource metadata and IAM policies across GCP projects
- **Forseti Security**: Legacy open-source GCP security toolkit, superseded by SCC but still referenced in compliance frameworks

## Common Scenarios

### Scenario: Assessing a Newly Acquired GCP Organization

**Context**: After a company acquisition, the security team needs to assess the security posture of the acquired company's GCP organization with 30+ projects.

**Approach**:
1. Enable Cloud Asset API and export full resource inventory to BigQuery for analysis
2. Run `gcloud asset search-all-iam-policies` to find all Owner/Editor bindings and public access grants
3. Audit firewall rules across all projects for overly permissive ingress from `0.0.0.0/0`
4. Check all storage buckets for public access using `gsutil iam get`
5. Run ScoutSuite for a comprehensive automated assessment with HTML report
6. Enable SCC and review all CRITICAL and HIGH findings
7. Generate a risk-prioritized remediation roadmap for the integration team

**Pitfalls**: GCP IAM bindings are inherited from organization to folder to project. A permissive binding at the organization level affects all downstream projects. Always audit IAM at every level of the hierarchy, not just at the project level.

## Output Format

```
GCP Security Assessment Report
=================================
Organization: acme-acquired-org (ORG_ID: 123456789)
Projects Assessed: 34
Assessment Date: 2026-02-23
Standards: CIS GCP Foundations 2.0

IAM FINDINGS:
  Users with Owner role at org level:       3
  Service accounts with Editor role:        12
  Resources with allUsers binding:           5
  Service account keys > 90 days:           18

NETWORK FINDINGS:
  Firewall rules allowing 0.0.0.0/0:       14
  SSH open to internet:                      7
  RDP open to internet:                      2
  Subnets without VPC flow logs:            22

STORAGE FINDINGS:
  Publicly accessible buckets:               5
  Buckets without CMEK encryption:          28
  Buckets without uniform access:           15

CRITICAL FINDINGS: 12
HIGH FINDINGS: 34
MEDIUM FINDINGS: 78
LOW FINDINGS: 145

TOP REMEDIATION PRIORITIES:
  1. Remove allUsers bindings from 5 storage buckets (CRITICAL)
  2. Restrict 0.0.0.0/0 firewall rules to specific CIDRs (HIGH)
  3. Rotate 18 service account keys older than 90 days (HIGH)
  4. Enable VPC flow logs on 22 subnets (MEDIUM)
```
