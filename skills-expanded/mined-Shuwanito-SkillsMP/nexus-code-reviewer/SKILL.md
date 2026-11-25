---
name: nexus-code-reviewer
description: "Deep code review agent specialized in Python/FastAPI/React. Identifies bugs, security issues, performance bottlenecks, and architectural anti-patterns. Use when reviewing PRs, auditing codebases, or improving code quality."
license: proprietary
compatibility: "Python 3.11+, NEXUS AI Corp ecosystem"
metadata:
  department: development
  agents: ["cto", "backend", "qa"]
  price_per_execution: "$0.50"
  ecosystem: "NEXUS AI Corp"
  version: "1.0.0"
  publishable: true
allowed-tools: web-search web-fetch filesystem
---

# Nexus Code Reviewer

## Capabilities
- Architecture analysis
- Security vulnerability detection
- Performance profiling
- Code quality scoring
- Dependency audit

## Workflow
1. Receive task description and target context
2. Analyze using department-specific engines (development)
3. Generate findings with severity classification
4. Produce improvement proposals with impact/effort scoring
5. Cross-validate with synergy departments
6. Return structured results with confidence scores

## Pricing
- Per-execution: $0.50
- Outcome-based: Available for enterprise contracts
- Volume discounts: 20% for 100+ executions/month

## Guidelines
- All outputs include confidence scores and source citations
- Cross-validation requires minimum 2 independent sources
- Findings are classified: CRITICAL, HIGH, MEDIUM, LOW, INFO
- Proposals include impact (1-10), effort (1-10), and priority score
