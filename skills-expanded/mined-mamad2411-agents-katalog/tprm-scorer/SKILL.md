---
name: tprm-scorer
description: Calculates vendor risk scores using inherent and residual risk factors. Generates risk ratings, comparisons, and treatment recommendations.
allowed-tools: Read, Write
---

# TPRM Risk Scorer

Calculates and manages vendor risk scores.

## Capabilities

- **Risk Scoring**: Calculate inherent and residual risk
- **Rating Assignment**: Assign risk ratings (Critical/High/Medium/Low)
- **Trend Analysis**: Track risk score changes over time
- **Peer Comparison**: Compare vendors in same category

## Scoring Methodology

### Inherent Risk Factors (40%)

| Factor | Weight |
|--------|--------|
| Data Sensitivity | 15% |
| System Access Level | 10% |
| Business Criticality | 10% |
| Regulatory Impact | 5% |

### Control Risk Factors (60%)

| Factor | Weight |
|--------|--------|
| Security Certifications | 15% |
| Questionnaire Score | 20% |
| Audit Findings | 15% |
| Incident History | 10% |

## Risk Rating Thresholds

| Rating | Score Range | Review Frequency |
|--------|-------------|------------------|
| Critical | 80-100 | Quarterly |
| High | 60-79 | Semi-Annual |
| Medium | 40-59 | Annual |
| Low | 0-39 | Biennial |

## Output Formats

- Risk scorecard
- Rating justification
- Treatment recommendations
- Monitoring requirements
