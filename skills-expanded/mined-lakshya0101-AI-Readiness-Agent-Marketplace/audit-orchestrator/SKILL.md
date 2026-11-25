---
name: audit-orchestrator
description: Coordinates multi-dimensional website AI readiness audits, validates findings, deduplicates issues, normalizes severities and priorities, and produces actionable evidence-backed audit reports.
---

# Audit Orchestrator Skill

The `audit-orchestrator` is the primary entrypoint for the Brand AI Readiness Agent Marketplace. It coordinates specialized audit skills across AI Discoverability and On-Site Engagement dimensions to produce a consolidated, evidence-backed audit report.

## Responsibilities

1. **Input Validation**: Validates and sanitizes target website URLs.
2. **Skill Coordination**: Dispatches audit requests to specialized skills (`ai-discoverability`, `engagement-audit`).
3. **Payload & Finding Validation**: Enforces strict finding contracts. Never hallucinates or fabricates evidence.
4. **Rating Normalization**: Normalizes severity levels (`critical`, `high`, `medium`, `low`) and derives evidence-backed action priorities.
5. **Conservative Deduplication**: Merges duplicate findings describing the same core defect while preserving distinct insights.
6. **Graceful Degradation**: Handles single-module failure without aborting the entire audit, recording explicit limitations in the final report.
7. **Report Generation**: Produces a structured JSON audit report and prioritized action plan.

## Input Contract

```json
{
  "site": "https://example.com"
}
```

See [input_schema.json](references/input_schema.json) for full schema details.

## Finding Contract

All specialized skills submit findings adhering to the standard finding contract:

```json
{
  "id": "DISC-001",
  "category": "ai_discoverability",
  "subcategory": "structured_data",
  "title": "Missing Schema.org Organization JSON-LD markup",
  "severity": "high",
  "evidence": "Audited https://example.com/ - No JSON-LD Organization script tags found.",
  "why_it_matters": "LLMs and crawlers cannot unambiguously resolve corporate identity or official brand URLs.",
  "suggested_action": {
    "summary": "Implement Schema.org Organization markup in JSON-LD",
    "details": "Embed JSON-LD on homepage declaring '@type': 'Organization', 'name', and 'url'.",
    "priority": "high"
  }
}
```

See [finding_schema.json](references/finding_schema.json) for complete property definitions.

## Output Contract

The orchestrator produces a structured audit report:

```json
{
  "site": "https://example.com",
  "audited_at": "2026-09-08T23:50:00Z",
  "summary": {
    "total_findings": 4,
    "critical": 0,
    "high": 2,
    "medium": 2,
    "low": 0
  },
  "findings": [...],
  "modules": { ... },
  "limitations": [...],
  "prioritized_action_plan": [...]
}
```

See [report_schema.json](references/report_schema.json) for schema details.

## Execution

Programmatic usage:
```python
import sys
from pathlib import Path

# Add skill scripts directory to sys.path
sys.path.insert(0, str(Path("skills/audit-orchestrator/scripts")))
from orchestrator import AuditOrchestrator

orchestrator = AuditOrchestrator()
report = orchestrator.run_audit("https://example.com")
print(report.to_dict())
```

CLI usage:
```bash
python skills/audit-orchestrator/scripts/orchestrator.py https://example.com --json
```
