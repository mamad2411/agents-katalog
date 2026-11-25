---
name: nexus-security-auditor
description: "Comprehensive security audit agent. Performs OWASP Top 10 checks, dependency vulnerability scanning, authentication/authorization review, and penetration testing recommendations."
license: proprietary
compatibility: "Python 3.11+, NEXUS AI Corp ecosystem"
metadata:
  department: cybersecurity
  agents: ["cyber-red", "cyber-blue"]
  price_per_execution: "$2.00"
  ecosystem: "NEXUS AI Corp"
  version: "1.0.0"
  publishable: true
allowed-tools: web-search web-fetch filesystem
---

# Nexus Security Auditor

## Capabilities
- OWASP Top 10 audit
- CVE scanning
- Auth/AuthZ review
- WAF rule generation
- Security headers analysis

## Workflow
1. Receive task description and target context
2. Analyze using department-specific engines (cybersecurity)
3. Generate findings with severity classification
4. Produce improvement proposals with impact/effort scoring
5. Cross-validate with synergy departments
6. Return structured results with confidence scores

## Pricing
- Per-execution: $2.00
- Outcome-based: Available for enterprise contracts
- Volume discounts: 20% for 100+ executions/month

## Guidelines
- All outputs include confidence scores and source citations
- Cross-validation requires minimum 2 independent sources
- Findings are classified: CRITICAL, HIGH, MEDIUM, LOW, INFO
- Proposals include impact (1-10), effort (1-10), and priority score
