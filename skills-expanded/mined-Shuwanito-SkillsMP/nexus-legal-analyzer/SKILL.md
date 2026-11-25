---
name: nexus-legal-analyzer
description: "Legal analysis agent with RAG over Spanish, EU, and international law. Analyzes contracts, checks regulatory compliance, and monitors legislative changes."
license: proprietary
compatibility: "Python 3.11+, NEXUS AI Corp ecosystem"
metadata:
  department: legal
  agents: ["legal-rag", "legal-compliance"]
  price_per_execution: "$3.00"
  ecosystem: "NEXUS AI Corp"
  version: "1.0.0"
  publishable: true
allowed-tools: web-search web-fetch filesystem
---

# Nexus Legal Analyzer

## Capabilities
- Contract clause extraction
- Regulatory compliance check
- GDPR/EU AI Act analysis
- Jurisprudence search
- Risk assessment

## Workflow
1. Receive task description and target context
2. Analyze using department-specific engines (legal)
3. Generate findings with severity classification
4. Produce improvement proposals with impact/effort scoring
5. Cross-validate with synergy departments
6. Return structured results with confidence scores

## Pricing
- Per-execution: $3.00
- Outcome-based: Available for enterprise contracts
- Volume discounts: 20% for 100+ executions/month

## Guidelines
- All outputs include confidence scores and source citations
- Cross-validation requires minimum 2 independent sources
- Findings are classified: CRITICAL, HIGH, MEDIUM, LOW, INFO
- Proposals include impact (1-10), effort (1-10), and priority score
