# Zen Risk Engine Skill

How the false positive reduction and risk scoring system works.

## False Positive Engine

```python
from risk_engine.false_positive_engine import (
    FalsePositiveEngine,
    Vulnerability,
    ScanContext,
)

engine = FalsePositiveEngine()

# Assess a finding
finding = {
    "vuln_type": "reflected_xss",
    "param": "search",
    "url": "https://example.com/search?q=<script>alert(1)</script>",
    "technique": "polyglot",
    "confidence": 0.9,
}

result = engine.assess_finding(
    finding,
    ScanContext(
        target_domain="example.com",
        scan_phase="vulnerability_scan",
        tool_source="nuclei",
    ),
)

print(f"FP probability: {result.fp_probability}")  # 0.0–1.0
print(f"Decision: {result.decision}")  # TRUE_POSITIVE | FALSE_POSITIVE | INDETERMINATE
```

## Detection Models

The engine uses a multi-model voting system:
- Bayesian classifier: historical pattern matching
- WAF detection: checks if WAF modifies response (false positive indicator)
- Context analyzer: domain reputation, response similarity
- Parameter anomaly: checks if injection reflects server-generated

## Risk Scoring (CVSS v3.1)

```python
from risk_engine.cvss_scorer import CVSS31Scorer, CVSSVector

vector = CVSSVector(
    AV="N",
    AC="L",
    PR="N",
    UI="R",
    S="C",
    C="H",
    I="H",
    A="H",
)
scorer = CVSS31Scorer(vector)
print(scorer.score)  # 8.8 (HIGH)
print(scorer.severity)  # "HIGH"
```

## EPSS Integration

```python
from risk_engine.epss_client import EPPSScorer

epss = EPPSScorer()
prob = epss.get_exploit_probability("CVE-2025-12345")
print(f"Exploitation probability: {prob}")

# Combined risk
from risk_engine.composite_scorer import CompositeScorer

combined = CompositeScorer(cvss_vector, epss_prob, fp_probability)
# Returns RECOMMENDATION, PRIORITY_LEVEL, URGENT_ACTION_REQUIRED
```

## Workflow Integration

```python
# Via MCP
zen-agents_agent_run agent_type=analysis target=example.com \
  data='{"tool_outputs": [{"tool": "nuclei", "finding": "xss detected"}]}'

# The analysis agent will:
# 1. Score each finding via risk_engine
# 2. Filter false positives
# 3. Rank by combined CVSS + EPSS + FP score
# 4. Return actionable vulnerabilities only
```
